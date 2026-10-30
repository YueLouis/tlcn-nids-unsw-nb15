"""Prepare traceable replay fixtures, selected before inspecting model scores."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'demo/cases'

def main():
    DEST.mkdir(parents=True,exist_ok=True)
    source=ROOT/'data/raw/UNSW_NB15_testing-set.csv'
    registry=json.loads((ROOT/'artifacts/data/data_manifest.json').read_text(encoding='utf-8'))
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    assert source_hash==registry['files']['test']['sha256'],'Frozen input differs from registry'
    raw=pd.read_csv(source,float_precision='round_trip')
    groups={cat:raw.loc[raw.attack_cat.eq(cat)].sort_values('id').head(20).copy()
            for cat in ['Normal','Generic','Reconnaissance','DoS','Exploits']}
    mixed=pd.concat([groups[cat].head(10) for cat in groups],ignore_index=True)
    specs=[
      ('normal','Lưu lượng Normal',groups['Normal'],'CS','Đo cảnh báo nhầm trên 20 bản ghi có nhãn Normal.'),
      ('known','Tấn công Generic đã biết',groups['Generic'],'CS','Quan sát phát hiện một category có trong development của closed-set.'),
      ('mixed','Normal xen các nhóm tấn công',mixed,'CS','Xem đồng thời phát hiện, báo nhầm và bỏ sót trên 50 dòng minh họa.'),
      ('heldout-r','Giấu Reconnaissance khi học',groups['Reconnaissance'],'LR','Dùng bundle LR đã loại Reconnaissance khỏi development; xem vẫn phát hiện được bao nhiêu.'),
      ('heldout-d','Giấu DoS khi học',groups['DoS'],'LD','Dùng bundle LD đã loại DoS khỏi development; chưa phải phát hiện mọi zero-day.'),
      ('heldout-e','Giấu Exploits khi học',groups['Exploits'],'LE','Dùng bundle LE đã loại Exploits khỏi development.'),
      ('unlabeled','Dữ liệu đầu vào chưa có nhãn',mixed.drop(columns=['label','attack_cat']),'CS','Chỉ xem dự đoán; không có nhãn thật để kết luận FP/FN hoặc tính độ đúng.'),
      ('invalid','CSV sai schema',mixed.head(2).drop(columns=['dur']),'CS','Minh họa từ chối file thiếu feature dur, không tạo dự đoán thay thế.')]
    rows=[]
    for case,title,frame,scenario,question in specs:
        file=DEST/(case+'.csv');frame.to_csv(file,index=False)
        rows.append(dict(id=case,title=title,filename=file.name,rows=len(frame),recommended_scenario=scenario,
            purpose=question,labels_present='label' in frame.columns,expected_schema_valid=case!='invalid',
            source_record_ids=[int(x) for x in frame.id],sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
            selection='Smallest 20 numeric IDs per declared category; mixed uses first 10 of each. Unlabeled removes labels; invalid removes dur. No selection by scores/predictions.'))
    provenance=dict(dataset='UNSW-NB15',authors='Nour Moustafa; Jill Slay',
        official_source=registry['official_source'],declared_mirror=registry['mirror_source'],
        paper_doi='https://doi.org/10.1109/MilCIS.2015.7348942',
        official_page_checked_on='2026-10-26',official_download_byte_match='NOT VERIFIED',
        acquisition_limit='Registry records an official source and a Hugging Face mirror. Exact original download route and byte identity to a newly downloaded UNSW copy have not been established.',
        source_file=source.name,source_sha256=source_hash,official_train_rows=175341,official_test_rows=82332,
        raw_columns=45,input_features=42,excluded_metadata=['id','label','attack_cat'],
        local_test_rows_matching_official_train_features=8541,
        limitation='Lab-generated network traffic, finite historical categories, imbalance and exact feature overlap. This replay is not a live attack, an independent dataset, a prevention system or online learning.')
    catalog=dict(version='application-replay-20261026',prepared_on='2026-10-26',provenance=provenance,cases=rows)
    (DEST/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(cases=len(rows),source_sha256=source_hash,input_unchanged=True),ensure_ascii=False))

if __name__=='__main__':main()
