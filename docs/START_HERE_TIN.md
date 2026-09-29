# BẮT ĐẦU TỪ ĐÂY CHO NGUYỄN TRỌNG TÍN

> **Lưu ý:** Đây là tài liệu nền được viết ngày 13/09/2026 cho giai đoạn Gate 1. Trạng thái hiện tại đã chuyển sang đợt 2; cả nhóm đọc `docs/START_HERE_NHOM.md` trước để biết bản đồ dự án và phần nào đã được đồng bộ.

**Ngày:** 13/09/2026  
**Mục tiêu hiện tại:** hiểu đúng đề tài và đóng Gate 1 trước khi làm dữ liệu thật.

## 1. Đề tài này đang làm gì

Mỗi dòng trong UNSW-NB15 là một bản ghi lưu lượng mạng, gồm các thông tin như giao thức, thời lượng, số byte và số packet. Dòng đó có thể là `Normal` hoặc `Attack`.

Nhóm dùng bốn mô hình để trả lời hai câu hỏi:

1. Khi mô hình đã thấy các loại attack trong lúc học, mô hình nào phát hiện tốt hơn?
2. Nếu giấu một loại attack khỏi giai đoạn phát triển rồi đưa loại đó vào test, mô hình có còn nhận ra đó là bất thường không?

Đây là một nghiên cứu benchmark có quy trình kiểm soát. Nhóm **không** phải xây một SOC hoàn chỉnh và **không** được tuyên bố đã phát hiện mọi zero-day ngoài thực tế.

## 2. Bốn mô hình có ý nghĩa gì

| Mô hình | Học từ đâu | Hiểu đơn giản |
|---|---|---|
| Random Forest | Normal + Attack có nhãn | Học ranh giới giữa hai loại đã biết |
| XGBoost | Normal + Attack có nhãn | Học ranh giới theo cách boosting |
| Isolation Forest | Chủ yếu Normal | Tìm dòng khác xa các dòng bình thường |
| Autoencoder | Chủ yếu Normal | Học tái tạo Normal; tái tạo kém thì xem là bất thường |

Hai mô hình đầu là **supervised learning**. Hai mô hình sau là **anomaly detection**.

## 3. Vai trò của Tín

Em là người giữ “đường ray kỹ thuật”:

- Quy định cấu trúc code và file config.
- Nhận hợp đồng dữ liệu từ Trâm Anh và biến thành input thống nhất.
- Viết preprocessing sao cho không rò rỉ dữ liệu.
- Chạy Random Forest và XGBoost.
- Quản lý mã 80 lần chạy, seed, trạng thái, log và artifact.
- Nhận output IF/AE của Vương Thu, kiểm tra cùng schema.
- Sinh bảng/hình và tích hợp kết quả vào báo cáo, prototype.

Em **không** phải tự làm data audit, IF/AE, related work và toàn bộ báo cáo một mình.

## 4. Trạng thái máy hiện tại

Đã có:

- Repository `tlcn-nids-unsw-nb15`.
- Config bốn scenario, bốn model và năm seed.
- `RUN_MATRIX.csv` đủ 80 run, không trùng ID.
- Result schema, metric/threshold spec, checklist Gate 1.
- Script `scripts/validate_protocol.py` để kiểm tra hợp đồng protocol.

Chưa có và chưa cần có ở Tuần 1:

- Dataset CSV trong thư mục repo.
- Preprocessing chính thức.
- Model đã train.
- Kết quả metric thật.

## 5. Việc phải làm ngay hôm nay

### Bước A - kiểm tra nền tảng

Mở PowerShell tại thư mục repo rồi chạy:

```powershell
python scripts\validate_protocol.py
```

Kết quả đúng phải có:

```text
Protocol validation passed: 4 scenarios x 4 models x 5 seeds = 80 unique runs
Gate 1 remains a human review step; this script does not mark PASS automatically
```

### Bước B - đọc đúng ba file

Đọc theo thứ tự:

1. `configs/experiment_matrix.yaml` - nhóm sẽ chạy những gì.
2. `docs/protocol/RQ_TO_EVIDENCE.md` - mỗi câu hỏi cần bằng chứng gì.
3. `docs/protocol/RESULT_SCHEMA.md` - mỗi lần chạy phải lưu output ra sao.

Không cần đọc toàn bộ 15 tuần một lần. Chỉ đọc phần liên quan đến việc hôm nay.

### Bước C - chuẩn bị Gate 1

Gửi hai bạn cùng xác nhận bảy điểm sau:

- Giữ nguyên official train/test của UNSW-NB15.
- Held-out classes là Reconnaissance, DoS và Exploits.
- Bốn model là RF, XGBoost, IF và Autoencoder.
- Seed là 42, 52, 62, 72, 82.
- Threshold được chọn tại FPR 1% và 5% trên Normal validation.
- Score cao hơn nghĩa là giống Attack/anomaly hơn.
- Không dùng `id`, `label`, `attack_cat` làm feature.

Sau khi hai bạn trả lời, ghi lại câu trả lời vào `docs/meetings/BIEN_BAN_HOP_01.md`.

## 6. Việc của ba bạn trong Tuần 1

| Người | Việc cần làm | File chứng minh |
|---|---|---|
| Tín | Protocol, run matrix, schema, validator, tổng hợp review | `scripts/validate_protocol.py`, `RUN_MATRIX.csv`, biên bản Gate 1 |
| Trâm Anh | Thuật ngữ, nguồn dữ liệu, checklist data audit, related work | `GLOSSARY.md`, `DATA_AUDIT_CHECKLIST.md`, `RELATED_WORK_MATRIX.csv` |
| Vương Thu | Score, threshold, metric và test giả lập | `METRIC_THRESHOLD_SPEC.md`, `SYNTHETIC_TESTS.md` |

## 7. Sau khi Gate 1 được nhóm xác nhận

```text
Gate 1
  -> Trâm Anh tải và kiểm kê 2 CSV chính thức
  -> Trâm Anh bàn giao data_contract
  -> Tín viết preprocessing + leakage tests
  -> Tín chạy RF/XGBoost
  -> Thu chạy IF/Autoencoder + threshold/metric
  -> Tín gom registry, bảng và hình
  -> Cả nhóm phân tích, viết báo cáo, làm prototype
```

Không nhảy cóc qua mũi tên. Nếu chưa có `data_contract`, Tín chưa chạy baseline cuối; nếu threshold chưa được khóa, không nhìn vào official test để chọn lại.

## 8. Khi nào được coi là em đã làm xong phần của mình

Ở giai đoạn cuối, phần Tín đạt khi:

- Có pipeline đọc manifest và tạo đúng vai trò Normal/known/held-out.
- Không có cột cấm trong feature matrix.
- Preprocessor chỉ fit trên vùng được phép.
- RF/XGBoost chạy được với đủ seed và lưu artifact.
- 80 run có trạng thái và fingerprint truy vết được.
- Bảng/hình trong báo cáo sinh từ result files, không nhập tay số liệu.

**Câu nhớ nhanh:** Trâm Anh làm dữ liệu, Vương Thu làm anomaly và metric, Tín nối tất cả thành pipeline có thể chạy lại.
