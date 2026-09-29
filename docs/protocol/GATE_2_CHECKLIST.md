# GATE 2 - CHECKLIST DATA CONTRACT VÀ PIPELINE

**Ngày chuẩn bị hồ sơ:** 26/09/2026  
**Trạng thái:** TECHNICAL EVIDENCE PASS - HUMAN REVIEW PENDING

## 1. Data identity

- [x] Dataset là UNSW-NB15.
- [x] Giữ đúng official train/test split.
- [x] Train audit: 175341 dòng x 45 cột, missing=0, duplicate=0, infinity=0.
- [x] Test audit: 82332 dòng x 45 cột, missing=0, duplicate=0, infinity=0.
- [x] SHA-256, byte size, source URL và dtype được lưu trong `artifacts/data/data_manifest.json`.

## 2. Feature and label contract

- [x] `id` bị loại khỏi feature.
- [x] `label` chỉ dùng làm target.
- [x] `attack_cat` chỉ dùng cho scenario/analysis.
- [x] `proto`, `service`, `state` được xử lý như categorical.
- [x] Nhãn Normal=0 và Attack=1 được kiểm tra bằng unit test.

## 3. Leakage and evaluation contract

- [x] Preprocessor chỉ fit trên development partition hợp lệ.
- [x] Official test chỉ dùng cho đánh giá cuối.
- [x] LOACO loại held-out class trước split và trước fit.
- [x] IF/AE fit trên Normal development.
- [x] Threshold lấy từ Normal validation tại FPR 1% và 5%.
- [x] 80/80 run có đủ `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib`.
- [x] 17/17 unit test PASS; protocol validator 80/80 PASS.

## 4. Human review record

> **DRAFT — nội dung dưới đây do AI soạn để ba thành viên review và xác nhận. Không thay thế chữ ký. Ba thành viên cần tự đọc, tự đánh giá, chỉnh sửa nếu cần, rồi ký và điền ngày ở cột cuối.**

| Reviewer | Phạm vi đã đọc | Nhận xét/vấn đề | Kết luận | Ngày/ký |
|---|---|---|---|---|
| Trịnh Trâm Anh | Manifest, schema, label/category, data contract | Bản nháp (chờ xác nhận): `REVIEW_DU_LIEU_TRAM_ANH.md` — đã đối chiếu SHA-256, 45 cột, missing/infinity = 0. Duplicate được tính lại theo 3 cách (0 / 67,601+26,387 / 74,301+28,386) và cross-split overlap 8,541/82,332 đã được giải thích rõ trong data contract. Nếu đồng ý, sửa thành `PASS` và ký. | PASS / FAIL | ................ |
| Hoàng Văn Vương Thu | Leakage, threshold, metric/support, anomaly roles | Bản nháp (chờ xác nhận): `REVIEW_MO_HINH_METRIC_THU.md` — score direction IF/AE có test riêng, threshold chỉ chọn trên Normal validation, support semantics đã mô tả. Điểm cần lưu ý: FPR thực tế trên official test vượt target (RF 5% → 18.6%, XGB → 18.7%), đã được diễn giải là distribution shift chứ không phải lỗi. Nếu đồng ý, sửa thành `PASS` và ký. | PASS / FAIL | ................ |
| Nguyễn Trọng Tín | Tích hợp source, run registry, PDF và evidence | Bản nháp (chờ xác nhận): 80 run ID đúng ma trận, 320 artifact đủ, `check_dot2_final.py` PASS, PDF cập nhật đủ bảng mean/std. Nếu đồng ý, sửa thành `PASS` và ký. | PASS / FAIL | ................ |

## 5. Gate decision

**Kết luận Gate 2:** PASS / FAIL / OPEN  
**Vấn đề còn mở và owner:** ........................................................................  
**Ngày chốt:** ....../....../2026

> Các dấu `[x]` ở phần 1--3 chỉ xác nhận bằng chứng kỹ thuật đã tồn tại. Gate 2 chỉ được đổi sang PASS sau khi cả ba reviewer ghi nhận xét và ký ở phần 4.
