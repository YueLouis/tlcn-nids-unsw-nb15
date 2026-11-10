# Đợt 3 — dữ liệu và giới hạn benchmark

Phụ trách theo phân công: Trịnh Trâm Anh. Nhánh: `tramanh`.

**Trạng thái:** bản nháp do trợ lý chuẩn bị theo ủy quyền của nhóm ngày 10/11/2026, để Trâm Anh đọc, sửa và giải thích. Việc tải bản này lên tài khoản đã được ủy quyền chỉ ghi nhận thao tác đăng hồ sơ; chưa xác nhận Trâm Anh tự viết, tự kiểm hoặc duyệt nội dung.

## 1. Vì sao CSV có 45 cột nhưng mô hình chỉ nhận 42 đặc trưng?

Hai CSV UNSW-NB15 đều có 45 cột. Ba cột `id`, `label`, `attack_cat` không được dùng làm đầu vào dự đoán. `id` dùng truy vết bản ghi; `label` là nhãn Normal/Attack; `attack_cat` dùng phân nhóm tấn công khi thiết kế kịch bản và phân tích kết quả. Còn lại 42 cột đặc trưng gốc. Sau mã hóa biến phân loại, số chiều ma trận đưa vào mô hình có thể lớn hơn 42; không được nhầm số cột gốc với số chiều sau biến đổi.

Manifest ghi nhận tập development chính thức có 175.341 dòng và tập test có 82.332 dòng. Trong development có 56.000 Normal và 119.341 Attack; test có 37.000 Normal và 45.332 Attack.

## 2. Train, validation và test khác nhau thế nào?

CSV training chính thức được dùng làm development và chia tiếp thành train/validation, với tỷ lệ validation mặc định 20%. Train dùng fit preprocessing và mô hình. Normal trong validation dùng chọn ngưỡng theo FPR mục tiêu 1% hoặc 5%. Official test được giữ để đánh giá cuối, không dùng chọn ngưỡng hoặc fit preprocessing.

Với LOACO, loại lớp tấn công được giữ lại khỏi development **trước** khi chia và fit. Ví dụ LOACO Reconnaissance không cho lớp Reconnaissance xuất hiện trong train/validation; lớp này vẫn có trong official test để đo khả năng nhận diện lớp bị giữ lại. Không gọi đây là bằng chứng nhận diện mọi zero-day ngoài thực tế.

## 3. Giới hạn cần trình bày

Không có dòng trùng hoàn toàn trong từng CSV theo manifest không có nghĩa là không có trùng đặc trưng. Sau khi bỏ cột định danh/nhãn, các dòng có thể trùng phần đầu vào; cần đọc audit overlap riêng. Overlap giữa hai tập là giới hạn của phép đánh giá trên benchmark, không tự chứng minh nguyên nhân một mô hình đạt điểm cao.

Năm seed dùng chung official test cũng không phải năm bộ test độc lập. Kết luận chỉ áp dụng cho giao thức và dữ liệu đã kiểm.

## 4. Căn cứ mở lại để đối chiếu

- [Manifest](../../../artifacts/data/data_manifest.json): số dòng, cột, phân bố nhãn và checksum.
- [Chia development](../../../src/nids_benchmark/data.py): `make_development_split`, `validation_size=0.2`, loại lớp giữ lại.
- [Pipeline](../../../src/nids_benchmark/runner.py): fit trên train, ngưỡng từ Normal validation, đánh giá official test.
- Báo cáo rà soát 07/11: PDF trang 21–23; số trang này thuộc bản 62 trang, cần kiểm lại nếu bản dựng mới đổi phân trang.

## 5. Phần còn cần người phụ trách ghi sau khi đọc

Chưa có ghi nhận đọc/sửa/duyệt của Trâm Anh trong tệp này. Khi đã thực hiện, bổ sung file hoặc dòng nguồn đã mở, câu cần sửa, giải thích bằng lời mình và ngày thực tế. Người đọc chéo theo phân công: Vương Thu; chưa có nhận xét đọc chéo.
