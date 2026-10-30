"""Check the actual local draft handoff without certifying human approval."""
from pathlib import Path
import hashlib
import json
import re
import zipfile
from datetime import date

import pymupdf

ROOT=Path(__file__).resolve().parents[1]
WORKSPACE=ROOT.parent
PACKAGE=WORKSPACE/'02_Bao_cao/BO_HO_SO_NHOM_20261025'
EVIDENCE=ROOT/'docs/evidence/dot_03/session_20261025'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    reports=[]
    for kind,prefix,count in (('dot1','01',20),('dot2','02',37),('dot3','03',59),('dot4','04',63),('tong','05',57)):
        path=next((PACKAGE/'01_Bao_cao').glob(f'{prefix}_*.pdf'))
        with pymupdf.open(path) as pdf:
            assert len(pdf)==count
            assert all(len(page.get_text().strip())>20 for page in pdf)
        if kind in ('dot1','dot2'):
            original=WORKSPACE/f'02_Bao_cao/NhomTLCN_TramAnh_VuongThu_TrongTin_{kind}.pdf'
            assert digest(path)==digest(original)
        else:
            source=ROOT/f'docs/report_{kind}_20261025'
            assert digest(path)==digest(source/'build/main.pdf')
            log=(source/'build/main.log').read_text(encoding='utf-8',errors='replace')
            assert 'Overfull' not in log
            assert not re.search(r'(?:Reference|Citation).*undefined|There were undefined|Label\(s\) may have changed',log)
        reports.append(dict(kind=kind,pages=count,sha256=digest(path)))
    for x in json.loads((EVIDENCE/'PROTECTED_REPORTS.json').read_text(encoding='utf-8')):
        assert digest(Path(x['path']))==x['sha256']
    for path,expected in ((PACKAGE/'06_Trinh_bay/presentation.pdf',20),(PACKAGE/'06_Trinh_bay/huong_dan_tap_noi/guide.pdf',9)):
        with pymupdf.open(path) as pdf:
            assert len(pdf)==expected
            assert all(page.get_text().strip() for page in pdf)
    for x in json.loads((ROOT/'docs/presentation_20261025/CONTENT_AUDIT.json').read_text(encoding='utf-8'))['sources']:
        assert digest(ROOT/x['path'])==x['sha256']
    ui=json.loads((EVIDENCE/'PRESENTATION_UI_AUDIT.json').read_text(encoding='utf-8'))
    assert len(ui['checks'])==5 and not any(x['issues'] for x in ui['checks'])
    assert ui['keyboard_pass'] and not ui['guide_issues'] and not ui['page_errors']
    tests=(EVIDENCE/'clean_snapshot_tests.log').read_text(encoding='utf-8')
    assert 'Ran 46 tests' in tests and '\nOK' in tests
    diagnostics=json.loads((ROOT/'docs/evidence/dot_03/final_diagnostics_20261025/FINAL_DIAGNOSTICS_AUDIT.json').read_text(encoding='utf-8'))
    assert diagnostics['run_count']==80 and diagnostics['metric_checks']==1040
    assert diagnostics['inputs_unchanged'] and diagnostics['current_inference_parity_rows']==8000
    tables=json.loads((EVIDENCE/'FINAL_DIAGNOSTIC_TABLE_CHECK.json').read_text(encoding='utf-8'))
    assert tables['source_metric_partition_checks']==1920 and tables['group_summaries']==8768
    assert tables['stability_error_totals'] and tables['near_threshold_raw_prediction_and_selection'] and tables['pair_error_identities']
    demo_ui=json.loads((ROOT/'docs/evidence/dot_04/demo_20261025/DEMO_UI_AUDIT.json').read_text(encoding='utf-8'))
    assert demo_ui['models_compared']==4 and demo_ui['global_explanation'] and demo_ui['unlabeled_without_fake_fp_fn']
    assert not demo_ui['page_errors'] and not any(x['horizontal_overflow'] for x in demo_ui['checks'])
    clean=json.loads((EVIDENCE/'CLEAN_ENV_HANDOFF_AUDIT.json').read_text(encoding='utf-8'))
    assert clean['fresh_venv'] and not clean['user_site_enabled']
    assert clean['unpacked_snapshot_tests']==46 and clean['individual_predictions_checked']==3200
    assert clean['application_cases']==56 and clean['application_predictions']==1600
    assert clean['http_comparison_models']==4 and clean['max_abs_score_diff']<=clean['tolerance']
    ui_revision=json.loads((ROOT/'docs/evidence/dot_04/application_20261026/UI_REVISION_20261026.json').read_text(encoding='utf-8'))
    changed_presentation={row['path']:row for row in ui_revision['presentation_files']}
    for row in clean['covered_runtime_and_test_files']:
        folder=PACKAGE/'07_Ma_nguon' if row['package']=='light' else WORKSPACE/'02_Bao_cao/DEMO_NIDS_NHOM_20261025'
        current=digest(folder/row['path'])
        if current!=row['sha256']:
            revision=changed_presentation[row['path']]
            assert row['path'] in ('demo/index.html','demo/lab.html','demo/MO_DEMO.ps1')
            assert row['sha256']==revision['clean_environment_sha256'] and current==revision['current_sha256']
        else:assert current==row['sha256'],row['path']
    frozen=json.loads((EVIDENCE/'FROZEN_INPUTS_RECHECK.json').read_text(encoding='utf-8'))
    assert frozen['frozen_inputs_checked']==333 and frozen['matched']
    reading_audit=EVIDENCE/'READING_UI_AUDIT_20261026.json'
    opening_audit=EVIDENCE/'OPENING_LINKS_RECHECK_20261026.json'
    links=json.loads((opening_audit if opening_audit.exists() else EVIDENCE/'OPENING_LINKS_RECHECK.json').read_text(encoding='utf-8'))['links']
    assert len(links)>=19 and all(x['status']==200 for x in links)
    if reading_audit.exists():
        reading=json.loads(reading_audit.read_text(encoding='utf-8'))
        assert not reading['page_errors'] and not any(x['overflow'] for x in reading['viewports'])
        assert reading['role_switching'] and reading['notes_persist'] and reading['export_matches_input']
        assert reading['blank_export_is_unfilled'] and reading['notes_are_separate']
        assert digest(PACKAGE/'08_Tu_doc_va_gop_y/BAT_DAU.html')==reading['page_sha256']
        assert len(links)==23 and any('08_Tu_doc_va_gop_y' in x['href'] for x in links)
    application_path=ROOT/'docs/evidence/dot_04/application_20261026'
    application=json.loads((application_path/'APPLICATION_AUDIT.json').read_text(encoding='utf-8'))
    assert application['predictions_checked']==1600 and application['fixture_values_match_raw']
    application_ui=json.loads((application_path/'APPLICATION_UI_AUDIT.json').read_text(encoding='utf-8'))
    assert not application_ui['page_errors'] and len(application_ui['viewports'])==140
    assert not any(x['overflow'] or x['vertical_scroll'] or x['content_clipped'] or x['table_clipped'] for x in application_ui['viewports'])
    assert application_ui['six_in_page_sections'] and application_ui['result_pagination_all_ids'] and application_ui['notes_survive_navigation']
    assert digest(PACKAGE/'07_Ma_nguon/demo/lab.html')==application_ui['page_sha256']
    assert digest(PACKAGE/'09_Demo_ung_dung/report.pdf')==digest(ROOT/'docs/application_20261026/report.pdf')
    with pymupdf.open(PACKAGE/'09_Demo_ung_dung/report.pdf') as appendix:assert len(appendix)==5
    assert len(list((PACKAGE/'02_Anh_huong_dan').glob('0*.png')))==5
    assert len(list((PACKAGE/'07_Ma_nguon/results/runs').glob('*/run.json')))==80
    checked=0
    for x in json.loads((PACKAGE/'MANIFEST.json').read_text(encoding='utf-8'))['files']:
        p=PACKAGE/x['path']
        assert p.stat().st_size==x['bytes'] and digest(p)==x['sha256'],x['path']
        checked+=1
    archive=WORKSPACE/'02_Bao_cao/BO_BAO_CAO_VA_HUONG_DAN_GUI_NHOM_20261025.zip'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for p in PACKAGE.rglob('*'):
            if p.is_file():
                content=z.read(f'{PACKAGE.name}/{p.relative_to(PACKAGE).as_posix()}')
                assert hashlib.sha256(content).hexdigest()==digest(p)
    result=dict(checked_on=date.today().isoformat(),scope='Preparation complete, drafts awaiting group reading/revision; not submitted or academically approved',
                reports=reports,slides=20,guide_pages=9,guidance_images=5,light_code_snapshot_runs=80,
                snapshot_tests=46,protocol_validator='passed separately from snapshot',frozen_input_hashes=333,
                final_diagnostic_runs=80,final_diagnostic_figures=8,current_inference_parity_rows=8000,
                additional_group_metric_checks=1920,near_threshold_examples_rechecked=264,
                prototype_models_compared=4,prototype_explanation=True,application_replay_cases=8,application_prediction_checks=1600,application_appendix_pages=5,
                historical_fresh_venv_zip_test=True,current_presentation_revision_audited=True,fresh_venv_prediction_rows=3200,fresh_venv_covered_files=len(clean['covered_runtime_and_test_files']),
                original_reports_and_sources_unchanged=True,opening_links=len(links),viewports=5,
                package_files_verified=checked,zip_crc_and_contents=True,zip_bytes=archive.stat().st_size,
                remaining_human_steps=['Read and explain own part','Record actual contributions and review','Revise and approve the submission','Submit at the agreed deadline'],
                limitations=['One UNSW-NB15 split; three finite held-out classes','S07 abstract only','Historical isolated train time and hardware were not recorded; T2/T9 remain partially evidenced','No causal overlap-removal retraining, external dataset, or live traffic','Fresh virtual environment verified on the same Windows host; other physical machines and OS remain unverified'])
    (EVIDENCE/'COMPLETE_DRAFT_HANDOFF_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
