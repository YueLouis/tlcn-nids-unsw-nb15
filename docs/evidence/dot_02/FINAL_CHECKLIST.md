# Checklist Đợt 2 - Kiểm tra cuối

Ngày kiểm tra: 26/09/2026

> Đây là checklist tại mốc 26/09. Đọc [đánh giá và phân công ngày 29/09](../../management/PHAN_CONG_DOT_02_HIEN_TAI_20260929.md) để theo dõi các điểm còn mở về duplicate/overlap, kiểm thử và báo cáo. Các giá trị duplicate=0 ở đây tính cả cột định danh; chưa thay thế audit trên feature.

| Mã | Đầu ra | Bằng chứng hiện tại | Trạng thái |
|---|---|---|---|
| D2.1 | Gate 1 protocol được review | `docs/protocol/GATE_1_CHECKLIST.md`, `docs/meetings/BIEN_BAN_HOP_01.md` | CHỜ BA THÀNH VIÊN KÝ |
| D2.2 | Manifest và fingerprint hai official split | `artifacts/data/data_manifest.json` | PASS kỹ thuật |
| D2.3 | Audit schema/chất lượng/label/category | `artifacts/data/data_manifest.json`, báo cáo PDF | PASS kỹ thuật |
| D2.4 | Data contract | `docs/evidence/dot_02/DATA_CONTRACT.md`, `docs/protocol/GATE_2_CHECKLIST.md` | PASS kỹ thuật; chờ review Gate 2 |
| D2.5 | Preprocessing chống leakage | `src/nids_benchmark/preprocessing.py`, `src/nids_benchmark/data.py`, 9 unit tests | PASS kỹ thuật |
| D2.6 | Bốn scenario và LOACO roles | Bảng scenario trong PDF | PASS tài liệu |
| D2.7 | Bốn baseline và artifact | `results/runs/`: 80 run x 4 artifact | PASS kỹ thuật |
| D2.8 | Test có tên, input/hành vi, expected và kết quả | `tests/`, log kiểm tra cuối, ảnh `D2_03` | PASS: 9/9 |
| D2.9 | Metric, threshold, support, mean/std | `docs/reports/DOT_02_METRICS_ALL_RUNS.csv`, `DOT_02_METRICS_MEAN_STD.csv` | PASS kỹ thuật |
| D2.10 | Ma trận tiến độ chi tiết | Chương 1 và phụ lục PDF | PASS tài liệu |

## Kiểm tra tự động cuối

- `python -m unittest discover -s tests -q`: 9/9 PASS.
- `python scripts/validate_protocol.py`: 80 run ID hợp lệ.
- 80 thư mục run tồn tại.
- Mỗi run có `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib`.
- Hai official split: train 175341 x 45, test 82332 x 45; missing/duplicate/infinity đều bằng 0.
- PDF đã compile và render kiểm tra ở A4, layout theo mẫu đợt 1.

## Phần nhóm phải xác nhận

Trâm Anh, Vương Thu và Tín cần đọc checklist, data contract, PDF và biên bản; sau đó ghi nhận xét, ngày review và PASS/FAIL Gate 1/Gate 2. Đây là bước xác nhận người thật, không được thay bằng validator tự động.
