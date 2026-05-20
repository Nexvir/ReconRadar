"""
ReconRadar APOLLO v6.0 PRO — Frontend Module
---------------------------------------------
Imported by backend.py via: from frontend import HTML_TEMPLATE
Drop-in replacement for the original frontend.py.
Compatible with all WebSocket messages: log / result / status
"""

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ReconRadar APOLLO</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Bebas+Neue&family=Exo+2:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
/* ═══════════════════════════════════════════
   DESIGN SYSTEM
═══════════════════════════════════════════ */
:root {
  /* palette */
  --bg0:       #020509;
  --bg1:       #050c12;
  --bg2:       #080f18;
  --bg3:       #0d1822;
  --bg4:       #111f2e;

  --g0:        #00ff88;   /* primary accent — phosphor green */
  --g1:        #00cc6a;
  --g2:        #006636;
  --g3:        #003320;

  --c0:        #00e5ff;   /* secondary — electric cyan */
  --c1:        #00b8cc;
  --c2:        #005566;

  --r0:        #ff2244;   /* danger red */
  --r1:        #cc0033;

  --a0:        #ff8c00;   /* amber warning */
  --p0:        #bf5fff;   /* purple info */

  --t0:        #cce8ff;   /* text bright */
  --t1:        #7098b8;   /* text mid */
  --t2:        #2e4860;   /* text dim */
  --t3:        #182838;   /* text ghost */

  --border:    rgba(0,229,255,.08);
  --border-hl: rgba(0,255,136,.22);

  --mono: 'JetBrains Mono', 'Courier New', monospace;
  --ui:   'Exo 2', sans-serif;
  --head: 'Bebas Neue', sans-serif;

  --rad: 0px;  /* sharp edges — military aesthetic */
}

/* ── reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; background: var(--bg0); color: var(--t1); font-family: var(--mono); font-size: 12px; overflow: hidden; }

/* ── noise texture overlay ── */
body::before {
  content: '';
  position: fixed; inset: 0; z-index: 9998; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  opacity: .6;
}

/* ── scanlines ── */
body::after {
  content: '';
  position: fixed; inset: 0; z-index: 9997; pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent, transparent 2px,
    rgba(0,255,136,.018) 2px, rgba(0,255,136,.018) 4px
  );
}

/* ── custom scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--t3); }
::-webkit-scrollbar-thumb:hover { background: var(--t2); }

/* ══════════════════════════════════════════
   APP SHELL  —  3-column layout
   [sidebar 270px] [terminal flex] [results flex]
══════════════════════════════════════════ */
#app {
  display: grid;
  grid-template-columns: 264px 1fr 1.6fr;
  height: 100vh;
  overflow: hidden;
  gap: 0;
}

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
#sidebar {
  background: var(--bg1);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* corner bracket decoration */
#sidebar::before {
  content: '';
  position: absolute; top: 0; left: 0;
  width: 28px; height: 28px;
  border-top: 2px solid var(--g0);
  border-left: 2px solid var(--g0);
  pointer-events: none; z-index: 10;
}

/* ── logo ── */
.sb-head {
  padding: 18px 16px 12px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.logo-row {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 10px;
}
.logo-icon {
  width: 36px; height: 36px;
  background: var(--g3);
  border: 1px solid var(--g2);
  display: flex; align-items: center; justify-content: center;
  color: var(--g0); font-size: 16px;
  box-shadow: 0 0 12px rgba(0,255,136,.15), inset 0 0 8px rgba(0,255,136,.08);
  flex-shrink: 0;
  position: relative;
}
.logo-icon::after {
  content: '';
  position: absolute; bottom: -1px; right: -1px;
  width: 8px; height: 8px;
  border-right: 1px solid var(--g0);
  border-bottom: 1px solid var(--g0);
}
.logo-text {
  font-family: var(--head);
  font-size: 20px;
  letter-spacing: .12em;
  color: var(--t0);
  line-height: 1;
}
.logo-text span { color: var(--g0); }
.logo-sub {
  font-size: 9px;
  letter-spacing: .22em;
  color: var(--t2);
  margin-top: 2px;
  text-transform: uppercase;
}
.version-tag {
  display: inline-block;
  background: rgba(0,255,136,.07);
  border: 1px solid rgba(0,255,136,.22);
  color: var(--g0);
  font-size: 8px; letter-spacing: .18em;
  padding: 1px 7px;
  margin-left: 2px;
}

.status-row {
  display: flex; align-items: center; gap: 10px;
}
#connection-status {
  display: flex; align-items: center; gap: 6px;
  font-size: 10px; letter-spacing: .08em;
}
.dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-on {
  background: var(--g0);
  box-shadow: 0 0 8px var(--g0), 0 0 16px rgba(0,255,136,.3);
}
.dot-off {
  background: var(--r0);
  animation: dotblink 1.4s step-end infinite;
}
@keyframes dotblink { 50% { opacity: .12; } }

#scan-timer {
  font-family: var(--mono);
  font-size: 10px; letter-spacing: .1em;
  color: var(--a0);
  background: rgba(255,140,0,.06);
  border: 1px solid rgba(255,140,0,.2);
  padding: 1px 8px;
}

/* ── sidebar scroll body ── */
.sb-body {
  flex: 1; overflow-y: auto; overflow-x: hidden;
}

/* ── section ── */
.sb-sec {
  padding: 11px 14px;
  border-bottom: 1px solid var(--border);
}
.sb-label {
  font-size: 8px; text-transform: uppercase;
  letter-spacing: .24em; color: var(--t2);
  margin-bottom: 8px;
  display: flex; align-items: center; gap: 6px;
}
.sb-label::after {
  content: '';
  flex: 1; height: 1px;
  background: linear-gradient(to right, var(--border), transparent);
}
.sb-label i { font-size: 8px; color: var(--g1); }

/* ── inputs ── */
.inp-wrap { position: relative; margin-bottom: 6px; }
.inp-wrap:last-child { margin-bottom: 0; }
.inp-ico {
  position: absolute; left: 10px; top: 50%;
  transform: translateY(-50%);
  color: var(--t2); font-size: 10px;
  pointer-events: none;
}
.inp {
  width: 100%;
  background: var(--bg0);
  border: 1px solid var(--border);
  color: var(--t0);
  padding: 8px 10px 8px 28px;
  font-family: var(--mono); font-size: 11px;
  outline: none;
  transition: border-color .15s, box-shadow .15s;
}
.inp:focus {
  border-color: rgba(0,255,136,.35);
  box-shadow: 0 0 0 1px rgba(0,255,136,.08), 0 0 14px rgba(0,255,136,.06);
}
.inp::placeholder { color: var(--t3); font-size: 10px; }
.inp:disabled { opacity: .3; cursor: not-allowed; }
select.inp { appearance: none; cursor: pointer; }
textarea.inp {
  padding: 8px 10px;
  resize: vertical; min-height: 56px; line-height: 1.6;
  color: var(--g0);
  border-color: rgba(0,255,136,.18);
  font-size: 10px;
}
textarea.inp::placeholder { color: var(--g2); font-size: 10px; }

/* ── modules grid ── */
.mods-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 4px;
}
.mod-lbl {
  display: flex; align-items: center; gap: 5px;
  padding: 5px 8px;
  background: var(--bg0);
  border: 1px solid var(--border);
  color: var(--t2); font-size: 10px;
  cursor: pointer;
  transition: all .12s;
  user-select: none;
  letter-spacing: .04em;
}
.mod-lbl:hover { border-color: var(--g2); color: var(--g1); }
.mod-lbl input[type="checkbox"] {
  accent-color: var(--g0);
  width: 10px; height: 10px;
  flex-shrink: 0;
}
.mod-lbl.full { grid-column: 1 / -1; }
.mod-lbl:has(input:checked) {
  border-color: rgba(0,255,136,.28);
  color: var(--g0);
  background: rgba(0,255,136,.04);
}

/* ── buttons ── */
.btn-row { display: flex; gap: 6px; }

#scan-btn {
  flex: 1;
  padding: 10px 8px;
  background: linear-gradient(135deg, var(--g2), var(--g3));
  border: 1px solid var(--g1);
  color: var(--g0);
  font-family: var(--head);
  font-size: 14px;
  letter-spacing: .14em;
  cursor: pointer;
  transition: all .15s;
  display: flex; align-items: center; justify-content: center; gap: 7px;
  box-shadow: 0 0 14px rgba(0,255,136,.12);
  position: relative; overflow: hidden;
}
#scan-btn::before {
  content: '';
  position: absolute; top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0,255,136,.18), transparent);
  transition: left .4s;
}
#scan-btn:hover:not(:disabled)::before { left: 150%; }
#scan-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--g1), var(--g2));
  box-shadow: 0 0 22px rgba(0,255,136,.25);
  color: #000;
}
#scan-btn:disabled { opacity: .3; cursor: not-allowed; }

#stop-btn {
  padding: 10px 12px;
  background: rgba(255,34,68,.04);
  border: 1px solid rgba(255,34,68,.22);
  color: var(--r0);
  font-family: var(--mono); font-size: 10px;
  cursor: pointer;
  transition: all .15s;
  display: flex; align-items: center; gap: 5px;
  letter-spacing: .06em;
}
#stop-btn:hover:not(:disabled) {
  background: rgba(255,34,68,.10);
  box-shadow: 0 0 12px rgba(255,34,68,.15);
}
#stop-btn:disabled { opacity: .2; cursor: not-allowed; }

/* ── sidebar footer ── */
.sb-foot {
  padding: 9px 14px;
  border-top: 1px solid var(--border);
  font-size: 10px; color: var(--t3);
  flex-shrink: 0;
}
.sb-foot a { color: var(--c0); text-decoration: none; }
.sb-foot a:hover { color: var(--g0); text-decoration: underline; }
.sb-foot .disc { font-size: 9px; color: var(--t3); margin-top: 3px; opacity: .5; }

/* ══════════════════════════════════════════
   TERMINAL  (middle column)
══════════════════════════════════════════ */
#term-col {
  display: flex; flex-direction: column;
  background: var(--bg0);
  border-right: 1px solid var(--border);
  overflow: hidden;
  position: relative;
}

/* animated corner brackets */
#term-col::before,
#term-col::after {
  content: '';
  position: absolute;
  width: 14px; height: 14px;
  pointer-events: none; z-index: 5;
}
#term-col::before {
  top: 0; right: 0;
  border-top: 1px solid var(--g0);
  border-right: 1px solid var(--g0);
}
#term-col::after {
  bottom: 0; left: 0;
  border-bottom: 1px solid var(--g0);
  border-left: 1px solid var(--g0);
}

.pane-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 6px 12px;
  background: var(--bg1);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  z-index: 4; position: relative;
}
.pane-title {
  font-size: 8px; letter-spacing: .26em; text-transform: uppercase;
  display: flex; align-items: center; gap: 7px;
}
.pane-title.green { color: var(--g0); }
.pane-title.cyan  { color: var(--c0); }
.live-dot {
  width: 6px; height: 6px;
  border-radius: 50%; background: var(--g0);
  animation: livepulse 2s ease-in-out infinite;
}
@keyframes livepulse {
  0%,100% { box-shadow: 0 0 4px var(--g0), 0 0 8px rgba(0,255,136,.4); opacity: 1; }
  50%      { box-shadow: none; opacity: .3; }
}

.pane-acts {
  display: flex; align-items: center; gap: 6px;
}
.pane-btn {
  background: none;
  border: 1px solid var(--border);
  color: var(--t2);
  font-family: var(--mono); font-size: 8px;
  padding: 2px 8px; letter-spacing: .08em;
  cursor: pointer;
  transition: all .12s;
  text-transform: uppercase;
}
.pane-btn:hover { border-color: var(--g2); color: var(--g0); }

.win-dots { display: flex; gap: 5px; margin-left: 6px; }
.win-dots span {
  width: 9px; height: 9px;
  border-radius: 50%;
  opacity: .6;
}

/* ── terminal body ── */
#terminal {
  flex: 1;
  overflow-y: auto;
  padding: 10px 13px;
  font-family: var(--mono);
  font-size: 11.5px;
  line-height: 1.8;
  color: var(--g0);
  word-break: break-word;
  white-space: pre-wrap;
}

/* log line colors */
.ll { display: block; }
.ll::before { content: '❯ '; color: var(--t3); font-size: 9px; }
.ll-err  { color: var(--r0) !important; }
.ll-warn { color: var(--a0) !important; }
.ll-sys  { color: var(--t2) !important; }
.ll-sys::before { content: '# '; color: var(--t3); font-size: 9px; }
.ll-crt  { color: var(--c0) !important; }
.ll-who  { color: var(--p0) !important; }
.ll-nmap { color: #ffd60a !important; }
.ll-http { color: #5ad2ff !important; }
.ll-sub  { color: var(--a0) !important; }
.ll-ok   { color: var(--g0) !important; font-weight: 600; }
.ll-phase {
  color: var(--g0) !important;
  font-weight: 700;
  padding: 2px 0;
  letter-spacing: .06em;
}
.ll-phase::before { content: '▶ '; color: var(--g1); font-size: 9px; }

.blinking-cursor {
  color: var(--g0);
  animation: curblink 1s step-end infinite;
}
@keyframes curblink { 50% { opacity: 0; } }

/* ── term stats bar ── */
.term-stats {
  display: grid; grid-template-columns: repeat(3, 1fr);
  border-top: 1px solid var(--border);
  flex-shrink: 0;
}
.stat-cell {
  padding: 7px 6px;
  text-align: center;
  border-right: 1px solid var(--border);
}
.stat-cell:last-child { border-right: none; }
.stat-num {
  display: block;
  font-family: var(--head);
  font-size: 18px;
  letter-spacing: .06em;
  line-height: 1.1;
  color: var(--g0);
}
.stat-num.red  { color: var(--r0); }
.stat-num.cyan { color: var(--c0); }
.stat-label {
  font-size: 7px; letter-spacing: .18em;
  text-transform: uppercase; color: var(--t3);
  margin-top: 1px;
}

/* progress bar */
#prog-wrap {
  height: 2px;
  background: var(--bg1);
  flex-shrink: 0;
}
#prog-bar {
  height: 100%; width: 0%;
  background: linear-gradient(90deg, var(--g0), var(--c0));
  transition: width .4s ease;
  box-shadow: 0 0 8px var(--g0);
}

/* ══════════════════════════════════════════
   RESULTS  (right column)
══════════════════════════════════════════ */
#results-col {
  display: flex; flex-direction: column;
  overflow: hidden;
  background: var(--bg1);
}

/* ── tab bar ── */
.tab-bar {
  display: flex; align-items: stretch;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  overflow-x: auto;
}
.tab-bar::-webkit-scrollbar { height: 0; }

.tab-btn {
  padding: 9px 14px;
  background: none; border: none;
  border-bottom: 2px solid transparent;
  border-right: 1px solid var(--border);
  color: var(--t2);
  font-family: var(--mono); font-size: 9px;
  letter-spacing: .1em; text-transform: uppercase;
  cursor: pointer; white-space: nowrap;
  transition: all .12s;
  display: flex; align-items: center; gap: 5px;
}
.tab-btn:hover { color: var(--t1); background: rgba(0,255,136,.02); }
.tab-btn.active {
  color: var(--g0);
  border-bottom-color: var(--g0);
  background: rgba(0,255,136,.04);
}
.tab-btn.active i { color: var(--g0); }
.tab-btn i { color: var(--t3); font-size: 9px; }

/* count bubble */
.tcnt {
  display: inline-block;
  min-width: 16px;
  text-align: center;
  padding: 0 4px;
  font-size: 8px;
  background: rgba(0,255,136,.08);
  border: 1px solid rgba(0,255,136,.15);
  color: var(--g1);
  line-height: 14px;
}
.tcnt.has { background: rgba(0,255,136,.15); color: var(--g0); }
.tcnt.red { background: rgba(255,34,68,.12); border-color: rgba(255,34,68,.3); color: var(--r0); }

.tab-actions {
  margin-left: auto;
  display: flex; align-items: center;
  gap: 8px; padding: 0 12px;
  flex-shrink: 0;
}
#asset-count {
  font-size: 9px; font-family: var(--mono);
  letter-spacing: .1em; color: var(--g0);
  background: rgba(0,255,136,.06);
  border: 1px solid rgba(0,255,136,.15);
  padding: 2px 10px;
}
.btn-export {
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--t1); font-family: var(--mono); font-size: 9px;
  letter-spacing: .06em; padding: 3px 10px;
  cursor: pointer; transition: all .12s;
  text-transform: uppercase;
}
.btn-export:hover { border-color: var(--c1); color: var(--c0); }

/* ── table container ── */
.tbl-wrap {
  flex: 1; overflow: auto;
}

/* ── data table ── */
table.rtbl {
  width: 100%; border-collapse: collapse;
  font-family: var(--mono); font-size: 10.5px;
}
table.rtbl thead th {
  padding: 8px 13px;
  font-size: 8px; text-transform: uppercase;
  letter-spacing: .2em; color: var(--t2);
  font-weight: 400;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  position: sticky; top: 0;
  white-space: nowrap;
}
table.rtbl thead th:last-child { text-align: right; }
table.rtbl tbody tr {
  border-bottom: 1px solid rgba(13,24,34,.9);
  transition: background .1s;
}
table.rtbl tbody tr:hover { background: rgba(0,255,136,.025); }
table.rtbl td {
  padding: 7px 13px;
  word-break: break-word;
  max-width: 240px;
  vertical-align: middle;
  color: var(--t1);
}
td.bright { color: var(--t0); }
td.mono   { font-size: 10px; }
td.right  { text-align: right; }
td.xs     { font-size: 10px; }

.empty-row td {
  text-align: center;
  padding: 40px 13px;
  color: var(--t3);
  font-size: 10px;
  letter-spacing: .08em;
}
.empty-row td::before {
  content: '[ NO DATA ]';
  display: block;
  font-family: var(--head);
  font-size: 18px;
  letter-spacing: .2em;
  color: var(--bg4);
  margin-bottom: 6px;
}

.row-high { background: rgba(255,34,68,.04) !important; }
.row-med  { background: rgba(255,140,0,.03) !important; }

/* ── badges ── */
.badge {
  display: inline-block;
  padding: 1px 7px;
  font-size: 8px; font-family: var(--mono);
  letter-spacing: .08em;
  border: 1px solid;
  text-transform: uppercase;
}
.b-red    { color: var(--r0);  border-color: rgba(255,34,68,.35);   background: rgba(255,34,68,.07); }
.b-amber  { color: var(--a0);  border-color: rgba(255,140,0,.35);   background: rgba(255,140,0,.07); }
.b-green  { color: var(--g0);  border-color: rgba(0,255,136,.28);   background: rgba(0,255,136,.06); }
.b-cyan   { color: var(--c0);  border-color: rgba(0,229,255,.28);   background: rgba(0,229,255,.06); }
.b-gray   { color: var(--t1);  border-color: var(--border);         background: var(--bg3); }
.b-purple { color: var(--p0);  border-color: rgba(191,95,255,.28);  background: rgba(191,95,255,.06); }

.osint-link {
  color: var(--c0); text-decoration: none;
  font-size: 9px;
  opacity: .8;
  transition: opacity .12s;
}
.osint-link:hover { opacity: 1; text-decoration: underline; }
</style>
</head>
<body>
<div id="app">

<!-- ══════════════════════ SIDEBAR ══════════════════════ -->
<aside id="sidebar">

  <div class="sb-head">
    <div class="logo-row">
      <div class="logo-icon">
        <i class="fa-solid fa-satellite-dish"></i>
      </div>
      <div>
        <div class="logo-text">Recon<span>Radar</span></div>
        <div class="logo-sub">Offensive Recon Engine <span class="version-tag">APOLLO&nbsp;v5</span></div>
      </div>
    </div>
    <div class="status-row">
      <span id="connection-status">
        <span class="dot dot-off"></span>
        <span style="color:var(--r0)">OFFLINE</span>
      </span>
      <span id="scan-timer" style="display:none">00:00</span>
    </div>
  </div>

  <div class="sb-body">
    <form id="scan-form">

      <!-- TARGET -->
      <div class="sb-sec">
        <div class="sb-label"><i class="fa-solid fa-crosshairs"></i> Target</div>
        <div class="inp-wrap">
          <i class="inp-ico fa-solid fa-angle-right"></i>
          <input type="text" id="target" class="inp"
            placeholder="domain.tld  ·  sub.domain  ·  IP" required
            autocomplete="off" spellcheck="false">
        </div>
      </div>

      <!-- NMAP PROFILE -->
      <div class="sb-sec">
        <div class="sb-label"><i class="fa-solid fa-sliders"></i> Nmap Profile</div>
        <div class="inp-wrap">
          <i class="inp-ico fa-solid fa-chevron-down"></i>
          <select id="scan-preset" class="inp">
            <option value="-sV -T4 -F --version-intensity 5 -O --osscan-guess">Aggressive OS + Service</option>
            <option value="-sT -sV -T4 -A -Pn -n -v">Full Aggressive — TCP+OS+Scripts</option>
            <option value="-sT -sV -T5 -p- -Pn -n --min-rate 1000">Full Port Blitz (65535)</option>
            <option value="-sT -sV -T4 -p 1-10000 -Pn -A -f">Stealth TCP + Fragment</option>
            <option value="-sT -sV -T4 -p- -Pn --script vuln,safe,discovery,version">Vuln Script Deep Scan</option>
            <option value="-sV -T4 -p 80,443,8080,8443 -Pn --script http-enum,http-headers,http-title">Web Forensics</option>
            <option value="-sT -sV -T4 -p- -Pn -n -f --mtu 24 --data-length 200">TCP + Fragment Evasion</option>
            <option value="-sT -sV -T4 -p 22,3389,1433,3306,445,139,389,5900,6379,27017 -A">Critical Services</option>
            <option value="-sn -T4 -n -v">Ping Sweep / Discovery</option>
            <option value="-sU --top-ports 100 -T4 -n">UDP Top 100</option>
            <option value="--script safe,discovery -sV -T4 -p-">Safe Script Discovery</option>
            <option value="CUSTOM">Custom flags…</option>
          </select>
        </div>
        <div id="custom-nmap-row" class="inp-wrap" style="display:none">
          <textarea id="custom-nmap" class="inp" rows="3"
            placeholder="-sT -sV -T4 -p 80,443 -Pn&#10;Note: use -sT (no admin) or run as Administrator for -sS"></textarea>
        </div>
      </div>

      <!-- MODULES -->
      <div class="sb-sec">
        <div class="sb-label"><i class="fa-solid fa-cubes"></i> Modules</div>
        <div class="mods-grid">
          <label class="mod-lbl"><input type="checkbox" id="mod-dns"       checked> DNS</label>
          <label class="mod-lbl"><input type="checkbox" id="mod-whois"     checked> WHOIS</label>
          <label class="mod-lbl"><input type="checkbox" id="mod-subdomain" checked> Subdomain</label>
          <label class="mod-lbl"><input type="checkbox" id="mod-takeover"  checked> Takeover</label>
          <label class="mod-lbl"><input type="checkbox" id="mod-web"       checked> HTTP Probe</label>
          <label class="mod-lbl"><input type="checkbox" id="mod-dnszone"   checked> DNS Zone</label>
          <label class="mod-lbl full"><input type="checkbox" id="mod-osint" checked> OSINT Links</label>
        </div>
      </div>

      <!-- ACTIONS -->
      <div class="sb-sec">
        <div class="btn-row">
          <button type="submit" id="scan-btn">
            <i class="fa-solid fa-bolt"></i> LAUNCH RECON
          </button>
          <button type="button" id="stop-btn" disabled>
            <i class="fa-solid fa-square-full"></i> STOP
          </button>
        </div>
      </div>

    </form>
  </div>

  <div class="sb-foot">
    <a href="https://github.com/Nexvir" target="_blank">
      <i class="fa-brands fa-github"></i> github.com/Nexvir
    </a>
    &nbsp;&middot;&nbsp;
    <a href="https://github.com/Nexvir/ReconRadar" target="_blank">ReconRadar</a>
    <div class="disc">For authorized security testing only.</div>
  </div>

</aside>

<!-- ══════════════════════ TERMINAL ══════════════════════ -->
<div id="term-col">

  <div class="pane-bar">
    <span class="pane-title green">
      <span class="live-dot"></span> LIVE FEED
    </span>
    <div class="pane-acts">
      <button class="pane-btn" onclick="clearTerminal()">CLR</button>
      <button class="pane-btn" onclick="copyTerminal()">CPY</button>
      <div class="win-dots">
        <span style="background:#ff5f57"></span>
        <span style="background:#febc2e"></span>
        <span style="background:#28c840"></span>
      </div>
    </div>
  </div>

  <div id="prog-wrap"><div id="prog-bar"></div></div>

  <div id="terminal">
<span class="ll ll-sys" style="color:var(--t3)">╔═══════════════════════════════════════════╗</span>
<span class="ll ll-sys" style="color:var(--t3)">║  ReconRadar APOLLO  ·  github.com/Nexvir  ║</span>
<span class="ll ll-sys" style="color:var(--t3)">╚═══════════════════════════════════════════╝</span>
<span class="ll ll-sys">[sys] Modules: DNS · WHOIS · CRT.SH · SUBDOMAIN · TAKEOVER · HTTPX · ZONE · OSINT</span>
<span class="ll ll-sys">[sys] Configure target in sidebar → LAUNCH RECON</span>
<span class="blinking-cursor">█</span>
  </div>

  <div class="term-stats">
    <div class="stat-cell">
      <span class="stat-num" id="st-total">0</span>
      <span class="stat-label">Findings</span>
    </div>
    <div class="stat-cell">
      <span class="stat-num red" id="st-high">0</span>
      <span class="stat-label">High Risk</span>
    </div>
    <div class="stat-cell">
      <span class="stat-num cyan" id="st-ports">0</span>
      <span class="stat-label">Open Ports</span>
    </div>
  </div>

</div>

<!-- ══════════════════════ RESULTS ══════════════════════ -->
<div id="results-col">

  <div class="tab-bar">
    <button class="tab-btn active" id="btn-dns"   onclick="switchTab('dns')">
      <i class="fa-solid fa-globe"></i> DNS
      <span class="tcnt" id="cnt-dns">0</span>
    </button>
    <button class="tab-btn" id="btn-sub"   onclick="switchTab('sub')">
      <i class="fa-solid fa-sitemap"></i> SUB
      <span class="tcnt" id="cnt-sub">0</span>
    </button>
    <button class="tab-btn" id="btn-port"  onclick="switchTab('port')">
      <i class="fa-solid fa-network-wired"></i> PORTS
      <span class="tcnt" id="cnt-port">0</span>
    </button>
    <button class="tab-btn" id="btn-web"   onclick="switchTab('web')">
      <i class="fa-solid fa-server"></i> WEB
      <span class="tcnt" id="cnt-web">0</span>
    </button>
    <button class="tab-btn" id="btn-vuln"  onclick="switchTab('vuln')">
      <i class="fa-solid fa-bug"></i> VULNS
      <span class="tcnt" id="cnt-vuln">0</span>
    </button>
    <button class="tab-btn" id="btn-osint" onclick="switchTab('osint')">
      <i class="fa-solid fa-eye"></i> OSINT
      <span class="tcnt" id="cnt-osint">0</span>
    </button>
    <div class="tab-actions">
      <span id="asset-count">0&nbsp;ITEMS</span>
      <button class="btn-export" onclick="exportHtml()">
        <i class="fa-solid fa-download"></i> EXPORT
      </button>
    </div>
  </div>

  <div class="tbl-wrap">

    <!-- DNS -->
    <table class="rtbl" id="table-dns">
      <thead><tr>
        <th>ASSET</th><th>TYPE</th><th>DETAILS</th><th>INFO</th>
      </tr></thead>
      <tbody id="results-body-dns">
        <tr class="empty-row"><td colspan="4">Awaiting scan</td></tr>
      </tbody>
    </table>

    <!-- Subdomains -->
    <table class="rtbl" id="table-sub" style="display:none">
      <thead><tr>
        <th>SUBDOMAIN</th><th>IP / CNAME</th><th>SOURCE</th><th>STATUS</th>
      </tr></thead>
      <tbody id="results-body-sub">
        <tr class="empty-row"><td colspan="4">Awaiting scan</td></tr>
      </tbody>
    </table>

    <!-- Ports -->
    <table class="rtbl" id="table-port" style="display:none">
      <thead><tr>
        <th>HOST:PORT</th><th>STATE</th><th>SERVICE / VERSION / OS</th><th>RISK</th>
      </tr></thead>
      <tbody id="results-body-port">
        <tr class="empty-row"><td colspan="4">Awaiting scan</td></tr>
      </tbody>
    </table>

    <!-- Web -->
    <table class="rtbl" id="table-web" style="display:none">
      <thead><tr>
        <th>URL</th><th>STATUS</th><th>TECH STACK / HEADERS</th><th>WAF / REDIRECT</th>
      </tr></thead>
      <tbody id="results-body-web">
        <tr class="empty-row"><td colspan="4">Awaiting scan</td></tr>
      </tbody>
    </table>

    <!-- Vulns -->
    <table class="rtbl" id="table-vuln" style="display:none">
      <thead><tr>
        <th>TARGET</th><th>THREAT</th><th>DETAILS / PoC</th><th>SEVERITY</th>
      </tr></thead>
      <tbody id="results-body-vuln">
        <tr class="empty-row"><td colspan="4">Awaiting scan</td></tr>
      </tbody>
    </table>

    <!-- OSINT -->
    <table class="rtbl" id="table-osint" style="display:none">
      <thead><tr>
        <th>SOURCE</th><th>TYPE</th><th>LINK / INFO</th><th>CONFIDENCE</th>
      </tr></thead>
      <tbody id="results-body-osint">
        <tr class="empty-row"><td colspan="4">Awaiting scan</td></tr>
      </tbody>
    </table>

  </div><!-- /tbl-wrap -->
</div><!-- /results-col -->

</div><!-- /app -->

<script>
/* ───────────────────────────────────────
   STATE
─────────────────────────────────────── */
const terminal    = document.getElementById('terminal');
const form        = document.getElementById('scan-form');
const targetInput = document.getElementById('target');
const presetSel   = document.getElementById('scan-preset');
const customInput = document.getElementById('custom-nmap');
const customRow   = document.getElementById('custom-nmap-row');
const scanBtn     = document.getElementById('scan-btn');
const stopBtn     = document.getElementById('stop-btn');
const assetCount  = document.getElementById('asset-count');
const statusInd   = document.getElementById('connection-status');
const scanTimer   = document.getElementById('scan-timer');
const progBar     = document.getElementById('prog-bar');

let ws, scanActive=false, timerInt=null, seconds=0;
let allResults=[], totalCount=0, highCount=0, portCount=0;
let tabCounts = {dns:0,sub:0,port:0,web:0,vuln:0,osint:0};
let currentScanId=null;

/* ───────────────────────────────────────
   WEBSOCKET
─────────────────────────────────────── */
function connectWS() {
  const proto = location.protocol==='https:'?'wss:':'ws:';
  ws = new WebSocket(`${proto}//${location.host}/ws`);
  ws.onopen  = () => setOnline(true);
  ws.onclose = () => { setOnline(false); setTimeout(connectWS,3000); };
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if      (m.type==='log')      appendLog(m.data);
    else if (m.type==='result')   appendResult(m.data);
    else if (m.type==='status')   handleStatus(m.data);
    else if (m.type==='progress') setProgress(m.data);
  };
}
function setOnline(on) {
  statusInd.innerHTML = on
    ? `<span class="dot dot-on"></span><span style="color:var(--g0)">ONLINE</span>`
    : `<span class="dot dot-off"></span><span style="color:var(--r0)">OFFLINE</span>`;
}

/* ───────────────────────────────────────
   TIMER / PROGRESS
─────────────────────────────────────── */
function startTimer() {
  seconds=0; scanTimer.style.display='';
  if (timerInt) clearInterval(timerInt);
  timerInt = setInterval(()=>{
    seconds++;
    scanTimer.textContent = `${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`;
  }, 1000);
}
function stopTimer() {
  if(timerInt){clearInterval(timerInt);timerInt=null;}
  scanTimer.style.display='none';
}
function setProgress(pct) {
  progBar.style.width = pct+'%';
  if(pct===0) progBar.style.boxShadow='none';
  else progBar.style.boxShadow='0 0 8px var(--g0)';
}

/* ───────────────────────────────────────
   TERMINAL
─────────────────────────────────────── */
function appendLog(text) {
  const cursor = terminal.querySelector('.blinking-cursor');
  if (cursor) cursor.remove();
  const sp = document.createElement('span');
  const t = text.toLowerCase();
  let cls = 'll ';
  if      (t.includes('[error]')||t.includes('[fatal]')||t.includes('[!!!]')) cls+='ll-err';
  else if (t.includes('[warn]')||t.includes('nmap error'))                    cls+='ll-warn';
  else if (t.includes('[sys]')||t.includes('[system]'))                       cls+='ll-sys';
  else if (t.includes('[phase'))                                               cls+='ll-phase';
  else if (t.includes('[crt.')||t.includes('[ct]'))                           cls+='ll-crt';
  else if (t.includes('[whois]'))                                              cls+='ll-who';
  else if (t.includes('[nmap]'))                                               cls+='ll-nmap';
  else if (t.includes('[http]')||t.includes('[port]')||t.includes('[httpx]')) cls+='ll-http';
  else if (t.includes('[subdomain]')||t.includes('[sub]'))                    cls+='ll-sub';
  else if (t.includes('[+]')||t.includes('complete')||t.includes('success'))  cls+='ll-ok';
  sp.className=cls; sp.textContent=text;
  terminal.appendChild(sp);
  const c=document.createElement('span'); c.className='blinking-cursor'; c.textContent='█';
  terminal.appendChild(c);
  terminal.scrollTop=terminal.scrollHeight;
}

function clearTerminal() {
  terminal.innerHTML='<span class="ll ll-sys">[sys] Terminal cleared.</span><span class="blinking-cursor">█</span>';
}
function copyTerminal() {
  navigator.clipboard.writeText(terminal.innerText.replace(/█/g,'').trim());
  appendLog('[sys] Copied to clipboard.');
}

/* ───────────────────────────────────────
   TABS
─────────────────────────────────────── */
function switchTab(id) {
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(`btn-${id}`).classList.add('active');
  document.querySelectorAll('[id^="table-"]').forEach(t=>t.style.display='none');
  document.getElementById(`table-${id}`).style.display='';
}

/* ───────────────────────────────────────
   RESULTS
─────────────────────────────────────── */
function appendResult(data) {
  const cat  = data.category||'dns';
  const tbody= document.getElementById(`results-body-${cat}`);
  if (!tbody) return;
  if (tbody.querySelector('.empty-row')) tbody.innerHTML='';

  totalCount++;
  tabCounts[cat]=(tabCounts[cat]||0)+1;
  document.getElementById(`cnt-${cat}`).textContent = tabCounts[cat];
  const cntEl = document.getElementById(`cnt-${cat}`);
  cntEl.className = tabCounts[cat]>0 ? (cat==='vuln'?'tcnt red':'tcnt has') : 'tcnt';

  if (data.severity==='High') { highCount++; document.getElementById('st-high').textContent=highCount; }
  if (cat==='port'&&data.col2==='OPEN') { portCount++; document.getElementById('st-ports').textContent=portCount; }
  document.getElementById('st-total').textContent=totalCount;
  assetCount.textContent = `${totalCount}\u00a0ITEMS`;
  allResults.push(data);

  const tr=document.createElement('tr');

  function sev(s){
    const u=String(s||'').toUpperCase();
    if(u==='HIGH')   return `<span class="badge b-red">HIGH</span>`;
    if(u==='MEDIUM') return `<span class="badge b-amber">MED</span>`;
    if(u==='LOW')    return `<span class="badge b-gray">LOW</span>`;
    if(u==='INFO')   return `<span class="badge b-cyan">INFO</span>`;
    if(u.startsWith('2')) return `<span class="badge b-green">${esc(s)}</span>`;
    if(u.startsWith('3')) return `<span class="badge b-cyan">${esc(s)}</span>`;
    if(u.startsWith('4')) return `<span class="badge b-amber">${esc(s)}</span>`;
    if(u.startsWith('5')) return `<span class="badge b-red">${esc(s)}</span>`;
    return `<span class="badge b-gray">${esc(s)}</span>`;
  }

  if(cat==='port'){
    if(data.severity==='High')   tr.classList.add('row-high');
    if(data.severity==='Medium') tr.classList.add('row-med');
    tr.innerHTML=`
      <td class="bright mono">${esc(data.col1)}</td>
      <td>${sev(data.col2)}</td>
      <td class="mono xs">${esc(data.col3)}</td>
      <td class="right">${sev(data.severity)}</td>`;
  } else if(cat==='vuln'){
    tr.classList.add('row-high');
    tr.innerHTML=`
      <td class="bright mono xs">${esc(data.col1)}</td>
      <td>${sev(data.col2||data.severity)}</td>
      <td class="mono xs">${esc(data.col3)}</td>
      <td class="right">${sev(data.severity)}</td>`;
  } else if(cat==='web'){
    tr.innerHTML=`
      <td class="bright mono xs">${esc(data.col1)}</td>
      <td>${sev(data.severity)}</td>
      <td class="mono xs">${esc(data.col3)}</td>
      <td class="right xs" style="color:var(--t2)">${esc(data.col2||'')}</td>`;
  } else if(cat==='sub'){
    tr.innerHTML=`
      <td class="bright mono xs">${esc(data.col1)}</td>
      <td class="mono xs" style="color:var(--t2)">${esc(data.col3||'')}</td>
      <td><span class="badge b-gray">${esc(data.col2)}</span></td>
      <td class="right">${sev(data.severity)}</td>`;
  } else if(cat==='osint'){
    tr.innerHTML=`
      <td class="bright">${esc(data.col1)}</td>
      <td><span class="badge b-purple">${esc(data.col2)}</span></td>
      <td class="xs"><a href="${esc(data.col3)}" target="_blank" class="osint-link">${esc(data.col3)}</a></td>
      <td class="right">${sev(data.severity)}</td>`;
  } else {
    tr.innerHTML=`
      <td class="bright">${esc(data.col1)}</td>
      <td><span class="badge b-gray">${esc(data.col2)}</span></td>
      <td class="mono xs">${esc(data.col3)}</td>
      <td class="right">${sev(data.severity)}</td>`;
  }
  tbody.insertBefore(tr, tbody.firstChild);
}

/* ───────────────────────────────────────
   STATUS HANDLER
─────────────────────────────────────── */
function handleStatus(s) {
  if(s==='done'||s==='error'||s==='stopped'){
    scanBtn.disabled=false; stopBtn.disabled=true;
    targetInput.disabled=false; presetSel.disabled=false; customInput.disabled=false;
    scanBtn.innerHTML=`<i class="fa-solid fa-bolt"></i> LAUNCH RECON`;
    scanActive=false; stopTimer();
    setProgress(s==='done'?100:0);
    appendLog(`[sys] Operation ${s}.`);
    setTimeout(()=>{ if(s==='done') setProgress(0); }, 2000);
  }
}

/* ───────────────────────────────────────
   HTML EXPORT  (styled report)
─────────────────────────────────────── */
function exportHtml() {
  if(!allResults.length){ appendLog('[sys] No data to export.'); return; }
  const target = targetInput.value||'target';
  const date   = new Date().toISOString().slice(0,10);
  const cats = {
    dns:  { label:'DNS Records',      cols:['ASSET','TYPE','DETAILS','INFO'] },
    sub:  { label:'Subdomains',       cols:['SUBDOMAIN','SOURCE','IP/CNAME','STATUS'] },
    port: { label:'Ports',            cols:['HOST:PORT','STATE','SERVICE','RISK'] },
    web:  { label:'Web Services',     cols:['URL','STATUS','TECH / HEADERS','WAF'] },
    vuln: { label:'Vulnerabilities',  cols:['TARGET','THREAT','DETAILS','SEVERITY'] },
    osint:{ label:'OSINT Links',      cols:['SOURCE','TYPE','LINK','CONFIDENCE'] },
  };
  const grouped={};
  for(const k of Object.keys(cats)) grouped[k]=[];
  for(const r of allResults){ if(grouped[r.category]) grouped[r.category].push(r); }

  function sc(s){ const u=(s||'').toUpperCase(); if(u==='HIGH')return'#ff2244';if(u==='MEDIUM')return'#ff8c00';if(u==='LOW')return'#ffd60a';if(u.startsWith('2'))return'#00ff88';if(u.startsWith('3'))return'#00e5ff';if(u.startsWith('4'))return'#ff8c00';if(u.startsWith('5'))return'#ff2244';return'#7098b8'; }
  function e(s){ return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

  const summary = Object.entries(grouped).map(([k,v])=>`<span style="color:#00e5ff">${cats[k].label}</span>:<b style="color:#fff">${v.length}</b>`).join(' &nbsp;|&nbsp; ');
  let sections='';
  for(const [cat,info] of Object.entries(cats)){
    const rows=grouped[cat]; if(!rows.length) continue;
    let tbody='';
    for(const r of rows){
      const isLink=cat==='osint'&&(r.col3||'').startsWith('http');
      const c3 = isLink?`<a href="${e(r.col3)}" style="color:#00e5ff">${e(r.col3)}</a>`:e(r.col3);
      tbody+=`<tr><td>${e(r.col1)}</td><td>${e(r.col2)}</td><td>${c3}</td><td style="color:${sc(r.severity)};font-weight:700">${e(r.severity||'INFO')}</td></tr>`;
    }
    sections+=`<h2>${info.label} <small>(${rows.length})</small></h2>
    <table><thead><tr>${info.cols.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>${tbody}</tbody></table>`;
  }
  const html=`<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>ReconRadar — ${e(target)} — ${date}</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#020509;color:#7098b8;font-family:'JetBrains Mono','Courier New',monospace;font-size:11px;padding:28px}
h2{color:#00ff88;font-size:12px;letter-spacing:.18em;text-transform:uppercase;margin:26px 0 7px;border-bottom:1px solid #0d1822;padding-bottom:5px}
h2 small{color:#2e4860;font-size:10px}
table{width:100%;border-collapse:collapse;margin-bottom:10px}
th{padding:6px 10px;text-align:left;color:#2e4860;font-size:8px;letter-spacing:.18em;border-bottom:1px solid #0d1822}
td{padding:6px 10px;border-bottom:1px solid #0a1420;word-break:break-word;vertical-align:top;max-width:320px}
tr:hover td{background:rgba(0,255,136,.02)}
a{color:#00e5ff;text-decoration:none}a:hover{text-decoration:underline}
.hdr{border:1px solid #0d1822;padding:18px 22px;margin-bottom:22px;background:#050c12}
.ftr{margin-top:28px;color:#182838;font-size:9px;text-align:center;letter-spacing:.1em}
</style></head><body>
<div class="hdr">
  <div style="color:#00ff88;font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:.18em;margin-bottom:4px">ReconRadar APOLLO — Intelligence Report</div>
  <div style="color:#cce8ff;margin-bottom:3px">Target: <b style="color:#fff">${e(target)}</b></div>
  <div style="color:#2e4860;font-size:10px;margin-bottom:8px">Generated: ${new Date().toUTCString()}</div>
  <div style="font-size:10px">${summary}</div>
</div>
${sections}
<div class="ftr">ReconRadar APOLLO v5 — github.com/Nexvir — For authorized security testing only</div>
</body></html>`;
  const blob=new Blob([html],{type:'text/html'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download=`reconradar_${target}_${date}.html`;
  a.click(); URL.revokeObjectURL(a.href);
  appendLog(`[sys] HTML report exported — ${allResults.length} findings.`);
}

/* ───────────────────────────────────────
   FORM SUBMIT
─────────────────────────────────────── */
function esc(s){ if(!s)return''; return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

form.addEventListener('submit', e => {
  e.preventDefault();
  if(scanActive||!ws||ws.readyState!==WebSocket.OPEN) return;
  const target=targetInput.value.trim();
  let nmapArgs=presetSel.value;
  if(nmapArgs==='CUSTOM') nmapArgs=customInput.value.trim()||'-sV -T4 -F -Pn';
  if(!target) return;

  // reset
  ['dns','sub','port','web','vuln','osint'].forEach(id=>{
    const tb=document.getElementById(`results-body-${id}`);
    if(tb) tb.innerHTML=`<tr class="empty-row"><td colspan="4" style="color:var(--t3)"><i class="fa-solid fa-circle-notch fa-spin" style="color:var(--g2)"></i>&nbsp; Scanning…</td></tr>`;
    tabCounts[id]=0;
    const cnt=document.getElementById(`cnt-${id}`);
    if(cnt){ cnt.textContent='0'; cnt.className='tcnt'; }
  });
  totalCount=0; highCount=0; portCount=0;
  document.getElementById('st-total').textContent='0';
  document.getElementById('st-high').textContent='0';
  document.getElementById('st-ports').textContent='0';
  allResults=[]; terminal.innerHTML=''; currentScanId=Date.now().toString();
  assetCount.textContent='0\u00a0ITEMS';
  setProgress(3);

  const mods={
    dns:       document.getElementById('mod-dns')?.checked??true,
    whois:     document.getElementById('mod-whois')?.checked??true,
    subdomain: document.getElementById('mod-subdomain')?.checked??true,
    takeover:  document.getElementById('mod-takeover')?.checked??true,
    web:       document.getElementById('mod-web')?.checked??true,
    dnszone:   document.getElementById('mod-dnszone')?.checked??true,
    osint:     document.getElementById('mod-osint')?.checked??true,
  };

  appendLog(`[+] TARGET: ${target}`);
  appendLog(`[+] NMAP: ${nmapArgs}`);
  appendLog(`[+] MODULES: ${Object.entries(mods).filter(([,v])=>v).map(([k])=>k).join(', ')}`);

  scanBtn.disabled=true; stopBtn.disabled=false;
  targetInput.disabled=true; presetSel.disabled=true; customInput.disabled=true;
  scanBtn.innerHTML=`<i class="fa-solid fa-spinner fa-spin"></i> DEPLOYING…`;
  scanActive=true; startTimer();

  ws.send(JSON.stringify({action:'start_scan',target,nmap_args:nmapArgs,modules:mods,scan_id:currentScanId}));
});

stopBtn.addEventListener('click', () => {
  if(scanActive&&ws&&ws.readyState===WebSocket.OPEN){
    ws.send(JSON.stringify({action:'stop_scan',scan_id:currentScanId}));
    stopBtn.disabled=true;
    appendLog('[sys] Stop signal sent…');
  }
});

presetSel.addEventListener('change', () => {
  customRow.style.display = presetSel.value==='CUSTOM'?'':'none';
});

/* ── boot ── */
connectWS();
window.switchTab=switchTab;
</script>
</body>
</html>
"""
