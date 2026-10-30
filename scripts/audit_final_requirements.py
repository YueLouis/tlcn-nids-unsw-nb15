"""Map the original requirements to current evidence without inventing sign-off."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import html
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/dot_03/session_20261025'


def digest(path):
    with path.open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()


def main():
    rows=[]
    def item(code,requirement,status,evidence,note=''):
        for rel in evidence:assert (ROOT/rel).exists(),rel
        rows.append(dict(code=code,requirement=requirement,status=status,evidence=evidence,note=note))
    runs=ROOT/'results/runs'
    assert len(list(runs.glob('*/run.json')))==80
    assert all((p/name).is_file() for p in runs.iterdir() for name in ('run.json','metrics.csv','predictions.csv','model_bundle.joblib'))
    diag='docs/evidence/dot_03/final_diagnostics_20261025/'
    pr='docs/evidence/dot_03/pr_scores_20261022/'
    cat='docs/evidence/dot_02/category_errors_20261014/'
    final=json.loads((ROOT/diag/'FINAL_DIAGNOSTICS_AUDIT.json').read_text(encoding='utf-8'))
    assert final['run_count']==80 and final['metric_checks']==1040 and final['figures']==8
    tests=(OUT/'clean_snapshot_tests.log').read_text(encoding='utf-8')
    assert 'Ran 46 tests' in tests and '\nOK' in tests
    demo=json.loads((ROOT/'docs/evidence/dot_04/demo_20261025/DEMO_AUDIT.json').read_text(encoding='utf-8'))
    assert demo['prediction_comparisons']==3200 and demo['inputs_unchanged']
    for code,title,paths in [
        ('SP1','Báo cáo đợt 3, đợt 4 và báo cáo tổng',['docs/report_dot3_20261025/build/main.pdf','docs/report_dot4_20261025/build/main.pdf','docs/report_tong_20261025/build/main.pdf']),
        ('SP2','Code có cấu trúc và hướng dẫn chạy',['src/nids_benchmark','scripts','tests','README.md','requirements-analysis.txt']),
        ('SP3','Data inventory và audit dữ liệu',['artifacts/data/data_manifest.json','docs/evidence/dot_02/DATA_CONTRACT.md']),
        ('SP4','Preprocessor đã lưu',['results/runs/CS-RF-S42/model_bundle.joblib']),
        ('SP5','Bốn model/cấu hình, đủ 80 run',['configs/experiment_matrix.yaml','docs/protocol/RUN_MATRIX.csv','results/runs']),
        ('SP6','Closed-set và ba LOACO, năm seed',[pr+'OPERATING_POINTS_ALL_RUNS.csv',pr+'AP_MEAN_STD.csv']),
        ('SP7','Bảng/hình sinh từ artifact khóa',[diag+'FINAL_DIAGNOSTICS_AUDIT.json','scripts/prepare_final_diagnostic_chapter.py']),
        ('SP8','Prototype có so sánh và giải thích',['demo/index.html','src/nids_benchmark/demo.py','docs/evidence/dot_04/demo_20261025/DEMO_UI_AUDIT.json']),
        ('SP9','Slide và câu hỏi phản biện',['docs/presentation_20261025/presentation.pdf','docs/team_guide_20261025/guide.pdf']),
        ('SP10','Demo kịch bản, nguồn dữ liệu, bản đồ code và phiếu tự nhận xét',['demo/lab.html','demo/cases/catalog.json','src/nids_benchmark/application.py','docs/application_20261026/report.pdf','docs/evidence/dot_04/application_20261026/APPLICATION_AUDIT.json','docs/evidence/dot_04/application_20261026/APPLICATION_UI_AUDIT.json']),
    ]:item(code,title,'Đã chuẩn bị / kiểm kỹ thuật',paths,'Chưa thay duyệt nội dung, tự chạy và nộp bài của nhóm.')
    for code,title,status,paths,note in [
        ('T1','Support Normal và 9 category','Có bằng chứng',['artifacts/data/data_manifest.json'],'Bảng Chương 3 báo cáo tổng.'),
        ('T2','Phần cứng, thư viện, seed, feature version','MỘT PHẦN',['results/runs/CS-RF-S42/run.json',diag+'HARDWARE_CURRENT.json'],'Có phiên bản/seed/config; không có phần cứng train lịch sử. Máy đo suy luận hiện tại được ghi riêng.'),
        ('T3','Cấu hình bốn mô hình','Có bằng chứng',['configs/experiment_matrix.yaml','src/nids_benchmark/models.py'],'Cấu hình/bundle giữ nguyên.'),
        ('T4','Closed-set P/R/F1/FPR/AP','Có bằng chứng',['docs/report_tong_20261025/main.tex',pr+'AP_MEAN_STD.csv'],'Bảng tổng hợp trong Chương 6; hai target trong CSV.'),
        ('T5','LOACO Reconnaissance, hai target','Có bằng chứng',[pr+'OPERATING_POINTS_MEAN_STD.csv'],'Known Recall/UADR/FPR, mean/sample std n=5.'),
        ('T6','LOACO DoS, hai target','Có bằng chứng',[pr+'OPERATING_POINTS_MEAN_STD.csv'],'Cùng định nghĩa metric và scope.'),
        ('T7','LOACO Exploits, hai target','Có bằng chứng',[pr+'OPERATING_POINTS_MEAN_STD.csv'],'Cùng định nghĩa metric và scope.'),
        ('T8','Detection theo attack category','Có bằng chứng',[cat+'CATEGORY_ERRORS_MEAN_STD.csv',diag+'CATEGORY_DETECTION_HEATMAP.png'],'Detection=1-FN/support Attack.'),
        ('T9','Train/inference time và kích thước','MỘT PHẦN',[diag+'RUNTIME_SIZE_ALL_RUNS.csv',diag+'RUNTIME_SIZE_MEAN_STD.csv'],'Không có train-only/inference cũ. Có duration toàn run, bundle bytes và phép đo mới 80 bundle (warm-up1/repeat3). Không gọi tổng run là train time.'),
        ('T10','Lỗi role/category/proto/service/state','Có bằng chứng',[cat+'CATEGORY_ERRORS_ALL_RUNS.csv',diag+'GROUP_ERRORS_ALL_RUNS.csv',diag+'NEAR_THRESHOLD_EXAMPLES_S42.csv'],'Mẫu số từng role/nhóm; không suy diễn nhân quả.'),
    ]:item(code,title,status,paths,note)
    for code,title,paths in [
        ('H1','UADR hai target và sai số',[diag+'UADR_BOTH_TARGETS.png']),
        ('H2','Known Recall và UADR theo FPR quan sát',[diag+'TRADEOFF_KNOWN_RECALL.png',diag+'TRADEOFF_UADR.png']),
        ('H3','PR closed-set bốn model',[pr+'PR_CS_all_S42.png']),
        ('H4','Score theo role và threshold, đủ ba LOACO',[pr+f'SCORE_ECDF_{s}_S42.png' for s in ['LR','LD','LE']]),
        ('H5','Confusion CS và ba LOACO',[diag+'CONFUSION_ALL_SCENARIOS_S42.png']),
        ('H6','Category detection heatmap',[diag+'CATEGORY_DETECTION_HEATMAP.png']),
        ('H7','Metric theo seed',[diag+'SEED_STABILITY.png']),
        ('H8','RF/XGB feature importance',['docs/evidence/dot_03/features_20261025/FEATURES_CS.png','docs/evidence/dot_03/features_20261025/FEATURE_IMPORTANCE_MEAN_STD.csv']),
    ]:item(code,title,'Có bằng chứng',paths,'Script/CSV nguồn giữ cùng evidence; hình chính có trong PDF.')
    for code,title in [('P1','Normal/Attack'),('P2','Score và threshold'),('P3','Model/run/seed'),('P4','Feature hoặc giải thích score phù hợp'),('P5','So sánh bốn model cùng CSV')]:
        item(code,title,'Đã kiểm tự động',['docs/evidence/dot_04/demo_20261025/DEMO_UI_AUDIT.json','tests/test_demo_inference.py'],'Importance RF/XGB là toàn model, không giải thích nhân quả từng record.')
    for i,(title,paths,note) in enumerate([
        ('Protocol',['docs/protocol/GATE_1_CHECKLIST.md','docs/protocol/RUN_MATRIX.csv'],'Ma trận/RQ/split có kiểm kỹ thuật. Không tạo phê duyệt giảng viên hoặc ký thay nhóm.'),
        ('Data',['docs/protocol/GATE_2_CHECKLIST.md','artifacts/data/data_manifest.json'],'Hash/schema/support đã kiểm; xem lại nội dung và giới hạn theo phần Anh.'),
        ('Pipeline',['tests/test_preprocessing.py'] if (ROOT/'tests/test_preprocessing.py').exists() else ['tests'],'46 test hiện tại đạt trong venv mới ngày 26/10. Chưa thay tự chạy của thành viên.'),
        ('Baselines',['docs/evidence/dot_03/overlap_20261025/OVERLAP_AUDIT.json'],'Đủ 80 run/320 artifact; không huấn luyện lại.'),
        ('LOACO',[diag+'FINAL_DIAGNOSTICS_AUDIT.json',pr+'PR_SCORE_AUDIT.json'],'Ba held-out, mean/std, error analysis. T2/T9 còn thiếu log lịch sử như nêu trên.'),
        ('Prototype',['docs/evidence/dot_04/demo_20261025/DEMO_AUDIT.json','docs/evidence/dot_03/session_20261025/CLEAN_ENV_HANDOFF_AUDIT.json'],'16 bundle/32 case/3.200 dự đoán, thêm so sánh/explanation UI. ZIP giải nén đã kiểm lại trong venv mới không dùng user-site trên cùng máy Windows; chưa thử máy vật lý khác.'),
        ('Report',['docs/report_tong_20261025/build/main.pdf'],'Đã compile/render và truy vết bảng; cả nhóm cần đọc, sửa và chọn bản nộp.'),
    ],1):item(f'G{i}',title,'Có kiểm kỹ thuật; CHƯA ký duyệt thay người',paths,note)
    inventory=json.loads((ROOT/'docs/evidence/dot_03/overlap_20261025/OVERLAP_AUDIT.json').read_text(encoding='utf-8'))['inputs']
    mismatches=[x['path'] for x in inventory if digest(ROOT/x['path'])!=x['sha256']]
    assert not mismatches,mismatches
    (OUT/'FROZEN_INPUTS_RECHECK.json').write_text(json.dumps(dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),frozen_inputs_checked=len(inventory),matched=True,mismatches=[],includes='80 runs x 4 artifacts, two raw CSV and original diagnostic source/config evidence'),indent=2),encoding='utf-8')
    result=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),requirements=rows,
        unfilled_historical_evidence=['T2: original training hardware','T9: isolated original train/inference durations'],
        human_pending=['Cả ba đọc/sửa, tự giải thích và tự chạy phần của mình','Ghi đóng góp thật và review thật','Nhóm duyệt bản nộp','Nộp đúng thông báo môn'],
        source_limit='S07 chỉ đọc/đối chiếu abstract; không viện dẫn toàn văn chưa có',external_delivery='NOT SENT / NOT SUBMITTED by this preparation')
    (OUT/'DOI_CHIEU_YEU_CAU.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    body=''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [r['code'],r['requirement'],r['status'],r['note'],'; '.join(r['evidence'])])+'</tr>' for r in rows)
    text='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Đối chiếu yêu cầu toàn đề tài</title><style>body{font:17px/1.6 "Segoe UI",sans-serif;margin:30px;color:#293b32}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd6c6;padding:12px;text-align:left;vertical-align:top}td:last-child{font:13px/1.5 Consolas,monospace;overflow-wrap:anywhere;max-width:360px}th{background:#e6edde}.wrap{overflow:auto}</style><h1>Đã chuẩn bị những gì, còn chỗ nào cần nói rõ?</h1><p>Ngày kiểm 25/10/2026. Có bản nháp, code, model, phân tích, demo và tài liệu trình bày để nhóm xem dần. Chưa phải xác nhận cả nhóm đã duyệt/nộp.</p><p><b>Hai mục thiếu bằng chứng lịch sử:</b> T2 chưa có phần cứng train cũ; T9 chưa có thời gian train/inference cũ tách riêng. Đã có thời gian tổng run, kích thước bundle và phép đo suy luận hiện tại; không điền thay số thiếu. S07 chỉ dùng abstract.</p><p><b>Cả ba còn làm:</b> đọc/sửa, tự giải thích và tự chạy phần của mình; ghi đóng góp/review thật rồi chọn bản nộp. Đợt 1–2 giữ nguyên. Chưa gửi nhóm hoặc giảng viên bằng công cụ trong bước chuẩn bị này.</p><div class="wrap"><table><thead><tr><th>Mã</th><th>Yêu cầu</th><th>Trạng thái</th><th>Cách hiểu</th><th>Bằng chứng trong repo</th></tr></thead><tbody>'''+body+'</tbody></table></div></html>'
    (OUT/'DOI_CHIEU_YEU_CAU.html').write_text(text,encoding='utf-8')
    print(f'Checked {len(rows)} requirements and {len(inventory)} frozen hashes; T2/T9 explicitly partial; human review open.')


if __name__=='__main__':main()
