"""Assemble current draft reports for rounds 3/4 and the whole thesis."""
from pathlib import Path
import json
import shutil
import re

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
R3=DOCS/'report_dot3_20261025'


def prepare():
    demo=DOCS/'evidence/dot_04/demo_20261025'
    audit=json.loads((demo/'DEMO_AUDIT.json').read_text(encoding='utf-8'))
    if audit['operating_cases']!=32 or not audit['inputs_unchanged']: raise ValueError('Demo not verified')
    # Update narrative to reflect the latest direct instruction: prepare all content now, review later.
    chapter=(R3/'dot3_analysis_20261025.tex').read_text(encoding='utf-8')
    chapter=chapter.replace('Theo nhóm trưởng ngày 25/10, Anh và Thu chưa gửi bài; phần nhận xét riêng, đối chiếu nguồn và đọc chéo vẫn chờ thực hiện.',
        'Theo thống nhất mới qua nhóm trưởng ngày 25/10, công cụ hỗ trợ chuẩn bị đầy đủ nội dung và báo cáo trước, sau đó cả ba đọc, kiểm và sửa từng phần. Chưa có bài bàn giao độc lập của Anh và Thu; bản chuẩn bị chung không xác nhận đóng góp hay mức hiểu của từng người.')
    chapter=chapter.replace('Bộ kiểm ngày 25/10 có 33 test đạt: 17 test nền, 9 test PR/score và 7 test overlap.',
        'Bộ kiểm ngày 25/10 có 42 test đạt: 17 test nền, 9 test PR/score, 7 test overlap, 8 test demo và 1 test mẫu số lát cắt lỗi.')
    chapter=chapter.replace('session_20261025/tests.log','session_20261025/tests_completion.log')
    chapter=chapter.replace('Chương này bổ sung phân tích hậu nghiệm', 'Chương này bổ sung phân tích hậu nghiệm')
    chapter=chapter.replace('Ba lát cắt tại target validation 5\\%; mean/sample std qua năm seed. Nhóm matched/unmatched thay đổi theo model và seed; xem support trước khi so sánh.',
        'Ba lát cắt tại target validation 5\\%; mean/sample std qua năm seed. IF/AE không có held-out matched nên UADR matched không xác định, không phải 0. Nhóm thay đổi theo model/seed; xem support trước khi so sánh.')
    insert=r"""
Ví dụ LR/RF, target validation 5\%: nhóm held-out unmatched có 3.249--3.266 mẫu qua năm seed, UADR $97.56\%\pm0.32$ điểm phần trăm. Nhóm matched có 230--247 held-out. Kết quả cao còn hiện diện ngoài exact feature match; tuy nhiên không loại trừ các tương đồng khác của official split hoặc chứng minh tác động nhân quả. IF/AE không có held-out matched trong ba LOACO, nên UADR ở nhóm này không xác định.

"""
    chapter=chapter.replace(insert,'')
    chapter=chapter.replace(r'\textbf{Giới hạn diễn giải:}',insert+r'\textbf{Giới hạn diễn giải:}')
    chapter=chapter.replace('Trạng thái ngày 25/10/2026','Trạng thái ngày 25/10/2026')
    chapter=chapter.replace('Scenario &','Sc. &')
    (R3/'dot3_analysis_20261025.tex').write_text(chapter,encoding='utf-8')
    base=(R3/'main.tex').read_text(encoding='utf-8')
    base=base.replace('33 test đạt ngày 25/10','42 test đạt ngày 25/10')
    base=base.replace('Theo Tín ngày 25/10, Anh và Thu chưa gửi bài. Bản thảo do công cụ hỗ trợ, chưa xác nhận đóng góp, mức hiểu hay phê duyệt nội dung.',
        'Nhóm thống nhất qua Tín ngày 25/10: chuẩn bị trọn bộ trước để cả ba đọc/sửa dần. Bản nháp chưa được nhóm duyệt để nộp.')
    base=base.replace('Đây là tài liệu nền có hỗ trợ công cụ. Anh và Thu chưa gửi bài theo nhóm trưởng xác nhận ngày 25/10; phần viết riêng, kiểm nguồn, tự giải thích và đọc chéo còn chờ thực hiện.',
        'Theo thống nhất mới ngày 25/10, tài liệu được chuẩn bị đầy đủ với công cụ hỗ trợ để cả ba đọc/sửa dần; đóng góp và mức hiểu được ghi sau khi các bạn thực sự kiểm và góp ý.')
    (R3/'main.tex').write_text(base,encoding='utf-8')
    sample=DOCS/'evidence/dot_02/category_errors_20261014/ERROR_EXAMPLES_CS_S42.csv'
    examples=pd.read_csv(sample,float_precision='round_trip')
    chosen=examples[examples.run_id.isin(['CS-RF-S42','CS-IF-S42'])].sort_values('record_id').groupby(['run_id','error_type']).head(1)
    error_rows='\n'.join(f"{r.run_id} & {int(r.record_id)} & {r.error_type} & {r.attack_cat} & {r.score:.6f} & {r.threshold:.6f}"+r'\\' for r in chosen.itertuples())
    demo_chapter=r"""
\chapter{PROTOTYPE CSV VÀ KIỂM CHỨNG SUY LUẬN}\label{chap:demo}
\section{Mục tiêu, đầu vào và luồng sử dụng}
Prototype giúp cả nhóm mở một CSV UNSW-NB15-compatible, chọn một trong bốn scenario và bốn model, chọn target validation 1\%/5\%, rồi đọc score, threshold và dự đoán. Dùng bundle seed 42 đã lưu; không fit lại preprocessing/model hoặc chọn lại ngưỡng. Đây là minh họa suy luận CSV, không phải cảm biến bắt gói hoặc hệ thống ngăn chặn xâm nhập vận hành.

Giao diện chạy tại \url{http://127.0.0.1:4397}. File \path{demo/MO_DEMO.ps1} mở server local ẩn rồi mở trình duyệt; hoặc chạy \path{scripts/demo_server.py}. Mọi xử lý ở máy local. Chọn ``Dùng 100 dòng mẫu'' rồi ``Chạy mô hình''; đổi model/scenario để thấy cùng mẫu có thể nhận score và dự đoán khác nhau. Bảng có FP/FN khi CSV kèm nhãn thật; nhãn không đi vào feature.

Nút ``So sánh cả 4 mô hình'' xử lý cùng CSV, scenario, target và seed 42 qua RF/XGB/IF/AE. Bốn thẻ ghi số Attack/Normal, threshold riêng và FP/FN nếu có nhãn; CSV không nhãn không tự tạo FP/FN. Score khác thang nên không xếp hạng model bằng độ lớn score.

Phần ``Cách đọc model này'' hiển thị năm feature importance cao nhất của RF/XGB trong bundle, gom one-hot về feature raw. Đây là importance toàn model (RF impurity, XGB gain), không phải nguyên nhân dự đoán từng dòng. IF giải thích score bằng âm decision function; AE dùng mean reconstruction MSE. Không gắn importance của cây sang IF/AE.

Mẫu gồm 10 ID nhỏ nhất của mỗi nhóm trong 10 category, chọn theo quy tắc trước khi suy luận, tổng 100 dòng. Có chủ ý để đọc luồng và xem đủ nhóm, không phải mẫu ngẫu nhiên đại diện; không dùng tỷ lệ đúng trên mẫu này thay metric toàn test. Metadata id/label/attack\_cat chỉ phục vụ đối chiếu, đầu vào model đúng 42 feature.

\section{Luồng xử lý và các tình huống}
Server kiểm schema và số dòng 1--1.000, kiểm dữ liệu số/categorical, biến đổi bằng preprocessor đã lưu, tính score bằng adapter tương ứng, lấy ngưỡng validation trong bundle và so sánh score $\geq$ threshold. Kết quả cho biết run ID, seed, target, score, threshold, dự đoán, nhãn thật và TP/FP/TN/FN nếu có. Người xem có thể tải kết quả CSV.

CSV thiếu feature, số không đọc được, NaN/vô cực và file rỗng bị từ chối bằng thông báo; chỉ chọn bundle trong danh sách scenario/model. CSV không có nhãn vẫn được suy luận và ghi ``Chưa có'' ở cột đối chiếu; không tự gán nhãn thật từ dự đoán. Thư viện và các bundle cần có trên máy chạy. Ngưỡng 1\%/5\% là mục tiêu trên Normal validation, không bảo đảm cùng FPR trên test.

\begin{figure}[H]\centering
\includegraphics[width=\textwidth]{assets/demo_20261025/DEMO_DESKTOP.png}
\caption{Giao diện demo sau khi chạy dữ liệu mẫu bằng RF closed-set, seed 42. Bảng hiển thị score, ngưỡng và nhãn đối chiếu.}
\end{figure}

\begin{figure}[H]\centering
\includegraphics[width=\textwidth]{assets/demo_20261025/DEMO_COMPARISON.png}
\caption{Cùng CSV mẫu qua bốn model, CS seed 42, target validation 5\%. Tỷ lệ trên mẫu minh họa không thay metric toàn test.}
\end{figure}

\section{Kiểm chứng bằng bundle thật}
Đã chạy lại suy luận 16 bundle seed 42 (4 scenario $\times$ 4 model), mỗi bundle ở hai ngưỡng: 32 trường hợp $\times$ 100 dòng = 3.200 so sánh dự đoán. Toàn bộ nhãn dự đoán và ngưỡng khớp prediction đã khóa. Sai khác score lớn nhất $2.20\times10^{-7}$, dưới dung sai $10^{-6}$, ghi rõ trong audit; không coi score là giống từng byte. Kiểm thêm bốn trường hợp lỗi: thiếu feature, rỗng, số không hợp lệ và vô cực; đều bị từ chối. Bundle và prediction gốc không đổi.

Kiểm giao diện: dùng mẫu/chạy RF, đổi LR/IF/target 1\%, so sánh bốn model, explanation, tải CSV, CSV không nhãn/không hợp lệ và năm độ rộng màn hình. Bằng chứng tại \path{docs/evidence/dot_04/demo_20261025/}. Test suy luận xác nhận metadata không vào model, nhãn thật không thay score, trường hợp score bằng ngưỡng thành Attack và các đầu vào không hợp lệ bị từ chối. Đây là kiểm kỹ thuật đã thực hiện; nhóm vẫn cần tự chạy và giải thích khi trình bày.

\section{Bốn ví dụ để cả nhóm tập giải thích}
Các dòng dưới đây lấy ID nhỏ nhất của từng nhóm FP/FN trong RF/IF closed-set seed42, target validation 5\%; chọn để mở lại dễ dàng, không đại diện mọi lỗi. Mỗi người đọc nhãn thật, score, ngưỡng rồi tự nói vì sao là FP/FN. Feature importance không đủ để kết luận nguyên nhân từng dòng.
\begin{table}[H]\centering\small
\caption{Ví dụ score/ngưỡng và lỗi từ prediction thật}
\begin{tabular}{L{2.7cm}L{.7cm}L{.7cm}L{3cm}rr}\toprule Run & ID & Lỗi & Nhóm thật & Score & Ngưỡng\\\midrule
ERROR_ROWS
\bottomrule\end{tabular}\end{table}

\section{Khả năng tái lập và phạm vi còn mở}
Mã, cấu hình, phiên bản thư viện, bảng run và audit được giữ trong repo. CSV gốc, mô hình và dự đoán nặng giữ ở local hoặc Drive như hồ sơ cũ. Chạy test bằng PYTHONPATH=src; 42 test đạt ngày 25/10. Script overlap/feature/demo đọc artifact đã lưu, không huấn luyện lại. Các báo cáo được biên dịch và kiểm render; bundle nặng không đưa vào ZIP báo cáo nhẹ.

Đã đo transform+score trên 100 dòng mẫu cho 80 bundle; chưa đánh giá cảm biến trực tiếp, độ trễ/throughput vận hành, concept drift hoặc chi phí triển khai. Chưa có thời gian train-only và phần cứng lịch sử; không coi tổng run là train time. Chưa có dataset độc lập, retrain loại overlap hay thẩm định mới của giảng viên. S07 chỉ sử dụng phạm vi abstract đã đối chiếu, không viện dẫn kết quả/split toàn văn chưa có. Hạn đợt 4/bản cuối cần theo thông báo môn; ngày biên tập 25/10 không phải ngày nộp trong tương lai. Việc chuẩn bị sớm không đổi ngày của 80 run hoặc xác nhận review thay thành viên.
""".replace('ERROR_ROWS',error_rows)
    conclusion=r"""
\chapter{KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN}\label{chap:conclusion}
\section{Trả lời ba câu hỏi nghiên cứu}
Với RQ1, trên closed-set official split, RF/XGB đạt AP xấp xỉ 0,988; tại target validation 5\%, recall Attack khoảng 97\% nhưng FPR test khoảng 18,6--18,7\%. IF có FPR test 6,15\% nhưng recall 31,44\%. Kết quả thể hiện trade-off và không so được tại cùng FPR test thực tế để tuyên bố mô hình tốt nhất.

Với RQ2, khả năng phát hiện held-out tùy category/model. LR tại target 5\% có UADR RF/XGB 97,73\%/98,06\%, IF/AE 0,66\%/23,82\%. AP Normal/held-out của RF/XGB 0,7077/0,6623 thấp hơn AP toàn test 0,9852. Overlap hậu nghiệm cho thấy RF vẫn có UADR 97,56\% ở held-out unmatched, song đó không chứng minh hiệu quả trên mọi zero-day hoặc loại trừ các phụ thuộc khác của official split.

Với RQ3, RF closed-set chuyển target validation 1\% lên 5\% tăng recall từ 90,27\% lên 97,14\% và FPR test từ 4,21\% lên 18,57\%. Ngưỡng validation không bảo đảm ngân sách test. Precision/recall/AP phải được đọc cùng support, prevalence, threshold, scope và giới hạn.

\section{Sản phẩm hiện có và giới hạn}
Sản phẩm kỹ thuật gồm pipeline bốn model, 80 run đã khóa, kiểm metadata/held-out/phạm vi fit, PR/score, phân tích lỗi, matched/unmatched theo tập fit có kiểm chứng, importance mô tả RF/XGB và prototype CSV có kiểm suy luận thật. 42 test đạt, 3.200 dự đoán demo khớp; các con số kỹ thuật không thay nghiệm thu nội dung.

Giới hạn chính: một official split UNSW-NB15; ba lớp held-out hữu hạn; overlap và tương đồng dữ liệu còn hiện hữu; năm seed dùng cùng test; importance không là nguyên nhân; khác prevalence/scope và khác FPR test; chưa có thử nghiệm lưu lượng vận hành hay retrain loại overlap. Nguồn S07 chưa có toàn văn. Nhóm cần tự đọc, góp ý và giải thích từng phần trước khi duyệt nộp.

Hướng tiếp theo có thể kiểm trên bộ dữ liệu ngoài, thiết kế thí nghiệm loại overlap riêng, đánh giá độ ổn định theo thời gian và chi phí vận hành. Đây là đề xuất, chưa ghi thành kết quả đã chạy. Báo cáo được chuẩn bị ngày 25/10 với công cụ hỗ trợ theo yêu cầu nhóm, để cả ba có tài liệu cụ thể mà kiểm và sửa dần.
"""
    # Round-3 contains all analysis; round-4 adds the working demo. No future work is falsely dated as done.
    for kind,folder,title,subtitle in (
        ('dot4','report_dot4_20261025','Báo cáo TLCN - Đợt 4 (nháp chuẩn bị sớm)','BẢN TÍCH LŨY - ĐỢT 4 (NHÁP)'),
        ('tong','report_tong_20261025','Báo cáo tổng TLCN - Bản nháp','BÁO CÁO TỔNG (BẢN NHÁP)')):
        target=DOCS/folder
        for name in ('assets','figures'): shutil.copytree(R3/name,target/name,dirs_exist_ok=True)
        for path in R3.glob('*.tex'):
            if path.name!='main.tex': shutil.copy2(path,target/path.name)
        demo_assets=target/'assets/demo_20261025';demo_assets.mkdir(parents=True,exist_ok=True)
        for path in demo.glob('*.png'): shutil.copy2(path,demo_assets/path.name)
        (target/'demo_chapter.tex').write_text(demo_chapter,encoding='utf-8')
        (target/'conclusion_current.tex').write_text(conclusion,encoding='utf-8')
        text=base.replace('BẢN TÍCH LŨY - ĐỢT 3 (NHÁP)',subtitle).replace('Bản tích lũy đợt 3 - Nháp',title)
        short_header='TLCN - Đợt 4 - Nháp' if kind=='dot4' else 'TLCN - Báo cáo tổng - Nháp'
        text=text.replace('Báo cáo TLCN - '+title,short_header)
        text=text.replace('Tích lũy đợt 3 - Bản nháp',title)
        text=text.replace('Báo cáo tích lũy đợt 3 -- BẢN NHÁP; kế thừa nội dung đợt 1--2, bổ sung phân tích PR/score và feature overlap.',
            ('Bản đợt 4 chuẩn bị sớm ngày 25/10: tích lũy phân tích và prototype CSV có kiểm chứng; chưa duyệt nộp.' if kind=='dot4' else 'Báo cáo tổng bản nháp: nghiên cứu, phương pháp, kết quả, phân tích và prototype; chưa duyệt nộp.'))
        text=text.replace('Đợt 3; hạn 09/11/2026 đã được nhóm trưởng xác nhận thống nhất với giảng viên.',
            'Giữ hạn đợt 3 là 09/11 theo nhóm trưởng; chưa có xác nhận hạn mới cho đợt 4/bản cuối trong lượt chuẩn bị này.')
        # Remove the dated round-2 conclusion; use the current conclusion after all evidence.
        a=text.index(r'\chapter{KẾT LUẬN VÀ GIỚI HẠN CỦA ĐỢT 2}')
        b=text.index(r'\input{dot3_analysis_20261025.tex}',a)
        text=text[:a]+text[b:]
        text=text.replace(r'\input{dot3_analysis_20261025.tex}',r'\input{dot3_analysis_20261025.tex}'+'\n'+r'\input{demo_chapter.tex}'+'\n'+r'\input{conclusion_current.tex}')
        if kind=='tong':
            # A research report flows directly from literature to data; management history stays in prior rounds.
            a=text.index(r'\chapter{ĐỐI CHIẾU GÓP Ý ĐỢT 1 VÀ TIẾN ĐỘ ĐỢT 2}')
            b=text.index(r'\chapter{DỮ LIỆU VÀ DATA CONTRACT}',a)
            text=text[:a]+r'\section{Trạng thái kiểm và đọc chéo}\label{sec:teamreview}\label{sec:progress}'+'\n'+r'Bản nháp có nội dung đầy đủ để nhóm đọc/sửa dần theo thống nhất ngày 25/10. Chưa xác nhận đóng góp hay nghiệm thu thay thành viên. Lịch sử tiến độ và phản hồi ở báo cáo đợt 1--4; bản tổng tập trung vào phương pháp, kết quả và giới hạn.'+'\n\n'+text[b:]
            a=text.index(r'\section{Tính liên tục giữa hai đợt}')
            b=text.index(r'\chapter{CƠ SỞ LÝ THUYẾT',a)
            text=text[:a]+r'\section{Bố cục báo cáo}'+'\n'+r'Báo cáo trình bày cơ sở lý thuyết, dữ liệu, protocol, pipeline, kết quả trên official split, phân tích hậu nghiệm, prototype và kết luận. Tất cả đánh giá dựa trên artifact đã lưu; bản nháp được chuẩn bị với công cụ hỗ trợ rồi cả nhóm kiểm và sửa.'+'\n\n'+text[b:]
            text=text.replace('TÓM TẮT TIẾN ĐỘ','TÓM TẮT NGHIÊN CỨU')
        # Make current analysis headings suitable for accumulated/final reading.
        module=(target/'dot3_analysis_20261025.tex').read_text(encoding='utf-8')
        module=module.replace('PHÂN TÍCH BỔ SUNG ĐỢT 3 -- BẢN NHÁP','PHÂN TÍCH PR, SCORE, OVERLAP VÀ FEATURE')
        (target/'dot3_analysis_20261025.tex').write_text(module,encoding='utf-8')
        (target/'main.tex').write_text(text,encoding='utf-8')
    print('Full draft sources prepared: round 3, round 4, total report.')


if __name__=='__main__': prepare()
