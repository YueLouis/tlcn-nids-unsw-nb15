# Trạng thái đồng bộ hồ sơ đợt 2

Cập nhật 03:51 ngày 14/10/2026. **Drive chưa hoàn tất bàn giao.**

## Drive

- Đã quan sát đủ `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib` ở **80/80 tên run**. Đây là kiểm tra sự hiện diện theo thư mục; chưa xác nhận toàn bộ 80 thư mục duy nhất/320 file và chưa tính hash cho toàn bộ Drive.
- Bốn run vừa xác minh thêm: `LE-XGB-S42`, `LE-RF-S72`, `LE-IF-S72`, `LE-AE-S72`. `LE-IF-S72` còn bản lặp trong cùng thư mục.
- `LE-XGB-S42`: đã tải xuống cả bảy file, kiểm CRC và SHA-256 khớp local; chuyển ba bản lặp vào thùng rác có thể khôi phục. Thư mục ID `1zi3UO7ITb4YoI_fEONEk_6qdh4DPDUk_` đã đổi về tên `LE-XGB-S42`, còn đúng bốn artifact.
- `LE-RF-S72` đủ bốn artifact ở ID `1ZrE40Mtr3u_KNOiNZDF8m8TKA5Xp3IYw`, hiện tên `LE-RF-S72 (1)`. `LE-IF-S72` đủ bốn loại ở ID `1DVt5RU8CBkM_fAZfvH07HrlbkO46uK-w`, hiện tên `LE-IF-S72 (1)`. Cần hợp nhất các bản sau khi kiểm nội dung.
- Hai lượt `LD-RF-S82` và `LD-RF-S42 (1)` đã báo 4/4 và đọc lại đủ bốn loại tệp. LD82: ID `1pWRUwh7G5MfmCduTNiElLjW3QYc8bajz` có đúng bốn tệp. LD42: ID `157GMHq8YyWJuamP32nzWN1igmJmw63gA` có bảy tệp, gồm bốn metrics.csv; đã yêu cầu tải các metrics để đối chiếu, còn chờ ZIP. Chưa dọn khi chưa có hash.
- `CS-IF-S62` ở ID `1hrt3Mn5OkydyXOwZrW6_KQKaHWdiYQ-l` đã tải xong và đọc đúng bốn tệp. `CS-RF-S62` ở ID `1Nfst9SQV1EdoORHQiv53xydN9WFPeGUW` đã báo xong 4/4 sau Thử lại predictions.csv do lỗi. Đọc lại năm tệp/bốn loại, gồm hai predictions.csv; chưa hash/dọn bản lặp.
- `CS-RF-S42` ID `1Wi9nIZPqDKT8vz2FigGtXnA_NUQF5fq3`: sau khi làm mới riêng đã đọc được sáu tệp, đủ bốn loại, có hai run.json và hai metrics.csv; chưa đối chiếu hash bản lặp. Không tải lại run này.
- Đã kiểm đúng breadcrumb và thư mục trống trước khi bổ sung riêng bốn tệp vào các ID hiện có. `CS-IF-S82` có bảy tệp/bốn loại ở `1WfnfvgShfd3UoYkFkdWePv0CO4Gxb9AL`; `LE-IF-S42` có năm tệp/bốn loại ở `1lcd2C1fewMXQkGRDwQDh1206rOYvSrik`, lượt tải báo hoàn tất. `LE-XGB-S82` có 11 tệp/bốn loại ở `1URZaCCbb9wgMecduM3ll3KAX8vuGMaXx`; lượt tải đã báo xong 4/4 sau khi dùng Thử lại cho run.json và predictions.csv do lỗi kết nối. Cả ba còn bản lặp chưa đối chiếu hash. Giữ nguyên các lượt đang chạy.
- `01_De_cuong_Ke_hoach` ID `154dxGCWFhjVMx_mvHg2gnWexnc8BjEJ2`: năm tài liệu cấp đầu đã báo tải xong và đọc đủ năm tên, nhưng hiện 20 tệp do bản lặp. PDF đề cương tên nhóm SHA-256 `2be9849ec1b7d6c071e646cc82e74a06a6562d3294158d092a6d43e15e1ac23c` và `00_GIAO_THUC_NGHIEN_CUU.md` SHA-256 `8cf655e87c597acbf1ecdf433c0b69a2b85374daaf062e59535de83e8eef9d7c` tải xuống khớp local. Yêu cầu ZIP và tải hai PDF lặp gặp timeout/lỗi HTTP; chưa dọn các bản đó. Nguồn `De_Cuong_Chi_Tiet_LaTeX` đã báo 6/6 mục (gồm thư mục assets); đọc đủ bốn tên cấp đầu và logo_fithcmute.png ở assets, có ghi chú lịch sử. ID nguồn `12iRUkVmhVLOnmclkSnV3Wa1-x1k4AoAV`; bản lặp trong nguồn chưa dọn.
- Đã yêu cầu tải toàn bộ thư mục runs xuống để kiểm kê/hash lúc khoảng 03:33; Drive từng báo đang nén; sau đó hộp thoại biến mất nhưng chưa thấy ZIP hoặc link tải trong trang/Downloads. Chưa rõ kết quả, không yêu cầu lại mù. Tải riêng Word/protocol lặp cũng gặp lỗi HTTP, chưa dọn bản lặp.
- Trang kiểm tra mới vẫn thiếu đường dẫn hoặc báo Đang xử lý khi xem trước/tải bản lặp; không dùng trạng thái đó để kết luận thư mục trống. Chưa dọn thêm tệp/folder trong lượt này.
- `02_Bao_cao` đã có hai PDF; bản đợt 2 đã mở được 30 trang trước đó. Raw data/manifest/audit có bốn tên; tài liệu tham khảo ba tên; comment/yêu cầu hai tên; quy ước/đối chiếu hai tên. Chưa kiểm hash từ xa các tài liệu này.
- Phiếu Drive ID `1c37eZOMLW0JqnFvTcgvG2PUFmnC0xygr` đã cập nhật thành công qua quản lý phiên bản lúc 03:43; có phiên bản hiện tại và mười bản trước, cùng ID. Nội dung tải lên ghi mốc 80/80, còn CS-RF-S62 đang tải tại thời điểm đó. Cần cập nhật bản cuối sau dọn và kiểm chứng. Không tạo file phiếu mới.

[Drive nhóm](https://drive.google.com/drive/folders/13KGqMT4NUr8JfvTpF0IEKfUDT0Dlvq5S) · [runs](https://drive.google.com/drive/u/0/folders/15CTWUOaQ_tq95N9fzCP-chk8QHTjC_zu) · [PDF đợt 2](https://drive.google.com/file/d/10BIGA6jecCcQnlGO2nK-M2QBm0Atj7fc/view)

## GitHub và local

- GitHub main đã push và đối chiếu remote tại commit `3c03bf4afd2402c33436a7bc8a19a43a4d9ffefc` lúc 03:29 trước lần cập nhật ghi chú này. [Kho mã nguồn](https://github.com/YueLouis/tlcn-nids-unsw-nb15).
- Lần kiểm kỹ thuật khoảng 02:30 ngày 14/10: `check_dot2_final.py` PASS 80 run/320 artifact, unique ID, manifest, 17 test, validator, bảng tổng hợp và PDF. Không huấn luyện lại.
- Hai cặp PDF trong `02_Bao_cao` và repo vẫn trùng SHA-256: đợt 1 `8a9b77a5cc9c120f6a0d3c603ad69d6eb75a53ef8281ef21f58a754f24739ae6`; đợt 2 `77e2a953e30f463aa084a34ec9b44b900bb350a8673ae522d713a6239d190a0c`.
- Audit số liệu trước đó: 13.173.120 prediction, 1.040 metric, 80 summary, 16 nhóm; không phát hiện sai lệch. Không chạy lại huấn luyện khi đồng bộ.
- Hồ sơ hỗ trợ cá nhân, lịch sử nháp và cache nằm ngoài thư mục làm việc; không đưa lên Drive/GitHub. 11 cache phát sinh từ kiểm tra vừa được chuyển ra ngoài và đối chiếu hash.

Còn mở về học thuật: so sánh toàn văn 13 nguồn, phân tích lỗi/độ nhạy overlap, demo và bộ cuối đề tài. Nhóm tự đọc, hiểu và chịu trách nhiệm nội dung. Chưa gửi email, chưa nộp thay nhóm, không có xác nhận giảng viên duyệt.
