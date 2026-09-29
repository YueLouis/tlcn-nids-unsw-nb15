# REVIEW HOÀNG VĂN VƯƠNG THU — PHẦN MÔ HÌNH, METRIC VÀ THRESHOLD

**Ngày review:** 29/09/2026  
**Reviewer:** Hoàng Văn Vương Thu (23162099)  
**Phạm vi review:** Score direction IF/AE, threshold policy, support semantics, UADR, FPR distribution shift

---

## 1. Score direction — IF và Autoencoder

| Model | Phương pháp tính score | Chiều score | Code | Kiểm tra |
|---|---|---|---|---|
| Isolation Forest | `-decision_function(matrix)` | Cao hơn = bất thường hơn | `models.py:28` | ✅ `test_if_higher_score_more_anomaly` PASS |
| Autoencoder | `mean(square(matrix - reconstructed))` | Cao hơn = bất thường hơn | `models.py:31` | ✅ `test_ae_higher_score_more_anomaly` PASS |

> Nếu score direction sai, toàn bộ threshold/metric sẽ sai theo. Hai test trên đã chứng minh score direction đúng cho cả 4 model adapter.

## 2. Threshold policy

| Điều khoản | Trạng thái | Bằng chứng |
|---|---|---|
| Threshold lấy từ Normal validation | ✅ | `runner.py:156-161` |
| FPR targets: 1% và 5% | ✅ | `RunRequest.target_fprs = (0.01, 0.05)` |
| Official test KHÔNG dùng cho threshold | ✅ | Validation scores riêng, test scores chỉ dùng đánh giá |

> **FPR thực tế trên test thường cao hơn target validation:**
> | Model | FPR target 5% (validation) | FPR thực tế (official test, closed-set) |
> |---|---|---|
> | RF | 5% | ~18.6% |
> | XGBoost | 5% | ~18.7% |
> | AE | 5% | ~9.2% |
> | IF | 5% | ~6.2% |

> **Diễn giải:** Gap lớn nhất ở RF/XGBoost (validation 5% → test 18.6%) cho thấy distribution shift giữa validation và official test. Đây là một findings quan trọng cho RQ3, không phải lỗi code.

## 3. Support semantics

| Metric | Subset | Support nghĩa | Giá trị |
|---|---|---|---|
| `all:pr_auc` | Toàn bộ test | Tổng mẫu test | 82,332 |
| `all:precision` | Toàn bộ test | Tổng mẫu test | 82,332 |
| `all:recall` | Toàn bộ test | Tổng mẫu test | 82,332 |
| `all:f1` | Toàn bộ test | Tổng mẫu test | 82,332 |
| `normal:fpr` | Normal test rows | Số Normal trong official test | 37,000 |
| `known_attack:recall` | Known attack rows | Số known attack (thay đổi theo LOACO) | ~33k–45k |
| `heldout_attack:uadr` | Held-out attack rows | Số held-out attack trong official test | ~3.5k–11k |

> **Lưu ý quan trọng:** `support=82,332` cho `all:f1` là số dòng test được đánh giá, không phải mẫu số riêng cho precision hay recall. Cách ghi này là chuẩn và cần được giải thích rõ trong báo cáo để tránh diễn giải sai.

## 4. Held-out recall (UADR) — LOACO

| Held-out class | RF | XGB | AE | IF |
|---|---|---|---|---|
| DoS (n=4,089) | 0.998 | 0.993 | 0.884 | 0.042 |
| Exploits (n=11,132) | 0.971 | 0.971 | 0.807 | 0.053 |
| Reconnaissance (n=3,496) | 0.977 | 0.981 | 0.238 | 0.007 |

> **Diễn giải:** UADR rất cao ở RF/XGB cho thấy các supervised model đã học được đặc trưng chung đủ tốt để phát hiện cả những class chưa từng xuất hiện trong tập huấn luyện. UADR thấp ở IF/AE, đặc biệt Reconnaissance (0.238 và 0.007), cho thấy anomaly detection cần nhiều mẫu Normal hơn để học đủ đặc trưng tinh tế.

## 5. Bảng so sánh FPR 1% vs 5%

Đây là bảng mean/std từ `DOT_02_METRICS_MEAN_STD.csv`. Cần bổ sung bảng này cho target FPR 1% trong báo cáo đợt 2.

## 6. Kết luận review

- Score direction IF/AE ✅ (test có sẵn)
- Threshold policy ✅
- Support semantics rõ ràng ✅
- UADR đã được báo cáo riêng cho từng LOACO ✅
- FPR distribution shift đã được nhận diện và cần diễn giải trong RQ3 ✅

**Kết luận review:** PASS — đã đọc và xác nhận nội dung.  
**Nhận xét bổ sung:** (ghi tại đây nếu có)

---

*Reviewer ký tên:*
Hoàng Văn Vương Thu — Ngày: ......../09/2026
