/* Real inference, with stale-result invalidation and no invented ground truth. */
(()=>{
 const el=id=>document.getElementById(id);
 let result=null,fileText='',uploadFileName='',sourceName='',busy=false,version=0;
 const dec=n=>n.toLocaleString('vi-VN',{minimumFractionDigits:6,maximumFractionDigits:6});
 const status=(text,state='empty')=>{el('inference-status').textContent=text;el('inference-status').dataset.state=state};
 function showDemoView(view){
  if(view==='result'&&!result)return;
  el('inference-form').hidden=view!=='setup';el('live-output').hidden=view!=='result';el('demo-scope').hidden=view!=='scope';
  document.querySelectorAll('[data-demo-view]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.demoView===view)));
  window.scrollTo(0,0);
 }
 document.querySelectorAll('[data-demo-view]').forEach(button=>button.onclick=()=>showDemoView(button.dataset.demoView));
 document.querySelectorAll('[data-question]').forEach(button=>button.onclick=()=>{document.querySelectorAll('[data-question]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('[data-answer]').forEach(a=>a.hidden=a.dataset.answer!==button.dataset.question)});
 el('notes-toggle').onclick=()=>{el('speaker-notes').showModal();el('notes-toggle').setAttribute('aria-pressed','true')};
 el('speaker-notes').addEventListener('close',()=>el('notes-toggle').setAttribute('aria-pressed','false'));
 el('close-notes').onclick=()=>el('speaker-notes').close();
 function invalidate(){version++;result=null;el('live-result').hidden=true;el('run-provenance').hidden=true;el('demo-result-tab').disabled=true;showDemoView('setup');status('Cấu hình đã đổi · bấm Chạy suy luận để xem kết quả mới')}
 function setBusy(value){busy=value;el('live-output').setAttribute('aria-busy',String(value));el('run-demo').disabled=value;el('run-demo').textContent=value?'Đang suy luận…':'Chạy suy luận →';document.querySelectorAll('#inference-form select,#inference-form input').forEach(x=>x.disabled=value)}
 function rowView(){
  const position=Math.max(0,Math.min(result.results.length-1,Math.trunc(Number(el('record-position').value)-1)||0));
  el('record-position').value=position+1;
  el('record-prev').disabled=position===0;el('record-next').disabled=position===result.results.length-1;
  const row=result.results[position];el('record-title').textContent='Bản ghi #'+row.record_id;
  const attack=row.prediction==='Attack';
  el('live-score').textContent=dec(row.score);el('live-threshold').textContent=dec(row.threshold);
  el('live-comparator').textContent=attack?'≥':'<';el('live-verdict').textContent=row.prediction;
  el('live-verdict').parentElement.classList.toggle('normal',!attack);
  el('row-truth').textContent=row.truth?'Nhãn đối chiếu: '+row.truth:'Chưa có nhãn đối chiếu';
  const meaning={FP:'Báo động nhầm (FP): dữ liệu có nhãn Normal, mô hình cảnh báo Attack.',TN:'Dự đoán đúng (TN): dữ liệu có nhãn Normal, mô hình trả Normal.',TP:'Phát hiện đúng (TP): dữ liệu có nhãn Attack, mô hình cảnh báo Attack.',FN:'Bỏ sót (FN): dữ liệu có nhãn Attack, mô hình trả Normal.'};
  el('decision-reading').textContent=meaning[row.outcome]||'Chưa có nhãn hợp lệ nên chưa kết luận được dự đoán đúng hay sai.';
  el('decision-reading').classList.toggle('normal',!attack);
 }
 function render(){
  el('batch-rows').textContent=result.rows;el('batch-attack').textContent=result.attack_predictions;el('batch-normal').textContent=result.normal_predictions;
  el('record-position').value=1;el('record-position').max=result.rows;el('record-count').textContent='/ '+result.rows;
  const c=result.confusion;
  el('label-coverage').textContent=result.labeled_rows===0?'0/'+result.rows+' dòng có nhãn hợp lệ · chỉ hiển thị dự đoán, không tính đúng/sai':result.labeled_rows+'/'+result.rows+' dòng có nhãn hợp lệ · TP '+c.TP+' · FP '+c.FP+' · TN '+c.TN+' · FN '+c.FN;
  el('run-provenance').textContent=result.run_id+' · target validation '+(result.target_fpr*100)+'% · '+sourceName;
  el('run-provenance').hidden=false;
  el('live-result').hidden=false;el('demo-result-tab').disabled=false;rowView();showDemoView('result');
 }
 el('record-position').onchange=()=>{if(result)rowView()};
 el('record-prev').onclick=()=>{el('record-position').value=Number(el('record-position').value)-1;rowView()};
 el('record-next').onclick=()=>{el('record-position').value=Number(el('record-position').value)+1;rowView()};
 el('demo-source').onchange=()=>{
  const source=el('demo-source').value;el('upload-area').hidden=source!=='upload';
  const suggested={'heldout-r':'LR','heldout-d':'LD','heldout-e':'LE'}[source];if(suggested)el('demo-scenario').value=suggested;
  invalidate();
 };
 ['demo-scenario','demo-model','demo-target'].forEach(id=>el(id).onchange=invalidate);
 el('demo-file').onchange=async()=>{
  invalidate();fileText='';uploadFileName='';const file=el('demo-file').files[0];if(!file){el('file-state').textContent='Chưa chọn tệp';return}
  const readVersion=version;
  if(file.size>1900000){status('Tệp quá lớn · chọn CSV dưới 1,9 MB và tối đa 1.000 dòng','error');return}
  status('Đang đọc tệp CSV…','loading');
  try{const text=await file.text();if(readVersion!==version)return;fileText=text;uploadFileName=file.name;el('file-state').textContent=file.name;status('Đã đọc tệp · bấm Chạy suy luận để kiểm tra dữ liệu')}
  catch{status('Không đọc được tệp · chọn lại CSV trên máy','error')}
 };
 el('inference-form').onsubmit=async event=>{
  event.preventDefault();if(busy)return;
  result=null;el('live-result').hidden=true;el('run-provenance').hidden=true;el('demo-result-tab').disabled=true;showDemoView('setup');
  const source=el('demo-source').value;
  if(source==='upload'&&!fileText.trim()){status('Chưa có nội dung CSV · chọn tệp rồi chạy lại','error');return}
  const requestVersion=version;const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),60000);
  setBusy(true);status('Đang chạy mô hình đã lưu · chưa có kết quả mới','loading');
  try{
   const payload={scenario:el('demo-scenario').value,model:el('demo-model').value,target:Number(el('demo-target').value)};
   if(source==='upload')payload.csv=fileText;else payload.case=source;
   let data;
   if(window.NIDSInference)data=await window.NIDSInference(payload,controller.signal);
   else{const response=await fetch(source==='upload'?'/api/predict':'/api/lab/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),signal:controller.signal});data=await response.json();if(!response.ok)throw new Error(data.error||'Máy chủ chưa trả được kết quả')}
   if(requestVersion!==version)return;
   result=data.prediction||data;sourceName=source==='upload'?uploadFileName:data.case.title+' · tập con UNSW-NB15';
   render();status('Đã chạy '+result.rows+' dòng · '+result.run_id,'success');
  }catch(error){if(requestVersion!==version)return;result=null;el('live-result').hidden=true;const browser=Boolean(window.NIDSInference);status(error.name==='AbortError'?(browser?'Chờ quá lâu · kiểm tra kết nối rồi chạy lại':'Chờ quá lâu · kiểm tra máy chủ demo rồi chạy lại'):error instanceof TypeError?(browser?'Chưa tải được dữ liệu hoặc mô hình · kiểm tra kết nối rồi chạy lại':'Mất kết nối máy chủ demo · mở lại máy chủ rồi chạy lại'):error.message,'error')}
  finally{clearTimeout(timeout);setBusy(false)}
 };
 el('export-result').onclick=()=>{
  if(!result)return;
  const fields=['record_id','score','threshold','prediction','truth','outcome','attack_cat'];
  const cell=value=>'"'+String(value??'').replaceAll('"','""')+'"';
  const csv=[fields.join(','),...result.results.map(row=>fields.map(key=>cell(row[key])).join(','))].join('\r\n');
  const url=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download=result.run_id+'_target_'+result.target_fpr+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 };
})();
