"""Independent aggregate/denominator checks for the final frozen diagnostics."""
from pathlib import Path
from datetime import datetime,timezone
import json

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'docs/evidence/dot_03/final_diagnostics_20261025'
OUT=ROOT/'docs/evidence/dot_03/session_20261025'


def read(name):return pd.read_csv(DATA/name,float_precision='round_trip')


def main():
    groups=read('GROUP_ERRORS_ALL_RUNS.csv')
    keys=['run_id','target_fpr','dimension','evaluation_role','feature_value']
    assert not groups.duplicated(keys).any()
    assert set(groups.dimension)=={'proto','service','state'}
    assert set(groups.seed)=={42,52,62,72,82}
    assert np.array_equal(groups[['tp','fp','tn','fn']].sum(axis=1),groups.support)
    assert np.array_equal(groups.fp+groups.fn,groups.error_count)
    assert np.allclose(groups.error_rate,groups.error_count/groups.support,rtol=0,atol=1e-15)
    normal=groups[groups.evaluation_role=='normal'];attack=groups[groups.evaluation_role!='normal']
    assert (normal.tp.eq(0)&normal.fn.eq(0)).all()
    assert (attack.tn.eq(0)&attack.fp.eq(0)).all()
    aggregate=groups.groupby(['run_id','target_fpr','dimension'])[['tp','fp','tn','fn','support']].sum()
    checks=0
    for run_id in groups.run_id.unique():
        metrics=pd.read_csv(ROOT/'results/runs'/run_id/'metrics.csv',float_precision='round_trip')
        for target in (.01,.05):
            for dim in ('proto','service','state'):
                r=aggregate.loc[run_id,target,dim]
                assert r.support==82332
                for subset,name,value in [('normal','fpr',r.fp/(r.fp+r.tn)),('all','recall',r.tp/(r.tp+r.fn)),('all','precision',r.tp/(r.tp+r.fp)),('all','f1',2*r.tp/(2*r.tp+r.fp+r.fn))]:
                    expected=metrics[(metrics.subset==subset)&(metrics.metric==name)&(metrics.target_fpr==target)].value.iloc[0]
                    assert np.isclose(value,expected,rtol=0,atol=1e-12),(run_id,dim,name)
                    checks+=1
    summary=read('GROUP_ERRORS_MEAN_STD.csv')
    for r in summary.itertuples():
        p=groups[(groups.scenario==r.scenario)&(groups.model==r.model)&(groups.target_fpr==r.target_fpr)&(groups.evaluation_role==r.evaluation_role)&(groups.dimension==r.dimension)&(groups.feature_value==r.feature_value)]
        assert p.seed.nunique()==r.seed_count==5
        assert p.support.min()==r.support_min==r.support_max
        assert np.isclose(p.error_rate.mean(),r.error_rate_mean,rtol=0,atol=1e-12)
        assert np.isclose(p.error_rate.std(ddof=1),r.error_rate_std,rtol=0,atol=1e-12)
    stability=read('ERROR_STABILITY.csv')
    for key,p in stability.groupby(['scenario','model','target_fpr','evaluation_role']):
        assert set(p.error_seed_count)==set(range(6))
        assert p.role_support.nunique()==1 and p.record_count.sum()==p.role_support.iloc[0]
        scenario,model,target,role=key
        errors=groups[(groups.scenario==scenario)&(groups.model==model)&(groups.target_fpr==target)&(groups.evaluation_role==role)&(groups.dimension=='proto')].error_count.sum()
        assert (p.error_seed_count*p.record_count).sum()==errors
    pairs=read('MODEL_DISAGREEMENT_S42.csv')
    for r in pairs.itertuples():
        counts=[]
        for model in (r.model_a,r.model_b):
            p=groups[(groups.scenario==r.scenario)&(groups.model==model)&(groups.seed==42)&(groups.target_fpr==r.target_fpr)&(groups.dimension=='proto')]
            counts.append(int(p.error_count.sum()))
        assert sum(counts)-2*r.both_wrong==r.different_prediction_count
        assert sum(counts)-r.both_wrong==r.either_wrong
        assert np.isclose(r.both_wrong/r.either_wrong,r.error_jaccard,atol=1e-15,rtol=0)
    raw=pd.read_csv(ROOT/'data/raw/UNSW_NB15_testing-set.csv',low_memory=False).set_index('id')
    near=read('NEAR_THRESHOLD_EXAMPLES_S42.csv')
    for run_id,p in near.groupby('run_id'):
        pred=pd.read_csv(ROOT/'results/runs'/run_id/'predictions.csv',float_precision='round_trip').set_index(['target_fpr','record_id'])
        for r in p.itertuples():
            record=raw.loc[r.record_id];reference=pred.loc[r.target_fpr,r.record_id]
            for name in ('proto','service','state','dur','sttl','dbytes'):
                observed=getattr(r,name)
                if isinstance(observed,(float,np.floating)):assert np.isclose(observed,record[name],rtol=0,atol=1e-12)
                else:assert observed==record[name]
            assert r.y_pred==reference.y_pred and r.y_true==record.label
            assert r.score==reference.score and r.threshold==reference.threshold
            assert np.isclose(abs(r.score-r.threshold),r.abs_margin,rtol=0,atol=1e-15)
        for (target,role),q in p.groupby(['target_fpr','evaluation_role']):
            reference=pred.xs(target).query('evaluation_role == @role').reset_index()
            reference['margin']=(reference.score-reference.threshold).abs()
            expected=reference.sort_values(['margin','record_id']).head(3).record_id.to_list()
            assert q.record_id.to_list()==expected
    costs=read('RUNTIME_SIZE_ALL_RUNS.csv')
    assert len(costs)==80 and costs.run_id.nunique()==80
    assert costs.historical_train_only_seconds.isna().all()
    for r in costs.itertuples():
        folder=ROOT/'results/runs'/r.run_id
        meta=json.loads((folder/'run.json').read_text(encoding='utf-8'))
        assert r.bundle_bytes==(folder/'model_bundle.joblib').stat().st_size
        assert r.historical_total_run_seconds==meta['duration_seconds']
        assert r.warmup==1 and r.repeats==3 and r.current_inference_100_rows_seconds>0
        assert r.score_max_abs_diff<=1e-6
    result=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),group_rows=len(groups),group_summaries=len(summary),
        source_metric_partition_checks=checks,role_denominators=True,stability_rows=len(stability),stability_error_totals=True,
        model_pairs=len(pairs),pair_error_identities=True,near_threshold_rows=len(near),near_threshold_raw_prediction_and_selection=True,
        runtime_runs=80,historical_train_only_missing_preserved=True,bundle_sizes_and_old_total_times=True)
    (OUT/'FINAL_DIAGNOSTIC_TABLE_CHECK.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
