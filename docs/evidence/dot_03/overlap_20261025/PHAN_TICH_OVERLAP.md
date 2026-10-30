# Kết quả phân tích overlap — 25/10/2026

Đã kiểm 80 run, 13.173.120 dòng prediction, 1.040 metric; input/model giữ nguyên. Không huấn luyện hoặc chọn lại ngưỡng. Match đúng 42 feature raw với tập fit thực tế: RF/XGB dùng development train, IF/AE chỉ Normal.

CSV có 480 dòng run/target/cohort và 96 nhóm tổng hợp. Các chỉ số thiếu mẫu số là NaN; AP yêu cầu cả hai nhãn. Năm seed cùng test, std không là khoảng tin cậy.

## Ví dụ cách đọc

- Closed-set RF, target validation 5%: FPR matched 22,55%, unmatched 18,41%; recall Attack 99,77% / 96,69%. Đây là hai nhóm khác thành phần, không xác lập nhân quả.
- LR RF, cùng target: held-out unmatched 3.249–3.266 mẫu, UADR 97,56% ± 0,32 điểm phần trăm. UADR cao vẫn hiện diện ngoài exact feature matching nhưng chưa chứng minh khái quát ngoài official split.
- IF/AE không có held-out matched ở ba LOACO; UADR nhóm đó không xác định, không phải 0. Trên hình không có cột cho nhóm không xác định.

Đặc tả trước khi chạy: `docs/management/DAC_TA_OVERLAP_DOT_03_20261025.md`. Audit đối chiếu scaler, row count, ID partition và hash từng run. Khác biệt nhóm không phải tác động loại overlap; chưa retrain loại trùng. Đây là tài liệu chuẩn bị có hỗ trợ công cụ, chưa là review của thành viên.
