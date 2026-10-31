"""Kadans WASDEV — talk to a Chromium through the DevTools protocol (standard library only, no Node, no Playwright).

GPU rasterization is on (5x faster than software on a normal PC); KADANS_NO_GPU=1 forces software rendering.
Browsers, in order:
  1. $KADANS_CHROME, then Microsoft Edge / Google Chrome / Chromium already on the machine (Edge ships with Windows),
     started headless with a private, throw-away profile and the network blocked;
  2. otherwise the Chromium inside PySide6 (QtWebEngine), started in its own process (kadans.qt_host).
Nothing is shared with the person's own browser (no cookies, no sessions).
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

_NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
_SUSPENDED = 0x00000004
_JOB = None
_JOB_LOCK = threading.Lock()
_LIVE: set = set()                                    # open Browser objects (closed at exit)


def _job():
    """Windows: ONE job for every render browser of this process, with KILL_ON_JOB_CLOSE. When this process ends —
    finished, error, cancelled, the host app closed, even killed — Windows ends every browser and all its children.
    (Before: a Python stopped mid-render left its headless browsers running: 294 found on one PC.)"""
    global _JOB
    if os.name != "nt":
        return None
    with _JOB_LOCK:
        if _JOB is None:
            try:
                import ctypes
                from ctypes import wintypes

                class Basic(ctypes.Structure):
                    _fields_ = [("a", ctypes.c_int64), ("b", ctypes.c_int64), ("LimitFlags", wintypes.DWORD),
                                ("c", ctypes.c_size_t), ("d", ctypes.c_size_t), ("e", wintypes.DWORD),
                                ("f", ctypes.c_size_t), ("g", wintypes.DWORD), ("h", wintypes.DWORD)]

                class Ext(ctypes.Structure):
                    _fields_ = [("Basic", Basic), ("Io", ctypes.c_uint64 * 6), ("i", ctypes.c_size_t),
                                ("j", ctypes.c_size_t), ("k", ctypes.c_size_t), ("l", ctypes.c_size_t)]
                k32 = ctypes.WinDLL("kernel32", use_last_error=True)
                k32.CreateJobObjectW.restype = wintypes.HANDLE
                k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
                ntdll = ctypes.WinDLL("ntdll")
                ntdll.NtResumeProcess.argtypes = [wintypes.HANDLE]
                h = k32.CreateJobObjectW(None, None)
                info = Ext()
                info.Basic.LimitFlags = 0x2000                       # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                if not h or not k32.SetInformationJobObject(h, 9, ctypes.byref(info), ctypes.sizeof(info)):
                    raise OSError("job object")
                _JOB = (k32, ntdll, h)
            except (OSError, AttributeError):
                _JOB = False
    return _JOB or None


def _spawn(cmd: list, **kw) -> subprocess.Popen:
    """Start a browser (or the Qt host) so it can never outlive us: Windows = suspended → into the job → resumed
    (its child processes are born inside the job); elsewhere its own process group (killed as a group)."""
    job = _job()
    if job:
        p = subprocess.Popen(cmd, creationflags=_NOWIN | _SUSPENDED, **kw)
        k32, ntdll, h = job
        k32.AssignProcessToJobObject(h, int(p._handle))
        ntdll.NtResumeProcess(int(p._handle))
        return p
    if os.name == "nt":
        return subprocess.Popen(cmd, creationflags=_NOWIN, **kw)
    return subprocess.Popen(cmd, start_new_session=True, **kw)


def _close_all():
    for b in list(_LIVE):
        try:
            b.close()
        except Exception:                                    # noqa: BLE001
            pass


import atexit  # noqa: E402
atexit.register(_close_all)


class CDPError(RuntimeError):
    pass


# ----------------------------------------------------------------------------------------------- websocket
class WebSocket:
    """Minimal RFC 6455 client (text frames, client masking, fragmentation, ping)."""

    def __init__(self, url: str, timeout: float = 60):
        u = urlparse(url)
        self.sock = socket.create_connection((u.hostname, u.port or 80), timeout=timeout)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f"GET {u.path or '/'}{('?' + u.query) if u.query else ''} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\n"
               f"Upgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
               f"Sec-WebSocket-Version: 13\r\n\r\n")
        self.sock.sendall(req.encode())
        head = b""
        while b"\r\n\r\n" not in head:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise CDPError("websocket handshake failed")
            head += chunk
        if b" 101 " not in head.split(b"\r\n", 1)[0]:
            raise CDPError(f"websocket refused: {head[:120]!r}")
        self.buf = head.split(b"\r\n\r\n", 1)[1]

    def _read(self, n: int) -> bytes:
        while len(self.buf) < n:
            chunk = self.sock.recv(max(65536, n - len(self.buf)))
            if not chunk:
                raise CDPError("websocket closed")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def send(self, text: str, opcode: int = 1):
        data = text.encode() if isinstance(text, str) else text
        n = len(data)
        head = bytes([0x80 | opcode])
        if n < 126:
            head += bytes([0x80 | n])
        elif n < 65536:
            head += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            head += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data)) if n < 4096 else _xor(data, mask)
        self.sock.sendall(head + mask + masked)

    def recv(self) -> str:
        parts = []
        while True:
            b0, b1 = self._read(2)
            op, n = b0 & 0x0F, b1 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._read(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._read(8))[0]
            if b1 & 0x80:
                mask = self._read(4)
                payload = _xor(self._read(n), mask)
            else:
                payload = self._read(n)
            if op == 9:                                    # ping -> pong
                self.send(payload, 10)
                continue
            if op == 8:
                raise CDPError("websocket closed by the browser")
            if op in (0, 1, 2):
                parts.append(payload)
                if b0 & 0x80:
                    return b"".join(parts).decode("utf-8", "replace")

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


def _xor(data: bytes, mask: bytes) -> bytes:
    n = len(data)
    m = (mask * (n // 4 + 1))[:n]
    return (int.from_bytes(data, "little") ^ int.from_bytes(m, "little")).to_bytes(n, "little")


class Page:
    """One browser tab: call(method, **params) -> result (events are skipped)."""

    def __init__(self, ws_url: str):
        self.ws = WebSocket(ws_url)
        self._id = 0

    def call(self, method: str, **params):
        self._id += 1
        k = self._id
        self.ws.send(json.dumps({"id": k, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == k:
                if "error" in msg:
                    raise CDPError(f"{method}: {msg['error'].get('message')}")
                return msg.get("result", {})

    def eval(self, expr: str, wait: bool = True):
        r = self.call("Runtime.evaluate", expression=expr, awaitPromise=wait, returnByValue=True)
        if r.get("exceptionDetails"):
            d = r["exceptionDetails"]
            raise CDPError(f"page error: {(d.get('exception') or {}).get('description') or d.get('text')}")
        return (r.get("result") or {}).get("value")

    def close(self):
        self.ws.close()


# ----------------------------------------------------------------------------------------------- browsers
def find_chromium() -> str | None:
    env = os.environ.get("KADANS_CHROME")
    if env and Path(env).is_file():
        return env
    from .deps import chrome_path                   # `kadans setup`: the same Chromium on every PC
    pinned = chrome_path()
    if pinned:
        return str(pinned)
    pf = [os.environ.get(k, "") for k in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA")]
    cands = [Path(b) / rel for b in pf if b for rel in (
        "Microsoft/Edge/Application/msedge.exe", "Google/Chrome/Application/chrome.exe",
        "Chromium/Application/chrome.exe")]
    cands += [Path(p) for p in (shutil.which("msedge"), shutil.which("google-chrome"), shutil.which("chromium"),
                                shutil.which("chromium-browser"), shutil.which("chrome")) if p]
    cands += [Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
              Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")]
    return next((str(c) for c in cands if c.is_file()), None)


def _http(url: str, method: str = "GET"):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode() or "null")


class Browser:
    """A private headless Chromium. pages(url, n) opens n tabs on the composition."""

    FLAGS = ["--headless=new", "--no-first-run", "--no-default-browser-check", "--disable-extensions",
             "--hide-scrollbars", "--mute-audio", "--force-color-profile=srgb",
             "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
             "--disable-backgrounding-occluded-windows", "--allow-file-access-from-files",
             "--disable-features=Translate,MediaRouter,OptimizationHints", "--font-render-hinting=none",
             "--proxy-server=127.0.0.1:9", "--proxy-bypass-list=<-loopback>"]       # network blocked: all local

    def __init__(self, exe: str | None = None, log=None, no_gpu: bool = False):
        self.log = log or (lambda m: None)
        self.tmp = tempfile.mkdtemp(prefix="kadans-")
        self.proc = None
        exe = exe or find_chromium()
        if not exe:                                    # no Edge / Chrome / Chromium: get the pinned one, once
            from .deps import auto_setup
            if auto_setup("chromium"):
                exe = find_chromium()
        if exe:
            self.kind = Path(exe).stem
            flags = list(self.FLAGS)
            if no_gpu or os.environ.get("KADANS_NO_GPU"):
                flags.extend(["--disable-gpu", "--disable-d3d11", "--disable-gpu-compositing"])
            self.proc = _spawn([exe, f"--user-data-dir={self.tmp}", "--remote-debugging-port=0", *flags,
                                "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            _LIVE.add(self)
            port_file = Path(self.tmp) / "DevToolsActivePort"
            t0 = time.time()
            while True:
                try:
                    txt = port_file.read_text().strip() if port_file.is_file() else ""
                except OSError:                       # the browser is still writing it
                    txt = ""
                if txt:
                    break
                if self.proc.poll() is not None or time.time() - t0 > 30:
                    raise CDPError(f"{self.kind} did not start")
                time.sleep(0.05)
            self.port = int(txt.split()[0])
            self._bws = txt.split()[1] if len(txt.split()) > 1 else ""     # /devtools/browser/<id>
        else:
            self.kind = "qtwebengine"
            self.port = None
        self.log(f"browser: {self.kind}")

    def version(self) -> str:
        """Non + vèsyon motè navigatè a (pou render.json: si yon mizajou Edge chanje yon rann)."""
        if self.port is None:
            return "qtwebengine"
        try:
            return str(_http(f"http://127.0.0.1:{self.port}/json/version").get("Browser") or self.kind)
        except Exception:                                    # noqa: BLE001
            return self.kind

    def pages(self, url: str, n: int, w: int, h: int, scale: float = 1.0) -> list[Page]:
        if self.kind == "qtwebengine":
            return self._qt_pages(url, n, w, h)
        out = []
        for _ in range(n):                         # blank tab, then navigate: an URL given to /json/new loses its #hash
            t = _http(f"http://127.0.0.1:{self.port}/json/new?about:blank", "PUT")
            out.append(Page(t["webSocketDebuggerUrl"]))
        for p in out:
            p.call("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=scale, mobile=False)
            p.call("Page.navigate", url=url)
            _wait_ready(p, url)
        return out

    def _qt_pages(self, url: str, n: int, w: int, h: int) -> list[Page]:
        """No Chrome / Edge: the Chromium of PySide6, in its own process (kadans.qt_host)."""
        port = _free_port()
        self.proc = _spawn([sys.executable, "-m", "kadans.qt_host", url, str(n), str(w), str(h), str(port)],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                           cwd=str(Path(__file__).resolve().parent.parent))
        _LIVE.add(self)
        line = self.proc.stdout.readline().strip()
        if line != "READY":
            raise CDPError("no Chromium found: install Edge or Chrome, or PySide6 (QtWebEngine)")
        self.port = port
        targets = [t for t in _http(f"http://127.0.0.1:{port}/json") if t.get("type") == "page"]
        out = [Page(t["webSocketDebuggerUrl"]) for t in targets[:n]]
        for p in out:
            p.call("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=False)
            _wait_ready(p)
        return out

    def close(self):
        _LIVE.discard(self)
        if self.proc and self.proc.poll() is None and getattr(self, "_bws", ""):
            try:                                             # the clean way: Chromium closes itself AND its children
                ws = WebSocket(f"ws://127.0.0.1:{self.port}{self._bws}", timeout=5)
                ws.send(json.dumps({"id": 1, "method": "Browser.close"}))
                ws.close()
                self.proc.wait(1.5)
            except (OSError, CDPError, subprocess.TimeoutExpired, ValueError):
                pass
        if self.proc and self.proc.poll() is None and os.name == "nt":
            # Edge can ignore TerminateProcess (measured): end the whole tree from outside
            subprocess.run(["taskkill", "/PID", str(self.proc.pid), "/T", "/F"], capture_output=True,
                           creationflags=_NOWIN)
        if self.proc and self.proc.poll() is None:
            if os.name != "nt":
                try:
                    os.killpg(self.proc.pid, 15)             # the whole group: renderer / GPU children too
                except OSError:
                    self.proc.terminate()
            else:
                self.proc.terminate()                        # its children exit with it (and the job is the net)
            try:
                self.proc.wait(1.5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        for _ in range(6):                                  # the profile is locked a moment after exit
            shutil.rmtree(self.tmp, ignore_errors=True)
            if not os.path.isdir(self.tmp):
                break
            time.sleep(0.05)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def _wait_ready(p: Page, url: str | None = None, timeout: float = 30):
    t0 = time.time()
    want = "RENDER === true" if url and ("#render" in url or "render" in url.split("?", 1)[-1]) else "true"
    while time.time() - t0 < timeout:
        try:
            if p.eval("typeof window.__seek === 'function' && document.readyState === 'complete' && "
                      f"(typeof RENDER === 'undefined' || {want})", wait=False):
                return
        except CDPError:
            pass
        time.sleep(0.1)
    raise CDPError("the composition page did not load (no window.__seek)")


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def screenshot(p: Page, w: int, h: int, fmt: str = "jpeg", quality: int = 92) -> bytes:
    args = {"format": fmt, "fromSurface": True, "captureBeyondViewport": False,
            "clip": {"x": 0, "y": 0, "width": w, "height": h, "scale": 1}}
    if fmt == "jpeg":
        args["quality"] = quality
    if getattr(p, "_fast", True):
        args["optimizeForSpeed"] = True            # faster encoder in the browser (~1.4x measured on Edge)
    try:
        return base64.b64decode(p.call("Page.captureScreenshot", **args)["data"])
    except CDPError:
        if not args.pop("optimizeForSpeed", None):
            raise
        p._fast = False                            # an older Chromium: without it
        return base64.b64decode(p.call("Page.captureScreenshot", **args)["data"])


__all__ = ["Browser", "Page", "CDPError", "find_chromium", "screenshot", "threading"]
