# Gate 2 - Data contract và pipeline

**Cập nhật sau trao đổi ngày 17/10/2026:** nhóm trưởng cho biết chưa chắc mức hiểu của từng thành viên; cả nhóm dự kiến tự rà soát đợt 1 và đợt 2 ngày 18/10 sau khi nghỉ ngơi. Do đó, lời báo đã đồng ý trước đó không được dùng để kết luận đã đọc, giải thích được hoặc nghiệm thu nội dung. **Kiểm kỹ thuật đã thực hiện; rà soát nội dung của nhóm còn mở; email giữ nháp, chưa gửi.** PDF 32 trang ngày 14/10 giữ nguyên để nhóm kiểm lại. Xem `HUONG_DAN_RA_SOAT_HAI_DOT_20261018.md` trong thư mục quản lý nhóm.

Phần bên dưới giữ các mốc kiểm tra và lời báo trước đó để truy vết; trạng thái hiện tại theo cập nhật trên.

Cập nhật 13/10/2026.

**Bằng chứng kỹ thuật:** PASS trong phạm vi kiểm tra tự động. **Xác nhận nội dung:** nhóm trưởng cung cấp thông tin cả ba thành viên đã xác nhận; xem `../evidence/dot_02/final_20261013/XAC_NHAN_NHOM_20261013.md`. Không tạo chữ ký hoặc ngày review từng người.

- [x] Raw train/test đúng manifest, SHA-256 kiểm tra lại khớp.
- [x] 175341/82332 dòng, 45 cột; zero missing/infinity.
- [x] 42 feature; id/label/attack_cat là metadata/target; proto/service/state categorical.
- [x] Duplicate được đếm ba cách; overlap test/train 8541/82332 là giới hạn.
- [x] Pipeline fit đúng partition theo protocol; 17/17 test PASS.
- [x] 80 run completed, đủ 320 artifact bắt buộc.

**Còn mở về nghiên cứu:** chưa định lượng ảnh hưởng overlap bằng thí nghiệm độ nhạy. Không dùng checklist pipeline để kết luận feature overlap vô hại.

Bản hiện tại tổng hợp kết quả kiểm tra và lời xác nhận của nhóm trưởng. Mẫu hỗ trợ tháng 9, ghi chú nguồn gốc và ô ký cũ được giữ nguyên bên ngoài workspace theo nhật ký di chuyển. Không coi xác nhận nội dung chung là bằng chứng đã ký mọi biên bản hoặc giảng viên đã phê duyệt.
