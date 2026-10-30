# Việc của Vương Thu — kết quả và lỗi

**Cách làm mới 25/10:** đã có [bộ báo cáo và ảnh hướng dẫn](../../../../02_Bao_cao/BO_HO_SO_NHOM_20261025/MO_DAU.html). Thu đọc Chương 6–7 và bốn ví dụ lỗi Chương 8 của báo cáo tổng; tự đối chiếu một bảng, một FP/FN rồi ghi điều hiểu và chỗ muốn sửa. Chưa cần viết lại từ đầu. Các yêu cầu tự viết/hạn bên dưới là phương án lịch sử 22/10, không áp làm hạn chậm nộp.

## Phương án ban đầu 22/10 (lịch sử)

Bạn chịu trách nhiệm phần “mô hình phát hiện được gì, báo nhầm/bỏ sót gì, đánh đổi ra sao”. Hạn ví dụ đầu **25/10**, bản chính **02/11**, sửa sau review **05/11**; đây là hạn nội bộ đề xuất.

## Bắt đầu từ đây

Tính từ gốc repo:

1. `results/runs/CS-IF-S42/` và `results/runs/CS-RF-S42/`: `run.json`, `metrics.csv`, `predictions.csv`; file lớn lấy từ Tín/Drive khi clone chưa có.
2. `docs/evidence/dot_02/category_errors_20261014/PHAN_TICH_LOI_BAN_DAU.md` và CSV cùng thư mục.
3. `docs/reports/DOT_02_TWO_TARGETS.csv` và `docs/protocol/RQ_TO_EVIDENCE.md`.
4. Bộ nền mới `docs/evidence/dot_03/pr_scores_20261022/`: bảng AP/điểm vận hành, hình PR và score. Đây là sản phẩm hỗ trợ chuẩn bị sẵn; phần của bạn là tự kiểm và viết nhận xét có căn cứ.

## Sản phẩm bạn tự tạo

**`THU_PHAN_TICH_KET_QUA.md`**: đối chiếu 4 model trong closed-set và ba LOACO ở target 1%/5%. Mỗi nhận xét phải chỉ scenario, target, metric và bảng/hình nguồn. Đọc mean/std qua năm seed; không dùng riêng seed42 để kết luận model nào ổn định. Tách AP toàn test khỏi AP chỉ Normal + held-out; hai scope khác prevalence, không xếp hạng chéo trực tiếp. FPR target trên validation không bảo đảm FPR test cùng mức.

**`THU_TRUY_VET_4_LOI.csv`**: một FP và một FN của mỗi model IF/RF trong CS seed42 target5%. Có thể dùng ví dụ gợi ý đợt 2 để bắt đầu nhưng phải tự mở prediction. Ghi `run_id`, `record_id`, `attack_cat`, `y_true`, `score`, `threshold`, `y_pred`, loại lỗi, quy tắc chọn và lời giải thích. Quy tắc Attack là score >= threshold; không suy đoán feature gây lỗi từ category/score.

**`THU_NOI_DUNG_BAO_CAO.md`**: khoảng 2–3 trang bàn luận từ PR, ECDF score và bảng lỗi. Trả lời: RF/XGB được gì và đổi bằng FPR bao nhiêu? IF/AE bỏ sót nhóm nào? Tại sao AP cao chưa đủ kết luận phát hiện held-out tốt? Một giả thuyết cần kiểm tiếp là gì? Chỉ kết luận trong phạm vi dữ liệu/cấu hình hiện có.

Lượt đầu 25/10 chỉ cần tự kiểm 4 ví dụ và một phép tính FPR/Recall của từng model. Bản chính mở rộng toàn ma trận, không yêu cầu bạn train lại 80 run hoặc tự viết toàn bộ công cụ.

## Đạt khi nào

- Tín kiểm được phép tính và số nguồn; mọi tỷ lệ có mẫu số/support đúng.
- Bạn giải thích được một PR curve và ngưỡng của một run; biết seed42 chỉ là ví dụ định trước.
- Anh đọc được phần viết và kiểm tính rõ ràng; bạn tự sửa sau nhận xét.
- Không đồng nhất LOACO với mọi zero-day hoặc nói model tốt nhất tuyệt đối.

**Chưa có sản phẩm do bạn bàn giao trong hồ sơ mới.** Không điền hoàn thành hoặc đóng góp thay bạn; ghi phần được hỗ trợ khi bàn giao.
