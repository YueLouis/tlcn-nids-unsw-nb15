# Bộ chuẩn bị bảo vệ — ngày 13/11/2026

[Web trình bày và suy luận public](https://nids-unsw-nb15-tlcn.nttin181.chatgpt.site) · [Drive cùng phiên bản](https://drive.google.com/drive/folders/1d-m5b35FVvGU3AEuA8vx1c9btG5xznUl) · [Hướng dẫn ba thành viên](../../management/BAN_GIAO_BAO_VE_20261113.md)

Đợt 4 và tổng dưới đây là bản sẵn sàng đọc duyệt, **chưa được nhóm duyệt và chưa gửi giảng viên**. Đợt 3 giữ nguyên bản đã gửi ngày 12/11; không dùng bản mới để thay lịch sử đã nộp.

| Mở tệp | Nội dung |
|---|---|
| [Báo cáo đợt 4](reports/NhomTLCN_dot4_BAN_NHAP_20261113.pdf) | 68 trang, 174 dòng bảng đã đối chiếu |
| [Báo cáo tổng](reports/NhomTLCN_tong_BAN_NHAP_20261113.pdf) | 62 trang, 174 dòng bảng đã đối chiếu |
| [Slide PDF dự phòng](slides/NhomTLCN_slide_du_phong_20261113.pdf) | 9 trang 16:9, nền sáng; không chạy được suy luận mới trong PDF |
| [Phiếu phân việc và ôn nhóm](slides/NhomTLCN_phan_viec_on_nhom_20261113.pdf) | 2 trang: từng người mở đâu, đọc trang nào, cần tự trả lời gì |
| [Nguồn đợt 4](reports/Nguon_dot4_BAN_NHAP_20261113.zip) / [nguồn tổng](reports/Nguon_tong_BAN_NHAP_20261113.zip) | Nguồn XeLaTeX và ảnh trong cùng ZIP, manifest SHA-256 |
| [Nguồn slide và phiếu](slides/Nguon_slide_va_phan_viec_20261113.zip) | Hai nguồn TeX chỉnh sửa được |

Gói đầy đủ `NIDS_BAN_GIAO_20261113.zip` trên Drive gồm các tệp trên và ZIP demo offline. Gói offline có 16 bộ tham số model seed 42, CSV mẫu và trình phục vụ loopback bằng thư viện chuẩn Python; cần Python 3 và Chrome/Edge hiện hành, không cần cài thư viện học máy. Giải nén rồi chạy `CHAY_DEMO.cmd`, mở địa chỉ in trong cửa sổ. Cổng mặc định 4399 tự đổi khi đang bận. Không mở HTML bằng nhấp đúp.

Web có 7 màn điều khiển bằng nút. Demo chia Chọn dữ liệu / Xem kết quả / Phạm vi demo; đổi cấu hình vô hiệu kết quả cũ. Bản public tính tại trình duyệt từ tham số đã xuất, CSV không gửi lên API ngoài. Bản local gốc gọi Python API tại `127.0.0.1:4397`; đọc cách chạy trong README gốc. Dữ liệu mẫu là tập con UNSW-NB15, chưa phải traffic độc lập do nhóm thu.

Bằng chứng trong `evidence/`: triển khai public thành công; 32.000 dự đoán so với Python không lệch nhãn trong phạm vi mẫu kiểm; chạy thực tế cả 4 họ model trên public, dữ liệu chưa nhãn, lỗi schema và tải CSV. API local đối chiếu 3.200 dự đoán/32 trường hợp, 46 unit test và ma trận 80 run đạt. Kiểm này không xác nhận độ chính xác với mọi dữ liệu mới hoặc mức hiểu của thành viên.

SHA-256 của từng PDF nằm trong `reports/*_DRAFT_CHECK.json` và `slides/SLIDES_CHECK.json`. Đã kiểm font nhúng, liên kết/mục lục, hình/bảng và xem tất cả trang; các kiểm kỹ thuật không thay lượt nhóm đọc chéo. Chưa thử cáp HDMI/máy chiếu thật, chưa có dữ liệu mạng độc lập hoặc chấp thuận mới của giảng viên.

## Tái tạo bản trình bày

Nguồn giao diện nằm ở `demo/presentation/`. `scripts/prepare_presentation_20261112.py` tái tạo HTML từ `template.html` được version hóa; không cần chạy khi chỉ mở demo. `scripts/export_browser_models.py` cần các bundle gốc trong `results/runs/` để xuất 16 model; `scripts/build_public_presentation.py` ghép code/assets/cases vào checkout hosting riêng. Không đưa tham số nặng hoặc Git hosting lồng nhau vào kho mã học thuật.

`node tests/test_browser_engine.mjs` kiểm schema/CSV/cột cấm/nhãn/ngưỡng. Kiểm parity đầy đủ cần model đã xuất và fixture do `scripts/prepare_browser_parity.py` tạo; sau đó chạy `node scripts/check_browser_parity.mjs`. Toàn bộ kết quả benchmark gốc giữ nguyên.
