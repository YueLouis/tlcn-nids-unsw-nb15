# Hoàng Văn Vương Thu — mô hình bất thường, metric và phân tích lỗi

**Bộ hiện hành — 15/11/2026:** [mở phần Hoàng Văn Vương Thu](BAN_GIAO_BAO_VE_20261115.md), [hồ sơ ATTQ NIDS](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so) và [bộ báo cáo đợt 4/tổng trên main](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/main/docs/releases/final_handoff_20261114). Nội dung bên dưới giữ các mốc lịch sử trước bản 14/11. Chỉ mục mới không thay xác nhận tự đọc, sửa hoặc đóng góp của thành viên.

Nhánh `vuongthu` lưu phần phụ trách của Hoàng Văn Vương Thu, tài khoản `hoangvvthu`. Báo cáo tổng hợp nằm trên [main](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/main).

[Mở phần chuyên môn, bảng số và mã liên quan](docs/group_delivery_20261110/VuongThu/README.md) · [Phạm vi qua các đợt](docs/group_delivery_20261110/VuongThu/QUA_TRINH_CAC_DOT.md)

Hồ sơ ngày 11/11/2026 có phần giải thích, CSV/ảnh và ZIP giữ đường dẫn mã nguồn, kiểm thử, cấu hình và bằng chứng. Các tệp lịch sử được phân theo trách nhiệm để đối chiếu; không coi lần bổ sung này là commit đã có ở đợt 1 hoặc 2. Nội dung được chuẩn bị có công cụ hỗ trợ và tải theo ủy quyền; việc đọc, sửa và nhận xét thực tế của thành viên được ghi riêng khi thực hiện.

| Đợt | Tình trạng |
|---|---|
| 1 | Báo cáo tổng hợp đã gửi 14/09, giữ lịch sử gốc |
| 2 | Báo cáo tổng hợp đã gửi 17/10; phản hồi thầy 31/10 được đối chiếu trong báo cáo |
| 3 | Bổ sung hồ sơ chuyên môn ngày 11/11, giữ kết quả chốt 30/10 |
| 4 và tổng | Hoàn chỉnh nội dung ngày 14/11; email chưa gửi |

Phạm vi đề tài là so sánh RF/XGB/IF/AE trên UNSW-NB15, gồm CS và LOACO, năm seed, ngưỡng Normal validation 1%/5%. Raw, prediction và model nặng giữ trên [Drive dùng chung](https://drive.google.com/drive/folders/13KGqMT4NUr8JfvTpF0IEKfUDT0Dlvq5S). Bộ mã đầy đủ, hướng dẫn chạy và báo cáo hiện hành mở từ main.
