"""Recheck frozen round-3 evidence without modifying earlier handoffs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import sys

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/evidence/dot_03/final_20261030'
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'scripts'))
from analyze_feature_importance import raw_importance
from nids_benchmark.demo import load_bundle, predict_frame, compare_csv


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    audit = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
             'training_performed': False, 'threshold_tuning_performed': False}
    frozen = json.loads((ROOT / 'docs/evidence/dot_03/overlap_20261025/OVERLAP_AUDIT.json').read_text())['inputs']
    for entry in frozen:
        assert sha(ROOT / entry['path']) == entry['sha256'], entry['path']
    audit['frozen_input_hashes_matched'] = len(frozen)
    print('333 frozen inputs unchanged', flush=True)

    comparisons = []
    for old, new, names in [
        ('pr_scores_20261022', 'pr_scores', ['AP_ALL_RUNS', 'AP_MEAN_STD', 'OPERATING_POINTS_ALL_RUNS', 'OPERATING_POINTS_MEAN_STD', 'SCORE_QUANTILES_ALL_RUNS']),
        ('overlap_20261025', 'overlap', ['FIT_SET_CHECKS', 'OVERLAP_ALL_RUNS', 'OVERLAP_MEAN_STD']),
    ]:
        for name in names:
            a = pd.read_csv(ROOT / 'docs/evidence/dot_03' / old / (name + '.csv'), float_precision='round_trip')
            b = pd.read_csv(OUT / new / (name + '.csv'), float_precision='round_trip')
            pd.testing.assert_frame_equal(a, b, check_exact=True)
            comparisons.append({'file': name + '.csv', 'rows': len(a), 'exact_match': True})
    audit['fresh_csv_comparisons'] = comparisons
    print('8 freshly recomputed CSVs exactly match earlier results', flush=True)

    feature_data = pd.read_csv(ROOT / 'docs/evidence/dot_03/features_20261025/FEATURE_IMPORTANCE_ALL_RUNS.csv', float_precision='round_trip')
    for run_id, frame in feature_data.groupby('run_id'):
        actual = raw_importance(joblib.load(ROOT / 'results/runs' / run_id / 'model_bundle.joblib'))
        expected = frame.set_index('feature').importance.loc[actual.index]
        np.testing.assert_allclose(actual, expected, atol=1e-15, rtol=0)
    summary = feature_data.groupby(['scenario', 'model', 'method', 'feature'], as_index=False).agg(
        importance_mean=('importance', 'mean'), importance_std=('importance', 'std'), seeds=('seed', 'nunique'))
    expected = pd.read_csv(ROOT / 'docs/evidence/dot_03/features_20261025/FEATURE_IMPORTANCE_MEAN_STD.csv', float_precision='round_trip')
    pd.testing.assert_frame_equal(summary, expected, check_exact=False, rtol=0, atol=1e-15)
    audit['importance'] = {'runs': 40, 'raw_feature_rows': len(feature_data), 'summary_rows': len(summary), 'matched': True}
    print('40 importance bundles and 336 groups matched', flush=True)

    spec = importlib.util.spec_from_file_location('verify_final_tables', ROOT / 'scripts/verify_final_diagnostic_tables.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.OUT = OUT
    module.main()

    # Read the already declared sample rather than recreating an earlier handoff.
    frame = pd.read_csv(ROOT / 'demo/sample.csv', float_precision='round_trip')
    raw = pd.read_csv(ROOT / 'data/raw/UNSW_NB15_testing-set.csv', float_precision='round_trip').set_index('id')
    pd.testing.assert_frame_equal(frame.set_index('id'), raw.loc[frame.id], check_exact=True)
    rows = 0
    maximum = 0.0
    for scenario in ('CS', 'LR', 'LD', 'LE'):
        for model in ('RF', 'XGB', 'IF', 'AE'):
            rid = f'{scenario}-{model}-S42'
            stored = pd.read_csv(ROOT / 'results/runs' / rid / 'predictions.csv', float_precision='round_trip')
            bundle = load_bundle(scenario, model)
            for target in (.01, .05):
                result = predict_frame(bundle, frame, target)
                actual = pd.DataFrame(result['results']).sort_values('record_id', key=lambda x: x.astype(int))
                reference = stored[stored.target_fpr.eq(target) & stored.record_id.isin(frame.id)].sort_values('record_id')
                np.testing.assert_array_equal(actual.record_id.astype(int), reference.record_id)
                np.testing.assert_array_equal(actual.prediction.eq('Attack').astype(int), reference.y_pred)
                np.testing.assert_array_equal(actual.threshold, reference.threshold)
                diff = float(np.max(np.abs(actual.score.to_numpy() - reference.score.to_numpy())))
                assert diff <= 1e-6, (rid, diff)
                maximum = max(maximum, diff)
                rows += len(actual)
            print(f'Inference parity {rid}', flush=True)
    compare = compare_csv('CS', .05, frame.to_csv(index=False))
    assert [item['model'] for item in compare['comparisons']] == ['RF', 'XGB', 'IF', 'AE']
    invalid = []
    for name, bad in [('missing_feature', frame.drop(columns=['dur'])), ('empty', frame.iloc[:0]),
                      ('nonnumeric', frame.assign(dur='abc')), ('infinite', frame.assign(dur=np.inf))]:
        try:
            predict_frame(load_bundle('CS', 'RF'), bad, .05)
        except ValueError:
            invalid.append(name)
        else:
            raise AssertionError(name)
    audit['fresh_demo'] = {'bundles': 16, 'operating_cases': 32, 'prediction_rows': rows,
                           'max_abs_score_difference': maximum, 'score_atol': 1e-6,
                           'labels_and_thresholds_exact': True, 'invalid_inputs_rejected': invalid,
                           'scope': 'Replay of existing official-test sample, not live traffic or independent validation'}
    for entry in frozen:
        assert sha(ROOT / entry['path']) == entry['sha256'], entry['path']
    audit['inputs_unchanged_after_inference'] = True
    (OUT / 'FRESH_AUDIT.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in audit.items() if k != 'fresh_csv_comparisons'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
