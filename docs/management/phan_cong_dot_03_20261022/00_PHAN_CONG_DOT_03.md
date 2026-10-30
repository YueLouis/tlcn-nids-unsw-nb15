# Chia việc đợt 3 cho Anh – Thu – Tín

**Phương án mới 25/10/2026:** nhóm trưởng yêu cầu chuẩn bị đầy đủ nội dung đợt 3–4 và báo cáo tổng trước, rồi cả ba đọc/kiểm/sửa dần. Bộ chung đã có tại [trang mở hồ sơ](../../../../02_Bao_cao/BO_HO_SO_NHOM_20261025/MO_DAU.html). Vai trò chuyển thành: Anh kiểm dữ liệu/nguồn/giới hạn; Thu kiểm kết quả/lỗi/cách diễn giải; Tín kiểm tái lập/demo và tích hợp sửa. Bảng hạn và yêu cầu tự viết ban đầu bên dưới lưu phương án 22/10, không áp làm hạn chậm bàn giao. Nội dung chuẩn bị không chứng minh nhận việc, mức hiểu, đóng góp hoặc review thực tế của người nào.

**Ngày lập: 22/10/2026. Mốc báo cáo: 09/11/2026**, nhóm trưởng xác nhận đã thống nhất với thầy. Hạn từng việc bên dưới là đề xuất nội bộ để nhóm triển khai, chưa có xác nhận nhận việc của từng bạn.

Mục tiêu đợt 3: từ kết quả 80 run đã có, cả ba tự kiểm, phân tích và viết được phần chuyên môn của mình. Đợt 1–2 giữ nguyên bản bàn giao; báo cáo mới vẫn tích lũy từ đầu đề tài. Bộ script/biểu đồ do công cụ hỗ trợ chuẩn bị là **tài liệu nền dùng chung**, không tự tính là đóng góp của Anh, Thu hoặc Tín.

## Làm online trước, hẹn ra quán khi cả ba rảnh

Theo trao đổi của nhóm qua Tín, bắt đầu bằng việc chia phần và làm online. Tín gửi đúng file/link đầu vào cho Anh và Thu; mỗi bạn gửi bản đang làm, điều đã làm và chỗ đang vướng vào nhóm Zalo. Chấp nhận Word, bảng tính hoặc ghi chú; Tín hỗ trợ đưa vào repo sau, không yêu cầu các bạn biết Git mới bắt đầu được.

Buổi ra quán sẽ hẹn khi cả ba rảnh, hiện chưa có ngày cụ thể. Trước buổi gặp, mỗi bạn đọc bản của nhau và ghi câu hỏi; lúc gặp ưu tiên giải thích số liệu, gỡ chỗ vướng, đọc chéo và ghép bài. Công việc vẫn tiến hành online nếu chưa sắp được buổi gặp; các hạn nhỏ bên dưới còn chờ nhóm thống nhất.

## Mỗi người sở hữu một phần rõ ràng

| Người | Phần chịu trách nhiệm | Đầu ra do bạn tự làm | Hạn bàn giao chính | Review |
|---|---|---|---|---|
| **Trịnh Trâm Anh** | Dữ liệu, nguồn học thuật và giới hạn benchmark | Bảng dữ liệu/support/overlap có nguồn; phiếu đọc ít nhất 3 nguồn liên quan; phần viết dữ liệu và giới hạn | 29/10; sửa sau review trước 05/11 | Thu kiểm mẫu số/ý nghĩa; Tín kiểm đường dẫn và số liệu |
| **Hoàng Văn Vương Thu** | Đánh giá mô hình và phân tích FP/FN | Bảng đối chiếu closed-set/3 LOACO ở cả hai target; 4 ví dụ lỗi tự truy vết; phần viết kết quả, trade-off và giới hạn | 02/11; sửa sau review trước 05/11 | Tín kiểm phép tính; Anh kiểm cách giải thích |
| **Nguyễn Trọng Tín** | Tái lập kỹ thuật, hỗ trợ phép tính và tích hợp | Log tự chạy; kiểm một run từ score đến metric; phân tích feature/overlap theo phương án đã ghi trước; bản nháp tích lũy và kiểm PDF | 02/11 cho kỹ thuật; 06/11 cho bản ghép | Thu kiểm score/ngưỡng/metric; Anh kiểm nội dung/nguồn |

Tín không nhận viết toàn bộ phần dữ liệu của Anh hay kết luận mô hình của Thu. Khi bạn nào chưa làm/không hiểu, ghi rõ mục đó và cùng xử lý; không đổi tên người trên nội dung công cụ đã sinh để coi là hoàn thành.

## Việc đầu tiên, làm ngay 22–25/10

| Người | Mở tài liệu gì | Việc tự làm trong lượt đầu | Nộp lại cái gì |
|---|---|---|---|
| Anh | Manifest; Chương dữ liệu PDF đợt 2; nguồn S03 và S13 | Đối chiếu số dòng/cột, 42 feature và support ba held-out; viết vì sao overlap là giới hạn | Bản đầu `ANH_DU_LIEU_VA_GIOI_HAN.md`, kèm đúng đường dẫn/trang đã đọc |
| Thu | `CS-IF-S42` và `CS-RF-S42`; bảng lỗi category đợt 2 | Tự truy vết một FP và một FN mỗi model; tính lại FPR/Recall; giải thích target validation khác test | Bản đầu `THU_PHAN_TICH_KET_QUA.md` với 4 record ID, phép tính và nhận xét riêng |
| Tín | README; test; script PR/score mới | Tự chạy test và một lệnh tái tạo vào output riêng; đọc audit; giải thích vì sao loại bản sao target khi tính AP | `TIN_NHAT_KY_TAI_LAP.md` kèm lệnh, log, lỗi gặp và cách xử lý |

Thẻ việc chi tiết: [Anh](01_ANH_DU_LIEU_NGUON.md), [Thu](02_THU_KET_QUA_LOI.md), [Tín](03_TIN_TAI_LAP_TICH_HOP.md). Các file đầu ra nêu trên **do người được giao tạo khi làm**, chưa tạo sẵn nội dung hoặc câu trả lời thay bạn.

Nơi bàn giao tính từ gốc repo: Anh đặt file trong `docs/evidence/dot_03/member_work/tram_anh/`, Thu trong `docs/evidence/dot_03/member_work/vuong_thu/`, Tín trong `docs/evidence/dot_03/member_work/trong_tin/`. Tạo thư mục khi bắt đầu làm; log/hình nặng để local/Drive và ghi link kèm checksum trong bài bàn giao.

## Mốc nhóm cùng kiểm

| Mốc nội bộ | Nhóm cần có |
|---|---|
| **25/10** | Cả ba bàn giao bản đầu của lượt việc trên; báo vướng cụ thể nếu chưa chạy/đọc được |
| **29/10** | Anh có bản dữ liệu/nguồn; Thu và Tín có nhận xét review, không chỉ nhắn “ổn” |
| **02/11** | Thu có phân tích hoàn chỉnh; Tín có bằng chứng kỹ thuật và kết quả bổ sung thực sự đã chạy |
| **05/11** | Mỗi bạn đã sửa phần của mình sau review và tự giải thích được các con số đang dùng |
| **06/11** | Tín ghép nháp; Anh biên tập nguồn/nội dung; Thu đối chiếu toàn bộ bảng kết quả |
| **08/11** | Cả ba đọc bản PDF cuối và đối chiếu đóng góp thực tế; mục còn thiếu phải ghi rõ |
| **09/11** | Nhóm trưởng nộp bản đã review theo mốc thống nhất |

## Nhận bàn giao thế nào

Mỗi lần bàn giao cần: file/link hoặc commit, điều đã tự làm, phần được hỗ trợ, lệnh/trang nguồn đã kiểm, kết luận bằng lời của mình và phần chưa rõ. Mỗi review cần: người review thật, ngày thật, nhận xét cụ thể và cách đã xử lý. Chấp nhận Markdown/Word/CSV hoặc ghi chú có cấu trúc; không bắt hai bạn phải viết code mới để có đóng góp chuyên môn.

Nếu dùng GitHub thì làm nhánh riêng và PR. Nếu chưa quen Git, gửi file vào thư mục đúng tên; Tín tích hợp và ghi đúng người tạo, không dùng commit của Tín làm bằng chứng Tín làm thay tất cả. Đây là hướng dẫn bàn giao; chưa gửi lời nhắn hay giao việc ra tài khoản của thành viên.

## Trạng thái ngày lập 22/10 (lịch sử)

| Người | Nhận việc | Sản phẩm do thành viên bàn giao | Review |
|---|---|---|---|
| Anh | Chờ nhóm trưởng trao đổi | Chưa có bằng chứng mới | Chưa thực hiện |
| Thu | Chờ nhóm trưởng trao đổi | Chưa có bằng chứng mới | Chưa thực hiện |
| Tín | Đã yêu cầu lập phân công; chưa xác nhận hoàn thành việc chuyên môn | Chưa có nhật ký tự làm đợt 3 | Chưa thực hiện |

Trạng thái này không thay phiếu tự rà soát đợt 1–2. Ghi nhận mức hiểu/đóng góp sau khi thực sự làm; không ký hộ hoặc tự chuyển Gate sang PASS.
