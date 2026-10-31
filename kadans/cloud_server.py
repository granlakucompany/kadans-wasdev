"""Kadans WASDEV — Cloud Rendering Server (Docker / AWS Lambda / Cloud Run / Modal / RunPod).

Sèvè HTTP otonòm ki pèmèt rann videyo nan nwaj la ak Docker oswa AWS Lambda / Google Cloud Run.
San depandans lou, li itilize dirèkteman motè Kadans pou:
- Resevwa yon spec JSON pa POST /render
- Rann videyo a an paralèl sou nwayo CPU/GPU kontenè a
- Retounen fichye MP4 a dirèkteman oswa estati travay la
"""
from __future__ import annotations

import cgi
import http.server
import json
import os
import socketserver
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

from . import __version__, NAME
from .renderer import render
from .spec import SpecError, validate
from .hyperframes import import_kadans_html


class KadansCloudHandler(http.server.BaseHTTPRequestHandler):
    server_version = f"KadansCloud/{__version__}"

    def _json(self, status: int, data: dict):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/health", "/status"):
            from .renderer import encoder
            try:
                enc_name, _ = encoder(1920, 1080, 30)
            except Exception:
                enc_name = "unknown"
            self._json(200, {
                "status": "healthy",
                "service": NAME,
                "version": __version__,
                "mode": "cloud",
                "encoder": enc_name,
                "cpu_count": os.cpu_count(),
            })
        else:
            self._json(404, {"error": "Not Found"})

    def do_POST(self):
        if self.path == "/validate":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                raw = json.loads(body)
                clean = validate(raw)
                self._json(200, {"ok": True, "title": clean.get("title"), "scenes": len(clean.get("scenes", []))})
            except Exception as e:
                self._json(400, {"ok": False, "error": str(e)})
            return

        if self.path == "/import-hf":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                data = json.loads(body)
                html_code = data.get("html", "")
                title = data.get("title", "Imported Kadans HTML")
                lang = data.get("lang", "fr")
                voice_text = data.get("voice", "")
                
                with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
                    f.write(html_code)
                    tmp_src = f.name
                try:
                    spec = import_kadans_html(tmp_src, title=title, lang=lang, voice_text=voice_text)
                finally:
                    try:
                        os.unlink(tmp_src)
                    except OSError:
                        pass
                self._json(200, {"ok": True, "spec": spec})
            except Exception as e:
                self._json(400, {"ok": False, "error": str(e)})
            return

        if self.path == "/render":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                raw_spec = json.loads(body)
                clean_spec = validate(raw_spec)
                
                # Kreye dosye travay tanporè
                with tempfile.TemporaryDirectory(prefix="kadans_cloud_") as tmp_dir:
                    td = Path(tmp_dir)
                    out_mp4 = td / "output.mp4"
                    
                    t0 = time.time()
                    res = render(clean_spec, out_mp4, base=td, cache=td / ".cache")
                    elapsed = round(time.time() - t0, 2)
                    
                    if not out_mp4.is_file():
                        self._json(500, {"error": "Rann videyo a echwe pou pwodui fichye final la."})
                        return

                    video_bytes = out_mp4.read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", "video/mp4")
                    self.send_header("Content-Length", str(len(video_bytes)))
                    self.send_header("Content-Disposition", f'attachment; filename="{clean_spec.get("title", "video")}.mp4"')
                    self.send_header("X-Kadans-Elapsed", str(elapsed))
                    self.send_header("X-Kadans-Encoder", str(res.get("encoder", "unknown")))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(video_bytes)
            except Exception as e:
                self._json(500, {"error": str(e)})
            return

        self._json(404, {"error": "Endpoint not found"})


def run_server(port: int = 8080, host: str = "0.0.0.0"):
    """Kouri sèvè Kadans Cloud la."""
    server_address = (host, port)
    with socketserver.ThreadingTCPServer(server_address, KadansCloudHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"🚀 Kadans Cloud Render Server k ap kouri sou http://{host}:{port}")
        print(f"   - GET  /health   -> Sante & enfòmasyon motè a")
        print(f"   - POST /render   -> Rann JSON spec an videyo MP4")
        print(f"   - POST /import-hf-> Enpòte HTML/GSAP Kadans")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nFèmen Kadans Cloud Server...")
