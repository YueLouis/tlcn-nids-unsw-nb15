import assert from 'node:assert/strict';
import {createDownloadWorker} from '../deployment/cloudflare/zip-download.mjs';

const parts = [new Uint8Array([0x50, 0x4b, 3, 4]), new Uint8Array([0, 1, 255]), new Uint8Array([80, 75, 5, 6])];
const manifest = {path: '/downloads/ATTQ.zip', filename: 'ATTQ.zip', bytes: 11,
  sha256: 'example', parts: parts.map((data, index) => ({path: '/parts/' + index}))};
const worker = createDownloadWorker(manifest);
const requests = [];
const env = {ASSETS: {async fetch(request) {
  requests.push(request.url);
  const path = new URL(request.url).pathname;
  if (path.startsWith('/parts/')) return new Response(parts[Number(path.split('/').at(-1))]);
  return new Response('static');
}}};
const url = 'https://example.workers.dev/downloads/ATTQ.zip';
const head = await worker.fetch(new Request(url, {method: 'HEAD'}), env);
assert.equal(head.status, 200); assert.equal(head.headers.get('content-length'), '11');
assert.equal(head.headers.get('content-type'), 'application/zip');
assert.equal(await head.text(), ''); assert.equal(requests.length, 0);
const download = await worker.fetch(new Request(url), env);
assert.equal(download.headers.get('content-disposition'), 'attachment; filename="ATTQ.zip"');
assert.deepEqual(new Uint8Array(await download.arrayBuffer()), new Uint8Array([80, 75, 3, 4, 0, 1, 255, 80, 75, 5, 6]));
assert.deepEqual(requests.map((item) => new URL(item).pathname), ['/parts/0', '/parts/1', '/parts/2']);
assert.equal((await worker.fetch(new Request(url, {method: 'POST'}), env)).status, 405);
const ordinary = await worker.fetch(new Request('https://example.workers.dev/ho-so'), env);
assert.equal(await ordinary.text(), 'static');
const broken = await worker.fetch(new Request(url), {ASSETS: {async fetch() {return new Response('missing', {status: 404});}}});
await assert.rejects(broken.arrayBuffer(), /Offline archive part unavailable/);
console.log('PASS: ZIP streamed in order; HEAD metadata; method guard; static pass-through; missing-part fails');
