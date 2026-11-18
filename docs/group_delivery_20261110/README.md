# Hồ sơ tổng hợp và ba phần phụ trách

**Bộ hiện hành:** [bàn giao hoàn chỉnh ngày 14/11](../releases/final_handoff_20261114/README.md), [ATTQ NIDS](https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so). Nội dung đã đóng bộ cho nhóm mở dùng và xem lại; email chưa gửi. Các đoạn 10–13/11 bên dưới giữ để truy vết.

`main` là phần tổng của nhóm. Ba nhánh còn lại lưu hồ sơ theo phân công; mỗi nhánh có trang mở đầu riêng, phần chuyên môn, bảng/ảnh và gói mã kèm nguồn truy vết.

## Luồng nhánh và tích hợp

Mỗi thành viên thực hiện phần được giao trên nhánh của mình (`tramanh`, `vuongthu`, `trongtin`), commit bằng tài khoản của người thực hiện, rồi mở pull request vào `main`. Nhóm xem phần thay đổi và kiểm tra tự động trên pull request; sau khi xử lý góp ý thì mới merge. `main` là bản tổng đã tích hợp, còn nhánh thành viên giữ lịch sử phần việc riêng. [PR #1](https://github.com/YueLouis/tlcn-nids-unsw-nb15/pull/1) đã đưa ba nhánh vào `main`; [biên bản tích hợp](../evidence/dot_03/clarifications_20261115/INTEGRATION_CHECK_20261115.json) ghi các đầu nhánh và commit merge trung gian. Kiểm lại remote ngày 19/11 xác nhận cả ba đầu nhánh vẫn thuộc lịch sử `main`.

Lịch sử nhánh và người ghi trong commit cho biết thay đổi được lưu ở đâu và dưới danh tính Git nào; tự nó không chứng minh ai trực tiếp làm, đã đọc hay hiểu nội dung. Phần tự kiểm, giải thích và góp ý của từng thành viên phải được chính người đó thực hiện và ghi nhận riêng.

| Phần | Tài khoản nộp | Nội dung | Drive |
|---|---|---|---|
| [Tổng nhóm](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/main) | YueLouis, đại diện nhóm | Báo cáo tích lũy, protocol, mã tích hợp và bộ phát hành | [main](https://drive.google.com/drive/folders/1Qwx3tQCd5kPXtYwP_0sc2_hluz6Erj2R) |
| [Trâm Anh](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/tramanh) | tta2405 | Dữ liệu, nguồn học thuật, chia tập và giới hạn benchmark | [TramAnh](https://drive.google.com/drive/folders/1irSmdeRNb9CpduOqoDrgvhfj87vkgQQ_) |
| [Vương Thu](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/vuongthu) | hoangvvthu | IF/AE, metric, ngưỡng, kết quả và phân tích lỗi | [VuongThu](https://drive.google.com/drive/folders/1P7w0gHoP2ONR5SiHyxDc5lCzthSVadTV) |
| [Trọng Tín](https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/trongtin) | YueLouis | Pipeline, RF/XGB, tái lập, demo và tích hợp | [TrongTin](https://drive.google.com/drive/folders/1DjfTb9KOFXn4lqTEsGIJkMF9adWMGoLL) |

[Báo cáo tiến độ đợt 3 ngày 11/11/2026](../releases/submission_dot3_20261111/README.md) giữ kết quả chốt 30/10. Các bản đọc trước và hồ sơ đã gửi đợt 1–2 được giữ nguyên để đối chiếu.

Trong từng phần, `QUA_TRINH_CAC_DOT.md` nối phân công với tài liệu đợt 1, 2, 3 và phần tiếp nối. `CHI_MUC_NGUON.csv` ghi đường dẫn gốc và SHA-256. ZIP có mã, kiểm thử và cấu hình theo đường dẫn gốc, không tách một tệp Python khỏi phụ thuộc. Raw, model và prediction nặng lưu ở Drive dùng chung.

Hồ sơ cá nhân bổ sung ngày 11/11 không chứng minh đã có commit cá nhân ở đợt 1–2. Phản hồi của thầy ngày 31/10 và lịch sử tác giả được giữ nguyên. Phân công là phạm vi chịu trách nhiệm; tài liệu/mã dùng chung có công cụ hỗ trợ không tự thành sản phẩm độc lập do một thành viên viết. Thao tác tải theo ủy quyền và việc thành viên tự đọc, sửa, nhận xét được phân biệt rõ.

Đợt 4, báo cáo tổng và bộ bảo vệ đã hoàn chỉnh nội dung ngày 14/11; mở các PDF và nguồn hiện hành trong [bộ bàn giao](../releases/final_handoff_20261114/README.md). Hồ sơ kiểm ngày 14/11 ghi rõ chưa có xác nhận nhóm duyệt và chưa gửi giảng viên; việc đọc, tự kiểm và góp ý thực tế của thành viên vẫn cần từng bạn tự làm, không được suy ra từ bản báo cáo hay CI. Trạng thái thư đợt 3 được lưu riêng theo biên nhận thực tế.
