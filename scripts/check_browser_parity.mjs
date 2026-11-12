import {readFile,writeFile} from 'node:fs/promises';
import {gunzipSync} from 'node:zlib';
import {unpack,predict} from '../demo/presentation/browser-engine.mjs';
const root=new URL('../',import.meta.url),fixture=JSON.parse(await readFile(new URL('output/browser_parity/fixture.json',root),'utf8'));
const observations=[];
for(const item of fixture.cases){
 const binary=gunzipSync(await readFile(new URL('sites/nids-presentation/dist/models/'+item.run_id+'.bin.gz',root)));
 const model=unpack(binary.buffer.slice(binary.byteOffset,binary.byteOffset+binary.byteLength));
 const result=predict(model,fixture.csv,item.target);
 let maxAbs=0,maxRelative=0,mismatches=0;
 result.results.forEach((row,i)=>{const expected=item.scores[i],delta=Math.abs(row.score-expected);maxAbs=Math.max(maxAbs,delta);maxRelative=Math.max(maxRelative,delta/Math.max(1,Math.abs(expected)));if(row.prediction!==item.predictions[i])mismatches++});
 const pass=mismatches===0&&maxRelative<2e-5;
 observations.push({run_id:item.run_id,target:item.target,rows:result.rows,max_abs_error:maxAbs,max_relative_error:maxRelative,prediction_mismatches:mismatches,pass});
 console.log(item.run_id,item.target,'delta',maxAbs,'relative',maxRelative,'mismatches',mismatches);
}
const audit={scope:'1000 deterministic test rows including50mixed examples;16frozen models×2targets. Additional currentCSV tests documented separately.',cases:observations,pass:observations.every(x=>x.pass)};
await writeFile(new URL('output/browser_parity/PARITY.json',root),JSON.stringify(audit,null,2));
if(!audit.pass)process.exitCode=1;
