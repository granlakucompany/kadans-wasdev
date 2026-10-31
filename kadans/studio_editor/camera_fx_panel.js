/* Kadans Timeline — PANNO KAMERA + PATIKIL (onglè «Efè» lè yon SÈN chwazi).
 * Kamera dekò vektè (sèn html): pan, zoom, swiv yon pèsonaj, tranbleman, limit → kle spec `camera`.
 * Patikil detèminis: pousyè, etensèl, sillage, lapli, lafimen → kle spec `fx` (lis).
 * Fichye apa (pa nan editor.js): li ranplase renderEffect pou sèn yo epi rele ansyen an pou rès la.
 * Menm kle ak motè a (kadans/spec.py _camera_html / _fx_list) — sa AI a ekri ak sa panno a montre se menm bagay.
 */
(function () {
  "use strict";
  const T = (k, d) => (window.KadansI18n && window.KadansI18n.t ? window.KadansI18n.t(k, d) : d);
  const FX_TYPES = [
    ["dust", "Pousyè"], ["sparks", "Etensèl"], ["trail", "Sillage limyè"], ["rain", "Lapli"], ["smoke", "Lafimen"]];
  const FX_DEF = {                                  // menm valè pa defo ak spec.py
    dust: { dur: 0.7, count: 10, color: "#cbbfd8", size: 14 }, sparks: { dur: 0.8, count: 16, color: "#ffd27a", size: 5 },
    trail: { dur: 3, count: 14, color: "#ffb347", size: 10 }, rain: { dur: 600, count: 90, color: "#a9c4e8", size: 2 },
    smoke: { dur: 2.5, count: 8, color: "#9a94a8", size: 60 }};
  const EASES = [["inout", "Dous (antre + soti)"], ["out", "Ralanti nan fen"], ["punch", "Fò"], ["linear", "Lineyè"]];

  function el(tag, css, txt) { const e = document.createElement(tag); if (css) e.style.cssText = css; if (txt != null) e.textContent = txt; return e; }
  function changed(full) { DIRTY = true; if (full) renderRight(); build(); }
  function card(f, title, hint) {
    const c = el("div", "background:#17122b;border:1px solid #35295c;border-radius:9px;padding:9px 10px;margin:0 0 10px");
    c.appendChild(el("div", "font-weight:800;color:#c4b5fd;font-size:13px;margin-bottom:3px", title));
    if (hint) c.appendChild(el("div", "color:var(--dim);font-size:11px;margin-bottom:4px", hint));
    f.appendChild(c); return c;
  }
  function grid(p) { const g = el("div", "display:grid;grid-template-columns:1fr 1fr;gap:0 8px"); p.appendChild(g); return g; }
  // chan nimewo: label vizib (pa janm ikòn san non) + snapshot pou Undo
  function num(p, lab, get, set, o) {
    o = o || {};
    const w = el("div"); const l = el("label", "", lab); const i = el("input");
    i.type = "number"; i.step = o.step || 1; if (o.min != null) i.min = o.min; if (o.max != null) i.max = o.max;
    const v = get(); i.value = v == null ? "" : v; if (o.ph != null) i.placeholder = o.ph;
    i.onchange = () => { snapshot(); const x = i.value === "" ? null : +i.value; set(x == null || isNaN(x) ? null : x); changed(o.full); };
    w.appendChild(l); w.appendChild(i); p.appendChild(w); return i;
  }
  function sel(p, lab, opts, get, set, full) {
    const w = el("div"); w.appendChild(el("label", "", lab));
    const s = el("select");
    for (const [v, t] of opts) { const op = el("option", "", t); op.value = v; s.appendChild(op); }
    s.value = get() || ""; s.onchange = () => { snapshot(); set(s.value); changed(full); };
    w.appendChild(s); p.appendChild(w); return s;
  }
  function btn(p, txt, fn, pri, title) {
    const b = el("button", "justify-content:center;font-size:11px;padding:4px 8px", txt); if (pri) b.className = "pri";
    if (title) b.title = title; b.onclick = fn; p.appendChild(b); return b;
  }
  const r2 = x => Math.round(x * 100) / 100;
  const nowIn = () => r2(Math.max(0, CUR - sStart(SEL)));          // «kounye a» = tèt lekti a, an segonn nan sèn nan
  const rigNames = sc => Object.keys((sc && sc.rig) || {});

  // ------------------------------------------------------------------ KAMERA
  function cameraUI(f, sc) {
    const c = card(f, T("camfx_cam_title", "📷 Kamera"),
      T("camfx_cam_hint", "Pou dekò vektè Design (sèn html). Kouch «fon 1…6» yo deplase pi dousman: paralaks."));
    if (sc.type !== "html") {
      c.appendChild(el("div", "color:var(--dim);font-size:11px", T("camfx_cam_only_html", "Sèn sa a pa yon sèn html. Pou imaj / videyo, zoom nan Prop la.")));
      return;
    }
    const on = !!(sc.camera && typeof sc.camera === "object" && !sc.camera.from);
    const row = el("div", "display:flex;gap:6px;margin:4px 0"); c.appendChild(row);
    if (!on) {
      btn(row, T("camfx_cam_add", "Aktive kamera a"), () => {
        snapshot(); sc.camera = { pan: [70, 0], zoom: 1.05, ease: "inout", limit: 120 }; changed(true);
      }, true).style.flex = "1";
      return;
    }
    const cam = sc.camera;
    const pan = Array.isArray(cam.pan) ? cam.pan : [+cam.pan || 0, 0];
    const zoom = Array.isArray(cam.zoom) ? cam.zoom : [1, cam.zoom == null ? 1 : +cam.zoom];
    let g = grid(c);
    num(g, T("camfx_pan_x", "Deplase orizontal (px, + = adwat)"), () => pan[0], v => { cam.pan = [v || 0, pan[1]]; }, { step: 10 });
    num(g, T("camfx_pan_y", "Deplase vètikal (px, + = anba)"), () => pan[1], v => { cam.pan = [pan[0], v || 0]; }, { step: 10 });
    num(g, T("camfx_zoom_from", "Zoom kòmansman"), () => zoom[0], v => { cam.zoom = [v || 1, zoom[1]]; }, { step: 0.01, min: 0.2, max: 5 });
    num(g, T("camfx_zoom_to", "Zoom fen"), () => zoom[1], v => { cam.zoom = [zoom[0], v || 1]; }, { step: 0.01, min: 0.2, max: 5 });
    const og = cam.origin || [];
    num(g, T("camfx_origin_x", "Pwen zoom x (px)"), () => og[0], v => { if (v == null) delete cam.origin; else cam.origin = [v, og[1] != null ? og[1] : 540]; }, { ph: "mitan" });
    num(g, T("camfx_origin_y", "Pwen zoom y (px)"), () => og[1], v => { if (v == null) delete cam.origin; else cam.origin = [og[0] != null ? og[0] : 960, v]; }, { ph: "mitan" });
    sel(g, T("camfx_ease", "Mouvman"), EASES, () => cam.ease || "inout", v => { cam.ease = v; });
    num(g, T("camfx_limit", "Limit (px)"), () => cam.limit, v => { if (v == null) delete cam.limit; else cam.limit = v; }, { step: 10, min: 0, ph: "san limit" });
    // swiv yon pèsonaj (rig sèn nan)
    const names = rigNames(sc);
    const fol = typeof cam.follow === "string" ? { rig: cam.follow } : (cam.follow || null);
    g = grid(c);
    sel(g, T("camfx_follow", "Swiv pèsonaj"), [["", T("camfx_none", "Okenn")]].concat(names.map(n => [n, n])),
      () => (fol && fol.rig) || "", v => { if (!v) delete cam.follow; else cam.follow = { rig: v, amount: (fol && fol.amount) || 0.5 }; }, true);
    if (fol && fol.rig)
      num(g, T("camfx_follow_amt", "Fòs swiv (0-1)"), () => fol.amount != null ? fol.amount : 0.5,
        v => { cam.follow = { ...fol, amount: Math.max(0, Math.min(1, v == null ? 0.5 : v)) }; }, { step: 0.05, min: 0, max: 1 });
    // tranbleman
    c.appendChild(el("div", "font-weight:700;color:#e9d5ff;font-size:12px;margin:10px 0 2px", T("camfx_shake", "Tranbleman (chòk, ateri)")));
    const sh = Array.isArray(cam.shake) ? cam.shake : (cam.shake ? [cam.shake] : []);
    cam.shake = sh;
    sh.forEach((s, j) => {
      const gg = el("div", "display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:0 6px;align-items:end"); c.appendChild(gg);
      num(gg, T("camfx_at", "Lè (s)"), () => s.at, v => { s.at = v || 0; }, { step: 0.1, min: 0 });
      num(gg, T("camfx_force", "Fòs (px)"), () => s.force != null ? s.force : 6, v => { s.force = v == null ? 6 : v; }, { step: 1, min: 0, max: 80 });
      num(gg, T("camfx_dur", "Dire (s)"), () => s.dur != null ? s.dur : 0.35, v => { s.dur = v == null ? 0.35 : v; }, { step: 0.05, min: 0.05 });
      btn(gg, T("camfx_del", "Retire"), () => { snapshot(); sh.splice(j, 1); changed(true); });
    });
    const r = el("div", "display:flex;gap:6px;margin-top:6px;flex-wrap:wrap"); c.appendChild(r);
    btn(r, T("camfx_shake_add", "+ Tranbleman kounye a"), () => { snapshot(); sh.push({ at: nowIn(), force: 7, dur: 0.35 }); changed(true); },
      false, T("camfx_now_title", "Lè tèt lekti a ye nan sèn nan"));
    btn(r, T("camfx_cam_off", "Retire kamera a"), () => { snapshot(); delete sc.camera; changed(true); });
  }

  // ------------------------------------------------------------------ PATIKIL
  function fxListUI(f, sc) {
    const c = card(f, T("camfx_fx_title", "✨ Patikil"),
      T("camfx_fx_hint", "Menm imaj chak fwa (aperçu = rann). Pozisyon an px nan sèn nan."));
    const list = Array.isArray(sc.fx) ? sc.fx : [];
    const names = rigNames(sc);
    list.forEach((e, j) => {
      const box = el("div", "border-top:1px solid #2d254c;margin-top:8px;padding-top:6px"); c.appendChild(box);
      const head = el("div", "display:flex;align-items:center;justify-content:space-between");
      head.appendChild(el("b", "color:#fde68a;font-size:12px", (j + 1) + ". " + ((FX_TYPES.find(x => x[0] === e.type) || [0, e.type])[1])));
      btn(head, T("camfx_del", "Retire"), () => { snapshot(); list.splice(j, 1); if (!list.length) delete sc.fx; changed(true); });
      box.appendChild(head);
      const g = grid(box), d = FX_DEF[e.type] || {};
      num(g, T("camfx_at", "Lè (s)"), () => e.at != null ? e.at : 0, v => { e.at = v || 0; }, { step: 0.1, min: 0 });
      num(g, T("camfx_dur", "Dire (s)"), () => e.dur != null ? e.dur : d.dur, v => { if (v == null) delete e.dur; else e.dur = v; }, { step: 0.1, min: 0.05 });
      if (e.type === "trail") {
        sel(g, T("camfx_trail_rig", "Dèyè pèsonaj"), names.length ? names.map(n => [n, n]) : [[e.follow || "", e.follow || "—"]],
          () => e.follow || "", v => { e.follow = v; });
        num(g, T("camfx_off_x", "Dekalaj x"), () => (e.offset || [0, 0])[0], v => { e.offset = [v || 0, (e.offset || [0, 0])[1]]; });
        num(g, T("camfx_off_y", "Dekalaj y"), () => (e.offset || [0, 0])[1], v => { e.offset = [(e.offset || [0, 0])[0], v || 0]; });
      } else if (e.type !== "rain") {
        num(g, "x (px)", () => e.x, v => { e.x = v || 0; }, { step: 5 });
        num(g, "y (px)", () => e.y, v => { e.y = v || 0; }, { step: 5 });
      } else {
        num(g, T("camfx_angle", "Ang (degre)"), () => e.angle != null ? e.angle : 12, v => { e.angle = v == null ? 12 : v; }, { min: -80, max: 80 });
      }
      num(g, T("camfx_count", "Kantite"), () => e.count != null ? e.count : d.count, v => { if (v == null) delete e.count; else e.count = Math.round(v); }, { min: 1, max: 300 });
      num(g, T("camfx_size", "Gwosè (px)"), () => e.size != null ? e.size : d.size, v => { if (v == null) delete e.size; else e.size = v; }, { step: 0.5, min: 0.5 });
      num(g, T("camfx_opacity", "Opasite (0-1)"), () => e.opacity != null ? e.opacity : (e.type === "rain" ? 0.45 : 0.6),
        v => { if (v == null) delete e.opacity; else e.opacity = Math.max(0, Math.min(1, v)); }, { step: 0.05, min: 0, max: 1 });
      const cw = el("div"); cw.appendChild(el("label", "", T("camfx_color", "Koulè")));
      const ci = el("input"); ci.type = "color"; ci.value = (e.color || d.color || "#ffffff").slice(0, 7);
      ci.onchange = () => { snapshot(); e.color = ci.value; changed(); }; cw.appendChild(ci); g.appendChild(cw);
    });
    c.appendChild(el("div", "font-weight:700;color:#e9d5ff;font-size:12px;margin:10px 0 4px", T("camfx_fx_add", "Ajoute (lè tèt lekti a ye)")));
    const r = el("div", "display:flex;gap:5px;flex-wrap:wrap"); c.appendChild(r);
    for (const [t, lab] of FX_TYPES) {
      if (t === "trail" && !names.length) continue;                 // sillage: bezwen yon pèsonaj rig
      btn(r, "+ " + T("camfx_t_" + t, lab), () => {
        snapshot();
        if (!Array.isArray(sc.fx)) sc.fx = [];                      // filtè koulè sèn nan pa t janm rann: ranplase l
        const e = { type: t, at: t === "rain" ? 0 : nowIn() };
        if (t === "trail") { e.follow = names[0]; e.at = 0; e.dur = r2(sDur(SEL)); }
        else if (t !== "rain") { e.x = 960; e.y = 540; }
        sc.fx.push(e); changed(true);
      });
    }
  }

  const _orig = typeof renderEffect === "function" ? renderEffect : null;
  renderEffect = function (f) {                                       // eslint-disable-line no-global-assign
    const sc = SEL >= 0 && SPEC && SPEC.scenes ? SPEC.scenes[SEL] : null;
    if (!sc || CLIPSEL) return _orig ? _orig(f) : undefined;
    f.innerHTML = "";
    const h = el("h3", "color:var(--mov);margin:0 0 6px;font-size:14px", T("camfx_tab", "Efè · Kamera · Patikil"));
    f.appendChild(h);
    cameraUI(f, sc);
    fxListUI(f, sc);
    if (!Array.isArray(sc.fx) && _orig) {                             // ansyen filtè koulè yo (konpatibilite)
      const holder = el("div", "opacity:.95"); f.appendChild(holder);
      _orig(holder);
      const h2 = holder.querySelector("h3"); if (h2) h2.textContent = T("camfx_filters", "Filtè koulè");
    }
  };
})();
