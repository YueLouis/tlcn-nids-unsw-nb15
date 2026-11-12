/* Public builds keep CSV local to the browser; the Python API remains local. */
(()=>{
 let worker,sequence=0;
 const pending=new Map();
 const start=()=>{
  if(worker)return;
  worker=new Worker('./browser-worker.mjs',{type:'module'});
  worker.onmessage=({data})=>{
   const request=pending.get(data.id);if(!request)return;
   if(data.progress){document.getElementById('inference-status').textContent=data.progress;return}
   pending.delete(data.id);request.cleanup();data.error?request.reject(new Error(data.error)):request.resolve(data.result);
  };
  worker.onerror=()=>{for(const request of pending.values()){request.cleanup();request.reject(new Error('Trình duyệt chưa chạy được mô hình · tải lại trang rồi thử lại'))}pending.clear();worker.terminate();worker=null};
 };
 window.NIDSInference=(payload,signal)=>new Promise((resolve,reject)=>{
  if(!('Worker' in window)||!('DecompressionStream' in window)){reject(new Error('Dùng Chrome hoặc Edge mới để chạy bản online'));return}
  if(signal.aborted){reject(new DOMException('Đã hủy','AbortError'));return}
  start();const id=++sequence;
  const abort=()=>{const request=pending.get(id);if(request){pending.delete(id);request.cleanup();reject(new DOMException('Đã hủy','AbortError'))}worker?.terminate();worker=null};
  const cleanup=()=>signal.removeEventListener('abort',abort);
  signal.addEventListener('abort',abort,{once:true});pending.set(id,{resolve,reject,cleanup});worker.postMessage({id,payload});
 });
})();
