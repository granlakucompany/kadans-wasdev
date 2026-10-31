// media_panel.js - Kadans Timeline media panel (loaded after editor.js):
//  - a small play button on every audio / video tile: hear / watch it WITHOUT adding it to the timeline
//    (click again = stop; one preview at a time)
//  - video tiles show their first frame (/api/thumb, cached JPEG made by ffmpeg on the server)
//  - audio tiles show a mini waveform + length (/api/media-info, cached), video tiles their length
//  - live refresh: when a file lands in medya/ (host app tree drop / menu / AI), the list updates by itself
//  - host drops (WASDEV): KMP.hostDrop(paths, x, y) copies the files into medya/<kind>/ and, if they were dropped
//    on the viewer / timeline, places them there like a normal media drag.
(function () {
  "use strict";
  const VID = /\.(mp4|webm|mov|m4v|mkv|avi)$/i, AUD = /\.(wav|mp3|m4a|aac|ogg|opus|flac)$/i;
  const TK = () => encodeURIComponent(typeof TOK !== "undefined" ? TOK : "");
  // SEKIRITE: apèl API fetch yo voye jeton an nan header (pa URL). URL medya (src img/audio) rete ak token.
  const HDR = () => ({ "X-Kadans-Token": (typeof TOK !== "undefined" ? TOK : "") });
  let PREV = null;                 // { el: HTMLMediaElement, tile, btn }
  const INFO = new Map();          // rel -> {dur, wave}
  const QUEUE = [];                // media-info requests (2 at a time: never a burst of ffmpeg on the server)
  let busy = 0, lastRev = null, lastProj = null;

  const css = document.createElement("style");
  css.textContent = [
    ".asset.kmp-tile{position:relative;padding:0}",
    ".kmp-thumb{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:none!important;opacity:1!important;border-radius:7px;pointer-events:none}",
    ".kmp-wave{position:absolute;left:6px;right:6px;top:22%;height:46%;display:flex;align-items:center;gap:1px;pointer-events:none}",
    ".kmp-wave i{flex:1;background:var(--mov,#8b5cf6);opacity:.85;border-radius:1px;min-height:2px}",
    ".kmp-dur{position:absolute;right:3px;bottom:3px;font:600 9px system-ui;color:#fff;background:#000a;padding:1px 4px;border-radius:4px;pointer-events:none}",
    ".kmp-name{position:absolute;left:3px;right:3px;top:3px;font:500 9px system-ui;color:#ddd;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;pointer-events:none;text-shadow:0 1px 2px #000}",
    ".kmp-play{position:absolute;left:4px;bottom:4px;width:22px;height:22px;border-radius:50%;border:0;padding:0;display:flex;align-items:center;justify-content:center;background:#8b5cf6;color:#fff;cursor:pointer;box-shadow:0 1px 4px #000a;z-index:2}",
    ".kmp-play:hover{background:#a78bfa}.kmp-play svg{width:11px;height:11px;fill:currentColor;stroke:none}",
    ".kmp-tile.kmp-on{border-color:#a78bfa;box-shadow:0 0 0 1px #a78bfa inset}",
    ".kmp-vid{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000;border-radius:7px;z-index:1;pointer-events:none}",
    "#left.kmp-hover{outline:2px dashed #a78bfa;outline-offset:-4px}"
  ].join("\n");
  document.head.appendChild(css);

  const PLAY = '<svg viewBox="0 0 24 24"><polygon points="7 4 20 12 7 20"/></svg>';
  const STOP = '<svg viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="1.5"/></svg>';
  const fmt = s => { s = Math.max(0, Math.round(s || 0)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); };
  const fileUrl = rel => rel + (rel.indexOf("?") >= 0 ? "&" : "?") + "token=" + TK();

  function stop() {
    if (!PREV) return;
    try { PREV.el.pause(); PREV.el.removeAttribute("src"); PREV.el.load(); } catch (e) {}
    if (PREV.el.parentNode && PREV.el.classList.contains("kmp-vid")) PREV.el.remove();
    PREV.tile.classList.remove("kmp-on");
    PREV.btn.innerHTML = PLAY;
    PREV = null;
  }
  function toggle(tile, btn, m, isVid) {
    const same = PREV && PREV.tile === tile;
    stop();
    if (same) return;
    try { if (typeof playing !== "undefined" && playing && typeof setPlaying === "function") setPlaying(false); } catch (e) {}
    let el;
    if (isVid) { el = document.createElement("video"); el.className = "kmp-vid"; el.playsInline = true; tile.appendChild(el); }
    else el = new Audio();
    el.preload = "auto";
    el.src = fileUrl(m.rel);
    el.onended = () => { if (PREV && PREV.el === el) stop(); };
    el.onerror = () => {
      if (!(PREV && PREV.el === el)) return;
      if (!el._kmpFallback) {                 // no MP3 / AAC decoder in this browser: a cached WAV from the server
        el._kmpFallback = true;
        el.src = "/api/preview-audio?file=" + encodeURIComponent(m.rel) + "&token=" + TK();
        const p2 = el.play(); if (p2 && p2.catch) p2.catch(() => {});
        return;
      }
      stop(); if (typeof msg === "function") msg("pa ka jwe medya sa a");
    };
    PREV = { el, tile, btn, rel: m.rel };
    tile.classList.add("kmp-on"); btn.innerHTML = STOP;
    const p = el.play(); if (p && p.catch) p.catch(() => {});
  }

  function pump() {
    while (busy < 2 && QUEUE.length) {
      const job = QUEUE.shift(); busy++;
      fetch("/api/media-info?file=" + encodeURIComponent(job.rel), { headers: HDR() })
        .then(r => r.json()).catch(() => ({}))
        .then(j => { if (j && j.dur != null) INFO.set(job.rel, j); job.done(j || {}); })
        .finally(() => { busy--; pump(); });
    }
  }
  function withInfo(rel, cb) {
    if (INFO.has(rel)) { cb(INFO.get(rel)); return; }
    QUEUE.push({ rel, done: cb }); pump();
  }
  function bar(v, op) { const i = document.createElement("i"); i.style.height = v + "%"; if (op) i.style.opacity = op; return i; }
  function paintInfo(a, j, isVid) {
    if (!a.isConnected || !j) return;
    if (j.dur) {
      let d = a.querySelector(".kmp-dur");
      if (!d) { d = document.createElement("span"); d.className = "kmp-dur"; a.appendChild(d); }
      d.textContent = fmt(j.dur);
    }
    if (!isVid && j.wave && j.wave.length) {
      const w = a.querySelector(".kmp-wave"); if (!w) return;
      w.textContent = "";
      j.wave.filter((_, i) => i % 2 === 0).forEach(v => w.appendChild(bar(Math.max(6, Math.round(v * 100)))));
    }
  }
  const IO = ("IntersectionObserver" in window) ? new IntersectionObserver(ents => {
    ents.forEach(en => { if (en.isIntersecting) { IO.unobserve(en.target); const f = en.target._kmpLoad; if (f) f(); } });
  }) : null;

  // Called by renderImported (editor.js) for each tile
  function decorate(a, m) {
    const name = m.name || m.rel || "", isVid = VID.test(name), isAud = AUD.test(name);
    if (!isVid && !isAud) return;
    a.classList.add("kmp-tile");
    a.textContent = "";
    if (isVid) {
      const img = document.createElement("img"); img.className = "kmp-thumb"; img.loading = "lazy"; img.alt = "";
      img.onerror = () => { img.remove(); if (typeof svg === "function") a.insertAdjacentHTML("afterbegin", svg("film")); };
      img.src = "/api/thumb?file=" + encodeURIComponent(m.rel) + "&token=" + TK();
      a.appendChild(img);
    } else {
      const w = document.createElement("div"); w.className = "kmp-wave";
      [3, 6, 4, 8, 5, 9, 6, 4, 7, 5, 3, 6, 8, 4, 6, 3].forEach(v => w.appendChild(bar(v * 10, ".35")));
      a.appendChild(w);
    }
    const nm = document.createElement("span"); nm.className = "kmp-name"; nm.textContent = name; a.appendChild(nm);
    const b = document.createElement("button"); b.className = "kmp-play"; b.type = "button"; b.draggable = false;
    b.title = "Tande / gade l san ajoute l sou timeline";
    if (PREV && PREV.rel === m.rel) stop();         // list re-rendered while previewing: stop cleanly
    b.innerHTML = PLAY;
    b.addEventListener("mousedown", ev => ev.stopPropagation());
    b.addEventListener("click", ev => { ev.preventDefault(); ev.stopPropagation(); toggle(a, b, m, isVid); });
    a.appendChild(b);
    const load = () => withInfo(m.rel, j => paintInfo(a, j, isVid));
    if (IO) { a._kmpLoad = load; IO.observe(a); } else load();
  }

  async function refresh(force) {
    try {
      const r = await fetch("/api/media-rev", { headers: HDR() }); const j = await r.json();
      if (!force && j.rev === lastRev && j.project === lastProj) return false;
      const first = lastRev === null;
      lastRev = j.rev; lastProj = j.project;
      if (first && !force) return false;
      const r2 = await fetch("/api/media", { headers: HDR() }); const j2 = await r2.json();
      window.IMPORTED = (j2 && j2.media) || [];
      const g = document.getElementById("mgrid");
      if (g && typeof renderImported === "function") renderImported(g);
      return true;
    } catch (e) { return false; }
  }
  setInterval(() => { if (!document.hidden) refresh(false); }, 2500);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) refresh(false); });  // back on the tab
  refresh(false);

  function hostHover(on) { const l = document.getElementById("left"); if (l) l.classList.toggle("kmp-hover", !!on); }

  // WASDEV: files dragged from the project tree (or right-click "Add to Kadans Timeline media")
  async function hostDrop(paths, x, y) {
    hostHover(false);
    const added = [];
    for (const p of paths || []) {
      try {
        const r = await fetch("/api/media/add", {
          method: "POST", headers: { "Content-Type": "application/json", ...HDR() }, body: JSON.stringify({ path: p }) });
        const j = await r.json();
        if (j && j.ok) added.push(j);
        else if (typeof msg === "function") msg("ere: " + ((j && j.error) || p));
      } catch (e) {}
    }
    window.__kmpLast = { added, at: Date.now() };
    if (!added.length) return added;
    await refresh(true);
    const el = (x != null && y != null) ? document.elementFromPoint(x, y) : null;
    const onTimeline = el && !el.closest("#left") && el.closest("#tracks, #tlscrollwrap, #viewer, #pvwrap, #stage, #pv");
    if (onTimeline) {
      for (const it of added) {                // same path as a media dragged from the panel
        const dt = new DataTransfer();
        dt.setData("text/kadans-asset", it.rel);
        dt.setData("text/kadans-kind", typeof mediaKind === "function" ? mediaKind(it.rel) : "");
        el.dispatchEvent(new DragEvent("drop", { bubbles: true, cancelable: true, clientX: x, clientY: y, dataTransfer: dt }));
      }
    } else if (typeof selTab === "function" && typeof LT !== "undefined" && LT !== "media") selTab("media");
    if (typeof msg === "function") msg("medya ajoute: " + added.map(a => a.rel).join(", "));
    return added;
  }

  // EXACT length of an audio / video file (seconds) for a clip dropped on a track: server first (ffmpeg, cached),
  // then the browser's own metadata. 0 = unknown (images, missing file).
  function relOf(src) { return String(src || "").split("?")[0].replace(/^\/+/, ""); }
  function metaDur(src) {
    return new Promise(res => {
      const el = VID.test(relOf(src)) ? document.createElement("video") : new Audio();
      const done = v => { el.onloadedmetadata = el.onerror = null; try { el.removeAttribute("src"); el.load(); } catch (e) {} res(v); };
      el.preload = "metadata";
      el.onloadedmetadata = () => done(isFinite(el.duration) ? el.duration : 0);
      el.onerror = () => done(0);
      setTimeout(() => done(0), 6000);
      el.src = fileUrl(relOf(src));
    });
  }
  async function duration(src) {
    const rel = relOf(src);
    if (!VID.test(rel) && !AUD.test(rel)) return 0;
    if (INFO.has(rel) && INFO.get(rel).dur > 0) return INFO.get(rel).dur;
    try {
      const ctl = new AbortController(); const tm = setTimeout(() => ctl.abort(), 8000);
      const r = await fetch("/api/media-info?file=" + encodeURIComponent(rel), { headers: HDR(), signal: ctl.signal });
      clearTimeout(tm);
      const j = await r.json();
      if (j && j.dur > 0) { INFO.set(rel, j); return j.dur; }
    } catch (e) {}
    return await metaDur(rel);
  }

  // Files dropped from OUTSIDE the page (WASDEV Edge engine: drag from the project tree): ask the host first —
  // it knows the full path, asks which Kadans project when there are several, and copies server-side.
  // Anything the host does not claim goes on to the editor's normal drop handlers (upload).
  window.addEventListener("drop", ev => {
    if (ev.__kmpReplay) return;
    const dt = ev.dataTransfer;
    if (!dt || !dt.files || !dt.files.length) return;
    const files = Array.from(dt.files), target = ev.target, x = ev.clientX, y = ev.clientY;
    ev.preventDefault(); ev.stopPropagation(); ev.stopImmediatePropagation();
    hostHover(false);
    (async () => {
      let res = {};
      try {
        const r = await fetch("/api/audio-bridge", { method: "POST", headers: { "Content-Type": "application/json", ...HDR() },
          body: JSON.stringify({ cmd: "host_drop", names: files.map(f => f.name), sizes: files.map(f => f.size) }) });
        res = await r.json();
      } catch (e) {}
      if (res && res.handled) {
        if (res.here && res.paths) await hostDrop(res.paths, x, y);
        else if (res.added && typeof msg === "function") msg("medya ajoute: " + (res.project || "") + " → " + res.added.join(", "));
        return;
      }
      const d2 = new DataTransfer(); files.forEach(f => d2.items.add(f));
      const e2 = new DragEvent("drop", { bubbles: true, cancelable: true, clientX: x, clientY: y, dataTransfer: d2 });
      e2.__kmpReplay = true;
      target.dispatchEvent(e2);
    })();
  }, true);

  window.KMP = { decorate, stop, refresh, hostDrop, hostHover, duration, info: rel => INFO.get(rel), current: () => PREV };
})();
