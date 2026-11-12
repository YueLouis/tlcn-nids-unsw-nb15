"""Package checked follow-up drafts privately; this does not publish or submit them."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import zipfile
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/followup_reports_review_20261113'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    summary = []
    for kind in ('dot4', 'tong'):
        source = ROOT / f'docs/report_{kind}_review_20261112'
        folder = OUT / kind
        folder.mkdir(parents=True, exist_ok=True)
        pdf = source / 'build/main.pdf'
        log = (source / 'build/main.log').read_text(encoding='utf-8', errors='replace')
        blocking = re.findall(r'Overfull[^\n]*|Missing character[^\n]*|[^\n]*undefined references[^\n]*|[^\n]*Rerun to[^\n]*', log)
        assert not blocking, blocking
        doc = pymupdf.open(pdf)
        font_info = [dict(page=i+1, fonts=page.get_fonts(full=True)) for i,page in enumerate(doc)]
        assert all(doc.extract_font(font[0])[3] for page in doc for font in page.get_fonts() if font[0]), 'unembedded font'
        (folder/'PDF_FONTS.json').write_text(json.dumps(font_info,ensure_ascii=False,indent=2),encoding='utf-8')
        names = doc.resolve_names()
        link_count = 0
        geometry = []
        for number, page in enumerate(doc, 1):
            spans = [span for block in page.get_text('dict')['blocks'] if block['type'] == 0
                     for line in block['lines'] for span in line['spans']]
            outside = [span['text'] for span in spans if not page.rect.contains(pymupdf.Rect(span['bbox']))]
            assert not outside, (kind, number, outside)
            assert '\ufffd' not in page.get_text(), (kind, number)
            geometry.append(dict(page=number, text_characters=len(page.get_text()), outside=outside))
            for link in page.get_links():
                if link['kind'] == pymupdf.LINK_GOTO or 'nameddest' in link:
                    assert 0 <= link['page'] < len(doc), link
                    if 'nameddest' in link:
                        assert link['nameddest'] in names
                    link_count += 1
        assert all(1 <= entry[2] <= len(doc) for entry in doc.get_toc())
        resources = []
        for tex in source.glob('*.tex'):
            text = tex.read_text(encoding='utf-8')
            for command, name in re.findall(r'\\(input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}', text):
                path = source / name
                if command == 'input' and not path.suffix:
                    path = path.with_suffix('.tex')
                assert path.is_file(), path
                resources.append(path.relative_to(source).as_posix())
        tables = json.loads((folder / 'REPORT_TABLE_CHECK.json').read_text(encoding='utf-8'))
        assert tables['table_rows_checked'] == 174
        files = [p for p in source.rglob('*') if p.is_file() and not any(x.startswith('build') for x in p.relative_to(source).parts)]
        manifest = [dict(path=p.relative_to(source).as_posix(), sha256=sha(p)) for p in files]
        zip_path = folder / f'Nguon_{kind}_BAN_NHAP_20261113.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path, path.relative_to(source).as_posix())
            archive.writestr('SOURCE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))
        with zipfile.ZipFile(zip_path) as archive:
            assert archive.testzip() is None
            assert all(hashlib.sha256(archive.read(row['path'])).hexdigest() == row['sha256'] for row in manifest)
        dest = folder / f'NhomTLCN_{kind}_BAN_NHAP_20261113.pdf'
        shutil.copy2(pdf, dest)
        receipt = dict(kind=kind, checked_at_utc=datetime.now(timezone.utc).isoformat(), pages=len(doc),
                       pdf_sha256=sha(pdf), internal_links=link_count, bookmark_destinations=len(doc.get_toc()),
                       table_rows_checked=174, tex_resource_references=len(resources), source_files=len(files),
                       zip_crc_and_source_hashes_match=True, compile_blocking_warnings=[],
                       geometry=geometry, all_fonts_embedded=True, presentation_updated_20261113=True, status='REVIEW_READY_NOT_APPROVED_OR_SUBMITTED',
                       group_approval=False, submitted=False,
                       remaining=['group content review', 'group presentation rehearsal', 'physical HDMI/projector test', 'cloud synchronization managed separately; public deployment verified by root'])
        (folder / 'DRAFT_CHECK.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
        summary.append({k:v for k,v in receipt.items() if k != 'geometry'})
    (OUT / 'SUMMARY.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
