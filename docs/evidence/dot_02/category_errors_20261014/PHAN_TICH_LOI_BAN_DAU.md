# Phân tích lỗi ban đầu đợt 2 - 14/10/2026

Dữ liệu đầu vào: predictions.csv và metrics.csv của đúng 80 run gốc; không huấn luyện lại, không thay threshold, không loại trùng khỏi official split. Script tái tạo: `scripts/analyze_category_errors.py`. Đã đối chiếu 13.173.120 dòng prediction và 760 giá trị metric, không sai lệch; hash prediction trước/sau giữ nguyên.

Mỗi target có 82.332 record gồm 37.000 Normal và 45.332 Attack. FP là Normal bị dự đoán Attack; FN là Attack bị dự đoán Normal. Mẫu số tỷ lệ FP chỉ là Normal, mẫu số FN là số record của từng category. Trung bình và sample std (ddof=1) tính từ năm seed; không coi 5 lần đánh giá cùng official test là năm tập dữ liệu độc lập.

## Closed-set tại target validation 5%

| Category | Support mỗi seed | Loại lỗi | RF (%) | XGB (%) | IF (%) | AE (%) |
|---|---:|---|---:|---:|---:|---:|
| Analysis | 677 | FN | 0.89 ± 0.42 | 5.67 ± 1.11 | 95.18 ± 3.45 | 0.44 ± 0.91 |
| Backdoor | 583 | FN | 0.00 ± 0.00 | 0.10 ± 0.09 | 93.62 ± 4.31 | 6.59 ± 0.31 |
| DoS | 4089 | FN | 0.15 ± 0.02 | 0.45 ± 0.22 | 94.87 ± 2.03 | 13.20 ± 2.11 |
| Exploits | 11132 | FN | 0.73 ± 0.04 | 0.89 ± 0.04 | 94.16 ± 1.21 | 18.12 ± 2.89 |
| Fuzzers | 6062 | FN | 19.65 ± 0.41 | 20.23 ± 0.81 | 90.98 ± 0.70 | 55.94 ± 2.77 |
| Generic | 18871 | FN | 0.01 ± 0.00 | 0.01 ± 0.00 | 32.43 ± 5.64 | 1.38 ± 0.12 |
| Normal | 37000 | FP | 18.57 ± 0.34 | 18.71 ± 0.43 | 6.15 ± 0.40 | 9.16 ± 0.39 |
| Reconnaissance | 3496 | FN | 0.13 ± 0.02 | 0.21 ± 0.04 | 99.41 ± 0.27 | 77.56 ± 3.01 |
| Shellcode | 378 | FN | 1.43 ± 0.14 | 1.59 ± 0.32 | 100.00 ± 0.00 | 95.24 ± 1.39 |
| Worms | 44 | FN | 0.45 ± 1.02 | 0.91 ± 1.24 | 88.18 ± 2.49 | 42.27 ± 16.04 |

IF có FP 6,15% nhưng FN trên Reconnaissance 99,41% và Shellcode 100%; AE bỏ sót Shellcode 95,24%. RF/XGB có FN thấp hơn trên nhiều category nhưng FP khoảng 18,57%/18,71%; riêng Fuzzers vẫn bị bỏ sót khoảng 19,65%/20,23%. Đây là trade-off tại cùng target validation, không phải cùng FPR test. Worms chỉ có 44 mẫu, không kết luận khả năng khái quát từ tỷ lệ nhỏ.

## Ví dụ truy vết

Ví dụ lấy hai lỗi có record_id nhỏ nhất mỗi loại FP/FN của từng model, ở CS seed42 target5%; đây là lựa chọn để mở lại dòng gốc, không phải mẫu ngẫu nhiên đại diện hoặc giải thích nguyên nhân theo feature.

| Run | Record | Nhãn/category | Lỗi | Score | Threshold |
|---|---:|---|---|---:|---:|
| CS-AE-S42 | 28 | Normal | FP | 0.012390 | 0.011699 |
| CS-AE-S42 | 50 | Normal | FP | 0.076255 | 0.011699 |
| CS-AE-S42 | 253 | Exploits | FN | 0.001504 | 0.011699 |
| CS-AE-S42 | 254 | Exploits | FN | 0.001969 | 0.011699 |
| CS-IF-S42 | 38 | Normal | FP | 0.018721 | 0.007771 |
| CS-IF-S42 | 39 | Normal | FP | 0.012433 | 0.007771 |
| CS-IF-S42 | 244 | Reconnaissance | FN | -0.059887 | 0.007771 |
| CS-IF-S42 | 245 | Reconnaissance | FN | -0.059887 | 0.007771 |
| CS-RF-S42 | 1 | Normal | FP | 0.705741 | 0.557282 |
| CS-RF-S42 | 2 | Normal | FP | 0.804156 | 0.557282 |
| CS-RF-S42 | 278 | Fuzzers | FN | 0.429308 | 0.557282 |
| CS-RF-S42 | 282 | Fuzzers | FN | 0.506029 | 0.557282 |
| CS-XGB-S42 | 1 | Normal | FP | 0.895352 | 0.633283 |
| CS-XGB-S42 | 2 | Normal | FP | 0.838029 | 0.633283 |
| CS-XGB-S42 | 255 | Exploits | FN | 0.564823 | 0.633283 |
| CS-XGB-S42 | 278 | Fuzzers | FN | 0.464827 | 0.633283 |

Ví dụ RF record1 là Normal nhưng score 0,705741 vượt threshold 0,557282 nên thành FP. IF record244 là Reconnaissance nhưng score -0,059887 thấp hơn 0,007771 nên thành FN. Score chưa chỉ ra feature nào gây lỗi; điều đó cần phân tích tiếp và không được suy đoán từ category.

## Giới hạn và việc tiếp nối

Bộ CSV đầy đủ có 1.600 dòng theo run/category và 320 nhóm mean/std, bao gồm hai target và cả closed-set/LOACO. Với held-out category, FN rate bằng 1-UADR ở cùng run/target; known/held-out role giữ theo run.json. Kết quả ban đầu chưa thay cho PR curves, score distributions, giải thích feature hoặc độ nhạy khi loại overlap. Giữ các việc này trong mốc tiếp nối của kế hoạch toàn đề tài.
