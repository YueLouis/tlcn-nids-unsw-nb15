# Đặc tả trước khi chạy: phân tích overlap đợt 3

Ngày lập: **25/10/2026**. Đây là phân tích hậu nghiệm của công cụ hỗ trợ trên 80 run đã lưu, chưa phải bài bàn giao hay nhận xét của thành viên.

Câu hỏi: tại ngưỡng validation đã khóa, các chỉ số trên mẫu test có cùng 42 feature với tập model thực sự được fit khác thế nào so với phần còn lại? Phân tích này mô tả hai nhóm, không ước lượng tác động nhân quả của việc loại dữ liệu trùng.

- Tái dựng development train/validation bằng `make_development_split`, stratify theo `attack_cat`, seed 42/52/62/72/82; loại held-out trước chia. Kiểm fingerprint cấu hình và dữ liệu, ID tập train với audit partition đã lưu, số dòng và scaler mean/variance trong từng model bundle.
- RF/XGB: tập match là toàn bộ development train. IF/AE: chỉ Normal của development train, đúng phạm vi fit model và preprocessing. Không match với validation hoặc toàn bộ official train thay cho tập fit.
- Match chính xác trên 42 feature raw được pipeline nạp; loại `id`, `label`, `attack_cat`. Không làm tròn hoặc dùng khoảng cách; khử key trùng phía fit để mỗi mẫu test được đếm một lần. Một key có nhãn khác vẫn được tính match feature, không coi đó là cùng nhãn hay cùng sự kiện mạng.
- Với từng run, chia test thành `matched` và `unmatched`; giữ `all` làm đối chứng. Giữ nguyên score, ngưỡng và dự đoán. Kiểm tổng TP/FP/TN/FN và support hai nhóm bằng toàn test, đối chiếu metric gốc.
- Ghi support Normal/known/held-out, confusion counts, precision/recall/FPR/UADR và AP cho từng nhóm. AP chỉ tính một bản sao mỗi record/run. Nhóm không có mẫu số tương ứng ghi thiếu (`NaN`), không đổi thành 0.
- Tổng hợp mean và sample std qua năm seed; ghi min/max support và số seed có metric hợp lệ. Seed dùng cùng official test; std không phải khoảng tin cậy. Nhóm matched thay đổi theo seed và họ mô hình nên không phải tập test chung để xếp hạng công bằng.
- Không retrain, thay seed, tune ngưỡng, chọn cấu hình hay xóa dòng khỏi baseline. Bảo vệ hash raw, run metadata, predictions, metrics, model bundles, audit và mã liên quan trước/sau.

Đầu ra: `docs/evidence/dot_03/overlap_20261025/` gồm CSV từng run, CSV tổng hợp, audit JSON, hình và ghi chú cách đọc. Chỉ chuyển kết quả vào bản PDF **nháp** sau khi kiểm số liệu. Nhóm vẫn cần tự đối chiếu nguồn, viết nhận xét và đọc chéo.
