"""SOUNDS — bibliyotèk son CC0 (ambyans, bruitage) + son yon sèn (`sounds`, `ambience`) + pa pèsonaj yo (rig `steps`).

Bibliyotèk la: `assets/sfx/index.json` (57 son CC0: krikèt, krapo, nwit twopikal, kòk, chen, zwazo, lanmè, van,
lapli, loraj, dife, foul, bravo, lari, timoun, moto, klòch, limyè k ap limen, papye, kreyon, zèl, pòt, pa sou
bwa / beton / zèb…, frape, penso, majik, pop, boing, kè…) + dosye anplis nan KADANS_SFX_DIRS (separe ak os.pathsep):
yon dosye ki gen pwòp index.json li, oswa jis fichye odyo (non fichye a = tag yo).

Nan yon spec: «find:krikèt nwit» (rechèch: kreyòl, franse, angle — aksan / majiskil pa konte), «sfx:rooster» (id
egzak), oswa yon chemen fichye. Yon son ki gen plizyè VARYANT (pa sou bwa: 5) chanje chak fwa li jwe.
"""
from __future__ import annotations

import json
import os
import unicodedata
from pathlib import Path

LIB = Path(__file__).with_name("assets") / "sfx"
AUDIO_EXT = (".ogg", ".wav", ".mp3", ".m4a", ".flac", ".opus", ".aac")
BUSES = ("fx", "bed")
SURFACES = {"soft": "footstep-soft", "dirt": "footstep-soft", "concrete": "footstep-concrete",
            "grass": "footstep-grass", "wood": "footstep-wood", "snow": "footstep-snow", "carpet": "footstep-carpet",
            "metal": "impact-metal", "tin": "impact-metal", "tè": "footstep-soft", "beton": "footstep-concrete",
            "zèb": "footstep-grass", "bwa": "footstep-wood", "tòl": "impact-metal", "tapi": "footstep-carpet"}
SOUND_KEYS = {"src", "at", "dur", "volume", "loop", "fade", "bus"}
_CACHE: dict = {}


def _plain(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn")
    return " ".join("".join(c if c.isalnum() else " " for c in s).split())


def roots() -> list[Path]:
    out = [LIB]
    for d in (os.environ.get("KADANS_SFX_DIRS") or "").split(os.pathsep):
        if d.strip() and Path(d.strip()).is_dir():
            out.append(Path(d.strip()))
    return out


def library() -> list[dict]:
    """Tout son yo: [{id, files (chemen konplè), kind sfx|ambience, loop, tags, dur, title, author, source,
    license}] — kach la rekonstwi lè yon index.json chanje."""
    key = tuple((str(r), (r / "index.json").stat().st_mtime if (r / "index.json").is_file() else
                 sum(1 for _ in r.iterdir())) for r in roots())
    if _CACHE.get("key") == key:
        return _CACHE["lib"]
    lib, seen = [], set()
    for r in roots():
        idx = r / "index.json"
        if idx.is_file():
            try:
                items = json.loads(idx.read_text(encoding="utf-8")).get("sounds") or []
            except (OSError, ValueError):
                items = []
            for e in items:
                files = [r / f for f in e.get("files") or [] if (r / f).is_file()]
                if files and e.get("id") not in seen:
                    seen.add(e["id"])
                    lib.append({**e, "files": files})
        else:                                            # dosye san index: chak fichye = yon son
            for f in sorted(r.iterdir()):
                if f.suffix.lower() in AUDIO_EXT and f.stem not in seen:
                    seen.add(f.stem)
                    lib.append({"id": f.stem, "files": [f], "kind": "sfx", "loop": False,
                                "tags": _plain(f.stem).split(), "dur": None, "title": f.stem, "license": "?"})
    _CACHE.update(key=key, lib=lib)
    return lib


def search(query: str, kind: str | None = None, limit: int = 12) -> list[dict]:
    """Son ki pi koresponn ak mo yo (id 3 pwen, tag egzak 2, kòmansman yon tag 1, tit 1)."""
    words = _plain(query).split()
    out = []
    for e in library():
        if kind and e.get("kind") != kind:
            continue
        tags = [_plain(t) for t in e.get("tags") or []]
        ident, title = _plain(e["id"]), _plain(e.get("title", ""))
        score = 0.0
        for w in words:
            if w in ident.split():
                score += 3
            if w in tags:
                score += 2
            elif len(w) >= 4 and any(t.startswith(w) or w.startswith(t) and len(t) >= 4 for t in tags):
                score += 1
            if len(w) >= 4 and w in title:
                score += 1
        if score > 0:
            out.append((score, e))
    out.sort(key=lambda x: (-x[0], x[1]["id"]))
    return [e for _s, e in out[:limit]]


def by_id(sid: str) -> dict | None:
    return next((e for e in library() if e["id"] == sid), None)


def entry(src: str, base: Path | None = None) -> dict | None:
    """«find:…» / «sfx:id» / chemen → antre bibliyotèk la (oswa yon antre pou fichye a)."""
    s = str(src or "").strip()
    if s.startswith("find:"):
        hit = search(s[5:], limit=1)
        return hit[0] if hit else None
    if s.startswith("sfx:"):
        return by_id(s[4:].strip())
    from .media import resolve
    p = resolve(s, base)
    return {"id": p.stem, "files": [p], "kind": "sfx", "loop": False, "dur": None} if p.is_file() else None


def resolve(src: str, base: Path | None = None, seed: int = 0) -> Path | None:
    """Fichye pou jwe a (varyant seed % n). None = pa jwenn."""
    e = entry(src, base)
    return e["files"][seed % len(e["files"])] if e else None


def length(path: Path) -> float:
    for e in library():
        if path in e["files"] and e.get("dur"):
            return float(e["dur"])
    from .media import probe_audio
    try:
        return probe_audio(path)
    except Exception:                                    # noqa: BLE001
        return 2.0


# ------------------------------------------------------------------ spec
def _num(v, p, err, lo, hi, d):
    if v is None:
        return d
    try:
        return max(lo, min(hi, float(v)))
    except (TypeError, ValueError):
        err.append(f"{p}: number")
        return d


def normalize_sounds(v, p: str, err: list) -> list:
    """Kle sèn `sounds`: [«find:kòk»] oswa [{src, at (s / yon mo), dur, volume 0-2, loop, fade, bus fx|bed}]."""
    if v in (None, False, [], ""):
        return []
    if isinstance(v, (str, dict)):
        v = [v]
    if not isinstance(v, list):
        err.append(f"{p}: [\"find:rooster\", {{\"src\": \"find:door creak\", \"at\": 2.5}}]")
        return []
    out = []
    for i, it in enumerate(v):
        q = f"{p}[{i}]"
        if isinstance(it, str):
            it = {"src": it}
        if not isinstance(it, dict) or not str(it.get("src") or "").strip():
            err.append(f"{q}: {{\"src\": \"find:…\" | \"sfx:id\" | file, \"at\": …}}")
            continue
        bad = set(it) - SOUND_KEYS
        if bad:
            err.append(f"{q}: unknown key(s) {', '.join(sorted(bad))} (use {', '.join(sorted(SOUND_KEYS))})")
        x = {"src": str(it["src"]).strip()}
        at = it.get("at")
        x["at"] = at.strip() if isinstance(at, str) and at.strip() else _num(at, f"{q}.at", err, 0, 600, 0.0)
        x["dur"] = _num(it.get("dur"), f"{q}.dur", err, 0.05, 600, None)
        x["volume"] = _num(it.get("volume"), f"{q}.volume", err, 0, 2, 1.0)
        x["fade"] = _num(it.get("fade"), f"{q}.fade", err, 0, 10, None)
        if it.get("loop") not in (None, True, False):
            err.append(f"{q}.loop: true | false")
        x["loop"] = it.get("loop")
        if it.get("bus") is not None and it["bus"] not in BUSES:
            err.append(f"{q}.bus: fx (short effects, own bus) | bed (ambience, under the voice like music)")
        x["bus"] = it.get("bus")
        out.append(x)
    return out


def normalize_ambience(v, p: str, err: list) -> dict | None:
    """Kle sèn `ambience`: «find:krikèt» oswa {src, volume, fade}: son fon an pandan tout sèn nan (an bouk)."""
    if v in (None, False, ""):
        return None
    if isinstance(v, str):
        v = {"src": v}
    if not isinstance(v, dict) or not str(v.get("src") or "").strip() or set(v) - {"src", "volume", "fade"}:
        err.append(f"{p}: \"find:crickets night\" | {{\"src\", \"volume\", \"fade\"}}")
        return None
    return {"src": str(v["src"]).strip(), "volume": _num(v.get("volume"), f"{p}.volume", err, 0, 2, 0.6),
            "fade": _num(v.get("fade"), f"{p}.fade", err, 0, 10, 0.8)}


def scene_cues(sc: dict, t: dict) -> list[dict]:
    """Son yon sèn sou lè videyo a: [{src, t, dur, volume, loop, fade, bus}] (dur None = longè fichye a)."""
    from .compose import _find_word
    out = []
    amb = sc.get("ambience")
    if amb:
        out.append({"src": amb["src"], "t": t["start"], "dur": amb.get("dur", t["dur"]), "volume": amb.get("volume", 1.0), "loop": amb.get("loop", True),
                    "fade": amb.get("fade", 0.6), "bus": amb.get("bus", "bed")})
    for s in sc.get("sounds") or []:
        at = s.get("at", 0.0)
        if isinstance(at, str):
            wd = _find_word(t.get("words") or [], at, t["start"])
            at = (wd["s"] - t["start"]) if wd else 0.0
        out.append({"src": s["src"], "t": round(t["start"] + float(at), 3), "dur": s.get("dur"), "volume": s.get("volume", 1.0),
                    "loop": s.get("loop", False), "fade": s.get("fade"), "bus": s.get("bus", "fx"), "word": s.get("at") if isinstance(s.get("at"), str)
                    else None})
    return out


def clips(spec: dict, tl: list[dict], base: Path | None = None, total: float | None = None) -> tuple[list, list]:
    """Tout son sèn yo + pa pèsonaj yo → klip pou mix la: ([{path, start, dur, volume, fadein, fadeout, fx, loop}],
    [son ki pa jwenn])."""
    out, missing = [], []
    by_id_ = {x["id"]: x for x in tl}
    used: dict = {}
    for sc in spec["scenes"]:
        t = by_id_[sc["id"]]
        cues = scene_cues(sc, t)
        from .motion import step_cues
        cues += step_cues(sc, t, base)
        for c in cues:
            e = entry(c["src"], base)
            if e is None:
                missing.append({"scene": sc["id"], "src": c["src"]})
                continue
            n = used.get(e["id"], 0)
            used[e["id"]] = n + 1
            path = e["files"][n % len(e["files"])]
            loop = c["loop"] if c["loop"] is not None else bool(e.get("loop"))
            natural = length(path)
            dur = float(c["dur"]) if c["dur"] else (t["start"] + t["dur"] - c["t"] if loop else natural)
            if not loop:
                dur = min(dur, natural)
            if total is not None:
                dur = min(dur, max(0.0, total - c["t"]))
            if dur <= 0.02:
                continue
            fade = c["fade"] if c["fade"] is not None else (0.6 if loop else 0.0)
            bus = c["bus"] or ("bed" if e.get("kind") == "ambience" or loop else "fx")
            out.append({"path": path, "start": c["t"], "dur": round(dur, 3), "volume": c["volume"],
                        "fadein": min(fade, dur / 2), "fadeout": min(max(fade, 0.03), dur / 2),
                        "fx": bus == "fx", "loop": loop})
    return out, missing
