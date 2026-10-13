# Trạng thái đồng bộ hồ sơ đợt 2

Cập nhật lúc 01:25 ngày 14/10/2026. Bàn giao Drive còn mở; chưa gửi email hoặc xác nhận giảng viên đã duyệt.

- GitHub main: nội dung đã push tại c0662c6a0ee2a318b4939e27310e7be17a790887. Trước cập nhật này HEAD local/remote cùng là 9c68fa9065ec98c8e3641d0d10d712a54276d816; worktree sạch.
- [02_Bao_cao](https://drive.google.com/drive/u/0/folders/1LzZjXRK7zM_h3ofd0QeRXDs3Y5XswU0Z): đọc lại đủ hai PDF, mỗi tên một bản. [Đợt 2](https://drive.google.com/file/d/10BIGA6jecCcQnlGO2nK-M2QBm0Atj7fc/view) đã mở kiểm tra 30 trang ở lượt trước. SHA-256 local: 77e2a953e30f463aa084a34ec9b44b900bb350a8673ae522d713a6239d190a0c. Chưa tính hash từ bản tải xuống.
- [04_Du_lieu](https://drive.google.com/drive/u/0/folders/1fnffJ8xoVuHnNVeCbMvj3aLMpYBfIkvS): đủ raw train/test CSV, manifest và overlap audit; chưa tính hash từ xa.
- [03_Tai_lieu_tham_khao](https://drive.google.com/drive/u/0/folders/1RgtU5blqKd8NZ51sz-ksGLtHA0a66aFp): đủ ba tên ma trận, metadata và trạng thái nguồn.
- [07_Thu_tu_voi_giang_vien](https://drive.google.com/drive/u/0/folders/1dETJEXQS40jgsYHSaMq-TC0ZXKHSP4-M): đủ PDF comment gốc và bảng yêu cầu/đối chiếu.
- [06_Bao_cao_tien_do](https://drive.google.com/drive/u/0/folders/1ZRB7Oe3OKDpwSAWKV52Z78sH18EHu4Hr): đủ quy ước tích lũy và bảng đối chiếu góp ý.
- [05_Ket_qua_Thi_nghiem](https://drive.google.com/drive/u/0/folders/1OTUR12qsUInUWIW6hxHzHO5bHtq-H8NL): bảng/log đã có; runs chưa xác minh đủ. Các tab lượt 2,13 GB cũ không còn, không có bằng chứng hoàn tất.

Danh mục runs ban đầu: 119 thư mục/74 tên. Mở kiểm kê quan sát được 53 tên đủ bốn loại artifact, LR-XGB-S42 chưa thấy model và 20 tên chưa thấy file. Các quan sát trống có thể do trang chưa nạp đủ; cần kiểm tra sâu trước khi phục hồi hoặc dọn. Không xóa thư mục dựa chỉ vào tên.

Sáu tên thiếu trong danh mục đã bắt đầu phục hồi: CS-IF-S52 báo 4/4; CS-RF-S52, CS-RF-S72, CS-XGB-S62, LD-XGB-S82, LE-AE-S42 còn chạy và thường tải lại file lớn. Model LR-XGB-S42 báo tải xong nhưng chưa thấy trong danh sách đọc lại. Chưa coi là đủ 80 run/320 file từ xa. Phiếu bàn giao trên Drive cần cập nhật phiên bản và kiểm tra lại.

Local đã kiểm tra lại đủ 80 tên run duy nhất/320 artifact, mỗi run đủ bộ bốn file. Kiểm tra kỹ thuật và audit số liệu trước đó đã đạt; không cần huấn luyện lại. Các mục học thuật còn mở được ghi trong PDF và bảng tiến độ. Theo dõi tiếp tục đến khi khôi phục, dọn bản trùng và kiểm chứng bàn giao hoàn tất.

Cập nhật sau lúc 01:33: sáu lượt phục hồi đã đồng loạt báo 4/4. Phiếu bàn giao hiện có phiên bản mới lúc 01:31, 5 KB, tại cùng file cũ; không tạo thêm tên trùng. Sau đó Drive báo ngoại tuyến và danh mục đọc lại chưa hiện các thư mục mới hoặc model vừa bổ sung. Hoàn tất lượt tải chưa thay thế kiểm chứng danh sách từ xa; chưa xác nhận đủ 80/320 và chưa dọn run trùng. Cần chờ Drive kết nối lại, tìm vị trí các lượt vừa hoàn tất rồi đọc lại nội dung trước khi tải thêm.
