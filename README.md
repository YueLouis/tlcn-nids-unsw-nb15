# TLCN NIDS - UNSW-NB15

So sánh mô hình học có giám sát và phát hiện bất thường cho hệ thống phát hiện
xâm nhập mạng trên UNSW-NB15 bằng đánh giá leave-one-attack-class-out (LOACO).

## Phạm vi nghiên cứu

- Mô hình học có giám sát: Random Forest và XGBoost.
- Mô hình phát hiện bất thường: Isolation Forest và Autoencoder.
- Kịch bản: closed-set và ba vòng LOACO giữ lại lần lượt Reconnaissance, DoS,
  Exploits.
- Seed cố định: 42, 52, 62, 72, 82.
- Tổng ma trận chính: 4 kịch bản x 4 mô hình x 5 seed = 80 run.

Ba câu hỏi nghiên cứu chính và bằng chứng cần thu thập được mô tả tại
[`docs/protocol/RQ_TO_EVIDENCE.md`](docs/protocol/RQ_TO_EVIDENCE.md).

## Trạng thái

Tuần 1 (10/09/2026-16/09/2026): khóa giao thức, phân công, ma trận thí nghiệm,
schema kết quả và điều kiện PASS/FAIL của Gate 1. Nhóm chưa huấn luyện mô hình
trước khi hoàn tất kiểm kê dữ liệu và Gate 2.

## Cấu trúc repository

```text
configs/                Cấu hình nghiên cứu đã version hóa
docs/management/        Phân công và tiến độ
docs/meetings/          Biên bản họp nhóm
docs/protocol/          Giao thức, schema và checklist các gate
docs/week_01/           Kế hoạch và đầu ra tuần 1
scripts/                Công cụ tạo/kiểm tra artifact
src/nids_benchmark/     Mã nguồn (bắt đầu sau khi hợp đồng dữ liệu được duyệt)
tests/                  Kiểm thử chống sai protocol và data leakage
```

## Quy tắc dữ liệu và bảo mật

- Không đưa dataset UNSW-NB15, model nặng, prediction theo từng record hoặc file
  chứa thông tin nhạy cảm lên GitHub.
- Không commit mật khẩu, token, API key, file `.env` hoặc thông tin đăng nhập.
- `label`, `attack_cat` và `id` không được dùng làm feature của mô hình.
- Official test chỉ dùng để đánh giá cuối; không dùng để fit preprocessing,
  chọn hyperparameter hoặc chọn threshold.

## Bắt đầu tuần 1

1. Đọc [`docs/week_01/KE_HOACH_TUAN_01.md`](docs/week_01/KE_HOACH_TUAN_01.md).
2. Mỗi thành viên nhận đúng artifact trong
   [`docs/management/PHAN_CONG_NHOM.md`](docs/management/PHAN_CONG_NHOM.md).
3. Cả nhóm review và ký Gate 1 ngày 16/09/2026.
4. Tạo lại ma trận 80 run bằng `python scripts/generate_run_matrix.py`.

## Thành viên

- Nguyễn Trọng Tín - nhóm trưởng, repository, preprocessing, RF/XGBoost và tích hợp.
- Trịnh Trâm Anh - dữ liệu, tổng quan NIDS, related work và biên tập báo cáo.
- Hoàng Văn Vương Thu - Isolation Forest, Autoencoder, threshold, metric và error analysis.
