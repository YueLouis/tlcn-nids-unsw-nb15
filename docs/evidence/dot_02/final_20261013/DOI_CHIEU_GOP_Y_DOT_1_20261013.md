# Đối chiếu góp ý đợt 1 - bản đợt 2 ngày 13/10/2026

Nguồn đối chiếu: email của ThS. Nguyễn Đăng Quang ngày 19/09/2026 và PDF comment gốc `NhomTLCN_TramAnh_VuongThu_TrongTin_dot1-cmts.pdf` (20 trang). Bản gốc được giữ tại `07_Thu_tu_voi_giang_vien` trong thư mục chung.

Bản đợt 2: `NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf`, 30 trang. Bảng đối chiếu trực tiếp nằm ở Mục 3.1, trang in 7 (trang thứ 12 của tệp PDF).

| Góp ý / vị trí bản gốc | Nội dung đã cập nhật | Vị trí trong PDF đợt 2 (trang in) |
|---|---|---|
| Trang 7 và email 19/09: tách đầu việc, nêu cụ thể phần xong/chưa đạt | Tách NIDS, UNSW-NB15, bốn mô hình, mẫu ma trận, metadata và so sánh toàn văn; từng dòng có đầu ra, thiếu gì, cách tính và người phụ trách | Mục 3.2-3.3, trang 7-10 |
| Trang 16: giải nghĩa metric dạng long | Giải thích một dòng là một metric tại subset/operating point; kèm support, target FPR và threshold; có ví dụ thật | Mục 6.2, trang 15-17 |
| Trang 17: trình bày từng loại cấu trúc dữ liệu | Tên bốn file/run; key/cột, kiểu, ý nghĩa, ví dụ run.json, metrics.csv và predictions.csv; số dòng prediction 164.664/run | Mục 6.2, trang 15-17 |
| Trang 17: cụ thể test gì, thế nào là PASS | Đủ 17 test thực tế, input/expected/kết quả; phân biệt assertion đạt với độ chính xác của model; lưu log thật | Mục 7.1, trang 18-19; Phụ lục A |
| Trang 17: scenario được mô tả thế nào | Closed-set và ba LOACO; held-out trước split/fit; support theo scenario; threshold chỉ từ Normal validation | Mục 5.1, trang 14 |
| Trang 17: số liệu/mô tả cụ thể | Audit raw split, 80 run/320 artifact, 16 nhóm mean/std qua 5 seed, FPR 1%/5%, UADR và support, hai hình từ metric thật | Chương 4; Mục 7.2-7.3, trang 19-21 |
| Yêu cầu báo cáo tích lũy và kế hoạch toàn đề tài | Giữ đặt vấn đề/RQ/lý thuyết từ nền đợt 1; bổ sung phương pháp/kết quả/giới hạn; Gantt baseline 19 tuần; không sửa ngày artifact cho khớp kế hoạch | Chương 1-3 và 4-8 |

Kiểm tra lại ngày 13/10: 80 run, 320 artifact, 17/17 test; 13.173.120 dòng prediction, 1.040 metric, 80 summary và 16 nhóm tổng hợp, không phát hiện sai lệch. SHA-256 raw khớp manifest. PDF không có cảnh báo tràn mép, thiếu glyph hay tham chiếu chưa giải quyết.

Còn mở và đã nêu trong PDF: so sánh toàn văn 13 nguồn; phân tích lỗi sâu và độ nhạy overlap; demo hoàn chỉnh và sản phẩm cuối đề tài. Metadata nguồn đã kiểm chứng không có nghĩa là đã đọc/nghiệm thu toàn văn. Xác nhận nội dung chung qua nhóm trưởng không thay chữ ký từng biên bản hoặc phê duyệt của giảng viên.
