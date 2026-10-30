"""Application replay over frozen binary models, without fitting or relabeling."""
from pathlib import Path
import hashlib
import json
from .demo import predict_csv

ROOT=Path(__file__).resolve().parents[2]
CASES=ROOT/'demo/cases'

def catalog() -> dict:
    return json.loads((CASES/'catalog.json').read_text(encoding='utf-8'))

def load_case(case_id: str) -> tuple[dict,str]:
    match=next((row for row in catalog()['cases'] if row['id']==case_id),None)
    if match is None:raise ValueError('Chọn một kịch bản trong danh sách.')
    path=(CASES/match['filename']).resolve()
    if not path.is_relative_to(CASES.resolve()):raise ValueError('Đường dẫn mẫu không hợp lệ.')
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=match['sha256']:raise ValueError('CSV mẫu khác hash trong hồ sơ; kiểm lại trước khi demo.')
    return match,raw.decode('utf-8')

def summarize(results: list[dict], heldout_class: str | None=None) -> dict:
    confusion={key:sum(row.get('outcome')==key for row in results) for key in ('TP','FP','TN','FN')}
    normal=confusion['TN']+confusion['FP'];attack=confusion['TP']+confusion['FN']
    heldout=[r for r in results if heldout_class and r.get('attack_cat')==heldout_class and r.get('truth')=='Attack']
    ratio=lambda numerator,denominator:None if denominator==0 else numerator/denominator
    return dict(confusion=confusion,labeled_rows=normal+attack,normal_support=normal,attack_support=attack,
        fpr=ratio(confusion['FP'],normal),recall=ratio(confusion['TP'],attack),
        precision=ratio(confusion['TP'],confusion['TP']+confusion['FP']),
        heldout_class=heldout_class,heldout_support=len(heldout),
        uadr=ratio(sum(r['prediction']=='Attack' for r in heldout),len(heldout)))

def run_case(case_id: str,scenario: str,model: str,target: float) -> dict:
    spec,text=load_case(case_id)
    result=predict_csv(scenario,model,target,text)
    heldout={'LR':'Reconnaissance','LD':'DoS','LE':'Exploits'}.get(scenario)
    return dict(case=spec,provenance=catalog()['provenance'],prediction=result,
        summary=summarize(result['results'],heldout),
        replay_method='Batch predictions are computed first, then revealed in order for presentation. Replay speed is not model latency or network throughput.',
        assessment_scope='Descriptive results on a preselected demonstration subset, not a new benchmark or independent generalization estimate.',
        model_output='Normal/Attack only; attack_cat is supplied ground truth, never a predicted attack type.')
