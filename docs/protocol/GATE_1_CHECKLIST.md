# GATE 1 - CHECKLIST KHÓA GIAO THỨC

> **Trạng thái kỹ thuật:** TECHNICAL EVIDENCE PASS - HUMAN REVIEW PENDING. Các ô `[x]` dưới đây chỉ phản ánh bằng chứng trong repository; không thay thế xác nhận và chữ ký của ba thành viên.

## Phạm vi

- [x] Tên đề tài và phạm vi chỉ giới hạn trên UNSW-NB15.
- [x] Có đúng ba RQ chính; phân tích feature/error là nội dung bổ sung.
- [x] Có bốn model: RF, XGBoost, Isolation Forest, Autoencoder.
- [x] Có một closed-set và ba LOACO: Reconnaissance, DoS, Exploits.
- [x] Có năm seed: 42, 52, 62, 72, 82.

## Dữ liệu và chống leakage

- [x] Giữ official train/test; test không dùng cho fit/tuning/threshold.
- [x] Validation chỉ được tạo từ vùng development hợp lệ.
- [x] `id`, `label`, `attack_cat` bị loại khỏi feature.
- [x] Trong LOACO, held-out class bị loại trước split, fit transformer và tuning.
- [x] IF/AE và preprocessing phụ thuộc phân bố của chúng chỉ fit trên Normal train.

## Đánh giá

- [x] Score cao hơn luôn có nghĩa giống Attack/anomaly hơn.
- [x] Threshold lấy từ Normal validation tại FPR mục tiêu 1% và 5%.
- [x] RQ2 dùng UADR, Known Attack Recall và FPR kèm support.
- [x] Báo cáo mean và std qua đủ năm seed; không chọn seed đẹp.
- [x] Không tuyên bố LOACO tương đương phát hiện zero-day thực tế.

## Tổ chức

- [ ] Mỗi artifact có owner, reviewer và deadline.
- [ ] Dataset/model nặng lưu ngoài GitHub.
- [ ] Mỗi thay đổi protocol được ghi trong biên bản/decision log.
- [ ] Lịch dùng ngày `dd/mm`, không chỉ ghi “Tuần 1, Tuần 2”.
- [ ] Cả ba thành viên xác nhận biên bản họp số 01.

## Kết quả Gate

**Trạng thái:** TECHNICAL EVIDENCE PASS - HUMAN REVIEW PENDING
**Ngày review:** ..../09/2026  
**Kết luận:** PASS / FAIL  
**Vấn đề còn mở và owner:** ....................................................
