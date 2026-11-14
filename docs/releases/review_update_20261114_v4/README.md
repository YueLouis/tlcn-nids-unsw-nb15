# Hồ sơ nhóm — sửa luồng góp ý và liên kết, ngày 14/11/2026

Bản này sửa ba điểm của cửa vào hồ sơ: bổ sung lựa chọn Trâm Anh bị thiếu thẻ HTML, thêm sao chép góp ý kèm tên người ghi và đổi liên kết tương đối trong Markdown tải xuống thành liên kết GitHub. Khi sao chép tự động bị chặn, khung văn bản có sẵn nội dung để người dùng tự nhấn Ctrl+C. Nút tải TXT chỉ báo đã yêu cầu tải; người dùng kiểm tệp trước khi gửi Zalo.

Đây là sửa giao diện/bàn giao. PDF và ZIP nguồn 13/11, 16 model và số liệu thực nghiệm giữ nguyên. Đợt 3 đã gửi ngày 12/11; đợt 4 và tổng vẫn chờ nhóm đọc và duyệt. Trang không tự gửi góp ý hoặc xác nhận đã duyệt.

## Mở và góp ý

1. Mở [hồ sơ nhóm](https://nids-unsw-nb15-tlcn.nttin181.chatgpt.site/ho-so.html), chọn **Tài liệu**, rồi mở đúng PDF.
2. Chọn **Phần từng người** và tên mình để xem trang cần đọc, mã và câu hỏi.
3. Ở **Cần chốt**, chọn tên, ghi tệp/trang cùng nhận xét, bấm **Sao chép góp ý** rồi tự dán vào Zalo. Có thể tải TXT; nếu không thấy tệp thì dùng sao chép. Nội dung chưa gửi đi chỉ ở trang đang mở.

[Phạm vi kiểm trước đó](../review_update_20261114/README.md) và [bản PDF/nguồn 13/11](../review_final_20261113/README.md) được giữ để truy vết. Kiểm bản sửa, triển khai và gói mới được ghi riêng trong thư mục evidence đi cùng tài liệu này.

## Đã kiểm và phần còn mở

- **Triển khai v4 thành công:** [biên bản](evidence/DEPLOYMENT.json). Quyền xem public được giữ nguyên.
- **51 test Python và hai bộ kiểm JavaScript đạt:** [tổng hợp](evidence/VALIDATION_SUMMARY.json). Kiểm góp ý chạy nguyên JS bằng DOM mô phỏng, không thay kiểm trình duyệt thật.
- **HTTP local:** hai Markdown trả 200, nội dung khớp bộ chuyển liên kết; bảng đối chiếu có 63 liên kết tuyệt đối. Xem [biên bản](evidence/LOCAL_HTTP_CHECK.json).
- **HTTP public có xác thực của Sites:** JS, CSS, hai Markdown, manifest và cả bốn PDF đều trả 200, khớp byte build. HTML trả 200, giữ nguyên toàn bộ nội dung nguồn và được nền tảng chèn thêm một script; không khẳng định HTML khớp từng byte. Xem [tải kiểm](evidence/AUTHORIZED_HTTP_CHECK.json) và [kiểm nội dung HTML](evidence/HTML_RESPONSE_CHECK.json). Đây không phải kiểm truy cập ẩn danh hoặc lượt thử giao diện thực tế.
- **Gói offline v4:** `output/review_update_20261114_v4/NIDS_CAP_NHAT_20261114_v4.zip` trong checkout gốc. [Đóng gói](evidence/PACKAGE_CHECK.json) xác nhận CRC, 54 hash, đủ 16 model và nguyên vẹn PDF/ZIP nguồn 13/11. Tệp 80.827.443 byte, SHA-256 `edfedefdd208f9ebf27f890fae25c9129897d054c05b229414d4c34421e11e25`.

**Drive chưa có v4:** công cụ Google Drive đang báo `Unknown tool` dù plugin được liệt kê đã cài. [Gói v3 trên Drive](https://drive.google.com/file/d/1SZlzTmU8x6I-h0NVQ2pZ_DvAreVQHdyK/view) được giữ nguyên; PDF, model và demo của gói đó không thay. Dùng web v4 để chọn đủ ba tên và sao chép góp ý. Không gọi gói cũ trên Drive là v4.

**Giao diện chưa thử lại trực tiếp ở v4:** công cụ trình duyệt không kết nối được do profile đang chạy; chưa xác nhận lại clipboard/tải TXT hoặc không cuộn ở bản sửa mới. Bằng chứng không tràn trang của v3 vẫn ở hồ sơ cũ. Cả ba vẫn cần đọc, ghi góp ý, tập nói và thử HDMI thực tế.

S07 chỉ có bằng chứng từ abstract; phần cứng train lịch sử và thời gian train/suy luận lịch sử còn thiếu; nhóm chưa có traffic độc lập. Phần này tiếp tục khai báo trong bảng đối chiếu, không dùng kết quả kiểm giao diện để điền thay.
