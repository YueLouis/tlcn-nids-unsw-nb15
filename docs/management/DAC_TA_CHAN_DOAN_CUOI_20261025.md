# Đối chiếu đầu ra còn thiếu — 25/10/2026

Mục đích: hoàn thành các đầu ra kỹ thuật trong giao thức mục 12–14, RQ_TO_EVIDENCE và bảng T1–T10/hình 1–8 của phân công chi tiết. Không huấn luyện lại, chọn lại threshold hoặc sửa 80 run gốc. Kết quả mới là phân tích hậu nghiệm trên cùng official test.

1. Nối prediction bằng record_id với raw official test; kiểm ID, nhãn, category, role, hai target và metric gốc bằng các hàm đã kiểm trong PR/overlap. Đọc float với round_trip.
2. Phân nhóm riêng theo proto, service và state, trong từng evaluation_role/target/model/scenario/seed. Ghi support, TP/FP/TN/FN; FP rate chỉ trên Normal, FN rate chỉ trên từng vai trò Attack. Tổng support của mỗi chiều phải bằng toàn test; không cộng ba chiều làm ba lần mẫu độc lập.
3. Bảng exploratory chọn nhóm có support tối thiểu 100 mỗi seed, xếp error rate trung bình giảm dần; tối đa sáu nhóm mỗi hình. Luôn có support và sample std, không suy ra nguyên nhân.
4. Chọn tối đa hai FP/FN/TP-heldout thấp ID nhất và ba record gần threshold nhất mỗi role cho seed42/hai target. Giữ raw feature và score/ngưỡng; ví dụ có quy tắc nhưng không đại diện thống kê.
5. Độ ổn định lỗi: số lần sai trên cùng record qua năm seed (0–5); đây là cùng test, không phải năm test độc lập. Đồng thuận: so dự đoán từng cặp model trên cùng record, seed42, giữ cả hai target.
6. Hình: UADR hai target với sample std; Known Recall/UADR cạnh FPR quan sát; confusion matrix CS/ba LOACO seed42/5%; detection heatmap category; biến thiên recall/UADR theo seed; nhóm FP/FN theo proto/service/state.
7. Chi phí: giữ duration_seconds lịch sử đúng nghĩa thời gian cả run, không gọi là thời gian train riêng. Kiểm kích thước bundle. Đo hiện tại cả 80 bundle trên cùng 100 dòng mẫu đã chọn trước: một lượt làm nóng, ba lượt transform + score; không tính load bundle, HTTP/JSON hoặc I/O; không retrain. So score/decision với prediction gốc theo ID ở target5%. Lưu phần cứng hiện tại riêng; không gán cho phần cứng lúc huấn luyện nếu chưa có bằng chứng.
8. Prototype phải có so sánh bốn model cùng CSV, thông tin importance RF/XGB hoặc cách tính score IF/AE, kèm cảnh báo không phải giải thích nhân quả từng dòng. Kiểm API, UI, không có nhãn, lỗi input và artifact parity.

Các Gate cần review/giải thích từ thành viên tiếp tục để mở. S07 chỉ dùng abstract đã đối chiếu; không coi thành toàn văn. Việc chưa có bộ dữ liệu ngoài hoặc live traffic là giới hạn nghiên cứu, không đổi thành kết quả đã làm.
