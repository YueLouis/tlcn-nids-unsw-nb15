# Bắt đầu từ đây — bộ chuẩn bị bảo vệ ngày 13/11/2026

Web trình bày: https://nids-unsw-nb15-tlcn.nttin181.chatgpt.site

Ba bạn đọc tài liệu này cùng phiếu phân việc PDF. Bộ này phục vụ đọc duyệt và tập báo cáo; đợt 4 và báo cáo tổng chưa được nhóm duyệt, chưa gửi giảng viên. Đợt 3 đã gửi trong chuỗi thư cũ lúc 23:16 ngày 12/11, kèm đúng PDF 62 trang; chưa có bằng chứng thầy đã đọc hoặc duyệt.

## Mở gì trước

1. Mở web trên laptop. Dùng bảy nút dưới cùng: Bài toán, Dữ liệu, Thực nghiệm, Kết quả, Demo, Hỏi đáp, Tự đánh giá. Không cần tìm nội dung bằng cuộn trang ở các khung đã kiểm.
2. Đọc PDF đợt 4 và báo cáo tổng trong thư mục `reports` của gói bàn giao. Tên `BAN_NHAP` được giữ đến khi cả ba chốt nội dung.
3. Mở `slides/NhomTLCN_slide_du_phong_20261113.pdf` khi cần trình chiếu dự phòng. Đây là slide tĩnh; muốn chạy CSV phải mở web.
4. Ghi góp ý theo mẫu ở cuối. Đọc phần được phân công trước, rồi đọc chéo phần một bạn khác.

## Mỗi người phụ trách phần nào

| Thành viên | Đọc và kiểm | Mở mã/tài liệu | Tự giải thích được |
|---|---|---|---|
| Trịnh Trâm Anh | Nguồn UNSW-NB15, 42 feature, chia tập, giấu lớp, nguy cơ trùng dữ liệu | `docs/group_delivery_20261110/TramAnh/PHAN_CHUYEN_MON.md`, `src/nids_benchmark/data.py`, `src/nids_benchmark/preprocessing.py`; web Dữ liệu và Thực nghiệm | Vì sao bỏ id/label/attack_cat; lớp bị giấu bị loại ở đâu; tại sao test giữ độc lập |
| Hoàng Văn Vương Thu | IF/AE, ý nghĩa score, chọn ngưỡng, FPR/Recall/UADR/AP, phân tích sai số | `docs/group_delivery_20261110/VuongThu/PHAN_CHUYEN_MON.md`, `src/nids_benchmark/evaluation.py`; web Kết quả và Hỏi đáp | Vì sao IF/AE chỉ học Normal; ngưỡng 1%/5% từ đâu; AP cao chưa đủ kết luận phát hiện lớp mới tốt |
| Nguyễn Trọng Tín | RF/XGB, ma trận 80 run, khả năng tái lập, API và demo, ghép kết luận | `docs/group_delivery_20261110/TrongTin/PHAN_CHUYEN_MON.md`, `scripts/demo_server.py`, `demo/presentation/`; web Bài toán, Demo và Tự đánh giá | 80 run được tính thế nào; bản public tính ở đâu; CSV chưa có nhãn có thể kết luận gì |

Số trang theo thứ tự trong trình xem PDF, không phải số in dưới chân trang:

| Bạn | Báo cáo tổng | Đợt 4 |
|---|---|---|
| Anh | 16–19 và 33–36 | 21–24 và 39–42 |
| Thu | 12–14, 19, 24–29; chọn đọc sâu phần phân tích 31–48 | 12–14, 24, 29–34; chọn đọc sâu 37–54 |
| Tín | 12, 20–24 và 53–58 | 12, 25–29 và 59–64 |

Đối chiếu thêm phiếu phân việc đi cùng đúng phiên bản. Không lấy số trang từ bản đợt 3 để tìm trong báo cáo tổng mới.

`main` là tổng nhóm; `tramanh`, `vuongthu`, `trongtin` là ba nhánh theo phân công. Có hồ sơ mã/CSV/ảnh kèm nguồn, không chỉ có một tệp Markdown. Phân công là trách nhiệm kiểm và giải thích; lịch sử commit và thao tác đăng thay theo ủy quyền không tự chứng minh một người đã tự viết hay tự đọc toàn bộ. Không sửa ngược lịch sử đóng góp.

## Tập trình bày một lượt 12–15 phút

| Khoảng thời gian | Người nói | Nội dung và thao tác |
|---|---|---|
| 0–2 phút | Tín | Bài toán: hệ thống có nhận ra loại tấn công chưa xuất hiện lúc học không; mục tiêu là so sánh có kiểm soát |
| 2–5 phút | Anh | Dữ liệu → Thực nghiệm: UNSW-NB15 là benchmark, 42 feature, loại lớp giữ lại trước khi chia tập; test không chọn ngưỡng |
| 5–8 phút | Thu | Kết quả: phân biệt all-test với Normal + lớp bị giấu; giải thích một điểm mạnh và một thất bại, không đọc hết bảng |
| 8–11 phút | Tín | Demo CS–RF cùng dữ liệu, đổi target 5% sang 1%; cho thấy cùng score đổi quyết định vì ngưỡng |
| 11–13 phút | Thu rồi Anh | Tự đánh giá: giới hạn dữ liệu công bố, chưa có traffic độc lập; hướng bổ sung và cách đánh giá công bằng |
| 13–15 phút | Cả ba | Chốt câu trả lời, chuyển Hỏi đáp khi giảng viên yêu cầu |

Đây là lịch tập đề xuất, không phải thời lượng chính thức của khoa. Mỗi người luyện nói bằng ý của mình. Khi chưa hiểu một ý, dừng lại hỏi và sửa trước khi học thuộc câu.

## Kịch bản demo dễ giải thích

1. Chọn **Demo → 1 · Chọn dữ liệu**. Dữ liệu **Normal xen các nhóm tấn công**, kịch bản **CS**, mô hình **RF**, target **5%**, bấm **Chạy suy luận**.
2. Màn **2 · Xem kết quả** hiện 50 dòng. Bản ghi vị trí 1: nhãn Normal, score khoảng **0,705741**, ngưỡng **0,557282**, dự đoán Attack. Đây là **báo động nhầm**, không phải mô hình đúng 100%.
3. Quay **1 · Chọn dữ liệu**, đổi target **1%**, chạy lại. Cùng score, ngưỡng khoảng **0,805367**, dự đoán Normal. Số tổng: TP 39, FP 0, TN 10, FN 1; đổi ngưỡng giảm báo nhầm nhưng có thể bỏ sót.
4. Bấm **Phạm vi demo** để mở nguồn lần chạy và giới hạn. Bấm **Tải kết quả CSV** khi cần đối chiếu từng dòng.
5. Nếu giảng viên đưa CSV: chọn **Mở tệp CSV trên máy…**. Tệp cần đủ 42 feature cùng schema, tối đa 1.000 dòng; không thể đưa tùy ý log mạng hoặc file pcap rồi gọi đó là cùng dữ liệu đầu vào.
6. CSV chưa có `label` vẫn dự đoán Normal/Attack. Không có nhãn đối chiếu thì chưa kết luận độ chính xác hay đúng/sai. `id`, `label`, `attack_cat` chỉ dùng hiển thị/đối chiếu, không vào model.

Bản public tải tham số mô hình và tính trong Web Worker tại trình duyệt; CSV không gửi lên API ngoài. Bản local gốc gọi API Python tại `127.0.0.1:4397`. Cả hai dùng model seed 42 đã lưu, không huấn luyện lại. Đã đối chiếu 32.000 dự đoán trên 1.000 dòng xác định × 16 model × 2 ngưỡng: không lệch nhãn; score có sai số số thực nhỏ. Phép kiểm này không chứng minh độ chính xác trên mọi traffic mới.

## Khi mất mạng hoặc cần phương án dự phòng

Trước buổi báo cáo, tải và giải nén `NIDS_DEMO_OFFLINE_20261113.zip` ra thư mục thường. Máy cần Python 3 và trình duyệt Chrome/Edge hiện hành. Chạy `CHAY_DEMO.cmd`, giữ cửa sổ đó mở, vào địa chỉ được in trong cửa sổ, thường là `http://127.0.0.1:4399/`. Nếu cổng đang bận, chương trình tự chọn cổng trống tiếp theo. Gói có đủ tham số 16 model và CSV mẫu, không cần pip hoặc Internet để suy luận. Không mở `web/index.html` bằng nhấp đúp vì Web Worker cần HTTP.

Trên máy Tín đã có môi trường Python nghiên cứu, có thể chạy từ repository: `python scripts/demo_server.py`, rồi mở `http://127.0.0.1:4397/presentation/`. Bản này cần các `results/runs/*-S42/model_bundle.joblib` và thư viện theo `requirements-repro.txt`.

Nếu không mở được web, dùng PDF slide dự phòng để tiếp tục trình bày phương pháp và kết quả; nói rõ lúc đó đang trình chiếu kết quả đã kiểm, chưa chạy suy luận mới.

## Câu hỏi phải tự trả lời trước buổi báo cáo

- **Ý nghĩa ngoài đời?** So cách nhận diện hoạt động mạng đáng ngờ khi gặp loại tấn công chưa học. Kết quả giúp hiểu hạn chế của mô hình; chưa phải hệ thống bảo vệ mạng triển khai thực tế.
- **LOACO là gì?** Chọn một lớp tấn công, bỏ khỏi vùng phát triển, rồi kiểm trên test có lớp đó. Đây là mô phỏng loại chưa thấy trong benchmark; chưa đủ chứng minh chống mọi zero-day thực tế.
- **Có dataset riêng chưa?** Chưa có bộ traffic độc lập do nhóm thu. Các preset là tập con UNSW-NB15; thêm giao diện demo không biến chúng thành dataset riêng.
- **Phần làm thêm là gì?** Pipeline tái lập, phân tích nhiều seed/ngưỡng/lỗi và demo kiểm thử CSV. Khi được hỏi, chỉ nhận phần có mã và kết quả thực tế; không nhận dữ liệu độc lập hoặc triển khai trực tiếp chưa làm.
- **Có phát triển khóa luận được không?** Có thể đề xuất thu traffic hợp lệ trong lab, bổ sung trích feature tương thích, đánh giá chéo miền/thời gian và độ trễ. Đây là hướng phát triển cần giảng viên duyệt, không phải kết quả đã đạt.
- **Dùng AI bao nhiêu phần trăm?** Không có phép đo đáng tin để gán tùy ý một tỷ lệ. Trình bày các việc đã được hỗ trợ thực tế và phần mỗi người tự kiểm/hiểu/sửa; nếu chưa hiểu thì nói cần bổ sung, không nhận là đã tự làm.

## HDMI và màn hình lớp

Chuẩn bị sạc, một cáp đã thử, PDF và ZIP offline trên máy/USB. Đến sớm, chọn đúng ngõ HDMI của TV/máy chiếu, cắm chắc hai đầu. Dùng **Win + P → Duplicate** nếu muốn cùng hình trên laptop và màn hình lớp; thử **Extend** nếu Duplicate không phù hợp. Nếu không nhận ổn định, thử **1920×1080, 60 Hz**, đổi cổng/cáp và thử trực tiếp màn khác để khoanh vùng.

Không thể kết luận cáp, cổng hay driver hỏng từ mô tả “lúc được lúc không”. Chỉ đánh dấu kiểm thực tế sau khi cắm đúng TV/máy chiếu tại lớp và chuyển đủ bảy mục. Tắt thông báo riêng tư trước khi trình chiếu. Nút gợi ý lời nói cũng hiện lên máy chiếu; cân nhắc tắt trước buổi chính thức.

## Cách ghi góp ý và chốt

Mỗi góp ý ghi: **tên bạn · tên tệp + số trang hoặc tên màn · chỗ chưa ổn · đề xuất sửa · câu chưa hiểu**. Nếu thấy sai số, gửi cả hàng/cột và nguồn đối chiếu. Không sửa thẳng bảng số liệu để “đẹp” hơn.

Đọc chéo: **Thu → Anh; Tín → Thu; Anh → Tín**. Cả ba chốt nội dung cùng phiên bản PDF/SHA trước khi đại diện gửi mail. Ô chưa đọc hoặc chưa hiểu để trống hoặc ghi rõ còn vướng. Không dùng trạng thái “đã kiểm kỹ thuật” thay cho nhóm duyệt, giảng viên duyệt hay đã nộp.

Mẫu phản hồi:

> tên: … | đã đọc tệp/phiên bản: … | phần hiểu được: … | phần còn vướng: … | lỗi/góp ý: … | đồng ý dùng bản này sau khi sửa: …
