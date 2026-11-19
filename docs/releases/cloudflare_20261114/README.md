# ATTQ NIDS — bản công khai Cloudflare, cập nhật 19/11/2026

## Phạm vi công khai từ 19/11

Web public phục vụ trình bày và demo, CSV số liệu và tham số model. **PDF báo cáo, nguồn ZIP, gói offline và tài liệu ôn được mở trong [Drive hạn chế của nhóm](https://drive.google.com/drive/folders/1s5d-14RMFRqoWnEDMVtRtUSsrUeguP_z)** bằng tài khoản đã được mời. [Hồ sơ đề tài](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so) dẫn tới Drive và bốn nhánh GitHub. Hướng dẫn tự kiểm vẫn có trong Drive/repo và snapshot offline; không còn hiển thị trên hub public.

Builder dùng danh sách tệp cho phép và dọn tài liệu còn sót ở dist. Worker chuyển URL tài liệu cũ, kể cả các phần ZIP, sang Drive mà không đọc hoặc phục vụ byte riêng tư. Các PDF/ZIP đã chốt giữ nguyên. Lệnh kiểm và triển khai hiện hành nằm ở [hướng dẫn Cloudflare](../../../deployment/cloudflare/README.md); các biên bản dưới đây thuộc ngày 14–15/11, không tự xác nhận bản triển khai ngày 19/11.

## Lịch sử hướng dẫn và kết quả kiểm ngày 14–15/11

Các bước tự đọc, góp ý và tải ZIP public bên dưới mô tả snapshot trước khi giới hạn tài liệu ngày 19/11; dùng Drive cho tài liệu hiện hành.

**ATTQ = Anh · Thu · Tín · Quang:** ba thành viên Trịnh Trâm Anh, Hoàng Văn Vương Thu, Nguyễn Trọng Tín thực hiện; ThS. Nguyễn Đăng Quang hướng dẫn. Tên web do nhóm chọn, không thay tên đề tài học thuật hoặc ghi thầy là người thực hiện mã nguồn.

Trình bày và demo: https://attq-nids.phttrongtin-nguyen-a46.workers.dev/

Hồ sơ nhóm: https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so

Bản này dùng Cloudflare Workers Static Assets. Pages không nhận được quyền OAuth sau bước đăng nhập, nên dùng quyền Workers đã có để phục vụ cùng bộ web tĩnh. Không chạy API Python trên Cloudflare; suy luận nằm trong Web Worker tại trình duyệt. Trang không yêu cầu tài khoản ChatGPT.

Các PDF/ZIP nguồn báo cáo 13/11 được giữ trong lịch sử; 16 model seed 42 và kết quả thực nghiệm giữ nguyên. Đợt 3 đã gửi ngày 12/11; đợt 4 và tổng đã có [bộ hoàn chỉnh nội dung ngày 14/11](../final_handoff_20261114/README.md) để nhóm sử dụng và xem lại; email chưa gửi. Trang không tự đồng bộ góp ý hoặc xác nhận đã duyệt.

## Ba bước để nhóm tự đọc

1. Ở **Tài liệu**, mở báo cáo đợt 4, tổng, slide hoặc phiếu phân việc.
2. Ở **Phần từng người**, chọn đúng tên của mình, đọc trang PDF được chỉ, mã liên quan và ba câu hỏi.
3. Ở **Ôn và góp ý**, chọn tên, ghi tệp/trang cùng nhận xét, bấm **Sao chép góp ý** rồi tự dán vào Zalo. Nếu sao chép bị chặn, dùng khung văn bản được chọn sẵn và nhấn Ctrl+C. Tải TXT cần kiểm tệp trong Downloads.

Ngày 15/11 bổ sung nút **Việc tự kiểm** trong phần từng người, dẫn tới đầu vào, ba bước và tệp cần tự viết. [Hướng dẫn tải xuống](../../management/TU_KIEM_CA_NHAN_20261115.md) có cách lưu bằng đúng tài khoản GitHub/Drive. Ba hướng dẫn đã kiểm trên 1366×768, 1440×900 và 1920×1080, không cần cuộn; không ghi nhận thay việc thành viên thực hiện. Bản online có hướng dẫn mới, ZIP v4 giữ nguyên snapshot đã đóng.

## Tự cập nhật về sau

Cấu hình duy nhất: [wrangler.json](../../../deployment/cloudflare/wrangler.json). Lưu tên Worker và URL trong [site.json](../../../deployment/cloudflare/site.json). Đọc [hướng dẫn triển khai](../../../deployment/cloudflare/README.md) trước khi cập nhật. Không chạy lệnh deploy từ dự án web khác và không đổi tên Worker cũ của dự án khác.

Các biên bản ở thư mục evidence chỉ chứng minh phạm vi kiểm được ghi; không thay lượt đọc duyệt và tập báo cáo của thành viên.

## Bộ và kết quả kiểm ngày 15/11

- Gói PDF, nguồn và demo offline v4 có 80.829.337 byte, 55 tệp theo manifest; ngày 15/11 đã tải lại qua URL công khai, kiểm đủ hash và CRC. Từ 19/11 lấy gói này trong [Drive hạn chế](https://drive.google.com/drive/folders/1s5d-14RMFRqoWnEDMVtRtUSsrUeguP_z). Giải nén rồi chạy `CHAY_DEMO.cmd`; cần Python 3 và Chrome/Edge hiện hành.
- [Báo cáo đợt 4, tổng và nguồn hiện hành](../final_handoff_20261114/README.md): đợt 4 có 68 trang, tổng có 62 trang. Mỗi PDF đã đối chiếu 174 dòng bảng, kiểm font nhúng, liên kết và trang thay đổi.
- [Biên bản public](evidence/COMPLETE_PUBLIC_CHECK.json): 55 tài nguyên khớp bản build, đủ 16 model; thực thi worker được phát hành bằng Node và đối chiếu 1.600 dự đoán với Python, không lệch nhãn. Đây không phải kiểm thao tác trong trình duyệt.
- [Biên bản tải gói v4](evidence/PUBLIC_CHECK_20261115_V4.json), [phiên bản triển khai v4](evidence/DEPLOYMENT_20261115_V4.json), [tổng kiểm](evidence/FINAL_VALIDATION_SUMMARY.json).
- [QR trang trình bày](ATTQ_NIDS_QR.png) và [QR hồ sơ nhóm](ATTQ_HO_SO_QR.png) đã giải mã lại đúng địa chỉ ATTQ.

[Bộ Drive hiện hành](https://drive.google.com/drive/folders/1s5d-14RMFRqoWnEDMVtRtUSsrUeguP_z) đã tải lại riêng đủ 11 tệp, đối chiếu SHA-256 và dung lượng đều khớp; cả ba ZIP đạt kiểm CRC theo [biên bản Drive](evidence/DRIVE_DELIVERY_STATUS_20261115.json). Các gói Drive cũ giữ riêng làm lịch sử. Manifest hiện hành đã bỏ đường dẫn cục bộ và tải lại kiểm hash; phiên bản cũ trên Drive vẫn còn trong lịch sử, nên chưa xem là đã xử lý hết dữ liệu riêng tư. [Kiểm trình duyệt thực tế ngày 15/11](evidence/BROWSER_UI_CHECK_20261115.json) đã chạy bảy màn ở 1366×768, 1440×900 và 1920×1080; các màn và kết quả demo không cuộn hoặc cắt nội dung. Lỗi cuộn 4 px ở hai phần cá nhân đã sửa và kiểm lại trên public. Demo RF hai ngưỡng, AE, lớp bị giấu và CSV sai schema đã chạy qua giao diện. Nút sao chép góp ý đã trả thành công với nội dung kiểm kỹ thuật; đã tải TXT bằng trình duyệt và đọc lại tệp UTF-8 trong Downloads; chưa thử HDMI phòng học. Không gửi góp ý thử nghiệm vào Zalo. Các giới hạn dữ liệu và bằng chứng lịch sử vẫn giữ; email đợt 4/tổng chưa gửi.
