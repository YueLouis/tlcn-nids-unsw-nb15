// Verify the actual local teaching prototype after all required fields were added.
const fs=require('fs');
const path=require('path');
const assert=require('assert/strict');
const {chromium}=require('C:/Users/TrongTin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
const evidence=path.join(root,'docs/evidence/dot_04/demo_20261025');
const port=process.env.NIDS_UI_PORT||'4399';
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows']});
 try {
  const page=await browser.newPage({viewport:{width:1440,height:1100},acceptDownloads:true,reducedMotion:'reduce'});
  const wait=page.waitForFunction.bind(page);page.waitForFunction=(fn,arg,options={})=>wait(fn,arg,{polling:100,timeout:60000,...options});
  // Headless Edge can throttle animation frames on this host; native pointer
  // clicks with force skip its frame-stability wait. Layout is checked below.
  const pointerClick=page.click.bind(page);page.click=(selector)=>pointerClick(selector,{force:true});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${port}`);await page.evaluate(()=>document.fonts.ready);console.log('Opened demo');
  await page.click('#sample');await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('Đã chọn'));console.log('Sample loaded');
  await page.click('#compare');await page.waitForFunction(()=>!document.querySelector('#comparison').hidden,{},{timeout:120000});
  assert.equal(await page.locator('.compare-card').count(),4);
  assert.match(await page.locator('#compareMeta').textContent(),/100 dòng/);
  assert.match(await page.locator('#compareGrid').textContent(),/FP/);
  console.log('Four models compared');
  await page.screenshot({path:path.join(evidence,'DEMO_COMPARISON.png'),fullPage:true});
  await page.click('#run');await page.waitForFunction(()=>!document.querySelector('#output').hidden);
  assert.equal(await page.locator('#count').textContent(),'100');
  assert.equal(await page.locator('#featureList li').count(),5);
  assert.match(await page.locator('#explanationLimit').textContent(),/không/i);
  const [download]=await Promise.all([page.waitForEvent('download'),page.click('#download')]);
  await download.saveAs(path.join(evidence,'UI_RESULTS_CS_RF_S42.csv'));
  await page.screenshot({path:path.join(evidence,'DEMO_DESKTOP.png'),fullPage:true});
  await page.selectOption('#model','IF');assert.equal(await page.locator('#output').isHidden(),true);
  await page.selectOption('#scenario','LR');await page.selectOption('#target','0.01');
  await page.click('#run');await page.waitForFunction(()=>!document.querySelector('#output').hidden);
  assert.equal(await page.locator('#featureList li').count(),0);
  assert.match(await page.locator('#explanationText').textContent(),/decision_function/);
  const raw=fs.readFileSync(path.join(root,'demo/sample.csv'),'utf8').trim().split(/\r?\n/);
  assert(raw.every(x=>!x.includes('"')),'Use a CSV parser if sample includes quotes');
  const cols=raw[0].split(','),keep=cols.map((x,i)=>['label','attack_cat'].includes(x)?-1:i).filter(i=>i>=0);
  const unlabeled=raw.map(x=>{const cells=x.split(',');return keep.map(i=>cells[i]).join(',')}).join('\n');
  await page.setInputFiles('#file',{name:'khong_nhan.csv',mimeType:'text/csv',buffer:Buffer.from(unlabeled)});
  await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('khong_nhan.csv'));
  await page.click('#compare');await page.waitForFunction(()=>!document.querySelector('#comparison').hidden);
  assert.match(await page.locator('#compareGrid').textContent(),/chưa có nhãn/);
  const checks=[];
  for(const width of [1440,1024,768,390,375]){
   await page.setViewportSize({width,height:900});
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
   checks.push({width,horizontal_overflow:overflow});assert.equal(overflow,false);
  }
  await page.screenshot({path:path.join(evidence,'DEMO_MOBILE.png'),fullPage:true});
  await page.setInputFiles('#file',{name:'thieu_feature.csv',mimeType:'text/csv',buffer:Buffer.from('id,proto\n1,tcp\n')});
  await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('thieu_feature.csv'));
  await page.click('#compare');await page.waitForFunction(()=>!document.querySelector('#compare').disabled);
  assert.equal(await page.locator('#comparison').isHidden(),true);
  assert.match(await page.locator('#status').textContent(),/feature|thiếu/i);
  assert.deepEqual(errors,[]);
  const audit={checked_on:'2026-10-25',port:Number(port),native_pointer_clicks:true,frame_stability_wait_skipped:true,models_compared:4,comparison_rows:100,global_explanation:true,score_explanation:true,download:true,unlabeled_without_fake_fp_fn:true,invalid_csv_rejected:true,stale_results_cleared:true,checks,page_errors:errors};
  fs.writeFileSync(path.join(evidence,'DEMO_UI_AUDIT.json'),JSON.stringify(audit,null,2));console.log(JSON.stringify(audit));
 } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
