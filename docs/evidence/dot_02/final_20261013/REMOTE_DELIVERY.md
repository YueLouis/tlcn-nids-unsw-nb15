# Trạng thái đồng bộ hồ sơ đợt 2

Cập nhật 02:02 ngày 14/10/2026. **Chưa hoàn tất bàn giao Drive.** Không có xác nhận nộp hoặc giảng viên duyệt.

## Drive

- Lượt kiểm danh mục trước các bổ sung gần nhất: 125 thư mục/80 tên run. Đã quan sát đủ bốn loại artifact tại 68 tên; còn bản trùng, chưa đối chiếu hash từ xa. Số thư mục có tên không thay thế số run đủ file.
- Sáu run phục hồi `CS-IF-S52`, `CS-RF-S52`, `CS-RF-S72`, `CS-XGB-S62`, `LD-XGB-S82`, `LE-AE-S42` đã mở đúng đích và thấy đủ bốn loại file.
- `LR-XGB-S42` đã có model sau khi bổ sung; `LR-XGB-S72` phục hồi đủ bốn file tại thư mục `1Vo31PDb22YN7ExBgJ6jKsKuQLRhGAAql`.
- 12 tên còn chưa đủ bằng chứng: `LE-XGB-S82`, `LE-XGB-S42`, `LE-RF-S72`, `LE-IF-S72`, `LE-IF-S42`, `LE-AE-S72`, `LD-RF-S82`, `LD-RF-S42`, `CS-RF-S62`, `CS-RF-S42`, `CS-IF-S82`, `CS-IF-S62`.
- Đang phục hồi `LE-XGB-S72` và `LE-XGB-S42` bằng tải thư mục; `LE-IF-S42` bằng bốn file vào thư mục đã có. `LE-XGB-S82` đã dùng Thử lại cho prediction sau lỗi; phải chờ xong rồi đọc lại đúng đích. Không khởi động lại các lượt còn chạy.
- `01_De_cuong_Ke_hoach` trên Drive đang hiển thị trống; còn cần bổ sung tài liệu gốc phù hợp cấu trúc.
- `02_Bao_cao`: hai tên PDF, mỗi tên một bản. Đợt 2 đã mở được 30 trang ở lượt kiểm tra trước. [PDF đợt 2](https://drive.google.com/file/d/10BIGA6jecCcQnlGO2nK-M2QBm0Atj7fc/view).
- `04_Du_lieu`: hai raw CSV, manifest và overlap audit, bốn tên. `03_Tai_lieu_tham_khao`: ba tên. `06_Bao_cao_tien_do`: quy ước và đối chiếu góp ý, hai tên. `07_Thu_tu_voi_giang_vien`: comment gốc và bảng yêu cầu, hai tên.
- Phiếu bàn giao có phiên bản 01:31 tại cùng file ID `1c37eZOMLW0JqnFvTcgvG2PUFmnC0xygr`; còn cần cập nhật trạng thái mới. Chỉ chuyển bản trùng đã kiểm chứng vào thùng rác khi đủ bản giữ lại.

[Drive nhóm](https://drive.google.com/drive/folders/13KGqMT4NUr8JfvTpF0IEKfUDT0Dlvq5S) · [Kết quả](https://drive.google.com/drive/u/0/folders/1OTUR12qsUInUWIW6hxHzHO5bHtq-H8NL) · [runs](https://drive.google.com/drive/u/0/folders/15CTWUOaQ_tq95N9fzCP-chk8QHTjC_zu)

## GitHub và local

Trước lần cập nhật này, HEAD local/remote main cùng là `62fde03cb25d2561ccc4a264856c09ee7164a882`, worktree sạch. Không huấn luyện lại. Local đọc lại đủ 80 tên run duy nhất/320 artifact. Các kiểm tra kỹ thuật và audit số liệu trước đó đạt; không suy ra toàn bộ việc học thuật đã hoàn tất.

PDF local/repo kiểm tra lại SHA-256 ngày 14/10: đợt 1 `8a9b77a5cc9c120f6a0d3c603ad69d6eb75a53ef8281ef21f58a754f24739ae6`; đợt 2 `77e2a953e30f463aa084a34ec9b44b900bb350a8673ae522d713a6239d190a0c`. Hai cặp bản sao khớp. Thư mục hỗ trợ cá nhân và lịch sử nháp nằm ngoài workspace; không upload lên Drive/GitHub.

Còn mở: kiểm chứng/hoàn thiện Drive, dọn bản trùng, cập nhật phiếu; so sánh toàn văn 13 nguồn, phân tích lỗi/độ nhạy overlap, demo và bộ cuối đề tài. Chưa gửi email hoặc nộp thay nhóm.

Cập nhật tiếp 02:06: LE-XGB-S72 báo tải xong và đã mở đúng thư mục, thấy đủ bốn file. LE-XGB-S82 và LE-IF-S42 cũng báo tải xong sau xử lý hộp thoại phiên bản/Thử lại, nhưng danh sách đúng đích vẫn chưa nạp đủ; không tải lại các lượt này. Drive tìm kiếm báo "Không thể làm mới; hãy kiểm tra kết nối mạng rồi thử lại". Lượt LE-XGB-S42 đang tải tại tên LE-XGB-S42 (1), chưa đọc lại file và chưa đổi tên/dọn bản cũ. Phiếu Drive đã có phiên bản cập nhật 02:03 tại cùng file ID; phiên bản đó chưa có đoạn 02:06 này. Tiếp tục theo dõi, chưa chốt 80/320 và chưa dọn run trùng. Quan sát đề cương trống vẫn cần kiểm lại khi Drive kết nối ổn định.
