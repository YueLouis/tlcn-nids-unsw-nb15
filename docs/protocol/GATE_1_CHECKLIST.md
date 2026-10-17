# Gate 1 - Protocol

**Cập nhật sau trao đổi ngày 17/10/2026:** nhóm trưởng cho biết chưa chắc mức hiểu của từng thành viên; cả nhóm dự kiến tự rà soát đợt 1 và đợt 2 ngày 18/10 sau khi nghỉ ngơi. Do đó, lời báo đã đồng ý trước đó không được dùng để kết luận đã đọc, giải thích được hoặc nghiệm thu nội dung. **Kiểm kỹ thuật đã thực hiện; rà soát nội dung của nhóm còn mở; email giữ nháp, chưa gửi.** PDF 32 trang ngày 14/10 giữ nguyên để nhóm kiểm lại. Xem `HUONG_DAN_RA_SOAT_HAI_DOT_20261018.md` trong thư mục quản lý nhóm.

Phần bên dưới giữ các mốc kiểm tra và lời báo trước đó để truy vết; trạng thái hiện tại theo cập nhật trên.

Cập nhật 13/10/2026.

**Bằng chứng kỹ thuật:** PASS trong phạm vi kiểm tra tự động. **Xác nhận nội dung:** nhóm trưởng cung cấp thông tin cả ba thành viên đã xác nhận; xem `../evidence/dot_02/final_20261013/XAC_NHAN_NHOM_20261013.md`. Không tạo chữ ký hoặc ngày review từng người.

- [x] Phạm vi UNSW-NB15, ba RQ, bốn model, bốn scenario, năm seed.
- [x] Ma trận 80 ID duy nhất; `RUN_MATRIX.csv` và validator.
- [x] Official test không dùng fit/tuning/threshold; LOACO loại held-out trước split/fit.
- [x] IF/AE và preprocessor chỉ fit Normal development-train.
- [x] Threshold từ Normal validation ở 1%/5%; AP và support ghi rõ.
- [x] Kết quả mean/std qua năm seed; không coi LOACO là phát hiện mọi zero-day.

Bản hiện tại tổng hợp kết quả kiểm tra và lời xác nhận của nhóm trưởng. Mẫu hỗ trợ tháng 9, ghi chú nguồn gốc và ô ký cũ được giữ nguyên bên ngoài workspace theo nhật ký di chuyển. Không coi xác nhận nội dung chung là bằng chứng đã ký mọi biên bản hoặc giảng viên đã phê duyệt.
