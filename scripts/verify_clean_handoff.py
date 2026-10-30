"""Exercise the actual ZIPs in an isolated venv, without global user packages."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import site
import subprocess
import sys
import time
import urllib.request
import zipfile


ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'docs/evidence/dot_03/session_20261025'
SANDBOX=ROOT/'tmp/clean_handoff_extract_20261026'


def covered_files(light,portable):
    """Fingerprint the runtime, tests and protocol that the fresh env used.

    This remains independently checkable after documentation/audit repackaging;
    archive hashes identify the original tested ZIP, not a self-hashed archive.
    """
    rows=[]
    for label,folder in [('light',light),('portable',portable)]:
        for path in sorted(folder.rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts:continue
            rel=path.relative_to(folder).as_posix()
            if label=='portable':
                include=rel.startswith(('src/','demo/','results/runs/')) or rel in ('scripts/demo_server.py','requirements-repro.txt')
            else:
                include=rel.startswith(('src/','tests/','configs/')) or rel in ('scripts/validate_protocol.py','scripts/analyze_pr_scores.py','scripts/analyze_overlap_slices.py','scripts/analyze_final_diagnostics.py','docs/protocol/RUN_MATRIX.csv','requirements-analysis.txt','requirements-repro.txt')
            if include:rows.append(dict(package=label,path=rel,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    return rows


def main():
    assert sys.prefix!=sys.base_prefix,'Run this verifier with a fresh venv Python'
    assert not site.ENABLE_USER_SITE,'User site packages must be disabled'
    SANDBOX.mkdir(parents=True,exist_ok=True)
    archives=[ROOT.parent/'02_Bao_cao/BO_BAO_CAO_VA_HUONG_DAN_GUI_NHOM_20261025.zip',
              ROOT.parent/'02_Bao_cao/DEMO_NIDS_NHOM_20261025.zip']
    archive_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in archives}
    for path in archives:
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None
            for name in z.namelist():assert (SANDBOX/name).resolve().is_relative_to(SANDBOX.resolve())
            z.extractall(SANDBOX)
    light=SANDBOX/'BO_HO_SO_NHOM_20261025/07_Ma_nguon'
    portable=SANDBOX/'DEMO_NIDS_NHOM_20261025'
    env=dict(os.environ,PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONPATH=str(light/'src'))
    tests=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-q'],cwd=light,env=env,capture_output=True,text=True,encoding='utf-8')
    (EVIDENCE/'clean_snapshot_tests.log').write_text(tests.stdout+tests.stderr,encoding='utf-8')
    assert tests.returncode==0 and 'Ran 46 tests' in tests.stderr,tests.stderr
    validator=subprocess.run([sys.executable,'scripts/validate_protocol.py'],cwd=light,env=env,capture_output=True,text=True,encoding='utf-8')
    (EVIDENCE/'clean_snapshot_protocol.log').write_text(validator.stdout+validator.stderr,encoding='utf-8')
    assert validator.returncode==0
    print('Unpacked lightweight code: 46 tests and protocol validator passed',flush=True)
    sys.path.insert(0,str(portable/'src'))
    import numpy as np
    import pandas as pd
    import sklearn
    from nids_benchmark import demo
    assert Path(demo.__file__).resolve().is_relative_to(portable.resolve())
    assert Path(sklearn.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    data=(portable/'demo/sample.csv').read_text(encoding='utf-8')
    checked=0;max_diff=0
    for scenario in ('CS','LR','LD','LE'):
        for model in ('RF','XGB','IF','AE'):
            for target in (.01,.05):
                result=demo.predict_csv(scenario,model,target,data)
                reference=pd.read_csv(ROOT/'results/runs'/result['run_id']/'predictions.csv',float_precision='round_trip')
                expected=reference[reference.target_fpr==target].set_index('record_id')
                for row in result['results']:
                    ref=expected.loc[int(row['record_id'])]
                    diff=abs(row['score']-float(ref.score));max_diff=max(max_diff,diff)
                    assert diff<=1e-6
                    assert row['threshold']==float(ref.threshold)
                    assert int(row['prediction']=='Attack')==int(ref.y_pred)
                    checked+=1
        print('Clean inference:',scenario,flush=True)
    assert checked==3200
    payload=json.dumps(dict(scenario='CS',target=.05,csv=data)).encode('utf-8')
    env['PYTHONPATH']=str(portable/'src')
    log=(EVIDENCE/'clean_demo_server.log').open('w',encoding='utf-8')
    server=subprocess.Popen([sys.executable,'scripts/demo_server.py','--port','4401'],cwd=portable,env=env,stdout=log,stderr=log)
    try:
        for attempt in range(60):
            assert server.poll() is None,'Clean server exited unexpectedly'
            try:
                health=json.load(urllib.request.urlopen('http://127.0.0.1:4401/health',timeout=1))
                break
            except OSError:time.sleep(.2)
        else:raise AssertionError('Clean server did not start')
        assert health['app']=='nids-demo'
        req=urllib.request.Request('http://127.0.0.1:4401/api/compare',payload,{'Content-Type':'application/json'})
        comparison=json.load(urllib.request.urlopen(req,timeout=90))
        assert [m['model'] for m in comparison['comparisons']]==['RF','XGB','IF','AE']
        assert comparison['rows']==100
        application_cases=0;application_predictions=0
        expected=json.loads((ROOT/'docs/evidence/dot_04/application_20261026/APPLICATION_AUDIT.json').read_text(encoding='utf-8'))
        for row in expected['checks']:
            payload=json.dumps(dict(case=row['case'],scenario=row['scenario'],model=row['model'],target=row['target_fpr'])).encode('utf-8')
            request=urllib.request.Request('http://127.0.0.1:4401/api/lab/run',payload,{'Content-Type':'application/json'})
            actual=json.load(urllib.request.urlopen(request,timeout=90))
            assert actual['summary']==row['summary'],row
            assert actual['prediction']['rows']==row['rows']
            application_cases+=1;application_predictions+=actual['prediction']['rows']
        assert application_cases==56 and application_predictions==1600
        print('Unpacked application API: 56 cases and 1,600 predictions checked',flush=True)
    finally:
        server.terminate();server.wait(timeout=15);log.close()
    result=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),fresh_venv=True,user_site_enabled=site.ENABLE_USER_SITE,
        python=sys.version,sklearn_version=sklearn.__version__,sklearn_from_venv=True,nids_from_extracted_zip=True,
        source_archive_sha256=archive_hashes,covered_runtime_and_test_files=covered_files(light,portable),unpacked_snapshot_tests=46,protocol_validator=True,model_bundles=16,operating_cases=32,
        individual_predictions_checked=checked,max_abs_score_diff=max_diff,tolerance=1e-6,http_comparison_models=4,
        application_cases=application_cases,application_predictions=application_predictions,
        scope='Fresh virtual environment and ZIP extraction on the same Windows host; not another physical machine or OS')
    (EVIDENCE/'CLEAN_ENV_HANDOFF_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
