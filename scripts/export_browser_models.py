"""Export frozen seed-42 parameters; never fit or modify benchmark bundles."""
from pathlib import Path
import gzip, hashlib, json, math, sys
import joblib
import numpy as np
from sklearn.ensemble._iforest import _average_path_length

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
OUT=ROOT/'sites/nids-presentation/dist/models'
OUT.mkdir(parents=True,exist_ok=True)

def export(scenario,model):
    source=ROOT/'results/runs'/f'{scenario}-{model}-S42/model_bundle.joblib'
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    b=joblib.load(source);p=b['preprocessor'];e=b['fitted_model'].estimator
    numeric=p.transformers_[0][2];cat=p.transformers_[1][2]
    scaler=p.named_transformers_['numeric'].named_steps['scaler']
    encoder=p.named_transformers_['categorical'].named_steps['onehot']
    meta=dict(run_id=b['run_id'],model=model,seed=42,features=b['features'],
        numeric=list(numeric),categorical=list(cat),means=scaler.mean_.tolist(),scales=scaler.scale_.tolist(),
        categories=[v.tolist() for v in encoder.categories_],thresholds=b['thresholds'],
        source_sha256=before,arrays={})
    parts=[];offset=0
    def add(name,values,dtype):
        nonlocal offset
        padding=(-offset)%8
        if padding:parts.append(b'\0'*padding);offset+=padding
        a=np.asarray(values,dtype=dtype).reshape(-1)
        meta['arrays'][name]=dict(offset=offset,count=len(a),dtype=dtype)
        data=a.tobytes();parts.append(data);offset+=len(data)
    if model in ('RF','IF','XGB'):
        left=[];right=[];feature=[];threshold=[];value=[];roots=[]
        if model=='XGB':
            raw=json.loads(e.get_booster().save_raw(raw_format='json'))
            trees=raw['learner']['gradient_booster']['model']['trees']
            base=raw['learner']['learner_model_param']['base_score']
            base=float(json.loads(base)[0] if base.startswith('[') else base)
            meta['base_margin']=float(np.float32(math.log(base/(1-base))))
            for t in trees:
                start=len(left);roots.append(start)
                left.extend(x+start if x>=0 else -1 for x in t['left_children'])
                right.extend(x+start if x>=0 else -1 for x in t['right_children'])
                feature.extend(t['split_indices'])
                # XGBoost compares float32 matrix values to float32 split values.
                conditions=np.asarray(t['split_conditions'],dtype=np.float32).tolist()
                threshold.extend(conditions);value.extend(conditions)
        else:
            for i,est in enumerate(e.estimators_):
                t=est.tree_;start=len(left);roots.append(start)
                left.extend(np.where(t.children_left>=0,t.children_left+start,-1))
                right.extend(np.where(t.children_right>=0,t.children_right+start,-1))
                f=t.feature.copy()
                if model=='IF':
                    chosen=e.estimators_features_[i];mask=f>=0;f[mask]=chosen[f[mask]]
                feature.extend(f);threshold.extend(t.threshold)
                value.extend(t.value[:,0,1] if model=='RF' else _average_path_length(t.n_node_samples))
            if model=='IF':
                meta['normalizer']=float(len(roots)*_average_path_length([e.max_samples_])[0])
                meta['offset']=float(e.offset_)
        for name,vals,dtype in [('left',left,'<i4'),('right',right,'<i4'),('feature',feature,'<i4'),('threshold',threshold,'<f8'),('value',value,'<f8'),('roots',roots,'<i4')]:add(name,vals,dtype)
    else:
        meta['layers']=[]
        for i,(weights,bias) in enumerate(zip(e.coefs_,e.intercepts_)):
            meta['layers'].append(dict(input=weights.shape[0],output=weights.shape[1]))
            add(f'weights{i}',weights,'<f4');add(f'bias{i}',bias,'<f4')
    header=json.dumps(meta,ensure_ascii=False,separators=(',',':')).encode()
    # First 4 bytes: header length, followed by an 8-byte-aligned JSON header.
    prefix=np.asarray([len(header)],dtype='<u4').tobytes()+header
    prefix+=b'\0'*((-len(prefix))%8)
    packed=prefix+b''.join(parts)
    path=OUT/f'{scenario}-{model}-S42.bin.gz'
    path.write_bytes(gzip.compress(packed,compresslevel=9,mtime=0))
    assert hashlib.sha256(source.read_bytes()).hexdigest()==before
    return dict(run_id=b['run_id'],file=path.name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source_sha256=before)

if __name__=='__main__':
    rows=[]
    for scenario in ('CS','LR','LD','LE'):
        for model in ('RF','XGB','IF','AE'):
            row=export(scenario,model);rows.append(row);print(row['run_id'],row['bytes'],flush=True)
    (OUT/'manifest.json').write_text(json.dumps(dict(format='nids-browser-parameters-v1',models=rows,scope='Frozen seed42 only; browser floating-point parity audited separately'),ensure_ascii=False,indent=2),encoding='utf-8')
