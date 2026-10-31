"""LIPSYNC — bouch pèsonaj yo swiv vwa a, je yo bat.

- Rhubarb Lip Sync (Daniel S. Wolf, lisans MIT, lokal, pa rezo): WAV -> fòm bouch A..H + X ak lè yo.
  Mòd «phonetic» la pa depann de lang lan (fr, ht, en, es, pt). Chemen: varyab KADANS_RHUBARB oswa `rhubarb`
  nan PATH. Rezilta a nan kach bò kote WAV la (<vwa>.mouth.json), menm jan ak .words.json.
- Rhubarb pa la (oswa aperçu san vwa): fòm yo estime ak lèt mo yo (vwayèl / konsòn) sou lè mo yo.
- Nan paj la: yon eleman `data-mouth` ak pitit `data-shape="A"` ... `data-shape="X"` (youn parèt alafwa);
  yon eleman `data-eyes` ak pitit `data-eye="open|half|closed"` (bat je detèminis, menm rann chak fwa).

Fòm yo (Preston Blair): A fèmen (M B P) · B ti louvri, dan sere (S T K I) · C louvri (È É) · D louvri nèt (A)
E won (O) · F won pouse (OU W) · G dan sou lèv (F V) · H lang leve (L) · X repo.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import unicodedata
from pathlib import Path

SHAPES = ("A", "B", "C", "D", "E", "F", "G", "H", "X")
FALLBACK = {"G": "B", "H": "C", "X": "A"}          # yon pèsonaj ki pa gen fòm sa a desine: sa a ranplase l
_NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def find_rhubarb() -> str | None:
    p = os.environ.get("KADANS_RHUBARB")
    if p and Path(p).is_file():
        return p
    return shutil.which("rhubarb")


def rhubarb_cues(wav: Path, timeout: float = 180) -> list[list] | None:
    """[[start, end, shape], ...] (segonn, relatif a WAV la). Kach: <wav>.mouth.json. None = Rhubarb pa la / echwe."""
    wav = Path(wav)
    side = wav.with_suffix(".mouth.json")
    try:
        if side.is_file() and side.stat().st_mtime >= wav.stat().st_mtime:
            return json.loads(side.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    exe = find_rhubarb()
    if not exe or not wav.is_file():
        return None
    tmp = wav.with_suffix(".mouth.part.json")
    try:
        r = subprocess.run([exe, "-q", "-r", "phonetic", "-f", "json", "--extendedShapes", "GHX",
                            "-o", str(tmp), str(wav)], capture_output=True, text=True, timeout=timeout,
                           creationflags=_NOWIN)
        if r.returncode != 0 or not tmp.is_file():
            return None
        data = json.loads(tmp.read_text(encoding="utf-8"))
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    finally:
        tmp.unlink(missing_ok=True)
    cues = [[round(float(c["start"]), 3), round(float(c["end"]), 3), str(c["value"])]
            for c in data.get("mouthCues") or [] if str(c.get("value")) in SHAPES]
    try:
        side.write_text(json.dumps(cues), encoding="utf-8")
    except OSError:
        pass
    return cues


def voice_cues(spec: dict, vmap: dict) -> dict:
    """{scene id: cues relatif a vwa a} pou sèn ki gen `lipsync` ak yon vwa. Sèn Rhubarb pa ka fè yo: absan
    (timeline() estime yo ak mo yo)."""
    out = {}
    for sc in spec["scenes"]:
        wav = vmap.get(sc["id"])
        if sc.get("lipsync") and wav:
            c = rhubarb_cues(Path(wav))
            if c:
                out[sc["id"]] = c
    return out


def _plain(w: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", w.lower()) if unicodedata.category(ch) != "Mn")


_DIGRAPHS = (("ou", "F"), ("au", "E"), ("eau", "E"), ("oi", "F"), ("an", "D"), ("on", "E"), ("en", "C"),
             ("in", "C"), ("ch", "B"), ("ph", "G"))
_LETTER = {c: s for letters, s in (("a", "D"), ("e", "C"), ("iy", "B"), ("o", "E"), ("uw", "F"), ("mbp", "A"),
                                    ("fv", "G"), ("l", "H"), ("stkdgnrzcjqx", "B")) for c in letters}


def word_shapes(word: str) -> list[str]:
    """Fòm bouch yon mo, estime ak lèt li (sèvi lè Rhubarb pa la): «papa» -> A D A D."""
    w, i, out = _plain(word), 0, []
    w = "".join(ch for ch in w if ch.isalpha())
    while i < len(w):
        for dg, s in sorted(_DIGRAPHS, key=lambda d: -len(d[0])):
            if w.startswith(dg, i):
                out.append(s)
                i += len(dg)
                break
        else:
            s = _LETTER.get(w[i])
            if s:
                out.append(s)
            i += 1
    shapes = [s for k, s in enumerate(out) if k == 0 or s != out[k - 1]]
    return shapes or ["C"]


def from_words(words: list[dict]) -> list[list]:
    """Cues estime sou lè mo yo [{w, s, e}] (lè absoli): chak mo separe an fòm li yo, silans = X."""
    cues, last = [], None
    for wd in words:
        s, e = float(wd["s"]), float(wd["e"])
        if last is not None and s - last > 0.12:
            cues.append([round(last, 3), round(s, 3), "X"])
        sh = word_shapes(wd["w"])
        step = max(0.04, (e - s) / len(sh))
        for k, x in enumerate(sh):
            a = s + k * step
            if a >= e:
                break
            cues.append([round(a, 3), round(min(e, a + step), 3), x])
        last = e
    if cues:
        cues.append([cues[-1][1], round(cues[-1][1] + 0.3, 3), "X"])
    return cues
