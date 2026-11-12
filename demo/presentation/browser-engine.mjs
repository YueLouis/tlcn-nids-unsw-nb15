/* Parameter-only inference. No training, remote CSV upload, or benchmark edits. */
export function unpack(buffer){
 const view=new DataView(buffer),length=view.getUint32(0,true);
 const meta=JSON.parse(new TextDecoder().decode(new Uint8Array(buffer,4,length)));
 const start=Math.ceil((4+length)/8)*8;
 for(const [key,a] of Object.entries(meta.arrays)){
  const Type={'<i4':Int32Array,'<f8':Float64Array,'<f4':Float32Array}[a.dtype];
  if(!Type)throw new Error('Định dạng model chưa được hỗ trợ');
  meta[key]=new Type(buffer,start+a.offset,a.count);
 }
 return meta;
}
export function parseCSV(text){
 text=text.replace(/^\uFEFF/,'');let rows=[],row=[],cell='',quoted=false,closedQuote=false;
 for(let i=0;i<text.length;i++){
  const c=text[i];
  if(closedQuote&&c!==','&&c!=='\n'&&c!=='\r')throw new Error('CSV có ký tự sau dấu nháy đóng');
  if(c==='"'){if(quoted&&text[i+1]==='"'){cell+='"';i++}else if(quoted){quoted=false;closedQuote=true}else if(cell==='')quoted=true;else throw new Error('Dấu nháy CSV không hợp lệ')}
  else if(!quoted&&(c===','||c==='\n'||c==='\r')){
   row.push(cell);cell='';closedQuote=false;if(c!==','){if(c==='\r'&&text[i+1]==='\n')i++;if(row.some(v=>v!==''))rows.push(row);row=[]}
  }else cell+=c;
 }
 if(quoted)throw new Error('CSV có dấu nháy chưa đóng');
 row.push(cell);if(row.some(v=>v!==''))rows.push(row);
 const header=rows.shift();if(!header||new Set(header).size!==header.length)throw new Error('CSV trống hoặc trùng tên cột');
 if(rows.length<1||rows.length>1000)throw new Error('Chọn từ 1 đến 1.000 dòng CSV mỗi lượt');
 return rows.map((cells,i)=>{if(cells.length!==header.length)throw new Error('CSV sai số cột ở dòng '+(i+2));return Object.fromEntries(header.map((key,j)=>[key,cells[j]]))});
}
export function transform(model,rows){
 const required=model.features,first=rows[0];const missing=required.filter(k=>!(k in first));
 if(missing.length)throw new Error('CSV thiếu cột: '+missing.sort().join(', '));
 const width=model.numeric.length+model.categories.reduce((n,a)=>n+a.length,0);
 return rows.map(row=>{
  const x=new Float32Array(width);
  model.numeric.forEach((key,j)=>{const raw=row[key];if(raw===undefined||!String(raw).trim()||!Number.isFinite(Number(raw)))throw new Error('Cột số có ô trống hoặc dữ liệu không hợp lệ: '+key);x[j]=(Number(raw)-model.means[j])/model.scales[j]});
  let offset=model.numeric.length;
  model.categorical.forEach((key,j)=>{if(row[key]===undefined||!String(row[key]).trim())throw new Error('Cột '+key+' có ô trống');const index=model.categories[j].indexOf(row[key]);if(index>=0)x[offset+index]=1;offset+=model.categories[j].length});
  if(!x.every(Number.isFinite))throw new Error('Dữ liệu sau biến đổi không hữu hạn');return x;
 });
}
export function score(model,x){
 if(model.model==='AE'){
  let layer=x;
  for(let k=0;k<model.layers.length;k++){
   const {input,output}=model.layers[k],w=model['weights'+k],bias=model['bias'+k],next=new Float32Array(output);
   for(let j=0;j<output;j++){let sum=0;for(let i=0;i<input;i++)sum+=layer[i]*w[i*output+j];next[j]=Math.fround(Math.fround(sum)+bias[j]);if(k<model.layers.length-1&&next[j]<0)next[j]=0}
   layer=next;
  }
  let error=0;for(let i=0;i<x.length;i++){const d=Math.fround(x[i]-layer[i]);error+=Math.fround(d*d)}return error/x.length;
 }
 let total=model.model==='XGB'?model.base_margin:0;
 for(const root of model.roots){
  let n=root,depth=0;
  while(model.left[n]>=0){const v=x[model.feature[n]],goLeft=model.model==='XGB'?v<model.threshold[n]:v<=model.threshold[n];n=goLeft?model.left[n]:model.right[n];depth++}
  if(model.model==='XGB')total=Math.fround(total+Math.fround(model.value[n]));
  else total+=model.model==='IF'?depth+model.value[n]:model.value[n];
 }
 if(model.model==='XGB')return Math.fround(1/(1+Math.exp(-total)));
 if(model.model==='IF')return Math.pow(2,-total/model.normalizer)+model.offset;
 return total/model.roots.length;
}
export function predict(model,text,target){
 const threshold=model.thresholds.find(x=>Number(x.target_fpr)===Number(target))?.threshold;
 if(threshold===undefined)throw new Error('Chỉ hỗ trợ target validation 1% hoặc 5%');
 const rows=parseCSV(text),matrix=transform(model,rows),confusion={TP:0,FP:0,TN:0,FN:0};
 const results=rows.map((row,i)=>{
  const s=score(model,matrix[i]);if(!Number.isFinite(s))throw new Error('Mô hình trả score không hữu hạn');
  const attack=s>=threshold,out={record_id:row.id||String(i+1),score:s,threshold,prediction:attack?'Attack':'Normal'};
  const label=String(row.label??'').trim();
  // Decimal numeric labels match CSV/Python normalization without turning blanks into zero.
  if(/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(label)&&[0,1].includes(Number(label))){const truth=Number(label)===1;out.truth=truth?'Attack':'Normal';out.outcome=truth?(attack?'TP':'FN'):(attack?'FP':'TN');confusion[out.outcome]++}
  if(row.attack_cat)out.attack_cat=row.attack_cat;return out;
 });
 const attacks=results.filter(r=>r.prediction==='Attack').length;
 return {run_id:model.run_id,seed:42,target_fpr:Number(target),threshold,rows:rows.length,attack_predictions:attacks,normal_predictions:rows.length-attacks,labeled_rows:Object.values(confusion).reduce((a,b)=>a+b,0),confusion,results,engine:'browser-parameters-v1'};
}
