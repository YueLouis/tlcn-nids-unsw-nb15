# Tiến độ hiện tại - bổ sung 14/10/2026

Bản hiện tại thay cho các bảng trạng thái tháng 9. Tỷ lệ dưới đây đếm đầu ra theo checklist, không đo mức hiểu và không lấy trung bình thành tỷ lệ toàn đề tài.

| Phần | Đã có | Còn thiếu | Tiêu chí / mức hiện tại | Chủ trì / review |
|---|---|---|---|---|
| Đặt vấn đề và phạm vi | Bối cảnh, mục tiêu, 3 RQ, phạm vi | Theo dõi góp ý mới của thầy | 4/4 mục bản hiện tại; 100% | Cả nhóm; Tín tổng hợp |
| Lý thuyết NIDS | Flow/NIDS, chữ ký-bất thường, supervised-anomaly | Vị trí triển khai/xử lý cảnh báo chi tiết | 3/4 mục; 75% | Trâm Anh / cả nhóm |
| UNSW-NB15 | Nguồn, split, schema, imbalance/overlap | Phân tích tác động overlap tách riêng bên dưới | 4/4 mục mô tả; 100% | Trâm Anh / Tín |
| Bốn mô hình cơ sở | Nguyên lý RF/XGB/IF/AE và cấu hình thực tế | Tổng quan biến thể sâu chưa thuộc bản hiện tại | 4/4 mô tả cơ sở; 100% | Trâm Anh, Thu / Tín |
| Mẫu ma trận tài liệu | Schema và 13 dòng nguồn nền | Không thiếu cấu trúc mẫu | 1/1 mẫu; 100% | Trâm Anh / Thu |
| Định danh nguồn | 12 DOI metadata đối chiếu; trang UNSW | Không đồng nghĩa đọc toàn văn | 13/13 nguồn có định danh; 100% | Trâm Anh / Tín |
| Đối chiếu nội dung nguồn | 12/13 nguồn có đoạn/trang, phạm vi và giới hạn; ma trận đã điền nội dung | S07 chỉ abstract; nghiệm thu toàn bài còn mở | 12/13 có đối chiếu đoạn nguồn; 92,3% | Trâm Anh / Thu |
| Protocol | 4 scenario x 4 model x 5 seed, schema/threshold/metric | Theo dõi thay đổi nếu có | 80/80 ID hợp lệ; 100% | Tín / Thu |
| Audit dữ liệu | Manifest 2 split, 42 features, duplicate/overlap | Thí nghiệm ảnh hưởng overlap còn mở | 2/2 split audit; 100% phạm vi này | Trâm Anh / Tín, Thu |
| Baseline và thí nghiệm | 80 run, 320 artifact, 16 nhóm mean/std, 2 target FPR | Chưa phải hoàn thành toàn đề tài | 80/80 run; 100% | Tín, Thu / cả nhóm |
| Kiểm thử | 17/17 test và protocol validator PASS | Không chứng nhận triển khai thực tế | 17/17 test; 100% phạm vi test | Tín, Thu / Trâm Anh |
| Phân tích lỗi ban đầu | 80 run, 1.600 dòng category, 320 nhóm mean/std và 16 ví dụ; 760 đối chiếu metric khớp | PR/score distribution, giải thích feature, độ nhạy overlap còn là bước sâu | 80/80 run phân tích category; 100% phạm vi ban đầu | Thu / Trâm Anh |
| Prototype hoàn chỉnh | Có CLI `scripts/predict_csv.py` | Demo hoàn chỉnh, bộ tình huống và nghiệm thu | 0/1 bộ demo nghiệm thu; 0% | Tín / cả nhóm |
| Viết và bàn giao cuối | Báo cáo tích lũy đợt 2 | Bản cuối, slide/bảo vệ, đóng gói nghiệm thu cuối | 1/4 đầu ra; 25% | Trâm Anh biên tập / cả nhóm |

## Bằng chứng chính

Tính từ repo `tlcn-nids-unsw-nb15/`:

- `docs/report_cumulative/BAO_CAO_TLCN_TICH_LUY_DOT_02.tex` và `output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf`.
- `docs/evidence/dot_02/final_20261013/`: log thật, audit prediction, metadata nguồn và bản ghi xác nhận.
- `docs/references/RELATED_WORK_MATRIX_DOT_02.csv`: trang/đoạn, điều kiện và giới hạn từng nguồn; S07 chưa có toàn văn, nghiệm thu nhóm còn mở.
- `artifacts/data/data_manifest.json`, `artifacts/data/duplicate_overlap_audit.json`.
- `results/runs/<run-id>/`: run.json, metrics.csv, predictions.csv, model_bundle.joblib.

## Xác nhận và phân công tiếp tục

Nhóm trưởng cho biết cả ba thành viên đã xác nhận nội dung ngày 13/10; ngày 17/10/2026 nhóm trưởng báo cả ba thành viên đã xác nhận bản hiện tại, gồm phần bổ sung ngày 14/10; bản ghi ở `../evidence/dot_02/final_20261013/XAC_NHAN_NHOM_20261013.md`. Không tạo chữ ký hoặc ngày review thay thành viên; đây không phải phê duyệt của giảng viên.

Trâm Anh tiếp tục related-work matrix và lý thuyết NIDS; Thu phụ trách phân tích lỗi/điều kiện so sánh; Tín tích hợp tái lập và prototype. Mỗi mục chỉ chuyển hoàn thành khi có sản phẩm và review thật. Đọc kế hoạch gốc tại `GANTT_CHART.md`; baseline thời gian và thực tế chạy sớm được phân biệt trong Chương 3 PDF.
