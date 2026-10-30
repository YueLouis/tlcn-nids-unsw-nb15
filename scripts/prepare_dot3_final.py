"""Prepare the separate 30 October release; preserve the earlier drafts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/report_dot3_20261025'
DEST = ROOT / 'docs/report_dot3_final_20261030'


def edit(name, replacements):
    text = (SOURCE / name).read_text(encoding='utf-8')
    for old, new in replacements:
        assert old in text, (name, old)
        text = text.replace(old, new)
    (DEST / name).write_text(text, encoding='utf-8')


def main():
    edit('main.tex', [
        ('Tích lũy đợt 3 - Bản nháp', 'Tích lũy đợt 3 - 30/10/2026'),
        ('Bản tích lũy đợt 3 - Nháp', 'Bản tích lũy đợt 3'),
        ('BẢN TÍCH LŨY - ĐỢT 3 (NHÁP)', 'BẢN TÍCH LŨY - ĐỢT 3'),
        ('17/08/2026 - 25/10/2026 (bản nháp)', '17/08/2026 - 30/10/2026'),
        ('Ngày cập nhật bản nháp:} & 25/10/2026', 'Ngày cập nhật:} & 30/10/2026'),
        ('Báo cáo tích lũy đợt 3 -- BẢN NHÁP; kế thừa nội dung đợt 1--2, bổ sung phân tích PR/score và feature overlap.', 'Báo cáo tích lũy đợt 3; chốt kỹ thuật ngày 30/10, chờ nhóm rà soát nội dung trước khi gửi.'),
        ('PR/score: audit ngày 22/10; overlap trên tập fit thực tế: 25/10; đều hậu nghiệm trên kết quả đã lưu.', 'PR/score, overlap theo tập fit, importance và chẩn đoán lỗi; phân tích hậu nghiệm từ kết quả đã lưu.'),
        ('42 test đạt ngày 25/10; CSV/audit dùng để đối chiếu; bản nháp còn chờ review nội dung.', '46 test đạt ngày 30/10; tính lại PR/overlap đủ 80 run, đối chiếu 1.040 metric; log và audit mới đi kèm.'),
        ('Nhóm thống nhất qua Tín ngày 25/10: chuẩn bị trọn bộ trước để cả ba đọc/sửa dần. Bản nháp chưa được nhóm duyệt để nộp.', 'Chưa đủ xác nhận đọc chéo và đóng góp thực tế của cả ba; nghiệm thu nội dung còn mở. Chưa gửi đợt 3.'),
        ('Bản nháp ngày 25/10 kế thừa pipeline, 80 run và kết quả đợt 2; bổ sung PR/score và phân tích matched/unmatched theo tập model thực sự được fit.', 'Bản ngày 30/10 kế thừa pipeline, 80 run và kết quả đợt 2; bổ sung PR/score, overlap theo tập model thực sự được fit, importance và chẩn đoán lỗi. Phạm vi tổng hợp đến 30/10, chưa bao gồm công việc có thể phát sinh từ 31/10 đến hết kỳ 08/11.'),
        ('Theo thống nhất mới ngày 25/10, tài liệu được chuẩn bị đầy đủ với công cụ hỗ trợ để cả ba đọc/sửa dần; đóng góp và mức hiểu được ghi sau khi các bạn thực sự kiểm và góp ý. Bản nháp chưa được nhóm duyệt để nộp. Hạn báo cáo 09/11 đã thống nhất với giảng viên theo xác nhận của nhóm trưởng.', 'Tài liệu được chuẩn bị với công cụ hỗ trợ theo trao đổi ngày 25/10. Kiểm kỹ thuật ngày 30/10 không thay xác nhận mức hiểu, đóng góp và đọc chéo của thành viên. Hồ sơ chưa đủ để ghi cả ba đã duyệt nộp. Mốc gửi 09/11 do nhóm trưởng xác nhận đã thống nhất với giảng viên; nhóm trưởng sẽ tự gửi trong chuỗi thư hiện có.'),
        ('Tính liên tục giữa hai đợt', 'Tính liên tục giữa các đợt'),
        ('\\noindent\\textbf{Các mốc:} 17/08--13/09 là kỳ đợt 1; 14/09--11/10 là kỳ đợt 2; 13/10 kiểm lại kết quả và biên tập; 14/10 bổ sung phân tích lỗi/đối chiếu nguồn; 17/10 rà soát toàn văn và trình bày.', '\\noindent\\textbf{Các mốc:} kỳ đợt 1: 17/08--13/09; đợt 2: 14/09--11/10; đợt 3: 12/10--08/11. Ngày 13--17/10 kiểm và biên tập; 22--26/10 bổ sung phân tích/prototype; 30/10 chốt kỹ thuật.'),
        (r'\chapter{ĐỐI CHIẾU GÓP Ý ĐỢT 1 VÀ TIẾN ĐỘ ĐỢT 2}', r'\chapter{ĐỐI CHIẾU GÓP Ý ĐỢT 1 VÀ TIẾN ĐỘ ĐỢT 2}' + '\n' + r'\noindent\textit{Chương này lưu tiến độ lịch sử đến 17/10. Trạng thái ngày 30/10 ở Chương~\ref{chap:dot3}. Vai trò trong bảng là phân công dự kiến, không xác nhận người đó đã tự hoàn thành.}\par'),
        ('vị trí sửa là mục và số trang in dưới chân trang của bản đợt 2 hiện tại.', 'tham chiếu vị trí sửa dẫn đến mục tương ứng trong bản tích lũy này.'),
        ('trạng thái hiện tại được tách ở bảng ngay sau hình.', 'bảng sau hình lưu trạng thái lịch sử tại 17/10.'),
        ('Cập nhật ngày 25/10 theo nhóm trưởng: Anh và Thu chưa bàn giao bài đợt 3.', 'Tín xác nhận ngày 27/10 chưa hoàn thành tự đọc/chạy/review; bài tập demo có hướng dẫn sau đó chưa thay một lượt tự kiểm toàn bộ. Hồ sơ đến 30/10 chưa có bàn giao độc lập của Anh và Thu, nên trạng thái đọc và đóng góp của hai bạn chưa xác nhận.'),
        ('Chúng chưa chứng minh nguyên nhân tạo bản ghi trùng, chưa xác định mức overlap trong tập fit thực tế theo từng seed và chưa định lượng ảnh hưởng đến UADR.', r'Chúng chưa chứng minh nguyên nhân tạo bản ghi trùng. Chương~\ref{chap:dot3} cập nhật overlap theo tập fit thực tế từng model/seed và metric matched/unmatched; đây là liên hệ mô tả, chưa phải thí nghiệm loại trùng để đo tác động nhân quả lên UADR.'),
        ('Phân tích này chưa thay cho PR curve, score distribution, giải thích feature hay thí nghiệm độ nhạy overlap.', r'Phân tích category là bằng chứng lịch sử; PR/score, importance và lát cắt overlap được bổ sung ở Chương~\ref{chap:dot3}, còn retrain loại trùng chưa thực hiện.'),
        ('Mã, cấu hình và tài liệu nhẹ được quản lý trên GitHub; raw, model bundle và prediction nặng lưu tại máy/Drive.', 'Bản chốt 30/10 được kiểm tại máy; chưa xác nhận đồng bộ bản mới lên GitHub/Drive. Raw, bundle và prediction nặng không nằm trong ZIP nguồn báo cáo.'),
        (r'\path{output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf} & PDF đợt 2 dùng nộp; bản chính theo tên nhóm.\\', r'\path{docs/report_dot3_final_20261030/main.tex} & Nguồn bản chốt kỹ thuật đợt 3.\\' + '\n' + r'\path{docs/evidence/dot_03/final_20261030/} & Log 46 test, validator, PR/overlap tính lại và audit mới.\\' + '\n' + r'\path{docs/evidence/dot_03/features_20261025/} & Importance đủ 40 run RF/XGB.\\' + '\n' + r'\path{docs/evidence/dot_03/final_diagnostics_20261025/} & Lát cắt lỗi, ổn định, bất đồng và thời gian có ghi giới hạn.\\' + '\n' + r'\path{demo/} & Prototype CSV và tình huống replay.\\' + '\n' + r'\path{output/pdf/NhomTLCN_TramAnh_VuongThu_TrongTin_dot2.pdf} & PDF đợt 2 đã gửi, giữ nguyên làm lịch sử.\\'),
    ])
    edit('dot3_analysis_20261025.tex', [
        ('PHÂN TÍCH BỔ SUNG ĐỢT 3 -- BẢN NHÁP', 'PHÂN TÍCH VÀ KẾT LUẬN ĐỢT 3'),
        ('Phạm vi và trạng thái ngày 25/10/2026', 'Phạm vi và trạng thái ngày 30/10/2026'),
        (r'\section{Precision--Recall và phân bố score}', r'\input{status_20261030.tex}' + '\n\n' + r'\section{Precision--Recall và phân bố score}'),
        (r'\section{Phần nhóm cần đọc và kiểm tiếp}', r'\input{conclusion_20261030.tex}' + '\n\n' + r'\section{Phần nhóm cần đọc và kiểm tiếp}'),
        ('Bộ kiểm ngày 25/10 có 42 test đạt:', 'Bằng chứng lịch sử ngày 25/10 có 42 test đạt:'),
    ])
    edit('final_diagnostics.tex', [
        ('Máy đo suy luận hiện tại:', 'Máy dùng đo suy luận ngày 25/10:'),
        ('Đây là thông tin máy đo hiện tại,', 'Đây là thông tin máy của phép đo ngày 25/10,'),
        ('T9/T10 và các hình còn thiếu của kế hoạch.', 'chi phí và chẩn đoán lỗi cùng các hình còn thiếu của kế hoạch.'),
    ])
    print('Prepared separate source with checked replacements')


if __name__ == '__main__':
    main()
