# Rà soát hai đợt trước khi nộp - dự kiến 18/10/2026

Trạng thái ngày 17/10: nhóm chưa hoàn tất tự kiểm mức hiểu. Đây là hướng dẫn đọc và kiểm lại, không phải biên bản đã nghiệm thu. Bắt đầu sau khi nghỉ ngơi; có thể chia thành các lượt ngắn và dành thêm thời gian ở phần chưa hiểu.

## Mở đúng hai bản

- Đợt 1: `NhomTLCN_TramAnh_VuongThu_TrongTin_dot1.pdf`, 20 trang, bản lịch sử. Các nhận xét của thầy giữ ở `07_Thu_tu_voi_giang_vien`.
- Đợt 2: `NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf`, 32 trang, tích lũy từ đầu đến mốc 11/10; hoàn thiện kỹ thuật 14/10.
- Đọc Mục 3.1 đợt 2 (trang vật lý 12) cùng comment gốc; tiếp đến Chương 4-7, Mục 7.4 (trang 27), kết luận (trang 28) và Phụ lục C (trang 32).
- Kết luận PDF mô tả trạng thái xác nhận tại ngày 14/10. Chỉ cập nhật trạng thái nghiệm thu sau khi nhóm thực sự đọc lại; không xem ghi chú cũ hoặc kết quả test là bằng chứng từng người đã hiểu.

## Chia phần theo phân công hiện có

| Người | Phần cần tự kiểm và giải thích | Bằng chứng cần tự mở |
|---|---|---|
| Trâm Anh | NIDS/flow; nguồn dữ liệu; 45 cột gồm 42 feature và 3 metadata; ma trận tài liệu và giới hạn S07 | Chương 1-4, Phụ lục C; ma trận 13 nguồn; manifest; nguồn gốc được dẫn URL/trang |
| Tín | Closed-set/LOACO; thứ tự loại held-out, chia dữ liệu, fit và chọn threshold; cấu trúc bốn artifact | Chương 5-6; `data.py`, `runner.py`, `preprocessing.py`; run CS-RF-S42 |
| Vương Thu | Score RF/XGB/IF/AE; AP, FPR, UADR; mean/std; lỗi theo category và các giới hạn so sánh | Chương 6-8; `models.py`, `evaluation.py`; metrics và category-error CSV |

Mỗi người giải thích bằng lời của mình, mở đúng bằng chứng và sửa được một ví dụ nhỏ. Cả ba cần nắm các ý chung dưới đây; chưa hiểu phần nào thì ghi đúng phần đó để học/sửa, không xác nhận thay nhau.

## Tự trả lời trước, rồi đối chiếu

1. Đợt 1 đã có gì, đợt 2 bổ sung gì và thầy góp ý ở đâu? Đợt 1 là phạm vi/protocol/khung kiểm; đợt 2 có dữ liệu thật, pipeline, 80 run, schema, test và kết quả. Dùng bảng Mục 3.1 để chỉ ra từng thay đổi; không sửa lịch sử đợt 1 thành kết quả chạy tháng 9.
2. Vì sao có 80 run và 320 file? Bốn scenario × bốn model × năm seed; mỗi run có run.json, metrics.csv, predictions.csv, model_bundle.joblib. 164.664 dòng prediction/run là 82.332 record ở hai target, không phải 164.664 record độc lập.
3. LOACO khác closed-set thế nào? Loại một attack category khỏi official train trước chia development 80/20 phân tầng attack_cat; official test vẫn giữ đủ 82.332 record. Held-out không tham gia fit preprocessing/model/chọn ngưỡng. LOACO chưa chứng minh phát hiện zero-day ngoài thực tế.
4. Tại sao bỏ id/label/attack_cat khỏi feature? id để truy vết, label là đáp án, attack_cat dùng chia scenario/phân tích; đưa chúng vào feature có thể làm sai phép đánh giá. Còn 42 feature, trong đó proto/service/state là categorical.
5. Bốn model tạo score ra sao? RF/XGB: xác suất Attack; IF: âm decision_function; AE: MSE tái tạo đầu vào. Score càng cao càng giống Attack. Với IF/AE, preprocessor và model fit Normal train; ngưỡng dùng Normal validation.
6. Target FPR 5% có nghĩa FPR test phải bằng 5% không? Không. Ngưỡng thỏa ngân sách trên Normal validation; test có thể khác. Ví dụ CS-RF-S42 target 1%: threshold 0,8053672551; FPR test khoảng 4,22%. Ở target 5%, FPR test RF/XGB closed-set trung bình khoảng 18,57%/18,71%. Không gọi là so sánh tại cùng FPR test thực tế.
7. FPR, UADR và AP có mẫu số/ý nghĩa gì? FPR=FP/37.000 Normal; UADR=TP trên đúng held-out/support held-out (LR 3.496, LD 4.089, LE 11.132). CS không có held-out nên UADR null. Cột pr_auc hiện dùng average_precision_score, tức AP. Năm seed dùng cùng official test; std không phải độ bất định trên năm test độc lập.
8. Chỉ ra một lỗi thật và một giới hạn quan trọng? CS-RF-S42, target 5%: record 1 Normal có score 0,705741 vượt ngưỡng 0,557282 nên FP. 8.541 dòng test có feature vector xuất hiện ở train; chưa có thí nghiệm loại trùng để định lượng tác động. Chưa được suy diễn nguyên nhân hoặc ưu thế tổng quát từ recall cao.
9. Một citation hỗ trợ câu nào, ở trang nào, có gì chưa đọc? Tự mở nguồn phần mình phụ trách bằng ma trận. Hiện 12/13 nguồn có đối chiếu đoạn nội dung; S07 chỉ abstract, chưa toàn văn. Không gọi kiểm metadata/đoạn nguồn là đã đọc và nghiệm thu toàn bài.
10. 17 test PASS chứng minh gì? Các assertion trên dữ liệu tổng hợp về contract, split, threshold, support, chiều score và phạm vi fit; không chứng minh accuracy cao, không thay nghiệm thu nhóm. Mở một test và đổi một input để tự dự đoán kết quả trước khi chạy.

## Trước khi bấm gửi

Ghi lại phần đã thực sự đọc, câu chưa giải thích được và chỗ cần sửa; kiểm cả tên/MSSV/phân công có phản ánh đúng công việc thực tế. Nếu mô tả đóng góp chưa đúng, sửa theo thực tế trước khi nộp. Sau rà soát, đối chiếu trạng thái xác nhận trong PDF, ghi chú và mail; nếu cần sửa PDF thì thay đúng cả local/repo/Drive/tệp đính kèm. Không đổi dữ liệu hoặc kết quả gốc để làm đẹp báo cáo.

Mail đang nháp; chưa gửi. Các giới hạn nghiên cứu phải được giữ rõ. Nhóm trả lời trung thực khi giảng viên hỏi về cách thực hiện và phần hỗ trợ; không dùng tài liệu này để học thuộc lời xác nhận thay cho hiểu bài.
