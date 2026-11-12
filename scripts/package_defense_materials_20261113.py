"""Check and package the compiled static defense deck and team reading sheet."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/presentation_defense_20261113'
OUT = ROOT / 'output/release_20261113/slides'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for stem, name, expected in [
        ('main', 'NhomTLCN_slide_du_phong_20261113.pdf', 9),
        ('phan_viec', 'NhomTLCN_phan_viec_on_nhom_20261113.pdf', 2),
    ]:
        log = (SOURCE / f'build/{stem}.log').read_text(encoding='utf-8', errors='replace')
        warnings = re.findall(r'Overfull[^\n]*|Missing character[^\n]*|[^\n]*undefined references[^\n]*', log)
        assert not warnings, warnings
        pdf = SOURCE / f'build/{stem}.pdf'
        document = pymupdf.open(pdf)
        assert len(document) == expected
        geometry = []
        for number, page in enumerate(document, 1):
            if stem == 'main':
                assert abs(page.rect.width / page.rect.height - 16/9) < .001
            spans = [s for b in page.get_text('dict')['blocks'] if b['type'] == 0
                     for line in b['lines'] for s in line['spans']]
            outside = [s['text'] for s in spans if not page.rect.contains(pymupdf.Rect(s['bbox']))]
            assert not outside, (stem, number, outside)
            assert '\ufffd' not in page.get_text()
            assert len(page.get_text().strip()) > 100, (stem, number, 'blank page')
            assert all(document.extract_font(f[0])[3] for f in page.get_fonts() if f[0])
            geometry.append(dict(page=number, outside=outside, characters=len(page.get_text())))
            prefix = 'SLIDE' if stem == 'main' else 'PHAN_VIEC'
            page.get_pixmap(matrix=pymupdf.Matrix(1.2, 1.2)).save(OUT / f'{prefix}_{number:02}.png')
        target = OUT / name
        shutil.copy2(pdf, target)
        shutil.copy2(SOURCE / f'{stem}.tex', OUT / f'{stem}.tex')
        records.append(dict(pdf=name, pages=len(document), sha256=sha(target),
                            fonts_embedded=True, page_geometry=geometry))
        if stem == 'main':
            contact = Image.new('RGB', (1800, 1110), '#dce4df')
            draw = ImageDraw.Draw(contact)
            for i, page in enumerate(document):
                pix = page.get_pixmap(matrix=pymupdf.Matrix(.6, .6))
                image = Image.frombytes('RGB', [pix.width, pix.height], pix.samples).resize((580, 326))
                x, y = 10 + (i % 3)*600, 30 + (i // 3)*365
                contact.paste(image, (x, y))
                draw.text((x, y-18), str(i+1), fill='#153e38')
            contact.save(OUT / 'CONTACT_9_SLIDES.jpg')
    archive = OUT / 'Nguon_slide_va_phan_viec_20261113.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for filename in ('main.tex', 'phan_viec.tex'):
            z.write(SOURCE / filename, filename)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    receipt = dict(status='CHECKED_PENDING_GROUP_REVIEW_AND_REHEARSAL', records=records,
                   source_zip=archive.name, source_zip_sha256=sha(archive),
                   physical_hdmi_checked=False, group_approved=False,
                   note='Static PDF cannot run inference. No member understanding or authorship is certified.')
    (OUT / 'SLIDES_CHECK.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
