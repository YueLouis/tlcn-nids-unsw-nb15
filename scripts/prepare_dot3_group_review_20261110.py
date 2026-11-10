"""Package the checked 10 Nov report for group reading; never email or approve it."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import html
import json
import shutil
import zipfile

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'docs/report_dot3_review_20261106'
BUILD = SRC / 'build_review_20261110'
AUDIT = ROOT / 'docs/evidence/dot_03/recheck_20261110/release_review'
OUT = ROOT / 'docs/releases/review_dot3_20261110'
PDF_NAME = 'BAO_CAO_DOT3_CHO_NHOM_DUYET_20261110.pdf'
ZIP_NAME = 'DOT3_GOI_DOC_DUYET_20261110.zip'
SOURCE_NAME = 'DOT3_NGUON_LATEX_20261110.zip'
GITHUB = 'https://github.com/YueLouis/tlcn-nids-unsw-nb15'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = BUILD / 'main.pdf'
    tech = json.loads((AUDIT / 'DELIVERY_TECHNICAL_CHECK.json').read_text(encoding='utf-8'))
    geometry = json.loads((AUDIT / 'PDF_GEOMETRY.json').read_text(encoding='utf-8'))
    table = json.loads((AUDIT / 'REPORT_TABLE_CHECK.json').read_text(encoding='utf-8'))
    assert sha(pdf) == tech['pdf_sha256'] == geometry['sha256']
    assert tech['pdf_pages'] == geometry['page_count'] == 62
    assert tech['internal_links_checked'] == 200
    assert table['table_rows_checked'] == 174 and table['all_displayed_cells_match_rounding']
    doc = pymupdf.open(pdf)
    text = ' '.join(p.get_text() for p in doc)
    assert 'nhóm trưởng cung cấp' in text and 'chưa có thư gốc' in text
    assert 'chưa được kiểm trực tiếp' in text
    shutil.copy2(pdf, OUT / PDF_NAME)

    source_files = sorted(p for p in SRC.rglob('*') if p.is_file()
                          and not any(part.startswith('build') for part in p.relative_to(SRC).parts))
    with zipfile.ZipFile(OUT / SOURCE_NAME, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in source_files:
            z.write(path, path.relative_to(SRC).as_posix())
        z.write(pdf, 'PDF_DA_KIEM.pdf')
        z.writestr('BIEN_DICH.txt', 'Main: main.tex\nXeLaTeX, three passes.\nFonts: Times New Roman, Arial, Consolas.\nReview copy; group approval pending.\n')
        z.writestr('SOURCE_MANIFEST.json', json.dumps([
            {'path': p.relative_to(SRC).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
            for p in source_files], ensure_ascii=False, indent=2))

    readme = f'''# Đợt 3 — bản thống nhất để cả nhóm đọc duyệt

Mở **{PDF_NAME}**, 62 trang. Đây là bản đã sửa cách dẫn nguồn mốc 09/11; số liệu và 80 run giữ nguyên. Gói này thay bản đọc cũ cho lượt duyệt hiện tại, không ghi đè hồ sơ đã nộp trước đây. Chưa gửi mail trong lượt chuẩn bị này; chờ cả ba đọc, sửa và báo duyệt.

PDF SHA-256: `{sha(pdf)}`

## Mỗi người mở gì trước

| Người | Phần đọc trước | Cần kiểm và giải thích |
|---|---|---|
| Trâm Anh | PDF trang 21–23; bản nháp dữ liệu ở nhánh tramanh | 45 cột/42 feature; 175.341 development và 82.332 test; train/validation/test; loại lớp LOACO trước chia |
| Vương Thu | PDF trang 34, 37–38, 55; bản nháp và CSV ở nhánh vuongthu | Mẫu số FPR/Recall/UADR; AP toàn test khác AP held-out; ID 68699 là FP và 975 là FN |
| Trọng Tín | PDF trang 23, 55, 58–59, 61; bản nháp ở nhánh trongtin | Pipeline không leakage; ví dụ CS-RF-S42 ID 1 đổi threshold; nguồn/hash và tổng hợp góp ý |

Số trang trên là số ở ô chuyển trang PDF. Sau phần được giao, cả ba đọc toàn bộ báo cáo: tên, thuật ngữ, bảng/hình, kết luận và trích dẫn. Ghi điều chưa hiểu hoặc câu cần sửa ngay tại trang tương ứng.

## Link từng phần

- [Drive chung: main và ba phần thành viên](https://drive.google.com/drive/folders/1ISRWybXz0efLyH4i4XsPZTvkQhQ48meA)
- [Drive bản chung main](https://drive.google.com/drive/folders/1Qwx3tQCd5kPXtYwP_0sc2_hluz6Erj2R)
- [Hồ sơ chung trên main]({GITHUB}/tree/main/docs/releases/review_dot3_20261110)
- [Trâm Anh]({GITHUB}/tree/tramanh/docs/group_delivery_20261110/TramAnh)
- [Vương Thu]({GITHUB}/tree/vuongthu/docs/group_delivery_20261110/VuongThu)
- [Trọng Tín]({GITHUB}/tree/trongtin/docs/group_delivery_20261110/TrongTin)

Các bản nháp đã được trợ lý chuẩn bị/tải theo ủy quyền; nhóm bổ sung nhận xét sau khi thực sự đọc. Không cần tự tải lại toàn bộ tệp để chứng minh đã đọc: ghi trang, nguồn đã mở, câu đã sửa và người đọc chéo là đủ rõ việc thực tế.

## Gói tải về

- `{SOURCE_NAME}`: nguồn LaTeX, hình, tài nguyên và PDF cùng hash.
- `{ZIP_NAME}`: PDF, nguồn LaTeX, ba bản nháp theo phân công, CSV ví dụ, các file mã/bảng nhẹ để đối chiếu và kết quả kiểm.
- `MANIFEST.json`: tên, kích thước và SHA-256 của các tệp phát hành.

Đã kiểm 174 dòng bảng khớp nguồn, 200 liên kết nội bộ, 56 bookmark, nguồn hình và bốn ví dụ gần ngưỡng. Không có lỗi biên dịch chặn, ký tự thay thế hoặc chữ vượt khổ trang. Chín thông báo Underfull hbox còn trong log; các trang sửa đã được xem lại. Kiểm kỹ thuật không thay việc cả nhóm đọc duyệt.

## Sau khi đọc

Mỗi bạn ghi ngắn: đã đọc trang nào; một con số/ví dụ đã đối chiếu với file nào; câu muốn sửa; điều chưa hiểu. Vòng đọc chéo: Thu đọc phần Anh, Tín đọc phần Thu, Anh đọc phần Tín. Nhóm thống nhất sửa, kiểm lại PDF và xác nhận đúng phiên bản trước khi Tín yêu cầu gửi email.

Đợt 4, báo cáo tổng và website vẫn là các hạng mục riêng. Việc gói đợt 3 sẵn sàng để đọc không xác nhận toàn bộ môn đã hoàn tất.
'''
    put(OUT / 'README.md', readme)
    put(OUT / 'BAT_DAU.html', '<!doctype html><html lang="vi"><meta charset="utf-8"><title>Đọc duyệt đợt 3</title><style>body{max-width:920px;margin:32px auto;padding:0 24px;font:17px/1.65 Segoe UI,Arial;color:#17324a}pre{white-space:pre-wrap;font:inherit}a{color:#005a9c}</style><h1>Đợt 3 · bản để nhóm duyệt</h1><p><a href="' + PDF_NAME + '">Mở báo cáo 62 trang</a> · <a href="' + ZIP_NAME + '">Tải gói đọc đầy đủ</a></p><pre>' + html.escape(readme) + '</pre></html>')

    audit_names = ['DELIVERY_TECHNICAL_CHECK.json', 'REPORT_TABLE_CHECK.json',
                   'VISUAL_REVIEW_20261110.json']
    for name in audit_names:
        assert (AUDIT / name).is_file(), name
        shutil.copy2(AUDIT / name, OUT / name)

    with zipfile.ZipFile(OUT / ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in [PDF_NAME, SOURCE_NAME, 'README.md', 'BAT_DAU.html'] + audit_names:
            z.write(OUT / name, name)
        for rel in ['docs/group_delivery_20261110/TramAnh/DOT3_DU_LIEU_BAN_NHAP.md',
                    'docs/group_delivery_20261110/VuongThu/DOT3_KET_QUA_BAN_NHAP.md',
                    'docs/group_delivery_20261110/VuongThu/NGUON_VI_DU_THU.csv',
                    'docs/group_delivery_20261110/TrongTin/DOT3_PROTOCOL_DEMO_BAN_NHAP.md',
                    'docs/management/ban_giao_dot3_review_20261107/NGUON_VI_DU.csv',
                    'docs/reports/DOT_02_TWO_TARGETS.csv', 'artifacts/data/data_manifest.json',
                    'src/nids_benchmark/data.py', 'src/nids_benchmark/runner.py',
                    'src/nids_benchmark/evaluation.py']:
            z.write(ROOT / rel, rel)
    zip_checks = {}
    for name in [SOURCE_NAME, ZIP_NAME]:
        with zipfile.ZipFile(OUT / name) as z:
            assert z.testzip() is None
            embedded_pdf = 'PDF_DA_KIEM.pdf' if name == SOURCE_NAME else PDF_NAME
            assert hashlib.sha256(z.read(embedded_pdf)).hexdigest() == sha(pdf)
            if name == SOURCE_NAME:
                for path in source_files:
                    assert hashlib.sha256(z.read(path.relative_to(SRC).as_posix())).hexdigest() == sha(path)
            zip_checks[name] = {'crc_ok': True, 'pdf_parity': True, 'entries': len(z.namelist())}
    manifest = {'prepared_at_utc': datetime.now(timezone.utc).isoformat(),
                'status': 'READY_FOR_GROUP_REVIEW', 'group_approval': 'pending',
                'email_sent_by_this_script': False, 'pdf_sha256': sha(pdf), 'pdf_pages': 62,
                'zip_checks': zip_checks, 'source_files': len(source_files),
                'files': [{'name': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)}
                          for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'MANIFEST.json']}
    put(OUT / 'MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps({'output': str(OUT), 'pdf_sha256': sha(pdf), 'zip_checks': zip_checks}))


if __name__ == '__main__':
    main()
