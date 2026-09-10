# DATA AUDIT CHECKLIST V0.1

## Nguồn và toàn vẹn

- [ ] Ghi URL nguồn chính thức UNSW-NB15 và ngày truy cập.
- [ ] Xác nhận đúng hai tệp `UNSW_NB15_training-set.csv` và `UNSW_NB15_testing-set.csv`.
- [ ] Ghi byte size, row count và SHA-256; không sửa raw file.
- [ ] Lưu manifest ngoài GitHub nếu file raw lớn.

## Schema

- [ ] Liệt kê mọi cột, dtype, non-null count và unique count cho train/test.
- [ ] Đánh dấu vai trò: feature, target, metadata.
- [ ] Xác nhận `id`, `label`, `attack_cat` không đi vào feature matrix.
- [ ] Kiểm tra categorical columns `proto`, `service`, `state` và category mới ở test.

## Nhãn và support

- [ ] Đếm `label` Normal/Attack ở train và test.
- [ ] Đếm `attack_cat` ở train/test, không gộp mất Reconnaissance, DoS, Exploits.
- [ ] Ghi support cho ba held-out class và Normal.
- [ ] Kiểm tra mapping nhãn nhất quán giữa hai official split.

## Chất lượng dữ liệu

- [ ] Missing, empty string, `inf`, `-inf`, giá trị không hợp lệ.
- [ ] Duplicate full-row.
- [ ] Duplicate sau khi bỏ `id`.
- [ ] Feature-only collision và giao nhau train-test theo khóa đã ghi rõ.
- [ ] Cardinality bất thường của categorical columns.

## Bàn giao

- [ ] `data_manifest.json` có nguồn, fingerprint và row count.
- [ ] `schema_report.csv` bao phủ toàn bộ cột.
- [ ] `quality_report.csv` có kết quả định lượng.
- [ ] `label_distribution.csv` có support/tỷ lệ.
- [ ] `duplicate_report.json` nêu khóa và phạm vi kiểm tra.
- [ ] Tín và Thu review trước khi đánh dấu Gate 2 PASS.

