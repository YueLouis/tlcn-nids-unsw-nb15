# Bàn giao cá nhân đợt 3

## Cập nhật ngày 15/11/2026

Đợt 3 đã gửi lúc 23:16 ngày 12/11, kèm [báo cáo 62 trang ngày 11/11](../../../releases/submission_dot3_20261111/README.md). Ngày 15/11 thầy phản hồi tích cực về báo cáo và số liệu, đồng thời góp ý về repository; đây chưa phải xác nhận nghiệm thu toàn bộ đợt 3.

Ba nhánh thành viên đã được tích hợp vào `main` qua [PR #1](https://github.com/YueLouis/tlcn-nids-unsw-nb15/pull/1); [PR #2](https://github.com/YueLouis/tlcn-nids-unsw-nb15/pull/2) ghi nhận đối chiếu tệp bàn giao trên Drive. Bốn nhánh không còn cùng trỏ tới `93d9c13`. Xem [cập nhật repo](../../../management/CAP_NHAT_REPO_20261115.md) để phân biệt thay đổi kỹ thuật với phần còn mở.

Ba tệp tự phân tích hoặc tự chạy trong bảng dưới vẫn chưa có. Đọc [phạm vi hồ sơ cá nhân](../clarifications_20261115/PHAM_VI_HO_SO_CA_NHAN_20261115.md) và [hướng dẫn mở nguồn, demo hiện hành](../../../management/BAN_GIAO_BAO_VE_20261113.md). Ghi ngày thực hiện thật, nguồn đã kiểm, phần được hỗ trợ và nhận xét đọc chéo cụ thể; không dùng tài liệu chuẩn bị hoặc thao tác đăng tải thay cho việc đã trực tiếp làm.

## Khung bàn giao ngày 06–10/11 — giữ để truy vết

Phần bên dưới ghi trạng thái tại thời điểm chuẩn bị khung. Các câu “đang chờ nhóm duyệt”, “chưa đồng bộ” và mốc nhánh `93d9c13` thuộc lịch sử; dùng mục cập nhật phía trên để xem trạng thái hiện hành. Các bản PDF cũ và ghi nhận cũ được giữ nguyên.

Thư mục này là nơi để từng thành viên đưa phần tự đọc hoặc tự chạy của mình vào **bộ chung**. Bản rà soát trình bày 07/11 có 62 trang, đang chờ nhóm duyệt tại mốc đó, ở `docs/report_dot3_review_20261106/build/main.pdf` trên máy local. Khung cũ dẫn tới hướng dẫn và mẫu trắng `docs/management/ban_giao_dot3_review_20261107/DOC_TRUOC.md`; tệp này không có trong repository hiện hành, nên dùng hướng dẫn ở đầu trang. Bản PDF 60 trang ở `docs/releases/dot_03/` được giữ làm lịch sử 30/10. Tại mốc khung cũ, chưa đồng bộ bản rà soát hoặc xác nhận nhóm đã duyệt.

## Ba phần cần bàn giao

| Người | File cần tự viết | Căn cứ bắt đầu | Người đọc chéo |
|---|---|---|---|
| Trịnh Trâm Anh | `tram_anh/ANH_DU_LIEU_VA_GIOI_HAN.md` | PDF rà soát 07/11 trang 21–22, manifest và phần overlap | Vương Thu |
| Hoàng Văn Vương Thu | `vuong_thu/THU_PHAN_TICH_KET_QUA.md` | PDF rà soát 07/11 trang 34 và 55, bảng lỗi/CSV | Trọng Tín |
| Nguyễn Trọng Tín | `trong_tin/TIN_NHAT_KY_TAI_LAP.md` | Demo `CS-RF-S42`, ID 1, target 5% và 1% | Trâm Anh |

Mỗi file phải do người được giao tự viết, ghi ngày, nguồn hoặc trang đã mở, phần được hỗ trợ, điều chưa rõ và nhận xét đọc chéo. Bài yêu cầu chạy demo phải kèm log hoặc ảnh của chính lượt chạy đó.

## Trạng thái ghi nhận trong khung cũ

- Đây là khung bàn giao do Tín chuẩn bị ngày 06/11/2026, không phải bài đã làm của Anh hoặc Thu.
- Bốn nhánh `main`, `tramanh`, `vuongthu`, `trongtin` hiện cùng trỏ tới commit `93d9c13` (10/11/2026); lịch sử commit riêng của ba bạn chưa được chứng minh. Xem hướng dẫn theo từng nhánh tại `docs/group_delivery_20261110/`.
- Chưa được ghi `PASS` cho thành viên nào chỉ vì file kỹ thuật của nhóm đã kiểm.
- Không tạo commit hoặc Drive upload dưới tên Anh/Thu thay cho hai bạn.
- Sau khi từng bạn tự hoàn thành, dùng nhánh/tài khoản của người làm để commit file tương ứng, tải cùng file vào thư mục Drive cá nhân trong bộ đợt 3, rồi ghi link commit và link Drive vào nhóm.
- Giao diện `Create new file` hoặc Settings không đủ chứng minh push thành công; chỉ ghi nhận khi commit xuất hiện trên đúng nhánh với đúng tài khoản tác giả.
- Tín chỉ tích hợp vào PDF chung sau khi có bài thật và nhận xét đọc chéo cụ thể.

## Tiêu chí nhận bài

Một phần được tính là đã bàn giao khi có file do đúng người tự viết, căn cứ kiểm được, commit của người làm hoặc xác nhận file do người làm gửi, bản Drive tương ứng, và nhận xét đọc chéo có câu/số liệu cụ thể. Nếu còn vướng thì ghi rõ vướng mắc để cả nhóm gỡ tiếp.
