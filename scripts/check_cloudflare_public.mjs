// Anonymous HTTP audit and actual worker execution over verified deployed bytes.
// Node supplies Fetch/Web Streams; this is not a browser or layout test.
import assert from 'node:assert/strict';
import {readFile, readdir, writeFile} from 'node:fs/promises';
import {join, relative} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';

const [origin, dist, referencePath, receiptPath] = process.argv.slice(2);
assert.ok(origin && dist && referencePath && receiptPath,
  'Usage: node scripts/check_cloudflare_public.mjs URL DIST PYTHON_REFERENCE RECEIPT');
assert.equal(new URL(origin).protocol, 'https:');
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const nativeFetch = globalThis.fetch;
const downloaded = new Map();
const checks = [];
async function get(path) {
  const response = await nativeFetch(new URL(path, origin + '/'), {
    headers: {'User-Agent': 'Mozilla/5.0 NIDS-public-audit'},
    signal: AbortSignal.timeout(45000),
  });
  return {response, bytes: Buffer.from(await response.arrayBuffer())};
}
async function files(directory) {
  const rows = [];
  for (const item of await readdir(directory, {withFileTypes: true})) {
    const path = join(directory, item.name);
    if (item.isDirectory()) rows.push(...await files(path));
    else if (item.isFile() && item.name !== '_headers') rows.push(path);
  }
  return rows;
}
const pending = await files(dist);
let index = 0;
await Promise.all(Array.from({length: 4}, async () => {
  while (index < pending.length) {
    const local = pending[index++];
    const path = '/' + relative(dist, local).replaceAll('\\', '/');
    const expected = await readFile(local);
    const {response, bytes} = await get(path);
    assert.equal(response.status, 200, path + ' must be public HTTP 200');
    assert.equal(hash(bytes), hash(expected), path + ' differs from build');
    const type = response.headers.get('content-type');
    if (path.endsWith('.mjs')) assert.match(type, /javascript/i);
    if (path.endsWith('.bin.gz')) {
      assert.equal(bytes[0], 0x1f); assert.equal(bytes[1], 0x8b);
      assert.match(type, /application\/octet-stream/i);
    }
    downloaded.set(path, {bytes, headers: Object.fromEntries(response.headers)});
    checks.push({path, status: response.status, bytes: bytes.length, sha256: hash(bytes),
      content_type: type, content_encoding: response.headers.get('content-encoding'),
      matches_build: true});
  }
}));
for (const path of ['/', '/ho-so', '/ho-so.html']) {
  const {response, bytes} = await get(path);
  assert.equal(response.status, 200, path);
  const local = join(dist, path === '/' ? 'index.html' : 'ho-so.html');
  assert.equal(hash(bytes), hash(await readFile(local)), path);
}
const missing = await get('/models/no-such-model.bin.gz');
assert.equal(missing.response.status, 404, 'Missing model must never be a 200 SPA page');

// Run the shipped worker module with Fetch responses obtained above, including
// its DecompressionStream and parameter unpacking; no CSV leaves this process.
let messages = [];
globalThis.self = {postMessage(message) {messages.push(message);}};
globalThis.fetch = async (input) => {
  const path = new URL(input, origin + '/').pathname;
  const item = downloaded.get(path);
  assert.ok(item, 'Worker requested an unverified asset: ' + path);
  return new Response(item.bytes, {status: 200, headers: item.headers});
};
const outcomes = [];
try {
  await import(pathToFileURL(join(dist, 'browser-worker.mjs')));
  const reference = JSON.parse(await readFile(referencePath, 'utf8'));
  for (const row of reference.cases) {
    const expectedPrediction = row.prediction ?? row;
    messages = [];
    await self.onmessage({data: {id: row.run_id + '-' + row.target,
      payload: {scenario: row.scenario, model: row.model, target: row.target, case: 'mixed'}}});
    const error = messages.find((message) => message.error);
    assert.ok(!error, error?.error);
    const actual = messages.find((message) => message.result)?.result?.prediction;
    assert.ok(actual, 'Worker did not produce a result');
    assert.equal(actual.threshold, expectedPrediction.threshold);
    assert.deepEqual(actual.confusion, expectedPrediction.confusion);
    assert.equal(actual.results.length, expectedPrediction.results.length);
    let maxError = 0;
    actual.results.forEach((item, position) => {
      const expected = expectedPrediction.results[position];
      assert.equal(item.record_id, expected.record_id);
      assert.equal(item.prediction, expected.prediction);
      assert.equal(item.threshold, expected.threshold);
      const error = Math.abs(item.score - expected.score);
      assert.ok(error <= 1e-6 * Math.max(1, Math.abs(expected.score)),
        row.run_id + ' score differs from Python');
      maxError = Math.max(maxError, error);
    });
    outcomes.push({run_id: row.run_id, target: row.target, rows: actual.rows,
      confusion: actual.confusion, max_absolute_score_error: maxError,
      prediction_mismatches: 0, threshold_matches: true});
  }
} finally {
  globalThis.fetch = nativeFetch;
  delete globalThis.self;
}
const receipt = {checked_at_utc: new Date().toISOString(), url: origin,
  verification: 'Anonymous HTTP; actual shipped worker in Node over downloaded bytes, not a browser UI test',
  credential_used: false, all_asset_hashes_match: true,
  model_files: checks.filter((row) => row.path.endsWith('.bin.gz')).length,
  root_and_hub_routes_pass: true, missing_model_http_status: 404,
  assets: checks.sort((a, b) => a.path.localeCompare(b.path)), inference: outcomes,
  clipboard_download_browser_e2e: 'NOT_RETESTED', layout_no_scroll: 'NOT_RETESTED'};
await writeFile(receiptPath, JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify({assets: checks.length, model_files: receipt.model_files,
  inference_cases: outcomes.length, predictions: outcomes.reduce((sum, row) => sum + row.rows, 0),
  max_score_error: Math.max(...outcomes.map((row) => row.max_absolute_score_error)),
  missing_model_http_status: 404, receipt: receiptPath}));
