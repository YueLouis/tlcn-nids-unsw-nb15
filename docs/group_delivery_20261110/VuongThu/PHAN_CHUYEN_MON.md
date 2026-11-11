# Kết quả, ngưỡng và phân tích lỗi

## Đọc ba chỉ số chính

Attack là lớp dương. FPR = FP / số Normal, recall Attack = TP / số Attack, UADR = số held-out được phát hiện / tổng held-out. Mẫu số của FPR khác mẫu số của UADR. AP mô tả xếp hạng theo score trên nhiều ngưỡng; nó không thay tỷ lệ phát hiện và báo nhầm tại một ngưỡng cụ thể.

Hai target 1% và 5% là ngân sách FPR trên Normal validation. Chúng không bảo đảm FPR test bằng 1% hoặc 5%. Với RF closed-set, đổi target 1% sang 5% làm recall test trung bình tăng 90,27% lên 97,14%, đồng thời FPR test tăng 4,21% lên 18,57%. Số liệu lấy từ `HAI_NGUONG_FPR.csv`, trung bình năm seed cùng official test.

## Kết quả chính của đợt 3

Trong LR, RF có AP toàn test khoảng 0,9852 nhưng AP chỉ trên Normal và Reconnaissance held-out là 0,7077. XGB tương ứng 0,9852 và 0,6623. Chỉ đọc AP toàn test dễ bỏ qua độ khó riêng của held-out vì phần known Attack cũng góp vào chỉ số chung. Hai scope có thành phần và tỷ lệ dương khác nhau; không dùng chênh lệch AP giữa scope như một phép so sánh công bằng giữa model.

IF ở closed-set có FPR test thấp hơn RF tại target 5% (6,15% so với 18,57%) nhưng recall Attack thấp hơn (31,44% so với 97,14%). AE và IF có cách sinh score khác RF/XGB. Cần đọc hướng score đã chuẩn hóa, support, threshold và cả hai loại lỗi; không chọn model tốt nhất từ một con số.

## Ví dụ có thể truy vết

LR-RF-S42, target validation 5%, threshold 0,55681266574524546:

| ID | Nhãn thật | Score | Dự đoán | Kết quả |
|---|---|---:|---|---|
| 68699 | Normal | 0,5568311122449866 | Attack | FP: vượt ngưỡng rất ít |
| 975 | Reconnaissance | 0,55649131907993055 | Normal | FN: thấp hơn ngưỡng |

Nguồn là `results/runs/LR-RF-S42/predictions.csv`; hash và dữ liệu hai hàng được giữ trong `NGUON_VI_DU_THU.csv`. Score sát ngưỡng giải thích quy tắc quyết định, chưa chứng minh feature nào gây ra lỗi. Các ví dụ được chọn theo tiêu chí gần ngưỡng để mở lại, không phải mẫu ngẫu nhiên đại diện.

## Độ ổn định và giới hạn

`DO_ON_DINH_LOI.csv` đếm lỗi lặp qua năm seed; `VI_DU_GAN_NGUONG.csv` lưu ví dụ kèm vai trò và feature. Năm seed đều dùng cùng official test, nên độ lệch chuẩn không phải khoảng tin cậy trên năm dataset độc lập. Biểu đồ theo category cũng phải đọc cùng support; Worms chỉ có 44 mẫu test.

ZIP giữ mã `evaluation.py`, adapter IF/AE trong `models.py`, các test score/metric và script phân tích theo đường dẫn gốc. Đây là mã dùng chung được liên kết theo phạm vi phụ trách, không phải khai báo toàn bộ mã đó mới do một người viết ngày 11/11.
