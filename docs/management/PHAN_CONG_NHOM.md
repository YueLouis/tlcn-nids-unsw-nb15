# PHÂN CÔNG NHÓM

**Đề tài:** So sánh supervised learning và anomaly detection cho NIDS trên
UNSW-NB15 bằng LOACO  
**Tuần hiện tại:** 10/09/2026-16/09/2026  
**Nhóm trưởng:** Nguyễn Trọng Tín

## Trách nhiệm chính

| Thành viên | Phụ trách | Người review chéo |
|---|---|---|
| Trịnh Trâm Anh | Data audit, tổng quan NIDS/UNSW-NB15, related work, biên tập báo cáo | Tín review data contract; Thu review support lớp |
| Hoàng Văn Vương Thu | Isolation Forest, Autoencoder, score, threshold, metric, error analysis | Tín review interface; Trâm Anh review cách diễn giải |
| Nguyễn Trọng Tín | Nhóm trưởng, GitHub, kiến trúc mã nguồn, preprocessing, RF/XGBoost, quản lý thí nghiệm và tích hợp | Trâm Anh review schema; Thu review score/metric |
| Cả nhóm | Protocol, kết quả, báo cáo, slide và demo | Review lẫn nhau trước mỗi gate |

## Công việc Tuần 1

### Trịnh Trâm Anh

- [ ] Đọc đề cương và protocol; ghi lại điểm chưa rõ, không tự đổi phạm vi.
- [ ] Tạo glossary cho: NIDS, supervised learning, anomaly detection, closed-set,
  held-out attack, LOACO, UADR, Known Attack Recall và FPR.
- [ ] Tạo mẫu ma trận related work với các cột: nguồn, dataset, split, model,
  metric, kết quả, hạn chế và mức độ so sánh được.
- [ ] Soạn checklist dữ liệu cần kiểm kê: nguồn, checksum, schema, missing,
  duplicate, phân bố lớp và categorical cardinality.

**Bàn giao chậm nhất 14/09/2026:** glossary v0.1, mẫu related work và checklist
data audit. Không cần tải dataset trong tuần này.

### Hoàng Văn Vương Thu

- [ ] Đọc đề cương và protocol; xác nhận assumption của anomaly detection.
- [ ] Viết đặc tả score chung: score càng cao càng giống Attack/anomaly.
- [ ] Chốt công thức UADR, Known Attack Recall, FPR, Precision, Recall và F1.
- [ ] Viết cách chọn threshold trên Normal validation tại FPR mục tiêu 1% và 5%.
- [ ] Đề xuất test synthetic cho score direction, threshold, label mapping và mẫu
  số bằng 0; chưa cần train IF/AE.

**Bàn giao chậm nhất 14/09/2026:** metric/threshold specification v0.1 và danh
sách test synthetic.

### Nguyễn Trọng Tín

- [x] Tạo repository private và `.gitignore` Python.
- [x] Chốt cấu trúc repository và cấu hình ma trận thí nghiệm.
- [x] Tạo ma trận 80 run có ID duy nhất.
- [x] Soạn result schema, prediction schema và checklist Gate 1.
- [ ] Mời hai thành viên bằng tài khoản GitHub riêng; không dùng chung mật khẩu.
- [ ] Review artifact của Trâm Anh và Vương Thu trước buổi ký Gate 1.

**Bàn giao chậm nhất 15/09/2026:** repository v0.1, nhận xét review chéo và danh
sách vấn đề còn mở.

### Cả nhóm

- [ ] Họp kickoff, xác nhận đã hiểu ba RQ và ranh giới trách nhiệm.
- [ ] Xác nhận ba held-out class: Reconnaissance, DoS, Exploits.
- [ ] Xác nhận năm seed: 42, 52, 62, 72, 82.
- [ ] Review official split, cột cấm và quy tắc không dùng test để tuning.
- [ ] Ký PASS/FAIL Gate 1 ngày 16/09/2026 bằng biên bản họp số 01.

## Quy tắc bàn giao

- Một việc chỉ được đánh dấu hoàn thành khi có file/đường dẫn và người review.
- Mỗi người làm trên branch riêng, gửi pull request; không đẩy trực tiếp vào
  `main` sau khi nhóm bắt đầu cộng tác.
- Dataset và model nặng lưu ở Drive cá nhân đã chia sẻ, không lưu trong GitHub.
- Mọi thay đổi protocol phải ghi lý do trong biên bản, không thỏa thuận miệng.
