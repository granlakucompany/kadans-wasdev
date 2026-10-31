"""Kadans WASDEV — `kadans doctor` (what works, what is missing, how to fix it) and `kadans setup` (one command that
gets the two programs Kadans needs, in Kadans' own folder, the same version for everyone):

- Chromium: Google's "chrome-headless-shell" (Chrome for Testing, BSD-style license), version pinned below. Every PC
  then renders with the SAME engine (fonts, CSS, colors identical); without it Kadans uses Edge / Chrome.
- FFmpeg: an LGPL build (no GPL encoders) from github.com/BtbN/FFmpeg-Builds, checked against the release checksums.

Folder: $KADANS_HOME, else %LOCALAPPDATA%\\kadans (Windows) / ~/.cache/kadans. Nothing is installed system-wide.
The first render gets what is missing by itself (auto_setup); KADANS_NO_AUTO_SETUP=1 turns that off.
"""
from __future__ import annotations

import hashlib
import io
import os
import platform
import shutil
import sys
import tarfile
import threading
import time
import urllib.request
import zipfile
from pathlib import Path

CHROME_VERSION = "155.0.8059.84"
CHROME_URL = "https://storage.googleapis.com/chrome-for-testing-public/{v}/{p}/chrome-headless-shell-{p}.zip"
CHROME_SHA256 = {"win64": "5ca590a4968864e219ea25ccd134597ef8898a733a4698c07fc3e8b2c480fef4"}
FFMPEG_REL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
FFMPEG_ASSET = {"win64": "ffmpeg-n8.1-latest-win64-lgpl-8.1.zip", "winarm64": "ffmpeg-n8.1-latest-winarm64-lgpl-8.1.zip",
                "linux64": "ffmpeg-n8.1-latest-linux64-lgpl-8.1.tar.xz",
                "linuxarm64": "ffmpeg-n8.1-latest-linuxarm64-lgpl-8.1.tar.xz"}
EXE = ".exe" if os.name == "nt" else ""


def home() -> Path:
    env = os.environ.get("KADANS_HOME")
    if env:
        return Path(env)
    return Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".cache") / "kadans"


def plat() -> str:
    m = platform.machine().lower()
    arm = m in ("arm64", "aarch64")
    if sys.platform == "win32":
        return "winarm64" if arm else "win64"
    if sys.platform == "darwin":
        return "mac-arm64" if arm else "mac-x64"
    return "linuxarm64" if arm else "linux64"


def chrome_path() -> Path | None:
    """The pinned Chromium of `kadans setup`, if it is there."""
    p = plat()
    cp = "win64" if p == "winarm64" else ("linux64" if p == "linuxarm64" else p)   # arm: x64 build (emulated)
    exe = home() / "chrome" / CHROME_VERSION / f"chrome-headless-shell-{cp}" / ("chrome-headless-shell" + EXE)
    return exe if exe.is_file() else None


def ffmpeg_dir() -> Path:
    return home() / "ffmpeg" / "bin"


# ----------------------------------------------------------------------------------------------- download
def _get(url: str, say, label: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "kadans-setup"})
    with urllib.request.urlopen(req, timeout=60) as r:
        size = int(r.headers.get("Content-Length") or 0)
        buf, t0 = io.BytesIO(), time.time()
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            buf.write(chunk)
            if time.time() - t0 > 1 or not chunk:
                t0 = time.time()
                say(f"{label}: {buf.tell() >> 20} / {size >> 20} MB" if size else f"{label}: {buf.tell() >> 20} MB")
        return buf.getvalue()


def _safe_extract(data: bytes, name: str, dest: Path) -> None:
    """zip / tar.xz into dest; no path may leave dest."""
    dest.mkdir(parents=True, exist_ok=True)
    root = dest.resolve()
    if name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for m in z.infolist():
                target = (dest / m.filename).resolve()
                if root != target and root not in target.parents:
                    raise RuntimeError(f"unsafe path in archive: {m.filename}")
            z.extractall(dest)
    else:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:xz") as t:
            t.extractall(dest, filter="data")


def setup_chrome(say=print) -> Path:
    p = plat()
    cp = "win64" if p == "winarm64" else ("linux64" if p == "linuxarm64" else p)
    have = chrome_path()
    if have:
        say(f"Chromium {CHROME_VERSION}: already here ({have})")
        return have
    url = CHROME_URL.format(v=CHROME_VERSION, p=cp)
    data = _get(url, say, f"Chromium {CHROME_VERSION}")
    want = CHROME_SHA256.get(cp)
    got = hashlib.sha256(data).hexdigest()
    if want and got != want:
        raise RuntimeError(f"Chromium download is damaged (SHA-256 {got[:16]}…, expected {want[:16]}…)")
    dest = home() / "chrome" / CHROME_VERSION
    _safe_extract(data, url, dest)
    exe = chrome_path()
    if not exe:
        raise RuntimeError("Chromium: the archive did not contain chrome-headless-shell")
    if os.name != "nt":
        exe.chmod(0o755)
    say(f"Chromium {CHROME_VERSION}: ok ({exe})")
    return exe


def setup_ffmpeg(say=print) -> Path:
    p = plat()
    asset = FFMPEG_ASSET.get(p)
    exe = ffmpeg_dir() / ("ffmpeg" + EXE)
    if exe.is_file():
        say(f"FFmpeg: already here ({exe})")
        return exe
    if not asset:
        raise RuntimeError("FFmpeg: no ready-made LGPL build for macOS here — install it with `brew install ffmpeg` "
                           "(or set KADANS_FFMPEG)")
    sums = _get(FFMPEG_REL + "checksums.sha256", lambda m: None, "checksums").decode()
    want = next((ln.split()[0] for ln in sums.splitlines() if ln.strip().endswith(asset)), None)
    if not want:
        raise RuntimeError(f"FFmpeg: {asset} is not in the release checksums")
    data = _get(FFMPEG_REL + asset, say, "FFmpeg (LGPL)")
    if hashlib.sha256(data).hexdigest() != want:
        raise RuntimeError("FFmpeg download is damaged (SHA-256 does not match the release checksums)")
    tmp = home() / "ffmpeg.tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    _safe_extract(data, asset, tmp)
    top = next(d for d in tmp.iterdir() if d.is_dir())
    dst = home() / "ffmpeg"
    shutil.rmtree(dst, ignore_errors=True)
    top.replace(dst)
    shutil.rmtree(tmp, ignore_errors=True)
    for f in (ffmpeg_dir() / ("ffplay" + EXE),):                  # not needed
        f.unlink(missing_ok=True)
    if os.name != "nt":
        for f in ffmpeg_dir().iterdir():
            f.chmod(0o755)
    say(f"FFmpeg: ok ({exe})")
    return exe


_AUTO_LOCK = threading.Lock()
_AUTO_TRIED: set[str] = set()


def auto_setup(what: str) -> bool:
    """First render without FFmpeg / without any Chromium: download it once (messages on stderr — stdout may be an
    MCP channel). Several render threads ask at the same time: one downloads, the others wait. False = not possible."""
    if os.environ.get("KADANS_NO_AUTO_SETUP"):
        return False
    with _AUTO_LOCK:
        if what in _AUTO_TRIED:
            return (ffmpeg_dir() / ("ffmpeg" + EXE)).is_file() if what == "ffmpeg" else chrome_path() is not None
        _AUTO_TRIED.add(what)

        def say(m):
            print(f"[kadans] {m}", file=sys.stderr, flush=True)
        try:
            say(f"{what} not found: downloading it once into {home()} (KADANS_NO_AUTO_SETUP=1 to turn this off)")
            (setup_ffmpeg if what == "ffmpeg" else setup_chrome)(say)
            return True
        except Exception as e:                                    # noqa: BLE001
            say(f"{what}: automatic download failed ({e}) - run `kadans doctor`")
            return False


def setup(browser: bool = True, ffmpeg: bool = True, say=print) -> dict:
    out = {}
    if ffmpeg:
        out["ffmpeg"] = str(setup_ffmpeg(say))
    if browser:
        out["chromium"] = str(setup_chrome(say))
    return out


# ----------------------------------------------------------------------------------------------- doctor
def doctor(render_test: bool = True) -> list[dict]:
    """[{name, ok, detail, fix}] — every check, with the exact fix when something is missing."""
    from . import media
    from .cdp import Browser, find_chromium
    res = []

    def add(name, ok, detail, fix=""):
        res.append({"name": name, "ok": bool(ok), "detail": detail, "fix": "" if ok else fix})

    add("python", sys.version_info >= (3, 10), platform.python_version(), "Python 3.10 or newer is needed")
    exe = find_chromium()
    pinned = chrome_path()
    env = os.environ.get("KADANS_CHROME")
    add("chromium", exe, (exe or "none") + ("  (pinned: same engine on every PC)" if exe and pinned and
                                              Path(exe) == pinned else "  (KADANS_CHROME)" if exe and exe == env
                                              else "  (system browser)" if exe else ""),
        "run `kadans setup` (downloads Chromium for Kadans), or install Edge / Chrome")
    if exe and not pinned and exe != env:
        res[-1]["fix"] = "optional: `kadans setup` gives every PC the same Chromium (identical renders)"
    try:
        ff = media.find_tool("ffmpeg")
        from .renderer import encoder
        enc = encoder(1920, 1080, 30)[0]
        add("ffmpeg", True, f"{ff}  (H.264 encoder: {enc})")
        if enc == "mpeg4":
            res[-1]["fix"] = "this FFmpeg has no H.264 encoder: `kadans setup` gets one"
    except Exception as e:                                        # noqa: BLE001
        add("ffmpeg", False, str(e), "run `kadans setup` (downloads FFmpeg LGPL), or set KADANS_FFMPEG")
    try:
        from . import fonts
        add("fonts", True, f"{len(fonts.families())} font families on this PC")
    except Exception as e:                                        # noqa: BLE001
        add("fonts", False, str(e), "fonts could not be read (Kadans still works with web-safe fonts)")
    try:
        from .renderer import _free_ram_mb, default_workers
        ram = _free_ram_mb()
        add("memory", not ram or ram > 1500, f"{ram} MB free - {default_workers()} browsers in parallel" if ram
            else "unknown", "close some programs: each render browser needs ~450 MB")
    except Exception as e:                                        # noqa: BLE001
        add("memory", True, f"unknown ({e})")
    for mod, what, fix in (("numpy", "exact blend modes (10 of the 27)", "pip install kadans-wasdev[blend]"),
                           ("faster_whisper", "word timing from the voice", "pip install faster-whisper")):
        try:
            __import__(mod)
            add(mod, True, what)
        except ImportError:
            add(mod, True, f"not installed (optional: {what})")
            res[-1]["fix"] = fix
    if render_test and exe:
        t0 = time.time()
        try:
            import tempfile
            page = Path(tempfile.mkdtemp(prefix="kadans-doc-")) / "t.html"
            page.write_text("<html><body style='margin:0;background:#07080f'><div id=x style='color:#22d3ee;"
                            "font:700 60px sans-serif'>Kadans</div><script>window.__seek=async t=>{"
                            "document.getElementById('x').style.transform='translateX('+t*100+'px)'};"
                            "</script></body></html>", encoding="utf-8")
            from .cdp import screenshot
            with Browser() as br:
                pg = br.pages(page.as_uri(), 1, 640, 360)[0]
                pg.eval("window.__seek(1)")
                img = screenshot(pg, 640, 360)
            shutil.rmtree(page.parent, ignore_errors=True)
            add("render test", len(img) > 1000, f"one frame captured in {time.time() - t0:.1f} s ({br.kind})",
                "the browser starts but cannot capture: try KADANS_NO_GPU=1, or `kadans setup`")
        except Exception as e:                                    # noqa: BLE001
            add("render test", False, f"{type(e).__name__}: {e}",
                "the browser could not render: try KADANS_NO_GPU=1, or `kadans setup`")
    return res


def report(rows: list[dict]) -> str:
    lines = []
    for r in rows:
        mark = "ok " if r["ok"] and not r["fix"] else ("-- " if r["ok"] else "XX ")
        lines.append(f"  {mark}{r['name']:<14} {r['detail']}")
        if r["fix"]:
            lines.append(f"      -> {r['fix']}")
    bad = [r for r in rows if not r["ok"]]
    lines.append("  Ready to render." if not bad else f"  {len(bad)} problem(s): see the -> lines above.")
    return "\n".join(lines)


__all__ = ["doctor", "report", "setup", "setup_chrome", "setup_ffmpeg", "home", "chrome_path", "ffmpeg_dir",
           "CHROME_VERSION"]
