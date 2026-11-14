"""Create new complete-content copies from frozen 13/11 source ZIPs, never overwrite them."""
from pathlib import Path
from datetime import datetime,timezone
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

import pymupdf

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'docs/releases/review_final_20261113/reports'
OUT=ROOT/'output/complete_reports_20261114_build05'
RELEASE=ROOT/'docs/releases/final_handoff_20261114/reports'
PUBLIC='https://attq-nids.phttrongtin-nguyen-a46.workers.dev'
LOCKS={
    'dot4':('5a8f70dbcf77f829f0dfa82e7d62b841f35ddad307b48cab422f0e5b42d0cc68','d163bfd63b78d7cd06ccacd7450d03180a22195fe2623606b15b52890497f6df',68),
    'tong':('f503750b9766f67a617251c37a769f3515e0ab5cb1096280e0f734277180a1ef','4268e8506db1b87dc18a00e785af1ed198d59674a1fd4a3bdbba1cd0210e5445',62),
}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write_json(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def update_source(text,name,kind):
    changes=[]
    def replace(old,new):
        nonlocal text
        if old in text:
            count=text.count(old);text=text.replace(old,new)
            changes.append(dict(old=old,new=new,count=count))
    if name=='main.tex':
        replace(r'\path{docs/report_'+kind+r'_review_20261112/main.tex} & Nguồn bản nháp ngày 13/11;',
                r'\path{main.tex} & Nguồn bản hoàn chỉnh ngày 14/11 trong ZIP này;')
        replace('Bản nháp ngày 13/11/2026','Bản hoàn chỉnh nội dung ngày 14/11/2026')
        replace(' - Nháp',' - Hoàn chỉnh')
        replace(' (BẢN NHÁP)','')
        replace('Ngày cập nhật bản nháp:','Ngày hoàn chỉnh nội dung:')
        replace('17/08/2026 - 13/11/2026','17/08/2026 - 14/11/2026')
        replace(r'& 13/11/2026 \\',r'& 14/11/2026 \\')
        replace('bản nháp ngày 13/11;','hoàn chỉnh nội dung ngày 14/11;')
        replace('Chưa duyệt nộp bản này.','Chưa gửi giảng viên.')
        replace('Kiểm lại bản nháp này được lưu trong hồ sơ ngày 13/11;','Kiểm bản nền được lưu trong hồ sơ ngày 13/11;')
        replace('Bản nháp ngày 13/11 kế thừa','Bản hoàn chỉnh nội dung ngày 14/11 kế thừa')
        replace('Bản này dành cho nhóm đọc, góp ý và hoàn thiện trước khi duyệt nộp; không tự ghi nhận nghiệm thu nội dung hoặc ý kiến giảng viên.',
                'Bản hoàn chỉnh nội dung này được bàn giao để nhóm rà soát; chưa gửi giảng viên, không tự ghi nhận nghiệm thu hoặc ý kiến giảng viên.')
        replace('Bản nháp ngày 13/11 giữ kết quả','Bản hoàn chỉnh nội dung ngày 14/11 giữ kết quả')
        replace('bản nháp này chưa được nộp.','bản này chưa gửi giảng viên.')
        replace('Nguồn bản nháp ngày 13/11;','Nguồn bản kế thừa ngày 13/11;')
        replace('bản nháp này','bản hoàn chỉnh nội dung này')
    elif name=='conclusion_current.tex':
        replace('Bản nháp cập nhật ngày 13/11 từ nội dung đã có,','Bản hoàn chỉnh nội dung ngày 14/11 từ nội dung đã có,')
        replace('bản đợt 4 và bản tổng cần được đọc và duyệt riêng trước khi nộp.',
                'bản đợt 4 và tổng đã hoàn chỉnh nội dung, chưa gửi giảng viên.')
    elif name=='demo_chapter.tex':
        replace('Ngày 13/11, giao diện trình bày được triển khai tại \\url{https://nids-unsw-nb15-tlcn.nttin181.chatgpt.site}.',
                'Địa chỉ công khai hiện hành ngày 14/11 là \\href{'+PUBLIC+'}{ATTQ NIDS trên Cloudflare}.')
        replace('bản đợt 4 và tổng cần được đọc duyệt riêng.',
                'bản đợt 4 và tổng đã hoàn chỉnh nội dung, chưa gửi giảng viên.')
    return text,changes


def page_text(page):
    # Cover/version are compared separately; body normalization excludes running furniture.
    spans=[(line['bbox'][1],''.join(s['text'] for s in line['spans']))
           for block in page.get_text('dict')['blocks'] if block['type']==0 for line in block['lines']]
    return re.sub(r'\s+',' ', ' '.join(text for y,text in spans if 60<y<795)).strip()


def main():
    assert not OUT.exists(),'Refuse to overwrite prior generated work'
    assert not RELEASE.exists() or not any(RELEASE.iterdir()),'Refuse to overwrite prior complete-content release'
    RELEASE.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True)
    summary=[]
    for kind,(zip_sha,pdf_sha,expected_pages) in LOCKS.items():
        old_zip=OLD/f'Nguon_{kind}_BAN_NHAP_20261113.zip'
        old_pdf=OLD/f'NhomTLCN_{kind}_BAN_NHAP_20261113.pdf'
        assert sha(old_zip)==zip_sha and sha(old_pdf)==pdf_sha
        folder=OUT/kind;source=folder/'source';source.mkdir(parents=True)
        old_sources={};changes=[]
        with zipfile.ZipFile(old_zip) as archive:
            assert archive.testzip() is None
            original_manifest=json.loads(archive.read('SOURCE_MANIFEST.json'))
            for row in original_manifest:
                raw=archive.read(row['path']);assert hashlib.sha256(raw).hexdigest()==row['sha256']
                target=(source/row['path']).resolve();assert target.is_relative_to(source.resolve())
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);old_sources[row['path']]=raw
        for name,raw in old_sources.items():
            if name.endswith('.tex'):
                text,edits=update_source(raw.decode('utf-8'),name,kind)
                if edits:
                    (source/name).write_bytes(text.encode('utf-8'));changes.append(dict(file=name,replacements=edits))
        # Every numeric table row and every unedited source asset stays byte-identical.
        numeric_rows=0
        for name,old_raw in old_sources.items():
            new_raw=(source/name).read_bytes()
            if not any(x['file']==name for x in changes):assert old_raw==new_raw
            if name.endswith('.tex'):
                old_rows=[line.rstrip() for line in re.findall(r'^(?:CS|LR|LD|LE|Analysis|Backdoor|DoS|Exploits|Fuzzers|Generic|Reconnaissance|Shellcode|Worms) & .*$',old_raw.decode('utf-8'),re.M)]
                new_rows=[line.rstrip() for line in re.findall(r'^(?:CS|LR|LD|LE|Analysis|Backdoor|DoS|Exploits|Fuzzers|Generic|Reconnaissance|Shellcode|Worms) & .*$',new_raw.decode('utf-8'),re.M)]
                assert old_rows==new_rows,(kind,name,'numeric table changed');numeric_rows+=len(old_rows)
        build=source/'build';build.mkdir()
        for iteration in range(1,4):
            result=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=build','main.tex'],cwd=source,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            (folder/f'XELATEX_PASS_{iteration}.log').write_bytes(result.stdout)
            assert result.returncode==0,(kind,iteration,result.stdout[-1800:].decode('utf-8',errors='replace'))
            print(kind,'pass',iteration,'complete',flush=True)
        log=(build/'main.log').read_text(encoding='utf-8',errors='replace')
        blocking=re.findall(r'Overfull[^\n]*|Missing character[^\n]*|[^\n]*undefined references[^\n]*|[^\n]*Rerun to[^\n]*',log)
        assert not blocking,(kind,blocking)
        current=pymupdf.open(build/'main.pdf');previous=pymupdf.open(old_pdf)
        assert len(current)==expected_pages,(kind,len(current),expected_pages)
        links=0
        named_destinations=current.resolve_names()
        old_named_destinations=previous.resolve_names()
        assert named_destinations==old_named_destinations,(kind,'named destinations moved')
        for number,page in enumerate(current,1):
            assert '\ufffd' not in page.get_text(),(kind,number)
            assert all(current.extract_font(font[0])[3] for font in page.get_fonts() if font[0]),'unembedded font'
            for block in page.get_text('dict')['blocks']:
                if block['type']!=0:continue
                for line in block['lines']:
                    for span in line['spans']:
                        assert page.rect.contains(pymupdf.Rect(span['bbox'])),(kind,number,span['text'])
            for link in page.get_links():
                if link['kind']==pymupdf.LINK_GOTO or 'nameddest' in link:
                    assert 0<=link['page']<len(current);links+=1
                    if 'nameddest' in link:assert link['nameddest'] in named_destinations
        assert current.get_toc()==previous.get_toc(),(kind,'TOC destinations moved')
        diffs=[]
        for index,(old_page,new_page) in enumerate(zip(previous,current),1):
            old_text=page_text(old_page);new_text=page_text(new_page)
            if old_text!=new_text:
                delta=list(difflib.unified_diff(old_text.split(),new_text.split(),n=3))
                diffs.append(dict(pdf_page=index,word_diff=delta))
        # Trace exact source replacements and page changes rather than blanket-excluding whole pages.
        pdf_name=f'NhomTLCN_{kind}_20261114.pdf'
        pdf_dest=RELEASE/pdf_name;shutil.copy2(build/'main.pdf',pdf_dest)
        files=[p for p in source.rglob('*') if p.is_file() and 'build' not in p.relative_to(source).parts]
        manifest=[dict(path=p.relative_to(source).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)]
        zip_dest=RELEASE/f'Nguon_{kind}_20261114.zip'
        with zipfile.ZipFile(zip_dest,'x',zipfile.ZIP_DEFLATED) as archive:
            for p in sorted(files):archive.write(p,p.relative_to(source).as_posix())
            archive.writestr('SOURCE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        with zipfile.ZipFile(zip_dest) as archive:
            assert archive.testzip() is None
            assert all(hashlib.sha256(archive.read(row['path'])).hexdigest()==row['sha256'] for row in manifest)
        receipt=dict(kind=kind,checked_at_utc=datetime.now(timezone.utc).isoformat(),status='COMPLETE_CONTENT_NOT_SUBMITTED',group_approval=False,submitted=False,
                     input_zip_sha256=zip_sha,input_pdf_sha256=pdf_sha,old_inputs_unchanged=sha(old_zip)==zip_sha and sha(old_pdf)==pdf_sha,
                     pages=len(current),page_count_unchanged=True,toc_and_page_destinations_unchanged=True,internal_links=links,named_destinations=len(named_destinations),named_destinations_unchanged=True,
                     numeric_source_rows_unchanged=numeric_rows,source_assets_unchanged_except=changes,
                     changed_pdf_pages=[row['pdf_page'] for row in diffs],normalized_page_text_differences=diffs,
                     pdf=dict(file=pdf_name,bytes=pdf_dest.stat().st_size,sha256=sha(pdf_dest)),
                     source_zip=dict(file=zip_dest.name,bytes=zip_dest.stat().st_size,sha256=sha(zip_dest),source_files=len(manifest),crc_and_hashes_match=True),
                     compile_passes=3,compile_blocking_warnings=[],fonts_embedded=True,
                     limits=['Technical content is complete; this does not assert group approval, authorship sign-off or lecturer approval','Historic 80-run results and protocol metadata remain unchanged','No physical HDMI or new browser UI claim'])
        write_json(RELEASE/f'{kind}_COMPLETE_CHECK.json',receipt)
        summary.append({k:v for k,v in receipt.items() if k not in ('source_assets_unchanged_except','normalized_page_text_differences')})
        print(json.dumps(summary[-1],ensure_ascii=False),flush=True)
    write_json(RELEASE/'SUMMARY.json',summary)


if __name__=='__main__':main()
