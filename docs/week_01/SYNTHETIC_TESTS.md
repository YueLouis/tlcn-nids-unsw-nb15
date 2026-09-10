# SYNTHETIC TEST LIST V0.1

Các test này chạy trên mảng nhỏ tự tạo, trước khi dùng dataset thật.

| ID | Tình huống | Kỳ vọng |
|---|---|---|
| T01 | Score tăng dần, threshold cố định | Record có score >= threshold được gán Attack |
| T02 | Normal validation có 100 score, target FPR 5% | Threshold cho không quá 5 record Normal bị cảnh báo, theo tie rule |
| T03 | Normal validation rỗng | Trạng thái invalid; không sinh threshold giả |
| T04 | Held-out class xuất hiện trong development | Validator FAIL ngay |
| T05 | `id`, `label`, `attack_cat` nằm trong feature list | Validator FAIL ngay |
| T06 | Closed-set không có held-out class | UADR trả null, không trả 0 |
| T07 | LOACO có known và held-out attack | Known Recall chỉ tính known; UADR chỉ tính held-out |
| T08 | Tất cả record là Normal | Precision/Recall/F1 của Attack xử lý mẫu số 0 đúng schema |
| T09 | Model trả anomaly score thấp hơn khi bất thường | Adapter đổi chiều trước evaluator |
| T10 | Hai run trùng `run_id` | Registry từ chối duplicate |

