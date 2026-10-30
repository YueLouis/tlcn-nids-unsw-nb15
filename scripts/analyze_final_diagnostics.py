"""Complete planned frozen-result slices, figures, stability and cost evidence."""
from pathlib import Path
from time import perf_counter
import hashlib
import json
import os
import platform
import sys

import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score

from analyze_pr_scores import unique_scores, verify_saved_metrics, sha256
from analyze_overlap_slices import align_predictions

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/dot_03/final_diagnostics_20261025'
MODELS=('RF','XGB','IF','AE')
SCENARIOS={'CS':None,'LR':'Reconnaissance','LD':'DoS','LE':'Exploits'}
SEEDS=(42,52,62,72,82)
COLORS=dict(RF='#356a50',XGB='#327896',IF='#b26c47',AE='#806399')


def grouped_errors(frame, dimension):
    rows=[]
    for (role,value),g in frame.groupby(['evaluation_role',dimension],sort=True):
        y=g.y_true.to_numpy(); p=g.y_pred.to_numpy()
        counts=dict(tp=int(((y==1)&(p==1)).sum()),fp=int(((y==0)&(p==1)).sum()),
            tn=int(((y==0)&(p==0)).sum()),fn=int(((y==1)&(p==0)).sum()))
        rows.append(dict(dimension=dimension,feature_value=str(value),evaluation_role=role,support=len(g),
            error_count=counts['fp']+counts['fn'],error_rate=(counts['fp']+counts['fn'])/len(g),**counts))
    return rows


def save(fig,name):
    fig.savefig(OUT/name,dpi=155,bbox_inches='tight');plt.close(fig)


def plots(points,category,group_summary,confusions):
    fig,axes=plt.subplots(1,2,figsize=(12,4.2),layout='constrained',sharey=True)
    for ax,target in zip(axes,(.01,.05)):
        x=np.arange(3)
        for j,model in enumerate(MODELS):
            p=points[(points.model==model)&(points.target_fpr==target)].set_index('scenario').loc[['LR','LD','LE']]
            ax.bar(x+(j-1.5)*.18,100*p.uadr_mean,width=.18,yerr=100*p.uadr_std,capsize=2,label=model,color=COLORS[model])
        ax.set_xticks(x,['Reconnaissance','DoS','Exploits']);ax.set_ylim(0,106);ax.set_title(f'Validation target {target:.0%}');ax.set_ylabel('UADR (%)');ax.grid(axis='y',alpha=.15)
    axes[1].legend(ncol=4,loc='upper center',bbox_to_anchor=(.5,-.12))
    fig.suptitle('Held-out class simulation; mean / sample std across five seeds on the same test')
    save(fig,'UADR_BOTH_TARGETS.png')
    for metric,title,scenarios in [('known_recall','Known Attack Recall',list(SCENARIOS)),('uadr','Held-out recall / UADR',['LR','LD','LE'])]:
        fig,axes=plt.subplots(1,len(scenarios),figsize=(4*len(scenarios),4),layout='constrained',sharey=True)
        for ax,scenario in zip(np.atleast_1d(axes),scenarios):
            for model in MODELS:
                p=points[(points.scenario==scenario)&(points.model==model)].sort_values('target_fpr')
                ax.errorbar(100*p.fpr_mean,100*p[metric+'_mean'],xerr=100*p.fpr_std,yerr=100*p[metric+'_std'],fmt='o-',capsize=2,color=COLORS[model],label=model)
                for r in p.itertuples():ax.annotate(f'{int(r.target_fpr*100)}%',(100*r.fpr_mean,100*getattr(r,metric+'_mean')),fontsize=7,xytext=(2,3),textcoords='offset points')
            ax.set_title(scenario);ax.set_xlabel('Observed test FPR (%)');ax.set_ylim(0,105);ax.set_xlim(0,25);ax.grid(alpha=.15)
        np.atleast_1d(axes)[0].set_ylabel(title+' (%)');np.atleast_1d(axes)[-1].legend(fontsize=8)
        fig.suptitle('Validation targets 1% / 5%; mean and sample std, n=5 seeds; same official test')
        save(fig,'TRADEOFF_'+metric.upper()+'.png')
    fig,axes=plt.subplots(4,4,figsize=(10,9),layout='constrained')
    for i,scenario in enumerate(SCENARIOS):
        for j,model in enumerate(MODELS):
            tn,fp,fn,tp=confusions[(scenario,model)]
            a=np.array([[tn,fp],[fn,tp]])
            ax=axes[i,j];ax.imshow(a,cmap='Greens',vmin=0,vmax=45332)
            for (r,c),v in np.ndenumerate(a):ax.text(c,r,f'{v:,}',ha='center',va='center',fontsize=9,color='white' if v>25000 else '#203126')
            ax.set_xticks([0,1],['Normal','Attack'],fontsize=8);ax.set_yticks([0,1],['Normal','Attack'],fontsize=8);ax.set_title(f'{scenario} / {model}',fontsize=10)
    fig.suptitle('Confusion matrices; seed42, validation target5%; rows=true, columns=prediction; each test n=82,332')
    save(fig,'CONFUSION_ALL_SCENARIOS_S42.png')
    fig,axes=plt.subplots(2,2,figsize=(10,9),layout='constrained')
    for ax,scenario in zip(axes.flat,SCENARIOS):
        part=category[(category.scenario==scenario)&(category.target_fpr==.05)&(category.attack_cat!='Normal')]
        a=part.pivot(index='attack_cat',columns='model',values='error_rate_mean').reindex(columns=MODELS)
        im=ax.imshow(100*(1-a),cmap='YlGnBu',vmin=0,vmax=100,aspect='auto')
        for (r,c),v in np.ndenumerate(a.to_numpy()):ax.text(c,r,f'{100*(1-v):.1f}',ha='center',va='center',fontsize=8,color='white' if 1-v>.7 else '#203126')
        ax.set_xticks(range(4),MODELS);ax.set_yticks(range(len(a)),a.index,fontsize=8);ax.set_title(scenario)
    fig.colorbar(im,ax=axes.ravel().tolist(),label='Detection rate (%)',shrink=.8)
    fig.suptitle('Per-category mean detection, validation target5%, n=5 seeds; category support in CSV')
    save(fig,'CATEGORY_DETECTION_HEATMAP.png')
    all_points=pd.read_csv(ROOT/'docs/evidence/dot_03/pr_scores_20261022/OPERATING_POINTS_ALL_RUNS.csv',float_precision='round_trip')
    fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
    for ax,scenario in zip(axes.flat,SCENARIOS):
        metric='recall' if scenario=='CS' else 'uadr'
        for model in MODELS:
            part=all_points[(all_points.scenario==scenario)&(all_points.model==model)&(all_points.target_fpr==.05)].sort_values('seed')
            ax.plot(part.seed,100*part[metric],'o-',color=COLORS[model],label=model)
        ax.set_title(scenario+' / '+metric);ax.set_xticks(SEEDS);ax.set_ylim(0,105);ax.set_ylabel('Recall (%)');ax.grid(alpha=.15)
    axes[0,0].legend(ncol=4,fontsize=8)
    fig.suptitle('Metric stability across five seeds; same official test, target validation5%')
    save(fig,'SEED_STABILITY.png')
    for scenario,role,name in [('CS','normal','FP_GROUPS_CS'),('LR','heldout_attack','FN_GROUPS_LR')]:
        fig,axes=plt.subplots(3,2,figsize=(11,10),layout='constrained')
        for i,dimension in enumerate(('proto','service','state')):
            for j,model in enumerate(('RF','IF')):
                part=group_summary[(group_summary.scenario==scenario)&(group_summary.model==model)&(group_summary.target_fpr==.05)&(group_summary.evaluation_role==role)&(group_summary.dimension==dimension)&(group_summary.support_min>=100)].nlargest(6,'error_rate_mean').sort_values('error_rate_mean')
                ax=axes[i,j];ax.barh(part.feature_value,100*part.error_rate_mean,xerr=100*part.error_rate_std,color=COLORS[model],capsize=2)
                for k,r in enumerate(part.itertuples()):ax.text(min(100*r.error_rate_mean+2,85),k,f'n={int(r.support_min):,}',va='center',fontsize=8)
                ax.set_xlim(0,110);ax.set_title(f'{scenario} / {model} / {dimension}');ax.set_xlabel('Error rate (%)');ax.grid(axis='x',alpha=.15)
        fig.suptitle(f'Exploratory {role} error slices; target5%; mean/sample std n=5; minimum support100; top six rates')
        save(fig,name+'.png')


def run():
    if OUT.exists():raise ValueError('Use a fresh output directory; do not overwrite evidence')
    OUT.mkdir(parents=True)
    raw_path=ROOT/'data/raw/UNSW_NB15_testing-set.csv';raw_hash=sha256(raw_path)
    raw=pd.read_csv(raw_path,low_memory=False).sort_values('id').reset_index(drop=True)
    sample=pd.read_csv(ROOT/'demo/sample.csv',low_memory=False)
    rows=[];examples=[];stable=[];runtime=[];disagreement=[];inputs=[];confusions={};predictions={};metric_checks=0;checked=0;max_diff=0
    for scenario,heldout in SCENARIOS.items():
        for model in MODELS:
            seed_arrays={.01:[],.05:[]}
            for seed in SEEDS:
                rid=f'{scenario}-{model}-S{seed}';folder=ROOT/'results/runs'/rid
                protected=[folder/n for n in ('run.json','metrics.csv','predictions.csv','model_bundle.joblib')]
                before={p:sha256(p) for p in protected}
                meta=json.loads((folder/'run.json').read_text())
                frame=align_predictions(pd.read_csv(folder/'predictions.csv',float_precision='round_trip'),raw,rid,heldout)
                ranking=unique_scores(frame)
                ap=float(average_precision_score(ranking.y_true,ranking.score))
                _,n_checks=verify_saved_metrics(meta,frame,pd.read_csv(folder/'metrics.csv',float_precision='round_trip'),ap)
                metric_checks+=n_checks
                checked+=len(frame)
                for target,part in frame.groupby('target_fpr',sort=True):
                    joined=part.merge(raw[['id','proto','service','state','dur','sttl','dbytes']],left_on='record_id',right_on='id',validate='one_to_one',sort=False)
                    assert len(joined)==len(raw)
                    seed_arrays[target].append(joined.y_pred.to_numpy(dtype=np.int8))
                    predictions[(scenario,model,target,seed)]=joined.y_pred.to_numpy(dtype=np.int8) if seed==42 else None
                    for dimension in ('proto','service','state'):
                        groups=grouped_errors(joined,dimension)
                        assert sum(x['support'] for x in groups)==len(raw)
                        rows.extend(dict(run_id=rid,scenario=scenario,model=model,seed=seed,target_fpr=target,**x) for x in groups)
                    if seed==42:
                        if target==.05:
                            y=joined.y_true.to_numpy();p=joined.y_pred.to_numpy()
                            confusions[(scenario,model)]=(int(((y==0)&(p==0)).sum()),int(((y==0)&(p==1)).sum()),int(((y==1)&(p==0)).sum()),int(((y==1)&(p==1)).sum()))
                        for role,g in joined.groupby('evaluation_role'):
                            g=g.copy();g['abs_margin']=(g.score-g.threshold).abs()
                            selected=g.sort_values(['abs_margin','record_id']).head(3)
                            for x in selected.to_dict('records'):examples.append(dict(selection='nearest_threshold_per_role',**{k:x[k] for k in ['record_id','run_id','target_fpr','evaluation_role','attack_cat','y_true','y_pred','score','threshold','abs_margin','proto','service','state','dur','sttl','dbytes']}))
                bundle=joblib.load(folder/'model_bundle.joblib');pre=bundle['preprocessor'];model_fit=bundle['fitted_model']
                def predict():
                    matrix=np.asarray(pre.transform(sample[bundle['features']]),dtype=np.float32)
                    return model_fit.score(matrix)
                scores=predict();times=[]
                for _ in range(3):
                    start=perf_counter();scores=predict();times.append(perf_counter()-start)
                expected=frame[(frame.target_fpr==.05)&frame.record_id.isin(sample.id)].sort_values('record_id')
                actual=pd.Series(scores,index=sample.id).sort_index()
                diff=float(np.max(np.abs(actual.to_numpy()-expected.score.to_numpy())))
                assert diff<=1e-6,(rid,diff)
                assert np.array_equal(actual.to_numpy()>=expected.threshold.to_numpy(),expected.y_pred.astype(bool).to_numpy())
                max_diff=max(max_diff,diff)
                runtime.append(dict(run_id=rid,scenario=scenario,model=model,seed=seed,historical_total_run_seconds=meta['duration_seconds'],historical_train_only_seconds=np.nan,
                    bundle_bytes=(folder/'model_bundle.joblib').stat().st_size,current_inference_100_rows_seconds=float(np.mean(times)),current_repeat_std_seconds=float(np.std(times,ddof=1)),warmup=1,repeats=3,score_max_abs_diff=diff))
                del bundle
                for path,h in before.items():
                    assert sha256(path)==h,path
                    inputs.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=h))
                print('Final diagnostics verified:',rid,flush=True)
            y=raw.label.to_numpy()
            roles=np.where(y==0,'normal',np.where(raw.attack_cat.eq(heldout),'heldout_attack','known_attack'))
            for target,arrays in seed_arrays.items():
                wrong=(np.stack(arrays)!=y).sum(axis=0)
                for role in np.unique(roles):
                    mask=roles==role
                    for count in range(6):stable.append(dict(scenario=scenario,model=model,target_fpr=target,evaluation_role=role,error_seed_count=count,record_count=int((mask&(wrong==count)).sum()),role_support=int(mask.sum())))
        for target in (.01,.05):
            for i,model_a in enumerate(MODELS):
                for model_b in MODELS[i+1:]:
                    a=predictions[(scenario,model_a,target,42)];b=predictions[(scenario,model_b,target,42)];y=raw.label.to_numpy()
                    both=int(((a!=y)&(b!=y)).sum());either=int(((a!=y)|(b!=y)).sum())
                    disagreement.append(dict(scenario=scenario,seed=42,target_fpr=target,model_a=model_a,model_b=model_b,support=len(raw),different_prediction_count=int((a!=b).sum()),both_wrong=both,either_wrong=either,error_jaccard=both/either if either else np.nan))
    all_rows=pd.DataFrame(rows)
    keys=['scenario','model','target_fpr','evaluation_role','dimension','feature_value']
    summary=all_rows.groupby(keys,as_index=False).agg(seed_count=('seed','nunique'),support_min=('support','min'),support_max=('support','max'),error_rate_mean=('error_rate','mean'),error_rate_std=('error_rate','std'),error_count_mean=('error_count','mean'))
    assert summary.seed_count.eq(5).all()
    all_rows.to_csv(OUT/'GROUP_ERRORS_ALL_RUNS.csv',index=False);summary.to_csv(OUT/'GROUP_ERRORS_MEAN_STD.csv',index=False)
    pd.DataFrame(examples).to_csv(OUT/'NEAR_THRESHOLD_EXAMPLES_S42.csv',index=False)
    pd.DataFrame(stable).to_csv(OUT/'ERROR_STABILITY.csv',index=False);pd.DataFrame(disagreement).to_csv(OUT/'MODEL_DISAGREEMENT_S42.csv',index=False)
    costs=pd.DataFrame(runtime);costs.to_csv(OUT/'RUNTIME_SIZE_ALL_RUNS.csv',index=False)
    cost_summary=costs.groupby(['scenario','model'],as_index=False).agg(seed_count=('seed','nunique'),total_run_seconds_mean=('historical_total_run_seconds','mean'),total_run_seconds_std=('historical_total_run_seconds','std'),current_inference_ms_mean=('current_inference_100_rows_seconds',lambda x:1000*x.mean()),current_inference_ms_std=('current_inference_100_rows_seconds',lambda x:1000*x.std()),bundle_mb_mean=('bundle_bytes',lambda x:x.mean()/1e6),bundle_mb_std=('bundle_bytes',lambda x:x.std()/1e6))
    cost_summary.to_csv(OUT/'RUNTIME_SIZE_MEAN_STD.csv',index=False)
    hardware=dict(measured_on='2026-10-25',scope='Current inference measurement only; historical training hardware not recorded',platform=platform.platform(),processor=platform.processor(),logical_cpus=os.cpu_count(),python=sys.version)
    if sys.platform=='win32':
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'HARDWARE\DESCRIPTION\System\CentralProcessor\0') as k:hardware['cpu_name']=winreg.QueryValueEx(k,'ProcessorNameString')[0]
    (OUT/'HARDWARE_CURRENT.json').write_text(json.dumps(hardware,ensure_ascii=False,indent=2),encoding='utf-8')
    points=pd.read_csv(ROOT/'docs/evidence/dot_03/pr_scores_20261022/OPERATING_POINTS_MEAN_STD.csv',float_precision='round_trip')
    category=pd.read_csv(ROOT/'docs/evidence/dot_02/category_errors_20261014/CATEGORY_ERRORS_MEAN_STD.csv',float_precision='round_trip')
    plots(points,category,summary,confusions)
    assert sha256(raw_path)==raw_hash
    audit=dict(created_on='2026-10-25',run_count=80,prediction_rows_checked=checked,metric_checks=metric_checks,group_rows=len(all_rows),group_summary_rows=len(summary),near_threshold_examples=len(examples),model_pair_rows=len(disagreement),figures=len(list(OUT.glob('*.png'))),current_inference_parity_rows=8000,max_abs_score_diff=max_diff,
        raw_unchanged=True,inputs_unchanged=True,training_performed=False,threshold_tuning_performed=False,inputs=inputs,
        current_benchmark='100 deterministic illustrative test rows; transform+score only; warmup1/repeats3; not live traffic latency',
        historical_missing='No isolated historical train/inference time or hardware record; report total-run duration only, do not fabricate missing timing',
        limitations='Exploratory slices on same test, correlated seeds, no causal explanations or causal overlap removal')
    (OUT/'FINAL_DIAGNOSTICS_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in audit.items() if k!='inputs'},ensure_ascii=False,indent=2))


if __name__=='__main__':run()
