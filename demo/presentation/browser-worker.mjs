import {unpack,predict} from './browser-engine.mjs';
let cachedModel=null,cachedKey='';
self.onmessage=async({data})=>{
 try{
  const {id,payload}=data,key=payload.scenario+'-'+payload.model+'-S42';
  if(!['CS','LR','LD','LE'].includes(payload.scenario)||!['RF','XGB','IF','AE'].includes(payload.model))throw new Error('Chọn kịch bản và mô hình trong danh sách');
  if(key!==cachedKey){
   self.postMessage({id,progress:'Đang tải mô hình '+key+' cho trình duyệt…'});
   const response=await fetch('./models/'+key+'.bin.gz');if(!response.ok)throw new Error('Chưa tải được mô hình · kiểm tra kết nối rồi chạy lại');
   const compressed=await response.blob();
   const bytes=await new Response(compressed.stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();
   cachedModel=unpack(bytes);cachedKey=key;
  }
  let text=payload.csv,spec;
  if(payload.case){
   const catalog=await(await fetch('./cases/catalog.json')).json();spec=catalog.cases.find(c=>c.id===payload.case);
   if(!spec)throw new Error('Chọn dữ liệu trong danh sách');
   const response=await fetch('./cases/'+spec.filename);if(!response.ok)throw new Error('Chưa tải được CSV mẫu');text=await response.text();
  }
  self.postMessage({id,progress:'Đang suy luận '+key+' ngay trong trình duyệt…'});
  const prediction=predict(cachedModel,text,payload.target);
  self.postMessage({id,result:spec?{case:spec,prediction}:prediction});
 }catch(error){self.postMessage({id:data.id,error:error.message||'Chưa chạy được mô hình'})}
};
