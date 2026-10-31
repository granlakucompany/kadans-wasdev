"""Kadans WASDEV — the video SPEC: one JSON document that describes a whole video.

An AI (or a person) writes the spec; every other stage (voice, timeline, HTML scenes, render, checks) only reads it.

    {
      "kadans": 1,
      "title": "WASDEV launch",
      "lang": "fr",
      "ratio": "16:9",                       # 16:9 | 9:16 | 1:1 | 4:5 | 21:9 | 1.91:1 | 4k
      "fps": 30,
      "brand": {"name": "WAS*DEV*", "logo": "logo.svg",
                "colors": {"bg": "#0b0816", "primary": "#8b5cf6", "accent": "#0098ff", "text": "#f3eefe"}},
      "voice": {"engine": "elevenlabs", "gender": "female", "sample": null},
      "music": {"mood": "upbeat", "volume": 0.22},
      "credit": true,                        # small "Made with Kadans WASDEV" line on the last scene
      "scenes": [
        {"type": "hook", "title": "What if *one app* did it all?", "voice": "Et si un seul logiciel faisait tout ?"},
        {"type": "features", "title": "Everything to *create*",
         "items": [{"icon": "🎨", "title": "Design", "text": "2D + 3D"}], "voice": "..."},
        {"type": "cta", "title": "Try it today", "subtitle": "wasdev.ai", "voice": "..."}
      ]
    }

Text markup: *word* = highlighted (brand gradient). Durations are optional: by default a scene lasts as long as
its voice line (+ breathing room), never shorter than its animations need.
"""
from __future__ import annotations

import copy
import re

SPEC_VERSION = 1
RATIOS = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080), "4:5": (1080, 1350),
          "21:9": (2520, 1080), "1.91:1": (1200, 628), "4k": (3840, 2160)}

# type -> (required fields, list field, min items, max items)
SCENE_TYPES = {
    "hook":     (("title",), None, 0, 0),
    "text":     (("title",), None, 0, 0),
    "logo":     ((), None, 0, 0),
    "features": (("title",), "items", 1, 4),
    "list":     (("title",), "items", 1, 5),
    "stat":     ((), "items", 1, 4),
    "code":     ((), "lines", 1, 8),
    "compare":  (("left", "right"), None, 0, 0),
    "cta":      (("title",), None, 0, 0),
    "video":    (("src",), None, 0, 0),
    "image":    (("src",), None, 0, 0),
    "html":     ((), None, 0, 0),
    "chart":    (("chart",), "items", 1, 12),
    "social":   ((), None, 0, 0),
    "lottie":   (("src",), None, 0, 0),
    "stickman": ((), None, 0, 0),
}
SCENE_HELP = {
    "hook": "title (big question / problem), subtitle?",
    "text": "title, subtitle?",
    "stickman": "title?, subtitle?, speech?, name?, color?, palette?, accessory?, scale?, x?, y?, do?",
    "logo": "tagline? (uses brand name + logo)",
    "features": "title, items[1-4] {icon, title, text?}",
    "list": "title, items[1-5] (strings: checkmarks)",
    "stat": "title?, items[1-4] {value, label}",
    "code": "title?, lines[1-8] (code lines, typed live), chips[]? (labels)",
    "compare": "title?, left {title, items[]}, right {title, items[]} (right = you, highlighted)",
    "cta": "title (button text), subtitle?",
    "video": "src (your clip), in? / out? (seconds, trim), fit? cover|contain, audio? 0-1 (clip sound), "
             "title? / subtitle? (caption), caption? bottom|center|top, zoom? (slow push-in), "
             "focus? {x,y} 0-1 (zoom origin - keep a logo off the edge), backdrop? blur|none|#rrggbb "
             "(fill behind a 'contain' clip instead of black bars), title_backdrop? true|auto (dark band behind title)",
    "html": "html (inline HTML/CSS/JS - full creative freedom) OR src (.html file); libs? [anime|chart|lottie|three|motion|gsap]; "
            "use class='a' data-on='word' on any element to reveal it when that word is spoken (Whisper-synced); "
            "*word* or <span class=hl>word</span> pulses when spoken; camera? {pan, zoom, follow, shake} "
            "(parallax over Design layers 'fon N'); fx? [dust|sparks|trail|rain|smoke]",
    "chart": "chart bar|line|pie|doughnut|area, items[1-12] {label, value}, title? (drawn with Chart.js, WASDEV palette)",
    "social": "actions? [like|subscribe|follow|share|comment|bell] (default like+subscribe), handle? (@name), title?",
    "lottie": "src (.json Lottie animation file / URL / data object), title?, subtitle?, fit? contain|cover, loop? bool, speed? float",
    "image": "src (photo / screenshot), fit? cover|contain, zoom? (default true), title? / subtitle?, caption?, "
             "focus? {x,y} 0-1 (zoom origin), backdrop? blur|none|#rrggbb (auto-blur fill for 'contain' / 9:16, "
             "no black bars), title_backdrop? true|auto (dark band behind title for legibility), "
             "camera? {from:{zoom,x,y}, to:{zoom,x,y}, ease:inout|out|punch|linear} (real zoom/pan), "
             "cards? [{crop:[x,y,w,h], at:[x,y], width, from:left|right|up|down, rotate, enter, pill?, icon?}] "
             "(cut-out cards that fly in), layout? window (9:16 rounded window over the blurred backdrop)",
}
FITS = ("cover", "contain")
LIBS = ("anime", "chart", "lottie", "three", "motion", "gsap")   # bibliyotek animasyon vandorize lokal (Kadans 100% konpatib)
LIB_ALIASES = {"gsap3": "gsap", "chartjs": "chart", "threejs": "three", "lottieweb": "lottie"}
CHART_KINDS = ("bar", "line", "pie", "doughnut", "area")
SOCIAL_ACTIONS = ("like", "subscribe", "follow", "share", "comment", "bell")
TRANSITIONS = ("none", "fade", "slide", "slideright", "slideup", "slidedown", "wipe", "wipeup", "zoom", "zoomout", "flip", "rotate", "blur")   # tranzisyon ant sen yo
TRANSITION_ALIASES = {
    "crossfade": "fade", "dissolve": "fade", "fadein": "fade", "fade-in": "fade", "fade_in": "fade",
    "fadeout": "fade", "fade-out": "fade", "fade_out": "fade",
    "slide_right": "slideright", "slide-right": "slideright", "slider": "slideright", "push_right": "slideright",
    "slide_left": "slide", "slide-left": "slide", "slidetoleft": "slide", "push": "slide", "push_left": "slide",
    "slide_up": "slideup", "slide-up": "slideup", "push_up": "slideup",
    "slide_down": "slidedown", "slide-down": "slidedown", "push_down": "slidedown",
    "wipe_up": "wipeup", "wipe-up": "wipeup", "wipe_down": "wipe", "wipe-down": "wipe",
    "wipe_left": "wipe", "wipe-left": "wipe", "wipe_right": "wipe", "wipe-right": "wipe",
    "zoom_in": "zoom", "zoom-in": "zoom", "zoomin": "zoom",
    "zoom_out": "zoomout", "zoom-out": "zoomout",
    "cut": "none", "off": "none", "false": "none", "null": "none",
}
import os as _os
LANGS = ("fr", "en", "ht", "es", "pt", "de", "it", "ru")   # 8 lang ofisyèl Kadans WASDEV
DEFAULT_LANG = (_os.environ.get("KADANS_LANG") or "fr").strip() or "fr"   # lang videyo pa defo (franse)
# Kle valab yo (refize kle enkoni: yon fot frap / opsyon ki pa egziste = erè klè, pa inyore an silans)
TOP_KEYS = {"kadans", "title", "lang", "ratio", "fps", "brand", "voice", "music", "credit", "progress_bar",
            "background", "overlays", "captions", "subtitles", "sfx", "look", "motion_blur", "scenes", "total_duration", "libs", "transition", "tracks", "volume", "mix", "markers", "sub_cues", "sub_style", "skills"}
MIX_KEYS = {"cap", "bed_ceiling", "bed_peak", "duck", "fx_peak", "fx_duck", "target_lufs", "target_tp", "hum_hz", "clarity", "clarity_preset", "denoise"}
SCENE_KEYS = {"type", "id", "title", "subtitle", "tagline", "voice", "voice_file", "duration", "background",
              "overlays", "focus", "title_backdrop", "items", "lines", "chips", "left", "right", "src", "in",
              "out", "fit", "caption", "zoom", "audio", "backdrop", "camera", "cards", "layout", "html", "libs", "chart", "actions",
              "handle", "transition", "marks", "fx", "lut", "loop", "speed", "lipsync", "rig", "sounds", "ambience", "speaker",
              "voice_speed", "timing", "responsive_timing", "stickman", "speech", "accessory", "prop", "palette", "scale", "name", "color", "x", "y", "do", "skills"}
EASES = ("inout", "out", "punch", "linear")
CARD_FROM = ("left", "right", "up", "down", "none")
CARD_KEYS = {"crop", "at", "width", "from", "rotate", "enter", "pill", "icon", "rot", "w", "label"}
BG_KEYS = {"src", "kind", "fit", "opacity", "dim", "blur", "zoom", "tint", "tint_strength", "color", "in", "out"}
VOICE_KEYS = {"engine", "gender", "sample", "lang", "lexicon", "retries", "verify", "enhance", "compressor", "voice_id", "model",
              "speed", "hum_hz", "clarity", "clarity_preset", "denoise"}
VOICE_SPEED = (0.5, 2.0)            # vitès vwa (atempo: ton an pa chanje)
VIDEO_SPEED = (0.25, 4.0)           # vitès klip videyo yon sèn
CAPTIONS = ("bottom", "center", "top")
VIDEO_EXT = (".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".wmv", ".mpg", ".mpeg", ".3gp")
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg")
AUDIO_EXT = (".wav", ".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac", ".webm")
DEFAULT_COLORS = {"bg": "#0b0816", "primary": "#8b5cf6", "accent": "#0098ff", "text": "#f3eefe", "muted": "#b9addb"}
GENDERS = ("female", "male")
MOODS = ("upbeat", "calm", "epic", "tech")
DEFAULT_LOOK = {"grain": 0.15, "bloom": 0.25, "vignette": 0.3}     # cinematic finish applied after capture
MOTION_BLUR = (0, 2, 4, 6)
CAPTION_STYLES = ("karaoke", "pop")
# captions: koulè 3 eta mo yo (ap vini / di / k ap di kounye a) + alo, gwosè (px a 1080), koupaj liy yo
CAPTION_KEYS = ("style", "position", "colors", "size", "max_words", "max_chars", "min_words")
CAPTION_COLORS = ("upcoming", "spoken", "current", "glow")
_HEXA = re.compile(r"^#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
# Son otomatik: kind -> pa defo. type = klavye pandan kòd la ap tape · text = son lè tit / tèks parèt
SFX_KINDS = {"whoosh": True, "pop": True, "hit": True, "type": False, "text": False}
# The 31 layer blend modes of photo editors (27 Photoshop + 4 Paint.NET), in their usual order.
# NATIVE ones are drawn by the browser itself (identical in preview and render);
# EXACT ones have no browser equivalent: the renderer composites them pixel by
# pixel (kadans.blend) and the live preview shows the nearest native mode.
BLENDS = ("normal", "dissolve",
          "darken", "multiply", "color-burn", "linear-burn", "darker-color",
          "lighten", "screen", "color-dodge", "linear-dodge", "lighter-color",
          "overlay", "soft-light", "hard-light", "vivid-light", "linear-light", "pin-light", "hard-mix",
          "difference", "exclusion", "subtract", "divide",
          "hue", "saturation", "color", "luminosity",
          "reflect", "glow", "negation", "xor")
NATIVE_BLEND = {"normal": "normal", "darken": "darken", "multiply": "multiply", "color-burn": "color-burn",
                "lighten": "lighten", "screen": "screen", "color-dodge": "color-dodge", "linear-dodge": "plus-lighter",
                "overlay": "overlay", "soft-light": "soft-light", "hard-light": "hard-light",
                "difference": "difference", "exclusion": "exclusion", "hue": "hue", "saturation": "saturation",
                "color": "color", "luminosity": "luminosity"}
PREVIEW_BLEND = {"dissolve": "normal", "linear-burn": "color-burn", "darker-color": "darken",
                 "lighter-color": "lighten", "vivid-light": "hard-light", "linear-light": "hard-light",
                 "pin-light": "hard-light", "hard-mix": "hard-light", "subtract": "difference", "divide": "color-dodge",
                 "reflect": "color-dodge", "glow": "screen", "negation": "difference", "xor": "difference"}
EXACT_BLEND = tuple(PREVIEW_BLEND)


def blend_name(v) -> str:
    """«Linear Dodge (Add)», «linear_dodge», «add» → «linear-dodge»."""
    n = str(v or "").strip().lower().replace("(add)", "").strip().replace("_", "-").replace(" ", "-")
    return {"add": "linear-dodge", "plus-lighter": "linear-dodge", "plus": "linear-dodge"}.get(n, n)
OV_ANIMS = ("none", "drift", "pulse", "spin", "float", "reveal", "sweep")
LAYERS = ("back", "front")
MAX_OVERLAYS = 8
_NAMED_COLORS = ("primary", "accent", "text", "muted", "bg")


ICON_MAP = {"code": "💻", "palette": "🎨", "file": "📄", "document": "📄", "sparkles": "✨", "layout": "🧩",
            "rocket": "🚀", "bolt": "⚡", "lightning": "⚡", "check": "✓", "star": "★", "heart": "❤",
            "gear": "⚙", "settings": "⚙", "globe": "🌐", "web": "🌐", "phone": "📱", "mobile": "📱",
            "camera": "📷", "video": "🎬", "image": "🖼", "photo": "🖼", "music": "🎵", "mic": "🎤",
            "chart": "📊", "stats": "📊", "money": "💰", "cash": "💰", "lock": "🔒", "secure": "🔒",
            "cloud": "☁", "mail": "✉", "email": "✉", "bell": "🔔", "search": "🔍", "pen": "✏", "edit": "✏",
            "brush": "🖌", "paint": "🖌", "cube": "🧊", "3d": "🧊", "fire": "🔥", "bulb": "💡", "idea": "💡",
            "target": "🎯", "calendar": "📅", "clock": "🕐", "time": "🕐", "flag": "🚩", "pin": "📍",
            "location": "📍", "map": "🗺", "users": "👥", "team": "👥", "user": "👤", "person": "👤",
            "play": "▶", "download": "⬇", "upload": "⬆", "link": "🔗", "wrench": "🔧", "tool": "🔧",
            "shield": "🛡", "gift": "🎁", "tag": "🏷", "cart": "🛒", "shop": "🛒", "store": "🏪", "ai": "🤖",
            "robot": "🤖", "brain": "🧠", "eye": "👁", "folder": "📁", "book": "📖", "chat": "💬",
            "message": "💬", "like": "👍", "win": "🏆", "trophy": "🏆"}


def icon_glyph(v) -> str:
    """Non ikòn (egz. «code», «palette») → emoji. Yon emoji/senbòl rete; yon mo ki pa nan kat la → ★."""
    s = str(v or "").strip()
    if not s:
        return "★"
    if s.lower() in ICON_MAP:
        return ICON_MAP[s.lower()]
    if any(ord(c) > 0x2100 for c in s) or (len(s) <= 2 and not s.isalpha()):
        return s
    return "★"


def icon_unknown(v) -> bool:
    """True = yon mo ki pa yon emoji e ki pa nan ICON_MAP (li t ap parèt kòm gwo tèks)."""
    s = str(v or "").strip()
    if not s or s.lower() in ICON_MAP:
        return False
    return not (any(ord(c) > 0x2100 for c in s) or (len(s) <= 2 and not s.isalpha()))


def _media_src(v, path: str, err: list, kinds=("image", "video")) -> tuple[str, str]:
    """(src, kind) of a background / overlay source; kind = image | video (svg / png / jpg are images)."""
    src = _s(v)
    if not src:
        err.append(f"{path}: src required")
        return "", ""
    ext = ("." + src.rsplit(".", 1)[-1].lower()) if "." in src.rsplit("/", 1)[-1] else ""
    if ext in VIDEO_EXT and "video" in kinds:
        return src, "video"
    if ext in IMAGE_EXT and "image" in kinds:
        return src, "image"
    if src.startswith("find:"):                       # host apps may resolve a search before validating
        return src, "image"
    err.append(f"{path}: '{src}' is not an image / video file")
    return src, ""


def _color(v, path: str, err: list):
    if v in (None, ""):
        return None
    v = _s(v)
    if v in _NAMED_COLORS or _HEX.match(v):
        return v
    err.append(f"{path}: '{v}' - #rrggbb or {' | '.join(_NAMED_COLORS)}")
    return None


def _num(d: dict, k: str, default: float, lo: float, hi: float, path: str, err: list) -> float:
    try:
        return max(lo, min(hi, float(d.get(k, default) if d.get(k) is not None else default)))
    except (TypeError, ValueError):
        err.append(f"{path}.{k}: number {lo}-{hi}")
        return default


def _camera(v, path: str, err: list):
    """Mouvman kamera: {from:{zoom,x,y}, to:{zoom,x,y}, ease} — vrè zoom/panoramik (pa zoom fiks sèlman)."""
    if v in (None, False, ""):
        return None
    if not isinstance(v, dict):
        err.append(f"{path}: {{from, to, ease}}")
        return None

    def pt(d, dz):
        d = d if isinstance(d, dict) else {}
        return {"zoom": _num(d, "zoom", dz, 0.2, 5, path, err), "x": _num(d, "x", 0.5, 0, 1, path, err),
                "y": _num(d, "y", 0.5, 0, 1, path, err)}
    ease = _s(v.get("ease")) or "inout"
    if ease not in EASES:
        err.append(f"{path}.ease: {' | '.join(EASES)}")
        ease = "inout"
    return {"from": pt(v.get("from"), 1.0), "to": pt(v.get("to"), 1.08), "ease": ease}


CAM_HTML_KEYS = {"pan", "zoom", "origin", "ease", "follow", "shake", "depth", "limit"}
FOLLOW_KEYS = {"rig", "amount", "offset"}
SHAKE_KEYS = {"at", "force", "dur"}


def _pair(v, path: str, err: list, lo: float = -1e5, hi: float = 1e5):
    """[x, y] (oswa yon sèl nonb = x, y = 0) → [float, float]."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return [max(lo, min(hi, float(v))), 0.0]
    if isinstance(v, (list, tuple)) and len(v) == 2:
        try:
            return [max(lo, min(hi, float(v[0]))), max(lo, min(hi, float(v[1])))]
        except (TypeError, ValueError):
            pass
    err.append(f"{path}: [x, y] (px)")
    return [0.0, 0.0]


def _camera_html(v, path: str, err: list):
    """KAMERA pou yon sèn html (dekò vektè Design an kouch): pan / zoom / origin / follow / shake / depth.
    Kouch «fon N» (oswa data-depth) deplase mwens pase kamera a → paralaks. Tout detèminis (loc)."""
    if v in (None, False, ""):
        return None
    if not isinstance(v, dict):
        err.append(f"{path}: {{pan, zoom, origin, ease, follow, shake, depth, limit}}")
        return None
    for k in v:
        if k not in CAM_HTML_KEYS:
            err.append(f"{path}.{k}: unknown key - {', '.join(sorted(CAM_HTML_KEYS))}")
    out = {"pan": [0.0, 0.0], "zoom": [1.0, 1.0], "origin": None, "ease": "inout", "follow": None,
           "shake": [], "depth": {}, "limit": None}
    if v.get("pan") is not None:                      # kamera a deplase [x, y] px pandan sèn nan (+x = adwat)
        out["pan"] = _pair(v["pan"], f"{path}.pan", err, -4000, 4000)
    z = v.get("zoom")
    if z is not None:                                 # 1.05 = fini a 105 % · [1, 1.1] = soti → rive
        try:
            zz = [1.0, float(z)] if isinstance(z, (int, float)) and not isinstance(z, bool) else [float(z[0]), float(z[1])]
            out["zoom"] = [max(0.2, min(5.0, zz[0])), max(0.2, min(5.0, zz[1]))]
        except (TypeError, ValueError, IndexError, KeyError):
            err.append(f"{path}.zoom: 1.05 | [from, to] (0.2-5)")
    if v.get("origin") is not None:                   # pwen zoom (px nan sèn nan), pa defo = mitan
        out["origin"] = _pair(v["origin"], f"{path}.origin", err, -1e4, 1e4)
    ease = _s(v.get("ease")) or "inout"
    if ease not in EASES:
        err.append(f"{path}.ease: {' | '.join(EASES)}")
        ease = "inout"
    out["ease"] = ease
    f = v.get("follow")
    if isinstance(f, str) and f.strip():
        f = {"rig": f}
    if isinstance(f, dict) and _s(f.get("rig")):
        for k in f:
            if k not in FOLLOW_KEYS:
                err.append(f"{path}.follow.{k}: unknown key - {', '.join(sorted(FOLLOW_KEYS))}")
        out["follow"] = {"rig": _s(f["rig"]), "amount": _num(f, "amount", 0.5, 0, 1, f"{path}.follow", err),
                         "offset": _pair(f["offset"], f"{path}.follow.offset", err) if f.get("offset") is not None
                         else [0.0, 0.0]}
    elif f not in (None, False, ""):
        err.append(f"{path}.follow: \"Lina\" | {{rig, amount 0-1, offset [x, y]}}")
    sh = v.get("shake") or []
    if isinstance(sh, dict):
        sh = [sh]
    if not isinstance(sh, list):
        err.append(f"{path}.shake: [{{at, force, dur}}]")
        sh = []
    for j, s in enumerate(sh[:20]):                   # tranbleman: chòk, ateri, eksplozyon
        if not isinstance(s, dict) or s.get("at") is None:
            err.append(f"{path}.shake[{j}]: {{at (s), force px, dur s}}")
            continue
        for k in s:
            if k not in SHAKE_KEYS:
                err.append(f"{path}.shake[{j}].{k}: unknown key - at, force, dur")
        out["shake"].append({"at": _num(s, "at", 0, 0, 600, f"{path}.shake[{j}]", err),
                             "force": _num(s, "force", 6, 0, 80, f"{path}.shake[{j}]", err),
                             "dur": _num(s, "dur", 0.35, 0.05, 5, f"{path}.shake[{j}]", err)})
    d = v.get("depth") or {}
    if not isinstance(d, dict):
        err.append(f"{path}.depth: {{\"non kouch\": 0-1}}")
        d = {}
    for k, x in d.items():                            # pwofondè pa non kouch (pi fò pase «fon N» / data-depth)
        try:
            out["depth"][str(k)] = max(0.0, min(2.0, float(x)))
        except (TypeError, ValueError):
            err.append(f"{path}.depth.{k}: 0 (pa bouje) - 1 (premye plan)")
    if v.get("limit") is not None:                    # kamera pa janm ale pi lwen pase ±limit px (bò dekò a)
        out["limit"] = _num(v, "limit", 120, 0, 4000, path, err)
    return out


FX_TYPES = ("dust", "sparks", "trail", "rain", "smoke")
FX_KEYS = {"type", "at", "dur", "x", "y", "color", "count", "size", "seed", "follow", "offset", "spread",
           "speed", "opacity", "angle"}


def _fx_list(v, path: str, err: list):
    """EFÈ PATIKIL detèminis (menm imaj chak fwa): dust | sparks | trail | rain | smoke.
    Yon dict SAN «type» = filtè koulè editè a (blur, brightness…) → kite l jan l ye."""
    if isinstance(v, dict) and "type" not in v:
        return v
    if v in (None, False, "", []):
        return None
    if isinstance(v, dict):
        v = [v]
    if not isinstance(v, list):
        err.append(f"{path}: [{{type: {'|'.join(FX_TYPES)}, at, dur, x, y, …}}]")
        return None
    out = []
    for j, e in enumerate(v[:24]):
        p = f"{path}[{j}]"
        if not isinstance(e, dict) or _s(e.get("type")).lower() not in FX_TYPES:
            err.append(f"{p}.type: {' | '.join(FX_TYPES)}")
            continue
        for k in e:
            if k not in FX_KEYS:
                err.append(f"{p}.{k}: unknown key - {', '.join(sorted(FX_KEYS))}")
        t = _s(e["type"]).lower()
        dflt = {"dust": (0.7, 10, "#cbbfd8", 14), "sparks": (0.8, 16, "#ffd27a", 5), "trail": (3.0, 14, "#ffb347", 10),
                "rain": (600.0, 90, "#a9c4e8", 2), "smoke": (2.5, 8, "#9a94a8", 60)}[t]
        o = {"type": t, "at": _num(e, "at", 0, 0, 600, p, err), "dur": _num(e, "dur", dflt[0], 0.05, 600, p, err),
             "count": int(_num(e, "count", dflt[1], 1, 300, p, err)), "color": dflt[2],
             "size": _num(e, "size", dflt[3], 0.5, 400, p, err), "seed": int(_num(e, "seed", j + 1, 0, 1e9, p, err)),
             "opacity": _num(e, "opacity", 0.6 if t != "rain" else 0.45, 0, 1, p, err),
             "spread": _num(e, "spread", 1.0, 0.05, 20, p, err), "speed": _num(e, "speed", 1.0, 0.05, 20, p, err),
             "angle": _num(e, "angle", 12 if t == "rain" else 0, -80, 80, p, err)}
        c = e.get("color")
        if c is not None:
            if isinstance(c, str) and _HEXA.match(c.strip()) or (isinstance(c, str) and _HEX.match(c.strip())):
                o["color"] = c.strip()
            else:
                err.append(f"{p}.color: #rrggbb")
        if t == "trail":                              # sillage limyè dèyè yon pèsonaj rig (Anima)
            if not _s(e.get("follow")):
                err.append(f"{p}.follow: non pèsonaj rig la (trail)")
                continue
            o["follow"] = _s(e["follow"])
            o["offset"] = _pair(e["offset"], f"{p}.offset", err) if e.get("offset") is not None else [0.0, 0.0]
        elif t != "rain":                             # pwen kote efè a pati (px nan sèn nan)
            if e.get("x") is None or e.get("y") is None:
                err.append(f"{p}: x, y (px) obligatwa pou {t}")
                continue
            o["x"], o["y"] = _num(e, "x", 0, -1e4, 1e4, p, err), _num(e, "y", 0, -1e4, 1e4, p, err)
        out.append(o)
    return out or None


def _cards(v, path: str, err: list) -> list:
    """Kat koupe nan imaj la: [{crop:[x,y,w,h], at:[x,y], width, from, rotate, enter, pill?, icon?}]."""
    if v in (None, False, ""):
        return []
    if not isinstance(v, list):
        err.append(f"{path}: lis kat")
        return []
    out = []
    for j, c in enumerate(v[:8]):
        p = f"{path}[{j}]"
        c = dict(c) if isinstance(c, dict) else {}
        for canon, alias in (("rotate", "rot"), ("width", "w"), ("pill", "label")):   # alias kout → kle kanonik
            if alias in c and canon not in c:
                c[canon] = c[alias]
        for k in c:
            if k not in CARD_KEYS:
                err.append(f"{p}.{k}: unknown key - {', '.join(sorted(CARD_KEYS))}")
        crop = c.get("crop")
        if not (isinstance(crop, (list, tuple)) and len(crop) == 4):
            err.append(f"{p}.crop: [x, y, w, h] (fraksyon 0-1)")
            continue
        try:
            crop = [max(0.0, min(1.0, float(x))) for x in crop]
        except (TypeError, ValueError):
            err.append(f"{p}.crop: nonm")
            continue
        at = c.get("at", [0.5, 0.5])
        if not (isinstance(at, (list, tuple)) and len(at) == 2):
            err.append(f"{p}.at: [x, y] pozisyon kat la (0-1) - se pa yon le")
            at = [0.5, 0.5]
        try:
            ax, ay = float(at[0]), float(at[1])
        except (TypeError, ValueError, IndexError):
            err.append(f"{p}.at: [x, y] (nonm 0-1)")
            ax, ay = 0.5, 0.5
        frm = _s(c.get("from")) or "up"
        if frm not in CARD_FROM:
            err.append(f"{p}.from: {' | '.join(CARD_FROM)}")
            frm = "up"
        out.append({"crop": crop, "at": [ax, ay], "width": _num(c, "width", 0.4, 0.05, 1, p, err), "from": frm,
                    "rotate": _num(c, "rotate", 0.0, -45, 45, p, err), "enter": _num(c, "enter", 0.0, 0, 30, p, err),
                    "pill": _s(c.get("pill")) or None, "icon": _s(c.get("icon")) or None})
    return out


def _focus(v, path: str, err: list):
    """Pwen fokis (0-1, 0-1) = kote zoom nan santre (pou l pa koupe yon logo sou bò a). None = santre."""
    if v in (None, False, ""):
        return None
    if not isinstance(v, dict):
        err.append(f"{path}: {{x, y}} (0-1 chak)")
        return None
    return {"x": _num(v, "x", 0.5, 0, 1, path, err), "y": _num(v, "y", 0.5, 0, 1, path, err)}


def background(v, path: str, err: list):
    """Normalized background: {src, kind, fit, opacity, dim, zoom, tint, color, in, out} - or None."""
    if v in (None, False, ""):
        return None
    if isinstance(v, str):
        v = {"src": v}
    if not isinstance(v, dict):
        err.append(f"{path}: {{src, fit?, opacity?, dim?, zoom?, tint?, color?}} or a file path")
        return None
    for k in v:
        if k not in BG_KEYS:
            err.append(f"{path}.{k}: unknown key - {', '.join(sorted(BG_KEYS))}")
    src, kind = _media_src(v.get("src"), f"{path}.src", err)
    fit = _s(v.get("fit")) or "cover"
    if fit not in FITS:
        err.append(f"{path}.fit: cover | contain")
    out = {"src": src, "kind": kind, "fit": fit,
           "blur": _num(v, "blur", 0.0, 0, 100, path, err),       # flou (px) - fon dou dèyè yon imaj / fon flou 9:16
           "opacity": _num(v, "opacity", 1.0, 0, 1, path, err),
           "dim": _num(v, "dim", 0.35, 0, 0.95, path, err),       # darkens the picture so text stays readable
           "zoom": v.get("zoom", True) is not False,
           "tint": _color(v.get("tint"), f"{path}.tint", err),    # colour wash over the picture (brand colour)
           "tint_strength": _num(v, "tint_strength", 0.3, 0, 1, path, err),   # 0.3: a hint of the colour, not a mono picture
           "color": _color(v.get("color"), f"{path}.color", err),  # recolour a one-colour SVG asset
           "in": _num(v, "in", 0.0, 0, 36000, path, err)}
    if v.get("out") not in (None, ""):
        out["out"] = _num(v, "out", 0.0, 0.2, 36000, path, err)
    return out


def overlays(v, path: str, err: list) -> list:
    """Atmosphere layers (smoke, light, splash, shapes…) behind (back) or in front of (front) the content."""
    if v in (None, False):
        return []
    if not isinstance(v, list):
        err.append(f"{path}: list of {{src, layer?, blend?, opacity?, x?, y?, w?, anim?, speed?, color?, rotate?}}")
        return []
    if len(v) > MAX_OVERLAYS:
        err.append(f"{path}: {len(v)} overlays - max {MAX_OVERLAYS} (heavy layers slow the render)")
    out = []
    for j, o in enumerate(v[:MAX_OVERLAYS]):
        p = f"{path}[{j}]"
        if isinstance(o, str):
            o = {"src": o}
        if not isinstance(o, dict):
            err.append(f"{p}: object or file path")
            continue
        src, kind = _media_src(o.get("src"), f"{p}.src", err)
        layer, blend, anim = _s(o.get("layer")) or "back", blend_name(o.get("blend") or "screen"), _s(o.get("anim")) or "drift"
        if layer not in LAYERS:
            err.append(f"{p}.layer: back | front")
        if blend not in BLENDS:
            err.append(f"{p}.blend: '{blend}' - {' | '.join(BLENDS)}")
        if anim not in OV_ANIMS:
            err.append(f"{p}.anim: {' | '.join(OV_ANIMS)}")
        out.append({"src": src, "kind": kind, "layer": layer, "blend": blend, "anim": anim,
                    "opacity": _num(o, "opacity", 0.6, 0, 1, p, err), "x": _num(o, "x", 0.5, -0.5, 1.5, p, err),
                    "y": _num(o, "y", 0.5, -0.5, 1.5, p, err), "w": _num(o, "w", 0.6, 0.02, 3, p, err),
                    "speed": _num(o, "speed", 1.0, 0, 10, p, err), "rotate": _num(o, "rotate", 0.0, -360, 360, p, err),
                    "color": _color(o.get("color"), f"{p}.color", err)})
    return out       # karaoke: the phrase is shown, the spoken word lights up; pop: words appear
_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")

# speaking rate used before the real voice exists (words per second, conservative)
WORDS_PER_S = 2.6
LEAD_IN, TAIL = 0.35, 0.55          # silence before the voice starts / after it ends, inside a scene
MIN_SCENE = 2.0
MAX_SCENES, MAX_TOTAL_S = 20, 180


class SpecError(ValueError):
    """Invalid spec. .errors = list of "path: message" strings an AI can fix one by one."""

    def __init__(self, errors: list[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


def _s(v) -> str:
    return v.strip() if isinstance(v, str) else ""


def _line(x) -> str:
    if isinstance(x, dict):
        return str(x.get("text") or x.get("title") or "")
    return str(x)


def _libs(val, path, err):
    """Lis bibliyotek animasyon (anime/chart/lottie/three/motion/gsap) - refize sa ki enkoni."""
    if val in (None, ""):
        return []
    if isinstance(val, str):
        val = [val]
    if not isinstance(val, list):
        err.append(f"{path}: list of {', '.join(LIBS)}")
        return []
    out = []
    for v in val:
        v = _s(v).lower()
        v = LIB_ALIASES.get(v, v)
        if v and v not in LIBS:
            err.append(f"{path}: '{v}' - one of {', '.join(LIBS)}")
        elif v and v not in out:
            out.append(v)
    return out


def _skills_err(v, path: str) -> str:
    """`skills` = lis kòmand slash (egz. ["/zoomin", "/soundhot"]): metadata sèlman, rann lan pa chanje."""
    if not isinstance(v, list) or not all(isinstance(x, str) and x.strip().startswith("/") for x in v):
        return f'{path}: must be a list of slash commands, e.g. ["/zoomin", "/soundhot"]'
    return ""


def validate(spec: dict) -> dict:
    """Return a complete, normalized copy of the spec (defaults filled in). Raise SpecError listing EVERY problem."""
    err: list[str] = []
    if not isinstance(spec, dict):
        raise SpecError(["spec: must be a JSON object"])
    s = copy.deepcopy(spec)
    try:
        s["kadans"] = int(s.get("kadans") or SPEC_VERSION)
    except (TypeError, ValueError):
        s["kadans"] = SPEC_VERSION
    if s["kadans"] > SPEC_VERSION:
        err.append(f"kadans: version {s['kadans']} is newer than this engine ({SPEC_VERSION})")
    s["title"] = _s(s.get("title")) or "Kadans video"
    s["lang"] = _s(s.get("lang")) or DEFAULT_LANG
    s["ratio"] = _s(s.get("ratio")) or "16:9"
    if s["ratio"] not in RATIOS:
        err.append(f"ratio: '{s['ratio']}' - use one of {', '.join(RATIOS)}")
        s["ratio"] = "16:9"
    s["w"], s["h"] = RATIOS[s["ratio"]]
    try:
        s["fps"] = max(12, min(60, int(s.get("fps") or 30)))
    except (TypeError, ValueError):
        err.append("fps: must be a number (12-60)")
        s["fps"] = 30

    b = s.get("brand") or {}
    if not isinstance(b, dict):
        err.append("brand: must be an object")
        b = {}
    cols = dict(DEFAULT_COLORS)
    for k, v in (b.get("colors") or {}).items():
        if k in cols:
            if isinstance(v, str) and _HEX.match(v):
                cols[k] = v
            else:
                err.append(f"brand.colors.{k}: '{v}' - use #rrggbb")
    font = _s(b.get("font")) or "Segoe UI"
    s["brand"] = {"name": _s(b.get("name")), "logo": _s(b.get("logo")) or None, "colors": cols,
                  "font": font,                                       # body text (any font installed on the PC:
                  "font_title": _s(b.get("font_title")) or font,      # `kadans fonts`), titles / buttons / numbers,
                  "font_code": _s(b.get("font_code")) or "Cascadia Code"}  # and code

    v = s.get("voice")
    if v is not None and v is not False:
        v = v if isinstance(v, dict) else {}
        for k in v:
            if k not in VOICE_KEYS:
                err.append(f"voice.{k}: unknown key - {', '.join(sorted(VOICE_KEYS))}")
        g = _s(v.get("gender")) or "female"
        if g not in GENDERS:
            err.append(f"voice.gender: '{g}' - female | male")
        lex = v.get("lexicon")                            # {mo: IPA} oswa {lang: {mo: IPA}} - pwononsyasyon
        if lex not in (None, {}, False) and not isinstance(lex, dict):
            err.append("voice.lexicon: {mo: IPA} (oswa {lang: {mo: IPA}})")
            lex = None
        try:
            retries = max(1, min(8, int(v.get("retries") or 3)))
        except (TypeError, ValueError):
            err.append("voice.retries: nonm 1-8")
            retries = 3
        s["voice"] = {"engine": _s(v.get("engine")) or "elevenlabs", "gender": g,
                      "sample": _s(v.get("sample")) or None, "lang": _s(v.get("lang")) or s["lang"],
                      "lexicon": (lex or None), "retries": retries, "verify": v.get("verify", False) is True,
                      "enhance": v.get("enhance", True) is not False}
        if _s(v.get("voice_id")):
            s["voice"]["voice_id"] = _s(v.get("voice_id"))
        if _s(v.get("model")):
            s["voice"]["model"] = _s(v.get("model"))
        if v.get("speed") not in (None, ""):               # VITÈS VWA a pou tout videyo a (1 = nòmal)
            try:
                s["voice"]["speed"] = round(max(VOICE_SPEED[0], min(VOICE_SPEED[1], float(v["speed"]))), 3)
            except (TypeError, ValueError):
                err.append(f"voice.speed: nonm {VOICE_SPEED[0]}-{VOICE_SPEED[1]} (1 = nòmal)")
        comp = v.get("compressor")
        if isinstance(comp, dict):
            cc = {}
            for ck in ("threshold", "ratio", "attack", "release", "makeup"):
                if ck in comp:
                    try:
                        cc[ck] = float(comp[ck])
                    except (TypeError, ValueError):
                        err.append(f"voice.compressor.{ck}: nonm")
            if cc:
                s["voice"]["compressor"] = cc
        elif comp not in (None,):
            err.append("voice.compressor: {threshold, ratio, attack, release, makeup}")
        if v.get("hum_hz"):
            s["voice"]["hum_hz"] = v.get("hum_hz")
        if v.get("clarity_preset") or v.get("clarity"):
            s["voice"]["clarity_preset"] = v.get("clarity_preset") or v.get("clarity")
        if v.get("denoise") is not None:
            s["voice"]["denoise"] = v.get("denoise")
    else:
        s["voice"] = None
    m = s.get("music")
    if m is not None and m is not False:
        m = m if isinstance(m, dict) else {}
        try:
            vol = max(0.0, min(1.0, float(m.get("volume", 0.22) or 0)))
        except (TypeError, ValueError):
            err.append("music.volume: number 0-1")
            vol = 0.22
        mood = _s(m.get("mood")) or "upbeat"
        if mood not in MOODS:
            err.append(f"music.mood: '{mood}' - {' | '.join(MOODS)}")
        try:
            seed = int(m.get("seed") or 0)
        except (TypeError, ValueError):
            seed = 0
        s["music"] = {"mood": mood, "file": _s(m.get("file")) or None, "volume": vol, "seed": seed}
    else:
        s["music"] = None
    if "volume" in s:
        try:
            s["volume"] = max(0.0, min(2.0, float(s["volume"])))
        except (TypeError, ValueError):
            err.append("volume: nonm 0-2")
            s["volume"] = 1.0
    s["credit"] = s.get("credit", True) is not False
    s["progress_bar"] = bool(s.get("progress_bar", False))
    s["background"] = background(s.get("background"), "background", err)      # whole video (under every scene)
    s["overlays"] = overlays(s.get("overlays"), "overlays", err)
    sub_cfg = s.get("subtitles")
    if isinstance(sub_cfg, dict):
        sub_prov = _s(sub_cfg.get("provider")) or "ai_auto"
        sub_sty = _s(sub_cfg.get("style")) or "karaoke_bottom"
        sub_en = bool(sub_cfg.get("enabled", True)) and sub_prov != "none"
        sub_pos = "top" if sub_sty == "top_bar" else ("middle" if sub_sty == "center_pop" else "bottom")
        s["subtitles"] = {
            "enabled": sub_en,
            "provider": sub_prov,
            "style": sub_sty,
            "position": _s(sub_cfg.get("position")) or sub_pos,
            "karaoke": bool(sub_cfg.get("karaoke", sub_sty in ("karaoke_bottom", "center_pop"))),
        }
        if "captions" not in spec:
            if sub_en:
                s["captions"] = {
                    "style": "pop" if sub_sty == "center_pop" else "karaoke",
                    "position": "top" if sub_sty == "top_bar" else ("middle" if sub_sty == "center_pop" else "bottom"),
                }
            else:
                s["captions"] = None
    elif sub_cfg is False:
        s["subtitles"] = {"enabled": False, "provider": "none", "style": "karaoke_bottom", "position": "bottom", "karaoke": False}
        if "captions" not in spec:
            s["captions"] = None
    cap = s.get("captions")
    if cap in (None, False):
        s["captions"] = None
    else:
        cap = {} if cap is True else (cap if isinstance(cap, dict) else {})
        for _ck in cap:
            if _ck not in CAPTION_KEYS:
                err.append(f"captions.{_ck}: unknown key - {', '.join(CAPTION_KEYS)}")
        style, pos = _s(cap.get("style")) or "karaoke", _s(cap.get("position")) or "bottom"
        if style not in CAPTION_STYLES:
            err.append(f"captions.style: {' | '.join(CAPTION_STYLES)}")
        if pos not in ("bottom", "top", "middle"):
            err.append("captions.position: bottom | top | middle")
        s["captions"] = {"style": style, "position": pos}
        # v3.10: koulè, gwosè ak koupaj soutit yo NAN spec la (anvan: script deyò ki te efase chak rebati)
        cols = cap.get("colors")
        if cols is not None:
            if not isinstance(cols, dict):
                err.append("captions.colors: {upcoming?, spoken?, current?, glow?} (#rrggbb or #rrggbbaa)")
            else:
                out_c = {}
                for ck, cv in cols.items():
                    if ck not in CAPTION_COLORS:
                        err.append(f"captions.colors.{ck}: unknown key - {', '.join(CAPTION_COLORS)}")
                    elif not (isinstance(cv, str) and _HEXA.match(cv.strip())):
                        err.append(f"captions.colors.{ck}: #rrggbb or #rrggbbaa")
                    else:
                        out_c[ck] = cv.strip()
                if out_c:
                    s["captions"]["colors"] = out_c
        for ck, lo, hi in (("size", 24, 140), ("max_words", 2, 20), ("max_chars", 12, 120), ("min_words", 1, 6)):
            if cap.get(ck) is not None:
                v = _num(cap, ck, 0, lo, hi, "captions", err)
                s["captions"][ck] = int(v) if ck != "size" else v
    fx = s.get("sfx", True)
    if fx is False:
        s["sfx"] = None
    else:
        fx = fx if isinstance(fx, dict) else {}
        try:
            s["sfx"] = {"volume": max(0.0, min(1.0, float(fx.get("volume", 0.5))))}
        except (TypeError, ValueError):
            err.append("sfx.volume: number 0-1")
            s["sfx"] = {"volume": 0.5}
        for kind, default in SFX_KINDS.items():         # chak son: limen / etenn (whoosh/pop/hit pa defo)
            v = fx.get(kind, default)
            if not isinstance(v, bool):
                err.append(f"sfx.{kind}: true | false")
                v = default
            s["sfx"][kind] = v
    lk = s.get("look")
    lk = dict(DEFAULT_LOOK) if lk in (None, True) else ({} if lk is False else lk)
    if not isinstance(lk, dict):
        err.append("look: {grain, bloom, vignette} (0-1 each) or false")
        lk = {}
    look = {}
    for k in DEFAULT_LOOK:
        try:
            look[k] = max(0.0, min(1.0, float(lk.get(k, 0) or 0)))
        except (TypeError, ValueError):
            err.append(f"look.{k}: number 0-1")
            look[k] = 0.0
    s["look"] = look
    try:
        mb = int(s.get("motion_blur") or 0)
    except (TypeError, ValueError):
        mb = -1
    if mb not in MOTION_BLUR:
        err.append(f"motion_blur: one of {', '.join(map(str, MOTION_BLUR))} (sub-frames per frame; 0 = off)")
        mb = 0
    s["motion_blur"] = mb
    mx = s.get("mix")                                # plafon mizik / SFX anba vwa a (audio.bed_cap)
    if mx is not None:
        if not isinstance(mx, dict):
            err.append("mix: {cap, bed_ceiling, bed_peak, duck}")
            s["mix"] = {}
        else:
            for k in mx:
                if k not in MIX_KEYS:
                    err.append(f"mix.{k}: unknown key - {', '.join(sorted(MIX_KEYS))}")
            for k, lo, hi in (("bed_ceiling", -40, 0), ("bed_peak", 0.1, 1), ("fx_peak", 0.1, 1),
                              ("target_lufs", -70, -5), ("target_tp", -20, 0)):
                if k in mx and (isinstance(mx[k], bool) or not isinstance(mx[k], (int, float)) or not lo <= mx[k] <= hi):
                    err.append(f"mix.{k}: number {lo}..{hi}")
            if "hum_hz" in mx and mx["hum_hz"] not in (None, 50, 60, "50", "60", "50hz", "60hz"):
                err.append("mix.hum_hz: 50 | 60")
    td0 = s.get("total_duration")
    if td0 not in (None, "", False):
        try:
            s["total_duration"] = max(0.0, min(MAX_TOTAL_S, float(td0)))
        except (TypeError, ValueError):
            err.append("total_duration: segonn (nonm)")
            s["total_duration"] = None
    else:
        s["total_duration"] = None

    mk0 = s.get("markers")                           # pwen repè sou timeline la (T4): {t, label, color?, dur?, comment?, chapter?}
    if mk0 not in (None, "", False):
        if not isinstance(mk0, list):
            err.append("markers: a list of {t, label, color?}")
            s["markers"] = []
        else:
            out_mk = []
            for j, m in enumerate(mk0):
                if not isinstance(m, dict):
                    err.append(f"markers[{j}]: an object {{t, label}}")
                    continue
                try:
                    t = max(0.0, float(m.get("t")))
                except (TypeError, ValueError):
                    err.append(f"markers[{j}].t: seconds (number)")
                    continue
                col = m.get("color")
                if col is not None and not (isinstance(col, str) and _HEX.match(col)):
                    err.append(f"markers[{j}].color: '#rrggbb'")
                    col = None
                mm = {"t": round(t, 3), "label": _s(m.get("label"))}
                if col:
                    mm["color"] = col
                dur = m.get("dur") if m.get("dur") is not None else m.get("duration")
                if dur is not None:
                    try:
                        dur_f = max(0.0, float(dur))
                        if dur_f > 0:
                            mm["dur"] = round(dur_f, 3)
                    except (TypeError, ValueError):
                        err.append(f"markers[{j}].dur: seconds (number >= 0)")
                if m.get("comment"):
                    mm["comment"] = _s(m.get("comment"))
                if m.get("chapter") not in (None, "", False):
                    mm["chapter"] = True if m.get("chapter") is True else _s(m.get("chapter"))
                out_mk.append(mm)
            s["markers"] = sorted(out_mk, key=lambda x: x["t"])
    else:
        s["markers"] = []

    tr0 = s.get("tracks")                            # tracks adisyonèl (video, audio, sfx, imaj, tèks)
    if tr0 is not None:
        if not isinstance(tr0, list):
            err.append("tracks: a list of track objects")
            s["tracks"] = []
        else:
            out_tr = []
            for j, tk in enumerate(tr0):
                if not isinstance(tk, dict):
                    err.append(f"tracks[{j}]: must be an object")
                    continue
                ttk = dict(tk)
                if "locked" in ttk:
                    ttk["locked"] = bool(ttk["locked"])
                if "sync_lock" in ttk:
                    ttk["sync_lock"] = bool(ttk["sync_lock"])
                if "targeted" in ttk:
                    ttk["targeted"] = bool(ttk["targeted"])
                out_tr.append(ttk)
            s["tracks"] = out_tr

    for k in spec:                                   # REFIZE kle enkoni (O1): fot frap / opsyon ki pa egziste
        if k not in TOP_KEYS:
            err.append(f"{k}: unknown key - {', '.join(sorted(TOP_KEYS))}")
    if "skills" in spec:                             # skills slash devlopè a mande (metadata: WASDEV verifye yo)
        e = _skills_err(spec["skills"], "skills")
        if e:
            err.append(e)
    scenes = s.get("scenes")
    if scenes is None:
        scenes = []
    elif not isinstance(scenes, list):
        err.append("scenes: must be a list of scenes")
        scenes = []
    if len(scenes) > MAX_SCENES:
        err.append(f"scenes: {len(scenes)} scenes - max {MAX_SCENES}")
    out, ids = [], set()
    for i, sc in enumerate(scenes):
        p = f"scenes[{i}]"
        if not isinstance(sc, dict):
            err.append(f"{p}: must be an object")
            continue
        sc = dict(sc)
        for k in sc:                                 # REFIZE kle enkoni nan yon sèn
            if k not in SCENE_KEYS:
                err.append(f"{p}.{k}: unknown key - {', '.join(sorted(SCENE_KEYS))}")
        if "skills" in sc:
            e = _skills_err(sc["skills"], f"{p}.skills")
            if e:
                err.append(e)
        t = _s(sc.get("type"))
        if t not in SCENE_TYPES:
            err.append(f"{p}.type: '{t}' - one of {', '.join(SCENE_TYPES)}")
            continue
        req, lst, lo, hi = SCENE_TYPES[t]
        for f in req:
            if not sc.get(f):
                err.append(f"{p}.{f}: required for '{t}' ({SCENE_HELP[t]})")
        if lst:
            items = sc.get(lst)
            if not isinstance(items, list) or not (lo <= len(items) <= hi):
                err.append(f"{p}.{lst}: {lo}-{hi} entries for '{t}' ({SCENE_HELP[t]})")
                items = []
            if t == "features":
                for j, it in enumerate(items):
                    if not isinstance(it, dict) or not _s(it.get("title")):
                        err.append(f"{p}.items[{j}]: {{icon, title, text?}} with a title")
            if t == "stat":
                for j, it in enumerate(items):
                    if not isinstance(it, dict) or not str(it.get("value", "")).strip():
                        err.append(f"{p}.items[{j}]: {{value, label}} with a value")
            if t in ("list", "code"):
                items = [_line(x) for x in items]
            sc[lst] = items
        if t in ("video", "image"):
            src = _s(sc.get("src"))
            ext = ("." + src.rsplit(".", 1)[-1].lower()) if "." in src else ""
            if src and ext not in (VIDEO_EXT if t == "video" else IMAGE_EXT):
                err.append(f"{p}.src: '{src}' is not a {t} file ({', '.join(VIDEO_EXT if t == 'video' else IMAGE_EXT)})")
            sc["src"] = src
            sc["fit"] = _s(sc.get("fit")) or "cover"
            if sc["fit"] not in FITS:
                err.append(f"{p}.fit: cover | contain")
            sc["camera"] = _camera(sc.get("camera"), f"{p}.camera", err)   # vrè zoom/panoramik
            sc["cards"] = _cards(sc.get("cards"), f"{p}.cards", err)       # kat koupe anime
            lay = _s(sc.get("layout")) or "full"
            if lay not in ("full", "window"):
                err.append(f"{p}.layout: full | window")
                lay = "full"
            sc["layout"] = lay
            bd = sc.get("backdrop", None)                # fon dèyè yon imaj "contain" (olye bann nwa)
            if bd in (None, ""):
                sc["backdrop"] = "blur" if sc["fit"] == "contain" else None   # oto: fon flou pou letterbox
            elif bd is False or (isinstance(bd, str) and _s(bd).lower() in ("none", "off", "black")):
                sc["backdrop"] = None
            elif bd is True or (isinstance(bd, str) and _s(bd).lower() in ("blur", "blurfill")):
                sc["backdrop"] = "blur"
            elif isinstance(bd, str) and _HEX.match(bd):
                sc["backdrop"] = bd
            else:
                err.append(f"{p}.backdrop: true / \"blur\" | \"none\" | #rrggbb")
                sc["backdrop"] = "blur" if sc["fit"] == "contain" else None
            sc["caption"] = _s(sc.get("caption")) or "bottom"
            if sc["caption"] not in CAPTIONS:
                err.append(f"{p}.caption: bottom | center | top")
            sc["zoom"] = bool(sc.get("zoom", t == "image"))
            if t == "video":
                try:
                    sc["in"] = max(0.0, float(sc.get("in") or 0))
                    sc["out"] = float(sc["out"]) if sc.get("out") not in (None, "") else None
                except (TypeError, ValueError):
                    err.append(f"{p}.in / out: seconds (numbers)")
                    sc["in"], sc["out"] = 0.0, None
                if sc["out"] is not None and sc["out"] <= sc["in"] + 0.2:
                    err.append(f"{p}.out: must be after in (+0.2 s)")
                try:
                    a = sc.get("audio")
                    sc["audio"] = None if a in (None, "") else max(0.0, min(1.0, float(a)))
                except (TypeError, ValueError):
                    err.append(f"{p}.audio: clip volume 0-1")
                    sc["audio"] = None
        if t == "html":
            raw = sc.get("html")
            src = _s(sc.get("src"))
            if not (isinstance(raw, str) and raw.strip()) and not src:
                err.append(f"{p}.html: inline HTML (string) OR src (.html file) required ({SCENE_HELP['html']})")
            if src:
                ext = ("." + src.rsplit(".", 1)[-1].lower()) if "." in src else ""
                if ext not in (".html", ".htm"):
                    err.append(f"{p}.src: '{src}' must be a .html file for an html scene")
                sc["src"] = src
            sc["html"] = raw if isinstance(raw, str) else ""
            sc["libs"] = _libs(sc.get("libs"), f"{p}.libs", err)
            sc["camera"] = _camera_html(sc.get("camera"), f"{p}.camera", err)   # kamera + paralaks dekò vektè
        if t == "chart":
            ck = _s(sc.get("chart")).lower()
            if ck not in CHART_KINDS:
                err.append(f"{p}.chart: {' | '.join(CHART_KINDS)}")
            sc["chart"] = ck or "bar"
            for j, it in enumerate(sc.get("items") or []):
                if not isinstance(it, dict) or not _s(it.get("label")) or str(it.get("value", "")).strip() == "":
                    err.append(f"{p}.items[{j}]: {{label, value}} required for a chart")
        if t == "social":
            acts = sc.get("actions") or ["like", "subscribe"]
            if isinstance(acts, str):
                acts = [acts]
            if not isinstance(acts, list):
                err.append(f"{p}.actions: list of {', '.join(SOCIAL_ACTIONS)}")
                acts = ["like", "subscribe"]
            for a in acts:
                if _s(a).lower() not in SOCIAL_ACTIONS:
                    err.append(f"{p}.actions: '{a}' - one of {', '.join(SOCIAL_ACTIONS)}")
            sc["actions"] = [_s(a).lower() for a in acts if _s(a).lower() in SOCIAL_ACTIONS] or ["like", "subscribe"]
            sc["handle"] = _s(sc.get("handle"))
        if t == "lottie":
            src = _s(sc.get("src"))
            if not src:
                err.append(f"{p}.src: Lottie JSON file or URL required ({SCENE_HELP['lottie']})")
            sc["src"] = src
            sc["fit"] = _s(sc.get("fit", "contain")).lower()
            sc["loop"] = bool(sc.get("loop", False))
            try:
                sc["speed"] = float(sc.get("speed", 1.0))
            except (ValueError, TypeError):
                sc["speed"] = 1.0
        if t == "compare":
            for side in ("left", "right"):
                c = sc.get(side)
                if c and (not isinstance(c, dict) or not isinstance(c.get("items", []), list)):
                    err.append(f"{p}.{side}: {{title, items[]}}")
        sid = _s(sc.get("id")) or f"s{i + 1}"
        if sid in ids:
            err.append(f"{p}.id: '{sid}' used twice")
        ids.add(sid)
        sc["id"], sc["type"] = sid, t
        for _mk in ("cards", "camera", "backdrop", "layout", "fit", "caption"):
            allowed_t = ("image", "video", "lottie") if _mk == "fit" else ("image", "video", "html") if _mk == "camera" else ("image", "video")
            if t not in allowed_t and sc.get(_mk) not in (None, "", [], {}):
                err.append(f"{p}.{_mk}: se sèlman sou sèn {', '.join(allowed_t)} (type la se '{t}')")
        sc["focus"] = _focus(sc.get("focus"), f"{p}.focus", err)   # orijin zoom (pa koupe logo sou bò a)
        _raw_tr = _s(sc.get("transition")).lower().strip()
        _clean_tr = _raw_tr.replace(" ", "").replace("_", "")
        _tr = TRANSITION_ALIASES.get(_raw_tr, TRANSITION_ALIASES.get(_clean_tr, _clean_tr))
        if _tr and _tr not in TRANSITIONS:
            _tr = "fade"
        sc["transition"] = _tr   # vid = eritye tranzisyon nivo paj la
        tb = sc.get("title_backdrop", False)                       # bann fonse dèyè tit la (lizibilite)
        if tb in (None, False, "", "none", "off"):
            sc["title_backdrop"] = None
        elif tb is True or (isinstance(tb, str) and _s(tb).lower() in ("on", "true", "blur", "band")):
            sc["title_backdrop"] = True
        elif isinstance(tb, str) and _s(tb).lower() == "auto":
            sc["title_backdrop"] = "auto"
        else:
            err.append(f"{p}.title_backdrop: true | \"auto\" | false")
            sc["title_backdrop"] = None
        if t not in ("video", "image"):
            sc["background"] = background(sc.get("background"), f"{p}.background", err)
        else:
            sc["background"] = None                 # the clip / photo already fills the frame
        sc["overlays"] = overlays(sc.get("overlays"), f"{p}.overlays", err)
        sc["voice"] = _s(sc.get("voice"))
        vf = _s(sc.get("voice_file"))                # VOICE-OVER: your own recording instead of the voice engine
        if vf and ("." + vf.rsplit(".", 1)[-1].lower()) not in AUDIO_EXT:
            err.append(f"{p}.voice_file: '{vf}' is not an audio file ({', '.join(AUDIO_EXT)})")
        sc["voice_file"] = vf or None
        vsp = sc.get("voice_speed")                  # VITÈS VWA sèn sa a (ranplase voice.speed)
        if vsp in (None, ""):
            sc["voice_speed"] = None
        else:
            try:
                sc["voice_speed"] = round(max(VOICE_SPEED[0], min(VOICE_SPEED[1], float(vsp))), 3)
            except (TypeError, ValueError):
                err.append(f"{p}.voice_speed: nonm {VOICE_SPEED[0]}-{VOICE_SPEED[1]} (1 = nòmal)")
                sc["voice_speed"] = None
        if t == "video":                             # VITÈS KLIP la: 0.5 = ralanti, 2 = 2x pi vit (son an swiv)
            try:
                sc["speed"] = round(max(VIDEO_SPEED[0], min(VIDEO_SPEED[1], float(sc.get("speed", 1.0) or 1.0))), 3)
            except (TypeError, ValueError):
                err.append(f"{p}.speed: nonm {VIDEO_SPEED[0]}-{VIDEO_SPEED[1]} (1 = nòmal)")
                sc["speed"] = 1.0
        ls = sc.get("lipsync")                       # bouch data-mouth swiv vwa a (Rhubarb) + je data-eyes bat
        if ls in (None, False, "", "off", "none"):
            if (t == "stickman" or sc.get("stickman")) and (sc.get("voice") or sc.get("speech")):
                sc["lipsync"] = {"blink": True}
            else:
                sc["lipsync"] = None
        elif ls is True or ls == "on":
            sc["lipsync"] = {"blink": True}
        elif isinstance(ls, dict) and set(ls) <= {"blink"}:
            sc["lipsync"] = {"blink": ls.get("blink", True) is not False}
        else:
            err.append(f"{p}.lipsync: true | false | {{\"blink\": true|false}}")
            sc["lipsync"] = None
        spk = sc.get("speaker")                     # MOUN K AP PALE nan sèn nan: pwòp vwa li (dyalòg)
        if spk in (None, "", False):
            sc["speaker"] = None
        elif spk in ("female", "male"):
            sc["speaker"] = {"gender": spk}
        elif isinstance(spk, dict) and set(spk) <= {"gender", "voice_id", "name"} and \
                spk.get("gender", "female") in ("female", "male"):
            sc["speaker"] = {k: str(v) for k, v in spk.items() if v}
        else:
            err.append(f"{p}.speaker: \"female\" | \"male\" | {{\"name\", \"gender\": female|male, \"voice_id\"}}")
            sc["speaker"] = None
        from .sounds import normalize_ambience, normalize_sounds   # son CC0 bibliyotèk la / fichye pa w
        sc["sounds"] = normalize_sounds(sc.get("sounds"), f"{p}.sounds", err)
        sc["ambience"] = normalize_ambience(sc.get("ambience"), f"{p}.ambience", err)
        sc["fx"] = _fx_list(sc.get("fx"), f"{p}.fx", err)   # patikil: pousyè, etensèl, sillage, lapli, lafimen
        if not sc.get("rig") and (t == "stickman" or sc.get("stickman")):
            sm_cfg = sc if t == "stickman" else (sc.get("stickman") if isinstance(sc.get("stickman"), dict) else {})
            sm_name = sm_cfg.get("name") or sm_cfg.get("speaker") or "Stickman"
            actions = sm_cfg.get("do") or [{"do": "talk" if (sc.get("voice") or sc.get("speech")) else "idle"}]
            sc["rig"] = {sm_name: {"face": sm_cfg.get("face", "right"), "idle": True, "ground": True, "do": actions}}
        from .motion import normalize as _rig_norm      # pèsonaj cut-out ki mache / kouri / chita (rig Design)
        sc["rig"] = _rig_norm(sc.get("rig"), f"{p}.rig", err)
        tm = sc.get("timing") or sc.get("responsive_timing")
        if tm not in (None, False, ""):
            if isinstance(tm, dict):
                try:
                    sc["timing"] = {
                        "intro": max(0.0, float(tm.get("intro", 0.5))),
                        "outro": max(0.0, float(tm.get("outro", 0.5))),
                        "design": max(0.1, float(tm.get("design", tm.get("intro", 0.5) + tm.get("outro", 0.5) + 1.0)))
                    }
                except (ValueError, TypeError):
                    err.append(f"{p}.timing: {{'intro': seconds, 'outro': seconds, 'design'?: seconds}}")
                    sc["timing"] = None
            else:
                err.append(f"{p}.timing: {{'intro': seconds, 'outro': seconds, 'design'?: seconds}}")
                sc["timing"] = None
        else:
            sc["timing"] = None
        d = sc.get("duration")
        if d not in (None, ""):
            try:
                sc["duration"] = max(MIN_SCENE, min(30.0, float(d)))
            except (TypeError, ValueError):
                err.append(f"{p}.duration: seconds (number)")
                sc["duration"] = None
        else:
            sc["duration"] = None
        out.append(sc)
    td = s.get("total_duration")                     # distribye / verifye total_duration
    if td and out:
        fixed = sum(sc["duration"] for sc in out if sc.get("duration"))
        free = [sc for sc in out if not sc.get("duration")]
        if not free:
            if abs(fixed - td) > 0.05:
                # Olye erè fatak ki bloke rann lan, senkronize total_duration sou som reyèl sèn yo
                s["total_duration"] = round(fixed, 3)
        else:
            need = [max(MIN_SCENE, LEAD_IN + estimate_voice(sc.get("voice", "")) + TAIL) for sc in free]
            rest = td - fixed
            if rest < sum(need) - 0.05:
                # Olye erè ki koupe vwa oswa bloke rann lan, elaji total_duration pou tout vwa anfòm san koupe!
                min_needed = fixed + sum(need)
                s["total_duration"] = round(min_needed, 3)
                rest = min_needed - fixed
                k = 1.0
                for sc, nd in zip(free, need):
                    sc["duration"] = round(nd * k, 3)
            else:
                k = rest / sum(need)
                for sc, nd in zip(free, need):
                    sc["duration"] = round(nd * k, 3)
    s["libs"] = _libs(s.get("libs"), "libs", err)
    _raw_ptr = _s(s.get("transition")).lower().strip()
    _clean_ptr = _raw_ptr.replace(" ", "").replace("_", "")
    _ptr = TRANSITION_ALIASES.get(_raw_ptr, TRANSITION_ALIASES.get(_clean_ptr, _clean_ptr))
    if _ptr and _ptr not in TRANSITIONS:
        _ptr = "fade"
    s["transition"] = _ptr or "fade"
    s["scenes"] = out
    if err:
        raise SpecError(err)
    return s


def estimate_voice(text: str) -> float:
    """Seconds a voice line will take, before it is synthesized (replaced by the real WAV length later)."""
    words = len(re.findall(r"\w+", text or ""))
    return 0.0 if not words else words / WORDS_PER_S + 0.25


def anim_need(sc: dict) -> float:
    """Seconds the scene's entrance animations need (so a short voice line never cuts them off)."""
    n = len(sc.get("items") or sc.get("lines") or []) + len(sc.get("chips") or [])
    if sc["type"] == "compare":
        n = len((sc.get("left") or {}).get("items") or []) + len((sc.get("right") or {}).get("items") or [])
    return max(MIN_SCENE, 1.4 + 0.45 * n)


def clip_length(sc: dict, media_s: dict | None) -> float | None:
    """Usable seconds of a video scene's clip after trimming (None = unknown: not probed yet)."""
    if sc["type"] != "video":
        return None
    full = (media_s or {}).get(sc["id"])
    end = sc.get("out") if sc.get("out") is not None else full
    if end is None:
        return None
    if full is not None:
        end = min(end, full)
    return max(0.2, (end - sc.get("in", 0.0)) / float(sc.get("speed") or 1.0))   # 2x pi vit = mwatye tan


_TOKEN = re.compile(r"\S+")


def estimate_words(text: str, dur: float) -> list[list]:
    """Word timing without a speech recognizer: time shared by word length, with pauses after punctuation.
    [[word, start, end], ...] relative to the start of the voice line."""
    toks = _TOKEN.findall(text or "")
    if not toks or dur <= 0:
        return []
    wts = [len(t) + 1.5 + (3.0 if t[-1] in ",;:" else 5.0 if t[-1] in ".!?…" else 0.0) for t in toks]
    k, at, out = dur / sum(wts), 0.0, []
    for t, wt in zip(toks, wts):
        speak = (len(t) + 1.5) * k
        out.append([t, round(at, 3), round(at + speak, 3)])
        at += wt * k
    return out


def timeline(spec: dict, voice_s: dict | None = None, media_s: dict | None = None,
             words_s: dict | None = None, mouth_s: dict | None = None) -> list[dict]:
    """Scene start / length on the video clock. voice_s = {scene id: real voice seconds} (missing -> estimate);
    media_s = {scene id: full clip seconds} (video scenes). A video scene lasts as long as its trimmed clip unless a
    duration is given (a longer voice line extends it: the last frame holds).
    words_s = {scene id: [[word, start, end], ...]} relative to the voice line (speech recognizer; missing ->
    estimated). mouth_s = {scene id: [[start, end, shape], ...]} relative to the voice line (Rhubarb; missing ->
    estimated from the words) for `lipsync` scenes.
    Returns [{id, start, dur, voice_at, voice_dur, last, clip?, words: [{w, s, e}], mouth?: [[s, e, shape]],
    blink?, rig?: {name: {face, idle, ground, drawn, do: [actions with at / dur in scene seconds]}}} with absolute
    times]."""
    voice_s = voice_s or {}
    tl, t = [], 0.0
    for i, sc in enumerate(spec["scenes"]):
        vd = voice_s.get(sc["id"])
        measured = vd is not None                          # v3.12: vrè fichye vwa a (pa yon estimasyon 2,6 mo/s)
        if vd is None:
            vd = estimate_voice(sc.get("voice", ""))
        clip = clip_length(sc, media_s)
        if sc["type"] == "video":
            base = clip if clip is not None else 4.0          # not probed yet: placeholder length
        elif sc["type"] == "image":
            base = 3.5
        else:
            base = anim_need(sc)
        words = None
        if (sc.get("voice") or sc.get("voice_file")) and vd:
            ws = (words_s or {}).get(sc["id"]) or estimate_words(sc.get("voice") or "", vd)
            at = t + LEAD_IN
            words = [{"w": w, "s": round(at + a, 3), "e": round(at + b, 3)} for w, a, b in ws]
        if not sc.get("rig") and (sc.get("type") == "stickman" or sc.get("stickman")):
            sm_cfg = sc if sc.get("type") == "stickman" else (sc.get("stickman") if isinstance(sc.get("stickman"), dict) else {})
            sm_name = sm_cfg.get("name") or sm_cfg.get("speaker") or "Stickman"
            actions = sm_cfg.get("do") or [{"do": "talk" if (sc.get("voice") or sc.get("speech")) else "idle"}]
            sc["rig"] = {sm_name: {"face": sm_cfg.get("face", "right"), "idle": True, "ground": True, "do": actions}}
        if (sc.get("type") == "stickman" or sc.get("stickman")) and "lipsync" not in sc and (sc.get("voice") or sc.get("speech")):
            sc["lipsync"] = {"blink": True}
        rig = None
        if sc.get("rig"):                                  # aksyon pèsonaj yo: «at» yon mo → lè vwa a di l
            from .motion import need as _rig_need, resolve as _rig_resolve
            rig = _rig_resolve(sc["rig"], words, t)
            base = max(base, _rig_need(rig))
        # RÈG OBLIGATWA (devlopè a, 2026-10-20): yon vwa PA JANM koupe. Yon «duration» AI a bay se yon MINIMÒM:
        # si vwa a (+ LEAD_IN avan + TAIL apre) pi long, sèn nan alonje (anvan: duration te ranplase l → fen koupe).
        need_v = (LEAD_IN + vd + TAIL) if vd else 0.0
        dur = max(sc["duration"], need_v) if sc["duration"] else max(MIN_SCENE, base, need_v)
        # need = sa vwa a bezwen (editè a pa janm montre yon sèn pi kout pase sa: sèvè a ta alonje l kanmenm)
        tl.append({"id": sc["id"], "start": round(t, 3), "dur": round(dur, 3), "voice_at": round(t + LEAD_IN, 3),
                   "voice_dur": round(vd, 3), "need": round(need_v, 3),
                   "measured": bool(measured and vd), "last": i == len(spec["scenes"]) - 1})
        if clip is not None:
            tl[-1]["clip"] = round(clip, 3)
        if words is not None:
            tl[-1]["words"] = words
        if rig:
            tl[-1]["rig"] = rig
        if sc["type"] == "html" and sc.get("camera"):    # kamera dekò vektè (compose.py camApply)
            tl[-1]["camera"] = sc["camera"]
        if isinstance(sc.get("fx"), list):                # patikil detèminis (compose.py fxApply)
            tl[-1]["fx"] = sc["fx"]
        if sc.get("lipsync"):
            from .lipsync import from_words
            rel = (mouth_s or {}).get(sc["id"])
            at = t + LEAD_IN
            tl[-1]["mouth"] = ([[round(at + a, 3), round(at + b, 3), x] for a, b, x in rel] if rel
                               else from_words(tl[-1].get("words") or []))
            tl[-1]["blink"] = sc["lipsync"]["blink"]
        if sc.get("timing"):
            tl[-1]["timing"] = sc["timing"]
        t += dur
    if t > MAX_TOTAL_S:
        raise SpecError([f"total: {t:.0f} s - max {MAX_TOTAL_S} s (shorten voice lines or remove scenes)"])
    return tl


def ensure_ids(spec: dict) -> bool:
    """v3.12 — ID ESTAB: bay chak sèn ki pa gen `id` yon id inik, epi chanje yon id ki repete (validate refize l).
    Menm chema ak validate (`s<n>` = pozisyon an si l lib): yon spec san id jwenn menm id yo isit la ak nan aperçu a.
    Apre sa id a rete menm lè yo ajoute / deplase sèn (anvan: editè a pa t jwenn dire reyèl yon sèn san id → 2 s).
    Chanje spec la sou plas; True = yon bagay chanje (pou moun ki rele l la sove l)."""
    scenes = spec.get("scenes") if isinstance(spec, dict) else None
    if not isinstance(scenes, list):
        return False
    used, changed, todo = set(), False, []
    for i, sc in enumerate(scenes):
        if not isinstance(sc, dict):
            continue
        sid = _s(sc.get("id"))
        if sid and sid not in used:
            used.add(sid)
            if sc.get("id") != sid:
                sc["id"], changed = sid, True
        else:
            todo.append((i, sc))
    n = 0
    for i, sc in todo:
        sid = f"s{i + 1}"
        while sid in used:
            n += 1
            sid = f"s{len(scenes) + n}"
        sc["id"] = sid
        used.add(sid)
        changed = True
    return changed


def total(tl: list[dict], spec: dict | None = None) -> float:
    t = round(tl[-1]["start"] + tl[-1]["dur"], 3) if tl else 0.0
    if spec and isinstance(spec, dict):
        for tk in spec.get("tracks") or []:
            for c in tk.get("clips") or []:
                try:
                    st = float(c.get("start", 0) or 0)
                    du = float(c.get("dur", 0) or 0)
                    if st + du > t:
                        t = st + du
                except (TypeError, ValueError):
                    pass
        if spec.get("total_duration"):
            try:
                td = float(spec["total_duration"])
                if td > t:
                    t = td
            except (TypeError, ValueError):
                pass
    return round(t, 3)


def json_schema() -> dict:
    """JSON Schema of the spec (for AI tool definitions / editors)."""
    color = {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"}
    item = {"type": "object", "properties": {"on": {"type": "string", "description": "spoken word that makes it appear"},
                                             "icon": {"type": "string"}, "title": {"type": "string"},
                                             "text": {"type": "string"}, "value": {"type": "string"},
                                             "label": {"type": "string"}}}
    bg = {"type": ["object", "string", "null"], "description": "picture / video / design asset behind the scene",
          "properties": {"src": {"type": "string"}, "fit": {"enum": list(FITS)}, "opacity": {"type": "number"},
                         "dim": {"type": "number", "description": "0-0.95 darkening for readable text"},
                         "zoom": {"type": "boolean"}, "tint": {"type": "string"}, "tint_strength": {"type": "number"}, "color": {"type": "string"},
                         "in": {"type": "number"}, "out": {"type": "number"}}}
    ovs = {"type": "array", "maxItems": MAX_OVERLAYS, "description": "atmosphere layers (smoke, light, splash, shapes)",
           "items": {"type": ["object", "string"], "properties": {
               "src": {"type": "string"}, "layer": {"enum": list(LAYERS)}, "blend": {"enum": list(BLENDS)},
               "anim": {"enum": list(OV_ANIMS)}, "opacity": {"type": "number"}, "x": {"type": "number"},
               "y": {"type": "number"}, "w": {"type": "number", "description": "width, fraction of the frame"},
               "speed": {"type": "number"}, "rotate": {"type": "number"},
               "color": {"type": "string", "description": "#rrggbb or primary / accent / text"}}}}
    side = {"type": "object", "properties": {"title": {"type": "string"},
                                             "items": {"type": "array", "items": {"type": "string"}}}}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Kadans WASDEV spec", "type": "object",
        "required": ["scenes"],
        "properties": {
            "kadans": {"const": SPEC_VERSION}, "title": {"type": "string"}, "lang": {"type": "string"},
            "ratio": {"enum": list(RATIOS)}, "fps": {"type": "integer", "minimum": 12, "maximum": 60},
            "credit": {"type": "boolean"}, "progress_bar": {"type": "boolean"},
            "captions": {"type": ["object", "boolean"], "description": "animated word-by-word captions: one sentence "
                         "per line (cut on punctuation when too long). Words come from scene voices AND from voice "
                         "clips on audio tracks (their <file>.words.json, or clip.words)",
                         "properties": {"style": {"enum": list(CAPTION_STYLES)},
                                        "position": {"enum": ["bottom", "top", "middle"]},
                                        "colors": {"type": "object", "description": "word colours #rrggbb[aa]",
                                                   "properties": {k: {"type": "string"} for k in CAPTION_COLORS}},
                                        "size": {"type": "number", "minimum": 24, "maximum": 140,
                                                 "description": "font size in px at 1080 (default 58)"},
                                        "max_words": {"type": "integer", "minimum": 2, "maximum": 20},
                                        "max_chars": {"type": "integer", "minimum": 12, "maximum": 120},
                                        "min_words": {"type": "integer", "minimum": 1, "maximum": 6}}},
            "sfx": {"type": ["object", "boolean"], "description": "automatic sound effects: whoosh (scene "
                    "change), pop (items), hit (logo / cta), type (keyboard while code types), text (title appears); "
                    "false = none", "properties": {"volume": {"type": "number", "minimum": 0, "maximum": 1},
                                                   **{k: {"type": "boolean"} for k in SFX_KINDS}}},
            "look": {"type": ["object", "boolean"], "description": "cinematic finish after capture (default on)",
                     "properties": {k: {"type": "number", "minimum": 0, "maximum": 1} for k in DEFAULT_LOOK}},
            "motion_blur": {"enum": list(MOTION_BLUR), "description": "sub-frames averaged per frame (slower)"},
            "mix": {"type": "object", "description": "music, SFX, clip and track sound never louder than the voice "
                    "(on by default)", "properties": {
                        "cap": {"type": "boolean", "description": "false = no ceiling"},
                        "bed_ceiling": {"type": "number", "minimum": -40, "maximum": 0,
                                        "description": "loudest moment of the bed vs voice level, LU (default -4)"},
                        "bed_peak": {"type": "number", "minimum": 0.1, "maximum": 1,
                                     "description": "bed peak as a fraction of the voice peak (default 0.6)"},
                        "duck": {"type": "boolean", "description": "lower the bed while the voice speaks (default true)"},
                        "fx_peak": {"type": "number", "minimum": 0.1, "maximum": 1,
                                    "description": "SFX bus peak as a fraction of the voice peak (default 0.9)"},
                        "fx_duck": {"type": "boolean", "description": "light 2.5:1 dip of the SFX while the voice "
                                    "speaks (default true; music keeps its full duck)"}}},
            "brand": {"type": "object", "properties": {
                "name": {"type": "string", "description": "*part* = highlighted, e.g. WAS*DEV*"},
                "logo": {"type": "string", "description": "path to an SVG / PNG / JPG"},
                "font": {"type": "string", "description": "body font: any installed family (kadans fonts)"},
                "font_title": {"type": "string", "description": "titles, buttons, numbers"},
                "font_code": {"type": "string", "description": "code scenes"},
                "colors": {"type": "object", "properties": {k: color for k in DEFAULT_COLORS}}}},
            "voice": {"type": ["object", "null"], "properties": {
                "engine": {"type": "string"}, "gender": {"enum": list(GENDERS)}, "sample": {"type": "string"},
                "lang": {"type": "string"}}},
            "music": {"type": ["object", "null"], "properties": {
                "mood": {"enum": list(MOODS)}, "file": {"type": "string"}, "seed": {"type": "integer"},
                "volume": {"type": "number", "minimum": 0, "maximum": 1}}},
            "scenes": {"type": "array", "minItems": 1, "maxItems": MAX_SCENES, "items": {
                "type": "object", "required": ["type"],
                "description": " | ".join(f"{k}: {v}" for k, v in SCENE_HELP.items()),
                "properties": {
                    "id": {"type": "string"}, "type": {"enum": list(SCENE_TYPES)},
                    "title": {"type": "string", "description": "*word* = highlighted"},
                    "subtitle": {"type": "string"}, "tagline": {"type": "string"},
                    "voice": {"type": "string", "description": "narration spoken during this scene"},
                    "voice_file": {"type": "string", "description": "your own recording for this scene (voice-over: "
                                   "replaces the voice engine; 'voice' = its text, optional — transcribed if absent)"},
                    "duration": {"type": "number", "description": "seconds (optional: follows the voice)"},
                    "items": {"type": "array", "items": {"anyOf": [{"type": "string"}, item]}},
                    "lines": {"type": "array", "items": {"type": "string"}},
                    "chips": {"type": "array", "items": {"type": ["string", "object"], "description":
                              "label, or {title, on: spoken word that makes it appear}"}},
                    "left": side, "right": side,
                    "src": {"type": "string", "description": "video / image file (video, image scenes)"},
                    "in": {"type": "number"}, "out": {"type": "number"},
                    "fit": {"enum": list(FITS)}, "caption": {"enum": list(CAPTIONS)},
                    "audio": {"type": "number", "minimum": 0, "maximum": 1}, "zoom": {"type": "boolean"},
                    "lipsync": {"type": ["boolean", "object"], "description": "mouths [data-mouth] > [data-shape=A..H|X] "
                                "follow this scene's voice (Rhubarb Lip Sync, local); eyes [data-eyes] > "
                                "[data-eye=open|half|closed] blink", "properties": {"blink": {"type": "boolean"}}},
                    "sounds": {"type": "array", "description": "sound effects of this scene: \"find:rooster\" "
                               "(CC0 library search, any language), \"sfx:id\" or a file; or {src, at (s or a spoken "
                               "word), dur, volume 0-2, loop, fade, bus fx|bed}"},
                    "speaker": {"type": ["string", "object"], "description": "who speaks this scene's voice line "
                                "(dialogue): \"female\" | \"male\" | {name, gender, voice_id} — overrides the video "
                                "voice for this scene"},
                    "ambience": {"type": ["string", "object"], "description": "background sound looping under the "
                                 "whole scene (bed, ducked under the voice): \"find:crickets night\" or {src, volume, "
                                 "fade}"},
                    "rig": {"type": "object", "description": "cut-out characters exported from Design ([data-rig=name]) "
                            "move: {name: [{do: walk|run|jump|sit|stand|wave|talk|nod|point|cheer|fall|fly|glide|hop|"
                            "idle|pose, at (s or a spoken word), dur, to [x, y] | by [dx, dy] | path [[x, y]...] "
                            "(video px, feet point), face right|left|auto, speed, amount, side r|l, ease, angles}]} "
                            "or {name: {face, idle, ground, drawn, expr, light, do: [...]}} — light: auto | night | moon | "
                            "candle | dusk | day | indoor | {tint, amount, rim, rim_side, shadow, glow} (the character "
                            "takes the background's light; auto reads the scene image)"},
                    "camera": {"type": "object", "description": "image / video: {from:{zoom,x,y}, to:{zoom,x,y}, ease}. "
                               "html (vector set from Design, layers 'fon 1'..'fon 6' or data-depth 0-1): {pan [x, y] px "
                               "the camera travels (+x = right), zoom 1.05 | [from, to], origin [x, y], ease, follow "
                               "\"Lina\" | {rig, amount 0-1, offset}, shake [{at s, force px, dur s}], depth {layer name: "
                               "0-1}, limit px} — far layers move less (parallax), deterministic"},
                    "fx": {"type": ["array", "object"], "description": "deterministic particles: [{type: dust|sparks|"
                           "trail|rain|smoke, at s, dur s, x, y (px; trail: follow rig name + offset), color, count, "
                           "size, seed, spread, speed, opacity, angle}]"},
                    "background": bg, "overlays": ovs}}},
            "background": bg, "overlays": ovs,
        },
    }


# ----------------------------------------------------------------------------------------------- exact timebase
# Drift-free integer timebase (SMPTE / professional NLE standard)
# 254,016,000,000 ticks/sec is evenly divisible by 24, 25, 30, 48, 50, 60, 120, 240 fps,
# NTSC drop-frame rates (23.976, 29.97, 59.94), and 44.1k/48k/96k/192k audio rates.
TICKS_PER_SECOND = 254_016_000_000


def sec_to_ticks(seconds: float | int) -> int:
    """Konvèti segonn an ticks antye san drift."""
    try:
        return int(round(float(seconds) * TICKS_PER_SECOND))
    except (TypeError, ValueError):
        return 0


def ticks_to_sec(ticks: int) -> float:
    """Konvèti ticks antye an segonn (float)."""
    try:
        return float(ticks) / TICKS_PER_SECOND
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


def frames_to_ticks(frames: int, fps: float = 30.0) -> int:
    """Konvèti kantite imaj (frames) an ticks."""
    fps = max(1.0, float(fps))
    return int(round((frames * TICKS_PER_SECOND) / fps))


def ticks_to_frames(ticks: int, fps: float = 30.0) -> int:
    """Konvèti ticks an kantite imaj (frames)."""
    fps = max(1.0, float(fps))
    return int(round((ticks * fps) / TICKS_PER_SECOND))


def quantize_time(seconds: float | int, fps: float = 30.0) -> float:
    """Aliyen tan an egzakteman sou fwontyè ki pi pre yon frame (evite sub-frame drift)."""
    fps = max(1.0, float(fps))
    t = sec_to_ticks(seconds)
    f = ticks_to_frames(t, fps)
    return round(float(f) / fps, 6)


def timecode(seconds: float | int, fps: float = 30.0, drop_frame: bool = False) -> str:
    """Konvèti segonn an kòd tan estanda SMPTE HH:MM:SS:FF (oswa HH:MM:SS;FF pou drop-frame)."""
    fps = max(1.0, float(fps))
    total_frames = max(0, int(round(float(seconds) * fps)))
    int_fps = int(round(fps))
    ff = total_frames % int_fps
    total_sec = total_frames // int_fps
    ss = total_sec % 60
    mm = (total_sec // 60) % 60
    hh = total_sec // 3600
    sep = ";" if drop_frame else ":"
    return f"{hh:02d}:{mm:02d}:{ss:02d}{sep}{ff:02d}"


def parse_timecode(tc_str: str, fps: float = 30.0) -> float:
    """Li yon kòd tan SMPTE (HH:MM:SS:FF oswa HH:MM:SS;FF) oswa HH:MM:SS.mmm epi retounen segonn."""
    s = str(tc_str or "").strip()
    if not s:
        return 0.0
    fps = max(1.0, float(fps))
    m = re.match(r"^(\d+):(\d{2}):(\d{2})[:;](\d+)$", s)
    if m:
        hh, mm, ss, ff = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        return (hh * 3600) + (mm * 60) + ss + (ff / fps)
    m = re.match(r"^(\d+):(\d{2}):(\d{2})(?:\.(\d+))?$", s)
    if m:
        hh, mm, ss = int(m.group(1)), int(m.group(2)), int(m.group(3))
        ms = float(f"0.{m.group(4)}") if m.group(4) else 0.0
        return (hh * 3600) + (mm * 60) + ss + ms
    try:
        return float(s)
    except ValueError:
        return 0.0
