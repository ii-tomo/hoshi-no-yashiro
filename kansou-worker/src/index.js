// 星の社 感想帳 — 送信を受けてKVにしまうだけの、ちいさな社務所
// 読み出しAPIは持たない（感想を見るのは wrangler kv 経由のみ。漏れる口を作らない）
const ALLOWED = [
  'https://hoshi-no-yashiro.pages.dev',
  'http://localhost:8936',
  'http://127.0.0.1:8936',
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const cors = {
      'Access-Control-Allow-Origin': ALLOWED.includes(origin) ? origin : ALLOWED[0],
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST') {
      return new Response('hoshi-no-yashiro kansou api', { status: 200, headers: cors });
    }
    let data;
    try { data = await request.json(); } catch {
      return new Response('bad json', { status: 400, headers: cors });
    }
    if (data.hp) {
      // honeypot: botには静かに「ok」を返して何もしない
      return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { ...cors, 'Content-Type': 'application/json' } });
    }
    const clip = (v, n) => String(v == null ? '' : v).slice(0, n);
    const rec = {
      name: clip(data.name, 40),          // ペンネーム（任意）
      device: clip(data.device, 20),      // iPhone / Android / その他・PC
      moved: clip(data.moved, 20),        // うごいた / ときどき変 / うごかなかった
      favorite: clip(data.favorite, 20),  // 好きだった遊び
      trouble: clip(data.trouble, 1000),  // わかりにくかったところ（任意）
      comment: clip(data.comment, 1000),  // ひとこと感想（任意）
      consent: clip(data.consent, 30),    // 紹介の同意
      at: new Date().toISOString(),
      ua: clip(request.headers.get('User-Agent'), 200),
    };
    const key = 'kansou:' + rec.at + ':' + Math.random().toString(36).slice(2, 8);
    await env.KANSOU.put(key, JSON.stringify(rec));
    return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { ...cors, 'Content-Type': 'application/json' } });
  },
};
