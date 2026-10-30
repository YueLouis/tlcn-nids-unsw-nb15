"""Compare typeset numeric cells with independently audited round-3 tables."""
from pathlib import Path
from datetime import datetime, timezone
import re
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'docs/report_dot3_final_20261030'
OUT = ROOT / 'docs/evidence/dot_03/final_20261030'
OLD = ROOT / 'docs/evidence/dot_03/final_diagnostics_20261025'
checks = []


def read(path):
    return pd.read_csv(path, float_precision='round_trip')


def lines(file, start, end=None):
    text = (SRC / file).read_text(encoding='utf-8').split(start, 1)[1]
    if end:
        text = text.split(end, 1)[0]
    return [line.strip().removesuffix('\\\\').split(' & ') for line in text.splitlines()
            if re.match(r'^(CS|LR|LD|LE) & ', line)]


def pair(cell, mean, std, digits, scale=1):
    if pd.isna(mean):
        assert cell == '--', cell
        return
    actual = cell.replace('$', '').replace('\\%', '').split('\\pm')
    expected = [f'{mean * scale:.{digits}f}', f'{std * scale:.{digits}f}']
    assert actual == expected, (cell, expected)


def unique(frame, **filters):
    for k, v in filters.items():
        frame = frame[frame[k].eq(v)]
    assert len(frame) == 1, (filters, len(frame))
    return frame.iloc[0]


def main():
    overlap = read(OUT / 'overlap/OVERLAP_MEAN_STD.csv')
    runs = read(OUT / 'overlap/OVERLAP_ALL_RUNS.csv')
    ap = read(OUT / 'pr_scores/AP_MEAN_STD.csv')
    for row in lines('main.tex', r'\caption{Mean và sample std', r'\bottomrule'):
        sc, model = row[:2]
        r = unique(overlap, scenario=sc, model=model, cohort='all', target_fpr=.05)
        ar = unique(ap, scenario=sc, model=model, scope='all')
        p = runs[(runs.scenario == sc) & (runs.model == model) & runs.cohort.eq('all') & runs.target_fpr.eq(.05)]
        f1 = 2 * p.precision * p.recall / (p.precision + p.recall)
        for cell, mean, std in zip(row[2:],
             [r.precision_mean, ar.ap_mean, r.fpr_mean, r.known_recall_mean, r.uadr_mean, f1.mean()],
             [r.precision_std, ar.ap_std, r.fpr_std, r.known_recall_std, r.uadr_std, f1.std(ddof=1)]):
            pair(cell, mean, std, 4)
        checks.append('baseline ' + sc + '/' + model)
    for row in lines('main.tex', r'\caption{FPR official test', r'\bottomrule'):
        sc, model = row[:2]
        for target, cell in zip((.01, .05), row[2:]):
            r = unique(overlap, scenario=sc, model=model, cohort='all', target_fpr=target)
            pair(cell, r.fpr_mean, r.fpr_std, 2, 100)
        checks.append('two-target FPR ' + sc + '/' + model)
    for row in lines('rq3_two_targets.tex', r'\caption{Khả năng phát hiện', r'\bottomrule'):
        sc, model = row[:2]
        metric = 'recall' if sc == 'CS' else 'uadr'
        for target, cell in zip((.01, .05), row[2:4]):
            r = unique(overlap, scenario=sc, model=model, cohort='all', target_fpr=target)
            pair(cell, r[metric + '_mean'], r[metric + '_std'], 2, 100)
        checks.append('two-target detection ' + sc + '/' + model)
    for row in lines('dot3_analysis_20261025.tex', r'\caption{AP toàn test', r'\bottomrule'):
        sc, model = row[:2]
        r = unique(ap, scenario=sc, model=model, scope='all')
        pair(row[2], r.ap_mean, r.ap_std, 4)
        if sc != 'CS':
            r = ap[(ap.scenario == sc) & (ap.model == model) & ~ap.scope.eq('all')].iloc[0]
            pair(row[3], r.ap_mean, r.ap_std, 4)
            assert row[4] == f'{int(r.support):,}'
            assert row[5] == f'{100 * r.prevalence:.2f}\\%'
        checks.append('AP ' + sc + '/' + model)
    for row in lines('dot3_analysis_20261025.tex', r'\caption{Nhóm trùng/không trùng', r'\bottomrule'):
        sc, model, cohort = row[:3]
        r = unique(overlap, scenario=sc, model=model, cohort='matched' if cohort == 'Trùng' else 'unmatched', target_fpr=.05)
        assert row[3] == f'{int(r.support_min):,}--{int(r.support_max):,}'
        for cell, metric in zip(row[4:], ('fpr', 'recall', 'uadr')):
            pair(cell, r[metric + '_mean'], r[metric + '_std'], 2, 100)
        checks.append('overlap ' + sc + '/' + model + '/' + cohort)
    for row in lines('dot3_analysis_20261025.tex', r'\caption{Support nhóm matched', r'\bottomrule'):
        sc, family = row[:2]
        model = 'RF' if family == 'RF/XGB' else 'IF'
        r = unique(overlap, scenario=sc, model=model, cohort='matched', target_fpr=.05)
        for cell, role in zip(row[2:], ('normal', 'known', 'heldout')):
            low, high = int(r[role + '_min']), int(r[role + '_max'])
            assert cell == ('0' if low == high == 0 else f'{low:,}--{high:,}')
        checks.append('fit matched support ' + sc + '/' + family)
    importance = read(ROOT / 'docs/evidence/dot_03/features_20261025/FEATURE_IMPORTANCE_MEAN_STD.csv')
    for row in lines('dot3_analysis_20261025.tex', r'\caption{Ba feature', r'\bottomrule'):
        sc, model = row[:2]
        r = importance[importance.scenario.eq(sc) & importance.model.eq(model)].nlargest(3, 'importance_mean')
        text = '; '.join(f'{x.feature.replace("_", chr(92) + "_")} ({x.importance_mean:.3f})' for x in r.itertuples())
        assert row[2] == text
        checks.append('importance ' + sc + '/' + model)
    errors = read(OLD / 'GROUP_ERRORS_MEAN_STD.csv')
    for row in lines('final_diagnostics.tex', r'\caption{Lát cắt lỗi', r'\bottomrule'):
        sc, model, dim, value = row[:4]
        role = 'normal' if sc == 'CS' else 'heldout_attack'
        r = unique(errors, scenario=sc, model=model, target_fpr=.05, evaluation_role=role, dimension=dim, feature_value=value)
        assert row[4] == f'{int(r.support_min):,}'
        pair(row[5], r.error_rate_mean, r.error_rate_std, 2, 100)
        checks.append('error slice ' + sc + '/' + model + '/' + dim)
    stability = read(OLD / 'ERROR_STABILITY.csv')
    for row in lines('final_diagnostics.tex', r'\caption{Record sai', r'\bottomrule'):
        sc, model = row[:2]
        for cell, role in zip(row[2:], ('normal', 'heldout_attack')):
            if sc == 'CS' and role == 'heldout_attack':
                assert cell == '--'
                continue
            r = unique(stability, scenario=sc, model=model, target_fpr=.05, evaluation_role=role, error_seed_count=5)
            assert cell == f'{int(r.record_count):,} / {int(r.role_support):,}'
        checks.append('error stability ' + sc + '/' + model)
    pairs = read(OLD / 'MODEL_DISAGREEMENT_S42.csv')
    for row in lines('final_diagnostics.tex', r'\caption{Bất đồng', r'\bottomrule'):
        sc, models = row[:2]
        a, b = models.split(' / ')
        r = unique(pairs, scenario=sc, model_a=a, model_b=b, target_fpr=.05)
        assert row[2:] == [f'{int(r.different_prediction_count):,}', f'{int(r.both_wrong):,}', f'{r.error_jaccard:.4f}']
        checks.append('disagreement ' + sc + '/' + models)
    costs = read(OLD / 'RUNTIME_SIZE_MEAN_STD.csv')
    for row in lines('final_diagnostics.tex', r'\caption{Chi phí', r'\bottomrule'):
        sc, model = row[:2]
        r = unique(costs, scenario=sc, model=model)
        for cell, name in zip(row[2:], ('total_run_seconds', 'current_inference_ms', 'bundle_mb')):
            pair(cell, r[name + '_mean'], r[name + '_std'], 4)
        checks.append('runtime ' + sc + '/' + model)
    category = read(ROOT / 'docs/evidence/dot_02/category_errors_20261014/CATEGORY_ERRORS_MEAN_STD.csv')
    text = (SRC / 'main.tex').read_text(encoding='utf-8').split(r'\caption{Tỷ lệ bỏ sót FN', 1)[1].split(r'\bottomrule', 1)[0]
    for line in text.splitlines():
        if not re.match(r'^(Analysis|Backdoor|DoS|Exploits|Fuzzers|Generic|Reconnaissance|Shellcode|Worms) & ', line):
            continue
        row = line.strip().removesuffix('\\\\').split(' & ')
        name, support = row[:2]
        for cell, model in zip(row[2:], ('RF', 'XGB', 'IF', 'AE')):
            r = unique(category, scenario='CS', model=model, target_fpr=.05, attack_cat=name)
            assert support == f'{int(r.support):,}'.replace(',', '.')
            pair(cell, r.error_rate_mean, r.error_rate_std, 2, 100)
        checks.append('category ' + name)
    predictions = read(ROOT / 'results/runs/CS-RF-S42/predictions.csv')
    p = predictions[predictions.target_fpr.eq(.05)]
    assert ((p.y_true == 0) & (p.y_pred == 0)).sum() == 30198
    assert ((p.y_true == 0) & (p.y_pred == 1)).sum() == 6802
    assert ((p.y_true == 1) & (p.y_pred == 0)).sum() == 1284
    assert ((p.y_true == 1) & (p.y_pred == 1)).sum() == 44048
    checks.append('CS-RF-S42 confusion')
    result = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'table_rows_checked': len(checks),
              'all_displayed_cells_match_rounding': True, 'checks': checks,
              'scope': 'Main results, both targets, AP, overlap metrics, importance, group errors, stability, disagreement, costs'}
    (OUT / 'REPORT_TABLE_CHECK.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Typeset numeric rows matched:', len(checks))


if __name__ == '__main__':
    main()
