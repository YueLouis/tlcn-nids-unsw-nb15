# REVIEW TRỊNH TRÂM ANH — PHẦN DỮ LIỆU VÀ DATA CONTRACT

**Ngày review:** 29/09/2026  
**Reviewer:** Trịnh Trâm Anh (23162005)  
**Phạm vi review:** Manifest, schema, duplicate/overlap, dtype, missing, label, attack category, data contract

---

## 1. Kiểm tra manifest

| Hạng mục | Kết quả |
|---|---|
| `artifacts/data/data_manifest.json` | ✅ Tồn tại |
| Train: 175,341 dòng × 45 cột | ✅ Khớp |
| Test: 82,332 dòng × 45 cột | ✅ Khớp |
| SHA-256 train: `bec7dd5e...e0648fa` | ✅ Khớp checksum |
| SHA-256 test: `734fe664...c0a559` | ✅ Khớp checksum |
| Missing: 0 (cả 2 split) | ✅ |
| Infinity: 0 (cả 2 split) | ✅ |

## 2. Audit duplicate

| Cách đếm | Train | Test | Ghi chú |
|---|---|---|---|
| Full-row (có id) | 0 | 0 | ✅ Khớp manifest |
| Bỏ id, giữ label + attack_cat | 67,601 | 26,387 | Hàng identical nhưng khác id — không tự động là leakage |
| Chỉ 42 feature | 74,301 | 28,386 | Cùng 42 feature, khác nhau ở metadata |

> **Diễn giải:** `duplicate=0` trong manifest tính full-row bao gồm `id`. Khi bỏ `id` vẫn còn nhiều dòng trùng do UNSW-NB15 quy nén các packet-flow có đặc trưng giống nhau. Đây là tính chất tự nhiên của dữ liệu network flow, không chứng minh có rò rỉ giữa train/test.

## 3. Cross-split overlap

| Hạng mục | Giá trị |
|---|---|
| Test rows trùng đủ 42 features với train | 8,541 / 82,332 (10.4%) |

### Overlap theo held-out class (sau LOACO removal)

Đây là test rows của held-out class vẫn có hàng trùng trong train (sau khi LOACO loại held-out class khỏi development):

| LOACO scenario | Held-out class | Overlap test rows | Tổng test held-out | Tỷ lệ |
|---|---|---|---|---|
| LOACO-R | Reconnaissance | 262 | 3,496 | 7.5% |
| LOACO-D | DoS | 2,000 | 4,089 | 48.9% |
| LOACO-E | Exploits | 1,800 | 11,132 | 16.2% |

> **Diễn giải:** Overlap lớn nhất ở DoS (48.9%) — giải thích một phần vì sao UADR của RF/XGB trên LOACO-DoS rất cao (~0.99). Reconnaissance overlap thấp nhất (7.5%) — tương ứng UADR của AE trên LOACO-R thấp hơn rõ rệt (~0.24).

## 4. Label và attack category

| Hạng mục | Train | Test |
|---|---|---|
| Normal (label=0) | 56,000 | 37,000 |
| Attack (label=1) | 119,341 | 45,332 |
| Tổng category | 10 (9 attack + Normal) | 10 |

Attack category lớn nhất: Generic (40,000 train / 18,871 test), Exploits (33,393 / 11,132), Fuzzers (18,184 / 6,062), DoS (12,264 / 4,089), Reconnaissance (10,491 / 3,496).

## 5. Data contract review

| Điều khoản | Trạng thái |
|---|---|
| `id` không dùng làm feature | ✅ Loại bởi `FORBIDDEN_FEATURES` |
| `label` chỉ làm target | ✅ |
| `attack_cat` chỉ dùng cho scenario/analysis | ✅ |
| `proto`, `service`, `state` xử lý categorical | ✅ One-hot trong preprocessor |
| Normal=0, Attack=1 được test | ✅ `test_binary_label_normalization` PASS |

## 6. Kết luận

- Manifest và checksum ✅
- Schema audit đầy đủ ✅
- Duplicate/overlap đã được audit và có diễn giải rõ ✅
- Data contract khớp với mã nguồn ✅

**Kết luận review:** PASS — đã đọc và xác nhận nội dung.  
**Nhận xét bổ sung:** (ghi tại đây nếu có)

---

*Reviewer ký tên:*
Trịnh Trâm Anh — Ngày: ......../09/2026
