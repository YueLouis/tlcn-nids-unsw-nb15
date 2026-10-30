# Phần bổ sung ứng dụng — 26/10/2026

Nguồn yêu cầu: Tín góp ý cần nhìn thấy hệ thống, thuật toán/hàm code, nguồn dữ liệu, dữ liệu mẫu, kịch bản demo, kết quả và nhận xét. Tín xác nhận thầy chưa yêu cầu lab tấn công/phòng thủ hoặc tự học; đây là đề xuất của Tín, cho phép làm nếu phù hợp. Chưa có rubric để bảo đảm điểm bonus hoặc kết luận đủ chuẩn 5 tín chỉ.

## Quyết định thực hiện

Bổ sung một phòng demo phát lại bản ghi flow, dùng mô hình thật, cùng hệ thống CSV hiện có. Không đổi tên đề tài, RQ, 80 run hoặc hai PDF đợt 1–2. Không gọi phần này là tấn công đang xảy ra trên mạng thật, IPS, nhận diện chính xác loại mới hay online learning.

1. Bộ tình huống có nguồn và quy tắc chọn trước: Normal, Generic, ba lớp held-out, hỗn hợp, CSV không nhãn và thiếu feature. Chọn theo category/ID từ dữ liệu test, không chọn theo score hay chỉ giữ ví dụ đoán đúng. Đây là demo minh họa, không thêm mẫu test độc lập.
2. Giao diện một tab chia sáu mục bằng nút: thiết lập, kết quả, ghi chú, dữ liệu, mã xử lý và hướng dẫn. Bảng/tài liệu có Trước–Tiếp để không phải cuộn trang dài; hệ thống phát lần lượt kết quả thật, xem cảnh báo và đối chiếu confusion/FPR/recall có mẫu số. Tốc độ phát là tốc độ trình bày giao diện, không phải latency/throughput của NIDS.
3. Ghi chú người xem và xuất hồ sơ phiên demo/CSV. Không dùng dự đoán làm nhãn thật hoặc tự đưa test vào huấn luyện.
4. Bản đồ kiến trúc tới hàm thật: chia dữ liệu, tiền xử lý, fit/score, chọn ngưỡng, API, web, đánh giá. Tách thư viện/thuật toán kế thừa khỏi mã tích hợp và quy trình thí nghiệm của dự án; công cụ hỗ trợ không phải đóng góp cá nhân đã được xác nhận.
5. Hồ sơ nguồn dữ liệu: trang UNSW, bài gốc, official split, mirror khai báo, SHA-256 local, feature/nhãn, duplicate/overlap và giới hạn. Chưa có đối chiếu byte trực tiếp từ file UNSW thì ghi chưa có.
6. Báo cáo bổ sung và kịch bản thuyết trình, ghi số đo sau khi chạy thật. Không sửa ngày lịch sử hoặc gọi phần chuẩn bị là nghiệm thu nhóm.

## Tiêu chí kiểm

- Mẫu có thể truy về ID/category trong official test local, hash đầu vào giữ nguyên.
- Các dòng replay gọi lại bộ suy luận hiện có; không có kết quả dựng sẵn hay nhãn category giả làm dự đoán.
- LOACO chỉ gọi lớp held-out là chưa xuất hiện trong phát triển; binary classifier vẫn trả Normal/Attack.
- CSV chưa có label không có FP/FN hay accuracy được tự tạo.
- Sai schema bị từ chối rõ; export khớp phiên; không sửa baseline hoặc tự gán đóng góp cho thành viên.
- Kiểm API, UI, responsive, gói giải nén và tài liệu trước bàn giao.
