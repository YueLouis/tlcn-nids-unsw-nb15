"""Build the round-3 draft source from preserved round-2 text and audited CSVs."""
from pathlib import Path
import hashlib
import json
import shutil

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/report_cumulative"
PROJECT = ROOT / "docs/report_dot3_20261025"
PR = ROOT / "docs/evidence/dot_03/pr_scores_20261022"
OVERLAP = ROOT / "docs/evidence/dot_03/overlap_20261025"
FEATURES = ROOT / "docs/evidence/dot_03/features_20261025"


def pm(mean, std, percent=False):
    if pd.isna(mean):
        return "--"
    scale, digits = (100, 2) if percent else (1, 4)
    return f"${mean*scale:.{digits}f}\\pm{std*scale:.{digits}f}$" if pd.notna(std) else f"${mean*scale:.{digits}f}$"


def support(low, high):
    return f"{int(low):,}" if low == high else f"{int(low):,}--{int(high):,}"


def table(caption, header, columns, rows):
    return (r"\begingroup\small\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.18}" + "\n"
        + r"\begin{longtable}{" + columns + "}\n\\caption{" + caption + "}\\\\\n"
        + r"\toprule " + header + r"\\\midrule" + "\n\\endfirsthead\n"
        + r"\multicolumn{" + str(header.count("&")+1) + r"}{l}{\small Bảng \thetable\ (tiếp)}\\" + "\n"
        + r"\toprule " + header + r"\\\midrule" + "\n\\endhead\n"
        + "\n".join(" & ".join(row)+r"\\" for row in rows)
        + "\n" + r"\bottomrule\end{longtable}\endgroup" + "\n")


def prepare():
    pr_audit = json.loads((PR / "PR_SCORE_AUDIT.json").read_text(encoding="utf-8"))
    overlap_audit = json.loads((OVERLAP / "OVERLAP_AUDIT.json").read_text(encoding="utf-8"))
    if not (pr_audit["inputs_unchanged"] and overlap_audit["inputs_unchanged"] and overlap_audit["run_count"] == 80):
        raise ValueError("Diagnostics must pass before generating report")
    if not PROJECT.is_dir():
        raise ValueError("Create the dedicated round-3 LaTeX project first")
    for name in ("assets", "figures"):
        shutil.copytree(REPORT / name, PROJECT / name, dirs_exist_ok=True)
    for name in ("model_mechanisms.tex", "related_work_comparison.tex", "rq3_two_targets.tex"):
        shutil.copy2(REPORT / name, PROJECT / name)
    assets = PROJECT / "assets/dot3_20261025"
    assets.mkdir(parents=True, exist_ok=True)
    for folder in (PR, OVERLAP, FEATURES):
        for path in folder.glob("*.png"):
            shutil.copy2(path, assets / path.name)
    ap = pd.read_csv(PR / "AP_MEAN_STD.csv")
    summary = pd.read_csv(OVERLAP / "OVERLAP_MEAN_STD.csv")
    ap_rows = []
    for scenario in ("CS", "LR", "LD", "LE"):
        for model in ("RF", "XGB", "IF", "AE"):
            all_row = ap.query("scenario == @scenario and model == @model and scope == 'all'").iloc[0]
            held = ap.query("scenario == @scenario and model == @model and scope == 'normal_vs_heldout'")
            held_pm = pm(held.iloc[0].ap_mean, held.iloc[0].ap_std) if len(held) else "--"
            held_n = f"{int(held.iloc[0].support):,}" if len(held) else "--"
            prevalence = f"{100*held.iloc[0].prevalence:.2f}\\%" if len(held) else "--"
            ap_rows.append([scenario, model, pm(all_row.ap_mean,all_row.ap_std),held_pm,held_n,prevalence])
    ap_table = table("AP toàn test và Normal/held-out: mean và sample std, năm seed", "Scenario & Model & AP toàn test & AP Normal/held-out & Support slice & Tỷ lệ held-out", "L{1.25cm}L{1.05cm}L{3.0cm}L{3.0cm}L{2.2cm}L{2.3cm}", ap_rows)
    overlap_rows = []
    for scenario in ("CS", "LR", "LD", "LE"):
        for model in ("RF", "XGB", "IF", "AE"):
            for cohort in ("matched", "unmatched"):
                row = summary.query("scenario == @scenario and model == @model and cohort == @cohort and target_fpr == .05").iloc[0]
                overlap_rows.append([scenario, model, "Trùng" if cohort == "matched" else "Không trùng",
                    support(row.support_min,row.support_max), pm(row.fpr_mean,row.fpr_std,True),
                    pm(row.recall_mean,row.recall_std,True), pm(row.uadr_mean,row.uadr_std,True)])
    overlap_table = table("Nhóm trùng/không trùng với tập fit; target validation 5\\%; chỉ số theo \\%, std theo điểm phần trăm", "Sc. & Model & Nhóm & Support min--max & FPR & Recall Attack & UADR", "L{0.65cm}L{1.25cm}L{1.45cm}L{2.35cm}L{2.4cm}L{2.45cm}L{2.45cm}", overlap_rows)
    role_rows = []
    for scenario in ("CS", "LR", "LD", "LE"):
        for model in ("RF", "IF"):
            row = summary.query("scenario == @scenario and model == @model and cohort == 'matched' and target_fpr == .05").iloc[0]
            role_rows.append([scenario, "RF/XGB" if model == "RF" else "IF/AE", support(row.normal_min,row.normal_max),
                             support(row.known_min,row.known_max),support(row.heldout_min,row.heldout_max)])
    role_table=table("Support nhóm matched theo vai trò; min--max qua năm seed", "Scenario & Phạm vi fit & Normal & Known Attack & Held-out Attack", "L{1.3cm}L{2.1cm}L{3.4cm}L{3.4cm}L{3.4cm}",role_rows)
    fi = pd.read_csv(FEATURES / "FEATURE_IMPORTANCE_MEAN_STD.csv")
    fi_rows = []
    for scenario in ("CS", "LR"):
        for model in ("RF", "XGB"):
            part = fi.query("scenario == @scenario and model == @model").nlargest(3, "importance_mean")
            top = "; ".join(f"{row.feature} ({row.importance_mean:.3f})" for row in part.itertuples())
            fi_rows.append([scenario, model, top.replace("_", r"\_")])
    fi_table = table("Ba feature có importance trung bình cao nhất; mô tả theo 5 seed", "Scenario & Model & Ba feature đứng đầu (importance mean)", "L{1.3cm}L{1.2cm}L{11.3cm}", fi_rows)
    chapter = r"""
\chapter{PHÂN TÍCH BỔ SUNG ĐỢT 3 -- BẢN NHÁP}
\label{chap:dot3}
\section{Phạm vi và trạng thái ngày 25/10/2026}
Chương này bổ sung phân tích hậu nghiệm trên 80 run đã hoàn thành ở đợt 2. Không huấn luyện lại baseline, không chọn lại ngưỡng trên test và không thay official split. Bảng, hình và bản thảo do công cụ hỗ trợ chuẩn bị để nhóm kiểm lại; chưa tính là bài bàn giao hay xác nhận đóng góp của từng thành viên. Theo nhóm trưởng ngày 25/10, Anh và Thu chưa gửi bài; phần nhận xét riêng, đối chiếu nguồn và đọc chéo vẫn chờ thực hiện. Hạn báo cáo 09/11 đã thống nhất với giảng viên theo xác nhận của nhóm trưởng.

\section{Precision--Recall và phân bố score}
Mỗi record có hai dòng prediction cho target validation 1\% và 5\%, nhưng score giống nhau. AP chỉ dùng một bản sao mỗi record/run: tổng 13.173.120 dòng đã đọc tương ứng 6.586.560 cặp record/run. Hàm \texttt{average\_precision\_score} được dùng, khác diện tích hình thang của đường PR. Có 1.040 metric gốc được đối chiếu; hash đầu vào không đổi. Dữ liệu số thực CSV được đọc theo round-trip để giữ thứ tự score gần bằng nhau.

Các đường minh họa dùng seed 42 đã định trước; các bảng dùng đủ năm seed. AP toàn test có support 82.332 và tỷ lệ Attack 55,06\%. Scope Normal/held-out loại known Attack; tỷ lệ dương lần lượt 8,63\% ở LR, 9,95\% ở LD và 23,13\% ở LE. Vì support, prevalence và thành phần Attack khác nhau, không so AP trực tiếp giữa các scope/scenario để kết luận mô hình tốt hơn.
AP_TABLE

Ở LR, AP toàn test của RF/XGB xấp xỉ 0,9852, trong khi AP Normal/held-out là 0,7077/0,6623. IF có AP toàn test 0,8214 nhưng AP Normal/held-out 0,0905, gần tỷ lệ dương 0,0863; đây là mô tả khả năng xếp hạng trong slice, không thay UADR tại ngưỡng đã khóa. Known Attack có thể che mức khó của lớp held-out khi chỉ đọc AP toàn test.

\begin{figure}[H]\centering
\includegraphics[width=.90\textwidth]{assets/dot3_20261025/PR_LR_normal_vs_heldout_S42.png}
\caption{PR ở LOACO Reconnaissance, chỉ Normal và held-out; seed 42 minh họa. Chấm/trục dùng ngưỡng validation có sẵn, không dùng đường test chọn lại ngưỡng.}
\end{figure}

\begin{figure}[H]\centering
\includegraphics[width=.95\textwidth]{assets/dot3_20261025/SCORE_ECDF_LR_S42.png}
\caption{ECDF score theo Normal/known/held-out và hai threshold, LR seed 42. Score khác thang giữa các mô hình; hình mô tả mức chồng lấn, chưa chứng minh nguyên nhân lỗi.}
\end{figure}

\section{Độ nhạy mô tả theo feature overlap}
Đặc tả đã ghi trước khi chạy ở \path{docs/management/DAC_TA_OVERLAP_DOT_03_20261025.md}. Mẫu test thuộc nhóm \textit{matched} khi 42 feature raw bằng một vector trong tập model thực sự được fit, không dùng id/label/attack\_cat làm key. Khử key trùng phía fit để mỗi record test chỉ đếm một lần. Nhóm còn lại là \textit{unmatched}. Match không phải cùng sự kiện mạng hoặc cùng nhãn.

Với từng seed/scenario, pipeline tái dựng chia development bằng stratify attack\_cat, loại held-out trước chia. RF/XGB fit toàn development train; IF/AE chỉ fit Normal. Phạm vi fit được kiểm bằng fingerprint cấu hình/dữ liệu, ID partition trong audit lịch sử, số dòng và mean/variance scaler trong bundle đã lưu. Đây là tái dựng có kiểm chứng, không phải nhật ký từng row fit được ghi trực tiếp khi huấn luyện.

Hai nhóm giữ nguyên score, threshold và prediction. Tổng support và TP/FP/TN/FN hai nhóm bằng toàn test ở mỗi run/target; 1.040 metric gốc tiếp tục khớp. Khi không có mẫu số, bảng ghi --; CSV giữ NaN và số seed hợp lệ. AP của nhóm chỉ có một nhãn cũng ghi thiếu, không diễn giải là AP=0. RF/XGB dùng cùng phạm vi fit, IF/AE cùng Normal-only; nhóm matched khác nhau giữa hai họ và có thể khác theo seed.
ROLE_TABLE
OVERLAP_TABLE

\begin{figure}[H]\centering
\includegraphics[width=\textwidth]{assets/dot3_20261025/OVERLAP_SLICES.png}
\caption{Ba lát cắt tại target validation 5\%; mean/sample std qua năm seed. Nhóm matched/unmatched thay đổi theo model và seed; xem support trước khi so sánh.}
\end{figure}

\textbf{Giới hạn diễn giải:} đây là liên hệ mô tả giữa hai nhóm của test đang có, không phải thí nghiệm huấn luyện loại overlap. Nhãn, loại tấn công và độ khó có thể khác; chênh lệch metric không chứng minh overlap gây tăng/giảm hiệu quả. Không xem nhóm unmatched là test mới độc lập hoặc so trực tiếp các nhóm khác nhau để xếp hạng mô hình. Năm seed cùng dùng official test; sample std không phải khoảng tin cậy. Chưa thực hiện retrain loại trùng hay kiểm trên dữ liệu vận hành.

\section{Importance của feature: gợi ý đọc, chưa phải nguyên nhân lỗi}
Đã trích importance trong bundle RF/XGB cho 40 run (4 scenario, 2 model, 5 seed), gom contribution của one-hot về 42 feature raw. RF dùng mean decrease in impurity; XGB dùng normalized gain. Đây là mô tả mô hình đã fit, không phải permutation importance trên test và không cho biết feature gây ra từng FP/FN. Categorical feature có thể chịu thiên lệch do số mức.
FI_TABLE

\begin{figure}[H]\centering
\includegraphics[width=.92\textwidth]{assets/dot3_20261025/FEATURES_CS.png}
\caption{Mười feature đứng đầu ở closed-set; mean/sample std qua năm seed. RF và XGB dùng định nghĩa importance khác nhau.}
\end{figure}
\begin{figure}[H]\centering
\includegraphics[width=.92\textwidth]{assets/dot3_20261025/FEATURES_LR.png}
\caption{Mười feature đứng đầu ở LOACO Reconnaissance; mô tả feature quan trọng trong mô hình, chưa là giải thích nhân quả.}
\end{figure}

\input{final_diagnostics.tex}

\section{Phần nhóm cần đọc và kiểm tiếp}
Anh đối chiếu bảng dữ liệu/support với nguồn và viết giới hạn bằng lời của mình. Thu tự truy vết RF và IF, closed-set seed 42, target validation 5\%: một FP và một FN mỗi model; sau đó nhận xét bảng/hình có support, threshold và nguồn. Tín tự chạy/kiểm một run, ghi phần được công cụ hỗ trợ và ghép nội dung đã nhận. Feature importance RF/XGB, kiểm thêm nhóm proto/service/state và nguồn S07 toàn văn chưa được coi là đã xong.

Nhóm làm online trước, trao đổi file/bản đang làm qua Zalo; buổi ra quán hẹn khi cả ba rảnh, chưa ấn định ngày. Trước khi nộp, cả ba cần đọc PDF và ghi góp ý, đóng góp, mức hiểu thực tế. Các mốc nhỏ là lịch đề xuất; việc biên dịch PDF không thay việc review nhóm.

\section{Bằng chứng và kiểm kỹ thuật}
CSV gốc của chương: \path{docs/evidence/dot_03/pr_scores_20261022/} và \path{docs/evidence/dot_03/overlap_20261025/}; audit kèm hash, phiên bản, 80 run và kiểm đầu vào. Bảng overlap đủ 480 dòng run/target/cohort, 96 nhóm tổng hợp; mỗi nhóm có năm seed. CSV đầy đủ giữ cả target 1\% và 5\%, AP và support các vai trò.

Bộ kiểm ngày 25/10 có 33 test đạt: 17 test nền, 9 test PR/score và 7 test overlap. Test mới kiểm khác biệt Normal-only/toàn train, key validation không thuộc fit, key feature không dùng nhãn, không nhân support do duplicate, không làm tròn khi match, mẫu số rỗng và đối chiếu ID/vai trò. Log tại \path{docs/evidence/dot_03/session_20261025/tests.log}. Kiểm thử không xác nhận thay việc hiểu bài hay phê duyệt của giảng viên.
"""
    chapter=chapter.replace("OVERLAP_TABLE",overlap_table).replace("AP_TABLE",ap_table).replace("ROLE_TABLE",role_table).replace("FI_TABLE",fi_table)
    if overlap_table not in chapter or ap_table not in chapter or chapter.count("CS & RF & Trùng &") != 1:
        raise ValueError("Report table substitution/coverage mismatch")
    chapter=chapter.replace("Feature importance RF/XGB, kiểm thêm nhóm proto/service/state và nguồn S07 toàn văn chưa được coi là đã xong.", "Importance RF/XGB và lát cắt proto/service/state đã có ở mức mô tả; từng bạn cần tự kiểm và giải thích. Nguồn S07 toàn văn chưa có; chỉ dùng phạm vi abstract đã đối chiếu.")
    (PROJECT / "dot3_analysis_20261025.tex").write_text(chapter,encoding="utf-8")
    source=REPORT / "BAO_CAO_TLCN_TICH_LUY_DOT_02.tex"
    text=source.read_text(encoding="utf-8")
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    for old,new in (("Tích lũy đợt 2}","Tích lũy đợt 3 - Bản nháp}"),
                    ("Bản tích lũy đợt 2}","Bản tích lũy đợt 3 - Nháp}"),
                    ("BẢN TÍCH LŨY - ĐỢT 2","BẢN TÍCH LŨY - ĐỢT 3 (NHÁP)"),
                    ("14/09/2026 - 11/10/2026", "17/08/2026 - 25/10/2026 (bản nháp)"),
                    (r"\textbf{Ngày cập nhật bản nộp:} & 17/10/2026",r"\textbf{Ngày cập nhật bản nháp:} & 25/10/2026")):
        text=text.replace(old,new)
    start=text.index("Loại tài liệu &")
    end=text.index(r"\bottomrule\end{tabularx}\endgroup",start)
    text=text[:start]+r"""Loại tài liệu & Báo cáo tích lũy đợt 3 -- BẢN NHÁP; kế thừa nội dung đợt 1--2, bổ sung phân tích PR/score và feature overlap.\\
Đợt báo cáo & Đợt 3; hạn 09/11/2026 đã được nhóm trưởng xác nhận thống nhất với giảng viên.\\
Nền thực nghiệm & 80 run và 320 artifact gốc giữ nguyên; ngưỡng validation 1\%/5\% không thay đổi.\\
Phân tích bổ sung & PR/score: audit ngày 22/10; overlap trên tập fit thực tế: 25/10; đều hậu nghiệm trên kết quả đã lưu.\\
Kiểm kỹ thuật & 33 test đạt ngày 25/10; CSV/audit dùng để đối chiếu; bản nháp còn chờ review nội dung.\\
Trạng thái nhóm & Theo Tín ngày 25/10, Anh và Thu chưa gửi bài. Bản thảo do công cụ hỗ trợ, chưa xác nhận đóng góp, mức hiểu hay phê duyệt nội dung.\\
"""+text[end:]
    text=text.replace("Đợt 3 & 08/11/2026 & 09/11 là mốc nội bộ dự kiến.",
                      "Đợt 3 & 08/11/2026 & 09/11 đã thống nhất với giảng viên theo nhóm trưởng xác nhận.")
    a=text.index(r"\chapter*{TÓM TẮT TIẾN ĐỘ}")
    b=text.index(r"\clearpage\pagenumbering{arabic}",a)
    text=text[:a]+r"""\chapter*{TÓM TẮT TIẾN ĐỘ}
\addcontentsline{toc}{chapter}{TÓM TẮT TIẾN ĐỘ}
Bản nháp ngày 25/10 kế thừa pipeline, 80 run và kết quả đợt 2; bổ sung PR/score và phân tích matched/unmatched theo tập model thực sự được fit. Các chương nền và bảng tiến độ đợt 2 giữ ngày đối chiếu lịch sử của chúng; phần cập nhật ở Chương~\ref{chap:dot3}.

Kết quả AP toàn test cao không bảo đảm xếp hạng tốt riêng lớp held-out: LR có AP toàn test RF/XGB khoảng 0,9852 nhưng AP Normal/held-out là 0,7077/0,6623. Chênh lệch metric giữa matched/unmatched được mô tả kèm support, không coi là tác động nhân quả của overlap hoặc đánh giá test mới.

Đây là tài liệu nền có hỗ trợ công cụ. Anh và Thu chưa gửi bài theo nhóm trưởng xác nhận ngày 25/10; phần viết riêng, kiểm nguồn, tự giải thích và đọc chéo còn chờ thực hiện. Bản nháp chưa được nhóm duyệt để nộp. Hạn báo cáo 09/11 đã thống nhất với giảng viên theo xác nhận của nhóm trưởng.

"""+text[b:]
    text=text.replace(r"\chapter{KẾT LUẬN VÀ GIỚI HẠN CỦA ĐỢT 2}",
        r"\chapter{KẾT LUẬN VÀ GIỚI HẠN CỦA ĐỢT 2}"+"\n"+r"\noindent\textit{Mục này giữ kết luận lịch sử đợt 2. Các phân tích mới và giới hạn đã cập nhật ở Chương~\ref{chap:dot3}.}\par")
    text=text.replace(r"\begingroup\small\setstretch{1.1}\begin{thebibliography}{99}",
        "\\input{dot3_analysis_20261025.tex}\n\\clearpage\n"+r"\begingroup\small\setstretch{1.1}\begin{thebibliography}{99}")
    # The status section must not suggest the unconfirmed 18/10 meeting is still upcoming.
    a=text.index("Tại ngày 17/10/2026, bản hiện tại đang chờ nhóm rà soát;")
    b=text.index(r"\chapter{DỮ LIỆU VÀ DATA CONTRACT}",a)
    text=text[:a]+r"""Ở bản đợt 2 ngày 17/10, nhóm còn chờ rà soát; các ghi nhận đồng ý cũ được lưu là lịch sử. Cập nhật ngày 25/10 theo nhóm trưởng: Anh và Thu chưa bàn giao bài đợt 3. Chưa có xác nhận đọc chéo, mức hiểu hay đóng góp mới để đóng Gate 1/Gate 2 nội dung. Phân tích và kiểm kỹ thuật do công cụ hỗ trợ không thay tự đọc, giải thích và đối chiếu đóng góp của từng bạn.

"""+text[b:]
    target=PROJECT / "main.tex"
    target.write_text(text,encoding="utf-8")
    if hashlib.sha256(source.read_bytes()).hexdigest()!=source_hash:
        raise ValueError("Original round-2 source changed")
    print(target)
    print("Round-3 chapter and 12 diagnostic figures prepared; round-2 source preserved.")


if __name__ == "__main__":
    prepare()
