"""Compare stored scaler statistics with deterministic development partitions."""
from pathlib import Path
import hashlib
import json
import sys

import joblib
import numpy as np
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from nids_benchmark.data import load_official_splits, make_development_split

OUT = ROOT / 'docs/evidence/dot_02/final_20261013/saved_split_audit.json'
raw = load_official_splits(ROOT / 'data/raw')
entries = []
scenarios = {'CS': None, 'LR': 'Reconnaissance', 'LD': 'DoS', 'LE': 'Exploits'}
numeric = [c for c in raw.train.columns if c not in {'id', 'label', 'attack_cat', 'proto', 'service', 'state'}]
for code, heldout in scenarios.items():
    for seed in (42, 52, 62, 72, 82):
        split = make_development_split(raw.train, heldout_class=heldout, seed=seed)
        development = raw.train if heldout is None else raw.train.loc[raw.train.attack_cat.ne(heldout)]
        binary_train, _ = train_test_split(development, test_size=.2, random_state=seed, stratify=development['label'])
        for model_code in ('RF', 'XGB', 'IF', 'AE'):
            run_id = f'{code}-{model_code}-S{seed}'
            run_dir = ROOT / 'results/runs' / run_id
            metadata = json.loads((run_dir / 'run.json').read_text(encoding='utf-8'))
            bundle = joblib.load(run_dir / 'model_bundle.joblib')
            scaler = bundle['preprocessor'].named_transformers_['numeric'].named_steps['scaler']
            fit_frame = split.train.loc[split.train.label.eq(0)] if model_code in ('IF', 'AE') else split.train
            binary_fit = binary_train.loc[binary_train.label.eq(0)] if model_code in ('IF', 'AE') else binary_train
            expected_mean = fit_frame[numeric].mean().to_numpy()
            expected_var = fit_frame[numeric].var(ddof=0).to_numpy()
            mean_match = bool(np.allclose(scaler.mean_, expected_mean, rtol=1e-10, atol=1e-10))
            variance_match = bool(np.allclose(scaler.var_, expected_var, rtol=1e-10, atol=1e-10))
            binary_match = bool(np.allclose(scaler.mean_, binary_fit[numeric].mean().to_numpy(), rtol=1e-10, atol=1e-10))
            rows_match = bool(metadata['row_counts']['preprocessor_fit_rows'] == len(fit_frame) == scaler.n_samples_seen_)
            ids = np.sort(split.train.id.to_numpy(dtype=np.int64))
            record = {'run_id': run_id, 'attack_cat_mean_match': mean_match, 'attack_cat_variance_match': variance_match,
                      'binary_label_mean_match': binary_match, 'fit_rows_match': rows_match,
                      'fit_rows': len(fit_frame), 'development_train_id_sha256': hashlib.sha256(ids.tobytes()).hexdigest()}
            entries.append(record)
            del bundle
        print(f'Checked {code}/seed {seed}: {len(entries)}/80', flush=True)
result = {'checked_on': '2026-10-14', 'method': 'Compare saved scaler mean/variance and sample count with reconstructed partitions; no model training',
          'partition': 'stratify=attack_cat', 'runs_checked': len(entries),
          'failure_count': sum(not (r['attack_cat_mean_match'] and r['attack_cat_variance_match'] and r['fit_rows_match']) for r in entries),
          'binary_matching_runs': sum(r['binary_label_mean_match'] for r in entries), 'entries': entries}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'entries'}, ensure_ascii=False), flush=True)
raise SystemExit(bool(result['failure_count']))
