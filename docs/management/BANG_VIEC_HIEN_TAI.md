# BẢN ĐỒ CÔNG VIỆC NHÓM TLCN

> Hồ sơ lịch sử tháng 9, giữ nguyên nội dung tại thời điểm lập. Trạng thái hiện tại: `docs/management/TIEN_DO_HIEN_TAI_20261013.md` (tính từ repo). Xác nhận nhóm mới ghi riêng, không điền chữ ký vào mẫu cũ.


> **Lưu ý trạng thái:** Đây là bản đồ nền được lập trước khi dữ liệu thật được audit. Đọc `docs/START_HERE_NHOM.md` để xem trạng thái đồng bộ GitHub/Drive và các artifact mới nhất của đợt 2.

**Đề tài:** So sánh supervised learning và anomaly detection cho NIDS trên UNSW-NB15 bằng LOACO  
**Ngày cập nhật:** 13/09/2026  
**Mục tiêu trước mắt:** Gửi bù báo cáo 4 tuần đầu ngày 14/09/2026, hoàn tất Gate 1
ngày 16/09/2026, sau đó mới chuyển sang dữ liệu thật.

## 1. Hiểu đề tài bằng một câu

Nhóm dùng bốn mô hình để xem mô hình nào phát hiện được traffic tấn công trên UNSW-NB15, đặc biệt khi cố tình giấu một loại attack khỏi giai đoạn phát triển rồi kiểm tra lại loại đó.

## 2. Ba người làm ba luồng khác nhau

| Người | Nói đơn giản là phụ trách | Sản phẩm chính |
|---|---|---|
| **Nguyễn Trọng Tín** | Dựng khung kỹ thuật, nối các phần thành pipeline, phụ trách Random Forest/XGBoost và quản lý toàn bộ lần chạy | Repo, config, preprocessing, RF/XGBoost, registry 80 run, validator, bảng/hình tổng hợp, tích hợp cuối |
| **Trịnh Trâm Anh** | Làm nền dữ liệu và nền tảng học thuật để nhóm biết dữ liệu là gì, nguồn nào đáng tin và các bài trước đã làm gì | Data manifest, schema/quality/label/duplicate report, data contract, related-work matrix, phần NIDS/UNSW-NB15, biên tập |
| **Hoàng Văn Vương Thu** | Làm luồng phát hiện bất thường và cách đo kết quả công bằng | Isolation Forest, Autoencoder, score adapter, threshold, metric, error analysis |
| **Cả nhóm** | Chốt protocol, review chéo, phân tích kết quả, viết kết luận, slide và demo | Gate 1-7, báo cáo, slide, demo |

Tín là người **tích hợp**, không có nghĩa là Tín phải tự làm thay hai bạn. Tín chỉ nhận đầu ra của hai bạn, kiểm tra có đúng hợp đồng hay không, rồi đưa vào pipeline chung.

## 3. Tình trạng hiện tại

### Đã có

- Phạm vi UNSW-NB15, bốn model, ba vòng LOACO và năm seed đã được ghi trong config.
- Ma trận `RUN_MATRIX.csv` có đủ 80 run, không trùng `run_id`.
- RQ-to-evidence, result schema, metric/threshold spec và synthetic-test list đã có bản nháp.
- Quy định của thầy đã được chốt: viết liên tục, gửi báo cáo tiến độ 4 tuần/lần.
- `scripts/validate_protocol.py` đã chạy PASS và kiểm tra được hợp đồng 80 run.

### Chưa được coi là xong

- Gate 1 chưa có xác nhận của cả ba người và vẫn là `NOT REVIEWED`.
- Hai bạn chưa review chéo và ký nhận các artifact.
- Chưa có data manifest, schema report hay quality report vì nhóm chưa bước vào Gate 2.
- Chưa được train model và chưa có kết quả thực nghiệm thật.

## 4. Việc của Tín ngay bây giờ

### Hôm nay - 13/09

1. Mở `configs/experiment_matrix.yaml`, `docs/protocol/RQ_TO_EVIDENCE.md` và `docs/protocol/RESULT_SCHEMA.md`; ghi lại các điểm nhóm phải đồng ý, không tự đổi ngầm.
2. Chạy `python scripts/validate_protocol.py`; nếu PASS thì gửi kết quả cho hai bạn để review.
3. Gửi cho Trâm Anh và Vương Thu danh sách cần xác nhận: official split, ba held-out classes, bốn model, năm seed, FPR 1%/5%, score direction và ba cột cấm.

### Ngày 14-15/09

1. Nhận glossary/data-audit/related-work của Trâm Anh và metric/threshold/synthetic tests của Vương Thu.
2. Review chéo từng file; ghi người review, nhận xét và vấn đề còn mở.
3. Điền `docs/meetings/BIEN_BAN_HOP_01.md`, không đánh dấu PASS nếu chưa đủ xác nhận.

### Ngày 16/09

1. Họp kickoff 30-45 phút.
2. Mở config, run matrix và result schema để cả nhóm hiểu cùng một protocol.
3. Kết luận Gate 1 là PASS hoặc FAIL bằng văn bản.

## 5. Sau Gate 1, mỗi tuần phải tạo ra gì

| Giai đoạn | Tín | Trâm Anh | Vương Thu |
|---|---|---|---|
| **17-23/09** | Thiết kế module source, config schema, registry và đọc 2 bài RF/XGBoost | Viết nền NIDS/UNSW-NB15, bắt đầu tracker 10-15 bài | Chốt anomaly assumptions, interface score/threshold và tài nguyên IF/AE |
| **24-30/09** | Chuẩn bị manifest reader và cấu trúc data artifact | Tải đúng hai CSV chính thức, checksum, row count, schema và inventory | Review Normal support, category, missing/infinity và rủi ro IF/AE |
| **21-27/09** | Tích hợp data contract, chuẩn bị báo cáo tiến độ tiếp theo | Hoàn tất quality/duplicate/label/category report và đề xuất Gate 2 | Review dữ liệu và quyết định khả thi cho IF/AE | 
| **08-14/10** | Viết preprocessing và leakage/schema tests | Kiểm tra feature roles và data contract | Hoàn thiện evaluator/adapter skeleton |
| **15-28/10** | Chạy RF/XGBoost và điều phối registry | Cập nhật phần viết theo artifact | Chạy IF/AE, threshold và learning/runtime checks |
| **29/10-25/11** | Điều phối closed-set và ba vòng LOACO, đủ 80 run | Hỗ trợ bảng/hình và diễn giải dữ liệu | Chạy anomaly models, metric và error analysis |

## 6. Luồng bàn giao giữa ba người

```text
Trâm Anh: raw data -> manifest/schema/quality -> data_contract.md
                                      |
                                      v
Tín: data contract -> preprocessing -> RF/XGBoost -> experiment registry
                                      ^                         |
                                      |                         v
Thu: score/threshold/metric -> IF/AE adapters -> evaluator ----+
                                      |
                                      v
                         bảng, hình, báo cáo, prototype
```

Không được bỏ qua mũi tên giữa các bước. Ví dụ: Tín không chạy baseline cuối trước khi Trâm Anh bàn giao data contract và Gate 2; Thu không chọn threshold bằng official test.

## 7. Quy tắc để hết mông lung

- Mỗi việc phải trả lời được: **ai làm, file nào chứng minh, ai review, hạn ngày nào**.
- Báo cáo nội bộ hằng tuần chỉ để nhóm tự quản lý; báo cáo gửi thầy theo kế hoạch là 4 tuần/lần.
- Tuần 1 không tải dataset và không train model; mục tiêu là khóa protocol.
- Nếu một quyết định chưa được ghi trong biên bản hoặc file protocol thì xem như chưa chốt.
- Mọi số liệu sau này phải truy ngược được về run, seed, threshold và fingerprint dữ liệu.

## 8. Mốc gửi thầy

- **14/09/2026:** gửi bù báo cáo tiến độ lần 1, tổng hợp bốn tuần đầu.
- **12/10/2026:** báo cáo tiến độ lần 2 theo baseline đã hiệu chỉnh.
- **09/11/2026:** báo cáo tiến độ lần 3 theo baseline đã hiệu chỉnh.
- **23/12/2026:** hồ sơ cuối, báo cáo, code, slide và demo.
