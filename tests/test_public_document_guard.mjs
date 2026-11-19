import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createPublicDemoWorker} from '../deployment/cloudflare/private-documents.mjs';

const policy = JSON.parse(readFileSync(new URL('../deployment/cloudflare/private-documents.json', import.meta.url)));
const worker = createPublicDemoWorker(policy);
const calls = [];
const env = {ASSETS: {async fetch(request) {calls.push(request.url); return new Response('public demo');}}};
const retired = [
  '/downloads/ATTQ_NIDS_BAN_GIAO_20261114.zip',
  '/downloads/NhomTLCN_tong_20261114.pdf',
  '/downloads/Nguon_dot4_20261114.zip',
  '/downloads/TU_KIEM_CA_NHAN_20261115.md',
  '/downloads/MANIFEST.json', '/downloads',
  '/package-parts/ATTQ_NIDS_20261114_00.part', '/package-parts',
  '/assets/BAO_CAO_DOT3.pdf', '/other/report.pdf',
  '/%64ownloads/source.zip', '/ASSETS/BAO_CAO_DOT3.PDF',
];
for (const path of retired) {
  for (const method of ['GET', 'HEAD']) {
    const response = await worker.fetch(new Request('https://example.test' + path + '?download=1', {method}), env);
    assert.equal(response.status, 302, path);
    const expected = decodeURIComponent(path).toLowerCase() === '/assets/bao_cao_dot3.pdf'
      ? policy.round3_url : policy.reports_url;
    assert.equal(response.headers.get('location'), expected, path);
    assert.equal(response.headers.get('cache-control'), 'no-store');
    assert.equal(await response.text(), '');
  }
  const response = await worker.fetch(new Request('https://example.test' + path, {method: 'POST'}), env);
  assert.equal(response.status, 405);
}
assert.equal(calls.length, 0, 'Private paths must never be read from the ASSETS binding');
for (const path of ['/', '/ho-so', '/ho-so.html', '/browser-worker.mjs',
                    '/models/CS-RF-S42.bin.gz', '/cases/normal.csv', '/assets/AP_MEAN_STD.csv']) {
  const response = await worker.fetch(new Request('https://example.test' + path), env);
  assert.equal(await response.text(), 'public demo');
}
assert.equal(calls.length, 7);
const config = JSON.parse(readFileSync(new URL('../deployment/cloudflare/wrangler.json', import.meta.url)));
assert.equal(config.assets.run_worker_first, true, 'The guard runs before every static asset');
const entry = readFileSync(new URL('../deployment/cloudflare/download.mjs', import.meta.url), 'utf8');
assert.match(entry, /createPublicDemoWorker\(policy\)/);
assert.doesNotMatch(entry, /download-manifest|createDownloadWorker/);
console.log('PASS: retired documents redirect without reading assets; demo, model and CSV routes pass through');
