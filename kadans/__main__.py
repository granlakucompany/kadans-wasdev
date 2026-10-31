"""Kadans WASDEV command line.

    kadans validate spec.json               check a spec (every problem listed)
    kadans html spec.json [-o out.html]     composition page (open it in a browser = live preview with a time bar)
    kadans lint spec.json                   layout / timing report (JSON) before rendering
    kadans frame spec.json --t 12.4 -o x.png   one frame, for an AI (or you) to look at
    kadans render spec.json -o pub.mp4 [--workers 3]   MP4 + .srt (finished scenes are cached: re-runs are fast)
    kadans export spec.json -o one.html     one self-contained .html (inlined, plays itself)
    kadans timeline <folder|spec.json>      open the editor (Kadans Timeline) in a browser
    kadans schema                           JSON Schema of the spec
    kadans fonts [word]                     fonts installed on this PC (for brand.font / font_title / font_code)
    kadans doctor                           what works, what is missing, and the exact fix
    kadans setup [--no-browser] [--no-ffmpeg]   get Chromium (pinned) + FFmpeg (LGPL) into Kadans' own folder
    kadans mcp [--install CLIENT | --print] MCP server: any AI (Claude, ChatGPT / Codex, Gemini, Cursor, VS Code…)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from . import NAME, __version__
from .spec import SpecError, json_schema, timeline, total, validate

BANNER = f"  </> {NAME} {__version__} - GRAN LAKU COMPANY"


def _load(p: str) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["mcp"]:                       # MCP server for every AI client (stdout = protocol only)
        from .mcp_server import main as mcp_main
        return mcp_main(argv[1:])
    ap = argparse.ArgumentParser(prog="kadans", description=f"{NAME}: videos written as code (JSON -> HTML -> MP4)")
    ap.add_argument("--version", action="version", version=f"{NAME} {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, hlp in (("validate", "check a spec"), ("html", "write the composition page (live preview)"),
                      ("lint", "layout / timing report"), ("frame", "one frame as PNG"), ("render", "render the MP4"),
                      ("export", "one self-contained .html (libs/fonts/images inlined, plays itself)")):
        p = sub.add_parser(name, help=hlp)
        p.add_argument("spec")
        if name in ("html", "frame", "render", "export"):
            p.add_argument("-o", "--out")
        if name == "frame":
            p.add_argument("--t", type=float, required=True, help="time in seconds")
        if name == "render":
            p.add_argument("--workers", type=int, help="browsers capturing in parallel")
            p.add_argument("--no-srt", action="store_true")
    sub.add_parser("schema", help="print the spec JSON Schema")
    fp = sub.add_parser("fonts", help="fonts installed on this PC (usable in brand.font / font_title / font_code)")
    fp.add_argument("query", nargs="?", default="")
    fp.add_argument("--json", action="store_true")
    sop = sub.add_parser("sounds", help="the CC0 sound library (find:… / sfx:id in sounds, ambience, rig steps)")
    sop.add_argument("query", nargs="?", default="")
    sop.add_argument("--json", action="store_true")
    sub.add_parser("doctor", help="check everything Kadans needs (and how to fix what is missing)")
    sp = sub.add_parser("setup", help="download Chromium (pinned version) and FFmpeg (LGPL) for Kadans")
    sp.add_argument("--no-browser", action="store_true")
    sp.add_argument("--no-ffmpeg", action="store_true")
    ihp = sub.add_parser("import-html", aliases=["import-hf"], help="import an HTML/CSS/GSAP animation project into a Kadans spec")
    ihp.add_argument("source", help="path to HTML animation file or folder")
    ihp.add_argument("-o", "--out", help="destination spec.json path")
    ihp.add_argument("--title", help="video title")
    ihp.add_argument("--lang", default="fr", help="language (ht, fr, en, es, pt)")
    ihp.add_argument("--voice", help="voice narration line for the scene")
    stp = sub.add_parser("timeline", aliases=["studio"], help="open the editor (Kadans Timeline) in a browser")
    stp.add_argument("path", help="a project folder or a spec.json")
    stp.add_argument("--port", type=int, default=0)
    stp.add_argument("--token", default=None, help="session token")
    stp.add_argument("--no-open", action="store_true")
    np_ = sub.add_parser("new", help="create a project with the standard layout (01-senaryo, 02-storyboard, medya/, Exported Videos/)")
    np_.add_argument("name", help="a REAL descriptive name, e.g. Lanmou-nan-Jakmel (not an id, not project1)")
    np_.add_argument("--dir", default="Analyseur-Kadans", help="parent folder (default: Analyseur-Kadans)")
    srv_p = sub.add_parser("server", help="run HTTP Cloud render server for Docker / Cloud Run / Lambda")
    srv_p.add_argument("--port", type=int, default=8080, help="port to listen on (default: 8080)")
    srv_p.add_argument("--host", default="0.0.0.0", help="host address (default: 0.0.0.0)")
    a = ap.parse_args(argv)
    if a.cmd in ("doctor", "setup"):
        from . import deps as S
        print(BANNER)
        if a.cmd == "setup":
            try:
                S.setup(browser=not a.no_browser, ffmpeg=not a.no_ffmpeg, say=lambda m: print("  " + m, flush=True))
            except Exception as e:                    # noqa: BLE001
                print(f"  setup failed: {e}", file=sys.stderr)
                return 1
        rows = S.doctor()
        print(S.report(rows))
        return 0 if all(r["ok"] for r in rows) else 1
    if a.cmd == "new":
        from . import layout as LY
        why = LY.check_name(a.name)
        if why:
            print(f"refused: {why} - give the project a real descriptive name", file=sys.stderr)
            return 2
        d = LY.ensure(Path(a.dir) / a.name.strip().replace(" ", "-"), a.name)
        print(f"created {d}")
        for x in (LY.SCRIPT, LY.BOARD, *(f"{LY.MEDIA}/{k}" for k in LY.KINDS), LY.RENDERS):
            print(f"  {x}/")
        return 0
    if a.cmd == "schema":
        print(json.dumps(json_schema(), indent=2, ensure_ascii=False))
        return 0
    if a.cmd == "fonts":
        from .fonts import families
        fams = families(query=a.query)
        if a.json:
            print(json.dumps(fams, indent=1, ensure_ascii=False))
        else:
            for f in fams:
                print(f"{f['family']}  ({', '.join(f['styles'][:6])}{'…' if len(f['styles']) > 6 else ''})")
            print(f"{len(fams)} families", file=sys.stderr)
        return 0
    if a.cmd == "sounds":
        from . import sounds as SO
        hits = SO.search(a.query, limit=50) if a.query else SO.library()
        if a.json:
            print(json.dumps([{**e, "files": [str(f) for f in e["files"]]} for e in hits], indent=1, ensure_ascii=False))
        else:
            for e in hits:
                loop = " loop" if e.get("loop") else ""
                print(f"sfx:{e['id']:<20} {e.get('kind', ''):<9}{loop:<5} {(e.get('dur') or 0):5.1f} s  "
                      f"x{len(e['files'])}  {' '.join((e.get('tags') or [])[:7])}")
            print(f"{len(hits)} sounds (CC0)", file=sys.stderr)
        return 0
    if a.cmd in ("timeline", "studio"):
        from .studio_server import open_studio
        pth = Path(a.path).resolve()
        if pth.is_dir() or not pth.suffix:
            work, spec_path, base = pth, pth / "spec.json", pth
        else:
            work, spec_path, base = pth.parent, pth, pth.parent
        if not spec_path.is_file():
            work.mkdir(parents=True, exist_ok=True)
            starter = {"brand": {"name": "Nouvo videyo", "colors": {"bg": "#0b0816", "primary": "#8b5cf6", "accent": "#0098ff", "text": "#f3eefe"}},
                       "ratio": "16:9", "voice": {"gender": "female", "enhance": True},
                       "scenes": [{"type": "hook", "id": "s1", "title": "Byenveni", "subtitle": "Kadans Timeline", "voice": "Byenveni nan Kadans", "duration": 2.5},
                                  {"type": "cta", "id": "s2", "title": "Komanse", "voice": "Ann komanse", "duration": 2}]}
            spec_path.write_text(json.dumps(starter, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  nouvo spec.json kreye: {spec_path}")
        srv = open_studio(work, spec_path, base, port=a.port, token=getattr(a, "token", None))
        print(BANNER)
        try:
            srv.build()
        except Exception as e:                            # noqa: BLE001
            print(f"  build warning: {e}", file=sys.stderr)
        print(f"  Kadans Timeline: {srv.url()}")
        if not a.no_open:
            import webbrowser
            webbrowser.open(srv.url())
        print("  Ctrl+C pou kanpe.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            srv.stop()
    if a.cmd in ("import-html", "import-hf"):
        from .hyperframes import import_kadans_html
        sp = import_kadans_html(a.source, title=a.title or "", lang=a.lang or "fr", voice_text=a.voice or "")
        out = Path(a.out or Path(a.source).with_suffix(".json")).resolve()
        out.write_text(json.dumps(sp, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"ok: Pwojè animasyon HTML enpòte nan {out}")
        return 0
    if a.cmd == "server":
        from .cloud_server import run_server
        run_server(port=a.port, host=a.host)
        return 0
    print(BANNER, file=sys.stderr)
    src = Path(a.spec).resolve()
    try:
        spec = validate(_load(a.spec))
    except SpecError as e:
        print("spec errors:", *("  - " + x for x in e.errors), sep="\n", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read {a.spec}: {e}", file=sys.stderr)
        return 1
    base = src.parent
    try:
        if a.cmd == "validate":
            tl = timeline(spec)
            print(f"ok: {len(spec['scenes'])} scenes, ~{total(tl):.1f} s, {spec['w']}x{spec['h']} @ {spec['fps']} fps")
        elif a.cmd == "html":
            from .compose import build_html
            from .media import prepare
            out = Path(a.out or src.with_suffix(".html")).resolve()
            media_s, clips = prepare(spec, base, base / ".kadans-cache" / "clips")
            out.write_text(build_html(spec, timeline(spec, None, media_s), base, clips, out.parent), encoding="utf-8")
            print(f"ok: {out}")
        elif a.cmd == "lint":
            from .lint import lint
            r = lint(spec, base)
            print(json.dumps(r, indent=2, ensure_ascii=False))
            return 0 if r["ok"] else 2
        elif a.cmd == "frame":
            from .renderer import frame
            out = frame(spec, a.t, a.out or src.with_name(f"{src.stem}_{a.t:g}s.png"), base)
            print(f"ok: {out}")
        elif a.cmd == "export":
            from .export import export_html
            out = Path(a.out or src.with_name(f"{src.stem}-export.html")).resolve()
            export_html(spec, out, base)
            print(f"ok: {out} (single self-contained HTML)")
        elif a.cmd == "render":
            from .renderer import render
            last = [0.0]

            def prog(stage, done, tot, info):
                if stage != "frames" or time.time() - last[0] > 2 or done == tot:
                    last[0] = time.time()
                    print(f"\r  {stage:7s} {done}/{tot} {info}".ljust(70), end="", file=sys.stderr, flush=True)
            r = render(spec, a.out or src.with_suffix(".mp4"), base, workers=a.workers, progress=prog,
                       subtitles=not a.no_srt)
            print(file=sys.stderr)
            print(f"ok: {r['mp4']} ({r['seconds']:.1f} s, {r['frames']} frames, {r['captured']} scenes captured, "
                  f"{r['reused']} from cache, {r['encoder']}, {r['elapsed']} s)")
    except Exception as e:                                            # noqa: BLE001 - one clear line for the CLI
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
