"""Kadans WASDEV — your own videos and photos: probe, trim, and prepare them for the HTML composition.

Every video scene's clip is extracted ONCE into a JPEG sequence trimmed to [in, out], scaled to the video frame, at
the video fps: __seek(t) then shows exactly frame round(t * fps) (a <video> element cannot be seeked frame-exactly,
and some embedded Chromiums have no H.264 decoder). Sound never goes through the browser: FFmpeg mixes the clip's
own audio later. Results are cached by (file, size, mtime, trim, frame size): editing one scene never re-extracts
the others.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

_NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
_TOOLS: dict[str, str] = {}


class MediaError(RuntimeError):
    pass


def find_tool(name: str = "ffmpeg") -> str:
    """ffmpeg / ffprobe: $KADANS_FFMPEG (a folder or the ffmpeg exe), then `kadans setup`'s, then PATH."""
    if name in _TOOLS:
        return _TOOLS[name]
    exe = name + (".exe" if os.name == "nt" else "")
    env = os.environ.get("KADANS_FFMPEG", "")
    cands = []
    if env:
        e = Path(env)
        cands += [e / exe, e / "bin" / exe] if e.is_dir() else [e.with_name(exe)]
    from .deps import auto_setup, ffmpeg_dir        # `kadans setup`
    cands.append(ffmpeg_dir() / exe)
    w = shutil.which(name)
    if w:
        cands.append(Path(w))
    for c in cands:
        if c.is_file():
            _TOOLS[name] = str(c)
            return _TOOLS[name]
    c = ffmpeg_dir() / exe                              # nothing anywhere: get it once, by itself
    if auto_setup("ffmpeg") and c.is_file():
        _TOOLS[name] = str(c)
        return _TOOLS[name]
    raise MediaError(f"{name} not found: run `kadans setup` (or install FFmpeg / set KADANS_FFMPEG)")


def set_ffmpeg(path: str) -> None:
    """Host apps (e.g. WASDEV) point Kadans at their own FFmpeg."""
    p = Path(path)
    _TOOLS["ffmpeg"] = str(p)
    probe = p.with_name("ffprobe" + p.suffix)
    if probe.is_file():
        _TOOLS["ffprobe"] = str(probe)


ROOTS: dict[str, Path] = {}                 # «lib:SMOKE/…» → host app folders (WASDEV: design library, lights…)


def set_root(tag: str, folder) -> None:
    """Let a spec point into a host app's asset library: set_root("lib", "/…/DESIGN") → "lib:SMOKE/a.svg"."""
    if folder:
        ROOTS[tag] = Path(folder)


def resolve(src: str, base: Path | None) -> Path:
    tag, sep, rest = str(src).partition(":")
    if sep and len(tag) > 1 and tag in ROOTS:            # (a one-letter tag is a Windows drive: C:\…)
        return ROOTS[tag] / rest
    p = Path(src)
    if not p.is_absolute() and base is not None:
        p = base / p
    return p


def probe(path: Path) -> dict:
    """{duration, w, h, fps, audio} of a video file."""
    try:
        r = subprocess.run([find_tool("ffprobe"), "-v", "error", "-print_format", "json", "-show_format",
                            "-show_streams", str(path)], capture_output=True, text=True, timeout=30,
                           creationflags=_NOWIN)
    except (OSError, subprocess.SubprocessError) as e:
        raise MediaError(f"ffprobe {path.name}: {e}") from e
    if r.returncode != 0:
        raise MediaError(f"cannot read {path.name}: {r.stderr.strip()[:200]}")
    js = json.loads(r.stdout or "{}")
    v = next((s for s in js.get("streams", []) if s.get("codec_type") == "video"), None)
    if v is None:
        raise MediaError(f"{path.name}: no video stream")
    num, _, den = (v.get("avg_frame_rate") or "30/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 30.0
    dur = float(js.get("format", {}).get("duration") or v.get("duration") or 0)
    return {"duration": round(dur, 3), "w": int(v.get("width") or 0), "h": int(v.get("height") or 0),
            "fps": round(fps, 3), "audio": any(s.get("codec_type") == "audio" for s in js.get("streams", []))}


def probe_audio(path: Path) -> float:
    """Length in seconds of any audio / video file."""
    r = subprocess.run([find_tool("ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                        str(path)], capture_output=True, text=True, timeout=30, creationflags=_NOWIN)
    try:
        return float(r.stdout.strip())
    except ValueError as e:
        raise MediaError(f"cannot read {path.name}") from e


def _key(path: Path, *parts) -> str:
    st = path.stat()
    raw = json.dumps([str(path.resolve()), st.st_size, int(st.st_mtime), *parts])
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def frames(path: Path, cache: Path, w: int, h: int, fps: int, t_in: float = 0.0, t_out: float | None = None,
           progress=None, fit: str = "cover") -> dict:
    """Extract a clip's frames (JPEG, at the video fps; cover = scaled + center-cropped to the frame, contain = fitted inside it) into a cached folder.
    A <video> element cannot be seeked frame-exactly; an image sequence can: __seek(t) shows frame round(t*fps).
    Returns {dir, count, fps}."""
    d = cache / f"{re.sub(r'[^A-Za-z0-9_-]+', '_', path.stem)[:40]}-{_key(path, w, h, fps, t_in, t_out, fit)}"
    done = d / "frames.json"
    if done.is_file():
        try:
            return json.loads(done.read_text(encoding="utf-8")) | {"dir": str(d)}
        except (OSError, ValueError):
            pass
    tmp = d.with_name(d.name + ".part")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    cmd = [find_tool("ffmpeg"), "-y", "-v", "error", "-ss", f"{t_in:.3f}"]
    if t_out is not None:
        cmd += ["-to", f"{t_out:.3f}"]
    cmd += ["-i", str(path), "-an", "-vf",
            (f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps}" if fit == "cover" else
             f"scale={w}:{h}:force_original_aspect_ratio=decrease:force_divisible_by=2,fps={fps}"),
            "-q:v", "3", str(tmp / "%05d.jpg")]
    if progress:
        progress(f"preparing {path.name}")
    r = subprocess.run(cmd, capture_output=True, text=True, creationflags=_NOWIN)
    n = len(list(tmp.glob("*.jpg")))
    if r.returncode != 0 or n == 0:
        shutil.rmtree(tmp, ignore_errors=True)
        raise MediaError(f"cannot read frames of {path.name}: {r.stderr.strip()[-300:]}")
    info = {"count": n, "fps": fps}
    (tmp / "frames.json").write_text(json.dumps(info), encoding="utf-8")
    shutil.rmtree(d, ignore_errors=True)
    tmp.replace(d)
    return info | {"dir": str(d)}


def prepare(spec: dict, base: Path | None, cache: Path, progress=None) -> tuple[dict, dict]:
    """For every video scene: probe + frame extraction. Returns (media_s {scene id: full clip seconds},
    clips {scene id: {dir, count, fps}}). Missing files raise MediaError naming the scene."""
    media_s, clips = {}, {}
    for sc in spec["scenes"]:
        if sc["type"] != "video":
            continue
        p = resolve(sc["src"], base)
        if not p.is_file():
            raise MediaError(f"scene {sc['id']}: file not found: {p}")
        info = probe(p)
        media_s[sc["id"]] = info["duration"]
        out = sc.get("out")
        if out is not None:
            out = min(out, info["duration"])
        clips[sc["id"]] = frames(p, cache, spec["w"], spec["h"], spec["fps"], sc.get("in", 0.0), out, progress,
                                 sc.get("fit", "cover"))
    # videos used as backgrounds / overlays: frames too (they loop; their length never drives the timeline)
    layers = [("stage", spec.get("background"), spec.get("overlays") or [])] + \
             [(sc["id"], sc.get("background"), sc.get("overlays") or []) for sc in spec["scenes"]]
    for owner, bg, ovs in layers:
        items = ([("bg", bg)] if bg else []) + [(f"ov{j}", o) for j, o in enumerate(ovs)]
        for tag, it in items:
            if it.get("kind") != "video":
                continue
            p = resolve(it["src"], base)
            if not p.is_file():
                raise MediaError(f"{owner} {tag}: file not found: {p}")
            w = spec["w"] if tag == "bg" else max(64, int(spec["w"] * min(1.0, it.get("w", 0.6)) // 2 * 2))
            h = spec["h"] if tag == "bg" else max(64, int(w * spec["h"] / spec["w"] // 2 * 2))
            clips[f"{owner}#{tag}"] = frames(p, cache, w, h, spec["fps"], it.get("in", 0.0), it.get("out"), progress,
                                             it.get("fit", "cover") if tag == "bg" else "contain")

    def _check_img(src, who):                        # IMAJ yo tcheke tou (O2): chemen ki manke = erè klè
        if not src or str(src).startswith("find:"):
            return
        q = resolve(src, base)
        if not q.is_file():
            raise MediaError(f"{who}: image not found: {q}")
    for sc in spec["scenes"]:
        if sc["type"] == "image":
            _check_img(sc.get("src"), f"scene {sc['id']}")
    for owner, bg, ovs in layers:
        for tag, it in (([("bg", bg)] if bg else []) + [(f"ov{j}", o) for j, o in enumerate(ovs)]):
            if it.get("kind") == "image":
                _check_img(it.get("src"), f"{owner} {tag}")
    return media_s, clips


def list_media(folder: Path) -> list[dict]:
    """Videos and photos in a folder (for a host app's media picker): [{path, kind, size, duration?, w?, h?}]."""
    from .spec import IMAGE_EXT, VIDEO_EXT
    out = []
    for f in sorted(folder.iterdir()) if folder.is_dir() else []:
        ext = f.suffix.lower()
        if ext in VIDEO_EXT:
            row = {"path": str(f), "kind": "video", "size": f.stat().st_size}
            try:
                row.update(probe(f))
            except MediaError as e:
                row["error"] = str(e)
            out.append(row)
        elif ext in IMAGE_EXT:
            out.append({"path": str(f), "kind": "image", "size": f.stat().st_size})
    return out
