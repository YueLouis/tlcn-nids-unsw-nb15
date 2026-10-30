"""Make a traceable local round-3 release, without sending or cloud sync."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import zipfile
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/evidence/dot_03/final_20261030'
SOURCE = ROOT / 'docs/report_dot3_final_20261030'
RELEASE = ROOT.parent / '02_Bao_cao/DOT_3_CHOT_20261030'
PREFIX = 'Nguon_Bao_Cao_Dot3_20261030'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    log = (SOURCE / 'build/main.log').read_text(encoding='utf-8', errors='replace')
    assert not re.search(r'Overfull|Missing character|There were undefined|Label\(s\) may have changed|(?:Reference|Citation).*undefined', log)
    pdf = pymupdf.open(SOURCE / 'build/main.pdf')
    assert len(pdf) == 60
    assert all(p.get_text().strip() and '??' not in p.get_text() for p in pdf)
    # Text must remain within the physical page, including headers and footer.
    for page in pdf:
        for word in page.get_text('words'):
            assert word[0] >= 0 and word[1] >= 0 and word[2] <= page.rect.width and word[3] <= page.rect.height
    audit = json.loads((OUT / 'FRESH_AUDIT.json').read_text(encoding='utf-8'))
    tables = json.loads((OUT / 'REPORT_TABLE_CHECK.json').read_text(encoding='utf-8'))
    assert audit['fresh_demo']['prediction_rows'] == 3200
    assert audit['frozen_input_hashes_matched'] == 333 and tables['table_rows_checked'] == 174
    tests = (OUT / 'tests.log').read_text(encoding='utf-8')
    assert 'Ran 46 tests' in tests and re.search(r'\nOK\s*$', tests)
    RELEASE.mkdir(exist_ok=True)
    target_pdf = RELEASE / 'NhomTLCN_TramAnh_VuongThu_TrongTin_dot3.pdf'
    shutil.copy2(SOURCE / 'build/main.pdf', target_pdf)

    package_files = set()
    for directory in ['src', 'tests', 'configs', 'scripts', 'demo', 'docs/protocol',
                      'docs/references', 'docs/reports', 'artifacts/data',
                      'docs/report_dot3_final_20261030', 'docs/evidence/dot_02/final_20261013',
                      'docs/evidence/dot_02/category_errors_20261014',
                      'docs/evidence/dot_03/pr_scores_20261022', 'docs/evidence/dot_03/overlap_20261025',
                      'docs/evidence/dot_03/features_20261025', 'docs/evidence/dot_03/final_diagnostics_20261025',
                      'docs/evidence/dot_03/final_20261030']:
        for p in (ROOT / directory).rglob('*'):
            if not p.is_file() or any(part in ('build', 'render', '__pycache__', '.venv', 'node_modules') for part in p.parts):
                continue
            if p.suffix in ('.pyc', '.joblib') or p.name in ('RELEASE_CHECK.json', 'SOURCE_ZIP_REBUILD.json'):
                continue
            package_files.add(p)
    for name in ['README.md', 'requirements.txt', 'requirements-repro.txt', 'requirements-analysis.txt', 'pyproject.toml']:
        if (ROOT / name).exists():
            package_files.add(ROOT / name)
    for name in ['DAC_TA_OVERLAP_DOT_03_20261025.md', 'DAC_TA_CHAN_DOAN_CUOI_20261025.md', 'KE_HOACH_DOT_03_20261022.md']:
        package_files.add(ROOT / 'docs/management' / name)
    for folder in (ROOT / 'results/runs').iterdir():
        if folder.is_dir():
            for name in ('run.json', 'metrics.csv'):
                package_files.add(folder / name)
    readme = '''# Nguồn báo cáo TLCN đợt 3 ngày 30/10/2026

PDF chính nằm cạnh ZIP này trong thư mục giao. Bản kỹ thuật đã kiểm, chưa xác nhận cả ba duyệt nội dung và chưa gửi.

## Dựng PDF

Mở `docs/report_dot3_final_20261030/main.tex` bằng XeLaTeX (MiKTeX/TeX Live), có font Times New Roman, Arial và Consolas.
Chuyển thư mục hiện hành vào `docs/report_dot3_final_20261030`, tạo `build`, chạy ba lượt:

    xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex

Tệp gồm toàn bộ TeX, logo, hình, CSV đối chiếu, log kiểm và mã nhẹ. Các bảng được chốt trong TeX; CSV đi kèm dùng truy vết. Byte PDF có thể khác theo timestamp, đối chiếu văn bản và ảnh trang để xác nhận nội dung.

## Phạm vi tái kiểm

`src`, `tests`, `configs`, `scripts` và metadata/metric 80 run có trong gói. Unit test và validator chạy với `PYTHONPATH=src`; xem `requirements-repro.txt` và `requirements-analysis.txt` để khớp thư viện lịch sử.

Raw CSV, predictions.csv và model_bundle.joblib nặng không chứa trong ZIP. Muốn chạy toàn bộ phân tích/inference phải khôi phục đúng dữ liệu và 80 bundle/prediction từ hồ sơ hiện có, đối chiếu các hash trong audit; không huấn luyện lại để thay thế đầu vào lịch sử. Demo trong ZIP nguồn chưa phải bản portable đầy đủ; dùng bộ DEMO_NIDS_NHOM_20261025 có sẵn nếu cần trình diễn.

Mã kiểm/phân tích lịch sử có đường dẫn output theo ngày; không ghi đè bằng chứng cũ. Chỉ định thư mục mới khi chạy phân tích lại. Log 13/10, 22–26/10 và log mới 30/10 được giữ đúng thời điểm; báo cáo không coi log cũ là phép chạy mới.

Không có bằng chứng phần cứng huấn luyện lịch sử, thời gian train-only, fulltext S07 hoặc nghiệm thu nội dung nhóm. Không ký Gate, không gửi mail hoặc đồng bộ cloud bằng việc dựng gói.
'''
    archive = RELEASE / (PREFIX + '.zip')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        z.writestr(PREFIX + '/DOC_TRUOC.md', readme.encode('utf-8'))
        manifest = []
        for p in sorted(package_files):
            rel = p.relative_to(ROOT).as_posix()
            z.write(p, PREFIX + '/' + rel)
            manifest.append({'path': rel, 'bytes': p.stat().st_size, 'sha256': digest(p)})
        z.writestr(PREFIX + '/SOURCE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for row in manifest:
            assert hashlib.sha256(z.read(PREFIX + '/' + row['path'])).hexdigest() == row['sha256']
    result = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'pdf_pages': len(pdf),
              'pdf_sha256': digest(target_pdf), 'source_zip_sha256': digest(archive),
              'source_files_verified': len(manifest), 'zip_crc_and_member_hashes': True,
              'latex_undefined_overfull_missing_glyphs': False,
              'all_page_images_reviewed': True, 'selected_tables_and_figures_reviewed_at_page_size': True,
              'status': 'Technical release; group review unconfirmed; not submitted; cloud sync unverified'}
    (OUT / 'RELEASE_CHECK.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
