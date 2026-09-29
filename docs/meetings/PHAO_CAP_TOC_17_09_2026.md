# PHAO CẤP TỐC GẶP THẦY - 17/09/2026

## Câu mở đầu

> Dạ nhóm em cảm ơn Thầy đã dành thời gian. Báo cáo vừa rồi của nhóm em trình bày chưa đúng cách để Thầy theo dõi, nên hôm nay nhóm em xin nghe Thầy hướng dẫn lại. Nhóm em sẽ ghi rõ cách báo cáo, sản phẩm cần có và mốc thời gian để sửa đúng theo yêu cầu của Thầy ạ.

## Đề tài trong một câu

> Nhóm em dùng UNSW-NB15 để so sánh Random Forest, XGBoost, Isolation Forest và Autoencoder trong phát hiện xâm nhập, gồm closed-set và LOACO - tức là giữ lại một loại tấn công khỏi giai đoạn phát triển rồi mới đưa vào kiểm tra.

## Hiện tại đã làm thật được gì?

- Đề cương, phân công và Gantt theo ngày.
- GitHub private và cấu trúc repository.
- Cấu hình 4 kịch bản, 4 mô hình và 5 seed.
- `RUN_MATRIX.csv` có 80 **cấu hình dự kiến**, không phải 80 kết quả.
- Result schema, checklist Gate 1, RQ-to-evidence.
- Code contract chống dùng cột đáp án và chống để held-out class lọt vào development.
- Anh vừa kiểm tra trên máy: **6/6 unit test PASS** và protocol validator PASS.

## Chưa có - phải nói đúng

- Chưa audit đầy đủ dữ liệu chính thức.
- Chưa có preprocessing chạy trên dữ liệu thật.
- Chưa train 4 mô hình.
- Chưa có metric, bảng, biểu đồ hoặc kết luận mô hình nào tốt hơn.
- Chưa có prototype hoàn chỉnh.
- Gate 1 vẫn `NOT REVIEWED`, chưa được cả ba thành viên ký PASS.

## Mỗi người phụ trách gì?

**Nguyễn Trọng Tín:** nhóm trưởng, repository, protocol, preprocessing, Random Forest, XGBoost, quản lý các lần chạy và tích hợp.

**Trịnh Trâm Anh:** UNSW-NB15, nguồn dữ liệu, checksum, schema, data quality, related work và biên tập.

**Hoàng Văn Vương Thu:** Isolation Forest, Autoencoder, score, threshold, metric và phân tích FP/FN.

## Thầy hỏi - đáp ngay

**“Sản phẩm cuối là gì?”**

> Dạ là bộ benchmark có thể chạy lại để so sánh bốn mô hình, kết quả closed-set và LOACO, bảng biểu, phân tích lỗi, báo cáo, slide và prototype local. Nhóm em chưa xác định phải làm web hay VMware, nên hôm nay muốn xin Thầy chốt yêu cầu sản phẩm cuối.

**“LOACO là gì?”**

> Dạ nhóm loại hoàn toàn một attack class khỏi vùng phát triển trước khi split, fit preprocessing, train và tuning; sau đó mới đánh giá class đó trên test.

**“Có phải phát hiện zero-day không?”**

> Dạ không. LOACO chỉ mô phỏng một loại tấn công chưa thấy trong benchmark, không chứng minh phát hiện mọi zero-day ngoài thực tế.

**“Tại sao có 80 run?”**

> Dạ 4 kịch bản nhân 4 mô hình nhân 5 seed bằng 80 cấu hình dự kiến. Nhóm em chưa chạy 80 cấu hình này.

**“Tại sao dùng 5 seed?”**

> Dạ để đánh giá độ ổn định và báo cáo mean/std, tránh chọn một lần chạy đẹp.

**“Code tới đâu?”**

> Dạ mới có scaffold và contract kiểm tra protocol: loại cột cấm, chuẩn hóa nhãn, phân vai Normal/known/held-out, loại held-out khỏi development và kiểm tra run matrix. Sáu unit test đang PASS; chưa có training pipeline và kết quả model.

**“Validator PASS nghĩa là đề tài chạy xong chưa?”**

> Dạ chưa. Validator chỉ chứng minh cấu hình đủ và không trùng. Gate 1 vẫn phải được nhóm review, còn mô hình chưa train.

**“Tại sao không dùng Accuracy?”**

> Dạ dữ liệu mất cân bằng nên Accuracy có thể cao dù bỏ sót attack. Nhóm ưu tiên recall của held-out attack, recall của known attack và FPR trên Normal, rồi bổ sung Precision, F1 và PR-AUC.

**“Có dùng AI không?”**

> Dạ nhóm có dùng AI để hỗ trợ tạo khung, giải thích và kiểm tra logic. Nhưng từng thành viên phải đọc, review, chạy kiểm tra, hiểu và chịu trách nhiệm phần được giao. Phần nào chưa review thì nhóm em sẽ nói là chưa hoàn thành.

**“Tại sao báo cáo thầy không theo dõi được?”**

> Dạ nhóm em nhận thiếu sót vì đưa nhiều thuật ngữ nhưng chưa trình bày theo đúng luồng Thầy cần. Nhóm xin Thầy chỉ rõ mẫu và thứ tự; nhóm sẽ sửa thành công việc - người phụ trách - bằng chứng - trạng thái - việc tiếp theo.

**“Nhóm trễ gì?”**

> Dạ nhóm gửi báo cáo tổng hợp bốn tuần đầu chậm và phần thực nghiệm chưa bắt đầu. Nhóm xin nhận thiếu sót, nghe Thầy chốt lại cách báo cáo và lịch thực hiện.

## Nhất định phải hỏi thầy

1. Một lần báo cáo cần đúng những mục nào và theo thứ tự nào?
2. Báo cáo chính 4 tuần/lần; giữa các đợt có cần cập nhật hàng tuần không?
3. Thầy cần PDF, Word, link Drive hay link GitHub? Quy tắc đặt tên file?
4. Hạn báo cáo tiếp theo tính từ ngày nào và ngày cụ thể là ngày nào?
5. Phạm vi 4 model và 3 lớp LOACO có phù hợp không?
6. Sản phẩm cuối cần benchmark + prototype local, hay cần web/VMware/demo traffic sống?
7. Thầy có mẫu báo cáo hoặc báo cáo cũ để nhóm tham khảo không?

## File mở sẵn nếu thầy hỏi

1. `docs/reports/BAO_CAO_TIEN_DO_4_TUAN_LAN_01.pdf`
2. `docs/management/GANTT_CHART.md`
3. `docs/management/PHAN_CONG_NHOM.md`
4. `configs/experiment_matrix.yaml`
5. `docs/protocol/RUN_MATRIX.csv`
6. `docs/protocol/GATE_1_CHECKLIST.md`
7. `src/nids_benchmark/contracts.py`
8. `tests/test_contracts.py`

## Câu cứu nguy

> Dạ phần này hiện nhóm em chưa có đủ bằng chứng để kết luận. Em xin ghi lại đúng câu hỏi của Thầy, sau buổi gặp nhóm em sẽ kiểm tra và phản hồi trong cùng chuỗi mail ạ.

## Cuối buổi phải đọc lại cho thầy xác nhận

> Dạ để nhóm em xác nhận lại: nhóm cần làm ..., báo cáo theo ..., sản phẩm gồm ..., và hạn tiếp theo là ... Đúng như vậy không ạ?

## Không được nói nhầm

- Không nói “đã có 80 kết quả”; chỉ có 80 cấu hình dự kiến.
- Không nói “Gate 1 đã PASS”; hiện vẫn `NOT REVIEWED`.
- Không nói “đã có IDS/prototype/model”; chưa train dữ liệu thật.
- Tín không trả lời thay hết cho hai bạn. Thầy hỏi ai thì người đó trả lời trước, Tín chỉ bổ sung khi cần.
