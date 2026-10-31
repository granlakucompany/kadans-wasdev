"""Kadans Timeline media panel helpers: where an imported file goes, a cheap thumbnail, its length + a tiny waveform.

- import_kind(path)          -> vwa | mizik | sfx | imaj | videyo  (by extension + name/folder hints)
- import_file(work, src)     -> COPY (never move, never trim) an outside file into <work>/medya/<kind>/
- thumb(src, cache)          -> first-frame JPEG of a video (cached by path + size + mtime), or None
- info(src, cache)           -> {"dur": seconds, "wave": [0..1] * 48} (cached the same way)

Everything here runs in the server's request threads (ThreadingHTTPServer): the editor never waits on it.
"""
from __future__ import annotations

import array
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from . import layout

_NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
VOICE_HINTS = ("vwa", "voice", "voix", "voz", "narr", "voiceover", "voice-over", "vo_", "dialog", "dub")
SFX_HINTS = ("sfx", "fx_", "fx-", "whoosh", "swoosh", "click", "clic", "hit", "boom", "impact", "pop", "ding",
             "beep", "riser", "transition", "notif", "swipe", "glitch", "door", "pot", "step")
MAX_SFX_SECONDS = 4.0


def _tokens(path: Path) -> str:
    """Lower-cased file name + its two parent folders (where the developer keeps it says a lot)."""
    parts = [path.stem] + [p.name for p in list(path.parents)[:2]]
    return " ".join(parts).lower()


def import_kind(path, dur: float | None = None) -> str:
    """Media kind for an imported file. Audio: voice-like names -> vwa, sfx-like names (or very short) -> sfx,
    anything else -> mizik."""
    p = Path(str(path))
    s = p.suffix.lower()
    if s in layout.IMG:
        return "imaj"
    if s in layout.VID:
        return "videyo"
    if s not in layout.AUD:
        return layout.kind_of(p)
    t = _tokens(p)
    words = set(re.split(r"[^a-z0-9]+", t))
    if any(h in t for h in VOICE_HINTS if len(h) > 3) or words & {"vo", "vwa", "voice", "voix", "narr"}:
        return "vwa"
    if any(h in t for h in SFX_HINTS if len(h) > 3) or words & {"sfx", "fx", "hit", "pop", "pot"}:
        return "sfx"
    if dur is not None and 0 < dur <= MAX_SFX_SECONDS:
        return "sfx"
    return "mizik"


def import_file(work, src, kind: str = "") -> tuple[Path, str]:
    """Copy src into <work>/medya/<kind>/ (unique, clean name). Returns (dest, kind). The source is never touched.
    A file already inside the project is returned as is."""
    w, s = Path(work).resolve(), Path(src).resolve()
    if not s.is_file():
        raise FileNotFoundError(str(src))
    if s.suffix.lower() not in (layout.IMG | layout.VID | layout.AUD):
        raise ValueError(f"not a media file: {s.name}")
    k = kind if kind in layout.KINDS else import_kind(s)
    try:
        s.relative_to(w / layout.MEDIA)
        return s, k                                          # already in this project's media
    except ValueError:
        pass
    d = layout.media_dir(w, k)
    fname = layout.clean_filename(s.stem, s.suffix.lower())
    same = d / fname
    if same.is_file() and same.stat().st_size == s.stat().st_size:
        return same, k                                       # same file dropped twice: no second copy
    dst = layout.unique(d, fname)
    tmp = dst.with_name(dst.stem + ".part" + dst.suffix)     # list_media skips ".part." while copying
    shutil.copy2(s, tmp)
    tmp.replace(dst)
    return dst, k


def _key(src: Path, tag: str) -> str:
    st = src.stat()
    return hashlib.sha1(json.dumps([str(src.resolve()), st.st_size, int(st.st_mtime), tag]).encode()).hexdigest()[:20]


def _ffmpeg() -> str:
    from .media import find_tool
    return find_tool("ffmpeg")


def thumb(src, cache) -> Path | None:
    """First frame (at 0.5 s, or 0 for very short clips) of a video as a 320 px JPEG, cached."""
    s = Path(src)
    if not s.is_file() or s.suffix.lower() not in layout.VID:
        return None
    d = Path(cache)
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"thumb-{_key(s, 'v1')}.jpg"
    if out.is_file() and out.stat().st_size > 200:
        return out
    tmp = out.with_suffix(".part.jpg")
    for ss in ("0.5", "0"):
        try:
            subprocess.run([_ffmpeg(), "-v", "error", "-y", "-ss", ss, "-i", str(s), "-frames:v", "1",
                            "-vf", "scale=320:-2", "-q:v", "5", str(tmp)],
                           capture_output=True, timeout=30, creationflags=_NOWIN)
        except Exception:                                    # noqa: BLE001 - no ffmpeg / broken file: no thumb
            return None
        if tmp.is_file() and tmp.stat().st_size > 200:
            tmp.replace(out)
            return out
    tmp.unlink(missing_ok=True)
    return None


def preview_wav(src, cache) -> Path | None:
    """Browsers without an MP3 / AAC decoder (e.g. a Chromium built without proprietary codecs): the media panel
    falls back to this small mono 22 kHz WAV of the file, made once and cached."""
    s = Path(src)
    if not s.is_file():
        return None
    d = Path(cache)
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"prev-{_key(s, 'w1')}.wav"
    if out.is_file() and out.stat().st_size > 100:
        return out
    tmp = out.with_suffix(".part.wav")
    try:
        subprocess.run([_ffmpeg(), "-v", "error", "-y", "-i", str(s), "-vn", "-ac", "1", "-ar", "22050",
                        "-c:a", "pcm_s16le", str(tmp)], capture_output=True, timeout=180, creationflags=_NOWIN)
    except Exception:                                        # noqa: BLE001
        return None
    if tmp.is_file() and tmp.stat().st_size > 100:
        tmp.replace(out)
        return out
    tmp.unlink(missing_ok=True)
    return None


def info(src, cache, bars: int = 48) -> dict:
    """{"dur": seconds, "wave": bars peak values 0..1} of an audio / video file, cached as JSON."""
    s = Path(src)
    if not s.is_file():
        return {"dur": 0, "wave": []}
    d = Path(cache)
    d.mkdir(parents=True, exist_ok=True)
    js = d / f"info-{_key(s, 'v1-%d' % bars)}.json"
    if js.is_file():
        try:
            return json.loads(js.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    sr = 1000                                                # 1 kHz mono is plenty for a 48-bar sketch
    try:
        r = subprocess.run([_ffmpeg(), "-v", "error", "-i", str(s), "-vn", "-ac", "1", "-ar", str(sr),
                            "-f", "s16le", "-"], capture_output=True, timeout=60, creationflags=_NOWIN)
        data = array.array("h")
        data.frombytes(r.stdout[: len(r.stdout) // 2 * 2])
    except Exception:                                        # noqa: BLE001
        data = array.array("h")
    dur = round(len(data) / sr, 2)
    if dur <= 0 and s.suffix.lower() in layout.VID:          # silent video: length from ffprobe
        try:
            from .media import probe_audio
            dur = round(probe_audio(s), 2)
        except Exception:                                    # noqa: BLE001
            dur = 0
    wave = []
    if len(data):
        win = max(1, len(data) // bars)
        for i in range(0, win * bars, win):
            chunk = data[i:i + win]
            wave.append(round(max((abs(x) for x in chunk), default=0) / 32768, 3))
        top = max(wave) or 1
        wave = [round(v / top, 3) for v in wave]
    res = {"dur": dur, "wave": wave}
    try:
        js.write_text(json.dumps(res), encoding="utf-8")
    except OSError:
        pass
    return res


__all__ = ["import_kind", "import_file", "thumb", "info", "preview_wav"]
