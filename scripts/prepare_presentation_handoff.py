"""Create an offline deck and a plain-language team guide from audited results."""
from pathlib import Path
import hashlib
import html
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'docs/presentation_20261025'
GUIDE = ROOT / 'docs/team_guide_20261025'
PR = ROOT / 'docs/evidence/dot_03/pr_scores_20261022'
OVERLAP = ROOT / 'docs/evidence/dot_03/overlap_20261025'
FEATURES = ROOT / 'docs/evidence/dot_03/features_20261025'


def esc(value):
    return html.escape(str(value))


def table(headers, rows):
    return '<table><thead><tr>' + ''.join(f'<th>{esc(x)}</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{esc(x)}</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table>'


def cards(items):
    return '<div class="grid">' + ''.join(f'<div class="card"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in items) + '</div>'


def bullets(items):
    return '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in items) + '</ul>'


def pct(row, metric):
    return f'{100 * row[metric + "_mean"]:.2f} ± {100 * row[metric + "_std"]:.2f}'


CSS = r'''
/* Viewport-safe base; print shows every slide, screen uses scroll snapping. */
*{box-sizing:border-box}html,body{height:100%;overflow-x:hidden;margin:0}
html{scroll-snap-type:y mandatory;scroll-behavior:smooth}
:root{--title-size:clamp(1.5rem,4.4vw,3.7rem);--h2-size:clamp(1.25rem,3.3vw,2.8rem);--h3-size:clamp(1rem,2vw,1.7rem);--body-size:clamp(.9rem,1.75vw,1.55rem);--small-size:clamp(.7rem,1vw,1rem);--slide-padding:clamp(1rem,4vw,4rem);--content-gap:clamp(.6rem,1.7vw,1.8rem);--element-gap:clamp(.3rem,1vw,1rem);--ink:#293b32;--paper:#f8f6ef;--green:#35654e}
body{background:var(--paper);color:var(--ink);font-family:'Segoe UI',Arial,sans-serif}
.slide{width:100vw;height:100vh;height:100dvh;overflow:hidden;scroll-snap-align:start;display:flex;flex-direction:column;position:relative;border-top:clamp(4px,.7vh,8px) solid var(--green)}
.slide-content{flex:1;display:flex;flex-direction:column;justify-content:center;max-height:100%;overflow:hidden;padding:var(--slide-padding);gap:var(--content-gap);min-height:0}
.eyebrow{font-size:var(--small-size);letter-spacing:.1em;text-transform:uppercase;color:#627665;margin:0}
h1,h2,h3,p,ul{margin:0}h1{font:600 var(--title-size)/1.16 Georgia,'Times New Roman',serif;max-width:23ch}h2{font:600 var(--h2-size)/1.15 Georgia,'Times New Roman',serif;max-width:32ch}h3{font-size:var(--h3-size);line-height:1.25}p,li{font-size:var(--body-size);line-height:1.45}ul{padding-left:1.25em;display:grid;gap:var(--element-gap)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:clamp(.5rem,1.5vw,1rem)}
.card{padding:clamp(.6rem,1.4vw,1.4rem);border:1px solid #cdd7c9;border-radius:clamp(4px,.6vw,10px);background:#fffdf8;max-width:min(90vw,1300px);max-height:min(80vh,700px)}.card p{margin-top:var(--element-gap)}
.note{border-left:clamp(2px,.3vw,4px) solid #ac795d;padding-left:var(--element-gap);font-size:var(--body-size)}
table{width:100%;border-collapse:collapse;font-size:var(--body-size);font-variant-numeric:tabular-nums}th,td{text-align:left;padding:clamp(.35rem,1vw,.9rem) clamp(.3rem,1.2vw,1rem);border-bottom:1px solid #d6dece}th{color:var(--green);font-weight:600;background:#eaf0e3}td:not(:first-child),th:not(:first-child){white-space:nowrap}
.source{font-size:var(--small-size);line-height:1.35;color:#596c5d;overflow-wrap:anywhere;margin-top:auto;padding-top:var(--element-gap)}
.slide-footer{display:flex;justify-content:space-between;gap:var(--element-gap);font-size:var(--small-size);color:#596c5d;padding:0 var(--slide-padding) clamp(.6rem,1.2vh,1rem)}
.cover{background:#e8eee2}.cover .subtitle{max-width:52ch}.formula{font:600 clamp(1.6rem,4vw,3rem)/1.2 Georgia,serif;color:var(--green)}.reveal{opacity:1;transform:none}.seen .reveal{animation:enter .35s ease both}@keyframes enter{from{opacity:.4;transform:translateY(8px)}to{opacity:1;transform:none}}
nav{position:fixed;right:clamp(.6rem,2vw,2rem);bottom:clamp(.5rem,1vh,1rem);z-index:4;display:flex;align-items:center;gap:.35rem;background:#f8f6eff2;border:1px solid #cdd7c9;border-radius:5px;padding:.2rem .4rem;font-size:12px}button{font:inherit;background:none;border:0;color:var(--ink);cursor:pointer;padding:.3rem .45rem}button:focus-visible{outline:2px solid var(--green)}#progress{width:4ch;text-align:center}
@media(max-height:700px){:root{--slide-padding:clamp(.8rem,3vw,2rem);--content-gap:clamp(.5rem,1.5vw,1rem);--title-size:clamp(1.5rem,4.2vw,2.8rem);--h2-size:clamp(1.25rem,3vw,2rem)}}
@media(max-height:600px){:root{--slide-padding:clamp(.65rem,2.5vw,1.5rem);--content-gap:clamp(.35rem,1vw,.75rem);--body-size:clamp(.85rem,1.6vw,1rem);--h3-size:clamp(.9rem,1.8vw,1.15rem)}}
@media(max-height:500px){:root{--slide-padding:clamp(.5rem,2vw,1rem);--h2-size:clamp(1.15rem,2.5vw,1.5rem);--body-size:clamp(.8rem,1.8vw,.95rem);--small-size:clamp(.65rem,1.1vw,.8rem);--content-gap:clamp(.3rem,.9vw,.6rem)}.card{padding:.5rem}th,td{padding:.3rem .4rem}.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){:root{--title-size:clamp(1.7rem,7vw,2.5rem);--h2-size:clamp(1.4rem,6.2vw,2rem);--h3-size:clamp(1rem,4vw,1.2rem);--body-size:clamp(.9rem,3.7vw,1rem);--small-size:clamp(.67rem,2.7vw,.8rem)}.grid{grid-template-columns:1fr}.card p{margin-top:.2rem}table{font-size:clamp(.72rem,3vw,.85rem)}th,td{padding:.45rem .2rem}.slide-footer{padding-right:7rem}}
@media(max-width:600px) and (min-height:500px){:root{--slide-padding:1rem;--content-gap:.6rem}.grid{gap:.5rem}.card{padding:.5rem}.card p{line-height:1.3}.source{line-height:1.2}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}html{scroll-behavior:auto}}
@page{size:13.333333in 7.5in;margin:0}
@media print{html,body{height:auto;overflow:visible;scroll-snap-type:none}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}.slide{width:13.333333in;height:7.5in;break-after:page;page-break-after:always}.slide:last-of-type{break-after:auto}nav{display:none}.slide-content{padding:36px 54px;gap:18px}h1{font-size:46px}h2{font-size:36px}h3{font-size:24px}p,li,table,.note{font-size:20px}.source,.eyebrow,.slide-footer{font-size:12px}.slide-footer{padding:0 54px 20px}.card{padding:18px}.grid{grid-template-columns:repeat(2,1fr)}.reveal{animation:none!important}}
'''

JS = r'''
class PresentationController {
 constructor(){this.slides=[...document.querySelectorAll('.slide')];this.index=0;this.lock=0;
 const observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){this.index=this.slides.indexOf(e.target);e.target.classList.add('seen');document.getElementById('progress').textContent=`${this.index+1}/${this.slides.length}`;}},{threshold:.55});this.slides.forEach(s=>observer.observe(s));
 document.addEventListener('keydown',e=>{if(['ArrowDown','ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();this.go(1)}if(['ArrowUp','ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();this.go(-1)}if(e.key==='Home'){e.preventDefault();this.to(0)}if(e.key==='End'){e.preventDefault();this.to(this.slides.length-1)}});
 window.addEventListener('wheel',e=>{if(Math.abs(e.deltaY)>10){e.preventDefault();if(Date.now()>this.lock){this.go(Math.sign(e.deltaY));this.lock=Date.now()+500}}},{passive:false});
 let start=0;window.addEventListener('touchstart',e=>{start=e.changedTouches[0].clientY},{passive:true});window.addEventListener('touchend',e=>{const d=start-e.changedTouches[0].clientY;if(Math.abs(d)>50)this.go(Math.sign(d))},{passive:true});
 document.getElementById('prev').onclick=()=>this.go(-1);document.getElementById('next').onclick=()=>this.go(1);
 }to(i){this.index=Math.max(0,Math.min(this.slides.length-1,i));this.slides[this.index].scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});}go(d){this.to(this.index+d)}
}
window.deck=new PresentationController();
'''


def main():
    DECK.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    points = pd.read_csv(PR / 'OPERATING_POINTS_MEAN_STD.csv', float_precision='round_trip')
    aps = pd.read_csv(PR / 'AP_MEAN_STD.csv', float_precision='round_trip')
    slices = pd.read_csv(OVERLAP / 'OVERLAP_MEAN_STD.csv', float_precision='round_trip')
    features = pd.read_csv(FEATURES / 'FEATURE_IMPORTANCE_MEAN_STD.csv', float_precision='round_trip')
    data_manifest = json.loads((ROOT/'artifacts/data/data_manifest.json').read_text(encoding='utf-8'))
    sources = []
    metric_cells = []
    for p in (PR/'OPERATING_POINTS_MEAN_STD.csv', PR/'AP_MEAN_STD.csv', OVERLAP/'OVERLAP_MEAN_STD.csv', FEATURES/'FEATURE_IMPORTANCE_MEAN_STD.csv', ROOT/'artifacts/data/data_manifest.json'):
        sources.append(dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    def point(scenario, model, target=.05):
        return points[(points.scenario==scenario)&(points.model==model)&(points.target_fpr==target)].iloc[0]
    def metric(scenario, model, target, name):
        text = pct(point(scenario, model, target), name)
        metric_cells.append(dict(scenario=scenario,model=model,target=target,metric=name,text=text))
        return text
    slides=[]
    def slide(title, body, note, source, speaker, say, cover=False):
        slides.append(dict(title=title,body=body,note=note,source=source,speaker=speaker,say=say,cover=cover))
    slide('So sánh bốn mô hình phát hiện xâm nhập mạng', '<p class="subtitle">UNSW-NB15 · Closed-set và ba kịch bản LOACO</p>',
          'Trịnh Trâm Anh · Hoàng Văn Vương Thu · Nguyễn Trọng Tín', 'Bản chuẩn bị 25/10/2026 · chờ cả nhóm đọc, sửa và duyệt', 'Cả nhóm',
          'Nhóm so sánh hai mô hình học từ Normal và Attack với hai mô hình chỉ học Normal. Bài tập trung vào khả năng phát hiện và số lần báo nhầm trên một benchmark cụ thể.', True)
    slide('Mình muốn trả lời ba câu hỏi', cards([
        ('RQ1 · Nhận ra Attack?', 'Khi các lớp tấn công đều có trong phát triển mô hình, kết quả ra sao?'),
        ('RQ2 · Giấu một lớp?', 'Bỏ một attack class khỏi phát triển, rồi đo recall riêng lớp đó (UADR).'),
        ('RQ3 · Đổi ngưỡng?', 'Đổi target FPR validation 1% → 5%; xem mức phát hiện và FPR test đổi thế nào.')]),
        'Mỗi câu hỏi gắn với bảng/run cụ thể.', 'docs/protocol/RQ_TO_EVIDENCE.md · cách diễn đạt RQ3 theo operating points thực tế', 'Trâm Anh',
        'RQ2 giống một bài kiểm tra có một dạng chưa xuất hiện lúc học. Đây là held-out class trong dữ liệu, chưa phải chứng minh phát hiện mọi zero-day ngoài đời.')
    train = data_manifest['files']['train']['audit']['rows']; test = data_manifest['files']['test']['audit']['rows']
    slide('Dữ liệu mình đang dùng', cards([
        (f'Train · {train:,} dòng', 'Official training subset; chia development train/validation theo từng seed.'),
        (f'Test · {test:,} dòng', '37.000 Normal và 45.332 Attack; giữ nguyên để đánh giá.'),
        ('42 feature gốc', '39 numeric; proto, service, state là categorical.'),
        ('3 cột chỉ để đối chiếu', 'id, label, attack_cat không đưa vào mô hình.')]),
        'Dữ liệu trùng feature là một giới hạn cần đọc cùng kết quả.', 'artifacts/data/data_manifest.json · S03/S13 trong ma trận nguồn', 'Trâm Anh',
        'Một dòng là bản ghi flow đã được tổng hợp. Mình không đưa nhãn hay mã ID vào cho mô hình đoán; ba cột đó chỉ dùng truy vết và đánh giá.')
    slide('Từ một dòng CSV đến cảnh báo', '<p class="formula">Feature → tiền xử lý → score → ngưỡng → Normal / Attack</p>' + bullets([
        'Fit imputer, scaler và one-hot trên đúng vùng train của mô hình.',
        'Dùng preprocessor đã lưu cho validation, test và demo.',
        'Score cao hơn nghĩa là giống Attack/anomaly hơn.']),
        'Cảnh báo cần người kiểm tra tiếp; chưa phải xác nhận đã có sự cố.', 'src/nids_benchmark/ · báo cáo tổng Chương 4–5', 'Trọng Tín',
        'Tiền xử lý phải học từ train trước rồi dùng lại nguyên trạng. Demo cũng dùng bundle cũ, vì fit lại lúc chạy demo sẽ đổi bài toán mình đã đo.')
    slide('Hai cách học, bốn baseline', cards([
        ('RF · Random Forest', 'Nhiều cây bỏ phiếu; fit Normal và Attack đã biết.'),
        ('XGB · XGBoost', 'Cây học nối tiếp để giảm lỗi; fit Normal và Attack đã biết.'),
        ('IF · Isolation Forest', 'Fit chỉ Normal; dễ bị cô lập hơn thì bất thường hơn.'),
        ('AE · Autoencoder', 'Fit chỉ Normal; lỗi tái tạo lớn hơn thì bất thường hơn.')]),
        'Score khác thang giữa các model; không so trực tiếp hai giá trị score.', 'Báo cáo tổng Chương 2, 5 · src/nids_benchmark/models.py', 'Vương Thu',
        'Học chỉ Normal không tự bảo đảm phát hiện tấn công tốt hơn. Mình phải đọc recall và FPR thực tế, đồng thời nhớ hai họ dùng dữ liệu fit khác nhau.')
    slide('Target 5% đặt ở validation', '<p class="formula">score ≥ ngưỡng ⇒ báo Attack</p>' + bullets([
        'Chọn ngưỡng thấp nhất vẫn thỏa ngân sách trên Normal validation.',
        'Giữ nguyên ngưỡng khi đo test; không chọn lại từ đường PR test.',
        'Test có thể báo nhầm cao hơn hoặc thấp hơn target.']),
        'Tăng target cho phép nhiều cảnh báo hơn; cần xem cả phần bắt được và báo nhầm.', 'src/nids_benchmark/evaluation.py · run.json: threshold_policy', 'Trọng Tín',
        'Ví dụ target 5% chỉ nói ngân sách đặt trên validation. Mình không thể nói mô hình sẽ báo nhầm đúng 5% khi đem sang tập test hoặc mạng thực tế.')
    slide('80 lượt chạy, cùng một protocol', table(['Kịch bản','Lớp bị giữ lại khỏi phát triển'],[
        ['CS','Không giữ lại'],['LR','Reconnaissance'],['LD','DoS'],['LE','Exploits']]) + '<p>4 kịch bản × 4 model × 5 seed = 80 run</p>',
        'Seed: 42, 52, 62, 72, 82. Mỗi run có hai operating points 1% / 5%.', 'docs/protocol/RUN_MATRIX.csv · configs/experiment_matrix.yaml', 'Trọng Tín',
        'Bỏ lớp held-out trước khi chia development. Năm seed vẫn dùng cùng official test, nên mean và sample std không phải năm lần kiểm trên năm dữ liệu độc lập.')
    rows = [[m, metric('CS',m,.05,'recall'), metric('CS',m,.05,'fpr')] for m in ('RF','XGB','IF','AE')]
    slide('Closed-set: bắt được và báo nhầm', table(['Model','Recall Attack (%)','FPR test (%)'],rows),
        'Target validation 5% · mean ± sample std, 5 seed. Support: 45.332 Attack / 37.000 Normal.', 'PR_SCORE/OPERATING_POINTS_MEAN_STD.csv · scenario=CS, target_fpr=0.05', 'Vương Thu',
        'RF và XGB bắt được nhiều Attack hơn trong phép đo này, đồng thời báo nhầm Normal nhiều hơn. Mình không kết luận thắng tuyệt đối từ một cột recall.')
    support = data_manifest['files']['test']['audit']['attack_category_counts']
    for scenario, label in [('LR','Reconnaissance'),('LD','DoS'),('LE','Exploits')]:
        rows=[[m,metric(scenario,m,.05,'uadr'),metric(scenario,m,.05,'fpr')] for m in ('RF','XGB','IF','AE')]
        slide(f'LOACO · giấu {label}', table(['Model','UADR (%)','FPR test (%)'],rows),
              f'Target validation 5% · mean ± sample std, 5 seed. Held-out: {support[label]:,} mẫu; Normal: 37.000.',
              f'PR_SCORE/OPERATING_POINTS_MEAN_STD.csv · scenario={scenario}, target_fpr=0.05', 'Vương Thu',
              f'UADR chỉ đếm {label} đã bị giấu khỏi phát triển. Khi so hai mô hình, mình đọc kèm FPR test vì chúng không có cùng mức báo nhầm trên test dù target validation giống nhau.')
    rows=[[f'{m} · {int(t*100)}%',metric('CS',m,t,'recall'),metric('CS',m,t,'fpr')] for m in ('RF','IF') for t in (.01,.05)]
    slide('Đổi target: được gì, đổi lại gì?',table(['Model · target val.','Recall (%)','FPR test (%)'],rows),
          'CS · mean ± sample std, 5 seed; support như slide closed-set. Cùng target chưa phải cùng FPR test.',
          'PR_SCORE/OPERATING_POINTS_MEAN_STD.csv · CS, RF/IF, target=0.01/0.05', 'Vương Thu',
          'Khi cho ngân sách lớn hơn, ngưỡng giảm nên recall và FPR đều có thể tăng. Đây là trade-off; kết quả không xác định model thắng ở một FPR test đã được ghép bằng nhau.')
    ap_rows=[]
    for m in ('RF','XGB'):
        vals=[]
        for scope in ('all','normal_vs_heldout'):
            r=aps[(aps.scenario=='LR')&(aps.model==m)&(aps.scope==scope)].iloc[0]
            vals.append(f'{r.ap_mean:.4f} ± {r.ap_std:.4f}')
        ap_rows.append([m]+vals)
    slide('AP cao toàn test vẫn có chỗ khó',table(['Model','AP toàn test','AP Normal/held-out'],ap_rows),
          'LR · 5 seed. Toàn test: 82.332 mẫu; Normal/held-out: 40.496 mẫu (3.496 held-out). Khác prevalence.',
          'PR_SCORE/AP_MEAN_STD.csv · LR. AP=average_precision_score; khử bản sao hai target.', 'Vương Thu',
          'Toàn test có cả attack đã biết. Khi chỉ giữ Normal và Reconnaissance, AP thấp hơn; điều này giúp thấy phép đo tổng có thể che phần khó. AP không phụ thuộc một threshold cụ thể.')
    r=slices[(slices.scenario=='LR')&(slices.model=='RF')&(slices.cohort=='unmatched')&(slices.target_fpr==.05)].iloc[0]
    slide('Đọc kết quả cùng giới hạn overlap',cards([
        ('Matched là gì?', '42 feature raw trùng chính xác một vector trong tập fit thực tế của model.'),
        ('LR / RF · held-out unmatched', f'UADR {pct(r,"uadr")}% · {int(r.heldout_min):,}–{int(r.heldout_max):,} mẫu qua 5 seed; target validation 5%.')]),
          'Phân tích hậu nghiệm. Không xóa overlap, không retrain; chưa chứng minh quan hệ nhân quả.',
          'OVERLAP/OVERLAP_MEAN_STD.csv · fit theo model/seed; IF/AE không có held-out matched.', 'Trâm Anh',
          'RF vẫn bắt được nhiều held-out ở nhóm không exact match. Tuy vậy unmatched chưa bảo đảm dữ liệu độc lập hoàn toàn; các tương đồng khác vẫn có thể tồn tại. UADR matched IF/AE thiếu mẫu nên không xác định, không phải bằng 0.')
    feat_rows=[]
    for m in ('RF','XGB'):
        top=features[(features.scenario=='CS')&(features.model==m)].nlargest(3,'importance_mean')
        feat_rows.append([m, ', '.join(top.feature)])
    slide('Feature nào được model sử dụng nhiều?',table(['Model · CS','Ba feature đứng đầu theo mean importance'],feat_rows),
          '5 seed. RF: giảm impurity; XGB: gain; gộp one-hot về feature gốc.',
          'FEATURES/FEATURE_IMPORTANCE_MEAN_STD.csv · importance mô tả, không là nguyên nhân.', 'Trâm Anh',
          'Hai model có hai định nghĩa importance khác nhau. Bảng cho biết vai trò tương đối trong model đã học, chưa giải thích nguyên nhân một dòng bị dự đoán sai và chưa chứng minh quan hệ nhân quả.')
    examples=pd.read_csv(ROOT/'docs/evidence/dot_02/category_errors_20261014/ERROR_EXAMPLES_CS_S42.csv',float_precision='round_trip')
    chosen=examples[examples.run_id.isin(['CS-RF-S42','CS-IF-S42'])].sort_values('record_id').groupby(['run_id','error_type']).head(1)
    rows=[[r.run_id.replace('CS-','').replace('-S42',''),int(r.record_id),r.error_type,f'{r.score:.6f}',f'{r.threshold:.6f}'] for r in chosen.itertuples()]
    slide('Một FP và một FN để tự giải thích',table(['Model','ID','Lỗi','Score','Ngưỡng'],rows),
          'CS · seed 42 · target validation 5%. FP: Normal báo Attack; FN: Attack báo Normal.',
          'ERROR_EXAMPLES_CS_S42.csv · ID nhỏ nhất mỗi nhóm RF/IF FP/FN; ví dụ không đại diện mọi lỗi.', 'Vương Thu',
          'Đọc nhãn thật trước, rồi so score với ngưỡng. RF ID 1 là Normal nhưng vượt ngưỡng nên FP; IF ID 244 là Reconnaissance nhưng dưới ngưỡng nên FN. Không so score của RF với score của IF.')
    slide('Demo: dùng lại mô hình đã lưu',bullets([
        'Dùng 100 dòng mẫu → chọn CS / RF / 5% → chạy.',
        'Xem score, ngưỡng, FP/FN; đổi một lựa chọn mỗi lần.',
        'Tải CSV để đối chiếu; mẫu giúp giải thích luồng suy luận.']),
          '16 bundle seed 42 · kiểm 32 trường hợp, 3.200 nhãn dự đoán. CSV, chưa bắt gói mạng trực tiếp.',
          'DEMO/DEMO_AUDIT.json · max lệch score 2,20e−7 < 1e−6; nhãn/ngưỡng khớp baseline.', 'Trọng Tín',
          'Mẫu chọn 10 ID nhỏ nhất mỗi category, không lấy tỷ lệ đúng của mẫu làm thành tích nghiên cứu. Máy khác cần cài đúng môi trường; số kiểm kỹ thuật không chứng minh model hiệu quả ngoài thực tế.')
    slide('Kết luận cần giữ đúng phạm vi',bullets([
        'Một official split UNSW-NB15; ba lớp held-out hữu hạn.',
        'FPR validation và FPR test khác nhau; năm seed dùng cùng test.',
        'Overlap, prevalence và vùng fit ảnh hưởng cách so sánh.',
        'Chưa đo live traffic, độ trễ hoặc dataset ngoài; S07 mới dùng abstract.']),
          'Không khẳng định phát hiện mọi zero-day hoặc sẵn sàng triển khai vận hành.',
          'Báo cáo tổng Chương 3, 7–9 · ma trận nguồn S07 và S12', 'Trâm Anh',
          'Điểm mạnh của bài là protocol chung, trace được số liệu và giải thích giới hạn. Muốn kết luận rộng hơn cần thiết kế đánh giá độc lập, chứ chưa thể suy ra từ bộ test hiện tại.')
    slide('Điều bài nghiên cứu cho thấy',cards([
        ('RQ1', 'Trong CS, RF/XGB có recall cao hơn và FPR test cũng cao hơn trong cấu hình đã đo.'),
        ('RQ2', 'UADR thay đổi theo lớp held-out; anomaly detection không luôn tốt hơn supervised.'),
        ('RQ3', 'Tăng target validation làm đổi trade-off; không giữ cố định được FPR test.')]),
          'Báo cáo, CSV và demo cùng dùng 80 run đã khóa; không chọn lại ngưỡng từ test.',
          'Bảng điểm vận hành/AP/overlap và các run ID đã chỉ ở từng slide', 'Cả nhóm',
          'Nhóm không chỉ chọn một model thắng. Nhóm chỉ ra điều kiện so sánh và trade-off, có artifact để kiểm lại, cùng những điều kết quả chưa chứng minh được.')
    slide('Cả nhóm đọc dần theo phần này',cards([
        ('Anh · dữ liệu / nguồn', 'Báo cáo tổng Chương 3, overlap Chương 7, nguồn. Kiểm một bảng và nguồn đi kèm.'),
        ('Thu · kết quả / lỗi', 'Chương 6–7 và ví dụ Chương 8. Giải thích một FP, một FN và trade-off.'),
        ('Tín · protocol / demo', 'Chương 4–5 và 8. Tự chạy demo, gom góp ý để sửa một bản chung.')]),
          'Nhắn: “Mình xem trang…, hiểu là…, muốn sửa / hỏi…”. Online trước, rảnh thì cùng ra quán.',
          'Phần nói là gợi ý để tập; chưa ghi nhận đã đọc, đã làm hoặc đã review thay ai.', 'Cả nhóm',
          'Mỗi bạn không cần đọc cả bộ trong một buổi. Bắt đầu đúng phần rồi giải thích lại bằng lời mình; phần nào chưa hiểu thì ghi lại để cùng xử lý.')
    sections=[]
    for i,s in enumerate(slides,1):
        tag='h1' if s['cover'] else 'h2'
        sections.append(f'<section class="slide {"cover" if s["cover"] else ""}" aria-label="Slide {i}: {esc(s["title"])}"><div class="slide-content"><p class="eyebrow">TLCN · UNSW-NB15 · {esc(s["speaker"])}</p><{tag}>{esc(s["title"])}</{tag}><div class="reveal">{s["body"]}</div><p class="note">{esc(s["note"])}</p><p class="source">Nguồn: {esc(s["source"])}</p></div><footer class="slide-footer"><span>Bản nháp · 25/10/2026</span><span>{i:02d} / {len(slides):02d}</span></footer></section>')
    document='<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NIDS · Bài trình bày của nhóm</title><style>'+CSS+'</style></head><body><main>'+''.join(sections)+'</main><nav aria-label="Chuyển slide"><button id="prev" aria-label="Slide trước">←</button><span id="progress">1/'+str(len(slides))+'</span><button id="next" aria-label="Slide tiếp">→</button></nav><script>'+JS+'</script></body></html>'
    (DECK/'presentation.html').write_text(document,encoding='utf-8')
    (DECK/'noi_dung_slide.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2),encoding='utf-8')

    # Reading copy: short pages, with editable text and no claims of member completion.
    pages=[]
    def page(title, body): pages.append((title,body))
    page('Mở bài nào trước, mình xem gì?', '<p>Bộ bài đã có sẵn nội dung để cả ba đọc, kiểm và sửa dần. Đây là bản chuẩn bị chung ngày 25/10; chưa duyệt nộp, chưa xác nhận mức hiểu hay đóng góp của từng bạn.</p>'+table(['Bạn','Mở báo cáo tổng','Lượt đầu làm một việc'],[
        ['Anh','Chương 3; overlap Chương 7; nguồn','Kiểm một bảng dữ liệu và nguồn đi kèm.'],['Thu','Chương 6–7; ví dụ Chương 8','Đọc một bảng; giải thích một FP/FN.'],['Tín','Chương 4–5 và 8','Thử demo; đối chiếu score với ngưỡng.']])+ '<h2>Gửi góp ý vào nhóm thế nào?</h2><p>“Mình đọc trang …, hiểu là …; chỗ … mình muốn hỏi/sửa vì …; mình đã đối chiếu với …”. Có thể gửi tin nhắn, ảnh ghi chú hoặc Word. Mỗi lần chỉ cần kiểm một phần cho rõ.</p><h2>Nhóm đang có gì?</h2><p>Đợt 1–2 giữ bản đã chốt. Đợt 3 có PR/score, lỗi, overlap và feature; đợt 4 thêm demo; báo cáo tổng trình bày xuyên suốt nghiên cứu. Slide và tài liệu này giúp tập giải thích. Năm ảnh hướng dẫn là bản gọn để gửi Zalo.</p><p>09/11 là mốc đợt 3 đã thống nhất qua nhóm trưởng. Chưa xác nhận lại hạn đợt 4/bản cuối; kế hoạch gốc kết thúc 23/12. Buổi ra quán hẹn khi cả ba rảnh, chưa có ngày cụ thể.</p>')
    for start in range(0,len(slides),5):
        content='<p>Gợi ý lời nói để tập, không cần học thuộc. Cả ba có thể đổi người nói sau khi đọc thử; chưa coi đây là phân công đã nhận hoặc công việc đã hoàn thành.</p>'
        for i,s in enumerate(slides[start:start+5],start+1):
            content+=f'<h2>{i:02d}. {esc(s["title"])} <span>· {esc(s["speaker"])}</span></h2><p>{esc(s["say"])}</p>'
        page(f'Tập nói · slide {start+1}–{min(start+5,len(slides))}',content)
    page('Chạy demo cùng nhau · khoảng 3 phút', '<ol><li>Mở <b>MO_DEMO.ps1</b> trên máy Tín; trang chạy ở <b>http://127.0.0.1:4397/lab</b>. Có sáu mục bằng nút: Thiết lập, Kết quả, Ghi chú, Dữ liệu, Mã xử lý và Hướng dẫn.</li><li>Ở <b>Thiết lập</b>, chọn dữ liệu rồi bấm <b>Tiếp: chọn mô hình</b>. Giữ CS / RF / 5%, bấm <b>Chạy kịch bản</b> để sang Kết quả.</li><li>Dùng <b>Trước/Tiếp</b> để xem từng nhóm dòng; bấm <b>Xem</b> để đọc ID, score, ngưỡng, nhãn và FP/FN. Giải thích vì sao dòng đó là báo nhầm hoặc bỏ sót.</li><li>Giữ model, đổi 5% sang 1%; sau đó thử IF. Chỉ đổi một lựa chọn mỗi lần. Không so trực tiếp score giữa model.</li><li>Sang <b>Ghi chú</b> để tự ghi điều quan sát và lưu JSON/CSV. Muốn dùng CSV riêng hoặc so sánh bốn model, bấm <b>Nhập CSV</b> ở đầu trang.</li></ol><h2>Khi máy chưa chạy được</h2><p>Kiểm server và thư viện đã cài. Máy khác dùng ZIP demo riêng cùng DOC_TRUOC.txt. Không chạy lại training vào results/runs. Có thể dùng ảnh giao diện hoặc bảng lỗi trong báo cáo; nói rõ đó là bản đã lưu, chưa phải lần chạy trực tiếp.</p><h2>Điều cần nhớ</h2><p>Mẫu chọn trước theo ID chỉ để minh họa. Demo đọc flow CSV, chưa bắt gói mạng. Nhãn thật chỉ dùng đối chiếu. Kiểm 1.600 dự đoán ứng dụng và 3.200 dòng CSV là bằng chứng kỹ thuật; chưa thay phần tự chạy và tự nhận xét của thành viên.</p>')
    qa1=[
        ('Tại sao gọi là LOACO?', 'Mỗi scenario loại một attack class khỏi phát triển mô hình rồi đo recall riêng class đó trên official test. Đó là UADR; chưa chứng minh mọi zero-day ngoài thực tế.'),
        ('Test có được dùng chọn ngưỡng không?', 'Không. Ngưỡng lấy từ Normal validation với target 1%/5%, giữ nguyên khi đo test. Đường PR test chỉ được dùng phân tích hậu nghiệm.'),
        ('RF/XGB và IF/AE học dữ liệu nào?', 'RF/XGB học development train có Normal và Attack đã biết. IF/AE chỉ fit Normal của development train. Tiền xử lý cũng fit đúng phạm vi tương ứng.'),
        ('42 feature hay 45 cột?', 'File raw có 45 cột: 42 feature và id/label/attack_cat. Sau one-hot số chiều có thể lớn hơn 42, phụ thuộc category trong vùng fit.'),
        ('Vì sao nói 80 run mà có 160 operating points?', '4 scenario × 4 model × 5 seed là 80 lần fit đã lưu. Mỗi run đánh giá ở hai threshold; không phải huấn luyện 160 lần.'),
        ('Làm sao kiểm một con số?', 'Chọn scenario, model, target và seed hoặc nhóm seed. Mở CSV tương ứng, run.json và metrics/predictions. Các slide đều ghi nguồn, metric và support. Bảng mean/std lấy từ CSV, không gõ lại số.')]
    page('Nếu thầy hỏi về cách làm', ''.join(f'<h2>{esc(q)}</h2><p>{esc(a)}</p>' for q,a in qa1))
    qa2=[
        ('Target 5% mà FPR test cao hơn có sai không?', 'Target áp trên Normal validation. Phân bố test khác nên FPR test có thể khác; phải báo đúng số đo, không gọi target là FPR test đã đạt.'),
        ('Cùng target có so công bằng hoàn toàn không?', 'Đó là cùng chính sách chọn ngưỡng validation; chưa phải cùng operating FPR trên test. Kết luận cần đọc kèm FPR test, recall và support.'),
        ('AP có bằng diện tích hình thang PR không?', 'Code dùng average_precision_score. AP tổng hợp precision theo bước tăng recall, không phải tích phân hình thang. Hai bản sao target phải khử trước khi tính.'),
        ('Unmatched có giải quyết hết leakage chưa?', 'Không. Chỉ loại exact raw feature match khi phân nhóm. Đây là hậu nghiệm giữ nguyên model/score; chưa retrain loại overlap và chưa loại các tương đồng khác.'),
        ('Feature importance có giải thích nguyên nhân FP không?', 'Chưa. RF impurity và XGB gain là mô tả nội tại mô hình; không phải giải thích nhân quả từng bản ghi, cũng có thể chịu bias cardinality.'),
        ('Năm seed và kiểm demo chứng minh gì?', 'Std cho biến thiên theo seed trên cùng official test, chưa là khoảng tin cậy ngoài dữ liệu. Kiểm demo chứng minh suy luận dùng lại bundle khớp prediction trong dung sai; chưa chứng minh hiệu năng vận hành.')]
    page('Nếu thầy hỏi về kết quả và giới hạn', ''.join(f'<h2>{esc(q)}</h2><p>{esc(a)}</p>' for q,a in qa2))
    page('Góp ý thật rồi mới chốt bản nộp', '<p>Không cần ký xác nhận ở tài liệu chuẩn bị sẵn này. Mỗi bạn tự ghi phần thực sự đã đọc/kiểm, câu hỏi và sửa đổi của mình. Phần được hỗ trợ vẫn ghi đúng thực tế.</p>'+table(['Bạn','Trang / bảng / nguồn đã kiểm','Điều hiểu / muốn sửa'],[['Anh','................................','................................'],['Thu','................................','................................'],['Tín','................................','................................']])+ '<h2>Khi cùng xem ở quán</h2>'+bullets(['Mỗi bạn giải thích một bảng hoặc ví dụ; hai bạn còn lại hỏi chỗ chưa rõ.','Chạy thử demo; kiểm lời nói có đúng score/ngưỡng và giới hạn không.','Tín gom sửa một bản chung; Anh kiểm nguồn/dữ liệu; Thu kiểm metric và diễn giải.','Đọc lại PDF và slide sau sửa; nhóm quyết định bản nào dùng nộp.'])+ '<h2>Hồ sơ để tra lại</h2><p>01_Bao_cao: năm báo cáo. 02_Anh_huong_dan: năm ảnh cho Zalo. 05_Bang_so_lieu: CSV và audit. 06_Trinh_bay: slide và tài liệu tập nói. 07_Ma_nguon: bản chụp code/config/tests và hướng dẫn tái lập. ZIP demo riêng chứa 16 bundle seed 42; dữ liệu raw và 80 run gốc vẫn giữ ở local/Drive như hồ sơ cũ.</p><p>Những hướng chưa làm (dataset ngoài, live traffic, retrain loại overlap) là giới hạn/đề xuất nghiên cứu, không tự đổi thành việc thành viên đã hoàn thành. S07 chỉ dùng abstract đã đối chiếu.</p>')
    guide_css='''*{box-sizing:border-box}body{margin:0;background:#e6e9e0;color:#293b32;font:11.2pt/1.48 "Segoe UI",Arial,sans-serif}.page{width:210mm;height:297mm;margin:16px auto;padding:17mm 18mm 15mm;background:#fffdf8;position:relative;overflow:hidden}h1{font:600 23pt/1.15 Georgia,"Times New Roman",serif;margin:0 0 7mm}h2{font-size:12pt;margin:5mm 0 1.4mm;color:#35654e}h2 span{font-size:10pt;font-weight:400;color:#63745f}p{margin:0 0 3mm}table{border-collapse:collapse;width:100%;font-size:9.5pt;margin:4mm 0}th,td{padding:2.5mm 2mm;text-align:left;border-bottom:1px solid #d3dccb;vertical-align:top}th{background:#e8eee2}ol,ul{padding-left:5mm;margin:3mm 0}li{margin:0 0 3mm}.top{font-size:8pt;letter-spacing:.08em;color:#63745f;margin-bottom:4mm}.foot{position:absolute;bottom:8mm;left:18mm;right:18mm;display:flex;justify-content:space-between;font-size:8pt;color:#63745f}@page{size:A4;margin:0}@media print{body{background:white;-webkit-print-color-adjust:exact;print-color-adjust:exact}.page{margin:0;break-after:page}.page:last-child{break-after:auto}}@media screen and (max-width:800px){.page{width:auto;height:auto;min-height:100vh;margin:0 0 8px;padding:24px}.foot{position:static;margin-top:24px}}'''
    parts=[]
    for i,(title,body) in enumerate(pages,1):
        parts.append(f'<section class="page"><div class="top">ANH – THU – TÍN · TÀI LIỆU CÙNG ĐỌC</div><h1>{esc(title)}</h1><div class="page-body">{body}</div><div class="foot"><span>Nháp chuẩn bị 25/10/2026 · chờ nhóm đọc/sửa</span><span>{i} / {len(pages)}</span></div></section>')
    (GUIDE/'guide.html').write_text('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nhóm mình đọc và tập trình bày</title><style>'+guide_css+'</style></head><body>'+''.join(parts)+'</body></html>',encoding='utf-8')
    (GUIDE/'noi_dung_huong_dan.json').write_text(json.dumps([dict(title=t,body=b) for t,b in pages],ensure_ascii=False,indent=2),encoding='utf-8')
    audit=dict(created_on='2026-10-25',slides=len(slides),guide_pages=len(pages),sources=sources,metric_cells=metric_cells,values_derived_from_csv=True,manual_review='Awaiting group review; draft only')
    (DECK/'CONTENT_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(slides=len(slides),guide_pages=len(pages),metric_cells=len(metric_cells)),ensure_ascii=False))


if __name__=='__main__':
    main()
