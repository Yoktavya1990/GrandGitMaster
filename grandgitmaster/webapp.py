"""The GrandGitMaster mobile web app (PWA), embedded as a single page.

Installable on any phone: open it, "Add to Home Screen", done. Talks to the
JSON API served by server.py. Built for non-coders: scores, medals and
plain-language flags instead of jargon.
"""

MANIFEST = {
    "name": "GrandGitMaster",
    "short_name": "GGM",
    "description": "The king of Git — the best repo for anything, ranked.",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0d1117",
    "theme_color": "#0d1117",
    "icons": [{
        "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
               "viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' "
               "fill='%230d1117'/%3E%3Ctext x='50' y='68' font-size='52' "
               "text-anchor='middle'%3E%F0%9F%91%91%3C/text%3E%3C/svg%3E",
        "sizes": "any", "type": "image/svg+xml", "purpose": "any"}],
}

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0d1117">
<link rel="manifest" href="/manifest.json">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext x='50' y='72' font-size='64' text-anchor='middle'%3E%F0%9F%91%91%3C/text%3E%3C/svg%3E">
<title>GrandGitMaster</title>
<style>
:root{
  --bg:#0d1117; --panel:#161b22; --border:#30363d; --text:#e6edf3;
  --dim:#8b949e; --gold:#e3b341; --accent:#58a6ff; --green:#3fb950;
}
@media (prefers-color-scheme: light){
  :root{--bg:#f6f8fa;--panel:#ffffff;--border:#d0d7de;--text:#1f2328;--dim:#57606a}
}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--text);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  padding-bottom:env(safe-area-inset-bottom)}
header{position:sticky;top:0;z-index:5;background:var(--bg);padding:14px 16px 10px;
  border-bottom:1px solid var(--border)}
h1{font-size:20px;display:flex;align-items:center;gap:8px}
h1 small{color:var(--dim);font-size:12px;font-weight:400}
#search{width:100%;margin-top:10px;padding:12px 14px;border-radius:12px;border:1px solid var(--border);
  background:var(--panel);color:var(--text);font-size:16px;outline:none}
#search:focus{border-color:var(--accent)}
#chips{display:flex;gap:8px;overflow-x:auto;padding:10px 0 4px;scrollbar-width:none}
#chips::-webkit-scrollbar{display:none}
.chip{flex:0 0 auto;padding:6px 12px;border-radius:999px;border:1px solid var(--border);
  background:var(--panel);color:var(--dim);font-size:13px;cursor:pointer;white-space:nowrap}
.chip.on{background:var(--gold);color:#1f2328;border-color:var(--gold);font-weight:600}
main{padding:12px 16px;max-width:720px;margin:0 auto}
.card{background:var(--panel);border:1px solid var(--border);border-radius:14px;
  padding:14px;margin-bottom:12px;position:relative}
.card.champ{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold)}
.crown{position:absolute;top:-11px;right:14px;background:var(--gold);color:#1f2328;
  font-size:11px;font-weight:700;padding:2px 10px;border-radius:999px}
.rname{font-weight:600;font-size:16px;word-break:break-all}
.rname a{color:var(--accent);text-decoration:none}
.rdesc{color:var(--dim);font-size:14px;margin:4px 0 8px}
.meta{display:flex;flex-wrap:wrap;gap:6px 12px;font-size:12.5px;color:var(--dim);margin-bottom:8px}
.scorebar{display:flex;align-items:center;gap:10px}
.meter{flex:1;height:8px;border-radius:4px;background:var(--border);overflow:hidden}
.meter i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,#f85149,var(--gold),var(--green))}
.score{font-weight:700;font-variant-numeric:tabular-nums;min-width:44px;text-align:right}
.verdict{font-size:13px;margin-top:6px}
.flags{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.flag{font-size:11.5px;background:var(--bg);border:1px solid var(--border);
  border-radius:999px;padding:3px 9px;color:var(--dim)}
.empty{color:var(--dim);text-align:center;padding:40px 20px}
#stats{color:var(--dim);font-size:12px;margin:2px 0 8px}
#addbar{position:fixed;bottom:0;left:0;right:0;display:flex;gap:8px;padding:10px 16px calc(10px + env(safe-area-inset-bottom));
  background:var(--bg);border-top:1px solid var(--border)}
#addbar input{flex:1;padding:11px 13px;border-radius:12px;border:1px solid var(--border);
  background:var(--panel);color:var(--text);font-size:15px;outline:none}
#addbar button{padding:11px 18px;border-radius:12px;border:0;background:var(--gold);
  color:#1f2328;font-weight:700;font-size:15px;cursor:pointer}
main{padding-bottom:86px}
.pending{opacity:.65}
</style>
</head>
<body>
<header>
  <h1>👑 GrandGitMaster <small>the best repo for anything</small></h1>
  <input id="search" type="search" placeholder="What do you need? e.g. scraping, agents, free APIs…" autocomplete="off">
  <div id="chips"></div>
</header>
<main>
  <div id="stats"></div>
  <div id="list"><div class="empty">Loading the kingdom…</div></div>
</main>
<div id="addbar">
  <input id="add" placeholder="Paste a GitHub or X link (or any text)…">
  <button onclick="addStuff()">Ingest</button>
</div>
<script>
let cat = "", q = "";
const $ = s => document.querySelector(s);
async function api(p, opt){ const r = await fetch("/api/"+p, opt); return r.json(); }
function esc(s){ return (s||"").replace(/[&<>"]/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
function card(r, champ){
  const pend = r.status !== "scored";
  return `<div class="card ${champ?"champ":""} ${pend?"pending":""}">
    ${champ?'<div class="crown">👑 CATEGORY KING</div>':""}
    <div class="rname"><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.full_name)}</a></div>
    <div class="rdesc">${esc(r.description) || (pend?"⏳ waiting for the Ringer…":"")}</div>
    <div class="meta">
      <span>📂 ${esc(r.category)}</span>
      ${r.stars?`<span>⭐ ${r.stars.toLocaleString()}</span>`:""}
      ${r.language?`<span>💬 ${esc(r.language)}</span>`:""}
    </div>
    ${pend?"":`<div class="scorebar"><div class="meter"><i style="width:${r.score}%"></i></div>
      <div class="score">${r.score}</div></div>
    <div class="verdict">${esc(r.verdict)}</div>`}
    <div class="flags">${(r.flags||[]).map(f=>`<span class="flag">${esc(f)}</span>`).join("")}</div>
  </div>`;
}
async function load(){
  const s = await api("stats");
  $("#stats").textContent = `${s.total||0} repos · ${s.scored||0} ranked · ${s.from_x||0} caught from X`;
  const chips = await api("categories");
  $("#chips").innerHTML = `<span class="chip ${!cat?"on":""}" onclick="setCat('')">👑 Champions</span>` +
    chips.categories.map(c=>`<span class="chip ${cat===c.category?"on":""}"
      onclick="setCat('${c.category}')">${c.category} (${c.n})</span>`).join("");
  let data, champNames = new Set();
  if (q) data = (await api("search?q="+encodeURIComponent(q)+(cat?"&category="+cat:""))).results;
  else if (cat) data = (await api("top?category="+cat)).top;
  else { data = (await api("top")).champions; data.forEach(r=>champNames.add(r.full_name)); }
  $("#list").innerHTML = data.length
    ? data.map(r=>card(r, champNames.has(r.full_name))).join("")
    : `<div class="empty">Nothing here yet.<br>Paste a GitHub or X link below 👇<br>then run <b>ggm ringer</b> to rank it.</div>`;
}
function setCat(c){ cat = c; load(); }
let t; $("#search").addEventListener("input", e=>{ clearTimeout(t); t=setTimeout(()=>{ q=e.target.value.trim(); load(); },250); });
async function addStuff(){
  const v = $("#add").value.trim(); if(!v) return;
  const out = await api("ingest", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({text:v})});
  $("#add").value = "";
  alert(out.message || "Ingested.");
  load();
}
load();
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(()=>{});
</script>
</body>
</html>
"""

SERVICE_WORKER = """
self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => self.clients.claim());
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || e.request.url.includes('/api/')) return;
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
  e.waitUntil(caches.open('ggm-v1').then(c => fetch(e.request).then(r => c.put(e.request, r)).catch(()=>{})));
});
"""
