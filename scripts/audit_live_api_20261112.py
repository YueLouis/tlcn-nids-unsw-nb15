"""Compare the running HTTP API with locked predictions; save a private current receipt."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import hashlib
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/code_api_review_20261112'
BASE = 'http://127.0.0.1:4397'


def request(path, payload=None, raw=None, origin=None):
    data = raw if raw is not None else (None if payload is None else json.dumps(payload).encode())
    headers = {'Content-Type': 'application/json'}
    if origin:
        headers['Origin'] = origin
    try:
        with urlopen(Request(BASE + path, data=data, headers=headers), timeout=120) as response:
            body = response.read()
            return response.status, json.loads(body) if 'application/json' in response.headers.get('Content-Type', '') else body
    except HTTPError as exc:
        return exc.code, json.loads(exc.read())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert request('/health')[1]['app'] == 'nids-demo'
    sample = (ROOT / 'demo/sample.csv').read_text(encoding='utf-8')
    rows = pd.read_csv(ROOT / 'demo/sample.csv')
    comparisons = []
    input_hashes = []
    for scenario in ('CS', 'LR', 'LD', 'LE'):
        for model in ('RF', 'XGB', 'IF', 'AE'):
            rid = f'{scenario}-{model}-S42'
            source = ROOT / 'results/runs' / rid / 'predictions.csv'
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            expected = pd.read_csv(source, float_precision='round_trip')
            for target in (.01, .05):
                status, result = request('/api/predict', dict(scenario=scenario, model=model, target=target, csv=sample))
                assert status == 200, (rid, target, status, result)
                actual = pd.DataFrame(result['results'])
                actual['record_id'] = actual.record_id.astype(int)
                actual = actual.sort_values('record_id')
                ref = expected[expected.target_fpr.eq(target) & expected.record_id.isin(rows.id)].sort_values('record_id')
                assert actual.record_id.tolist() == ref.record_id.tolist()
                assert actual.prediction.eq('Attack').astype(int).tolist() == ref.y_pred.tolist()
                assert np.array_equal(actual.threshold, ref.threshold)
                delta = float(np.max(np.abs(actual.score.to_numpy() - ref.score.to_numpy())))
                assert delta <= 1e-6, (rid, delta)
                comparisons.append(dict(run_id=rid, target=target, rows=len(actual), max_abs_score_difference=delta))
            assert hashlib.sha256(source.read_bytes()).hexdigest() == before
            input_hashes.append(dict(path=source.relative_to(ROOT).as_posix(), sha256=before))
            print(f'HTTP predictions match: {rid}', flush=True)
        code, compare = request('/api/compare', dict(scenario=scenario, target=.05, csv=sample))
        assert code == 200 and {x['model'] for x in compare['comparisons']} == {'RF', 'XGB', 'IF', 'AE'}
    status, cat = request('/api/lab/catalog')
    assert status == 200 and len(cat['cases']) == 8
    replay = []
    for case in cat['cases']:
        status, result = request('/api/lab/run', dict(case=case['id'], scenario=case['recommended_scenario'], model='RF', target=.05))
        assert status == (200 if case['expected_schema_valid'] else 400), (case['id'], status)
        if status == 200:
            assert result['prediction']['rows'] == len(result['prediction']['results'])
            if not case['labels_present']:
                assert result['summary']['labeled_rows'] == 0 and result['summary']['fpr'] is None
        replay.append(dict(case=case['id'], status=status))
    unlabeled = rows.drop(columns=['label', 'attack_cat']).to_csv(index=False)
    status, result = request('/api/predict', dict(csv=unlabeled))
    assert status == 200 and result['labeled_rows'] == 0
    assert all('truth' not in r and 'outcome' not in r for r in result['results'])
    invalid = [
        ('missing_feature', dict(csv=rows.drop(columns=['dur']).to_csv(index=False))),
        ('empty_csv', dict(csv='')),
        ('not_a_number', dict(csv=rows.assign(dur='abc').to_csv(index=False))),
        ('infinity', dict(csv=rows.assign(dur=np.inf).to_csv(index=False))),
        ('invalid_model', dict(csv=sample, model='../model')),
        ('invalid_scenario', dict(csv=sample, scenario='OTHER')),
        ('invalid_target', dict(csv=sample, target=.25)),
        ('null_csv', dict(csv=None)),
    ]
    edges = []
    for name, payload in invalid:
        status, result = request('/api/predict', payload)
        edges.append(dict(case=name, status=status, error=result.get('error')))
    for name, raw in [('json_list', b'[]'), ('json_null', b'null'), ('broken_json', b'{')]:
        status, result = request('/api/predict', raw=raw)
        edges.append(dict(case=name, status=status, error=result.get('error')))
    status, result = request('/api/predict', dict(csv=sample), origin='https://example.org')
    assert status == 403
    assert request('/does-not-exist')[0] == 404
    assert request('/api/does-not-exist', dict(csv=sample))[0] == 404
    failures = [r for r in edges if r['status'] != 400]
    receipt = dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),
                   http_operating_cases=len(comparisons), prediction_rows_checked=sum(r['rows'] for r in comparisons),
                   exact_labels_and_thresholds=True, score_absolute_tolerance=1e-6,
                   max_abs_score_difference=max(r['max_abs_score_difference'] for r in comparisons),
                   model_comparisons_scenarios=4, catalog_cases=replay,
                   unlabeled_input_does_not_create_truth=True, invalid_requests=edges,
                   cross_origin_rejected=True, unknown_routes_404=True,
                   failures=failures, comparisons=comparisons, inputs_unchanged=input_hashes,
                   scope='Loopback HTTP API with frozen seed-42 bundles; selected official-test examples, not independent traffic or public hosting')
    (OUT / 'API_AUDIT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('comparisons', 'inputs_unchanged')}, ensure_ascii=False, indent=2))
    assert not failures, failures


if __name__ == '__main__':
    main()
