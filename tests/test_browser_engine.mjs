import assert from 'node:assert/strict';
import {parseCSV, transform, predict} from '../demo/presentation/browser-engine.mjs';

// Contract checks for uploaded flow data, independent of saved model assets.
const model={model:'RF',run_id:'contract-test',features:['duration','proto'],numeric:['duration'],categorical:['proto'],categories:[['tcp','udp']],means:[10],scales:[2],roots:[0],left:[1,-1,-1],right:[2,-1,-1],feature:[0,0,0],threshold:[0,0,0],value:[0,.1,.9],thresholds:[{target_fpr:.05,threshold:.5}]};
const csv='duration,proto,id,label,attack_cat\n8,tcp,row-1,0,Normal\n12,udp,row-2,1,Exploits\n';
assert.deepEqual(predict(model,csv,.05).results.map(r=>r.prediction),['Normal','Attack']);
assert.deepEqual(predict(model,csv,.05).confusion,{TP:1,FP:0,TN:1,FN:0});
const reordered='attack_cat,label,id,proto,duration\nanything,1,changed,tcp,8\nNormal,0,changed,udp,12\n';
assert.deepEqual(predict(model,reordered,.05).results.map(r=>r.score),predict(model,csv,.05).results.map(r=>r.score),'metadata and column order must not change scores');
const noLabels=predict(model,'duration,proto\n8,tcp\n12,udp',.05);
assert.equal(noLabels.labeled_rows,0);
assert.deepEqual(noLabels.confusion,{TP:0,FP:0,TN:0,FN:0});
assert.deepEqual(Array.from(transform(model,[{duration:'8',proto:'unseen'}])[0]),[-1,0,0],'unseen categories follow fitted encoder handle_unknown=ignore');
assert.equal(parseCSV('\uFEFFduration,proto,note\r\n8,tcp,"a,b"\r\n')[0].note,'a,b');
assert.equal(parseCSV('duration,proto,note\n8,tcp,"a""b\nc"')[0].note,'a"b\nc');
// A closed quoted field must end at a CSV delimiter, not silently join trailing text.
for(const cell of ['"tcp"x','"tcp" "','"tcp""'])assert.throws(()=>parseCSV('duration,proto\n8,'+cell));
assert.deepEqual(parseCSV('duration,proto\r\n8,"tcp"\r\n12,"udp"').map(r=>r.proto),['tcp','udp']);
// Equivalent decimal labels are valid; blanks/invalid values must never imply Normal.
const decimalLabels=predict(model,'duration,proto,label\n8,tcp,0.00\n12,udp, 1 \n8,tcp,0e0',.05);
assert.equal(decimalLabels.labeled_rows,3);
assert.deepEqual(decimalLabels.confusion,{TP:1,FP:0,TN:2,FN:0});
for(const label of ['', ' ', 'abc', '2', 'NaN', 'Infinity', '0x0'])assert.equal(predict(model,'duration,proto,label\n8,tcp,'+label,.05).labeled_rows,0);
for(const text of ['', 'a,a\n1,2', 'a,\n1,2', 'a,b\n1', 'a\n"unterminated', 'a\n'+Array(1001).fill('1').join('\n')])assert.throws(()=>parseCSV(text));
for(const raw of ['', 'NaN', 'Infinity', '1e400', 'abc', '0x10', '0b10', '0o10'])assert.throws(()=>transform(model,[{duration:raw,proto:'tcp'}]));
assert.throws(()=>transform(model,[{proto:'tcp'}]));
assert.throws(()=>transform(model,[{duration:'8',proto:''}]));
assert.throws(()=>predict(model,csv,.03));
console.log('PASS: CSV quoting/schema/limits, numeric validation, metadata isolation, category handling, no-label metrics and threshold contract');
