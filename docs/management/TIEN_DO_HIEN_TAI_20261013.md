# Tiến độ hiện tại - hiệu chỉnh 17/10/2026

Bản hiện tại thay cho các bảng trạng thái tháng 9. Tỷ lệ dưới đây đếm đầu ra theo checklist, không đo mức hiểu và không lấy trung bình thành tỷ lệ toàn đề tài.

| Phần | Đã có | Còn thiếu | Tiêu chí / mức hiện tại | Chủ trì / review |
|---|---|---|---|---|
| Đặt vấn đề và phạm vi | Bối cảnh, mục tiêu, 3 RQ, phạm vi | Theo dõi góp ý mới của thầy | 4/4 mục bản hiện tại; 100% | Cả nhóm; Tín tổng hợp |
| Lý thuyết NIDS | Flow/NIDS, chữ ký-bất thường, supervised-anomaly | Chưa triển khai cảm biến/xử lý cảnh báo thực tế | 4/4 mục mô tả khái niệm; 100% phạm vi trình bày | Trâm Anh / cả nhóm |
| UNSW-NB15 | Nguồn, split, schema, imbalance/overlap | Phân tích tác động overlap tách riêng bên dưới | 4/4 mục mô tả; 100% | Trâm Anh / Tín |
| Bốn mô hình cơ sở | Cơ chế, công thức, score, dữ liệu fit, cấu hình và giới hạn RF/XGB/IF/AE | Nhóm còn tự kiểm phần giải thích | 4/4 mô tả; mức hiểu còn mở | Trâm Anh, Thu / Tín |
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

PDF hiện hành: 37 trang, hiệu chỉnh toàn văn 17/10; bảng hai target tại trang vật lý 30. Protocol 80/80 chỉ là kiểm ID; Gate 1/Gate 2 nội dung chưa nghiệm thu.

## Bằng chứng chính

Tính từ repo `tlcn-nids-unsw-nb15/`:

- `docs/report_cumulative/BAO_CAO_TLCN_TICH_LUY_DOT_02.tex` và `output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf`.
- `docs/evidence/dot_02/final_20261013/`: log thật, audit prediction, metadata nguồn và bản ghi xác nhận.
- `docs/references/RELATED_WORK_MATRIX_DOT_02.csv`: trang/đoạn, điều kiện và giới hạn từng nguồn; S07 chưa có toàn văn, nghiệm thu nhóm còn mở.
- `artifacts/data/data_manifest.json`, `artifacts/data/duplicate_overlap_audit.json`.
- `results/runs/<run-id>/`: run.json, metrics.csv, predictions.csv, model_bundle.joblib.

## Xác nhận và phân công tiếp tục

Cập nhật 17/10/2026: sau lời báo đồng ý trước đó, nhóm trưởng làm rõ rằng chưa chắc mức hiểu từng thành viên và cả nhóm dự kiến tự rà soát hai đợt ngày 18/10. Xác nhận lịch sử ngày 13/10 và lời báo đồng ý ngày 17/10 được giữ ở `XAC_NHAN_NHOM_20261013.md`; không dùng làm bằng chứng đã nghiệm thu nội dung. Mô tả phân công trong bảng là kế hoạch, cần đối chiếu đóng góp thực tế. Không tạo chữ ký hoặc ngày review thay thành viên; đây không phải phê duyệt của giảng viên.

Trâm Anh tiếp tục related-work matrix và lý thuyết NIDS; Thu phụ trách phân tích lỗi/điều kiện so sánh; Tín tích hợp tái lập và prototype. Mỗi mục chỉ chuyển hoàn thành khi có sản phẩm và review thật. Đọc kế hoạch gốc tại `../tlcn-nids-unsw-nb15/docs/management/GANTT_CHART.md`; baseline thời gian và thực tế chạy sớm được phân biệt trong Chương 3 PDF.
