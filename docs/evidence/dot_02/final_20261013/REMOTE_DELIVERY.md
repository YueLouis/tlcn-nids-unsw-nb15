# Trạng thái đồng bộ hồ sơ đợt 2

Cập nhật 04:46 ngày 14/10/2026. **Drive đã kiểm đủ bộ bàn giao, các bản trùng đã dọn vào thùng rác khôi phục được.**

## Drive

- `05_Ket_qua_Thi_nghiem/runs`: đúng 80 thư mục có tên chuẩn, 320 tệp; mỗi run gồm `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib`. Toàn bộ 320 SHA-256 khớp local.
- Cách kiểm: đọc 496 tệp trước dọn qua ổ Drive đồng bộ; đối chiếu từng tệp với local. Sau giữ bản chuẩn, kiểm hash lại toàn bộ 320 tệp; làm mới web và đọc đủ 80 ID/80 tên duy nhất. Một model gặp lỗi đọc ban đầu đã đọc lại và hash khớp.
- 176 artifact dư, 50 thư mục run dư và 26 tài liệu trùng đã gom thành một gói và chuyển vào Thùng rác lúc 04:34; web xác nhận có nút khôi phục. Không xóa vĩnh viễn, không dọn dựa theo tên.
- Hai PDF, hai CSV raw, manifest/audit, bảng tổng hợp và các tài liệu tham khảo/góp ý đã đối chiếu hash. Đề cương và nguồn LaTeX đã giữ một bản cho mỗi tệp.
- Đã bổ sung các tài liệu học tập nhẹ còn thiếu, phân công có ghi chú lịch sử, ghi âm/thư gốc và log kiểm; không upload thư mục hỗ trợ cá nhân hoặc lịch sử nháp.
- Phiếu bàn giao cập nhật tại cùng file đang có. 00_MO_DAU là điểm mở hồ sơ trên máy và Drive.

## GitHub rồi local

- GitHub main đã push và đối chiếu remote. Ghi chú này mô tả bộ đã kiểm chứng; phiếu tại thư mục bàn giao ghi commit cuối sau push.
- Local: đúng 80 run/320 artifact, không bad run; hai PDF root/repo trùng SHA-256. Mã thí nghiệm không đổi, giữ kết quả 17 test đạt ở lần kiểm trước, không huấn luyện lại.
- PDF đợt 1: 20 trang, SHA-256 `8a9b77a5cc9c120f6a0d3c603ad69d6eb75a53ef8281ef21f58a754f24739ae6`.
- PDF đợt 2: 30 trang, SHA-256 `77e2a953e30f463aa084a34ec9b44b900bb350a8673ae522d713a6239d190a0c`.

[Drive nhóm](https://drive.google.com/drive/folders/13KGqMT4NUr8JfvTpF0IEKfUDT0Dlvq5S) · [GitHub](https://github.com/YueLouis/tlcn-nids-unsw-nb15)

Còn mở về học thuật: so sánh toàn văn 13 nguồn, phân tích lỗi/độ nhạy overlap, demo và bộ cuối đề tài. Nhóm tự đọc, hiểu và chịu trách nhiệm nội dung; bàn giao tệp không thay cho nghiệm thu những phần này.

Chưa gửi email hoặc nộp thay nhóm; không có xác nhận giảng viên duyệt. Nhật ký đối chiếu đầy đủ và lịch sử thao tác được lưu ngoài thư mục làm việc.
