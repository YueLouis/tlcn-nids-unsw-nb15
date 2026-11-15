# Đối chiếu tích hợp ba nhánh cá nhân

Ngày đối chiếu: 15/11/2026. Dùng `git merge-tree --write-tree main <nhánh>` trong kho kiểm độc lập; không thay HEAD, index, nhánh hay nội dung checkout làm việc.

| Nhánh | Kết quả tích hợp thử | Thư mục bàn giao chung |
|---|---|---|
| `tramanh` | Xung đột nội dung `README.md` | Không có thay đổi so với main |
| `vuongthu` | Xung đột nội dung `README.md` | Không có thay đổi so với main |
| `trongtin` | Xung đột nội dung `README.md` | Không có thay đổi so với main |

Cả ba cây tích hợp tạm chỉ có `A BAN_GIAO_BAO_VE_20261115.md` và `M README.md` so với main. Không thấy thao tác xóa hồ sơ Thu, Tín hoặc Anh trong `docs/group_delivery_20261110/` ở các cây này.

So sánh trực tiếp hai đầu nhánh cho thấy những tệp nhánh cá nhân chưa có, nhưng không mô phỏng kết quả merge ba chiều. Vì vậy không dùng riêng `git diff main nhánh` để kết luận merge sẽ xóa hồ sơ thành viên khác.

Chưa thực hiện merge. Khi tích hợp thật cần giải quyết README theo vai trò: giữ trang vào chung trên main, đưa hướng dẫn cá nhân vào đúng thư mục. Cùng tên tệp bàn giao ở gốc cũng cần quyết định vị trí rõ ràng khi tích hợp nhiều nhánh, tránh ghi đè hướng dẫn của người khác.

Phạm vi commit đã đối chiếu:

| Nhánh | Commit |
|---|---|
| `main` | `6262444d770012fc4223b6808312ebcb95f458be` |
| `tramanh` | `074f80c1625d9a4fad4f421c1410bd5d759ad47e` |
| `vuongthu` | `ae5f0a8d9cd854e4e717ee1b285d2b2db1c28173` |
| `trongtin` | `a0c62e5d0a131f7c6dc6cfdea819b33fc4c15aab` |
