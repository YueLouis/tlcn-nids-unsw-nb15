"""Check the revised PDF's resources, links and worked examples; never sign for members."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import argparse

import pandas as pd
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'docs/report_dot3_review_20261106'
OUT = ROOT / 'docs/evidence/dot_03/recheck_20261106/review_20261107_v2'
BUILD = SRC / 'build'
PLOT_INPUTS = OUT.parent / 'PLOT_PRESENTATION_INPUTS.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return pd.read_csv(path, float_precision='round_trip')


def main():
    resources = []
    for source in sorted(SRC.rglob('*.tex')):
        if any(part.startswith('build') for part in source.relative_to(SRC).parts):
            continue
        text = source.read_text(encoding='utf-8')
        for kind, name in re.findall(r'\\(input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}', text):
            path = SRC / name
            if kind == 'input' and not path.suffix:
                path = path.with_suffix('.tex')
            assert path.is_file(), (source, kind, name)
            resources.append({'source': source.relative_to(SRC).as_posix(),
                              'resource': path.relative_to(SRC).as_posix(), 'sha256': sha(path)})

    paths = []
    text = (SRC / 'main.tex').read_text(encoding='utf-8')
    appendix = text.split(r'\caption{Đường dẫn', 1)[1].split(r'\bottomrule', 1)[0]
    for name in re.findall(r'\\path\{([^}]+)\}', appendix):
        path = ROOT / name
        if '<run-id>' in name:
            matches = list((ROOT / 'results/runs').glob('*-S*'))
            assert len(matches) == 80
            paths.append({'path': name, 'run_directories': len(matches)})
        else:
            assert path.exists(), name
            paths.append({'path': name, 'exists': True})

    plot_inputs = json.loads(PLOT_INPUTS.read_text(encoding='utf-8'))
    for item in plot_inputs:
        assert sha(ROOT / item['path']) == item['sha256'], item['path']

    pdf = BUILD / 'main.pdf'
    doc = pymupdf.open(pdf)
    names = doc.resolve_names()
    links = []
    for page_index, page in enumerate(doc):
        for link in page.get_links():
            if link['kind'] == pymupdf.LINK_GOTO or 'nameddest' in link:
                assert 0 <= link['page'] < len(doc), link
                if 'nameddest' in link:
                    assert link['nameddest'] in names, link
                dest = doc[link['page']]
                point = link.get('to')
                assert point is None or (-1 <= point.y <= dest.rect.height + 1), link
                links.append({'from_pdf_page': page_index + 1, 'to_pdf_page': link['page'] + 1})
    assert len(links) > 100
    index_entries = []
    for ext, label in [('lot', 'Bảng'), ('lof', 'Hình')]:
        index_text = (BUILD / f'main.{ext}').read_text(encoding='utf-8')
        for line in index_text.splitlines():
            if not line.startswith(r'\contentsline'):
                continue
            number = re.search(r'\\numberline\s*\{([^}]+)\}', line).group(1)
            destination = re.search(r'\}\{([^{}]+)\}\s*%?$', line).group(1)
            assert destination in names
            page_index = names[destination]['page']
            expected = label + ' ' + number
            assert re.search(re.escape(expected) + r'\.', doc[page_index].get_text()), (expected, page_index + 1)
            index_entries.append({'caption': expected, 'pdf_page': page_index + 1, 'destination': destination})
    assert len(index_entries) > 40
    toc = doc.get_toc()
    assert toc and all(1 <= row[2] <= len(doc) for row in toc)
    assert len(doc) == 62
    geometry = json.loads((OUT / 'PDF_GEOMETRY.json').read_text(encoding='utf-8'))
    assert geometry['sha256'] == sha(pdf)
    assert all(not p['text_spans_outside_page'] and not p['has_replacement_character']
               for p in geometry['pages'])
    log = (BUILD / 'main.log').read_text(encoding='utf-8', errors='replace')
    warnings = re.findall(r'Overfull[^\n]*|Missing character[^\n]*|[^\n]*undefined references[^\n]*|[^\n]*Rerun to[^\n]*', log)
    assert not warnings, warnings

    raw_path = ROOT / 'data/raw/UNSW_NB15_testing-set.csv'
    raw = read(raw_path).set_index('id')
    assert len(raw) == 82332 and len(raw.columns) + 1 == 45
    assert raw.label.value_counts().to_dict() == {1: 45332, 0: 37000}
    support = {'Reconnaissance': 3496, 'DoS': 4089, 'Exploits': 11132}
    assert all(int(raw.attack_cat.eq(cat).sum()) == count for cat, count in support.items())
    manifest = json.loads((ROOT / 'artifacts/data/data_manifest.json').read_text(encoding='utf-8'))
    assert sha(raw_path) == manifest['files']['test']['sha256']

    near = read(ROOT / 'docs/evidence/dot_03/final_diagnostics_20261025/NEAR_THRESHOLD_EXAMPLES_S42.csv')
    final = (SRC / 'final_diagnostics.tex').read_text(encoding='utf-8')
    part = final.split('{Ví dụ gần ngưỡng nhất', 1)[1].split(r'\bottomrule', 1)[0]
    traces = []
    for line in part.splitlines():
        if not re.match(r'^(IF|RF) & ', line):
            continue
        model, record_id, outcome, margin, proto, service, duration, ttl, dbytes = line.removesuffix('\\\\').split(' & ')
        run_id = f'LR-{model}-S42'
        rows = near[near.run_id.eq(run_id) & near.record_id.eq(int(record_id)) & near.target_fpr.eq(.05)]
        assert len(rows) == 1
        row = rows.iloc[0]
        prediction = read(ROOT / f'results/runs/{run_id}/predictions.csv')
        prediction = prediction[prediction.target_fpr.eq(.05)].copy()
        pr = prediction[prediction.record_id.eq(int(record_id))].iloc[0]
        for key in ('score', 'threshold', 'y_true', 'y_pred', 'evaluation_role', 'attack_cat'):
            assert pr[key] == row[key], (record_id, key)
        rr = raw.loc[int(record_id)]
        assert rr.label == row.y_true and rr.attack_cat == row.attack_cat
        assert int(row.y_pred) == int(row.score >= row.threshold)
        actual = 'FP' if row.y_true == 0 and row.y_pred == 1 else 'FN' if row.y_true == 1 and row.y_pred == 0 else 'correct'
        assert outcome == actual
        assert margin == f'{abs(row.score-row.threshold):.2g}'
        assert [proto, service, duration, ttl, dbytes] == [str(rr.proto), str(rr.service), f'{rr.dur:.3g}', str(int(rr.sttl)), str(int(rr.dbytes))]
        prediction['margin'] = (prediction.score - prediction.threshold).abs()
        closest = prediction[prediction.evaluation_role.eq(row.evaluation_role)].sort_values(['margin', 'record_id']).iloc[0]
        assert closest.record_id == int(record_id)
        traces.append({'run_id': run_id, 'record_id': int(record_id), 'target_fpr': .05,
                       'y_true': int(row.y_true), 'score': float(row.score), 'threshold': float(row.threshold),
                       'y_pred': int(row.y_pred), 'outcome': outcome, 'closest_in_role': True})
    assert len(traces) == 4

    teaching = read(ROOT / 'results/runs/CS-RF-S42/predictions.csv')
    teaching = teaching[teaching.record_id.eq(1)]
    assert len(teaching) == 2 and teaching.y_true.eq(0).all()
    assert teaching.score.nunique() == 1
    assert teaching.loc[teaching.target_fpr.eq(.05), 'y_pred'].item() == 1
    assert teaching.loc[teaching.target_fpr.eq(.01), 'y_pred'].item() == 0

    result = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'pdf_sha256': sha(pdf),
              'pdf_pages': len(doc), 'tex_resources_checked': resources, 'appendix_paths_checked': paths,
              'plot_inputs_hashes_checked': len(plot_inputs), 'internal_links_checked': len(links),
              'bookmark_destinations_checked': len(toc), 'index_internal_links_checked': sum(x['from_pdf_page'] in (5, 6) for x in links),
              'index_entries_match_caption_destination': index_entries,
              'compile_errors_or_blocking_warnings': warnings, 'underfull_hboxes': log.count('Underfull \\hbox'),
              'raw_test_support_checked': True, 'near_threshold_raw_traces': traces,
              'teaching_example': teaching.to_dict('records'),
              'scope_limit': 'Technical and presentation checks only; member work, group approval and submission remain unverified.'}
    (OUT / 'DELIVERY_TECHNICAL_CHECK.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('tex_resources_checked', 'appendix_paths_checked', 'near_threshold_raw_traces', 'teaching_example', 'index_entries_match_caption_destination')}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SRC)
    parser.add_argument('--build', type=Path, default=BUILD)
    parser.add_argument('--output', type=Path, default=OUT)
    parser.add_argument('--plot-inputs', type=Path, default=PLOT_INPUTS)
    args = parser.parse_args()
    SRC = args.source.resolve()
    BUILD = args.build.resolve()
    OUT = args.output.resolve()
    PLOT_INPUTS = args.plot_inputs.resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    main()
