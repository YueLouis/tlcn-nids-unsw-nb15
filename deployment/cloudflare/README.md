# Cập nhật web NIDS trên Cloudflare

Dùng đúng `deployment/cloudflare/wrangler.json`; tên Worker `attq-nids` là riêng dự án này. URL công khai: https://attq-nids.phttrongtin-nguyen-a46.workers.dev

## Chuẩn bị

- Node.js hiện hành và Wrangler 4; trên máy Tín đang có Wrangler trong `E:\AVDR_Toeic_Ielts\mot-chut-cloudflare\node_modules\wrangler\bin\wrangler.js`. Đường dẫn đó là công cụ dùng chung, không phải nguồn web NIDS.
- Tài khoản Cloudflare đã đăng nhập bằng `wrangler login`, có quyền Workers. Không đưa token vào mã hoặc GitHub.
- Checkout nghiên cứu có `sites/nids-presentation/dist/models/manifest.json` cùng đủ 16 tệp tham số. Nếu checkout mới chưa có model, lấy từ gói offline đã kiểm của nhóm. Mã GitHub chủ ý không chứa model nặng.

## Cập nhật từ 19/11/2026

1. Chỉnh nguồn trong `demo/presentation/`; `ho-so-public.html` là trang hồ sơ public. `ho-so.html` và `ho-so.js` gốc dành cho bản local/offline của nhóm. Giữ PDF chốt và model đã kiểm.
2. Chạy `python -X utf8 scripts/build_public_presentation.py` từ thư mục gốc kho NIDS.
3. Chạy `python -m unittest tests.test_public_privacy -v` và `node tests/test_public_document_guard.mjs`. Builder chỉ nhận tệp trình bày, CSV được chỉ định và model trong manifest; nó dọn PDF, ZIP, MD, `downloads/` và `package-parts/` còn sót trong dist. Gói offline đã chốt giữ nguyên trên Drive hạn chế, không đưa vào build public. `attach_cloudflare_download.py` đã ngừng xuất ZIP công khai; script đóng gói cũ cần snapshot web đầy đủ đã lưu riêng, không dùng dist public mới để tạo gói báo cáo.
4. Chạy `wrangler deploy --dry-run --config deployment/cloudflare/wrangler.json` để kiểm thư mục tài nguyên.
5. Chạy `wrangler deploy --config deployment/cloudflare/wrangler.json`; ghi lại Version ID và URL từ đầu ra.
6. Mở URL public, kiểm Hồ sơ đề tài dẫn tới đúng Drive; dùng tài khoản được mời để mở báo cáo. Kiểm demo RF với hai ngưỡng 1%/5% và AE, model tải đủ, đường model không có trả 404. URL PDF/ZIP/MD và các phần ZIP cũ phải trả 302 sang Drive mà không trả byte tài liệu; `check_cloudflare_public.mjs` kiểm cả điều này bằng HTTP không đăng nhập. Tập lại bằng gói offline đã lưu ở Drive trước buổi báo cáo.

Nếu máy không có `wrangler` trong PATH, dùng `npx wrangler@4` hoặc gọi đường dẫn công cụ hiện có bằng Node. Không cần chạy `wrangler pages` vì bản này dùng Static Assets trên Workers.

Bản web công khai chỉ có trình bày, demo, số liệu CSV và 16 model tham số. Worker chạy trước mọi static asset: tài liệu cũ chuyển sang Drive hạn chế theo `private-documents.json`, các đường demo đi tiếp tới ASSETS. Không ghép ZIP hoặc đọc tài liệu riêng tư từ ASSETS nữa. `download-manifest.json` và `zip-download.mjs` giữ lại làm lịch sử cơ chế cũ; entrypoint không sử dụng chúng. Tài liệu hiện hành: https://drive.google.com/drive/folders/1s5d-14RMFRqoWnEDMVtRtUSsrUeguP_z. CSV được xử lý tại máy người mở. Không dùng fallback SPA cho tệp model bị thiếu, không đặt `Content-Encoding: gzip` cho dữ liệu `.bin.gz` và không bật cache immutable cho tên model cố định.

Để rollback, chọn phiên bản đã kiểm và đã áp dụng giới hạn tài liệu ngày 19/11; bản trước thay đổi này có thể đưa PDF/ZIP nội bộ ra công khai trở lại. Giữ gói offline và biên bản phiên bản trước trong Drive hạn chế; triển khai thành công không có nghĩa nhóm đã duyệt báo cáo hoặc đã gửi email.
