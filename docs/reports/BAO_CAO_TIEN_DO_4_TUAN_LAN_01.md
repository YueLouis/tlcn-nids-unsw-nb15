# Báo cáo tiến độ 4 tuần lần 1

**Đề tài:** So sánh mô hình học có giám sát và phát hiện bất thường cho hệ thống phát hiện xâm nhập mạng trên UNSW-NB15: Đánh giá theo phương pháp leave-one-attack-class-out  
**Nhóm:** Trịnh Trâm Anh (23162005), Nguyễn Trọng Tín (23162102), Hoàng Văn Vương Thu (23162099)  
**Giảng viên hướng dẫn:** ThS. Nguyễn Đăng Quang (`quangnd@hcmute.edu.vn`)  
**Kỳ báo cáo:** 17/08/2026-13/09/2026  
**Ngày gửi lần đầu:** 14/09/2026  
**Ngày cập nhật:** 16/09/2026 (bổ sung kế hoạch thực hiện theo góp ý của giảng viên hướng dẫn)  
**Trạng thái:** Báo cáo tổng hợp bốn tuần đầu; nhóm chưa có kết quả mô hình thật

## 1. Tóm tắt tiến độ

Nhóm đăng ký thực hiện đề tài từ ngày 17/08/2026. Trong bốn tuần đầu, nhóm đã hình thành phạm vi nghiên cứu, hoàn thiện đề cương, chuẩn bị tài liệu giải thích, phân công ba luồng công việc và dựng bộ khung kỹ thuật cho thí nghiệm. Tại thời điểm 13/09/2026, nhóm đã có repository, cấu hình thí nghiệm, ma trận 80 lần chạy dự kiến, schema kết quả, checklist Gate 1 và công cụ kiểm tra protocol.

Nhóm **chưa huấn luyện mô hình và chưa có số liệu đánh giá trên dữ liệu thật**. Đây là giới hạn cần nêu rõ để tránh hiểu nhầm rằng sản phẩm đã hoàn thành toàn bộ đề tài. Từ Tuần 5, nhóm sẽ hoàn tất việc kiểm tra dữ liệu và thống nhất cách chạy trước khi thực hiện thí nghiệm thật.

## 2. Đề tài nhóm đang làm là gì

Nhóm xây dựng một quy trình thực nghiệm để so sánh bốn mô hình phát hiện xâm nhập mạng trên dữ liệu dạng network flow của UNSW-NB15:

- **Random Forest** và **XGBoost**: học có giám sát, được học từ Normal và các attack class đã biết.
- **Isolation Forest** và **Autoencoder**: phát hiện bất thường, chủ yếu học mẫu Normal rồi chấm điểm độ bất thường.

Nhóm có hai kịch bản. Ở **closed-set**, các nhóm tấn công có đại diện trong vùng huấn luyện. Ở **LOACO**, nhóm loại hoàn toàn một attack class khỏi vùng phát triển, sau đó kiểm tra class đó trên official test. Ba class được đề xuất giữ lại là **Reconnaissance, DoS và Exploits**. Thiết kế này chỉ mô phỏng unseen/held-out attack trong một benchmark; nhóm không tuyên bố đã chứng minh phát hiện zero-day ngoài thực tế.

Mục tiêu không phải chỉ lấy Accuracy cao. Nhóm sẽ theo dõi UADR/held-out recall, Known Attack Recall và FPR trên Normal, cùng các chỉ số phụ như Precision, F1, PR-AUC, confusion matrix và thời gian chạy.

## 3. Tiến độ theo từng tuần

### Tuần 1: 17/08-23/08 - Chọn hướng và soạn đề cương

**Đã thực hiện:**

- Soạn tên đề tài, vấn đề, mục tiêu, câu hỏi nghiên cứu, phạm vi dữ liệu và nhóm mô hình.
- Chọn UNSW-NB15 làm bộ dữ liệu trung tâm.
- Đề xuất so sánh supervised learning với anomaly detection và bổ sung đánh giá tấn công chưa xuất hiện trong huấn luyện.

**Artifact/bằng chứng:** đề cương Markdown, DOCX/PDF và bản đề cương chi tiết LaTeX được tạo trong thư mục hồ sơ của nhóm ngày 19-22/08/2026.

**Chưa hoàn thành:** chưa có data inventory, chưa có pipeline chạy trên dataset và chưa có kết quả thực nghiệm.

### Tuần 2: 24/08-30/08 - Đăng ký và làm rõ phạm vi

**Đã thực hiện:**

- Gửi/hoàn thiện nội dung đăng ký hướng dẫn với danh sách ba thành viên.
- Chuẩn bị các tài liệu trực quan giải thích NIDS, UNSW-NB15, hai hướng mô hình, LOACO, metric và câu hỏi nghiên cứu để nhóm dùng khi trao đổi.
- Giữ phạm vi ở mức bốn mô hình, không mở rộng quá nhiều thuật toán.

**Artifact/bằng chứng:** hồ sơ đăng ký/trao đổi với thầy và bộ infographic giải thích đề tài trong thư mục cấp môn, tạo ngày 27/08/2026.

**Chưa hoàn thành:** related-work matrix chưa có đủ 10-15 nguồn đã kiểm chứng; chưa chốt bằng biên bản Gate 1.

### Tuần 3: 31/08-06/09 - Phân công và chuẩn bị bàn giao

**Đã thực hiện:**

- Phân tách ba luồng công việc để tránh làm trùng: dữ liệu và related work; pipeline, supervised models và tích hợp; anomaly models, threshold, metric và error analysis.
- Ghi rõ owner, reviewer, đầu ra và chuỗi bàn giao Data -> Pipeline -> Models -> Evaluation.
- Chuẩn bị infographic phân công để ba thành viên có thể trình bày cùng một cách.

**Artifact/bằng chứng:** `Phan_Cong/00_TONG_HOP_PHAN_CONG_NHOM.md`, ba hồ sơ phân công chi tiết và bộ infographic phân công, tạo ngày 04/09/2026.

**Chưa hoàn thành:** chưa có xác nhận review chéo của cả ba thành viên; chưa tải dữ liệu chính thức.

### Tuần 4: 07/09-13/09 - Dựng khung protocol và repository

**Đã thực hiện:**

- Đọc và chuyển yêu cầu của thầy thành quy tắc làm việc: viết liên tục từ đầu, báo cáo 4 tuần/lần, Gantt dùng ngày cụ thể và có thể được yêu cầu demo code/config.
- Dựng repository GitHub private và cấu trúc `configs`, `docs`, `scripts`, `src`, `data`.
- Khóa bản làm việc của RQ, official train/test split, bốn model, ba LOACO class, năm seed `42, 52, 62, 72, 82`, score direction, metric/threshold và các cột cấm `id`, `label`, `attack_cat`.
- Tạo `RUN_MATRIX.csv` với 80 run duy nhất (`4 scenario x 4 model x 5 seed`) và tạo schema cho `run.json`, `metrics.csv`, `predictions.csv`.
- Viết checklist Gate 1, ánh xạ RQ-to-evidence, metric/threshold spec, synthetic-test list và validator protocol.

**Kiểm tra đã chạy:** `python scripts/validate_protocol.py` xác nhận 4 scenario x 4 model x 5 seed = 80 run duy nhất. Kiểm tra này chỉ xác nhận cấu hình; không tự động kết luận Gate 1 PASS.

**Chưa hoàn thành:** chưa có data manifest/checksum/schema report, chưa train bốn model, chưa có kết quả closed-set/LOACO, chưa có prototype chạy được và Gate 1 chưa được cả nhóm ký xác nhận.

## 4. Phân công và sản phẩm của từng người

| Thành viên | Phụ trách trong đề tài | Sản phẩm đã có trong bốn tuần đầu | Việc cần làm tiếp |
|---|---|---|---|
| **Nguyễn Trọng Tín** | Nhóm trưởng; khung repository, protocol, pipeline, Random Forest/XGBoost, registry và tích hợp | Repo, config, run matrix, result schema, Gantt, validator và báo cáo tổng hợp | Điều phối review Gate 1, tích hợp data contract, viết preprocessing và chạy supervised baseline |
| **Trịnh Trâm Anh** | NIDS/UNSW-NB15, nguồn tài liệu, data audit, related work và biên tập | Đề cương, glossary, data-audit checklist, related-work template và phần tài liệu nền | Tải dữ liệu chính thức, checksum, inventory, schema/quality/duplicate report và related work có nguồn |
| **Hoàng Văn Vương Thu** | Isolation Forest, Autoencoder, score, threshold, metric và error analysis | Metric/threshold specification và synthetic-test list | Chốt interface score, evaluator, threshold trên Normal validation và phân tích FP/FN |

Ba thành viên cùng chịu trách nhiệm review chéo, chốt protocol, phân tích kết quả, viết kết luận, slide, demo và bảo vệ. Tín là người tích hợp, không thay thế phần chuyên môn của hai bạn.

## 5. Sản phẩm hiện có và sản phẩm chưa có

### Đã có

- Đề cương và giao thức nghiên cứu bản làm việc.
- Phân công, Gantt đã hiệu chỉnh theo ngày bắt đầu thực tế 17/08/2026.
- Repository private và quy tắc không đưa dataset/model nặng lên GitHub.
- `configs/experiment_matrix.yaml`.
- `docs/protocol/RUN_MATRIX.csv` với 80 run duy nhất.
- `docs/protocol/RQ_TO_EVIDENCE.md` và `docs/protocol/RESULT_SCHEMA.md`.
- `docs/protocol/GATE_1_CHECKLIST.md`.
- `scripts/validate_protocol.py` và kết quả kiểm tra protocol PASS.

### Chưa có và không được báo cáo như đã xong

- Dataset raw, checksum và data inventory.
- Báo cáo chất lượng dữ liệu, missing values, duplicate và cardinality.
- Preprocessing chạy trên dữ liệu thật.
- Kết quả của Random Forest, XGBoost, Isolation Forest hoặc Autoencoder.
- 80 kết quả chính thức, bảng/hình RQ1-RQ3, error analysis.
- Prototype dự đoán và demo cuối.
- Xác nhận Gate 1 bằng chữ ký/biên bản của cả ba thành viên.

## 6. Kế hoạch thực hiện đề tài

Kế hoạch này bao quát toàn bộ thời gian từ ngày đăng ký đến khi đóng gói hồ sơ cuối. Các mốc đã qua dùng để đối chiếu với tiến độ; các mốc tiếp theo là căn cứ phân công và kiểm tra chéo.

| Thời gian | Nội dung thực hiện | Phụ trách chính | Sản phẩm/mốc kiểm tra |
|---|---|---|---|
| 17/08-23/08 | Chọn hướng, mục tiêu, câu hỏi nghiên cứu và bộ dữ liệu | Cả nhóm | Đề cương ban đầu |
| 24/08-30/08 | Hoàn thiện đăng ký, phạm vi và tài liệu giải thích | Tín + cả nhóm | Hồ sơ đăng ký |
| 31/08-06/09 | Phân công, đầu ra và luồng bàn giao | Cả nhóm | Bảng phân công |
| 07/09-13/09 | Khóa protocol, RQ, run matrix, result schema và validator | Tín + cả nhóm | Gate 1 draft; báo cáo lần 1 |
| 14/09-20/09 | Review protocol, họp nhóm, tải dữ liệu chính thức, checksum và manifest | Cả nhóm; Trâm Anh chủ trì dữ liệu | Gate 1 + data manifest |
| 21/09-27/09 | Audit schema/chất lượng/duplicate/nhãn và chốt data contract | Trâm Anh + Tín | Gate 2 |
| 28/09-04/10 | Preprocessing, validation split và leakage tests | Tín | Gate 3 |
| 05/10-11/10 | Random Forest, XGBoost và evaluator | Tín + Thu | Supervised baseline |
| 12/10-18/10 | Isolation Forest, Autoencoder và smoke test bốn mô hình | Thu + Tín | Gate 4 |
| 19/10-25/10 | Closed-set đủ năm seed và bảng/hình RQ1 | Tín + Thu | Kết quả closed-set |
| 26/10-01/11 | LOACO Reconnaissance | Tín + Thu | Kết quả LOACO-R |
| 02/11-08/11 | LOACO DoS | Tín + Thu | Kết quả LOACO-D |
| 09/11-15/11 | LOACO Exploits, kiểm tra đủ 80 run và tổng hợp RQ2-RQ3 | Tín + Thu | Gate 5 |
| 16/11-22/11 | Error analysis, feature importance và thảo luận giới hạn | Thu + Trâm Anh | Chương kết quả/thảo luận |
| 23/11-29/11 | Xây dựng prototype dùng đúng artifact đã khóa | Tín + cả nhóm | Gate 6 |
| 30/11-06/12 | Hoàn thiện báo cáo và đối chiếu số liệu với result files | Trâm Anh + cả nhóm | Bản báo cáo hoàn chỉnh |
| 07/12-13/12 | Slide, câu hỏi phản biện và chạy thử demo | Cả nhóm | Bộ bảo vệ |
| 14/12-20/12 | Đóng gói tái lập và rà soát cuối | Cả nhóm | Gate 7 |
| 21/12-23/12 | Hoàn thiện, nộp hồ sơ cuối | Cả nhóm | Báo cáo, code/config, slide, demo |

### Mốc báo cáo

- **14/09/2026:** báo cáo lần 1; bản ngày 16/09 bổ sung kế hoạch theo góp ý của thầy.
- **12/10/2026:** báo cáo lần 2, dự kiến gồm data audit, preprocessing, leakage tests và baseline ban đầu.
- **09/11/2026:** báo cáo lần 3, dự kiến gồm kết quả LOACO, bảng/biểu đồ và error analysis ban đầu.
- **23/12/2026:** hồ sơ cuối gồm báo cáo, mã nguồn/config, slide, prototype và hướng dẫn chạy.

Nhóm sẽ tiếp tục cập nhật trong cùng chuỗi thư trao đổi với giảng viên. Mỗi đợt ghi rõ việc đã hoàn thành, bằng chứng, vấn đề còn mở và kế hoạch giai đoạn tiếp theo. Mốc thời gian có thể điều chỉnh theo lịch chính thức của môn học hoặc góp ý của giảng viên.

## 7. Vấn đề cần thầy xác nhận

1. Thầy cho nhóm xác nhận tên đề tài và phạm vi bốn model, ba held-out class như protocol hiện tại có phù hợp không.
2. Thầy cho ý kiến liệu nhóm được tiếp tục dùng official train/test split và chọn threshold trên Normal validation như đã mô tả không.
3. Thầy cho nhóm biết có cần demo ngay repository/config ở thời điểm báo cáo bù này không.
4. Nếu mốc báo cáo tiếp theo hoặc format file khác với Gantt, nhóm xin thầy cho nhóm điều chỉnh lại.

## 8. Kết luận

Bốn tuần đầu đã tạo được nền tảng để bắt đầu triển khai có kiểm soát, nhưng sản phẩm hiện tại là **bộ protocol và khung kỹ thuật**, chưa phải một IDS hoàn chỉnh và chưa có kết quả mô hình. Nhóm nhận trách nhiệm gửi bù báo cáo lần 1 ngay đầu Tuần 5, tiếp thu góp ý của thầy và hoàn thiện Gate 1 trước khi dùng dữ liệu thật.

## Phụ lục A - Danh mục artifact

- Repository private của nhóm: `configs/`, `docs/`, `scripts/`, `src/`, `data/`.
- Protocol: `configs/experiment_matrix.yaml`, `docs/protocol/RQ_TO_EVIDENCE.md`, `docs/protocol/RESULT_SCHEMA.md`.
- Validator: `scripts/validate_protocol.py`.
- Tài liệu nội bộ và dữ liệu raw không nằm trong file gửi thầy; nhóm sẽ trình bày theo yêu cầu.
