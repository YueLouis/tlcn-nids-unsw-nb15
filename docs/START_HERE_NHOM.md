# Bắt đầu làm việc cùng nhóm

**Bản đọc đợt 3 cập nhật 10/11/2026:** mở [PDF 62 trang và hướng dẫn đọc](releases/review_dot3_20261110/README.md). `main` giữ bản chung; ba nhánh `tramanh`, `vuongthu`, `trongtin` giữ các bản nháp theo [phân công](group_delivery_20261110/README.md). Đây là lượt đọc duyệt hiện tại, chưa gửi mail trong công việc này. Đợt 1/2 và bản kỹ thuật đợt 3 ngày 30/10 giữ nguyên làm lịch sử. Thầy phản hồi ngày 31/10 về báo cáo đợt 2; không dùng thư đó làm xác nhận duyệt bản đợt 3.

**Mốc 25/11:** Tín xác nhận hiện chỉ nghe một bạn khác truyền lại; chưa tìm thấy ngày này trong email thầy hoặc hồ sơ lớp đang có. Email hướng dẫn 08/09 yêu cầu báo cáo bốn tuần/lần theo kế hoạch; Gantt của nhóm ghi hồ sơ cuối 23/12. Hãy dùng 25/11 làm mốc luyện tập tạm thời, không gọi đó là hạn nộp chính thức cho tới khi có thông báo.

**Luyện trước mốc dự kiến:** [Lịch ôn 09–24/11](management/KE_HOACH_ON_NHOM_BAO_CAO_NIDS_20261109.md). Mỗi bạn tự trả lời và truy nguồn; lịch này không ghi nhận thay phần đã học hay đóng góp.

**Kiểm kỹ thuật local 09/11:** 46/46 unit test đạt; protocol validator xác nhận 80 run duy nhất; audit báo cáo rà soát đợt 3 xác nhận PDF 62 trang, 29 hash đầu vào hình, 200 liên kết nội bộ và không có lỗi/tham chiếu thiếu chặn phát hành. Demo local đã chạy ma trận bốn mô hình × bốn kịch bản, so sánh đủ bốn mô hình, mẫu chưa nhãn không tính FP/FN/FPR/Recall, CSV thiếu cột bị từ chối HTTP 400 và hiện thông báo lỗi có hướng xử lý. Kiểm 375/390/768/1366 px và 1920×1080 không tràn ngang; không có lỗi JavaScript chưa xử lý. Lượt thử CSV sai schema cố ý tạo một dòng 400 trong console trình duyệt. Các kiểm tra này không thay review nhóm, xác nhận giảng viên hoặc bằng chứng đã nộp.

**GitHub:** `origin/main` hiện ở `37c159b5c863bd7ffd421fc5c3839497120200a0`, trùng HEAD local. Các thay đổi sau commit này còn ở máy; GitHub CLI chưa đăng nhập nên chưa xác nhận bản mới đã được đẩy lên.

**30/10/2026 — Đợt 3 chốt kỹ thuật:** [PDF, nguồn và bằng chứng](releases/dot_03/README.md) · [Drive bản chốt](https://drive.google.com/drive/folders/1AyxVWgeJj9mZ0L_d0AVosxKS6IUpghbe). Bản chốt Drive ngày 30/10 tải lại đủ 14 tệp khớp hash. Lịch sử có mốc dự kiến gửi 09/11; hiện không dùng mốc dự kiến đó làm bằng chứng đã gửi.

**26/10/2026 — Demo ứng dụng:** chạy server và mở `http://127.0.0.1:4397/lab`. Trong một tab có sáu nút: Thiết lập, Kết quả, Ghi chú, Dữ liệu, Mã xử lý và Hướng dẫn; bảng/tài liệu có Trước–Tiếp nên không phải cuộn trang dài. [Báo cáo bổ sung năm trang](application_20261026/report.html). Đây là phát lại flow trên bundle đã lưu; nhận xét, tự chạy và đóng góp cá nhân chưa được xác nhận thay nhóm.

Trước khi lên bục, làm theo [checklist HDMI và trình chiếu](management/CHECKLIST_TRINH_CHIEU_HDMI_20261109.md) trên đúng laptop/cáp/TV sẽ dùng. Kiểm viewport mô phỏng không xác nhận thiết bị phòng học.

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

Mỗi bạn làm trên nhánh được nhóm chốt: `tramanh`, `vuongthu` hoặc
`trongtin`. Commit đúng file đã sửa, push nhánh và gửi link để đọc chéo.
Ghi việc đã đổi, lệnh kiểm tra, kết quả và người review; tránh commit dataset
hoặc model nặng.

## 5. Trạng thái lịch sử ngày 13–17/10

- 80 run, 320 artifact, 17 test PASS; validator xác nhận 80 ID.
- PDF đợt 2 hiện 37 trang, hiệu chỉnh toàn văn ngày 17/10, ở `../output/pdf/`; nguồn đầy đủ ở `report_cumulative/`. Xem `reports/DOT_02_CAP_NHAT_20261017.md` và bảng hai target.
- Audit số liệu ngày 13/10 khớp predictions; bản ghi/log ở `evidence/dot_02/final_20261013/`.
- Các lời báo đồng ý cũ thuộc bản trước; bản 37 trang chờ nhóm tự đọc/giải thích và đối chiếu đóng góp. Phân công là kế hoạch; không xác nhận thay thành viên.
- Related-work toàn văn, phân tích lỗi sâu và demo hoàn chỉnh còn mở, đã ghi trong PDF.

Đọc [tiến độ hiện tại](management/TIEN_DO_HIEN_TAI_20261013.md), [protocol](protocol/RQ_TO_EVIDENCE.md), [schema](protocol/RESULT_SCHEMA.md), [data contract](evidence/dot_02/DATA_CONTRACT.md) và [tài liệu nền](references/README.md).
