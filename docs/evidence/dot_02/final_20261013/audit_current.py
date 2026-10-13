from pathlib import Path
import json, hashlib, sys
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'configs/experiment_matrix.yaml').exists())
OUT = Path(__file__).resolve().parent
raw = pd.read_csv(ROOT / 'data/raw/UNSW_NB15_testing-set.csv')
failures = []
all_metrics = []
metadata = []

def check(condition, message):
    if not condition:
        failures.append(message)

def equal(a, b):
    return bool((pd.isna(a) and pd.isna(b)) or np.isclose(a, b, rtol=1e-10, atol=1e-12, equal_nan=True))

for i, run in enumerate(sorted((ROOT/'results/runs').iterdir())):
    if not run.is_dir() or run.name[:2] not in {'CS','LR','LD','LE'}:
        continue
    spec = json.loads((run/'run.json').read_text(encoding='utf-8'))
    metadata.append(spec)
    pred = pd.read_csv(run/'predictions.csv', float_precision='round_trip')
    metrics = pd.read_csv(run/'metrics.csv', float_precision='round_trip')
    all_metrics.append(metrics)
    check(len(pred) == 164664, f'{run.name}: prediction row count')
    roles = np.where(raw.label.eq(0), 'normal', np.where(raw.attack_cat.eq(spec['heldout_class']), 'heldout_attack', 'known_attack'))
    values = {}
    for sel in spec['threshold_policy']['selections']:
        target = sel['target_fpr']
        p = pred.loc[pred.target_fpr.eq(target)]
        check(len(p) == len(raw), f'{run.name}: target support {target}')
        check(np.array_equal(p.record_id.to_numpy(), raw.id.to_numpy()), f'{run.name}: record IDs')
        check(np.array_equal(p.y_true.to_numpy(), raw.label.to_numpy()), f'{run.name}: true labels')
        check(np.array_equal(p.attack_cat.to_numpy(), raw.attack_cat.to_numpy()), f'{run.name}: categories')
        check(np.array_equal(p.evaluation_role.to_numpy(), roles), f'{run.name}: roles')
        check(p.run_id.eq(run.name).all() and p.split.eq('official_test').all(), f'{run.name}: identifiers')
        check(np.isfinite(p.score).all(), f'{run.name}: scores finite')
        check(np.allclose(p.threshold, sel['threshold'], rtol=0, atol=1e-12), f'{run.name}: thresholds')
        y = raw.label.to_numpy(); yhat = (p.score.to_numpy() >= sel['threshold']).astype(int)
        check(np.array_equal(yhat, p.y_pred.to_numpy()), f'{run.name}: threshold predictions')
        tp=int(((y==1)&(yhat==1)).sum()); fp=int(((y==0)&(yhat==1)).sum())
        fn=int(((y==1)&(yhat==0)).sum()); tn=int(((y==0)&(yhat==0)).sum())
        values[('all','precision',target)] = (tp/(tp+fp) if tp+fp else 0.,len(y))
        values[('all','recall',target)] = (tp/(tp+fn),len(y))
        values[('all','f1',target)] = (2*tp/(2*tp+fp+fn),len(y))
        for subset,metric in [('normal','fpr'),('known_attack','recall'),('heldout_attack','uadr')]:
            mask=roles==subset; support=int(mask.sum())
            values[(subset,metric,target)] = (float(yhat[mask].mean()) if support else np.nan,support)
        if target == .01:
            values[('all','pr_auc',None)] = (float(average_precision_score(y,p.score)),len(y))
            baseline_scores = p.score.to_numpy()
        else:
            check(np.array_equal(baseline_scores,p.score.to_numpy()),f'{run.name}: score consistency across targets')
    check(len(metrics)==13,f'{run.name}: metric row count')
    for row in metrics.itertuples():
        key = (row.subset,row.metric,None if pd.isna(row.target_fpr) else row.target_fpr)
        value,support = values[key]
        check(equal(row.value,value),f'{run.name}: {key} metric')
        check(row.support==support,f'{run.name}: {key} support')
    if len(metadata)%10 == 0:
        print(f'Audited {len(metadata)}/80 runs; failures={len(failures)}',flush=True)

metrics=pd.concat(all_metrics,ignore_index=True)
selected=metrics.loc[metrics.target_fpr.eq(.05)].copy()
selected['metric_key']=selected.subset+':'+selected.metric
wide=selected.pivot(index='run_id',columns='metric_key',values='value').reset_index()
ap=metrics.loc[metrics.metric.eq('pr_auc'),['run_id','value']].rename(columns={'value':'pr_auc'})
meta=pd.DataFrame([{'run_id':m['run_id'],'scenario':m['scenario'],'model':m['model']} for m in metadata])
recomputed=meta.merge(wide,on='run_id').merge(ap,on='run_id')
stored=pd.read_csv(ROOT/'docs/reports/DOT_02_METRICS_ALL_RUNS.csv')
metric_columns=['pr_auc','all:f1','all:precision','all:recall','normal:fpr','known_attack:recall','heldout_attack:uadr']
for rid in recomputed.run_id:
    for c in metric_columns:
        a=recomputed.set_index('run_id').loc[rid,c]; b=stored.set_index('run_id').loc[rid,c]
        check(equal(a,b),f'{rid}: summary {c}')
agg=pd.read_csv(ROOT/'docs/reports/DOT_02_METRICS_MEAN_STD.csv').set_index(['scenario','model'])
for key,g in recomputed.groupby(['scenario','model']):
    for c in ['pr_auc','all:f1','normal:fpr','known_attack:recall','heldout_attack:uadr']:
        for stat in ['mean','std']:
            a=getattr(g[c],stat)(); b=agg.loc[key,c+'_'+stat]
            check(equal(a,b),f'{key}: aggregate {c} {stat}')
raw_hashes={}
manifest=json.loads((ROOT/'artifacts/data/data_manifest.json').read_text(encoding='utf-8'))
for split,entry in manifest['files'].items():
    p=ROOT/'data/raw'/entry['filename']
    raw_hashes[split]=hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256']
    check(raw_hashes[split],f'raw SHA-256 {split}')
result={'checked_on':'2026-10-13','runs_checked':len(metadata),'prediction_rows_checked':len(metadata)*164664,'metric_rows_checked':len(metrics),'summary_rows_checked':len(stored),'aggregate_groups_checked':len(agg),'raw_sha256_matches':raw_hashes,'failure_count':len(failures),'failures':failures}
(OUT/'numerical_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False),flush=True)
sys.exit(bool(failures))
