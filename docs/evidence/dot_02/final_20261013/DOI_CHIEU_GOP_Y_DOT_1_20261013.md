# Đối chiếu góp ý đợt 1 - bản đợt 2 hiệu chỉnh 17/10/2026

Nguồn đối chiếu: email của ThS. Nguyễn Đăng Quang ngày 19/09/2026 và PDF comment gốc `NhomTLCN_TramAnh_VuongThu_TrongTin_dot1-cmts.pdf` (20 trang). Bản gốc được giữ tại `07_Thu_tu_voi_giang_vien` trong thư mục chung.

Bản đợt 2: `NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf`, 37 trang. Bảng đối chiếu trực tiếp nằm ở Mục 3.1, trang in 8 (trang thứ 15 của tệp PDF).

| Góp ý / vị trí bản gốc | Nội dung đã cập nhật | Vị trí trong PDF đợt 2 (trang in) |
|---|---|---|
| Trang 7 và email 19/09: tách đầu việc, nêu cụ thể phần xong/chưa đạt | Tách NIDS, UNSW-NB15, bốn mô hình, mẫu ma trận, metadata và đối chiếu đoạn nguồn; từng dòng có đầu ra, thiếu gì, cách tính và người phụ trách | Mục 3.2-3.3, trang 8-12 |
| Trang 16: giải nghĩa metric dạng long | Giải thích một dòng là một metric tại subset/operating point; kèm support, target FPR và threshold; có ví dụ thật | Mục 6.2, trang 17-19 |
| Trang 17: trình bày từng loại cấu trúc dữ liệu | Tên bốn file/run; key/cột, kiểu, ý nghĩa, ví dụ run.json, metrics.csv và predictions.csv; số dòng prediction 164.664/run | Mục 6.2, trang 17-19 |
| Trang 17: cụ thể test gì, thế nào là PASS | Đủ 17 test thực tế, input/expected/kết quả; phân biệt assertion đạt với độ chính xác của model; lưu log thật | Mục 7.1, trang 20; Phụ lục A |
| Trang 17: scenario được mô tả thế nào | Closed-set và ba LOACO; held-out trước split/fit; support theo scenario; threshold chỉ từ Normal validation | Mục 5.1, trang 15 |
| Trang 17: số liệu/mô tả cụ thể | Audit raw split, 80 run/320 artifact, 16 nhóm mean/std qua 5 seed, FPR 1%/5%, UADR và support, hai hình từ metric thật | Chương 4; Mục 7.2-7.3, trang 21-24 |
| Đối chiếu tài liệu tham khảo cụ thể | Ma trận ghi đoạn/trang, điều kiện, giới hạn; 12/13 nguồn có kiểm đoạn, S07 abstract-only | Chương 2; ND2.6; Phụ lục C, trang in 30 |
| Phân tích số liệu theo lỗi | FN theo category, mean/std năm seed và hai dòng FP/FN truy vết; không đổi threshold/test | Mục 7.4, trang in 25 |
| Yêu cầu báo cáo tích lũy và kế hoạch toàn đề tài | Giữ đặt vấn đề/RQ/lý thuyết từ nền đợt 1; bổ sung phương pháp/kết quả/giới hạn; Gantt baseline 19 tuần; không sửa ngày artifact cho khớp kế hoạch | Chương 1-3 và 4-8 |


Kiểm toàn văn 17/10: 384 giá trị in khớp mức làm tròn; thêm bảng Precision, confusion matrix và Recall/UADR hai target. Bộ 80 run/320 artifact, raw, code/test và đợt 1 không đổi. Log 17 test đạt giữ mốc 13/10. Nhóm còn tự đọc/giải thích và đối chiếu đóng góp; không coi kỹ thuật đạt là nghiệm thu nội dung. S07 chỉ abstract; toàn văn còn mở. Email đã gửi lúc 23:38 ngày 17/10/2026, kèm PDF 37 trang.
