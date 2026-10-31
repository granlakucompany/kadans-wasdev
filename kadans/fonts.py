"""Kadans WASDEV — every font installed on the machine, found automatically (standard library only).

Scans the system and per-user font folders (Windows, macOS, Linux) plus any extra folders (a project's fonts/),
reads each TTF / OTF / TTC name table (family, style, weight) and keeps the list in a small cache that refreshes
itself when a folder changes. A spec can then use any of them (brand.font, brand.font_title, brand.font_code):
the composition embeds the chosen files with @font-face, so the render never falls back to another font.
"""
from __future__ import annotations

import json
import os
import struct
import sys
from pathlib import Path

FONT_EXT = (".ttf", ".otf", ".ttc", ".otc")
_CACHE: dict = {}


def font_dirs(extra=()) -> list[Path]:
    dirs = []
    if os.name == "nt":
        dirs.append(Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts")
        if os.environ.get("LOCALAPPDATA"):
            dirs.append(Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts")
    elif sys.platform == "darwin":
        dirs += [Path("/System/Library/Fonts"), Path("/Library/Fonts"), Path.home() / "Library" / "Fonts"]
    else:
        dirs += [Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".local/share/fonts",
                 Path.home() / ".fonts"]
    dirs += [Path(d) for d in extra if d]
    return [d for d in dirs if d.is_dir()]


def _names(data: bytes, off: int) -> dict:
    """name table of one font face at offset `off` → {family, style, full, weight}."""
    num = struct.unpack(">H", data[off + 4:off + 6])[0]
    tables = {}
    for i in range(num):
        tag, _cs, toff, tlen = struct.unpack(">4sIII", data[off + 12 + 16 * i:off + 28 + 16 * i])
        tables[tag] = (toff, tlen)
    out = {}
    if b"name" in tables:
        toff, _ = tables[b"name"]
        _fmt, count, soff = struct.unpack(">HHH", data[toff:toff + 6])
        best: dict = {}
        for i in range(count):
            pid, eid, lid, nid, ln, no = struct.unpack(">HHHHHH", data[toff + 6 + 12 * i:toff + 18 + 12 * i])
            if nid not in (1, 2, 4, 16, 17):
                continue
            raw = data[toff + soff + no:toff + soff + no + ln]
            if pid == 3 or pid == 0:
                txt = raw.decode("utf-16-be", "ignore")
                rank = 0 if (pid == 3 and lid == 0x409) else 1
            elif pid == 1:
                txt = raw.decode("mac_roman", "ignore")
                rank = 2
            else:
                continue
            if txt and (nid not in best or rank < best[nid][0]):
                best[nid] = (rank, txt.strip())
        g = {k: v[1] for k, v in best.items()}
        out = {"family": g.get(16) or g.get(1, ""), "style": g.get(17) or g.get(2, "Regular"), "full": g.get(4, "")}
    if b"OS/2" in tables:
        toff, _ = tables[b"OS/2"]
        out["weight"] = struct.unpack(">H", data[toff + 4:toff + 6])[0]
    return out


def read_font(path: Path) -> list[dict]:
    """Faces in one font file: [{family, style, full, weight, path, index}]."""
    try:
        data = path.read_bytes()
    except OSError:
        return []
    faces = []
    try:
        if data[:4] in (b"ttcf",):
            n = struct.unpack(">I", data[8:12])[0]
            offs = struct.unpack(">%dI" % n, data[12:12 + 4 * n])
        else:
            offs = (0,)
        for k, o in enumerate(offs):
            info = _names(data, o)
            if info.get("family"):
                faces.append({**info, "path": str(path), "index": k})
    except (struct.error, IndexError):
        return []
    return faces


def _cache_file() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".cache") / "kadans"
    base.mkdir(parents=True, exist_ok=True)
    return base / "fonts.json"


def scan(extra=(), refresh: bool = False) -> list[dict]:
    """All font faces of the machine (+ extra folders). Cached; rescanned when a folder's content changes."""
    dirs = font_dirs(extra)
    stamp = []
    for d in dirs:
        try:
            stamp.append([str(d), int(d.stat().st_mtime), sum(1 for _ in os.scandir(d))])
        except OSError:
            pass
    key = json.dumps(stamp)
    if not refresh and _CACHE.get("key") == key:
        return _CACHE["faces"]
    cf = _cache_file()
    if not refresh:
        try:
            js = json.loads(cf.read_text(encoding="utf-8"))
            if js.get("key") == key:
                _CACHE.update(js)
                return js["faces"]
        except (OSError, ValueError):
            pass
    faces = []
    for d in dirs:
        for root, _sub, files in os.walk(d):
            for f in files:
                if f.lower().endswith(FONT_EXT):
                    faces += read_font(Path(root) / f)
    faces.sort(key=lambda x: (x["family"].lower(), x.get("weight", 400), x["style"].lower()))
    _CACHE.update(key=key, faces=faces)
    try:
        cf.write_text(json.dumps({"key": key, "faces": faces}, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return faces


def families(extra=(), query: str = "") -> list[dict]:
    """[{family, styles: [..], files: n}] sorted by name, optionally filtered by a search word."""
    fams: dict = {}
    for f in scan(extra):
        e = fams.setdefault(f["family"], {"family": f["family"], "styles": [], "files": 0})
        if f["style"] not in e["styles"]:
            e["styles"].append(f["style"])
        e["files"] += 1
    q = query.lower().strip()
    return [v for k, v in sorted(fams.items(), key=lambda kv: kv[0].lower()) if not q or q in k.lower()]


def find(name: str, extra=()) -> list[dict]:
    """Faces of one family (case-insensitive exact name, else the first family that starts with it)."""
    n = (name or "").strip().lower()
    if not n:
        return []
    faces = scan(extra)
    exact = [f for f in faces if f["family"].lower() == n]
    if exact:
        return exact
    starts = sorted({f["family"] for f in faces if f["family"].lower().startswith(n)}, key=len)
    return [f for f in faces if starts and f["family"] == starts[0]]


def face_css(family: str, faces: list[dict], url_fn) -> str:
    """@font-face rules for a family's files (weight / italic from the face): the page never needs the font to be
    installed in the browser profile, and the render is identical on any machine that has the files."""
    out = []
    for f in faces:
        if f.get("index", 0) or f["path"].lower().endswith((".ttc", ".otc")):
            continue                                   # collections: the installed font is used by name
        style = "italic" if "italic" in f["style"].lower() or "oblique" in f["style"].lower() else "normal"
        fmt = "opentype" if f["path"].lower().endswith(".otf") else "truetype"
        out.append(f'@font-face{{font-family:"{family}";src:url("{url_fn(Path(f["path"]))}") format("{fmt}");'
                   f'font-weight:{int(f.get("weight") or 400)};font-style:{style};font-display:block}}')
    return "\n".join(out)
