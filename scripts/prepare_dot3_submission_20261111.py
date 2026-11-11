"""Create a dated submission copy; preserve the previous group-review release."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'docs/report_dot3_review_20261106'
NEW = ROOT / 'docs/report_dot3_submission_20261111'


def replace_exact(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f'Expected one occurrence: {old[:100]!r}, got {text.count(old)}')
    return text.replace(old, new, 1)


def main():
    if NEW.exists():
        raise FileExistsError(NEW)
    shutil.copytree(OLD, NEW, ignore=shutil.ignore_patterns('build*', 'qa_render*', '*.log', '*.aux'))
    p = NEW / 'main.tex'
    s = p.read_text(encoding='utf-8')
    s = s.replace('Tích lũy đợt 3 - Rà soát 07/11/2026', 'Tích lũy đợt 3 - Bản ngày 11/11/2026')
    s = s.replace(r'\textbf{Ngày rà soát trình bày:} & 07/11/2026', r'\textbf{Ngày cập nhật bản nộp:} & 11/11/2026')
    s = replace_exact(s, 'Báo cáo tích lũy đợt 3; kết quả chốt 30/10, rà soát trình bày 07/11. Chờ nhóm đọc chéo trước khi gửi.',
                      'Báo cáo tiến độ tích lũy đợt 3; kết quả chốt 30/10, cập nhật trình bày và hồ sơ ngày 11/11/2026.')
    s = replace_exact(s, 'Đợt 3; mốc gửi 09/11/2026 do nhóm trưởng cung cấp. Hồ sơ được rà soát chưa có thư gốc xác nhận riêng ngày này.',
                      'Kỳ kế hoạch đến 08/11/2026. Kết quả thực nghiệm và phân tích trong bản này giữ mốc 30/10; không ghi nhận lượt huấn luyện mới sau mốc đó.')
    s = replace_exact(s, 'Trạng thái nhóm & Hồ sơ rà soát đến 10/11/2026 chưa đủ xác nhận đọc chéo và đóng góp thực tế của cả ba; nghiệm thu nội dung còn mở. Trạng thái gửi email hiện tại chưa được kiểm trực tiếp.',
                      'Phạm vi xác nhận & Kiểm kỹ thuật và phân công được trình bày riêng. Việc đọc chéo, giải thích và xác nhận đóng góp từng thành viên đang tiếp tục; bản này không ghi nhận các việc đó là đã hoàn tất.')
    start = s.index('Tài liệu được chuẩn bị với công cụ hỗ trợ theo trao đổi ngày 25/10.')
    end = s.index('\n\n', start)
    s = s[:start] + ('Bản thảo, mã và các phép kiểm có sử dụng công cụ hỗ trợ theo thống nhất của nhóm. '
                    'Kết quả kiểm kỹ thuật không thay xác nhận đóng góp hoặc mức hiểu của từng thành viên. '
                    'Nhóm trưởng gửi bản này để báo cáo tiến độ; việc đọc chéo và hoàn thiện phần giải thích cá nhân tiếp tục sau đợt báo cáo.') + s[end:]
    s = replace_exact(s, 'Mốc gửi 09/11 do nhóm trưởng cung cấp; chưa có thư gốc xác nhận riêng ngày này trong hồ sơ được rà soát.',
                      '09/11 là mốc nội bộ do nhóm trưởng cung cấp; kỳ tổng hợp không đồng nghĩa hạn nộp riêng do giảng viên ấn định.')
    s = replace_exact(s, 'Đường dẫn tính từ repo. Bản rà soát 07/11 giữ kết quả chốt 30/10. Hồ sơ đến 10/11/2026 chưa có biên nhận; trạng thái gửi email chưa kiểm trực tiếp. Đồng bộ cần đối chiếu đúng hash.',
                      'Đường dẫn tính từ repo. Bản ngày 11/11 giữ kết quả chốt 30/10. Bản PDF và gói nguồn được định danh bằng SHA-256 trong hồ sơ phát hành; biên nhận gửi thư được lưu riêng sau khi gửi.')
    s = replace_exact(s, r'\path{docs/report_dot3_review_20261106/main.tex} & Nguồn bản rà soát trình bày 07/11; kết quả chốt 30/10.',
                      r'\path{docs/report_dot3_submission_20261111/main.tex} & Nguồn bản báo cáo ngày 11/11; kết quả chốt 30/10.')
    p.write_text(s, encoding='utf-8')

    p = NEW / 'dot3_analysis_20261025.tex'
    s = p.read_text(encoding='utf-8')
    start = s.index('Chương này bổ sung phân tích hậu nghiệm')
    end = s.index('\n\n', start)
    s = s[:start] + ('Chương này bổ sung phân tích hậu nghiệm trên 80 run đã hoàn thành ở đợt 2. '
                    'Không huấn luyện lại baseline, không chọn lại ngưỡng trên test và không thay official split. '
                    'Các đầu ra gồm đường PR, phân bố score, lát cắt overlap, importance và chẩn đoán lỗi. '
                    'Phạm vi xác nhận đóng góp và đọc chéo của thành viên được nêu ở phần thông tin phiên bản; '
                    'các bảng dưới đây chỉ báo cáo đầu ra kỹ thuật có nguồn truy vết.') + s[end:]
    start = s.index(r'\section{Phần nhóm cần đọc và kiểm tiếp}')
    end = s.index(r'\section{Bằng chứng và kiểm kỹ thuật}', start)
    s = s[:start] + (r'\section{Phân công phần việc tiếp nối}' + '\n'
        'Trâm Anh phụ trách dữ liệu, đối chiếu nguồn và giới hạn benchmark; Vương Thu phụ trách metric, '
        'ngưỡng và phân tích lỗi; Trọng Tín phụ trách protocol, tích hợp và demo. '
        'Các nhánh tramanh, vuongthu, trongtin lưu hồ sơ theo phạm vi phân công, main lưu kết quả chung. '
        'Việc đồng bộ tệp theo ủy quyền không tự chứng nhận tác giả hoặc lượt đọc chéo. '
        'Nhóm tiếp tục kiểm ví dụ, góp ý nội dung và ghi nhận phần chỉnh sửa thực tế của từng người.\n\n') + s[end:]
    p.write_text(s, encoding='utf-8')

    p = NEW / 'conclusion_20261030.tex'
    s = p.read_text(encoding='utf-8')
    s = replace_exact(s, 'Nhóm cần tự đọc, tái kiểm ví dụ, viết nhận xét và xác nhận đóng góp trước khi gửi. Bản chốt kỹ thuật không tự đóng Gate nội dung hoặc xác nhận giảng viên đã duyệt.',
                      'Phần tiếp nối gồm hoàn thiện giải thích cá nhân, đọc chéo, kiểm thử demo và chuẩn bị bảo vệ. Các kiểm kỹ thuật không thay nghiệm thu nội dung hoặc ý kiến của giảng viên.')
    p.write_text(s, encoding='utf-8')
    print(NEW)


if __name__ == '__main__':
    main()
