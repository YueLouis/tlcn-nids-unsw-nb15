# Phân tích PR và phân bố score — đợt 3

**Ngày chạy: 22/10/2026.** Đây là phân tích hậu nghiệm trên prediction/metric đã lưu; không train lại, không chọn lại threshold và không sửa 80 run gốc.

## Cách kiểm

- Đủ 80 run (4 scenario × 4 model × 5 seed), 13.173.120 dòng prediction đã đọc; vì mỗi record có hai target FPR nên còn 6.586.560 cặp record/run để tính AP một lần.
- 1.040 metric đã lưu được đối chiếu lại từ prediction; hash đầu vào giữ nguyên. AP dùng `average_precision_score`, không phải diện tích hình thang PR. Độ lệch qua seed là sample std trên cùng official test, không phải khoảng tin cậy.
- Đường PR và ECDF score dùng seed 42 đã định trước để minh họa; bảng mean/std dùng cả năm seed. Các chấm/ngưỡng dùng threshold lấy từ Normal validation 1% và 5%; FPR trên official test được đo riêng.

## Kết quả AP

AP toàn official test (support 82.332; prevalence Attack 55,06%):

| Scenario | Model | AP mean ± std |
|---|---|---:|
| Closed-set | AE | 0.9254 ± 0.0085 |
| Closed-set | IF | 0.8184 ± 0.0120 |
| Closed-set | RF | 0.9879 ± 0.0001 |
| Closed-set | XGB | 0.9883 ± 0.0003 |
| LOACO DoS | AE | 0.9293 ± 0.0037 |
| LOACO DoS | IF | 0.8183 ± 0.0059 |
| LOACO DoS | RF | 0.9876 ± 0.0001 |
| LOACO DoS | XGB | 0.9881 ± 0.0003 |
| LOACO Exploits | AE | 0.9294 ± 0.0044 |
| LOACO Exploits | IF | 0.8172 ± 0.0037 |
| LOACO Exploits | RF | 0.9831 ± 0.0004 |
| LOACO Exploits | XGB | 0.9840 ± 0.0005 |
| LOACO Reconnaissance | AE | 0.9237 ± 0.0096 |
| LOACO Reconnaissance | IF | 0.8214 ± 0.0102 |
| LOACO Reconnaissance | RF | 0.9852 ± 0.0003 |
| LOACO Reconnaissance | XGB | 0.9852 ± 0.0004 |

AP trong scope Normal và held-out attack (không gồm known attack). Support và prevalence khác nhau nên chỉ so trong cùng scenario; không xếp hạng trực tiếp giữa các scenario:

| Scenario | Model | Support | Held-out prevalence | AP mean ± std |
|---|---|---:|---:|---:|
| LOACO DoS | AE | 41,089 | 9.95% | 0.6001 ± 0.0223 |
| LOACO DoS | IF | 41,089 | 9.95% | 0.1751 ± 0.0031 |
| LOACO DoS | RF | 41,089 | 9.95% | 0.9652 ± 0.0007 |
| LOACO DoS | XGB | 41,089 | 9.95% | 0.9738 ± 0.0006 |
| LOACO Exploits | AE | 48,132 | 23.13% | 0.7701 ± 0.0113 |
| LOACO Exploits | IF | 48,132 | 23.13% | 0.3206 ± 0.0054 |
| LOACO Exploits | RF | 48,132 | 23.13% | 0.9258 ± 0.0046 |
| LOACO Exploits | XGB | 48,132 | 23.13% | 0.9408 ± 0.0057 |
| LOACO Reconnaissance | AE | 40,496 | 8.63% | 0.1376 ± 0.0050 |
| LOACO Reconnaissance | IF | 40,496 | 8.63% | 0.0905 ± 0.0017 |
| LOACO Reconnaissance | RF | 40,496 | 8.63% | 0.7077 ± 0.0173 |
| LOACO Reconnaissance | XGB | 40,496 | 8.63% | 0.6623 ± 0.0357 |

## Điểm vận hành

Mean ± std qua năm seed; `FPR test` có mẫu số Normal test, `known recall` có mẫu số known Attack và `UADR` có mẫu số held-out Attack. Dấu `—` là closed-set không có held-out class.

| Scenario | Model | Target validation FPR | FPR test | Known recall | UADR |
|---|---|---:|---:|---:|---:|
| Closed-set | AE | 1% | 2.72% ± 0.32% | 57.28% ± 7.95% | — ± — |
| Closed-set | AE | 5% | 9.16% ± 0.39% | 79.40% ± 1.36% | — ± — |
| Closed-set | IF | 1% | 0.78% ± 0.15% | 19.97% ± 1.63% | — ± — |
| Closed-set | IF | 5% | 6.15% ± 0.40% | 31.44% ± 2.92% | — ± — |
| Closed-set | RF | 1% | 4.21% ± 0.36% | 90.27% ± 0.25% | — ± — |
| Closed-set | RF | 5% | 18.57% ± 0.34% | 97.14% ± 0.07% | — ± — |
| Closed-set | XGB | 1% | 4.78% ± 0.58% | 91.23% ± 0.31% | — ± — |
| Closed-set | XGB | 5% | 18.71% ± 0.43% | 96.91% ± 0.12% | — ± — |
| LOACO DoS | AE | 1% | 2.92% ± 0.26% | 61.89% ± 4.21% | 47.99% ± 11.35% |
| LOACO DoS | AE | 5% | 9.11% ± 0.39% | 78.91% ± 0.70% | 88.38% ± 1.12% |
| LOACO DoS | IF | 1% | 0.84% ± 0.25% | 21.33% ± 2.04% | 0.72% ± 0.26% |
| LOACO DoS | IF | 5% | 6.11% ± 0.23% | 33.05% ± 2.48% | 4.21% ± 0.99% |
| LOACO DoS | RF | 1% | 3.82% ± 0.23% | 89.23% ± 0.18% | 95.35% ± 0.33% |
| LOACO DoS | RF | 5% | 18.75% ± 0.35% | 96.82% ± 0.18% | 99.81% ± 0.03% |
| LOACO DoS | XGB | 1% | 4.74% ± 0.17% | 90.60% ± 0.14% | 96.98% ± 0.12% |
| LOACO DoS | XGB | 5% | 18.41% ± 0.55% | 96.56% ± 0.17% | 99.33% ± 0.18% |
| LOACO Exploits | AE | 1% | 2.49% ± 0.20% | 67.39% ± 3.72% | 44.73% ± 3.90% |
| LOACO Exploits | AE | 5% | 9.01% ± 0.38% | 78.83% ± 0.70% | 80.69% ± 2.90% |
| LOACO Exploits | IF | 1% | 0.89% ± 0.15% | 26.82% ± 0.83% | 0.35% ± 0.02% |
| LOACO Exploits | IF | 5% | 6.26% ± 0.29% | 38.07% ± 0.82% | 5.29% ± 0.96% |
| LOACO Exploits | RF | 1% | 4.15% ± 0.28% | 87.85% ± 0.25% | 81.06% ± 1.27% |
| LOACO Exploits | RF | 5% | 18.32% ± 0.82% | 96.02% ± 0.39% | 97.06% ± 0.57% |
| LOACO Exploits | XGB | 1% | 4.79% ± 0.77% | 88.77% ± 0.55% | 87.25% ± 1.17% |
| LOACO Exploits | XGB | 5% | 18.70% ± 0.55% | 95.75% ± 0.33% | 97.07% ± 0.27% |
| LOACO Reconnaissance | AE | 1% | 2.51% ± 0.37% | 63.47% ± 10.13% | 6.37% ± 2.30% |
| LOACO Reconnaissance | AE | 5% | 9.07% ± 0.44% | 84.27% ± 1.25% | 23.82% ± 3.75% |
| LOACO Reconnaissance | IF | 1% | 0.87% ± 0.24% | 21.61% ± 1.85% | 0.00% ± 0.00% |
| LOACO Reconnaissance | IF | 5% | 6.20% ± 0.43% | 34.54% ± 3.27% | 0.66% ± 0.26% |
| LOACO Reconnaissance | RF | 1% | 4.27% ± 0.18% | 89.70% ± 0.11% | 60.90% ± 2.30% |
| LOACO Reconnaissance | RF | 5% | 18.58% ± 0.24% | 96.94% ± 0.13% | 97.73% ± 0.30% |
| LOACO Reconnaissance | XGB | 1% | 5.06% ± 0.50% | 90.54% ± 0.30% | 65.76% ± 6.19% |
| LOACO Reconnaissance | XGB | 5% | 18.76% ± 0.47% | 96.53% ± 0.12% | 98.06% ± 0.85% |

## Cách đọc hiện tại

- RF/XGB có AP toàn test cao và ổn định hơn IF/AE trong bảng này, nhưng điều đó không đủ để gọi mô hình tốt nhất cho mọi mục tiêu; điểm vận hành cho thấy FPR test có thể cao hơn target validation.
- Ở LOACO, phải đọc UADR cùng held-out support và target. AP trong scope Normal/held-out cho biết thứ tự score ở đúng slice đó; nó không thay UADR tại threshold.
- AP cao không chứng minh phát hiện tốt category bị giấu; ngược lại UADR thấp ở một target có thể bị che bởi score distribution và trade-off với FPR. Không suy rộng LOACO thành mọi zero-day ngoài UNSW-NB15.
- Bản này chưa phân tích feature importance, proto/service/state và chưa định lượng tác động của overlap bằng retrain. Đó là việc tiếp theo trong phân công; nếu chạy loại overlap phải tạo run mới riêng.

## Artifact

- `AP_ALL_RUNS.csv`, `AP_MEAN_STD.csv` — AP từng run và mean/std.
- `OPERATING_POINTS_ALL_RUNS.csv`, `OPERATING_POINTS_MEAN_STD.csv` — điểm vận hành từng run và tổng hợp.
- `SCORE_QUANTILES_ALL_RUNS.csv` — quantile score theo vai trò.
- `PR_*.png`, `SCORE_ECDF_*.png` — hình seed42 theo chính sách đã ghi.
- `PR_SCORE_AUDIT.json` — commit, phiên bản, hash input, số dòng và điều kiện kiểm.

Phân công đợt 3: [Anh–Thu–Tín](../../../management/phan_cong_dot_03_20261022/00_PHAN_CONG_DOT_03.md).
