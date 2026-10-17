# Kiểm tra trước khi gửi đợt 2 - cập nhật 17/10/2026

**Hiện tại: đã kiểm kỹ thuật; nhóm chưa hoàn tất tự rà soát/giải thích; email chưa gửi.** Nhóm trưởng cho biết chưa chắc mức hiểu từng người và dự kiến cả nhóm đọc lại hai đợt ngày 18/10 sau khi nghỉ ngơi. Lời báo đồng ý trước đó được giữ làm lịch sử, không dùng làm bằng chứng đã nghiệm thu nội dung.

## Kết quả kiểm kỹ thuật ngày 17/10

- PDF đợt 2: 32 trang, 385.265 byte, SHA-256 `22b68ec396c88845879d8e33f7433a6ea047a5da5668d3a2462d7ad34c365d0c`. Bản root/repo và PDF tải từ Drive khớp. Giữ nguyên bản ngày 14/10 để nhóm kiểm lại.
- PDF đợt 1: bản lịch sử 20 trang; root/repo khớp. Không dùng đợt 1 làm bản nộp hiện tại.
- Đọc comment thật trong PDF gốc: tiến độ đã/chưa có; metric dạng long; schema; thế nào là PASS; scenario; số liệu cụ thể. Mục 3.1 đợt 2 đã có đối chiếu và các phần giải thích tương ứng. Điều này không phải kết luận giảng viên đã chấp thuận sửa đổi.
- Đã đọc lại phương pháp cùng mã data/preprocessing/runner/models/evaluation: loại metadata; held-out trước split; stratify=attack_cat; IF/AE và preprocessor fit Normal train; ngưỡng trên Normal validation. Giới hạn cross-split overlap vẫn giữ rõ.
- Chạy lại bộ kiểm tra cuối bằng môi trường có đủ thư viện: **17/17 test đạt**, protocol validator và kiểm đủ 80 run/320 artifact đạt. Lượt đầu dùng môi trường thiếu scikit-learn không chạy được test; đã đổi đúng môi trường trước khi kết luận.
- Tính lại trực tiếp 13.173.120 dòng prediction của 80 run: **1.040 dòng metric, 80 dòng tổng hợp, 16 nhóm mean/std khớp; không phát hiện sai lệch**. Hai CSV raw khớp manifest. Không huấn luyện lại hoặc sửa score.
- Xem bố cục toàn bộ 32 trang qua bản render; không thấy bảng bị cắt khỏi khổ trang. Đọc nội dung từ nguồn báo cáo; những trang bảng dày được giữ để nhóm kiểm nội dung từng dòng.
- Đối chiếu thêm 224 giá trị literal của bảng kết quả mean/std và lỗi category với CSV: khớp; 13 citation key đều có mục tham khảo, không có mục thiếu/không dùng; 17 tên test trong báo cáo khớp 17 test trong mã. Ba bảng category CSV tái tạo khớp bản lưu.
- Nguồn: 13 định danh trong ma trận; 12 có bằng chứng đoạn nguồn từ lần kiểm 14/10, S07 chỉ abstract. Kiểm lại 9 PDF nguồn đã lưu: hash khớp bằng chứng; đối chiếu các đoạn về NIDS, RF/XGB/IF, đánh giá và giới hạn NIDS. Đây không phải nghiệm thu toàn bài của thành viên.
- Local: đủ 80 tên run chuẩn/320 tệp; manifest bàn giao trước đó khớp. Không phát hiện tên thư mục hỗ trợ cá nhân/cache trong workspace. Audit chi tiết, bản render và file tạm giữ ngoài workspace.

## Đồng bộ và thư nháp

Drive đủ bộ 80 thư mục/320 artifact và toàn bộ hash được kiểm ngày 14/10. Lượt 17/10 kiểm lại PDF; không tải lại toàn bộ bộ run từ xa. GitHub local/remote khớp trước cập nhật ghi chú, mã thực nghiệm không đổi.

Gmail: gửi từ `23162102@student.hcmute.edu.vn` tới `quangnd@hcmute.edu.vn`, tiêu đề `[TLCN] Báo cáo tiến độ đợt 2 - Nhóm Nguyễn Trọng Tín`; có PDF đợt 2 hiển thị 377K. Đã bỏ câu cả ba thành viên đã rà soát và không thêm lời xác nhận hiểu bài. Thư giữ nháp, chưa bấm Gửi.

## Việc còn trước khi nộp

1. Nhóm tự đọc đợt 1, comment gốc và đợt 2; giải thích phần mình phụ trách theo `HUONG_DAN_RA_SOAT_HAI_DOT_20261018.md`.
2. Kiểm mô tả đóng góp/phân công và các câu xác nhận có đúng thực tế. Ghi nhận điểm chưa hiểu/chưa làm; không xác nhận thay nhau.
3. Khi có rà soát thực tế, xử lý đoạn kết luận PDF còn ghi trạng thái ngày 14/10 và cập nhật bản nộp nếu cần; kiểm lại các bản sao/tệp đính kèm nếu PDF đổi.
4. Giữ rõ S07 chưa toàn văn; phân tích chuyên sâu, độ nhạy overlap và demo chưa hoàn tất. Kiểm kỹ thuật không chứng minh mức hiểu hoặc khả năng được giảng viên chấp nhận.
