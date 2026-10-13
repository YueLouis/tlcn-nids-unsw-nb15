# Gate 1 - Protocol

Cập nhật 13/10/2026.

**Bằng chứng kỹ thuật:** PASS trong phạm vi kiểm tra tự động. **Xác nhận nội dung:** nhóm trưởng cung cấp thông tin cả ba thành viên đã xác nhận; xem `../evidence/dot_02/final_20261013/XAC_NHAN_NHOM_20261013.md`. Không tạo chữ ký hoặc ngày review từng người.

- [x] Phạm vi UNSW-NB15, ba RQ, bốn model, bốn scenario, năm seed.
- [x] Ma trận 80 ID duy nhất; `RUN_MATRIX.csv` và validator.
- [x] Official test không dùng fit/tuning/threshold; LOACO loại held-out trước split/fit.
- [x] IF/AE và preprocessor chỉ fit Normal development-train.
- [x] Threshold từ Normal validation ở 1%/5%; AP và support ghi rõ.
- [x] Kết quả mean/std qua năm seed; không coi LOACO là phát hiện mọi zero-day.

Bản hiện tại tổng hợp kết quả kiểm tra và lời xác nhận của nhóm trưởng. Mẫu hỗ trợ tháng 9, ghi chú nguồn gốc và ô ký cũ được giữ nguyên bên ngoài workspace theo nhật ký di chuyển. Không coi xác nhận nội dung chung là bằng chứng đã ký mọi biên bản hoặc giảng viên đã phê duyệt.
