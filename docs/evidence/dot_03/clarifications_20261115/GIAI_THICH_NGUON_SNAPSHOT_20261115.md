# Nguồn của các gói bàn giao cá nhân

Ngày đối chiếu: 15/11/2026. Các gói ZIP và `CHI_MUC_NGUON.csv` cũ được giữ nguyên; ba CSV `SNAPSHOT_PROVENANCE_*_20261115.csv` là bảng đối chiếu bổ sung, không thay manifest lịch sử.

## Phần kiểm được

| Gói | Dòng trong chỉ mục | Kiểm CRC ZIP | Hash từng dòng khớp byte trong ZIP |
|---|---:|---|---|
| Trâm Anh | 52 | Đạt | 52/52 |
| Vương Thu | 52 | Đạt | 52/52 |
| Trọng Tín | 50 | Đạt | 50/50 |

Ba chỉ mục có các dòng tham chiếu theo phần việc khác nhau, không phải ba tệp hoàn toàn giống nhau. CRC và hash khớp chỉ chứng minh gói tự nhất quán, chưa chứng minh mọi byte xuất phát từ một commit duy nhất hoặc do thành viên tự viết.

## Khác biệt với main đã kiểm

Sau khi chuẩn hóa CRLF/LF, cả ba gói còn năm tệp khác nội dung:

- `src/nids_benchmark/demo.py`, `tests/test_demo_inference.py`, `scripts/demo_server.py`: byte trong ZIP khớp phiên bản tại commit `0856152af5bb37c0a06eb398f92d595ab9a1d400`.
- `demo/index.html`, `demo/lab.html`: chưa tìm được byte tương ứng trong lịch sử Git truy cập được, kể cả sau chuẩn hóa xuống dòng. Đây là nguồn snapshot ngoài các phiên bản Git đã xác định; chưa gán được commit nguồn.

Ngoài năm tệp trên, 18 dòng ở gói Anh, 17 dòng ở gói Thu và 16 dòng ở gói Tín khác hash so với main chỉ vì dạng xuống dòng. Không xem chúng là thay đổi nội dung, nhưng vẫn giữ hash byte gốc để kiểm đúng ZIP.

## Cách sử dụng

Dùng gói cũ để xem hồ sơ đã bàn giao tại thời điểm đóng gói. Muốn chạy phiên bản hiện tại, dùng checkout theo commit được ghi trong biên bản kiểm hiện tại. Không gọi ZIP cũ là bản sao chính xác của main mới và không thay âm thầm tệp trong ZIP để làm khớp main.

SHA-256 trong manifest đo byte tệp; Git blob ID thuộc cơ chế đối tượng của Git. Hai loại hash không dùng thay nhau. Bảng bổ sung ghi cả hai, chỉ khi đã tìm thấy đối tượng tương ứng.

Phạm vi lịch sử đã đối chiếu:

| Nhánh | Commit |
|---|---|
| `main` | `6262444d770012fc4223b6808312ebcb95f458be` |
| `tramanh` | `074f80c1625d9a4fad4f421c1410bd5d759ad47e` |
| `vuongthu` | `ae5f0a8d9cd854e4e717ee1b285d2b2db1c28173` |
| `trongtin` | `a0c62e5d0a131f7c6dc6cfdea819b33fc4c15aab` |
