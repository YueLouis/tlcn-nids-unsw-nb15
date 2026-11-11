"""Package and independently rebuild the dated round-three progress report."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import zipfile
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'docs/report_dot3_submission_20261111'
EVIDENCE=ROOT/'docs/evidence/dot_03/submission_20261111'
OUT=ROOT/'docs/releases/submission_dot3_20261111'
REBUILD=ROOT/'output/dot3_submission_source_rebuild_20261111'
PDF='NhomTLCN_TramAnh_VuongThu_TrongTin_dot3_20261111.pdf'
ZIP='Nguon_Bao_cao_dot3_20261111.zip'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    tech=json.loads((EVIDENCE/'DELIVERY_TECHNICAL_CHECK.json').read_text(encoding='utf-8'))
    tables=json.loads((EVIDENCE/'REPORT_TABLE_CHECK.json').read_text(encoding='utf-8'))
    pdf=SRC/'build_submission/main.pdf'
    assert sha(pdf)==tech['pdf_sha256']
    assert tables['table_rows_checked']==174
    shutil.copy2(pdf,OUT/PDF)
    files=[p for p in SRC.rglob('*') if p.is_file() and not any(x.startswith('build') for x in p.relative_to(SRC).parts)]
    manifest=[{'path':p.relative_to(SRC).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in files]
    with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.relative_to(SRC).as_posix())
        z.writestr('SOURCE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
        z.writestr('BIEN_DICH.txt','Main: main.tex\nXeLaTeX, three passes.\nFonts: Times New Roman, Arial, Consolas.\nProgress report; individual reading and review remain separate.\n')
    if REBUILD.exists():raise FileExistsError(REBUILD)
    REBUILD.mkdir(parents=True)
    with zipfile.ZipFile(OUT/ZIP) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(set(z.namelist()))
        z.extractall(REBUILD)
    for e in manifest:assert sha(REBUILD/e['path'])==e['sha256']
    for i in range(1,4):
        r=subprocess.run([r'C:\Program Files\MiKTeX\miktex\bin\x64\xelatex.exe','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=REBUILD,capture_output=True)
        (REBUILD/f'pass_{i}.txt').write_bytes(r.stdout+r.stderr)
        assert r.returncode==0,r.stdout[-3000:]
    before=pymupdf.open(pdf);after=pymupdf.open(REBUILD/'main.pdf')
    assert len(before)==len(after)==62
    assert [p.get_text() for p in before]==[p.get_text() for p in after]
    equal=[a.get_pixmap(dpi=96).samples==b.get_pixmap(dpi=96).samples for a,b in zip(before,after)]
    assert all(equal),equal
    log=(REBUILD/'main.log').read_text(encoding='utf-8',errors='replace')
    assert not any(x in log for x in ['Overfull \\hbox','Missing character:','undefined references','Rerun to get'])
    result={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'source_entries':len(files),'zip_crc_ok':True,'source_hashes_match':True,'rebuild_passes':3,'pages':62,'text_equal_all_pages':True,'raster_equal_pages_at_96_dpi':sum(equal),'binary_equal':sha(pdf)==sha(REBUILD/'main.pdf'),'original_pdf_sha256':sha(pdf),'rebuilt_pdf_sha256':sha(REBUILD/'main.pdf')}
    (EVIDENCE/'SOURCE_REBUILD.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    for n in ['DELIVERY_TECHNICAL_CHECK.json','REPORT_TABLE_CHECK.json','SOURCE_REBUILD.json']:
        shutil.copy2(EVIDENCE/n,OUT/n)
    (OUT/'README.md').write_text(f'''# Báo cáo tiến độ đợt 3 — bản ngày 11/11/2026

[Mở báo cáo PDF 62 trang]({PDF}) · [Nguồn XeLaTeX]({ZIP})

Bản này cập nhật cách trình bày và hồ sơ bàn giao, giữ kết quả thực nghiệm chốt 30/10: 80 lượt chạy, bốn mô hình, CS và ba LOACO, năm seed. Không có lượt huấn luyện mới hoặc chỉnh ngưỡng theo test. Bản đọc duyệt ngày 10/11 được giữ riêng trong lịch sử.

Kiểm ngày 11/11: 46 unit test đạt, validator đủ 80 tổ hợp, 174 dòng bảng khớp nguồn; 200 liên kết nội bộ và 56 bookmark có đích hợp lệ. Nguồn đã giải nén sang thư mục mới và biên dịch ba lượt; cả 62 trang trùng văn bản và raster với PDF bàn giao. Các bằng chứng kỹ thuật kèm theo không thay việc đọc chéo, nhận xét hoặc xác nhận đóng góp của thành viên.

PDF SHA-256: `{sha(OUT/PDF)}`

`main` lưu báo cáo tổng hợp; [hồ sơ ba phần phụ trách](../../group_delivery_20261110/README.md) liên kết các nhánh thành viên. Raw, model và prediction nặng giữ trên Drive dùng chung. Trạng thái gửi thư và biên nhận được ghi riêng sau khi gửi; phát hành tài liệu không tự xác nhận thư đã gửi hoặc giảng viên đã duyệt.
''',encoding='utf-8')
    release={'prepared_at_utc':datetime.now(timezone.utc).isoformat(),'status':'TECHNICALLY_CHECKED_PROGRESS_REPORT','group_leader_authorized_email':True,'full_member_review_verified':False,'email_status':'NOT_SENT_IN_THIS_PACKAGING_STEP','pdf_pages':62,'files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='MANIFEST.json']}
    (OUT/'MANIFEST.json').write_text(json.dumps(release,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
