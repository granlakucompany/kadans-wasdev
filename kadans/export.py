# Ekspòtasyon Kadans -> yon sèl fichye HTML otonòm (tout bagay inline: libs, fonts, imaj) ki jwe poukont li.
# Pafè pou pataje (yon sèl .html) oswa pou animasyon web: yo ka itilize Kadans pou vwa/lang.
# Klip videyo (frame jpg) PA inline (yo chaje an dirèk) - ekspò yon-sèl-fichye bon pou sen anime/chart/html/imaj.
from __future__ import annotations

import base64
import mimetypes
import re
import shutil
import tempfile
from pathlib import Path


def export_html(spec: dict, out_html, base=None, progress=None) -> Path:
    """Konpoze spec la epi ekri YON sèl fichye HTML otonòm nan out_html. Retounen chemen an."""
    from . import compose, media
    from .spec import timeline, validate
    out_html = Path(out_html)
    clean = spec if isinstance(spec, dict) and "w" in spec else validate(spec)
    base = Path(base) if base else None
    tmp = Path(tempfile.mkdtemp(prefix="kadans_export_"))
    try:
        media_s, clips = media.prepare(clean, base, tmp / ".cache", progress)
        tl = timeline(clean, None, media_s)
        html = compose.build_html(clean, tl, base, clips, tmp)
        (tmp / "composition.html").write_text(html, encoding="utf-8")
        html = (tmp / "composition.html").read_text(encoding="utf-8")

        def datauri(p: Path) -> str:
            mime = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
            return "data:" + mime + ";base64," + base64.b64encode(p.read_bytes()).decode("ascii")

        def inline_script(m):
            rel = m.group(1)
            f = tmp / rel
            if f.is_file():
                return "<script>" + f.read_text(encoding="utf-8", errors="ignore") + "</script>"
            return m.group(0)
        html = re.sub(r'<script src="([^"]+\.js)"></script>', inline_script, html)

        def inline_url(m):
            ref = m.group(1).strip().strip('"').strip("'")
            if ref.startswith("data:") or "://" in ref:
                return m.group(0)
            f = tmp / ref
            return 'url("' + datauri(f) + '")' if f.is_file() else m.group(0)
        html = re.sub(r'url\(([^)]+)\)', inline_url, html)

        def inline_src(m):
            ref = m.group(1)
            if ref.startswith("data:") or "://" in ref:
                return m.group(0)
            f = tmp / ref
            return 'src="' + datauri(f) + '"' if f.is_file() else m.group(0)
        html = re.sub(r'src="([^"]+)"', inline_src, html)

        out_html.parent.mkdir(parents=True, exist_ok=True)
        out_html.write_text(html, encoding="utf-8")
        return out_html
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
