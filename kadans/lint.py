"""Kadans WASDEV — lint: look at every scene the way a viewer will, before spending minutes on a render.

For each scene, at the moment its entrance animations are finished, the page measures its own layout
(getBoundingClientRect) and reports, as JSON an AI can act on:
  outside_safe_area  a text / card leaves the safe area (5 % margin: phones and TVs crop the edges)
  text_clipped       a word wider than its box
  text_too_long      a title / subtitle so long it fills almost half the frame (shorten it)
  overlap            two text blocks cover each other
  image_missing      a logo / photo / clip frame / background / overlay failed to load
  overlay_covers_text  a front overlay (opacity > 0.45) covers more than 30 % of a text block
  card_covers_text     a cut-out card covers more than 30 % of a text block
  image_not_shown      a card's background-image url() was rejected by CSS (space in path?)
  font_missing       the brand font is not installed (the browser falls back to another one)
  voice_too_long     the voice line is longer than the requested duration: the scene is extended (never cut) and
                     every later scene moves by shift_s
  lipsync_no_mouth   a `lipsync` scene has no [data-mouth] element with [data-shape] children
  lipsync_no_voice   a `lipsync` scene has no voice line (the mouth stays closed)
  mouth_shape_missing  a mouth has no A / B / C / D / E / F shape (the closest one is shown instead)
  rig_missing        a `rig` names a character that is not in the scene ([data-rig="Lina"] from Design)
  sound_not_found    a `sounds` / `ambience` src finds nothing in the CC0 library («find:…», «sfx:id») or the
                     file does not exist
  rig_no_roles       an action needs limbs the character does not have (walk without legs, fly without
                     wings: name the bones «kwis dwat», «zèl goch»… or set them with rig2d_role)
  voice_double       a narration clip on an audio track AND scene voices: two voices would speak at once
  track_voice_no_words  captions are on but a narration clip has no word times (<file>.words.json / clip.words)
"""
from __future__ import annotations

import math
import os
import re
import subprocess
from pathlib import Path

from . import media
from .cdp import Browser
from .compose import build_html
from .spec import LEAD_IN, TAIL, anim_need, icon_unknown, timeline as make_timeline, validate

_JS = r"""
(() => {
  const W = K.w, H = K.h, m = Math.min(W, H) * 0.05, out = [], sc = document.querySelector(`.scene[data-s="%d"]`);
  const SEL = ".h1,.h2,.sub,.tagline,.brand,.cta,.card,.check,.stat,.chip,.col,.code";
  const name = el => (el.className.split(" ")[0] || el.tagName) + ": " + (el.innerText || "").trim().slice(0, 40).replace(/\s+/g, " ");
  const els = [...sc.querySelectorAll(SEL)].filter(el => { const r = el.getBoundingClientRect(); return r.width > 2 && r.height > 2; });
  for (const el of els) {
    const r = el.getBoundingClientRect();
    const over = Math.max(m - r.left, m - r.top, r.right - (W - m), r.bottom - (H - m));
    if (over > 1) out.push({kind: "outside_safe_area", el: name(el), px: Math.round(over)});
    // a word really cut sticks out by letters; a glyph overhang (italic "x", highlight padding) is a few px
    const tol = Math.max(4, 0.15 * parseFloat(getComputedStyle(el).fontSize || 16));
    if (el.scrollWidth > el.clientWidth + tol && !el.matches(".code")) out.push({kind: "text_clipped", el: name(el)});
    const oh = el.offsetHeight || r.height;   // offsetHeight = layout (pa gwosi/piti pa yon transform pandan animasyon an)
    if (el.matches(".h1,.h2,.sub") && oh > H * 0.42) out.push({kind: "text_too_long", el: name(el), lines: Math.round(oh / parseFloat(getComputedStyle(el).lineHeight || 1))});
  }
  for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
    const a = els[i], b = els[j]; if (a.contains(b) || b.contains(a)) continue;
    const A = a.getBoundingClientRect(), B = b.getBoundingClientRect();
    const ix = Math.max(0, Math.min(A.right, B.right) - Math.max(A.left, B.left));
    const iy = Math.max(0, Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top));
    const small = Math.min(A.width * A.height, B.width * B.height);
    if (ix * iy > 0.04 * small) out.push({kind: "overlap", el: name(a), with: name(b), pct: Math.round(100 * ix * iy / small)});
  }
  if (K.scenes[%d].mouth) {                                // lipsync: bouch [data-mouth] > [data-shape]
    const ms = [...sc.querySelectorAll("[data-mouth]")];
    if (!ms.length || !ms.some(g => g.querySelector("[data-shape]"))) out.push({kind: "lipsync_no_mouth",
      hint: "<g data-mouth='Lina'><g data-shape='A'>...</g> ... <g data-shape='X'>...</g></g>"});
    for (const g of ms) {
      const have = new Set([...g.querySelectorAll("[data-shape]")].flatMap(e => e.dataset.shape.split(/[\s,]+/)));
      const miss = ["A", "B", "C", "D", "E", "F"].filter(x => !have.has(x));
      if (have.size && miss.length) out.push({kind: "mouth_shape_missing", el: g.dataset.mouth, missing: miss.join("")});
    }
  }
  const RS = K.scenes[+sc.dataset.s].rig;                // pèsonaj cut-out: yo la? zo yo gen wòl mouvman an?
  if (RS) for (const nm in RS) {
    const el = [...sc.querySelectorAll("[data-rig]")].find(e => e.dataset.rig.toLowerCase() === nm.toLowerCase());
    const faceOnly = [...sc.querySelectorAll("[data-mouth],[data-eyes],[data-brows]")].some(e =>
      (e.dataset.mouth || e.dataset.eyes || e.dataset.brows || "").toLowerCase() === nm.toLowerCase());
    if (!el && faceOnly && !(RS[nm].do || []).length) continue;     // figi sèlman (ekspresyon), pa gen kò
    if (!el) { out.push({kind: "rig_missing", el: nm, have: [...sc.querySelectorAll("[data-rig]")].map(e => e.dataset.rig),
                         hint: "Design: op character / rig2d_create, then kadans_scene"}); continue; }
    let roles = []; try { roles = JSON.parse(el.dataset.rigdef).bones.map(b => b.role).filter(Boolean); } catch (e) {}
    for (const a of RS[nm].do || []) {
      const want = Object.keys((K.rigm[a.do] || {}).keys || {}).filter(r => /^(arm|forearm|hand|thigh|shin|foot|wing)_/.test(r));
      if (want.length && !want.some(r => roles.includes(r) || roles.includes(r.replace(/_[rl]$/, a.side === "l" ? "_r" : "_l"))))
        out.push({kind: "rig_no_roles", el: nm, do: a.do, need: want.join(" "), have: roles.join(" ")});
    }
  }
  for (const im of sc.querySelectorAll("img")) if (!im.complete || !im.naturalWidth) out.push({kind: "image_missing", el: im.getAttribute("src")});
  for (const ov of [...sc.querySelectorAll(".ov.front"), ...document.querySelectorAll("#stagefront .ov")]) {
    if (+getComputedStyle(ov).opacity < 0.45) continue;
    const O = ov.getBoundingClientRect();
    for (const el of els) {
      const A = el.getBoundingClientRect();
      const ix = Math.max(0, Math.min(A.right, O.right) - Math.max(A.left, O.left));
      const iy = Math.max(0, Math.min(A.bottom, O.bottom) - Math.max(A.top, O.top));
      if (ix * iy > 0.3 * A.width * A.height) { out.push({kind: "overlay_covers_text", el: name(el), overlay: ov.dataset.anim}); break; }
    }
  }
  for (const card of sc.querySelectorAll(".card3d")) {
    if (getComputedStyle(card).backgroundImage === "none")
      out.push({kind: "image_not_shown", el: name(card), hint: "url() rejte pa CSS (espas/karaktè espesyal nan chemen an?)"});
    const C = card.getBoundingClientRect();
    for (const el of els) {
      const A = el.getBoundingClientRect();
      const ix = Math.max(0, Math.min(A.right, C.right) - Math.max(A.left, C.left));
      const iy = Math.max(0, Math.min(A.bottom, C.bottom) - Math.max(A.top, C.top));
      if (ix * iy > 0.3 * A.width * A.height) { out.push({kind: "card_covers_text", el: name(el), fix: "deplase cards[].at oswa redwi cards[].width"}); break; }
    }
  }
  return out;
})()
"""


def track_voice_issues(spec: dict, base) -> list[dict]:
    """Voice clips on audio tracks: a scene voice playing over them (two voices at once), or captions on but no word
    times for the clip (its captions would be missing)."""
    from pathlib import Path
    from .audio import is_voice_clip
    from .compose import _words_file
    issues = []
    voiced = [i for i, sc in enumerate(spec["scenes"]) if sc.get("voice") or sc.get("voice_file")]
    for ti, tk in enumerate(spec.get("tracks") or []):
        if tk.get("muted"):
            continue
        for ci, c in enumerate(tk.get("clips") or []):
            if c.get("kind") not in ("audio", "voice") or not c.get("src"):
                continue
            p = media.resolve(c["src"], base)
            if not is_voice_clip(tk, c, p):
                continue
            try:
                a, b = float(c.get("start", 0) or 0), float(c.get("start", 0) or 0) + float(c.get("dur", 0) or 0)
            except (TypeError, ValueError):
                continue
            if voiced:
                issues.append({"scene": voiced[0], "kind": "voice_double", "track": ti, "clip": ci,
                               "scenes_with_voice": voiced[:8], "span": [round(a, 2), round(b, 2)],
                               "fix": "the narration on the track already speaks: remove the scenes' voice / voice_file "
                                      "(or mute the track)"})
            if spec.get("captions") and c.get("captions") is not False and not c.get("words") and not (
                    Path(p).is_file() and _words_file(Path(p))):
                issues.append({"scene": None, "kind": "track_voice_no_words", "track": ti, "clip": ci,
                               "src": c["src"], "fix": "<voice file>.words.json (ElevenLabs / Whisper word times) "
                                                       "or clip.words = [[word, start, end], ...]"})
    return issues


def measure_loudness(audio_path: str | Path) -> dict:
    """Mezire konfòmite EBU R128 / ITU-R BS.1770 sou yon fichye odyo (LUFS, LRA, True Peak)."""
    p = Path(audio_path).resolve()
    if not p.is_file():
        return {"ok": False, "error": f"Fichye odyo pa jwenn: {p}"}

    try:
        from . import media
        ff = media.find_tool("ffmpeg")
        cmd = [
            ff, "-nostats", "-i", str(p),
            "-filter_complex", "ebur128=peak=true",
            "-f", "null", "-"
        ]
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, creationflags=flags)
        stderr = res.stderr or ""
        i_m = re.search(r"Integrated loudness:\s+I:\s+([-\d.]+)\s+LUFS", stderr)
        lra_m = re.search(r"Loudness range:\s+LRA:\s+([-\d.]+)\s+LU", stderr)
        tpk_m = re.search(r"True peak:\s+Peak:\s+([-\d.]+)\s+dBFS", stderr)
        if i_m:
            i_val = float(i_m.group(1))
            lra_val = float(lra_m.group(1)) if lra_m else 0.0
            tpk_val = float(tpk_m.group(1)) if tpk_m else -99.0
            return {
                "ok": True,
                "file": str(p),
                "integrated_lufs": round(i_val, 1),
                "loudness_range_lu": round(lra_val, 1),
                "true_peak_db": round(tpk_val, 1),
                "method": "ebur128_ffmpeg",
                "social_compliant": (-16.0 <= i_val <= -12.0) and tpk_val <= -1.0,
                "broadcast_compliant": (-24.0 <= i_val <= -22.0) and tpk_val <= -1.0,
            }
    except Exception:
        pass

    try:
        import struct
        import wave
        with wave.open(str(p), "rb") as wf:
            sampwidth = wf.getsampwidth()
            nframes = wf.getnframes()
            if sampwidth == 2 and nframes > 0:
                raw = wf.readframes(min(nframes, 48000 * 60))
                samples = struct.unpack(f"<{len(raw)//2}h", raw)
                peak = max(abs(s) for s in samples) if samples else 1
                rms = math.sqrt(sum(s * s for s in samples) / len(samples)) if samples else 1
                peak_db = 20 * math.log10(max(1, peak) / 32768.0)
                rms_db = 20 * math.log10(max(1.0, rms) / 32768.0)
                est_lufs = round(rms_db - 0.691, 1)
                return {
                    "ok": True,
                    "file": str(p),
                    "integrated_lufs": est_lufs,
                    "loudness_range_lu": 5.0,
                    "true_peak_db": round(peak_db, 1),
                    "method": "rms_fallback",
                    "social_compliant": (-16.0 <= est_lufs <= -12.0) and peak_db <= -1.0,
                    "broadcast_compliant": (-24.0 <= est_lufs <= -22.0) and peak_db <= -1.0,
                }
    except Exception as ex:
        return {"ok": False, "error": str(ex)}

    return {"ok": False, "error": "Mezi odyo pa posib sou fichye sa a"}


def check_loudness_issues(spec: dict, base: Path, cache: Path) -> list[dict]:
    """Tcheke konfòmite EBU R128 (-14 LUFS Social / -23 LUFS Broadcast) sou odyo ki disponib la."""
    issues = []
    cands = [
        cache / "render" / "preview-audio.wav",
        cache / "preview-audio.wav",
        base / "preview-audio.wav",
        base / "mix.wav",
    ]
    for sc in spec.get("scenes") or []:
        vf = sc.get("voice_file")
        if vf:
            p = Path(vf) if Path(vf).is_absolute() else base / vf
            cands.append(p)
    music = spec.get("music")
    if isinstance(music, dict) and music.get("src"):
        mp = Path(music["src"]) if Path(music["src"]).is_absolute() else base / music["src"]
        cands.append(mp)

    target_file = next((f for f in cands if f.is_file()), None)
    if not target_file:
        return []

    meas = measure_loudness(target_file)
    if not meas.get("ok"):
        return []

    i_lufs = meas.get("integrated_lufs", -14.0)
    tpk = meas.get("true_peak_db", -2.0)

    if i_lufs > -11.5:
        issues.append({
            "scene": None,
            "kind": "loudness_too_high",
            "integrated_lufs": i_lufs,
            "target_lufs": -14.0,
            "true_peak_db": tpk,
            "file": target_file.name,
            "fix": f"Nivo odyo {target_file.name} twò fò ({i_lufs} LUFS > -14 LUFS YouTube/TikTok). Diminye volim nan spec la (mix.bed_ceiling oswa volume)."
        })
    elif i_lufs < -26.0:
        issues.append({
            "scene": None,
            "kind": "loudness_too_low",
            "integrated_lufs": i_lufs,
            "target_lufs": -14.0,
            "true_peak_db": tpk,
            "file": target_file.name,
            "fix": f"Nivo odyo {target_file.name} twò ba ({i_lufs} LUFS < -14 LUFS YouTube/TikTok). Ogmante volim vwa oswa mizik la."
        })

    if tpk > -0.5:
        issues.append({
            "scene": None,
            "kind": "true_peak_clipping",
            "true_peak_db": tpk,
            "file": target_file.name,
            "fix": f"Pik odyo {target_file.name} rive {tpk} dBFS (> -1.0 dBFS sekirite). Risk saturation sou aparèy mobil."
        })

    return issues



def check_color_contrast_issues(spec: dict) -> list:
    """Kontwole kontras kolorimetrik ak lisibilite tèks sou fon videyo."""
    issues = []
    brand = spec.get("brand") or {}
    bg = brand.get("bg")
    fg = brand.get("text")
    if bg and fg:
        try:
            import sys
            root_wasdev = Path(__file__).resolve().parent.parent.parent / "wasdev"
            if str(root_wasdev) not in sys.path:
                sys.path.insert(0, str(root_wasdev))
            from app.design.color_math import contrast_ratio
            ratio = contrast_ratio(bg, fg)
            if ratio < 3.0:
                issues.append({
                    "scene": None,
                    "kind": "low_contrast_brand",
                    "bg": bg,
                    "text": fg,
                    "ratio": round(ratio, 2),
                    "fix": f"Rapò kontras tèks ({fg}) sou fon ({bg}) se {round(ratio, 2)}:1 (< 3.0:1). Ogmante diferans lan pou pi bon lisibilite."
                })
        except Exception:
            pass
    return issues


def lint(spec: dict, base=None, cache=None, voice_s: dict | None = None) -> dict:
    """{ok, issues: [{scene, id, type, t, kind, ...}]}. Voice lengths (voice_s) make the timing check exact."""
    from pathlib import Path
    base = Path(base).resolve() if base else Path.cwd()
    cache = Path(cache).resolve() if cache else base / ".kadans-cache"
    spec = validate(spec) if "w" not in spec else spec
    media_s, clips = media.prepare(spec, base, cache / "clips")
    vs = dict(voice_s or {})                              # O13: vrè dire WAV voice_file yo (pa estimasyon tèks la)
    for sc in spec["scenes"]:
        vf = sc.get("voice_file")
        if vf and sc["id"] not in vs:
            try:
                from .audio import wav_seconds
                q = Path(vf) if Path(vf).is_absolute() else base / vf
                vs[sc["id"]] = wav_seconds(q)
            except Exception:                            # noqa: BLE001
                pass
    tl = make_timeline(spec, vs or None, media_s)
    work = cache / "render"
    work.mkdir(parents=True, exist_ok=True)
    page = work / "lint.html"
    page.write_text(build_html(spec, tl, base, clips, work), encoding="utf-8")
    issues = []
    for i, sc in enumerate(spec["scenes"]):              # O12: ikòn enkoni (li t ap parèt kòm gwo tèks)
        if sc["type"] == "features":
            for j, it in enumerate(sc.get("items") or []):
                if isinstance(it, dict) and icon_unknown(it.get("icon")):
                    issues.append({"scene": i, "id": sc["id"], "type": "features", "kind": "unknown_icon",
                                   "item": j, "icon": str(it.get("icon")),
                                   "hint": "yon emoji, oswa yon non tankou code/palette/rocket/chart/users"})
    for i, (sc, t) in enumerate(zip(spec["scenes"], tl)):
        end = LEAD_IN + (t["voice_dur"] or 0)
        # v3.12: depi v3.04 sèn nan ALONJE pou vwa a (li pa janm koupe), kidonk t["dur"] toujou >= vwa a: konpare ak
        # «duration» moun nan / AI a te mande a. Rezilta: sèn nan pi long, tout sèn ki apre l yo deplase — di l klè.
        if sc.get("duration") and t["voice_dur"] and end + TAIL > sc["duration"] + 0.05:
            import math
            issues.append({"scene": i, "id": sc["id"], "type": sc["type"], "kind": "voice_too_long",
                           "voice_s": round(t["voice_dur"], 3), "scene_s": t["dur"], "asked_s": sc["duration"],
                           "voice_start": LEAD_IN, "voice_end": round(end, 3), "tail_min": TAIL,
                           "cut": False,                                 # vwa a pa janm koupe: sèn nan alonje
                           "shift_s": round(t["dur"] - sc["duration"], 3),  # konbyen sèn ki apre yo deplase
                           "measured": bool(t.get("measured")),
                           "fix": f"duration >= {math.ceil((end + TAIL) * 10) / 10} s (or shorten the voice line)"})
        if sc.get("lipsync") and not (sc.get("voice") or sc.get("voice_file")):
            issues.append({"scene": i, "id": sc["id"], "type": sc["type"], "kind": "lipsync_no_voice",
                           "fix": "add a voice line (voice / voice_file) or remove lipsync"})
    issues += track_voice_issues(spec, base)
    issues += check_loudness_issues(spec, base, cache)
    issues += check_color_contrast_issues(spec)
    from .sounds import clips as _sound_clips             # son ki pa jwenn (find: san rezilta, fichye ki pa la)
    for m in _sound_clips(spec, tl, base)[1]:
        i = next(k for k, sc in enumerate(spec["scenes"]) if sc["id"] == m["scene"])
        issues.append({"scene": i, "id": m["scene"], "type": spec["scenes"][i]["type"], "kind": "sound_not_found",
                       "src": m["src"], "hint": "kadans sounds <words> lists the CC0 library (or use a file path)"})
    with Browser() as br:
        pg = br.pages(page.as_uri() + "#render", 1, spec["w"], spec["h"])[0]
        for key in ("font", "font_title", "font_code"):
            font = (spec["brand"].get(key) or "").replace('"', "").replace("'", "")
            if not font:
                continue
            # @font-face fonts load only when text needs them: load it NOW, or the canvas measures the fallback
            pg.eval("document.fonts.load('40px \"" + font + "\"').then(() => true, () => false)")
            # missing = draws exactly like BOTH fallbacks (one fallback alone fails for a monospace font such as
            # Consolas, which IS the default monospace)
            same = pg.eval("(() => { const c = document.createElement('canvas').getContext('2d'); const s = 'WASDEVmgil10';"
                           "const m = g => { c.font = '40px ' + g; return c.measureText(s).width; };"
                           f"return m('\"{font}\", monospace') === m('monospace') && m('\"{font}\", serif') === m('serif'); }})()",
                           wait=False)
            if same:                               # draws exactly like the fallback: not installed, not embedded
                issues.append({"scene": None, "kind": "font_missing", "field": f"brand.{key}", "font": font,
                               "hint": "kadans fonts <word> lists the fonts of this PC"})
        for i, (sc, t) in enumerate(zip(spec["scenes"], tl)):
            at = t["start"] + min(t["dur"] - 0.4, max(anim_need(sc), 1.2) + 0.1)
            pg.eval(f"window.__seek({max(t['start'], at):.3f})")
            for it in pg.eval(_JS % (i, i), wait=False) or []:
                issues.append({"scene": i, "id": sc["id"], "type": sc["type"], "t": round(at, 2), **it})
    return {"ok": not issues, "issues": issues, "scenes": len(tl)}
