# Dữ liệu, nguồn và giới hạn đánh giá

## Dữ liệu được dùng

Nhóm sử dụng hai tập chia chính thức của UNSW-NB15: 175.341 dòng phát triển và 82.332 dòng kiểm tra. Mỗi tập có 45 cột. Ba cột `id`, `label`, `attack_cat` phục vụ định danh hoặc đánh giá, không đưa vào mô hình; đầu vào mô hình còn 42 đặc trưng. Trong đó `proto`, `service`, `state` là dạng phân loại, 39 cột còn lại là số.

`DU_LIEU_MANIFEST.json` ghi nguồn, SHA-256, số dòng, kiểu dữ liệu và số mẫu từng nhãn. Kiểm missing và infinity không phát hiện giá trị thiếu/vô hạn trong hai CSV được ghi nhận. Đây là kết quả audit bộ dữ liệu cụ thể, không phải bảo đảm mọi dữ liệu đầu vào sau này đều sạch.

## Cách chia tập và tránh dùng nhầm dữ liệu

Official train được chia thành vùng huấn luyện và validation. Với LOACO, loại lớp giữ lại khỏi vùng phát triển trước phép chia. RF/XGB học từ Normal và các Attack còn được phép; IF/AE học Normal. Preprocessing chỉ được fit trong vùng huấn luyện phù hợp. Ngưỡng được chọn bằng Normal validation; official test không tham gia chọn ngưỡng.

Trong ba lượt LOACO, lớp được giữ lại lần lượt là Reconnaissance, DoS và Exploits. Test vẫn chứa các lớp đó để đo khả năng nhận ra một loại chưa xuất hiện khi học. LOACO không chứng minh phát hiện mọi zero-day ngoài thực tế.

## Vì sao duplicate bằng 0 vẫn có overlap

Đếm cả hàng có `id` cho duplicate bằng 0. Nếu chỉ đếm 42 đặc trưng, số hàng lặp sau lần đầu là 74.301 ở train và 28.386 ở test. Có 8.541/82.332 dòng test trùng vector 42 đặc trưng với một dòng trong toàn official train. Các phép đếm này dùng các khóa khác nhau nên không mâu thuẫn.

Đợt 3 bổ sung overlap với đúng tập model được fit, thay vì mặc định toàn official train. `KIEM_TRA_TAP_FIT.csv` ghi 80 lượt; `OVERLAP_MEAN_STD.csv` tách matched/unmatched và support. Tập fit của supervised khác Normal-only nên hai họ không có cùng nhóm matched. Không diễn giải chênh lệch metric giữa hai nhóm là tác động nhân quả của overlap; chưa có thí nghiệm retrain loại trùng.

## Nguồn và giới hạn

`MA_TRAN_TAI_LIEU.csv` ghi DOI/URL, nội dung dùng và phạm vi đối chiếu. Nguồn S07 mới được đối chiếu abstract; không dùng nó để trích metric hay cách chia tập chi tiết. Nhóm mới đo một dataset/official split, chưa kiểm dữ liệu vận hành độc lập. Nguồn gốc dataset thuộc UNSW; dữ liệu này không phải dataset do nhóm tự thu thập.

Mã và kiểm thử liên quan nằm trong ZIP theo đường dẫn gốc: `src/nids_benchmark/data.py`, `scripts/audit_data.py`, `scripts/audit_duplicate_overlap.py`, `tests/test_data_pipeline.py`. Các bản sao giữ nguyên nội dung nguồn và hash, không đổi tác giả lịch sử.
