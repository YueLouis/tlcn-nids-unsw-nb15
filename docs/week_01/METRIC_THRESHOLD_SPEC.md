# METRIC VÀ THRESHOLD SPECIFICATION V0.1

**Owner:** Hoàng Văn Vương Thu  
**Review:** Nguyễn Trọng Tín, Trịnh Trâm Anh  
**Trạng thái:** DRAFT

## Quy ước chung

- Nhãn nhị phân: Normal = 0, Attack = 1.
- Score cao hơn luôn có nghĩa record giống Attack/anomaly hơn.
- `y_pred = 1` khi `score >= threshold`; tie rule này phải dùng nhất quán.
- Metric không có mẫu số hợp lệ trả `null`, không tự ghi 0.

## Metric chính

- **UADR / Held-out Attack Recall:** `TP_heldout / support_heldout`.
- **Known Attack Recall:** `TP_known / support_known`.
- **FPR trên Normal:** `FP_normal / support_normal`.
- **Precision:** `TP / (TP + FP)`.
- **Recall:** `TP / (TP + FN)`.
- **F1:** `2 * precision * recall / (precision + recall)`.

Mọi metric phải ghi `scenario`, `run_id`, `seed`, `split`, `subset`, `support` và
`target_fpr` nếu là operating point.

## Chọn threshold

1. Chỉ dùng score của Normal validation để chọn threshold.
2. Với target FPR `alpha` bằng 0.01 hoặc 0.05, xét các threshold duy nhất theo
   thứ tự tăng dần.
3. Chọn threshold thấp nhất nhưng vẫn thỏa `FP_normal / N_normal <= alpha`; cách
   này ưu tiên độ nhạy cao nhất trong ngân sách cảnh báo nhầm.
4. Nếu không có candidate thỏa do dữ liệu rỗng, trả trạng thái `invalid` và ghi
   lý do; không nhìn vào official test để sửa.
5. Lưu threshold, số Normal validation, FPR thực tế và tie rule vào `run.json`.

## Kiểm tra bắt buộc

- [ ] Score direction của cả bốn model đã quy về cùng chiều.
- [ ] Threshold không được fit từ attack validation hoặc official test.
- [ ] UADR chỉ có giá trị ở LOACO; closed-set ghi `null`.
- [ ] Known Attack Recall loại held-out class khỏi support trong LOACO.
- [ ] Mẫu số bằng 0 được kiểm thử và cảnh báo.

