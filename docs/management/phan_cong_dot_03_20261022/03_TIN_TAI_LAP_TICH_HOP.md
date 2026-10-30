# Việc của Tín — tái lập và tích hợp

**Bắt đầu 26/10:** mở hướng dẫn [từng lượt của ba bạn](../../../../02_Bao_cao/BO_HO_SO_NHOM_20261025/08_Tu_doc_va_gop_y/BAT_DAU.html), chọn Tín. Lượt đầu chỉ thử ID 1 trong demo CS/RF, so target 5% và 1%, rồi ghi cách hiểu bằng lời mình. Các bước tự chạy test/phân tích bên dưới dành cho lượt sau khi đã hiểu demo; không phải việc phải làm hết ngay.

**Cách làm mới 25/10:** đã có [bộ báo cáo, demo và ảnh hướng dẫn](../../../../02_Bao_cao/BO_HO_SO_NHOM_20261025/MO_DAU.html). Tín đọc Chương 4–5 và 8 của báo cáo tổng, tự chạy thử demo, ghi điều đã kiểm và gom góp ý của Anh/Thu để sửa một bản chung. Các hạn bên dưới là phương án lịch sử 22/10, không áp làm hạn chậm nộp. Log do công cụ chuẩn bị chưa phải nhật ký tự làm của Tín.

## Phương án ban đầu 22/10 (lịch sử)

Em chịu trách nhiệm để kết quả kiểm lại được và ba phần ghép thành báo cáo đúng bằng chứng. Hạn log đầu **25/10**, kỹ thuật **02/11**, nháp ghép **06/11**, kiểm nhóm **08/11**; đây là hạn nội bộ đề xuất.

## Lượt đầu em tự làm

Từ gốc repo, chạy test và tái tạo PR/score vào thư mục riêng. Môi trường cần thư viện trong `requirements-analysis.txt`.

```powershell
$env:PYTHONPATH='src'
$env:PYTHONUTF8='1'
python -m unittest discover -s tests -q
python scripts/analyze_pr_scores.py --output results/member_checks/tin/pr_scores_lan_01
```

Script phân tích đủ 80 run nhưng chỉ đọc predictions/metric, không huấn luyện lại; dự kiến vài phút tùy máy. Nếu thư mục đích đã có, dùng hậu tố lần tiếp theo. Đầu vào lớn nhận đúng bản từ local/Drive; đừng thay output thành `results/runs/`.

Tự mở `PR_SCORE_AUDIT.json`, một hình PR và một hình ECDF. Giải thích được tại sao có 13.173.120 dòng prediction nhưng chỉ 6.586.560 cặp record/run, vì mỗi record có hai target; AP chỉ tính một lần/record/run.

## Sản phẩm em tự tạo

**`TIN_NHAT_KY_TAI_LAP.md`**: ngày thực hiện, môi trường, lệnh đã chạy, log gốc, kết quả và lỗi gặp/cách xử lý; phân biệt kết quả công cụ chuẩn bị sẵn với phần em thực sự kiểm. Chỉ ghi số test/pass đúng lần em chạy; không lấy log người khác làm log của mình.

**`TIN_KIEM_TRA_KY_THUAT.md`**: tự kiểm score/ngưỡng/prediction/metric một run; ghi đề xuất feature importance RF/XGB và cách kiểm độ nhạy overlap. Chốt trước input, 42 feature matching, tập fit thực tế theo seed/model, support và metric. IF/AE fit Normal-only phải phân biệt với fit RF/XGB. Nếu phân tích subset trên test sẵn có, gọi đúng là hậu nghiệm; nếu retrain thì tạo run mới riêng. Không xóa overlap hoặc điều chỉnh threshold trong 80 run gốc.

Khi triển khai bước khó, có thể nhờ công cụ hỗ trợ rồi tự chạy/kiểm/giải thích, ghi rõ phần hỗ trợ. Không cần tự viết tất cả từ đầu để có đóng góp thật.

**Bản nháp tích lũy đợt 3**: nhận file Anh và Thu, ghép nội dung có nguồn, lập bảng claim → bằng chứng, kiểm số liệu và render PDF. Giữ PDF đợt 1–2. Chưa có đầu ra nào thì giữ “đang làm/chưa có”, không viết như kết quả đã hoàn tất.

## Review chéo và ranh giới

- Thu kiểm threshold/metric và cách đọc biểu đồ em tạo.
- Anh kiểm thuật ngữ, citation và giới hạn dữ liệu.
- Em nhận xét cụ thể phần của mỗi bạn rồi trả lại để bạn tự sửa; không tự viết hết và chỉ ghi tên bạn.
- Trước 08/11, cả ba tự nói được phần mình và ghi đóng góp thực tế; em tổng hợp phần được hỗ trợ trung thực.

Prototype hoàn chỉnh và bộ bảo vệ cuối vẫn theo kế hoạch toàn đề tài. Đợt 3 ưu tiên phân tích và báo cáo đúng những gì đã hoàn thành.

**Chưa có nhật ký tự làm đợt 3 của em trong hồ sơ mới.** Các script/test/hình do công cụ hỗ trợ tạo trong buổi khởi động là tài liệu dùng chung; tự chạy và giải thích là bước riêng của em.
