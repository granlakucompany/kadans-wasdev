"""Kadans WASDEV — spec -> MP4.

    voice (cached per line) -> timeline -> composition page -> frames (headless Chromium, DevTools) -> FFmpeg

- One CHUNK per scene, cached by what the scene looks like (its spec, timing, brand, look, engine version): change
  one sentence and only the scenes that really changed are captured again. A render that stops (crash, power cut)
  resumes where it was: finished chunks are kept.
- Several private browsers capture different scenes at the same time (workers).
- Motion blur: k sub-frames per frame, averaged by FFmpeg (tmix).
- Cinematic finish AFTER capture, on real pixels (bloom, film grain, vignette): heavy CSS effects are what makes
  browser rendering slow and unequal between machines.
- Colors tagged BT.709, yuv420p, faststart: plays the same everywhere (phones, social networks, TVs).
"""
from __future__ import annotations

import hashlib
import json
import os
import queue
import shutil
import subprocess
import threading
import time
from pathlib import Path

from . import __version__, audio, media
from .cdp import Browser, CDPError, screenshot
from .compose import build_html
from .spec import EXACT_BLEND, timeline as make_timeline, total as tl_total, validate

_NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
_ENC: dict[str, list[str]] = {}
ENGINE_HASH = hashlib.sha1(b"".join(
    (Path(__file__).with_name(f).read_bytes() for f in ("compose.py", "renderer.py", "lipsync.py", "motion.py", "sounds.py")))).hexdigest()[:10]


class RenderError(RuntimeError):
    pass


_WORKING_ENC: dict[str, tuple[str, list[str]]] = {}
# Kalite JPEG imaj kaptire yo anvan ankodaj (92 → 97: tèks, liy fen ak degrade pa fè «blòk» ankò)
CAPTURE_Q = max(70, min(100, int(os.environ.get("KADANS_CAPTURE_Q", "97") or 97)))


def _test_encoder(ff: str, name: str, opt: list[str]) -> bool:
    """Tcheke si yon ankodè fonksyone vrèman sou machin nan (GPU prezan ak chofè valid)."""
    try:
        r = subprocess.run(
            [ff, "-y", "-v", "error", "-f", "lavfi", "-i", "color=s=320x240:d=0.2", "-c:v", name, *opt, "-f", "null", "-"],
            capture_output=True, text=True, creationflags=_NOWIN, timeout=1.5
        )
        return r.returncode == 0
    except Exception:
        return False


# Politique de licence MIT / LGPL (identique à GLC CONVERTER) : aucun encodeur GPL ne doit être utilisé.
FORBIDDEN_ENCODERS = frozenset({"libx264", "libx265", "libxvid", "libxavs", "libxavs2", "libfdk_aac"})


def encoder(w: int, h: int, fps: int) -> tuple[str, list[str]]:
    """Pi bon ankodè H.264 pou FFmpeg sa a: Priyorite GPU (MediaFoundation sou Windows, NVENC, AMF, QuickSync)
    pou divize tan rann pa 4x a 5x, apre sa libopenh264 (BSD) / mpeg4 (LGPL). Pa janm sèvi ak ankodè GPL."""
    ff = media.find_tool("ffmpeg")
    if ff not in _ENC:
        r = subprocess.run([ff, "-hide_banner", "-encoders"], capture_output=True, text=True, creationflags=_NOWIN)
        _ENC[ff] = [ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith(" V") and len(ln.split()) > 1]
    have = [e for e in _ENC[ff] if e not in FORBIDDEN_ENCODERS]
    # KALITE WO (2026-10-26): 0.26 bit / piksèl / imaj → 1080p30 ≈ 16 Mbit/s, 4K30 ≈ 65 Mbit/s (avan: 0.17 → 10 Mbit/s,
    # h264_mf an pwofil «Baseline» → tèks ak bò yo te flou). Pwofil High (100) sou tout ankodè ki aksepte l.
    rate_n = max(4, int(w * h * fps * 0.26 / 1e6))
    rate, buf = f"{rate_n}M", f"{rate_n * 2}M"
    # Chak ankodè: varyant KALITE WO an premye, apre varyant senp lan (si chofè a refize yon opsyon, tès la
    # pase sou pwochen varyant lan olye l desann sou yon ankodè pi fèb).
    opts = {
        "h264_mf": [["-profile:v", "100", "-b:v", rate, "-maxrate", rate, "-bufsize", buf],   # Windows Media Foundation
                    ["-b:v", rate]],
        "h264_nvenc": [["-preset", "p5", "-tune", "hq", "-rc", "vbr", "-cq", "19", "-b:v", rate, "-maxrate", buf,
                        "-profile:v", "high"],
                       ["-preset", "p4", "-tune", "hq", "-rc", "vbr", "-b:v", rate]],          # NVIDIA GPU
        "h264_amf": [["-quality", "quality", "-rc", "vbr_peak", "-b:v", rate, "-maxrate", buf, "-profile:v", "high"],
                     ["-quality", "balanced", "-rc", "vbr_latency", "-b:v", rate]],             # AMD Radeon GPU
        "h264_qsv": [["-preset", "medium", "-b:v", rate, "-maxrate", buf, "-profile:v", "high"],
                     ["-preset", "veryfast", "-b:v", rate]],                                    # Intel Quick Sync GPU
        "h264_videotoolbox": [["-b:v", rate, "-profile:v", "high"], ["-b:v", rate]],
        "h264_vaapi": [["-b:v", rate], []],
        "libopenh264": [["-b:v", rate]],                                                        # Cisco OpenH264 (BSD-2-Clause)
        "mpeg4": [["-q:v", "2"]]                                                                # FFmpeg native MPEG-4 (LGPL)
    }
    first = lambda n: (opts.get(n) or [[]])[0]
    want = os.environ.get("KADANS_ENCODER")
    if want and want in FORBIDDEN_ENCODERS:
        raise RenderError(f"GPL encoder '{want}' is forbidden by the MIT/LGPL license policy")
    if want and want in have:
        return want, ["-c:v", want, *first(want)]

    if ff in _WORKING_ENC:
        name, args = _WORKING_ENC[ff]
        return name, ["-c:v", name, *args]

    # Lòd priyorite: Sou Windows, h264_mf kouvri tout GPU (AMD, Intel, Nvidia) ak CPU san echèk
    if os.name == "nt":
        candidates = ["h264_mf", "h264_nvenc", "h264_amf", "h264_qsv", "libopenh264", "mpeg4"]
    else:
        candidates = ["h264_videotoolbox", "h264_nvenc", "h264_vaapi", "libopenh264", "mpeg4"]

    for name in candidates:
        if name in have:
            for test_opt in opts.get(name, [[]]):
                if _test_encoder(ff, name, test_opt):
                    _WORKING_ENC[ff] = (name, test_opt)
                    return name, ["-c:v", name, *test_opt]

    # Fallback si okenn tès pa pase: chwazi yon ankodè ki garanti fonksyone san depandans chofè GPU
    safe_order = ["h264_mf", "libopenh264", "mpeg4"] if os.name == "nt" else ["libopenh264", "mpeg4"]
    for name in safe_order:
        if name in have:
            return name, ["-c:v", name, *(opts.get(name) or [[]])[-1]]

    for name in candidates:
        if name in have:
            return name, ["-c:v", name, *(opts.get(name) or [[]])[-1]]

    raise RenderError("this FFmpeg has no H.264 / MPEG-4 encoder")


def _look_filter(look: dict, w: int, h: int, k: int) -> str:
    """Filtergraph applied to the captured frames: motion-blur average, bloom, grain, vignette, BT.709 yuv420p.
    Bloom (screen blend) needs RGB; its blur runs at 1/4 size (a blur has no detail: same glow, 16x fewer pixels).
    Vignette and grain run AFTER the switch to YUV: 3x faster than in RGB (measured), grain on luma = film-like."""
    f = []
    if k > 1:
        f.append(f"tmix=frames={k}:weights='{' '.join(['1'] * k)}',framestep={k}")
    if look.get("bloom", 0) > 0:
        s = max(1.0, min(w, h) / 1080 * 28 / 4)
        f.append(f"format=gbrp,split[a][b];[b]scale={max(2, w // 4)}:{max(2, h // 4)}:flags=area,"
                 f"colorlevels=rimin=0.62:gimin=0.62:bimin=0.62,gblur=sigma={s:.1f},scale={w}:{h}:flags=bilinear[g];"
                 f"[a][g]blend=all_mode=screen:all_opacity={min(0.9, look['bloom'] * 1.4):.2f}")
    f.append("scale=out_color_matrix=bt709:out_range=tv,format=yuv420p")
    if look.get("vignette", 0) > 0:
        f.append(f"vignette=angle={0.25 + 0.5 * look['vignette']:.3f}")
    if look.get("grain", 0) > 0:
        f.append(f"noise=c0s={max(1, int(look['grain'] * 20))}:c0f=t")
    return ",".join(f)


def _scene_key(spec: dict, sc: dict, t: dict, clips: dict, enc: str) -> str:
    glob = {k: spec.get(k) for k in ("w", "h", "fps", "brand", "lang", "credit", "progress_bar", "look", "motion_blur",
                                     "captions", "background", "overlays")}
    raw = json.dumps([__version__, ENGINE_HASH, enc, glob, sc, t, (clips or {}).get(sc["id"]),
                      tl_total([t]) if not spec.get("progress_bar") else spec.get("_total")], sort_keys=True, default=str)
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def _uses_exact_blend(spec: dict, sc: dict) -> bool:
    return any(o.get("blend") in EXACT_BLEND for o in (spec.get("overlays") or []) + (sc.get("overlays") or []))


def _shot_rect(pg, x: int, y: int, w: int, h: int) -> bytes:
    import base64
    return base64.b64decode(pg.call("Page.captureScreenshot", format="png", fromSurface=True,
                                    clip={"x": x, "y": y, "width": w, "height": h, "scale": 1})["data"])


def _layered_frame(pg, w: int, h: int) -> bytes:
    """One frame with exact blend modes: under-layer capture, each exact layer alone (transparent PNG, only its
    rectangle, reused while it does not change) blended with kadans.blend, then what lies above it (skipped when
    nothing is visible there), alpha-over. Raw RGB24 bytes."""
    from . import blend as B
    xb = pg.eval("window.__xb()", wait=False) or []
    if not xb:
        return B.to_bytes(B.decode(screenshot(pg, w, h)))
    xb.sort(key=lambda e: e[0])
    cache = pg.__dict__.setdefault("_layer_cache", {})
    try:
        pg.eval(f"window.__pass(0, {xb[0][0]}, false)", wait=False)
        img = B.decode(screenshot(pg, w, h)).copy()
        for n, (i, mode, (rx, ry, rw, rh), sig) in enumerate(xb):
            hit = cache.get(i)
            if hit is not None and hit[0] == (sig, rx, ry, rw, rh):
                layer = hit[1]
            else:
                pg.eval(f"window.__pass({i}, {i + 1}, true)", wait=False)
                layer = B.decode(_shot_rect(pg, rx, ry, rw, rh), alpha=True)
                cache[i] = ((sig, rx, ry, rw, rh), layer)
            lh, lw = layer.shape[:2]
            reg = img[ry:ry + lh, rx:rx + lw]
            img[ry:ry + lh, rx:rx + lw] = B.composite(reg, layer[:reg.shape[0], :reg.shape[1]], mode, seed=i)
            nxt = xb[n + 1][0] if n + 1 < len(xb) else 10 ** 9
            box = pg.eval(f"window.__any({i + 1}, {nxt})", wait=False) if nxt > i + 1 else None
            if box:                                   # what lies above: only the rectangle it occupies
                bx, by, bw, bh = box
                pg.eval(f"window.__pass({i + 1}, {nxt}, true)", wait=False)
                top = B.decode(_shot_rect(pg, bx, by, bw, bh), alpha=True)
                reg = img[by:by + top.shape[0], bx:bx + top.shape[1]]
                img[by:by + top.shape[0], bx:bx + top.shape[1]] = B.over(reg, top[:reg.shape[0], :reg.shape[1]])
    finally:
        pg.eval("window.__passEnd()", wait=False)
    return B.to_bytes(img)


def _as_wav(p: Path, cache: Path) -> Path:
    """A recording in any format → 48 kHz WAV (cached) for timing and the mix."""
    if p.suffix.lower() == ".wav":
        return p
    cache.mkdir(parents=True, exist_ok=True)
    out = cache / f"vo-{hashlib.sha1((str(p.resolve()) + str(p.stat().st_mtime)).encode()).hexdigest()[:16]}.wav"
    if not out.is_file():
        r = subprocess.run([media.find_tool("ffmpeg"), "-y", "-v", "error", "-i", str(p), "-ac", "1", "-ar", "48000", str(out)],
                           capture_output=True, text=True, creationflags=_NOWIN)
        if r.returncode != 0:
            raise RenderError(f"voice_file {p.name}: {r.stderr.strip()[-200:]}")
    return out

PIECE_S = 2.0          # seconds per captured piece (cache unit)
MAX_WORKERS = 16       # chak navigatè sou yon nwayo CPU; RAM gating anba a pwoteje machin ki pi piti yo


def _free_ram_mb() -> int | None:
    try:
        if os.name == "nt":
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("len", ctypes.c_ulong), ("load", ctypes.c_ulong), ("total", ctypes.c_ulonglong),
                            ("avail", ctypes.c_ulonglong), ("pt", ctypes.c_ulonglong), ("pa", ctypes.c_ulonglong),
                            ("vt", ctypes.c_ulonglong), ("va", ctypes.c_ulonglong), ("ve", ctypes.c_ulonglong)]
            m = MS()
            m.len = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return int(m.avail // 1048576)
        return int(os.sysconf("SC_AVPHYS_PAGES") * os.sysconf("SC_PAGE_SIZE") // 1048576)
    except (OSError, ValueError, AttributeError):
        return None


def default_workers() -> int:
    """Browsers in parallel: multi-workers default (4+ workers). Check KADANS_WORKERS first."""
    env_w = os.environ.get("KADANS_WORKERS")
    if env_w:
        try:
            return max(1, min(MAX_WORKERS, int(env_w)))
        except ValueError:
            pass
    cores = os.cpu_count() or 4
    n = min(MAX_WORKERS, max(4, cores))
    ram = _free_ram_mb()
    if ram and ram > 2000:
        n = max(2, min(n, (ram - 512) // 350))
    elif ram and ram <= 2000:
        n = 2
    return max(2, n)


def render(spec: dict, out: str | Path, base: str | Path | None = None, cache: str | Path | None = None,
           tts=None, tts_fn=None, voices: dict | None = None, workers: int | None = None, progress=None,
           subtitles: bool = True, cancel=None, align=None, verify: bool = False,
           scale: float = 1.0, **kw) -> dict:
    """Render a spec (dict, validated or not) to an MP4. base = folder for relative paths in the spec.
    tts(text, lang, gender, sample, out_wav) makes the voice lines (or voices = {scene id: wav}).
    align(wav, text, lang) -> [[word, start, end], ...] (a speech recognizer, e.g. Whisper): animations, captions
    and sound effects follow the spoken words; without it word times are estimated.
    progress(stage, done, total, info). cancel() -> True stops (finished chunks stay cached).
    Returns {mp4, srt, seconds, frames, reused, captured, fps_capture, timeline}."""
    tts = tts if tts is not None else (tts_fn if tts_fn is not None else kw.get("tts_fn"))
    t_start = time.time()
    out = Path(out).resolve()
    base = Path(base).resolve() if base else out.parent
    cache = Path(cache).resolve() if cache else out.parent / ".kadans-cache"
    say = progress or (lambda *a: None)
    spec = validate(spec) if "w" not in spec else spec
    if 0.1 <= scale < 1.0:                               # bouyon rapid: rezolisyon pi ba (mwens piksèl = pi vit)
        spec = dict(spec)
        spec["w"] = max(16, round(spec["w"] * scale / 2) * 2)
        spec["h"] = max(16, round(spec["h"] * scale / 2) * 2)
    w, h, fps = spec["w"], spec["h"], spec["fps"]
    k = spec.get("motion_blur") or 1

    # 1. sound first: real voice lengths drive the timeline
    vmap = dict(voices or {})
    _t_prep = time.time()
    if tts is not None and spec.get("voice"):
        vmap.update(audio.voices(spec, cache / "voice", tts, progress=say))
    for sc in spec["scenes"]:                        # voice-over: the person's own recordings
        if sc.get("voice_file"):
            p = media.resolve(sc["voice_file"], base)
            if not p.is_file():
                for cr in (out.parent.parent, out.parent):
                    cand = (cr / sc["voice_file"]).resolve()
                    if cand.is_file():
                        p = cand
                        break
            if not p.is_file() and base is not None:
                vf_name = Path(sc["voice_file"]).name
                found = list(Path(base).glob(f"**/{vf_name}"))
                if found and found[0].is_file():
                    p = found[0].resolve()
            if not p.is_file():
                raise RenderError(f"scene {sc['id']}: voice_file not found: {p}")
            vmap[sc["id"]] = _as_wav(p, cache / "voice")
    say("media", 0, 1, "")
    media_s, clips = media.prepare(spec, base, cache / "clips", lambda m: say("media", 0, 1, m))
    if vmap:
        say("words", 0, 1, "")
    words_s = audio.word_times(spec, vmap, cache / "voice", align) if vmap else {}
    mouth_s = {}
    if vmap and any(sc.get("lipsync") for sc in spec["scenes"]):
        say("lipsync", 0, 1, "")
        from .lipsync import voice_cues
        mouth_s = voice_cues(spec, vmap)                      # Rhubarb; pa la -> timeline() estime ak mo yo
    tl = make_timeline(spec, audio.voice_seconds(vmap), media_s, words_s, mouth_s)
    t_prep = round(time.time() - _t_prep, 1)   # vwa + Whisper + medya
    total = tl_total(tl, spec)
    spec = dict(spec, _total=total)
    n_frames = int(round(total * fps))

    # 2. the composition page (relative links to the clip frames)
    work = cache / "render"
    work.mkdir(parents=True, exist_ok=True)
    page = work / "composition.html"
    page.write_text(build_html(spec, tl, base, clips, work), encoding="utf-8")
    url = page.as_uri() + "#render"

    # 3. which pieces must be captured: every scene is cut in pieces of PIECE_S seconds, so ALL the browsers work
    #    even on a 3-scene video (capture speed grows almost linearly with browsers: the GPU read-back waits, the
    #    CPU does not). A piece is the cache unit: a re-render redoes only the pieces of the changed scenes.
    enc_name, enc_args = encoder(w, h, fps)
    vf = _look_filter(spec.get("look") or {}, w, h, k)
    jobs, chunks = [], []
    step = max(1, int(round(PIECE_S * fps)))
    for i, (sc, t) in enumerate(zip(spec["scenes"], tl)):
        f0 = int(round(t["start"] * fps))
        f1 = n_frames if t["last"] else int(round((t["start"] + t["dur"]) * fps))
        if f1 <= f0:
            continue
        key = _scene_key(spec, sc, t, clips, enc_name)
        for n, a in enumerate(range(f0, f1, step)):
            b = min(f1, a + step)
            if f1 - b < step // 3:                            # no tiny last piece: it joins this one
                b = f1
            ck = work / f"chunk-{key}-{n:03d}.mp4"
            chunks.append(ck)
            if not ck.is_file():
                jobs.append((i, a, b, ck))
            if b == f1:
                break
    reused = len(chunks) - len(jobs)
    todo = sum(f1 - f0 for _, f0, f1, _ in jobs)
    n_workers = max(1, min(workers or default_workers(), len(jobs) or 1, MAX_WORKERS))
    done = [0]
    browser_ver = [""]
    errors: list[str] = []
    lock = threading.Lock()
    q: queue.Queue = queue.Queue()
    for j in jobs:                                                # in order: the start of the video is ready first
        q.put(j)
    ff = media.find_tool("ffmpeg")
    t_cap = time.time()

    def worker():
        try:
            br = Browser()
            with lock:
                if not browser_ver[0]:
                    browser_ver[0] = br.version()
            pg = br.pages(url, 1, w, h)[0]
        except (CDPError, OSError) as e:
            with lock:
                errors.append(f"browser: {e}")
            return
        try:
            while not errors:
                try:
                    i, f0, f1, ck = q.get_nowait()
                except queue.Empty:
                    return
                part = ck.with_suffix(".part.mp4")
                from . import blend as B
                layered = B.AVAILABLE and _uses_exact_blend(spec, spec["scenes"][i])
                if layered and not getattr(pg, "_transparent", False):       # transparent PNG for lone layers
                    pg.call("Emulation.setDefaultBackgroundColorOverride", color={"r": 0, "g": 0, "b": 0, "a": 0})
                    pg._transparent = True
                src_args = (["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}"] if layered
                            else ["-f", "image2pipe", "-c:v", "mjpeg"])
                cmd = [ff, "-y", "-v", "error", *src_args, "-framerate", str(fps * k),
                       "-i", "-", "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", *enc_args, "-r", str(fps),
                       "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-an",
                       str(part)]
                enc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=_NOWIN)
                try:
                    last_shot = None
                    last_was_moving = True
                    for fi in range(f0, f1):
                        if cancel and cancel():
                            raise RenderError("cancelled")
                        t_frame = fi / fps
                        is_moving = (k > 1 or pg.eval(f"window.__busy({t_frame:.6f})", wait=False) is not False)
                        # Sote imaj ki pa bouje (Frame Deduplication):
                        # Lè sèn nan pa bouje epi dènye imaj la deja pran,
                        # re-itilize dènye imaj la dirèkteman pou FFmpeg san rekalkile piksèl nan navigatè a!
                        if not is_moving and not last_was_moving and last_shot is not None:
                            enc.stdin.write(last_shot * k)
                        else:
                            for s in range(k if (k > 1 and is_moving) else 1):
                                pg.eval(f"window.__seek({(fi + s / k) / fps:.6f})")
                                shot = _layered_frame(pg, w, h) if layered else screenshot(pg, w, h, quality=CAPTURE_Q)
                                enc.stdin.write(shot * (1 if (k > 1 and is_moving) else k))
                                last_shot = shot
                        last_was_moving = is_moving
                        with lock:
                            done[0] += 1
                            if done[0] % 5 == 0 or done[0] == todo:
                                el = time.time() - t_cap
                                say("frames", done[0], todo, f"{done[0] / el:.1f} fps" if el > 0 else "")
                    enc.stdin.close()
                    err = enc.stderr.read().decode(errors="replace")
                    if enc.wait() != 0 or not part.is_file():
                        raise RenderError(f"encoder ({enc_name}): {err.strip()[-300:]}")
                    part.replace(ck)                                      # chunk finished = checkpoint
                except BaseException as e:
                    enc.kill()
                    part.unlink(missing_ok=True)
                    with lock:
                        errors.append(str(e))
                    return
        finally:
            br.close()

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(n_workers if jobs else 0)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    if errors:
        raise RenderError(errors[0])
    cap_s = time.time() - t_cap

    # 4. sound + assembly
    say("sound", 0, 1, "")
    _t_asm = time.time()
    from .compose import events
    sound = audio.mix(spec, tl, total, work / "sound.m4a", base, vmap, cache / "music", events(spec, tl))
    lst = work / "chunks.txt"
    lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in chunks), encoding="utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.stem + ".part.mp4")
    r = subprocess.run([ff, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(sound),
                        "-map", "0:v", "-map", "1:a", "-c", "copy", "-t", f"{total:.3f}", "-movflags", "+faststart",
                        "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                        str(tmp)], capture_output=True, text=True, creationflags=_NOWIN)
    if r.returncode != 0 or not tmp.is_file() or tmp.stat().st_size < 1024:
        tmp.unlink(missing_ok=True)
        raise RenderError(f"asanblaj MP4 final la echwe (imaj + son): {(r.stderr or '').strip()[-300:] or 'fichye vid'}")
    # Ranplase tmp -> out ak sekirite sou Windows (kont WinError 5 lè yon lektè te louvri l)
    replaced = False
    for _try in range(6):
        try:
            tmp.replace(out)
            replaced = True
            break
        except PermissionError:
            time.sleep(0.3)
    if not replaced:
        try:
            if out.is_file():
                bak = out.with_name(f"{out.stem}.old{int(time.time())}.mp4")
                try:
                    out.rename(bak)
                    tmp.replace(out)
                    try:
                        bak.unlink(missing_ok=True)
                    except Exception:
                        pass
                    replaced = True
                except Exception:
                    pass
            if not replaced:
                tmp.replace(out)
        except PermissionError as e:
            raise RenderError(f"Fichye videyo a ({out.name}) bloke paske li louvri nan yon lektè sou PC a. Fèmen lektè a epi relanse: {e}")
    t_asm = round(time.time() - _t_asm, 1)   # mix odyo + konkatenasyon
    srt = audio.write_srt(spec, tl, out.with_suffix(".srt")) if subtitles else None
    result = {"mp4": out, "srt": srt, "seconds": total, "frames": n_frames, "reused": reused,
              "captured": len(jobs), "fps_capture": round(todo / cap_s, 2) if todo and cap_s else None,
              "encoder": enc_name, "browser": browser_ver[0] or "?", "workers": n_workers,
              "elapsed": round(time.time() - t_start, 1),
              "timing": {"prep": t_prep, "capture": round(cap_s, 1), "assemble": t_asm}, "timeline": tl}
    if verify:                                           # KONTWÒL MP4 apre rann (son + fraz nan bon sèn)
        try:
            result["qc"] = audio.check_render(spec, tl, out, spec.get("lang", "fr"))
        except Exception as e:                           # noqa: BLE001
            result["qc"] = {"checked": False, "note": str(e), "issues": []}
    say("done", 1, 1, str(out))
    return result


def frame(spec: dict, t: float, out: str | Path, base: str | Path | None = None, cache: str | Path | None = None) -> Path:
    """One PNG of instant t (for an AI to look at)."""
    out = Path(out).resolve()
    base = Path(base).resolve() if base else out.parent
    cache = Path(cache).resolve() if cache else out.parent / ".kadans-cache"
    spec = validate(spec) if "w" not in spec else spec
    media_s, clips = media.prepare(spec, base, cache / "clips")
    tl = make_timeline(spec, None, media_s)
    work = cache / "render"
    work.mkdir(parents=True, exist_ok=True)
    page = work / "frame.html"
    page.write_text(build_html(spec, tl, base, clips, work), encoding="utf-8")
    with Browser(no_gpu=True) as br:
        pg = br.pages(page.as_uri() + "#render", 1, spec["w"], spec["h"])[0]
        pg.eval(f"window.__seek({max(0.0, min(t, tl_total(tl, spec))):.4f})")
        out.write_bytes(screenshot(pg, spec["w"], spec["h"], "png"))
    return out


def clear_cache(cache: str | Path) -> None:
    shutil.rmtree(cache, ignore_errors=True)
