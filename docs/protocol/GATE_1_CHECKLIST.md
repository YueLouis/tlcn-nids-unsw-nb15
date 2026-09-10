# GATE 1 - CHECKLIST KHÓA GIAO THỨC

## Phạm vi

- [ ] Tên đề tài và phạm vi chỉ giới hạn trên UNSW-NB15.
- [ ] Có đúng ba RQ chính; phân tích feature/error là nội dung bổ sung.
- [ ] Có bốn model: RF, XGBoost, Isolation Forest, Autoencoder.
- [ ] Có một closed-set và ba LOACO: Reconnaissance, DoS, Exploits.
- [ ] Có năm seed: 42, 52, 62, 72, 82.

## Dữ liệu và chống leakage

- [ ] Giữ official train/test; test không dùng cho fit/tuning/threshold.
- [ ] Validation chỉ được tạo từ vùng development hợp lệ.
- [ ] `id`, `label`, `attack_cat` bị loại khỏi feature.
- [ ] Trong LOACO, held-out class bị loại trước split, fit transformer và tuning.
- [ ] IF/AE và preprocessing phụ thuộc phân bố của chúng chỉ fit trên Normal train.

## Đánh giá

- [ ] Score cao hơn luôn có nghĩa giống Attack/anomaly hơn.
- [ ] Threshold lấy từ Normal validation tại FPR mục tiêu 1% và 5%.
- [ ] RQ2 dùng UADR, Known Attack Recall và FPR kèm support.
- [ ] Báo cáo mean và std qua đủ năm seed; không chọn seed đẹp.
- [ ] Không tuyên bố LOACO tương đương phát hiện zero-day thực tế.

## Tổ chức

- [ ] Mỗi artifact có owner, reviewer và deadline.
- [ ] Dataset/model nặng lưu ngoài GitHub.
- [ ] Mỗi thay đổi protocol được ghi trong biên bản/decision log.
- [ ] Lịch dùng ngày `dd/mm`, không chỉ ghi “Tuần 1, Tuần 2”.
- [ ] Cả ba thành viên xác nhận biên bản họp số 01.

## Kết quả Gate

**Trạng thái:** NOT REVIEWED  
**Ngày review:** ..../09/2026  
**Kết luận:** PASS / FAIL  
**Vấn đề còn mở và owner:** ....................................................

