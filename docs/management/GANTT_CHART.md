# GANTT CHART THEO NGÀY

> Đây là baseline dự kiến của toàn đề tài, không phải nhật ký thực hiện. Bốn baseline và 80 run đã có artifact ngày 26/09, sớm hơn cửa sổ dự kiến. Tiến độ thực tế và phần còn thiếu: `TIEN_DO_HIEN_TAI_20261013.md`. Không thay đổi ngày của 80 run để khớp Gantt.


**Ngày bắt đầu thực tế:** 17/08/2026  
**Ngày hoàn thành dự kiến:** 23/12/2026  
**Lưu ý:** nhóm đăng ký thực hiện từ 17/08/2026. Báo cáo này hiệu chỉnh lại
baseline cũ 10/09/2026 để phản ánh đúng bốn tuần đầu. Báo cáo gửi giảng viên
mỗi 4 tuần, không phải hàng tuần.

| Thời gian | Trọng tâm | Chủ trì | Mốc kiểm chứng |
|---|---|---|---|
| 17/08-23/08/2026 | Chọn hướng, soạn đề cương và xác định bài toán | Cả nhóm | Đề cương ban đầu |
| 24/08-30/08/2026 | Gửi đăng ký, làm rõ phạm vi và chuẩn bị tài liệu giải thích | Tín + cả nhóm | Hồ sơ đăng ký |
| 31/08-06/09/2026 | Chốt phân công, luồng bàn giao và cách lưu trữ | Cả nhóm | Phân công nhóm |
| 07/09-13/09/2026 | Khóa protocol, RQ, run matrix, result schema và validator | Tín + cả nhóm | Gate 1 draft + Báo cáo 4 tuần |
| 14/09-20/09/2026 | Review chéo, họp Gate 1, tải dữ liệu chính thức và checksum | Cả nhóm, Trâm Anh chủ trì dữ liệu | Gate 1 + data manifest |
| 21/09-27/09/2026 | Audit schema/chất lượng/duplicate và chốt data contract | Trâm Anh + Tín | Gate 2 |
| 28/09-04/10/2026 | Preprocessing và kiểm thử chống leakage | Tín | Gate 3 |
| 05/10-11/10/2026 | Random Forest/XGBoost và evaluator | Tín + Thu | Supervised baseline |
| 12/10-18/10/2026 | Isolation Forest/Autoencoder và smoke test bốn model | Thu | Gate 4 |
| 19/10-25/10/2026 | Closed-set đủ seed, bảng/hình RQ1 | Tín + Thu | RQ1 |
| 26/10-01/11/2026 | LOACO Reconnaissance | Tín + Thu | LOACO-R |
| 02/11-08/11/2026 | LOACO DoS | Tín + Thu | LOACO-D |
| 09/11-15/11/2026 | LOACO Exploits và tổng hợp 80 run | Tín + Thu | Gate 5 |
| 16/11-22/11/2026 | Error analysis và bàn luận | Thu + Trâm Anh | Chương kết quả |
| 23/11-29/11/2026 | Prototype dùng artifact đã khóa | Tín + cả nhóm | Gate 6 |
| 30/11-06/12/2026 | Hoàn thiện báo cáo và kiểm tra chéo | Trâm Anh + cả nhóm | Bản báo cáo |
| 07/12-13/12/2026 | Slide, câu hỏi phản biện và chạy thử demo | Cả nhóm | Bộ bảo vệ |
| 14/12-20/12/2026 | Đóng gói tái lập, rà soát cuối và chuẩn bị nộp | Cả nhóm | Gate 7 |
| 21/12-23/12/2026 | Nộp hồ sơ cuối theo yêu cầu môn | Cả nhóm | Hồ sơ cuối |

## Các đợt gửi giảng viên

| Hạn nội bộ | Nội dung tối thiểu |
|---|---|
| 14/09/2026 (gửi bù) | Việc đã làm 4 tuần đầu, phân công, Gantt ngày cụ thể, protocol và code/config hiện có |
| 12/10/2026 | Data audit, pipeline, kiểm thử leakage, cấu hình bốn baseline và kết quả closed-set ban đầu |
| 09/11/2026 | Kết quả LOACO, metric, error analysis ban đầu và phần báo cáo đã viết |
| 23/12/2026 | Báo cáo, mã nguồn/config, slide, demo và hướng dẫn tái lập cuối |

Mỗi đợt phải ghi rõ: đã hoàn thành, artifact/đường dẫn, kiểm tra đã chạy, vấn đề
đang mở, quyết định cần thầy xác nhận và kế hoạch giai đoạn kế tiếp.
