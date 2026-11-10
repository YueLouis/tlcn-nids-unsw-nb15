# Ghi nhận kiểm tra kỹ thuật - Nguyễn Trọng Tín

**Ngày kiểm tra:** 10/11/2026  
**Cách chuẩn bị:** công cụ hỗ trợ chạy kiểm và soạn ghi nhận theo yêu cầu Tín; Tín chưa xác nhận tự chạy hoặc đọc duyệt ghi nhận này. Đây là bản chuẩn bị cho phần việc của Tín, chưa là bài cá nhân đã nghiệm thu.  
**Phạm vi:** kiểm tra lại artifact đợt 3, rà soát build và bố cục PDF đợt 4/báo cáo tổng.  
**Trạng thái:** ghi nhận kiểm tra kỹ thuật; chưa phải duyệt học thuật, xác nhận hiểu bài hay xác nhận đã nộp cho giảng viên.

## Kết quả

- PDF đợt 3 bản rà soát có 62 trang, SHA-256 `762C9F3E0DB3D73C8A6D2A9764E5D70694C74EB23CAD0E0971D60D3CF1EABEAE`. Kiểm tra lại xác nhận 333 hash đầu vào không đổi, 8 CSV tính lại khớp, 43.840 nhóm lỗi, 1.920 phân vùng đối chiếu metric, 264 ví dụ gần ngưỡng và 3.200 dự đoán phát lại từ 16 bundle khớp trong sai số score `2.2e-7`. Không huấn luyện lại hoặc chọn lại threshold.
- Kiểm tra đợt 3 cũng xác nhận không có lỗi build chặn, 200 liên kết nội bộ và 56 bookmark hợp lệ. Đây là kiểm tra kỹ thuật trên dữ liệu và bundle hiện có, không phải xác thực bằng dữ liệu độc lập hay lưu lượng mạng thật.
- PDF đợt 4 có 63 trang, SHA-256 `2418A29771E701F1FD3D39ADF8F4688D1609DD35C7F85E4BCCAB72B2511275BC`; báo cáo tổng có 57 trang, SHA-256 `3269509F6D6277ADF8ED605FC1C1A935D9F7C447E2F64DBF0C790F16D98D1BA0`. Cả hai build không có lỗi fatal hoặc undefined reference; mỗi bản còn cảnh báo `Underfull \\hbox` trong log.
- Một lượt đối chiếu độc lập ngày 10/11 giữa bảng FPR hai target, recall và UADR trong hai nguồn báo cáo với `docs/reports/DOT_02_TWO_TARGETS.csv` không thấy số lệch. Phạm vi đó chưa phải kiểm hết mọi bảng trong hai PDF.
- Rà cấu trúc trang của hai PDF xác nhận không có trang trắng, ký tự thay thế hoặc text span vượt ngoài khổ trang. Kiểm tra này chưa thay thế lượt xem trực quan từng trang.

## Việc còn mở

- Đợt 4 và báo cáo tổng chưa có bộ đối chiếu toàn bộ bảng số liệu độc lập tương đương đợt 3; cần kiểm các bảng còn lại, hình/bảng và xem trực quan từng trang cùng các đoạn có cảnh báo dàn dòng.
- Cả ba thành viên cần đọc chéo nội dung, ghi nhận xét thật và chốt bản cuối trước khi đổi trạng thái thành đã duyệt hoặc đã nộp.
- Các PDF đợt 3 rà soát, đợt 4 và báo cáo tổng vẫn là bản chờ duyệt/nháp theo hồ sơ hiện tại. Chưa gửi email trong lượt kiểm này.

## Nguồn kiểm tra

- `scripts/audit_dot3_review_delivery.py`
- `scripts/audit_dot3_final.py`
- `scripts/verify_final_diagnostic_tables.py`
- `docs/evidence/dot_03/final_20261030/FRESH_AUDIT.json`
- `docs/evidence/dot_03/session_20261025/FINAL_DIAGNOSTIC_TABLE_CHECK.json`
- `docs/evidence/dot_03/recheck_20261106/recheck_20261109/REPORT_TABLE_CHECK.json`
- `docs/evidence/dot_03/recheck_20261106/review_20261107_v2/DELIVERY_TECHNICAL_CHECK.json`
- Đối chiếu read-only bảng FPR hai target/recall/UADR với `docs/reports/DOT_02_TWO_TARGETS.csv` ngày 10/11/2026; chưa tạo audit artifact riêng.
