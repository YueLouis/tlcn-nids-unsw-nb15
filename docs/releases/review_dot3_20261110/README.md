# Đợt 3 — bản thống nhất để cả nhóm đọc duyệt

Mở **BAO_CAO_DOT3_CHO_NHOM_DUYET_20261110.pdf**, 62 trang. Đây là bản đã sửa cách dẫn nguồn mốc 09/11; số liệu và 80 run giữ nguyên. Gói này thay bản đọc cũ cho lượt duyệt hiện tại, không ghi đè hồ sơ đã nộp trước đây. Chưa gửi mail trong lượt chuẩn bị này; chờ cả ba đọc, sửa và báo duyệt.

PDF SHA-256: `a3a2cf6bc9a3345978db3b997a561c1015b1d2bcba4e695f27b7c0021ac37d90`

## Mỗi người mở gì trước

| Người | Phần đọc trước | Cần kiểm và giải thích |
|---|---|---|
| Trâm Anh | PDF trang 21–23; bản nháp dữ liệu ở nhánh tramanh | 45 cột/42 feature; 175.341 development và 82.332 test; train/validation/test; loại lớp LOACO trước chia |
| Vương Thu | PDF trang 34, 37–38, 55; bản nháp và CSV ở nhánh vuongthu | Mẫu số FPR/Recall/UADR; AP toàn test khác AP held-out; ID 68699 là FP và 975 là FN |
| Trọng Tín | PDF trang 23, 55, 58–59, 61; bản nháp ở nhánh trongtin | Pipeline không leakage; ví dụ CS-RF-S42 ID 1 đổi threshold; nguồn/hash và tổng hợp góp ý |

Số trang trên là số ở ô chuyển trang PDF. Sau phần được giao, cả ba đọc toàn bộ báo cáo: tên, thuật ngữ, bảng/hình, kết luận và trích dẫn. Ghi điều chưa hiểu hoặc câu cần sửa ngay tại trang tương ứng.

## Link từng phần

- [Drive chung: main và ba phần thành viên](https://drive.google.com/drive/folders/1ISRWybXz0efLyH4i4XsPZTvkQhQ48meA)
- [Drive bản chung main](https://drive.google.com/drive/folders/1Qwx3tQCd5kPXtYwP_0sc2_hluz6Erj2R)
- [Hồ sơ chung trên main](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/main/docs/releases/review_dot3_20261110)
- [Trâm Anh](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/tramanh/docs/group_delivery_20261110/TramAnh)
- [Vương Thu](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/vuongthu/docs/group_delivery_20261110/VuongThu)
- [Trọng Tín](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/trongtin/docs/group_delivery_20261110/TrongTin)

Các bản nháp đã được trợ lý chuẩn bị/tải theo ủy quyền; nhóm bổ sung nhận xét sau khi thực sự đọc. Không cần tự tải lại toàn bộ tệp để chứng minh đã đọc: ghi trang, nguồn đã mở, câu đã sửa và người đọc chéo là đủ rõ việc thực tế.

## Gói tải về

- `DOT3_NGUON_LATEX_20261110.zip`: nguồn LaTeX, hình, tài nguyên và PDF cùng hash.
- `DOT3_GOI_DOC_DUYET_20261110.zip`: PDF, nguồn LaTeX, ba bản nháp theo phân công, CSV ví dụ, các file mã/bảng nhẹ để đối chiếu và kết quả kiểm.
- `MANIFEST.json`: tên, kích thước và SHA-256 của các tệp phát hành.

Đã kiểm 174 dòng bảng khớp nguồn, 200 liên kết nội bộ, 56 bookmark, nguồn hình và bốn ví dụ gần ngưỡng. Không có lỗi biên dịch chặn, ký tự thay thế hoặc chữ vượt khổ trang. Chín thông báo Underfull hbox còn trong log; các trang sửa đã được xem lại. Kiểm kỹ thuật không thay việc cả nhóm đọc duyệt.

## Sau khi đọc

Mỗi bạn ghi ngắn: đã đọc trang nào; một con số/ví dụ đã đối chiếu với file nào; câu muốn sửa; điều chưa hiểu. Vòng đọc chéo: Thu đọc phần Anh, Tín đọc phần Thu, Anh đọc phần Tín. Nhóm thống nhất sửa, kiểm lại PDF và xác nhận đúng phiên bản trước khi Tín yêu cầu gửi email.

Đợt 4, báo cáo tổng và website vẫn là các hạng mục riêng. Việc gói đợt 3 sẵn sàng để đọc không xác nhận toàn bộ môn đã hoàn tất.
