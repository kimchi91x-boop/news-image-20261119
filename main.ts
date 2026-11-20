// news-image-20261119 entry (Node 22, standard library only).
//
// The entry's image is the entry.png beside this file: a six-panel editorial
// poster summing up Thursday 19 November 2026 (the Trump-Xi-Putin trilateral
// summit in Shenzhen, the UN court ruling that Myanmar committed genocide
// against the Rohingya, Anthropic's record IPO, Iran widening its Gulf
// attacks around Hormuz, Denmark approving the Greenland-US Arctic security
// pact, and Ukraine hitting the Crimea bridge again). The file holds JPEG
// bytes under the name entry.png, which the gate accepts: PNG or JPEG, told
// apart by the first bytes, at most 1 MiB and 1024 by 1024 pixels.
//
// The program copies the image to /output/entry.png. Outside the grader's
// container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

if (!existsSync(source)) {
  console.error(`entry image missing: ${source}`);
  process.exit(1);
}

// Self-check against the gate's limits before copying: a PNG or JPEG (by
// first bytes) of at most 1 MiB. Fail loudly here rather than ship an
// invalid entry.
const bytes = readFileSync(source);
const isPng = bytes.length >= 8 && bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
const isJpeg = bytes.length >= 3 && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff;
if (!isPng && !isJpeg) {
  console.error('entry image is neither PNG nor JPEG');
  process.exit(1);
}
if (statSync(source).size > 1048576) {
  console.error('entry image is over the 1 MiB gate limit');
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target} (${bytes.length} bytes, ${isJpeg ? 'JPEG' : 'PNG'})`);
