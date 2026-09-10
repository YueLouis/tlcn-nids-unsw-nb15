# BIÊN BẢN HỌP NHÓM SỐ 01 - KICKOFF VÀ GATE 1

**Trạng thái:** DRAFT - chỉ đổi thành FINAL sau khi đủ ba thành viên xác nhận  
**Thời gian:** ......, ngày ..../09/2026  
**Địa điểm/hình thức:** ........................................................  
**Thành phần:** Nguyễn Trọng Tín, Trịnh Trâm Anh, Hoàng Văn Vương Thu

## Mục tiêu buổi họp

1. Giảng lại đề tài bằng ngôn ngữ đơn giản để cả ba người hiểu giống nhau.
2. Chốt phạm vi, ba câu hỏi nghiên cứu và thiết kế closed-set + LOACO.
3. Chốt phân công, artifact Tuần 1 và cách review trên GitHub.
4. Quyết định PASS/FAIL Gate 1.

## Nội dung cần trình bày

- NIDS là gì và UNSW-NB15 chứa dữ liệu dạng flow như thế nào.
- Hai hướng tiếp cận: supervised learning và anomaly detection.
- Bốn mô hình: Random Forest, XGBoost, Isolation Forest, Autoencoder.
- LOACO: loại một attack class khỏi toàn bộ vùng phát triển mô hình rồi chỉ đánh
  giá class đó trên official test.
- Vì sao không được dùng test để fit, tuning hoặc chọn threshold.
- Ba metric trọng tâm: UADR, Known Attack Recall và FPR trên Normal.
- Repository lưu code/config/lịch sử; Drive lưu dataset, tài liệu và file nặng.

## Quyết định cần chốt

| Mục | Đề xuất hiện tại | Kết luận của nhóm |
|---|---|---|
| Official split | Giữ nguyên train/test chính thức | ... |
| Held-out classes | Reconnaissance, DoS, Exploits | ... |
| Models | RF, XGBoost, IF, Autoencoder | ... |
| Seeds | 42, 52, 62, 72, 82 | ... |
| Threshold | Chọn trên Normal validation tại FPR 1% và 5% | ... |
| Score direction | Score cao hơn = giống Attack/anomaly hơn | ... |
| Cột cấm | `id`, `label`, `attack_cat` | ... |
| Báo cáo tiến độ | 4 tuần/lần, vừa làm vừa viết | ... |

## Bàn giao Tuần 1

| Thành viên | Artifact | Deadline | Link/commit | Review bởi | Trạng thái |
|---|---|---|---|---|---|
| Trâm Anh | Glossary, related-work template, data-audit checklist | 14/09/2026 | ... | Tín + Thu | ... |
| Vương Thu | Metric/threshold spec, synthetic-test list | 14/09/2026 | ... | Tín + Trâm Anh | ... |
| Trọng Tín | Repo structure, run matrix, schema, Gate 1 checklist | 15/09/2026 | ... | Trâm Anh + Thu | ... |

## Vấn đề mở

| Vấn đề | Người xử lý | Hạn | Kết quả |
|---|---|---|---|
| Xác nhận deadline chính thức của môn để hiệu chỉnh Gantt | Tín | 16/09/2026 | ... |
| Xác nhận email/username GitHub của hai thành viên | Tín | 11/09/2026 | ... |

## Kết luận Gate 1

- [ ] PASS - cả nhóm hiểu và đồng ý protocol; được chuyển sang Tuần 2.
- [ ] FAIL - còn mâu thuẫn; ghi owner và deadline xử lý trước khi tiếp tục.

**Xác nhận:**

- Nguyễn Trọng Tín: ................................ ngày ..../09/2026
- Trịnh Trâm Anh: .................................. ngày ..../09/2026
- Hoàng Văn Vương Thu: ............................. ngày ..../09/2026

