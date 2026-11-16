#!/usr/bin/env node
// Generates videos through the same MuAPI endpoints the Open Higgsfield app uses.
// No dependencies; needs Node 18+.
//
//   node make_video.mjs prompts.json
//   node make_video.mjs --prompt "a fox running through snow" --model seedance-lite-t2v
//
// The key comes from MUAPI_KEY. In a Claude cloud session with the key saved as a
// network secret for api.muapi.ai, the proxy injects it and MUAPI_KEY can stay unset.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const BASE = 'https://api.muapi.ai/api/v1';
const KEY = process.env.MUAPI_KEY || 'injected-by-proxy';
const HEADERS = { 'Content-Type': 'application/json', 'x-api-key': KEY };
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), 'videos');
const DEFAULT_MODEL = 'seedance-lite-t2v';
const PARAMS = ['prompt', 'aspect_ratio', 'duration', 'resolution', 'quality', 'mode', 'image_url'];
const DONE = new Set(['completed', 'succeeded', 'success']);
const FAILED = new Set(['failed', 'error', 'cancelled', 'canceled']);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function parseArgs(argv) {
  const job = {};
  let file;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) job[argv[i].slice(2).replace(/-/g, '_')] = argv[++i];
    else file = argv[i];
  }
  return { job, file };
}

async function generate(job, index) {
  const model = job.model || DEFAULT_MODEL;
  const name = job.name || `video-${String(index + 1).padStart(2, '0')}`;
  const payload = {};
  for (const k of PARAMS) if (job[k] !== undefined) payload[k] = job[k];
  if (payload.duration !== undefined) payload.duration = Number(payload.duration);

  const submit = await fetch(`${BASE}/${model}`, { method: 'POST', headers: HEADERS, body: JSON.stringify(payload) });
  if (!submit.ok) throw new Error(`submit ${submit.status}: ${(await submit.text()).slice(0, 300)}`);
  const submitted = await submit.json();
  const id = submitted.request_id || submitted.id;
  if (!id) throw new Error(`no request id in response: ${JSON.stringify(submitted).slice(0, 300)}`);
  console.log(`[${name}] submitted to ${model}, request ${id}`);

  let result;
  for (let attempt = 0; attempt < 900; attempt++) {   // up to 30 minutes
    await sleep(2000);
    const poll = await fetch(`${BASE}/predictions/${id}/result`, { headers: HEADERS }).catch(() => null);
    if (!poll || poll.status >= 500) continue;
    if (!poll.ok) throw new Error(`poll ${poll.status}: ${(await poll.text()).slice(0, 300)}`);
    const body = await poll.json().catch(() => null);
    const status = body?.status?.toLowerCase();
    if (DONE.has(status)) { result = body; break; }
    if (FAILED.has(status)) throw new Error(`generation failed: ${JSON.stringify(body.error ?? body.message ?? body).slice(0, 300)}`);
  }
  if (!result) throw new Error(`timed out waiting for request ${id}`);

  const url = result.outputs?.[0] || result.url || result.output?.url;
  if (!url) throw new Error(`no output url: ${JSON.stringify(result).slice(0, 300)}`);
  const video = await fetch(url);
  if (!video.ok) throw new Error(`download ${video.status} from ${url}`);
  await mkdir(OUT, { recursive: true });
  const file = path.join(OUT, `${name}.mp4`);
  await writeFile(file, Buffer.from(await video.arrayBuffer()));
  console.log(`[${name}] saved ${file}`);
  return file;
}

const { job, file } = parseArgs(process.argv.slice(2));
const jobs = file ? JSON.parse(await readFile(file, 'utf8')) : [job];
if (!jobs.length || jobs.some((j) => !j.prompt)) {
  console.error('Every job needs a prompt. See prompts.example.json.');
  process.exit(2);
}

// Jobs run one at a time so a bad key or empty balance fails on the first, not on all.
let failures = 0;
for (const [i, j] of jobs.entries()) {
  try { await generate(j, i); }
  catch (e) { failures++; console.error(`[${j.name || i + 1}] ${e.message}`); }
}
process.exit(failures ? 1 : 0);
