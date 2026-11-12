"""Build a review handoff and an offline browser demo without claiming submission."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import zipfile
import qrcode

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/release_20261113'
URL = 'https://nids-unsw-nb15-tlcn.nttin181.chatgpt.site'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    guide = ROOT / 'docs/management/BAN_GIAO_BAO_VE_20261113.md'
    shutil.copy2(guide, OUT / 'BAT_DAU.md')
    qrcode.make(URL).save(OUT / 'QR_WEB_NIDS.png')
    (OUT / 'WEB_PUBLIC.txt').write_text(URL + '\n', encoding='utf-8')
    (OUT / 'DRIVE_DOC_DUYET.txt').write_text('https://drive.google.com/drive/folders/1d-m5b35FVvGU3AEuA8vx1c9btG5xznUl\n', encoding='utf-8')
    reports = OUT / 'reports'
    reports.mkdir(exist_ok=True)
    for kind in ('dot4', 'tong'):
        source = ROOT / f'output/followup_reports_review_20261113/{kind}'
        for name in (f'NhomTLCN_{kind}_BAN_NHAP_20261113.pdf', f'Nguon_{kind}_BAN_NHAP_20261113.zip', 'DRAFT_CHECK.json', 'REPORT_TABLE_CHECK.json', 'VISUAL_REVIEW.json'):
            path = source / name
            if not path.is_file():
                raise FileNotFoundError(path)
            shutil.copy2(path, reports / (f'{kind}_{name}' if name.endswith('.json') else name))
    evidence = OUT / 'evidence'
    evidence.mkdir(exist_ok=True)
    for source, dest in [('output/browser_parity/PARITY.json','BROWSER_PARITY.json'), ('output/public_site_20261113/DEPLOYMENT.json','DEPLOYMENT.json'), ('output/public_site_20261113/LIVE_BROWSER_CHECK.json','LIVE_BROWSER_CHECK.json'), ('output/code_api_review_20261112/API_AUDIT.json','LOCAL_API_AUDIT.json'), ('output/presentation_review_20261113/LAYOUT_CHECKS.json','LAYOUT_CHECKS.json')]:
        shutil.copy2(ROOT / source, evidence / dest)
    (OUT/'TRANG_THAI.json').write_text(json.dumps(dict(prepared_at_utc=datetime.now(timezone.utc).isoformat(), public_url=URL, dot3='SENT_20261112_2316_GMT7', dot4='REVIEW_READY_NOT_SUBMITTED', tong='REVIEW_READY_NOT_SUBMITTED', group_review=False, physical_hdmi_test=False, independent_traffic_dataset=False), ensure_ascii=False, indent=2), encoding='utf-8')
    offline = OUT / 'NIDS_DEMO_OFFLINE_20261113.zip'
    web = ROOT / 'sites/nids-presentation/dist'
    with zipfile.ZipFile(offline, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in web.rglob('*'):
            if path.is_file():
                archive.write(path, 'web/' + path.relative_to(web).as_posix())
        archive.write(ROOT/'scripts/offline_presentation.py', 'offline_presentation.py')
        archive.writestr('CHAY_DEMO.cmd', '@echo off\r\ncd /d "%~dp0"\r\npython offline_presentation.py\r\npause\r\n')
        archive.writestr('DOC_TRUOC.txt', 'Giai nen day du. Can Python 3 va Chrome/Edge hien hanh. Chay CHAY_DEMO.cmd, giu cua so mo, mo dia chi in trong cua so (thuong la http://127.0.0.1:4399/; tu chon cong khac neu ban). Khong can pip hoac Internet. Ctrl+C de dung.\n')
    with zipfile.ZipFile(offline) as archive:
        assert archive.testzip() is None
        assert len([n for n in archive.namelist() if n.endswith('.bin.gz')]) == 16
    files = [p for p in OUT.rglob('*') if p.is_file() and p.name not in ('MANIFEST.json', 'NIDS_BAN_GIAO_20261113.zip') and not p.name.startswith(('CONTACT_', 'SLIDE_'))]
    manifest = [dict(path=p.relative_to(OUT).as_posix(), bytes=p.stat().st_size, sha256=sha(p)) for p in files]
    (OUT/'MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    final_zip = OUT / 'NIDS_BAN_GIAO_20261113.zip'
    with zipfile.ZipFile(final_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files + [OUT/'MANIFEST.json']:
            archive.write(path, path.relative_to(OUT).as_posix())
    with zipfile.ZipFile(final_zip) as archive:
        assert archive.testzip() is None
        assert all(hashlib.sha256(archive.read(row['path'])).hexdigest() == row['sha256'] for row in manifest)
    print(json.dumps(dict(package=str(final_zip), bytes=final_zip.stat().st_size, sha256=sha(final_zip), files=len(files), crc_and_hashes_match=True), ensure_ascii=False))


if __name__ == '__main__':
    main()
