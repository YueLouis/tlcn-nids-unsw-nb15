"""Check each replay fixture against raw data and frozen prediction artifacts."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from nids_benchmark.application import catalog,load_case,run_case

def main():
    out=ROOT/'docs/evidence/dot_04/application_20261026';out.mkdir(parents=True,exist_ok=True)
    cat=catalog();raw_path=ROOT/'data/raw/UNSW_NB15_testing-set.csv';raw=pd.read_csv(raw_path,float_precision='round_trip').set_index('id')
    assert hashlib.sha256(raw_path.read_bytes()).hexdigest()==cat['provenance']['source_sha256']
    checks=[];counts=0;max_diff=0;max_relative_diff=0;invalid=0;fixture_rows=0
    for c in cat['cases']:
        _,text=load_case(c['id']);frame=pd.read_csv(ROOT/'demo/cases'/c['filename'],float_precision='round_trip').set_index('id')
        expected=raw.loc[c['source_record_ids'],frame.columns]
        pd.testing.assert_frame_equal(frame,expected,check_exact=True)
        fixture_rows+=len(frame)
        for model in ['RF','XGB','IF','AE']:
            for target in [.01,.05]:
                if not c['expected_schema_valid']:
                    try:run_case(c['id'],c['recommended_scenario'],model,target)
                    except ValueError as exc:assert 'dur' in str(exc);invalid+=1
                    else:raise AssertionError('Invalid schema accepted')
                    continue
                result=run_case(c['id'],c['recommended_scenario'],model,target)
                rid=result['prediction']['run_id'];pred=result['prediction']['results']
                reference=pd.read_csv(ROOT/'results/runs'/rid/'predictions.csv',float_precision='round_trip')
                match=reference[np.isclose(reference.target_fpr,target)].set_index('record_id').loc[[int(row['record_id']) for row in pred]]
                score=np.array([r['score'] for r in pred]);baseline=match['score'].to_numpy();difference=float(np.abs(score-baseline).max());max_diff=max(max_diff,difference)
                relative=float((np.abs(score-baseline)/np.maximum(np.abs(baseline),1e-12)).max());max_relative_diff=max(max_relative_diff,relative)
                # Float32 AE matrix multiplication depends on inference batch size.
                # Some raw feature outliers yield very large MSE: use explicit
                # relative + absolute bounds, and still require identical labels.
                assert np.allclose(score,baseline,atol=1e-6,rtol=1e-6),(c['id'],model,difference,relative)
                assert [int(r['prediction']=='Attack') for r in pred]==match.y_pred.tolist()
                assert np.allclose([r['threshold'] for r in pred],match.threshold,atol=0,rtol=0)
                if not c['labels_present']:
                    assert all('truth' not in r and 'outcome' not in r and 'attack_cat' not in r for r in pred)
                    assert result['summary']['labeled_rows']==0 and result['summary']['fpr'] is None and result['summary']['recall'] is None
                s=result['summary'];conf=s['confusion']
                if s['normal_support']:assert s['fpr']==conf['FP']/s['normal_support']
                if s['attack_support']:assert s['recall']==conf['TP']/s['attack_support']
                counts+=len(pred);checks.append(dict(case=c['id'],model=model,scenario=c['recommended_scenario'],target_fpr=target,rows=len(pred),max_abs_score_diff=difference,max_relative_score_diff=relative,summary=s))
                (out/f'{c["id"]}_{model}_T{int(target*100):02d}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    audit=dict(checked_on='2026-10-26',cases=len(cat['cases']),fixture_rows_checked=fixture_rows,fixture_values_match_raw=True,
        successful_cases=len(checks),predictions_checked=counts,invalid_schema_rejections=invalid,max_abs_score_diff=max_diff,max_relative_score_diff=max_relative_diff,atol=1e-6,rtol=1e-6,
        numerical_limit='Float32 AE scores can differ with batch size, especially large reconstruction MSE; labels must match exactly and scores satisfy abs_diff <= atol + rtol*abs(reference). This is a different expanded-sample check from the earlier absolute-only 100-row demo audit.',
        no_training_or_threshold_selection=True,scope='Replay subsets of existing official test; not independent test data or live traffic',checks=checks)
    (out/'APPLICATION_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in audit.items() if k!='checks'},ensure_ascii=False))
if __name__=='__main__':main()
