"use strict";
// Ikon pwofesyonel pa nou menm (stroke SVG 24x24, pa emoji)
const ICON = {
  film:'<rect x="2" y="2" width="20" height="20" rx="2.2"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/>',
  check:'<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
  refresh:'<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
  download:'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
  save:'<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>',
  play:'<polygon points="6 3 20 12 6 21 6 3"/>',
  pause:'<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>',
  sliders:'<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
  sparkles:'<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 14l.7 1.9L22 17l-2.3.8L19 20l-.7-2.2L16 17l2.3-1.1z"/>',
  undo:'<polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>',
  redo:'<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
  scissors:'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/>',
  magnet:'<path d="M5 3v6a7 7 0 0 0 14 0V3"/><line x1="4" y1="3" x2="9" y2="3"/><line x1="15" y1="3" x2="20" y2="3"/>',
  zoomin:'<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16" y2="16"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/>',
  zoomout:'<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16" y2="16"/><line x1="8" y1="11" x2="14" y2="11"/>',
  fit:'<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>',
  pointer:'<path d="M4 4l7.07 17 2.51-7.39L21 11.07z"/>',
  caret:'<polyline points="7 10 12 15 17 10"/>',
  arrowleft:'<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
  arrowright:'<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
  diamond:'<path d="M12 2l10 10-10 10L2 12z"/>',
  folder:'<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
  open:'<path d="M2 11V5c0-1.1.9-2 2-2h5l2 3h9c1.1 0 2 .9 2 2v3"/><path d="m3.5 21 2.3-9.2A2 2 0 0 1 7.7 10h14.6a1.5 1.5 0 0 1 1.4 2l-2.4 8.2a2 2 0 0 1-1.9 1.4H4.9a1.5 1.5 0 0 1-1.4-.6z"/>',
  code:'<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
  image:'<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',
  plus:'<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
  palette:'<circle cx="13.5" cy="6.5" r="1.3"/><circle cx="17.5" cy="10.5" r="1.3"/><circle cx="8.5" cy="7.5" r="1.3"/><circle cx="6.5" cy="12.5" r="1.3"/><path d="M12 2a10 10 0 1 0 0 20c1.1 0 2-.9 2-2a2 2 0 0 1 2-2h2a4 4 0 0 0 4-4 10 10 0 0 0-10-10z"/>',
  music:'<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
  mic:'<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/>',
  text:'<polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/>',
  layers:'<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
  record:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5" fill="currentColor"/>',
  replay:'<path d="M3 12a9 9 0 1 0 2.6-6.3"/><polyline points="3 3 3 9 9 9"/>',
  copy:'<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
  trash:'<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
  settings:'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
  volume:'<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>',
  caretup:'<polyline points="18 15 12 9 6 15"/>',
  lock:'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
  unlock:'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>',
  eye:'<path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"/><circle cx="12" cy="12" r="3"/>',
  eyeoff:'<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>',
  mute:'<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/>',
  camera:'<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
  delleft:'<polyline points="6 6 6 18"/><line x1="20" y1="12" x2="6" y2="12"/><polyline points="13 7 8 12 13 17"/>',
  delright:'<polyline points="18 6 18 18"/><line x1="4" y1="12" x2="18" y2="12"/><polyline points="11 7 16 12 11 17"/>',
  freeze:'<rect x="4" y="4" width="16" height="16" rx="2"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/>',
  reverse:'<polygon points="11 19 2 12 11 5 11 19"/><polygon points="22 19 13 12 22 5 22 19"/>',
  mirror:'<path d="M12 3v18"/><polyline points="8 7 3 12 8 17"/><polyline points="16 7 21 12 16 17"/>',
  rotate:'<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
  crop:'<path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/>',
  link:'<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
  scrub:'<path d="M2 10v4"/><path d="M6 7v10"/><path d="M10 4v16"/><path d="M14 7v10"/><path d="M18 10v4"/><path d="M22 12v0"/>',
  blend:'<circle cx="9" cy="12" r="6"/><circle cx="15" cy="12" r="6"/>',
  lut:'<rect x="2" y="2" width="20" height="20" rx="2.5"/><line x1="2" y1="8" x2="22" y2="8"/><line x1="2" y1="16" x2="22" y2="16"/><line x1="8" y1="2" x2="6" y2="8"/><line x1="16" y1="2" x2="14" y2="8"/>',
  sound:'<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/>',
  grip:'<circle cx="8" cy="6" r="1.5" fill="currentColor"/><circle cx="16" cy="6" r="1.5" fill="currentColor"/><circle cx="8" cy="12" r="1.5" fill="currentColor"/><circle cx="16" cy="12" r="1.5" fill="currentColor"/><circle cx="8" cy="18" r="1.5" fill="currentColor"/><circle cx="16" cy="18" r="1.5" fill="currentColor"/>',
  target:'<circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/><circle cx="12" cy="12" r="6" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="12" cy="12" r="2" fill="currentColor"/>'
};
function paintIcons(root) {
  (root || document).querySelectorAll("[data-ico]").forEach(el => {
    const p = ICON[el.dataset.ico]; if (p) el.innerHTML = '<svg class="ic" viewBox="0 0 24 24">' + p + '</svg>';
  });
}
window.paintIcons = paintIcons;
function svg(name, cls) { return '<svg class="' + (cls || "ic") + '" viewBox="0 0 24 24">' + (ICON[name] || "") + '</svg>'; }

const Q = new URLSearchParams(location.search), TOK = Q.get("token") || "";
const $ = s => document.querySelector(s);
const esc = s => (s == null ? "" : String(s)).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
let SPEC = null, VER = "", SEL = -1, KD = null, DIRTY = false, ISSUES = {};
let PPS = 90, CUR = 0, SNAP = true, playing = false, TOOL = "select", LT = "media", RT = "props", TRACKSEL = "scenes", CLIPSEL = null, RECORDING = false, OVSEL = null;
let EDITMODE = "overwrite";                        // montaj clip-primè: "overwrite" | "insert"
let MAIN_MAGNET = true, LINKAGE = true, SCRUB_AUDIO = true;
let ACAT = "", AOFF = 0;    // asset: kategori + offset

async function api(method, path, body) {
  // SEKIRITE: jeton an ale nan header X-Kadans-Token (pa nan URL) → li pa parèt nan F12 / istorik / kapti ekran.
  const opt = { method, headers: { "X-Kadans-Token": TOK } };
  if (body) { opt.headers["Content-Type"] = "application/json"; opt.body = JSON.stringify(body); }
  const r = await fetch(path, opt); let j = {}; try { j = await r.json(); } catch (e) {}
  return { status: r.status, body: j };
}
const msg = t => { $("#msg").textContent = window.KadansI18n ? window.KadansI18n.tp(t) : t; };
const scName = sc => (sc.title || sc.handle || sc.id || sc.type || "").toString().replace(/\*/g, "").slice(0, 24);
const total = () => {
  let T = (KD && KD.total) || (SPEC.scenes || []).reduce((a, s) => a + (s.duration || 2), 0);
  (SPEC.tracks || []).forEach(tk => (tk.clips || []).forEach(c => { T = Math.max(T, (c.start || 0) + (c.dur || 2)); }));
  if (!T && SPEC && SPEC.total_duration) T = Number(SPEC.total_duration);
  return T || (SPEC && SPEC.total_duration ? Number(SPEC.total_duration) : 30);
};
// v3.12 DIRE ESTAB: dire yon sèn = sa sèvè a kalkile (vrè vwa a), chèche pa ID ESTAB li. Anvan: spec AI yo pa t gen
// id → editè a pa t janm jwenn sèn nan nan KD → CHAK sèn te parèt 2 s pandan aperçu a te jwe vrè dire yo.
const kdEntry = (sc, i) => {
  if (!KD || !KD.scenes) return null;
  return KD.scenes.find(x => x.id === sc.id) || (sc.id == null && i != null ? KD.scenes.find(x => x.spec_index === i) : null) || null;
};
const kdDur = (sc, i) => { const e = kdEntry(sc, i); return e ? e.dur : 2; };
// Yon «duration» se yon MINIMÒM: si vwa a pi long, sèvè a alonje sèn nan (vwa a pa janm koupe) — editè a montre menm bagay la.
const sDur = i => { const sc = SPEC.scenes[i]; if (sc.duration == null) return kdDur(sc, i); const e = kdEntry(sc, i); return Math.max(sc.duration, (e && e.need) || 0); };
function ensureIds() {               // menm chema ak kadans/spec.py ensure_ids: s<pozisyon> si l lib, jamè 2 fwa menm id
  if (!SPEC || !Array.isArray(SPEC.scenes)) return false;
  const used = new Set(), todo = []; let ch = false;
  SPEC.scenes.forEach((sc, i) => { const id = typeof sc.id === "string" ? sc.id.trim() : "";
    if (id && !used.has(id)) { used.add(id); if (sc.id !== id) { sc.id = id; ch = true; } } else todo.push([i, sc]); });
  let n = 0;
  todo.forEach(([i, sc]) => { let id = "s" + (i + 1); while (used.has(id)) { n++; id = "s" + (SPEC.scenes.length + n); } sc.id = id; used.add(id); ch = true; });
  return ch;
}
const sStart = i => { let s = 0; for (let k = 0; k < i; k++) s += sDur(k); return s; };
const srcOf = sc => sc.src || sc.image || sc.video || sc.url || (sc.background && sc.background.src) || "";
const sceneAt = t => { let i = 0; for (; i < SPEC.scenes.length; i++) { if (t < sStart(i) + sDur(i)) return i; } return Math.max(0, SPEC.scenes.length - 1); };

let AUDIO_MAP = { voices: {}, music: "", mix: "", rev: 0 };
let _pendingVoiceFetch = false;
let PVZOOM = 1, PVPANX = 0, PVPANY = 0;

function withTok(u) {
  if (!u) return "";
  if (/^(https?:|data:|blob:)/i.test(u)) return u;
  const rev = (AUDIO_MAP && AUDIO_MAP.rev) || Date.now();
  return u + (u.includes("?") ? "&" : "?") + "token=" + encodeURIComponent(TOK) + "&_r=" + rev;
}
function voiceUrlForScene(sc, i) {
  if (!sc) return "";
  if (sc.voice_file) return sc.voice_file;
  const vm = (AUDIO_MAP && AUDIO_MAP.voices) || {};
  return (sc.id && vm[sc.id]) || vm[String(i)] || "";
}
function applyPvZoom() {
  const pv = $("#pv");
  if (pv) {
    pv.style.transform = (Math.abs(PVZOOM - 1) < 0.01 && PVPANX === 0 && PVPANY === 0)
      ? ""
      : ("translate(" + PVPANX + "px," + PVPANY + "px) scale(" + PVZOOM.toFixed(3) + ")");
  }
  const lbl = $("#pvZoomLbl");
  if (lbl) lbl.textContent = Math.abs(PVZOOM - 1) < 0.01 ? "Fit" : (Math.round(PVZOOM * 100) + "%");
  setTimeout(renderOvHandle, 20);
}
function setPvZoom(z) {
  PVZOOM = Math.max(0.25, Math.min(4.0, z));
  if (Math.abs(PVZOOM - 1) < 0.03) { PVZOOM = 1; PVPANX = 0; PVPANY = 0; }
  applyPvZoom();
}
function fitScreenView() {
  PVZOOM = 1; PVPANX = 0; PVPANY = 0;
  applyPvZoom();
  const pv = $("#pv"), wrap = $("#pvwrap");
  if (pv && wrap) {
    try {
      const doc = pv.contentDocument || (pv.contentWindow && pv.contentWindow.document);
      if (doc) {
        let stCss = doc.getElementById("kd-ed-fit-css");
        if (!stCss && doc.head) {
          stCss = doc.createElement("style");
          stCss.id = "kd-ed-fit-css";
          stCss.textContent = "#kbar, #bar { display: none !important; } html, body { margin: 0; width: 100%; height: 100%; overflow: hidden; background: #07050f; }";
          doc.head.appendChild(stCss);
        }
        const st = doc.getElementById("stage");
        if (st) {
          const kw = (KD && KD.w) || parseInt(st.style.width, 10) || 1920;
          const kh = (KD && KD.h) || parseInt(st.style.height, 10) || 1080;
          const pw = Math.max(60, (wrap.clientWidth || 800) - 20);
          const ph = Math.max(60, (wrap.clientHeight || 450) - 20);
          const k = Math.min(pw / kw, ph / kh);
          st.style.transformOrigin = "top left";
          st.style.transform = "scale(" + k + ")";
          st.style.left = Math.round(((wrap.clientWidth || 800) - kw * k) / 2) + "px";
          st.style.top = Math.round(((wrap.clientHeight || 450) - kh * k) / 2) + "px";
        }
      }
    } catch (e) {}
  }
  post({ cmd: "fit" });
  setTimeout(renderOvHandle, 40);
}

async function load() {
  const r = await api("GET", "/api/spec");
  SPEC = r.body.spec || {}; VER = r.body.version || ""; SEL = -1; DIRTY = false; ISSUES = {};
  if (r.body.audio) AUDIO_MAP = r.body.audio;
  if (!SPEC.scenes) SPEC.scenes = [];
  if (!SPEC.tracks) SPEC.tracks = [];
  if (ensureIds()) DIRTY = true;           // v3.12 (sèvè a deja bay id yo; sa se sekirite)
  const _vm = (AUDIO_MAP && AUDIO_MAP.voices) || {};
  let _vbound = false;
  SPEC.scenes.forEach((sc, i) => {
    if (sc && sc.voice && !sc.voice_file) {
      const vf = (sc.id && _vm[sc.id]) || _vm[String(i)];
      if (vf) { sc.voice_file = vf; _vbound = true; }
    }
  });
  if (_vbound) DIRTY = true;
  if (SPEC.scenes.some(s => s.voice && !s.voice_file) && (!_vm || !Object.keys(_vm).length)) {
    api("GET", "/api/audio-map").then(am => {
      if (am && am.body && am.body.audio && am.body.audio.voices) {
        AUDIO_MAP = am.body.audio;
        const nvm = AUDIO_MAP.voices || {};
        let chg = false;
        SPEC.scenes.forEach((sc, i) => {
          if (sc && sc.voice && !sc.voice_file) {
            const vf = (sc.id && nvm[sc.id]) || nvm[String(i)];
            if (vf) { sc.voice_file = vf; chg = true; }
          }
        });
        if (chg) { renderTimeline(); }
      }
    }).catch(() => {});
  }
  if (Array.isArray(r.body.timing) && r.body.timing.length) {   // v3.12: vrè dire yo TOUSWIT, pa 2 s jiskaske aperçu a chaje
    const tm = r.body.timing, last = tm[tm.length - 1];
    KD = Object.assign({}, KD || {}, { scenes: tm, total: Math.max((last.start || 0) + (last.dur || 0), r.body.total || 0) });
  } else {
    KD = { scenes: [], total: r.body.total || 0 };
  }
  $("#vtitle").value = SPEC.title || (SPEC.brand && SPEC.brand.name) || "";
  const KI = window.KadansI18n;
  const urlLang = new URLSearchParams(location.search).get("lang");
  if (KI && (r.body.embedded || urlLang)) {
    // Anndan WASDEV: entèfas la = lang sistèm WASDEV la (URL), pa gen selektè; videyo a kenbe lang pa l
    KI.setEmbedded(true);
    KI.setLang(urlLang || KI.getLang());
    if (!SPEC.lang && !(SPEC.voice && SPEC.voice.lang)) SPEC.lang = KI.getLang();
  } else {
    const curLang = localStorage.getItem("wasdev_kadans_lang") || SPEC.lang || (SPEC.voice && SPEC.voice.lang) || "fr";
    if (KI) KI.setLang(curLang);
    if ($("#vlang")) $("#vlang").value = curLang;
  }
  updateVolUI(SPEC.volume != null ? SPEC.volume : 1);
  try { labelHistory(); } catch (e) {}
  mountPreview();
  selTab(LT); selRTab(RT); paintIcons();
  renderTimeline(); msg(KI ? KI.t("ready", "pare") : "pare");
  if (SPEC.scenes && SPEC.scenes.length > 0 && SEL < 0) {
    selectScene(0);
  } else if (!SPEC.scenes || SPEC.scenes.length === 0) {
    SEL = -1;
    renderRight();
  }
}
function mountPreview() {
  const pv = $("#pv");
  if (!pv) return;
  pv.onload = () => {
    try {
      const doc = pv.contentDocument || (pv.contentWindow && pv.contentWindow.document);
      if (doc && doc.body && doc.body.innerText && doc.body.innerText.indexOf('"error": "not found"') >= 0) {
        api("POST", "/api/build", { spec: cln() }).then(r => {
          if (r.body && r.body.ok) {
            pv.src = "composition.html?token=" + encodeURIComponent(TOK) + "&_t=" + Date.now();
          }
        }).catch(() => {});
        return;
      }
    } catch (ex) {}
    fitScreenView();
    post({ cmd: "pause" });
    post({ cmd: "seek", t: CUR });
    applySink();
    try {
      const w = pv.contentWindow;
      if (w) {
        w.addEventListener("wheel", e => {
          e.preventDefault();
          const factor = e.deltaY < 0 ? 1.12 : (1 / 1.12);
          setPvZoom(PVZOOM * factor);
        }, { passive: false });
      }
    } catch (e) {}
  };
  pv.src = "composition.html?token=" + encodeURIComponent(TOK) + "&_t=" + Date.now();
}
const post = m => { const w = $("#pv").contentWindow; if (w) w.postMessage(m, "*"); };
function applySink() { try { const spk = localStorage.getItem("kd_spk"); if (!spk) return; const w = $("#pv").contentWindow; if (!w) return; w.document.querySelectorAll("audio,video").forEach(e => { if (e.setSinkId) e.setSinkId(spk).catch(() => {}); }); } catch (e) {} }
async function syncOfficialWasdevAudio() {
  try {
    const r = await api("GET", "/api/audio-settings");
    if (!r || !r.body || !r.body.ok) return;
    const inName = (r.body.input && r.body.input.name) || "";
    const outName = (r.body.output && r.body.output.name) || "";
    if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) return;
    const devs = await navigator.mediaDevices.enumerateDevices().catch(() => []);
    if (inName && devs.length) {
      const matchIn = devs.find(d => d.kind === "audioinput" && d.label && (
        d.label.toLowerCase() === inName.toLowerCase() ||
        d.label.toLowerCase().includes(inName.toLowerCase()) ||
        inName.toLowerCase().includes(d.label.toLowerCase())
      ));
      if (matchIn) {
        localStorage.setItem("kd_mic", matchIn.deviceId);
        localStorage.setItem("kd_mic_name", matchIn.label);
      }
    }
    if (outName && devs.length) {
      const matchOut = devs.find(d => d.kind === "audiooutput" && d.label && (
        d.label.toLowerCase() === outName.toLowerCase() ||
        d.label.toLowerCase().includes(outName.toLowerCase()) ||
        outName.toLowerCase().includes(d.label.toLowerCase())
      ));
      if (matchOut) {
        localStorage.setItem("kd_spk", matchOut.deviceId);
        localStorage.setItem("kd_spk_name", matchOut.label);
        applySink();
      }
    }
  } catch (e) {}
}
let AUDIOELS = [];
function notifyWasdevAudio(cmd, extra) {
  const mvol = (SPEC && SPEC.volume != null) ? SPEC.volume : 1;
  const payload = Object.assign({ cmd, t: CUR, volume: mvol, playing: !!playing }, extra || {});
  api("POST", "/api/audio-bridge", payload).catch(() => {});
}
function stopAudio() {
  AUDIOELS.forEach(a => {
    if (!a) return;
    try {
      a._stopped = true;
      if (a._to) { clearTimeout(a._to); a._to = null; }
      if (a._endTo) { clearTimeout(a._endTo); a._endTo = null; }
      a.onloadedmetadata = null;
      a.onerror = null;
      a.onended = null;
      a.ontimeupdate = null;
      a.pause();
      try { a.currentTime = 0; } catch (x) {}
      if (typeof a.src === "string") {
        a.removeAttribute("src");
        try { a.load(); } catch (x) {}
      }
    } catch (e) {}
  });
  AUDIOELS = [];
  try { if (window.speechSynthesis) window.speechSynthesis.cancel(); } catch (e) {}
  notifyWasdevAudio("stop", { playing: false, native: false });
}
function syncActiveAudioVolumes() {
  const mvol = (SPEC && SPEC.volume != null) ? SPEC.volume : 1;
  const mv = (SPEC && SPEC.music && SPEC.music.volume != null) ? SPEC.music.volume : 0.22;
  AUDIOELS.forEach(a => {
    if (!a || a._stopped) return;
    try {
      if (a._kind === "music") {
        if (a.volume != null) a.volume = Math.max(0, Math.min(1, mv * mvol));
      } else if (a._clip) {
        const cv = (a._clip.volume != null) ? a._clip.volume : 1;
        if (a.volume != null) a.volume = Math.max(0, Math.min(1, cv * mvol));
      } else if (a._kind === "video" && a._scene) {
        const scv = (typeof a._scene.audio === "number") ? a._scene.audio : 0.9;
        if (a.volume != null) a.volume = Math.max(0, Math.min(1, scv * mvol));
      } else if (a._kind === "voice" && a._scene) {
        const vv = (typeof a._scene.voice_volume === "number") ? a._scene.voice_volume : 1;
        if (a.volume != null) a.volume = Math.max(0, Math.min(1, vv * mvol));
      } else if (a._kind === "mix") {
        if (a.volume != null) a.volume = Math.max(0, Math.min(1, mvol));
      } else if (a.volume != null) {
        a.volume = Math.max(0, Math.min(1, (a._baseVol != null ? a._baseVol : 1) * mvol));
      }
    } catch (e) {}
  });
  post({ cmd: "volume", volume: mvol, musicVolume: mv });
  notifyWasdevAudio("volume", { volume: mvol, musicVolume: (SPEC && SPEC.music ? SPEC.music.volume : 0) });
}
function audioSources() {
  const mvol = (SPEC && SPEC.volume != null) ? SPEC.volume : 1;
  if (mvol <= 0.001) return [];
  const vMuted = tState({ key: "voice" }, "muted");
  const mMuted = tState({ key: "music" }, "muted");
  const sMuted = tState({ key: "scenes" }, "muted");
  const anyUserMuted = (SPEC.tracks || []).some((tk, ti) => tState({ key: "tk" + ti, track: ti }, "muted"));
  const anySolo = (SPEC.tracks || []).some(tk => tk && tk.solo);   // solo (T4): sèlman track solo yo jwe
  // Si okenn track pa mute/solo epi nou gen master preview-audio.wav ki deja mikse pa FFmpeg, sèvi ak li an priyorite
  if (!vMuted && !mMuted && !sMuted && !anyUserMuted && !anySolo && !DIRTY && AUDIO_MAP && AUDIO_MAP.mix && (!SPEC.music || SPEC.music.volume == null || Math.abs(SPEC.music.volume - 0.22) < 0.01)) {
    return [{ src: withTok(AUDIO_MAP.mix), start: 0, dur: Math.max(total(), 1), vol: Math.min(1, mvol), kind: "mix" }];
  }

  const out = [];
  const seenKeys = new Set();
  const trackMediaSrcs = new Set();
  const normAudioKey = s => {
    if (!s) return "";
    const base = String(s).split("?")[0].split("#")[0].trim().toLowerCase();
    const parts = base.split(/[\\\/]/);
    return parts[parts.length - 1] || base;
  };

  const addSource = (s) => {
    if (!s) return;
    const key = (s.src || s.sfx || s.tts || "") + "@" + (Math.round((s.start || 0) * 100) / 100) + "@" + (s.kind || "");
    if (seenKeys.has(key)) return;
    seenKeys.add(key);
    out.push(s);
  };

  (SPEC.tracks || []).forEach((tk, ti) => {
    if (tState({ key: "tk" + ti, track: ti }, "muted")) return;
    if (anySolo && !tk.solo) return;                 // gen solo: sote track ki pa solo

    (tk.clips || []).forEach(c => {
      const k = c.kind || mediaKind(c.src || "", c.type);
      if (["audio", "video", "sfx", "music", "voice"].indexOf(k) >= 0 && (c.src || c.sfx)) {
        if (c.src) {
          trackMediaSrcs.add(String(c.src).trim().toLowerCase());
          const fn = normAudioKey(c.src);
          if (fn) trackMediaSrcs.add(fn);
        }
        const cv = (c.volume != null ? c.volume : 1) * mvol;
        addSource({
          src: c.src ? withTok(c.src) : "",
          sfx: c.sfx || "",
          start: c.start || 0,
          dur: c.dur || 2,
          inOff: c.in || 0,
          vol: Math.min(1, Math.max(0, cv)),
          kind: k,
          clip: c,
          trackIndex: ti
        });
      }
    });
  });

  // Deteksyon egzat klip vwa ki sou track yo pou evite 2 vwa jwe an menm tan (anti-collision)
  const trackVoiceSpans = [];
  (SPEC.tracks || []).forEach((tk, ti) => {
    if (tState({ key: "tk" + ti, track: ti }, "muted")) return;
    (tk.clips || []).forEach(c => {
      const isVoice = (tk.kind === "voice" || c.kind === "voice" || c.voice || /vwa|voice|voix|narr/i.test(tk.name || "") || /\.(vwa|voice|voix)\./i.test(c.src || "") || /\/medya\/vwa\//i.test(c.src || ""));
      if (isVoice) {
        const c_st = floatVal(c.start, 0), c_du = floatVal(c.dur, 2);
        trackVoiceSpans.push({ start: c_st, end: c_st + c_du });
      }
    });
  });

  if (!vMuted) {
    SPEC.scenes.forEach((sc, i) => {
      const ss = sStart(i), se = ss + sDur(i);
      // Si gen yon klip vwa sou yon track ki kouvri sèn sa a, pa jwe vwa sèn nan an menm tan (anti-collision)
      const hasTrackVoiceCollision = trackVoiceSpans.some(v => v.start < se - 0.2 && v.end > ss + 0.2);
      if (hasTrackVoiceCollision) return;

      const vf = voiceUrlForScene(sc, i);
      const vv = (typeof sc.voice_volume === "number" ? sc.voice_volume : 1);
      const vfn = normAudioKey(vf);
      const vOff = Number(sc.voice_offset || 0);
      const vIn = Math.max(0, Number(sc.voice_in || 0));
      const vDur = (sc.voice_dur != null ? Number(sc.voice_dur) : sDur(i));
      const vStart = Math.max(0, ss + vOff);

      if (vf && !trackMediaSrcs.has(String(vf).trim().toLowerCase()) && (!vfn || !trackMediaSrcs.has(vfn))) {
        addSource({ src: withTok(vf), start: vStart, dur: vDur, inOff: vIn, vol: Math.min(1, vv * mvol), kind: "voice", scene: sc, sceneIndex: i });
      } else if (!vf && sc.voice && String(sc.voice).trim()) {
        // Pa gen vwa wobo navigatè: vwa a dwe soti nan ElevenLabs.
        // Si vwa a poko jenere, deklanche build pou ElevenLabs pwodwi li.
        if (!_pendingVoiceFetch) {
          _pendingVoiceFetch = true;
          api("GET", "/api/audio-map").then(am => {
            _pendingVoiceFetch = false;
            if (am && am.body && am.body.audio && am.body.audio.voices && Object.keys(am.body.audio.voices).length) {
              AUDIO_MAP = am.body.audio;
              renderTimeline();
            }
          }).catch(() => { _pendingVoiceFetch = false; });
        }
      }
    });
  }

  if (!sMuted) {
    SPEC.scenes.forEach((sc, i) => {
      if (sc.type === "video" && sc.audio !== false && sc.audio !== 0) {
        const vs = srcOf(sc);
        const vsn = normAudioKey(vs);
        const scv = (typeof sc.audio === "number" ? sc.audio : 0.9);
        if (vs && !trackMediaSrcs.has(String(vs).trim().toLowerCase()) && (!vsn || !trackMediaSrcs.has(vsn))) {
          addSource({ src: withTok(vs), start: sStart(i), dur: sDur(i), inOff: sc.in || 0, vol: Math.min(1, scv * mvol), kind: "video", scene: sc, sceneIndex: i });
        }
      }
    });
  }

  if (!mMuted && SPEC.music) {
    const mf = SPEC.music.file || (AUDIO_MAP && AUDIO_MAP.music) || "";
    const mfn = normAudioKey(mf);
    const mv = (SPEC.music.volume != null ? SPEC.music.volume : 0.22);
    if (mf && !trackMediaSrcs.has(String(mf).trim().toLowerCase()) && (!mfn || !trackMediaSrcs.has(mfn))) {
      addSource({ src: withTok(mf), start: 0, dur: Math.max(total(), 1), vol: Math.min(1, mv * mvol), loop: !SPEC.music.file, kind: "music" });
    }
  }

  if (!out.length && AUDIO_MAP && AUDIO_MAP.mix && (!vMuted || !mMuted)) {
    addSource({ src: withTok(AUDIO_MAP.mix), start: 0, dur: Math.max(total(), 1), vol: Math.min(1, mvol), kind: "mix" });
  }

  return out;
}
function playAudio() {
  stopAudio();
  if (!playing) return;
  const spk = (function () { try { return localStorage.getItem("kd_spk"); } catch (e) { return ""; } })();
  const curTime = CUR;
  const srcs = audioSources();
  let bridgeRequested = false;

  const fallbackToWasdevBridge = () => {
    if (bridgeRequested || !playing) return;
    bridgeRequested = true;
    AUDIOELS.forEach(a => {
      if (!a) return;
      try {
        a._stopped = true;
        if (a._to) { clearTimeout(a._to); a._to = null; }
        if (a._endTo) { clearTimeout(a._endTo); a._endTo = null; }
        a.pause();
        a.src = "";
      } catch (e) {}
    });
    AUDIOELS = [];
  };

  notifyWasdevAudio("play", { playing: true, native: false });

  srcs.forEach(s => {
    const start = s.start || 0;
    const dur = s.dur || 0;
    const end = start + dur;

    // Si pozisyon tèt lekti a (curTime) deja depase fen clip la, li pa dwe jwe
    if (!s.loop && curTime >= end - 0.02) return;

    if (s.sfx && !s.src) {
      const off = curTime - start;
      const holder = {
        _stopped: false,
        _to: null,
        pause() { this._stopped = true; if (this._to) clearTimeout(this._to); },
        _kind: "sfx",
        _clip: s.clip
      };
      const playSfxNow = () => {
        if (!playing || holder._stopped) return;
        playSfxSynth(s.sfx);
      };
      if (off < -0.02) {
        holder._to = setTimeout(playSfxNow, (start - curTime) * 1000);
        AUDIOELS.push(holder);
      } else if (off < Math.min(dur, 0.25)) {
        playSfxNow();
      }
      return;
    }

    if (s.tts && !s.src) {
      // Okenn motè wobo: ElevenLabs sèlman
      return;
    }

    if (!s.src) return;

    const a = new Audio();
    a.preload = "auto";
    a.src = s.src;
    a._kind = s.kind;
    a._clip = s.clip;
    a._scene = s.scene;
    a._baseVol = s.vol;
    a._stopped = false;
    a._to = null;
    a._endTo = null;
    if (s.loop) a.loop = true;
    a.volume = Math.max(0, Math.min(1, s.vol));
    if (spk && a.setSinkId) a.setSinkId(spk).catch(() => {});

    const baseIn = s.inOff || 0;
    // VITÈS klip / sèn videyo a: sekonn fichye = sekonn timeline × vitès (koupe yo rete egzak)
    const rate = Math.max(0.25, Math.min(4, +((s.clip && s.clip.speed) || (s.scene && s.scene.type === "video" && s.scene.speed) || 1)));
    try { a.playbackRate = rate; a.preservesPitch = true; } catch (e) {}
    const maxMediaPos = baseIn + dur * rate;

    const stopThisAudio = () => {
      a._stopped = true;
      if (a._to) { clearTimeout(a._to); a._to = null; }
      if (a._endTo) { clearTimeout(a._endTo); a._endTo = null; }
      try {
        a.pause();
      } catch (e) {}
    };

    a.ontimeupdate = () => {
      if (a._stopped) return;
      if (!s.loop && a.currentTime >= maxMediaPos - 0.02) {
        stopThisAudio();
      }
    };

    const startAt = (targetOff) => {
      if (!playing || a._stopped) return;
      const seekTarget = Math.max(0, baseIn + targetOff * rate);
      const remainingTime = Math.max(0, dur - targetOff);

      if (!s.loop && remainingTime <= 0.02) {
        stopThisAudio();
        return;
      }

      const doPlay = () => {
        if (!playing || a._stopped) return;
        try { if (seekTarget > 0.02) a.currentTime = seekTarget; } catch (e) {}
        const p = a.play();
        if (p && p.catch) p.catch(() => fallbackToWasdevBridge());

        if (!s.loop && remainingTime > 0) {
          if (a._endTo) clearTimeout(a._endTo);
          a._endTo = setTimeout(() => {
            if (a._stopped) return;
            stopThisAudio();
          }, remainingTime * 1000);
        }
      };

      if (a.readyState >= 1) {
        doPlay();
      } else {
        a.addEventListener("loadedmetadata", () => {
          if (!playing || a._stopped) return;
          doPlay();
        }, { once: true });
        a.addEventListener("error", () => {
          if (!playing || a._stopped) return;
          fallbackToWasdevBridge();
        }, { once: true });
        a.load();
      }
    };

    const off = curTime - start;
    if (off < -0.02) {
      a._to = setTimeout(() => {
        if (!playing || a._stopped) return;
        startAt(0);
      }, (start - curTime) * 1000);
    } else if (s.loop || off < dur) {
      startAt(Math.max(0, off));
    }

    AUDIOELS.push(a);
  });
}
function setPlaying(p) {
  if (p && total() <= 0) {
    msg((window.KadansI18n && window.KadansI18n.t("timeline_empty_play_hint")) || "Timeline vid — ajoute yon sèn oswa yon clip anvan");
    return;
  }
  playing = p; setPlayIcon();
  if (p) {
    if (CUR >= total() - 0.05) CUR = 0;
    post({ cmd: "seek", t: CUR });
    post({ cmd: "play" });
    playAudio();
  } else {
    post({ cmd: "pause" });
    stopAudio();
  }
}
addEventListener("message", e => {
  const m = e.data || {};
  if (m.evt === "ready") { const old = KD; KD = m.kadans; noteMoved(old, KD); renderTimeline(); updateDur(); fitScreenView(); }
  else if (m.evt === "time") { CUR = +m.t; movePlayhead(); $("#time").textContent = CUR.toFixed(1) + " / " + total().toFixed(1) + " s"; }
  else if (m.evt === "ended") {
    const tot = total();
    if (CUR >= tot - 0.3 || (m.t != null && m.t >= tot - 0.3)) {
      CUR = tot;
      movePlayhead();
      setPlaying(false);
    }
  }
  else if (m.evt === "wheel") { const factor = m.deltaY < 0 ? 1.12 : (1 / 1.12); setPvZoom(PVZOOM * factor); }
  else if (m.evt === "click") { selectScene(m.spec_index); }
  else if (m.evt === "keydown") {
    if (m.code === "Space") { setPlaying(!playing); }
    else if (m.code === "ArrowRight") { seek(CUR + 1 / ((SPEC && SPEC.fps) || 30)); }
    else if (m.code === "ArrowLeft") { seek(CUR - 1 / ((SPEC && SPEC.fps) || 30)); }
  }
});
function updateDur() { $("#dur").textContent = (SPEC.scenes && SPEC.scenes.length ? SPEC.scenes.length + " sen / " : "") + total().toFixed(1) + " s"; }
// v3.12: yon sèn pa janm chanje longè AN SILANS. Lè yon rebati bay yon lòt dire (vwa a fin jenere / mezire, tèks vwa a
// chanje), editè a di ki sèn ak konbyen — moun nan konnen poukisa sa ki apre l yo deplase.
function noteMoved(oldK, newK) {
  if (!oldK || !oldK.scenes || !newK || !newK.scenes || !SPEC) return;
  const moved = [];
  newK.scenes.forEach(e => {
    const o = oldK.scenes.find(x => x.id === e.id); if (!o || Math.abs((o.dur || 0) - (e.dur || 0)) < 0.15) return;
    const i = SPEC.scenes.findIndex(s => s.id === e.id);
    if (i < 0 || SPEC.scenes[i].duration != null && Math.abs(SPEC.scenes[i].duration - e.dur) < 0.05) return;  // moun nan te mete l
    moved.push(_tk("dur_moved", "Sèn {n}: {a} s → {b} s").replace("{n}", i + 1).replace("{a}", (o.dur || 0).toFixed(1)).replace("{b}", (e.dur || 0).toFixed(1))
      + (e.measured && !o.measured ? " (" + _tk("dur_measured", "vrè vwa a") + ")" : ""));
  });
  if (!moved.length) return;
  let t = document.getElementById("kmoved");
  if (!t) { t = document.createElement("div"); t.id = "kmoved";
    t.style.cssText = "position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:99998;max-width:70vw;padding:7px 12px;border-radius:8px;" +
      "background:#3b1d70;border:1px solid #8b5cf6;color:#f3eefe;font:600 12px/1.4 system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.5)";
    document.body.appendChild(t); }
  t.textContent = _tk("dur_moved_head", "Dire chanje:") + " " + moved.slice(0, 3).join(" · ") + (moved.length > 3 ? " …" : "");
  t.style.display = "block"; clearTimeout(t._h); t._h = setTimeout(() => { t.style.display = "none"; }, 8000);
}

// ---- Eta track (lock / hide / mute) ----
function tState(def, pre) {
  if (def.track != null && SPEC.tracks && SPEC.tracks[def.track]) return !!SPEC.tracks[def.track][pre];
  try { return localStorage.getItem(pre + "_" + def.key) === "1"; } catch (x) { return false; }
}
function tToggle(def, pre) {
  const v = !tState(def, pre);
  if (def.track != null && SPEC.tracks[def.track]) { SPEC.tracks[def.track][pre] = v; DIRTY = true; }
  else { try { localStorage.setItem(pre + "_" + def.key, v ? "1" : "0"); } catch (x) {} }
  if (playing && (pre === "muted" || pre === "solo")) playAudio();
  renderTimeline();
}
function trackLockedByKey(key) {
  if (key && key.indexOf("tk") === 0) { const ti = +key.slice(2); return !!(SPEC.tracks[ti] && SPEC.tracks[ti].locked); }
  try { return localStorage.getItem("locked_" + key) === "1"; } catch (x) { return false; }
}
// ---- TIMELINE (sen + vwa + mizik + track itilizate yo) ----
// Palèt amonik siklik Kadans (6 aksan thèm × 6 nivo teyint HSL pou 36 koulè kowòdone san kolizyon)
const TRACK_PALETTE = [
  "#8b5cf6", "#22d3ee", "#10b981", "#f59e0b", "#ef4444", "#ec4899",
  "#b99dfa", "#7ae4f5", "#70d5b4", "#f9c56d", "#f58f8f", "#f492c2",
  "#6845b9", "#1a9eb2", "#0c8b61", "#b87708", "#b33333", "#b13673",
  "#d1befc", "#a7ecf8", "#a0e3cd", "#fbda9d", "#f9b4b4", "#f7b6d7",
  "#462e7b", "#116a77", "#085d41", "#7b4f06", "#782222", "#76244d",
  "#a27df8", "#4fdbf1", "#40c79a", "#f7af3c", "#f26a6a", "#f06dae"
];
function tracksDef() {
  // Track itilizatè yo ANLÈ (sak pi nouvo nan tèt), epi Sen/Vwa/Mizik anba - tankou pwofesyonel
  SPEC.tracks = SPEC.tracks || [];
  if (!SPEC.tracks.length && (!SPEC.scenes || !SPEC.scenes.length)) {
    SPEC.tracks = [
      { kind: "video", name: "Videyo 1", clips: [] },
      { kind: "audio", name: "Odyo 1", clips: [] }
    ];
  }
  const defs = (SPEC.tracks || []).map((tk, ti) => ({ key: "tk" + ti, name: tk.name || tk.kind, kind: tk.kind, track: ti, height: tk.height }));
  if (SPEC.scenes && SPEC.scenes.length > 0 && !SPEC._hide_scenes) {
    defs.push({ key: "scenes", name: "Sen", kind: "scenes" });
  }
  if ((SPEC.scenes && SPEC.scenes.some(s => s.voice || s.voice_file)) || TRACKSEL === "voice" || VOICESEL != null || (SPEC.tracks || []).some(t => t.kind === "voice")) {
    defs.push({ key: "voice", name: "Vwa", kind: "voice" });
  }
  if (SPEC.music) defs.push({ key: "music", name: "Mizik", kind: "music" });
  defs.forEach((d, i) => {
    let c = (d.track != null && SPEC.tracks[d.track] && SPEC.tracks[d.track].color) || null;
    if (!c) { try { c = localStorage.getItem("kdtc_" + d.key); } catch (x) {} }
    d.color = c || TRACK_PALETTE[i % TRACK_PALETTE.length];   // chak track koulè pa l (chanjab)
    if (d.track == null) { try { const nn = localStorage.getItem("kdtn_" + d.key); if (nn) d.name = nn; } catch (x) {} }
    let h = (d.track != null && SPEC.tracks[d.track] && SPEC.tracks[d.track].height) || (SPEC._trackH && SPEC._trackH[d.key]) || null;
    if (!h) { try { const sh = localStorage.getItem("kdth_" + d.key); if (sh) h = +sh; } catch (x) {} }
    d.height = h || (d.kind === "scenes" || d.kind === "video" ? 54 : (d.kind === "voice" || d.kind === "audio" || d.kind === "music" ? 48 : 42));
  });
  trackLabels(defs);
  return defs;
}
// Track head titles: a clear kind name + its NUMBER per kind, top to bottom ("Vwa 1", "Vwa 2", "Odyo 1", "SFX 1",
// "Mizik 1", "Videyo 1", "Tèks 1"...), recomputed on every render (adding / removing a track renumbers them).
// A custom name is kept after the number ("Odyo 2 · Ambyans lanmè").
const TRACK_KIND_LABEL = { voice: "Vwa", audio: "Odyo", sfx: "SFX", music: "Mizik", video: "Videyo", image: "Imaj", text: "Tèks", asset: "Asset", scenes: "Sen" };
const AUTO_TRACK_NAME = /^(audio|odyo|video|videyo|image|imaj|text|teks|tèks|asset|sfx|voice|vwa|music|mizik|sen|scenes?)(\s*\d+)?$/i;
function trackFamily(d) {
  if (d.track == null) return d.kind;                                  // built-in lanes: scenes / voice / music
  const tk = SPEC.tracks[d.track] || {}, clips = tk.clips || [];
  if (d.kind !== "audio") return TRACK_KIND_LABEL[d.kind] ? d.kind : "audio";
  const nm = String(tk.name || "");
  if (/vwa|voice|voix|narr|dialog/i.test(nm) || tk.voice || (clips.length && clips.every(c => c.voice || /\/medya\/vwa\/|(^|\/)voices?\//.test(c.src || "")))) return "voice";
  if (clips.length && clips.every(c => /\/medya\/mizik\//.test(c.src || ""))) return "music";
  if (clips.length && clips.every(c => c.kind === "sfx" || /\/medya\/sfx\//.test(c.src || ""))) return "sfx";
  return "audio";
}
function trackLabels(defs) {
  const count = {};
  defs.forEach(d => {
    const fam = trackFamily(d), base = TRACK_KIND_LABEL[fam] || fam;
    count[fam] = (count[fam] || 0) + 1;
    const raw = String(d.name || "").trim();
    const custom = raw && !AUTO_TRACK_NAME.test(raw) && raw !== base ? raw : "";
    d.num = base + " " + count[fam]; d.custom = custom;
    d.label = d.num + (custom ? " · " + custom : "");
    d.name = custom || base;                                           // rename prompt edits the custom part
  });
}

function wireTrackResizer(resizer, rResizer, def, nm, row) {
  const onDown = ev => {
    ev.preventDefault(); ev.stopPropagation();
    const y0 = ev.clientY;
    const h0 = nm.offsetHeight;
    resizer.classList.add("resizing");
    if (rResizer) rResizer.classList.add("resizing");
    document.body.style.cursor = "ns-resize";
    const mv = e => {
      const nh = Math.max(28, Math.min(280, h0 + (e.clientY - y0)));
      nm.style.height = nh + "px";
      row.style.height = nh + "px";
      movePlayhead();
    };
    const up = e => {
      document.removeEventListener("mousemove", mv);
      document.removeEventListener("mouseup", up);
      resizer.classList.remove("resizing");
      if (rResizer) rResizer.classList.remove("resizing");
      document.body.style.cursor = "";
      const finalH = Math.max(28, Math.min(280, h0 + (e.clientY - y0)));
      if (def.track != null && SPEC.tracks[def.track]) {
        SPEC.tracks[def.track].height = finalH;
      } else {
        SPEC._trackH = SPEC._trackH || {};
        SPEC._trackH[def.key] = finalH;
        try { localStorage.setItem("kdth_" + def.key, finalH); } catch (x) {}
      }
      DIRTY = true;
      renderTimeline();
      msg("Wotè track '" + def.name + "' regle: " + finalH + "px");
    };
    document.addEventListener("mousemove", mv);
    document.addEventListener("mouseup", up);
  };
  resizer.addEventListener("mousedown", onDown);
  if (rResizer) rResizer.addEventListener("mousedown", onDown);

  const resetH = ev => {
    ev.stopPropagation();
    if (def.track != null && SPEC.tracks[def.track]) delete SPEC.tracks[def.track].height;
    else if (SPEC._trackH) delete SPEC._trackH[def.key];
    try { localStorage.removeItem("kdth_" + def.key); } catch (x) {}
    DIRTY = true; renderTimeline(); msg("Wotè track '" + def.name + "' retounen pa defo");
  };
  resizer.addEventListener("dblclick", resetH);
  if (rResizer) rResizer.addEventListener("dblclick", resetH);
}

function wireTrackDrag(nm, drag, def, row) {
  const onStartDrag = ev => {
    if (ev.button !== 0) return;
    if (ev.target.classList.contains("t-resizer") || ev.target.classList.contains("dot") || ev.target.closest(".tctl")) return;
    const y0 = ev.clientY;
    let moved = false;
    let dropLine = null;
    let targetDef = null;
    let insertPos = "before";

    const mv = e => {
      if (!moved && Math.abs(e.clientY - y0) > 4) {
        moved = true;
        nm.classList.add("t-dragging");
        row.classList.add("t-dragging");
        document.body.style.cursor = "grabbing";
        dropLine = document.getElementById("trackDropLine");
        if (!dropLine) {
          dropLine = document.createElement("div");
          dropLine.id = "trackDropLine";
          dropLine.className = "t-drop-line";
          const namesWrap = $("#tlnames");
          if (namesWrap) namesWrap.appendChild(dropLine);
        }
      }
      if (!moved) return;

      const namesList = Array.from(document.querySelectorAll("#names .tname"));
      let hit = null;
      for (const t of namesList) {
        const rc = t.getBoundingClientRect();
        if (e.clientY >= rc.top && e.clientY <= rc.bottom) {
          hit = t;
          const mid = rc.top + rc.height / 2;
          insertPos = e.clientY < mid ? "before" : "after";
          const lineY = insertPos === "before" ? t.offsetTop : (t.offsetTop + t.offsetHeight);
          if (dropLine) {
            dropLine.style.top = lineY + "px";
            dropLine.style.display = "block";
          }
          break;
        }
      }
      if (hit) {
        const hitKey = hit.dataset.trackKey;
        targetDef = tracksDef().find(d => d.key === hitKey) || null;
      } else {
        targetDef = null;
        if (dropLine) dropLine.style.display = "none";
      }
    };

    const up = e => {
      document.removeEventListener("mousemove", mv);
      document.removeEventListener("mouseup", up);
      document.body.style.cursor = "";
      if (dropLine) dropLine.remove();
      nm.classList.remove("t-dragging");
      row.classList.remove("t-dragging");

      if (!moved) {
        TRACKSEL = def.key;
        document.querySelectorAll("#names .tname").forEach(el => {
          const isSel = el.dataset.trackKey === TRACKSEL;
          el.classList.toggle("sel", isSel);
          const d2 = tracksDef().find(x => x.key === el.dataset.trackKey);
          if (d2) el.style.background = d2.color + (isSel ? "33" : "16");
        });
        document.querySelectorAll("#tracks .trow").forEach(el => {
          const isSel = el.dataset.track === TRACKSEL;
          const d2 = tracksDef().find(x => x.key === el.dataset.track);
          if (d2) {
            el.style.background = d2.color + (isSel ? "33" : "16");
            el.style.boxShadow = isSel ? ("inset 0 0 0 1px " + d2.color + "88") : "";
          }
        });
        if (def.key === "music" || def.key === "voice" || def.kind === "audio" || def.kind === "sfx") {
          CLIPSEL = null; selRTab("sound");
        } else if (def.key === "scenes") {
          if (SEL < 0 && SPEC.scenes.length) selectScene(0);
          else { CLIPSEL = null; selRTab("props"); }
        } else {
          CLIPSEL = null; selRTab("props");
        }
        return;
      }

      if (!targetDef || targetDef.key === def.key) return;

      if (def.track != null && targetDef.track != null) {
        snapshot();
        const fromIdx = def.track;
        const item = SPEC.tracks.splice(fromIdx, 1)[0];
        let toIdx = targetDef.track;
        if (insertPos === "after" && fromIdx > toIdx) toIdx++;
        else if (insertPos === "before" && fromIdx < toIdx) toIdx--;
        toIdx = Math.max(0, Math.min(SPEC.tracks.length, toIdx));
        SPEC.tracks.splice(toIdx, 0, item);
        DIRTY = true;
        renderTimeline();
        renderLeft();
        msg("Track '" + (item.name || item.kind) + "' deplase " + (insertPos === "before" ? "anlè" : "anba") + " '" + (targetDef.name || targetDef.kind) + "'");
      } else if (def.track != null) {
        snapshot();
        const fromIdx = def.track;
        const item = SPEC.tracks.splice(fromIdx, 1)[0];
        if (insertPos === "before" && (targetDef.key === "scenes" || targetDef.key === "voice" || targetDef.key === "music")) {
          SPEC.tracks.push(item);
        } else {
          SPEC.tracks.unshift(item);
        }
        DIRTY = true;
        renderTimeline();
        renderLeft();
        msg("Track '" + (item.name || item.kind) + "' deplase");
      }
    };
    document.addEventListener("mousemove", mv);
    document.addEventListener("mouseup", up);
  };

  drag.addEventListener("mousedown", onStartDrag);
  nm.addEventListener("mousedown", onStartDrag);
}

let VOICESEL = null;

function floatVal(v, def) {
  const n = parseFloat(v);
  return isNaN(n) ? def : n;
}

function voiceBlock(sc, i, color) {
  const b = document.createElement("div");
  const isSel = (VOICESEL === i) || (TRACKSEL === "voice" && SEL === i && !CLIPSEL);
  b.className = "blk" + (isSel ? " sel" : "");
  const vOffset = Number(sc.voice_offset || 0);
  const vIn = Math.max(0, Number(sc.voice_in || 0));
  const rawDur = (sc.voice_dur != null ? Number(sc.voice_dur) : (kdDur(sc, i) || sDur(i)));
  const vDur = Math.max(0.3, rawDur - vIn);
  const vStart = Math.max(0, sStart(i) + vOffset);

  b.style.left = (vStart * PPS) + "px";
  b.style.width = Math.max(14, vDur * PPS - 2) + "px";
  b.style.background = "linear-gradient(180deg," + color + "," + color + "cc)";
  b.style.borderColor = isSel ? "#ffffff" : color;
  b.style.cursor = "grab";

  const lbl = scName(sc) + (sc.voice_file ? " (anr.)" : (sc.voice ? " (AI)" : ""));
  b.innerHTML = '<span class="hdll" title="Koupe kòmansman vwa"></span>' +
                '<span class="lab">' + esc(lbl) + '</span>' +
                '<span class="hdl" title="Koupe finisman vwa"></span>';
  b.title = "Vwa sèn " + (i + 1) + ": " + esc(sc.voice || sc.voice_file || "") +
            " (" + vDur.toFixed(1) + "s) — Trennen pou avanse/recule; Koupe ak rebò yo; Del = efase vwa san kraze sèn.";

  const vf = voiceUrlForScene(sc, i);
  if (vf) drawWave(b, vf);

  const hdll = b.querySelector(".hdll");
  hdll.addEventListener("mousedown", ev => {
    ev.stopPropagation(); ev.preventDefault();
    if (trackLockedByKey("voice")) return;
    snapshot();
    const x0 = ev.clientX, s0 = vStart, right = s0 + vDur, in0 = vIn;
    const mv = e => {
      let ns = Math.max(0, Math.min(right - 0.3, s0 + (e.clientX - x0) / PPS));
      if (SNAP) ns = Math.round(ns * 10) / 10;
      const shift = ns - s0;
      sc.voice_offset = Math.round(((sc.voice_offset || 0) + shift) * 100) / 100;
      sc.voice_in = Math.max(0, Math.round((in0 + shift) * 100) / 100);
      sc.voice_dur = Math.max(0.3, Math.round((right - ns) * 100) / 100);
      b.style.left = (ns * PPS) + "px";
      b.style.width = Math.max(14, (right - ns) * PPS - 2) + "px";
    };
    const up = () => {
      document.removeEventListener("mousemove", mv);
      document.removeEventListener("mouseup", up);
      DIRTY = true; renderTimeline(); renderRight();
    };
    document.addEventListener("mousemove", mv);
    document.addEventListener("mouseup", up);
  });

  const hdl = b.querySelector(".hdl");
  hdl.addEventListener("mousedown", ev => {
    ev.stopPropagation(); ev.preventDefault();
    if (trackLockedByKey("voice")) return;
    const x0 = ev.clientX, w0 = b.offsetWidth;
    const mv = e => {
      b.style.width = Math.max(14, w0 + (e.clientX - x0)) + "px";
    };
    const up = () => {
      document.removeEventListener("mousemove", mv);
      document.removeEventListener("mouseup", up);
      let d = (b.offsetWidth + 2) / PPS;
      if (SNAP) d = Math.round(d * 10) / 10;
      snapshot();
      sc.voice_dur = Math.max(0.3, d);
      DIRTY = true; renderTimeline(); renderRight();
    };
    document.addEventListener("mousemove", mv);
    document.addEventListener("mouseup", up);
  });

  b.addEventListener("mousedown", ev => {
    if (ev.target === hdl || ev.target === hdll) return;
    ev.stopPropagation();
    const x0 = ev.clientX, l0 = b.offsetLeft;
    let moved = false;
    const mv = e => {
      if (trackLockedByKey("voice")) return;
      if (!moved && Math.abs(e.clientX - x0) > 4) {
        moved = true;
        b.style.cursor = "grabbing";
        b.style.zIndex = 9;
      }
      if (moved) {
        let nleft = Math.max(0, l0 + (e.clientX - x0));
        b.style.left = nleft + "px";
      }
    };
    const up = () => {
      document.removeEventListener("mousemove", mv);
      document.removeEventListener("mouseup", up);
      if (!moved) {
        selectVoice(i);
        return;
      }
      let ns = Math.max(0, b.offsetLeft / PPS);
      if (SNAP) ns = Math.round(ns * 10) / 10;
      snapshot();
      sc.voice_offset = Math.round((ns - sStart(i)) * 100) / 100;
      DIRTY = true;
      renderTimeline(); renderRight(); renderLeft();
      msg("Vwa sèn " + (i + 1) + " deplase: " + (sc.voice_offset >= 0 ? "+" : "") + sc.voice_offset.toFixed(2) + "s");
    };
    document.addEventListener("mousemove", mv);
    document.addEventListener("mouseup", up);
  });

  b.oncontextmenu = ev => {
    ev.preventDefault();
    selectVoice(i);
    voiceMenu(ev.clientX, ev.clientY, i);
  };

  return b;
}

function selectVoice(i) {
  VOICESEL = i;
  CLIPSEL = null;
  TRACKSEL = "voice";
  selectScene(i);
  selRTab("sound");
  const sc = SPEC.scenes[i];
  const wasPlaying = playing;
  stopAudio();
  const vStart = Math.max(0, sStart(i) + (sc.voice_offset || 0));
  CUR = vStart;
  movePlayhead();
  post({ cmd: "seek", t: CUR });
  $("#selinfo").textContent = "vwa sèn " + (i + 1) + ": " + (sc.voice || sc.voice_file || "");
  renderTimeline();
  if (wasPlaying) playAudio();
  msg("Vwa sèn " + (i + 1) + " chwazi");
}

function voiceMenu(x, y, i) {
  const old = document.getElementById("ctxmenu"); if (old) old.remove();
  const m = document.createElement("div"); m.id = "ctxmenu"; m.className = "menu";
  m.style.cssText = "display:block;position:fixed;left:" + x + "px;top:" + y + "px;z-index:200;min-width:210px";
  const sc = SPEC.scenes[i];
  const vf = voiceUrlForScene(sc, i);
  const items = [
    ["volume", "Tande vwa sa a (Preview)", () => {
      if (vf) { const a = new Audio(withTok(vf)); a.play().catch(() => {}); }
      else if (sc.voice) msg("Tèks: " + sc.voice);
    }],
    ["scissors", "Retabli pozisyon orijinal (0s)", () => {
      snapshot(); delete sc.voice_offset; delete sc.voice_in; delete sc.voice_dur;
      DIRTY = true; renderTimeline(); renderRight(); msg("Pozisyon vwa retabli");
    }],
    ["trash", "Efase vwa (kenbe sèn nan)", () => {
      snapshot();
      delete sc.voice; delete sc.voice_file; delete sc._regen;
      delete sc.voice_offset; delete sc.voice_in; delete sc.voice_dur;
      VOICESEL = null; DIRTY = true; renderTimeline(); renderRight(); renderLeft();
      msg("Vwa sèn " + (i + 1) + " efase — sèn nan rete entak");
    }]
  ];
  items.forEach(it => {
    const d = document.createElement("div"); d.className = "mi";
    d.innerHTML = svg(it[0]) + '<span style="flex:1">' + it[1] + '</span>';
    d.onclick = () => { m.remove(); it[2](); };
    m.appendChild(d);
  });
  document.body.appendChild(m);
  const r = m.getBoundingClientRect();
  if (r.right > window.innerWidth) m.style.left = (window.innerWidth - r.width - 6) + "px";
  if (r.bottom > window.innerHeight) m.style.top = (window.innerHeight - r.height - 6) + "px";
}

function renderTimeline() {
  if (!SPEC) return;
  if (ensureIds()) DIRTY = true;           // v3.12: yon sèn nouvo (nenpòt chemen) jwenn yon id estab touswit
  const T = total(), vw = ($("#tlscrollwrap").clientWidth || 600), W = Math.max(vw, Math.round((T + 2) * PPS));
  const inner = $("#tlinner"); inner.style.width = W + "px";
  const ruler = $("#ruler"); ruler.style.width = W + "px"; ruler.innerHTML = "";
  const stepS = PPS < 40 ? 5 : PPS < 90 ? 2 : 1;
  for (let s = 0; s <= (W / PPS) + 0.001; s += stepS) {
    const d = document.createElement("div"); d.className = "tk"; d.style.left = (s * PPS) + "px";
    d.textContent = (s < 60 ? s.toFixed(0) + "s" : Math.floor(s / 60) + ":" + String(Math.round(s % 60)).padStart(2, "0"));
    ruler.appendChild(d);
  }
  (SPEC.markers || []).forEach((mk, mi) => {       // pwen repè ak range markers / chapit
    const dur = Number(mk.dur || mk.duration || 0);
    const col = mk.color || "#fbbf24";
    if (dur > 0) {
      const band = document.createElement("div"); band.className = "marker-band";
      band.style.cssText = "position:absolute;top:0;bottom:0;cursor:pointer;z-index:3;background:" + col + "26;border-left:2px solid " + col + ";border-right:2px solid " + col + ";";
      band.style.left = ((mk.t || 0) * PPS) + "px";
      band.style.width = Math.max(4, dur * PPS) + "px";
      band.title = (mk.chapter ? "★ Chapit: " : "Zòn repè: ") + (mk.label || ("zòn " + (mi + 1))) + " (" + dur.toFixed(1) + "s)";
      band.onclick = e => { e.stopPropagation(); stopAudio(); CUR = mk.t || 0; movePlayhead(); post({ cmd: "seek", t: CUR }); };
      ruler.appendChild(band);
    }
    const el = document.createElement("div"); el.className = "marker";
    el.style.cssText = "position:absolute;top:0;bottom:0;width:2px;cursor:pointer;z-index:4;background:" + col;
    el.style.left = ((mk.t || 0) * PPS) + "px";
    const lab = (mk.chapter ? "★ Chapit: " : "") + (mk.label || ("repè " + (mi + 1))) + " · " + (mk.t || 0).toFixed(1) + "s" + (dur > 0 ? " [" + dur.toFixed(1) + "s]" : "") + (mk.comment ? "\n" + mk.comment : "") + " (klik = sote, double-klik = efase)";
    el.title = lab;
    el.onclick = e => { e.stopPropagation(); stopAudio(); CUR = mk.t || 0; movePlayhead(); post({ cmd: "seek", t: CUR }); };
    el.ondblclick = e => { e.stopPropagation(); snapshot(); SPEC.markers.splice(mi, 1); DIRTY = true; renderTimeline(); msg("repè efase"); };
    ruler.appendChild(el);
  });
  const defs = tracksDef(), names = $("#names"), tracks = $("#tracks");
  names.innerHTML = ""; tracks.innerHTML = "";
  for (const def of defs) {
    const visual = ["scenes", "video", "image", "text"].indexOf(def.kind) >= 0;
    const audioT = ["voice", "music", "audio"].indexOf(def.kind) >= 0;
    const hidden = tState(def, "hidden"), muted = tState(def, "muted"), locked = tState(def, "locked");
    const trkH = def.height;
    const nm = document.createElement("div"); nm.className = "tname" + (def.key === TRACKSEL ? " sel" : "");
    nm.style.height = trkH + "px";
    nm.dataset.trackKey = def.key;
    if (def.track != null) nm.dataset.ti = def.track;
    nm.style.background = def.color + (def.key === TRACKSEL ? "33" : "16");
    nm.style.boxShadow = "inset 3px 0 0 " + def.color;
    nm.style.opacity = (hidden || muted) ? "0.5" : "1";

    const drag = document.createElement("span");
    drag.className = "tdrag";
    drag.innerHTML = svg("grip");
    drag.title = "Klike epi trennen pou deplase track sa a anlè oswa anba lòt track";
    nm.appendChild(drag);

    const dot = document.createElement("span"); dot.className = "dot"; dot.style.background = def.color; dot.style.cursor = "pointer"; dot.title = "Chanje koule track la";
    dot.onclick = ev => { ev.stopPropagation(); trackColorPopup(def); };
    const nmt = document.createElement("span"); nmt.className = "t";
    const nb = document.createElement("b"); nb.textContent = def.num || def.name; nmt.appendChild(nb);   // «Vwa 2»: toujou antye
    if (def.custom) { const ns = document.createElement("small"); ns.textContent = def.custom; nmt.appendChild(ns); }
    nmt.title = (def.label || def.name) + " — Double-klike pou chanje non • Klike pou chwazi track la";
    nmt.ondblclick = ev => { ev.stopPropagation(); renameTrack(def); };
    nm.appendChild(dot); nm.appendChild(nmt);
    const tdd = document.createElement("span"); tdd.className = "tdd tctl"; tdd.textContent = "▾"; tdd.title = "Meni aksyon pou track sa a";
    tdd.onclick = ev => { ev.stopPropagation(); const rc = tdd.getBoundingClientRect(); trackMenu(rc.left, rc.bottom + 4, def); };
    nm.appendChild(tdd);
    const ctl = (ic, ti2, onc, col) => { const sp = document.createElement("span"); sp.className = "tctl"; sp.innerHTML = svg(ic); sp.title = ti2; sp.style.cssText = "cursor:pointer;flex:none;display:flex;color:" + (col || "var(--dim)"); sp.onclick = ev => { ev.stopPropagation(); onc(); }; nm.appendChild(sp); };
    if (def.kind === "voice" || def.kind === "audio") {
      const recOn = RECORDING && ((def.kind === "voice" && RECTARGET && RECTARGET.scene != null) || (def.kind === "audio" && RECTARGET && RECTARGET.track === def.track));
      ctl("record", "Anrejistre vwa", () => { if (def.kind === "voice") recordSceneVoice(); else recordToTrack(def.track); }, recOn ? "#ff5470" : "var(--mov)");
    }
    if (visual) ctl(hidden ? "eyeoff" : "eye", hidden ? "Montre track la" : "Kache track la", () => tToggle(def, "hidden"), hidden ? "var(--amb)" : "var(--dim)");
    if (audioT) ctl(muted ? "mute" : "volume", muted ? "Retabli son" : "Koupe son (mute)", () => tToggle(def, "muted"), muted ? "var(--amb)" : "var(--dim)");
    if (audioT) {                                    // SOLO (T4): sèlman track solo yo jwe (lèt «S»)
      const solo = tState(def, "solo");
      const ss = document.createElement("span"); ss.className = "tctl"; ss.textContent = "S";
      ss.title = solo ? "Retire solo" : "Solo — sèlman track sa a (ak lòt solo yo) ap jwe";
      ss.style.cssText = "cursor:pointer;flex:none;display:flex;align-items:center;justify-content:center;width:16px;"
        + "font-weight:800;font-size:11px;color:" + (solo ? "var(--amb)" : "var(--dim)");
      ss.onclick = ev => { ev.stopPropagation(); tToggle(def, "solo"); };
      nm.appendChild(ss);
    }
    ctl(locked ? "lock" : "unlock", locked ? "Debloke" : "Bloke", () => tToggle(def, "locked"), locked ? "var(--amb)" : "var(--dim)");
    if (def.track != null && SPEC.tracks && SPEC.tracks[def.track]) {
      const syncLocked = SPEC.tracks[def.track].sync_lock !== false;
      ctl("link", syncLocked ? "Sync Lock aktif (pwoteje senkronizasyon)" : "Sync Lock dezaktive", () => {
        SPEC.tracks[def.track].sync_lock = !syncLocked; DIRTY = true; renderTimeline();
        msg(SPEC.tracks[def.track].sync_lock ? "Sync-lock aktive" : "Sync-lock dezaktive");
      }, syncLocked ? "var(--mov)" : "var(--dim)");
      const targeted = !!SPEC.tracks[def.track].targeted;
      ctl("target", targeted ? "Track sibli pou enpòtasyon (Targeted)" : "Sib track sa a (Target)", () => {
        SPEC.tracks.forEach(t => t.targeted = false);
        SPEC.tracks[def.track].targeted = !targeted; DIRTY = true; renderTimeline();
        msg(SPEC.tracks[def.track].targeted ? "Track sibli" : "Sib retire");
      }, targeted ? "#10b981" : "var(--dim)");
    }

    const resizer = document.createElement("div");
    resizer.className = "t-resizer";
    resizer.title = "Klike epi trennen souri a pou ouvri track la pi wo (stretch) oswa diminye l (double-klike pou reset)";
    nm.appendChild(resizer);

    const row = document.createElement("div"); row.className = "trow"; row.style.width = W + "px"; row.dataset.track = def.key;
    row.style.height = trkH + "px";
    row.style.background = def.color + (def.key === TRACKSEL ? "33" : "16");
    if (def.key === TRACKSEL) row.style.boxShadow = "inset 0 0 0 1px " + def.color + "88";

    const rResizer = document.createElement("div");
    rResizer.className = "t-resizer";
    rResizer.title = "Klike epi trennen souri a pou ouvri track la pi wo (stretch) oswa diminye l (double-klike pou reset)";
    row.appendChild(rResizer);

    wireTrackResizer(resizer, rResizer, def, nm, row);
    wireTrackDrag(nm, drag, def, row);
    nm.oncontextmenu = ev => { ev.preventDefault(); trackMenu(ev.clientX, ev.clientY, def); };
    names.appendChild(nm);
    if (def.key === "scenes") {
      if (!SPEC.scenes.length) {
        const ph = document.createElement("div");
        ph.className = "t-empty-hint";
        ph.style.cssText = "position:absolute;left:24px;top:50%;transform:translateY(-50%);color:#a78bfa;font-size:12px;font-weight:600;pointer-events:none;display:flex;align-items:center;gap:8px;opacity:0.85;";
        const tipTxt = (window.KadansI18n && window.KadansI18n.t("timeline_empty_hint")) || "Timeline vid — Trennen yon videyo/foto isit la oswa klike [+] nan katalòg la pou kòmanse";
        ph.innerHTML = '<span data-ico="plus"></span><span>' + esc(tipTxt) + '</span>';
        row.appendChild(ph);
        if (typeof paintIcons === "function") paintIcons(ph);
      } else {
        SPEC.scenes.forEach((sc, i) => row.appendChild(sceneBlock(sc, i, def.color)));
      }
      wireScenesDrop(row);
    } else if (def.key === "voice") {
      SPEC.scenes.forEach((sc, i) => {
        const vf = voiceUrlForScene(sc, i);
        if (sc.voice || sc.voice_file || vf) {
          row.appendChild(voiceBlock(sc, i, def.color));
        }
      });
    } else if (def.key === "music") {
      const mb = spanBlock(0, T, def.color, "Mizik: " + (SPEC.music.mood || SPEC.music.file || "file"));
      mb.style.cursor = "pointer";
      mb.title = "Klike pou regle volim mizik fon an nan panèl Son";
      mb.onclick = ev => {
        ev.stopPropagation();
        TRACKSEL = "music"; CLIPSEL = null; selRTab("sound"); renderTimeline();
        msg("Mizik fon chwazi — regle volim ak imè nan panèl Son");
      };
      row.appendChild(mb);
      const mf = (SPEC.music && SPEC.music.file) || (AUDIO_MAP && AUDIO_MAP.music) || "";
      if (mf) drawWave(mb, mf);
    } else if (def.track != null) {
      const tk = SPEC.tracks[def.track];
      (tk.clips || []).forEach((c, ci) => row.appendChild(clipBlock(def.track, ci, def.color)));
      dropTarget(row, def.track);
    }
    tracks.appendChild(row);
  }
  const fillH = Math.max(0, $("#tlscrollwrap").clientHeight - 22);
  tracks.style.minHeight = fillH + "px";
  tracks.style.backgroundImage = "repeating-linear-gradient(90deg, #ffffff14 0, #ffffff14 1px, transparent 1px, transparent " + (stepS * PPS) + "px), repeating-linear-gradient(0deg, #ffffff0e 0, #ffffff0e 1px, transparent 1px, transparent 40px)";
  inner.style.minHeight = $("#tlscrollwrap").clientHeight + "px";
  movePlayhead(); updateDur();
}
function sceneBlock(sc, i, color) {
  const b = document.createElement("div");
  b.className = "blk" + (i === SEL ? " sel" : "") + (ISSUES[i] ? " bad" : "");
  b.style.left = (sStart(i) * PPS) + "px"; b.style.width = Math.max(14, sDur(i) * PPS - 2) + "px";
  if (!ISSUES[i] && color) { b.style.background = "linear-gradient(180deg," + color + "," + color + "cc)"; b.style.borderColor = color; }
  b.innerHTML = '<span class="lab">' + (i + 1) + ". " + esc(sc.type) + " / " + esc(scName(sc)) + "</span><span class=\"hdl\"></span>";
  b.title = ISSUES[i] || (sc.type + " / " + sDur(i).toFixed(1) + "s (double-klike pou zoom sou sèn sa a)");
  (sc.marks || []).forEach(mk => { const k = document.createElement("span"); k.className = "kf"; k.style.left = Math.max(0, mk * PPS - 4) + "px"; b.appendChild(k); });
  b.ondblclick = ev => { ev.stopPropagation(); toggleZoomMedia(sStart(i), sDur(i), "scene_" + i); };
  b.oncontextmenu = ev => { ev.preventDefault(); selectScene(i); showCtxMenu(ev.clientX, ev.clientY, i); };
  dragBlock(b, i);
  return b;
}
function spanBlock(start, dur, color, label) {
  const b = document.createElement("div"); b.className = "blk";
  b.style.left = (start * PPS) + "px"; b.style.width = Math.max(10, dur * PPS - 2) + "px";
  b.style.background = "linear-gradient(180deg," + color + "," + color + "cc)"; b.style.borderColor = color; b.style.cursor = "default";
  b.innerHTML = '<span class="lab">' + esc(label) + "</span>";
  return b;
}
function movePlayhead() {
  const ph = $("#playhead"); ph.style.left = (CUR * PPS) + "px";
  ph.style.height = Math.max($("#tlinner").offsetHeight, $("#tlscrollwrap").clientHeight) + "px";
  updateProg();
}
function getStageBox() {
  const pv = $("#pv");
  const wrap = $("#pvwrap");
  if (!wrap) return null;
  const wrapRect = wrap.getBoundingClientRect();
  if (pv) {
    try {
      const doc = pv.contentDocument || (pv.contentWindow && pv.contentWindow.document);
      if (doc) {
        const st = doc.getElementById("stage");
        if (st) {
          const r = st.getBoundingClientRect();
          const pvr = pv.getBoundingClientRect();
          if (r.width > 10 && r.height > 10) {
            return {
              left: r.left * PVZOOM + (pvr.left - wrapRect.left),
              top: r.top * PVZOOM + (pvr.top - wrapRect.top),
              width: r.width * PVZOOM,
              height: r.height * PVZOOM,
              doc: doc
            };
          }
        }
      }
    } catch (e) {}
  }
  const kw = (KD && KD.w) || 1920, kh = (KD && KD.h) || 1080;
  const pw = wrap.clientWidth || 800, ph = Math.max(100, wrap.clientHeight || 500);
  const k = Math.min((pw - 20) / kw, (ph - 20) / kh) * PVZOOM;
  const sw = kw * k, sh = kh * k;
  return {
    left: (pw - sw) / 2 + PVPANX,
    top: Math.max(0, (ph - sh) / 2) + PVPANY,
    width: sw,
    height: sh,
    doc: null
  };
}
function curTarget() {
  if (OVSEL && SPEC.scenes && SPEC.scenes[OVSEL.s] && SPEC.scenes[OVSEL.s].overlays && SPEC.scenes[OVSEL.s].overlays[OVSEL.o]) {
    const o = SPEC.scenes[OVSEL.s].overlays[OVSEL.o];
    return {
      type: "overlay",
      item: o,
      label: o.src ? o.src.split("/").pop().slice(0, 18) : "kouch",
      w: o.w != null ? o.w : 0.3,
      x: o.x != null ? o.x : 0.5,
      y: o.y != null ? o.y : 0.5,
      isText: false
    };
  }
  if (CLIPSEL && SPEC.tracks && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) {
    const c = SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c];
    const k = c.kind || c.type || SPEC.tracks[CLIPSEL.t].kind;
    if (["image", "video", "text", "asset"].indexOf(k) >= 0) {
      return {
        type: "clip",
        item: c,
        label: (c.label || c.text || k).slice(0, 18),
        w: c.w != null ? c.w : (k === "text" ? 0.6 : 0.3),
        x: c.x != null ? c.x : 0.5,
        y: c.y != null ? c.y : 0.5,
        isText: k === "text"
      };
    }
  }
  return null;
}
function renderOvHandle() {
  const pv = $("#pvwrap"); let box = document.getElementById("ovbox");
  const tgt = curTarget();
  if (!tgt) { if (box) box.style.display = "none"; return; }
  if (!box) { box = document.createElement("div"); box.id = "ovbox"; box.innerHTML = '<div class="ovlab">eleman</div><div class="ovr"></div>'; pv.appendChild(box); wireOvBox(box); }
  const lab = box.querySelector(".ovlab"); if (lab) lab.textContent = tgt.label;
  box.style.display = "block";
  const stBox = getStageBox();
  if (!stBox || stBox.width <= 0) { box.style.display = "none"; return; }
  const W = stBox.width, Hh = stBox.height;
  const w = Math.max(24, Math.min(W, tgt.w * W));
  const h = tgt.isText ? Math.max(28, w * 0.35) : w;
  const left = stBox.left + tgt.x * W - w / 2;
  const top = stBox.top + tgt.y * Hh - h / 2;
  box.style.width = Math.round(w) + "px"; box.style.height = Math.round(h) + "px";
  box.style.left = Math.round(left) + "px"; box.style.top = Math.round(top) + "px";
}
function wireOvBox(box) {
  let bt = null;
  const commit = () => { DIRTY = true; clearTimeout(bt); bt = setTimeout(() => build(), 450); };
  box.addEventListener("mousedown", e => {
    if (e.target.classList.contains("ovr")) return;
    e.preventDefault(); const tgt = curTarget(); if (!tgt) return;
    const stBox = getStageBox(); if (!stBox || stBox.width <= 0) return;
    const W = stBox.width, Hh = stBox.height, x0 = e.clientX, y0 = e.clientY;
    const ox = tgt.x, oy = tgt.y;
    const mv = ev => { tgt.item.x = Math.max(0.02, Math.min(0.98, ox + (ev.clientX - x0) / W)); tgt.item.y = Math.max(0.02, Math.min(0.98, oy + (ev.clientY - y0) / Hh)); renderOvHandle(); if (CLIPSEL) renderRight(); };
    const up = () => { document.removeEventListener("mousemove", mv); document.removeEventListener("mouseup", up); commit(); };
    document.addEventListener("mousemove", mv); document.addEventListener("mouseup", up);
  });
  box.querySelector(".ovr").addEventListener("mousedown", e => {
    e.preventDefault(); e.stopPropagation(); const tgt = curTarget(); if (!tgt) return;
    const stBox = getStageBox(); if (!stBox || stBox.width <= 0) return;
    const W = stBox.width, x0 = e.clientX, ow = tgt.w;
    const mv = ev => { tgt.item.w = Math.max(0.05, Math.min(1.0, ow + (ev.clientX - x0) / W * 2)); renderOvHandle(); if (CLIPSEL) renderRight(); };
    const up = () => { document.removeEventListener("mousemove", mv); document.removeEventListener("mouseup", up); commit(); };
    document.addEventListener("mousemove", mv); document.addEventListener("mouseup", up);
  });
}

function updateProg() {
  const T = total() || 1, pct = Math.max(0, Math.min(1, CUR / T));
  const pf = $("#progfill"), ph = $("#proghead");
  if (pf) pf.style.width = (pct * 100).toFixed(2) + "%";
  if (ph) ph.style.left = (pct * 100).toFixed(2) + "%";
}
function seekProg(ev) {
  const r = $("#prog").getBoundingClientRect();
  let t = Math.max(0, Math.min(total(), (ev.clientX - r.left) / r.width * total()));
  stopAudio(); playing = false; setPlayIcon();
  CUR = t; movePlayhead(); updateProg(); $("#time").textContent = CUR.toFixed(1) + " / " + total().toFixed(1) + " s";
  post({ cmd: "seek", t: CUR });
}
function seekAt(ev) {
  const r = $("#tlinner").getBoundingClientRect();
  let t = Math.max(0, Math.min(total(), (ev.clientX - r.left) / PPS));
  if (SNAP) t = Math.round(t * 10) / 10;
  CUR = t; movePlayhead(); $("#time").textContent = CUR.toFixed(1) + " / " + total().toFixed(1) + " s";
  stopAudio(); playing = false; setPlayIcon(); post({ cmd: "seek", t: CUR });
}
// ---- T6: filmstrip thumbnail sou clip video (preview pi rapid — ou wè kontni an san scrub) ----
// Jenerasyon pares + cache; sèvi ak createImageBitmap (chemen WebCodecs) lè l disponib, sinon drawImage.
const _STRIP_CACHE = {};
const _HAS_BITMAP = (typeof createImageBitmap === "function");
function genFilmstrip(src, n) {
  return new Promise((resolve, reject) => {
    const v = document.createElement("video"); v.muted = true; v.preload = "auto"; v.crossOrigin = "anonymous"; v.playsInline = true;
    const TW = 80, TH = 46; const canvas = document.createElement("canvas"); const g = canvas.getContext("2d");
    let times = [], i = 0, done = false;
    const finish = ok => { if (done) return; done = true; try { v.removeAttribute("src"); v.load(); } catch (e) {} if (ok && i > 0) { try { resolve(canvas.toDataURL("image/jpeg", 0.6)); return; } catch (e) {} } reject(); };
    v.addEventListener("error", () => finish(false), { once: true });
    v.addEventListener("loadedmetadata", () => {
      const dur = v.duration || 0; if (!isFinite(dur) || dur <= 0) { finish(false); return; }
      const cnt = Math.max(1, Math.min(n, Math.round(dur / 1.2) || n));
      for (let k = 0; k < cnt; k++) times.push(dur * (k + 0.5) / cnt);
      canvas.width = TW * cnt; canvas.height = TH; seekNext();
    }, { once: true });
    function seekNext() { if (i >= times.length) { finish(true); return; } try { v.currentTime = times[i]; } catch (e) { finish(i > 0); } }
    v.addEventListener("seeked", async () => {
      try {
        if (_HAS_BITMAP) { const bm = await createImageBitmap(v); g.drawImage(bm, i * TW, 0, TW, TH); if (bm.close) bm.close(); }
        else { g.drawImage(v, i * TW, 0, TW, TH); }
      } catch (e) {}
      i++; seekNext();
    });
    v.src = src;
    setTimeout(() => finish(i > 0), 9000);                 // garde-fou: pa janm pann
  });
}
function drawFilmstrip(b, c, color) {
  const vsrc = c.src || (c.angles && c.angles[0] && c.angles[0].src);
  if (!vsrc) return;
  const set = url => { b.style.backgroundImage = "linear-gradient(180deg," + color + "66," + color + "aa), url(" + url + ")"; b.style.backgroundSize = "cover, cover"; b.style.backgroundPosition = "center"; };
  if (_STRIP_CACHE[vsrc]) { if (_STRIP_CACHE[vsrc] !== "x") set(_STRIP_CACHE[vsrc]); return; }
  genFilmstrip(withTok(vsrc), 5).then(url => { if (url) { _STRIP_CACHE[vsrc] = url; set(url); } else { _STRIP_CACHE[vsrc] = "x"; } }).catch(() => { _STRIP_CACHE[vsrc] = "x"; });
}
async function drawWave(el, src) {
  if (!src) return;
  try {
    const r = await api("GET", "/api/peaks?file=" + encodeURIComponent(src));
    const pk = (r.body && r.body.peaks) || []; if (!pk.length) return;
    const mx = Math.max.apply(null, pk) || 1, n = pk.length, W = 100, H = 30;
    let top = "", bot = "";
    for (let i = 0; i < n; i++) { const x = (i / (n - 1)) * W, a = (pk[i] / mx) * (H / 2 - 1); top += (i ? "L" : "M") + x.toFixed(2) + "," + (H / 2 - a).toFixed(2) + " "; }
    for (let i = n - 1; i >= 0; i--) { const x = (i / (n - 1)) * W, a = (pk[i] / mx) * (H / 2 - 1); bot += "L" + x.toFixed(2) + "," + (H / 2 + a).toFixed(2) + " "; }
    const wrap = document.createElement("div"); wrap.className = "wave";
    wrap.innerHTML = '<svg width="100%" height="100%" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none"><path d="' + top + bot + 'Z" fill="#ffffff" opacity="0.5"/></svg>';
    el.insertBefore(wrap, el.firstChild);
  } catch (e) {}
}
function setZoom(p) { PPS = Math.max(8, Math.min(400, p)); renderTimeline(); }
function fit() { const w = $("#tlscrollwrap").clientWidth - 24; setZoom(w / Math.max(0.5, total())); }
let LAST_ZOOM_CLIP = null;
function toggleZoomMedia(start, dur, id) {
  if (LAST_ZOOM_CLIP === id) {
    fit();
    LAST_ZOOM_CLIP = null;
    msg("↔️ Dezoume tout timeline lan (Fit)");
  } else {
    zoomToMedia(start, dur);
    LAST_ZOOM_CLIP = id;
  }
}
function zoomToMedia(start, dur) {
  const wrap = $("#tlscrollwrap");
  const vw = (wrap && wrap.clientWidth ? wrap.clientWidth : 600) - 50;
  const targetPPS = Math.max(12, Math.min(500, vw / Math.max(0.12, dur)));
  PPS = targetPPS;
  renderTimeline();
  if (wrap) wrap.scrollLeft = Math.max(0, start * PPS - 25);
  msg("🔍 Zoom sou medya (" + dur.toFixed(1) + "s) — Double-klike ankò oswa peze 'Fit' pou dezoume");
}

// ---- Istorik (undo/redo) ----
let HIST = [], HIDX = -1;
const HIST_MAX = 100;                 // bòne memwa (lejè): kenbe dènye 100 eta yo
// Undo KONPLÈ: sove TOUT spec la (sèn, track, clip, mizik, vwa, koulè, soutit, ratio, lang…), pa sèlman scenes+tracks.
function snapshot() {
  HIST = HIST.slice(0, HIDX + 1);
  HIST.push(JSON.stringify(SPEC));
  if (HIST.length > HIST_MAX) HIST = HIST.slice(HIST.length - HIST_MAX);
  HIDX = HIST.length - 1;
}
function restore(k) {
  if (!HIST[k]) return;
  const s = JSON.parse(HIST[k]);
  for (const key in SPEC) delete SPEC[key];   // kenbe MENM objè SPEC la (lòt kòd kenbe referans li), ranplase kontni
  Object.assign(SPEC, s);
  HIDX = k; DIRTY = true;
  renderTimeline(); renderRight(); renderLeft();
}

// ---- Glise = reodone, bo dwat = chanje dire. KENBE epi pa retounen. ----
function dragBlock(b, i) {
  const hdl = b.querySelector(".hdl");
  hdl.addEventListener("mousedown", ev => {
    ev.stopPropagation(); ev.preventDefault(); if (trackLockedByKey("scenes")) return;
    const x0 = ev.clientX, w0 = b.offsetWidth;
    const mv = e => { b.style.width = Math.max(14, w0 + (e.clientX - x0)) + "px"; };
    const up = () => {
      document.removeEventListener("mousemove", mv); document.removeEventListener("mouseup", up);
      let d = (b.offsetWidth + 2) / PPS; if (SNAP) d = Math.round(d * 10) / 10;
      snapshot(); SPEC.scenes[i].duration = Math.max(0.3, d); DIRTY = true;
      renderTimeline(); renderRight(); renderLeft();
    };
    document.addEventListener("mousemove", mv); document.addEventListener("mouseup", up);
  });
  b.addEventListener("mousedown", ev => {
    if (ev.target === hdl) return;
    ev.stopPropagation();
    const x0 = ev.clientX, l0 = b.offsetLeft; let moved = false;
    const mv = e => {
      if (trackLockedByKey("scenes")) return;
      if (!moved && Math.abs(e.clientX - x0) > 4) { moved = true; b.style.cursor = "grabbing"; b.style.zIndex = 9; }
      if (moved) b.style.left = Math.max(0, l0 + (e.clientX - x0)) + "px";
    };
    const up = () => {
      document.removeEventListener("mousemove", mv); document.removeEventListener("mouseup", up);
      if (!moved) { if (TOOL === "split") splitAt(i); else selectScene(i); return; }
      const center = b.offsetLeft + b.offsetWidth / 2;
      const order = SPEC.scenes.map((s, k) => k).filter(k => k !== i);
      let j = 0, acc = 0;
      for (const k of order) { const w = sDur(k) * PPS; if (center > acc + w / 2) { j++; acc += w; } else break; }
      if (j !== i) { snapshot(); const s = SPEC.scenes.splice(i, 1)[0]; SPEC.scenes.splice(j, 0, s); DIRTY = true; SEL = j; }
      renderTimeline(); renderRight(); renderLeft();
    };
    document.addEventListener("mousemove", mv); document.addEventListener("mouseup", up);
  });
}
function selectScene(i) {
  SEL = i; CLIPSEL = null; renderTimeline(); renderRight();
  const sc = SPEC.scenes[i]; if (!sc) return;
  const wasPlaying = playing;
  stopAudio();
  CUR = sStart(i) + Math.min(0.4, Math.max(0.02, (sc.dur || 2) * 0.2));
  movePlayhead(); post({ cmd: "seek", t: CUR }); post({ cmd: "highlight", scene: sc.id || "" });
  $("#selinfo").textContent = (i + 1) + ". " + sc.type + (sc.voice ? " / vwa" : "");
  if (sc.overlays && sc.overlays.length) {
    const firstSmaller = sc.overlays.findIndex(o => (o.w == null || o.w < 0.85) && o.layer !== "back");
    OVSEL = firstSmaller >= 0 ? { s: i, o: firstSmaller } : null;
  } else {
    OVSEL = null;
  }
  setTimeout(renderOvHandle, 60);
  if (wasPlaying) playAudio();
}

// ---- Clip sou track itilizate (draggable, redimansyonab, deplase ant track) ----
function clipBlock(ti, ci, color) {
  const tk = SPEC.tracks[ti], c = tk.clips[ci];
  const b = document.createElement("div");
  b.className = "blk" + (CLIPSEL && CLIPSEL.t === ti && CLIPSEL.c === ci ? " sel" : "");
  b.style.left = ((c.start || 0) * PPS) + "px"; b.style.width = Math.max(14, (c.dur || 2) * PPS - 2) + "px";
  b.style.background = "linear-gradient(180deg," + color + "," + color + "cc)"; b.style.borderColor = color;
  b.innerHTML = '<span class="hdll"></span><span class="lab">' + esc(c.label || c.type || "clip") + '</span><span class="hdl"></span>';
  b.title = (c.label || c.kind || "clip") + " / " + (c.dur || 2).toFixed(1) + "s (double-klike pou zoom sou clip sa a)";
  b.ondblclick = ev => { ev.stopPropagation(); toggleZoomMedia(c.start || 0, c.dur || 2, "clip_" + ti + "_" + ci); };
  const _isAudio = c.src && /\.(wav|mp3|m4a|aac|ogg|opus|flac)$/i.test(c.src);
  if (_isAudio) drawWave(b, c.src);
  else if ((c.src && /\.(mp4|webm|mov|m4v|mkv)$/i.test(c.src)) || (c.angles && c.angles.length)) drawFilmstrip(b, c, color);
  const hdl = b.querySelector(".hdl"), hdll = b.querySelector(".hdll");
  const clocked0 = () => !!(SPEC.tracks[ti] && SPEC.tracks[ti].locked);
  hdll.addEventListener("mousedown", ev => {
    ev.stopPropagation(); ev.preventDefault(); if (clocked0()) return; snapshot();
    const x0 = ev.clientX, s0 = c.start || 0, right = s0 + (c.dur || 2);
    // KOUPE KÒMANSMAN AN: «in» (kote son / videyo a kòmanse nan fichye a) swiv rebò a — anvan li pa t chanje,
    // epi son an te «tounen nan plas li» (li te rekòmanse fichye a nan 0 s). Pa ka rale pi lwen pase kòmansman fichye a.
    const isMedia = !!c.src, in0 = +(c.in || 0), sp = +(c.speed || 1), minS = isMedia ? Math.max(0, s0 - in0 / sp) : 0;
    const mv = e => { let ns = Math.max(minS, Math.min(right - 0.3, s0 + (e.clientX - x0) / PPS)); if (SNAP) ns = Math.max(minS, Math.round(ns * 10) / 10); c.start = ns; c.dur = right - ns; if (isMedia) c.in = Math.max(0, Math.round((in0 + (ns - s0) * sp) * 1000) / 1000); b.style.left = (ns * PPS) + "px"; b.style.width = Math.max(14, c.dur * PPS - 2) + "px"; };
    const up = () => { document.removeEventListener("mousemove", mv); document.removeEventListener("mouseup", up); DIRTY = true; renderTimeline(); renderRight(); };
    document.addEventListener("mousemove", mv); document.addEventListener("mouseup", up);
  });
  const clocked = () => !!(SPEC.tracks[ti] && SPEC.tracks[ti].locked);
  hdl.addEventListener("mousedown", ev => {
    ev.stopPropagation(); ev.preventDefault(); if (clocked()) return; const x0 = ev.clientX, w0 = b.offsetWidth;
    const mv = e => { b.style.width = Math.max(14, w0 + (e.clientX - x0)) + "px"; };
    const up = () => { document.removeEventListener("mousemove", mv); document.removeEventListener("mouseup", up); let d = (b.offsetWidth + 2) / PPS; if (SNAP) d = Math.round(d * 10) / 10; snapshot(); c.dur = Math.max(0.3, d); DIRTY = true; renderTimeline(); renderRight(); };
    document.addEventListener("mousemove", mv); document.addEventListener("mouseup", up);
  });
  b.addEventListener("mousedown", ev => {
    if (ev.target === hdl || ev.target === hdll) return; ev.stopPropagation();
    const x0 = ev.clientX, l0 = b.offsetLeft; let moved = false;
    const mv = e => {
      if (clocked()) return;
      if (!moved && Math.abs(e.clientX - x0) > 4) { moved = true; b.style.cursor = "grabbing"; b.style.zIndex = 9; }
      if (moved) {
        let curLeft = Math.max(0, l0 + (e.clientX - x0));
        let curT = curLeft / PPS;
        // Magnétisme entèlijan (Snap): rale sou CUR oswa rebò lòt clips si li toupre (distans 0.12s)
        if (SNAP) {
          const snapTargets = [CUR];
          SPEC.scenes.forEach((sc, si) => { snapTargets.push(sStart(si)); snapTargets.push(sStart(si) + sDur(si)); });
          (tk.clips || []).forEach((other, oi) => {
            if (oi !== ci) {
              const ost = other.start || 0, oet = ost + (other.dur || 2);
              snapTargets.push(ost); snapTargets.push(oet);
            }
          });
          const cDur = c.dur || 2;
          for (const tgt of snapTargets) {
            if (Math.abs(curT - tgt) < 0.12) { curT = tgt; curLeft = tgt * PPS; break; }
            if (Math.abs((curT + cDur) - tgt) < 0.12) { curT = tgt - cDur; curLeft = Math.max(0, curT * PPS); break; }
          }
        }
        b.style.left = curLeft + "px";
        // Alèt vizyèl si li an kolizyon / chevocheman ak yon lòt clip sou menm track la
        const willEnd = curT + (c.dur || 2);
        const collides = (tk.clips || []).some((other, oi) => oi !== ci && ((other.start || 0) < willEnd - 0.05 && ((other.start || 0) + (other.dur || 2)) > curT + 0.05));
        b.style.boxShadow = collides ? "0 0 0 2px #f59e0b, 0 4px 12px rgba(245,158,11,0.4)" : "";
      }
    };
    const up = e => {
      document.removeEventListener("mousemove", mv); document.removeEventListener("mouseup", up);
      b.style.boxShadow = "";
      if (!moved) { selectClip(ti, ci); return; }
      let ns = Math.max(0, b.offsetLeft / PPS); if (SNAP) ns = Math.round(ns * 10) / 10;
      const rows = Array.from(document.querySelectorAll("#tracks .trow"));
      const tr = rows.find(r => { const rc = r.getBoundingClientRect(); return e.clientY >= rc.top && e.clientY <= rc.bottom; });
      let newTi = ti;
      if (tr && tr.dataset.track && tr.dataset.track.indexOf("tk") === 0) newTi = +tr.dataset.track.slice(2);
      snapshot();
      if (newTi !== ti) {
        const dst = SPEC.tracks[newTi];
        if (!kindOk(c.kind || mediaKind(c.src, c.type), dst.kind)) { msg("yon " + (c.kind || "medya") + " pa ka ale sou track " + dst.kind); renderTimeline(); return; }
        tk.clips.splice(ci, 1); dst.clips = dst.clips || []; c.start = ns; dst.clips.push(c); CLIPSEL = { t: newTi, c: dst.clips.length - 1 };
      } else { c.start = ns; }
      DIRTY = true; renderTimeline(); renderRight(); renderLeft();
    };
    document.addEventListener("mousemove", mv); document.addEventListener("mouseup", up);
  });
  b.oncontextmenu = ev => { ev.preventDefault(); selectClip(ti, ci); clipMenu(ev.clientX, ev.clientY, ti, ci); };
  return b;
}
function selectClip(ti, ci) {
  CLIPSEL = { t: ti, c: ci }; SEL = -1; TRACKSEL = "tk" + ti; OVSEL = null;
  const c = SPEC.tracks[ti].clips[ci]; renderTimeline();
  const k = c.kind || (typeof mediaKind === "function" ? mediaKind(c.src || "", c.type) : "");
  if (k === "audio" || k === "sfx" || k === "music" || k === "voice") selRTab("sound");
  else selRTab("props");
  const wasPlaying = playing;
  stopAudio();
  CUR = c.start || 0; movePlayhead(); post({ cmd: "seek", t: CUR }); $("#selinfo").textContent = "clip: " + (c.label || c.kind || "");
  setTimeout(renderOvHandle, 60);
  if (wasPlaying) playAudio();
}
function clipMenu(x, y, ti, ci) {
  const old = document.getElementById("ctxmenu"); if (old) old.remove();
  const m = document.createElement("div"); m.id = "ctxmenu"; m.className = "menu"; m.style.cssText = "display:block;position:fixed;left:" + x + "px;top:" + y + "px;z-index:200;min-width:180px";
  const c = SPEC.tracks[ti].clips[ci];
  const items = [
    ["zoomin", "Zoom sou clip sa a", () => toggleZoomMedia(c.start || 0, c.dur || 2, "clip_" + ti + "_" + ci)],
    ["fit", "Dezoume tout timeline", () => fit()],
    ["copy", "Kopye clip", () => { CLIP = { __clip: JSON.parse(JSON.stringify(SPEC.tracks[ti].clips[ci])) }; msg("clip kopye"); }],
    ["copy", "Kopye atribi...", () => copyClipAttributes(ti, ci)],
    ["plus", "Kole atribi...", () => pasteClipAttributes(ti, ci)],
    ["scissors", "Fèmen twou (Close Gap)", () => closeTrackGap(ti, ci)],
    ["trash", "Efase clip", () => { snapshot(); SPEC.tracks[ti].clips.splice(ci, 1); CLIPSEL = null; DIRTY = true; renderTimeline(); renderRight(); renderLeft(); }]
  ];
  items.forEach(it => { const d = document.createElement("div"); d.className = "mi"; d.innerHTML = svg(it[0]) + it[1]; d.onclick = () => { m.remove(); it[2](); }; m.appendChild(d); });
  document.body.appendChild(m);
  const r = m.getBoundingClientRect(); if (r.right > window.innerWidth) m.style.left = (window.innerWidth - r.width - 6) + "px"; if (r.bottom > window.innerHeight) m.style.top = (window.innerHeight - r.height - 6) + "px";
}

// ---- Meni klik-dwat sou clip (pwofesyonel: split/copy/cut/paste/double/efase) ----
let CLIP = null;
function showCtxMenu(x, y, i) {
  const old = document.getElementById("ctxmenu"); if (old) old.remove();
  const m = document.createElement("div"); m.id = "ctxmenu"; m.className = "menu";
  m.style.cssText = "display:block;position:fixed;left:" + x + "px;top:" + y + "px;z-index:200;min-width:210px";
  const dup = () => { snapshot(); const c = JSON.parse(JSON.stringify(SPEC.scenes[i])); c.id = (c.id || "s") + "_" + Math.random().toString(36).slice(2, 5); SPEC.scenes.splice(i + 1, 0, c); DIRTY = true; SEL = i + 1; renderTimeline(); renderRight(); renderLeft(); };
  const paste = () => { if (!CLIP) { msg("pa gen anyen kopye"); return; } snapshot(); const c = JSON.parse(JSON.stringify(CLIP)); c.id = (c.id || "s") + "_" + Math.random().toString(36).slice(2, 5); SPEC.scenes.splice(i + 1, 0, c); DIRTY = true; SEL = i + 1; renderTimeline(); renderRight(); renderLeft(); msg("kole"); };
  const items = [
    ["zoomin", "Zoom sou sèn sa a", "Dbl-Click", () => toggleZoomMedia(sStart(i), sDur(i), "scene_" + i)],
    ["fit", "Dezoume tout timeline", "", () => fit()],
    ["scissors", "Koupe (split)", "B", () => splitAt(i)],
    ["copy", "Kopye", "Ctrl+C", () => { CLIP = JSON.parse(JSON.stringify(SPEC.scenes[i])); msg("kopye"); }],
    ["scissors", "Koupe-deplase (cut)", "Ctrl+X", () => { CLIP = JSON.parse(JSON.stringify(SPEC.scenes[i])); delScene(); }],
    ["plus", "Kole apre", "Ctrl+V", paste],
    ["layers", "Double (duplicate)", "Ctrl+D", dup],
    ["diamond", "Mete keyframe", "M", () => { SEL = i; addKeyframe(); }],
    ["mic", "Vwa ON/OFF", "", () => { const sc = SPEC.scenes[i]; snapshot(); if (sc.voice) { sc._voicebak = sc.voice; delete sc.voice; } else if (sc._voicebak) { sc.voice = sc._voicebak; delete sc._voicebak; } DIRTY = true; renderTimeline(); renderRight(); }],
    ["trash", "Efase", "Del", () => { SEL = i; delScene(); }]
  ];
  items.forEach(it => { const d = document.createElement("div"); d.className = "mi"; d.innerHTML = svg(it[0]) + '<span style="flex:1">' + it[1] + '</span><span class="k">' + it[2] + "</span>"; d.onclick = () => { m.remove(); it[3](); }; m.appendChild(d); });
  document.body.appendChild(m);
  const r = m.getBoundingClientRect();
  if (r.right > window.innerWidth) m.style.left = (window.innerWidth - r.width - 6) + "px";
  if (r.bottom > window.innerHeight) m.style.top = (window.innerHeight - r.height - 6) + "px";
}

// ---- Track: koule (popup), rename, meni ----
function setTrackColor(def, c) {
  if (def.track != null && SPEC.tracks[def.track]) { SPEC.tracks[def.track].color = c; DIRTY = true; }
  else { try { localStorage.setItem("kdtc_" + def.key, c); } catch (x) {} }
  renderTimeline();
}
function trackColorPopup(def) {
  const old = document.getElementById("tcpop"); if (old) old.remove();
  const back = document.createElement("div"); back.id = "tcpop";
  back.style.cssText = "position:fixed;inset:0;background:#0007;z-index:120;display:flex;align-items:center;justify-content:center";
  const box = document.createElement("div"); box.style.cssText = "background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;width:300px;box-shadow:0 12px 40px #000c";
  box.innerHTML = '<h3 style="color:var(--mov);margin:0 0 8px;font-size:13px">Koule track: ' + esc(def.name) + '</h3>';
  const sw = document.createElement("div"); sw.className = "swatches";
  PALETTE.forEach(c => { const s = document.createElement("div"); s.className = "sw"; s.style.background = c; s.title = c; s.onclick = () => { setTrackColor(def, c); back.remove(); }; sw.appendChild(s); });
  box.appendChild(sw);
  const row = document.createElement("div"); row.style.cssText = "display:flex;gap:6px;margin-top:10px;align-items:center";
  const pick = document.createElement("input"); pick.type = "color"; pick.value = /^#[0-9a-f]{6}$/i.test(def.color) ? def.color : "#8b5cf6"; pick.style.cssText = "width:40px;height:32px;padding:0";
  pick.oninput = () => setTrackColor(def, pick.value);
  const cl = document.createElement("button"); cl.textContent = "Fèmen"; cl.style.flex = "1"; cl.onclick = () => back.remove();
  row.appendChild(pick); row.appendChild(cl); box.appendChild(row);
  back.appendChild(box); document.body.appendChild(back);
  back.onclick = e => { if (e.target === back) back.remove(); };
}
function renameTrack(def) {
  const nn = prompt("Nouvo non track la:", def.name);
  if (nn == null) return;
  if (def.track != null && SPEC.tracks[def.track]) { SPEC.tracks[def.track].name = nn; DIRTY = true; }
  else { try { localStorage.setItem("kdtn_" + def.key, nn); } catch (x) {} }
  renderTimeline();
}
function deleteTrack(def) {
  if (def.track == null) { msg("ou ka efase sèlman track ou ajoute"); return; }
  if (!confirm("Èske ou sèten ou vle efase track sa a nèt ak tout clips li yo?")) return;
  snapshot(); SPEC.tracks.splice(def.track, 1); DIRTY = true; renderTimeline(); renderLeft(); msg("track efase");
}
function moveTrack(ti, dir) {
  const j = ti + dir; if (ti == null || j < 0 || j >= (SPEC.tracks || []).length) return;
  snapshot(); const tmp = SPEC.tracks[ti]; SPEC.tracks[ti] = SPEC.tracks[j]; SPEC.tracks[j] = tmp; DIRTY = true; renderTimeline(); msg("track deplase");
}
function timelineMenu(x, y) {
  const old = document.getElementById("ctxmenu"); if (old) old.remove();
  const m = document.createElement("div"); m.id = "ctxmenu"; m.className = "menu"; m.style.cssText = "display:block;position:fixed;left:" + x + "px;top:" + y + "px;z-index:200;min-width:190px";
  const items = [["film", "Ajoute Track Video", () => addTrack("video")], ["music", "Ajoute Track Audio", () => addTrack("audio")], ["image", "Ajoute Track Imaj", () => addTrack("image")], ["text", "Ajoute Track Teks", () => addTrack("text")], ["layers", "Ajoute Track Asset", () => addTrack("asset")], ["plus", "Ajoute yon sen (katalog)", () => selTab("cat")], ["diamond", "Mete keyframe", () => addKeyframe()], ["fit", "Ajiste zoom", () => fit()]];
  if (CLIP) items.splice(6, 0, ["copy", "Kole", () => pasteAfter(SEL)]);
  items.forEach(it => { const d = document.createElement("div"); d.className = "mi"; d.innerHTML = svg(it[0]) + it[1]; d.onclick = () => { m.remove(); it[2](); }; m.appendChild(d); });
  document.body.appendChild(m);
  const r = m.getBoundingClientRect(); if (r.right > window.innerWidth) m.style.left = (window.innerWidth - r.width - 6) + "px"; if (r.bottom > window.innerHeight) m.style.top = (window.innerHeight - r.height - 6) + "px";
}
function promptAddClipToTrack(ti) {
  if (ti == null || !SPEC.tracks || !SPEC.tracks[ti]) return;
  const tk = SPEC.tracks[ti];
  if (tk.kind === "text") {
    const txt = prompt("Tèks pou mete sou track '" + (tk.name || tk.kind) + "':", "Nouvo Tèks");
    if (!txt) return;
    snapshot(); tk.clips = tk.clips || [];
    const st = freeStart(tk, CUR, 3);
    tk.clips.push({ type: "text", kind: "text", text: txt, label: txt, start: st, dur: 3, x: 0.5, y: 0.5, w: 0.5, color: "#ffffff" });
    DIRTY = true; CLIPSEL = { t: ti, c: tk.clips.length - 1 }; TRACKSEL = "tk" + ti;
    renderTimeline(); renderRight(); build(); msg("Tèks ajoute sou " + (tk.name || tk.kind));
    return;
  }
  const fi = document.createElement("input");
  fi.type = "file";
  if (tk.kind === "audio" || tk.kind === "sfx") fi.accept = "audio/*,video/*";
  else if (tk.kind === "video") fi.accept = "video/*,image/*";
  else fi.accept = "image/*,video/*,audio/*";
  fi.onchange = async () => {
    if (!fi.files || !fi.files.length) return;
    await importMedia(fi.files);
    if (window.IMPORTED && window.IMPORTED.length) {
      const m = window.IMPORTED[0];
      await dropAssetOnTrack(m.rel, ti, CUR, mediaKind(m.rel, tk.kind));
      build();
    }
  };
  fi.click();
}
function trackMenu(x, y, def) {
  const old = document.getElementById("ctxmenu"); if (old) old.remove();
  const m = document.createElement("div"); m.id = "ctxmenu"; m.className = "menu"; m.style.cssText = "display:block;position:fixed;left:" + x + "px;top:" + y + "px;z-index:99996;min-width:215px";
  const items = [];
  if (def.key === "scenes") {
    items.push(["plus", "Ajoute sèn @ kisè a", () => addScene("hook")]);
    items.push(["text", "Ajoute sèn tèks @ kisè a", () => addScene("text")]);
    items.push(["trash", "Retire tout sèn yo (Mòd Tracks Nòmal)", () => {
      if (confirm("Èske ou vle retire tout sèn yo pou travay sèlman ak tracks nòmal (san sèn)?")) {
        snapshot();
        SPEC.scenes = [];
        DIRTY = true;
        renderTimeline();
        renderRight();
        build();
        msg("Tout sèn yo retire — Mòd Tracks nòmal aktif");
      }
    }]);
  } else if (def.track != null) {
    items.push(["plus", "Ajoute " + (def.kind === "text" ? "Tèks" : "Medya / Clip") + " sou track sa a", () => promptAddClipToTrack(def.track)]);
    if (def.kind !== "audio" && def.kind !== "sfx") {
      items.push(["text", "Ajoute Tèks sou track sa a", () => {
        const tk = SPEC.tracks[def.track]; if (!tk) return;
        const txt = prompt("Tèks pou mete sou track la:", "Nouvo Tèks");
        if (!txt) return;
        snapshot(); tk.clips = tk.clips || [];
        const st = freeStart(tk, CUR, 3);
        tk.clips.push({ type: "text", kind: "text", text: txt, label: txt, start: st, dur: 3, x: 0.5, y: 0.5, w: 0.5, color: "#ffffff" });
        DIRTY = true; CLIPSEL = { t: def.track, c: tk.clips.length - 1 };
        renderTimeline(); renderRight(); build();
      }]);
    }
  }
  items.push(["text", "Chanje non track la", () => renameTrack(def)]);
  items.push(["palette", "Chanje koulè track la", () => trackColorPopup(def)]);
  if (def.kind === "voice") items.push(["record", "Anrejistre vwa", () => recordSceneVoice()]);
  if (def.kind === "audio") items.push(["record", "Anrejistre vwa", () => recordToTrack(def.track)]);
  if (def.track != null) { items.push(["caretup", "Monte track", () => moveTrack(def.track, -1)]); items.push(["caret", "Desann track", () => moveTrack(def.track, 1)]); items.push(["trash", "Efase track", () => deleteTrack(def)]); }
  items.forEach(it => { const d = document.createElement("div"); d.className = "mi"; d.innerHTML = svg(it[0]) + it[1]; d.onclick = () => { m.remove(); it[2](); }; m.appendChild(d); });
  document.body.appendChild(m);
  const r = m.getBoundingClientRect();
  if (r.right > window.innerWidth) m.style.left = (window.innerWidth - r.width - 6) + "px";
  if (r.bottom > window.innerHeight) m.style.top = (window.innerHeight - r.height - 6) + "px";
}

// ---- PANEL GOCH ----
const CATALOG = ["hook", "text", "logo", "features", "list", "stat", "code", "compare", "cta", "video", "image", "chart", "social", "html"];
let CODEVIEW = "html";
const L_TITLES = { media: "Medya", assets: "Asset", cat: "Katalog", sfx: "SFX (Efè son)", comp: "Konpozisyon", code: "Kòd (Spec JSON)" };

const SFX_PRESETS = [
  { id: "whoosh", name: "Whoosh Tranzisyon", desc: "Mouvman rapid lis", dur: 0.5, icon: "volume" },
  { id: "pop", name: "Pop Aparisyon", desc: "Aparisyon dinamik de eleman", dur: 0.3, icon: "sparkles" },
  { id: "hit", name: "Hit Enpak", desc: "Gwo frape ak bass", dur: 0.9, icon: "volume" },
  { id: "chime", name: "Chime Siksè", desc: "Klòch klere pou siksè", dur: 1.2, icon: "sparkles" },
  { id: "swoosh", name: "Swoosh Flèch", desc: "Kout van rapid", dur: 0.4, icon: "volume" },
  { id: "ding", name: "Ding Notifikasyon", desc: "Son klòch kout", dur: 0.6, icon: "volume" },
  { id: "riser", name: "Riser Tansyon", desc: "Monte tansyon anvan gout la", dur: 2.0, icon: "volume" },
  { id: "glitch", name: "Glitch Dijital", desc: "Erè vizyèl / dijital", dur: 0.4, icon: "code" },
  { id: "click", name: "Klike Bouton", desc: "Son klike sourit oswa switch", dur: 0.15, icon: "pointer" },
  { id: "applause", name: "Bat Bravo", desc: "Felisitasyon / cheering", dur: 2.5, icon: "volume" }
];

function playSfxSynth(id) {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    if (!window._sfxCtx || window._sfxCtx.state === "closed") {
      window._sfxCtx = new AudioCtx();
    }
    const ctx = window._sfxCtx;
    if (ctx.state === "suspended") ctx.resume().catch(() => {});
    const now = ctx.currentTime;
    if (id === "whoosh" || id === "swoosh") {
      const buf = ctx.createBuffer(1, Math.round(ctx.sampleRate * 0.5), ctx.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < buf.length; i++) data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (buf.length * 0.3));
      const src = ctx.createBufferSource(); src.buffer = buf;
      const filt = ctx.createBiquadFilter(); filt.type = "bandpass";
      filt.frequency.setValueAtTime(300, now); filt.frequency.exponentialRampToValueAtTime(2500, now + 0.25);
      filt.frequency.exponentialRampToValueAtTime(400, now + 0.45);
      src.connect(filt); filt.connect(ctx.destination);
      src.start(now);
    } else if (id === "pop") {
      const osc = ctx.createOscillator(); const gain = ctx.createGain();
      osc.type = "sine"; osc.frequency.setValueAtTime(520, now);
      osc.frequency.exponentialRampToValueAtTime(1400, now + 0.05);
      osc.frequency.exponentialRampToValueAtTime(200, now + 0.25);
      gain.gain.setValueAtTime(0.6, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(now); osc.stop(now + 0.26);
    } else if (id === "hit") {
      const osc = ctx.createOscillator(); const gain = ctx.createGain();
      osc.type = "triangle"; osc.frequency.setValueAtTime(150, now);
      osc.frequency.exponentialRampToValueAtTime(35, now + 0.6);
      gain.gain.setValueAtTime(0.9, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.7);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(now); osc.stop(now + 0.71);
    } else if (id === "chime" || id === "ding") {
      [880, 1320, 1760].forEach((freq, idx) => {
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.type = "sine"; osc.frequency.setValueAtTime(freq, now + idx * 0.04);
        gain.gain.setValueAtTime(0.35, now + idx * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.04 + 0.8);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(now + idx * 0.04); osc.stop(now + idx * 0.04 + 0.85);
      });
    } else if (id === "click") {
      const osc = ctx.createOscillator(); const gain = ctx.createGain();
      osc.type = "square"; osc.frequency.setValueAtTime(1200, now);
      gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.05);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(now); osc.stop(now + 0.06);
    } else {
      const osc = ctx.createOscillator(); const gain = ctx.createGain();
      osc.type = "sine"; osc.frequency.setValueAtTime(440, now);
      gain.gain.setValueAtTime(0.4, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(now); osc.stop(now + 0.45);
    }
  } catch (err) {}
}

function addSfxClip(p) {
  snapshot();
  const ti = ensureTrack("sfx");
  const tk = SPEC.tracks[ti];
  tk.clips = tk.clips || [];
  const st = freeStart(tk, CUR, p.dur);
  tk.clips.push({ kind: "sfx", sfx: p.id, label: p.name, start: st, dur: p.dur });
  DIRTY = true; CLIPSEL = { t: ti, c: tk.clips.length - 1 };
  renderTimeline(); renderRight();
  msg("SFX '" + p.name + "' ajoute sou track @ " + st.toFixed(1) + "s");
}

let L_OPEN = true, LAST_L_WIDTH = 335;
function toggleLeft(forceState) {
  const left = $("#left"), lpanel = $("#lpanel"), splitL = $("#splitL");
  if (!left || !lpanel) return;
  const shouldOpen = (forceState !== undefined) ? !!forceState : !L_OPEN;
  if (shouldOpen) {
    L_OPEN = true;
    lpanel.style.display = "flex";
    left.style.width = Math.max(160, LAST_L_WIDTH || 335) + "px";
    if (splitL) splitL.style.display = "";
    document.querySelectorAll("#lrail .rail-btn").forEach(b => b.classList.toggle("on", b.dataset.lt === LT));
    const tEl = $("#ltitle"); if (tEl) tEl.textContent = L_TITLES[LT] || LT.toUpperCase();
    renderLeft();
  } else {
    L_OPEN = false;
    if (left.offsetWidth > 70) LAST_L_WIDTH = left.offsetWidth;
    lpanel.style.display = "none";
    left.style.width = "64px";
    if (splitL) splitL.style.display = "none";
    document.querySelectorAll("#lrail .rail-btn").forEach(b => b.classList.remove("on"));
  }
  if (Math.abs(PVZOOM - 1) < 0.01) fitScreenView();
}
function onLeftRailClick(k) {
  if (L_OPEN && LT === k) {
    toggleLeft(false);
  } else {
    LT = k;
    toggleLeft(true);
  }
}
function selTab(k) {
  LT = k;
  toggleLeft(true);
}

function renderLeft() {
  const body = $("#lbody"); if (!body || !SPEC) return; body.innerHTML = "";
  if (LT === "media") {
    const imp = document.createElement("button"); imp.innerHTML = svg("plus") + "Enpote medya (foto / video / odyo)"; imp.style.cssText = "width:100%;justify-content:center";
    const fi = document.createElement("input"); fi.type = "file"; fi.multiple = true; fi.accept = "image/*,video/*,audio/*"; fi.style.display = "none";
    imp.onclick = () => fi.click(); fi.onchange = () => importMedia(fi.files);
    body.appendChild(imp); body.appendChild(fi);
    const hint = document.createElement("div"); hint.style.cssText = "color:var(--dim);font-size:11px;margin:2px 0"; hint.textContent = "Trennen yon medya sou viewer/timeline, oswa klike pou ajoute.";
    body.appendChild(hint);
    const mg = document.createElement("div"); mg.id = "mgrid"; mg.style.cssText = "display:grid;grid-template-columns:repeat(3,1fr);gap:6px"; body.appendChild(mg);
    renderImported(mg);
    api("GET", "/api/media").then(r => { const m = (r.body && r.body.media) || []; if (m.length) { window.IMPORTED = m; renderImported(mg); } });
  } else if (LT === "assets") {
    const bar = document.createElement("div"); bar.id = "asearch";
    bar.innerHTML = '<input id="aq" placeholder="Chache nan 10k asset..."><select id="acat"></select>';
    body.appendChild(bar);
    const grid = document.createElement("div"); grid.id = "agrid"; body.appendChild(grid);
    const more = document.createElement("button"); more.textContent = "Plis"; more.style.marginTop = "6px"; more.onclick = () => loadAssets(true); body.appendChild(more);
    $("#aq").oninput = () => { clearTimeout(window._at); window._at = setTimeout(() => { AOFF = 0; loadAssets(false); }, 250); };
    $("#acat").onchange = () => { ACAT = $("#acat").value; AOFF = 0; loadAssets(false); };
    loadAssets(false, true);
  } else if (LT === "cat") {
    const hint = document.createElement("div"); hint.style.cssText = "color:var(--dim);font-size:11px;padding:2px 2px 4px"; hint.textContent = "Klike pou ajoute yon sen @ kurse a:"; body.appendChild(hint);
    CATALOG.forEach(ty => { const d = document.createElement("div"); d.className = "cat"; d.innerHTML = svg("plus") + "<b>" + ty + "</b>"; d.onclick = () => addScene(ty); body.appendChild(d); });
  } else if (LT === "sfx") {
    const hint = document.createElement("div"); hint.style.cssText = "color:var(--dim);font-size:11px;padding:2px 2px 4px"; hint.textContent = "Klike pou tande, klike [+] pou mete sou track SFX oswa trennen sou timeline:";
    body.appendChild(hint);
    const sg = document.createElement("div"); sg.style.cssText = "display:flex;flex-direction:column;gap:6px";
    body.appendChild(sg);
    SFX_PRESETS.forEach(p => {
      const it = document.createElement("div"); it.className = "item"; it.draggable = true;
      it.innerHTML = '<span class="thumb" style="width:36px;height:36px">' + svg(p.icon || "volume") + '</span>' +
                     '<div class="t"><b>' + p.name + '</b><span>' + p.desc + ' • ' + p.dur + 's</span></div>' +
                     '<button class="ico sfx-play" title="Tande">' + svg("play") + '</button>' +
                     '<button class="ico sfx-add" title="Ajoute sou track SFX">' + svg("plus") + '</button>';
      it.querySelector(".sfx-play").onclick = (e) => { e.stopPropagation(); playSfxSynth(p.id); };
      it.querySelector(".sfx-add").onclick = (e) => { e.stopPropagation(); addSfxClip(p); };
      it.addEventListener("dragstart", ev => {
        ev.dataTransfer.setData("text/kadans-sfx", p.id);
        ev.dataTransfer.setData("text/kadans-kind", "sfx");
        ev.dataTransfer.effectAllowed = "copy";
      });
      sg.appendChild(it);
    });
    // ---- BIBLIYOTÈK SON CC0 (gratis): krikèt, kòk, lanmè, pòt, pa… → kopi nan medya/sfx/ pwojè a
    const lh = document.createElement("div"); lh.style.cssText = "margin-top:12px;font-weight:700;font-size:12px";
    lh.textContent = "Bibliyotèk son CC0 (gratis)"; body.appendChild(lh);
    const lq = document.createElement("input"); lq.id = "sfxq"; lq.placeholder = "krikèt, kòk, lanmè, pòt, pa bwa…";
    lq.style.cssText = "width:100%;margin:6px 0"; body.appendChild(lq);
    const lg = document.createElement("div"); lg.id = "sfxlib"; lg.style.cssText = "display:flex;flex-direction:column;gap:6px";
    body.appendChild(lg);
    lq.oninput = () => { clearTimeout(window._sq); window._sq = setTimeout(loadSounds, 220); };
    loadSounds();
  } else if (LT === "comp") {
    const d = document.createElement("div"); d.className = "item";
    d.innerHTML = '<span class="thumb">' + svg("folder") + '</span><div class="t"><b>composition.html</b><span>ROOT - ' + SPEC.scenes.length + " sen / " + total().toFixed(1) + ' s</span></div>' + svg("download");
    d.onclick = exportHtml; body.appendChild(d);
  } else if (LT === "code") {
    const tb = document.createElement("div"); tb.className = "tabrow"; tb.style.padding = "0 0 6px";
    tb.innerHTML = '<button class="' + (CODEVIEW === "html" ? "on" : "") + '" id="cvh">HTML reyel</button><button class="' + (CODEVIEW === "json" ? "on" : "") + '" id="cvj">spec.json</button>';
    body.appendChild(tb);
    const pre = document.createElement("pre"); pre.id = "codepre"; pre.textContent = "..."; body.appendChild(pre);
    $("#cvh").onclick = () => { CODEVIEW = "html"; renderLeft(); }; $("#cvj").onclick = () => { CODEVIEW = "json"; renderLeft(); };
    if (CODEVIEW === "json") pre.textContent = JSON.stringify(SPEC, null, 2);
    else api("GET", "/api/html").then(r => { pre.textContent = (r.body && r.body.html) || "(bati yon apesi anvan: bouton Apesi)"; });
  }
}

async function loadSounds() {
  const lg = $("#sfxlib"); if (!lg) return;
  const q = ($("#sfxq") && $("#sfxq").value || "").trim();
  const r = await api("GET", "/api/sounds?q=" + encodeURIComponent(q));
  lg.innerHTML = "";
  ((r.body && r.body.items) || []).forEach(s => {
    const it = document.createElement("div"); it.className = "item"; it.draggable = true;
    it.innerHTML = '<span class="thumb" style="width:36px;height:36px">' + svg("volume") + '</span>' +
      '<div class="t"><b>' + s.id + '</b><span>' + (s.loop ? "ambyans (bouk) • " : "") + (s.dur || 0).toFixed(1) + 's' +
      (s.n > 1 ? ' • ' + s.n + ' varyant' : '') + ' • ' + s.tags.slice(0, 4).join(" ") + '</span></div>' +
      '<button class="ico sfx-play" title="Tande">' + svg("play") + '</button>' +
      '<button class="ico sfx-add" title="Ajoute sou timeline la (kurse a)">' + svg("plus") + '</button>';
    it.querySelector(".sfx-play").onclick = e => { e.stopPropagation();
      try { if (window._sfxAudio) window._sfxAudio.pause(); window._sfxAudio = new Audio("/sfxlib/" + s.id); window._sfxAudio.play(); } catch (er) {} };
    it.querySelector(".sfx-add").onclick = e => { e.stopPropagation(); addLibSound(s.id, CUR); };
    it.addEventListener("dragstart", ev => { ev.dataTransfer.setData("text/kadans-cc0", s.id); ev.dataTransfer.effectAllowed = "copy"; });
    lg.appendChild(it);
  });
}
async function addLibSound(id, t) {
  const r = await api("POST", "/api/sounds/take", { id });
  const b = r.body || {}; if (!b.ok) { msg("son pa jwenn: " + id); return; }
  const ti = ensureTrack(b.loop ? "audio" : "sfx");
  const tk = SPEC.tracks[ti]; snapshot(); tk.clips = tk.clips || [];
  const start = freeStart(tk, Math.max(0, t || 0), Math.min(b.dur, 30));
  tk.clips.push({ src: b.rel, kind: "audio", start, dur: Math.min(b.dur, Math.max(0.2, total() - start) || b.dur),
                  label: "CC0 " + id, fadein: b.loop ? 0.6 : 0, fadeout: b.loop ? 0.6 : 0 });
  DIRTY = true; renderTimeline(); renderRight(); msg("son CC0 '" + id + "' → " + b.rel + " @ " + start.toFixed(1) + "s");
}
async function loadAssets(append, fillCats) {
  const grid = $("#agrid"); if (!grid) return;
  if (!append) { AOFF = 0; grid.innerHTML = ""; }
  const q = ($("#aq") && $("#aq").value || "").trim();
  const r = await api("GET", "/api/assets?offset=" + AOFF + "&limit=60&cat=" + encodeURIComponent(ACAT) + "&q=" + encodeURIComponent(q));
  const b = r.body || {};
  if (fillCats && $("#acat")) {
    const sel = $("#acat"); sel.innerHTML = '<option value="">Tout kategori</option>';
    (b.cats || []).forEach(c => { const o = document.createElement("option"); o.value = c; o.textContent = c.length > 26 ? "..." + c.slice(-24) : c; sel.appendChild(o); });
  }
  (b.items || []).forEach(it => {
    const a = document.createElement("div"); a.className = "asset"; a.title = it.path; a.draggable = true;
    const url = "assets/" + it.path.split("/").map(encodeURIComponent).join("/");
    a.innerHTML = '<img src="' + url + '" loading="lazy">';
    a.addEventListener("dragstart", ev => { ev.dataTransfer.setData("text/kadans-asset", url); ev.dataTransfer.setData("text/kadans-kind", "asset"); ev.dataTransfer.effectAllowed = "copy"; });
    a.onclick = () => dropAssetOnScene(url);
    grid.appendChild(a);
  });
  AOFF += (b.items || []).length;
  msg((b.total || 0) + " asset" + (q ? " pou '" + q + "'" : ""));
}
window.IMPORTED = window.IMPORTED || [];
const MEDIA_KINDS = [["vwa", "Vwa"], ["mizik", "Mizik"], ["sfx", "SFX"], ["imaj", "Imaj"], ["videyo", "Videyo"]];
function renderImported(grid) {
  grid.innerHTML = "";
  if (!window.IMPORTED.length) { grid.innerHTML = '<div style="grid-column:1/-1;color:var(--dim);font-size:11px">Pa gen medya enpote. Klike bouton an anwo.</div>'; return; }
  // Medya pwojè a KLASE pa kalite (dosye medya/vwa, mizik, sfx, imaj, videyo) — tout sa AI a oswa ou mete ladan l
  const order = MEDIA_KINDS.map(k => k[0]);
  const items = window.IMPORTED.slice().sort((a, b) => (order.indexOf(a.kind || "") + 99) % 99 - (order.indexOf(b.kind || "") + 99) % 99);
  let lastKind = null;
  items.forEach(m => {
    const k = m.kind || "";
    if (k !== lastKind) {
      lastKind = k;
      const lab = (MEDIA_KINDS.find(x => x[0] === k) || [k, "Medya"])[1];
      const h = document.createElement("div"); h.className = "mkind";
      h.style.cssText = "grid-column:1/-1;color:var(--dim);font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;margin:6px 0 0";
      h.textContent = lab;                                     // tèks apa: tradiksyon an jwenn mo a egzak
      const cnt = document.createElement("span"); cnt.textContent = " · " + items.filter(x => (x.kind || "") === k).length; h.appendChild(cnt);
      grid.appendChild(h);
    }
    const a = document.createElement("div"); a.className = "asset"; a.title = m.name; a.draggable = true;
    const isImg = /\.(png|jpe?g|gif|webp|svg|bmp)$/i.test(m.name);
    a.innerHTML = isImg ? '<img src="' + withTok(m.rel) + '" loading="lazy" style="filter:none;opacity:1">' : svg(/\.(mp4|webm|mov|m4v)$/i.test(m.name) ? "film" : "music");
    if (window.KMP) KMP.decorate(a, m);                       // media_panel.js: play preview, thumbnail, length
    a.addEventListener("dragstart", ev => { ev.dataTransfer.setData("text/kadans-asset", m.rel); ev.dataTransfer.setData("text/kadans-kind", mediaKind(m.rel)); ev.dataTransfer.effectAllowed = "copy"; });
    a.onclick = () => dropAssetOnScene(m.rel);
    grid.appendChild(a);
  });
}
async function importMedia(files) {
  for (const f of files) {
    msg("ap enpote " + f.name + "...");
    const buf = await f.arrayBuffer();
    const u = "/api/upload?name=" + encodeURIComponent(f.name) + "&token=" + encodeURIComponent(TOK);
    const r = await fetch(u, { method: "POST", body: buf });
    const j = await r.json().catch(() => ({}));
    if (j.ok) window.IMPORTED.unshift({ rel: j.rel, name: j.name, kind: j.kind });   // sak pi nouvo anlè
  }
  msg(window.IMPORTED.length + " medya enpote"); const g = $("#mgrid"); if (g) renderImported(g);
}
function addScene(type) {
  snapshot();
  if (TRACKSEL && TRACKSEL.indexOf("tk") === 0) {               // track itilizatè chwazi -> clip @ pozisyon kisè a
    const ti = +TRACKSEL.slice(2), tk = SPEC.tracks[ti];
    if (tk) { const k = (type === "text" ? "text" : type); if (!kindOk(k, tk.kind)) { msg("yon " + k + " pa ka ale sou track " + tk.kind); return; } tk.clips = tk.clips || []; const st = freeStart(tk, CUR, 2); tk.clips.push({ type, kind: k, start: st, dur: 2, label: (type === "text" ? "Teks" : type) }); DIRTY = true; CLIPSEL = { t: ti, c: tk.clips.length - 1 }; renderTimeline(); renderRight(); renderLeft(); msg(type + " sou " + (tk.name || tk.kind) + " @ " + st.toFixed(1) + "s"); return; }
  }
  const sc = { type, id: type + "_" + Math.random().toString(36).slice(2, 6) };
  if (type === "html") sc.html = "<div style=\"color:#fff;font:bold 48px system-ui;display:grid;place-items:center;height:100%\">Ekri teks ou a la</div>";
  else if (type === "text") sc.title = "Ekri teks ou a la";
  else sc.title = "Nouvo " + type;
  const at = SPEC.scenes.length ? (sceneAt(CUR) + 1) : 0;        // ENSERE kote kisè a ye (pa nan fen an)
  SPEC.scenes.splice(at, 0, sc); DIRTY = true; SEL = at;
  renderTimeline(); selRTab("props"); renderLeft(); msg("sen " + type + " ajoute @ pozisyon " + (at + 1));
  setTimeout(() => { const el = document.querySelector("#ibody input[type=text], #ibody input:not([type]), #ibody textarea"); if (el) { el.focus(); if (el.select) el.select(); } }, 40);
}

// ---- Drag-and-drop asset (nan sen / viewer / track) ----
function mediaKind(src, type) {
  if (type === "text") return "text";
  const s = (src || "").toLowerCase();
  if (/\.(mp4|webm|mov|m4v|mkv|avi)$/.test(s)) return (type === "audio" ? "audio" : "video");
  if (/\.(wav|mp3|m4a|aac|ogg|opus|flac)$/.test(s)) return "audio";
  if (/\.(png|jpe?g|gif|webp|svg|bmp)$/.test(s)) return "image";
  return type || "image";
}
function kindOk(clipKind, trackKind) {
  if (!trackKind || clipKind === trackKind) return true;
  if ((trackKind === "asset" || trackKind === "image") && (clipKind === "image" || clipKind === "asset")) return true;
  if ((trackKind === "audio" || trackKind === "sfx") && (clipKind === "audio" || clipKind === "sfx")) return true;
  if (trackKind === "video" && (clipKind === "video" || clipKind === "image")) return true;
  return false;
}
function ensureTrack(kind) {
  SPEC.tracks = SPEC.tracks || [];
  let ti = SPEC.tracks.findIndex(tk => tk.kind === kind);
  if (ti < 0) {
    const names = { video: "Video", audio: "Audio", image: "Imaj", text: "Teks", asset: "Asset" };
    SPEC.tracks.unshift({ kind, name: (names[kind] || kind) + " 1", clips: [] });
    ti = 0; msg("nouvo track " + (names[kind] || kind) + " kreye");
  }
  return ti;
}
function freeStart(tk, t, dur) {
  let start = Math.round(t * 10) / 10;
  (tk.clips || []).forEach(c => { const cs = c.start || 0, ce = cs + (c.dur || 2); if (start < ce && start + dur > cs) start = Math.round(ce * 10) / 10; });
  return start;
}
// Montaj clip-primè: mete clip la @ atT selon EDITMODE. Retounen endèks li nan tk.clips.
// insert = pouse tout clips ki kòmanse >= atT adwat pa dire clip la (pa gen chevochman).
// overwrite = clip la genyen sou entèval li a: koupe/separe/jete clips ki chevoche.
function placeClipAt(tk, clip, atT) {
  tk.clips = tk.clips || [];
  const s = Math.max(0, SNAP ? Math.round(atT * 10) / 10 : atT);
  const d = Math.max(0.1, clip.dur || 2), e = s + d;
  clip.start = s; clip.dur = d;
  if (EDITMODE === "insert") {
    tk.clips.forEach(x => { if ((x.start || 0) >= s - 1e-6) x.start = Math.round(((x.start || 0) + d) * 1000) / 1000; });
    tk.clips.push(clip);
    return tk.clips.indexOf(clip);
  }
  const kept = [];                                  // overwrite
  tk.clips.forEach(x => {
    const xs = x.start || 0, xe = xs + (x.dur || 0), isMed = (x.in != null);
    if (xe <= s + 1e-6 || xs >= e - 1e-6) { kept.push(x); return; }   // pa chevoche
    if (xs < s && xe > e) {                          // nouvo a nan mitan → koupe x an 2
      const right = JSON.parse(JSON.stringify(x));
      x.dur = Math.round((s - xs) * 1000) / 1000;
      right.start = e; right.dur = Math.round((xe - e) * 1000) / 1000;
      if (isMed) right.in = Math.round(((x.in || 0) + (e - xs)) * 1000) / 1000;
      kept.push(x); kept.push(right);
    } else if (xs < s) {                             // koupe fen x
      x.dur = Math.round((s - xs) * 1000) / 1000; kept.push(x);
    } else if (xe > e) {                             // pouse kòmansman x
      if (isMed) x.in = Math.round(((x.in || 0) + (e - xs)) * 1000) / 1000;
      x.start = e; x.dur = Math.round((xe - e) * 1000) / 1000; kept.push(x);
    }                                                // fèmen nèt anndan → jete
  });
  kept.push(clip); tk.clips = kept;
  return tk.clips.indexOf(clip);
}
function toggleEditMode() {
  EDITMODE = EDITMODE === "overwrite" ? "insert" : "overwrite";
  const b = $("#tEditMode");
  if (b) { b.textContent = EDITMODE === "insert" ? "Insert" : "Overwrite"; b.classList.toggle("on", EDITMODE === "insert"); }
  msg(EDITMODE === "insert" ? "Mòd Insert: nouvo clip pouse lòt yo adwat" : "Mòd Overwrite: nouvo clip ekrase sa ki anba");
}
async function useAsset(url) {
  // asset bibliyotek (assets/..) = kopye nan work/media pou apesi + render jwenn li; medya enpote (media/..) deja la
  if (url.indexOf("assets/") === 0) {
    const r = await api("POST", "/api/use-asset", { path: decodeURIComponent(url.slice(7)) });
    if (r.body && r.body.ok) return r.body.rel;
  }
  return url;
}
async function dropAssetOnScene(url, sceneIdx, x, y) {
  const i = sceneIdx != null ? sceneIdx : sceneAt(CUR);
  const sc = SPEC.scenes[i]; if (!sc) { msg("pa gen sen"); return; }
  const src = await useAsset(url);
  if (mediaKind(src) === "audio") {             // v3.10: yon son PA JANM yon kalk imaj (spec la te vin envalid)
    const ti = ensureTrack("audio");
    await dropAssetOnTrack(src, ti, CUR, "audio");
    msg(_tk("drop_audio_track", "son an mete sou yon track odyo (yon son pa ka yon kalk imaj)"));
    return;
  }
  snapshot();
  sc.overlays = sc.overlays || [];
  sc.overlays.push({ src, layer: "front", blend: "normal", opacity: 1, x: (x != null ? Math.round(x * 100) / 100 : 0.5), y: (y != null ? Math.round(y * 100) / 100 : 0.5), w: 0.3 });
  DIRTY = true; SEL = i; RT = "blend"; OVSEL = { s: i, o: sc.overlays.length - 1 };
  renderTimeline(); renderRight(); msg("asset ajoute @ kurse a - trennen/resize nan ekran an"); build();
}
async function dropAssetOnTrack(url, trackIdx, t, kind) {
  const tk = SPEC.tracks[trackIdx]; if (!tk) return;
  const src = await useAsset(url);
  const k = kind || mediaKind(src);
  if (!kindOk(k, tk.kind)) { msg("yon medya " + k + " pa ka ale sou yon track " + tk.kind); return; }
  const dur = await clipDur(src, k);                         // VRÈ dire fichye a (odyo / videyo), imaj: 2 s
  snapshot(); tk.clips = tk.clips || [];
  const nc = { src, kind: k, dur, label: src.split("/").pop() };
  const ci = placeClipAt(tk, nc, t);                         // Insert/Overwrite selon EDITMODE
  DIRTY = true; CLIPSEL = { t: trackIdx, c: ci }; renderTimeline(); renderRight(); renderLeft(); msg("clip ajoute (" + EDITMODE + ") @ " + nc.start.toFixed(1) + "s");
  return dur;
}
// Dire yon clip ki tonbe sou yon track: longè EGZAK fichye odyo / videyo a (media_panel.js: /api/media-info,
// ffmpeg, an kach; oswa metadata <audio>/<video>). Imaj / dire enkoni: 2 s pa defo.
async function clipDur(src, kind) {
  if (kind !== "audio" && kind !== "video" && kind !== "sfx") return 2;
  try { const d = window.KMP && KMP.duration ? await KMP.duration(src) : 0; if (d > 0) return Math.round(d * 100) / 100; } catch (e) {}
  return 2;
}
async function extractDropMedia(ev) {
  const items = [];
  if (ev.dataTransfer && ev.dataTransfer.files && ev.dataTransfer.files.length) {
    for (const f of ev.dataTransfer.files) {
      msg("ap enpote " + f.name + "...");
      try {
        const buf = await f.arrayBuffer();
        const u = "/api/upload?name=" + encodeURIComponent(f.name) + "&token=" + encodeURIComponent(TOK);
        const res = await fetch(u, { method: "POST", body: buf });
        const j = await res.json().catch(() => ({}));
        if (j && j.ok) {
          if (!window.IMPORTED.some(x => x.rel === j.rel)) window.IMPORTED.unshift({ rel: j.rel, name: j.name });
          items.push({ rel: j.rel, name: j.name, kind: mediaKind(j.name) });
        }
      } catch (e) {
        msg("ere enpote: " + e.message);
      }
    }
    const g = $("#mgrid"); if (g) renderImported(g);
    if (items.length) return items;
  }
  let url = (ev.dataTransfer && (ev.dataTransfer.getData("text/kadans-asset") || ev.dataTransfer.getData("text/plain") || ev.dataTransfer.getData("text/uri-list"))) || "";
  if (url) {
    url = url.trim();
    if (url.startsWith("file:///")) url = decodeURIComponent(url.replace("file:///", ""));
    const kind = (ev.dataTransfer && ev.dataTransfer.getData("text/kadans-kind")) || mediaKind(url);
    const resolved = await useAsset(url);
    items.push({ rel: resolved, name: resolved.split("/").pop(), kind });
  }
  return items;
}

function wireScenesDrop(row) {
  row.addEventListener("dragover", ev => { ev.preventDefault(); ev.dataTransfer.dropEffect = "copy"; row.classList.add("drop"); });
  row.addEventListener("dragleave", () => row.classList.remove("drop"));
  row.addEventListener("drop", async ev => {
    ev.preventDefault(); ev.stopPropagation(); row.classList.remove("drop");
    const mediaList = await extractDropMedia(ev);
    if (!mediaList || !mediaList.length) return;
    for (const m of mediaList) {
      if (m.kind === "video" || m.kind === "image") {
        const ti = ensureTrack(m.kind);
        const tk = SPEC.tracks[ti];
        const dur = await clipDur(m.rel, m.kind);
        const st = freeStart(tk, CUR, dur);
        snapshot();
        tk.clips = tk.clips || [];
        const nc = { src: m.rel, kind: m.kind, dur, start: st, label: m.name.replace(/\.[^.]+$/, "") };
        const ci = placeClipAt(tk, nc, st);
        DIRTY = true; CLIPSEL = { t: ti, c: ci }; renderTimeline(); renderRight(); build();
        msg((m.kind === "video" ? "videyo" : "imaj") + " ajoute sou track: " + m.name);
      } else if (m.kind === "audio") {
        const ti = ensureTrack("audio"); const tk = SPEC.tracks[ti]; tk.clips = tk.clips || [];
        const ad = await clipDur(m.rel, "audio");
        const st = freeStart(tk, CUR, ad); tk.clips.push({ src: m.rel, kind: "audio", start: st, dur: ad, label: m.name });
        DIRTY = true; renderTimeline(); renderRight(); msg("odyo ajoute sou track: " + m.name);
      }
    }
  });
}

function dropTarget(row, trackIdx) {
  const tk = SPEC.tracks[trackIdx];
  row.addEventListener("dragover", ev => { ev.preventDefault(); ev.dataTransfer.dropEffect = "copy"; row.classList.add("drop"); });
  row.addEventListener("dragleave", () => row.classList.remove("drop"));
  row.addEventListener("drop", async ev => {
    ev.preventDefault(); ev.stopPropagation(); row.classList.remove("drop");
    const mediaList = await extractDropMedia(ev);
    if (!mediaList || !mediaList.length) return;
    const r = $("#tlinner").getBoundingClientRect();
    let t = Math.max(0, (ev.clientX - r.left) / PPS);
    for (const m of mediaList) {
      let targetIdx = trackIdx;
      if (tk && !kindOk(m.kind, tk.kind)) {
        targetIdx = ensureTrack(m.kind);
      }
      const d = await dropAssetOnTrack(m.rel, targetIdx, t, m.kind);
      t += (d || 2) + 0.2;
    }
  });
}

function wireViewerDrop() {
  const w = $("#pvwrap");
  if (!w) return;
  w.addEventListener("dragover", ev => { ev.preventDefault(); ev.dataTransfer.dropEffect = "copy"; w.classList.add("drag"); });
  w.addEventListener("dragleave", () => w.classList.remove("drag"));
  w.addEventListener("drop", async ev => {
    ev.preventDefault(); w.classList.remove("drag");
    const mediaList = await extractDropMedia(ev);
    if (!mediaList || !mediaList.length) return;
    const r = w.getBoundingClientRect();
    const x = Math.max(0, Math.min(1, (ev.clientX - r.left) / r.width));
    const y = Math.max(0, Math.min(1, (ev.clientY - r.top) / r.height));
    for (const m of mediaList) {
      if (m.kind === "video") {
        const curSc = (SPEC.scenes && SPEC.scenes[SEL >= 0 ? SEL : sceneAt(CUR)]) || null;
        if (curSc && curSc.type === "video" && (!curSc.src || ev.altKey)) {
          snapshot(); curSc.src = m.rel; DIRTY = true; renderTimeline(); renderRight(); build(); msg("videyo sèn mete ajou: " + m.name);
        } else {
          const ti = ensureTrack("video");
          const tk = SPEC.tracks[ti];
          const dur = await clipDur(m.rel, "video");
          const st = freeStart(tk, CUR, dur);
          snapshot();
          tk.clips = tk.clips || [];
          const nc = { src: m.rel, kind: "video", dur, start: st, label: m.name.replace(/\.[^.]+$/, "") };
          const ci = placeClipAt(tk, nc, st);
          DIRTY = true; CLIPSEL = { t: ti, c: ci }; renderTimeline(); renderRight(); build();
          msg("videyo ajoute sou track " + (tk.name || "Videyo") + ": " + m.name);
        }
      } else if (m.kind === "audio") {
        const ti = ensureTrack("audio"); const tk = SPEC.tracks[ti]; tk.clips = tk.clips || [];
        const ad = await clipDur(m.rel, "audio");
        const st = freeStart(tk, CUR, ad); tk.clips.push({ src: m.rel, kind: "audio", start: st, dur: ad, label: m.name });
        DIRTY = true; renderTimeline(); renderRight(); msg("odyo ajoute sou track: " + m.name);
      } else {
        dropAssetOnScene(m.rel, undefined, x, y);
      }
    }
  });
}

// ---- PANEL DWAT (Pwopriyete / Koule / Blend / Son) ----
const TRANSITIONS = ["", "none", "fade", "slide", "slideright", "slideup", "slidedown", "wipe", "wipeup", "zoom", "zoomout", "flip", "rotate", "blur"];
function getRTitles() {
  const t = (window.KadansI18n && window.KadansI18n.t) || (k => k);
  return {
    props: t("prop_tab_title", "Propriétés"),
    color: t("color_tab_title", "Couleur (Étalonnage)"),
    blend: t("blend_tab_title", "Mélange & Opacité"),
    sound: t("sound_tab_title", "Son & Audio"),
    effect: t("effect_tab_title", "Effets Visuels"),
    lut: t("lut_tab_title", "LUT (Filtres Cinématiques)"),
    subs: t("subs_tab_title", "Sou-tit (Sous-titres)"),
    ai: t("ai_tab_title", "AI Chat & MCP")
  };
}
let R_OPEN = true, LAST_R_WIDTH = 360;
function toggleRight(forceState) {
  const insp = $("#insp"), ipanel = $("#ipanel"), splitR = $("#splitR"), rrail = $("#rrail");
  if (!insp || !ipanel) return;
  const shouldOpen = (forceState !== undefined) ? !!forceState : !R_OPEN;
  if (shouldOpen) {
    R_OPEN = true;
    insp.style.display = "flex";
    ipanel.style.display = "flex";
    insp.style.width = Math.max(200, LAST_R_WIDTH || 360) + "px";
    if (splitR) splitR.style.display = "";
    if (rrail) rrail.style.borderLeft = "";
    document.querySelectorAll("#rrail .rail-btn").forEach(b => b.classList.toggle("on", b.dataset.rt === RT));
    const tEl = $("#ititle"); if (tEl) tEl.textContent = (typeof getRTitles === "function" ? getRTitles()[RT] : "") || RT.toUpperCase();
    renderRight();
  } else {
    R_OPEN = false;
    if (insp.offsetWidth > 70) LAST_R_WIDTH = insp.offsetWidth;
    ipanel.style.display = "none";
    insp.style.width = "64px";
    if (splitR) splitR.style.display = "none";
    if (rrail) rrail.style.borderLeft = "none";
    document.querySelectorAll("#rrail .rail-btn").forEach(b => b.classList.remove("on"));
  }
  if (Math.abs(PVZOOM - 1) < 0.01) fitScreenView();
}
function onRightRailClick(k) {
  if (k === "ai") {
    api("POST", "/api/audio-bridge", { cmd: "open_ai_chat", project: PROJNAME || "" }).catch(() => {});
    msg("Ouvri Chat AI WASDEV...");
    return;
  }
  if (R_OPEN && RT === k) {
    toggleRight(false);
  } else {
    RT = k;
    toggleRight(true);
  }
}
function selRTab(k) {
  if (k === "ai") {
    api("POST", "/api/audio-bridge", { cmd: "open_ai_chat", project: PROJNAME || "" }).catch(() => {});
    msg("Ouvri Chat AI WASDEV...");
    k = "props";
  }
  RT = k;
  toggleRight(true);
}
function renderRight() {
  const f = $("#ibody"); if (!f) return;
  if (RT === "ai") return renderProps(f);
  const clip = CLIPSEL && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c];
  if (clip) return renderClipTab(f);
  if (RT === "props") return renderProps(f);
  if (RT === "color") return renderColor(f);
  if (RT === "blend") return renderBlend(f);
  if (RT === "sound") return renderSound(f);
  if (RT === "effect") return renderEffect(f);
  if (RT === "lut") return renderLut(f);
  if (RT === "subs") return renderSubs(f);
}
function renderSubs(f) {
  f.innerHTML = "";
  const h = document.createElement("h3"); h.innerHTML = svg("text") + " Sou-tit (edite tèks / tan / stil)"; f.appendChild(h);
  SPEC.sub_cues = SPEC.sub_cues || [];
  SPEC.sub_style = SPEC.sub_style || {};
  // Stil jeneral
  gradeSub(f, "Stil jeneral");
  const st = SPEC.sub_style;
  field(f, "Gwosè (px)", () => (st.size != null ? st.size : ""), v => { const n = parseFloat(v); if (isNaN(n)) delete st.size; else st.size = n; DIRTY = true; build(); }, { type: "number", step: "1", commit: 1 });
  colorRow(f, "Koulè tèks", () => st.color || "#ffffff", v => { st.color = v; DIRTY = true; build(); });
  colorRow(f, "Fon bwat la (bg)", () => st.bg || "#000000aa", v => { st.bg = v; DIRTY = true; build(); });
  field(f, "Pozisyon", () => st.pos || "bottom", v => { st.pos = v; DIRTY = true; build(); }, { list: ["bottom", "top", "middle"] });
  // Ajoute
  gradeSub(f, "Sou-tit yo");
  const ab = document.createElement("button"); ab.className = "pri"; ab.innerHTML = svg("plus") + "Ajoute sou-tit @ tèt lekti a"; ab.style.cssText = "width:100%;justify-content:center;margin-bottom:8px";
  ab.onclick = () => { snapshot(); const s = Math.round((CUR || 0) * 100) / 100; SPEC.sub_cues.push({ s, e: Math.round((s + 2) * 100) / 100, text: "Nouvo sou-tit" }); SPEC.sub_cues.sort((a, b) => a.s - b.s); DIRTY = true; renderSubs(f); build(); msg("sou-tit ajoute @ " + s.toFixed(1) + "s"); };
  f.appendChild(ab);
  if (!SPEC.sub_cues.length) { const d = document.createElement("div"); d.style.cssText = "color:var(--dim);font-size:12px"; d.textContent = "Pa gen sou-tit. Ajoute youn @ tèt lekti a."; f.appendChild(d); return; }
  SPEC.sub_cues.forEach((q, idx) => {
    const box = document.createElement("div"); box.style.cssText = "border:1px solid var(--line);border-radius:8px;padding:6px;margin-bottom:6px";
    const ta = document.createElement("textarea"); ta.value = q.text || ""; ta.rows = 2; ta.style.cssText = "width:100%;margin-bottom:4px"; ta.oninput = () => { q.text = ta.value; DIRTY = true; }; ta.onchange = () => build(); box.appendChild(ta);
    const row = document.createElement("div"); row.style.cssText = "display:flex;gap:4px;align-items:center;flex-wrap:wrap";
    const mk = (lab, get, set) => { const l = document.createElement("span"); l.textContent = lab; l.style.cssText = "font-size:10px;color:var(--dim)"; const i = document.createElement("input"); i.type = "number"; i.step = "0.1"; i.value = get(); i.style.cssText = "width:56px"; i.onchange = () => { set(parseFloat(i.value) || 0); DIRTY = true; renderTimeline(); build(); }; row.appendChild(l); row.appendChild(i); };
    mk("depa", () => (q.s || 0), v => { q.s = Math.max(0, v); if (q.e <= q.s) q.e = q.s + 1.5; });
    mk("fen", () => (q.e || 0), v => { q.e = v > (q.s || 0) ? v : (q.s || 0) + 1.5; });
    const go = document.createElement("button"); go.textContent = "▶"; go.title = "Ale @ sou-tit la"; go.style.cssText = "padding:2px 7px"; go.onclick = () => { CUR = q.s || 0; movePlayhead(); post({ cmd: "seek", t: CUR }); }; row.appendChild(go);
    const del = document.createElement("button"); del.textContent = "✕"; del.title = "Efase sou-tit"; del.style.cssText = "padding:2px 7px;margin-left:auto"; del.onclick = () => { snapshot(); SPEC.sub_cues.splice(idx, 1); DIRTY = true; renderSubs(f); build(); }; row.appendChild(del);
    box.appendChild(row); f.appendChild(box);
  });
  const cb = document.createElement("button"); cb.textContent = "Efase tout sou-tit"; cb.style.cssText = "width:100%;justify-content:center;margin-top:4px"; cb.onclick = () => { snapshot(); SPEC.sub_cues = []; DIRTY = true; renderSubs(f); build(); msg("tout sou-tit efase"); }; f.appendChild(cb);
}

let AI_HISTORY = [];
let AI_PROVIDERS = [];
let AI_ACTIVE_PROV = "claude";
let AI_LOADING = false;

async function renderAiChat(f) {
  const t = (window.KadansI18n && window.KadansI18n.t) || (k => k);
  f.innerHTML = `
    <div style="display:flex;flex-direction:column;height:100%;min-height:420px;gap:8px;padding:4px 2px">
      <div style="background:#17122b;border:1px solid #35295c;border-radius:9px;padding:8px 10px">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:6px">
          <span style="font-size:12px;font-weight:800;color:#c4b5fd">${t("ai_director_title", "Kadans AI Director & MCP")}</span>
          <button type="button" id="kdAiOpenWasdev" class="btn" style="padding:3px 8px;font-size:10px;background:#2e1754;border-color:#6d28d9;color:#e9d5ff" title="${t("ai_open_wasdev_title", "Louvri Chat AI WASDEV la epi voye pwojè a")}">${t("ai_open_wasdev", "↗ Chat WASDEV")}</button>
        </div>
        <div style="display:flex;gap:6px;align-items:center">
          <select id="kdAiProv" style="flex:1;background:#0e0b1a;border:1px solid #2a2440;color:#f3eefe;border-radius:6px;padding:5px 7px;font-size:11px">
            <option value="claude">Claude Code</option>
            <option value="gemini">Gemini CLI</option>
            <option value="antigravity">Google Antigravity</option>
            <option value="codex">OpenAI Codex</option>
          </select>
          <button type="button" id="kdAiMcpSetup" class="btn" style="padding:5px 8px;font-size:10px;background:#1e3a2f;border-color:#10b981;color:#6ee7b7" title="${t("ai_mcp_btn_title", "Konfigire MCP Kadans 1-Klik pou tout AI yo")}">${t("ai_mcp_btn", "⚡ 1-Click MCP")}</button>
        </div>
        <div id="kdAiStatus" style="font-size:10px;color:#9b8ec4;margin-top:5px">${t("ai_checking", "Ap verifye koneksyon AI & MCP...")}</div>
      </div>

      <div id="kdAiMsgs" style="flex:1;min-height:220px;max-height:52vh;overflow-y:auto;background:#0b0815;border:1px solid #221c38;border-radius:9px;padding:8px;display:flex;flex-direction:column;gap:8px">
        <div style="font-size:11px;color:#8e82b8;text-align:center;padding:18px 8px">
          ${t("ai_prompt_hint", "Ekri sa ou vle AI a fè nan videyo a...")}
        </div>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:4px">
        <button type="button" class="btn kdAiQuick" data-p="Kreye 4 sèn piblisite pwofesyonèl ak tranzisyon ak sou-tit karaoke" style="font-size:10px;padding:3px 7px">${t("ai_quick_4scenes", "✨ 4 Sèn Piblisite")}</button>
        <button type="button" class="btn kdAiQuick" data-p="Ajoute sou-tit karaoke mo-pa-mo sou tout sèn yo" style="font-size:10px;padding:3px 7px">${t("ai_quick_subtitles", "💬 Sou-tit Karaoke")}</button>
        <button type="button" class="btn kdAiQuick" data-p="Optimize koulè sinematik ak tranzisyon zoom sou sèn yo" style="font-size:10px;padding:3px 7px">${t("ai_quick_cinema", "🎨 Look Sinema")}</button>
      </div>

      <div style="display:flex;flex-direction:column;gap:6px">
        <textarea id="kdAiInput" rows="3" placeholder="${t("ai_input_placeholder", "Mande AI a monte oswa modifye videyo a...")}" style="width:100%;background:#0e0b1a;border:1px solid #35295c;color:#f3eefe;border-radius:8px;padding:7px 9px;font-size:12px;resize:vertical;outline:none"></textarea>
        <div style="display:flex;gap:6px">
          <button type="button" id="kdAiSend" class="btn pri" style="flex:1;padding:7px 10px;font-weight:700">${t("ai_send_btn", "🚀 Voye bay AI")}</button>
          <button type="button" id="kdAiClear" class="btn" style="padding:7px 10px;font-size:11px" title="${t("ai_clear_title", "Efase istwa chat la")}">🗑</button>
        </div>
      </div>
    </div>
  `;

  const provSel = f.querySelector("#kdAiProv");
  const statusEl = f.querySelector("#kdAiStatus");
  const msgsEl = f.querySelector("#kdAiMsgs");
  const inpEl = f.querySelector("#kdAiInput");
  const sendBtn = f.querySelector("#kdAiSend");
  const clearBtn = f.querySelector("#kdAiClear");
  const mcpBtn = f.querySelector("#kdAiMcpSetup");
  const openWasdevBtn = f.querySelector("#kdAiOpenWasdev");

  if (provSel) {
    provSel.value = AI_ACTIVE_PROV;
    provSel.onchange = () => { AI_ACTIVE_PROV = provSel.value; };
  }

  function renderMsgs() {
    if (!msgsEl) return;
    if (!AI_HISTORY || !AI_HISTORY.length) {
      msgsEl.innerHTML = `<div style="font-size:11px;color:#8e82b8;text-align:center;padding:18px 8px">
        ${t("ai_prompt_hint", "Ekri sa ou vle AI a fè nan videyo a (egz: <i>\"Fè yon piblisite 45 segonn ak 4 sèn, vwa ElevenLabs ak sou-tit karaoke\"</i>).")}
      </div>`;
      return;
    }
    msgsEl.innerHTML = "";
    AI_HISTORY.forEach(m => {
      const isUser = m.role === "user";
      const b = document.createElement("div");
      b.style.cssText = isUser
        ? "align-self:flex-end;max-width:90%;background:#3b1d70;color:#f5f3ff;border:1px solid #6d28d9;border-radius:10px 10px 2px 10px;padding:7px 9px;font-size:11.5px;white-space:pre-wrap;word-break:break-word"
        : "align-self:flex-start;max-width:94%;background:#161229;color:#e2dcf5;border:1px solid #2d254c;border-radius:10px 10px 10px 2px;padding:7px 9px;font-size:11.5px;white-space:pre-wrap;word-break:break-word";
      b.textContent = m.text || "";
      msgsEl.appendChild(b);
    });
    if (AI_LOADING) {
      const waitEl = document.createElement("div");
      waitEl.style.cssText = "align-self:flex-start;color:#a78bfa;font-size:11px;font-style:italic;padding:4px 6px";
      waitEl.textContent = "⏳ AI a ap travay sou timeline nan...";
      msgsEl.appendChild(waitEl);
    }
    msgsEl.scrollTop = msgsEl.scrollHeight;
  }

  async function refreshStatusAndHistory() {
    try {
      const [st, hi] = await Promise.all([
        api("GET", "/api/ai/status"),
        api("GET", "/api/ai/history"),
      ]);
      if (st.body && st.body.providers) {
        AI_PROVIDERS = st.body.providers;
        const inst = AI_PROVIDERS.filter(p => p.installed);
        const mcpCount = AI_PROVIDERS.filter(p => p.mcp_configured).length;
        if (statusEl) {
          statusEl.textContent = `✓ ${inst.length} AI detekte • ${mcpCount}/${AI_PROVIDERS.length} MCP konekte`;
        }
      }
      if (hi.body && Array.isArray(hi.body.history)) {
        AI_HISTORY = hi.body.history;
        renderMsgs();
      }
    } catch (e) {
      if (statusEl) statusEl.textContent = "⚡ Pare pou kominike ak AI Chat";
    }
  }

  async function doSend(textOverride) {
    const prompt = (typeof textOverride === "string" ? textOverride : (inpEl ? inpEl.value : "")).trim();
    if (!prompt || AI_LOADING) return;
    if (inpEl && typeof textOverride !== "string") inpEl.value = "";
    AI_HISTORY.push({ role: "user", text: prompt });
    AI_LOADING = true;
    renderMsgs();
    // Voye tou nan Chat WASDEV si li konekte
    api("POST", "/api/audio-bridge", { cmd: "send_prompt_to_chat", prompt: `/kadans ${prompt}`, auto_send: false }).catch(() => {});
    try {
      const r = await api("POST", "/api/ai/chat", {
        prompt,
        provider: provSel ? provSel.value : AI_ACTIVE_PROV,
        mode: "agent",
      });
      AI_LOADING = false;
      if (r.body && r.body.ok) {
        if (Array.isArray(r.body.history)) AI_HISTORY = r.body.history;
        else if (r.body.reply) AI_HISTORY.push({ role: "assistant", text: r.body.reply });
        if (r.body.spec_updated) {
          await load();
        }
      } else {
        AI_HISTORY.push({ role: "assistant", text: "⚠ " + ((r.body && r.body.error) || "Erè koneksyon AI") });
      }
    } catch (err) {
      AI_LOADING = false;
      AI_HISTORY.push({ role: "assistant", text: "⚠ Erè: " + err });
    }
    renderMsgs();
  }

  if (sendBtn) sendBtn.onclick = () => doSend();
  if (inpEl) {
    inpEl.onkeydown = e => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        doSend();
      }
    };
    setTimeout(() => inpEl.focus(), 40);
  }
  if (clearBtn) {
    clearBtn.onclick = async () => {
      await api("POST", "/api/ai/clear", {});
      AI_HISTORY = [];
      renderMsgs();
    };
  }
  if (mcpBtn) {
    mcpBtn.onclick = async () => {
      if (statusEl) statusEl.textContent = "⏳ Ap konfigire MCP Kadans pou tout AI yo...";
      const r = await api("POST", "/api/ai/setup-all", {});
      if (r.body && r.body.ok) {
        msg("MCP Kadans konfigire pou tout AI yo!");
        refreshStatusAndHistory();
      }
    };
  }
  if (openWasdevBtn) {
    openWasdevBtn.onclick = async () => {
      await api("POST", "/api/send-to-chat", { project: PROJNAME || "" }).catch(() => {});
      await api("POST", "/api/audio-bridge", {
        cmd: "send_prompt_to_chat",
        prompt: `/kadans Pwojè aktif: ${ (SPEC && SPEC.title) || PROJNAME || "Videyo Kadans" } (${ (SPEC && SPEC.ratio) || "16:9" }, dire: ${ (SPEC && SPEC.total_duration) || 30 }s)`,
        auto_send: false,
      }).catch(() => {});
      msg("Pwojè a voye nan Chat AI WASDEV la!");
    };
  }
  f.querySelectorAll(".kdAiQuick").forEach(b => {
    b.onclick = () => doSend(b.dataset.p || "");
  });

  renderMsgs();
  refreshStatusAndHistory();
}
function field(f, label, get, set, opts) {
  const l = document.createElement("label"); l.textContent = label; f.appendChild(l);
  let el;
  if (opts && opts.multi) el = document.createElement("textarea");
  else if (opts && opts.list) { el = document.createElement("select"); opts.list.forEach(o => { const op = document.createElement("option"); op.value = o; op.textContent = o === "" ? "(eritye)" : o; el.appendChild(op); }); }
  else { el = document.createElement("input"); if (opts && opts.type) el.type = opts.type; if (opts && opts.step) el.step = opts.step; }
  el.value = get() != null ? get() : "";
  const h = () => { set(el.value); };
  if (opts && (opts.list || opts.commit)) el.onchange = h; else el.oninput = h;
  f.appendChild(el); return el;
}
function clipHead(f, c, tk, k) {
  const head = document.createElement("div"); head.style.cssText = "background:#1b1530;border:1px solid var(--line);border-radius:9px;padding:8px;margin-bottom:6px";
  const hb = document.createElement("b"); hb.textContent = "Clip " + k + " sou " + (tk.name || tk.kind); head.appendChild(hb);
  const hs = document.createElement("div"); hs.style.cssText = "color:var(--dim);font-size:11px;margin-top:3px"; hs.textContent = (c.src ? c.src.split("/").pop() : (c.text || c.label || "")); head.appendChild(hs);
  f.appendChild(head);
}
function rngOn(f, obj, lab, key, mn, mx, st, dv) {
  const l = document.createElement("label"); const cur = obj[key] != null ? obj[key] : dv; l.textContent = lab + ": " + cur; f.appendChild(l);
  const r = document.createElement("input"); r.type = "range"; r.min = mn; r.max = mx; r.step = st; r.value = cur;
  r.oninput = () => {
    obj[key] = +r.value;
    l.textContent = lab + ": " + r.value;
    DIRTY = true;
    if (key === "volume" || key === "voice_volume") {
      syncActiveAudioVolumes();
    }
    if (["x", "y", "w", "rotate", "opacity"].indexOf(key) >= 0) {
      renderOvHandle();
      post({ cmd: "updateClip", clip: obj });
    }
  };
  r.onchange = () => {
    if (["x", "y", "w", "rotate", "opacity", "blend"].indexOf(key) >= 0) {
      build();
    }
  };
  f.appendChild(r);
}
// ---- Etalonaj koulè PWOFESYONÈL (clip imaj/videyo) : preview an dirèk sou kanva a ----
function gradeSub(f, t) {
  const d = document.createElement("div"); d.textContent = t;
  d.style.cssText = "font-size:11px;font-weight:800;color:var(--mov);margin:10px 0 2px;border-top:1px solid var(--line);padding-top:8px";
  f.appendChild(d);
}
function gradeRow(f, obj, lab, key, mn, mx, st, dv) {
  const cur = obj[key] != null ? obj[key] : dv;
  const l = document.createElement("label"); l.textContent = lab + ": " + cur; f.appendChild(l);
  const r = document.createElement("input"); r.type = "range"; r.min = mn; r.max = mx; r.step = st; r.value = cur;
  r.oninput = () => { obj[key] = +r.value; l.textContent = lab + ": " + r.value; DIRTY = true; };
  r.onchange = () => build();                      // preview sou kanva a lè w lage slider la
  f.appendChild(r); return r;
}
function gradeUI(f, obj) {
  obj.fx = obj.fx || {};
  const fx = obj.fx;
  // Enhance kalite (sharpen + yon ti kontras/satirasyon/gain otomatik nan rann lan)
  const en = document.createElement("button");
  en.className = fx.enhance ? "pri" : "";
  en.innerHTML = svg("sliders") + (fx.enhance ? "Enhance Kalite: ON" : "Enhance Kalite: OFF");
  en.style.cssText = "width:100%;justify-content:center;margin-bottom:8px";
  en.onclick = () => { fx.enhance = !fx.enhance; if (!fx.enhance) delete fx.enhance; DIRTY = true; renderRight(); build(); msg(obj.fx.enhance ? "Enhance kalite ON (sharpen + klète)" : "Enhance kalite OFF"); };
  f.appendChild(en);
  // Look sinema (LUT) an bouton
  const lab = document.createElement("label"); lab.textContent = "Look sinema (LUT)"; f.appendChild(lab);
  const pw = document.createElement("div"); pw.style.cssText = "display:flex;flex-wrap:wrap;gap:4px;margin-bottom:4px";
  LUTS.forEach(L => {
    const b = document.createElement("button"); b.textContent = L === "" ? "Okenn" : L;
    b.style.cssText = "font-size:10px;padding:3px 7px" + (((obj.lut || "") === L) ? ";background:var(--mov);color:#fff" : "");
    b.onclick = () => { if (L) obj.lut = L; else delete obj.lut; DIRTY = true; renderRight(); build(); msg("LUT: " + (L || "okenn")); };
    pw.appendChild(b);
  });
  f.appendChild(pw);
  gradeSub(f, "Ekspozisyon & ton");
  gradeRow(f, fx, "Ekspozisyon (EV)", "exposure", -2, 2, 0.05, 0);
  gradeRow(f, fx, "Limyè (brightness)", "brightness", 0.2, 2, 0.02, 1);
  gradeRow(f, fx, "Kontras", "contrast", 0.2, 2, 0.02, 1);
  gradeSub(f, "Koulè");
  gradeRow(f, fx, "Temperati (frèt/cho)", "temperature", -100, 100, 1, 0);
  gradeRow(f, fx, "Tint (vèt/majenta)", "tint", -100, 100, 1, 0);
  gradeRow(f, fx, "Satirasyon", "saturate", 0, 3, 0.02, 1);
  gradeRow(f, fx, "Vibrance", "vibrance", 0, 2, 0.02, 1);
  gradeRow(f, fx, "Wotasyon tint (hue)", "hue", -180, 180, 1, 0);
  gradeSub(f, "Wheels — lonbraj / mitan / klète");
  gradeRow(f, fx, "Lift (lonbraj)", "lift", -0.3, 0.3, 0.01, 0);
  gradeRow(f, fx, "Gamma (mitan)", "gamma", 0.3, 2.5, 0.02, 1);
  gradeRow(f, fx, "Gain (klète)", "gain", 0.3, 2.5, 0.02, 1);
  gradeSub(f, "Detay & kalite");
  gradeRow(f, fx, "Sharpen (netete)", "sharpen", 0, 2, 0.05, 0);
  gradeRow(f, fx, "Vignette (kwen fonse)", "vignette", 0, 1, 0.02, 0);
  gradeRow(f, fx, "Blur", "blur", 0, 20, 0.5, 0);
  gradeRow(f, fx, "Gri (grayscale)", "grayscale", 0, 1, 0.05, 0);
  gradeRow(f, fx, "Sepya", "sepia", 0, 1, 0.05, 0);
  const ab = document.createElement("button"); ab.className = "pri"; ab.textContent = "Aplike etalonaj"; ab.style.cssText = "margin-top:10px;width:100%;justify-content:center"; ab.onclick = () => { DIRTY = true; build(); msg("Etalonaj aplike"); }; f.appendChild(ab);
  const rb = document.createElement("button"); rb.textContent = "Reset etalonaj"; rb.style.cssText = "margin-top:6px;width:100%;justify-content:center"; rb.onclick = () => { delete obj.fx; delete obj.lut; DIRTY = true; renderRight(); build(); msg("Etalonaj reset"); }; f.appendChild(rb);
}
// ---- J/L-cut sou clip son: J = son antre avan koup la, L = son kontinye apre ----
function jlCut(c, cut, amt, fade) {
  amt = Math.max(0, +amt || 0); if (!amt) return "pa gen kantite";
  fade = (fade == null) ? Math.min(amt, 0.4) : Math.max(0, Math.min(+fade, amt));
  const start = c.start || 0, dur = c.dur || 0, inn = c.in || 0;
  if (cut === "J") {
    const lead = Math.min(amt, start, inn);
    if (lead <= 0) return "pa gen tèt disponib (trim 'in' oswa deplase clip la adwat anvan)";
    c.start = Math.round((start - lead) * 1000) / 1000;
    c.dur = Math.round((dur + lead) * 1000) / 1000;
    c.in = Math.round((inn - lead) * 1000) / 1000;
    c.fadein = Math.round(Math.max(c.fadein || 0, Math.min(fade, lead)) * 1000) / 1000;
  } else {
    c.dur = Math.round((dur + amt) * 1000) / 1000;
    c.fadeout = Math.round(Math.max(c.fadeout || 0, Math.min(fade, amt)) * 1000) / 1000;
  }
  return "";
}
function jlcutUI(f, c) {
  gradeSub(f, "J/L-cut (dekale son)");
  const note = document.createElement("div"); note.style.cssText = "color:var(--dim);font-size:11px;margin-bottom:6px";
  note.textContent = "J-cut: son antre AVAN imaj la (bezwen tèt — trim clip la). L-cut: son kontinye APRE.";
  f.appendChild(note);
  const wrap = document.createElement("div"); wrap.style.cssText = "display:flex;gap:4px;align-items:center";
  const amt = document.createElement("input"); amt.type = "number"; amt.step = "0.1"; amt.min = "0.1"; amt.value = "0.5"; amt.title = "Segonn"; amt.style.cssText = "width:62px";
  const bj = document.createElement("button"); bj.textContent = "J-cut"; bj.style.cssText = "flex:1;justify-content:center";
  const bl = document.createElement("button"); bl.textContent = "L-cut"; bl.style.cssText = "flex:1;justify-content:center";
  const run = cut => { snapshot(); const err = jlCut(c, cut, amt.value); if (err) { msg("J/L-cut: " + err); } else { DIRTY = true; renderRight(); renderTimeline(); build(); msg(cut + "-cut aplike (" + amt.value + "s)"); } };
  bj.onclick = () => run("J"); bl.onclick = () => run("L");
  wrap.appendChild(amt); wrap.appendChild(bj); wrap.appendChild(bl); f.appendChild(wrap);
}
// ---- Chroma key (green/blue screen) apwoksimatif ----
function chromaRow(f, obj, lab, key, dv) {
  const cur = obj[key] != null ? obj[key] : dv;
  const l = document.createElement("label"); l.textContent = lab + ": " + (+cur).toFixed(2); f.appendChild(l);
  const r = document.createElement("input"); r.type = "range"; r.min = 0; r.max = 1; r.step = 0.01; r.value = cur;
  r.oninput = () => { obj[key] = +r.value; l.textContent = lab + ": " + (+r.value).toFixed(2); DIRTY = true; };
  r.onchange = () => build(); f.appendChild(r);
}
function chromaUI(f, c) {
  gradeSub(f, "Chroma key (green/blue screen)");
  const on = !!c.chroma;
  const tb = document.createElement("button"); tb.className = on ? "pri" : "";
  tb.innerHTML = svg("sliders") + (on ? "Chroma key: ON" : "Chroma key: OFF");
  tb.style.cssText = "width:100%;justify-content:center;margin-bottom:6px";
  tb.onclick = () => { if (c.chroma) delete c.chroma; else c.chroma = { color: "green", amount: 0.5, threshold: 0.2, smooth: 0.2 }; DIRTY = true; renderRight(); build(); msg(c.chroma ? "Chroma key ON (fon vèt retire)" : "Chroma key OFF"); };
  f.appendChild(tb);
  if (c.chroma) {
    const ch = c.chroma;
    const sl = document.createElement("label"); sl.textContent = "Koulè fon an"; f.appendChild(sl);
    const s = document.createElement("select");
    [["green", "Vèt"], ["blue", "Ble"]].forEach(([v, lab]) => { const o = document.createElement("option"); o.value = v; o.textContent = lab; s.appendChild(o); });
    s.value = ch.color || "green"; s.onchange = () => { ch.color = s.value; DIRTY = true; build(); }; f.appendChild(s);
    chromaRow(f, ch, "Fòs (amount)", "amount", 0.5);
    chromaRow(f, ch, "Sèy (threshold)", "threshold", 0.2);
    chromaRow(f, ch, "Dous kontou (smooth)", "smooth", 0.2);
    const note = document.createElement("div"); note.style.cssText = "color:var(--dim);font-size:11px;margin-top:4px"; note.textContent = "Apwoksimatif (HTML→MP4): pi bon ak yon fon ini. Mete yon clip anba pou fon ranplasman."; f.appendChild(note);
  }
}
// ---- Multicam: plizyè kamera (angles) + koup (cuts) sou timeline ----
function multicamUI(f, c) {
  gradeSub(f, "Multicam (plizyè kamera)");
  if (!c.angles || !c.angles.length) {
    const b = document.createElement("button"); b.className = "pri"; b.innerHTML = svg("film") + "Aktive Multicam (ang 1 = clip sa a)";
    b.style.cssText = "width:100%;justify-content:center";
    b.onclick = () => { snapshot(); c.angles = [{ src: c.src, label: "Ang 1" }]; if (c.in != null) c.angles[0].in = c.in; c.cuts = c.cuts || []; DIRTY = true; renderRight(); build(); msg("Multicam aktive"); };
    f.appendChild(b); return;
  }
  const note = document.createElement("div"); note.style.cssText = "color:var(--dim);font-size:11px;margin-bottom:4px";
  note.textContent = "Ajoute kamera, epi mete koup (@ tèt lekti a) pou chanje ang."; f.appendChild(note);
  c.angles.forEach((ang, ai) => {
    const row = document.createElement("div"); row.style.cssText = "display:flex;align-items:center;gap:6px;font-size:11px;padding:3px 4px;border:1px solid var(--line);border-radius:6px;margin-bottom:3px";
    const sp = document.createElement("span"); sp.style.flex = "1"; sp.textContent = "Ang " + (ai + 1) + ": " + ((ang.label) || (ang.src || "").split("/").pop()); row.appendChild(sp);
    const kut = document.createElement("button"); kut.textContent = "Koupe la →"; kut.title = "Ajoute koup sou ang sa a @ tèt lekti a"; kut.style.cssText = "padding:2px 7px";
    kut.onclick = () => { const dur = c.dur || 2, t = Math.max(0, Math.min(1, dur > 0 ? ((CUR - (c.start || 0)) / dur) : 0)); snapshot(); c.cuts = c.cuts || []; c.cuts.push({ t: Math.round(t * 1000) / 1000, a: ai }); c.cuts.sort((x, y) => x.t - y.t); DIRTY = true; renderRight(); build(); msg("koup → Ang " + (ai + 1) + " @ " + (t * 100).toFixed(0) + "%"); };
    row.appendChild(kut);
    if (ai > 0) { const del = document.createElement("button"); del.textContent = "✕"; del.title = "Retire ang"; del.style.cssText = "padding:2px 7px"; del.onclick = () => { snapshot(); c.angles.splice(ai, 1); c.cuts = (c.cuts || []).filter(k => k.a !== ai).map(k => ({ t: k.t, a: k.a > ai ? k.a - 1 : k.a })); DIRTY = true; renderRight(); build(); }; row.appendChild(del); }
    f.appendChild(row);
  });
  const vids = (window.IMPORTED || []).filter(m => /\.(mp4|webm|mov|m4v|mkv)$/i.test(m.rel || m.src || ""));
  const aw = document.createElement("div"); aw.style.cssText = "display:flex;gap:4px;margin:4px 0";
  const sel = document.createElement("select"); sel.style.flex = "1"; const o0 = document.createElement("option"); o0.value = ""; o0.textContent = "— chwazi yon videyo —"; sel.appendChild(o0);
  vids.forEach(m => { const o = document.createElement("option"); o.value = m.rel || m.src; o.textContent = (m.name || m.rel || "").split("/").pop(); sel.appendChild(o); });
  const addb = document.createElement("button"); addb.innerHTML = svg("plus") + "Ajoute ang"; addb.onclick = () => { if (!sel.value) { msg("chwazi yon videyo nan lis la"); return; } snapshot(); c.angles.push({ src: sel.value, label: "Ang " + (c.angles.length + 1) }); DIRTY = true; renderRight(); build(); msg("ang ajoute"); };
  aw.appendChild(sel); aw.appendChild(addb); f.appendChild(aw);
  if (c.cuts && c.cuts.length) {
    gradeSub(f, "Koup yo");
    c.cuts.forEach((k, ci) => {
      const row = document.createElement("div"); row.style.cssText = "display:flex;align-items:center;gap:6px;font-size:11px;padding:2px 4px";
      const sp = document.createElement("span"); sp.style.flex = "1"; sp.textContent = "t=" + (k.t * 100).toFixed(0) + "% → Ang " + (k.a + 1); row.appendChild(sp);
      const del = document.createElement("button"); del.textContent = "✕"; del.style.cssText = "padding:2px 7px"; del.onclick = () => { snapshot(); c.cuts.splice(ci, 1); DIRTY = true; renderRight(); build(); }; row.appendChild(del);
      f.appendChild(row);
    });
  }
  const off = document.createElement("button"); off.textContent = "Dezaktive Multicam"; off.style.cssText = "width:100%;justify-content:center;margin-top:6px"; off.onclick = () => { snapshot(); delete c.angles; delete c.cuts; DIRTY = true; renderRight(); build(); msg("Multicam dezaktive"); }; f.appendChild(off);
}
// ---- Mask (fòm): koupe clip la an sèk / elips / rektang (clip-path) ----
function maskRow(f, obj, lab, key, dv) {
  const cur = obj[key] != null ? obj[key] : dv;
  const l = document.createElement("label"); l.textContent = lab + ": " + (+cur).toFixed(2); f.appendChild(l);
  const r = document.createElement("input"); r.type = "range"; r.min = 0; r.max = 1; r.step = 0.01; r.value = cur;
  r.oninput = () => { obj[key] = +r.value; l.textContent = lab + ": " + (+r.value).toFixed(2); DIRTY = true; };
  r.onchange = () => build(); f.appendChild(r);
}
function maskUI(f, c) {
  gradeSub(f, "Mask (fòm)");
  const sel = document.createElement("label"); sel.textContent = "Fòm mask"; f.appendChild(sel);
  const s = document.createElement("select");
  [["", "Okenn"], ["circle", "Sèk"], ["ellipse", "Elips"], ["inset", "Rektang"]].forEach(([v, lab]) => { const o = document.createElement("option"); o.value = v; o.textContent = lab; s.appendChild(o); });
  s.value = (c.mask && c.mask.shape) || "";
  s.onchange = () => {
    if (!s.value) { delete c.mask; }
    else { c.mask = c.mask || {}; c.mask.shape = s.value; }
    DIRTY = true; renderRight(); build();
  };
  f.appendChild(s);
  if (c.mask && c.mask.shape) {
    const m = c.mask, sh = m.shape;
    if (sh === "circle") { maskRow(f, m, "Reyon (r)", "r", 0.4); maskRow(f, m, "Sant X", "cx", 0.5); maskRow(f, m, "Sant Y", "cy", 0.5); }
    else if (sh === "ellipse") { maskRow(f, m, "Reyon X", "rx", 0.4); maskRow(f, m, "Reyon Y", "ry", 0.3); maskRow(f, m, "Sant X", "cx", 0.5); maskRow(f, m, "Sant Y", "cy", 0.5); }
    else if (sh === "inset") { maskRow(f, m, "Anwo", "top", 0.1); maskRow(f, m, "Adwat", "right", 0.1); maskRow(f, m, "Anba", "bottom", 0.1); maskRow(f, m, "Agoch", "left", 0.1); maskRow(f, m, "Kwen won (radius)", "radius", 0); }
    const rb = document.createElement("button"); rb.textContent = "Retire mask"; rb.style.cssText = "width:100%;justify-content:center;margin-top:6px"; rb.onclick = () => { delete c.mask; DIRTY = true; renderRight(); build(); msg("mask retire"); }; f.appendChild(rb);
  }
}
// ---- Speed ramp (video): vitès kap chanje sou dire clip la (slow-mo pwo) ----
function speedUI(f, c) {
  const start = c.start || 0, dur = c.dur || 2;
  gradeSub(f, "Speed ramp (vitès)");
  const note = document.createElement("div"); note.style.cssText = "color:var(--dim);font-size:11px;margin-bottom:6px";
  note.textContent = "Pwen vitès: v=1 nòmal, v<1 ralanti (slow-mo), v>1 vit."; f.appendChild(note);
  const pr = document.createElement("div"); pr.style.cssText = "display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px";
  const addPreset = (label, keys) => { const b = document.createElement("button"); b.textContent = label; b.style.cssText = "font-size:10px;padding:3px 7px"; b.onclick = () => { snapshot(); c.speedKeys = keys.map(k => ({ ...k })); DIRTY = true; renderRight(); build(); msg("Speed: " + label); }; pr.appendChild(b); };
  addPreset("Slow-mo mitan", [{ t: 0, v: 1 }, { t: 0.5, v: 0.3 }, { t: 1, v: 1 }]);
  addPreset("Vit → dous", [{ t: 0, v: 2 }, { t: 1, v: 0.6 }]);
  addPreset("Dous → vit", [{ t: 0, v: 0.6 }, { t: 1, v: 2 }]);
  f.appendChild(pr);
  const wrap = document.createElement("div"); wrap.style.cssText = "display:flex;gap:4px;align-items:center;margin-bottom:6px";
  const vin = document.createElement("input"); vin.type = "number"; vin.step = "0.1"; vin.min = "0.05"; vin.value = "0.5"; vin.title = "Vitès (v)"; vin.style.cssText = "width:62px";
  const ab = document.createElement("button"); ab.innerHTML = svg("plus") + "Pwen @ tèt lekti"; ab.style.cssText = "flex:1;justify-content:center";
  ab.onclick = () => { const t = Math.max(0, Math.min(1, dur > 0 ? (CUR - start) / dur : 0)); snapshot(); c.speedKeys = c.speedKeys || []; c.speedKeys.push({ t: Math.round(t * 1000) / 1000, v: Math.max(0.05, parseFloat(vin.value) || 1) }); c.speedKeys.sort((a, b) => a.t - b.t); DIRTY = true; renderRight(); build(); msg("pwen vitès @ " + (t * 100).toFixed(0) + "% · v=" + vin.value); };
  wrap.appendChild(vin); wrap.appendChild(ab); f.appendChild(wrap);
  if (c.speedKeys && c.speedKeys.length) {
    c.speedKeys.forEach((k, idx) => {
      const row = document.createElement("div"); row.style.cssText = "display:flex;align-items:center;gap:6px;font-size:11px;padding:3px 4px;border:1px solid var(--line);border-radius:6px;margin-bottom:3px";
      const sp = document.createElement("span"); sp.style.flex = "1"; sp.textContent = "t=" + (k.t * 100).toFixed(0) + "% · v=" + (+k.v).toFixed(2); row.appendChild(sp);
      const del = document.createElement("button"); del.textContent = "✕"; del.title = "Efase pwen vitès"; del.style.cssText = "padding:2px 7px"; del.onclick = () => { snapshot(); c.speedKeys.splice(idx, 1); if (!c.speedKeys.length) delete c.speedKeys; DIRTY = true; renderRight(); build(); }; row.appendChild(del);
      f.appendChild(row);
    });
    const cb = document.createElement("button"); cb.textContent = "Efase speed ramp"; cb.style.cssText = "width:100%;justify-content:center;margin-top:4px"; cb.onclick = () => { snapshot(); delete c.speedKeys; DIRTY = true; renderRight(); build(); msg("speed ramp efase"); }; f.appendChild(cb);
  }
}
// ---- Keyframes (animasyon clip): anime x/y/rotate/scale/opacity sou dire a ----
function kfUI(f, c) {
  const start = c.start || 0, dur = c.dur || 2;
  gradeSub(f, "Animasyon (keyframes)");
  const note = document.createElement("div"); note.style.cssText = "color:var(--dim);font-size:11px;margin-bottom:6px";
  note.textContent = "Keyframes anime pozisyon / wotasyon / eskal / opasite sou dire clip la."; f.appendChild(note);
  const pr = document.createElement("div"); pr.style.cssText = "display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px";
  const addPreset = (label, keys) => { const b = document.createElement("button"); b.textContent = label; b.style.cssText = "font-size:10px;padding:3px 7px"; b.onclick = () => { snapshot(); c.keys = keys.map(k => ({ ...k })); DIRTY = true; renderRight(); build(); msg("Animasyon: " + label); }; pr.appendChild(b); };
  addPreset("Zoom (Ken Burns)", [{ t: 0, scale: 1 }, { t: 1, scale: 1.15 }]);
  addPreset("Glise →", [{ t: 0, x: 0.35 }, { t: 1, x: 0.65 }]);
  addPreset("Fade in", [{ t: 0, opacity: 0 }, { t: 0.15, opacity: 1 }]);
  addPreset("Fade out", [{ t: 0.85, opacity: 1 }, { t: 1, opacity: 0 }]);
  f.appendChild(pr);
  const ab = document.createElement("button"); ab.innerHTML = svg("plus") + "Ajoute keyframe @ tèt lekti a"; ab.style.cssText = "width:100%;justify-content:center;margin-bottom:6px";
  ab.onclick = () => { const t = Math.max(0, Math.min(1, dur > 0 ? (CUR - start) / dur : 0)); snapshot(); c.keys = c.keys || []; c.keys.push({ t: Math.round(t * 1000) / 1000, x: c.x != null ? c.x : 0.5, y: c.y != null ? c.y : 0.5, rotate: c.rotate || 0, scale: c.scale != null ? c.scale : 1, opacity: c.opacity != null ? c.opacity : 1 }); c.keys.sort((a, b) => a.t - b.t); DIRTY = true; renderRight(); build(); msg("keyframe ajoute @ " + (t * 100).toFixed(0) + "%"); };
  f.appendChild(ab);
  if (c.keys && c.keys.length) {
    c.keys.forEach((k, idx) => {
      const row = document.createElement("div"); row.style.cssText = "display:flex;align-items:center;gap:6px;font-size:11px;padding:3px 4px;border:1px solid var(--line);border-radius:6px;margin-bottom:3px";
      const parts = []; ["x", "y", "rotate", "scale", "opacity"].forEach(p => { if (k[p] != null) parts.push(p[0] + ":" + (+k[p]).toFixed(2)); });
      const sp = document.createElement("span"); sp.style.flex = "1"; sp.textContent = "t=" + (k.t * 100).toFixed(0) + "% · " + parts.join(" "); row.appendChild(sp);
      const ez = document.createElement("select"); ez.title = "Ease / koub (segman ki soti nan kle sa a)"; ez.style.cssText = "font-size:10px;padding:1px 2px;width:auto";
      [["", "Lineyè"], ["in", "Ease-in"], ["out", "Ease-out"], ["inout", "Ease-io"]].forEach(([v, lab]) => { const o = document.createElement("option"); o.value = v; o.textContent = lab; ez.appendChild(o); });
      ez.value = (typeof k.ease === "string") ? k.ease : "";
      ez.onchange = () => { if (ez.value) k.ease = ez.value; else delete k.ease; DIRTY = true; build(); }; row.appendChild(ez);
      const del = document.createElement("button"); del.textContent = "✕"; del.title = "Efase keyframe sa a"; del.style.cssText = "padding:2px 7px"; del.onclick = () => { snapshot(); c.keys.splice(idx, 1); if (!c.keys.length) delete c.keys; DIRTY = true; renderRight(); build(); }; row.appendChild(del);
      f.appendChild(row);
    });
    const cb = document.createElement("button"); cb.textContent = "Efase tout keyframes"; cb.style.cssText = "width:100%;justify-content:center;margin-top:4px"; cb.onclick = () => { snapshot(); delete c.keys; DIRTY = true; renderRight(); build(); msg("keyframes efase"); }; f.appendChild(cb);
  }
}
function fxUI(f, obj) {
  obj.fx = obj.fx || {};
  rngOn(f, obj.fx, "Blur (px)", "blur", 0, 20, 0.5, 0);
  rngOn(f, obj.fx, "Limye (brightness)", "brightness", 0.2, 2, 0.05, 1);
  rngOn(f, obj.fx, "Kontras", "contrast", 0.2, 2, 0.05, 1);
  rngOn(f, obj.fx, "Satirasyon", "saturate", 0, 3, 0.05, 1);
  rngOn(f, obj.fx, "Gri (grayscale)", "grayscale", 0, 1, 0.05, 0);
  rngOn(f, obj.fx, "Sepya", "sepia", 0, 1, 0.05, 0);
  const ab = document.createElement("button"); ab.className = "pri"; ab.textContent = "Aplike efe"; ab.style.cssText = "margin-top:10px;width:100%;justify-content:center"; ab.onclick = () => { DIRTY = true; build(); msg("Efe aplike sou eleman an"); }; f.appendChild(ab);
  const rb = document.createElement("button"); rb.textContent = "Reset efe"; rb.style.cssText = "margin-top:6px;width:100%;justify-content:center"; rb.onclick = () => { delete obj.fx; DIRTY = true; renderRight(); build(); }; f.appendChild(rb);
}
const LUTS = ["", "sinema", "cho", "fret", "vintage", "nwa-blan", "sepya", "dramatik", "pastel", "teal-orange"];
function lutUI(f, obj) {
  field(f, "LUT / Look", () => obj.lut || "", v => { if (v) obj.lut = v; else delete obj.lut; DIRTY = true; build(); msg("LUT '" + v + "' aplike"); }, { list: LUTS });
  const n = document.createElement("div"); n.style.cssText = "color:var(--dim);font-size:11px;margin-top:8px"; n.textContent = "Look koule sinematik aplike sou medya a (rann nan ekspo a)."; f.appendChild(n);
}
function renderClipTab(f) {
  f.innerHTML = "";
  const cl = CLIPSEL, tk = SPEC.tracks[cl.t], c = tk.clips[cl.c], k = c.kind || c.type || "";
  clipHead(f, c, tk, k);
  const vis = ["image", "video", "text", "asset"].indexOf(k) >= 0;
  if (RT === "props") {
    if (c.src && /\.(png|jpe?g|gif|webp|svg|bmp)$/i.test(c.src)) { const im = document.createElement("img"); im.src = c.src; im.style.cssText = "width:100%;max-height:120px;object-fit:contain;background:#0e0b1a;border:1px solid var(--line);border-radius:8px;margin-bottom:6px"; f.appendChild(im); }
    field(f, "Non (label)", () => c.label, v => { c.label = v; DIRTY = true; renderTimeline(); });
    field(f, "Depa (start, s)", () => (c.start != null ? c.start : 0), v => { snapshot(); c.start = Math.max(0, parseFloat(v) || 0); DIRTY = true; renderTimeline(); }, { type: "number", step: "0.1", commit: 1 });
    field(f, "Dire (dur, s)", () => (c.dur != null ? c.dur : 2), v => { snapshot(); c.dur = Math.max(0.3, parseFloat(v) || 2); DIRTY = true; renderTimeline(); }, { type: "number", step: "0.1", commit: 1 });
    if (k === "text") field(f, "Teks", () => (c.text || c.label || ""), v => { c.text = v; c.label = v; DIRTY = true; renderTimeline(); }, { multi: 1 });
    if (vis) { rngOn(f, c, "Pozisyon X", "x", 0, 1, 0.01, 0.5); rngOn(f, c, "Pozisyon Y", "y", 0, 1, 0.01, 0.5); rngOn(f, c, "Gwose (scale)", "w", 0.05, 1, 0.01, (k === "text" ? 0.5 : 1)); rngOn(f, c, "Wotasyon", "rotate", -180, 180, 1, 0); kfUI(f, c); maskUI(f, c); if (k === "video") speedUI(f, c); if (k === "video" || k === "image") chromaUI(f, c); if (k === "video") multicamUI(f, c); }
  } else if (RT === "color") {
    if (k === "text") colorRow(f, "Koule teks", () => c.color || "#ffffff", v => { c.color = v; DIRTY = true; });
    else if (k === "image" || k === "video" || k === "asset") {
      if (k === "asset" || k === "image") colorRow(f, "Koule (recolor)", () => c.color || "#ffffff", v => { c.color = v; DIRTY = true; build(); });
      gradeUI(f, c);
    } else { const n = document.createElement("div"); n.style.cssText = "color:var(--dim);font-size:12px"; n.textContent = "Pa gen koule pou tip clip sa a."; f.appendChild(n); }
  } else if (RT === "blend") {
    if (vis) {
      field(f, "Mode blend", () => c.blend || "normal", v => { c.blend = v; DIRTY = true; }, { list: BLENDS });
      rngOn(f, c, "Opasite", "opacity", 0, 1, 0.05, 1);
      const ch = document.createElement("label"); ch.style.cssText = "display:flex;align-items:center;gap:8px;margin:10px 0;cursor:pointer;color:var(--fg)"; const cx = document.createElement("input"); cx.type = "checkbox"; cx.style.width = "auto"; cx.checked = !!c.shadow; cx.onchange = () => { c.shadow = cx.checked; DIRTY = true; renderRight(); }; ch.appendChild(cx); ch.appendChild(document.createTextNode("Lonbraj (shadow)")); f.appendChild(ch);
      if (c.shadow) { rngOn(f, c, "Lonbraj blur", "shadowBlur", 0, 50, 1, 10); colorRow(f, "Koule lonbraj", () => c.shadowColor || "#000000", v => { c.shadowColor = v; DIRTY = true; }); }
    } else { const n = document.createElement("div"); n.style.cssText = "color:var(--dim);font-size:12px"; n.textContent = "Blend se pou medya vizyel."; f.appendChild(n); }
  } else if (RT === "sound") {
    if (["audio", "video", "sfx", "music", "voice"].indexOf(k) >= 0) {
      rngOn(f, c, "Volim clip (" + (k.toUpperCase()) + ")", "volume", 0, 2, 0.05, 1);
      rngOn(f, c, "Fade in (s)", "fadein", 0, 5, 0.1, 0);
      rngOn(f, c, "Fade out (s)", "fadeout", 0, 5, 0.1, 0);
      const pbtn = document.createElement("button");
      pbtn.style.cssText = "margin-top:10px;width:100%;justify-content:center";
      pbtn.innerHTML = svg("volume") + "Tande son an (Preview)";
      pbtn.onclick = () => {
        if (c.sfx) playSfxSynth(c.sfx);
        else if (c.src) {
          const a = new Audio(withTok(c.src));
          const mvol = (SPEC && SPEC.volume != null) ? SPEC.volume : 1;
          a.volume = Math.max(0, Math.min(1, (c.volume != null ? c.volume : 1) * mvol));
          a.play().catch(() => {});
        }
      };
      f.appendChild(pbtn);
      if (["audio", "music", "voice", "sfx"].indexOf(k) >= 0) jlcutUI(f, c);
    } else {
      const n = document.createElement("div"); n.style.cssText = "color:var(--dim);font-size:12px"; n.textContent = "Pa gen son pou clip sa a."; f.appendChild(n);
    }
  } else if (RT === "effect") { fxUI(f, c); }
  else if (RT === "lut") { lutUI(f, c); }
  const rm = document.createElement("button"); rm.innerHTML = svg("trash") + "Efase clip"; rm.style.cssText = "margin-top:12px;width:100%;justify-content:center"; rm.onclick = () => { snapshot(); tk.clips.splice(cl.c, 1); CLIPSEL = null; DIRTY = true; renderTimeline(); renderRight(); renderLeft(); }; f.appendChild(rm);
}
function renderEffect(f) { f.innerHTML = ""; const h = document.createElement("h3"); h.textContent = "Efe"; h.style.cssText = "color:var(--mov);margin:0 0 6px;font-size:14px"; f.appendChild(h); if (SEL < 0 || !SPEC.scenes[SEL]) { const d = document.createElement("div"); d.style.color = "var(--dim)"; d.textContent = "Chwazi yon sen oswa clip."; f.appendChild(d); return; } fxUI(f, SPEC.scenes[SEL]); }
function renderLut(f) { f.innerHTML = ""; const h = document.createElement("h3"); h.textContent = "LUT / Look"; h.style.cssText = "color:var(--mov);margin:0 0 6px;font-size:14px"; f.appendChild(h); if (SEL < 0 || !SPEC.scenes[SEL]) { const d = document.createElement("div"); d.style.color = "var(--dim)"; d.textContent = "Chwazi yon sen oswa clip."; f.appendChild(d); return; } lutUI(f, SPEC.scenes[SEL]); }

function renderProps(f) {
  if (CLIPSEL) return renderClipProps(f);
  f.innerHTML = "";
  if (TRACKSEL && TRACKSEL.indexOf("tk") === 0) {
    const ti = +TRACKSEL.slice(2);
    const tk = SPEC.tracks && SPEC.tracks[ti];
    if (tk) {
      const def = tracksDef().find(d => d.key === TRACKSEL) || { key: TRACKSEL, name: tk.name || tk.kind, kind: tk.kind, track: ti, color: tk.color || "#8b5cf6" };
      const tcard = document.createElement("div");
      tcard.style.cssText = "background:#1b1530;border:1px solid " + def.color + "88;border-radius:9px;padding:10px;margin-bottom:10px";
      tcard.innerHTML = '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px"><b style="color:' + def.color + '">Track: ' + esc(tk.name || tk.kind) + ' (' + esc(tk.kind) + ')</b><span style="font-size:11px;color:var(--dim)">' + ((tk.clips && tk.clips.length) || 0) + ' clip</span></div>';
      const btnRow = document.createElement("div");
      btnRow.style.cssText = "display:flex;gap:6px;flex-wrap:wrap";
      const bAdd = document.createElement("button");
      bAdd.className = "pri";
      bAdd.style.cssText = "flex:1;justify-content:center;font-size:11px";
      bAdd.innerHTML = svg("plus") + (tk.kind === "text" ? "Ajoute Tèks" : "Ajoute Medya / Clip");
      bAdd.onclick = () => promptAddClipToTrack(ti);
      btnRow.appendChild(bAdd);
      if (tk.kind !== "audio" && tk.kind !== "sfx" && tk.kind !== "text") {
        const bTxt = document.createElement("button");
        bTxt.style.cssText = "flex:1;justify-content:center;font-size:11px";
        bTxt.innerHTML = svg("text") + "Ajoute Tèks";
        bTxt.onclick = () => {
          const txt = prompt("Tèks pou mete sou track la:", "Nouvo Tèks");
          if (!txt) return;
          snapshot(); tk.clips = tk.clips || [];
          const st = freeStart(tk, CUR, 3);
          tk.clips.push({ type: "text", kind: "text", text: txt, label: txt, start: st, dur: 3, x: 0.5, y: 0.5, w: 0.5, color: "#ffffff" });
          DIRTY = true; CLIPSEL = { t: ti, c: tk.clips.length - 1 };
          renderTimeline(); renderRight(); build();
        };
        btnRow.appendChild(bTxt);
      }
      tcard.appendChild(btnRow);
      const btnRow2 = document.createElement("div");
      btnRow2.style.cssText = "display:flex;gap:6px;margin-top:6px";
      const bRen = document.createElement("button"); bRen.style.cssText = "flex:1;justify-content:center;font-size:11px"; bRen.textContent = "✏️ Non"; bRen.onclick = () => renameTrack(def);
      const bCol = document.createElement("button"); bCol.style.cssText = "flex:1;justify-content:center;font-size:11px"; bCol.textContent = "🎨 Koulè"; bCol.onclick = () => trackColorPopup(def);
      const bDel = document.createElement("button"); bDel.style.cssText = "flex:1;justify-content:center;font-size:11px;color:#ff8a8a"; bDel.textContent = "🗑️ Efase"; bDel.onclick = () => deleteTrack(def);
      btnRow2.appendChild(bRen); btnRow2.appendChild(bCol); btnRow2.appendChild(bDel);
      tcard.appendChild(btnRow2);
      f.appendChild(tcard);
    }
  }
  if (SEL < 0 || !SPEC.scenes[SEL]) {
    if (!f.children.length) f.innerHTML = '<div style="color:var(--dim)">Chwazi yon sèn oswa yon clip nan timeline a.</div>';
    return;
  }
  const sc = SPEC.scenes[SEL];
  const head = document.createElement("div"); head.style.cssText = "background:#1b1530;border:1px solid var(--line);border-radius:9px;padding:8px;margin-bottom:6px";
  head.innerHTML = '<b>Sen ' + (SEL + 1) + " / " + esc(sc.type) + '</b><div style="color:var(--dim);font-size:11px;margin-top:3px">dire: ' + sDur(SEL).toFixed(1) + "s / depa: " + sStart(SEL).toFixed(1) + "s" + (sc.voice ? " / gen vwa lokal" : "") + "</div>"; f.appendChild(head);
  const D = () => { DIRTY = true; };
  field(f, "Tit (title)", () => sc.title, v => { if (v) sc.title = v; else delete sc.title; D(); renderTimeline(); });
  field(f, "Sou-tit (subtitle)", () => sc.subtitle, v => { if (v) sc.subtitle = v; else delete sc.subtitle; D(); });
  field(f, "Deskripsyon / tagline", () => sc.tagline, v => { if (v) sc.tagline = v; else delete sc.tagline; D(); }, { multi: 1 });
  field(f, "Mesaj narasyon / vwa lokal (voice)", () => sc.voice, v => { if (v) sc.voice = v; else delete sc.voice; sc._regen = true; D(); renderTimeline(); }, { multi: 1 });
  field(f, "Dire (s, vid = oto)", () => sc.duration, v => { snapshot(); const n = parseFloat(v); if (isNaN(n) || n <= 0) delete sc.duration; else sc.duration = n; D(); renderTimeline(); }, { type: "number", step: "0.1", commit: 1 });
  field(f, "Tranzisyon", () => sc.transition || "", v => { if (v) sc.transition = v; else delete sc.transition; D(); build(); }, { list: TRANSITIONS });
  field(f, "Layout", () => sc.layout || "", v => { if (v) sc.layout = v; else delete sc.layout; D(); }, { list: ["", "window"] });
  SPEC.brand = SPEC.brand || {};
  field(f, "Stil tit (font tout videyo a)", () => SPEC.brand.font_title || "", v => { if (v) SPEC.brand.font_title = v; else delete SPEC.brand.font_title; D(); build(); }, { list: FONT_STYLES });
  field(f, "Bann dèyè tit (lizibilite)", () => (sc.title_backdrop === true ? "true" : (sc.title_backdrop === "auto" ? "auto" : "")), v => { if (v === "true") sc.title_backdrop = true; else if (v === "auto") sc.title_backdrop = "auto"; else delete sc.title_backdrop; D(); build(); }, { list: ["", "auto", "true"] });
  const vb = document.createElement("button"); vb.style.marginTop = "8px"; vb.style.width = "100%"; vb.style.justifyContent = "center";
  vb.textContent = sc.voice ? "Vwa: ON - klike pou OFF (silans)" : "Vwa: OFF (silans) - klike pou ON";
  vb.onclick = () => { snapshot(); if (sc.voice) { sc._voicebak = sc.voice; delete sc.voice; } else if (sc._voicebak) { sc.voice = sc._voicebak; delete sc._voicebak; } D(); renderProps(f); renderTimeline(); };
  f.appendChild(vb);
}
let FONT_STYLES = ["", "Segoe UI", "Arial", "Georgia", "Impact"];   // ranpli ak vrè font PC a (loadFonts)

const PALETTE = ["#000000","#ffffff","#8b5cf6","#6d28d9","#c4b5fd","#0098ff","#1e6fd9","#22d3ee","#21a366","#84cc16",
  "#facc15","#f59e0b","#ff8a3d","#ef4444","#ec4899","#a855f7","#64748b","#1e293b","#0b0816","#f3eefe"];
function colorRow(f, label, get, set) {
  const l = document.createElement("label"); l.textContent = label; f.appendChild(l);
  const row = document.createElement("div"); row.style.cssText = "display:flex;gap:6px;align-items:center";
  const cur = (get() || "#000000");
  const pick = document.createElement("input"); pick.type = "color"; pick.value = /^#[0-9a-f]{6}$/i.test(cur) ? cur : "#000000"; pick.style.cssText = "width:40px;height:32px;padding:0";
  const hex = document.createElement("input"); hex.value = cur; hex.style.flex = "1";
  const apply = v => { set(v); hex.value = v; if (/^#[0-9a-f]{6}$/i.test(v)) pick.value = v; DIRTY = true; };
  pick.oninput = () => apply(pick.value); hex.onchange = () => apply(hex.value);
  row.appendChild(pick); row.appendChild(hex); f.appendChild(row);
  const sw = document.createElement("div"); sw.className = "swatches";
  PALETTE.forEach(c => { const s = document.createElement("div"); s.className = "sw"; s.style.background = c; s.title = c; s.onclick = () => apply(c); sw.appendChild(s); });
  f.appendChild(sw);
}
function renderColor(f) {
  f.innerHTML = "";
  const h = document.createElement("h3"); h.innerHTML = svg("palette") + " Koule mak la (tout videyo a)"; f.appendChild(h);
  SPEC.brand = SPEC.brand || {}; SPEC.brand.colors = SPEC.brand.colors || {};
  const C = SPEC.brand.colors;
  colorRow(f, "Fon (bg)", () => C.bg, v => { C.bg = v; build(); });
  colorRow(f, "Primè (primary)", () => C.primary, v => { C.primary = v; build(); });
  colorRow(f, "Aksan (accent)", () => C.accent, v => { C.accent = v; build(); });
  colorRow(f, "Teks (text)", () => C.text, v => { C.text = v; build(); });
  if (SEL >= 0 && SPEC.scenes[SEL]) {
    const sc = SPEC.scenes[SEL];
    const h2 = document.createElement("h3"); h2.innerHTML = svg("image") + " Fon sen " + (SEL + 1); f.appendChild(h2);
    colorRow(f, "Koule fon sen an", () => (sc.background && sc.background.color) || "", v => { sc.background = (typeof sc.background === "object" && sc.background) || {}; sc.background.color = v; build(); });
  }
}

const BLENDS = ["normal","dissolve","darken","multiply","color-burn","linear-burn","darker-color",
  "lighten","screen","color-dodge","linear-dodge","lighter-color","overlay","soft-light","hard-light",
  "vivid-light","linear-light","pin-light","hard-mix","difference","exclusion","subtract","divide",
  "hue","saturation","color","luminosity","reflect","glow","negation","xor"];
function renderBlend(f) {
  f.innerHTML = "";
  if (SEL < 0 || !SPEC.scenes[SEL]) { f.innerHTML = '<div style="color:var(--dim)">Chwazi yon sen. Trene yon asset sou li pou ajoute yon kouch.</div>'; return; }
  const sc = SPEC.scenes[SEL]; sc.overlays = sc.overlays || [];
  const h = document.createElement("h3"); h.innerHTML = svg("layers") + " Kouch & blend (sen " + (SEL + 1) + ")"; f.appendChild(h);
  if (!sc.overlays.length) { const d = document.createElement("div"); d.style.cssText = "color:var(--dim);font-size:12px"; d.textContent = "Pa gen kouch. Trene yon asset sou viewer a oswa sen an."; f.appendChild(d); }
  sc.overlays.forEach((ov, oi) => {
    const box = document.createElement("div"); box.style.cssText = "background:#1b1530;border:1px solid var(--line);border-radius:9px;padding:8px;margin-bottom:7px";
    box.innerHTML = '<div style="display:flex;align-items:center;gap:6px"><b style="flex:1;font-size:12px;overflow:hidden;text-overflow:ellipsis">' + esc((ov.src || "kouch").split("/").pop()) + '</b></div>';
    if (OVSEL && OVSEL.o === oi) box.style.outline = "1px solid var(--mov)";
    box.style.cursor = "pointer"; box.onclick = () => { OVSEL = { s: SEL, o: oi }; renderOvHandle(); renderRight(); };
    f.appendChild(box);
    field(box, "Mode blend", () => ov.blend || "normal", v => { ov.blend = v; DIRTY = true; build(); }, { list: BLENDS });
    const ol = document.createElement("label"); ol.textContent = "Opasite " + Math.round((ov.opacity != null ? ov.opacity : 1) * 100) + "%"; box.appendChild(ol);
    const or = document.createElement("input"); or.type = "range"; or.min = 0; or.max = 1; or.step = 0.05; or.value = ov.opacity != null ? ov.opacity : 1;
    or.oninput = () => { ov.opacity = +or.value; ol.textContent = "Opasite " + Math.round(or.value * 100) + "%"; DIRTY = true; };
    or.onchange = build; box.appendChild(or);
    const addRange = (lab, key, mn, mx, st, dv) => {
      const ll = document.createElement("label"); const cur = ov[key] != null ? ov[key] : dv; ll.textContent = lab + ": " + cur; box.appendChild(ll);
      const rr = document.createElement("input"); rr.type = "range"; rr.min = mn; rr.max = mx; rr.step = st; rr.value = cur;
      rr.oninput = () => { ov[key] = +rr.value; ll.textContent = lab + ": " + (+rr.value).toFixed(2); DIRTY = true; };
      rr.onchange = build; box.appendChild(rr);
    };
    addRange("Pozisyon X", "x", 0, 1, 0.01, 0.5);
    addRange("Pozisyon Y", "y", 0, 1, 0.01, 0.5);
    addRange("Gwosè (w)", "w", 0.05, 1, 0.01, 0.3);
    addRange("Wotasyon", "rotate", -180, 180, 1, 0);
    colorRow(box, "Koule (recolor asset)", () => ov.color || "", v => { if (v) ov.color = v; else delete ov.color; DIRTY = true; build(); });
    const rm = document.createElement("button"); rm.innerHTML = svg("trash") + "Retire kouch"; rm.style.cssText = "margin-top:8px;width:100%;justify-content:center"; rm.onclick = () => { snapshot(); sc.overlays.splice(oi, 1); DIRTY = true; renderRight(); build(); }; box.appendChild(rm);
  });
}

// ---- Son: mikser pwofesyonel (Master, Compressor/EQ vwa, Mizik, Soutit) ----
function renderSound(f) {
  f.innerHTML = "";
  SPEC.voice = SPEC.voice || {}; const V = SPEC.voice;
  const h = document.createElement("h3"); h.innerHTML = svg("mic") + " Vwa (Master / Compressor / EQ)"; f.appendChild(h);
  const vu = document.createElement("div"); vu.className = "vu"; vu.innerHTML = "<i></i>"; f.appendChild(vu);
  const en = document.createElement("label"); en.style.cssText = "display:flex;align-items:center;gap:8px;cursor:pointer";
  const cb = document.createElement("input"); cb.type = "checkbox"; cb.style.width = "auto"; cb.checked = V.enhance !== false;
  cb.onchange = () => { V.enhance = cb.checked; DIRTY = true; }; en.appendChild(cb);
  en.appendChild(document.createTextNode("Compressor + EQ + de-esser + limiter (netwaye vwa a)")); f.appendChild(en);
  const cbtn = document.createElement("button"); cbtn.innerHTML = svg("sliders") + "Compressor (regle nan popup)"; cbtn.style.cssText = "margin-top:6px;width:100%;justify-content:center"; cbtn.onclick = openCompressor; f.appendChild(cbtn);
  field(f, "Sèks vwa", () => V.gender || "female", v => { V.gender = v; DIRTY = true; }, { list: ["female", "male"] });
  field(f, "Lang vwa", () => V.lang || "", v => { if (v) V.lang = v; else delete V.lang; DIRTY = true; }, { list: ["", "ht", "fr", "en", "es", "pt", "ru", "it", "de"] });

  if (SEL >= 0 && SPEC.scenes[SEL]) {
    const sc = SPEC.scenes[SEL];
    if (sc.type === "video") {
      const hvid = document.createElement("h3"); hvid.innerHTML = svg("film") + " Odyo videyo sèn " + (SEL + 1); f.appendChild(hvid);
      const vvl = document.createElement("label");
      const curVidAudio = (typeof sc.audio === "number") ? sc.audio : (sc.audio === false ? 0 : 0.9);
      vvl.textContent = "Volim videyo: " + Math.round(curVidAudio * 100) + "%"; f.appendChild(vvl);
      const vvr = document.createElement("input"); vvr.type = "range"; vvr.min = 0; vvr.max = 1.5; vvr.step = 0.05; vvr.value = curVidAudio;
      vvr.oninput = () => {
        sc.audio = +vvr.value;
        vvl.textContent = "Volim videyo: " + Math.round(vvr.value * 100) + "%";
        DIRTY = true;
        syncActiveAudioVolumes();
      };
      f.appendChild(vvr);
    }
    if (sc.voice || sc.voice_file) {
      const hv = document.createElement("h3"); hv.innerHTML = svg("mic") + " Vwa lokal sèn " + (SEL + 1); f.appendChild(hv);
      const vvolL = document.createElement("label");
      const curVv = (typeof sc.voice_volume === "number") ? sc.voice_volume : 1;
      vvolL.textContent = "Volim vwa sèn: " + Math.round(curVv * 100) + "%"; f.appendChild(vvolL);
      const vvolR = document.createElement("input"); vvolR.type = "range"; vvolR.min = 0; vvolR.max = 1.5; vvolR.step = 0.05; vvolR.value = curVv;
      vvolR.oninput = () => {
        sc.voice_volume = +vvolR.value;
        vvolL.textContent = "Volim vwa sèn: " + Math.round(vvolR.value * 100) + "%";
        DIRTY = true;
        syncActiveAudioVolumes();
      };
      f.appendChild(vvolR);
    }
  }

  const h2 = document.createElement("h3"); h2.innerHTML = svg("music") + " Mizik fon"; f.appendChild(h2);
  const mon = document.createElement("label"); mon.style.cssText = "display:flex;align-items:center;gap:8px;cursor:pointer";
  const mcb = document.createElement("input"); mcb.type = "checkbox"; mcb.style.width = "auto"; mcb.checked = !!SPEC.music;
  mcb.onchange = () => { if (mcb.checked) SPEC.music = SPEC.music || { mood: "upbeat", volume: 0.22 }; else SPEC.music = null; DIRTY = true; syncActiveAudioVolumes(); renderTimeline(); renderRight(); }; mon.appendChild(mcb);
  mon.appendChild(document.createTextNode("Aktive mizik fon")); f.appendChild(mon);
  if (SPEC.music) {
    field(f, "Imè (mood)", () => SPEC.music.mood || "upbeat", v => { SPEC.music.mood = v; DIRTY = true; }, { list: ["upbeat", "calm", "epic", "tech"] });
    const vl = document.createElement("label"); const vv = SPEC.music.volume != null ? SPEC.music.volume : 0.22;
    vl.textContent = "Volim mizik " + Math.round(vv * 100) + "%"; f.appendChild(vl);
    const vr = document.createElement("input"); vr.type = "range"; vr.min = 0; vr.max = 1; vr.step = 0.02; vr.value = vv;
    vr.oninput = () => {
      SPEC.music.volume = +vr.value;
      vl.textContent = "Volim mizik " + Math.round(vr.value * 100) + "%";
      DIRTY = true;
      syncActiveAudioVolumes();
    };
    f.appendChild(vr);
  }
  const h3 = document.createElement("h3"); h3.innerHTML = svg("text") + " Soutit (captions)"; f.appendChild(h3);
  const con = document.createElement("label"); con.style.cssText = "display:flex;align-items:center;gap:8px;cursor:pointer";
  const ccb = document.createElement("input"); ccb.type = "checkbox"; ccb.style.width = "auto"; ccb.checked = !!SPEC.captions;
  ccb.onchange = () => { if (ccb.checked) SPEC.captions = SPEC.captions || { style: "karaoke", position: "bottom" }; else delete SPEC.captions; DIRTY = true; renderRight(); }; con.appendChild(ccb);
  con.appendChild(document.createTextNode("Montre soutit otomatik")); f.appendChild(con);
  if (SPEC.captions) {
    field(f, "Estil soutit", () => SPEC.captions.style || "karaoke", v => { SPEC.captions.style = v; DIRTY = true; }, { list: ["karaoke", "pop"] });
    field(f, "Pozisyon soutit", () => SPEC.captions.position || "bottom", v => { SPEC.captions.position = v; DIRTY = true; }, { list: ["bottom", "center", "top"] });
  }
}

// ---- Zouti + Track + Keyframe ----
function setTool(t) {
  TOOL = t;
  const selBtn = $("#tSelect");
  if (selBtn) selBtn.classList.toggle("on", t === "select");
}
function doTool(t) {
  if (t === "selleft") { if (SEL > 0) selectScene(SEL - 1); setTool("select"); }
  else if (t === "selright") { if (SEL >= 0 && SEL < SPEC.scenes.length - 1) selectScene(SEL + 1); setTool("select"); }
  else setTool(t);
}

function splitActive() {
  if (CLIPSEL && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) {
    const tk = SPEC.tracks[CLIPSEL.t], c = tk.clips[CLIPSEL.c];
    if (CUR > (c.start || 0) + 0.08 && CUR < (c.start || 0) + (c.dur || 2) - 0.08) {
      snapshot();
      const rel = CUR - (c.start || 0);
      const copy = JSON.parse(JSON.stringify(c));
      c.dur = Math.round(rel * 100) / 100;
      copy.start = CUR;
      copy.dur = Math.round((copy.dur - rel) * 100) / 100;
      if (c.src) copy.in = Math.round(((c.in || 0) + rel * (c.speed || 1)) * 1000) / 1000;   // 2yèm moso a kòmanse KOTE koupe a
      tk.clips.splice(CLIPSEL.c + 1, 0, copy);
      DIRTY = true; renderTimeline(); renderRight();
      msg("Clip divize sou track @ " + CUR.toFixed(2) + "s");
      return;
    }
  }
  const idx = (SEL >= 0 ? SEL : sceneAt(CUR));
  const sc = SPEC.scenes[idx];
  if (!sc) { msg("Chwazi yon sen oswa clip pou divize"); return; }
  const dur = sDur(idx);
  const rel = CUR - sStart(idx);
  if (rel < 0.1 || rel > dur - 0.1) { msg("Mete tèt lekti a nan mitan sèn nan pou divize l"); return; }
  snapshot();
  const copy = JSON.parse(JSON.stringify(sc));
  copy.id = (sc.id || "s") + "_b" + Math.random().toString(36).slice(2, 5);
  sc.duration = Math.round(rel * 100) / 100;
  copy.duration = Math.round((dur - rel) * 100) / 100;
  if (sc.type === "video") { const vsp = sc.speed || 1; sc.out = (sc.in || 0) + rel * vsp; copy.in = (sc.in || 0) + rel * vsp; }
  SPEC.scenes.splice(idx + 1, 0, copy);
  SEL = idx + 1; DIRTY = true; renderTimeline(); renderRight(); renderLeft();
  msg("Sèn divize an 2 @ " + CUR.toFixed(2) + "s");
}

function splitAt(i) {
  splitActive();
}

function deleteLeft() {
  if (CLIPSEL && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) {
    const tk = SPEC.tracks[CLIPSEL.t], c = tk.clips[CLIPSEL.c];
    if (CUR > (c.start || 0) && CUR < (c.start || 0) + (c.dur || 2)) {
      snapshot();
      const trim = CUR - (c.start || 0);
      c.start = CUR;
      c.dur = Math.max(0.2, Math.round((c.dur - trim) * 100) / 100);
      if (c.src) c.in = Math.round(((c.in || 0) + trim * (c.speed || 1)) * 1000) / 1000;      // pa rekòmanse fichye a nan 0 s
      DIRTY = true; renderTimeline(); renderRight();
      msg("Pati agoch clip la efase");
      return;
    }
  }
  const idx = (SEL >= 0 ? SEL : sceneAt(CUR));
  const sc = SPEC.scenes[idx];
  if (!sc) return;
  const st = sStart(idx), dur = sDur(idx), cut = CUR - st;
  if (cut > 0.1 && cut < dur - 0.1) {
    snapshot();
    sc.duration = Math.round((dur - cut) * 100) / 100;
    if (sc.type === "video") sc.in = (sc.in || 0) + cut * (sc.speed || 1);
    DIRTY = true; renderTimeline(); renderRight();
    msg("Pati agoch sèn nan efase");
  }
}

function deleteRight() {
  if (CLIPSEL && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) {
    const tk = SPEC.tracks[CLIPSEL.t], c = tk.clips[CLIPSEL.c];
    if (CUR > (c.start || 0) && CUR < (c.start || 0) + (c.dur || 2)) {
      snapshot();
      c.dur = Math.max(0.2, Math.round((CUR - (c.start || 0)) * 100) / 100);
      if (c.out != null) c.out = (c.in || 0) + c.dur * (c.speed || 1);
      DIRTY = true; renderTimeline(); renderRight();
      msg("Pati adwat clip la efase");
      return;
    }
  }
  const idx = (SEL >= 0 ? SEL : sceneAt(CUR));
  const sc = SPEC.scenes[idx];
  if (!sc) return;
  const st = sStart(idx), dur = sDur(idx), newDur = CUR - st;
  if (newDur > 0.1 && newDur < dur - 0.1) {
    snapshot();
    sc.duration = Math.round(newDur * 100) / 100;
    if (sc.type === "video") sc.out = (sc.in || 0) + newDur * (sc.speed || 1);
    DIRTY = true; renderTimeline(); renderRight();
    msg("Pati adwat sèn nan efase");
  }
}

function deleteActive() {
  if (CLIPSEL && SPEC.tracks[CLIPSEL.t]) {
    snapshot();
    SPEC.tracks[CLIPSEL.t].clips.splice(CLIPSEL.c, 1);
    CLIPSEL = null; DIRTY = true; renderTimeline(); renderRight(); renderLeft();
    msg("Clip efase nan track");
    return;
  }
  if (SEL >= 0) delScene();
}

function freezeActive() {
  const idx = (SEL >= 0 ? SEL : sceneAt(CUR));
  const sc = SPEC.scenes[idx];
  if (!sc) { msg("Chwazi yon sen oswa clip pou fikse imaj"); return; }
  snapshot();
  const copy = JSON.parse(JSON.stringify(sc));
  copy.id = (sc.id || "frz") + "_freeze_" + Math.random().toString(36).slice(2, 5);
  copy.freeze = true;
  copy.duration = 2.0;
  copy.title = (sc.title || "Imaj") + " (Fiks)";
  if (copy.type === "video") copy.speed = 0;
  SPEC.scenes.splice(idx + 1, 0, copy);
  SEL = idx + 1; DIRTY = true; renderTimeline(); renderRight(); renderLeft();
  msg("✓ Imaj fiks (Freeze frame 2.0s) kreye");
}

function reverseActive() {
  const target = (CLIPSEL && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) ||
                 SPEC.scenes[SEL >= 0 ? SEL : sceneAt(CUR)];
  if (!target) { msg("Chwazi yon sen oswa clip pou ranvèse"); return; }
  snapshot();
  target.reverse = !target.reverse;
  DIRTY = true; renderTimeline(); renderRight();
  msg(target.reverse ? "Ranvèse aktif (Reverse ON)" : "Ranvèse dezaktive (Reverse OFF)");
}

function mirrorActive() {
  const target = (CLIPSEL && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) ||
                 SPEC.scenes[SEL >= 0 ? SEL : sceneAt(CUR)];
  if (!target) { msg("Chwazi yon sen oswa clip pou reflete"); return; }
  snapshot();
  target.mirror = !target.mirror;
  DIRTY = true; renderTimeline(); renderRight();
  msg(target.mirror ? "Reflete orizontalman (Mirror ON)" : "Reflete dezaktive (Mirror OFF)");
}

function rotateActive() {
  const target = (CLIPSEL && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) ||
                 SPEC.scenes[SEL >= 0 ? SEL : sceneAt(CUR)];
  if (!target) { msg("Chwazi yon sen oswa clip pou vire"); return; }
  snapshot();
  target.rotation = (((target.rotation || 0) + 90) % 360);
  DIRTY = true; renderTimeline(); renderRight();
  msg("Wotasyon: " + target.rotation + "°");
}

function cropActive() {
  const target = (CLIPSEL && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) ||
                 SPEC.scenes[SEL >= 0 ? SEL : sceneAt(CUR)];
  if (!target) { msg("Chwazi yon sen oswa clip pou rekadre"); return; }
  snapshot();
  if (target.crop) {
    delete target.crop;
    msg("Rekadre retire");
  } else {
    target.crop = { x: 5, y: 5, w: 90, h: 90 };
    msg("Mòd Rekadre (Crop) aktive nan panèl Pwopriyete");
  }
  DIRTY = true; renderTimeline(); selRTab("props");
}

function toggleMagnet() {
  MAIN_MAGNET = !MAIN_MAGNET;
  const el = $("#tMainMagnet"); if (el) el.classList.toggle("on", MAIN_MAGNET);
  msg(MAIN_MAGNET ? "Leman pis prensipal (Magnet) ON" : "Leman pis prensipal OFF");
}

function toggleSnap() {
  SNAP = !SNAP;
  const el = $("#tSnap"); if (el) el.classList.toggle("on", SNAP);
  msg(SNAP ? "Aimantation (Snap) ON" : "Aimantation OFF");
}

function toggleLinkage() {
  LINKAGE = !LINKAGE;
  const el = $("#tLinkage"); if (el) el.classList.toggle("on", LINKAGE);
  msg(LINKAGE ? "Lyezon (Linkage) ON: eleman asosye yo lye" : "Lyezon OFF");
}

function toggleAudioScrubbing() {
  SCRUB_AUDIO = !SCRUB_AUDIO;
  const el = $("#tScrubAudio"); if (el) el.classList.toggle("on", SCRUB_AUDIO);
  msg(SCRUB_AUDIO ? "Odyo pandan scrubbing ON" : "Odyo pandan scrubbing OFF");
}

function addKeyframe() {
  if (SEL < 0) { msg("chwazi yon sen anvan"); return; }
  const sc = SPEC.scenes[SEL]; sc.marks = sc.marks || [];
  let rel = Math.max(0, CUR - sStart(SEL)); rel = Math.round(rel * 100) / 100;
  if (rel > sDur(SEL)) rel = sDur(SEL);
  if (!sc.marks.includes(rel)) { snapshot(); sc.marks.push(rel); sc.marks.sort((a, b) => a - b); DIRTY = true; renderTimeline(); msg("keyframe @ " + rel.toFixed(2) + "s"); }
}

function addTrack(kind) {
  snapshot(); SPEC.tracks = SPEC.tracks || [];
  const names = { video: "Video", audio: "Audio", sfx: "SFX (Efè son)", image: "Imaj", text: "Teks", asset: "Asset" };
  const kname = names[kind] || kind;
  SPEC.tracks.unshift({ kind, name: kname + " " + (SPEC.tracks.filter(t => t.kind === kind).length + 1), clips: [] });
  DIRTY = true; renderTimeline(); msg("Track ajoute: " + kname);
  const tm = $("#trackmenu"); if (tm) tm.style.display = "none";
}

// ---- Anrejistre / Bati / Lint / Ekspo ----
const cln = () => {
  const c = JSON.parse(JSON.stringify(SPEC));
  (c.scenes || []).forEach(s => { delete s._regen; delete s._voicebak; });
  if (c.total_duration) {
    const tot = total();
    if (tot > c.total_duration) {
      c.total_duration = Math.round(tot * 100) / 100;
    }
  }
  return c;
};
async function save() {
  msg("ap anrejistre..."); const r = await api("PUT", "/api/spec", { spec: cln(), version: VER });
  if (r.status === 409) { showConflict(); return; }      // pa janm jete chanjman moun nan san mande l
  if (!r.body.ok) { msg("ere: " + (r.body.error || "?")); return; }
  VER = r.body.version; DIRTY = false; SPEC.scenes.forEach(s => delete s._regen); await build();
}
async function build() {
  msg("ap bati...");
  const r = await api("POST", "/api/build", { spec: cln() });
  if (r.body && r.body.ok) {
    if (r.body.audio) AUDIO_MAP = r.body.audio;
    msg("OK " + (r.body.total || 0).toFixed(1) + " s");
    mountPreview();
    renderTimeline();
    if (r.body.built != null) BUILT = r.body.built;
  } else {
    msg("ere: " + ((r.body && (r.body.error || (r.body.errors || [])[0])) || "?"));
    if (r.body && r.body.errors) showBuildState(r.body.errors, []);
  }
}
async function lint() { msg("lint..."); const r = await api("POST", "/api/lint", { spec: cln() }); ISSUES = {};
  ((r.body && (r.body.issues || r.body.problems)) || []).forEach(it => { const s = typeof it === "string" ? it : JSON.stringify(it);
    const m = /scenes?\D?(\d+)/.exec(it.where || it.path || s); const idx = (it.scene != null ? it.scene : (m ? +m[1] : null));
    if (idx != null) ISSUES[idx] = (it.msg || it.kind || it.message || "pwoblem"); });
  renderTimeline(); msg((r.body && r.body.ok) ? "OK lint pwop" : (Object.keys(ISSUES).length + " pwoblem")); }
async function exportHtml() { msg("ekspotasyon..."); const r = await api("POST", "/api/export", { spec: cln() });
  msg(r.body && r.body.ok ? "OK ekspote: " + r.body.file : "ere ekspo"); }

// ---- Rann MP4 Kadans ak Progress Bar rapid ----
let _renderPolling = null;
async function startMp4Render() {
  const modal = $("#renderModal");
  if (!modal) return;
  if (DIRTY) {
    try { await autoSave(); } catch (e) {}
  }

  const rmProjName = $("#rmProjName");
  if (rmProjName) rmProjName.textContent = PROJNAME || (SPEC && SPEC.title) || "Videyo Kadans";
  const rmSpecs = $("#rmSpecs");
  if (rmSpecs && SPEC) {
    rmSpecs.textContent = (SPEC.w || 1920) + "×" + (SPEC.h || 1080) + " • " + (SPEC.fps || 30) + " fps • " + total().toFixed(1) + " s";
  }

  const bar = $("#rmBar"), pctTxt = $("#rmPctTxt"), stageTxt = $("#rmStageTxt"), detail = $("#rmDetail"), rmTimer = $("#rmTimer");
  const doneBox = $("#rmDoneBox"), errBox = $("#rmErrorBox"), vPrev = $("#rmVideoPreview");
  const btnCancel = $("#rmBtnCancel"), btnDl = $("#rmBtnDownload"), btnClose = $("#rmBtnClose");

  if (bar) bar.style.width = "0%";
  if (pctTxt) pctTxt.textContent = "0%";
  if (rmTimer) rmTimer.textContent = "⏱ 00:00";
  if (stageTxt) stageTxt.textContent = "Demaraj rann MP4...";
  if (detail) detail.textContent = "Ap prepare motè rann lan...";
  if (doneBox) doneBox.style.display = "none";
  if (errBox) { errBox.style.display = "none"; errBox.textContent = ""; }
  if (vPrev) { vPrev.style.display = "none"; vPrev.pause(); vPrev.removeAttribute("src"); vPrev.load(); }
  const fileRow = $("#rmFileRow");
  if (fileRow) fileRow.style.display = "none";
  if (btnCancel) { btnCancel.style.display = "inline-flex"; btnCancel.textContent = "Kanpe"; }
  if (btnDl) btnDl.style.display = "none";
  if (btnClose) btnClose.style.display = "none";
  modal.style.display = "flex";

  const renderStartMs = Date.now();
  const formatTimer = (sec) => {
    if (sec == null || isNaN(sec) || sec < 0) return "00:00";
    const s = Math.floor(sec);
    const m = Math.floor(s / 60);
    const rem = s % 60;
    return String(m).padStart(2, "0") + ":" + String(rem).padStart(2, "0");
  };

  const stageLabels = {
    start: "Inisyalizasyon...",
    voice: "Jenerasyon Vwa...",
    words: "Aliyman Mo yo...",
    media: "Preparasyon Medya yo...",
    frames: "Rann Imaj yo (Frames)...",
    sound: "Miksaj Odyo & FFmpeg...",
    done: "Fini avèk siksè!",
    error: "Erè rive nan rann lan"
  };

  if (total() <= 0 && (!SPEC.scenes || !SPEC.scenes.length)) {
    msg("Pwojè a vid — ajoute omwen yon sèn oswa yon clip anvan ou rann");
    alert("Pwojè a vid: pa gen okenn sèn ni klip pou rann videyo a.");
    return;
  }
  msg("ap lanse rann MP4...");
  const res = await api("POST", "/api/render", { spec: cln() });
  if (!res.body || !res.body.ok) {
    if (stageTxt) stageTxt.textContent = "Erè demaraj";
    if (errBox) {
      errBox.style.display = "block";
      errBox.textContent = (res.body && res.body.error) || "Pa ka demare rann lan.";
    }
    if (btnCancel) btnCancel.textContent = "Fèmen";
    return;
  }

  if (_renderPolling) clearInterval(_renderPolling);
  let fakeProgress = 4;

  _renderPolling = setInterval(async () => {
    try {
      const r = await api("GET", "/api/render-status");
      const st = (r.body && r.body.render) || {};

      let pct = 0;
      if (st.total > 0) {
        pct = Math.min(99, Math.round((st.done / st.total) * 100));
      } else {
        const stageWeights = { start: 10, voice: 25, words: 35, media: 50, sound: 92, done: 100 };
        const basePct = stageWeights[st.stage] || 15;
        fakeProgress = Math.min(basePct, fakeProgress + 2);
        pct = fakeProgress;
      }

      if (st.stage === "done" || (!st.active && st.mp4 && !st.error)) {
        pct = 100;
      }

      const elapsedSec = (typeof st.elapsed === "number" && st.elapsed > 0)
        ? st.elapsed
        : ((Date.now() - renderStartMs) / 1000);
      const etaSec = (typeof st.eta === "number" && st.eta > 0) ? st.eta : null;

      if (bar) bar.style.width = pct + "%";
      if (pctTxt) pctTxt.textContent = pct + "%";
      if (rmTimer) {
        let tStr = formatTimer(elapsedSec);
        if (etaSec != null && st.stage !== "done") {
          tStr += " (estime ~" + formatTimer(etaSec) + ")";
        }
        rmTimer.textContent = tStr;
      }
      if (stageTxt) stageTxt.textContent = stageLabels[st.stage] || st.stage || "Ap rann...";

      let det = st.info || "";
      if (st.total > 0 && st.stage === "frames") {
        det = "Imaj " + st.done + " sou " + st.total + " (" + pct + "%)";
      }
      if (detail) detail.textContent = det;
      msg("⏳ Rann MP4: " + pct + "%");

      // Si rann lan fini avèk siksè
      if (st.stage === "done" || (!st.active && st.mp4 && !st.error)) {
        clearInterval(_renderPolling);
        _renderPolling = null;
        if (bar) bar.style.width = "100%";
        if (pctTxt) pctTxt.textContent = "100%";
        if (rmTimer) {
          rmTimer.textContent = "Fini nan " + formatTimer(elapsedSec) + " (" + elapsedSec.toFixed(1) + "s)";
        }
        if (stageTxt) stageTxt.textContent = "Videyo MP4 pare!";
        if (detail) detail.textContent = "Videyo a pare pou telechaje oswa gade.";
        if (doneBox) doneBox.style.display = "flex";
        if (btnCancel) btnCancel.style.display = "none";
        if (btnDl) {
          btnDl.style.display = "inline-flex";
          btnDl.onclick = () => {
            const dlUrl = "/api/download-render?token=" + encodeURIComponent(TOK) + "&_t=" + Date.now();
            const a = document.createElement("a");
            a.href = dlUrl;
            a.download = (PROJNAME || "videyo") + ".mp4";
            document.body.appendChild(a);
            a.click();
            a.remove();
          };
        }
        if (btnClose) {
          btnClose.style.display = "inline-flex";
          btnClose.onclick = () => { modal.style.display = "none"; };
        }
        if (vPrev && (st.rel_mp4 || st.mp4)) {
          // inline=1: streaming ak Range (lektè a ka chèche nan videyo a, imaj yo parèt touswit)
          vPrev.src = "/api/download-render?inline=1&token=" + encodeURIComponent(TOK) + "&_t=" + Date.now();
          vPrev.style.display = "block";
        }
        // KOTE FICHYE A YE A: chemen konplè (pwojè + workspace) + «Ouvri kote fichye a ye a»
        modal.style.display = "flex";
        const fileRow = $("#rmFileRow"), filePath = $("#rmFilePath"), fileInfo = $("#rmFileInfo"), wsPath = $("#rmWorkspacePath");
        if (fileRow && st.mp4) {
          fileRow.style.display = "flex";
          if (filePath) filePath.textContent = "📁 Pwojè: " + st.mp4;
          if (wsPath) {
            const mPath = st.workspace_mp4 || st.mirror_mp4 || "";
            if (mPath && mPath !== st.mp4) {
              wsPath.style.display = "block";
              wsPath.textContent = "📂 Workspace: " + mPath;
            } else {
              wsPath.style.display = "none";
            }
          }
          if (fileInfo) {
            const mb = st.size ? (st.size / 1048576).toFixed(1) + " MB" : "";
            fileInfo.textContent = [st.resolution, mb, st.encoder ? "ankodè: " + st.encoder : ""].filter(Boolean).join(" · ");
          }
          const bRev = $("#rmBtnReveal"), bCopy = $("#rmBtnCopyPath");
          if (bRev) bRev.onclick = async () => {
            const rr = await api("POST", "/api/reveal-render", {});
            msg(rr.body && rr.body.ok ? "📂 Dosye a louvri: " + (rr.body.folder || "") : "Pa ka louvri dosye a");
          };
          if (bCopy) bCopy.onclick = async () => {
            try { await navigator.clipboard.writeText(st.mp4); msg("📋 Chemen an kopye"); }
            catch (e) {
              const r2 = document.createRange(); r2.selectNodeContents(filePath);
              const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r2); document.execCommand("copy");
              msg("📋 Chemen an kopye");
            }
          };
        }
        msg("✓ Rann MP4 fini!");
        notifyWasdevAudio("render_done", { mp4: st.mp4, workspace_mp4: st.workspace_mp4 || "", title: PROJNAME });
        return;
      }

      // Si gen yon erè
      if (st.error || (!st.active && !st.mp4)) {
        clearInterval(_renderPolling);
        _renderPolling = null;
        if (errBox) {
          errBox.style.display = "block";
          errBox.textContent = "Erè: " + (st.error || "Rann lan kanpe.");
        }
        if (stageTxt) stageTxt.textContent = "Erè rann";
        if (btnCancel) btnCancel.textContent = "Fèmen";
        msg("Erè rann");
        return;
      }
    } catch (e) {}
  }, 250);
}

async function cancelMp4Render() {
  if (_renderPolling) {
    clearInterval(_renderPolling);
    _renderPolling = null;
  }
  await api("POST", "/api/render-cancel").catch(() => {});
  const modal = $("#renderModal");
  if (modal) modal.style.display = "none";
  msg("Rann kanpe");
}

// ---- Jesyon pwoje (.kadans) ----
let PROJECTS = [], PROJNAME = "", OPENTABS = [];
async function loadProjects() {
  const r = await api("GET", "/api/projects");
  PROJECTS = (r.body && r.body.projects) || []; PROJNAME = (r.body && r.body.active) || "";
  const pn = $("#projname"); if (pn) pn.textContent = PROJNAME || "Pwoje";
  addTab(PROJNAME); renderProjTabs();
}
function loadOpenTabs() { try { OPENTABS = JSON.parse(localStorage.getItem("kd_opentabs") || "[]"); } catch (x) { OPENTABS = []; } }
function saveOpenTabs() { try { localStorage.setItem("kd_opentabs", JSON.stringify(OPENTABS)); } catch (x) {} }
function addTab(name) { if (name && OPENTABS.indexOf(name) < 0) { OPENTABS.push(name); saveOpenTabs(); } }
function renderProjTabs() {
  const el = $("#projtabs"); if (!el) return; el.innerHTML = "";
  OPENTABS.forEach(nm => {
    const pr = PROJECTS.find(p => p.name === nm);
    const d = document.createElement("div"); d.className = "ptab" + (nm === PROJNAME ? " on" : "");
    const titleText = (pr && (pr.title || pr.name)) || nm;
    d.title = titleText;
    const t1 = document.createElement("span");
    t1.className = "ptab-title";
    t1.textContent = titleText;
    d.onclick = e => {
      if (e.target === x) return;
      if (nm !== PROJNAME) openProject(nm);
    };
    const x = document.createElement("span");
    x.className = "x";
    x.textContent = "×";
    x.title = "Fèmen tab la (pa efase pwoje a)";
    x.onclick = e => {
      e.stopPropagation();
      setPlaying(false);
      stopAudio();
      OPENTABS = OPENTABS.filter(y => y !== nm);
      saveOpenTabs();
      if (nm === PROJNAME && OPENTABS.length) openProject(OPENTABS[0]);
      else renderProjTabs();
    };
    d.appendChild(t1); d.appendChild(x);
    d.oncontextmenu = e => { e.preventDefault(); e.stopPropagation(); showTabContextMenu(e.clientX, e.clientY, nm); };
    el.appendChild(d);
  });
  if (!el._wheelWired) {
    el._wheelWired = true;
    el.addEventListener("wheel", e => {
      if (e.deltaY) {
        el.scrollLeft += e.deltaY;
        e.preventDefault();
      }
    }, { passive: false });
  }
  if (!el._ctxWired) {
    el._ctxWired = true;
    el.addEventListener("contextmenu", e => {
      if (e.target.closest(".ptab")) return;
      e.preventDefault();
      showTabContextMenu(e.clientX, e.clientY, PROJNAME);
    });
  }
}

function showTabContextMenu(x, y, name) {
  const old = document.getElementById("ctxmenu"); if (old) old.remove();
  const m = document.createElement("div"); m.id = "ctxmenu"; m.className = "menu";
  m.style.cssText = "display:block;position:fixed;left:" + x + "px;top:" + y + "px;z-index:9999;min-width:210px";
  const pr = PROJECTS.find(p => p.name === name);
  const items = [
    ["refresh", "Rechaje pwojè a", () => openProject(name)],
    ["copy", "Duplike pwojè sa a", () => duplicateProject(name)],
    ["camera", "Louvri nan yon nouvo fenèt", () => window.open(location.href, "_blank")],
    ["copy", "Kopye adrès URL la", () => {
      try { navigator.clipboard.writeText(location.href); msg("Adrès URL kopye!"); } catch (e) {}
    }],
    ["scissors", "Fèmen tab sa a", () => {
      OPENTABS = OPENTABS.filter(y => y !== name);
      saveOpenTabs();
      if (name === PROJNAME && OPENTABS.length) openProject(OPENTABS[0]);
      else renderProjTabs();
    }]
  ];
  if (OPENTABS.length > 1) {
    items.push(["scissors", "Fèmen lòt tab yo", () => {
      OPENTABS = [name];
      saveOpenTabs();
      if (name !== PROJNAME) openProject(name);
      else renderProjTabs();
    }]);
  }
  if (PROJECTS.length > 1) {
    items.push(["trash", "Efase pwojè sa a", () => deleteProject(name)]);
  }
  items.forEach(it => {
    const d = document.createElement("div"); d.className = "mi";
    d.innerHTML = svg(it[0]) + it[1];
    d.onclick = () => { m.remove(); it[2](); };
    m.appendChild(d);
  });
  document.body.appendChild(m);
  const r = m.getBoundingClientRect();
  if (r.right > window.innerWidth) m.style.left = (window.innerWidth - r.width - 6) + "px";
  if (r.bottom > window.innerHeight) m.style.top = (window.innerHeight - r.height - 6) + "px";
}

async function sendActiveProjectToChat(name, extraText = "") {
  const prName = name || PROJNAME || "Pwoje";
  const pr = PROJECTS.find(p => p.name === prName);
  const title = (pr && pr.title) || ($("#vtitle") && $("#vtitle").value.trim()) || prName;
  msg("Ap voye nan Chat AI...");
  try {
    const r = await api("POST", "/api/send-to-chat", { title, name: prName, text: extraText });
    if (r.body && r.body.ok) {
      msg("Voye nan Chat AI avèk siksè!");
    } else {
      msg("Chat AI notifye");
    }
  } catch (e) {
    msg("Chat AI notifye");
  }
  try {
    if (window.parent && window.parent !== window) {
      window.parent.postMessage({
        evt: "send_to_chat",
        title,
        name: prName,
        text: extraText,
        url: location.href
      }, "*");
    }
  } catch (e) {}
  try {
    const link = location.href;
    const clipTxt = "🎬 **Pwojè Videyo :** " + title + "\n🔗 **Lyen :** [" + title + "](" + link + ")\n" + (extraText ? ("\n> " + extraText + "\n") : "");
    navigator.clipboard.writeText(clipTxt);
  } catch (e) {}
}

async function duplicateProject(name) {
  setPlaying(false);
  stopAudio();
  msg("ap duplike pwoje " + name + "...");
  const r = await api("POST", "/api/projects/duplicate", { name });
  if (r.body && r.body.ok) {
    await loadProjects();
    addTab(r.body.name);
    await openProject(r.body.name);
    msg("pwoje duplike: " + r.body.name);
  } else {
    msg("ere duplike: " + ((r.body && r.body.error) || "?"));
  }
}

async function deleteProject(name) {
  if (!confirm("Ou vle efase pwoje \"" + name + "\" sa a nèt?")) return;
  setPlaying(false);
  stopAudio();
  msg("ap efase " + name + "...");
  const r = await api("POST", "/api/projects/delete", { name });
  if (r.body && r.body.ok) {
    OPENTABS = OPENTABS.filter(y => y !== name);
    saveOpenTabs();
    await loadProjects();
    await load();
    await build();
    msg("pwoje efase");
  } else {
    msg("ere efase: " + ((r.body && r.body.error) || "?"));
  }
}
function renderProjectMenu() {
  const m = $("#projmenu"); if (!m) return; m.innerHTML = "";
  const add = document.createElement("div"); add.className = "mi"; add.innerHTML = svg("plus") + "Nouvo pwoje";
  add.onclick = newProject; m.appendChild(add);
  const openF = document.createElement("div"); openF.className = "mi"; openF.innerHTML = svg("open") + "Ouvri fichye (HTML, XML, Kadans)...";
  openF.onclick = () => { $("#projmenu").style.display = "none"; const fi = $("#fiOpenFile"); if (fi) { fi.value = ""; fi.click(); } };
  m.appendChild(openF);
  const sep = document.createElement("div"); sep.style.cssText = "height:1px;background:var(--line);margin:4px 0;"; m.appendChild(sep);
  PROJECTS.forEach(pr => {
    const d = document.createElement("div"); d.className = "mi" + (pr.active ? " on" : "");
    d.innerHTML = svg("folder") + '<span style="flex:1;overflow:hidden;text-overflow:ellipsis">' + esc(pr.title) + '</span><span class="k">' + pr.scenes + " sen</span>";
    d.onclick = () => openProject(pr.name); m.appendChild(d);
  });
}
async function newProject() {
  $("#projmenu").style.display = "none";
  const old = document.getElementById("kdNewProjModal");
  if (old) old.remove();
  const ov = document.createElement("div");
  ov.id = "kdNewProjModal";
  ov.style.cssText = "position:fixed;inset:0;background:rgba(8,5,18,0.76);z-index:9999;display:flex;align-items:center;justify-content:center;";
  const _tk = (k, fb) => (window.KadansI18n && window.KadansI18n.t(k, fb)) || fb || k;
  const defName = _tk("projects", "Pwoje") + " " + (PROJECTS.length + 1);
  ov.innerHTML = `
    <div style="background:#161127;border:1px solid #8b5cf6;border-radius:16px;padding:26px 32px;width:640px;max-width:95vw;box-shadow:0 24px 64px #000c;color:#f3eefe;font-family:system-ui,sans-serif">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
        <svg viewBox="0 0 64 64" style="width:24px;height:24px;display:block;flex:none"><defs><linearGradient id="nwg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#0098ff"/></linearGradient></defs><rect x="4" y="4" width="56" height="56" rx="14" fill="#1d1230"/><path d="M24 20L12 32l12 12" fill="none" stroke="url(#nwg)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M40 20l12 12-12 12" fill="none" stroke="url(#nwg)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M36 14L28 50" fill="none" stroke="#b794ff" stroke-width="5" stroke-linecap="round"/></svg>
        <span style="font-size:20px;font-weight:800;color:#c4b5fd">${_tk("np_modal_title", "Nouvo Pwojè Kadans Studio")}</span>
      </div>
      <div style="font-size:13px;color:#b9addb;margin-bottom:18px">${_tk("np_modal_sub", "Antre non nouvo pwojè videyo a epi chwazi fòma ekran an, dire a, ak lang li.")}</div>
      <label style="display:block;font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:6px">${_tk("np_name_lbl", "Non pwojè / videyo a :")}</label>
      <input id="kdNpName" value="${esc(defName)}" style="width:100%;background:#0e0b1a;border:1px solid #3d2c5e;color:#f3eefe;border-radius:9px;padding:10px 14px;font-size:14px;font-weight:600;margin-bottom:16px;outline:none">
      
      <div style="display:flex;gap:14px;margin-bottom:16px">
        <div style="flex:1">
          <label style="display:block;font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:6px">${_tk("np_ratio_lbl", "Fòma Ekran (Ratio) :")}</label>
          <select id="kdNpRatio" style="width:100%;background:#0e0b1a;border:1px solid #3d2c5e;color:#f3eefe;border-radius:9px;padding:10px 12px;font-size:13.5px;outline:none">
            <option value="16:9">16:9 — YouTube / Desktop (1920×1080)</option>
            <option value="9:16">9:16 — Reels / TikTok / Shorts (1080×1920)</option>
            <option value="1:1">1:1 — Kare Instagram / Post (1080×1080)</option>
            <option value="4:5">4:5 — Pòtrè Feed (1080×1350)</option>
          </select>
        </div>
        <div style="flex:1">
          <label style="display:block;font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:6px">${_tk("np_dur_lbl", "Dire videyo a :")}</label>
          <div style="display:flex;gap:8px">
            <div style="flex:1;display:flex;align-items:center;gap:6px;background:#0e0b1a;border:1px solid #3d2c5e;border-radius:9px;padding:8px 12px">
              <input id="kdNpMin" type="number" min="0" max="180" value="0" style="width:100%;background:transparent;border:none;color:#f3eefe;font-size:14px;font-weight:700;outline:none">
              <span style="font-size:12px;color:#a78bfa;font-weight:700">min</span>
            </div>
            <div style="flex:1;display:flex;align-items:center;gap:6px;background:#0e0b1a;border:1px solid #3d2c5e;border-radius:9px;padding:8px 12px">
              <input id="kdNpSec" type="number" min="0" max="59" value="30" style="width:100%;background:transparent;border:none;color:#f3eefe;font-size:14px;font-weight:700;outline:none">
              <span style="font-size:12px;color:#a78bfa;font-weight:700">seg</span>
            </div>
          </div>
        </div>
      </div>

      <label style="display:block;font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:6px">${_tk("np_lang_lbl", "Lang videyo a :")}</label>
      <select id="kdNpLang" style="width:100%;background:#0e0b1a;border:1px solid #3d2c5e;color:#f3eefe;border-radius:9px;padding:10px 12px;font-size:13.5px;margin-bottom:22px;outline:none">
        <option value="fr" selected>Français (fr)</option>
        <option value="ht">Kreyòl ayisyen (ht)</option>
        <option value="en">English (en)</option>
        <option value="es">Español (es)</option>
        <option value="pt">Português (pt)</option>
        <option value="ru">Русский / Ris (ru)</option>
        <option value="it">Italiano / Italyen (it)</option>
        <option value="de">Deutsch / Alman (de)</option>
      </select>
      <div style="display:flex;justify-content:flex-end;gap:12px">
        <button type="button" id="kdNpCancel" style="background:#2e1754;color:#f3eefe;border:1px solid #522b91;border-radius:8px;padding:9px 18px;font-size:13.5px;cursor:pointer">${_tk("cancel", "Anile")}</button>
        <button type="button" id="kdNpOk" class="pri" style="background:#4c1d95;border-color:#6d28d9;color:#fff;border-radius:8px;padding:9px 24px;cursor:pointer;font-weight:700;font-size:13.5px">${_tk("np_create_btn", "Kreye Pwojè a")}</button>
      </div>
    </div>`;
  document.body.appendChild(ov);
  const inp = document.getElementById("kdNpName");
  const sel = document.getElementById("kdNpRatio");
  const inpMin = document.getElementById("kdNpMin");
  const inpSec = document.getElementById("kdNpSec");
  const selLang = document.getElementById("kdNpLang");
  const KI = window.KadansI18n;
  if (selLang && KI) {
    selLang.value = KI.getLang();
    // Anndan WASDEV: lang videyo a = lang sistèm WASDEV la, pa gen selektè
    if (KI.isEmbedded()) { selLang.style.display = "none"; if (selLang.previousElementSibling) selLang.previousElementSibling.style.display = "none"; }
  }
  if (inp) { inp.focus(); inp.select(); }
  const close = () => ov.remove();
  document.getElementById("kdNpCancel").onclick = close;
  ov.onclick = e => { if (e.target === ov) close(); };
  const submit = async () => {
    const name = (inp && inp.value.trim()) || defName;
    const ratio = (sel && sel.value) || "16:9";
    const mins = Math.max(0, parseInt((inpMin && inpMin.value) || "0", 10) || 0);
    const secs = Math.max(0, parseInt((inpSec && inpSec.value) || "0", 10) || 0);
    const total_duration = Math.max(3, (mins * 60) + secs);
    const lang = (selLang && selLang.value) || "fr";
    close();
    setPlaying(false);
    stopAudio();
    CUR = 0;
    SEL = -1;
    CLIPSEL = null;
    VOICESEL = null;
    msg("ap kreye nouvo pwoje vid...");
    const r = await api("POST", "/api/projects/new", { name, ratio, lang, total_duration, empty: true });
    if (r.body && r.body.ok) {
      await loadProjects();
      await load();
      await build();
      msg("nouvo pwoje vid: " + r.body.name);
    } else {
      msg("ere: " + ((r.body && r.body.error) || "?"));
    }
  };
  document.getElementById("kdNpOk").onclick = submit;
  if (inp) inp.onkeydown = e => { if (e.key === "Enter") { e.preventDefault(); submit(); } else if (e.key === "Escape") close(); };
}
async function openProject(name) {
  if (DIRTY && !confirm("Gen chanjman ki pa anrejistre. Kite yo pou louvri lot pwoje a?")) return;
  setPlaying(false);
  stopAudio();
  const r = await api("POST", "/api/projects/open", { name });
  if (r.body && r.body.ok) {
    $("#projmenu").style.display = "none";
    CUR = 0;
    await loadProjects();
    await load();
    await build();
    msg("pwoje: " + r.body.name);
  } else {
    msg("ere: " + ((r.body && r.body.error) || "?"));
  }
}

// ---- Kadans Instant Tooltip System (Topbar & Timeline Controls) ----
function initKadansTooltips() {
  let tip = document.getElementById("kadans-tip");
  if (!tip) {
    tip = document.createElement("div");
    tip.id = "kadans-tip";
    document.body.appendChild(tip);
  }
  let activeEl = null;

  function show(el) {
    const main = el.getAttribute("data-tip") || el.getAttribute("data-original-title") || el.getAttribute("title");
    if (!main) return;
    activeEl = el;
    if (el.hasAttribute("title")) {
      el.setAttribute("data-original-title", el.getAttribute("title"));
      el.removeAttribute("title");
    }
    const sub = el.getAttribute("data-sub") || "";
    tip.innerHTML = '<span class="tip-main">' + esc(main) + '</span>' + (sub ? '<span class="tip-sub">' + esc(sub) + '</span>' : '');
    tip.classList.add("show");
    pos(el);
  }

  function pos(el) {
    if (!activeEl) return;
    const r = activeEl.getBoundingClientRect();
    const tw = tip.offsetWidth || 100;
    let x = r.left + r.width / 2;
    if (x - tw / 2 < 8) x = tw / 2 + 8;
    if (x + tw / 2 > window.innerWidth - 8) x = window.innerWidth - tw / 2 - 8;
    let y = r.bottom + 6;
    if (y + 40 > window.innerHeight) y = Math.max(8, r.top - (tip.offsetHeight || 30) - 6);
    tip.style.left = Math.round(x) + "px";
    tip.style.top = Math.round(y) + "px";
  }

  function hide() {
    if (activeEl && activeEl.hasAttribute("data-original-title")) {
      activeEl.setAttribute("title", activeEl.getAttribute("data-original-title"));
    }
    activeEl = null;
    tip.classList.remove("show");
  }

  document.addEventListener("mouseover", e => {
    const btn = e.target.closest("#top button, #tlhdr button, .icon-rail button, #pbar button");
    if (btn) show(btn);
  });
  document.addEventListener("mouseout", e => {
    const btn = e.target.closest("#top button, #tlhdr button, .icon-rail button, #pbar button");
    if (btn) hide();
  });
  window.addEventListener("scroll", hide, true);
  window.addEventListener("resize", hide);
}

// ---- Init ----
function setPlayIcon() { const bp = $("#bPlay"); if (bp && bp.querySelector("span")) bp.querySelector("span").innerHTML = svg(playing ? "pause" : "play"); }
function delScene() { if (SEL < 0) return; snapshot(); SPEC.scenes.splice(SEL, 1); SEL = Math.min(SEL, SPEC.scenes.length - 1); DIRTY = true; renderTimeline(); renderRight(); renderLeft(); msg("sen efase"); }
paintIcons();
initKadansTooltips();
$("#bSave").onclick = save; $("#bBuild").onclick = build; $("#bLint").onclick = lint; $("#bExport").onclick = exportHtml; $("#bSettings").onclick = openSettings;
if ($("#bRender")) $("#bRender").onclick = startMp4Render;
if ($("#rmCloseX")) $("#rmCloseX").onclick = () => { $("#renderModal").style.display = "none"; };
if ($("#rmBtnCancel")) $("#rmBtnCancel").onclick = cancelMp4Render;
if ($("#bNewProj")) $("#bNewProj").onclick = newProject;

// ---- Remotion On-Demand Studio Integration ----
async function openRemotionStudio(install = false) {
  const modal = $("#remotionModal");
  const progWrap = $("#remProgressWrap");
  const btnRow = $("#remBtnRow");
  const statusTxt = $("#remStatusTxt");

  msg("Ap prepare Remotion Studio...");
  try {
    const res = await post("/api/remotion/open", { spec: SPEC, install: install, open_browser: true });
    if (res && res.need_install) {
      if (modal) {
        modal.style.display = "flex";
        if (progWrap) progWrap.style.display = "none";
        if (btnRow) btnRow.style.display = "flex";
      }
      return;
    }
    if (res && res.ok) {
      if (modal) modal.style.display = "none";
      msg("✓ Remotion Studio louvri nan Edge: " + (res.url || "http://localhost:3333"));
    } else {
      if (statusTxt) statusTxt.textContent = "✕ Erè: " + (res ? res.error : "Erè enkoni");
      msg("Erè Remotion: " + (res ? res.error : "Erè enkoni"));
    }
  } catch (err) {
    msg("Erè Remotion: " + err.message);
  }
}

if ($("#bRemotion")) $("#bRemotion").onclick = () => openRemotionStudio(false);
if ($("#remCloseX")) $("#remCloseX").onclick = () => { $("#remotionModal").style.display = "none"; };
if ($("#remBtnCancel")) $("#remBtnCancel").onclick = () => { $("#remotionModal").style.display = "none"; };
if ($("#remBtnInstall")) $("#remBtnInstall").onclick = async () => {
  const progWrap = $("#remProgressWrap");
  const btnRow = $("#remBtnRow");
  const statusTxt = $("#remStatusTxt");
  if (progWrap) progWrap.style.display = "flex";
  if (btnRow) btnRow.style.display = "none";
  if (statusTxt) statusTxt.textContent = "⏳ Ap enstale Remotion sou PC a (Zero-Bloat)…";
  await openRemotionStudio(true);
};
async function openExternalFile(file) {
  if (!file) return;
  msg("Chaje fichye " + file.name + "...");
  try {
    const reader = new FileReader();
    reader.onload = async (e) => {
      const content = e.target.result;
      const res = await post("/api/projects/open-file", {
        filename: file.name,
        content: content
      });
      if (res && res.error) {
        msg("Erè: " + res.error);
        return;
      }
      msg("Pwojè " + (res.name || file.name) + " louvri avèk siksè!");
      await loadProjectList();
      if (res && res.name) {
        await openProject(res.name);
      }
    };
    reader.readAsText(file);
  } catch (err) {
    msg("Erè ouvèti: " + err.message);
  }
}
if ($("#bOpenFile")) {
  $("#bOpenFile").onclick = () => {
    const fi = $("#fiOpenFile");
    if (fi) {
      fi.value = "";
      fi.click();
    }
  };
}
if ($("#fiOpenFile")) {
  $("#fiOpenFile").onchange = (e) => {
    const f = e.target.files && e.target.files[0];
    if (f) openExternalFile(f);
  };
}
if ($("#vlang")) {
  $("#vlang").onchange = () => {
    const l = $("#vlang").value;
    SPEC.lang = l;
    SPEC.voice = SPEC.voice || {};
    SPEC.voice.lang = l;
    DIRTY = true;
    if (window.KadansI18n) window.KadansI18n.setLang(l);
    msg((window.KadansI18n ? window.KadansI18n.t("video_lang_title") : "Lang") + ": " + l);
    build();
  };
}
let _PREV_VOL = 1;
function updateVolUI(v) {
  v = Math.max(0, Math.min(2, Math.round(v * 100) / 100));
  const pct = Math.round(v * 100);
  const valEl = $("#volval");
  if (valEl) {
    valEl.textContent = pct + "%";
    valEl.style.color = (v <= 0.001) ? "var(--err)" : (v > 1.2 ? "var(--amb)" : "var(--mov)");
  }
  const fill = $("#volFill");
  if (fill) {
    fill.style.height = Math.min(100, Math.max(0, (v / 2) * 100)) + "%";
    fill.style.background = (v <= 0.001) ? "var(--line)" : (v > 1.2 ? "linear-gradient(0deg,#4c1d95,#ff8a3d)" : "linear-gradient(0deg,#4c1d95,#8b5cf6)");
  }
  const thumb = $("#volThumb");
  if (thumb) {
    thumb.style.bottom = Math.min(100, Math.max(0, (v / 2) * 100)) + "%";
  }
  const muteBtn = $("#volMute");
  const iconSpan = $("#volIcon");
  if (iconSpan) {
    if (v <= 0.001) {
      iconSpan.innerHTML = svg("mute");
      if (muteBtn) muteBtn.classList.add("muted");
    } else {
      iconSpan.innerHTML = svg("volume");
      if (muteBtn) muteBtn.classList.remove("muted");
    }
  }
}

function setMasterVol(v, notify = true) {
  v = Math.max(0, Math.min(2, Math.round(v * 100) / 100));
  if (v > 0.001) _PREV_VOL = v;
  if (!SPEC) SPEC = {};
  SPEC.volume = v;
  DIRTY = true;
  updateVolUI(v);
  syncActiveAudioVolumes();
  if (notify) notifyWasdevAudio("volume", { volume: v });
  msg("volim master: " + Math.round(v * 100) + "%");
}

function toggleMasterMute() {
  const cur = (SPEC && SPEC.volume != null) ? SPEC.volume : 1;
  if (cur > 0.001) {
    _PREV_VOL = cur;
    setMasterVol(0);
    msg("Son koupe (Muted)");
  } else {
    const restore = (_PREV_VOL > 0.001) ? _PREV_VOL : 1;
    setMasterVol(restore);
    msg("Volim retabli: " + Math.round(restore * 100) + "%");
  }
}

function setVol(delta) {
  const cur = (SPEC && SPEC.volume != null) ? SPEC.volume : 1;
  setMasterVol(cur + delta);
}

function initVolFader() {
  const track = $("#volTrack");
  if (!track) return;
  let dragging = false;
  const setFromPointer = e => {
    const rect = track.getBoundingClientRect();
    if (rect.height <= 0) return;
    const ratio = Math.max(0, Math.min(1, (rect.bottom - e.clientY) / rect.height));
    const v = Math.round(ratio * 200) / 100;
    setMasterVol(v);
  };
  track.addEventListener("pointerdown", e => {
    e.preventDefault();
    dragging = true;
    track.classList.add("dragging");
    try { track.setPointerCapture(e.pointerId); } catch (x) {}
    setFromPointer(e);
  });
  track.addEventListener("pointermove", e => {
    if (!dragging) return;
    setFromPointer(e);
  });
  const stopDrag = e => {
    if (!dragging) return;
    dragging = false;
    track.classList.remove("dragging");
    try { track.releasePointerCapture(e.pointerId); } catch (x) {}
  };
  track.addEventListener("pointerup", stopDrag);
  track.addEventListener("pointercancel", stopDrag);

  const handleWheel = e => {
    e.preventDefault();
    const cur = (SPEC && SPEC.volume != null) ? SPEC.volume : 1;
    const step = (e.shiftKey ? 0.01 : 0.05) * (e.deltaY < 0 ? 1 : -1);
    setMasterVol(cur + step);
  };
  track.addEventListener("wheel", handleWheel, { passive: false });
  const meterEl = $("#tlmeter");
  if (meterEl) meterEl.addEventListener("wheel", handleWheel, { passive: false });

  track.addEventListener("dblclick", () => {
    setMasterVol(1);
    msg("Volim reset a 100%");
  });
  const valEl = $("#volval");
  if (valEl) {
    valEl.addEventListener("dblclick", () => {
      setMasterVol(1);
      msg("Volim reset a 100%");
    });
  }
  const muteBtn = $("#volMute");
  if (muteBtn) muteBtn.onclick = toggleMasterMute;
}
initVolFader();
$("#bPlay").onclick = () => setPlaying(!playing);
$("#bReplayP").onclick = () => { stopAudio(); CUR = 0; movePlayhead(); post({ cmd: "seek", t: 0 }); setPlaying(true); };
if ($("#prog")) {
  let pDrag = false;
  $("#prog").addEventListener("mousedown", ev => {
    pDrag = true;
    seekProg(ev);
    const mv = e => { if (pDrag) seekProg(e); };
    const up = () => {
      pDrag = false;
      document.removeEventListener("mousemove", mv);
      document.removeEventListener("mouseup", up);
    };
    document.addEventListener("mousemove", mv);
    document.addEventListener("mouseup", up);
  });
}
if ($("#pvZoomIn")) $("#pvZoomIn").onclick = () => setPvZoom(PVZOOM * 1.2);
if ($("#pvZoomOut")) $("#pvZoomOut").onclick = () => setPvZoom(PVZOOM / 1.2);
if ($("#pvFit")) $("#pvFit").onclick = () => fitScreenView();
if ($("#pvZoomLbl")) $("#pvZoomLbl").onclick = () => fitScreenView();
if ($("#pvwrap")) {
  $("#pvwrap").addEventListener("wheel", e => {
    e.preventDefault();
    const factor = e.deltaY < 0 ? 1.12 : (1 / 1.12);
    setPvZoom(PVZOOM * factor);
  }, { passive: false });
}
function openFrameExportModal(fileUrl, defaultName, serverRelFile) {
  const old = document.getElementById("frameModal");
  if (old) old.remove();
  const modal = document.createElement("div");
  modal.id = "frameModal";
  modal.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,0.8);z-index:9999;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(6px);";

  const box = document.createElement("div");
  box.style.cssText = "background:var(--panel, #141124);border:1px solid var(--line, #382e54);border-radius:14px;padding:20px;width:450px;max-width:92vw;box-shadow:0 16px 48px rgba(0,0,0,0.8);display:flex;flex-direction:column;gap:14px;";

  const hdr = document.createElement("div");
  hdr.style.cssText = "display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:10px;";
  hdr.innerHTML = `<div style="font-weight:700;font-size:15px;color:var(--mov, #c4a5ff);display:flex;align-items:center;gap:8px;">${svg("camera")} Ekspòte Frame (@ ${CUR.toFixed(2)}s)</div>`;
  const btnClose = document.createElement("button");
  btnClose.innerHTML = "✕";
  btnClose.style.cssText = "background:none;border:none;color:#aaa;font-size:16px;cursor:pointer;padding:4px 8px;";
  btnClose.onclick = () => modal.remove();
  hdr.appendChild(btnClose);
  box.appendChild(hdr);

  const prevWrap = document.createElement("div");
  prevWrap.style.cssText = "width:100%;height:190px;background:#06050a;border-radius:8px;overflow:hidden;display:flex;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,0.08);";
  const img = document.createElement("img");
  img.src = fileUrl;
  img.style.cssText = "max-width:100%;max-height:100%;object-fit:contain;";
  prevWrap.appendChild(img);
  box.appendChild(prevWrap);

  const nameBox = document.createElement("div");
  nameBox.innerHTML = '<label style="font-size:12px;color:var(--dim, #a1a1aa);display:block;margin-bottom:6px;font-weight:600;">Non fichye a (PNG):</label>';
  const inputName = document.createElement("input");
  inputName.type = "text";
  inputName.value = defaultName;
  inputName.style.cssText = "width:100%;background:#0b0816;border:1px solid var(--line, #382e54);border-radius:8px;padding:8px 12px;color:#fff;font-size:13px;box-sizing:border-box;";
  nameBox.appendChild(inputName);
  box.appendChild(nameBox);

  const actCol = document.createElement("div");
  actCol.style.cssText = "display:flex;flex-direction:column;gap:8px;margin-top:4px;";

  const btnPick = document.createElement("button");
  btnPick.className = "pri";
  btnPick.style.cssText = "display:flex;align-items:center;justify-content:center;gap:8px;padding:10px;font-weight:600;font-size:13px;cursor:pointer;";
  btnPick.innerHTML = svg("folder") + " Chwazi kote pou w mete l (File Explorer)";
  btnPick.onclick = async () => {
    const chosenName = inputName.value.trim() || defaultName;
    if (window.showSaveFilePicker) {
      try {
        const resp = await fetch(fileUrl);
        const blob = await resp.blob();
        const handle = await window.showSaveFilePicker({
          suggestedName: chosenName,
          types: [{ description: "Imaj PNG (*.png)", accept: { "image/png": [".png"] } }]
        });
        const writable = await handle.createWritable();
        await writable.write(blob);
        await writable.close();
        msg("✓ Frame anrejistre nan: " + handle.name);
        modal.remove();
        return;
      } catch (err) {
        if (err.name === "AbortError") return;
      }
    }
    try {
      await api("POST", "/api/audio-bridge", {
        cmd: "save_frame_dialog",
        file: serverRelFile,
        suggestedName: chosenName
      });
      msg("✓ Dyalog eksploratè dosye louvri");
      modal.remove();
      return;
    } catch (ex) {}

    const a = document.createElement("a");
    a.href = fileUrl;
    a.download = chosenName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    msg("✓ Frame telechaje: " + chosenName);
    modal.remove();
  };
  actCol.appendChild(btnPick);

  const rowBtns = document.createElement("div");
  rowBtns.style.cssText = "display:flex;gap:8px;";

  const btnDown = document.createElement("button");
  btnDown.style.cssText = "flex:1;display:flex;align-items:center;justify-content:center;gap:6px;padding:9px;font-size:12px;cursor:pointer;";
  btnDown.innerHTML = svg("download") + " Telechaje dirèkteman";
  btnDown.onclick = () => {
    const chosenName = inputName.value.trim() || defaultName;
    const a = document.createElement("a");
    a.href = fileUrl;
    a.download = chosenName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    msg("✓ Frame telechaje: " + chosenName);
    modal.remove();
  };
  rowBtns.appendChild(btnDown);

  const btnMedia = document.createElement("button");
  btnMedia.style.cssText = "flex:1;display:flex;align-items:center;justify-content:center;gap:6px;padding:9px;font-size:12px;cursor:pointer;";
  btnMedia.innerHTML = svg("image") + " Mete nan Media pwojè";
  btnMedia.onclick = async () => {
    try {
      const chosenName = inputName.value.trim() || defaultName;
      msg("Ap ajoute frame nan medya...");
      const resp = await api("POST", "/api/use-asset", { path: serverRelFile, name: chosenName });
      if (resp.body && resp.body.ok) {
        msg("✓ Frame ajoute nan medya: " + (resp.body.name || resp.body.rel));
        try {
          const mResp = await api("GET", "/api/media");
          if (mResp.body && mResp.body.media) {
            window.IMPORTED = mResp.body.media;
          }
        } catch (x) {}
        selTab("media");
        const mg = $("#mgrid");
        if (mg) renderImported(mg);
        modal.remove();
      } else {
        msg("pa ka ajoute nan medya: " + ((resp.body && resp.body.error) || "?"));
      }
    } catch (e) {
      msg("ere: " + e.message);
    }
  };
  rowBtns.appendChild(btnMedia);
  actCol.appendChild(rowBtns);

  box.appendChild(actCol);
  modal.appendChild(box);
  modal.onclick = e => { if (e.target === modal) modal.remove(); };
  inputName.onkeydown = e => { if (e.key === "Enter") btnPick.click(); };
  document.body.appendChild(modal);
  inputName.focus();
  inputName.select();
}

async function shotFrame() {
  const b = $("#bShot");
  if (b) { b.disabled = true; b.style.opacity = "0.5"; }
  msg("Ap kaptire frame @ " + CUR.toFixed(2) + "s...");
  try {
    const spec = cln();
    if (spec && spec.scenes) {
      spec.scenes.forEach(sc => {
        const tr = (sc.transition || "").toString().toLowerCase().trim();
        if (!tr || !TRANSITIONS.includes(tr)) {
          sc.transition = "fade";
        } else {
          sc.transition = tr;
        }
      });
    }
    const r = await api("POST", "/api/frame", { spec, t: CUR });
    if (r.body && r.body.ok) {
      const fileUrl = r.body.file + "?token=" + encodeURIComponent(TOK);
      const suggestedName = (SPEC.title ? SPEC.title.replace(/[^a-zA-Z0-9_-]/g, "_") : "frame") + "_t" + CUR.toFixed(2) + "s.png";
      msg("✓ Frame pare: " + r.body.file);
      openFrameExportModal(fileUrl, suggestedName, r.body.file);
    } else {
      msg("ere frame: " + ((r.body && r.body.error) || "?"));
    }
  } catch (e) {
    msg("ere frame: " + e.message);
  } finally {
    if (b) { b.disabled = false; b.style.opacity = ""; }
  }
}
$("#bShot").onclick = shotFrame;
if ($("#tZoomMedia")) $("#tZoomMedia").onclick = () => {
  if (CLIPSEL && SPEC.tracks && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) {
    const c = SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c];
    toggleZoomMedia(c.start || 0, c.dur || 2, "clip_" + CLIPSEL.t + "_" + CLIPSEL.c);
  } else if (SEL >= 0 && SPEC.scenes && SPEC.scenes[SEL]) {
    toggleZoomMedia(sStart(SEL), sDur(SEL), "scene_" + SEL);
  } else {
    msg("Chwazi yon clip oswa sèn anvan pou fè zoom sou li");
  }
};
$("#tZoomIn").onclick = () => setZoom(PPS * 1.35);
$("#tZoomOut").onclick = () => setZoom(PPS / 1.35);
$("#tFit").onclick = fit;
$("#tUndo").onclick = () => restore(HIDX - 1);
$("#tRedo").onclick = () => restore(HIDX + 1);
if ($("#tSelect")) $("#tSelect").onclick = () => { TOOL = "select"; $("#tSelect").classList.add("on"); msg("Zouti Seleksyon (V)"); };
if ($("#tSplit")) $("#tSplit").onclick = splitActive;
if ($("#tDelLeft")) $("#tDelLeft").onclick = deleteLeft;
if ($("#tDelRight")) $("#tDelRight").onclick = deleteRight;
if ($("#tDelete")) $("#tDelete").onclick = deleteActive;
if ($("#tFreeze")) $("#tFreeze").onclick = freezeActive;
if ($("#tReverse")) $("#tReverse").onclick = reverseActive;
if ($("#tMirror")) $("#tMirror").onclick = mirrorActive;
if ($("#tRotate")) $("#tRotate").onclick = rotateActive;
if ($("#tCrop")) $("#tCrop").onclick = cropActive;
if ($("#tRecord")) $("#tRecord").onclick = doRecord;
if ($("#tMainMagnet")) $("#tMainMagnet").onclick = toggleMagnet;
if ($("#tSnap")) $("#tSnap").onclick = toggleSnap;
if ($("#tEditMode")) $("#tEditMode").onclick = toggleEditMode;
if ($("#tLinkage")) $("#tLinkage").onclick = toggleLinkage;
if ($("#tScrubAudio")) $("#tScrubAudio").onclick = toggleAudioScrubbing;

$("#tAddTrack").onclick = e => {
  e.stopPropagation();
  const m = $("#trackmenu");
  if (!m) return;
  const isVis = m.style.display === "block";
  const pm = $("#projmenu"); if (pm) pm.style.display = "none";
  if (isVis) { m.style.display = "none"; return; }
  const rc = $("#tAddTrack").getBoundingClientRect();
  m.style.position = "fixed";
  m.style.left = Math.max(8, Math.min(window.innerWidth - 200, rc.left)) + "px";
  m.style.top = Math.max(8, rc.bottom + 4) + "px";
  m.style.right = "auto";
  m.style.display = "block";
};
document.querySelectorAll("#trackmenu .mi").forEach(mi => mi.onclick = e => {
  e.stopPropagation();
  const m = $("#trackmenu"); if (m) m.style.display = "none";
  addTrack(mi.dataset.tk);
});
document.addEventListener("click", () => {
  const tm = $("#trackmenu"); if (tm) tm.style.display = "none";
  const pm = $("#projmenu"); if (pm) pm.style.display = "none";
  const cx = document.getElementById("ctxmenu"); if (cx) cx.remove();
});
document.querySelectorAll("#lrail .rail-btn").forEach(b => { if (b.dataset.lt) b.onclick = () => onLeftRailClick(b.dataset.lt); });
document.querySelectorAll("#rrail .rail-btn").forEach(b => { if (b.dataset.rt) b.onclick = () => onRightRailClick(b.dataset.rt); });
if ($("#bTopAi")) $("#bTopAi").onclick = () => {
  api("POST", "/api/audio-bridge", { cmd: "open_ai_chat", project: PROJNAME || "" }).catch(() => {});
  msg("Ouvri Chat AI WASDEV...");
};
if ($("#bLint")) $("#bLint").onclick = lint;
$("#vtitle").oninput = () => { SPEC.title = $("#vtitle").value; DIRTY = true; };
$("#tlscrollwrap").addEventListener("mousedown", ev => { if (ev.button === 0) seekAt(ev); });
$("#tlscrollwrap").addEventListener("contextmenu", ev => { if (ev.target.closest(".blk")) return; ev.preventDefault(); timelineMenu(ev.clientX, ev.clientY); });
$("#tracks").addEventListener("dragover", ev => { ev.preventDefault(); ev.dataTransfer.dropEffect = "copy"; });
$("#tracks").addEventListener("drop", async ev => {
  ev.preventDefault();
  const cc0 = ev.dataTransfer && ev.dataTransfer.getData("text/kadans-cc0");
  if (cc0) { const r0 = $("#tlinner").getBoundingClientRect(); addLibSound(cc0, Math.max(0, (ev.clientX - r0.left) / PPS)); return; }
  const sfxId = ev.dataTransfer && ev.dataTransfer.getData("text/kadans-sfx");
  if (sfxId) {
    const p = SFX_PRESETS.find(x => x.id === sfxId);
    if (p) {
      const r = $("#tlinner").getBoundingClientRect();
      const tt = Math.max(0, (ev.clientX - r.left) / PPS);
      const ti = ensureTrack("sfx");
      const tk = SPEC.tracks[ti];
      tk.clips = tk.clips || [];
      tk.clips.push({ kind: "sfx", sfx: p.id, label: p.name, start: tt, dur: p.dur });
      DIRTY = true; renderTimeline(); renderRight();
      msg("SFX '" + p.name + "' lage sou track @ " + tt.toFixed(1) + "s");
      return;
    }
  }
  const mediaList = await extractDropMedia(ev);
  if (!mediaList || !mediaList.length) return;
  const r = $("#tlinner").getBoundingClientRect();
  let tt = Math.max(0, (ev.clientX - r.left) / PPS);
  for (const m of mediaList) {
    const ti = ensureTrack(m.kind);
    const d = await dropAssetOnTrack(m.rel, ti, tt, m.kind);
    tt += (d || 2) + 0.2;
  }
});
// Defilman vètikal: kenbe kolòn non track yo aliye ak track yo (sa ki anba Sen vin vizib)
$("#tlscrollwrap").addEventListener("scroll", () => { const n = $("#names"); if (n) n.style.transform = "translateY(" + (-$("#tlscrollwrap").scrollTop) + "px)"; });
const tlscroll = $("#tlscrollwrap");
if (tlscroll) {
  tlscroll.addEventListener("wheel", e => {
    if (e.ctrlKey || e.altKey) {
      e.preventDefault();
      const rect = tlscroll.getBoundingClientRect();
      const mouseX = e.clientX - rect.left + tlscroll.scrollLeft;
      const tAtMouse = mouseX / PPS;
      const factor = e.deltaY < 0 ? 1.25 : 0.8;
      const newPPS = Math.max(8, Math.min(500, PPS * factor));
      if (newPPS !== PPS) {
        PPS = newPPS;
        renderTimeline();
        tlscroll.scrollLeft = Math.max(0, tAtMouse * PPS - (e.clientX - rect.left));
      }
    }
  }, { passive: false });
}
wireViewerDrop();
window.addEventListener("dragover", ev => { ev.preventDefault(); });
window.addEventListener("drop", ev => { ev.preventDefault(); });
const leftEl = $("#left");
if (leftEl) {
  leftEl.addEventListener("dragover", ev => { ev.preventDefault(); ev.dataTransfer.dropEffect = "copy"; });
  leftEl.addEventListener("drop", async ev => {
    ev.preventDefault();
    if (ev.dataTransfer && ev.dataTransfer.files && ev.dataTransfer.files.length) {
      await importMedia(ev.dataTransfer.files);
      selTab("media");
    }
  });
}
// Rakousi tankou pwofesyonel
function pasteAfter(idx) { if (!CLIP) { msg("pa gen anyen kopye"); return; } snapshot(); const c = JSON.parse(JSON.stringify(CLIP)); c.id = (c.id || "s") + "_" + Math.random().toString(36).slice(2, 5); const at = (idx < 0 ? SPEC.scenes.length - 1 : idx); SPEC.scenes.splice(at + 1, 0, c); SEL = at + 1; DIRTY = true; renderTimeline(); renderRight(); renderLeft(); msg("kole"); }
function dupAt(idx) { if (idx < 0) return; snapshot(); const c = JSON.parse(JSON.stringify(SPEC.scenes[idx])); c.id = (c.id || "s") + "_" + Math.random().toString(36).slice(2, 5); SPEC.scenes.splice(idx + 1, 0, c); SEL = idx + 1; DIRTY = true; renderTimeline(); renderRight(); renderLeft(); msg("double"); }
// ---- Clip yo sou yon track (CLIPSEL = {t, c}) — menm rakousi ak sèn yo, men yo aji sou clip ki chwazi a, ak Undo.
let CLIP_ATTRS = null;
function copyClipAttributes(ti, ci) {
  const c = SPEC.tracks[ti].clips[ci];
  CLIP_ATTRS = {
    fx: c.fx ? JSON.parse(JSON.stringify(c.fx)) : null,
    lut: c.lut || null,
    mask: c.mask ? JSON.parse(JSON.stringify(c.mask)) : null,
    chroma: c.chroma ? JSON.parse(JSON.stringify(c.chroma)) : null,
    keys: c.keys ? JSON.parse(JSON.stringify(c.keys)) : null,
    volume: c.volume != null ? c.volume : null,
    fadein: c.fadein != null ? c.fadein : null,
    fadeout: c.fadeout != null ? c.fadeout : null,
    speed: c.speed != null ? c.speed : null,
    speedKeys: c.speedKeys ? JSON.parse(JSON.stringify(c.speedKeys)) : null
  };
  msg('Atribi clip kopye');
}

function pasteClipAttributes(ti, ci) {
  if (!CLIP_ATTRS) { msg('Pa gen atribi kopye (fè Kopye atribi anvan)'); return; }
  const c = SPEC.tracks[ti].clips[ci];
  const old = document.getElementById('attripop'); if (old) old.remove();
  const back = document.createElement('div'); back.id = 'attripop';
  back.style.cssText = 'position:fixed;inset:0;background:#0008;z-index:250;display:flex;align-items:center;justify-content:center';
  const box = document.createElement('div'); box.style.cssText = 'background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;width:320px;box-shadow:0 12px 40px #000c';
  box.innerHTML = '<h3 style="color:var(--mov);margin:0 0 10px;font-size:14px">Kole Atribi Selektif</h3><div style="font-size:11px;color:var(--dim);margin-bottom:12px">Chwazi atribi ou vle aplike:</div>';
  const opts = [
    { id: 'opt_fx', key: 'fx', lab: 'Koulè & Efè (FX, courbes, tonemap)' },
    { id: 'opt_lut', key: 'lut', lab: 'Look Sinema (LUT)' },
    { id: 'opt_mask', key: 'mask', lab: 'Mask & Fòm (Mask)' },
    { id: 'opt_chroma', key: 'chroma', lab: 'Chroma Key (Green screen)' },
    { id: 'opt_vol', key: 'volume', lab: 'Son (Volim, Fade In/Out)' },
    { id: 'opt_keys', key: 'keys', lab: 'Animasyon & Keyframes' },
    { id: 'opt_speed', key: 'speed', lab: 'Vitès & Speed Ramping' }
  ];
  const checks = {};
  opts.forEach(op => {
    const hasAttr = CLIP_ATTRS[op.key] != null;
    const row = document.createElement('label'); row.style.cssText = 'display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:12px;cursor:pointer;' + (hasAttr ? 'color:var(--text)' : 'color:var(--dim);opacity:0.6;');
    const cb = document.createElement('input'); cb.type = 'checkbox'; cb.checked = hasAttr; cb.disabled = !hasAttr;
    checks[op.key] = cb;
    row.appendChild(cb); row.appendChild(document.createTextNode(op.lab + (hasAttr ? '' : ' (pa disponib)')));
    box.appendChild(row);
  });
  const rowBtn = document.createElement('div'); rowBtn.style.cssText = 'display:flex;gap:8px;margin-top:14px';
  const btnOk = document.createElement('button'); btnOk.className = 'pri'; btnOk.style.flex = '1'; btnOk.textContent = 'Kole';
  btnOk.onclick = () => {
    snapshot();
    if (checks.fx.checked && CLIP_ATTRS.fx) c.fx = JSON.parse(JSON.stringify(CLIP_ATTRS.fx));
    if (checks.lut.checked && CLIP_ATTRS.lut) c.lut = CLIP_ATTRS.lut;
    if (checks.mask.checked && CLIP_ATTRS.mask) c.mask = JSON.parse(JSON.stringify(CLIP_ATTRS.mask));
    if (checks.chroma.checked && CLIP_ATTRS.chroma) c.chroma = JSON.parse(JSON.stringify(CLIP_ATTRS.chroma));
    if (checks.volume.checked) {
      if (CLIP_ATTRS.volume != null) c.volume = CLIP_ATTRS.volume;
      if (CLIP_ATTRS.fadein != null) c.fadein = CLIP_ATTRS.fadein;
      if (CLIP_ATTRS.fadeout != null) c.fadeout = CLIP_ATTRS.fadeout;
    }
    if (checks.keys.checked && CLIP_ATTRS.keys) c.keys = JSON.parse(JSON.stringify(CLIP_ATTRS.keys));
    if (checks.speed.checked) {
      if (CLIP_ATTRS.speed != null) c.speed = CLIP_ATTRS.speed;
      if (CLIP_ATTRS.speedKeys) c.speedKeys = JSON.parse(JSON.stringify(CLIP_ATTRS.speedKeys));
    }
    back.remove(); DIRTY = true; renderTimeline(); renderRight(); msg('Atribi kole ak siksè');
  };
  const btnCancel = document.createElement('button'); btnCancel.textContent = 'Anile'; btnCancel.onclick = () => back.remove();
  rowBtn.appendChild(btnOk); rowBtn.appendChild(btnCancel); box.appendChild(rowBtn);
  back.appendChild(box); document.body.appendChild(back);
  back.onclick = ev => { if (ev.target === back) back.remove(); };
}

function closeTrackGap(ti, ci) {
  if (ti == null || !SPEC.tracks || !SPEC.tracks[ti]) return;
  const tk = SPEC.tracks[ti];
  if (tk.locked) { msg('track bloke'); return; }
  const clips = tk.clips || [];
  if (ci <= 0 || ci >= clips.length) { msg('Pa gen twou devan clip sa a'); return;
 }
  const target = clips[ci];
  let prevEnd = 0;
  for (let k = 0; k < clips.length; k++) {
    if (k !== ci && (clips[k].start || 0) < (target.start || 0)) {
      const pe = (clips[k].start || 0) + (clips[k].dur || 2);
      if (pe > prevEnd) prevEnd = pe;
    }
  }
  const gap = Math.round(((target.start || 0) - prevEnd) * 1000) / 1000;
  if (gap > 0.01) {
    snapshot();
    const st = target.start || 0;
    clips.forEach(cl => {
      if ((cl.start || 0) >= st - 0.001) {
        cl.start = Math.max(0, Math.round(((cl.start || 0) - gap) * 1000) / 1000);
      }
    });
    (SPEC.tracks || []).forEach((otk, oi) => {
      if (oi !== ti && !otk.locked && otk.sync_lock !== false) {
        (otk.clips || []).forEach(oc => {
          if ((oc.start || 0) >= st - 0.001) {
            oc.start = Math.max(0, Math.round(((oc.start || 0) - gap) * 1000) / 1000);
          }
        });
      }
    });
    DIRTY = true; renderTimeline(); renderRight(); renderLeft();
    msg('Twou ' + gap.toFixed(2) + 's fèmen (ripple)');
  } else {
    msg('Pa gen twou devan clip sa a');
  }
}

function topTailTrim(edge) {
  if (CLIPSEL && SPEC.tracks && SPEC.tracks[CLIPSEL.t] && SPEC.tracks[CLIPSEL.t].clips && SPEC.tracks[CLIPSEL.t].clips[CLIPSEL.c]) {
    const ti = CLIPSEL.t, tk = SPEC.tracks[ti];
    if (tk.locked) { msg('track bloke'); return; }
    const c = tk.clips[CLIPSEL.c], st = c.start || 0, dur = c.dur || 2;
    if (CUR > st + 0.02 && CUR < st + dur - 0.02) {
      snapshot();
      if (edge === 'head') {
        const delta = Math.round((CUR - st) * 1000) / 1000;
        c.dur = Math.max(0.1, Math.round((dur - delta) * 1000) / 1000);
        if (c.src) c.in = Math.round(((c.in || 0) + delta * (c.speed || 1)) * 1000) / 1000;
        const oldEnd = st + dur;
        (tk.clips || []).forEach(other => {
          if (other !== c && (other.start || 0) >= oldEnd - 0.01) {
            other.start = Math.max(0, Math.round(((other.start || 0) - delta) * 1000) / 1000);
          }
        });
        (SPEC.tracks || []).forEach((otk, oi) => {
          if (oi !== ti && !otk.locked && otk.sync_lock !== false) {
            (otk.clips || []).forEach(oc => {
              if ((oc.start || 0) >= oldEnd - 0.01) {
                oc.start = Math.max(0, Math.round(((oc.start || 0) - delta) * 1000) / 1000);
              }
            });
          }
        });
        CUR = st;
        msg('Top trim (Q) aplike');
      } else {
        const delta = Math.round(((st + dur) - CUR) * 1000) / 1000;
        c.dur = Math.max(0.1, Math.round((CUR - st) * 1000) / 1000);
        const oldEnd = st + dur;
        (tk.clips || []).forEach(other => {
          if (other !== c && (other.start || 0) >= oldEnd - 0.01) {
            other.start = Math.max(0, Math.round(((other.start || 0) - delta) * 1000) / 1000);
          }
        });
        (SPEC.tracks || []).forEach((otk, oi) => {
          if (oi !== ti && !otk.locked && otk.sync_lock !== false) {
            (otk.clips || []).forEach(oc => {
              if ((oc.start || 0) >= oldEnd - 0.01) {
                oc.start = Math.max(0, Math.round(((oc.start || 0) - delta) * 1000) / 1000);
              }
            });
          }
        });
        msg('Tail trim (W) aplike');
      }
      DIRTY = true; renderTimeline(); renderRight(); movePlayhead();
      return;
    }
  }
  const idx = (SEL >= 0 ? SEL : sceneAt(CUR));
  if (idx >= 0 && SPEC.scenes && SPEC.scenes[idx]) {
    const sc = SPEC.scenes[idx];
    const st = sStart(idx), dur = sDur(idx);
    if (CUR > st + 0.02 && CUR < st + dur - 0.02) {
      snapshot();
      if (edge === 'head') {
        const cut = Math.round((CUR - st) * 1000) / 1000;
        sc.duration = Math.max(0.2, Math.round((dur - cut) * 100) / 100);
        if (sc.type === 'video') sc.in = Math.round(((sc.in || 0) + cut * (sc.speed || 1)) * 1000) / 1000;
        CUR = st;
        msg('Top trim (Q) sèn aplike');
      } else {
        const newDur = Math.round((CUR - st) * 1000) / 1000;
        sc.duration = Math.max(0.2, Math.round(newDur * 100) / 100);
        msg('Tail trim (W) sèn aplike');
      }
      DIRTY = true; renderTimeline(); renderRight(); movePlayhead();
    }
  }
}

function _selClip() { if (!CLIPSEL || !SPEC.tracks) return null; const tk = SPEC.tracks[CLIPSEL.t]; return (tk && tk.clips && tk.clips[CLIPSEL.c]) ? tk : null; }
function clipCopy() { const tk = _selClip(); if (!tk) return false; CLIP = { __clip: JSON.parse(JSON.stringify(tk.clips[CLIPSEL.c])) }; msg("clip kopye"); return true; }
function clipDelete() { const tk = _selClip(); if (!tk) return false; snapshot(); tk.clips.splice(CLIPSEL.c, 1); CLIPSEL = null; DIRTY = true; renderTimeline(); renderRight(); renderLeft(); msg("clip efase"); return true; }
function clipDeleteRipple() {  // ripple: efase clip la EPI deplase clip ki apre yo agoch pou bouche twou a
  const tk = _selClip(); if (!tk) return false;
  const gone = tk.clips[CLIPSEL.c], gs = gone.start || 0, gd = gone.dur || 0;
  snapshot(); tk.clips.splice(CLIPSEL.c, 1);
  tk.clips.forEach(c => { if ((c.start || 0) >= gs) c.start = Math.max(0, Math.round(((c.start || 0) - gd) * 1000) / 1000); });
  CLIPSEL = null; DIRTY = true; renderTimeline(); renderRight(); renderLeft(); msg("clip efase (ripple)"); return true;
}
function clipCut() { return clipCopy() && clipDelete(); }
function clipDup() { const tk = _selClip(); if (!tk) return false; snapshot(); const c = tk.clips[CLIPSEL.c]; const d = JSON.parse(JSON.stringify(c)); d.start = (c.start || 0) + (c.dur || 2); tk.clips.push(d); CLIPSEL = { t: CLIPSEL.t, c: tk.clips.length - 1 }; DIRTY = true; renderTimeline(); renderRight(); renderLeft(); msg("clip double"); return true; }
function clipPaste() { if (!CLIP || !CLIP.__clip) return false; const ti = CLIPSEL ? CLIPSEL.t : null; if (ti == null || !SPEC.tracks || !SPEC.tracks[ti]) { msg("chwazi yon track pou kole clip la"); return false; } snapshot(); const tk = SPEC.tracks[ti]; const d = JSON.parse(JSON.stringify(CLIP.__clip)); const ci = placeClipAt(tk, d, CUR); CLIPSEL = { t: ti, c: ci }; DIRTY = true; renderTimeline(); renderRight(); renderLeft(); msg("clip kole (" + EDITMODE + ")"); return true; }
document.addEventListener("keydown", e => {
  const tn = e.target.tagName || "", ty = (e.target.type || "").toLowerCase();
  const typing = tn === "TEXTAREA" || e.target.isContentEditable ||
    (tn === "INPUT" && (ty === "" || ["text", "number", "search", "email", "url", "password", "tel"].indexOf(ty) >= 0));
  if (typing) return;
  // A list or a slider keeps its arrows (they change the value, not the playhead); Space / J / K / L still work.
  // Yon lis, yon slider oswa yon dropdown kenbe navigasyon + efase pa l (pa touche sèn / clip la).
  if ((tn === "SELECT" || ty === "range") && ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End", "PageUp", "PageDown", "Delete", "Backspace"].indexOf(e.key) >= 0) return;
  const k = e.key;
  if (e.ctrlKey || e.metaKey) {
    if (k === "z" || k === "Z") { e.preventDefault(); restore(e.shiftKey ? HIDX + 1 : HIDX - 1); }
    else if (k === "y" || k === "Y") { e.preventDefault(); restore(HIDX + 1); }
    else if (k === "s" || k === "S") { e.preventDefault(); save(); }
    else if (k === "n" || k === "N") { e.preventDefault(); newProject(); }
    else if (k === "o" || k === "O") { e.preventDefault(); const fi = $("#fiOpenFile"); if (fi) { fi.value = ""; fi.click(); } }
    // Ctrl+C/X/V/D: si yon CLIP chwazi (CLIPSEL) → aji sou clip la; sinon sou sèn ki chwazi a (SEL).
    else if (k === "c" || k === "C") { if (CLIPSEL) clipCopy(); else if (SEL >= 0) { CLIP = JSON.parse(JSON.stringify(SPEC.scenes[SEL])); msg("kopye"); } }
    else if (k === "x" || k === "X") { if (CLIPSEL) clipCut(); else if (SEL >= 0) { CLIP = JSON.parse(JSON.stringify(SPEC.scenes[SEL])); delScene(); } }
    else if (k === "v" || k === "V") { e.preventDefault(); if (CLIP && CLIP.__clip) clipPaste(); else pasteAfter(SEL); }
    else if (k === "d" || k === "D") { e.preventDefault(); if (CLIPSEL) clipDup(); else dupAt(SEL); }
    return;
  }
  if (k === "q" || k === "Q") { e.preventDefault(); topTailTrim("head"); }
  else if (k === "w" || k === "W") { e.preventDefault(); topTailTrim("tail"); }
  else if (k === "v" || k === "V") setTool("select");
  else if (k === "c" || k === "C" || k === "b" || k === "B") { setTool("split"); if (SEL >= 0 || sceneAt(CUR) >= 0) splitAt(); }
  else if (k === "a" || k === "A") doTool(e.shiftKey ? "selleft" : "selright");
  else if (k === "[") doTool("selleft");
  else if (k === "]") doTool("selright");
  else if (k === "s" || k === "S") { SNAP = !SNAP; $("#tSnap").classList.toggle("on", SNAP); msg("snap " + (SNAP ? "on" : "off")); }
  else if (k === "m" || k === "M") addKeyframe();
  else if (k === "=" || k === "+") setZoom(PPS * 1.4);
  else if (k === "-" || k === "_") setZoom(PPS / 1.4);
  else if (k === "Home") {
    const wasPlaying = playing;
    stopAudio(); CUR = 0; movePlayhead(); post({ cmd: "seek", t: 0 });
    if (wasPlaying) playAudio();
  }
  else if (k === "End") {
    setPlaying(false); CUR = total(); movePlayhead(); post({ cmd: "seek", t: CUR });
  }
  else if (k === " " || k === "k" || k === "K") { e.preventDefault(); setPlaying(!playing); }
  else if (k === "l" || k === "L") { setPlaying(true); }
  else if (k === "j" || k === "J") {
    const wasPlaying = playing;
    stopAudio(); CUR = Math.max(0, CUR - 0.5); movePlayhead(); post({ cmd: "seek", t: CUR });
    if (wasPlaying) playAudio();
  }
  else if (k === "ArrowLeft") {
    const wasPlaying = playing;
    stopAudio(); CUR = Math.max(0, CUR - (e.shiftKey ? 1 : 0.1)); movePlayhead(); post({ cmd: "seek", t: CUR });
    if (wasPlaying) playAudio();
  }
  else if (k === "ArrowRight") {
    const wasPlaying = playing;
    stopAudio(); CUR = Math.min(total(), CUR + (e.shiftKey ? 1 : 0.1)); movePlayhead(); post({ cmd: "seek", t: CUR });
    if (wasPlaying) playAudio();
  }
  // Efase (Delete oswa Backspace): clip ki chwazi a, vwa ki chwazi a, sinon sèn si se sou track sèn.
  else if (k === "Delete" || k === "Backspace") {
    if (CLIPSEL) {
      e.preventDefault();
      e.shiftKey ? clipDeleteRipple() : clipDelete();
    } else if (TRACKSEL === "voice" || VOICESEL != null) {
      e.preventDefault();
      const vi = (VOICESEL != null ? VOICESEL : (TRACKSEL === "voice" ? SEL : -1));
      if (vi >= 0 && SPEC.scenes && SPEC.scenes[vi]) {
        const sc = SPEC.scenes[vi];
        snapshot();
        delete sc.voice; delete sc.voice_file; delete sc._regen;
        delete sc.voice_offset; delete sc.voice_in; delete sc.voice_dur;
        VOICESEL = null;
        DIRTY = true; renderTimeline(); renderRight(); renderLeft();
        msg("Vwa sèn " + (vi + 1) + " efase (sèn nan rete entak, timeline pa redwi)");
      }
    } else if (TRACKSEL === "scenes" && SEL >= 0) {
      e.preventDefault();
      delScene();
    } else if (SEL >= 0 && TRACKSEL !== "music") {
      e.preventDefault();
      delScene();
    }
  }
});
addEventListener("beforeunload", e => { if (DIRTY) { e.preventDefault(); e.returnValue = ""; } });
$("#bProj").onclick = e => {
  e.stopPropagation();
  renderProjectMenu();
  const m = $("#projmenu");
  if (!m) return;
  const isVis = m.style.display === "block";
  const tm = $("#trackmenu"); if (tm) tm.style.display = "none";
  if (isVis) { m.style.display = "none"; return; }
  const rc = $("#bProj").getBoundingClientRect();
  m.style.position = "fixed";
  m.style.left = Math.max(8, rc.left) + "px";
  m.style.top = (rc.bottom + 4) + "px";
  m.style.display = "block";
};
// ---- Compressor popup (vrè, manipilab) ----
function openCompressor() {
  SPEC.voice = SPEC.voice || {}; SPEC.voice.compressor = SPEC.voice.compressor || {};
  const C = SPEC.voice.compressor;
  const defs = { threshold: [-60, 0, 1, -18, "dB"], ratio: [1, 20, 0.5, 3, ":1"], attack: [0.1, 200, 0.1, 5, "ms"], release: [1, 1000, 1, 140, "ms"], makeup: [0, 24, 0.5, 2, "dB"] };
  const old = document.getElementById("cpop"); if (old) old.remove();
  const back = document.createElement("div"); back.id = "cpop";
  back.style.cssText = "position:fixed;inset:0;background:#000a;z-index:100;display:flex;align-items:center;justify-content:center";
  const box = document.createElement("div");
  box.style.cssText = "background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;width:340px;box-shadow:0 12px 40px #000c";
  box.innerHTML = '<h3 style="color:var(--mov);margin:0 0 4px;font-size:13px">Compressor vwa (master)</h3><div style="color:var(--dim);font-size:11px;margin-bottom:8px">Rann sou vwa a (FFmpeg acompressor). Aplike = rebati videyo a.</div>';
  back.appendChild(box); document.body.appendChild(back);
  back.onclick = e => { if (e.target === back) back.remove(); };
  Object.keys(defs).forEach(k => {
    const d = defs[k]; const val = C[k] != null ? C[k] : d[3];
    const l = document.createElement("label"); l.style.cssText = "display:block;color:var(--dim);font-size:12px;margin:8px 0 2px"; l.textContent = k + ": " + val + " " + d[4];
    const r = document.createElement("input"); r.type = "range"; r.min = d[0]; r.max = d[1]; r.step = d[2]; r.value = val; r.style.width = "100%";
    r.oninput = () => { C[k] = +r.value; l.textContent = k + ": " + r.value + " " + d[4]; DIRTY = true; };
    box.appendChild(l); box.appendChild(r);
  });
  const row = document.createElement("div"); row.style.cssText = "display:flex;gap:6px;margin-top:12px";
  const ap = document.createElement("button"); ap.className = "pri"; ap.style.flex = "1"; ap.textContent = "Aplike (rann)"; ap.onclick = () => { back.remove(); build(); msg("compressor aplike"); };
  const rs = document.createElement("button"); rs.textContent = "Reset"; rs.onclick = () => { delete SPEC.voice.compressor; DIRTY = true; back.remove(); openCompressor(); };
  const cl = document.createElement("button"); cl.textContent = "Fèmen"; cl.onclick = () => back.remove();
  row.appendChild(ap); row.appendChild(rs); row.appendChild(cl); box.appendChild(row);
}

// ---- Anrejistre vwa (chwazi mikro -> voice_file sou sen chwazi a) ----
let MREC = null, MCHUNKS = [], RECTARGET = null;
async function recordSceneVoice() {
  if (MREC && MREC.state === "recording") { MREC.stop(); return; }
  if (SEL < 0) { msg("chwazi yon sen pou anrejistre vwa li"); return; }
  RECTARGET = { scene: SEL }; doRecord();
}
async function recordVoice() {
  if (MREC && MREC.state === "recording") { MREC.stop(); return; }
  let ti = null;
  if (TRACKSEL && TRACKSEL.indexOf("tk") === 0) { const x = +TRACKSEL.slice(2); if (SPEC.tracks[x] && SPEC.tracks[x].kind === "audio") ti = x; }
  if (ti == null) ti = ensureTrack("audio");
  TRACKSEL = "tk" + ti; RECTARGET = { track: ti }; doRecord();
}
async function recordToTrack(ti) {
  if (MREC && MREC.state === "recording") { MREC.stop(); return; }
  RECTARGET = { track: ti }; doRecord();
}
function doRecord() {
  let mic = ""; try { mic = localStorage.getItem("kd_mic") || ""; } catch (x) {}
  if (!mic) { openMicPicker(); return; }   // premye fwa sèlman -> chwazi
  startRecording(mic);
}
async function openMicPicker() {
  let devices = [];
  try {
    const tmp = await navigator.mediaDevices.getUserMedia({ audio: true });
    tmp.getTracks().forEach(x => x.stop());
    devices = (await navigator.mediaDevices.enumerateDevices()).filter(d => d.kind === "audioinput");
  } catch (e) { msg("pa ka jwenn mikro a: " + (e.message || e)); return; }
  let saved = ""; try { saved = localStorage.getItem("kd_mic") || ""; } catch (x) {}
  const old = document.getElementById("micpop"); if (old) old.remove();
  const back = document.createElement("div"); back.id = "micpop";
  back.style.cssText = "position:fixed;inset:0;background:#000a;z-index:100;display:flex;align-items:center;justify-content:center";
  const box = document.createElement("div"); box.style.cssText = "background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;width:360px;box-shadow:0 12px 40px #000c";
  box.innerHTML = '<h3 style="color:var(--mov);margin:0 0 4px;font-size:13px">Chwazi mikro a</h3><div style="color:var(--dim);font-size:11px;margin-bottom:8px">Chwa sa a ap sonje pou pwochen fwa yo (ou ka chanje l nenpot kile).</div>';
  const sel = document.createElement("select"); sel.style.cssText = "width:100%;background:#0e0b1a;border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:8px";
  devices.forEach((d, i) => { const o = document.createElement("option"); o.value = d.deviceId; o.textContent = d.label || ("Mikro " + (i + 1)); if (d.deviceId === saved) o.selected = true; sel.appendChild(o); });
  box.appendChild(sel);
  const row = document.createElement("div"); row.style.cssText = "display:flex;gap:6px;margin-top:12px";
  const go = document.createElement("button"); go.className = "pri"; go.style.flex = "1"; go.innerHTML = svg("record") + "Komanse anrejistre";
  go.onclick = () => { try { localStorage.setItem("kd_mic", sel.value); } catch (x) {} back.remove(); startRecording(sel.value); };
  const cl = document.createElement("button"); cl.textContent = "Anile"; cl.onclick = () => back.remove();
  row.appendChild(go); row.appendChild(cl); box.appendChild(row);
  back.appendChild(box); document.body.appendChild(back);
  back.onclick = e => { if (e.target === back) back.remove(); };
}
window.SETSEC = window.SETSEC || "video";
function openSettings() {
  const old = document.getElementById("setpop"); if (old) old.remove();
  const back = document.createElement("div"); back.id = "setpop"; back.style.cssText = "position:fixed;inset:0;background:#000b;z-index:120;display:flex;align-items:center;justify-content:center";
  const box = document.createElement("div"); box.style.cssText = "position:relative;background:var(--panel);border:1px solid var(--line);border-radius:14px;width:min(720px,94vw);height:min(500px,88vh);display:flex;overflow:hidden;box-shadow:0 20px 60px #000d";
  const menu = document.createElement("div"); menu.style.cssText = "width:186px;flex:none;background:#0e0b1a;border-right:1px solid var(--line);padding:14px 10px;display:flex;flex-direction:column;gap:4px";
  const brand = document.createElement("div"); brand.style.cssText = "display:flex;align-items:center;gap:8px;color:var(--mov);font-weight:800;font-size:14px;padding:2px 8px 14px"; brand.innerHTML = svg("settings") + "Paramet Kadans"; menu.appendChild(brand);
  const content = document.createElement("div"); content.id = "setcontent"; content.style.cssText = "flex:1;overflow:auto;padding:22px 24px";
  const secs = [["video", "Videyo", "film"], ["audio", "Audio", "music"], ["text", "Teks & Tit", "text"], ["color", "Koule", "palette"], ["project", "Pwoje", "folder"], ["general", "Jeneral", "sliders"]];
  secs.forEach(sx => {
    const on = window.SETSEC === sx[0];
    const b = document.createElement("div");
    b.style.cssText = "display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:10px;cursor:pointer;font-size:13px;font-weight:600;" + (on ? "background:linear-gradient(90deg,#8b5cf6,#6d28d9);color:#fff;box-shadow:0 3px 12px #8b5cf644" : "color:var(--dim)");
    b.innerHTML = svg(sx[2]) + "<span>" + sx[1] + "</span>";
    if (!on) { b.onmouseenter = () => b.style.background = "#1c1733"; b.onmouseleave = () => b.style.background = "transparent"; }
    b.onclick = () => { window.SETSEC = sx[0]; openSettings(); };
    menu.appendChild(b);
  });
  const xb = document.createElement("div"); xb.textContent = "✕"; xb.title = "Femen"; xb.style.cssText = "position:absolute;top:12px;right:16px;color:var(--dim);cursor:pointer;font-size:17px;z-index:3;line-height:1"; xb.onmouseenter = () => xb.style.color = "var(--err)"; xb.onmouseleave = () => xb.style.color = "var(--dim)"; xb.onclick = () => back.remove();
  box.appendChild(menu); box.appendChild(content); box.appendChild(xb); back.appendChild(box); document.body.appendChild(back);
  back.onclick = e => { if (e.target === back) back.remove(); };
  renderSettingsSection(content);
}
async function renderSettingsSection(f) {
  f.innerHTML = "";
  const H = txt => { const h = document.createElement("h3"); h.textContent = txt; h.style.cssText = "color:var(--mov);margin:0 0 8px;font-size:14px"; f.appendChild(h); };
  const sel = (lab, opts, get, set) => { const l = document.createElement("label"); l.textContent = lab; l.style.cssText = "color:var(--dim);font-size:12px;display:block;margin:10px 0 3px"; f.appendChild(l); const sl = document.createElement("select"); sl.style.cssText = "width:100%;background:#0e0b1a;border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:8px"; opts.forEach(o => { const op = document.createElement("option"); op.value = o; op.textContent = o === "" ? "(defo)" : o; if (String(get()) === String(o)) op.selected = true; sl.appendChild(op); }); sl.onchange = () => { set(sl.value); DIRTY = true; build(); }; f.appendChild(sl); };
  const rng = (lab, mn, mx, st, get, set) => { const l = document.createElement("label"); l.textContent = lab + ": " + get(); l.style.cssText = "color:var(--dim);font-size:12px;display:block;margin:10px 0 3px"; f.appendChild(l); const r = document.createElement("input"); r.type = "range"; r.min = mn; r.max = mx; r.step = st; r.value = get(); r.style.width = "100%"; r.oninput = () => { set(+r.value); l.textContent = lab + ": " + r.value; DIRTY = true; }; r.onchange = build; f.appendChild(r); };
  const chk = (lab, get, set) => { const l = document.createElement("label"); l.style.cssText = "display:flex;align-items:center;gap:8px;margin:10px 0;cursor:pointer;color:var(--fg)"; const c = document.createElement("input"); c.type = "checkbox"; c.style.width = "auto"; c.checked = get(); c.onchange = () => { set(c.checked); DIRTY = true; }; l.appendChild(c); l.appendChild(document.createTextNode(lab)); f.appendChild(l); };
  const note = txt => { const d = document.createElement("div"); d.style.cssText = "color:var(--dim);font-size:11px;margin-top:10px;line-height:1.5"; d.textContent = txt; f.appendChild(d); };
  const S = window.SETSEC;
  if (S === "video") {
    H("Videyo");
    sel("Ratio (fomada videyo a)", ["16:9", "9:16", "1:1", "4:5", "4:3", "21:9"], () => SPEC.ratio || "16:9", v => { SPEC.ratio = v; });
    sel("FPS (imaj pa segonn)", ["24", "30", "60"], () => SPEC.fps || 30, v => { SPEC.fps = +v; });
  } else if (S === "audio") {
    H("Audio");
    rng("Master volim (%)", 0, 200, 5, () => Math.round((SPEC.volume != null ? SPEC.volume : 1) * 100), v => { setMasterVol(v / 100); });
    chk("Netwaye vwa (compressor + EQ + de-esser + limiter)", () => (SPEC.voice ? SPEC.voice.enhance !== false : true), v => { SPEC.voice = SPEC.voice || {}; SPEC.voice.enhance = v; });
    const cb = document.createElement("button"); cb.innerHTML = svg("sliders") + "Regle compressor vwa a"; cb.style.cssText = "margin:8px 0;width:100%;justify-content:center"; cb.onclick = () => { const sp = document.getElementById("setpop"); if (sp) sp.remove(); openCompressor(); }; f.appendChild(cb);
    sel("Lang vwa & narasyon", ["ht", "fr", "en", "es", "pt", "ru", "it", "de"], () => (SPEC.voice && SPEC.voice.lang) || SPEC.lang || "fr", v => { SPEC.voice = SPEC.voice || {}; SPEC.voice.lang = v; SPEC.lang = v; if ($("#vlang")) $("#vlang").value = v; });
    const l = document.createElement("label"); l.textContent = "Mikro ofisyèl WASDEV (Audio IN)"; l.style.cssText = "color:var(--mov);font-weight:600;font-size:12px;display:block;margin:10px 0 3px"; f.appendChild(l);
    const ms = document.createElement("select"); ms.style.cssText = "width:100%;background:#0e0b1a;border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:8px"; f.appendChild(ms);
    let saved = ""; try { saved = localStorage.getItem("kd_mic") || ""; } catch (x) {}
    let devices = [];
    try { const tmp = await navigator.mediaDevices.getUserMedia({ audio: true }); tmp.getTracks().forEach(x => x.stop()); devices = (await navigator.mediaDevices.enumerateDevices()).filter(d => d.kind === "audioinput"); } catch (e) {}
    if (!devices.length) { const o = document.createElement("option"); o.value = ""; o.textContent = "(bay otorizasyon mikro a)"; ms.appendChild(o); }
    devices.forEach((d, i) => { const o = document.createElement("option"); o.value = d.deviceId; o.textContent = d.label || ("Mikro " + (i + 1)); if (d.deviceId === saved) o.selected = true; ms.appendChild(o); });
    ms.onchange = () => {
      const opt = ms.options[ms.selectedIndex]; const name = opt ? opt.textContent : "";
      try { localStorage.setItem("kd_mic", ms.value); localStorage.setItem("kd_mic_name", name); } catch (x) {}
      api("POST", "/api/audio-settings", { input_name: name, input_id: ms.value }).catch(() => {});
      msg("mikro ofisyèl WASDEV anrejistre nan tout sistèm nan");
    };
    const l2 = document.createElement("label"); l2.textContent = "Sòti son ofisyèl WASDEV (Audio OUT / Oratè)"; l2.style.cssText = "color:var(--mov);font-weight:600;font-size:12px;display:block;margin:10px 0 3px"; f.appendChild(l2);
    const os = document.createElement("select"); os.style.cssText = "width:100%;background:#0e0b1a;border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:8px"; f.appendChild(os);
    let savedO = ""; try { savedO = localStorage.getItem("kd_spk") || ""; } catch (x) {}
    const outs = devices.length ? (await navigator.mediaDevices.enumerateDevices()).filter(d => d.kind === "audiooutput") : [];
    if (!outs.length) { const o = document.createElement("option"); o.value = ""; o.textContent = "(sistèm defo)"; os.appendChild(o); }
    outs.forEach((d, i) => { const o = document.createElement("option"); o.value = d.deviceId; o.textContent = d.label || ("Soti " + (i + 1)); if (d.deviceId === savedO) o.selected = true; os.appendChild(o); });
    os.onchange = () => {
      const opt = os.options[os.selectedIndex]; const name = opt ? opt.textContent : "";
      try { localStorage.setItem("kd_spk", os.value); localStorage.setItem("kd_spk_name", name); } catch (x) {}
      applySink();
      api("POST", "/api/audio-settings", { output_name: name, output_id: os.value }).catch(() => {});
      msg("sòti son ofisyèl WASDEV chwazi pou tout sistèm nan");
    };
    const noteAudit = document.createElement("div");
    noteAudit.style.cssText = "color:var(--dim);font-size:11px;margin:6px 0 12px;padding:6px 10px;background:rgba(139,92,246,0.1);border-left:3px solid var(--mov);border-radius:4px";
    noteAudit.textContent = "✓ Chwa Audio IN ak OUT sa yo lye dirèkteman ak Paramèt ofisyèl WASDEV (Settings).";
    f.appendChild(noteAudit);
  } else if (S === "text") {
    H("Teks & Tit");
    sel("Font tit (tout videyo a)", FONT_STYLES, () => (SPEC.brand && SPEC.brand.font_title) || "", v => { SPEC.brand = SPEC.brand || {}; if (v) SPEC.brand.font_title = v; else delete SPEC.brand.font_title; });
    sel("Font ko (body)", FONT_STYLES, () => (SPEC.brand && SPEC.brand.font) || "", v => { SPEC.brand = SPEC.brand || {}; if (v) SPEC.brand.font = v; else delete SPEC.brand.font; });
    note("Font yo soti nan PC a (" + (FONT_STYLES.length - 1) + " disponib).");
  } else if (S === "color") {
    H("Koule mak la");
    SPEC.brand = SPEC.brand || {}; SPEC.brand.colors = SPEC.brand.colors || {};
    const C = SPEC.brand.colors;
    colorRow(f, "Fon (bg)", () => C.bg, v => { C.bg = v; build(); });
    colorRow(f, "Prime (primary)", () => C.primary, v => { C.primary = v; build(); });
    colorRow(f, "Aksan (accent)", () => C.accent, v => { C.accent = v; build(); });
    colorRow(f, "Teks (text)", () => C.text, v => { C.text = v; build(); });
  } else if (S === "project") {
    H("Pwoje");
    sel("Lang videyo a (jeneral)", ["ht", "fr", "en", "es", "pt", "ru", "it", "de"], () => SPEC.lang || "fr", v => { SPEC.lang = v; if (SPEC.voice) SPEC.voice.lang = v; if ($("#vlang")) $("#vlang").value = v; });
    note("Pwoje aktyel: " + (PROJNAME || "-") + ". Autosave chak 2 segonn. Videyo ekspote nan Analyseur-Kadans/exported videos/.");
    const nb = document.createElement("button"); nb.innerHTML = svg("plus") + "Nouvo pwoje"; nb.style.cssText = "margin-top:10px;width:100%;justify-content:center"; nb.onclick = () => { const sp = document.getElementById("setpop"); if (sp) sp.remove(); newProject(); }; f.appendChild(nb);
  } else {
    H("Jeneral");
    const KI = window.KadansI18n;
    note("Font PC: " + (FONT_STYLES.length - 1) + ". " + (KI ? KI.t("lang_name", "Kreyòl ayisyen") : "Kreyòl ayisyen") + ". Tout lokal. Rakousi: V chwazi, C koupe, S snap, M keyframe, Ctrl+Z/C/V/D.");
  }
  const row = document.createElement("div"); row.style.cssText = "display:flex;gap:6px;margin-top:16px";
  const ok = document.createElement("button"); ok.className = "pri"; ok.textContent = "Femen"; ok.style.flex = "1"; ok.onclick = () => { const sp = document.getElementById("setpop"); if (sp) sp.remove(); build(); }; row.appendChild(ok); f.appendChild(row);
}
async function startRecording(deviceId) {
  const btn = $("#tRecord");
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: deviceId ? { deviceId: { exact: deviceId } } : true });
    MREC = new MediaRecorder(stream); MCHUNKS = [];
    MREC.ondataavailable = e => { if (e.data && e.data.size) MCHUNKS.push(e.data); };
    MREC.onstop = async () => {
      btn.classList.remove("rec"); RECORDING = false; clearInterval(window._recTimer); stream.getTracks().forEach(x => x.stop());
      const blob = new Blob(MCHUNKS, { type: "audio/webm" }); msg("ap voye anrejistreman...");
      try { const au = new Audio(URL.createObjectURL(blob)); au.play(); } catch (x) {}   // tande l touswit
      const buf = await blob.arrayBuffer();
      const nm2 = "vwa-" + Date.now() + ".webm";
      const r = await fetch("/api/upload?name=" + encodeURIComponent(nm2) + "&token=" + encodeURIComponent(TOK), { method: "POST", body: buf });
      const j = await r.json().catch(() => ({}));
      if (!j.ok) { msg("ere anrejistreman"); return; }
      snapshot();
      if (RECTARGET && RECTARGET.track != null && SPEC.tracks[RECTARGET.track]) {
        const tk = SPEC.tracks[RECTARGET.track]; tk.clips = tk.clips || [];
        const rd = await clipDur(j.rel, "audio");
        tk.clips.push({ src: j.rel, kind: "audio", start: freeStart(tk, CUR, rd), dur: rd, label: "vwa" });
        msg("vwa anrejistre sou track la");
      } else if (SEL >= 0) { SPEC.scenes[SEL].voice_file = j.rel; msg("vwa anrejistre sou sen " + (SEL + 1)); }
      DIRTY = true; renderTimeline(); renderLeft();
    };
    MREC.start(); btn.classList.add("rec"); RECORDING = true; renderTimeline();
    const t0 = CUR, startT = performance.now();
    window._recTimer = setInterval(() => { CUR = t0 + (performance.now() - startT) / 1000; movePlayhead(); updateProg(); $("#time").textContent = CUR.toFixed(1) + " / " + Math.max(total(), CUR).toFixed(1) + " s"; }, 50);
    msg("ap anrejistre... kise a ap mache (klike Record ankò pou kanpe)");
  } catch (e) { msg("pa ka anrejistre: " + (e.message || e)); }
}

// ---- Autosave chak 2 segonn (pwoje pa janm pèdi) ----
let _saving = false;
async function autoSave() {
  if (!SPEC || !DIRTY || _saving || CONFLICT || window.__kadansMontage) return;   // MONTAJ AI an dirèk: disk la deja final
  _saving = true;
  try {
    const r = await api("PUT", "/api/spec", { spec: cln(), version: VER });
    if (r.status === 409) showConflict();                 // anvan: 409 an silans, chak 2 s, pou tout tan
    else if (r.body && r.body.ok) { VER = r.body.version; DIRTY = false; const m = $("#msg"); if (m && m.textContent.indexOf("ap ") !== 0) msg("otosove " + new Date().toLocaleTimeString().slice(0, 8)); }
  } catch (e) {}
  _saving = false;
}

// ---- ESTABILITE (v3.10): yon lòt moun (AI, yon lòt onglet, yon script) chanje spec.json ----
// Editè a poll /api/disk: si moun nan pa t gen chanjman ki poko sove → rechaje an silans (li wè vrè montaj la);
// si li te genyen → bann «konfli» ak 2 chwa, pa janm ekraze youn ni lòt san li deside. Erè build yo parèt tou.
let CONFLICT = false;
let BUILT = null;                  // kantite build sèvè a fini (aperçu a rechaje lè l chanje)
function stateBar() {
  let b = document.getElementById("kstate");
  if (!b) {
    b = document.createElement("div"); b.id = "kstate";
    b.style.cssText = "position:fixed;left:50%;top:8px;transform:translateX(-50%);z-index:99999;max-width:70vw;padding:8px 12px;" +
      "border-radius:8px;font:600 12px/1.4 system-ui,sans-serif;color:#fff;box-shadow:0 6px 24px rgba(0,0,0,.5);display:none";
    document.body.appendChild(b);
  }
  return b;
}
const _tk = (k, d) => (window.KadansI18n ? window.KadansI18n.t(k, d) : d);
function showConflict() {
  CONFLICT = true;
  const b = stateBar(); b.style.background = "#7c2d12"; b.style.display = "block";
  b.innerHTML = "";
  const t = document.createElement("div");
  t.textContent = _tk("conflict_text", "Montaj la chanje deyò Timeline la (AI, yon lòt onglet oswa yon script). Chanjman ou yo poko sove.");
  const row = document.createElement("div"); row.style.cssText = "display:flex;gap:8px;margin-top:6px;justify-content:flex-end";
  const mk = (label, fn) => { const x = document.createElement("button"); x.textContent = label;
    x.style.cssText = "border:0;border-radius:6px;padding:5px 10px;font:700 12px system-ui;cursor:pointer;background:#fff;color:#7c2d12"; x.onclick = fn; return x; };
  row.appendChild(mk(_tk("conflict_reload", "Pran vèsyon sou disk la"), async () => { CONFLICT = false; b.style.display = "none"; await load(); msg(_tk("reloaded", "montaj la rechaje")); }));
  row.appendChild(mk(_tk("conflict_keep", "Kenbe pa m (ranplase l)"), async () => {
    const d = await api("GET", "/api/disk"); if (d.body && d.body.disk) VER = d.body.disk;
    CONFLICT = false; b.style.display = "none"; DIRTY = true; await autoSave(); }));
  b.appendChild(t); b.appendChild(row);
}
function showBuildState(errors, warnings) {
  if (CONFLICT) return;
  const b = stateBar();
  if (errors && errors.length) {
    b.style.background = "#991b1b"; b.style.display = "block";
    b.textContent = _tk("build_errors", "Montaj la gen erè — aperçu a ak rann lan pa mete ajou jiskaske yo korije:") + " " + errors.slice(0, 4).join(" · ");
  } else if (warnings && warnings.length) {
    b.style.background = "#92400e"; b.style.display = "block";
    b.textContent = _tk("build_warnings", "Kite deyò nan aperçu a (pa yon imaj / fichye manke):") + " " + warnings.slice(0, 3).join(" · ");
  } else b.style.display = "none";
}
// ---- ISTORIK MONTAJ (v3.12): chak vèsyon spec.json sou sèvè a (.kadans-history/), kiyès ak kilè — remete youn ----
async function openHistory() {
  const old = document.getElementById("khist"); if (old) old.remove();
  const r = await api("GET", "/api/history");
  const items = (r.body && r.body.items) || [];
  const back = document.createElement("div"); back.id = "khist";
  back.style.cssText = "position:fixed;inset:0;background:#000b;z-index:99997;display:flex;align-items:center;justify-content:center";
  const box = document.createElement("div");
  box.style.cssText = "background:#150f28;border:1px solid #3b1d70;border-radius:12px;width:min(640px,92vw);max-height:80vh;overflow:auto;padding:16px 18px;color:#f3eefe;font:13px system-ui,sans-serif";
  const h = document.createElement("div"); h.style.cssText = "font-weight:800;font-size:15px;margin-bottom:4px";
  h.textContent = _tk("hist_title", "Istorik montaj la"); box.appendChild(h);
  const sub = document.createElement("div"); sub.style.cssText = "color:#c4b5fd;font-size:12px;margin-bottom:10px";
  sub.textContent = _tk("hist_sub", "Chak vèsyon sove isit la. Remete youn = li vin vèsyon aktyèl la; vèsyon kounye a rete nan lis la."); box.appendChild(sub);
  const who = { timeline: _tk("hist_timeline", "Timeline"), outside: _tk("hist_outside", "Deyò (AI / script)"), ai: _tk("hist_ai", "AI"),
                restore: _tk("hist_restore_a", "Restorasyon"), ids: _tk("hist_ids", "ID sèn yo") };
  if (!items.length) { const e = document.createElement("div"); e.textContent = _tk("hist_empty", "Poko gen okenn vèsyon."); box.appendChild(e); }
  items.forEach((it, k) => {
    const row = document.createElement("div");
    row.style.cssText = "display:flex;align-items:center;gap:10px;padding:7px 4px;border-top:1px solid #2a1f4a";
    const t = document.createElement("div"); t.style.cssText = "flex:1;min-width:0";
    t.innerHTML = "<b>" + esc(it.time) + "</b> · " + esc(who[it.author] || it.author) + (k === 0 ? " · <span style='color:#a3e635'>" + esc(_tk("hist_current", "aktyèl")) + "</span>" : "") +
      "<div style='color:#c4b5fd;font-size:11.5px'>" + esc(it.scenes + " " + _tk("hist_scenes", "sèn") + " · " + it.tracks + " " + _tk("hist_tracks", "pis") + (it.title ? " · " + it.title : "")) + "</div>";
    row.appendChild(t);
    if (k > 0) {
      const b = document.createElement("button"); b.textContent = _tk("hist_restore", "Remete l");
      b.style.cssText = "border:0;border-radius:6px;padding:5px 10px;font:700 12px system-ui;cursor:pointer;background:#8b5cf6;color:#fff";
      b.onclick = async () => {
        if (DIRTY) await autoSave();                       // chanjman ki poko sove yo antre nan istorik la AVAN
        const x = await api("POST", "/api/history/restore", { id: it.id });
        if (x.body && x.body.ok) { back.remove(); await load(); msg(_tk("hist_restored", "vèsyon an remete") + " (" + it.time + ")"); }
        else msg("ere: " + ((x.body && x.body.error) || "?"));
      };
      row.appendChild(b);
    }
    box.appendChild(row);
  });
  const close = document.createElement("button"); close.textContent = _tk("hist_close", "Fèmen");
  close.style.cssText = "margin-top:12px;border:1px solid #8b5cf6;border-radius:6px;padding:5px 12px;background:transparent;color:#f3eefe;cursor:pointer";
  close.onclick = () => back.remove(); box.appendChild(close);
  back.onclick = e => { if (e.target === back) back.remove(); };
  back.appendChild(box); document.body.appendChild(back);
}
function labelHistory() {           // rele nan load() (lang entèfas la fèk chwazi)
  const b = $("#bHistory"); if (!b) return; b.onclick = openHistory;
  const l = $("#bHistoryLbl"); if (l) l.textContent = _tk("hist_btn", "Istorik");
  b.title = _tk("hist_tip", "Istorik montaj la: tout vèsyon yo (Timeline, AI, restorasyon) — remete youn");
  b.setAttribute("data-tip", _tk("hist_btn", "Istorik"));
  b.setAttribute("data-sub", _tk("hist_tip", "Tout vèsyon yo"));
}

let _diskBusy = false;
async function watchDisk() {
  // PÈFÒMANS: pa poll sèvè a lè onglè a kache (li reprann otomatikman lè l vizib ankò).
  if (document.hidden || !SPEC || _diskBusy || _saving || CONFLICT || window.__kadansMontage) return;
  _diskBusy = true;
  try {
    const r = await api("GET", "/api/disk");
    const j = r.body || {};
    if (j.disk && VER && j.disk !== VER && !_saving) {
      if (DIRTY) showConflict();
      else { await load(); msg(_tk("reloaded_outside", "montaj la chanje deyò Timeline la — rechaje")); }
    }
    showBuildState(j.errors, j.warnings);
    if (j.built != null && BUILT !== null && j.built !== BUILT && !playing) {   // rebati deyò editè a (otosove,
      const am = await api("GET", "/api/audio-map");                           // chanjman AI): aperçu a swiv
      if (am.body && am.body.voices) AUDIO_MAP = am.body;
      mountPreview();
    }
    if (j.built != null && (BUILT === null || !playing)) BUILT = j.built;
  } catch (e) {}
  _diskBusy = false;
}
setInterval(watchDisk, 1500);

// Master meter: anime pandan play (reyaji ak play + vwa/mizik configirasyon an)
let _mLvl = 0;
function animateMeter() {
  const L = document.getElementById("meterL"), R = document.getElementById("meterR");
  if (L && R && SPEC) {
    let target = 0;
    const sc = SPEC.scenes[sceneAt(CUR)];
    const hasVoice = !!(sc && (sc.voice || sc.voice_file));
    const mv = (SPEC.music && SPEC.music.volume != null) ? SPEC.music.volume : 0;
    let hasClip = false;
    (SPEC.tracks || []).forEach(tk => (tk.clips || []).forEach(c => { if ((c.kind === "audio" || c.kind === "video") && (c.start || 0) <= CUR && CUR <= (c.start || 0) + (c.dur || 2)) hasClip = true; }));
    const hasAudio = hasVoice || (SPEC.music && mv > 0) || hasClip;
    if (RECORDING) target = 0.5 + 0.4 * Math.random();
    else if (playing && hasAudio) target = Math.min(1, (0.35 + 0.5 * Math.random()) * ((hasVoice ? 0.9 : 0) + mv + (hasClip ? 0.6 : 0)));
    _mLvl += (target - _mLvl) * 0.3;
    L.style.height = (_mLvl * 100).toFixed(0) + "%";
    R.style.height = Math.max(0, _mLvl * 100 - 5 * Math.random()).toFixed(0) + "%";
  }
  requestAnimationFrame(animateMeter);
}
animateMeter();
// Resize: splitter goch/dwat (lajè) + timeline (wotè), kenbe nan localStorage
function dragSplit(id, apply, min, max, store) {
  const el = $("#" + id); if (!el) return;
  el.addEventListener("mousedown", ev => {
    ev.preventDefault(); document.body.style.userSelect = "none";
    const pv = $("#pv"); if (pv) pv.style.pointerEvents = "none";   // iframe pa vale souri a pandan drag la
    const mv = e => { const v = apply(e); if (Math.abs(PVZOOM - 1) < 0.01) fitScreenView(); try { localStorage.setItem(store, v); } catch (x) {} };
    const up = () => { document.body.style.userSelect = ""; if (pv) pv.style.pointerEvents = ""; if (Math.abs(PVZOOM - 1) < 0.01) fitScreenView(); document.removeEventListener("mousemove", mv); document.removeEventListener("mouseup", up); };
    document.addEventListener("mousemove", mv); document.addEventListener("mouseup", up);
  });
}
dragSplit("splitL", e => { const w = Math.max(160, Math.min(460, e.clientX)); $("#left").style.width = w + "px"; LAST_L_WIDTH = w; return w; }, 160, 460, "kd_lw");
dragSplit("splitR", e => { const w = Math.max(220, Math.min(520, window.innerWidth - e.clientX)); $("#insp").style.width = w + "px"; LAST_R_WIDTH = w; return w; }, 220, 520, "kd_rw");
dragSplit("splitT", e => { const h = Math.max(140, Math.min(window.innerHeight - 180, window.innerHeight - e.clientY)); $("#tl").style.height = h + "px"; renderTimeline(); return h; }, 140, 600, "kd_th");
try {
  const lw = localStorage.getItem("kd_lw"); if (lw) { LAST_L_WIDTH = parseInt(lw, 10) || 335; $("#left").style.width = LAST_L_WIDTH + "px"; }
  const rw = localStorage.getItem("kd_rw"); if (rw) { LAST_R_WIDTH = parseInt(rw, 10) || 360; $("#insp").style.width = LAST_R_WIDTH + "px"; }
  const th = localStorage.getItem("kd_th"); if (th) $("#tl").style.height = th + "px";
} catch (x) {}
if ($("#tRecord")) $("#tRecord").onclick = recordVoice;
if ($("#tPlay2")) $("#tPlay2").onclick = () => setPlaying(!playing);
if ($("#tReplay")) $("#tReplay").onclick = () => { stopAudio(); CUR = 0; movePlayhead(); post({ cmd: "seek", t: 0 }); setPlaying(true); msg("rejwe"); };
async function loadFonts() {
  try {
    const r = await api("GET", "/api/fonts");
    const fx = (r.body && r.body.fonts) || [];
    if (fx.length) { FONT_STYLES = [""].concat(fx); if (RT === "props") renderRight(); msg(fx.length + " font PC disponib"); }
  } catch (e) {}
}
setInterval(autoSave, 2000);
window.addEventListener("resize", () => { if (Math.abs(PVZOOM - 1) < 0.01) fitScreenView(); else setTimeout(renderOvHandle, 40); });
loadOpenTabs(); setTool("select"); load(); loadProjects(); loadFonts(); syncOfficialWasdevAudio();
