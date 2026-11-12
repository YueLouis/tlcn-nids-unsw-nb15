"""Promote the reviewed presentation direction without touching frozen results."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'demo/presentation'
html=(dest/'template.html').read_text(encoding='utf-8')
html=html.replace('<title>NIDS · Đề xuất giao diện trình bày</title>','<title>NIDS · Trâm Anh – Vương Thu – Trọng Tín</title>')
html=html.replace('</style>','</style>\n<link rel="stylesheet" href="presentation.css">',1)
html=html.replace('<body>','<body>\n<a class="skip" href="#main">Đến nội dung trình bày</a>',1)
start=html.index(' <section class="scene" data-title="Demo"')
end=html.index(' <section class="scene" data-title="Hỏi đáp"',start)
html=html[:start]+''' <section class="scene live-scene" data-title="Demo" aria-labelledby="s4-title" hidden>
  <div class="heading-row"><div><p class="eyebrow">04 / Chạy mô hình đã lưu</p><h2 id="s4-title">Từ một flow đến một cảnh báo.</h2></div><p class="context">Chọn dữ liệu, chạy suy luận,<br>mở từng dòng để giải thích.</p></div>
  <nav class="demo-views" aria-label="Các bước chạy demo"><button type="button" id="demo-setup-tab" data-demo-view="setup" aria-pressed="true" aria-controls="inference-form">1 · Chọn dữ liệu</button><button type="button" id="demo-result-tab" data-demo-view="result" aria-pressed="false" aria-controls="live-output" disabled>2 · Xem kết quả</button><button type="button" data-demo-view="scope" aria-pressed="false" aria-controls="demo-scope">Phạm vi demo</button></nav>
  <p id="inference-status" class="live-status" role="status" aria-live="polite">Chưa chạy · chọn dữ liệu rồi bấm Chạy suy luận</p>
  <div class="live-grid"><form id="inference-form" class="live-controls">
   <div class="select-wrap source-config"><label for="demo-source">Dữ liệu minh họa</label><select id="demo-source"><option value="mixed">Normal xen các nhóm tấn công</option><option value="normal">Chỉ Normal · xem báo động nhầm</option><option value="heldout-r">Reconnaissance · lớp bị giấu</option><option value="heldout-d">DoS · lớp bị giấu</option><option value="heldout-e">Exploits · lớp bị giấu</option><option value="unlabeled">Dữ liệu chưa có nhãn</option><option value="invalid">CSV sai schema · thử kiểm tra</option><option value="upload">Mở tệp CSV trên máy…</option></select></div>
   <div id="upload-area" hidden><label for="demo-file">CSV · đủ 42 feature · tối đa 1.000 dòng</label><input type="file" id="demo-file" accept=".csv,text/csv"><p id="file-state" class="small muted">Chưa chọn tệp</p></div>
   <div class="control-pair"><div class="select-wrap"><label for="demo-scenario">Kịch bản huấn luyện</label><select id="demo-scenario"><option value="CS">CS · Không giấu lớp</option><option value="LR">LR · Giấu Recon</option><option value="LD">LD · Giấu DoS</option><option value="LE">LE · Giấu Exploits</option></select></div><div class="select-wrap"><label for="demo-model">Mô hình</label><select id="demo-model"><option>RF</option><option>XGB</option><option>IF</option><option>AE</option></select></div></div>
   <div class="select-wrap target-config"><label for="demo-target">Target FPR trên Normal validation</label><select id="demo-target"><option value="0.05">5% · ngưỡng đã lưu</option><option value="0.01">1% · ngưỡng đã lưu</option></select></div>
   <button id="run-demo" type="submit" class="primary">Chạy suy luận <span aria-hidden="true">→</span></button>
   <p class="small muted control-note">Seed 42 · model cố định, không học lại</p>
   <a href="/lab" class="small">Mở phòng thử nghiệm đầy đủ ↗</a>
  </form><div class="live-output" id="live-output" aria-busy="false" hidden>
   <div id="live-result" hidden>
    <div class="batch-summary"><div><span>Tổng số dòng</span><strong id="batch-rows" class="num"></strong></div><div><span>Cảnh báo Attack</span><strong id="batch-attack" class="num"></strong></div><div><span>Dự đoán Normal</span><strong id="batch-normal" class="num"></strong></div><div class="export"><button id="export-result" type="button" class="text-button">Tải kết quả CSV ↓</button></div></div>
    <div class="record-heading"><span id="record-title">Bản ghi</span><div class="record-stepper" role="group" aria-label="Chọn bản ghi"><button type="button" id="record-prev" aria-label="Bản ghi trước">←</button><label for="record-position" class="sr-only">Vị trí bản ghi</label><input type="number" id="record-position" min="1" value="1"><span id="record-count" class="small"></span><button type="button" id="record-next" aria-label="Bản ghi sau">→</button></div><span id="row-truth" class="small"></span></div>
    <div class="decision-strip"><div><span>Score</span><strong id="live-score" class="num"></strong></div><span id="live-comparator" aria-hidden="true"></span><div><span>Ngưỡng</span><strong id="live-threshold" class="num"></strong></div><div class="decision-verdict"><span>Dự đoán</span><strong id="live-verdict"></strong></div></div>
    <p id="decision-reading" class="decision-reading"></p>
    <p id="label-coverage" class="small muted"></p>
   </div>
  </div>
  <article id="demo-scope" class="demo-scope" hidden><h3>Dữ liệu và giới hạn của demo</h3><p>Các mẫu có sẵn là tập con UNSW-NB15, chưa phải bộ dữ liệu mạng độc lập do nhóm thu thập.</p><p>Demo suy luận từ CSV qua mô hình đã lưu ở seed 42. Chưa thu traffic trực tiếp, chưa tự học hay chặn tấn công. Kết quả mẫu không thay cho đánh giá toàn test.</p><p id="run-provenance" class="small muted provenance" hidden></p><a href="/lab">Mở phòng thử nghiệm đầy đủ ↗</a></article>
  </div>
 </section>
'''+html[end:]
html=html.replace('Hiện demo gốc suy luận từ flow CSV qua model đã lưu; chưa bắt gói mạng trực tiếp, chưa tự học và chưa chặn tấn công. Bản đề xuất giao diện này dùng kết quả đã lưu.','Demo chạy suy luận từ flow CSV qua model đã lưu; chưa bắt gói mạng trực tiếp, chưa tự học và chưa chặn tấn công. Dữ liệu mẫu có sẵn là tập con của UNSW-NB15, chưa phải bộ dữ liệu độc lập của nhóm.')
html=html.replace('Bản nhóm đang đọc duyệt · số trang theo trình xem PDF','Bản đã gửi đợt 3 · số trang theo trình xem PDF')
html=html.replace('Truy vết dữ liệu đang hiển thị trong bản mẫu','Truy vết số liệu, bản PDF và mô hình suy luận')
html=html.replace('BẢN ĐỀ XUẤT GIAO DIỆN · 11.11.2026 · CHƯA NỐI API SUY LUẬN','TRÂM ANH – VƯƠNG THU – TRỌNG TÍN · UNSW-NB15')
html=html.replace("+' · NIDS · Bản đề xuất'","+' · NIDS'")
html=html.replace("document.title=scenes[current].dataset.title+' · NIDS';}","document.title=scenes[current].dataset.title+' · NIDS';window.scrollTo(0,0);}")
html=html.replace('const $=id=>document.getElementById(id),scenes=[...document.querySelectorAll(\'.scene\')];let current=0,target=.05;','const $=id=>document.getElementById(id),scenes=[...document.querySelectorAll(\'.scene\')];let current=0;')
html=html.replace("if(e.target.closest('input,textarea,select,summary,details,[contenteditable=true]')", "if(document.querySelector('dialog[open]')||e.target.closest('input,textarea,select,summary,details,[contenteditable=true]')")
# Question buttons keep each answer on a single stable screen.
qa_start=html.index('  <div class="qa-grid">')
qa_end=html.index('\n </section>',qa_start)
html=html[:qa_start]+'''  <div class="qa-grid"><nav class="question-options" aria-label="Chọn câu hỏi"><button type="button" data-question="0" aria-pressed="true">01 <span>Giấu lớp tấn công thế nào?</span></button><button type="button" data-question="1" aria-pressed="false">02 <span>Vì sao chọn ngưỡng trên validation?</span></button><button type="button" data-question="2" aria-pressed="false">03 <span>AP cao đã đủ tốt chưa?</span></button><button type="button" data-question="3" aria-pressed="false">04 <span>Demo có tự học hoặc bắt gói không?</span></button><button type="button" data-question="4" aria-pressed="false">05 <span>Mở báo cáo và số liệu</span></button></nav><div class="answer-area">
   <article class="answer" data-answer="0"><p class="eyebrow">Thiết kế LOACO</p><h3>Không để lớp bị giấu lọt vào vùng phát triển.</h3><p>Loại lớp đó trước khi chia train và validation. Test giữ nguyên, vẫn chứa lớp bị giấu. IF và AE chỉ học từ Normal.</p><p class="answer-key">LR: Reconnaissance · LD: DoS · LE: Exploits</p><a href="assets/BAO_CAO_DOT3.pdf#page=23" target="_blank" rel="noopener">Đối chiếu phương pháp · PDF trang 23 ↗</a></article>
   <article class="answer" data-answer="1" hidden><p class="eyebrow">Tách chọn ngưỡng khỏi kiểm thử</p><h3>Test cần độc lập để đo kết quả.</h3><p>Nhóm dùng score của Normal validation để lưu hai ngưỡng, tương ứng target FPR 1% và 5%. Sau đó áp dụng nguyên ngưỡng lên test.</p><p class="answer-key">Target trên validation không bảo đảm FPR trên test bằng đúng target.</p><a href="assets/BAO_CAO_DOT3.pdf#page=24" target="_blank" rel="noopener">Đối chiếu phương pháp và chỉ số ↗</a></article>
   <article class="answer" data-answer="2" hidden><p class="eyebrow">Đọc đúng phạm vi</p><h3>AP toàn test có thể che khuất lớp bị giấu.</h3><p>Ở LR–RF, AP toàn test là 0,9852; AP trên Normal + Reconnaissance còn 0,7077, trung bình 5 seed. Cần đọc thêm UADR, FPR và số mẫu tại ngưỡng.</p><p class="answer-key">AP đo xếp hạng, không phải tỷ lệ dự đoán đúng.</p><button type="button" class="text-button" data-scene="3">Đối chiếu hai phạm vi ở màn Kết quả →</button></article>
   <article class="answer" data-answer="3" hidden><p class="eyebrow">Phạm vi sản phẩm đã có</p><h3>Demo suy luận từ CSV qua model đã lưu.</h3><p>Chưa thu gói mạng trực tiếp, chưa tự học và chưa chặn tấn công. Các mẫu có sẵn là tập con UNSW-NB15; nhóm chưa có bộ dữ liệu mạng độc lập.</p><p class="answer-key">Đầu ra mô hình: Normal hoặc Attack. attack_cat là nhãn đối chiếu.</p><button type="button" class="text-button" data-scene="4">Mở màn chạy suy luận →</button></article>
   <article class="answer evidence-links" data-answer="4" hidden><p class="eyebrow">Căn cứ của nhóm</p><h3>Đi từ kết luận về đúng nguồn.</h3><a href="assets/BAO_CAO_DOT3.pdf" target="_blank" rel="noopener">Báo cáo đợt 3 · bản đã gửi · 62 trang ↗</a><a href="assets/AP_MEAN_STD.csv" target="_blank" rel="noopener">AP theo kịch bản và phạm vi · 5 seed ↗</a><a href="assets/OPERATING_POINTS_MEAN_STD.csv" target="_blank" rel="noopener">FPR, Recall, UADR · hai target 1% và 5% ↗</a><a href="SOURCE_DATA.json" target="_blank" rel="noopener">Đường nguồn và SHA-256 các tệp ↗</a></article>
  </div></div>'''+html[qa_end:]
html=html.replace('<aside class="speaker-notes" id="speaker-notes" hidden><strong>Gợi ý lời nói · cùng hiển thị lên máy chiếu</strong><p id="speaker-text"></p></aside>', '<dialog class="speaker-notes" id="speaker-notes" aria-labelledby="notes-title"><div class="notes-heading"><strong id="notes-title">Gợi ý lời nói · cũng hiển thị lên máy chiếu</strong><button type="button" id="close-notes" autofocus>Đóng ×</button></div><p id="speaker-text"></p></dialog>')
html=html.replace("'Đọc score 0,705741 và ngưỡng 0,557282: mô hình báo Attack nhưng nhãn thật là Normal nên là FP. Chuyển target 1%: ngưỡng 0,805367 nên thành TN. Mẫu và score vẫn như cũ, không có học lại.'", "'Chạy mẫu Normal xen tấn công với CS–RF ở target 5%. Bản ghi 1 có score 0,705741 ≥ ngưỡng 0,557282 nên báo Attack, nhãn thật Normal: FP. Đổi target 1%, chạy lại: ngưỡng 0,805367 nên thành TN. Model không học lại. Với CSV mới không có nhãn, chỉ nói dự đoán; chưa kết luận đúng hay sai.'")
# Replace the saved-example renderer; AP rendering and navigation remain intact.
begin=html.index('function renderThreshold()')
end=html.index('</script>',begin)
html=html[:begin]+'renderResults();showScene(0);\n'+html[end:]
html=html.replace('</body>','<script src="presentation.js"></script>\n</body>')
(dest/'index.html').write_text(html,encoding='utf-8')
paths=['docs/evidence/dot_03/final_20261030/pr_scores/AP_MEAN_STD.csv',
       'docs/evidence/dot_03/final_20261030/pr_scores/OPERATING_POINTS_MEAN_STD.csv',
       'artifacts/data/data_manifest.json','configs/experiment_matrix.yaml',
       'docs/releases/submission_dot3_20261111/NhomTLCN_TramAnh_VuongThu_TrongTin_dot3_20261111.pdf']
manifest={'purpose':'Trình bày số liệu thực nghiệm và suy luận từ model đã lưu',
          'source_files':[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in paths],
          'inference':{'routes':['/api/lab/run','/api/predict'],'seed':42,'models':['RF','XGB','IF','AE'],'thresholds':'Normal validation 1% / 5%'},
          'limits':['Không thu gói mạng trực tiếp, không tự học hay chặn tấn công','Dữ liệu mẫu là tập con UNSW-NB15, không phải dataset độc lập','Nhãn attack_cat chỉ đối chiếu; mô hình dự đoán Normal/Attack']}
(dest/'SOURCE_DATA.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared',dest)
