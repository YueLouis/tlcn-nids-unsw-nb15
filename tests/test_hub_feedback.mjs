import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

// Run the real hub script; emulate only DOM operations used by that script.
const html=readFileSync(new URL('../demo/presentation/ho-so.html',import.meta.url),'utf8');
const script=readFileSync(new URL('../demo/presentation/ho-so.js',import.meta.url),'utf8');
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(match=>match[1]);
assert.equal(new Set(ids).size,ids.length,'HTML IDs must be unique');
const names=['Trịnh Trâm Anh','Hoàng Văn Vương Thu','Nguyễn Trọng Tín'];
const nameSelect=html.match(/<select\b[^>]*\bid="feedback-name"[^>]*>([\s\S]*?)<\/select>/)?.[1];
assert.ok(nameSelect,'Actual HTML contains the member select');
const options=[...nameSelect.matchAll(/<option\b[^>]*>([^<]*)<\/option>/g)].map(match=>match[1]);
assert.deepEqual(options,['Chọn tên của mình',...names],'Every member must be a real option');
assert.match(html,/<textarea\b[^>]*\bid="feedback-copy-preview"[^>]*\breadonly\b/);

function loadHub(clipboardMode='success') {
  const state={clipboard:[],blobs:[],clicks:[],timers:[],revoked:[],focused:null,selected:null};
  class Element {
    constructor(tag='div',id='') {
      this.tagName=tag.toUpperCase();this.id=id;this.value='';this.textContent='';
      this.attributes={};this.dataset={};this.listeners={};this.children=[];this.open=false;
    }
    addEventListener(type,handler) { (this.listeners[type]??=[]).push(handler); }
    setAttribute(name,value) { this.attributes[name]=value; }
    getAttribute(name) { return this.attributes[name]; }
    append(child) { this.children.push(child); }
    replaceChildren(...children) { this.children=children; }
    focus() { state.focused=this; }
    select() { state.selected=this; }
    showModal() { this.open=true; }
    close() { this.open=false; }
    click() { state.clicks.push(this); }
    remove() { this.removed=true; }
    async fire(type,event={}) {
      for(const handler of this.listeners[type]??[]) await handler(event);
    }
  }
  const elements=new Map(ids.map(id=>[id,new Element('div',id)]));
  const personButtons=['anh','thu','tin'].map(person=>{
    const button=new Element('button');button.dataset.person=person;return button;
  });
  const tabs=['docs','people','review'].map(key=>{
    const tab=elements.get('tab-'+key);tab.setAttribute('aria-controls','panel-'+key);return tab;
  });
  const document={
    body:new Element('body'),
    getElementById(id) { assert.ok(elements.has(id),`JS refers to actual HTML ID: ${id}`);return elements.get(id); },
    createElement(tag) { return new Element(tag); },
    querySelectorAll(selector) {
      if(selector==='[role="tab"]')return tabs;
      if(selector==='[data-person]')return personButtons;
      throw new Error('Unexpected selector '+selector);
    },
  };
  const navigator=clipboardMode==='unavailable'?{}:{clipboard:{async writeText(text) {
    if(clipboardMode==='blocked')throw new Error('NotAllowedError');
    state.clipboard.push(text);
  }}};
  const context=vm.createContext({document,navigator,Blob,Date,Intl,
    URL:{createObjectURL(blob) { state.blobs.push(blob);return 'blob:test-'+state.blobs.length; },revokeObjectURL(url) { state.revoked.push(url); }},
    setTimeout(callback,delay) { state.timers.push({callback,delay}); },
  });
  vm.runInContext(script,context,{filename:'ho-so.js'});
  return {state,elements,async submit(name,note,action) {
    elements.get('feedback-name').value=name;elements.get('feedback-text').value=note;
    let prevented=false;
    await elements.get('feedback-form').fire('submit',{submitter:{value:action},preventDefault() { prevented=true; }});
    assert.ok(prevented,'Feedback is handled locally, without form navigation');
  }};
}

const note='báo cáo tổng · trang 24\nchưa hiểu cách chọn ngưỡng 1% · cần nhóm giải thích lại';
for(const name of names) {
  const hub=loadHub();await hub.submit(name,'  '+note+'  ','copy');
  assert.equal(hub.state.clipboard.length,1);
  const text=hub.state.clipboard[0];
  assert.ok(text.includes('Người ghi: '+name));
  assert.ok(text.includes('\n\n'+note+'\n\n'),'Whitespace is trimmed, Vietnamese/newlines preserved');
  assert.ok(text.includes('không xác nhận đã duyệt hoặc đã nộp'));
  assert.match(hub.elements.get('feedback-status').textContent,/Đã sao chép/);
  assert.equal(hub.state.blobs.length,0);assert.equal(hub.elements.get('feedback-copy-dialog').open,false);
}

for(const mode of ['blocked','unavailable']) {
  const hub=loadHub(mode);const literal=note+'\n<img src=x onerror=alert(1)>';
  await hub.submit(names[0],literal,'copy');
  const preview=hub.elements.get('feedback-copy-preview');
  assert.equal(hub.elements.get('feedback-copy-dialog').open,true);
  assert.equal(hub.state.focused,preview);assert.equal(hub.state.selected,preview);
  assert.ok(preview.value.includes(literal),'Fallback places user input in plain textarea value');
  assert.ok(preview.value.includes('Người ghi: '+names[0]));
  assert.equal(hub.state.blobs.length,0);assert.equal(hub.state.clipboard.length,0);
  assert.match(hub.elements.get('feedback-status').textContent,/sao chép thủ công/);
  await hub.elements.get('feedback-copy-close').fire('click');
  assert.equal(hub.elements.get('feedback-copy-dialog').open,false);
}

for(const name of names) {
  const hub=loadHub();await hub.submit(name,note,'download');
  assert.equal(hub.state.blobs.length,1);assert.equal(hub.state.clicks.length,1);
  const blob=hub.state.blobs[0];const bytes=Buffer.from(await blob.arrayBuffer());
  assert.equal(blob.type,'text/plain;charset=utf-8');
  assert.deepEqual([...bytes.subarray(0,3)],[0xef,0xbb,0xbf],'TXT starts with a UTF-8 BOM');
  const decoded=bytes.subarray(3).toString('utf8');
  assert.ok(decoded.startsWith('GÓP Ý HỒ SƠ NIDS\n'));assert.ok(decoded.includes('Người ghi: '+name));
  assert.ok(decoded.includes(note));assert.equal(decoded.includes('\uFFFD'),false);
  const link=hub.state.clicks[0];assert.match(link.download,/^gop-y-nids-\d{4}-\d{2}-\d{2}\.txt$/);
  assert.equal(link.href,'blob:test-1');assert.equal(link.removed,true);
  assert.match(hub.elements.get('feedback-status').textContent,/yêu cầu tải TXT · kiểm tệp/,'Status does not claim browser delivery');
  assert.equal(hub.state.timers.length,1);assert.equal(hub.state.timers[0].delay,1000);
  hub.state.timers[0].callback();assert.deepEqual(hub.state.revoked,['blob:test-1']);
  assert.equal(hub.state.clipboard.length,0);
}

for(const action of ['copy','download'])for(const [name,text] of [['',note],[names[1],' \n\t ']]) {
  const hub=loadHub();await hub.submit(name,text,action);
  assert.match(hub.elements.get('feedback-status').textContent,/Chọn tên và ghi góp ý/);
  assert.equal(hub.state.clipboard.length,0);assert.equal(hub.state.blobs.length,0);
  assert.equal(hub.elements.get('feedback-copy-dialog').open,false);
}
console.log('PASS: actual hub JS; three HTML member options; copy for three names; blocked/unavailable clipboard plain-text fallback; TXT UTF-8/BOM; blank validation');
