"""Describe RF impurity/XGB gain importance without retraining or causal claims."""
from pathlib import Path
import hashlib
import json
import tempfile
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def raw_importance(bundle):
    pre=bundle['preprocessor']
    importance=np.asarray(bundle['fitted_model'].estimator.feature_importances_,dtype=float)
    rows=[]
    numeric=list(pre.transformers_[0][2])
    categories=list(pre.transformers_[1][2])
    encoder=pre.named_transformers_['categorical'].named_steps['onehot']
    mapping=numeric+[col for col,values in zip(categories,encoder.categories_) for _ in values]
    if len(mapping)!=len(importance) or not np.isfinite(importance).all() or (importance<0).any():
        raise ValueError('Encoded importance does not match fitted feature schema')
    grouped=pd.DataFrame({'feature':mapping,'importance':importance}).groupby('feature').importance.sum()
    if set(grouped.index)!=set(bundle['features']) or not np.isclose(grouped.sum(),1,atol=1e-5):
        raise ValueError('Raw feature importance coverage/normalization mismatch')
    return grouped


def run():
    output=ROOT/'docs/evidence/dot_03/features_20261025'
    if output.exists(): raise ValueError('Use a fresh output directory')
    rows=[]; inputs=[]
    for scenario in ('CS','LR','LD','LE'):
        for model in ('RF','XGB'):
            for seed in (42,52,62,72,82):
                rid=f'{scenario}-{model}-S{seed}'
                path=ROOT/'results/runs'/rid/'model_bundle.joblib'
                before=hashlib.sha256(path.read_bytes()).hexdigest()
                bundle=joblib.load(path)
                values=raw_importance(bundle)
                for feature,value in values.items():
                    rows.append(dict(run_id=rid,scenario=scenario,model=model,seed=seed,feature=feature,importance=value,
                        method='mean_decrease_impurity' if model=='RF' else 'normalized_gain'))
                if hashlib.sha256(path.read_bytes()).hexdigest()!=before: raise ValueError('Bundle changed')
                inputs.append(dict(path=str(path.relative_to(ROOT)),sha256=before))
            print(f'Feature importance: {scenario}/{model}',flush=True)
    data=pd.DataFrame(rows)
    summary=data.groupby(['scenario','model','method','feature'],as_index=False).agg(
        importance_mean=('importance','mean'),importance_std=('importance','std'),seeds=('seed','nunique'))
    if len(data)!=1680 or len(summary)!=336 or not summary.seeds.eq(5).all(): raise ValueError('Incomplete matrix')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent,prefix='.features_') as tmp:
        staging=Path(tmp)/'bundle';staging.mkdir()
        data.to_csv(staging/'FEATURE_IMPORTANCE_ALL_RUNS.csv',index=False)
        summary.to_csv(staging/'FEATURE_IMPORTANCE_MEAN_STD.csv',index=False)
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        for scenario in ('CS','LR'):
            fig,axes=plt.subplots(1,2,figsize=(10,5),layout='constrained')
            for ax,model in zip(axes,('RF','XGB')):
                part=summary.query('scenario == @scenario and model == @model').nlargest(10,'importance_mean').sort_values('importance_mean')
                ax.barh(part.feature,part.importance_mean,xerr=part.importance_std,color='#386A52' if model=='RF' else '#37657B',capsize=2)
                ax.set_title(f'{scenario}: {model}'); ax.set_xlabel('Normalized model importance'); ax.grid(axis='x',alpha=.15)
            fig.suptitle('Raw feature groups; mean/sample std across five seeds\nRF: impurity decrease; XGB: gain; descriptive, not causal',fontsize=12)
            fig.savefig(staging/f'FEATURES_{scenario}.png',dpi=160);plt.close(fig)
        audit=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),run_count=40,rows=1680,groups=336,
            inputs_unchanged=True,training_performed=False,threshold_tuning_performed=False,inputs=inputs,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            limitations='Built-in training importance, not held-out permutation importance or per-record causal explanation; categorical columns sum one-hot contributions and may have cardinality bias')
        (staging/'FEATURE_IMPORTANCE_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
        staging.rename(output)
    return audit


if __name__=='__main__':
    result=run();print(json.dumps({k:v for k,v in result.items() if k!='inputs'},indent=2))
