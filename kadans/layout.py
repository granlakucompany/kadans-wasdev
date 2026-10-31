"""Project layout — the SAME folder tree for every Kadans project (WASDEV and the open-source repo).

    <projects>/<Real-Project-Name>/
        spec.json, composition.html, <name>.kadans   the edit (Kadans timeline) — engine + editor read them here
        01-senaryo/        script, characters, synopsis (.docx / .fountain / .md)
        02-storyboard/     shot-by-shot frames (images + PDF)
        medya/
            vwa/           voices (TTS, voice-over, dubbing)
            mizik/         music
            sfx/           sound effects
            imaj/          images (AI or imported)
            videyo/        video clips
        Exported Videos/   final MP4 renders: <name>_v1.mp4, <name>_v2.mp4 …

Rules (also in AGENTS.md): a project gets a REAL descriptive name (never an id like «gslmmfs5sjm» or «project1»),
every media an AI makes or uses goes into medya/<kind>/ with a name that says what it is, renders go to
Exported Videos/ inside that project folder.
Old projects keep working: legacy folders (rann/, voices/, media/, root MP4s) are still read, never moved by force."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

SCRIPT, BOARD, MEDIA, RENDERS = "01-senaryo", "02-storyboard", "medya", "Exported Videos"
LEGACY_RENDERS = "rann"                     # old render folder: still listed + numbered, never moved
KINDS = ("vwa", "mizik", "sfx", "imaj", "videyo")
LEGACY_MEDIA = "media"                      # old flat upload folder of the timeline editor
LEGACY_VOICES = "voices"

IMG = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif"}
VID = {".mp4", ".webm", ".mov", ".m4v", ".mkv", ".avi"}
AUD = {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac"}

_README = """# {name}

Kadans project — same layout for every project:

- `spec.json` / `composition.html` — the edit (open it in Kadans Timeline)
- `01-senaryo/` — script, characters, synopsis
- `02-storyboard/` — shot by shot
- `medya/vwa` · `medya/mizik` · `medya/sfx` · `medya/imaj` · `medya/videyo` — every media of the project
- `Exported Videos/` — final MP4 renders (`{name}_v1.mp4`, `_v2`…)
"""


def ensure(work, name: str | None = None) -> Path:
    """Create the full tree (idempotent, never deletes). Returns the project folder."""
    w = Path(work)
    for d in (SCRIPT, BOARD, RENDERS, *(f"{MEDIA}/{k}" for k in KINDS)):
        (w / d).mkdir(parents=True, exist_ok=True)
    rd = w / "README.md"
    if not rd.exists():
        try:
            rd.write_text(_README.format(name=name or w.name), encoding="utf-8")
        except OSError:
            pass
    return w


def media_dir(work, kind: str) -> Path:
    d = Path(work) / MEDIA / (kind if kind in KINDS else kind_of_name(kind))
    d.mkdir(parents=True, exist_ok=True)
    return d


def kind_of(path, hint: str = "") -> str:
    """vwa | mizik | sfx | imaj | videyo. `hint` = the spec key / track kind the file came from."""
    s = Path(str(path)).suffix.lower()
    h = (hint or "").lower()
    if s in IMG:
        return "imaj"
    if s in VID and "audio" not in h:
        return "videyo"
    if "sfx" in h or "fx" == h:
        return "sfx"
    if "music" in h or "mizik" in h:
        return "mizik"
    if s in AUD or s in VID:
        return "vwa" if any(x in h for x in ("voice", "vwa", "sample", "narr")) else "mizik"
    return "imaj"


def kind_of_name(k: str) -> str:
    k = (k or "").lower()
    return {"voice": "vwa", "audio": "vwa", "music": "mizik", "image": "imaj", "video": "videyo",
            "images": "imaj", "videos": "videyo"}.get(k, k if k in KINDS else "imaj")


def voices_dir(work) -> Path:
    """Generated voices: medya/vwa (legacy voices/ kept for projects that already have it — no new TTS cost)."""
    w = Path(work)
    old = w / LEGACY_VOICES
    if old.is_dir() and any(old.iterdir()):
        return old
    return media_dir(w, "vwa")


def music_dir(work) -> Path:
    return media_dir(work, "mizik")


def renders_dir(work) -> Path:
    d = Path(work) / RENDERS
    d.mkdir(parents=True, exist_ok=True)
    return d


def render_dirs(work) -> list[Path]:
    """Every folder that holds final renders: Exported Videos/ first, then the legacy rann/ (if it exists)."""
    w = Path(work)
    return [d for d in (w / RENDERS, w / LEGACY_RENDERS) if d.is_dir()]


def next_render(work, name: str | None = None) -> Path:
    """Exported Videos/<name>_v<N>.mp4 — the next free version number (never overwrites an earlier render).
    The numbering continues after the versions already in the legacy rann/ folder."""
    w = Path(work)
    n = name or w.name
    d = renders_dir(w)
    nums = [int(m.group(1)) for rd in render_dirs(w) for f in rd.glob(f"{n}_v*.mp4")
            if (m := re.fullmatch(re.escape(n) + r"_v(\d+)", f.stem))]
    return d / f"{n}_v{max(nums, default=0) + 1}.mp4"


def list_media(work) -> list[dict]:
    """Every media of the project: medya/<kind>/** first (newest first per kind), then legacy media/."""
    w = Path(work)
    out = []
    exts = IMG | VID | AUD
    for k in KINDS:
        d = w / MEDIA / k
        if d.is_dir():
            files = [f for f in d.rglob("*") if f.is_file() and f.suffix.lower() in exts and ".part." not in f.name]
            for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
                out.append({"rel": f.relative_to(w).as_posix(), "name": f.name, "kind": k})
    old = w / LEGACY_MEDIA
    if old.is_dir():
        for f in sorted([x for x in old.iterdir() if x.is_file() and x.suffix.lower() in exts],
                        key=lambda x: x.stat().st_mtime, reverse=True):
            out.append({"rel": f.relative_to(w).as_posix(), "name": f.name, "kind": kind_of(f)})
    return out


# ------------------------------------------------------------------------------------------- names
_GENERIC = {"video", "videyo", "videos", "project", "projet", "pwoje", "pwojè", "proyecto", "projeto", "untitled",
            "sans-titre", "san-tit", "new", "nouvo", "nouveau", "test", "tes", "demo", "output", "out", "final",
            "temp", "tmp", "draft", "film", "movie", "clip", "pub", "ad", "short", "reel", "my-video", "default"}


def _looks_random(tok: str) -> bool:
    t = tok.lower()
    if len(t) >= 6 and re.search(r"\d", t) and re.search(r"[a-z]", t):
        return True                                       # gslmmfs5sjm, dQw4w9WgXcQ, a1b2c3d4
    if re.fullmatch(r"[0-9a-f]{8,}", t):
        return True                                       # hashes
    if len(t) >= 6 and re.search(r"[bcdfghjklmnpqrstvwxz]{5,}", t):
        return True                                       # no vowels: «gslmmfs»
    return False


def check_name(name: str) -> str:
    """'' if the project name is a real descriptive name, else the reason (to tell the AI / the user)."""
    n = (name or "").strip()
    toks = [t for t in re.split(r"[\s_\-.]+", n) if t]
    if not toks:
        return "empty name"
    base = re.sub(r"[\s_\-.]*\d+$", "", n).strip().lower()
    if base in _GENERIC or n.lower() in _GENERIC:
        return f"'{n}' is a generic name"
    if any(_looks_random(t) for t in toks):
        return f"'{n}' looks like an id / random letters"
    if not any(len(t) >= 3 and re.search(r"[aeiouyàâéèêëîïôöûüœ]", t.lower()) for t in toks):
        return f"'{n}' has no real word"
    return ""


def clean_filename(text: str, ext: str = "", limit: int = 60) -> str:
    """«Bonjou tout moun!» → «bonjou-tout-moun» (+ext). Accents kept out for portable file names."""
    import unicodedata
    s = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()[:limit].strip("-") or "medya"
    return s + (ext if not ext or ext.startswith(".") else "." + ext)


def unique(d: Path, fname: str) -> Path:
    p = Path(d) / fname
    k = 2
    while p.exists():
        p = Path(d) / f"{Path(fname).stem}-{k}{Path(fname).suffix}"
        k += 1
    return p


def collect(work, src: Path, kind: str = "", name: str = "") -> Path:
    """Copy an outside media into medya/<kind>/ with a clear name (no-op if it is already inside the project)."""
    w, s = Path(work).resolve(), Path(src).resolve()
    try:
        s.relative_to(w)
        return s
    except ValueError:
        pass
    k = kind if kind in KINDS else kind_of(s, kind)
    d = media_dir(w, k)
    fname = clean_filename(name or s.stem, s.suffix.lower())
    same = d / fname
    if same.is_file() and same.stat().st_size == s.stat().st_size:
        return same                                        # already collected
    dst = unique(d, fname)
    shutil.copy2(s, dst)
    return dst


__all__ = ["SCRIPT", "BOARD", "MEDIA", "RENDERS", "LEGACY_RENDERS", "KINDS", "ensure", "media_dir", "kind_of",
           "voices_dir", "music_dir", "renders_dir", "render_dirs", "next_render", "list_media", "check_name", "clean_filename", "collect"]
