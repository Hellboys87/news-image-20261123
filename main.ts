// News-image entry for make.fun news-image-20261123 (Node 22, stdlib only).
//
// The front page is pre-drawn in entry.png beside this file (render.py drew
// it locally with PIL and DejaVu fonts). This program only copies that
// finished image to the output directory, so it needs no fonts, no packages
// and no network, and every run writes identical bytes. The output directory
// is created when it does not exist yet.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
const target = join(outDir, 'entry.png');

mkdirSync(dirname(target), { recursive: true });
copyFileSync(source, target);
