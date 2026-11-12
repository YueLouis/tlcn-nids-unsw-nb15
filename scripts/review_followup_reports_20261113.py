"""Render every follow-up PDF page and verify demo examples against frozen predictions."""
from pathlib import Path
import json
import pymupdf
import pandas as pd
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/followup_reports_review_20261113'


def main():
    examples = [('CS-RF-S42', 1, .705741, .557282, 0, 1),
                ('CS-IF-S42', 38, .018721, .007771, 0, 1),
                ('CS-IF-S42', 244, -.059887, .007771, 1, 0),
                ('CS-RF-S42', 278, .429308, .557282, 1, 0)]
    for run, record_id, score, threshold, truth, prediction in examples:
        frame = pd.read_csv(ROOT / f'results/runs/{run}/predictions.csv', float_precision='round_trip')
        row = frame[frame.record_id.eq(record_id) & frame.target_fpr.eq(.05)].iloc[0]
        assert f'{row.score:.6f}' == f'{score:.6f}'
        assert f'{row.threshold:.6f}' == f'{threshold:.6f}'
        assert row.y_true == truth and row.y_pred == prediction
    for kind in ('dot4', 'tong'):
        folder = OUT / kind
        render = folder / 'visual'
        render.mkdir(exist_ok=True)
        pdf = pymupdf.open(folder / f'NhomTLCN_{kind}_BAN_NHAP_20261113.pdf')
        contacts = []
        critical = []
        for start in range(0, len(pdf), 12):
            sheet = Image.new('RGB', (1600, 1800), '#dddddd')
            draw = ImageDraw.Draw(sheet)
            for slot, number in enumerate(range(start, min(start+12, len(pdf)))):
                pix = pdf[number].get_pixmap(matrix=pymupdf.Matrix(.62, .62), alpha=False)
                im = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
                im.thumbnail((386, 552))
                x = (slot % 4)*400 + (400-im.width)//2
                y = (slot//4)*600 + 32
                sheet.paste(im, (x, y))
                draw.text(((slot % 4)*400+15, (slot//4)*600+10), f'{kind} - PDF page {number+1}', fill='black')
            name = f'CONTACT_{start+1:02d}_{min(start+12,len(pdf)):02d}.jpg'
            sheet.save(render / name, quality=90)
            contacts.append(name)
        for n, page in enumerate(pdf):
            txt = page.get_text()
            if ('GIAO DIỆN TRÌNH BÀY' in txt.upper() or 'Màn Demo ngày 13/11' in txt
                    or n < 2 or 'Ví dụ để tập giải thích' in txt
                    or 'DANH MỤC BẢNG' in txt[:200]):
                name = f'PAGE_{n+1:02d}.png'
                page.get_pixmap(matrix=pymupdf.Matrix(1.3, 1.3), alpha=False).save(render / name)
                critical.append(name)
        receipt = dict(pages_rendered=len(pdf), contacts=contacts, critical_pages=critical,
                       demo_examples_checked=len(examples),
                       note='Rendered contact sheets require visual inspection; rendering alone is not visual acceptance.')
        (folder / 'RENDER_CHECK.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
        print(kind, len(pdf), 'pages rendered; four demo rows match frozen predictions')


if __name__ == '__main__':
    main()
