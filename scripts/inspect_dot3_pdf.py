"""Render every PDF page and record geometry; visual conclusions are recorded separately."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re
import pymupdf
from PIL import Image, ImageChops, ImageDraw

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('pdf',type=Path)
parser.add_argument('output',type=Path)
args=parser.parse_args()
args.output.mkdir(parents=True,exist_ok=True)
render=args.output/'render_150'; render.mkdir(exist_ok=True)
doc=pymupdf.open(args.pdf)
pages=[]; all_text=[]
for i,page in enumerate(doc,1):
    path=render/f'page_{i:02}_150.png'
    pix=page.get_pixmap(dpi=150,alpha=False)
    pix.save(path)
    im=Image.open(path).convert('RGB')
    ink=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda v:255 if v>25 else 0)
    box=ink.getbbox()
    spans=[]
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            spans.extend(s for s in line['spans'] if s['text'].strip())
    outside=[{'text':s['text'],'bbox':s['bbox']} for s in spans
        if s['bbox'][0]<-.25 or s['bbox'][1]<-.25 or s['bbox'][2]>page.rect.width+.25 or s['bbox'][3]>page.rect.height+.25]
    images=[]
    for img in page.get_image_info():
        r=pymupdf.Rect(img['bbox'])
        images.append({'width_px':img['width'],'height_px':img['height'],'bbox_pt':list(r),
            'effective_dpi_x':round(img['width']/r.width*72,1),'effective_dpi_y':round(img['height']/r.height*72,1)})
    text=page.get_text()
    all_text.append(f'\n===== PDF PAGE {i} =====\n'+text)
    pages.append({'pdf_page':i,'page_size_pt':list(page.rect)[2:],
        'render_px':[pix.width,pix.height],'render_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'ink_bbox_px':box,'edge_clearance_px':min(box[0],box[1],pix.width-box[2],pix.height-box[3]) if box else None,
        'text_spans_outside_page':outside,'smallest_text_pt':round(min(s['size'] for s in spans),2) if spans else None,
        'raster_images':images,'has_replacement_character':'\ufffd' in text,
        'figure_caption_starts':re.findall(r'Hình \d+\.\d+\.[^\n]*',text),
        'table_caption_starts':re.findall(r'Bảng [\dA-Z]+\.\d+[^\n]*',text)})

for group in range((len(pages)+7)//8):
    sheet=Image.new('RGB',(1240,910),'#e5e5e5'); draw=ImageDraw.Draw(sheet)
    for slot in range(8):
        idx=group*8+slot
        if idx>=len(pages):break
        pic=Image.open(render/f'page_{idx+1:02}_150.png');pic.thumbnail((300,420))
        x=(slot%4)*310+(310-pic.width)//2; y=(slot//4)*455+25
        sheet.paste(pic,(x,y));draw.text(((slot%4)*310+8,(slot//4)*455+5),f'PDF {idx+1}',fill='black')
    sheet.save(render/f'sheet_{group+1:02}.jpg',quality=88)

report={'inspected_at_utc':datetime.now(timezone.utc).isoformat(),'pdf':str(args.pdf.resolve()),
    'sha256':hashlib.sha256(args.pdf.read_bytes()).hexdigest(),'page_count':len(doc),'render_dpi':150,
    'geometry_only':True,'visual_review_required':True,'pages':pages}
(args.output/'PDF_GEOMETRY.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(args.output/'FULL_TEXT.txt').write_text(''.join(all_text),encoding='utf-8')
print(json.dumps({'pages':len(doc),'rasterized':len(pages),'span_outside_page_count':sum(len(p['text_spans_outside_page']) for p in pages),
    'replacement_characters':sum(p['has_replacement_character'] for p in pages),'sha256':report['sha256']}))
