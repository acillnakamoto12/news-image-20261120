// News-image entry (Node 22, standard library only): its image is the entry.png beside this file,
// drawn by generate.py (Python + Pillow) from news.json — the day's verified stories.
// The program copies it to /output/entry.png. Deterministic: the same bytes on every run.
//
// Before copying, it checks the image is a real 1024x1024 PNG (signature + IHDR
// dimensions) and exits non-zero with a clear error if it is not, so a broken or
// wrong-sized image can never be submitted silently.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const ENTRY = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

let bytes: Buffer;
try {
  bytes = readFileSync(ENTRY);
} catch {
  console.error('error: entry.png is missing beside main.ts — cannot produce the entry image');
  process.exit(1);
}

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const isValidPng =
  bytes.length >= 33 &&
  bytes.subarray(0, 8).equals(PNG_SIGNATURE) &&
  bytes.readUInt32BE(8) === 13 &&
  bytes.subarray(12, 16).toString('latin1') === 'IHDR' &&
  bytes.readUInt32BE(16) === 1024 &&
  bytes.readUInt32BE(20) === 1024;

if (!isValidPng) {
  console.error('error: entry.png is not a valid 1024x1024 PNG — refusing to copy a broken entry image');
  process.exit(1);
}

copyFileSync(ENTRY, join(outDir, 'entry.png'));
