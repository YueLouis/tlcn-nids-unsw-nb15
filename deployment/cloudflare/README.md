# Cập nhật web NIDS trên Cloudflare

Dùng đúng `deployment/cloudflare/wrangler.json`; tên Worker `attq-nids` là riêng dự án này. URL công khai: https://attq-nids.phttrongtin-nguyen-a46.workers.dev

## Chuẩn bị

- Node.js hiện hành và Wrangler 4; trên máy Tín đang có Wrangler trong `E:\AVDR_Toeic_Ielts\mot-chut-cloudflare\node_modules\wrangler\bin\wrangler.js`. Đường dẫn đó là công cụ dùng chung, không phải nguồn web NIDS.
- Tài khoản Cloudflare đã đăng nhập bằng `wrangler login`, có quyền Workers. Không đưa token vào mã hoặc GitHub.
- Checkout nghiên cứu có `sites/nids-presentation/dist/models/manifest.json` cùng đủ 16 tệp tham số. Nếu checkout mới chưa có model, lấy từ gói offline đã kiểm của nhóm. Mã GitHub chủ ý không chứa model nặng.

## Cập nhật

1. Chỉnh nguồn trong `demo/presentation/`; giữ PDF chốt và model đã kiểm.
2. Chạy `python -X utf8 scripts/build_public_presentation.py` từ thư mục gốc kho NIDS.
3. Chỉ đóng gói lại khi thay đổi nội dung cần đưa vào ZIP: `python -X utf8 scripts/package_review_update_20261114.py --complete --revision v5` (revision phải có dạng `v4`, `v5`…; chọn số mới nếu tệp đã tồn tại), rồi `python -X utf8 scripts/attach_cloudflare_download.py <đường-dẫn-ZIP-vừa-tạo>`. Nếu chỉ cập nhật hướng dẫn online, có thể giữ gói v4 đã đóng và không chạy lại hai lệnh này; ghi rõ ZIP là ảnh chụp tại lần đóng gói. Gói ZIP được chia thành các phần tĩnh dưới 25 MiB; endpoint download ghép luồng thành một ZIP cho người dùng, không cần thao tác ghép tay.
4. Chạy `wrangler deploy --dry-run --config deployment/cloudflare/wrangler.json` để kiểm thư mục tài nguyên.
5. Chạy `wrangler deploy --config deployment/cloudflare/wrangler.json`; ghi lại Version ID và URL từ đầu ra.
6. Mở URL public, kiểm Hồ sơ nhóm, bốn PDF, demo RF với hai ngưỡng 1%/5% và AE. Kiểm model tải đủ, một đường model không có phải trả 404. Tập lại bằng gói offline trước buổi báo cáo.

Nếu máy không có `wrangler` trong PATH, dùng `npx wrangler@4` hoặc gọi đường dẫn công cụ hiện có bằng Node. Không cần chạy `wrangler pages` vì bản này dùng Static Assets trên Workers.

Bản web là tệp tĩnh và 16 model tham số; chỉ endpoint tải ZIP gọi Worker để ghép các phần thành luồng. CSV vẫn xử lý tại trình duyệt. Khi build/gói, thư mục `package-parts` không được đưa trở lại bên trong ZIP, tránh lặp gói. `deployment/cloudflare/download-manifest.json` lưu hash, dung lượng và thứ tự các phần. CSV được xử lý tại máy người mở. Không dùng fallback SPA cho tệp model bị thiếu, không đặt `Content-Encoding: gzip` cho dữ liệu `.bin.gz` và không bật cache immutable cho tên model cố định.

Để rollback, dùng dashboard đúng Worker, mục Deployments, chọn phiên bản đã kiểm. Giữ gói offline và biên bản phiên bản trước; triển khai thành công không có nghĩa nhóm đã duyệt báo cáo hoặc đã gửi email.
