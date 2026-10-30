# Bộ chung để nhóm đọc và sửa — 25/10/2026

**Cập nhật 30/10:** [Bản đợt 3 hiện hành](../releases/dot_03/README.md) đã chốt kỹ thuật; bản 59 trang trong bộ 25/10 bên dưới là nháp lịch sử. Phần ghi chưa đồng bộ bên dưới thuộc mốc 25–27/10. Tự đọc/duyệt và gửi email vẫn chưa xác nhận.

Theo yêu cầu trực tiếp mới của nhóm trưởng, chuẩn bị nội dung bốn đợt và báo cáo tổng trước để cả ba cùng đọc/sửa; không tiếp tục đợi bài viết độc lập rồi mới ghép. Hai bản đợt 1–2 giữ nguyên. Đợt 3 (59 trang), đợt 4 (63 trang) và tổng (57 trang) là nháp đã có nội dung, chưa duyệt nộp.

Mở từ workspace: `02_Bao_cao/BO_HO_SO_NHOM_20261025/MO_DAU.html`. ZIP gửi nhóm: `02_Bao_cao/BO_BAO_CAO_VA_HUONG_DAN_GUI_NHOM_20261025.zip`, khoảng 22 MB; có PDF, năm ảnh hướng dẫn, nguồn chỉnh sửa, bảng số liệu, 20 slide, tài liệu tập nói 9 trang và code/config/test nhẹ. Gói demo riêng: `02_Bao_cao/DEMO_NIDS_NHOM_20261025.zip`, khoảng 199 MB; 16 bundle seed42, mã, dữ liệu mẫu và hướng dẫn môi trường.

## Đã thực hiện

- PR/score đủ 80 run; phân tích overlap mới đối chiếu 1.040 metric từ 13.173.120 dòng prediction, match 42 feature với đúng tập fit được tái dựng và kiểm scaler/ID. 480 dòng cohort/target/run, 96 nhóm mean/std; chỉ mô tả hậu nghiệm, không retrain/tune ngưỡng.
- Importance RF/XGB của 40 run, 42 feature raw: RF impurity/XGB gain, gom one-hot; không diễn giải nhân quả hay thay permutation importance.
- Demo CSV chạy model thật: 16 bundle seed42, hai target; 3.200 nhãn dự đoán và threshold khớp baseline, score lệch tối đa 2,20e-7 dưới dung sai 1e-6. Từ chối bốn kiểu input sai. Giao diện thử RF/CS/5%, IF/LR/1%, so sánh cả bốn model trên cùng CSV, giải thích score/feature, CSV không nhãn, tải CSV và năm độ rộng màn hình.
- Chẩn đoán cuối đủ 80 run và 1.040 metric; 43.840 dòng nhóm lỗi proto/service/state, 8.768 nhóm tổng hợp, 264 ví dụ sát ngưỡng và 48 cặp so sánh model/target/scenario. Bổ sung 8 hình, phân bố lỗi 0–5 seed và phép đo suy luận hiện tại cho 80 bundle, 8.000 score đối chiếu khớp trong dung sai 1e-6. T2/T9 còn thiếu phần cứng/thời gian train riêng của run lịch sử; ghi rõ, không dùng tổng duration làm train time.
- 42 test đạt. Ba PDF được biên dịch nhiều lượt, không còn tham chiếu thiếu hoặc overfull box; render đủ 179 trang ba bản (59/63/57). Kiểm bảng overlap đủ 32 dòng trong mỗi PDF/source, đối chiếu các giá trị in. Các trang phân tích và demo mới đã được xem qua bản render. Năm ảnh hướng dẫn đã render/kiểm chữ và bố cục. Hai PDF/nguồn đợt 1–2 giữ hash gốc.
- Trang mở đầu bổ sung link slide/PDF tập nói/code: 19 link được thử HTTP 200. Hai ZIP kiểm CRC; manifest hash file đã đối chiếu. Hai ZIP còn được giải nén vào thư mục mới và kiểm bằng một venv vừa cài từ requirements, tắt user-site: code đạt 42 test/validator; demo đủ 16 bundle, 32 case, 3.200 dự đoán từng dòng khớp và API so sánh bốn model chạy được. Đây là môi trường mới trên cùng máy Windows, chưa phải máy vật lý khác.
- Bổ sung theo kế hoạch đầu ra cuối: slide HTML/PDF 20 trang và tài liệu tập nói/câu hỏi phản biện 9 trang. Giá trị bảng trên slide lấy từ CSV; có nguồn, scenario, target, seed và support. Kiểm năm viewport, bàn phím, PDF và bố cục; không ghi nhận ai đã trình bày/review.
- Snapshot `07_Ma_nguon` gồm src/scripts/tests/configs, protocol, bảng/audit nhẹ và metadata/metric 80 run; 42 test và validator đạt khi chạy từ chính snapshot bằng môi trường hiện có. Không gồm raw/model/prediction nặng; hướng dẫn ghi rõ đầu vào cần nhận thêm. Kiểm lại 333 hash từ audit overlap, gồm đủ 320 artifact và hai raw CSV: khớp. Hai PDF/nguồn đợt 1–2 giữ nguyên.

Nguồn bằng chứng: `docs/evidence/dot_03/session_20261025/`, các thư mục PR/overlap/features/final_diagnostics của đợt 3 và `docs/evidence/dot_04/demo_20261025/`. Bảng đối chiếu toàn bộ 39 mục ở `DOI_CHIEU_YEU_CAU.json` và bản HTML cùng tên; phân biệt đủ hồ sơ kỹ thuật, khoảng trống lịch sử và việc người thật chưa thực hiện.

## Cả nhóm đọc tiếp

Bổ sung ứng dụng 26/10 theo góp ý của Tín: demo `/lab`, tám tình huống truy vết từ official test local, nguồn/mirror/hash, bản đồ hàm code, phát/tạm dừng, hàng cần xem lại, ghi chú và xuất JSON/CSV. Báo cáo bổ sung năm trang tại `09_Demo_ung_dung/report.pdf`. Có 46 test, 56 trường hợp suy luận / 1.600 dự đoán khớp nhãn baseline; kiểm số có cả atol/rtol cho AE float32. Chi tiết audit tại `docs/evidence/dot_04/application_20261026/`. Đây là demo phát lại và khả năng ứng dụng bổ sung, không phải cải tiến thuật toán đã chứng minh, cảm biến/IPS hay tự học. Chưa bảo đảm điểm bonus hoặc chuẩn 5 tín chỉ khi chưa có rubric. Các trang nhận xét cá nhân tiếp tục để trống để nhóm tự thực hiện.

Bổ sung 26/10: mở `08_Tu_doc_va_gop_y/BAT_DAU.html` từ bộ chung hoặc chọn “CHỌN TÊN MÌNH VÀ BẮT ĐẦU” ở trang mở đầu. Có từng lượt đọc/thử cho ba bạn và ô ghi chú riêng, lưu trên trình duyệt hoặc tải TXT để tự gửi. Tín bắt đầu bằng ID 1, CS/RF, hai target; đọc Chương 4–5 và 8 ở lượt sau. Hướng dẫn được chuẩn bị sẵn không phải bằng chứng thành viên đã đọc hay góp ý. Ngày tạo bộ chung vẫn là 25/10; đây là phần hướng dẫn bổ sung ngày 26/10.

Anh: dữ liệu, nguồn và giới hạn. Thu: kết quả, FP/FN và trade-off. Tín: protocol, tái lập, demo và gom sửa. Mỗi lần đọc một đoạn/bảng, ghi trang đã xem, cách hiểu và chỗ cần sửa. Dùng năm ảnh mới trong bộ chung thay ảnh phân việc 22/10. Online trước, buổi ra quán hẹn khi cả ba rảnh; chưa có ngày cụ thể.

Chưa gửi tự động qua Zalo/Drive/GitHub/email, chưa nộp báo cáo mới. Chưa xác nhận thay bài tự đọc, mức hiểu, góp ý hoặc đóng góp của thành viên; Gate nội dung còn chờ bằng chứng thật. Mốc đợt 3 là 09/11 theo nhóm trưởng xác nhận, không tự chốt ngày nộp đợt 4/bản cuối. S07 vẫn chỉ dùng abstract; chưa có thí nghiệm dataset ngoài, retrain loại overlap hoặc bắt gói mạng trực tiếp.

Góp ý giao diện 26/10: `/lab` chia sáu mục trong cùng tab, thiết lập hai bước, bảng kết quả và tài liệu phân trang. Đã kiểm 140 lượt bố cục trên năm cỡ màn hình và luồng xem chi tiết/đánh dấu/giữ ghi chú/xuất phiên. Đây là kiểm giao diện sau lần kiểm môi trường sạch, không ghi thành chạy lại toàn bộ thực nghiệm.
