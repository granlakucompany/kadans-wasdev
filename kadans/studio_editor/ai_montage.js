// MONTAJ AN DIRÈK (2026-10-20): lè yon AI fin ekri videyo a, li FÈ montaj la DEVAN devlopè a nan Kadans Timeline —
// kurswa AI a pran chak medya (son, SFX, videyo, imaj) nan panèl la, li TRENNEN l sou bon track la nan bon moman an,
// epi li lage l. Se VRÈ fonksyon editè a ki ajoute klip la. spec.json sou disk la deja FINAL: si devlopè a fèmen paj
// la nan mitan montaj la, anyen pa pèdi (otosove a kanpe pandan montaj la).
(function () {
  "use strict";
  const AI = {};
  window.KadansMontage = AI;
  let cur = null, pos = { x: innerWidth * 0.5, y: innerHeight * 0.6 }, fast = false, skip = false;

  // ---------------------------------------------------------------- KURSWA AI FLUID
  function cursorEl() {
    if (cur) return cur;
    cur = document.createElement("div");
    cur.id = "kdAiCursor";
    cur.style.cssText = "position:fixed;left:0;top:0;z-index:2147483646;pointer-events:none;will-change:transform;" +
      "transform:translate3d(" + pos.x + "px," + pos.y + "px,0)";
    cur.innerHTML =
      '<div class="rip" style="position:absolute;left:-16px;top:-16px;width:32px;height:32px;border-radius:50%;' +
      'border:2.5px solid #a855f7;background:rgba(139,92,246,.22);opacity:0;transform:scale(.2)"></div>' +
      '<svg width="26" height="26" viewBox="0 0 24 24" style="filter:drop-shadow(0 3px 8px rgba(124,58,237,.65))">' +
      '<path d="M4 2L20 10.5L12.5 13L9.5 20.5L4 2Z" fill="#8b5cf6" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/></svg>' +
      '<span class="tag" style="position:absolute;left:20px;top:16px;background:linear-gradient(135deg,#7c3aed,#ec4899);' +
      'color:#fff;font:700 10px/1.2 system-ui,sans-serif;padding:2px 7px;border-radius:999px;white-space:nowrap;' +
      'box-shadow:0 2px 6px rgba(0,0,0,.4)">AI</span>';
    document.body.appendChild(cur);
    return cur;
  }
  const sleep = ms => new Promise(r => setTimeout(r, skip ? 0 : (fast ? ms * 0.45 : ms)));
  const ease = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

  // Mouvman sou yon ti KOUB (pa yon liy dwat ki sote), dire a depann de distans lan, 60 i/s (requestAnimationFrame)
  function moveTo(x, y, ghost) {
    const el = cursorEl();
    const x0 = pos.x, y0 = pos.y, dx = x - x0, dy = y - y0, dist = Math.hypot(dx, dy);
    if (skip || dist < 1) { pos = { x, y }; el.style.transform = "translate3d(" + x + "px," + y + "px,0)"; return Promise.resolve(); }
    const dur = Math.max(260, Math.min(950, 240 + dist * 0.55)) * (fast ? 0.45 : 1);
    const cx = x0 + dx * 0.5 - dy * 0.18, cy = y0 + dy * 0.5 + dx * 0.18;      // pwen kontwòl: koub dous
    const t0 = performance.now();
    return new Promise(res => {
      function step(now) {
        const k = Math.min(1, (now - t0) / dur), e = ease(k), u = 1 - e;
        const px = u * u * x0 + 2 * u * e * cx + e * e * x, py = u * u * y0 + 2 * u * e * cy + e * e * y;
        el.style.transform = "translate3d(" + px + "px," + py + "px,0)";
        if (ghost) ghost.style.transform = "translate3d(" + (px + 14) + "px," + (py + 12) + "px,0)";
        if (k < 1 && !skip) requestAnimationFrame(step);
        else { pos = { x, y }; el.style.transform = "translate3d(" + x + "px," + y + "px,0)"; res(); }
      }
      requestAnimationFrame(step);
    });
  }
  function press(label) {
    const el = cursorEl(), rip = el.querySelector(".rip"), tag = el.querySelector(".tag");
    if (label && tag) tag.textContent = label;
    if (!rip) return;
    rip.style.transition = "none"; rip.style.transform = "scale(.2)"; rip.style.opacity = "1";
    rip.getBoundingClientRect();
    rip.style.transition = "transform .38s ease-out, opacity .38s ease-out";
    rip.style.transform = "scale(1.7)"; rip.style.opacity = "0";
  }
  function center(el) {
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.left + Math.min(r.width / 2, 60)), y: Math.round(r.top + r.height / 2) };
  }
  function glow(el, on) {
    if (!el) return;
    if (on) { el.__kdo = el.style.outline; el.style.outline = "2px solid #a855f7"; el.style.outlineOffset = "2px"; }
    else { el.style.outline = el.__kdo || ""; }
  }
  AI.moveTo = moveTo; AI.press = press;

  // ---------------------------------------------------------------- BANN + «Fini touswit»
  let bar = null, shield = null;
  function banner(txt) {
    if (!bar) {
      shield = document.createElement("div");          // devlopè a pa ka chanje anyen PANDAN AI a ap trennen
      shield.style.cssText = "position:fixed;inset:0;z-index:2147483640;cursor:progress;background:transparent";
      document.body.appendChild(shield);
      bar = document.createElement("div");
      bar.style.cssText = "position:fixed;left:50%;top:10px;transform:translateX(-50%);z-index:2147483645;display:flex;" +
        "gap:10px;align-items:center;background:#1a1128;border:1px solid #7c3aed;border-radius:10px;padding:7px 12px;" +
        "color:#fff;font:600 12px system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.45)";
      bar.innerHTML = '<span class="t"></span>' +
        '<button class="f" style="background:#2a1d40;color:#fff;border:1px solid #5b3a99;border-radius:7px;padding:3px 9px;cursor:pointer">2x pi vit</button>' +
        '<button class="s" style="background:#7c3aed;color:#fff;border:none;border-radius:7px;padding:3px 9px;cursor:pointer">Fini touswit</button>';
      bar.querySelector(".f").onclick = () => { fast = !fast; bar.querySelector(".f").textContent = fast ? "Vitès nòmal" : "2x pi vit"; };
      bar.querySelector(".s").onclick = () => { skip = true; };
      document.body.appendChild(bar);
      const KI = window.KadansI18n;
      if (KI && KI.tp) bar.querySelectorAll("button").forEach(b => { b.textContent = KI.tp(b.textContent); });
    }
    bar.querySelector(".t").textContent = txt;
  }
  function done() {
    if (bar) bar.remove(); if (shield) shield.remove(); bar = shield = null;
    if (cur) { cur.style.transition = "opacity .5s"; cur.style.opacity = "0"; const c = cur; cur = null; setTimeout(() => c.remove(), 600); }
  }

  // ---------------------------------------------------------------- MONTAJ LA
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const base = s => String(s || "").split("/").pop();
  async function waitFor(fn, ms) {
    const t0 = performance.now();
    while (performance.now() - t0 < ms) { const v = fn(); if (v) return v; await new Promise(r => setTimeout(r, 60)); }
    return fn();
  }
  function ghostFor(label, icon) {
    const g = document.createElement("div");
    g.style.cssText = "position:fixed;left:0;top:0;z-index:2147483645;pointer-events:none;background:rgba(124,58,237,.9);" +
      "color:#fff;font:600 11px system-ui,sans-serif;padding:4px 8px;border-radius:7px;max-width:220px;white-space:nowrap;" +
      "overflow:hidden;text-overflow:ellipsis;box-shadow:0 4px 14px rgba(0,0,0,.45);transform:translate3d(" + (pos.x + 14) + "px," + (pos.y + 12) + "px,0)";
    g.textContent = (icon || "♪") + " " + label;
    document.body.appendChild(g);
    return g;
  }
  function iconFor(c) {
    const k = c.kind || "";
    return k === "video" ? "🎬" : (k === "image" || k === "asset") ? "🖼" : k === "text" ? "T" : k === "sfx" ? "✦" : "♪";
  }
  function sourceFor(c) {
    if (c.kind === "sfx" && c.sfx) {
      return [...document.querySelectorAll("#lbody .item")].find(it => (it.textContent || "").indexOf(c.label || c.sfx) >= 0);
    }
    if (c.src) {
      const b = base(c.src);
      return [...document.querySelectorAll("#mgrid .asset")].find(a => a.title === b);
    }
    return null;
  }
  async function clipStep(st, n, total) {
    const c = st.clip, tk = SPEC.tracks[st.t];
    if (!tk) return;
    const label = c.label || base(c.src) || c.sfx || c.kind || "klip";
    const tname = tk.name || tk.kind || ("track " + (st.t + 1));
    banner("AI ap fè montaj la: " + n + "/" + total + " — " + label + " → " + tname + " @ " + (c.start || 0).toFixed(1) + " s");
    let src = null;
    if (!skip) {
      if (c.kind === "sfx" && c.sfx) { if (LT !== "sfx") selTab("sfx"); }
      else if (c.src && LT !== "media") selTab("media");
      src = await waitFor(() => sourceFor(c), 1500);
      if (!src) src = document.querySelector('.tname[data-ti="' + st.t + '"]') || document.querySelector("#lbody");
      if (src && src.scrollIntoView) src.scrollIntoView({ block: "nearest" });
      const sw = document.querySelector("#tlscrollwrap");
      if (sw) sw.scrollLeft = Math.max(0, (c.start || 0) * PPS - sw.clientWidth * 0.3);
      await sleep(60);
      const p = center(src);
      await moveTo(p.x, p.y);
      glow(src, true); press("AI"); await sleep(160);
      const row = document.querySelector('.trow[data-track="tk' + st.t + '"]');
      if (row && row.scrollIntoView) row.scrollIntoView({ block: "nearest" });
      const inner = document.querySelector("#tlinner").getBoundingClientRect();
      const rr = row ? row.getBoundingClientRect() : inner;
      const g = ghostFor(label, iconFor(c));
      await moveTo(Math.round(inner.left + (c.start || 0) * PPS + 10), Math.round(rr.top + rr.height / 2), g);
      press("AI"); g.remove(); glow(src, false);
    }
    tk.clips = tk.clips || [];
    const at = Math.min(st.i, tk.clips.length);
    const cut = +(c.in || 0);
    if (cut > 0.05 && !skip) {
      // KOUPE AN DIRÈK: klip la tonbe ANTYE (fichye a pa janm koupe), epi kurswa a trennen rebò goch la jiska «in»
      const full = Object.assign({}, c), s1 = +(c.start || 0), d1 = +(c.dur || 2);
      const slip = s1 - cut < 0;                       // pa gen plas anvan: glise kontni an (slip) olye deplase klip la
      full.in = 0; full.start = slip ? s1 : s1 - cut; full.dur = slip ? d1 : d1 + cut;
      tk.clips.splice(at, 0, full);
      CLIPSEL = { t: st.t, c: at }; renderTimeline();
      banner("AI ap koupe: " + (c.label || base(c.src)) + " — kòmansman " + cut.toFixed(2) + " s");
      const inner = document.querySelector("#tlinner").getBoundingClientRect();
      const row = document.querySelector('.trow[data-track="tk' + st.t + '"]');
      const ry = row ? row.getBoundingClientRect() : inner;
      const y = Math.round(ry.top + ry.height / 2);
      await moveTo(Math.round(inner.left + full.start * PPS + 2), y);
      press("AI");
      const t0 = performance.now(), D = fast ? 360 : 800;
      await new Promise(res => {
        let last = 0;
        function f(now) {
          const k = Math.min(1, (now - t0) / D), e = ease(k), cl = tk.clips[at];
          if (!cl) return res();
          cl.in = +(cut * e).toFixed(3);
          if (!slip) { cl.start = +(s1 - cut + cut * e).toFixed(3); cl.dur = +(d1 + cut - cut * e).toFixed(3); }
          const x = Math.round(inner.left + (cl.start || 0) * PPS + 2);
          const el = cursorEl(); el.style.transform = "translate3d(" + x + "px," + y + "px,0)"; pos = { x, y };
          if (now - last > 50 || k >= 1) { last = now; renderTimeline(); }
          if (k < 1 && !skip) requestAnimationFrame(f); else res();
        }
        requestAnimationFrame(f);
      });
      tk.clips[at] = c;                                 // valè EGZAK AI a (menm ak disk la)
    } else {
      tk.clips.splice(at, 0, c);
    }
    CLIPSEL = { t: st.t, c: at };
    renderTimeline(); if (!skip) renderRight();
    msg("AI: " + label + " → " + tname + " @ " + (c.start || 0).toFixed(1) + " s");
    await sleep(240);
  }
  async function overlayStep(st, n, total) {
    const sc = SPEC.scenes[st.s];
    if (!sc) return;
    const o = st.ov, label = base(o.src) || "overlay";
    banner("AI ap fè montaj la: " + n + "/" + total + " — " + label + " → sèn " + (st.s + 1));
    if (!skip) {
      if (LT !== "media") selTab("media");
      const src = await waitFor(() => sourceFor(o), 1500) || document.querySelector("#lbody");
      if (typeof selectScene === "function") selectScene(st.s);
      await sleep(120);
      const p = center(src);
      await moveTo(p.x, p.y); glow(src, true); press("AI"); await sleep(160);
      const pv = document.querySelector("#pvwrap") || document.body;
      const r = pv.getBoundingClientRect();
      const g = ghostFor(label, "🖼");
      await moveTo(Math.round(r.left + r.width * (o.x != null ? o.x : 0.5)), Math.round(r.top + r.height * (o.y != null ? o.y : 0.5)), g);
      press("AI"); g.remove(); glow(src, false);
    }
    sc.overlays = sc.overlays || [];
    sc.overlays.splice(Math.min(st.i, sc.overlays.length), 0, o);
    renderTimeline(); if (!skip) renderRight();
    msg("AI: " + label + " → sèn " + (st.s + 1));
    await sleep(240);
  }

  // Retire klip plan an NAN MEMWA (pa sou disk), epi refè yo youn pa youn
  async function run(plan) {
    const steps = (plan && plan.steps) || [];
    if (!steps.length || !SPEC) return;
    window.__kadansMontage = true;                     // otosove kanpe: disk la deja gen vèsyon FINAL la
    const lt0 = LT;
    try {
      const rm = steps.slice().sort((a, b) => (b.t || b.s || 0) - (a.t || a.s || 0) || (b.i || 0) - (a.i || 0));
      for (const st of rm) {
        const arr = st.op === "overlay" ? ((SPEC.scenes[st.s] || {}).overlays || []) : ((SPEC.tracks[st.t] || {}).clips || []);
        const item = st.op === "overlay" ? st.ov : st.clip;
        let k = (arr[st.i] && same(arr[st.i], item)) ? st.i : arr.findIndex(x => same(x, item));
        if (k >= 0) arr.splice(k, 1); else st.skip = true;   // pa jwenn li (spec la chanje): pa refè l
      }
      renderTimeline();
      const todo = steps.filter(s => !s.skip).sort((a, b) => (a.op === b.op ? 0 : a.op === "clip" ? -1 : 1) ||
        ((a.clip || a.ov || {}).start || 0) - ((b.clip || b.ov || {}).start || 0));
      let n = 0;
      for (const st of todo) {
        n += 1;
        if (st.op === "overlay") await overlayStep(st, n, todo.length);
        else await clipStep(st, n, todo.length);
      }
      if (lt0 && LT !== lt0) selTab(lt0);
      renderTimeline(); renderRight();
      msg("AI: montaj la fini (" + todo.length + " medya)");
    } finally {
      DIRTY = false;                                   // menm ak disk la
      window.__kadansMontage = false;
      done();
      skip = false;
      if (typeof build === "function") { try { build(); } catch (e) {} }
    }
  }
  AI.run = run;

  // Lè paj la fin chaje SPEC la: gen yon plan montaj AI? (yon sèl fwa — sèvè a efase l)
  async function check() {
    const ok = await waitFor(() => (typeof SPEC !== "undefined" && SPEC && SPEC.scenes && document.querySelector("#tlinner")), 15000);
    if (!ok) return;
    try {
      const r = await api("GET", "/api/montage");
      if (r && r.body && r.body.steps && r.body.steps.length) await run(r.body);
    } catch (e) { window.__kadansMontage = false; }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", check); else check();
})();
