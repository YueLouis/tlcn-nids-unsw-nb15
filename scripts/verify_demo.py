"""Check real inference from all seed-42 bundles against frozen test predictions."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from io import StringIO

import numpy as np
import pandas as pd
from nids_benchmark.demo import load_bundle,predict_frame,compare_csv

ROOT=Path(__file__).resolve().parents[1]


def run():
    output=ROOT/'docs/evidence/dot_04/demo_20261025'
    output.mkdir(parents=True,exist_ok=True)
    raw=ROOT/'data/raw/UNSW_NB15_testing-set.csv'
    raw_hash=hashlib.sha256(raw.read_bytes()).hexdigest()
    test=pd.read_csv(raw,low_memory=False)
    # Ten smallest IDs per category, specified before model inference; not representative.
    sample=test.sort_values('id').groupby('attack_cat',sort=True).head(10).sort_values('id')
    sample_path=ROOT/'demo/sample.csv';sample.to_csv(sample_path,index=False)
    frame=pd.read_csv(sample_path,low_memory=False)
    cases=[];sources=[]
    for scenario in ('CS','LR','LD','LE'):
        for model in ('RF','XGB','IF','AE'):
            rid=f'{scenario}-{model}-S42';folder=ROOT/'results/runs'/rid
            inputs=[folder/'model_bundle.joblib',folder/'predictions.csv']
            before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
            expected=pd.read_csv(folder/'predictions.csv',float_precision='round_trip')
            bundle=load_bundle(scenario,model)
            for target in (.01,.05):
                result=predict_frame(bundle,frame,target)
                actual=pd.DataFrame(result['results'])
                actual['record_id']=actual.record_id.astype(int)
                reference=expected.loc[expected.target_fpr.eq(target)&expected.record_id.isin(frame.id)].sort_values('record_id')
                actual=actual.sort_values('record_id')
                difference=float(np.max(np.abs(actual.score.to_numpy()-reference.score.to_numpy())))
                if not np.array_equal(actual.record_id,reference.record_id) or not np.array_equal(actual.prediction.eq('Attack').astype(int),reference.y_pred):
                    raise ValueError(f'Prediction mismatch: {rid}/{target}')
                if difference>1e-6: raise ValueError(f'Score mismatch: {rid}/{difference}')
                if not np.array_equal(actual.threshold,reference.threshold): raise ValueError('Threshold changed')
                outcomes=actual.outcome.value_counts().to_dict()
                cases.append(dict(run_id=rid,target_fpr=target,rows=len(frame),max_abs_score_diff=difference,**outcomes))
                actual.to_csv(output/f'{rid}_T{int(target*100):02d}.csv',index=False)
            for p,before_hash in before.items():
                if hashlib.sha256(p.read_bytes()).hexdigest()!=before_hash: raise ValueError('Source changed')
                sources.append(dict(path=str(p.relative_to(ROOT)),sha256=before_hash))
            print(f'Demo verified: {rid}, both thresholds',flush=True)
    bundle=load_bundle('CS','RF')
    comparison=compare_csv('CS',.05,frame.to_csv(index=False))
    if [x['model'] for x in comparison['comparisons']] != ['RF','XGB','IF','AE']:
        raise ValueError('Comparison did not cover all four models')
    if any(x['rows'] != len(frame) or 'explanation' not in predict_frame(load_bundle('CS',x['model']),frame,.05) for x in comparison['comparisons']):
        raise ValueError('Comparison/explanation output incomplete')
    invalid=[]
    for name,bad in [('missing_feature',frame.drop(columns=['dur'])),('empty_csv',frame.iloc[:0]),
                     ('nonnumeric',frame.assign(dur='abc')),('infinite',frame.assign(dur=np.inf))]:
        try: predict_frame(bundle,bad,.05)
        except ValueError: invalid.append(name)
        else: raise ValueError(f'Invalid case accepted: {name}')
    pd.DataFrame(cases).to_csv(output/'DEMO_CASES.csv',index=False)
    if hashlib.sha256(raw.read_bytes()).hexdigest()!=raw_hash: raise ValueError('Raw test changed')
    audit=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),bundle_count=16,operating_cases=32,
        rows_per_case=len(frame),prediction_comparisons=32*len(frame),invalid_cases_rejected=invalid,
        comparison_models=['RF','XGB','IF','AE'],comparison_rows=len(frame),feature_explanation_checked=True,
        inputs_unchanged=True,training_performed=False,threshold_tuning_performed=False,
        sample_policy='Ten smallest official-test IDs per each of ten categories; declared before inference; illustration only, not a performance sample',
        sample_sha256=hashlib.sha256(sample_path.read_bytes()).hexdigest(),sources=sources,
        max_abs_score_diff=max(c['max_abs_score_diff'] for c in cases),score_tolerance=1e-6)
    (output/'DEMO_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    return audit


if __name__=='__main__':
    audit=run();print(json.dumps({k:v for k,v in audit.items() if k!='sources'},indent=2))
