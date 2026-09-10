# GLOSSARY V0.1 - TRÂM ANH REVIEW

| Thuật ngữ | Định nghĩa dùng trong đề tài | Cách tránh hiểu sai |
|---|---|---|
| NIDS | Hệ thống phát hiện xâm nhập mạng từ dữ liệu lưu lượng/flow và cảnh báo record đáng ngờ | Không đồng nhất flow-based ML với phân tích raw packet/payload |
| Supervised learning | Học từ record có nhãn Normal/Attack và các lớp attack đã xuất hiện trong vùng train | Không gọi mô hình supervised là học được mọi attack chưa thấy |
| Anomaly detection | Học đặc điểm của Normal để gán score bất thường cho record lệch khỏi Normal | Không mặc định mọi anomaly đều là một attack cụ thể |
| Closed-set | Vùng phát triển và test có cùng các lớp attack theo thiết kế baseline | Đây là mốc so sánh, không phải đánh giá held-out |
| Held-out attack class | Một attack class bị loại khỏi toàn bộ vùng phát triển mô hình trong một vòng LOACO | Không dùng từ này để khẳng định zero-day ngoài thực tế |
| LOACO | Leave-one-attack-class-out: loại một class trước split/fit/tuning rồi đánh giá class đó ở official test | Held-out class phải vắng mặt trong development, nhưng vẫn có support ở test |
| UADR | Tỷ lệ record của held-out attack class được gán Attack/anomaly trên official test | Chỉ có nghĩa trong vòng LOACO; báo cáo cùng support |
| Known Attack Recall | Recall trên các attack class không bị held out trong vòng LOACO | Không đưa held-out class vào tử số hoặc mẫu số |
| FPR | Tỷ lệ Normal bị cảnh báo là Attack tại threshold đang xét | Threshold phải lấy từ Normal validation, không lấy từ test |
| Score direction | Quy ước chung: score cao hơn nghĩa là giống Attack/anomaly hơn | Mô hình có chiều score ngược phải đổi dấu trước evaluator |

**Người review:** Trịnh Trâm Anh  
**Trạng thái:** DRAFT - cần cả nhóm xác nhận trước Gate 1

