# Bắt đầu làm việc cùng nhóm

**30/10/2026 — Đợt 3 chốt kỹ thuật:** [PDF, nguồn và bằng chứng](releases/dot_03/README.md) · [Drive bản chốt](https://drive.google.com/drive/folders/1AyxVWgeJj9mZ0L_d0AVosxKS6IUpghbe). Đã kiểm 46 test, 80 run và số liệu; bản Drive tải lại đủ 14 tệp khớp hash. Chờ cả ba tự review; chưa gửi email/nộp. Tín tự gửi ngày 09/11, có lời nhắc tối 08/11 và sáng 09/11.

**26/10/2026 — Demo ứng dụng:** chạy server và mở `http://127.0.0.1:4397/lab`. Trong một tab có sáu nút: Thiết lập, Kết quả, Ghi chú, Dữ liệu, Mã xử lý và Hướng dẫn; bảng/tài liệu có Trước–Tiếp nên không phải cuộn trang dài. [Báo cáo bổ sung năm trang](application_20261026/report.html). Đây là phát lại flow trên bundle đã lưu; nhận xét, tự chạy và đóng góp cá nhân chưa được xác nhận thay nhóm.

**25/10/2026 — Mở một chỗ:** [Bộ bài để Anh–Thu–Tín đọc và sửa dần](management/BO_HO_SO_NHOM_20261025.md). Theo yêu cầu mới, đã chuẩn bị PDF nháp đợt 3–4, báo cáo tổng, hướng dẫn từng người và demo CSV kiểm bằng mô hình thật. Không còn yêu cầu hai bạn viết từ đầu trước khi có bản chung; mỗi bạn kiểm, góp ý và giải thích phần mình. Bản nháp chưa duyệt nộp, không tính thay đóng góp thành viên. Hồ sơ đợt 2 bên dưới giữ mốc lịch sử.

**22/10/2026: bắt đầu đợt 3, mốc báo cáo 09/11 đã được nhóm trưởng xác nhận thống nhất với thầy.** Đọc [chia việc Anh–Thu–Tín](management/phan_cong_dot_03_20261022/00_PHAN_CONG_DOT_03.md) và [kế hoạch đợt 3](management/KE_HOACH_DOT_03_20261022.md). Script/hình hỗ trợ là tài liệu nền; mỗi bạn tự làm, giải thích và bàn giao phần được giao. Nội dung bên dưới giữ bằng chứng đợt 2.

**17/10/2026: email đã gửi lúc 23:38, kèm PDF 37 trang; nhóm dự kiến tự rà soát hai đợt ngày 18/10.** Đọc [hướng dẫn rà soát](management/HUONG_DAN_RA_SOAT_HAI_DOT_20261018.md). Chưa xác minh mức hiểu từng thành viên; không xem lời báo đồng ý trước đó là hoàn tất nghiệm thu nội dung.

**Cập nhật:** 13/10/2026

## 1. Lấy code về máy

Clone repo và cài môi trường theo [README](../README.md).
Sau khi cài đặt, chạy unit test và validator; hai bước này không cần dataset.

GitHub giữ code, config, test, manifest, bảng kết quả nhẹ và tài liệu nguồn.
Dataset, model, predictions và PDF nộp nhận từ Drive. Trên máy nhóm trưởng, PDF có thêm bản sao tại `output/pdf/`; thư mục này không có trong bản clone GitHub.

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

Xem [tiến độ hiện tại](management/TIEN_DO_HIEN_TAI_20261013.md) để biết đầu ra và người phụ trách.
[Phân công tháng 9](management/PHAN_CONG_DOT_02_HIEN_TAI_20260929.md) được giữ làm hồ sơ lịch sử.

## 4. Gửi thay đổi

Mỗi bạn làm trên nhánh riêng, ví dụ `work/tram-anh-data` hoặc
`work/vuong-thu-eval`. Commit đúng file đã làm, push nhánh và tạo Pull Request.
Ghi việc đã đổi, lệnh kiểm tra, kết quả và người review; tránh commit dataset
hoặc model nặng.

## 5. Trạng thái lịch sử ngày 13–17/10

- 80 run, 320 artifact, 17 test PASS; validator xác nhận 80 ID.
- PDF đợt 2 hiện 37 trang, hiệu chỉnh toàn văn ngày 17/10, ở `../output/pdf/`; nguồn đầy đủ ở `report_cumulative/`. Xem `reports/DOT_02_CAP_NHAT_20261017.md` và bảng hai target.
- Audit số liệu ngày 13/10 khớp predictions; bản ghi/log ở `evidence/dot_02/final_20261013/`.
- Các lời báo đồng ý cũ thuộc bản trước; bản 37 trang chờ nhóm tự đọc/giải thích và đối chiếu đóng góp. Phân công là kế hoạch; không xác nhận thay thành viên.
- Related-work toàn văn, phân tích lỗi sâu và demo hoàn chỉnh còn mở, đã ghi trong PDF.

Đọc [tiến độ hiện tại](management/TIEN_DO_HIEN_TAI_20261013.md), [protocol](protocol/RQ_TO_EVIDENCE.md), [schema](protocol/RESULT_SCHEMA.md), [data contract](evidence/dot_02/DATA_CONTRACT.md) và [tài liệu nền](references/README.md).
