"""Read-only inference reference for exported browser parameters."""
from pathlib import Path
import json,sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from nids_benchmark.demo import predict_csv
out=ROOT/'output/browser_parity';out.mkdir(parents=True,exist_ok=True)
test=pd.read_csv(ROOT/'data/raw/UNSW_NB15_testing-set.csv')
mixed=pd.read_csv(ROOT/'demo/cases/mixed.csv')
sample=pd.concat([mixed,test.sample(n=1000,random_state=1311)]).drop_duplicates('id').head(1000)
csv=sample.to_csv(index=False)
cases=[]
for scenario in ('CS','LR','LD','LE'):
    for model in ('RF','XGB','IF','AE'):
        for target in (.01,.05):
            r=predict_csv(scenario,model,target,csv)
            cases.append(dict(run_id=r['run_id'],target=target,scores=[x['score']for x in r['results']],predictions=[x['prediction']for x in r['results']]))
        print(scenario,model,flush=True)
(out/'fixture.json').write_text(json.dumps(dict(csv=csv,cases=cases),allow_nan=False,separators=(',',':')),encoding='utf-8')
