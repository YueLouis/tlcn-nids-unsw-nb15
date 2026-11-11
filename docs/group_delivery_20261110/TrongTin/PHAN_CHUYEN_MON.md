# Protocol, tái lập và demo

## Thực nghiệm chung

Ma trận gồm CS và ba LOACO LR/LD/LE, bốn mô hình RF/XGB/IF/AE, năm seed 42/52/62/72/82: tổng 80 lượt chạy. Mỗi lượt có `run.json`, `metrics.csv`, `predictions.csv`, `model_bundle.joblib`. Kết quả gốc và ngưỡng được giữ nguyên; bản cập nhật hồ sơ không phải lượt huấn luyện mới.

Pipeline bỏ lớp held-out trước chia vùng phát triển, fit preprocessing trong đúng vùng huấn luyện rồi chọn threshold trên Normal validation. Test chỉ được đưa qua các thành phần đã fit. Score chung được quy ước càng cao càng nghiêng về Attack. RF/XGB dùng dữ liệu có nhãn được phép; IF/AE fit Normal.

## Ví dụ hai ngưỡng

CS-RF-S42, ID 1 là Normal, score 0,7057412707296608. Target 5% có threshold 0,5572816867482743 nên dự đoán Attack (FP). Target 1% có threshold 0,8053672551154485 nên dự đoán Normal (TN). Mô hình và score không đổi; quyết định đổi do ngưỡng. Dữ liệu nguồn nằm trong ZIP ở `dot_03/VI_DU_HAI_NGUONG.csv`.

## Kiểm tra và khả năng tái lập

Ngày 11/11/2026 kiểm 46 unit test và validator 80 tổ hợp; 174 dòng bảng báo cáo đối chiếu khớp nguồn. Test AE có ConvergenceWarning trong dữ liệu tổng hợp; assertion đều đạt, không dùng kết quả đó để khẳng định AE hội tụ ở mọi bài toán. PDF có 62 trang, 200 liên kết nội bộ và 56 bookmark đã kiểm đích đến. Đây là kiểm kỹ thuật; không thay lượt đọc hoặc nghiệm thu của thành viên.

ZIP kèm toàn bộ `src/`, `tests/`, cấu hình và requirements để tránh mất phụ thuộc khi tách mã. Các raw CSV, prediction và bundle nặng nhận từ Drive dùng chung, kiểm hash theo manifest trước khi chạy. Lệnh PowerShell từ thư mục giải nén:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -q
python scripts/validate_protocol.py
python scripts/demo_server.py
```

Demo hiện có đọc CSV đúng schema và suy luận từ 16 bundle seed42 ở hai target. Nó có thể trả Normal/Attack, score, threshold và so sánh bốn model. Replay dùng mẫu từ official test là phần minh họa kết quả đã biết, không phải một dataset mới hoặc hệ thống tự học. Giao diện trình bày sáng đang được hoàn thiện riêng; chưa coi bản đề xuất giao diện là demo suy luận hoàn chỉnh.

## Phần cần phát triển tiếp

Hoàn thiện bản đợt 4/tổng, giao diện thuyết trình nối đúng inference, kịch bản hỏi đáp và đánh giá ưu/nhược. Nếu bổ sung dữ liệu tự thu thập, phải ghi nguồn, cách trích đủ đặc trưng tương thích và giới hạn so sánh; không tạo 42 số ngẫu nhiên rồi gọi là traffic thật.
