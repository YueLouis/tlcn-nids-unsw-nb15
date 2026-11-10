# Đợt 3 — protocol, demo và tích hợp

Phụ trách theo phân công: Nguyễn Trọng Tín. Nhánh: `trongtin`.

**Trạng thái:** bản nháp do trợ lý chuẩn bị theo ủy quyền ngày 10/11/2026. Không xác nhận Tín đã tự chạy demo hoặc cả nhóm đã duyệt; các kết quả có sẵn dưới đây là căn cứ để nhóm mở lại và giải thích.

## 1. Giao thức thực nghiệm

Ma trận gồm 4 kịch bản (closed-set, LOACO Reconnaissance, DoS, Exploits), 4 mô hình (RF, XGBoost, IF, AE) và 5 seed (42, 52, 62, 72, 82), tổng cộng 80 run. Mỗi run có `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib`. Artifact nặng giữ trên Drive; GitHub lưu code, config, bảng nhẹ và nguồn tài liệu.

Ba cột `id`, `label`, `attack_cat` không vào feature. LOACO loại lớp giữ lại trước chia development. Preprocessing fit trên train; Normal validation dùng chốt ngưỡng; official test đánh giá cuối. Không sửa threshold theo test để làm kết quả đẹp hơn.

## 2. Ví dụ CS-RF-S42, official-test ID 1

| Target FPR validation | Score cố định | Ngưỡng đã lưu | Dự đoán | Nhãn thật |
|---|---:|---:|---|---|
| 5% | 0.70574127072966075 | 0.55728168674827427 | Attack | Normal |
| 1% | 0.70574127072966075 | 0.80536725511544849 | Normal | Normal |

Score của cùng bản ghi không đổi; chỉ ngưỡng đổi. Tại target 5%, score vượt ngưỡng nên là FP; tại target 1%, score thấp hơn ngưỡng nên là TN. Đây là so sánh hai ngưỡng đã chọn từ validation, không huấn luyện lại. Căn cứ: `docs/management/ban_giao_dot3_review_20261107/NGUON_VI_DU.csv` và `results/runs/CS-RF-S42/predictions.csv`.

## 3. Khi trình bày demo

Chạy `python scripts/demo_server.py`, mở `http://127.0.0.1:4397/lab`, chọn đúng kịch bản/mô hình/seed và bản ghi. Demo phát lại flow CSV qua bundle đã lưu; không thu gói tin trực tiếp và không chứng minh hiệu quả triển khai mạng thật. Nếu CSV thiếu cột bắt buộc thì từ chối, không tự điền giá trị giả. Nếu thiếu nhãn thật thì không tính các metric cần nhãn.

## 4. Tích hợp vào hồ sơ chung

`main` là hồ sơ chung. Ba nhánh cá nhân giữ phần được phân công cùng lịch sử sửa thật. Trước tích hợp phải kiểm nội dung, đường dẫn, checksum PDF/nguồn và nhận xét đọc chéo; ghi riêng việc trợ lý chuẩn bị với việc thành viên đã thực hiện. Email chưa được gửi trong công việc này.

Chưa có log/ảnh chứng minh Tín tự chạy mới hoặc nhận xét đọc chéo của Trâm Anh trong bản này. Ghi nhận kiểm kỹ thuật đã chuẩn bị nằm ở `docs/evidence/dot_03/member_work/trong_tin/TIN_KIEM_TRA_KY_THUAT_20261110.md` và không thay xác nhận đó.
