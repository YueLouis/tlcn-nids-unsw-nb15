# Trạng thái đồng bộ hồ sơ đợt 2

Cập nhật 02:31 ngày 14/10/2026. **Drive chưa hoàn tất bàn giao.**

## Drive

- Đã quan sát đủ `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib` ở **72/80 tên run**. Đây là kiểm tra sự hiện diện theo thư mục; chưa xác nhận toàn bộ 80 thư mục duy nhất/320 file và chưa tính hash cho toàn bộ Drive.
- Bốn run vừa xác minh thêm: `LE-XGB-S42`, `LE-RF-S72`, `LE-IF-S72`, `LE-AE-S72`. `LE-IF-S72` còn bản lặp trong cùng thư mục.
- `LE-XGB-S42`: đã tải xuống cả bảy file, kiểm CRC và SHA-256 khớp local; chuyển ba bản lặp vào thùng rác có thể khôi phục. Thư mục ID `1zi3UO7ITb4YoI_fEONEk_6qdh4DPDUk_` đã đổi về tên `LE-XGB-S42`, còn đúng bốn artifact.
- `LE-RF-S72` đủ bốn artifact ở ID `1ZrE40Mtr3u_KNOiNZDF8m8TKA5Xp3IYw`, hiện tên `LE-RF-S72 (1)`. `LE-IF-S72` đủ bốn loại ở ID `1DVt5RU8CBkM_fAZfvH07HrlbkO46uK-w`, hiện tên `LE-IF-S72 (1)`. Cần hợp nhất các bản sau khi kiểm nội dung.
- Hai lượt `LD-RF-S82` và `LD-RF-S42 (1)` đang tải trên tab 14, mỗi lượt 2/4; không tải lại hoặc đóng/reload tab.
- Tám tên chưa đủ bằng chứng: `LE-XGB-S82`, `LE-IF-S42`, `LD-RF-S82`, `LD-RF-S42`, `CS-RF-S62`, `CS-RF-S42`, `CS-IF-S82`, `CS-IF-S62`.
- `LE-XGB-S82` và `LE-IF-S42` từng báo tải hoàn tất nhưng đúng đích vẫn chưa hiện đủ file; cần định vị lại khi kết nối ổn định. Đã chọn thư mục để tải `CS-RF-S62` và `CS-IF-S82` một lần trong phiên này, nhưng chưa thấy chúng trong tiến trình; chưa tải lại khi chưa biết kết quả.
- Drive tìm kiếm báo không thể làm mới. `01_De_cuong_Ke_hoach` chưa nạp được nội dung; tài liệu gốc có tại local, chưa tải đề cương trong phiên này.
- `02_Bao_cao` đã có hai PDF; bản đợt 2 đã mở được 30 trang trước đó. Raw data/manifest/audit có bốn tên; tài liệu tham khảo ba tên; comment/yêu cầu hai tên; quy ước/đối chiếu hai tên. Chưa kiểm hash từ xa các tài liệu này.
- Phiếu Drive ID `1c37eZOMLW0JqnFvTcgvG2PUFmnC0xygr` vẫn là phiên bản 02:03; bản đó cũ hơn trạng thái local hiện tại và cần cập nhật.

[Drive nhóm](https://drive.google.com/drive/folders/13KGqMT4NUr8JfvTpF0IEKfUDT0Dlvq5S) · [runs](https://drive.google.com/drive/u/0/folders/15CTWUOaQ_tq95N9fzCP-chk8QHTjC_zu) · [PDF đợt 2](https://drive.google.com/file/d/10BIGA6jecCcQnlGO2nK-M2QBm0Atj7fc/view)

## GitHub và local

- GitHub main đã đối chiếu với remote tại commit `bb02e7cdc4987d3f4b181b85b17b1cfda6c5af0e` trước lần cập nhật ghi chú này. [Kho mã nguồn](https://github.com/YueLouis/tlcn-nids-unsw-nb15).
- Local kiểm lại trong phiên này: `check_dot2_final.py` PASS 80 run/320 artifact, unique ID, manifest, 17 test, validator, bảng tổng hợp và PDF. Không huấn luyện lại.
- Hai cặp PDF trong `02_Bao_cao` và repo vẫn trùng SHA-256: đợt 1 `8a9b77a5cc9c120f6a0d3c603ad69d6eb75a53ef8281ef21f58a754f24739ae6`; đợt 2 `77e2a953e30f463aa084a34ec9b44b900bb350a8673ae522d713a6239d190a0c`.
- Audit số liệu trước đó: 13.173.120 prediction, 1.040 metric, 80 summary, 16 nhóm; không phát hiện sai lệch. Không chạy lại huấn luyện khi đồng bộ.
- Hồ sơ hỗ trợ cá nhân, lịch sử nháp và cache nằm ngoài thư mục làm việc; không đưa lên Drive/GitHub. 11 cache phát sinh từ kiểm tra vừa được chuyển ra ngoài và đối chiếu hash.

Còn mở về học thuật: so sánh toàn văn 13 nguồn, phân tích lỗi/độ nhạy overlap, demo và bộ cuối đề tài. Nhóm tự đọc, hiểu và chịu trách nhiệm nội dung. Chưa gửi email, chưa nộp thay nhóm, không có xác nhận giảng viên duyệt.
