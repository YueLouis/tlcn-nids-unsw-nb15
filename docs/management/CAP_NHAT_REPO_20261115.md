# Cập nhật hồ sơ và quy trình repository — 15/11/2026

Đợt 3 đã gửi ngày 12/11. Ngày 15/11 nhóm nhận nhận xét về repository; phản hồi tích cực về báo cáo và số liệu chưa đồng nghĩa mọi yêu cầu của đợt 3 đã được nghiệm thu. Phần đóng góp cá nhân và quản lý hồ sơ còn cần xử lý.

## Các việc có thể kiểm chứng bằng kho mã

| Nội dung | Thay đổi và bằng chứng |
|---|---|
| Trạng thái công khai | Đính chính tại [phân công nền](PHAN_CONG_NHOM.md). Repo hiện public; chưa đổi private để tránh mất quyền theo dõi khi tài khoản người hướng dẫn chưa được xác nhận. |
| Thư và thông tin liên hệ | Bỏ toàn văn hai thư cũ khỏi tệp hiện hành; bản gốc giữ riêng. Lịch sử Git và một số báo cáo cũ vẫn có dữ liệu cá nhân. Đây mới là giảm công khai ở bản hiện hành, chưa xử lý xong quyền truy cập toàn bộ lịch sử. |
| Quy trình cập nhật | Bổ sung mẫu pull request. Lần sửa này đưa lên nhánh tạm để mở PR vào `main`; giữ bốn nhánh lâu dài `main`, `tramanh`, `vuongthu`, `trongtin`. PR là nơi xem thay đổi và kết quả kiểm, không tự thay review chuyên môn của thành viên. |
| Kiểm tự động | [Workflow](../../.github/workflows/checks.yml) chạy unit test Python, validator protocol và ba bộ kiểm Node trên Windows/Linux; dùng phiên bản thư viện ghi trong hai requirements. Không cần dataset hoặc model riêng, không chạy lại 80 thí nghiệm và không xác nhận chất lượng học thuật bằng CI. Trạng thái chạy thật xem ở tab Actions và Checks của PR. |
| Mốc kiểm thử lịch sử | [Làm rõ log 42/46 bài](../evidence/dot_03/clarifications_20261115/KIEM_CHUNG_MOC_KIEM_THU_20261115.md). Có log local 42 bài, chưa xác định được commit nguồn đúng của lượt đó. |
| Nguồn gói cá nhân | [Đối chiếu ZIP và phiên bản Git](../evidence/dot_03/clarifications_20261115/GIAI_THICH_NGUON_SNAPSHOT_20261115.md). Manifest khớp byte trong ZIP, nhưng có hai HTML chưa tìm được phiên bản tương ứng trong Git. Giữ nguyên ZIP lịch sử. |
| Tích hợp nhánh | [Thử merge ba chiều](../evidence/dot_03/clarifications_20261115/DOI_CHIEU_TICH_HOP_NHANH_20261115.md) ghi rõ xung đột README và hồ sơ được giữ. Khi tích hợp thật, trang gốc giữ vai trò tổng hợp và mỗi hướng dẫn đặt ở thư mục thành viên. |

## Phần đóng góp cá nhân còn mở

Phân công cho một người không chứng minh người đó đã thực hiện. Các tài liệu chuẩn bị, CSV trích từ kết quả chung và nguồn chạy kèm trong gói chỉ giúp tiếp nhận công việc. Ghi đúng tài khoản tải lên cũng chưa đủ để xác nhận người ấy tự viết, tự chạy hoặc hiểu nội dung.

[Đối chiếu hồ sơ từng người](../evidence/dot_03/clarifications_20261115/PHAM_VI_HO_SO_CA_NHAN_20261115.md) ghi các tệp còn thiếu. Trước bước nghiệm thu tiếp theo, từng bạn cần trực tiếp thực hiện và giải thích một phần theo phân công: Anh đối chiếu dữ liệu và giới hạn; Thu đối chiếu một trường hợp kết quả; Tín tự chạy và ghi nhật ký tái lập. Ghi ngày thực hiện thật, đầu vào, kết quả, nguồn đã đọc và mức hỗ trợ đã nhận; đọc chéo bằng nhận xét cụ thể. Không tạo lịch sử ngược ngày hoặc ký xác nhận thay nhau.

Tài liệu này do trợ lý chuẩn bị theo yêu cầu của nhóm trưởng, chưa phải lời xác nhận từng thành viên đã đọc hoặc hoàn thành các việc trên. Không dùng thay cho góp ý thật hoặc quyết định đánh giá của giảng viên.
