"""Package the tested seed-42 demo separately from the small report bundle."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'02_Bao_cao/DEMO_NIDS_NHOM_20261025'


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    for p in DEST.rglob('*.pyc'):
        if '__pycache__' in p.parts:p.unlink()
    for folder in ('src','demo'):
        for p in (ROOT/folder).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix in ('.py','.csv','.html','.ps1','.json'):
                dest=DEST/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    (DEST/'scripts').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'scripts/demo_server.py',DEST/'scripts/demo_server.py')
    shutil.copy2(ROOT/'requirements-repro.txt',DEST/'requirements-repro.txt')
    for scenario in ('CS','LR','LD','LE'):
        for model in ('RF','XGB','IF','AE'):
            rid=f'{scenario}-{model}-S42'
            target=DEST/'results/runs'/rid;target.mkdir(parents=True,exist_ok=True)
            for name in ('model_bundle.joblib','run.json'):
                shutil.copy2(ROOT/'results/runs'/rid/name,target/name)
    (DEST/'CAI_THU_VIEN.ps1').write_text("$ErrorActionPreference = 'Stop'\nSet-Location -LiteralPath $PSScriptRoot\npython -m venv .venv\n& '.\\.venv\\Scripts\\python.exe' -m pip install -r requirements-repro.txt\nif ($LASTEXITCODE -ne 0) { throw 'Chưa cài được thư viện.' }\nWrite-Host 'Đã cài. Mở demo\\MO_DEMO.ps1 để thử.'\n",encoding='utf-8-sig')
    (DEST/'DOC_TRUOC.txt').write_text('DEMO NIDS — ANH / THU / TÍN\n\n1. Giải nén toàn bộ, không chỉ lấy file HTML.\n2. Môi trường gốc: Python 3.14.4, thư viện đúng requirements-repro.txt. Nếu máy chưa có thư viện, chạy CAI_THU_VIEN.ps1 (cần mạng lúc cài).\n3. Chạy demo/MO_DEMO.ps1, hoặc tại thư mục này chạy python scripts/demo_server.py rồi mở http://127.0.0.1:4397/lab . Có thể dùng .venv/Scripts/python.exe thay python nếu cài vào venv.\n4. Trong Thiết lập, chọn dữ liệu → mô hình → Chạy kịch bản. Kết quả và tài liệu có Trước/Tiếp. Sang Ghi chú để tự nhận xét và lưu phiên. Nếu muốn dùng CSV riêng hoặc so sánh bốn model, bấm Nhập CSV trên đầu trang (địa chỉ http://127.0.0.1:4397/).\n\nCó sẵn 16 bundle seed 42, không cần train lại. Dự đoán trên CSV UNSW-NB15, chưa bắt gói mạng trực tiếp. Mẫu là 10 ID nhỏ nhất mỗi category, dùng minh họa, không lấy độ đúng của 100 dòng làm kết quả nghiên cứu. Bản trên máy Tín đã kiểm 32 trường hợp / 3.200 dự đoán. Máy khác cần tự kiểm lại môi trường.\n',encoding='utf-8')
    with (DEST/'DOC_TRUOC.txt').open('a',encoding='utf-8') as handle:
        handle.write('\nBỔ SUNG 26/10/2026: mở http://127.0.0.1:4397/lab. Trong một tab có sáu mục bằng nút: Thiết lập, Kết quả, Ghi chú, Dữ liệu, Mã xử lý, Hướng dẫn; bảng và tài liệu có Trước–Tiếp để xem gọn trong màn hình. Có tám tình huống phát lại flow, tạm dừng/tiếp tục, xem chi tiết và xuất hồ sơ phiên. Chưa có cảm biến mạng, ngăn chặn hoặc tự học thêm. Ghi chú phiên cần tự nhập và lưu trước khi đổi cấu hình.\n')
    manifest=[]
    for p in sorted(DEST.rglob('*')):
        if p.is_file() and p.name!='MANIFEST.json':manifest.append(dict(path=p.relative_to(DEST).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    (DEST/'MANIFEST.json').write_text(json.dumps(dict(created_on='2026-10-25',updated_on='2026-10-26',files=manifest),indent=2),encoding='utf-8')
    archive=DEST.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=4) as z:
        for p in sorted(DEST.rglob('*')):
            if p.is_file(): z.write(p,arcname=f'{DEST.name}/{p.relative_to(DEST).as_posix()}',compress_type=zipfile.ZIP_STORED if p.suffix=='.joblib' else zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(archive) as z:
        if z.testzip():raise ValueError('Demo ZIP corrupt')
    print(archive,round(archive.stat().st_size/1e6,2),'MB')


if __name__=='__main__':main()
