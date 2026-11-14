"""Build only public presentation assets, parameter exports and demo subsets."""
from pathlib import Path
import json,shutil
from portable_markdown import render_portable_markdown
from static_host_files import write_static_host_files
from public_release import report_downloads
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'demo/presentation';DEST=ROOT/'sites/nids-presentation/dist'
DEST.mkdir(parents=True,exist_ok=True)
for name in ('presentation.css','presentation.js','data.js','SOURCE_DATA.json','browser-engine.mjs','browser-worker.mjs','browser-adapter.js'):
    shutil.copy2(SOURCE/name,DEST/name)
shutil.copytree(SOURCE/'assets',DEST/'assets',dirs_exist_ok=True)
shutil.copytree(ROOT/'demo/cases',DEST/'cases',dirs_exist_ok=True)
html=(SOURCE/'index.html').read_text(encoding='utf-8')
html=html.replace('<script src="presentation.js"></script>','<script src="browser-adapter.js"></script>\n<script src="presentation.js"></script>')
html=html.replace('<a href="/lab" class="small">Mở phòng thử nghiệm đầy đủ ↗</a>','<span class="small muted browser-note">Bản online · CSV được xử lý trên trình duyệt</span>')
html=html.replace('<a href="/lab">Mở phòng thử nghiệm đầy đủ ↗</a>','<a href="https://github.com/YueLouis/tlcn-nids-unsw-nb15#readme" target="_blank" rel="noopener">Mã nguồn và cách mở bản local ↗</a>')
html=html.replace('Demo suy luận từ CSV qua mô hình đã lưu ở seed 42.','Bản online suy luận ngay trong trình duyệt từ tham số mô hình seed 42 đã xuất. CSV bạn mở được xử lý tại máy, không tải lên máy chủ. Bản local dùng API Python.')
html=html.replace('Demo suy luận từ CSV qua model đã lưu;','Demo suy luận từ CSV qua tham số model đã lưu;')
(DEST/'index.html').write_text(html,encoding='utf-8')
# Group review uses the same hosted origin and frozen report files.
for name in ('ho-so.html','ho-so.css','ho-so.js'):
    shutil.copy2(SOURCE/name,DEST/name)
downloads=DEST/'downloads'
downloads.mkdir(exist_ok=True)
active_reports=report_downloads(ROOT)
if 'NhomTLCN_tong_20261114.pdf' in active_reports:
    for old in ('NhomTLCN_dot4_BAN_NHAP_20261113.pdf','NhomTLCN_tong_BAN_NHAP_20261113.pdf',
                'Nguon_dot4_BAN_NHAP_20261113.zip','Nguon_tong_BAN_NHAP_20261113.zip'):
        (downloads/old).unlink(missing_ok=True)
for path in active_reports.values():
    shutil.copy2(path,downloads/path.name)
for name in ('BAN_GIAO_BAO_VE_20261113.md','DOI_CHIEU_YEU_CAU_20261114.md'):
    source=ROOT/'docs/management'/name
    (downloads/name).write_text(render_portable_markdown(source.read_text(encoding='utf-8'),source,ROOT),encoding='utf-8')
download_manifest=[]
import hashlib
for path in sorted(downloads.iterdir()):
    if path.is_file() and path.name != 'MANIFEST.json':
        download_manifest.append(dict(file=path.name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(downloads/'MANIFEST.json').write_text(json.dumps(download_manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
provenance=json.loads((SOURCE/'SOURCE_DATA.json').read_text(encoding='utf-8'))
provenance['inference']['public_engine']='browser-parameters-v1: Web Worker, no CSV upload'
provenance['inference']['export_manifest']='models/manifest.json'
provenance['inference']['local_engine']='Python API: /api/lab/run and /api/predict'
(DEST/'SOURCE_DATA.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write_static_host_files(DEST,SOURCE)
print('Public assets prepared',DEST)
