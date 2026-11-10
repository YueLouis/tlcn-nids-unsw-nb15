# Đợt 3 — kết quả, FP/FN và ngưỡng

Phụ trách theo phân công: Hoàng Văn Vương Thu. Nhánh: `vuongthu`.

**Trạng thái:** bản nháp do trợ lý chuẩn bị theo ủy quyền của nhóm ngày 10/11/2026, để Vương Thu đọc, sửa và giải thích. Thao tác đăng hồ sơ được ủy quyền không xác nhận Thu tự viết, tự truy vết hoặc duyệt nội dung.

## 1. Hai loại sai cần phân biệt

FP là bản ghi Normal bị dự đoán Attack. FN là bản ghi Attack bị dự đoán Normal. FPR có mẫu số là số Normal (`FP/(FP+TN)`); Recall có mẫu số là số Attack (`TP/(TP+FN)`). UADR trong LOACO chỉ tính trên bản ghi của lớp tấn công bị giữ lại. Không dùng lẫn các mẫu số.

## 2. Truy vết hai ví dụ trong LR-RF-S42

Mở [CSV trích hai ví dụ](NGUON_VI_DU_THU.csv). Bản trích lấy từ `docs/management/ban_giao_dot3_review_20261107/NGUON_VI_DU.csv`; nguồn dự đoán đầy đủ là `results/runs/LR-RF-S42/predictions.csv`, có SHA-256 `19def4540004699c4271b55008f7a793e149360dd6fb1aba9381b634b1026bcc`. Đây là ví dụ được chuẩn bị sẵn để đối chiếu, chưa phải kết quả Thu tự truy. Bản trích nhỏ không thay thế bộ dự đoán đầy đủ trên Drive.

| ID trên official test | Nhãn thật | Score | Ngưỡng tại target validation 5% | Dự đoán | Loại sai |
|---:|---|---:|---:|---|---|
| 68699 | Normal (0) | 0.5568311122449866 | 0.55681266574524546 | Attack (1) | FP |
| 975 | Reconnaissance (1) | 0.55649131907993055 | 0.55681266574524546 | Normal (0) | FN |

Quy tắc của pipeline là score lớn hơn hoặc bằng ngưỡng thì dự đoán Attack. Bản ghi 68699 vượt ngưỡng rất ít nên thành FP; bản ghi 975 thấp hơn ngưỡng nên thành FN. Trong LR, Reconnaissance là lớp bị loại khỏi development. Hai trường hợp đơn lẻ minh họa lỗi sát ngưỡng, không đại diện toàn bộ phân bố.

## 3. Vì sao target 5% không có nghĩa test FPR đúng 5%?

Ngưỡng được chọn từ Normal validation. Khi đưa sang official test, phân bố score có thể khác nên test FPR không bị đảm bảo bằng target validation. Hạ ngưỡng thường bắt được nhiều Attack hơn nhưng cũng tăng cảnh báo sai; nâng ngưỡng thường giảm cảnh báo sai nhưng có thể bỏ sót thêm Attack. Phải so sánh cả hai phía trên cùng mô hình/kịch bản/seed.

AP đánh giá thứ hạng score trên nhiều ngưỡng, không phải Recall tại một ngưỡng. Khi nhận CSV không có nhãn thật, demo chỉ đưa ra dự đoán/score, không tính FP/FN/FPR/Recall.

## 4. Căn cứ và phần còn mở

- [Hàm metric](../../../src/nids_benchmark/evaluation.py) và [pipeline](../../../src/nids_benchmark/runner.py).
- [Bảng hai target](../../reports/DOT_02_TWO_TARGETS.csv).
- PDF rà soát 07/11 trang 34 và 55 (Bảng 9.7); số trang thuộc bản 62 trang, cần kiểm lại trên bản dựng mới.

Chưa có ghi nhận Thu tự kiểm/sửa hoặc nhận xét đọc chéo của Tín. Sau khi đọc cần ghi run/ID/dòng nguồn thực tế đã mở, sửa câu chưa đúng và giải thích bằng lời mình; không điền xác nhận thay người đọc.
