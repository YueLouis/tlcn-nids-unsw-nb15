// Export and check the offline deck at the viewport sizes from frontend-slides.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('C:/Users/TrongTin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
const evidence=path.join(root,'docs/evidence/dot_03/session_20261025');

(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1280,height:720},reducedMotion:'reduce'});
 const errors=[]; page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(root,'docs/presentation_20261025/presentation.html')).href);
 await page.evaluate(()=>document.fonts.ready);
 console.log('Opened offline deck');
 const checks=[];
 for(const [width,height] of [[1920,1080],[1280,720],[768,1024],[375,667],[667,375]]){
  await page.setViewportSize({width,height});
  await page.waitForTimeout(250);
  const issues=await page.evaluate(()=>{
   const issues=[];
   document.querySelectorAll('.slide').forEach((slide,i)=>{
    const box=slide.getBoundingClientRect(); const content=slide.querySelector('.slide-content'); const cb=content.getBoundingClientRect();
    for(const el of slide.querySelectorAll('h1,h2,h3,p,li,table,.card')){
     const r=el.getBoundingClientRect();
     if(r.right>box.right+1||r.left<box.left-1||r.bottom>cb.bottom+1||r.top<cb.top-1)issues.push({slide:i+1,text:el.textContent.slice(0,70),outside:true});
     if(el.scrollWidth>el.clientWidth+2||el.scrollHeight>el.clientHeight+2)issues.push({slide:i+1,text:el.textContent.slice(0,70),clipped:true});
    }
   });
   return issues;
  });
  checks.push({width,height,issues});
 }
 console.log('Checked five viewports');
 await page.setViewportSize({width:1280,height:720});
 await page.evaluate(()=>window.deck.to(0));
 await page.keyboard.press('ArrowRight');
 await page.waitForTimeout(150);
 const next=await page.evaluate(()=>window.deck.index);
 await page.keyboard.press('ArrowLeft');
 await page.waitForTimeout(150);
 const prev=await page.evaluate(()=>window.deck.index);
 await page.evaluate(()=>document.querySelector('nav').style.display='none');
 console.log('Exporting deck PDF');
 await page.pdf({path:path.join(root,'docs/presentation_20261025/presentation.pdf'),printBackground:true,preferCSSPageSize:true,timeout:60000});
 console.log('Exported deck PDF');
 await page.goto(pathToFileURL(path.join(root,'docs/team_guide_20261025/guide.html')).href);
 await page.evaluate(()=>document.fonts.ready);
 await page.emulateMedia({media:'print'});
 const guideIssues=await page.evaluate(()=>[...document.querySelectorAll('.page')].flatMap((p,i)=>{
  const body=p.querySelector('.page-body').getBoundingClientRect(), footer=p.querySelector('.foot').getBoundingClientRect();
  return body.bottom>footer.top-5?[{page:i+1,bodyBottom:body.bottom,footerTop:footer.top}]:[];
 }));
 await page.pdf({path:path.join(root,'docs/team_guide_20261025/guide.pdf'),printBackground:true,preferCSSPageSize:true,timeout:60000});
 console.log('Exported guide PDF');
 const audit={checked_on:new Date().toISOString().slice(0,10),checks,next,prev,keyboard_pass:next===1&&prev===0,guide_issues:guideIssues,page_errors:errors};
 fs.writeFileSync(path.join(evidence,'PRESENTATION_UI_AUDIT.json'),JSON.stringify(audit,null,2));
 console.log(JSON.stringify(audit));
 await browser.close();
 if(checks.some(c=>c.issues.length)||guideIssues.length||errors.length||!audit.keyboard_pass)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
