"""Package actual role products with source paths; do not invent personal authorship."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/group_delivery_20261110'
OUT = ROOT / 'output/role_deliverables_20261111'
REPO = 'https://github.com/YueLouis/tlcn-nids-unsw-nb15'
ROLES = {
    'TramAnh': ('Trịnh Trâm Anh', 'tta2405', 'tramanh', 'dữ liệu, nguồn học thuật và giới hạn benchmark'),
    'VuongThu': ('Hoàng Văn Vương Thu', 'hoangvvthu', 'vuongthu', 'mô hình bất thường, metric và phân tích lỗi'),
    'TrongTin': ('Nguyễn Trọng Tín', 'YueLouis', 'trongtin', 'protocol, pipeline, tái lập và tích hợp demo'),
}
FILES = {
    'TramAnh': [
        ('artifacts/data/data_manifest.json', 'DU_LIEU_MANIFEST.json'),
        ('artifacts/data/duplicate_overlap_audit.json', 'DUPLICATE_OVERLAP.json'),
        ('docs/references/RELATED_WORK_MATRIX_DOT_02.csv', 'MA_TRAN_TAI_LIEU.csv'),
        ('docs/evidence/dot_03/final_20261030/overlap/FIT_SET_CHECKS.csv', 'KIEM_TRA_TAP_FIT.csv'),
        ('docs/evidence/dot_03/final_20261030/overlap/OVERLAP_MEAN_STD.csv', 'OVERLAP_MEAN_STD.csv'),
    ],
    'VuongThu': [
        ('docs/reports/DOT_02_TWO_TARGETS.csv', 'HAI_NGUONG_FPR.csv'),
        ('docs/evidence/dot_03/final_20261030/pr_scores/AP_MEAN_STD.csv', 'AP_MEAN_STD.csv'),
        ('docs/evidence/dot_03/final_20261030/pr_scores/OPERATING_POINTS_MEAN_STD.csv', 'DIEM_VAN_HANH.csv'),
        ('docs/evidence/dot_03/final_diagnostics_20261025/NEAR_THRESHOLD_EXAMPLES_S42.csv', 'VI_DU_GAN_NGUONG.csv'),
        ('docs/evidence/dot_03/final_diagnostics_20261025/ERROR_STABILITY.csv', 'DO_ON_DINH_LOI.csv'),
        ('docs/evidence/dot_03/final_diagnostics_20261025/CATEGORY_DETECTION_HEATMAP.png', 'PHAT_HIEN_THEO_LOAI.png'),
    ],
    'TrongTin': [
        ('configs/experiment_matrix.yaml', 'MA_TRAN_THI_NGHIEM.yaml'),
        ('docs/evidence/dot_03/submission_20261111/REPORT_TABLE_CHECK.json', 'KIEM_BANG_BAO_CAO.json'),
        ('docs/evidence/dot_03/submission_20261111/DELIVERY_TECHNICAL_CHECK.json', 'KIEM_KY_THUAT_PDF.json'),
        ('docs/evidence/dot_03/final_diagnostics_20261025/MODEL_DISAGREEMENT_S42.csv', 'BAT_DONG_MO_HINH.csv'),
    ],
}
TEXT = {
    'TramAnh': '''# Dữ liệu, nguồn và giới hạn đánh giá

## Dữ liệu được dùng

Nhóm sử dụng hai tập chia chính thức của UNSW-NB15: 175.341 dòng phát triển và 82.332 dòng kiểm tra. Mỗi tập có 45 cột. Ba cột `id`, `label`, `attack_cat` phục vụ định danh hoặc đánh giá, không đưa vào mô hình; đầu vào mô hình còn 42 đặc trưng. Trong đó `proto`, `service`, `state` là dạng phân loại, 39 cột còn lại là số.

`DU_LIEU_MANIFEST.json` ghi nguồn, SHA-256, số dòng, kiểu dữ liệu và số mẫu từng nhãn. Kiểm missing và infinity không phát hiện giá trị thiếu/vô hạn trong hai CSV được ghi nhận. Đây là kết quả audit bộ dữ liệu cụ thể, không phải bảo đảm mọi dữ liệu đầu vào sau này đều sạch.

## Cách chia tập và tránh dùng nhầm dữ liệu

Official train được chia thành vùng huấn luyện và validation. Với LOACO, loại lớp giữ lại khỏi vùng phát triển trước phép chia. RF/XGB học từ Normal và các Attack còn được phép; IF/AE học Normal. Preprocessing chỉ được fit trong vùng huấn luyện phù hợp. Ngưỡng được chọn bằng Normal validation; official test không tham gia chọn ngưỡng.

Trong ba lượt LOACO, lớp được giữ lại lần lượt là Reconnaissance, DoS và Exploits. Test vẫn chứa các lớp đó để đo khả năng nhận ra một loại chưa xuất hiện khi học. LOACO không chứng minh phát hiện mọi zero-day ngoài thực tế.

## Vì sao duplicate bằng 0 vẫn có overlap

Đếm cả hàng có `id` cho duplicate bằng 0. Nếu chỉ đếm 42 đặc trưng, số hàng lặp sau lần đầu là 74.301 ở train và 28.386 ở test. Có 8.541/82.332 dòng test trùng vector 42 đặc trưng với một dòng trong toàn official train. Các phép đếm này dùng các khóa khác nhau nên không mâu thuẫn.

Đợt 3 bổ sung overlap với đúng tập model được fit, thay vì mặc định toàn official train. `KIEM_TRA_TAP_FIT.csv` ghi 80 lượt; `OVERLAP_MEAN_STD.csv` tách matched/unmatched và support. Tập fit của supervised khác Normal-only nên hai họ không có cùng nhóm matched. Không diễn giải chênh lệch metric giữa hai nhóm là tác động nhân quả của overlap; chưa có thí nghiệm retrain loại trùng.

## Nguồn và giới hạn

`MA_TRAN_TAI_LIEU.csv` ghi DOI/URL, nội dung dùng và phạm vi đối chiếu. Nguồn S07 mới được đối chiếu abstract; không dùng nó để trích metric hay cách chia tập chi tiết. Nhóm mới đo một dataset/official split, chưa kiểm dữ liệu vận hành độc lập. Nguồn gốc dataset thuộc UNSW; dữ liệu này không phải dataset do nhóm tự thu thập.

Mã và kiểm thử liên quan nằm trong ZIP theo đường dẫn gốc: `src/nids_benchmark/data.py`, `scripts/audit_data.py`, `scripts/audit_duplicate_overlap.py`, `tests/test_data_pipeline.py`. Các bản sao giữ nguyên nội dung nguồn và hash, không đổi tác giả lịch sử.
''',
    'VuongThu': '''# Kết quả, ngưỡng và phân tích lỗi

## Đọc ba chỉ số chính

Attack là lớp dương. FPR = FP / số Normal, recall Attack = TP / số Attack, UADR = số held-out được phát hiện / tổng held-out. Mẫu số của FPR khác mẫu số của UADR. AP mô tả xếp hạng theo score trên nhiều ngưỡng; nó không thay tỷ lệ phát hiện và báo nhầm tại một ngưỡng cụ thể.

Hai target 1% và 5% là ngân sách FPR trên Normal validation. Chúng không bảo đảm FPR test bằng 1% hoặc 5%. Với RF closed-set, đổi target 1% sang 5% làm recall test trung bình tăng 90,27% lên 97,14%, đồng thời FPR test tăng 4,21% lên 18,57%. Số liệu lấy từ `HAI_NGUONG_FPR.csv`, trung bình năm seed cùng official test.

## Kết quả chính của đợt 3

Trong LR, RF có AP toàn test khoảng 0,9852 nhưng AP chỉ trên Normal và Reconnaissance held-out là 0,7077. XGB tương ứng 0,9852 và 0,6623. Chỉ đọc AP toàn test dễ bỏ qua độ khó riêng của held-out vì phần known Attack cũng góp vào chỉ số chung. Hai scope có thành phần và tỷ lệ dương khác nhau; không dùng chênh lệch AP giữa scope như một phép so sánh công bằng giữa model.

IF ở closed-set có FPR test thấp hơn RF tại target 5% (6,15% so với 18,57%) nhưng recall Attack thấp hơn (31,44% so với 97,14%). AE và IF có cách sinh score khác RF/XGB. Cần đọc hướng score đã chuẩn hóa, support, threshold và cả hai loại lỗi; không chọn model tốt nhất từ một con số.

## Ví dụ có thể truy vết

LR-RF-S42, target validation 5%, threshold 0,55681266574524546:

| ID | Nhãn thật | Score | Dự đoán | Kết quả |
|---|---|---:|---|---|
| 68699 | Normal | 0,5568311122449866 | Attack | FP: vượt ngưỡng rất ít |
| 975 | Reconnaissance | 0,55649131907993055 | Normal | FN: thấp hơn ngưỡng |

Nguồn là `results/runs/LR-RF-S42/predictions.csv`; hash và dữ liệu hai hàng được giữ trong `NGUON_VI_DU_THU.csv`. Score sát ngưỡng giải thích quy tắc quyết định, chưa chứng minh feature nào gây ra lỗi. Các ví dụ được chọn theo tiêu chí gần ngưỡng để mở lại, không phải mẫu ngẫu nhiên đại diện.

## Độ ổn định và giới hạn

`DO_ON_DINH_LOI.csv` đếm lỗi lặp qua năm seed; `VI_DU_GAN_NGUONG.csv` lưu ví dụ kèm vai trò và feature. Năm seed đều dùng cùng official test, nên độ lệch chuẩn không phải khoảng tin cậy trên năm dataset độc lập. Biểu đồ theo category cũng phải đọc cùng support; Worms chỉ có 44 mẫu test.

ZIP giữ mã `evaluation.py`, adapter IF/AE trong `models.py`, các test score/metric và script phân tích theo đường dẫn gốc. Đây là mã dùng chung được liên kết theo phạm vi phụ trách, không phải khai báo toàn bộ mã đó mới do một người viết ngày 11/11.
''',
    'TrongTin': '''# Protocol, tái lập và demo

## Thực nghiệm chung

Ma trận gồm CS và ba LOACO LR/LD/LE, bốn mô hình RF/XGB/IF/AE, năm seed 42/52/62/72/82: tổng 80 lượt chạy. Mỗi lượt có `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib`. Kết quả gốc và ngưỡng được giữ nguyên; bản cập nhật hồ sơ không phải lượt huấn luyện mới.

Pipeline bỏ lớp held-out trước chia vùng phát triển, fit preprocessing trong đúng vùng huấn luyện rồi chọn threshold trên Normal validation. Test chỉ được đưa qua các thành phần đã fit. Score chung được quy ước càng cao càng nghiêng về Attack. RF/XGB dùng dữ liệu có nhãn được phép; IF/AE fit Normal.

## Ví dụ hai ngưỡng

CS-RF-S42, ID 1 là Normal, score 0,7057412707296608. Target 5% có threshold 0,5572816867482743 nên dự đoán Attack (FP). Target 1% có threshold 0,8053672551154485 nên dự đoán Normal (TN). Mô hình và score không đổi; quyết định đổi do ngưỡng. Dữ liệu nguồn nằm trong ZIP ở `dot_03/VI_DU_HAI_NGUONG.csv`.

## Kiểm tra và khả năng tái lập

Ngày 11/11/2026 kiểm 46 unit test và validator 80 tổ hợp; 174 dòng bảng báo cáo đối chiếu khớp nguồn. Test AE có ConvergenceWarning trong dữ liệu tổng hợp; assertion đều đạt, không dùng kết quả đó để khẳng định AE hội tụ ở mọi bài toán. PDF có 62 trang, 200 liên kết nội bộ và 56 bookmark đã kiểm đích đến. Đây là kiểm kỹ thuật; không thay lượt đọc hoặc nghiệm thu của thành viên.

ZIP kèm toàn bộ `src/`, `tests/`, cấu hình và requirements để tránh mất phụ thuộc khi tách mã. Các raw CSV, prediction và bundle nặng nhận từ Drive dùng chung, kiểm hash theo manifest trước khi chạy. Lệnh PowerShell từ thư mục giải nén:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -q
python scripts/validate_protocol.py
python scripts/demo_server.py
```

Demo hiện có đọc CSV đúng schema và suy luận từ 16 bundle seed42 ở hai target. Nó có thể trả Normal/Attack, score, threshold và so sánh bốn model. Replay dùng mẫu từ official test là phần minh họa kết quả đã biết, không phải một dataset mới hoặc hệ thống tự học. Giao diện trình bày sáng đang được hoàn thiện riêng; chưa coi bản đề xuất giao diện là demo suy luận hoàn chỉnh.

## Phần cần phát triển tiếp

Hoàn thiện bản đợt 4/tổng, giao diện thuyết trình nối đúng inference, kịch bản hỏi đáp và đánh giá ưu/nhược. Nếu bổ sung dữ liệu tự thu thập, phải ghi nguồn, cách trích đủ đặc trưng tương thích và giới hạn so sánh; không tạo 42 số ngẫu nhiên rồi gọi là traffic thật.
'''
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def put(p, s):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding='utf-8')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for role, (name, account, branch, responsibility) in ROLES.items():
        target = BASE / role
        put(target/'PHAN_CHUYEN_MON.md', TEXT[role])
        role_paths = FILES[role] + [
            ('docs/management/PHAN_CONG_NHOM.md', None),
            ('docs/management/PHAN_CONG_DOT_02_HIEN_TAI_20260929.md', None),
            ('docs/reports/BAO_CAO_TIEN_DO_4_TUAN_LAN_01.md', None),
        ]
        old = {'TramAnh': ['docs/week_01/GLOSSARY.md','docs/week_01/DATA_AUDIT_CHECKLIST.md','docs/evidence/dot_02/DATA_CONTRACT.md'],
               'VuongThu': ['docs/week_01/METRIC_THRESHOLD_SPEC.md','docs/week_01/SYNTHETIC_TESTS.md'],
               'TrongTin': ['docs/protocol/RUN_MATRIX.csv','docs/protocol/RESULT_SCHEMA.md','docs/protocol/RQ_TO_EVIDENCE.md']}[role]
        role_paths += [(p, None) for p in old]
        zpath = target/f'HO_SO_{role.upper()}_20261111.zip'
        entries=[]
        written=set()
        runtime=list((ROOT/'src').rglob('*.py'))+list((ROOT/'tests').rglob('*.py'))+list((ROOT/'configs').glob('*'))
        runtime += [ROOT/x for x in ['requirements.txt','requirements-repro.txt','scripts/validate_protocol.py','scripts/demo_server.py','scripts/audit_data.py','scripts/audit_duplicate_overlap.py','scripts/analyze_pr_scores.py','scripts/analyze_overlap_slices.py','scripts/analyze_final_diagnostics.py']]
        runtime += [p for p in (ROOT/'demo').rglob('*') if p.is_file() and p.suffix in ('.html','.css','.js','.json','.csv','.md','.png','.svg')]
        with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in runtime:
                if p.is_file():
                    rel=p.relative_to(ROOT).as_posix();z.write(p,rel);written.add(rel);entries.append({'path':rel,'sha256':sha(p),'kind':'shared_runtime'})
            for rel, flat in role_paths:
                p=ROOT/rel
                assert p.is_file(), p
                if rel not in written:
                    z.write(p,rel);written.add(rel);entries.append({'path':rel,'sha256':sha(p),'kind':'role_reference'})
                if flat: shutil.copy2(p,target/flat)
            if role == 'TrongTin':
                import pandas as pd
                df=pd.read_csv(ROOT/'results/runs/CS-RF-S42/predictions.csv',float_precision='round_trip')
                payload=df[df.record_id.eq(1)].to_csv(index=False,float_format='%.17g')
                z.writestr('dot_03/VI_DU_HAI_NGUONG.csv',payload)
                put(target/'VI_DU_HAI_NGUONG.csv',payload)
            if role == 'VuongThu':
                p=target/'NGUON_VI_DU_THU.csv';z.write(p,'dot_03/NGUON_VI_DU_THU.csv')
            z.writestr('PHAN_CHUYEN_MON.md',TEXT[role])
            z.writestr('SOURCE_MANIFEST.json',json.dumps(entries,ensure_ascii=False,indent=2))
            z.writestr('DOC_TRUOC.txt','Hồ sơ theo phạm vi phân công, bổ sung ngày 11/11/2026.\nMã và bằng chứng lịch sử giữ nguồn; không đổi tác giả hoặc ngày thực hiện.\nCó sử dụng công cụ hỗ trợ; upload theo ủy quyền không thay việc đọc/sửa của thành viên.\nRaw/model/prediction nhận từ Drive; cài requirements trước khi chạy.\n')
        with zipfile.ZipFile(zpath) as z: assert z.testzip() is None
        with (target/'CHI_MUC_NGUON.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['path','sha256','kind']);w.writeheader();w.writerows(entries)
        put(target/'QUA_TRINH_CAC_DOT.md',f'''# Phạm vi {name} qua các đợt

Nhánh: `{branch}`. Tài khoản nộp: `{account}`. Phụ trách: {responsibility}.

| Đợt | Nội dung theo phân công | Bằng chứng và trạng thái |
|---|---|---|
| 1 | Nền lý thuyết, đặc tả và kế hoạch theo phân công gốc | Các tài liệu tuần đầu trong ZIP giữ nguyên. Báo cáo chung đã gửi 14/09; không coi việc bổ sung hôm nay là commit cá nhân đã có từ tháng 9 |
| 2 | Dữ liệu/pipeline/baseline/metric theo phạm vi phụ trách | Bằng chứng gốc và mã giữ đường dẫn trong CHI_MUC_NGUON.csv. Báo cáo chung gửi 17/10. Thầy phản hồi 31/10 rằng repo lúc kiểm chỉ thấy commit của Tín; lịch sử đó không được sửa lại |
| 3 | Phần chuyên môn, bảng số và ví dụ truy vết | Hồ sơ ngày 11/11 gồm PHAN_CHUYEN_MON.md, bảng/ảnh và ZIP mã nguồn phụ thuộc. Kết quả gốc giữ mốc 30/10; đây là bổ sung hồ sơ hiện tại |
| 4 và tổng | Hoàn thiện demo, bàn luận và báo cáo cuối theo cùng vai trò | Đang tiếp tục; chưa ghi đã nộp hoặc nghiệm thu. Kết quả mới sẽ có ngày, tài khoản và nguồn riêng |

Phân công không đồng nghĩa toàn bộ mã/tài liệu tham chiếu do riêng người phụ trách viết. Nội dung được chuẩn bị có công cụ hỗ trợ và tải theo ủy quyền; phần tự đọc, sửa và nhận xét thực tế của thành viên được ghi riêng khi thực hiện. Bản tổng hợp trên main liên kết hồ sơ này, giữ nguyên tác giả commit và thời gian gốc.
''')
        put(target/'README.md',f'''# {name} — hồ sơ chuyên môn

**Phụ trách:** {responsibility}. Nhánh `{branch}`, tài khoản `{account}`. Bản tổng hợp của nhóm ở [main]({REPO}/tree/main).

- [Phần chuyên môn và kết luận](PHAN_CHUYEN_MON.md)
- [Phạm vi xuyên suốt các đợt](QUA_TRINH_CAC_DOT.md)
- [Chỉ mục nguồn và SHA-256](CHI_MUC_NGUON.csv)
- [Gói mã, kiểm thử và bằng chứng theo đường dẫn gốc]({zpath.name})

Các CSV/ảnh trong thư mục mở trực tiếp được; ZIP giữ thêm mã và phụ thuộc dùng chung. Kết quả thực nghiệm giữ mốc 30/10, hồ sơ được bổ sung ngày 11/11/2026. Mã/tài liệu lịch sử giữ nguồn; việc tải theo ủy quyền không thay xác nhận phần tự đọc, sửa hay đóng góp của thành viên.
''')
        dest=OUT/role;dest.mkdir(parents=True,exist_ok=True)
        upload_names=['README.md','PHAN_CHUYEN_MON.md','QUA_TRINH_CAC_DOT.md','CHI_MUC_NGUON.csv',zpath.name]+[flat for _,flat in FILES[role] if flat]
        upload_names += ['NGUON_VI_DU_THU.csv'] if role=='VuongThu' else ['VI_DU_HAI_NGUONG.csv'] if role=='TrongTin' else []
        for n in upload_names: shutil.copy2(target/n,dest/n)
        put(dest/'UPLOAD_MANIFEST.json',json.dumps({'role':role,'expected_account':account,'branch':branch,'prepared_at':datetime.now(timezone.utc).isoformat(),'files':[{'name':n,'sha256':sha(dest/n),'bytes':(dest/n).stat().st_size} for n in upload_names]},ensure_ascii=False,indent=2))
        print(role,len(upload_names),'files',zpath.stat().st_size,'zip bytes')


if __name__=='__main__':main()
