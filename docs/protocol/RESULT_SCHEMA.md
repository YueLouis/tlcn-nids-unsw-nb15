# RESULT SCHEMA V1

Schema này là hợp đồng đầu ra để bốn mô hình có thể được đánh giá bằng cùng một
evaluator. Các giá trị bên dưới chỉ là placeholder, không phải kết quả thật.

## `run.json`

```json
{
  "run_id": "LR-RF-S42",
  "protocol_version": "1.0-draft",
  "scenario": "loaco_reconnaissance",
  "heldout_class": "Reconnaissance",
  "model": "random_forest",
  "model_family": "supervised",
  "seed": 42,
  "status": "planned",
  "data_fingerprint": null,
  "config_fingerprint": null,
  "threshold_policy": {
    "source_split": "normal_validation",
    "target_fpr": [0.01, 0.05],
    "score_direction": "higher_means_more_attack_like"
  },
  "started_at": null,
  "completed_at": null,
  "software_versions": {},
  "artifact_paths": {}
}
```

## `metrics.csv` dạng long

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `run_id` | string | ID duy nhất liên kết với `run.json` |
| `split` | string | `validation` hoặc `official_test` |
| `subset` | string | `all`, `normal`, `known_attack`, `heldout_attack` |
| `metric` | string | Tên metric đã khóa |
| `value` | float/null | Giá trị; null nếu metric không có nghĩa |
| `support` | integer | Số record trong mẫu số |
| `target_fpr` | float/null | 0.01/0.05 nếu metric phụ thuộc operating point |
| `threshold` | float/null | Threshold lấy từ validation, không chọn từ test |

## `predictions.csv`

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `record_id` | string/int | ID truy vết record; không dùng làm feature |
| `run_id` | string | ID run |
| `split` | string | Split đánh giá |
| `attack_cat` | string/null | Chỉ để phân tích, không dùng làm feature |
| `evaluation_role` | string | `normal`, `known_attack`, `heldout_attack` |
| `y_true` | integer | 0 = Normal, 1 = Attack |
| `score` | float | Cao hơn = giống Attack/anomaly hơn |
| `target_fpr` | float | Operating point đang đánh giá |
| `threshold` | float | Threshold khóa từ validation |
| `y_pred` | integer | Nhãn sau threshold |

## Điều kiện một run hợp lệ

1. `run_id` khớp scenario, model và seed.
2. Held-out class vắng mặt trong toàn bộ vùng phát triển của vòng LOACO.
3. Preprocessor, hyperparameter và threshold không học từ official test.
4. `label`, `attack_cat`, `id` không xuất hiện trong feature matrix.
5. Score của mọi model đã quy về cùng chiều.
6. Có data/config fingerprint, software version và artifact path truy vết được.
7. Metric có support; trường hợp mẫu số bằng 0 trả null và cảnh báo.

