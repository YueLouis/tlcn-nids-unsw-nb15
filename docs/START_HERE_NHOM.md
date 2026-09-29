# Bắt đầu làm việc cùng nhóm

**Cập nhật:** 29/09/2026

## 1. Lấy code về máy

Clone repo và cài môi trường theo [README](../README.md).
Sau khi cài đặt, chạy unit test và validator; hai bước này không cần dataset.

GitHub giữ code, config, test, manifest, bảng kết quả nhẹ và tài liệu nguồn.
Dataset, model, predictions và bản PDF nằm ngoài GitHub.

## 2. Nhận dữ liệu

[Drive dùng chung](https://drive.google.com/drive/folders/13KGqMT4NUr8JfvTpF0IEKfUDT0Dlvq5S)
là nơi nhóm bàn giao file lớn. Nếu chưa thấy file hoặc chưa có quyền truy cập,
liên hệ Tín để nhận đúng bản có checksum trong
[manifest](../artifacts/data/data_manifest.json).

Đặt hai file vào `data/raw/`:

- `UNSW_NB15_training-set.csv`: 175.341 dòng, 45 cột.
- `UNSW_NB15_testing-set.csv`: 82.332 dòng, 45 cột.

Run artifact đặt ở `results/runs/` nếu cần kiểm tra đủ hồ sơ. Chạy thử mới
vào `results/member_checks/<ten>/` để bảo toàn 80 run hiện có.

## 3. Mỗi người làm gì

| Người | Phần chính | Bắt đầu đọc |
|---|---|---|
| Trâm Anh | Audit dữ liệu, related work, biên tập báo cáo | `src/nids_benchmark/data.py`, manifest, data contract |
| Vương Thu | IF/AE, threshold, metric và phân tích lỗi | `models.py`, `evaluation.py` trong `src/nids_benchmark/`, bảng metric |
| Tín | GitHub, môi trường, preprocessing, RF/XGBoost, tích hợp | `preprocessing.py`, `runner.py` trong `src/nids_benchmark/`, test và script |

Xem [phân công đợt 2](management/PHAN_CONG_DOT_02_HIEN_TAI_20260929.md)
để biết đầu ra, người review và hạn đề xuất.

## 4. Gửi thay đổi

Mỗi bạn làm trên nhánh riêng, ví dụ `work/tram-anh-data` hoặc
`work/vuong-thu-eval`. Commit đúng file đã làm, push nhánh và tạo Pull Request.
Ghi việc đã đổi, lệnh kiểm tra, kết quả và người review; tránh commit dataset
hoặc model nặng.

## 5. Trạng thái hiện tại

- Có code bốn model, 80 run và bảng tổng hợp qua năm seed.
- Có 9 unit test; validator xác nhận ma trận 80 run.
- Có nguồn báo cáo đợt 2; còn việc audit sâu, biên tập và phân tích kết quả.
- Gate 1/Gate 2 vẫn cần xác nhận thực tế của cả ba thành viên.

Đọc thêm [protocol](protocol/RQ_TO_EVIDENCE.md),
[schema đầu ra](protocol/RESULT_SCHEMA.md) và
[data contract](evidence/dot_02/DATA_CONTRACT.md).
