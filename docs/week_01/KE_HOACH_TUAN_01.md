# KẾ HOẠCH TUẦN 1 - 10/09/2026 ĐẾN 16/09/2026

## Mục tiêu duy nhất

Ba thành viên hiểu và đồng ý một giao thức nghiên cứu có thể kiểm chứng. Cuối
tuần phải PASS Gate 1; chưa cần tải dữ liệu hoặc train model để chạy theo tiến độ
ảo.

## Lịch 7 ngày

| Ngày | Việc chính | Người chủ trì | Đầu ra |
|---|---|---|---|
| 10/09 | Tín giới thiệu đề tài, Drive, GitHub và giao việc | Tín | Repo + kế hoạch tuần |
| 11/09 | Cả nhóm đọc đề cương/protocol, ghi câu hỏi và xác nhận tài khoản cộng tác | Cả nhóm | Checklist đọc + quyền truy cập |
| 12/09 | Chốt RQ, scenario, held-out class, seed và cột cấm | Tín | RQ matrix + protocol checklist |
| 13/09 | Làm artifact cá nhân; Tín kiểm tra run matrix/schema | Mỗi người | Bản nháp v0.1 |
| 14/09 | Trâm Anh và Thu bàn giao; Tín review lần 1 | Trâm Anh + Thu | Artifact cá nhân |
| 15/09 | Review chéo, sửa mâu thuẫn, điền biên bản | Cả nhóm | Bộ Gate 1 sẵn sàng ký |
| 16/09 | Họp 30-45 phút, demo repo/config và quyết định PASS/FAIL | Tín + cả nhóm | Biên bản họp số 01 |

## Kịch bản họp kickoff cho Tín

1. Giải thích bài toán trong 3 phút: phân biệt traffic Normal và Attack trên dữ
   liệu flow của UNSW-NB15.
2. Giải thích hai hướng trong 5 phút: supervised đã thấy attack khi train; anomaly
   chủ yếu học Normal.
3. Giải thích LOACO trong 5 phút bằng ví dụ loại toàn bộ Reconnaissance khỏi vùng
   phát triển rồi kiểm tra nó trên test.
4. Mở `RQ_TO_EVIDENCE.md`, `experiment_matrix.yaml` và `RUN_MATRIX.csv` để cho
   thấy nhóm sẽ thu bằng chứng gì.
5. Giao đúng artifact cho từng bạn, chốt deadline và cách review.
6. Nhắc lại: GitHub không chứa dataset/model nặng; không dùng chung mật khẩu.

## Definition of Done

- Repo có cấu trúc, config và ma trận đủ 80 ID duy nhất.
- Ba RQ ánh xạ được sang metric và artifact.
- Trâm Anh có glossary + data-audit/related-work template.
- Vương Thu có metric/threshold specification + synthetic-test list.
- Cả nhóm điền biên bản, hoàn thành checklist và quyết định Gate 1.
- Gantt dùng ngày cụ thể và đã ghi mốc báo cáo 4 tuần/lần.

## Không làm trong Tuần 1

- Không upload dataset lên GitHub.
- Không huấn luyện model để lấy số liệu trình bày sớm.
- Không tối ưu hyperparameter hoặc chọn threshold trên official test.
- Không gọi kết quả held-out class là phát hiện zero-day thực tế.

