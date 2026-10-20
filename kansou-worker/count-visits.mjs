// 来てくれた人の数を、日ごとに数える（アプリを開いた日に、一台から一度だけ届く記録）
// 使い方: このフォルダ（kansou-worker）で  node count-visits.mjs
//         直近の日数だけ見るなら          node count-visits.mjs 14
// 中身は KV の key list（metadata つき）だけで数える。一件ずつ読みには行かない
import { execSync } from 'node:child_process';

const NAMESPACE = 'd850e18e4a3545078b4a0d1120f58cb8';
const days = Number(process.argv[2]) || 0;

const out = execSync(
  `npx wrangler kv key list --namespace-id ${NAMESPACE} --remote --prefix visit:`,
  { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'inherit'] },
);
const keys = JSON.parse(out.slice(out.indexOf('[')));

const byDay = new Map();
for (const k of keys) {
  const m = k.metadata || {};
  const day = m.day || k.name.split(':')[1];
  const d = byDay.get(day) || { all: 0, first: 0, shugoshin: 0, hatsumoude: 0 };
  d.all++;
  if (m.first) d.first++;
  if (m.via === 'shugoshin') d.shugoshin++;
  if (m.via === 'hatsumoude') d.hatsumoude++;
  byDay.set(day, d);
}

let rows = [...byDay.entries()].sort((a, b) => a[0].localeCompare(b[0]));
if (days) rows = rows.slice(-days);
console.log('日付         来た人  うち新しく  また来た  守護神の入口  初詣の入口');
for (const [day, d] of rows) {
  const cols = [d.all, d.first, d.all - d.first, d.shugoshin, d.hatsumoude];
  console.log(day + '  ' + cols.map((n, i) => String(n).padStart([6, 10, 8, 12, 10][i])).join(''));
}
const total = rows.reduce((s, [, d]) => s + d.first, 0);
console.log('\n新しく来た人の合計（この表の範囲）: ' + total);
