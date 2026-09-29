# BÁO CÁO TIẾN ĐỘ NỘI BỘ TUẦN 1

**Đề tài:** So sánh mô hình học có giám sát và phát hiện bất thường cho hệ thống phát hiện xâm nhập mạng trên UNSW-NB15: Đánh giá theo phương pháp leave-one-attack-class-out  
**Nhóm:** Trịnh Trâm Anh (23162005), Nguyễn Trọng Tín (23162102), Hoàng Văn Vương Thu (23162099)  
**Người hướng dẫn:** Nguyễn Đăng Quang  
**Kỳ báo cáo:** 10/09/2026-16/09/2026  
**Phiên bản:** 0.1 - cập nhật đến 11/09/2026  
**Trạng thái:** Bản nội bộ chuẩn bị Gate 1

## 1. Tóm tắt tiến độ

Trong những ngày đầu của Tuần 1, nhóm đã dựng repository nghiên cứu, thống nhất
phạm vi dự kiến, ba câu hỏi nghiên cứu, bốn mô hình, ba vòng LOACO, năm random
seed và bộ quy tắc đánh giá. Nhóm cũng đã tạo ma trận 80 run, schema kết quả,
ánh xạ câu hỏi nghiên cứu sang bằng chứng, đặc tả metric/threshold và danh sách
kiểm thử synthetic.

Theo kế hoạch, nhóm **chưa tải dataset và chưa huấn luyện mô hình**. Đây không
phải là thiếu tiến độ: Tuần 1 chỉ nhằm khóa protocol và hoàn tất Gate 1 trước khi
chuyển sang kiểm kê dữ liệu. Tại thời điểm lập báo cáo, hồ sơ kỹ thuật đã sẵn
sàng để review nhưng Gate 1 **chưa được kết luận PASS** vì biên bản họp, ngày họp,
nhận xét review chéo và xác nhận của cả ba thành viên còn bỏ trống.

## 2. Công việc đã thực hiện

| Hạng mục | Kết quả hiện có | Bằng chứng |
|---|---|---|
| Cấu trúc repository và quy tắc lưu trữ | Đã tạo repo GitHub, thư mục `configs`, `docs`, `scripts`, `src`, `data`; raw data và model nặng được loại khỏi Git | `README.md`, `.gitignore` |
| Phạm vi và câu hỏi nghiên cứu | Đã khóa dự thảo RQ1 closed-set, RQ2 held-out attack và RQ3 detection/false-alarm trade-off | `docs/protocol/RQ_TO_EVIDENCE.md` |
| Kịch bản thí nghiệm | Đã định nghĩa closed-set và LOACO cho Reconnaissance, DoS, Exploits | `configs/experiment_matrix.yaml` |
| Mô hình và seed | Random Forest, XGBoost, Isolation Forest, Autoencoder; seed 42, 52, 62, 72, 82 | `configs/experiment_matrix.yaml` |
| Ma trận run | Có 80 run dự kiến, gồm 4 scenario x 4 model x 5 seed; `run_id` không trùng | `docs/protocol/RUN_MATRIX.csv`, `scripts/generate_run_matrix.py` |
| Hợp đồng đầu ra | Đã mô tả `run.json`, `metrics.csv`, `predictions.csv` và điều kiện một run hợp lệ | `docs/protocol/RESULT_SCHEMA.md` |
| Metric và threshold | Đã quy ước score cao hơn = giống Attack/anomaly hơn; threshold lấy từ Normal validation tại FPR 1% và 5% | `docs/week_01/METRIC_THRESHOLD_SPEC.md` |
| Kiểm thử trước dataset thật | Đã lập 10 synthetic tests cho score direction, threshold, label mapping, mẫu số bằng 0 và duplicate `run_id` | `docs/week_01/SYNTHETIC_TESTS.md` |
| Artifact dữ liệu và thuật ngữ | Đã có glossary, checklist data audit và mẫu ma trận related work | `docs/week_01/GLOSSARY.md`, `DATA_AUDIT_CHECKLIST.md`, `RELATED_WORK_MATRIX.csv` |
| Kế hoạch và phân công | Đã ghi mốc ngày cụ thể, owner, reviewer và mốc báo cáo 4 tuần/lần | `docs/management/PHAN_CONG_NHOM.md`, `GANTT_CHART.md` |

## 3. Kiểm tra bằng chứng kỹ thuật

- Trước khi tạo báo cáo, repository đang ở nhánh `main` và bộ artifact nền tảng
  đã được commit; báo cáo Tuần 1 này là các file bổ sung đang chờ commit.
- Commit gần nhất chứa bộ artifact Tuần 1 là `f5686f0` (`docs: add week 1 team
  artifacts`).
- `RUN_MATRIX.csv` có 80 dòng dữ liệu; phân bố là 20 run cho mỗi scenario:
  `closed_set`, `loaco_reconnaissance`, `loaco_dos` và `loaco_exploits`.
- Kiểm tra trùng `run_id` cho kết quả không có bản ghi trùng.
- Dataset raw chưa xuất hiện trong repository, phù hợp với quy tắc bảo mật và
  kế hoạch chỉ tải dữ liệu sau khi Gate 1 được duyệt.

## 4. Tiến độ theo thành viên

| Thành viên | Đã có | Còn phải đóng trong Tuần 1 | Trạng thái |
|---|---|---|---|
| Trịnh Trâm Anh | Glossary, data-audit checklist, related-work template | Review chéo, bổ sung nguồn/tiêu chí nếu nhóm thống nhất, xác nhận trong biên bản | Đang review |
| Hoàng Văn Vương Thu | Metric/threshold specification, 10 synthetic tests | Review score direction và metric với hai thành viên còn lại, ghi test owner | Đang review |
| Nguyễn Trọng Tín | Repository, config, ma trận 80 run, result schema, Gate 1 checklist | Mời/xác nhận tài khoản GitHub, tổng hợp review chéo, điền biên bản họp | Đang tích hợp |

## 5. Các quyết định protocol cần xác nhận bằng văn bản

Các điểm dưới đây đã có đề xuất thống nhất trong tài liệu làm việc nhưng chưa
được đánh dấu PASS trong biên bản họp:

1. Giữ official train/test split của UNSW-NB15 và không dùng official test để
   fit, tuning hoặc chọn threshold.
2. Chọn Reconnaissance, DoS và Exploits làm ba held-out attack classes.
3. Dùng bốn mô hình Random Forest, XGBoost, Isolation Forest và Autoencoder.
4. Chạy năm seed 42, 52, 62, 72, 82 và báo cáo mean +/- standard deviation.
5. Chọn threshold trên Normal validation tại ngân sách FPR 1% và 5%.
6. Loại `id`, `label` và `attack_cat` khỏi feature matrix.
7. Chỉ gọi kết quả là held-out/unseen trong thiết kế LOACO, không gọi là bằng
   chứng phát hiện zero-day thực tế.

## 6. Vấn đề còn mở và cách đóng

| Vấn đề | Owner | Hạn nội bộ | Cách đóng |
|---|---|---:|---|
| Chưa có ngày, hình thức và nội dung kết luận của kickoff | Tín + cả nhóm | 16/09/2026 | Họp 30-45 phút, điền `BIEN_BAN_HOP_01.md` |
| Chưa có review chéo và xác nhận của ba thành viên | Cả nhóm | 15/09/2026 | Review từng artifact, ghi người review và commit/link |
| Chưa xác nhận username GitHub của Trâm Anh và Vương Thu | Tín | 11/09/2026 | Xác nhận tài khoản riêng và quyền truy cập repo |
| Related-work matrix mới là header, chưa có bài cụ thể | Trâm Anh | Tuần 2 | Dùng đúng template để lập danh mục 10-15 nguồn có kiểm chứng |
| Gantt và nhịp báo cáo cần đối chiếu deadline chính thức của môn | Tín | 16/09/2026 | Xác nhận với giảng viên; giữ mốc 07/10/2026 là mốc nội bộ hiện tại |

## 7. Kế hoạch ngay sau Gate 1

Trong giai đoạn 17/09-23/09/2026, nhóm dự kiến:

- hoàn thiện related work có nguồn và tiêu chí so sánh;
- thiết kế kiến trúc pipeline, interface model và test plan;
- rà lại protocol theo góp ý của giảng viên nếu có;
- chuẩn bị checklist tải dữ liệu chính thức cho giai đoạn 24/09-30/09/2026;
- không đưa số liệu thực nghiệm vào báo cáo trước khi có data audit và Gate 2.

## 8. Kết luận và đề nghị xác nhận

Tuần 1 đã tạo được nền tảng cần thiết để bắt đầu nghiên cứu có kiểm soát: phạm
vi, protocol dự thảo, ma trận run, schema kết quả và phân công đều đã có artifact
truy vết được. Mức hoàn thành hiện tại phù hợp với mục tiêu Tuần 1, nhưng chưa đủ
cơ sở để ghi Gate 1 là PASS.

Nhóm đề nghị xác nhận ba việc trong buổi kickoff ngày 16/09/2026:

1. chấp thuận các quyết định protocol ở Mục 5;
2. ghi rõ vấn đề còn mở, owner và deadline nếu có thay đổi;
3. ký kết luận PASS/FAIL trong `docs/meetings/BIEN_BAN_HOP_01.md`.

**Kết luận hiện tại:** `NOT REVIEWED - chờ review chéo và xác nhận Gate 1`.

## Phụ lục A - Danh mục artifact Tuần 1

| Artifact | Vai trò |
|---|---|
| `docs/week_01/KE_HOACH_TUAN_01.md` | Mục tiêu và lịch 7 ngày |
| `docs/week_01/GLOSSARY.md` | Thuật ngữ thống nhất |
| `docs/week_01/DATA_AUDIT_CHECKLIST.md` | Checklist chuẩn bị Gate 2 |
| `docs/week_01/RELATED_WORK_MATRIX.csv` | Mẫu tổng hợp tài liệu liên quan |
| `docs/week_01/METRIC_THRESHOLD_SPEC.md` | Metric, score và threshold |
| `docs/week_01/SYNTHETIC_TESTS.md` | Danh sách test trước dataset thật |
| `docs/protocol/RQ_TO_EVIDENCE.md` | Ánh xạ RQ sang bằng chứng |
| `docs/protocol/RESULT_SCHEMA.md` | Hợp đồng artifact kết quả |
| `docs/protocol/RUN_MATRIX.csv` | Ma trận 80 run |
| `docs/protocol/GATE_1_CHECKLIST.md` | Điều kiện PASS/FAIL Gate 1 |
| `docs/meetings/BIEN_BAN_HOP_01.md` | Biên bản kickoff và xác nhận Gate 1 |
