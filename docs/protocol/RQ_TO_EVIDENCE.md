# ÁNH XẠ CÂU HỎI NGHIÊN CỨU SANG BẰNG CHỨNG

Tài liệu này khóa ba câu hỏi nghiên cứu chính. Phân tích feature importance và
trường hợp dự đoán sai là nội dung bổ sung, không được gọi là RQ4 nếu đề cương
chưa chính thức bổ sung câu hỏi thứ tư.

| RQ | Câu hỏi | Kịch bản | Bằng chứng chính | Artifact |
|---|---|---|---|---|
| RQ1 | Trong closed-set, bốn mô hình phát hiện Attack như thế nào? | Closed-set | PR-AUC, Recall, Precision, F1, FPR, support; mean và std qua 5 seed | Metrics, confusion matrix, PR curve, bảng tổng hợp |
| RQ2 | Khi một attack class bị loại khỏi phát triển mô hình, mỗi mô hình còn phát hiện được bao nhiêu mẫu của class đó? | LOACO-R, LOACO-D, LOACO-E | UADR/Held-out Attack Recall, Known Attack Recall, FPR; mean và std qua 5 seed | Metrics theo held-out class, score distribution, bảng LOACO |
| RQ3 | Khả năng phát hiện thay đổi thế nào tại cùng ngân sách cảnh báo nhầm? | Closed-set và LOACO | UADR/Known Recall tại threshold chọn trên Normal validation với FPR mục tiêu 1% và 5%; FPR thực tế trên test | Threshold metadata, operating-point table, trade-off plots |

## Phân tích bổ sung

- Feature importance của Random Forest/XGBoost.
- False Positive và False Negative theo `attack_cat`, `proto`, `service`, `state`.
- Score distribution của Normal, known attack và held-out attack.
- Giới hạn do mất cân bằng lớp, tuổi của UNSW-NB15 và thiết kế held-out class.

## Quy tắc diễn giải

- Không gọi LOACO là bằng chứng phát hiện mọi zero-day ngoài thực tế.
- Không dùng Accuracy làm bằng chứng chính khi dữ liệu mất cân bằng.
- Mọi metric phải đi cùng support, scenario, seed và threshold policy.
- So sánh tại cùng FPR target để tránh ưu ái một model bằng threshold khác.

