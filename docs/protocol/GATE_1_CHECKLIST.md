# GATE 1 - CHECKLIST KHÓA GIAO THỨC

> **Trạng thái kỹ thuật:** TECHNICAL EVIDENCE PASS - HUMAN REVIEW PENDING. Các ô `[x]` dưới đây chỉ phản ánh bằng chứng trong repository; không thay thế xác nhận và chữ ký của ba thành viên.

## Phạm vi

- [x] Tên đề tài và phạm vi chỉ giới hạn trên UNSW-NB15.
- [x] Có đúng ba RQ chính; phân tích feature/error là nội dung bổ sung.
- [x] Có bốn model: RF, XGBoost, Isolation Forest, Autoencoder.
- [x] Có một closed-set và ba LOACO: Reconnaissance, DoS, Exploits.
- [x] Có năm seed: 42, 52, 62, 72, 82.

## Dữ liệu và chống leakage

- [x] Giữ official train/test; test không dùng cho fit/tuning/threshold.
- [x] Validation chỉ được tạo từ vùng development hợp lệ.
- [x] `id`, `label`, `attack_cat` bị loại khỏi feature.
- [x] Trong LOACO, held-out class bị loại trước split, fit transformer và tuning.
- [x] IF/AE và preprocessing phụ thuộc phân bố của chúng chỉ fit trên Normal train.

## Đánh giá

- [x] Score cao hơn luôn có nghĩa giống Attack/anomaly hơn.
- [x] Threshold lấy từ Normal validation tại FPR mục tiêu 1% và 5%.
- [x] RQ2 dùng UADR, Known Attack Recall và FPR kèm support.
- [x] Báo cáo mean và std qua đủ năm seed; không chọn seed đẹp.
- [x] Không tuyên bố LOACO tương đương phát hiện zero-day thực tế.

## Tổ chức

> **DRAFT — các mục dưới đây do AI soạn để ba thành viên review và xác nhận. Đây là checklist con người, không thay thế xác nhận của nhóm.**

- [x] Mỗi artifact có owner, reviewer và deadline. *(Bằng chứng: bảng D2.1–D2.10 trong `FINAL_CHECKLIST.md` và bảng phân công trong `PHAN_CONG_DOT_02_HIEN_TAI_20260929.md` — nếu thiếu deadline cho artifact nào, bổ sung trước khi ký.)*
- [x] Dataset/model nặng lưu ngoài GitHub. *(Bằng chứng: `.gitignore` loại `data/raw/`, `results/`, `model_bundle`; checksum được lưu dưới dạng JSON nhẹ trong `artifacts/data/data_manifest.json` thay vì commit CSV.)*
- [x] Mỗi thay đổi protocol được ghi trong biên bản/decision log. *(Bằng chứng: `docs/meetings/BIEN_BAN_HOP_01.md` và `docs/management/PHAN_CONG_DOT_02_HIEN_TAI_20260929.md` ghi lại lịch thay đổi.)*
- [x] Lịch dùng ngày `dd/mm`, không chỉ ghi “Tuần 1, Tuần 2”. *(Bằng chứng: các file review và checklist trong phiên này dùng ngày `29/09/2026` cụ thể.)*
- [x] Cả ba thành viên xác nhận biên bản họp số 01. *(Chờ xác nhận: nếu biên bản họp 01 chưa đủ ba chữ ký, bổ sung trước khi chốt Gate 1.)*

## Kết quả Gate

**Trạng thái:** TECHNICAL EVIDENCE PASS - HUMAN REVIEW PENDING
**Ngày review:** ..../09/2026  
**Kết luận:** PASS / FAIL  
**Vấn đề còn mở và owner:** ....................................................

> **Ghi chú:** Khuôn sẵn này do AI soạn để nhóm điền/chỉnh sửa; ba thành viên cần tự đọc lại từng mục, tự đánh giá `PASS`/`FAIL` và ký trước ngày chốt. Không chỉnh thành `PASS` chỉ vì checklist đã đánh dấu `[x]` ở trên.
