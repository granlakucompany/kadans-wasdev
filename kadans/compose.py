"""Kadans WASDEV — spec + timeline -> ONE self-contained HTML page (the composition).

The page draws any instant of the video deterministically: window.__seek(t) (seconds). A renderer (any Chromium
through the DevTools protocol) seeks every frame and screenshots it; nothing depends on wall-clock time, so a frame
is identical on every machine. Opened directly in a browser (no #render in the URL) the page fits the window and
plays itself in a loop: that is the live preview.

Layout is written in "u" units (1u = min(width, height) / 1080 px) so one template works in 16:9, 9:16, 1:1, 4:5.
"""
from __future__ import annotations

import base64
import math
import html
import json
import math
import os
import shutil
import re
import unicodedata
from pathlib import Path

from .spec import NATIVE_BLEND, PREVIEW_BLEND, icon_glyph, timeline as _timeline, total as _total, validate
from .motion import JS as MOTION_JS, MOTIONS

ASSETS = Path(__file__).with_name("assets")
CREDIT = {"fr": "Créé avec", "en": "Made with", "ht": "Fèt ak", "es": "Hecho con", "pt": "Feito com",
          "de": "Erstellt mit", "it": "Creato con", "ru": "Сделано в"}
_MARK = re.compile(r"\*([^*]+)\*")


def mark(text) -> str:
    """Escape text; *word* -> highlighted span."""
    return _MARK.sub(r'<span class="hl">\1</span>', html.escape(str(text or "")))


# ----------------------------------------------------------------------------------------------- words -> motion
def _norm(w: str) -> str:
    w = unicodedata.normalize("NFD", str(w).lower())
    return "".join(c for c in w if c.isalnum() and unicodedata.category(c) != "Mn")


def _find_word(words: list[dict], label: str, after: float) -> dict | None:
    """First spoken word (at or after `after`) matching a word of the label (accents / case / punctuation ignored;
    a long word may match its beginning: «sécurisé» ~ «sécurité»)."""
    keys = [_norm(x) for x in re.split(r"[\s/+,·-]+", re.sub(r"\*", "", str(label or ""))) if len(_norm(x)) >= 3]
    keys = keys or [_norm(label)]
    for w in words:
        if w["s"] < after - 0.05:
            continue
        n = _norm(w["w"])
        if not n:
            continue
        for k in keys:
            if n == k or (len(k) >= 5 and len(n) >= 5 and (n.startswith(k[:5]) or k.startswith(n[:5]))):
                return w
    return None


def delays(sc: dict, t: dict | None) -> dict:
    """Entrance delay (seconds from the scene start) of every item, chip and column. Each one waits for the spoken
    word that names it (or the word given in "on"); without a match it keeps the default rhythm."""
    t = t or {}
    words, start = t.get("words") or [], t.get("start", 0.0)

    def anchored(labels, default):
        out, after = [], start
        for i, lab in enumerate(labels):
            d = default(i)
            w = _find_word(words, lab, after) if words and lab else None
            if w:
                d = max(0.1, w["s"] - start - 0.12)
                after = w["s"] + 0.01
            out.append(round(d, 2))
        return out
    typ, items = sc["type"], sc.get("items") or []
    lab = lambda it: (it.get("on") or it.get("title") or it.get("label") or it.get("value")) if isinstance(it, dict) else it
    D = {"items": [], "chips": [], "cols": []}
    if typ == "features":
        D["items"] = anchored([lab(it) for it in items], lambda i: 0.3 + 0.5 * i)
    elif typ == "list":
        D["items"] = anchored([lab(it) for it in items], lambda i: 0.5 + 0.4 * i)
    elif typ == "stat":
        D["items"] = anchored([lab(it) for it in items], lambda i: 0.3 + 0.4 * i)
    elif typ == "compare":
        D["cols"] = anchored([(sc.get(k) or {}).get("on") or (sc.get(k) or {}).get("title") for k in ("left", "right")],
                             lambda i: (0.3, 0.8)[i])
    if sc.get("chips"):
        D["chips"] = anchored([lab(c) for c in sc["chips"]], lambda i: 0.8 + 0.25 * i)
    return D


def chip_text(c) -> str:
    """A chip is a label, or {title|text|label, on?} (on = spoken word that makes it appear)."""
    if isinstance(c, dict):
        return str(c.get("title") or c.get("text") or c.get("label") or c.get("on") or "")
    return str(c)


def _emphasis(html_s: str, t: dict | None) -> str:
    """*highlighted* words get the time they are spoken (data-at): they pulse at that instant."""
    words = (t or {}).get("words") or []
    if not words:
        return html_s

    def sub(m):
        w = _find_word(words, html.unescape(m.group(1)), 0)
        return f'<span class="hl" data-at="{w["s"]}">{m.group(1)}</span>' if w else m.group(0)
    return re.sub(r'<span class="hl">([^<]+)</span>', sub, html_s)


LIB_FILES = {"anime": "anime.min.js", "chart": "chart.umd.min.js", "lottie": "lottie.min.js",
             "three": "three.min.js", "motion": "motion.min.js", "gsap": "gsap.min.js"}


def _html_reveals(raw, tle):
    words = (tle or {}).get("words") or []
    start = (tle or {}).get("start", 0.0)
    if not words or "data-on=" not in raw:
        return raw
    tag_re = re.compile(r'<([a-zA-Z][\w-]*)((?:[^>]*?)\bdata-on="([^"]+)"(?:[^>]*?))>')

    def sub(m):
        tag, attrs, word = m.group(1), m.group(2), m.group(3)
        w = _find_word(words, html.unescape(word), start)
        d = max(0.1, w["s"] - start - 0.12) if w else 0.3
        attrs = re.sub(r'\s*data-on="[^"]*"', "", attrs)
        cm = re.search(r'class="([^"]*)"', attrs)
        if cm:
            cls = cm.group(1)
            if "a" not in cls.split():
                attrs = attrs[:cm.start(1)] + (cls + " a").strip() + attrs[cm.end(1):]
        else:
            attrs = ' class="a"' + attrs
        return f'<{tag}{attrs} data-d="{d:.2f}">'
    return tag_re.sub(sub, raw)


def events(spec: dict, tl: list[dict]) -> list[dict]:
    """Sound-effect cues on the video clock: whoosh into every scene, pop when an item appears, hit on logo
    reveals. [{t, kind}] sorted, pops at least 0.22 s apart."""
    out = []
    on = spec.get("sfx") or {}
    for i, (sc, t) in enumerate(zip(spec["scenes"], tl)):
        if i > 0:
            out.append({"t": max(0.0, t["start"] - 0.18), "kind": "whoosh"})
        if sc["type"] in ("logo", "cta"):
            out.append({"t": t["start"] + 0.05, "kind": "hit"})
        if sc["type"] in ("hook", "text") and (sc.get("title") or sc.get("subtitle")):
            out.append({"t": t["start"] + 0.15, "kind": "text"})
        if sc["type"] == "code":                    # menm kalandriye ak animasyon tape a (0.5 s + liy pa liy)
            d = 0.5
            for ln in sc.get("lines") or []:
                ln_len = 0.35 + len(ln) / 45
                k = 0.0
                while ln.strip() and k < ln_len - 0.05 and d + k < t["dur"] - 0.2:
                    out.append({"t": t["start"] + d + k, "kind": "type"})
                    k += 0.5                            # echantiyon «type» la dire 0.5 s
                d += ln_len + 0.1
        D = delays(sc, t)
        for d in D["items"] + D["chips"] + D["cols"]:
            if d < t["dur"] - 0.2:
                out.append({"t": t["start"] + d + 0.05, "kind": "pop"})
    out = [e for e in out if on.get(e["kind"], e["kind"] in ("whoosh", "pop", "hit"))]
    out.sort(key=lambda e: e["t"])
    kept, last_pop = [], -9.0
    for e in out:
        if e["kind"] == "pop":
            if e["t"] - last_pop < 0.22:
                continue
            last_pop = e["t"]
        kept.append({"t": round(e["t"], 3), "kind": e["kind"]})
    return kept


_CAP_PAUSE = 0.45          # a real silence (s) always ends a caption line
# TTS markup the voice engine returns as «words» (<break time="0.8s" />, [laughs]…): never shown in captions
_MARKUP = re.compile(r"[<>]|^\w+=\"[^\"]*\"/?>?$|^\[[^\]]*\]$|^/>$")
_SENT_END = (".", "!", "?", "…")
_SOFT_CUT = (",", ";", ":")


def caption_config(spec: dict) -> dict:
    """captions spec (validated) + defaults that read well: one sentence per line, cut on punctuation only when it
    is too long, never a lonely word. Portrait frames get shorter lines."""
    cap = dict(spec.get("captions") or {})
    portrait = spec.get("h", 1080) > spec.get("w", 1920)
    cap.setdefault("max_words", 6 if portrait else 9)
    cap.setdefault("max_chars", 28 if portrait else 52)
    cap.setdefault("min_words", 3)
    return cap


def _cap_too_long(ws: list, cfg: dict) -> bool:
    return len(ws) > cfg["max_words"] or len(" ".join(w["w"] for w in ws)) > cfg["max_chars"]


def _cap_split(ws: list, cfg: dict) -> list[list]:
    """A sentence too long for one line: cut on the punctuation nearest the middle (a colon is preferred), else in
    the middle; both halves keep at least min_words words."""
    mn = max(1, min(cfg["min_words"], len(ws) // 2))
    if not _cap_too_long(ws, cfg) or len(ws) < 2 * mn:
        return [ws]
    mid = len(ws) / 2
    cuts = [i + 1 for i, w in enumerate(ws[:-1]) if w["w"].endswith(_SOFT_CUT) and i + 1 >= mn and len(ws) - i - 1 >= mn]
    if not cuts:
        cuts = [max(mn, min(len(ws) - mn, round(mid)))]
    k = min(cuts, key=lambda c: abs(c - mid) - (2 if ws[c - 1]["w"].endswith(":") else 0))
    return _cap_split(ws[:k], cfg) + _cap_split(ws[k:], cfg)


def caption_lines(tl: list[dict], cfg: dict | None = None, extra: list | None = None) -> list[dict]:
    """Spoken words grouped in caption lines: [{s, e, words: [{w, s, e}]}] (video clock). Words come from every
    scene voice (tl) and from voice clips on audio tracks (extra). A line is one sentence (ends on . ! ? or a real
    silence); a sentence too long is cut on its punctuation, never leaving a word alone."""
    cfg = cfg or {"max_words": 9, "max_chars": 52, "min_words": 3}
    raw = [w for t in tl for w in (t.get("words") or [])] + list(extra or [])
    words = []
    for w in sorted((w for w in raw if str(w.get("w") or "").strip() and not _MARKUP.search(str(w["w"]).strip())),
                    key=lambda w: w["s"]):
        txt = str(w["w"]).strip()
        if not any(ch.isalnum() for ch in txt):         # «:» «!» «—» poukont yo (fransè): kole sou mo anvan an
            if words:
                words[-1] = dict(words[-1], w=words[-1]["w"] + ("" if txt in ",." else " ") + txt)
            continue
        words.append(dict(w, w=txt))
    sentences, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt is None or w["w"].rstrip().endswith(_SENT_END) or nxt["s"] - w["e"] >= _CAP_PAUSE:
            sentences.append(cur)
            cur = []
    merged = []                                         # «Bilan :» poukont li → ak fraz ki vini apre a (poz kout)
    for sent in sentences:
        if merged and len(merged[-1]) < cfg["min_words"] and sent[0]["s"] - merged[-1][-1]["e"] < 1.2 \
                and not _cap_too_long(merged[-1] + sent[:cfg["min_words"]], cfg):
            merged[-1] = merged[-1] + sent
        else:
            merged.append(sent)
    lines = [part for sent in merged for part in _cap_split(sent, cfg)]
    return [{"s": ln[0]["s"], "e": ln[-1]["e"], "words": ln} for ln in lines]


# ---- words of the voice clips on audio tracks (a whole narration laid on a track, not cut in scenes) ----
_AUD_EXT = (".wav", ".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac")
_ONSET_CACHE: dict = {}


def _words_file(p: Path) -> Path | None:
    """<file>.words.json next to the voice (ElevenLabs / Whisper write it), also for the same voice in another
    format (narration.wav made from narration.mp3) anywhere in the project's medya/ folders."""
    cands = [Path(str(p) + ".words.json"), p.with_suffix(".words.json")]
    cands += [Path(str(p.with_suffix(e)) + ".words.json") for e in _AUD_EXT if e != p.suffix.lower()]
    media_root = p.parent.parent
    if media_root.name.lower() in ("medya", "media"):
        cands += sorted(media_root.glob(f"*/{p.stem}.*.words.json")) + sorted(media_root.glob(f"*/{p.stem}.words.json"))
    return next((c for c in cands if c.is_file()), None)


def _read_words(js: Path) -> list[list]:
    try:
        raw = json.loads(js.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if isinstance(raw, dict):
        raw = raw.get("words") or []
    out = []
    for w in raw if isinstance(raw, list) else []:
        try:
            if isinstance(w, dict):
                out.append([str(w.get("w") or w.get("word") or w.get("text") or ""), float(w.get("s", w.get("start"))),
                            float(w.get("e", w.get("end")))])
            else:
                out.append([str(w[0]), float(w[1]), float(w[2])])
        except (TypeError, ValueError, IndexError):
            continue
    return [w for w in out if w[0].strip()]


def _snap_onsets(words: list[list], audio_file: Path) -> list[list]:
    """A speech recognizer often puts the first word of a sentence on the silence before it: move such a word to
    where the voice really starts again (10 ms envelope, cached per file). Without ffmpeg: words unchanged."""
    try:
        st = audio_file.stat()
        key = (str(audio_file), st.st_size, st.st_mtime_ns)
    except OSError:
        return words
    env = _ONSET_CACHE.get(key)
    if env is None:
        try:
            from .audio import peaks
            env = peaks(audio_file, 10)
        except Exception:                                     # noqa: BLE001 - no ffmpeg: no correction
            env = []
        _ONSET_CACHE[key] = env
    if not env:
        return words
    thr = max(0.02, max(env) * 0.06)
    out = []
    for w, s, e in words:
        i = int(s * 100)
        if 0 <= i < len(env) and env[i] < thr:
            j = i
            while j < len(env) and env[j] < thr and j - i < 80:
                j += 1
            if j < len(env) and env[j] >= thr:
                s = round(j / 100, 3)
                e = max(e, s + 0.12)
        out.append([w, s, e])
    return out


def track_words(spec: dict, base: Path | None, out_dir: Path | None = None) -> list[dict]:
    """Caption words of the voice clips on audio tracks, on the video clock: a clip played from `in` for `dur`
    seconds at `speed` shows the words of that part only. Words: the clip's own "words", else the words file of the
    voice. A clip with "captions": false is skipped; a non-voice clip only counts with "captions": true."""
    from .audio import is_voice_clip
    from .media import resolve
    out = []
    for tk in spec.get("tracks") or []:
        if tk.get("muted") or tk.get("hidden"):
            continue
        for c in tk.get("clips") or []:
            if c.get("captions") is False or (c.get("kind") or tk.get("kind")) not in ("audio", "voice") or not c.get("src"):
                continue
            p = None
            for b in (base, out_dir):
                try:
                    rp = resolve(c["src"], b) if b else None
                except Exception:                             # noqa: BLE001
                    rp = None
                if rp and Path(rp).is_file():
                    p = Path(rp)
                    break
            if p is None or not (c.get("captions") is True or is_voice_clip(tk, c, p)):
                continue
            ws = c.get("words")
            ws = [[str(w[0]), float(w[1]), float(w[2])] for w in ws] if isinstance(ws, list) else None
            if ws is None:
                js = _words_file(p)
                ws = _snap_onsets(_read_words(js), p) if js else []
            try:
                start, dur = float(c.get("start", 0) or 0), float(c.get("dur", 0) or 0)
                cin = max(0.0, float(c.get("in", 0) or 0))
            except (TypeError, ValueError):
                continue
            sp = clip_speed(c)
            end_src = cin + dur * sp if dur > 0 else float("inf")
            for w, s, e in ws:
                if s < cin - 1e-3 or s >= end_src:
                    continue
                out.append({"w": w, "s": round(start + (s - cin) / sp, 3), "e": round(start + (min(e, end_src) - cin) / sp, 3)})
    return out


def _caption_css(spec: dict, px) -> str:
    """Caption look: size + the 3 word colours (to come / said / being said) + glow, from spec.captions."""
    c = spec["brand"]["colors"]
    cap = spec.get("captions") or {}
    col = cap.get("colors") or {}
    up, said = col.get("upcoming") or "rgba(255,255,255,.55)", col.get("spoken") or "#ffffff"
    now, glow = col.get("current") or c["primary"], col.get("glow") or (col.get("current") or c["primary"]) + "aa"
    size = float(cap.get("size") or 58)
    return (f"#capt{{position:absolute;left:{px(60)};right:{px(60)};text-align:center;font-size:{px(size)};font-weight:900;"
            f"line-height:1.22;letter-spacing:{px(-0.5)};text-shadow:0 {px(4)} {px(18)} rgba(0,0,0,.85),0 0 {px(2)} rgba(0,0,0,.9);"
            f"pointer-events:none}}\n"
            f"#capt.bottom{{bottom:{px(150)}}} #capt.top{{top:{px(130)}}} #capt.middle{{top:50%;transform:translateY(-50%)}}\n"
            f"#capt span{{display:inline-block;margin:0 .16em;color:{up};transform-origin:50% 60%}}\n"
            f"#capt span.on{{color:{said}}} #capt span.now{{color:{now};text-shadow:0 0 {px(22)} {glow},0 0 {px(40)} {glow},"
            f"0 {px(4)} {px(18)} rgba(0,0,0,.85)}}")


# ----------------------------------------------------------------------------------------------- backgrounds, overlays
_SVG_INLINE_MAX = 400_000              # bigger SVGs are linked (<img>), not inlined (they cannot be recoloured then)


_COLOR_TOKEN = re.compile(r"#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|white|black")
_PAINT = re.compile(r"""((?:fill|stroke|stop-color|flood-color|lighting-color)\s*[=:]\s*["']?\s*)(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|[A-Za-z]+)""")


def recolor_svg(svg: str, color: str) -> str:
    """One-colour asset (white smoke, black shape, splash) -> brand colour. Only paint values change: opacity,
    stop-opacity and gradients stay, so soft smoke stays soft. Paths without a fill inherit the new colour."""
    def paint(m):
        return m.group(1) + color if _COLOR_TOKEN.fullmatch(m.group(2)) else m.group(0)
    svg = _PAINT.sub(paint, svg)
    return re.sub(r"<svg\b", f'<svg fill="{color}"', svg, count=1)


_SVG_N = [0]


def unique_ids(svg: str) -> str:
    """Several inline SVGs share one page: their ids (gradients, clip paths…) must not collide."""
    _SVG_N[0] += 1
    pre = f"k{_SVG_N[0]}_"
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    if not ids:
        return svg
    svg = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{pre}{m.group(1)}"', svg)
    svg = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{pre}{m.group(1)})" if m.group(1) in ids else m.group(0), svg)
    return re.sub(r'href="#([^"]+)"', lambda m: f'href="#{pre}{m.group(1)}"' if m.group(1) in ids else m.group(0), svg)


def _colour(c, spec):
    if not c:
        return None
    return spec["brand"]["colors"].get(c, c)


def _layer_media(it: dict, key: str, spec: dict, media: dict | None, base: Path | None, out_dir: Path | None,
                 cls: str) -> str:
    """The picture of a background / overlay: looping clip frames, a recoloured inline SVG, or an <img>."""
    from .media import resolve
    clip = (media or {}).get(key)
    if clip:
        first = _url(Path(clip["dir"]) / "00001.jpg", out_dir)
        return f'<img class="{cls}" data-loop="{html.escape(key)}" src="{first}" alt="">'
    src = resolve(it["src"], base)
    col = _colour(it.get("color"), spec)
    if col and src.suffix.lower() == ".svg":
        try:
            if src.stat().st_size <= _SVG_INLINE_MAX:
                svg = re.sub(r"<\?xml[^>]*>|<!DOCTYPE[^>]*>", "", src.read_text(encoding="utf-8"))
                return f'<div class="{cls} svgc">{unique_ids(recolor_svg(svg, col))}</div>'
        except OSError:
            pass
    return f'<img class="{cls}" src="{_url(src, out_dir)}" alt="">'


def _background_html(bg: dict | None, key: str, spec: dict, media, base, out_dir) -> str:
    if not bg:
        return ""
    img = _layer_media(bg, key, spec, media, base, out_dir, "bgimg" + (" zoom" if bg.get("zoom") else ""))
    img = img.replace('class="bgimg', f'style="object-fit:{bg["fit"]}" class="bgimg', 1)
    tint = _colour(bg.get("tint"), spec)
    st = f'opacity:{bg["opacity"]:.2f}'
    if bg.get("blur"):
        st += f';filter:blur({bg["blur"] / 10:.2f}vw)'
    return (f'<div class="bgl" style="{st}">{img}'
            + (f'<div class="bgtint" style="background:{html.escape(tint)};opacity:{bg.get("tint_strength", 0.3):.2f}"></div>'
               if tint else "")
            + (f'<div class="bgdim" style="background:rgba(0,0,0,{bg["dim"]:.2f})"></div>' if bg.get("dim") else "")
            + "</div>")


def _overlays_html(ovs: list, owner: str, spec: dict, media, base, out_dir, layer: str) -> str:
    out = []
    for j, o in enumerate(ovs or []):
        if o["layer"] != layer:
            continue
        inner = _layer_media(o, f"{owner}#ov{j}", spec, media, base, out_dir, "ovimg")
        css = NATIVE_BLEND.get(o["blend"]) or PREVIEW_BLEND.get(o["blend"], "normal")
        xb = f' data-xblend="{o["blend"]}"' if o["blend"] in PREVIEW_BLEND else ""   # exact in the render (kadans.blend)
        out.append(f'<div class="ov {layer}"{xb} data-anim="{o["anim"]}" data-speed="{o["speed"]:.3f}" '
                   f'data-rot="{o["rotate"]:.1f}" data-op="{o["opacity"]:.3f}" style="left:{o["x"] * 100:.2f}%;'
                   f'top:{o["y"] * 100:.2f}%;width:{o["w"] * spec["w"]:.0f}px;mix-blend-mode:{css};'
                   f'opacity:{o["opacity"]:.3f}">{inner}</div>')
    return "".join(out)


WIDE_LOGO = 1.6          # wider than this (a word mark) = shown as it is, not shrunk inside the square tile


def _aspect_svg(svg: str) -> float:
    m = re.search(r'viewBox\s*=\s*["\']\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', svg)
    if not m:
        m = re.search(r'<svg[^>]*?\bwidth\s*=\s*["\']([\d.]+)[^>]*?\bheight\s*=\s*["\']([\d.]+)', svg)
    try:
        return float(m.group(1)) / float(m.group(2)) if m and float(m.group(2)) else 1.0
    except ValueError:
        return 1.0


def _aspect_bitmap(data: bytes) -> float:
    """PNG / JPEG / WebP width / height from the header (no imaging library)."""
    import struct
    try:
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", data[16:24])
            return w / h if h else 1.0
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            if data[12:16] == b"VP8X":
                w = int.from_bytes(data[24:27], "little") + 1
                h = int.from_bytes(data[27:30], "little") + 1
                return w / h
            return 1.0
        if data[:2] == b"\xff\xd8":
            i = 2
            while i + 9 < len(data):
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker, size = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
                if marker in (0xC0, 0xC1, 0xC2):
                    h, w = struct.unpack(">HH", data[i + 5:i + 9])
                    return w / h if h else 1.0
                i += 2 + size
    except (struct.error, IndexError):
        pass
    return 1.0


def _logo_html(path: str | None, base: Path | None, name: str) -> str:
    """Inline the brand logo (SVG inline, PNG / JPG as data URI). No file -> monogram of the brand name."""
    if path:
        p = Path(path)
        if not p.is_absolute() and base is not None:
            p = base / p
        try:
            if p.suffix.lower() == ".svg":
                svg = re.sub(r"<\?xml[^>]*>|<!DOCTYPE[^>]*>", "", p.read_text(encoding="utf-8"))
                cls = "logo-img wide" if _aspect_svg(svg) > WIDE_LOGO else "logo-img"
                return svg.replace("<svg", f'<svg class="{cls}"', 1)
            mime = {".png": "png", ".jpg": "jpeg", ".jpeg": "jpeg", ".webp": "webp"}.get(p.suffix.lower())
            if mime:
                data = p.read_bytes()
                b64 = base64.b64encode(data).decode()
                cls = "logo-img wide" if _aspect_bitmap(data) > WIDE_LOGO else "logo-img"
                return f'<img class="{cls}" src="data:image/{mime};base64,{b64}" alt="">'
        except OSError:
            pass
    letter = html.escape((re.sub(r"[^\w]", "", name) or "K")[0].upper())
    return f'<div class="mono">{letter}</div>'


def _fit(spec: dict, n: int, want: float, gap: float) -> float:
    """Width (px) of one of n boxes side by side: «want» u at most, never wider than 90 % of the frame."""
    u = min(spec["w"], spec["h"]) / 1080
    if spec["h"] > spec["w"]:
        return spec["w"] * 0.8
    return min(want * u, (spec["w"] * 0.9 - gap * u * (n - 1)) / max(1, n))


def _a(cls: str, fx: str, d: float, inner: str, extra: str = "") -> str:
    return f'<div class="{cls} a" data-fx="{fx}" data-d="{d:.2f}"{extra}>{inner}</div>'


def _url(path: Path, out_dir: Path | None) -> str:
    """Link from the composition page to a local file: relative when possible (the folder stays movable)."""
    path = Path(path)
    if out_dir is not None:
        try:
            return Path(os.path.relpath(path, out_dir)).as_posix()
        except ValueError:                              # another drive (Windows)
            pass
    return path.resolve().as_uri()


def _caption(sc: dict, d0: float = 0.4) -> str:
    if not (sc.get("title") or sc.get("subtitle")):
        return ""
    inner = (_a("h2 cap-t", "up", d0, mark(sc.get("title"))) if sc.get("title") else "") + \
            (_a("sub cap-s", "fade", d0 + 0.4, mark(sc.get("subtitle"))) if sc.get("subtitle") else "")
    pos = sc.get("caption", "bottom")
    strong = " strong" if sc.get("title_backdrop") else ""
    return f'<div class="shade {pos}{strong}"></div><div class="cap {pos}">{inner}</div>'


def _origin(sc: dict) -> str:
    """Orijin zoom nan (focus): kote zoom nan santre pou l pa koupe yon logo sou bo a."""
    f = sc.get("focus")
    return f'transform-origin:{f["x"] * 100:.1f}% {f["y"] * 100:.1f}%' if f else ""


def _backdrop(sc: dict, url: str) -> str:
    """Fon deye yon imaj 'contain' (olye bann nwa): kopi flou menm imaj la, oswa yon koule plen."""
    bd = sc.get("backdrop")
    if not bd or sc.get("fit") != "contain":
        return ""
    if bd == "blur":
        return f'<img class="media backdrop" src="{url}" style="object-fit:cover" alt="">'
    return f'<div class="media backdrop" style="background:{html.escape(bd)}"></div>'


def _media_extra(sc: dict) -> tuple[str, str, str]:
    """(klas anplis, style anplis, atribi data-cam) pou eleman medya a: camera / window / focus."""
    cam = sc.get("camera")
    cls = (" zoom" if sc.get("zoom") and not cam else "") + (" window" if sc.get("layout") == "window" else "")
    style = ("" if cam or not sc.get("focus") else ";" + _origin(sc))
    attr = f" data-cam='{html.escape(json.dumps(cam), quote=True)}'" if cam else ""
    return cls, style, attr


def _img_size(path) -> tuple[int, int] | None:
    """Dimansyon yon imaj (w, h) ak antet la sèlman - san okenn depandans (jpg/png/gif/webp/bmp)."""
    import struct
    try:
        with open(path, "rb") as f:
            head = f.read(32)
            if len(head) < 24:
                return None
            if head[1:4] == b"PNG":
                w, h = struct.unpack(">II", head[16:24]); return w, h
            if head[:6] in (b"GIF87a", b"GIF89a"):
                w, h = struct.unpack("<HH", head[6:10]); return w, h
            if head[:2] == b"BM":
                w, h = struct.unpack("<ii", head[18:26]); return abs(w), abs(h)
            if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
                tag = head[12:16]
                if tag == b"VP8 ":
                    w, h = struct.unpack("<HH", head[26:30]); return w & 0x3fff, h & 0x3fff
                if tag == b"VP8X":
                    return 1 + int.from_bytes(head[24:27], "little"), 1 + int.from_bytes(head[27:30], "little")
                if tag == b"VP8L":
                    n = int.from_bytes(head[21:25], "little")
                    return (n & 0x3fff) + 1, ((n >> 14) & 0x3fff) + 1
            if head[0] == 0xFF and head[1] == 0xD8:                 # JPEG: chèche makè SOF la
                f.seek(2)
                while True:
                    byte = f.read(1)
                    while byte and byte[0] != 0xFF:
                        byte = f.read(1)
                    while byte and byte[0] == 0xFF:
                        byte = f.read(1)
                    if not byte:
                        return None
                    m = byte[0]
                    if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                        f.read(3)
                        h, w = struct.unpack(">HH", f.read(4)); return w, h
                    ln = struct.unpack(">H", f.read(2))[0]
                    f.seek(ln - 2, 1)
    except Exception:                                    # noqa: BLE001
        pass
    return None


def _window_box(iw: int, ih: int, W: int, H: int, max_w: float = 0.84, max_h: float = 0.78):
    """Fenet santre sou RATIO imaj la (pa gen bann nwa). Retounen (left, top, width, height) an % kanva a."""
    ar = (iw / ih) if ih else (W / H)
    w = max_w * W
    h = w / ar
    if h > max_h * H:
        h = max_h * H; w = h * ar
    return 100 * (W - w) / 2 / W, 100 * (H - h) / 2 / H, 100 * w / W, 100 * h / H


def _window_style(sc: dict, src_path, spec: dict, fit: str):
    """layout:window → (fit=cover, style pozisyon). Fenet la pran fom imaj la, ranpli an cover (san bann nwa)."""
    if sc.get("layout") != "window":
        return fit, ""
    iw, ih = (_img_size(src_path) or (spec["w"], spec["h"])) if src_path else (spec["w"], spec["h"])
    l, tp, w, h = _window_box(iw, ih, spec["w"], spec["h"])
    return "cover", f";inset:auto;left:{l:.2f}%;top:{tp:.2f}%;width:{w:.2f}%;height:{h:.2f}%"


def _cards_html(sc: dict, url: str, spec: dict, src_path=None) -> str:
    """Kat koupe nan imaj la (background-crop) ki anime, pozisyone sou pwen `at`, aspek = zon crop la."""
    cards = sc.get("cards") or []
    if not cards:
        return ""
    W, H, parts = spec["w"], spec["h"], []
    iw, ih = (_img_size(src_path) or (0, 0)) if src_path else (0, 0)   # vrè fòm imaj la (pa ekran an)
    for c in cards:
        cx, cy, cw, ch = c["crop"]
        bx = (cx / (1 - cw) * 100) if cw < 1 else 0.0
        by = (cy / (1 - ch) * 100) if ch < 1 else 0.0
        bsx = (100 / cw) if cw > 0 else 100
        bsy = (100 / ch) if ch > 0 else 100
        data = html.escape(json.dumps({"at": c["at"], "from": c["from"], "rot": c["rotate"],
                                       "enter": c["enter"]}), quote=True)
        style = (f"background-image:url('{url}');background-size:{bsx:.1f}% {bsy:.1f}%;background-position:{bx:.1f}% {by:.1f}%;"
                 f"width:{c['width'] * 100:.2f}%;aspect-ratio:{cw * (iw or W):.1f}/{ch * (ih or H):.1f};"
                 f"left:{c['at'][0] * 100:.2f}%;top:{c['at'][1] * 100:.2f}%")
        pill = ""
        if c["pill"]:
            ic = html.escape(icon_glyph(c["icon"])) + " " if c["icon"] else ""
            pill = f'<div class="pill">{ic}{html.escape(c["pill"])}</div>'
        parts.append(f'<div class="card3d" data-card="{data}" style="{style}">{pill}</div>')
    return "".join(parts)


def _scene_body(sc: dict, spec: dict, logo: str, media: dict | None = None, base: Path | None = None,
                out_dir: Path | None = None, tle: dict | None = None) -> str:
    t, out = sc["type"], []
    D = delays(sc, tle)
    if t in ("video", "image"):
        fit = sc.get("fit", "cover")
        cls, style, cam = _media_extra(sc)
        if t == "video":
            clip = (media or {}).get(sc["id"])
            if clip:
                first = _url(Path(clip["dir"]) / "00001.jpg", out_dir)
                out.append(_backdrop(sc, first))
                _sz = Path(clip["dir"]) / "00001.jpg"
                fit2, wstyle = _window_style(sc, _sz, spec, fit)
                out.append(f'<img class="media{cls}" data-clip="{sc["id"]}" data-speed="{float(sc.get("speed") or 1):.3f}" src="{first}" '
                           f'style="object-fit:{fit2}{style}{wstyle}"{cam} alt="">')
                out.append(_cards_html(sc, first, spec, _sz))
            else:                                       # clip not prepared yet (spec preview): name it
                out.append(f'<div class="media missing">🎬 {html.escape(Path(sc["src"]).name)}</div>')
        else:
            src = Path(sc["src"])
            if not src.is_absolute() and base is not None:
                src = base / src
            url = _url(src, out_dir)
            out.append(_backdrop(sc, url))
            fit2, wstyle = _window_style(sc, src, spec, fit)
            out.append(f'<img class="media{cls}" src="{url}" style="object-fit:{fit2}{style}{wstyle}"{cam} alt="">')
            out.append(_cards_html(sc, url, spec, src))
        out.append(_caption(sc))
        return "\n".join(out)
    title, sub = sc.get("title"), sc.get("subtitle")
    brand = spec["brand"]["name"]
    if t == "hook":
        out.append(_a("h1", "up", 0, mark(title)))
        if sub:
            out.append(_a("sub", "fade", 0.6, mark(sub)))
    elif t == "text":
        out.append(_a("h2", "up", 0, mark(title)))
        if sub:
            out.append(_a("sub", "fade", 0.5, mark(sub)))
    elif t == "logo":
        out.append(_a("logo", "zoom", 0, logo))
        if brand:
            out.append(_a("brand", "up", 0.35, mark(brand)))
        if sc.get("tagline") or sub:
            out.append(_a("tagline", "fade", 0.8, mark(sc.get("tagline") or sub)))
    elif t == "features":
        out.append(_a("h2", "up", 0, mark(title)))
        cw = _fit(spec, len(sc["items"]), 420, 36)
        cards = "".join(_a("card", "pop", D["items"][i],
                           f'<div class="ic">{html.escape(icon_glyph(it.get("icon")))}</div>'
                           f'<div class="t">{mark(it.get("title"))}</div>'
                           + (f'<div class="s">{mark(it.get("text"))}</div>' if it.get("text") else ""),
                           f' style="width:{cw:.0f}px"')
                        for i, it in enumerate(sc["items"]))
        out.append(f'<div class="row cards">{cards}</div>')
    elif t == "list":
        out.append(_a("h2", "up", 0, mark(title)))
        checks = "".join(_a("check", "pop", D["items"][i], f"<span>✓</span>{mark(x)}")
                         for i, x in enumerate(sc["items"]))
        out.append(f'<div class="row checks">{checks}</div>')
    elif t == "stat":
        if title:
            out.append(_a("h2", "up", 0, mark(title)))
        u = min(spec["w"], spec["h"]) / 1080
        sw = _fit(spec, len(sc["items"]), 330, 36)
        longest = max(len(str(it.get("value"))) for it in sc["items"])
        vs = min(120 * u, (sw - 50 * u) / (0.62 * max(1, longest)))          # the number always fits on one line
        stats = "".join(_a("stat", "pop", D["items"][i],
                           f'<div class="v" style="font-size:{vs:.0f}px" data-count="{html.escape(str(it.get("value")))}">'
                           f'{html.escape(str(it.get("value")))}</div><div class="l">{mark(it.get("label"))}</div>',
                           f' style="width:{sw:.0f}px"')
                        for i, it in enumerate(sc["items"]))
        out.append(f'<div class="row stats">{stats}</div>')
    elif t == "code":
        if title:
            out.append(_a("h2", "up", 0, mark(title)))
        d, lines = 0.5, []
        for ln in sc["lines"]:
            ln_len = 0.35 + len(ln) / 45
            lines.append(f'<div class="type" data-d="{d:.2f}" data-len="{ln_len:.2f}">'
                         f'{html.escape(ln).replace("  ", "&nbsp;&nbsp;") or "&nbsp;"}</div>')
            d += ln_len + 0.1
        dots = '<div class="dots"><i style="background:#f14c6c"></i><i style="background:#e5b454"></i>' \
               '<i style="background:#4ec9a0"></i></div>'
        out.append(_a("code", "up", 0.2, dots + "".join(lines)))
        if sc.get("chips"):
            chips = "".join(_a("chip", "pop", D["chips"][i], mark(chip_text(c))) for i, c in enumerate(sc["chips"]))
            out.append(f'<div class="row chips">{chips}</div>')
    elif t == "compare":
        if title:
            out.append(_a("h2", "up", 0, mark(title)))
        cols = []
        for side, fx, sym, d0 in (("left", "left", "✕", D["cols"][0]), ("right", "right", "✓", D["cols"][1])):
            c = sc.get(side) or {}
            items = "".join(f'<div class="ci"><span>{sym}</span>{mark(x)}</div>' for x in c.get("items") or [])
            cols.append(_a(f"col {side}", fx, d0, f'<div class="ct">{mark(c.get("title"))}</div>{items}',
                           f' style="width:{_fit(spec, 2, 520, 44):.0f}px"'))
        out.append(f'<div class="row compare">{"".join(cols)}</div>')
    elif t == "cta":
        out.append(_a("logo small", "zoom", 0, logo))
        if brand:
            out.append(_a("brand small", "up", 0.25, mark(brand)))
        out.append(_a("cta", "pop", 0.9, mark(title)))
        if sub:
            out.append(_a("sub", "fade", 0.6, mark(sub)))
    elif t == "chart":
        import json as _json
        if title:
            out.append(_a("h2", "up", 0, mark(title)))
        def _cnum(x):
            try:
                return float(str(x).replace(",", "").replace("%", "").strip())
            except (TypeError, ValueError):
                return 0.0
        labels = [str(it.get("label", "")) for it in sc["items"]]
        data = [_cnum(it.get("value")) for it in sc["items"]]
        pal = ["#8b5cf6", "#21a366", "#2e8bff", "#ff8a3d", "#e0457b", "#17b3b0", "#b48a00", "#8a63d2"]
        kind = sc["chart"]
        cjs = "line" if kind == "area" else kind
        ds = {"label": title or "", "data": data,
              "backgroundColor": (pal[:len(data)] if kind in ("pie", "doughnut") else pal[0]),
              "borderColor": pal[0], "borderWidth": 2, "fill": (kind == "area"), "tension": 0.3}
        grid = {"color": "rgba(255,255,255,0.08)"}
        scales = {} if kind in ("pie", "doughnut") else {
            "x": {"ticks": {"color": "#b9addb"}, "grid": grid},
            "y": {"ticks": {"color": "#b9addb"}, "grid": grid}}
        cfg = {"type": cjs, "data": {"labels": labels, "datasets": [ds]},
               "options": {"responsive": False, "animation": {"duration": 900},
                           "plugins": {"legend": {"display": kind in ("pie", "doughnut"),
                                                  "labels": {"color": "#f3eefe"}}}, "scales": scales}}
        cid = "chart_" + re.sub(r"\W", "", sc["id"])
        W = int(spec["w"] * 0.6); H = int(spec["h"] * 0.5)
        out.append(_a("chartbox", "pop", 0.3, '<canvas id="' + cid + '" width="' + str(W) + '" height="' + str(H) + '"></canvas>',
                      " style=\"width:" + str(W) + "px;height:" + str(H) + "px\""))
        out.append('<script>(function(){var c=document.getElementById("' + cid +
                   '");if(c&&window.Chart){new Chart(c.getContext("2d"),' + _json.dumps(cfg) + ');}})();</script>')
    elif t == "social":
        if sc.get("handle"):
            out.append(_a("shandle", "up", 0, mark(sc["handle"]), " style=\"color:#b9addb;margin-bottom:.4em\""))
        if title:
            out.append(_a("h2", "up", 0, mark(title)))
        LB = {"like": "♥ Like", "subscribe": "▶ Subscribe", "follow": "+ Follow",
              "share": "↗ Share", "comment": "Comment", "bell": "🔔 Notifications"}
        CL = {"like": "#e0457b", "subscribe": "#ff3b30", "follow": "#8b5cf6", "share": "#2e8bff",
              "comment": "#17b3b0", "bell": "#b48a00"}
        btns = "".join(_a("sbtn", "pop", 0.3 + 0.18 * i,
                          "<span>" + html.escape(LB.get(a, a)) + "</span>",
                          " style=\"background:" + CL.get(a, "#8b5cf6") + ";color:#fff;padding:.5em 1.1em;"
                          "border-radius:999px;font-weight:700;margin:.3em;display:inline-block;box-shadow:0 .2em .8em #0006\"")
                       for i, a in enumerate(sc["actions"]))
        out.append('<div class="row social" style="display:flex;flex-wrap:wrap;justify-content:center;align-items:center">' + btns + '</div>')
    elif t == "lottie":
        import json as _json
        if title:
            out.append(_a("h2", "up", 0, mark(title)))
        if sub:
            out.append(_a("sub", "fade", 0.3, mark(sub)))
        src = sc.get("src", "")
        lottie_json_raw = None
        if base is not None and src:
            p = Path(src) if Path(src).is_absolute() else (base / src)
            if p.is_file() and p.suffix.lower() == ".json":
                try:
                    lottie_json_raw = p.read_text(encoding="utf-8")
                except OSError:
                    pass
        lid = "lottie_" + re.sub(r"\W", "", sc["id"])
        fit = sc.get("fit", "contain")
        loop = bool(sc.get("loop", False))
        speed = float(sc.get("speed", 1.0))
        W = int(spec["w"] * 0.7)
        H = int(spec["h"] * 0.6)
        out.append(_a("lottiebox", "pop", 0.2,
                      f'<div id="{lid}" style="width:{W}px;height:{H}px;margin:auto;display:flex;align-items:center;justify-content:center"></div>'))
        load_arg = f'animationData: {lottie_json_raw}' if lottie_json_raw else f'path: "{src}"'
        out.append(f'<script>(function(){{'
                   f'var c=document.getElementById("{lid}");'
                   f'if(c&&window.lottie){{'
                   f'var anim=lottie.loadAnimation({{container:c,renderer:"svg",loop:{"true" if loop else "false"},autoplay:false,{load_arg}}});'
                   f'window.__lottieAnims=window.__lottieAnims||{{}};'
                   f'window.__lottieAnims["{sc["id"]}"]=anim;'
                   f'anim.setSpeed({speed});'
                   f'}}}}();</script>')
    elif t == "html":
        raw = sc.get("html") or ""
        src_dir = ""
        if not raw and sc.get("src"):
            src = Path(sc["src"])
            src_dir = src.parent.as_posix()
            if not src.is_absolute() and base is not None:
                src = base / src
            try:
                raw = src.read_text(encoding="utf-8")
            except OSError:
                raw = '<div class="media missing">[HTML ' + html.escape(sc["src"]) + ']</div>'
        if "<body" in raw.lower():
            m_body = re.search(r'<body[^>]*>(.*?)</body>', raw, re.DOTALL | re.IGNORECASE)
            styles_head = "\n".join(re.findall(r'<style[^>]*>.*?</style>', raw, re.DOTALL | re.IGNORECASE))
            scripts_head = "\n".join(re.findall(r'<script[^>]*>.*?</script>', raw, re.DOTALL | re.IGNORECASE))
            body_inner = m_body.group(1) if m_body else raw
            raw = f"{styles_head}\n{body_inner}\n{scripts_head}"
        if src_dir and src_dir != ".":
            def _sub_rel(m):
                a, q, v = m.group(1), m.group(2), m.group(3)
                if v.startswith(("http://", "https://", "data:", "/", "#", "mailto:", "blob:")):
                    return m.group(0)
                return f'{a}={q}{src_dir.rstrip("/")}/{v}{q}'
            raw = re.sub(r'\b(src|href)=([\'"])(.*?)\2', _sub_rel, raw, flags=re.IGNORECASE)
        out.append('<div class="htmlwrap" style="position:absolute;inset:0;width:100%;height:100%">'
                   + _html_reveals(raw, tle) + '</div>')
    elif t == "stickman":
        from .stickman import build_stickman_scene_body
        out.append(build_stickman_scene_body(sc, spec, D, mark))
    if sc.get("stickman") and t != "stickman":
        from .stickman import generate_stickman_rig_svg
        cfg = sc["stickman"] if isinstance(sc["stickman"], dict) else {}
        out.append(generate_stickman_rig_svg(
            name=cfg.get("name") or "Stickman",
            color=cfg.get("color"),
            palette=cfg.get("palette", "cyan"),
            accessory=cfg.get("accessory") or cfg.get("prop"),
            scale=float(cfg.get("scale", 1.0)),
            x=float(cfg.get("x", spec.get("w", 1920) * 0.15)),
            y=float(cfg.get("y", spec.get("h", 1080) * 0.45)),
            glow=bool(cfg.get("glow", True)),
        ))
    return "\n".join(out)


def font_faces(spec: dict, base: Path | None, out_dir: Path | None) -> str:
    """@font-face for the brand fonts found on the PC (and in the project's fonts/ folder): the render uses exactly
    those files, never a fallback."""
    from . import fonts as F
    extra = [base / "fonts"] if base is not None and (base / "fonts").is_dir() else []
    css, seen = [], set()
    for fam in (spec["brand"]["font"], spec["brand"]["font_title"], spec["brand"]["font_code"]):
        if fam.lower() in seen:
            continue
        seen.add(fam.lower())
        try:
            faces = F.find(fam, extra)
        except OSError:
            faces = []
        if faces:
            css.append(F.face_css(fam, faces, lambda p: _url(p, out_dir)))
    return "\n".join(x for x in css if x)


def _css(spec: dict) -> str:
    w, h = spec["w"], spec["h"]
    c, font = spec["brand"]["colors"], spec["brand"]["font"]
    ft, fc = spec["brand"].get("font_title") or font, spec["brand"].get("font_code") or "Cascadia Code"
    u = min(w, h) / 1080

    def px(n: float) -> str:
        return f"{n * u:.1f}px"
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#000;overflow:hidden}}
#stage{{position:absolute;left:0;top:0;width:{w}px;height:{h}px;overflow:hidden;background:{c['bg']};color:{c['text']};
 font-family:"{font}","Segoe UI",system-ui,"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif;transform-origin:0 0}}
.orb{{position:absolute;border-radius:50%;opacity:.5;will-change:transform}}
#grid{{position:absolute;left:0;right:0;top:-{px(80)};height:calc(100% + {px(80)});will-change:transform;opacity:.09;background-image:linear-gradient({c['primary']} 1px,transparent 1px),
 linear-gradient(90deg,{c['primary']} 1px,transparent 1px);background-size:{px(80)} {px(80)}}}
.scene{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
 text-align:center;opacity:0;padding:0 {px(70)}}}
.a{{will-change:transform,opacity}}
.h1,.h2,.brand,.cta,.stat .v,.card .t,.check,.col .ct,.chip,#capt{{font-family:"{ft}","{font}","Segoe UI",system-ui,
 "Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif}}
.h1{{font-size:{px(96)};font-weight:800;letter-spacing:{px(-2)};line-height:1.08;max-width:{w * 0.9:.0f}px}}
.h2{{font-size:{px(64)};font-weight:800;letter-spacing:{px(-1)};line-height:1.12;max-width:{w * 0.9:.0f}px}}
.hl{{display:inline-block;background:linear-gradient(120deg,{c['text']} -40%,{c['primary']} 45%,{c['accent']});-webkit-background-clip:text;
 background-clip:text;color:transparent;padding:0 .08em .06em;margin:0 -.08em -.06em}}
.sub{{font-size:{px(36)};color:{c['muted']};margin-top:{px(22)};font-weight:500;max-width:{w * 0.85:.0f}px;line-height:1.35}}
.logo{{width:{px(300)};height:{px(300)};border-radius:{px(70)};background:rgba(255,255,255,.04);display:flex;
 align-items:center;justify-content:center;box-shadow:0 0 {px(120)} {c['primary']}99}}
.logo.small{{width:{px(210)};height:{px(210)};border-radius:{px(50)}}}
.logo-img{{width:78%;height:78%;object-fit:contain}}
.logo:has(> .wide){{width:auto;height:{px(190)};max-width:{w * 0.82:.0f}px;padding:0 {px(10)};background:none;box-shadow:none;
 border-radius:0}} .logo.small:has(> .wide){{height:{px(130)}}}
.logo-img.wide{{width:auto;height:100%;max-width:100%;filter:drop-shadow(0 0 {px(40)} {c['primary']}88)}}
.mono{{font-size:{px(170)};font-weight:900;color:{c['primary']}}}
.brand{{font-size:{px(150)};font-weight:900;letter-spacing:{px(6)};margin-top:{px(30)};line-height:1}}
.brand.small{{font-size:{px(110)};margin-top:{px(24)}}}
.brand .hl{{background:none;color:{c['primary']}}}
.tagline{{font-size:{px(38)};color:{c['primary']};letter-spacing:{px(3)};margin-top:{px(16)}}}
.row{{display:flex;justify-content:center;align-items:stretch;gap:{px(36)};margin-top:{px(48)}}}
.card{{width:{px(420)};min-height:{px(320)};border-radius:{px(28)};padding:{px(26)};background:linear-gradient(160deg,
 rgba(255,255,255,.07),rgba(255,255,255,.02));border:{px(2)} solid rgba(255,255,255,.10);display:flex;flex-direction:column;
 align-items:center;justify-content:center;box-shadow:0 {px(30)} {px(70)} rgba(0,0,0,.45)}}
.card .ic{{font-size:{px(110)};line-height:1.1}} .card .t{{font-size:{px(38)};font-weight:800;margin-top:{px(14)}}}
.card .s{{font-size:{px(25)};color:{c['muted']};margin-top:{px(8)}}}
.checks{{gap:{px(60)}}} .check{{font-size:{px(48)};font-weight:800}} .check span{{color:#34d399;margin-right:{px(14)}}}
.stat{{padding:{px(26)} {px(34)};border-radius:{px(28)};background:rgba(255,255,255,.05);
 border:{px(2)} solid rgba(255,255,255,.10)}}
.stat .v{{font-weight:900;line-height:1.05;color:{c['primary']};white-space:nowrap}}
.stat .l{{font-size:{px(30)};color:{c['muted']};margin-top:{px(8)}}}
.code{{width:{min(w * 0.9, 1100 * u * 1.0):.0f}px;margin-top:{px(36)};text-align:left;background:rgba(0,0,0,.35);
 border:{px(2)} solid rgba(255,255,255,.10);border-radius:{px(22)};padding:{px(30)} {px(40)};
 font-family:"{fc}",Consolas,"Cascadia Code",monospace;font-size:{px(30)};line-height:1.6;box-shadow:0 {px(40)} {px(90)} rgba(0,0,0,.5);
 white-space:pre-wrap;word-break:break-word}}
.code .dots{{margin-bottom:{px(14)}}} .code .dots i{{display:inline-block;width:{px(16)};height:{px(16)};border-radius:50%;
 margin-right:{px(10)}}}
.chip{{padding:{px(16)} {px(34)};border-radius:{px(40)};font-size:{px(32)};font-weight:700;background:{c['primary']}2e;
 border:{px(2)} solid {c['primary']}73}}
.chips{{gap:{px(22)};margin-top:{px(34)}}}
.compare{{gap:{px(44)}}}
.col{{width:{px(520)};padding:{px(34)};border-radius:{px(28)};text-align:left;background:rgba(255,255,255,.04);
 border:{px(2)} solid rgba(255,255,255,.08)}}
.col.right{{background:{c['primary']}26;border-color:{c['primary']};box-shadow:0 0 {px(80)} {c['primary']}55}}
.col .ct{{font-size:{px(40)};font-weight:800;margin-bottom:{px(18)}}} .col.left .ct{{color:{c['muted']}}}
.ci{{font-size:{px(30)};margin-top:{px(12)}}} .col.left .ci{{color:{c['muted']}}} .col.left .ci span{{color:#f87171}}
.col.right .ci span{{color:#34d399}} .ci span{{margin-right:{px(12)};font-weight:800}}
.cta{{margin-top:{px(44)};padding:{px(24)} {px(64)};border-radius:{px(60)};font-size:{px(42)};font-weight:800;color:#fff;
 background:linear-gradient(120deg,{c['primary']},{c['accent']});box-shadow:0 {px(20)} {px(60)} {c['primary']}88}}
.cta .hl{{background:none;color:#fff}}
{_caption_css(spec, px)}
#credit{{position:absolute;right:{px(36)};bottom:{px(30)};display:flex;align-items:center;gap:{px(10)};opacity:0;
 font-size:{px(22)};color:{c['muted']};letter-spacing:{px(.5)}}}
#credit svg{{width:{px(34)};height:{px(34)}}} #credit b{{color:{c['text']};font-weight:700}}
#kbar{{display:none !important;position:fixed;left:0;right:0;bottom:0;height:0;visibility:hidden;pointer-events:none}}
#kplay_center{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:{px(140)};height:{px(140)};border-radius:50%;background:rgba(18,13,31,0.78);border:{px(4)} solid {c['primary']};box-shadow:0 0 {px(50)} {c['primary']}99,0 {px(16)} {px(40)} rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:99;transition:transform 0.2s cubic-bezier(0.34,1.56,0.64,1),opacity 0.25s ease,background 0.2s ease;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);pointer-events:auto}}
#kplay_center:hover{{transform:translate(-50%,-50%) scale(1.12);background:rgba(139,92,246,0.45);box-shadow:0 0 {px(70)} {c['primary']},0 {px(20)} {px(50)} rgba(0,0,0,0.85)}}
#kplay_center svg{{width:{px(60)};height:{px(60)};margin-left:{px(8)};fill:#ffffff;filter:drop-shadow(0 {px(4)} {px(12)} rgba(0,0,0,0.6))}}
#kplay_center.playing{{opacity:0;pointer-events:none;transform:translate(-50%,-50%) scale(0.85)}}
body.is-render #kplay_center,
body[data-render="true"] #kplay_center,
.is-render #kplay_center,
#stage.is-render #kplay_center,
body.in-editor #kplay_center,
body[data-ineditor="true"] #kplay_center,
.in-editor #kplay_center,
#stage.ineditor #kplay_center,
.ineditor #kplay_center{{display:none !important;visibility:hidden !important;opacity:0 !important;pointer-events:none !important}}
#bar{{position:absolute;left:0;bottom:0;height:{px(8)};background:linear-gradient(90deg,{c['primary']},{c['accent']})}}
#subs{{position:absolute;left:{px(60)};right:{px(60)};text-align:center;font-size:{px(44)};font-weight:800;
 color:#fff;line-height:1.25;z-index:7;display:none;pointer-events:none}}
#subs.bottom{{bottom:{px(120)}}} #subs.top{{top:{px(110)}}} #subs.middle{{top:50%;transform:translateY(-50%)}}
#subs .sbx{{display:inline-block;padding:{px(6)} {px(20)};border-radius:{px(10)};background:#000a;
 text-shadow:0 {px(2)} {px(8)} #000c}}
.sc-video,.sc-image{{padding:0}}
.media{{position:absolute;inset:0;width:100%;height:100%;background:#000}}
.media.missing{{display:flex;align-items:center;justify-content:center;font-size:{px(40)};color:{c['muted']};
 background:repeating-linear-gradient(45deg,rgba(255,255,255,.03) 0 {px(30)},transparent {px(30)} {px(60)})}}
.media.backdrop{{filter:blur(2.6vw) brightness(.45);transform:scale(1.08);z-index:0}}

.media.backdrop ~ .media{{background:transparent}}   /* imaj contain devan an: kite backdrop flou a parèt (pa bann nwa) */
.media.window{{border-radius:{px(28)};overflow:hidden;box-shadow:0 {px(30)} {px(90)} rgba(0,0,0,.6);z-index:1}}
.card3d{{position:absolute;transform:translate(-50%,-50%);border-radius:{px(18)};overflow:hidden;background-repeat:no-repeat;
 box-shadow:0 {px(18)} {px(50)} rgba(0,0,0,.55);border:{px(2)} solid rgba(255,255,255,.16);will-change:transform,opacity;z-index:3}}
.card3d .pill{{position:absolute;left:{px(12)};bottom:{px(12)};padding:{px(6)} {px(16)};border-radius:{px(40)};
 color:#fff;font-weight:700;font-size:{px(26)};background:linear-gradient(120deg,{c['primary']},{c['accent']})}}
.shade{{position:absolute;left:0;right:0;height:55%;pointer-events:none}}
.shade.strong{{height:70%}}
.shade.strong.bottom{{background:linear-gradient(transparent,rgba(0,0,0,.94))}}
.shade.strong.top{{background:linear-gradient(rgba(0,0,0,.94),transparent)}}
.shade.bottom{{bottom:0;background:linear-gradient(transparent,rgba(0,0,0,.78))}}
.shade.top{{top:0;background:linear-gradient(rgba(0,0,0,.78),transparent)}}
.shade.center{{top:0;height:100%;background:rgba(0,0,0,.38)}}
.cap{{position:absolute;left:{px(70)};right:{px(70)};display:flex;flex-direction:column;align-items:center}}
.cap.bottom{{bottom:{px(90)}}} .cap.top{{top:{px(90)}}} .cap.center{{top:50%;transform:translateY(-50%)}}
.cap .h2{{text-shadow:0 {px(4)} {px(24)} rgba(0,0,0,.6)}} .cap .sub{{color:#e8e3f5}}
.bgl,#stagebg,#stageback,#stagefront{{position:absolute;inset:0;pointer-events:none}}
.bgl{{z-index:0;overflow:hidden;isolation:isolate}} .bgimg{{position:absolute;inset:0;width:100%;height:100%;will-change:transform}}
.bgimg.svgc svg{{width:100%;height:100%}} .bgtint{{position:absolute;inset:0;mix-blend-mode:color}}
.bgdim{{position:absolute;inset:0}}
.ov{{position:absolute;pointer-events:none;transform:translate(-50%,-50%);will-change:transform,opacity}} .ov.back{{z-index:1}} .ov.front{{z-index:4}}
.ovimg{{display:block;width:100%;height:auto}} .ovimg.svgc svg{{display:block;width:100%;height:auto}}
.scene>.a,.scene>.row,.scene>.cap,.scene>.shade{{z-index:2}} .scene>.a,.scene>.row{{position:relative}}
#stagefront{{z-index:6}}
#stagetracks{{position:absolute;inset:0;z-index:5;pointer-events:none}}
#stagetracks .tclip{{display:none;max-width:100%}}
.portrait .row{{flex-direction:column;align-items:center;gap:{px(26)};margin-top:{px(40)}}}
.portrait .card{{min-height:0;flex-direction:row;justify-content:flex-start;gap:{px(26)};text-align:left}}
.portrait .card .ic{{font-size:{px(80)}}} .portrait .card .t{{margin-top:0}}
.portrait .h1{{font-size:{px(88)}}}
"""


_JS = r"""
const K = window.__kadans, RENDER = location.hash.indexOf("render") >= 0 || /[?&]render\b/.test(location.search);
var INEDITOR = (!RENDER && (typeof window !== "undefined" && (window.parent !== window || location.hash.indexOf("ineditor") >= 0 || /[?&]ineditor\b/.test(location.search))));
window.INEDITOR = INEDITOR;
if (RENDER) {
  try {
    document.documentElement.classList.add("is-render");
    document.body.classList.add("is-render");
    document.body.setAttribute("data-render", "true");
    const kpc = document.getElementById("kplay_center");
    if (kpc) { kpc.style.display = "none"; kpc.remove(); }
  } catch (e) {}
}
if (INEDITOR) {
  try {
    document.documentElement.classList.add("in-editor");
    document.body.classList.add("in-editor");
    document.body.setAttribute("data-ineditor", "true");
    const kpc = document.getElementById("kplay_center");
    if (kpc) { kpc.style.display = "none"; }
  } catch (e) {}
}
let playing = false;
let VT = 0;                                          // the video clock (seconds) - the ONLY time source
if (RENDER) {                                        // nothing may depend on the real clock while rendering
  const t0 = Date.now();
  performance.now = () => VT * 1000;
  Date.now = () => t0 + VT * 1000;
  window.requestAnimationFrame = cb => setTimeout(() => cb(VT * 1000), 0);
}
const pad5 = n => String(n).padStart(5, "0");
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const easeOut = p => 1 - Math.pow(1 - p, 3);
const back = p => { const c = 1.70158; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
const easeK = (p, k) => k === "linear" ? p : k === "out" ? easeOut(p) : k === "punch" ? 1 - Math.pow(1 - p, 5) : p * p * (3 - 2 * p);
const dirVec = d => d === "left" ? [-1, 0] : d === "right" ? [1, 0] : d === "up" ? [0, -1] : d === "down" ? [0, 1] : [0, 0];
function cardAt(el, c, loc, dur) {                   // kat koupe: antre (back) soti direksyon, flote, soti nan fen
  const t0 = c.enter || 0, inp = clamp((loc - t0) / 0.55, 0, 1), outp = clamp((loc - (dur - 0.4)) / 0.4, 0, 1);
  const e = back(inp), v = dirVec(c.from); let k = 0.6 + 0.4 * e, o = inp;
  let dx = (1 - e) * v[0] * K.w * 0.4, dy = (1 - e) * v[1] * K.h * 0.4;
  if (outp > 0) { k *= 1 - 0.3 * outp; o *= 1 - outp; dy -= outp * K.h * 0.05; }
  dy += Math.sin((loc - t0) * 1.4) * K.h * 0.01;     // flotman dous
  css(el, "transform", `translate(-50%,-50%) translate(${dx.toFixed(1)}px,${dy.toFixed(1)}px) rotate(${(c.rot * (0.3 + 0.7 * e)).toFixed(2)}deg) scale(${k.toFixed(3)})`);
  css(el, "opacity", o.toFixed(3));
}
const typed = new Map();
document.querySelectorAll(".type").forEach(el => typed.set(el, el.innerHTML));
function typeAt(el, p) {
  const src = typed.get(el); let out = "", shown = 0;
  const plain = src.replace(/<[^>]+>/g, "").replace(/&[a-z]+;/g, "_").length, want = Math.floor(plain * p);
  for (let i = 0; i < src.length; i++) {
    if (src[i] === "<") { const j = src.indexOf(">", i); out += src.slice(i, j + 1); i = j; continue; }
    if (src[i] === "&") { const j = src.indexOf(";", i); if (shown < want) { out += src.slice(i, j + 1); shown++; } i = j; continue; }
    if (shown < want) { out += src[i]; shown++; }
  }
  const html = out + (p > 0 && p < 1 ? '<span style="opacity:.8">\u258c</span>' : "");
  if (el.__html !== html) { el.__html = html; el.innerHTML = html; }
}
function countAt(el, p) {
  const raw = el.dataset.count, m = raw.match(/^(\D*)(\d[\d\s.,]*\d|\d)(.*)$/);
  let txt = raw;
  if (m && p < 1) { const n = parseInt(m[2].replace(/[\s.,]/g, ""), 10);
    txt = m[1] + Math.round(n * easeOut(p)).toLocaleString("fr-FR") + m[3]; }
  if (el.textContent !== txt) el.textContent = txt;
}
// ---- RIG: pèsonaj cut-out Design ([data-rig] > [data-bone]) mache, kouri, chita… (motion.py: K.rigm + rigFrame)
const MI = [1, 0, 0, 1, 0, 0];
function mMul(A, B) { return [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1], A[0] * B[2] + A[2] * B[3],
  A[1] * B[2] + A[3] * B[3], A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]]; }
function mInv(A) { const d = (A[0] * A[3] - A[1] * A[2]) || 1e-12;
  return [A[3] / d, -A[1] / d, -A[2] / d, A[0] / d, (A[2] * A[5] - A[3] * A[4]) / d, (A[1] * A[4] - A[0] * A[5]) / d]; }
function mRot(deg, px, py) { const r = deg * Math.PI / 180, c = Math.cos(r), s = Math.sin(r);
  return [c, s, -s, c, px - c * px + s * py, py - s * px - c * py]; }
function mBox(w, h, rot, fx, fy) {                  // transfòmasyon pwòp eleman Design lan (flip + vire otou mitan)
  let m = [1, 0, 0, 1, w / 2, h / 2];
  m = mMul(m, mRot(+rot || 0, 0, 0)); m = mMul(m, [fx || 1, 0, 0, fy || 1, 0, 0]);
  return mMul(m, [1, 0, 0, 1, -w / 2, -h / 2]);
}
const mCss = A => "matrix(" + A.map(v => (Math.abs(v) < 1e-9 ? 0 : v).toFixed(5)).join(",") + ")";
const boxCss = (w, h, rot, fx, fy) => ` translate(${w / 2}px,${h / 2}px) rotate(${+rot || 0}deg) scale(${fx || 1},${fy || 1}) translate(${-w / 2}px,${-h / 2}px)`;
function rigChain(by, ang) {                        // M(zo) = M(paran) · R(zo): pitit la vire, paran yo pote l
  const memo = {};
  const f = id => { if (memo[id]) return memo[id]; const b = by[id]; if (!b) return MI;
    const R = mRot(ang(b), b.p[0], b.p[1]); return (memo[id] = b.parent && by[b.parent] ? mMul(f(b.parent), R) : R); };
  return f;
}
function rigInit(el) {
  let def; try { def = JSON.parse(el.dataset.rigdef); } catch (e) { return null; }
  const by = {}; for (const b of def.bones) by[b.id] = b;
  const curF = rigChain(by, b => +b.a || 0), curInv = {};
  for (const b of def.bones) curInv[b.id] = mInv(curF(b.id));
  const parts = [];
  for (const p of $$(el, "[data-bone]")) {
    let pt; try { pt = JSON.parse(p.dataset.pt); } catch (e) { continue; }
    const E = mBox(pt.w, pt.h, pt.rot, pt.fx, pt.fy), PE = mMul(pt.P, E);
    const cb = [[0, 0], [pt.w, 0], [0, pt.h], [pt.w, pt.h]].map(c => [PE[0] * c[0] + PE[2] * c[1] + PE[4], PE[1] * c[0] + PE[3] * c[1] + PE[5]]);
    p.style.transformOrigin = "0 0";
    parts.push({ el: p, bone: p.dataset.bone, P: pt.P, Pinv: mInv(pt.P), E: boxCss(pt.w, pt.h, pt.rot, pt.fx, pt.fy), cb, D: MI });
  }
  for (const P of parts) {                          // pati anndan yon lòt pati: transfòmasyon paran an deja aplike
    const a = P.el.parentElement && P.el.parentElement.closest("[data-bone]");
    P.anc = a && el.contains(a) ? parts.find(x => x.el === a) || null : null;
  }
  const low0 = Math.max(...parts.map(P => Math.max(...P.cb.map(c => c[1]))), -1e9);
  const bx = def.box || [0, 0, 0, 1, 1];
  el.style.transformOrigin = "0 0";
  const legs = def.bones.some(b => /^(foot|shin|thigh)_/.test(b.role || ""));
  return { el, def, by, curInv, parts, low0, legs, cx: bx[0] / 2, E: boxCss(bx[0], bx[1], bx[2], bx[3], bx[4]), segs: null, ch: null };
}
function rigApply(R, ch, loc) {
  if (R.ch !== ch) { R.segs = rigPlan(ch, R.def.ground); R.ch = ch; }
  const F = rigFrame(K.rigm, ch, loc, R.def.ground, R.def.h, R.segs);
  const own = b => (b.role && b.role in F.pose) ? F.pose[b.role] : (+b.a || 0);
  const byRole = {}; for (const b of R.def.bones) if (b.role) byRole[b.role] = b;
  const tgt = rigChain(R.by, b => (b.follow && byRole[b.follow.role]) ? (+b.follow.k || 1) * own(byRole[b.follow.role])
                                                                        : own(b)), D = {};   // follow: jip ↔ kwis
  for (const b of R.def.bones) D[b.id] = mMul(tgt(b.id), R.curInv[b.id]);
  let low = -1e9;
  for (const P of R.parts) {
    P.D = D[P.bone] || MI;
    for (const c of P.cb) { const y = P.D[1] * c[0] + P.D[3] * c[1] + P.D[5]; if (y > low) low = y; }
  }
  for (const P of R.parts) {
    const m = P.anc ? mMul(mInv(P.anc.D), P.D) : P.D;
    css(P.el, "transform", mCss(mMul(mMul(P.Pinv, m), P.P)) + P.E);
  }
  const k = R.def.k || 1, lock = (ch.ground === true || (ch.ground == null && R.legs)) && R.parts.length;
  const tx = (F.x - R.def.ground[0]) / k, ty = (F.y - R.def.ground[1]) / k + (lock ? R.low0 - low : 0) - F.lift / k;
  const flip = F.face * (R.def.drawn === "left" ? -1 : 1) < 0;
  css(R.el, "transform", `translate(${tx.toFixed(3)}px,${ty.toFixed(3)}px)`
      + (flip ? ` translate(${R.cx}px,0) scale(-1,1) translate(${-R.cx}px,0)` : "") + R.E);
  rigLight(R, ch.light, flip, { tx, ty, low, lock, lift: F.lift });
}
// ---- LIMYÈ pèsonaj la (motion.py LIGHTS): koulè dekò a (filtre SVG), liy limyè sou yon bò (rim), aura (glow),
// lonbraj anba pye yo — pèsonaj vektè a antre NAN imaj la olye l sanble kole sou li
let rigLN = 0;
function rigFilt(R) {
  if (R.fm) return R.fm;
  const NS = "http://www.w3.org/2000/svg";
  let host = document.getElementById("rigfx");
  if (!host) {
    host = document.createElementNS(NS, "svg"); host.id = "rigfx";
    host.setAttribute("width", "0"); host.setAttribute("height", "0");
    host.style.position = "absolute"; host.style.overflow = "hidden"; document.body.appendChild(host);
  }
  const f = document.createElementNS(NS, "filter"); R.fid = "rigl" + (++rigLN);
  f.setAttribute("id", R.fid); f.setAttribute("color-interpolation-filters", "sRGB");
  const m = document.createElementNS(NS, "feColorMatrix"); m.setAttribute("type", "matrix");
  f.appendChild(m); host.appendChild(f);
  return (R.fm = m);
}
function rigLight(R, L, flip, g) {
  if (!L) {
    if (R.lkey) { css(R.el, "filter", "none"); R.lkey = ""; }
    if (R.sh) R.sh.style.display = "none";
    return;
  }
  const k = R.def.k || 1, key = JSON.stringify(L) + (flip ? "|f" : "");
  if (R.lkey !== key) {
    R.lkey = key;
    const f = [], hexc = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255);
    const a = +L.amount || 0, br = L.bright == null ? 1 : +L.bright;
    if (L.tint && a > 0) {
      const d = hexc(L.tint).map(c => (((1 - a) + a * c) * br).toFixed(4));
      rigFilt(R).setAttribute("values", `${d[0]} 0 0 0 0 0 ${d[1]} 0 0 0 0 0 ${d[2]} 0 0 0 0 0 1 0`);
      f.push(`url(#${R.fid})`);
    } else if (br !== 1) f.push(`brightness(${br})`);
    if (L.rim) {
      const w = (+L.rim_w || 4) / k, dy = L.rim_side === "top" ? -w : 0;
      let dx = L.rim_side === "left" ? -w : (L.rim_side === "top" ? 0 : w);
      if (flip) dx = -dx;                              // filtre a nan kowòdone pèsonaj la: li vire avè l
      f.push(`drop-shadow(${dx.toFixed(2)}px ${dy.toFixed(2)}px ${(w * 0.18).toFixed(2)}px ${L.rim}d0)`);
    }
    if (L.glow) f.push(`drop-shadow(0 0 ${((+L.glow_w || 16) / k).toFixed(2)}px ${L.glow})`);
    css(R.el, "filter", f.join(" ") || "none");
  }
  const op = +L.shadow || 0;
  if (!(op > 0) || !g.lock) { if (R.sh) R.sh.style.display = "none"; return; }
  if (!R.sh) {                                       // menm bwat ak pèsonaj la, JIS anba l (pa vire, pa monte)
    const cs = getComputedStyle(R.el), sh = document.createElement("div"), e = document.createElement("div");
    sh.className = "rigshadow";
    sh.style.cssText = `position:${cs.position === "static" ? "absolute" : cs.position};left:${cs.left};top:${cs.top};`
      + `width:${cs.width};height:${cs.height};pointer-events:none;transform-origin:0 0;z-index:${cs.zIndex}`;
    e.style.cssText = "position:absolute;border-radius:50%;"
      + "background:radial-gradient(closest-side,rgba(0,0,0,.85),rgba(0,0,0,.35) 60%,rgba(0,0,0,0))";
    sh.appendChild(e); R.el.parentNode.insertBefore(sh, R.el); R.sh = sh; R.she = e;
  }
  const bx = R.def.box || [0, 0, 0, 1, 1], W = bx[0] * 0.55, H = Math.max(6, bx[0] * 0.09);
  const lift = Math.max(0, (+g.lift || 0) / k), s = 1 / (1 + lift / Math.max(40, (R.def.h || 300) / k * 0.6));
  R.sh.style.display = "";
  css(R.sh, "transform", `translate(${g.tx.toFixed(3)}px,${g.ty.toFixed(3)}px)` + R.E);
  css(R.she, "left", (R.cx - W * s / 2).toFixed(2) + "px");
  css(R.she, "top", (g.low + lift - H * s / 2).toFixed(2) + "px");
  css(R.she, "width", (W * s).toFixed(2) + "px");
  css(R.she, "height", (H * s).toFixed(2) + "px");
  css(R.she, "opacity", (op * s).toFixed(3));
}
function rigOf(S, name) {
  if (!S.rig) return null;
  if (S.rig[name]) return S.rig[name];
  const k = Object.keys(S.rig).find(x => x.toLowerCase() === String(name).toLowerCase());
  return k ? S.rig[k] : null;
}
// ---- KAMERA dekò vektè (sèn html, S.camera): pan, zoom, swiv yon pèsonaj, tranbleman + PARALAKS pa kouch
// (non «fon N» Design, data-depth, oswa camera.depth). Tout soti nan loc → aperçu ak rann bay menm imaj.
const CAM_DEPTH = { 1: 0.04, 2: 0.15, 3: 0.3, 4: 0.5, 5: 0.75, 6: 1.0 };
function htmlRoot(C) {                              // kad Design lan (premye div ki gen data-name nan .htmlwrap)
  if (C.hroot !== undefined) return C.hroot;
  const wrap = C.el.querySelector(".htmlwrap");
  return (C.hroot = wrap ? [...wrap.children].find(e => e.tagName === "DIV" && e.dataset.name) || null : null);
}
function camInit(C) {
  if (C.camR !== undefined) return C.camR;
  const root = htmlRoot(C);
  if (!root) return (C.camR = null);
  const W = root.offsetWidth || K.w, H = root.offsetHeight || K.h;
  const cam = document.createElement("div");       // tout kouch yo antre nan yon div kamera (kad la pa bouje)
  cam.className = "kcam";
  cam.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;will-change:transform`;
  while (root.firstChild) cam.appendChild(root.firstChild);
  root.appendChild(cam);
  const dmap = C.S.camera.depth || {}, layers = [];
  for (const el of cam.children) {
    const n = (el.dataset && el.dataset.name) || "";
    let d = null;
    if (n in dmap) d = +dmap[n];
    else if (el.dataset && el.dataset.depth != null && el.dataset.depth !== "") d = parseFloat(el.dataset.depth);
    else { const m = /^fon\s*(\d+)/i.exec(n); if (m && CAM_DEPTH[+m[1]] !== undefined) d = CAM_DEPTH[+m[1]]; }
    if (d !== null && isFinite(d) && Math.abs(d - 1) > 1e-6) layers.push({ el, d });
  }
  return (C.camR = { root, cam, W, H, layers });
}
function rigPos(C, name, loc) {                     // pozisyon pye / pwen ankraj yon pèsonaj rig nan nenpòt lè
  const ch = rigOf(C.S, name); if (!ch) return null;
  const R = C.rig.find(x => x.def.name.toLowerCase() === String(name).toLowerCase()); if (!R) return null;
  if (R.ch !== ch) { R.segs = rigPlan(ch, R.def.ground); R.ch = ch; }
  const F = rigFrame(K.rigm, ch, loc, R.def.ground, R.def.h, R.segs);
  return [F.x, F.y - (F.lift || 0)];
}
function camApply(C, loc) {
  const cm = C.S.camera, R = camInit(C); if (!R) return;
  const u = easeK(clamp(loc / C.S.dur, 0, 1), cm.ease);
  let cx = cm.pan[0] * u, cy = cm.pan[1] * u;
  const z = cm.zoom[0] + (cm.zoom[1] - cm.zoom[0]) * u;
  if (cm.follow) {                                  // swiv deplasman pèsonaj la sou x (depi kòmansman sèn nan)
    const p = rigPos(C, cm.follow.rig, loc), p0 = rigPos(C, cm.follow.rig, 0);
    if (p && p0) cx += (p[0] - p0[0]) * cm.follow.amount + cm.follow.offset[0];
  }
  if (cm.limit != null) { cx = clamp(cx, -cm.limit, cm.limit); cy = clamp(cy, -cm.limit, cm.limit); }
  let sx = 0, sy = 0;
  for (const s of cm.shake) {                       // tranbleman lè gen chòk (ateri, tonbe…)
    const dl = loc - s.at;
    if (dl > 0 && dl < s.dur) { const k = 1 - dl / s.dur; sx += Math.sin(dl * 90) * s.force * k; sy += Math.cos(dl * 70) * s.force * 0.7 * k; }
  }
  const o = cm.origin || [R.W / 2, R.H / 2];
  css(R.cam, "transformOrigin", `${o[0]}px ${o[1]}px`);
  css(R.cam, "transform", `translate(${(-cx + sx).toFixed(2)}px,${(-cy + sy).toFixed(2)}px) scale(${z.toFixed(4)})`);
  for (const L of R.layers)                         // kouch lwen yo deplase MWENS (prop translate: transform Design la rete)
    css(L.el, "translate", `${(cx * (1 - L.d)).toFixed(2)}px ${(cy * (1 - L.d)).toFixed(2)}px`);
}
// ---- FX: patikil detèminis (S.fx): dust · sparks · trail (sillage dèyè yon rig) · rain · smoke
const fxRnd = (s, i, k) => { const x = Math.sin(s * 12.9898 + i * 78.233 + (k || 0) * 37.719) * 43758.5453; return x - Math.floor(x); };
function fxInit(C) {
  if (C.fxR) return C.fxR;
  const R = C.S.camera && C.isHtml ? camInit(C) : null, root = C.isHtml ? htmlRoot(C) : null;
  const host = R ? R.cam : (root || C.el), W = R ? R.W : (root && root.offsetWidth) || K.w, H = R ? R.H : (root && root.offsetHeight) || K.h;
  C.fxR = { W, H, list: C.S.fx.map(e => {
    const ps = [];
    for (let i = 0; i < e.count; i++) {
      const p = document.createElement("div");
      const glow = e.type === "sparks" || e.type === "trail";
      p.style.cssText = `position:absolute;left:0;top:0;pointer-events:none;opacity:0;border-radius:${e.type === "rain" ? "1px" : "50%"};`
        + `background:${e.color};will-change:transform,opacity;` + (glow ? `box-shadow:0 0 ${(e.size * 0.9).toFixed(1)}px ${e.color};` : "")
        + (e.type === "smoke" ? `filter:blur(${(e.size * 0.22).toFixed(1)}px);` : e.type === "dust" ? "filter:blur(1px);" : "");
      host.appendChild(p); ps.push(p);
    }
    return { e, ps };
  }) };
  return C.fxR;
}
function fxDot(p, x, y, w, h, op, rot) {
  css(p, "width", w.toFixed(1) + "px"); css(p, "height", h.toFixed(1) + "px");
  css(p, "transform", `translate(${(x - w / 2).toFixed(1)}px,${(y - h / 2).toFixed(1)}px)` + (rot ? ` rotate(${rot}deg)` : ""));
  css(p, "opacity", op.toFixed(3));
}
function fxApply(C, loc) {
  const F = fxInit(C);
  for (const { e, ps } of F.list) {
    const dl = loc - e.at, n = ps.length, on = dl >= 0 && dl <= e.dur;
    ps.forEach((p, i) => {
      if (!on && e.type !== "trail") { css(p, "opacity", "0"); return; }
      const r1 = fxRnd(e.seed, i, 1), r2 = fxRnd(e.seed, i, 2), r3 = fxRnd(e.seed, i, 3);
      if (e.type === "dust") {                      // pousyè ki gaye sou kote lè yon pye frape tè a
        const s = dl / e.dur, a = Math.PI * (0.08 + 0.84 * (n > 1 ? i / (n - 1) : 0.5) + (r1 - 0.5) * 0.1);
        const r = (50 + 70 * r2) * e.spread * e.speed * Math.sqrt(s), k = 0.6 + 1.6 * s;
        fxDot(p, e.x + Math.cos(a) * r * 1.6, e.y - Math.sin(a) * r * 0.45, e.size * k, e.size * k, e.opacity * (1 - s));
      } else if (e.type === "sparks") {             // etensèl: eksplozyon + gravite
        const s = dl / e.dur, a = Math.PI * 2 * r1, v = (140 + 260 * r2) * e.speed * e.spread;
        const x = e.x + Math.cos(a) * v * dl, y = e.y - Math.abs(Math.sin(a)) * v * dl * (0.6 + 0.6 * r3) + 450 * dl * dl;
        const k = e.size * (1 - 0.6 * s);
        fxDot(p, x, y, k, k, e.opacity * (1 - s * s));
      } else if (e.type === "trail") {              // sillage limyè: pozisyon pèsonaj la nan tan ki sot pase
        const ti = loc - i * 0.045 / e.speed;
        const pos = ti >= e.at && ti <= e.at + e.dur ? rigPos(C, e.follow, ti) : null;
        if (!pos) { css(p, "opacity", "0"); return; }
        const f = 1 - i / n, k = e.size * (0.4 + 0.6 * f);
        fxDot(p, pos[0] + e.offset[0] + (r1 - 0.5) * 6 * e.spread, pos[1] + e.offset[1] + (r2 - 0.5) * 6 * e.spread, k, k, e.opacity * f);
      } else if (e.type === "rain") {               // lapli: tras ki tonbe, kouvri tout kad la
        const v = (900 + 600 * r2) * e.speed, len = 18 + 22 * r3, span = F.H + 120;
        const y = ((r1 * span + v * dl) % span) - 60, x = (fxRnd(e.seed, i, 4) * (F.W + 240) - 120) + Math.tan(e.angle * Math.PI / 180) * y;
        fxDot(p, x, y, e.size, len, e.opacity * (0.5 + 0.5 * r3), -e.angle);
      } else if (e.type === "smoke") {              // lafimen: ti nwaj k ap monte, grandi, disparèt
        const life = 1.8 / e.speed, tb = (i / n) * Math.max(0.01, e.dur - life * 0.5), age = dl - tb;
        if (age < 0 || age > life) { css(p, "opacity", "0"); return; }
        const s = age / life, k = e.size * (0.5 + 1.2 * s);
        fxDot(p, e.x + (r1 - 0.5) * 40 * e.spread + (r2 - 0.5) * 60 * e.spread * s, e.y - 140 * s * e.speed, k, k,
              e.opacity * 0.7 * Math.sin(Math.PI * s));
      }
    });
  }
}
// ---- caches built ONCE: every frame touches only the scene(s) on screen and writes only what changed
const $$ = (root, q) => [...root.querySelectorAll(q)];
const SC = $$(document, ".scene").map(sc => ({
  el: sc, S: K.scenes[+sc.dataset.s], shown: true,
  trans: sc.dataset.trans || "fade",
  isHtml: sc.dataset.type === "html",
  isLottie: sc.dataset.type === "lottie",
  timing: (K.scenes[+sc.dataset.s] && (K.scenes[+sc.dataset.s].timing || K.scenes[+sc.dataset.s].responsive_timing)) || null,
  a: $$(sc, ".a").map(el => ({ el, d: +el.dataset.d || 0, fx: el.dataset.fx })),
  type: $$(sc, ".type").map(el => ({ el, d: +el.dataset.d, len: +el.dataset.len })),
  zoom: $$(sc, "img.media.zoom"), clip: $$(sc, "img[data-clip]"),
  count: $$(sc, "[data-count]").map(el => ({ el, d: +((el.closest(".a") || el).dataset.d) || 0 })),
  loop: $$(sc, "img[data-loop]"), bgz: $$(sc, ".bgimg.zoom"), ov: $$(sc, ".ov"),
  hl: $$(sc, ".hl[data-at]").map(el => ({ el, at: +el.dataset.at })),
  cam: $$(sc, "img[data-cam]").map(el => ({ el, c: JSON.parse(el.dataset.cam) })),
  card: $$(sc, ".card3d").map(el => ({ el, c: JSON.parse(el.dataset.card) })),
  mouth: $$(sc, "[data-mouth]").map(el => ({ el, parts: $$(el, "[data-shape]"), cur: null })),
  eyes: $$(sc, "[data-eyes]").map((el, i) => ({ el, parts: $$(el, "[data-eye]"), cur: null,
                                                seed: (+sc.dataset.s + 1) * 7919 + i * 104729 })),
  brows: $$(sc, "[data-brows]").map(el => ({ el, parts: $$(el, "[data-expr]"), cur: null })),
  rig: $$(sc, "[data-rig]").map(el => rigInit(el)).filter(Boolean),
}));
// ---- lipsync: bouch [data-mouth] > [data-shape="A".."X"] swiv vwa a (cues Rhubarb nan S.mouth), je [data-eyes] bat
const MFALL = { G: "B", H: "C", X: "A", half: "closed" };
function mouthAt(S, t) {                            // fòm bouch nan lè t (cues ranje, rechèch dikotomik)
  const M = S.mouth; if (!M || !M.length || t < M[0][0] || t >= M[M.length - 1][1]) return "X";
  let lo = 0, hi = M.length - 1;
  while (lo < hi) { const m = (lo + hi + 1) >> 1; if (M[m][0] <= t) lo = m; else hi = m - 1; }
  return t < M[lo][1] ? M[lo][2] : "X";
}
function pickSet(G, key, want, expr) {              // montre SÈL pitit ki gen fòm nan (oswa fòm ranplasman li); vèsyon
  expr = expr || "neutral";                         // EKSPRESYON an (data-expr) an premye si l egziste
  const ck = want + "|" + expr; if (G.cur === ck) return; G.cur = ck;
  const has = (p, w) => (p.dataset[key] || "").split(/[\s,]+/).includes(w);
  const pickIn = w => { const c = G.parts.filter(p => has(p, w)); if (!c.length) return null;
    return c.find(p => p.dataset.expr === expr) || c.find(p => !p.dataset.expr) || c[0]; };
  let pick = pickIn(want);
  if (!pick && MFALL[want]) pick = pickIn(MFALL[want]);
  if (!pick) pick = pickIn(key === "shape" ? "X" : "open") || pickIn("A");
  for (const p of G.parts) css(p, "visibility", p === pick ? "visible" : "hidden");
}
function browSet(B, expr) {                         // sousi: vèsyon ekspresyon an (sinon «neutral»)
  if (B.cur === expr) return; B.cur = expr;
  const pick = B.parts.find(p => p.dataset.expr === expr) || B.parts.find(p => p.dataset.expr === "neutral") || B.parts[0];
  for (const p of B.parts) css(p, "visibility", p === pick ? "visible" : "hidden");
}
function exprOf(S, name, loc) { const ch = name ? rigOf(S, name) : null; return ch ? rigExpr(ch, loc) : "neutral"; }
function blinkStart(loc, seed) {                    // dènye bat je ki kòmanse anvan loc (orè detèminis: menm rann)
  let x = seed % 2147483647 || 1, b = 0.6;
  const rnd = () => (x = (x * 16807) % 2147483647) / 2147483647;
  b += rnd() * 1.6;
  let prev = -1e9;
  while (b <= loc) { prev = b; b += 2.2 + rnd() * 2.6 + (rnd() < 0.15 ? -1.9 : 0); }
  return [prev, b];
}
function eyeAt(loc, seed) {
  const d = loc - blinkStart(loc, seed)[0];
  return d < 0.05 ? "half" : d < 0.12 ? "closed" : d < 0.18 ? "half" : "open";
}
function blinkBusy(loc, seed) {
  const [a, b] = blinkStart(loc, seed);
  return loc - a < 0.24 || b - loc < 0.06;
}
const STAGE = { loop: $$(document, "#stagebg img[data-loop]"), bgz: $$(document, "#stagebg .bgimg.zoom"),
                ov: $$(document, "#stageback .ov, #stagefront .ov") };
const TC = $$(document, "#stagetracks .tclip").map(el => {
  const mc = el.classList.contains("mcam");
  const isRoll = el.dataset.roll === "1", isCrawl = el.dataset.crawl === "1";
  return {
    el, mcam: mc, roll: isRoll, crawl: isCrawl,
    rInner: (isRoll || isCrawl) ? el.firstElementChild : null,
    vid: mc ? null : (el.tagName === "VIDEO" ? el : el.querySelector("video")),
    angs: mc ? $$(el, "video[data-ang]").map(v => ({ el: v, in: +v.dataset.in || 0 })) : null,
    cuts: el.dataset.cuts ? (() => { try { return JSON.parse(el.dataset.cuts); } catch (e) { return null; } })() : null,
    s: +el.dataset.start, d: +el.dataset.dur, sp: +el.dataset.speed || 1, i0: +el.dataset.in || 0,
    kf: el.dataset.kf ? (() => { try { return JSON.parse(el.dataset.kf); } catch (e) { return null; } })() : null,
    sramp: el.dataset.sramp ? (() => { try { return JSON.parse(el.dataset.sramp); } catch (e) { return null; } })() : null,
    v: null
  };
});
function srampSrc(ramp, dur, L) {                    // segonn sous konsome @ tan lokal L (entegral vitès kap chanje)
  const pts = ramp.map(k => ({ s: k.t * dur, v: Math.max(0.05, k.v) }));
  if (!pts.length) return L;
  if (pts[0].s > 0) pts.unshift({ s: 0, v: pts[0].v });
  if (pts[pts.length - 1].s < dur) pts.push({ s: dur, v: pts[pts.length - 1].v });
  let src = 0;
  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1], b = pts[i], seg = b.s - a.s;
    if (seg <= 0) continue;
    if (L <= b.s) { const dt = Math.max(0, L - a.s), vL = a.v + (b.v - a.v) * (dt / seg); return src + (a.v + vL) / 2 * dt; }
    src += (a.v + b.v) / 2 * seg;
  }
  return src;
}
function cubicBezier(x1, y1, x2, y2) {               // menm koub ak CSS cubic-bezier
  if (x1 === 0 && y1 === 0 && x2 === 1 && y2 === 1) return t => t;
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const fx = t => ((ax * t + bx) * t + cx) * t;
  const fy = t => ((ay * t + by) * t + cy) * t;
  const dfx = t => (3 * ax * t + 2 * bx) * t + cx;
  return x => { let t = x; for (let i = 0; i < 6; i++) { const e = fx(t) - x; if (Math.abs(e) < 1e-4) break; const d = dfx(t); if (Math.abs(d) < 1e-6) break; t -= e / d; } return fy(Math.max(0, Math.min(1, t))); };
}
const KF_EASES = { linear: [0, 0, 1, 1], in: [.42, 0, 1, 1], out: [0, 0, .58, 1], inout: [.42, 0, .58, 1] };
function kfEaseFn(e) { let a = Array.isArray(e) ? e : KF_EASES[e]; if (!a || a.length < 4) a = KF_EASES.linear; return cubicBezier(a[0], a[1], a[2], a[3]); }
function kfLerp(kf, p) {                             // entèpolasyon kle yo @ pozisyon p (0..1), ak ease/bezye
  const b = kf.b, out = { x: b.x, y: b.y, rot: b.rot, sc: b.sc, op: b.op };
  ["x", "y", "rot", "sc", "op"].forEach(pr => {
    const pts = kf.k.filter(k => k[pr] != null);
    if (!pts.length) return;
    if (p <= pts[0].t) { out[pr] = pts[0][pr]; return; }
    if (p >= pts[pts.length - 1].t) { out[pr] = pts[pts.length - 1][pr]; return; }
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i], c2 = pts[i + 1];
      if (p >= a.t && p <= c2.t) {
        let f = (c2.t - a.t) ? (p - a.t) / (c2.t - a.t) : 0;
        if (a.e) { const ef = a._ef || (a._ef = kfEaseFn(a.e)); f = ef(f); }
        out[pr] = a[pr] + (c2[pr] - a[pr]) * f; break;
      }
    }
  });
  return out;
}
const O1 = document.getElementById("o1"), O2 = document.getElementById("o2"), GRID = document.getElementById("grid");
const BAR = document.getElementById("bar"), CAP = document.getElementById("capt"), CR = document.getElementById("credit");
const SUBS = document.getElementById("subs");
function css(el, prop, v) {                         // write a style only when it changes (no useless relayout)
  const k = el.__k || (el.__k = {});
  if (k[prop] !== v) { k[prop] = v; el.style[prop] = v; }
}
// ANIMASYON CSS / WAAPI nan sèn html (@keyframes, transition, el.animate(), Design → Kadans): te kouri sou revèy
// reyèl la → rann imaj pa imaj pa t egzak (yon imaj ka pran 200 ms pou kaptire). Kounye a chak animasyon kanpe
// (pause) epi pran tan LOKAL sèn nan: 0 = sèn nan kòmanse. Sèn ki vle kontwole pa l: data-waapi="off".
function waapiList(C) {
  if (C.noWaapi === undefined) C.noWaapi = !C.el.getAnimations || C.el.dataset.waapi === "off" ||
    !!C.el.querySelector('[data-waapi="off"]');
  return C.noWaapi ? [] : C.el.getAnimations({ subtree: true });
}
function waapiSeek(C, loc) {
  let targetLoc = loc;
  if (C.timing) {
    const tm = C.timing;
    const intro = Math.max(0, +tm.intro || 0);
    const outro = Math.max(0, +tm.outro || 0);
    const total = (C.S && C.S.dur) || 3.0;
    const design = Math.max(intro + outro + 0.1, +tm.design || (intro + outro + 1.0));
    if (total > (intro + outro) && design > (intro + outro)) {
      if (loc <= intro) {
        targetLoc = loc;
      } else if (loc >= total - outro) {
        const outroProg = (loc - (total - outro)) / Math.max(0.01, outro);
        targetLoc = (design - outro) + outroProg * outro;
      } else {
        const midProg = (loc - intro) / Math.max(0.01, total - intro - outro);
        targetLoc = intro + midProg * (design - intro - outro);
      }
    }
  }
  const ms = Math.max(0, targetLoc * 1000);
  for (const a of waapiList(C)) {
    try {
      if (a.playState !== "paused") a.pause();
      if (Math.abs((a.currentTime || 0) - ms) > 0.01) a.currentTime = ms;
    } catch (e) {}
  }
}
function waapiBusy(C, loc) {                           // yon animasyon CSS ap mache nan moman sa a?
  const ms = loc * 1000;
  return waapiList(C).some(a => {
    try { const g = a.effect.getComputedTiming(); return ms >= (g.delay || 0) - 30 && ms <= g.endTime + 30; }
    catch (e) { return false; }
  });
}
function seekSync(t) {
  VT = t;
  for (const c of TC) {
    const vis = t >= c.s - 0.001 && t <= c.s + c.d + 0.001;
    if (vis !== c.v) { c.v = vis; css(c.el, "display", vis ? "block" : "none"); if (!vis && c.vid && !c.vid.paused) { try { c.vid.pause(); } catch(e){} } }
    if (vis && c.mcam && c.angs) {                         // multicam: chwazi ang aktif la selon koup yo
      const p = c.d > 0 ? Math.max(0, Math.min(1, (t - c.s) / c.d)) : 0;
      let ang = (c.cuts && c.cuts.length) ? c.cuts[0].a : 0;
      if (c.cuts) for (const cut of c.cuts) { if (p >= cut.t) ang = cut.a; else break; }
      const L = Math.max(0, t - c.s);
      c.angs.forEach((m, i) => {
        const show = (i === ang);
        css(m.el, "display", show ? "block" : "none");
        if (show) { const vt = m.in + L; if (Math.abs((m.el.currentTime || 0) - vt) > 0.18) { try { m.el.currentTime = vt; } catch (e) {} } }
      });
    } else if (vis && c.vid) {
      const L = Math.max(0, t - c.s);                      // tan lokal nan clip la
      const vt = c.i0 + (c.sramp ? srampSrc(c.sramp, c.d, L) : L * c.sp);   // ramp oswa vitès konstan
      if (playing) {
        if (c.vid.paused) { c.vid.play().catch(() => {}); }
        if (Math.abs((c.vid.currentTime || 0) - vt) > 0.25) { try { c.vid.currentTime = vt; } catch (e) {} }
      } else {
        if (!c.vid.paused) { c.vid.pause(); }
        if (Math.abs((c.vid.currentTime || 0) - vt) > 0.04) { try { c.vid.currentTime = vt; } catch (e) {} }
      }
    }
    if (vis && c.kf) {                                     // animasyon keyframe sou clip la
      const p = c.d > 0 ? Math.max(0, Math.min(1, (t - c.s) / c.d)) : 0;
      const v = kfLerp(c.kf, p);
      css(c.el, "left", (v.x * 100).toFixed(3) + "%");
      css(c.el, "top", (v.y * 100).toFixed(3) + "%");
      css(c.el, "transform", "translate(-50%,-50%) rotate(" + v.rot.toFixed(2) + "deg) scale(" + v.sc.toFixed(3) + ")");
      css(c.el, "opacity", v.op.toFixed(3));
    }
    if (vis && (c.roll || c.crawl) && c.rInner) {
      const p = c.d > 0 ? Math.max(0, Math.min(1, (t - c.s) / c.d)) : 0;
      if (c.roll) {
        const contH = c.el.offsetHeight || K.h || 720;
        const totalH = c.rInner.scrollHeight || c.rInner.offsetHeight || 800;
        const y = contH - p * (contH + totalH);
        css(c.rInner, "transform", `translateY(${y.toFixed(1)}px)`);
      } else if (c.crawl) {
        const contW = c.el.offsetWidth || K.w || 1280;
        const totalW = c.rInner.scrollWidth || c.rInner.offsetWidth || 1000;
        const x = contW - p * (contW + totalW);
        css(c.rInner, "transform", `translateX(${x.toFixed(1)}px)`);
      }
    }
  }
  const W = K.w, H = K.h;
  css(O1, "transform", `translate(${W * -0.1 + Math.sin(t * .35) * W * .13}px, ${H * -0.23 + Math.cos(t * .27) * H * .15}px)`);
  css(O2, "transform", `translate(${W * 0.62 + Math.cos(t * .3) * W * .12}px, ${H * 0.35 + Math.sin(t * .4) * H * .16}px)`);
  css(GRID, "transform", `translateY(${((t * 20) % K.tile).toFixed(1)}px)`);
  if (BAR) css(BAR, "width", `${(clamp(t / K.total, 0, 1) * 100).toFixed(2)}%`);
  for (const C of SC) {
    const S = C.S, loc = t - S.start;
    const vis = loc >= -0.01 && loc <= S.dur + 0.01;
    if (!vis) {
      if (C.shown) { css(C.el, "opacity", "0"); css(C.el, "transform", ""); C.shown = false; }
      continue;
    }
    C.shown = true;
    const tin = (C.trans === "none") ? 0.001 : 0.35;
    let fin = S.start === 0 ? 1 : clamp(loc / tin, 0, 1);
    const fout = S.last ? 1 : clamp((S.dur - loc) / 0.35, 0, 1);
    if (INEDITOR && !playing && loc >= 0 && loc <= S.dur) fin = 1;
    css(C.el, "opacity", String(Math.min(fin, fout)));
    let _tr = fout < 1 ? `scale(${1 + (1 - fout) * 0.04})` : "";
    if (fin < 1 && S.start > 0 && !(INEDITOR && !playing)) {
      const _e = easeOut(fin), _inv = 1 - _e;
      if (C.trans === "slide") _tr = `translateX(${(_inv * 70).toFixed(1)}px)`;
      else if (C.trans === "slideright") _tr = `translateX(${(_inv * -70).toFixed(1)}px)`;
      else if (C.trans === "slideup") _tr = `translateY(${(_inv * 70).toFixed(1)}px)`;
      else if (C.trans === "slidedown") _tr = `translateY(${(_inv * -70).toFixed(1)}px)`;
      else if (C.trans === "zoom") _tr = `scale(${(0.9 + 0.1 * _e).toFixed(4)})`;
      else if (C.trans === "zoomout") _tr = `scale(${(1.1 - 0.1 * _e).toFixed(4)})`;
      else if (C.trans === "flip") _tr = `perspective(900px) rotateY(${(_inv * 80).toFixed(1)}deg)`;
      else if (C.trans === "rotate") _tr = `rotate(${(_inv * -8).toFixed(2)}deg) scale(${(0.9 + 0.1 * _e).toFixed(4)})`;
      else if (C.trans === "blur") css(C.el, "filter", `blur(${(_inv * 14).toFixed(1)}px)`);
      else if (C.trans === "wipe") css(C.el, "clip-path", `inset(0 ${(_inv * 100).toFixed(1)}% 0 0)`);
      else if (C.trans === "wipeup") css(C.el, "clip-path", `inset(${(_inv * 100).toFixed(1)}% 0 0 0)`);
    } else { if (C.trans === "wipe" || C.trans === "wipeup") css(C.el, "clip-path", ""); if (C.trans === "blur") css(C.el, "filter", ""); }
    css(C.el, "transform", _tr);
    for (const A of C.a) {
      const p = clamp((loc - A.d) / 0.6, 0, 1), e = easeOut(p), fx = A.fx;
      const op = (INEDITOR && !playing && loc >= 0 && loc <= S.dur) ? 1 : p;
      css(A.el, "opacity", String(op));
      let tr = "";
      if (p < 1 && !(INEDITOR && !playing)) {
        if (fx === "up") tr = `translateY(${(1 - e) * 60}px)`;
        else if (fx === "zoom") tr = `scale(${0.4 + 0.6 * back(p)}) rotate(${(1 - e) * -12}deg)`;
        else if (fx === "pop") tr = `scale(${0.6 + 0.4 * back(p)})`;
        else if (fx === "left") tr = `translateX(${(e - 1) * 300}px)`;
        else if (fx === "right") tr = `translateX(${(1 - e) * 300}px)`;
      }
      css(A.el, "transform", tr);
    }
    for (const T of C.type) typeAt(T.el, clamp((loc - T.d) / T.len, 0, 1));
    for (const el of C.zoom) css(el, "transform", `scale(${(1 + 0.08 * clamp(loc / S.dur, 0, 1)).toFixed(4)})`);
    for (const M of C.cam) {                          // vrè zoom/panoramik: orijin + echèl ki enterpole ak ease
      const p = easeK(clamp(loc / S.dur, 0, 1), M.c.ease), f = M.c.from, to = M.c.to;
      const z = f.zoom + (to.zoom - f.zoom) * p, x = f.x + (to.x - f.x) * p, y = f.y + (to.y - f.y) * p;
      css(M.el, "transform-origin", `${(x * 100).toFixed(2)}% ${(y * 100).toFixed(2)}%`);
      css(M.el, "transform", `scale(${z.toFixed(4)})`);
    }
    for (const M of C.card) cardAt(M.el, M.c, loc, S.dur);
    if (C.mouth.length) { const sh = mouthAt(S, t); for (const G of C.mouth) pickSet(G, "shape", sh, exprOf(S, G.el.dataset.mouth, loc)); }
    for (const E of C.eyes) pickSet(E, "eye", S.blink === false ? "open" : eyeAt(loc, E.seed), exprOf(S, E.el.dataset.eyes, loc));
    for (const B of C.brows) browSet(B, exprOf(S, B.el.dataset.brows, loc));
    if (S.rig) for (const R of C.rig) { const ch = rigOf(S, R.def.name); if (ch) rigApply(R, ch, loc); }
    if (S.camera && C.isHtml) camApply(C, loc);       // APRE rig yo: kamera ka swiv yon pèsonaj
    if (S.fx) fxApply(C, loc);
    for (const el of C.clip) {
      const c = K.clips[el.dataset.clip]; if (!c) continue;
      const f = clamp(Math.floor(loc * (+el.dataset.speed || 1) * c.fps + 1e-6), 0, c.count - 1) + 1, src = c.url + "/" + pad5(f) + ".jpg";
      if (el.getAttribute("src") !== src) { el.setAttribute("src", src); pendingImgs.push(el); }
    }
    for (const N of C.count) countAt(N.el, clamp((loc - N.d) / 1.2, 0, 1));
    for (const h of C.hl) {                               // highlighted word pulses when it is spoken
      const d = t - h.at, b = d >= 0 && d < 0.7 ? Math.sin(Math.min(1, d / 0.7) * Math.PI) : 0;
      css(h.el, "transform", b ? `scale(${1 + 0.1 * b})` : "");
      css(h.el, "filter", b ? `brightness(${1 + 0.5 * b})` : "");
    }
    if (C.isLottie || (typeof window.__lottieAnims !== "undefined" && window.__lottieAnims && window.__lottieAnims[S.id])) {
      const p = clamp(loc / S.dur, 0, 1);
      if (window.__lottieAnims && window.__lottieAnims[S.id]) {
        try {
          const la = window.__lottieAnims[S.id];
          const tot = la.totalFrames || (S.dur * (la.frameRate || K.fps));
          la.goToAndStop(p * tot, true);
        } catch(e){}
      }
    }
    if (C.isHtml) {
      const p = clamp(loc / S.dur, 0, 1);
      waapiSeek(C, loc);
      window.Kadans = { time: loc, globalTime: t, progress: p, frame: Math.round(loc * K.fps), fps: K.fps, duration: S.dur }; window.HyperFrames = window.Kadans;
      if (typeof window.onSeek === "function") {
        try { window.onSeek(t, loc, p, S.id); } catch(e){}
      }
      if (typeof window.__onFrame === "function") {
        try { window.__onFrame(t, loc, p, S.id); } catch(e){}
      }
      if (typeof gsap !== "undefined") {
        if (window.tl && typeof window.tl.seek === "function") {
          try { window.tl.seek(loc, false); } catch(e){}
        } else if (window.timeline && typeof window.timeline.seek === "function") {
          try { window.timeline.seek(loc, false); } catch(e){}
        } else if (gsap.globalTimeline) {
          try { gsap.globalTimeline.seek(loc, false); } catch(e){}
        }
      }
      if (typeof lottie !== "undefined") {
        if (window.lottieAnimation && typeof window.lottieAnimation.goToAndStop === "function") {
          try {
            const tot = window.lottieAnimation.totalFrames || (S.dur * (window.lottieAnimation.frameRate || K.fps));
            window.lottieAnimation.goToAndStop(p * tot, true);
          } catch(e){}
        } else if (window.anim && typeof window.anim.goToAndStop === "function") {
          try {
            const tot = window.anim.totalFrames || (S.dur * (window.anim.frameRate || K.fps));
            window.anim.goToAndStop(p * tot, true);
          } catch(e){}
        }
      }
      if (typeof anime !== "undefined" && window.animeTimeline && typeof window.animeTimeline.seek === "function") {
        try { window.animeTimeline.seek(loc * 1000); } catch(e){}
      }
      try {
        window.dispatchEvent(new CustomEvent("kadans:frame", { detail: { t: t, localTime: loc, progress: p, scene: S.id } }));
      } catch(e){}
    }
    layerSet(C, t, loc, S.dur);
  }
  layerSet(STAGE, t, t, K.total);
  if (CAP) {                                              // captions: rebuilt only when the spoken word changes
    const L = K.captions.find(l => t >= l.s - 0.15 && t <= l.e + 0.35);
    let key = "";
    if (L) key = K.captions.indexOf(L) + ":" + L.words.map(w => (t >= w.s && t < w.e + 0.05) ? 2 : t >= w.s ? 1 : 0).join("");
    if (CAP.__key !== key) {
      CAP.__key = key;
      CAP.innerHTML = !L ? "" : L.words.map(w => {
        if (K.cap_style === "pop" && t < w.s) return "";
        const cls = t >= w.s && t < w.e + 0.05 ? "now" : t >= w.s ? "on" : "";
        return `<span class="${cls}">${w.w.replace(/[<&*]/g, "")}</span>`; }).join("");   // gap = margin (the
        // spoken word grows: with a plain space it covered its neighbours -> "Dixlogiciels")
    }
  }
  if (SUBS && K.sub_cues && K.sub_cues.length) {          // sou-tit eksplisit (editè sou-tit)
    const Q = K.sub_cues.find(q => t >= q.s - 0.03 && t <= q.e + 0.03);
    const key = Q ? K.sub_cues.indexOf(Q) : -1;
    if (SUBS.__key !== key) {
      SUBS.__key = key;
      if (!Q) { SUBS.style.display = "none"; SUBS.innerHTML = ""; }
      else {
        const st = K.sub_style || {};
        SUBS.className = Q.pos || st.pos || "bottom";
        SUBS.style.fontSize = st.size ? (st.size + "px") : "";
        SUBS.style.color = st.color || "";
        SUBS.innerHTML = '<span class="sbx"' + (st.bg ? ' style="background:' + st.bg + '"' : "") + '>'
          + String(Q.text).replace(/[<&]/g, "").replace(/\\n/g, "<br>") + '</span>';
        SUBS.style.display = "block";
      }
    }
  }
  if (CR && K.scenes && K.scenes.length) { const L = K.scenes[K.scenes.length - 1]; if (L) css(CR, "opacity", String(clamp((t - L.start - 0.8) / 0.6, 0, 1))); }
}
// is anything moving FAST at instant t? (entrances, scene fades, typing, counting, emphasis pulses, clip frames)
// The renderer captures motion-blur sub-frames only when it is: a still frame is the same with or without blur.
window.__busy = function (t) {
  for (const C of SC) {
    const S = C.S, loc = t - S.start;
    if (loc < -0.05 || loc > S.dur + 0.05) continue;
    const M = S.mouth;                                    // bouch k ap pale / je k ap bat = imaj ki chanje
    if (C.mouth.length && M && M.length && t >= M[0][0] - 0.05 && t <= M[M.length - 1][1] + 0.05) return true;
    if (S.blink !== false && C.eyes.some(E => blinkBusy(loc, E.seed))) return true;
    if (S.rig && C.rig.some(R => rigOf(S, R.def.name))) return true;     // pèsonaj k ap bouje (menm respire)
    if (S.camera && S.camera.shake && S.camera.shake.some(s => loc > s.at && loc < s.at + s.dur)) return true;   // tranbleman
    if (S.fx && S.fx.some(e => e.type === "trail" ? loc >= e.at && loc <= e.at + e.dur + 1 : loc >= e.at && loc <= e.at + e.dur)) return true;
    if (C.isLottie || (typeof window.__lottieAnims !== "undefined" && window.__lottieAnims && window.__lottieAnims[S.id])) return true;
    if (C.isHtml) {
      if (typeof window.isSceneBusy === "function") {
        try { if (window.isSceneBusy(loc, t, S.id)) return true; } catch(e){}
      }
      if (loc < 0.45 || (!S.last && S.dur - loc < 0.4)) return true;
      if (waapiBusy(C, loc)) return true;
      if (typeof gsap !== "undefined" && gsap.globalTimeline && gsap.globalTimeline.isActive()) return true;
      if (typeof lottie !== "undefined" && (window.lottieAnimation || window.anim)) return true;
      continue;
    }
    if ((S.start > 0 && loc < 0.4) || (!S.last && S.dur - loc < 0.4)) return true;
    for (const A of C.a) { const p = (loc - A.d) / 0.6; if (p > -0.05 && p < 1.02) return true; }
    for (const T of C.type) { const p = (loc - T.d) / T.len; if (p > 0 && p < 1) return true; }
    for (const N of C.count) { const p = (loc - N.d) / 1.2; if (p > 0 && p < 1) return true; }
    for (const h of C.hl) { const d = t - h.at; if (d > -0.05 && d < 0.75) return true; }
    if (C.clip.length || C.loop.length || C.cam.length || C.card.length) return true;
    for (const el of C.ov) if (el.dataset.anim === "sweep" || el.dataset.anim === "spin" || el.dataset.anim === "reveal") return true;
  }
  for (const el of STAGE.ov) if (el.dataset.anim === "sweep" || el.dataset.anim === "spin") return true;
  return STAGE.loop.length > 0;
};
function layerSet(C, t, lt, dur) {                        // backgrounds + atmosphere overlays of one scene / the stage
  const W = K.w, H = K.h;
  for (const el of C.loop) {
    const c = K.clips[el.dataset.loop]; if (!c) continue;
    const f = ((Math.floor(Math.max(0, lt) * c.fps + 1e-6) % c.count) + c.count) % c.count + 1;
    const src = c.url + "/" + pad5(f) + ".jpg";
    if (el.getAttribute("src") !== src) { el.setAttribute("src", src); pendingImgs.push(el); }
  }
  for (const el of C.bgz) css(el, "transform", `scale(${(1.02 + 0.07 * clamp(lt / dur, 0, 1)).toFixed(4)})`);
  for (const el of C.ov) {
    const sp = +el.dataset.speed, rot0 = +el.dataset.rot, op = +el.dataset.op, a = el.dataset.anim;
    let dx = 0, dy = 0, r = rot0, k = 1, o = op;
    if (a === "drift") { dx = Math.sin(lt * 0.17 * sp) * W * 0.04 + lt * sp * W * 0.004; dy = Math.cos(lt * 0.13 * sp) * H * 0.03; }
    else if (a === "pulse") { const w = Math.sin(2 * Math.PI * 0.45 * sp * lt); k = 1 + 0.08 * w; o = op * (0.75 + 0.25 * w); }
    else if (a === "spin") { r = rot0 + lt * 14 * sp; }
    else if (a === "float") { dy = Math.sin(2 * Math.PI * 0.22 * sp * lt) * H * 0.025; r = rot0 + Math.sin(lt * 0.5 * sp) * 4; }
    else if (a === "reveal") { const p = clamp(lt / 1.1, 0, 1), e = easeOut(p); k = 0.6 + 0.4 * e; o = op * p; }
    else if (a === "sweep") { dx = (((lt * sp * 0.22) % 1.6) - 0.8) * W; }
    css(el, "transform", `translate(-50%,-50%) translate(${dx.toFixed(1)}px,${dy.toFixed(1)}px) rotate(${r.toFixed(2)}deg) scale(${k.toFixed(4)})`);
    css(el, "opacity", o.toFixed(3));
  }
}// ---- layered capture for the blend modes no browser has (renderer only): paint order of everything drawable
let PAINT = null;
function paintList() {
  if (PAINT) return PAINT;
  const L = [], add = e => { if (e) L.push(e); };
  ["o1", "o2", "grid", "stagebg"].forEach(id => add(document.getElementById(id)));
  document.querySelectorAll("#stageback > .ov").forEach(add);
  document.querySelectorAll(".scene").forEach(sc => { for (const c of sc.children) add(c); });
  document.querySelectorAll("#stagefront > .ov").forEach(add);
  ["capt", "credit", "bar"].forEach(id => add(document.getElementById(id)));
  return (PAINT = L);
}
// visible at this instant (its scene on screen, not fully transparent); the pass visibility flag is NOT looked at:
// __pass() itself hides the other items while a layer is captured alone
const shown = e => { const sc = e.closest(".scene"); return !(sc && !(+sc.style.opacity > 0)) &&
  +getComputedStyle(e).opacity > 0.001; };
// [[paint index, mode, [x, y, w, h], signature]] of the exact-blend layers visible now (rect: the only pixels the
// layer can touch; signature: same string = same pixels as last frame, the capture can be reused)
window.__xb = function () {
  return paintList().map((e, i) => {
    if (!e.dataset || !e.dataset.xblend || !shown(e)) return null;
    const r = e.getBoundingClientRect();
    const x = Math.max(0, Math.floor(r.left) - 2), y = Math.max(0, Math.floor(r.top) - 2);
    const x2 = Math.min(K.w, Math.ceil(r.right) + 2), y2 = Math.min(K.h, Math.ceil(r.bottom) + 2);
    if (x2 <= x || y2 <= y) return null;
    const sig = [e.style.transform, getComputedStyle(e).opacity, (e.closest(".scene") || {}).style?.opacity || 1,
                 [...e.querySelectorAll("img")].map(m => m.getAttribute("src")).join(",")].join("|");
    return [i, e.dataset.xblend, [x, y, x2 - x, y2 - y], sig];
  }).filter(Boolean);
};
// rectangle [x, y, w, h] covering everything visible in paint items [lo, hi) — null when nothing is visible
window.__any = function (lo, hi) {
  let x = 1e9, y = 1e9, x2 = -1e9, y2 = -1e9;
  for (const e of paintList().slice(lo, hi)) {
    if (!shown(e)) continue;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    x = Math.min(x, r.left); y = Math.min(y, r.top); x2 = Math.max(x2, r.right); y2 = Math.max(y2, r.bottom);
  }
  if (x2 <= x) return null;
  x = Math.max(0, Math.floor(x) - 2); y = Math.max(0, Math.floor(y) - 2);
  x2 = Math.min(K.w, Math.ceil(x2) + 2); y2 = Math.min(K.h, Math.ceil(y2) + 2);
  return x2 > x && y2 > y ? [x, y, x2 - x, y2 - y] : null;
};
// show only paint items [lo, hi); transparent = no page / stage background (a layer captured alone)
window.__pass = function (lo, hi, transparent) {
  const st = document.getElementById("stage");
  paintList().forEach((e, i) => {
    e.style.visibility = i >= lo && i < hi ? "" : "hidden";
    if (e.dataset && e.dataset.xblend) {
      if (e.dataset.mbm === undefined) e.dataset.mbm = e.style.mixBlendMode || "";
      e.style.mixBlendMode = transparent && hi - lo === 1 ? "normal" : e.dataset.mbm;
    }
  });
  st.style.background = transparent ? "transparent" : "";
  document.documentElement.style.background = document.body.style.background = transparent ? "transparent" : "";
  return paintList().length;
};
window.__passEnd = function () { window.__pass(0, 1e9, false); };
let pendingImgs = [];
// Draw instant t (seconds). Resolves once fonts and every image on screen are decoded: a captured frame is final.
window.__seek = async function (t) {
  pendingImgs = [];
  seekSync(t);
  await document.fonts.ready;
  const allImgs = [...document.querySelectorAll("#stage img")].filter(i => {
    const sc = i.closest(".scene");
    return (!sc || +sc.style.opacity > 0) && i.complete && i.naturalWidth > 0;
  });
  await Promise.all([
    ...pendingImgs.map(i => i.decode().catch(() => {})),
    ...allImgs.map(i => i.decode().catch(() => {}))
  ]);
  return true;
};
if (!RENDER) {        // PREVIEW = the render: same drawing code, driven by a time bar instead of the renderer
  const st = document.getElementById("stage"), BH = 0;
  const range = document.getElementById("krange"), lbl = document.getElementById("ktime"), btn = document.getElementById("kplay");
  const kplayCenter = document.getElementById("kplay_center");
  if (BAR && INEDITOR) { BAR.style.display = "none"; }
  range.max = K.total;
  playing = false;
  const updatePlayUI = () => {
    if (kplayCenter) {
      if (INEDITOR) {
        kplayCenter.style.display = "none";
      } else {
        if (playing) kplayCenter.classList.add("playing");
        else kplayCenter.classList.remove("playing");
      }
    }
    if (btn) btn.textContent = playing ? "❚❚" : "▶";
  };
  let t0 = performance.now(), pt = 0, drag = false;
  const EDTARGET = INEDITOR ? window.parent : window;
  function post(m) { try { EDTARGET.postMessage(m, "*"); } catch (e) {} }
  const fmt = x => `${Math.floor(x / 60)}:${(x % 60).toFixed(1).padStart(4, "0")}`;
  const fit = () => {
    const pad = INEDITOR ? 10 : 0;
    const aw = Math.max(40, innerWidth - pad * 2), ah = Math.max(40, innerHeight - BH - pad * 2);
    const k = Math.min(aw / K.w, ah / K.h);
    st.style.transform = `scale(${k})`; st.style.left = `${(innerWidth - K.w * k) / 2}px`;
    st.style.top = `${(innerHeight - BH - K.h * k) / 2}px`;
  };
  addEventListener("resize", fit); fit();
  if (INEDITOR) {
    addEventListener("wheel", e => {
      e.preventDefault();
      post({ evt: "wheel", deltaY: e.deltaY, deltaX: e.deltaX, ctrlKey: e.ctrlKey });
    }, { passive: false });
  }
  let lastF = -1;
  const show = x => { pt = clamp(x, 0, K.total); const f = Math.round(pt * K.fps); if (f === lastF) return; lastF = f;
    seekSync(f / K.fps); range.value = pt; lbl.textContent = `${fmt(pt)} / ${fmt(K.total)}`; post({ evt: "time", t: pt }); };
  // SON aperçu a (K.paudio = preview-sounds.m4a: ambyans, son, pa pèsonaj yo, mizik — san vwa)
  const PA = (!INEDITOR && K.paudio) ? document.body.appendChild(Object.assign(document.createElement("audio"),
                                                                   { src: K.paudio, preload: "auto" })) : null;
  const paSync = (go) => { if (!PA) return; try { PA.currentTime = pt; if (go === true) PA.play().catch(() => {});
                                                    else if (go === false) PA.pause(); } catch (e) {} };
  const toggle = (e) => {
    if (e && e.stopPropagation) e.stopPropagation();
    playing = !playing;
    updatePlayUI();
    if (playing) {
      if (pt >= K.total - 0.05) pt = 0;
      t0 = performance.now() - pt * 1000;
    } else {
      document.querySelectorAll("video").forEach(v => { try { v.pause(); } catch(e){} });
    }
    paSync(playing); };
  btn.onclick = toggle;
  if (kplayCenter) kplayCenter.onclick = toggle;
  if (!INEDITOR) st.onclick = toggle;
  addEventListener("keydown", e => {
    if (INEDITOR) {
      if (e.code === "Space" || e.code === "ArrowRight" || e.code === "ArrowLeft") {
        e.preventDefault();
        post({ evt: "keydown", code: e.code, key: e.key, shiftKey: e.shiftKey, ctrlKey: e.ctrlKey });
      }
      return;
    }
    if (e.code === "Space") { e.preventDefault(); toggle(); }
    if (e.code === "ArrowRight" || e.code === "ArrowLeft") {
      show(pt + (e.code === "ArrowRight" ? 1 : -1) / K.fps); t0 = performance.now() - pt * 1000; } });
  range.oninput = () => { drag = true; show(+range.value); t0 = performance.now() - pt * 1000; paSync(); };
  range.onchange = () => { drag = false; };
  const kvol = document.getElementById("kvol"), kvolic = document.getElementById("kvolic"), kvolval = document.getElementById("kvolval");
  if (kvol) {
    let prevKVol = 1;
    const applyVol = (v) => {
      v = Math.max(0, Math.min(2, Math.round(v * 100) / 100));
      kvol.value = v;
      if (kvolval) kvolval.textContent = Math.round(v * 100) + "%";
      if (kvolic) kvolic.textContent = (v <= 0.001) ? "🔇" : (v < 0.5 ? "🔉" : "🔊");
      document.querySelectorAll("video, audio").forEach(a => { try { a.volume = Math.min(1, v); } catch(e){} });
    };
    kvol.oninput = () => { applyVol(+kvol.value); if (+kvol.value > 0.001) prevKVol = +kvol.value; };
    if (kvolic) kvolic.onclick = () => {
      if (+kvol.value > 0.001) { prevKVol = +kvol.value; applyVol(0); }
      else { applyVol(prevKVol || 1); }
    };
  }
  const loop = now => {
    if (playing && !drag) {
      const x = (now - t0) / 1000;
      if (x > K.total + (INEDITOR ? 0.05 : 0.8)) {
        if (INEDITOR) { playing = false; updatePlayUI(); show(K.total); post({ evt: "ended", t: K.total }); }
        else { playing = false; updatePlayUI(); show(0); paSync(false); }
      } else { show(Math.min(x, K.total));
        if (PA && !PA.paused && Math.abs(PA.currentTime - x) > 0.25) { try { PA.currentTime = x; } catch (e) {} } }
    }
    requestAnimationFrame(loop); };
  addEventListener("message", e => {                    // Editè Timeline -> aperçu
    const m = e.data || {};
    if (m.cmd === "seek") { playing = false; updatePlayUI(); btn.textContent = "▶"; lastF = -1; show(+m.t || 0); t0 = performance.now() - pt * 1000; }
    else if (m.cmd === "play") { if (!playing) toggle(); else t0 = performance.now() - pt * 1000; }
    else if (m.cmd === "pause") { if (playing) toggle(); }
    else if (m.cmd === "fit") { fit(); }
    else if (m.cmd === "highlight") { document.querySelectorAll(".scene").forEach(s => {
      s.style.outline = ""; }); }
  });
  document.querySelectorAll(".scene").forEach(s => s.addEventListener("click", ev => {
    const el = ev.target.closest("[data-k]");
    post({ evt: "click", scene: s.dataset.id, spec_index: +s.dataset.s, element: el ? el.dataset.k : null });
  }, true));
  show(0);
  post({ evt: "ready", kadans: K });
  requestAnimationFrame(loop);
  // #autoplay / ?autoplay: jwe touswit san klik (zouti ki anrejistre paj la). Pou yon vrè rann imaj pa imaj,
  // sèvi ak #render + window.__seek(t) — san sa yon kaptiv jwenn sèlman bouton Play la sou sèn nan (2026-10-26).
  if (!INEDITOR && (location.hash.indexOf("autoplay") >= 0 || /[?&]autoplay\b/.test(location.search))) toggle();
} else { seekSync(0); }
"""


_LUT = {
    "sinema": "contrast(1.1) saturate(1.15) brightness(0.98)",
    "cho": "sepia(0.25) saturate(1.3) brightness(1.05)",
    "fret": "saturate(0.9) brightness(1.02) hue-rotate(-12deg)",
    "vintage": "sepia(0.4) contrast(0.92) saturate(0.82)",
    "nwa-blan": "grayscale(1) contrast(1.1)",
    "sepya": "sepia(0.8)",
    "dramatik": "contrast(1.3) brightness(0.9) saturate(1.1)",
    "pastel": "saturate(0.72) brightness(1.1)",
    "teal-orange": "contrast(1.08) saturate(1.2) hue-rotate(-6deg)",
}


def _curve_to_table(pts: list, master_pts: list | None = None, samples: int = 16) -> str:
    """Konvèti pwen koub [[x, y], ...] an valè tab feComponentTransfer (16 echantiyon 0..1)."""
    def _interp(p_list: list, x: float) -> float:
        if not p_list:
            return x
        try:
            sp = sorted([[float(p[0]), float(p[1])] for p in p_list if len(p) >= 2], key=lambda p: p[0])
        except (ValueError, TypeError):
            return x
        if not sp:
            return x
        if x <= sp[0][0]:
            return max(0.0, min(1.0, sp[0][1]))
        if x >= sp[-1][0]:
            return max(0.0, min(1.0, sp[-1][1]))
        for i in range(len(sp) - 1):
            x0, y0 = sp[i][0], sp[i][1]
            x1, y1 = sp[i + 1][0], sp[i + 1][1]
            if x0 <= x <= x1:
                t = (x - x0) / max(1e-6, (x1 - x0))
                return max(0.0, min(1.0, y0 + t * (y1 - y0)))
        return x

    out = []
    for k in range(samples):
        x = k / float(samples - 1)
        y = _interp(pts, x)
        if master_pts:
            y = _interp(master_pts, y)
        out.append(f"{y:.3f}")
    return " ".join(out)


def _tonemap_table(mode: str = "reinhard", samples: int = 16) -> str:
    """Tone-mapping S-curve pou HDR -> SDR oswa kontras sinema."""
    out = []
    mode = (str(mode or "")).lower()
    for k in range(samples):
        x = k / float(samples - 1)
        if mode in ("reinhard", "hdr"):
            y = (x * 1.5) / (1.0 + 0.5 * x)
        elif mode in ("filmic", "hable"):
            y = (x * x * (3.0 - 2.0 * x))
        elif mode == "mobius":
            y = x if x < 0.6 else 0.6 + 0.4 * math.tanh((x - 0.6) / 0.4)
        else:
            y = x
        out.append(f"{max(0.0, min(1.0, y)):.3f}")
    return " ".join(out)


def _grade(fx: dict | None, lut: str | None, uid: str) -> tuple[str, str]:
    """Etalonaj koulè PWOFESYONÈL. Retounen (CSS filter, defs SVG).
    CSS pote sa navigatè a fè vit (blur/limye/kontras/satirasyon/vibrance/hue/gri/sepya/LUT).
    SVG (filter url) pote sa CSS pa ka fè: temperati/tint (feColorMatrix),
    lift/gamma/gain pou lonbraj-mitan-klète (feComponentTransfer), ak sharpen pou KALITE (feConvolveMatrix).
    enhance=true = yon koutje kalite otomatik (sharpen + yon ti kontras/satirasyon/gain)."""
    fx = fx or {}

    def num(k, d):
        try:
            return float(fx.get(k, d))
        except (TypeError, ValueError):
            return d
    enhance = bool(fx.get("enhance"))
    css = []
    if num("blur", 0) > 0:
        css.append(f"blur({num('blur', 0):.1f}px)")
    bright = num("brightness", 1) * (2.0 ** num("exposure", 0))     # ekspozisyon an stop (2^EV)
    if abs(bright - 1) > 1e-3:
        css.append(f"brightness({bright:.3f})")
    contrast = num("contrast", 1) * (1.06 if enhance else 1.0)
    if abs(contrast - 1) > 1e-3:
        css.append(f"contrast({contrast:.3f})")
    sat = num("saturate", 1) * num("vibrance", 1) * (1.08 if enhance else 1.0)
    if abs(sat - 1) > 1e-3:
        css.append(f"saturate({sat:.3f})")
    if abs(num("hue", 0)) > 1e-3:
        css.append(f"hue-rotate({num('hue', 0):.1f}deg)")
    if num("grayscale", 0) > 0:
        css.append(f"grayscale({num('grayscale', 0):.2f})")
    if num("sepia", 0) > 0:
        css.append(f"sepia({num('sepia', 0):.2f})")
    if lut and lut in _LUT:
        css.append(_LUT[lut])

    # --- Pati avanse (SVG) ---
    temp = num("temperature", 0); tint = num("tint", 0)
    lift = num("lift", 0); gamma = num("gamma", 1); gain = num("gain", 1)
    sharpen = num("sharpen", 0)
    if enhance and sharpen <= 0:
        sharpen = 0.7
    if enhance:
        gain *= 1.04
    prims = []; last = "SourceGraphic"
    if abs(temp) > 1e-3 or abs(tint) > 1e-3:
        rr = 1 + 0.25 * (temp / 100.0)                    # cho = plis wouj, mwens ble
        bb = 1 - 0.25 * (temp / 100.0)
        gg = 1 - 0.20 * (tint / 100.0)                    # tint + = mwens vèt (majenta)
        mat = (f"{rr:.4f} 0 0 0 0  0 {gg:.4f} 0 0 0  "
               f"0 0 {bb:.4f} 0 0  0 0 0 1 0")
        prims.append(f'<feColorMatrix in="{last}" type="matrix" values="{mat}" result="cm"/>'); last = "cm"
    if abs(lift) > 1e-3 or abs(gamma - 1) > 1e-3 or abs(gain - 1) > 1e-3:
        expn = 1.0 / gamma if gamma > 1e-3 else 1.0       # out = amp * in^exp + off
        amp = max(0.0, gain); off = lift
        fn = "".join(f'<feFunc{ch} type="gamma" amplitude="{amp:.4f}" '
                     f'exponent="{expn:.4f}" offset="{off:.4f}"/>' for ch in "RGB")
        prims.append(f'<feComponentTransfer in="{last}" result="ct">{fn}</feComponentTransfer>'); last = "ct"
    if sharpen > 0:
        a = sharpen * 0.5
        k = (f"0 {-a:.4f} 0  {-a:.4f} {1 + 4 * a:.4f} {-a:.4f}  0 {-a:.4f} 0")
        prims.append(f'<feConvolveMatrix in="{last}" order="3" preserveAlpha="true" '
                     f'divisor="1" kernelMatrix="{k}" result="sh"/>'); last = "sh"

    # Courbes RVB paramétriques (RGB Spline Curves)
    curves = fx.get("curves")
    if isinstance(curves, dict) and curves:
        m_pts = curves.get("master") or curves.get("rgb") or []
        r_pts = curves.get("red") or curves.get("r") or []
        g_pts = curves.get("green") or curves.get("g") or []
        b_pts = curves.get("blue") or curves.get("b") or []
        if m_pts or r_pts or g_pts or b_pts:
            r_tbl = _curve_to_table(r_pts, m_pts)
            g_tbl = _curve_to_table(g_pts, m_pts)
            b_tbl = _curve_to_table(b_pts, m_pts)
            prims.append(
                f'<feComponentTransfer in="{last}" result="crv">'
                f'<feFuncR type="table" tableValues="{r_tbl}"/>'
                f'<feFuncG type="table" tableValues="{g_tbl}"/>'
                f'<feFuncB type="table" tableValues="{b_tbl}"/>'
                f'</feComponentTransfer>'
            )
            last = "crv"

    # Tone Mapping HDR -> SDR Rec.709
    tonemap = fx.get("tonemap") or fx.get("hdr_tonemap")
    if tonemap:
        tm_tbl = _tonemap_table(str(tonemap))
        prims.append(
            f'<feComponentTransfer in="{last}" result="tm">'
            f'<feFuncR type="table" tableValues="{tm_tbl}"/>'
            f'<feFuncG type="table" tableValues="{tm_tbl}"/>'
            f'<feFuncB type="table" tableValues="{tm_tbl}"/>'
            f'</feComponentTransfer>'
        )
        last = "tm"

    # Directional Motion Blur
    mb = fx.get("motion_blur") or fx.get("blur_dir")
    if mb:
        try:
            if isinstance(mb, (int, float)):
                ang = math.radians(float(fx.get("motion_angle", 0) or 0))
                dx = abs(float(mb) * math.cos(ang))
                dy = abs(float(mb) * math.sin(ang))
            elif isinstance(mb, (list, tuple)) and len(mb) >= 2:
                dx, dy = abs(float(mb[0])), abs(float(mb[1]))
            else:
                dx, dy = 0.0, 0.0
            if dx > 0.01 or dy > 0.01:
                prims.append(f'<feGaussianBlur in="{last}" stdDeviation="{dx:.2f} {dy:.2f}" result="mb"/>')
                last = "mb"
        except (ValueError, TypeError):
            pass
    svg = ""
    if prims:
        css.append(f"url(#{uid})")
        svg = (f'<filter id="{uid}" color-interpolation-filters="sRGB" '
               f'x="-8%" y="-8%" width="116%" height="116%">{"".join(prims)}</filter>')
    return " ".join(css), svg


def _fx_filter(fx: dict | None, lut: str | None) -> str:
    """Back-compat: CSS sèlman (san pati SVG avanse a)."""
    css = _grade(fx, lut, "_x")[0]
    return " ".join(p for p in css.split(" ") if not p.startswith("url(#_x"))


def _kf_attr(c: dict, x: float, y: float, rot: float, op: float) -> str:
    """Keyframes (animasyon clip): data-kf = {b: valè baz, k: lis kle triye}.
    Chak kle = {t 0..1 (fraksyon dire clip), x?, y?, rotate?, scale?, opacity?}."""
    ks = c.get("keys")
    if not isinstance(ks, list) or len(ks) < 1:
        return ""
    base = {"x": x, "y": y, "rot": rot, "sc": float(c.get("scale", 1) or 1), "op": op}
    norm = []
    for k in ks:
        if not isinstance(k, dict):
            continue
        o = {"t": max(0.0, min(1.0, float(k.get("t", 0) or 0)))}
        for src, dst in (("x", "x"), ("y", "y"), ("rotate", "rot"), ("scale", "sc"), ("opacity", "op")):
            if k.get(src) is not None:
                try:
                    o[dst] = float(k[src])
                except (TypeError, ValueError):
                    pass
        ease = k.get("ease")                           # ease/bezye sou segman ki soti nan kle sa a
        if isinstance(ease, (list, tuple)) and len(ease) == 4:
            try:
                o["e"] = [float(v) for v in ease]
            except (TypeError, ValueError):
                pass
        elif isinstance(ease, str) and ease:
            o["e"] = ease
        norm.append(o)
    norm.sort(key=lambda z: z["t"])
    payload = json.dumps({"b": base, "k": norm}, separators=(",", ":"))
    return f' data-kf="{html.escape(payload, quote=True)}"'


def _mask_css(c: dict) -> str:
    """Mask fòm sou clip la (CSS clip-path oswa mask-image feathered). shape = circle | ellipse | inset/rect.
    Paramèt yo nòmalize 0..1 (fraksyon bwat la). feather = adousi kontou an px."""
    m = c.get("mask")
    if not isinstance(m, dict):
        return ""
    shape = str(m.get("shape") or "").lower()

    def pct(key, d):
        try:
            return f"{max(0.0, float(m.get(key, d))) * 100:.2f}%"
        except (TypeError, ValueError):
            return f"{d * 100:.2f}%"

    try:
        feather = max(0.0, float(m.get("feather", 0) or 0))
    except (TypeError, ValueError):
        feather = 0.0

    if shape == "circle":
        if feather > 0:
            return (f"-webkit-mask-image:radial-gradient(circle at {pct('cx', 0.5)} {pct('cy', 0.5)}, "
                    f"#000 calc({pct('r', 0.4)} - {feather:.1f}px), transparent {pct('r', 0.4)});"
                    f"mask-image:radial-gradient(circle at {pct('cx', 0.5)} {pct('cy', 0.5)}, "
                    f"#000 calc({pct('r', 0.4)} - {feather:.1f}px), transparent {pct('r', 0.4)});")
        return f"clip-path:circle({pct('r', 0.4)} at {pct('cx', 0.5)} {pct('cy', 0.5)});"

    if shape == "ellipse":
        if feather > 0:
            return (f"-webkit-mask-image:radial-gradient(ellipse {pct('rx', 0.4)} {pct('ry', 0.3)} at {pct('cx', 0.5)} {pct('cy', 0.5)}, "
                    f"#000 calc(100% - {feather:.1f}px), transparent 100%);"
                    f"mask-image:radial-gradient(ellipse {pct('rx', 0.4)} {pct('ry', 0.3)} at {pct('cx', 0.5)} {pct('cy', 0.5)}, "
                    f"#000 calc(100% - {feather:.1f}px), transparent 100%);")
        return f"clip-path:ellipse({pct('rx', 0.4)} {pct('ry', 0.3)} at {pct('cx', 0.5)} {pct('cy', 0.5)});"

    if shape in ("inset", "rect"):
        rad = m.get("radius")
        rr = ""
        if rad is not None:
            try:
                rr = f" round {max(0.0, float(rad)) * 100:.2f}%"
            except (TypeError, ValueError):
                rr = ""
        if feather > 0:
            top_p = pct('top', 0.1); right_p = pct('right', 0.1)
            bot_p = pct('bottom', 0.1); left_p = pct('left', 0.1)
            return (f"-webkit-mask-image:linear-gradient(to bottom, transparent, #000 {feather:.1f}px calc(100% - {feather:.1f}px), transparent);"
                    f"mask-image:linear-gradient(to bottom, transparent, #000 {feather:.1f}px calc(100% - {feather:.1f}px), transparent);"
                    f"clip-path:inset({top_p} {right_p} {bot_p} {left_p}{rr});")
        return (f"clip-path:inset({pct('top', 0.1)} {pct('right', 0.1)} "
                f"{pct('bottom', 0.1)} {pct('left', 0.1)}{rr});")
    return ""


def sub_cues(spec: dict) -> list[dict]:
    """Sou-tit eksplisit (editè sou-tit): lis {s, e, text, pos?} triye, valide."""
    out = []
    for q in (spec.get("sub_cues") or []):
        if not isinstance(q, dict):
            continue
        txt = str(q.get("text") or "").strip()
        if not txt:
            continue
        try:
            s = max(0.0, float(q.get("s", 0) or 0)); e = float(q.get("e", s + 2) or (s + 2))
        except (TypeError, ValueError):
            continue
        if e <= s:
            e = s + 1.5
        pos = q.get("pos") if q.get("pos") in ("bottom", "top", "middle") else None
        cue = {"s": round(s, 3), "e": round(e, 3), "text": txt}
        if pos:
            cue["pos"] = pos
        out.append(cue)
    out.sort(key=lambda z: z["s"])
    return out


def _chroma_svg(c: dict, uid: str) -> tuple[str, str]:
    """Chroma key (green/blue screen) APWOKSIMATIF via SVG feColorMatrix:
    kalkile yon alpha ki soti nan dominans koulè kle a, epi koupe l (feFuncA lineyè).
    Retounen (url token, defs SVG). color=green|blue; amount=fòs; threshold/smooth=kontou."""
    ck = c.get("chroma")
    if not isinstance(ck, dict) or ck.get("on") is False:
        return "", ""

    def num(k, d):
        try:
            return float(ck.get(k, d))
        except (TypeError, ValueError):
            return d
    color = str(ck.get("color") or "green").lower()
    amount = max(0.0, min(1.0, num("amount", 0.5)))
    threshold = max(0.0, min(1.0, num("threshold", 0.2)))
    smooth = max(0.01, min(1.0, num("smooth", 0.2)))
    sup = 0.5 + amount * 0.9                               # konbyen R/B siprime koulè kle a
    if color == "blue":
        arow = f"{-sup:.3f} {-sup:.3f} 1 0 0"             # A = B - sup*R - sup*G
    else:
        arow = f"{-sup:.3f} 1 {-sup:.3f} 0 0"            # A = G - sup*R - sup*B
    slope = -1.0 / smooth                                  # A wo (kle) → alpha ba
    intercept = (threshold + smooth) / smooth
    svg = (f'<filter id="{uid}" color-interpolation-filters="sRGB">'
           f'<feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  {arow}"/>'
           f'<feComponentTransfer><feFuncA type="linear" slope="{slope:.4f}" '
           f'intercept="{intercept:.4f}"/></feComponentTransfer></filter>')
    return f"url(#{uid})", svg


def _sramp_attr(c: dict) -> str:
    """Speed ramp (vitès kap chanje): data-sramp = lis {t 0..1, v miltiplikatè vitès} triye."""
    sk = c.get("speedKeys")
    if not isinstance(sk, list) or len(sk) < 1:
        return ""
    norm = []
    for k in sk:
        if not isinstance(k, dict):
            continue
        try:
            norm.append({"t": max(0.0, min(1.0, float(k.get("t", 0) or 0))),
                         "v": max(0.05, float(k.get("v", 1) or 1))})
        except (TypeError, ValueError):
            continue
    if not norm:
        return ""
    norm.sort(key=lambda z: z["t"])
    return f' data-sramp="{html.escape(json.dumps(norm, separators=(",", ":")), quote=True)}"'


def _mcam_cuts(c: dict) -> list[dict]:
    """Multicam: lis koup {t 0..1 (fraksyon dire clip), a index ang} triye."""
    out = []
    for q in (c.get("cuts") or []):
        if not isinstance(q, dict):
            continue
        try:
            t = max(0.0, min(1.0, float(q.get("t", 0) or 0))); aa = int(q.get("a", 0))
        except (TypeError, ValueError):
            continue
        out.append({"t": round(t, 4), "a": max(0, aa)})
    out.sort(key=lambda z: z["t"])
    return out


def _vig_overlay(vig: float) -> str:
    """Vignette: yon radyal nwa ki fonse sou kwen yo (vig = fòs 0..1)."""
    inner = 30 + (1 - vig) * 35                      # mwens vig → nwa a kòmanse pi lwen
    return (f'<div style="position:absolute;inset:0;pointer-events:none;'
            f'background:radial-gradient(ellipse at center,rgba(0,0,0,0) {inner:.0f}%,'
            f'rgba(0,0,0,{vig:.3f}) 120%)"></div>')


def _tracks_html(spec: dict, media: dict | None = None, base: Path | None = None, out_dir: Path | None = None) -> str:
    from .media import resolve
    IMG = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg")
    VID = (".mp4", ".webm", ".mov", ".m4v", ".mkv")

    def _rsrc(s):                                            # rezoud yon chemen medya → url paj la
        for b_cand in (out_dir, base):
            if not b_cand:
                continue
            try:
                rp = resolve(s, b_cand)
                if rp and Path(rp).is_file():
                    return _url(Path(rp), out_dir)
            except Exception:
                continue
        return html.escape(str(s))
    els = []
    grade_defs = []                                          # filtè SVG etalonaj pa clip
    gi = 0
    for tk in (spec.get("tracks") or []):
        if tk.get("hidden"):
            continue
        kind = tk.get("kind")
        for c in (tk.get("clips") or []):
            k = c.get("kind") or c.get("type") or kind
            if k in ("audio", "sfx", "music", "voice"):
                continue
            try:
                start = float(c.get("start", 0)); dur = float(c.get("dur", 2))
                x = float(c.get("x", 0.5)); y = float(c.get("y", 0.5))
                w = float(c.get("w", 0.6 if k == "text" else (0.85 if k == "video" else 0.3)))
                op = float(c.get("opacity", 1)); rot = float(c.get("rotate", 0))
            except (TypeError, ValueError):
                continue
            blend = c.get("blend", "normal")
            nb = NATIVE_BLEND.get(blend) or PREVIEW_BLEND.get(blend, "normal")
            gi += 1
            filt, _gsvg = _grade(c.get("fx"), c.get("lut"), f"kgrade{gi}")
            if _gsvg:
                grade_defs.append(_gsvg)
            _ck_url, _ck_svg = _chroma_svg(c, f"ck{gi}")   # chroma key anvan etalonaj
            if _ck_svg:
                grade_defs.append(_ck_svg)
                filt = (_ck_url + " " + filt).strip()
            if c.get("shadow"):
                filt = (filt + f" drop-shadow(0 0 {c.get('shadowBlur', 10)}px {c.get('shadowColor', '#000')})").strip()
            pos_style = (f"position:absolute;left:{x * 100:.3f}%;top:{y * 100:.3f}%;width:{w * 100:.3f}%;"
                         f"transform:translate(-50%,-50%) rotate({rot:.1f}deg);opacity:{op:.3f};mix-blend-mode:{nb};")
            mask_css = _mask_css(c)
            if mask_css:
                pos_style += mask_css
            filt_style = f"filter:{filt};" if filt else ""
            style = pos_style + filt_style
            try:
                vig = max(0.0, min(1.0, float((c.get("fx") or {}).get("vignette", 0) or 0)))
            except (TypeError, ValueError):
                vig = 0.0
            xb = f' data-xblend="{blend}"' if blend in PREVIEW_BLEND else ""
            kf = _kf_attr(c, x, y, rot, op)                # animasyon keyframe (opsyonèl)
            sr = _sramp_attr(c)                            # speed ramp (video, opsyonèl)
            if k == "text":
                txt = html.escape(c.get("text") or c.get("label") or "")
                col = c.get("color", "#ffffff"); size = c.get("size", 48)
                font = c.get("font") or spec["brand"]["font_title"]
                grad = ""
                if c.get("gradient"):
                    grad = (f"background:linear-gradient(90deg,{c.get('grad1', '#8b5cf6')},{c.get('grad2', '#0098ff')});"
                            f"-webkit-background-clip:text;background-clip:text;color:transparent;")
                inner = (f'<div style="font-family:&quot;{html.escape(font)}&quot;,sans-serif;font-size:{size}px;'
                         f'font-weight:800;line-height:1.12;text-align:center;color:{col};{grad}">{txt}</div>')
                els.append(f'<div class="tclip" data-start="{start}" data-dur="{dur}"{kf} style="{style}">{inner}</div>')
            elif k == "roll" or c.get("roll"):
                txt = c.get("text") or c.get("label") or ""
                items = c.get("items") or []
                col = c.get("color", "#ffffff"); size = c.get("size", 36)
                font = c.get("font") or spec["brand"]["font_title"]
                role_col = c.get("role_color", "#a79bc8")
                roll_items = []
                if items and isinstance(items, list):
                    for it in items:
                        if isinstance(it, dict):
                            r = html.escape(str(it.get("role") or ""))
                            n = html.escape(str(it.get("name") or ""))
                            roll_items.append(
                                f'<div style="display:flex;width:100%;max-width:900px;justify-content:center;gap:36px;margin-bottom:18px;">'
                                f'<div style="color:{role_col};font-size:{round(size*0.75)}px;text-transform:uppercase;letter-spacing:1.5px;text-align:right;flex:1;">{r}</div>'
                                f'<div style="color:{col};font-size:{size}px;font-weight:700;text-align:left;flex:1.2;">{n}</div>'
                                f'</div>'
                            )
                        elif isinstance(it, str):
                            roll_items.append(f'<div style="color:{col};font-size:{size}px;margin-bottom:14px;font-weight:600;">{html.escape(it)}</div>')
                elif txt:
                    for line in str(txt).splitlines():
                        if line.strip():
                            roll_items.append(f'<div style="color:{col};font-size:{size}px;margin-bottom:14px;font-weight:600;">{html.escape(line)}</div>')
                inner_roll = "".join(roll_items) or f'<div style="color:{col};font-size:{size}px;">Kadans Credits</div>'
                roll_style = f"overflow:hidden;height:100%;{style}"
                inner = (f'<div class="kroll-inner" style="width:100%;height:auto;display:flex;flex-direction:column;align-items:center;'
                         f'font-family:&quot;{html.escape(font)}&quot;,sans-serif;will-change:transform;">{inner_roll}</div>')
                els.append(f'<div class="tclip" data-start="{start}" data-dur="{dur}" data-roll="1"{kf} style="{roll_style}">{inner}</div>')
            elif k == "crawl" or c.get("crawl"):
                txt = html.escape(c.get("text") or c.get("headline") or c.get("label") or "")
                col = c.get("color", "#ffffff"); size = c.get("size", 34)
                font = c.get("font") or spec["brand"]["font_title"]
                bg_bar = c.get("bg_bar", "rgba(18, 13, 31, 0.85)")
                crawl_style = f"overflow:hidden;white-space:nowrap;background:{bg_bar};padding:10px 0;{style}"
                inner = (f'<div class="kcrawl-inner" style="display:inline-block;white-space:nowrap;will-change:transform;'
                         f'font-family:&quot;{html.escape(font)}&quot;,sans-serif;font-size:{size}px;font-weight:700;color:{col};">{txt}</div>')
                els.append(f'<div class="tclip" data-start="{start}" data-dur="{dur}" data-crawl="1"{kf} style="{crawl_style}">{inner}</div>')
            elif isinstance(c.get("angles"), list) and c.get("angles"):
                cuts = _mcam_cuts(c)                         # multicam: plizyè kamera + koup
                first = cuts[0]["a"] if cuts else 0
                inner = []
                for ai, ang in enumerate(c["angles"]):
                    if not isinstance(ang, dict) or not ang.get("src"):
                        continue
                    asrc = _rsrc(ang["src"])
                    try:
                        ain = max(0.0, float(ang.get("in", 0) or 0))
                    except (TypeError, ValueError):
                        ain = 0.0
                    hide = "" if ai == first else "display:none;"
                    inner.append(f'<video data-ang="{ai}" data-in="{ain:.3f}" src="{asrc}" muted playsinline '
                                 f'preload="auto" style="width:100%;{hide}{filt_style}"></video>')
                cuts_attr = html.escape(json.dumps(cuts, separators=(",", ":")), quote=True)
                els.append(f'<div class="tclip mcam" data-start="{start}" data-dur="{dur}"{kf} '
                           f'data-cuts="{cuts_attr}" style="{pos_style}">{"".join(inner)}'
                           f'{_vig_overlay(vig) if vig > 0 else ""}</div>')
            elif c.get("src"):
                suf = Path(c["src"]).suffix.lower()
                resolved_p = None
                for b_cand in (out_dir, base):
                    if not b_cand:
                        continue
                    try:
                        rp = resolve(c["src"], b_cand)
                        if rp and Path(rp).is_file():
                            resolved_p = Path(rp)
                            break
                    except Exception:
                        continue
                src = _url(resolved_p, out_dir) if resolved_p else html.escape(str(c["src"]))
                if suf in IMG:
                    if vig > 0:
                        inner = (f'<img src="{src}"{xb} style="width:100%;display:block;{filt_style}">'
                                 f'{_vig_overlay(vig)}')
                        els.append(f'<div class="tclip" data-start="{start}" data-dur="{dur}"{kf} '
                                   f'style="{pos_style}">{inner}</div>')
                    else:
                        els.append(f'<img class="tclip" data-start="{start}" data-dur="{dur}"{kf} src="{src}"{xb} '
                                   f'style="{style}">')
                elif suf in VID:
                    _sp = clip_speed(c)
                    _in = max(0.0, float(c.get("in", 0) or 0)) if str(c.get("in", 0)).replace(".", "", 1).isdigit() else 0.0
                    if vig > 0:
                        inner = (f'<video src="{src}" muted playsinline preload="auto"{xb} '
                                 f'style="width:100%;display:block;{filt_style}"></video>{_vig_overlay(vig)}')
                        els.append(f'<div class="tclip" data-start="{start}" data-dur="{dur}"{kf}{sr} '
                                   f'data-speed="{_sp:.3f}" data-in="{_in:.3f}" style="{pos_style}">{inner}</div>')
                    else:
                        els.append(f'<video class="tclip" data-start="{start}" data-dur="{dur}"{kf}{sr} data-speed="{_sp:.3f}" data-in="{_in:.3f}" src="{src}" muted playsinline preload="auto"{xb} '
                                   f'style="{style}"></video>')
                elif suf in (".html", ".htm") or k == "html" or c.get("html"):
                    raw_html = c.get("html") or ""
                    if not raw_html and resolved_p and resolved_p.is_file():
                        try:
                            raw_html = resolved_p.read_text(encoding="utf-8")
                        except OSError:
                            raw_html = f'<div class="media missing">[HTML {html.escape(c.get("src", ""))}]</div>'
                    if "<body" in raw_html.lower():
                        m_b = re.search(r'<body[^>]*>(.*?)</body>', raw_html, re.DOTALL | re.IGNORECASE)
                        styles_h = "\n".join(re.findall(r'<style[^>]*>.*?</style>', raw_html, re.DOTALL | re.IGNORECASE))
                        scripts_h = "\n".join(re.findall(r'<script[^>]*>.*?</script>', raw_html, re.DOTALL | re.IGNORECASE))
                        b_in = m_b.group(1) if m_b else raw_html
                        raw_html = f"{styles_h}\n{b_in}\n{scripts_h}"
                    inner = f'<div class="htmlwrap" style="width:100%;height:100%;overflow:hidden;{filt_style}">{raw_html}</div>'
                    els.append(f'<div class="tclip htmlclip" data-start="{start}" data-dur="{dur}"{kf} style="{pos_style}">{inner}</div>')
    defs = (f'<svg width="0" height="0" style="position:absolute;pointer-events:none" aria-hidden="true">'
            f'<defs>{"".join(grade_defs)}</defs></svg>') if grade_defs else ""
    return defs + "".join(els)



def clip_speed(c: dict) -> float:
    """Vitès yon klip track (0.25-4, 1 = nòmal) — valè ki pa yon nonm = 1."""
    try:
        return max(0.25, min(4.0, float(c.get("speed", 1) or 1)))
    except (TypeError, ValueError):
        return 1.0


def build_html(spec: dict, tl: list[dict] | None = None, base: str | Path | None = None,
               media: dict | None = None, out_dir: str | Path | None = None, preview_audio: str | None = None) -> str:
    """Composition page for a (validated or raw) spec. tl = timeline (default: estimated from the voice lines).
    base = folder relative paths in the spec (logo, src) resolve against. media = {scene id: {dir, count, fps}}
    from media.prepare(). out_dir = folder the page will be saved in (links to media are made relative to it)."""
    if "w" not in spec:
        spec = validate(spec)
    tl = tl or _timeline(spec)
    base = Path(base) if base else None
    out_dir = Path(out_dir) if out_dir else None
    b, c = spec["brand"], spec["brand"]["colors"]
    logo = _logo_html(b["logo"], base, b["name"])
    tw = track_words(spec, base, out_dir) if (spec.get("tracks") and spec.get("captions") is not False) else []
    cap_lines = caption_lines(tl, caption_config(spec), tw) if spec.get("captions") else []
    if any(x.get("rig") for x in tl):                 # LIMYÈ OTOMATIK: koulè imaj fon chak sèn → pèsonaj yo
        from .motion import resolve_lights as _lights
        tl = [dict(x, rig=_lights(x["rig"], spec["scenes"][i], base)) if x.get("rig") and i < len(spec["scenes"])
              else x for i, x in enumerate(tl)]
    if tw:                       # narasyon sou yon pis: eleman / *mo* sèn yo parèt lè VWA SA A di yo tou
        tl = [x if x.get("words") else dict(x, words=[w for w in tw if x["start"] <= w["s"] < x["start"] + x["dur"]])
              for x in tl]
    scenes = "\n".join(
        f'<section class="scene sc-{sc["type"]}" data-s="{i}" data-id="{html.escape(sc["id"])}" data-type="{sc["type"]}"'
        f' data-start="{tl[i]["start"]}" data-duration="{tl[i]["dur"]}" data-trans="{sc.get("transition") or spec["transition"]}">\n'
        f'{_background_html(sc.get("background"), sc["id"] + "#bg", spec, media, base, out_dir)}'
        f'{_overlays_html(sc.get("overlays"), sc["id"], spec, media, base, out_dir, "back")}'
        f'{_emphasis(_scene_body(sc, spec, logo, media, base, out_dir, tl[i]), tl[i])}\n'
        f'{_overlays_html(sc.get("overlays"), sc["id"], spec, media, base, out_dir, "front")}</section>'
        for i, sc in enumerate(spec["scenes"]))
    stage_bg = _background_html(spec.get("background"), "stage#bg", spec, media, base, out_dir)
    stage_back = _overlays_html(spec.get("overlays"), "stage", spec, media, base, out_dir, "back")
    stage_front = _overlays_html(spec.get("overlays"), "stage", spec, media, base, out_dir, "front")
    tracks_html = _tracks_html(spec, media, base, out_dir)
    clips = {k: {"url": _url(Path(v["dir"]), out_dir), "count": v["count"], "fps": v["fps"]}
             for k, v in (media or {}).items()}
    credit = ""
    if spec["credit"]:
        icon = (ASSETS / "wasdev-icon.svg").read_text(encoding="utf-8")
        word = CREDIT.get(spec["lang"].split("-")[0], CREDIT["en"])
        credit = f'<div id="credit">{icon}<span>{html.escape(word)} <b>Kadans WASDEV</b></span></div>'
    meta = {"w": spec["w"], "h": spec["h"], "fps": spec["fps"], "total": _total(tl, spec), "scenes": [dict(x, spec_index=i) for i, x in enumerate(tl)],
            "sfx_cues": (events(spec, tl) if spec.get("sfx") else []), "clips": clips, "tile": round(80 * min(spec["w"], spec["h"]) / 1080, 3),
            "captions": cap_lines,
            "cap_style": (spec.get("captions") or {}).get("style"),
            "sub_cues": sub_cues(spec), "sub_style": (spec.get("sub_style") or {}),
            "title": spec["title"], "engine": "Kadans WASDEV"}
    if any(x.get("rig") for x in tl):                 # mouvman pèsonaj yo (menm tab ak Python an)
        meta["rigm"] = MOTIONS
    if preview_audio:                                  # aperçu: son sèn yo (audio.preview_sounds), san vwa
        meta["paudio"] = preview_audio
    portrait = " portrait" if spec["h"] > spec["w"] else ""
    libs = list(dict.fromkeys((spec.get("libs") or [])
                               + [l for sc in spec["scenes"] for l in (sc.get("libs") or [])]
                               + (["chart"] if any(sc["type"] == "chart" for sc in spec["scenes"]) else [])
                               + (["lottie"] if any(sc["type"] == "lottie" for sc in spec["scenes"]) else [])))
    _lp = []
    for l in libs:
        if l not in LIB_FILES:
            continue
        _srcf = ASSETS / "vendor" / LIB_FILES[l]
        if out_dir is not None:                       # kopye lib la akote paj la (menm orijin, pa pwoblem file://)
            (out_dir / "vendor").mkdir(parents=True, exist_ok=True)
            _dst = out_dir / "vendor" / LIB_FILES[l]
            if not _dst.exists():
                try:
                    shutil.copy2(_srcf, _dst)
                except OSError:
                    pass
            _ref = "vendor/" + LIB_FILES[l]
        else:
            _ref = _url(_srcf, None)
        _lp.append(f'<script src="{_ref}"></script>')
    lib_tags = "".join(_lp)
    return f"""<!doctype html>
<html lang="{html.escape(spec['lang'])}"><head><meta charset="utf-8">
<meta name="generator" content="Kadans WASDEV">
<title>{html.escape(spec['title'])}</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%238b5cf6'/%3E%3Cstop offset='1' stop-color='%230098ff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect x='4' y='4' width='56' height='56' rx='14' fill='%231d1230'/%3E%3Cpath d='M24 20L12 32l12 12' fill='none' stroke='url(%23g)' stroke-width='6' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M40 20l12 12-12 12' fill='none' stroke='url(%23g)' stroke-width='6' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M36 14L28 50' fill='none' stroke='%23b794ff' stroke-width='5' stroke-linecap='round'/%3E%3C/svg%3E">
<style>{font_faces(spec, base, out_dir)}
{_css(spec)}</style>{lib_tags}</head>
<body>
<div id="stage" class="{portrait.strip()}" data-width="{spec['w']}" data-height="{spec['h']}" data-fps="{spec['fps']}" data-duration="{_total(tl, spec)}">
<div class="orb" id="o1" style="width:{min(spec['w'], spec['h']) * 1.1:.0f}px;height:{min(spec['w'], spec['h']) * 1.1:.0f}px;background:radial-gradient(closest-side,{c['primary']}aa,{c['primary']}40 45%,transparent)"></div>
<div class="orb" id="o2" style="width:{min(spec['w'], spec['h']) * 1.0:.0f}px;height:{min(spec['w'], spec['h']) * 1.0:.0f}px;background:radial-gradient(closest-side,{c['accent']}99,{c['accent']}33 45%,transparent)"></div>
<div id="grid"></div>
{f'<div id="stagebg">{stage_bg}</div>' if stage_bg else ""}
{f'<div id="stageback">{stage_back}</div>' if stage_back else ""}
{scenes}
{f'<div id="stagefront">{stage_front}</div>' if stage_front else ""}
{f'<div id="stagetracks">{tracks_html}</div>' if tracks_html else ""}
{f'<div id="capt" class="{spec["captions"]["position"]}"></div>' if spec.get("captions") else ""}
<div id="subs" class="bottom"></div>
{credit}
{'<div id="bar"></div>' if spec.get("progress_bar") else ""}
<div id="kplay_center" class="kplay-center" title="Jwe / Poz (Espas)"><svg viewBox="0 0 24 24"><polygon points="7,4 19,12 7,20"></polygon></svg></div>
</div>
<div id="kbar" style="display:none !important"><button id="kplay">❚❚</button><input id="krange" type="range" min="0" step="0.001" value="0">
<span id="ktime"></span><div id="kvolwrap" style="display:flex;align-items:center;gap:6px" title="Volim (0% - 200%)"><span id="kvolic" style="cursor:pointer;user-select:none" title="Koupe / Retabli son">🔊</span><input id="kvol" type="range" min="0" max="2" step="0.02" value="1" style="width:70px;accent-color:{c['primary']};cursor:pointer" title="Volim master"><span id="kvolval" style="font-size:11px;min-width:32px;font-weight:700;color:{c['primary']}">100%</span></div><span id="kname">Kadans WASDEV</span></div>
<script>window.__kadans = {json.dumps(meta, ensure_ascii=False)};</script>
<script>{MOTION_JS}
{_JS}</script>
</body></html>
"""
