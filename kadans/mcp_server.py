"""Kadans WASDEV — MCP server (Model Context Protocol, stdio), standard library only.

Any AI client that speaks MCP can make videos with Kadans: Claude (Desktop, Code), ChatGPT / Codex, Gemini CLI,
Cursor, VS Code, Windsurf, Cline, Continue, Zed, LM Studio… — one server, the same tools for every AI.

    kadans mcp                         run the server (the AI client starts it)
    kadans mcp --install <client>      write the client's config (claude-desktop, claude-code, codex, gemini,
                                       cursor, vscode, windsurf) — a backup of the old config is kept
    kadans mcp --print                 the JSON block to paste into any other client

Voice: set KADANS_TTS_CMD to any local text-to-speech command, with {text} (a UTF-8 text file), {out} (the WAV to
write), {lang} and {gender}. Word timing: faster-whisper is used if it is installed, otherwise estimated.
"""
from __future__ import annotations

import base64
import copy
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from pathlib import Path

from . import NAME, __version__

PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")
_JOBS: dict = {}


def _log(*a):
    print(*a, file=sys.stderr, flush=True)


# ----------------------------------------------------------------------------------------------- helpers
def _spec_arg(a: dict) -> tuple[dict, Path]:
    """spec = object, JSON text, or a path to a spec.json; folder = where relative paths resolve."""
    spec, folder = a.get("spec"), a.get("folder")
    src = None
    if isinstance(spec, str):
        s = spec.strip()
        if s.startswith("{"):
            spec = json.loads(s)
        else:
            src = Path(s).expanduser()
            spec = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise ValueError("spec: a JSON object, JSON text or the path of a spec .json file")
    base = Path(folder).expanduser() if folder else (src.parent if src else Path.cwd())
    return spec, base.resolve()


def _tts():
    cmd = os.environ.get("KADANS_TTS_CMD", "").strip()
    if not cmd:
        return None

    def tts(text, lang, gender, sample, out):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
            fh.write(text)
        try:
            args = [a.format(text=fh.name, out=str(out), lang=lang or "", gender=gender or "") for a in shlex.split(cmd)]
            subprocess.run(args, check=True, capture_output=True, timeout=600)
        finally:
            os.unlink(fh.name)
    return tts


def _align():
    try:
        from faster_whisper import WhisperModel                       # optional
    except ImportError:
        return None
    holder = []

    def align(wav, text, lang):
        if not holder:
            holder.append(WhisperModel(os.environ.get("KADANS_WHISPER", "small"), device="cpu", compute_type="int8"))
        segs, _ = holder[0].transcribe(str(wav), language=(lang or "en")[:2], word_timestamps=True, initial_prompt=text)
        return [[w.word.strip(), w.start, w.end] for sg in segs for w in (sg.words or []) if w.word.strip()]
    return align


def _text(t: str, error: bool = False) -> dict:
    return {"content": [{"type": "text", "text": t}], "isError": error}


# ----------------------------------------------------------------------------------------------- tools
SPEC_ARG = {"description": "the video spec: JSON object, JSON text, or the path of a spec .json file "
                           "(see kadans_schema)", "type": ["object", "string"]}
FOLDER_ARG = {"type": "string", "description": "project folder: relative paths in the spec (clips, photos, logo, "
                                               "fonts/) resolve here and outputs go here (default: the spec's folder)"}

TOOLS = [
    {"name": "kadans_schema", "description":
        f"{NAME} {__version__}: how to write a video. Returns the JSON Schema of the spec and a short guide (scene "
        "types, backgrounds, overlays, 27 blend modes, fonts, captions, music, sound effects, cinematic look). "
        "Call it FIRST, then write a spec and use kadans_lint → kadans_render.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kadans_validate", "description": "Check a spec: every problem as 'path: message' (fix them all), or "
        "the scene count, estimated length and frame size.",
     "inputSchema": {"type": "object", "properties": {"spec": SPEC_ARG, "folder": FOLDER_ARG}, "required": ["spec"]}},
    {"name": "kadans_lint", "description": "Look at every scene like a viewer before rendering: text outside the "
        "safe area, text too long, clipped words, overlaps, overlays covering text, missing images / fonts, voice "
        "longer than its scene. Fix the spec until ok = true.",
     "inputSchema": {"type": "object", "properties": {"spec": SPEC_ARG, "folder": FOLDER_ARG}, "required": ["spec"]}},
    {"name": "kadans_frame", "description": "One frame of the video at time t (seconds), returned as an image so "
        "you can SEE the result (and saved as PNG).",
     "inputSchema": {"type": "object", "properties": {"spec": SPEC_ARG, "folder": FOLDER_ARG,
                                                      "t": {"type": "number"}, "out": {"type": "string"}},
                     "required": ["spec", "t"]}},
    {"name": "kadans_preview", "description": "Write the live preview page (HTML with a time bar: open it in a "
        "browser). Returns its path.",
     "inputSchema": {"type": "object", "properties": {"spec": SPEC_ARG, "folder": FOLDER_ARG, "out": {"type": "string"}},
                     "required": ["spec"]}},
    {"name": "kadans_render", "description": "Render the MP4 (+ .srt) in the BACKGROUND and return a job id at "
        "once; follow it with kadans_status. Finished scenes are cached: re-renders are fast.",
     "inputSchema": {"type": "object", "properties": {"spec": SPEC_ARG, "folder": FOLDER_ARG,
                                                      "out": {"type": "string", "description": "output .mp4"},
                                                      "workers": {"type": "integer"}}, "required": ["spec"]}},
    {"name": "kadans_status", "description": "Progress / result of a kadans_render job. wait = seconds to wait (max "
        "600) until it is finished — use it instead of sleeping.",
     "inputSchema": {"type": "object", "properties": {"job": {"type": "string"}, "wait": {"type": "number"}},
                     "required": ["job"]}},
    {"name": "kadans_fonts", "description": "Fonts installed on this computer (and in the project's fonts/), for "
        "brand.font / font_title / font_code.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "folder": FOLDER_ARG}}},
    {"name": "kadans_media", "description": "Videos and photos in a folder (duration, size, sound) to use in video / "
        "image scenes, backgrounds and overlays.",
     "inputSchema": {"type": "object", "properties": {"folder": {"type": "string"}}, "required": ["folder"]}},
    {"name": "kadans_edit", "description": "Edit a spec IN PLACE, one surgical change (the live timeline editor "
        "reloads when you pass the spec's file PATH). SCENES: add_scene (scene object, optional index) | update_scene "
        "(index + fields) | delete_scene (index) | move_scene (index + to) | duplicate_scene (index). CLIPS on audio "
        "tracks (track = track index, clip = clip index): add_clip (track + clip_obj; mode = overwrite [default, "
        "new clip wins over the overlap] or insert [push later clips right by its dur]) | update_clip (track + clip + "
        "fields; trim = set start/dur/in) | delete_clip (track + clip) | move_clip (track + clip + at = new start, or "
        "to = other track) | split_clip (track + clip + at = absolute seconds) | set_io (track + clip + at = IN point "
        "/ to = OUT point, in source seconds; dur = out - in) | grade (track + clip + grade = {exposure, brightness, "
        "contrast, saturate, vibrance, temperature -100..100, tint -100..100, hue -180..180, lift -0.3..0.3, gamma, "
        "gain, sharpen 0..2, blur, grayscale, sepia, enhance:true} merged into clip.fx; lut = cinema look name; "
        "reset:true clears all grading) | keyframe (track + clip + kf_op: add [at = 0..1 fraction of clip + "
        "fields{x,y,rotate,scale,opacity, ease:'linear|in|out|inout' or [x1,y1,x2,y2]}] / update [index or at] / "
        "delete [index] / clear — anime clip la) | mask (track + clip + mask = {shape: circle|ellipse|inset, "
        "params 0..1}; reset:true clears — koupe clip la an fòm) | speed (track + clip + sr_op: add [at 0..1 + "
        "v = speed multiplier] / delete [index] / clear — speed ramp sou video: vitès kap chanje, slow-mo) | "
        "chroma (track + clip + chroma = {color: green|blue, amount, threshold, smooth}; reset:true clears — "
        "green/blue screen apwoksimatif) | jl_cut (track + clip son + cut: J [lead-in: son kòmanse amount s pi bonè, "
        "bezwen tèt 'in'] / L [tail-out: son kontinye amount s pi lwen] + amount + fade? — crossfade otomatik) | "
        "multicam (track + clip + mc_op: on [ang 1 = clip la] / off / add_angle [angle{src,in?,label?}] / "
        "del_angle [index] / cut [at 0..1 + a = angle index] / del_cut [index] / clear_cuts — plizyè kamera, "
        "chanje ang sou timeline). "
        "SOU-TIT (top-level, pa bezwen track): subtitle st_op: add/update (fields{text,s,e,pos}) / delete (index) / "
        "clear / style (style{size,color,bg,pos}). "
        "MARKERS (timeline repère): add_marker "
        "(at = seconds, fields = {label, color?}) | update_marker (index + fields) | move_marker (index + at) | "
        "delete_marker (index). index may be negative (-1 = last).",
     "inputSchema": {"type": "object", "properties": {
         "spec": SPEC_ARG, "folder": FOLDER_ARG,
         "action": {"type": "string", "enum": ["add_scene", "update_scene", "delete_scene", "move_scene",
                                               "duplicate_scene", "add_clip", "update_clip", "delete_clip",
                                               "move_clip", "split_clip", "set_io", "grade", "keyframe", "mask",
                                               "speed", "chroma", "jl_cut", "multicam", "subtitle", "add_marker",
                                               "update_marker", "move_marker", "delete_marker",
                                               "roll", "slip", "slide", "rate_stretch", "ripple_trim",
                                               "close_gap", "paste_attributes", "track_settings"]},
         "index": {"type": "integer"}, "to": {"type": "integer"},
         "track": {"type": "integer", "description": "audio track index (clip actions)"},
         "clip": {"type": "integer", "description": "clip index within the track"},
         "at": {"type": "number", "description": "seconds: new start (move_clip) or split point (split_clip)"},
         "scene": {"type": "object", "description": "the scene to add (needs a 'type')"},
         "clip_obj": {"type": "object", "description": "the clip to add (start, dur, src/kind…)"},
         "mode": {"type": "string", "enum": ["overwrite", "insert"], "description": "add_clip edit mode"},
         "kf_op": {"type": "string", "enum": ["add", "update", "delete", "clear"],
                   "description": "action=keyframe sub-op (add uses at + fields{x,y,rotate,scale,opacity})"},
         "sr_op": {"type": "string", "enum": ["add", "delete", "clear"],
                   "description": "action=speed sub-op (add uses at 0..1 + v speed multiplier)"},
         "v": {"type": "number", "description": "speed multiplier for action=speed add (0.05..)"},
         "chroma": {"type": "object", "description": "action=chroma: {color: green|blue, amount 0..1, threshold 0..1, "
                    "smooth 0..1, on}; reset:true clears — green/blue screen apwoksimatif"},
         "st_op": {"type": "string", "enum": ["add", "update", "delete", "clear", "style"],
                   "description": "action=subtitle sub-op (add/update use fields{text,s,e,pos}; style uses style{size,color,bg,pos})"},
         "style": {"type": "object", "description": "action=subtitle st_op=style: {size, color, bg, pos}"},
         "cut": {"type": "string", "enum": ["J", "L"], "description": "action=jl_cut: J = lead-in, L = tail-out"},
         "mc_op": {"type": "string", "enum": ["on", "off", "add_angle", "del_angle", "cut", "del_cut", "clear_cuts"],
                   "description": "action=multicam sub-op"},
         "angle": {"type": "object", "description": "action=multicam add_angle: {src, in?, label?}"},
         "a": {"type": "integer", "description": "angle index for action=multicam cut"},
         "amount": {"type": "number", "description": "seconds (action=jl_cut)"},
         "fade": {"type": "number", "description": "crossfade seconds (action=jl_cut, default min(amount,0.4))"},
         "fields": {"type": "object", "description": "fields to merge (update_scene / update_clip)"},
         "grade": {"type": "object", "description": "color-grade params merged into clip.fx (action=grade). "
                   "reset:true clears fx + lut."},
         "lut": {"type": "string", "description": "cinema look name for action=grade (sinema, cho, fret, vintage, "
                 "nwa-blan, sepya, dramatik, pastel, teal-orange)"},
         "mask": {"type": "object", "description": "action=mask: {shape: circle|ellipse|inset, params 0..1 "
                  "(circle: r,cx,cy; ellipse: rx,ry,cx,cy; inset: top,right,bottom,left,radius)}; reset:true clears"},
         "ripple": {"type": "boolean", "description": "delete_clip: shift later clips on the track left to fill the gap"},
         "delta": {"type": "number", "description": "seconds shift (+/-) for roll, slip, slide, rate_stretch"},
         "dur": {"type": "number", "description": "target duration for rate_stretch"},
         "edge": {"type": "string", "enum": ["head", "tail", "left", "right", "start", "end"], "description": "ripple_trim edge (head = Q Top trim, tail = W Tail trim)"},
         "source_track": {"type": "integer", "description": "source track index (paste_attributes)"},
         "source_clip": {"type": "integer", "description": "source clip index (paste_attributes)"},
         "target_track": {"type": "integer", "description": "target track index (paste_attributes)"},
         "target_clip": {"type": "integer", "description": "target clip index (paste_attributes)"},
         "targets": {"type": "array", "description": "list of {track, clip} targets (paste_attributes)"},
         "attributes": {"type": ["array", "object"], "description": "attributes to paste (fx, lut, mask, chroma, volume, keys, speed)"},
         "all": {"type": "boolean", "description": "close all gaps (close_gap)"},
         "sync_lock": {"type": "boolean", "description": "ripple sync-locked tracks during ripple_trim, close_gap, or delete_clip ripple (default true)"}},
                     "required": ["spec", "action"]}},
    {"name": "kadans_doctor", "description": "Check what Kadans needs on this computer (Chromium, FFmpeg, fonts, "
        "memory, one test frame) and the exact fix for anything missing. setup=true downloads the missing Chromium "
        "(pinned) and FFmpeg (LGPL) into Kadans' own folder (~250 MB, ask the person first).",
     "inputSchema": {"type": "object", "properties": {"setup": {"type": "boolean"}}}},
    {"name": "kadans_interchange", "description": "Universal NLE Timeline Interchange: export/import between Kadans and "
        "Adobe Premiere Pro, DaVinci Resolve, Final Cut Pro, Avid (FCP7 XML xmeml v5 and CMX 3600 EDL). "
        "action = 'export' (default) | 'import'. format = 'fcpxml' (default) | 'edl'. out = destination file path.",
     "inputSchema": {"type": "object", "properties": {"spec": SPEC_ARG, "folder": FOLDER_ARG,
                                                      "action": {"type": "string", "enum": ["export", "import"]},
                                                      "format": {"type": "string", "enum": ["fcpxml", "edl"]},
                                                      "out": {"type": "string"}, "content": {"type": "string"}}}},
    {"name": "kadans_loudness", "description": "EBU R128 / ITU-R BS.1770 broadcast audio loudness check (-14 LUFS Social "
        "for YouTube/TikTok/Reels, -23 LUFS Broadcast TV, True Peak max -1.0 dBFS). file = audio path to measure.",
     "inputSchema": {"type": "object", "properties": {"file": {"type": "string"}, "folder": FOLDER_ARG}}},
]

GUIDE = """Write ONE JSON spec. Scenes: hook, logo, text, features, list, stat, code, compare, cta, video (your clip:
in/out, fit, audio, caption), image (photo). Each scene: optional "voice" (narration, appears on the spoken words),
"background" {src, dim, tint, zoom} and "overlays" [{src, blend, layer back|front, x, y, w, anim, color}].
Spec level: ratio (16:9 9:16 1:1 4:5 21:9 1.91:1 4k), brand {name ('WAS*DEV*' = highlighted part), logo, colors,
font, font_title, font_code}, voice {gender, sample}, music {mood upbeat|calm|epic|tech, seed}, captions, sfx,
look {grain, bloom, vignette}, motion_blur, background, overlays, credit. *word* = highlighted word.
Blend modes (27): normal dissolve darken multiply color-burn linear-burn darker-color lighten screen color-dodge
linear-dodge lighter-color overlay soft-light hard-light vivid-light linear-light pin-light hard-mix difference
exclusion subtract divide hue saturation color luminosity.
Flow: kadans_validate → kadans_lint (fix) → kadans_frame (look) → kadans_render → kadans_status."""


def _place_clip(clips: list, co: dict, mode: str) -> int:
    """Mete clip co nan clips selon mode (montaj clip-primè). Retounen endèks li.
    insert = pouse clips ki kòmanse >= start adwat pa dire co; overwrite = co genyen
    sou entèval li a (koupe/separe/jete clips ki chevoche). Menm lojik ak editor.js."""
    try:
        s = float(co.get("start") or 0.0); d = max(0.1, float(co.get("dur") or 2.0))
    except (TypeError, ValueError):
        s, d = 0.0, 2.0
    e = s + d
    if mode == "insert":
        for x in clips:
            try:
                if float(x.get("start") or 0.0) >= s - 1e-6:
                    x["start"] = round(float(x.get("start") or 0.0) + d, 3)
            except (TypeError, ValueError):
                continue
        clips.append(co)
        return clips.index(co)
    kept = []                                            # overwrite
    for x in clips:
        xs = float(x.get("start") or 0.0); xe = xs + float(x.get("dur") or 0.0)
        is_med = x.get("in") is not None
        if xe <= s + 1e-6 or xs >= e - 1e-6:
            kept.append(x); continue
        if xs < s and xe > e:                            # co nan mitan → koupe x an 2
            right = copy.deepcopy(x)
            x["dur"] = round(s - xs, 3)
            right["start"] = round(e, 3); right["dur"] = round(xe - e, 3)
            if is_med:
                right["in"] = round(float(x.get("in") or 0.0) + (e - xs), 3)
            kept.append(x); kept.append(right)
        elif xs < s:
            x["dur"] = round(s - xs, 3); kept.append(x)
        elif xe > e:
            if is_med:
                x["in"] = round(float(x.get("in") or 0.0) + (e - xs), 3)
            x["start"] = round(e, 3); x["dur"] = round(xe - e, 3); kept.append(x)
        # fèmen nèt anndan → jete
    kept.append(co)
    clips[:] = kept
    return clips.index(co)


def _ripple_other_tracks(tracks: list, origin_ti: int, at: float, delta: float):
    """Ripple shift clips on other tracks that have sync_lock enabled and are not locked."""
    for oj, otk in enumerate(tracks):
        if oj == origin_ti:
            continue
        if otk.get("locked"):
            continue
        if otk.get("sync_lock") is False:
            continue
        for oc in otk.get("clips") or []:
            ost = float(oc.get("start") or 0.0)
            if ost >= at - 0.005:
                oc["start"] = round(max(0.0, ost - delta), 3)


def call(name: str, a: dict) -> dict:
    from . import fonts as F
    from . import lint as L
    from . import media as M
    from .compose import build_html
    from .renderer import frame
    from .spec import SpecError, json_schema, timeline, total, validate
    try:
        if name == "kadans_schema":
            return _text(GUIDE + "\n\nJSON Schema:\n" + json.dumps(json_schema(), ensure_ascii=False))
        if name == "kadans_fonts":
            extra = [Path(a["folder"]) / "fonts"] if a.get("folder") else []
            fams = F.families(extra, str(a.get("query") or ""))
            return _text(f"{len(fams)} font families\n" + "\n".join(
                f"- {f['family']} ({', '.join(f['styles'][:6])})" for f in fams[:400]))
        if name == "kadans_doctor":
            from . import deps as S
            log = []
            if a.get("setup"):
                S.setup(say=log.append)
            rows = S.doctor()
            return _text("\n".join(log + [S.report(rows)]), error=not all(r["ok"] for r in rows))
        if name == "kadans_media":
            rows = M.list_media(Path(a["folder"]).expanduser())
            return _text(json.dumps(rows, ensure_ascii=False, indent=1) if rows else "no video / photo in that folder")
        if name == "kadans_status":
            t_end = time.time() + max(0.0, min(600.0, float(a.get("wait") or 0)))
            while (_JOBS.get(str(a.get("job"))) or {}).get("state") == "running" and time.time() < t_end:
                time.sleep(1.0)
            j = _JOBS.get(str(a.get("job")))
            return _text(json.dumps(j, ensure_ascii=False, default=str) if j else "unknown job", error=not j)
        if name == "kadans_edit":
            import copy
            act, raw = str(a.get("action") or ""), a.get("spec")
            path = None
            if isinstance(raw, str) and not raw.strip().startswith("{"):
                path = Path(raw).expanduser()
                spec = json.loads(path.read_text(encoding="utf-8"))
            elif isinstance(raw, str):
                spec = json.loads(raw)
            elif isinstance(raw, dict):
                spec = copy.deepcopy(raw)
            else:
                return _text("spec: a spec .json PATH (to edit live) or a JSON object", error=True)
            scenes = list(spec.get("scenes") or [])
            n = len(scenes)

            def _i(x):
                i = int(x)
                return i if i >= 0 else n + i

            def _i2(x, length):
                i = int(x)
                return i if i >= 0 else length + i
            if act in ("add_marker", "update_marker", "move_marker", "delete_marker"):
                marks = spec.get("markers") or []
                try:
                    if act == "add_marker":
                        mk = {"t": round(float(a.get("at") or 0.0), 3)}
                        fld = a.get("fields") or {}
                        for k in ("label", "color", "comment"):
                            if k in fld:
                                mk[k] = str(fld[k])
                        dur = fld.get("dur") if fld.get("dur") is not None else fld.get("duration")
                        if dur is not None:
                            mk["dur"] = round(max(0.0, float(dur)), 3)
                        if fld.get("chapter") not in (None, "", False):
                            mk["chapter"] = True if fld.get("chapter") is True else str(fld.get("chapter"))
                        marks.append(mk)
                    else:
                        mi = int(a.get("index"))
                        mi = mi if mi >= 0 else len(marks) + mi
                        if not (0 <= mi < len(marks)):
                            return _text(f"marker {a.get('index')} out of range (0..{len(marks) - 1})", error=True)
                        if act == "update_marker":
                            fld = a.get("fields") or {}
                            for k in ("label", "color", "comment"):
                                if k in fld:
                                    marks[mi][k] = str(fld[k])
                            if "t" in fld:
                                marks[mi]["t"] = round(float(fld["t"]), 3)
                            dur = fld.get("dur") if fld.get("dur") is not None else fld.get("duration")
                            if dur is not None:
                                marks[mi]["dur"] = round(max(0.0, float(dur)), 3)
                            if "chapter" in fld:
                                if fld["chapter"] in (None, "", False):
                                    marks[mi].pop("chapter", None)
                                else:
                                    marks[mi]["chapter"] = True if fld["chapter"] is True else str(fld["chapter"])
                        elif act == "move_marker":
                            marks[mi]["t"] = round(float(a.get("at") or 0.0), 3)
                        elif act == "delete_marker":
                            marks.pop(mi)
                except (ValueError, TypeError) as e:
                    return _text(f"bad index / at: {e}", error=True)
                marks.sort(key=lambda m: m.get("t", 0))
                spec["markers"] = marks
                if path is not None:
                    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
                elif isinstance(raw, dict):
                    raw.clear(); raw.update(spec)
                where = f" · saved to {path} (live editor reloads)" if path else " · pass a file PATH to edit in place"
                return _text(f"ok: {act} → {len(marks)} markers{where}\n" + json.dumps(marks, ensure_ascii=False))
            if act == "subtitle":                            # editè sou-tit (sub_cues eksplisit + stil)
                sop = str(a.get("st_op") or "add").lower()
                cues = spec.get("sub_cues") if isinstance(spec.get("sub_cues"), list) else []
                fld = a.get("fields") or {}
                try:
                    if sop == "clear":
                        spec.pop("sub_cues", None)
                        cues = []
                    elif sop == "style":
                        stl = dict(spec.get("sub_style") or {})
                        for k2, v2 in (a.get("style") or {}).items():
                            if k2 in ("color", "bg", "pos"):
                                stl[k2] = str(v2)
                            elif k2 == "size":
                                stl["size"] = float(v2)
                        spec["sub_style"] = stl
                    elif sop == "delete":
                        si = _i2(a["index"], len(cues))
                        if not (0 <= si < len(cues)):
                            return _text(f"subtitle {a.get('index')} out of range (0..{len(cues) - 1})", error=True)
                        cues.pop(si); spec["sub_cues"] = cues
                    elif sop in ("add", "update"):
                        if sop == "update":
                            si = _i2(a["index"], len(cues))
                            if not (0 <= si < len(cues)):
                                return _text(f"subtitle {a.get('index')} out of range", error=True)
                            cue = cues[si]
                        else:
                            if not str(fld.get("text") or "").strip():
                                return _text("subtitle add: fields.text required", error=True)
                            cue = {"s": 0.0, "e": 2.0, "text": ""}
                            cues.append(cue)
                        if fld.get("text") is not None:
                            cue["text"] = str(fld["text"])
                        if fld.get("s") is not None:
                            cue["s"] = round(max(0.0, float(fld["s"])), 3)
                        if fld.get("e") is not None:
                            cue["e"] = round(float(fld["e"]), 3)
                        if cue["e"] <= cue["s"]:
                            cue["e"] = round(cue["s"] + 1.5, 3)
                        if fld.get("pos") in ("bottom", "top", "middle"):
                            cue["pos"] = fld["pos"]
                        cues.sort(key=lambda z: z.get("s", 0)); spec["sub_cues"] = cues
                    else:
                        return _text(f"subtitle: unknown st_op '{sop}' (add/update/delete/clear/style)", error=True)
                except (ValueError, TypeError) as e:
                    return _text(f"subtitle: bad field/index: {e}", error=True)
                if path is not None:
                    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
                elif isinstance(raw, dict):
                    raw.clear(); raw.update(spec)
                where = f" · saved to {path} (live editor reloads)" if path else " · pass a file PATH to edit in place"
                return _text(f"ok: subtitle {sop} → {len(cues)} sou-tit{where}\n" + json.dumps(cues, ensure_ascii=False))
            if act in ("add_clip", "update_clip", "delete_clip", "move_clip", "split_clip", "set_io", "grade", "keyframe", "mask", "speed", "chroma", "jl_cut", "multicam",
                       "roll", "slip", "slide", "rate_stretch", "ripple_trim", "close_gap", "paste_attributes", "track_settings"):
                tracks = spec.get("tracks") or []
                try:
                    raw_ti = a.get("track") if a.get("track") is not None else (a.get("target_track") if a.get("target_track") is not None else a.get("source_track"))
                    if raw_ti is None:
                        return _text("track index required for clip actions", error=True)
                    ti = int(raw_ti)
                    ti = ti if ti >= 0 else len(tracks) + ti
                except (TypeError, ValueError):
                    return _text("track index required for clip actions", error=True)
                if not (0 <= ti < len(tracks)):
                    return _text(f"track {a.get('track')} out of range (0..{len(tracks) - 1})", error=True)

                if act == "track_settings":
                    tk = tracks[ti]
                    fld = a.get("fields") or {}
                    for k2, v2 in fld.items():
                        if k2 in ("locked", "sync_lock", "targeted", "solo", "muted"):
                            tk[k2] = bool(v2)
                        elif k2 == "volume":
                            tk[k2] = max(0.0, min(1.0, float(v2)))
                        elif k2 in ("name", "color", "kind"):
                            tk[k2] = str(v2)
                    spec["tracks"] = tracks
                    if path is not None:
                        path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
                    elif isinstance(raw, dict):
                        raw.clear(); raw.update(spec)
                    where = f" · saved to {path} (live editor reloads)" if path else " · pass a file PATH to edit in place"
                    return _text(f"ok: track_settings → track {ti} updated{where}\n" + json.dumps(tk, ensure_ascii=False))

                if tracks[ti].get("locked") and act not in ("paste_attributes",):
                    return _text(f"track {ti} is locked: unlock before editing", error=True)

                clips = tracks[ti].setdefault("clips", [])
                m = len(clips)
                try:
                    if act == "add_clip":
                        co = a.get("clip_obj") or {}
                        if not isinstance(co, dict):
                            return _text("add_clip: a 'clip_obj' object is required", error=True)
                        co.setdefault("start", float(a.get("at") or 0.0))
                        co.setdefault("dur", 2.0)
                        mode = str(a.get("mode") or "overwrite").lower()
                        _place_clip(clips, co, mode)
                    elif act == "close_gap":
                        if not clips:
                            return _text(f"close_gap: no clips on track {ti}", error=True)
                        clips_sorted = sorted(clips, key=lambda x: float(x.get("start") or 0.0))
                        if a.get("all"):
                            prev_end = 0.0
                            for k_idx, cl in enumerate(clips_sorted):
                                st = float(cl.get("start") or 0.0)
                                if st > prev_end + 0.01:
                                    gap = round(st - prev_end, 3)
                                    for shift_cl in clips_sorted[k_idx:]:
                                        shift_cl["start"] = round(max(0.0, float(shift_cl.get("start") or 0.0) - gap), 3)
                                    if a.get("sync_lock", True):
                                        _ripple_other_tracks(tracks, ti, st, gap)
                                    st = prev_end
                                prev_end = round(st + float(cl.get("dur") or 0.0), 3)
                        elif a.get("at") is not None:
                            at = float(a["at"])
                            found = False
                            prev_end = 0.0
                            for k_idx, cl in enumerate(clips_sorted):
                                st = float(cl.get("start") or 0.0)
                                if prev_end <= at < st:
                                    gap = round(st - prev_end, 3)
                                    for shift_cl in clips_sorted[k_idx:]:
                                        shift_cl["start"] = round(max(0.0, float(shift_cl.get("start") or 0.0) - gap), 3)
                                    if a.get("sync_lock", True):
                                        _ripple_other_tracks(tracks, ti, st, gap)
                                    found = True
                                    break
                                prev_end = round(st + float(cl.get("dur") or 0.0), 3)
                            if not found:
                                return _text(f"close_gap: no gap found at {at:g}s on track {ti}", error=True)
                        elif a.get("clip") is not None:
                            target_ci = int(a["clip"])
                            target_ci = target_ci if target_ci >= 0 else m + target_ci
                            if not (0 <= target_ci < m):
                                return _text(f"clip {a.get('clip')} out of range (0..{m - 1})", error=True)
                            target_cl = clips[target_ci]
                            st = float(target_cl.get("start") or 0.0)
                            prev_end = 0.0
                            for other in clips:
                                if other is not target_cl and float(other.get("start") or 0.0) < st:
                                    oe = float(other.get("start") or 0.0) + float(other.get("dur") or 0.0)
                                    if oe > prev_end:
                                        prev_end = oe
                            gap = round(st - prev_end, 3)
                            if gap > 0.01:
                                for cl in clips:
                                    if float(cl.get("start") or 0.0) >= st - 0.001:
                                        cl["start"] = round(max(0.0, float(cl.get("start") or 0.0) - gap), 3)
                                if a.get("sync_lock", True):
                                    _ripple_other_tracks(tracks, ti, st, gap)
                        else:
                            return _text("close_gap: specify 'at', 'clip', or all=True", error=True)
                    elif act == "paste_attributes":
                        sti = a.get("source_track") if a.get("source_track") is not None else a.get("src_track")
                        sci = a.get("source_clip") if a.get("source_clip") is not None else a.get("src_clip")
                        if sti is None or sci is None:
                            return _text("paste_attributes: 'source_track' and 'source_clip' required", error=True)
                        sti = int(sti); sti = sti if sti >= 0 else len(tracks) + sti
                        if not (0 <= sti < len(tracks)):
                            return _text(f"source_track {sti} out of range", error=True)
                        s_clips = tracks[sti].get("clips") or []
                        sci = int(sci); sci = sci if sci >= 0 else len(s_clips) + sci
                        if not (0 <= sci < len(s_clips)):
                            return _text(f"source_clip {sci} out of range", error=True)
                        s_clip = s_clips[sci]

                        raw_targets = a.get("targets")
                        if not raw_targets:
                            tti = a.get("target_track") if a.get("target_track") is not None else a.get("track", ti)
                            tci = a.get("target_clip") if a.get("target_clip") is not None else a.get("clip", 0)
                            raw_targets = [{"track": tti, "clip": tci}]

                        attr_arg = a.get("attributes") or ["fx", "lut", "mask", "chroma", "volume", "keys", "speed"]
                        attrs = set(attr_arg if isinstance(attr_arg, (list, tuple)) else [k for k, v in attr_arg.items() if v])

                        for tg in raw_targets:
                            t_ti = int(tg.get("track") if tg.get("track") is not None else ti)
                            t_ti = t_ti if t_ti >= 0 else len(tracks) + t_ti
                            if not (0 <= t_ti < len(tracks)):
                                continue
                            t_tk = tracks[t_ti]
                            if t_tk.get("locked"):
                                continue
                            t_clips = t_tk.get("clips") or []
                            t_ci = int(tg.get("clip") if tg.get("clip") is not None else 0)
                            t_ci = t_ci if t_ci >= 0 else len(t_clips) + t_ci
                            if not (0 <= t_ci < len(t_clips)):
                                continue
                            tc = t_clips[t_ci]

                            if ("fx" in attrs or "grade" in attrs) and "fx" in s_clip:
                                tc["fx"] = copy.deepcopy(s_clip["fx"])
                            if "lut" in attrs and "lut" in s_clip:
                                tc["lut"] = s_clip["lut"]
                            if "mask" in attrs and "mask" in s_clip:
                                tc["mask"] = copy.deepcopy(s_clip["mask"])
                            if "chroma" in attrs and "chroma" in s_clip:
                                tc["chroma"] = copy.deepcopy(s_clip["chroma"])
                            if "volume" in attrs:
                                for vk in ("volume", "fadein", "fadeout"):
                                    if vk in s_clip: tc[vk] = s_clip[vk]
                            if ("keys" in attrs or "keyframe" in attrs) and "keys" in s_clip:
                                tc["keys"] = copy.deepcopy(s_clip["keys"])
                            if "speed" in attrs and "speed" in s_clip:
                                tc["speed"] = s_clip["speed"]
                                if "speedKeys" in s_clip:
                                    tc["speedKeys"] = copy.deepcopy(s_clip["speedKeys"])
                    elif act == "ripple_trim" and a.get("clip") is None:
                        if a.get("at") is None:
                            return _text("ripple_trim: 'at' (seconds) required", error=True)
                        at = float(a["at"])
                        edge = str(a.get("edge") or "head").lower()
                        target_ci = None
                        for k_idx, cl in enumerate(clips):
                            st_k = float(cl.get("start") or 0.0)
                            dur_k = float(cl.get("dur") or 0.0)
                            if st_k <= at <= st_k + dur_k:
                                target_ci = k_idx
                                break
                        if target_ci is None:
                            return _text(f"ripple_trim: no clip found on track {ti} at {at:g}s", error=True)
                        c = clips[target_ci]
                        st_c = float(c.get("start") or 0.0)
                        dur_c = float(c.get("dur") or 0.0)
                        if edge in ("head", "left", "top", "start"):
                            delta = round(at - st_c, 3)
                            if delta <= 0.01 or delta >= dur_c - 0.01:
                                return _text(f"ripple_trim head: 'at' {at:g} must be strictly inside clip ({st_c:g}..{st_c + dur_c:g})", error=True)
                            c["dur"] = round(dur_c - delta, 3)
                            if "in" in c:
                                sp_c = float(c.get("speed") or 1.0)
                                c["in"] = round(max(0.0, float(c.get("in") or 0.0) + delta * sp_c), 3)
                            for cc in clips:
                                if float(cc.get("start") or 0.0) >= st_c + dur_c - 0.01:
                                    cc["start"] = round(max(0.0, float(cc.get("start") or 0.0) - delta), 3)
                            if a.get("sync_lock", True):
                                _ripple_other_tracks(tracks, ti, at, delta)
                        elif edge in ("tail", "right", "end"):
                            delta = round((st_c + dur_c) - at, 3)
                            if delta <= 0.01 or delta >= dur_c - 0.01:
                                return _text(f"ripple_trim tail: 'at' {at:g} must be strictly inside clip ({st_c:g}..{st_c + dur_c:g})", error=True)
                            c["dur"] = round(at - st_c, 3)
                            for cc in clips:
                                if float(cc.get("start") or 0.0) >= st_c + dur_c - 0.01:
                                    cc["start"] = round(max(0.0, float(cc.get("start") or 0.0) - delta), 3)
                            if a.get("sync_lock", True):
                                _ripple_other_tracks(tracks, ti, st_c + dur_c, delta)
                        else:
                            return _text(f"ripple_trim: unknown edge '{edge}' (head/tail)", error=True)
                    else:
                        ci = int(a.get("clip"))
                        ci = ci if ci >= 0 else m + ci
                        if not (0 <= ci < m):
                            return _text(f"clip {a.get('clip')} out of range (0..{m - 1})", error=True)
                        if act == "update_clip":
                            clips[ci] = {**clips[ci], **(a.get("fields") or {})}
                        elif act == "delete_clip":
                            gone = clips.pop(ci)
                            if a.get("ripple"):                      # bouche twou a: deplase clip ki apre yo agoch
                                gs, gd = float(gone.get("start") or 0.0), float(gone.get("dur") or 0.0)
                                for cc in clips:
                                    if float(cc.get("start") or 0.0) >= gs:
                                        cc["start"] = round(max(0.0, float(cc.get("start") or 0.0) - gd), 3)
                                if a.get("sync_lock", True):
                                    _ripple_other_tracks(tracks, ti, gs, gd)
                        elif act == "move_clip":
                            if a.get("to") is not None:                  # deplase sou yon LÒT track
                                tj = int(a["to"])
                                tj = tj if tj >= 0 else len(tracks) + tj
                                if not (0 <= tj < len(tracks)):
                                    return _text(f"to-track {a.get('to')} out of range", error=True)
                                c = clips.pop(ci)
                                if a.get("at") is not None:
                                    c["start"] = float(a["at"])
                                tracks[tj].setdefault("clips", []).append(c)
                            else:
                                clips[ci]["start"] = float(a.get("at") or 0.0)
                        elif act == "split_clip":
                            c = clips[ci]
                            s0, d0, at = float(c.get("start") or 0.0), float(c.get("dur") or 2.0), float(a.get("at"))
                            if not (s0 < at < s0 + d0):
                                return _text(f"split 'at' must be inside the clip ({s0:g}..{s0 + d0:g})", error=True)
                            c2 = copy.deepcopy(c)
                            c["dur"] = round(at - s0, 3)
                            c2["start"], c2["dur"] = round(at, 3), round(s0 + d0 - at, 3)
                            if "in" in c2:                               # medya: dekale pwen antre a
                                c2["in"] = round(float(c2.get("in") or 0.0) + (at - s0), 3)
                            clips.insert(ci + 1, c2)
                        elif act == "set_io":                            # pwen IN/OUT (trim sous la): dur = out - in
                            c = clips[ci]
                            if a.get("at") is None:
                                return _text("set_io: 'at' (IN point, source seconds) required", error=True)
                            inp = max(0.0, float(a["at"]))
                            c["in"] = round(inp, 3)
                            if a.get("to") is not None:
                                out = float(a["to"])
                                if out <= inp:
                                    return _text(f"set_io: 'to' (OUT {out:g}) must be greater than 'at' (IN {inp:g})",
                                                 error=True)
                                c["dur"] = round(out - inp, 3)
                        elif act == "keyframe":                          # animasyon clip (x/y/rotate/scale/opacity)
                            c = clips[ci]
                            op2 = str(a.get("kf_op") or "add").lower()
                            keys = c.get("keys") if isinstance(c.get("keys"), list) else []
                            if op2 == "clear":
                                c.pop("keys", None)
                            elif op2 == "delete":
                                ki = _i(a["index"]) if a.get("index") is not None else None
                                if ki is None:
                                    return _text("keyframe delete: 'index' required", error=True)
                                ki = ki if ki >= 0 else len(keys) + ki
                                if not (0 <= ki < len(keys)):
                                    return _text(f"keyframe {a.get('index')} out of range (0..{len(keys) - 1})", error=True)
                                keys.pop(ki); c["keys"] = keys
                            elif op2 in ("add", "update"):
                                fld = a.get("fields") or {}
                                allowed = ("x", "y", "rotate", "scale", "opacity")
                                kf = {}
                                for kk in allowed:
                                    if fld.get(kk) is not None:
                                        try:
                                            kf[kk] = float(fld[kk])
                                        except (TypeError, ValueError):
                                            return _text(f"keyframe: '{kk}' must be a number", error=True)
                                ez = fld.get("ease")      # ease/bezye: "linear|in|out|inout" oswa [x1,y1,x2,y2]
                                if isinstance(ez, (list, tuple)) and len(ez) == 4:
                                    kf["ease"] = [float(v) for v in ez]
                                elif isinstance(ez, str) and ez:
                                    kf["ease"] = ez
                                if op2 == "update" and a.get("index") is not None:
                                    ki = _i(a["index"]); ki = ki if ki >= 0 else len(keys) + ki
                                    if not (0 <= ki < len(keys)):
                                        return _text(f"keyframe {a.get('index')} out of range", error=True)
                                    if a.get("at") is not None:
                                        keys[ki]["t"] = max(0.0, min(1.0, float(a["at"])))
                                    keys[ki].update(kf)
                                else:
                                    if a.get("at") is None:
                                        return _text("keyframe add: 'at' (0..1 fraction of clip) required", error=True)
                                    if not kf:
                                        return _text("keyframe add: 'fields' needs at least one of x/y/rotate/scale/opacity", error=True)
                                    keys.append({"t": max(0.0, min(1.0, float(a["at"]))), **kf})
                                keys.sort(key=lambda z: z.get("t", 0))
                                c["keys"] = keys
                            else:
                                return _text(f"keyframe: unknown kf_op '{op2}' (add/update/delete/clear)", error=True)
                        elif act == "speed":                             # speed ramp (pwen vitès)
                            c = clips[ci]
                            sop = str(a.get("sr_op") or "add").lower()
                            sk = c.get("speedKeys") if isinstance(c.get("speedKeys"), list) else []
                            if sop == "clear":
                                c.pop("speedKeys", None)
                            elif sop == "delete":
                                ki = _i(a["index"]) if a.get("index") is not None else None
                                if ki is None:
                                    return _text("speed delete: 'index' required", error=True)
                                ki = ki if ki >= 0 else len(sk) + ki
                                if not (0 <= ki < len(sk)):
                                    return _text(f"speed {a.get('index')} out of range (0..{len(sk) - 1})", error=True)
                                sk.pop(ki); c["speedKeys"] = sk
                            elif sop == "add":
                                if a.get("at") is None or a.get("v") is None:
                                    return _text("speed add: 'at' (0..1) and 'v' (speed) required", error=True)
                                sk.append({"t": max(0.0, min(1.0, float(a["at"]))), "v": max(0.05, float(a["v"]))})
                                sk.sort(key=lambda z: z.get("t", 0)); c["speedKeys"] = sk
                            else:
                                return _text(f"speed: unknown sr_op '{sop}' (add/delete/clear)", error=True)
                        elif act == "multicam":                          # plizyè kamera + koup sou timeline
                            c = clips[ci]
                            mop = str(a.get("mc_op") or "").lower()
                            if mop == "on":
                                if not isinstance(c.get("angles"), list) or not c["angles"]:
                                    ang0 = {"src": c.get("src"), "label": "Ang 1"}
                                    if c.get("in") is not None:
                                        ang0["in"] = float(c.get("in") or 0)
                                    c["angles"] = [ang0] if c.get("src") else []
                                c.setdefault("cuts", [])
                            elif mop == "off":
                                c.pop("angles", None); c.pop("cuts", None)
                            elif mop == "add_angle":
                                ang = a.get("angle") or {}
                                if not isinstance(ang, dict) or not ang.get("src"):
                                    return _text("multicam add_angle: angle{src} required", error=True)
                                angs = c.get("angles") if isinstance(c.get("angles"), list) else []
                                na = {"src": str(ang["src"])}
                                if ang.get("label"):
                                    na["label"] = str(ang["label"])
                                if ang.get("in") is not None:
                                    na["in"] = float(ang["in"])
                                angs.append(na); c["angles"] = angs
                            elif mop == "del_angle":
                                angs = c.get("angles") or []
                                ki = _i2(a["index"], len(angs)) if a.get("index") is not None else None
                                if ki is None or not (0 <= ki < len(angs)):
                                    return _text("multicam del_angle: valid 'index' required", error=True)
                                angs.pop(ki); c["angles"] = angs
                            elif mop == "cut":
                                if a.get("at") is None or a.get("a") is None:
                                    return _text("multicam cut: 'at' (0..1) and 'a' (angle index) required", error=True)
                                cuts = c.get("cuts") if isinstance(c.get("cuts"), list) else []
                                cuts.append({"t": max(0.0, min(1.0, float(a["at"]))), "a": max(0, int(a["a"]))})
                                cuts.sort(key=lambda z: z.get("t", 0)); c["cuts"] = cuts
                            elif mop == "del_cut":
                                cuts = c.get("cuts") or []
                                ki = _i2(a["index"], len(cuts)) if a.get("index") is not None else None
                                if ki is None or not (0 <= ki < len(cuts)):
                                    return _text("multicam del_cut: valid 'index' required", error=True)
                                cuts.pop(ki); c["cuts"] = cuts
                            elif mop == "clear_cuts":
                                c["cuts"] = []
                            else:
                                return _text(f"multicam: unknown mc_op '{mop}' (on/off/add_angle/del_angle/cut/del_cut/clear_cuts)", error=True)
                        elif act == "jl_cut":                            # J/L-cut sou clip son (lead-in / tail-out)
                            c = clips[ci]
                            cut = str(a.get("cut") or "").upper()
                            if cut not in ("J", "L"):
                                return _text("jl_cut: 'cut' must be 'J' (lead-in) or 'L' (tail-out)", error=True)
                            try:
                                amt = float(a.get("amount"))
                            except (TypeError, ValueError):
                                return _text("jl_cut: 'amount' (seconds) required", error=True)
                            if amt <= 0:
                                return _text("jl_cut: 'amount' must be > 0", error=True)
                            try:
                                fade = float(a["fade"]) if a.get("fade") is not None else min(amt, 0.4)
                            except (TypeError, ValueError):
                                fade = min(amt, 0.4)
                            fade = max(0.0, min(fade, amt))
                            start = float(c.get("start") or 0.0); dur = float(c.get("dur") or 0.0)
                            inn = float(c.get("in") or 0.0)
                            if cut == "J":                               # son kòmanse pi bonè (bezwen tèt sous)
                                lead = min(amt, start, inn)
                                if lead <= 0:
                                    return _text("jl_cut J: pa gen tèt disponib (trim 'in' clip la oswa deplase l adwat anvan)", error=True)
                                c["start"] = round(start - lead, 3)
                                c["dur"] = round(dur + lead, 3)
                                c["in"] = round(inn - lead, 3)
                                c["fadein"] = round(max(float(c.get("fadein") or 0.0), min(fade, lead)), 3)
                            else:                                        # L: son kontinye pi lwen
                                c["dur"] = round(dur + amt, 3)
                                c["fadeout"] = round(max(float(c.get("fadeout") or 0.0), min(fade, amt)), 3)
                        elif act == "chroma":                            # chroma key (green/blue screen)
                            c = clips[ci]
                            ch = a.get("chroma") or {}
                            if not isinstance(ch, dict):
                                return _text("chroma: 'chroma' must be an object", error=True)
                            if ch.get("reset"):
                                c.pop("chroma", None)
                            else:
                                cur = dict(c.get("chroma") or {})
                                for k2, v2 in ch.items():
                                    if k2 == "reset":
                                        continue
                                    if k2 == "color":
                                        cur["color"] = str(v2)
                                    elif k2 == "on":
                                        cur["on"] = bool(v2)
                                    else:
                                        try:
                                            cur[k2] = float(v2)
                                        except (TypeError, ValueError):
                                            return _text(f"chroma: '{k2}' must be a number", error=True)
                                if cur:
                                    c["chroma"] = cur
                                else:
                                    c.pop("chroma", None)
                        elif act == "mask":                              # mask fòm (clip-path)
                            c = clips[ci]
                            mk = a.get("mask") or {}
                            if not isinstance(mk, dict):
                                return _text("mask: 'mask' must be an object", error=True)
                            if mk.get("reset"):
                                c.pop("mask", None)
                            else:
                                cur = dict(c.get("mask") or {})
                                for k2, v2 in mk.items():
                                    if k2 == "reset":
                                        continue
                                    if k2 == "shape":
                                        cur["shape"] = str(v2)
                                    else:
                                        try:
                                            cur[k2] = float(v2)
                                        except (TypeError, ValueError):
                                            return _text(f"mask: '{k2}' must be a number", error=True)
                                if cur:
                                    c["mask"] = cur
                                else:
                                    c.pop("mask", None)
                        elif act == "grade":                             # etalonaj koulè (fx + lut)
                            c = clips[ci]
                            g = a.get("grade") or {}
                            lut = a.get("lut")
                            if not isinstance(g, dict):
                                return _text("grade: 'grade' must be an object of params", error=True)
                            if g.get("reset") or (lut == "" and not g):
                                c.pop("fx", None); c.pop("lut", None)
                            else:
                                fxd = dict(c.get("fx") or {})
                                for k2, v2 in g.items():
                                    if k2 == "reset":
                                        continue
                                    if k2 == "enhance":
                                        if v2:
                                            fxd["enhance"] = True
                                        else:
                                            fxd.pop("enhance", None)
                                    elif k2 == "curves":
                                        if isinstance(v2, dict):
                                            fxd["curves"] = v2
                                        else:
                                            fxd.pop("curves", None)
                                    elif k2 in ("tonemap", "hdr_tonemap"):
                                        if v2:
                                            fxd[k2] = str(v2)
                                        else:
                                            fxd.pop(k2, None)
                                    elif k2 in ("motion_blur", "blur_dir"):
                                        if isinstance(v2, (int, float, list)):
                                            fxd[k2] = v2
                                        else:
                                            fxd.pop(k2, None)
                                    else:
                                        try:
                                            fxd[k2] = float(v2)
                                        except (TypeError, ValueError):
                                            return _text(f"grade: '{k2}' must be a number", error=True)
                                if fxd:
                                    c["fx"] = fxd
                                else:
                                    c.pop("fx", None)
                                if lut:
                                    c["lut"] = lut
                                elif lut == "":
                                    c.pop("lut", None)
                        elif act == "roll":
                            if ci >= m - 1:
                                return _text(f"roll: clip {ci} must have an adjacent subsequent clip on track {ti}", error=True)
                            try:
                                delta = float(a.get("delta"))
                            except (TypeError, ValueError):
                                return _text("roll: 'delta' (seconds) required", error=True)
                            ca, cb = clips[ci], clips[ci + 1]
                            dur_a = float(ca.get("dur") or 0.0)
                            dur_b = float(cb.get("dur") or 0.0)
                            start_b = float(cb.get("start") or 0.0)
                            if dur_a + delta < 0.05:
                                return _text(f"roll: delta {delta:g} exceeds clip {ci} duration ({dur_a:g})", error=True)
                            if dur_b - delta < 0.05:
                                return _text(f"roll: delta {delta:g} exceeds subsequent clip duration ({dur_b:g})", error=True)
                            ca["dur"] = round(dur_a + delta, 3)
                            cb["start"] = round(start_b + delta, 3)
                            cb["dur"] = round(dur_b - delta, 3)
                            if "in" in cb:
                                sp_b = float(cb.get("speed") or 1.0)
                                cb["in"] = round(max(0.0, float(cb.get("in") or 0.0) + delta * sp_b), 3)
                        elif act == "slip":
                            try:
                                delta = float(a.get("delta"))
                            except (TypeError, ValueError):
                                return _text("slip: 'delta' (seconds) required", error=True)
                            c = clips[ci]
                            cur_in = float(c.get("in") or 0.0)
                            c["in"] = round(max(0.0, cur_in + delta), 3)
                            if c.get("out") is not None:
                                c["out"] = round(max(0.0, float(c["out"]) + delta), 3)
                        elif act == "slide":
                            if ci <= 0 or ci >= m - 1:
                                return _text(f"slide: clip {ci} must be between two adjacent clips (index 1..{m - 2})", error=True)
                            try:
                                delta = float(a.get("delta"))
                            except (TypeError, ValueError):
                                return _text("slide: 'delta' (seconds) required", error=True)
                            c_prev, c_curr, c_next = clips[ci - 1], clips[ci], clips[ci + 1]
                            dur_prev = float(c_prev.get("dur") or 0.0)
                            dur_next = float(c_next.get("dur") or 0.0)
                            if dur_prev + delta < 0.05:
                                return _text(f"slide: delta {delta:g} exceeds previous clip duration ({dur_prev:g})", error=True)
                            if dur_next - delta < 0.05:
                                return _text(f"slide: delta {delta:g} exceeds next clip duration ({dur_next:g})", error=True)
                            c_prev["dur"] = round(dur_prev + delta, 3)
                            c_curr["start"] = round(float(c_curr.get("start") or 0.0) + delta, 3)
                            c_next["start"] = round(float(c_next.get("start") or 0.0) + delta, 3)
                            c_next["dur"] = round(dur_next - delta, 3)
                            if "in" in c_next:
                                sp_next = float(c_next.get("speed") or 1.0)
                                c_next["in"] = round(max(0.0, float(c_next.get("in") or 0.0) + delta * sp_next), 3)
                        elif act == "rate_stretch":
                            c = clips[ci]
                            old_dur = float(c.get("dur") or 2.0)
                            if a.get("dur") is not None:
                                new_dur = float(a["dur"])
                            elif a.get("delta") is not None:
                                new_dur = old_dur + float(a["delta"])
                            else:
                                return _text("rate_stretch: 'dur' or 'delta' required", error=True)
                            if new_dur < 0.05:
                                return _text(f"rate_stretch: new duration {new_dur:g} must be >= 0.05s", error=True)
                            old_speed = float(c.get("speed") or 1.0)
                            new_speed = round(old_speed * (old_dur / new_dur), 4)
                            c["dur"] = round(new_dur, 3)
                            c["speed"] = new_speed
                            if a.get("ripple"):
                                diff = round(new_dur - old_dur, 3)
                                old_end = float(c.get("start") or 0.0) + old_dur
                                for cc in clips:
                                    if cc is not c and float(cc.get("start") or 0.0) >= old_end - 0.01:
                                        cc["start"] = round(max(0.0, float(cc.get("start") or 0.0) + diff), 3)
                                if a.get("sync_lock", True):
                                    _ripple_other_tracks(tracks, ti, old_end, -diff)
                        elif act == "ripple_trim":
                            if a.get("at") is None:
                                return _text("ripple_trim: 'at' (seconds) required", error=True)
                            at = float(a["at"])
                            edge = str(a.get("edge") or "head").lower()
                            c = clips[ci]
                            st_c = float(c.get("start") or 0.0)
                            dur_c = float(c.get("dur") or 0.0)
                            if edge in ("head", "left", "top", "start"):
                                delta = round(at - st_c, 3)
                                if delta <= 0.01 or delta >= dur_c - 0.01:
                                    return _text(f"ripple_trim head: 'at' {at:g} must be strictly inside clip ({st_c:g}..{st_c + dur_c:g})", error=True)
                                c["dur"] = round(dur_c - delta, 3)
                                if "in" in c:
                                    sp_c = float(c.get("speed") or 1.0)
                                    c["in"] = round(max(0.0, float(c.get("in") or 0.0) + delta * sp_c), 3)
                                for cc in clips:
                                    if float(cc.get("start") or 0.0) >= st_c + dur_c - 0.01:
                                        cc["start"] = round(max(0.0, float(cc.get("start") or 0.0) - delta), 3)
                                if a.get("sync_lock", True):
                                    _ripple_other_tracks(tracks, ti, at, delta)
                            elif edge in ("tail", "right", "end"):
                                delta = round((st_c + dur_c) - at, 3)
                                if delta <= 0.01 or delta >= dur_c - 0.01:
                                    return _text(f"ripple_trim tail: 'at' {at:g} must be strictly inside clip ({st_c:g}..{st_c + dur_c:g})", error=True)
                                c["dur"] = round(at - st_c, 3)
                                for cc in clips:
                                    if float(cc.get("start") or 0.0) >= st_c + dur_c - 0.01:
                                        cc["start"] = round(max(0.0, float(cc.get("start") or 0.0) - delta), 3)
                                if a.get("sync_lock", True):
                                    _ripple_other_tracks(tracks, ti, st_c + dur_c, delta)
                            else:
                                return _text(f"ripple_trim: unknown edge '{edge}' (head/tail)", error=True)
                except (ValueError, TypeError) as e:
                    return _text(f"bad track / clip / at: {e}", error=True)
                spec["tracks"] = tracks
                if path is not None:
                    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
                elif isinstance(raw, dict):
                    raw.clear(); raw.update(spec)
                where = f" · saved to {path} (live editor reloads)" if path else " · pass a file PATH to edit in place"
                lst = [{"i": i, "start": cl.get("start"), "dur": cl.get("dur"),
                        "label": cl.get("label") or cl.get("kind") or cl.get("src", "")} for i, cl in enumerate(clips)]
                return _text(f"ok: {act} → track {ti}, {len(clips)} clips{where}\n" + json.dumps(lst, ensure_ascii=False))
            try:
                if act == "add_scene":
                    sc = a.get("scene") or {}
                    if not isinstance(sc, dict) or not sc.get("type"):
                        return _text("add_scene: a 'scene' object with a 'type' is required", error=True)
                    at = _i(a["index"]) if a.get("index") is not None else n
                    scenes.insert(max(0, min(at, n)), sc)
                elif act in ("update_scene", "delete_scene", "move_scene", "duplicate_scene"):
                    i = _i(a.get("index"))
                    if not (0 <= i < n):
                        return _text(f"index {a.get('index')} out of range (0..{n - 1})", error=True)
                    if act == "update_scene":
                        scenes[i] = {**scenes[i], **(a.get("fields") or {})}
                    elif act == "delete_scene":
                        scenes.pop(i)
                    elif act == "duplicate_scene":
                        scenes.insert(i + 1, copy.deepcopy(scenes[i]))
                    else:                                # move_scene
                        s = scenes.pop(i)
                        scenes.insert(max(0, min(_i(a.get("to")), len(scenes))), s)
                else:
                    return _text("action = add_scene | update_scene | delete_scene | move_scene | duplicate_scene",
                                 error=True)
            except (ValueError, TypeError) as e:
                return _text(f"bad index / to: {e}", error=True)
            spec["scenes"] = scenes
            if path is not None:
                path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
            elif isinstance(raw, dict):
                raw.clear(); raw.update(spec)
            where = f" · saved to {path} (live editor reloads)" if path else " · pass a file PATH to edit in place"
            lst = [{"i": i, "type": s.get("type"), "title": s.get("title", "")} for i, s in enumerate(scenes)]
            return _text(f"ok: {act} → {len(scenes)} scenes{where}\n" + json.dumps(lst, ensure_ascii=False))
        spec, base = _spec_arg(a)
        try:
            clean = validate(spec)
        except SpecError as e:
            return _text("spec errors (fix them all):\n" + "\n".join(f"- {x}" for x in e.errors), error=True)
        if name == "kadans_validate":
            tl = timeline(clean)
            return _text(f"ok: {len(clean['scenes'])} scenes, ~{total(tl):.1f} s (estimated before voice), "
                         f"{clean['w']}x{clean['h']} @ {clean['fps']} fps")
        if name == "kadans_lint":
            return _text(json.dumps(L.lint(clean, base), ensure_ascii=False, indent=1))
        if name == "kadans_interchange":
            from . import interchange as IC
            act = str(a.get("action") or "export").lower()
            fmt = str(a.get("format") or "fcpxml").lower()
            if act == "export":
                out_p = Path(a["out"]) if a.get("out") else (base / f"{clean['title'][:40] or 'timeline'}.{'xml' if fmt == 'fcpxml' else 'edl'}")
                res_xml = IC.export_timeline(clean, fmt=fmt, out_path=out_p, base=base)
                return _text(f"timeline exported ({fmt.upper()}): {out_p} ({len(res_xml)} chars)")
            elif act == "import":
                content = str(a.get("content") or "")
                if a.get("out") and Path(a["out"]).is_file():
                    content = Path(a["out"]).read_text(encoding="utf-8", errors="ignore")
                sp = IC.import_timeline(content, fmt=fmt)
                return _text(json.dumps(sp, ensure_ascii=False, indent=1))
        if name == "kadans_loudness":
            target = Path(a["file"]) if a.get("file") else (base / "preview-audio.wav")
            return _text(json.dumps(L.measure_loudness(target), ensure_ascii=False, indent=1))
        if name == "kadans_preview":
            out = Path(a.get("out") or base / "kadans-preview.html")
            media_s, clips = M.prepare(clean, base, base / ".kadans-cache" / "clips")
            out.write_text(build_html(clean, timeline(clean, None, media_s), base, clips, out.parent), encoding="utf-8")
            return _text(f"preview: {out}  (open it in a browser: play / pause / scrub)")
        if name == "kadans_frame":
            out = Path(a.get("out") or base / f"kadans-frame-{float(a['t']):g}s.png")
            png = frame(clean, float(a["t"]), out, base)
            raw, mime = png.read_bytes(), "image/png"
            try:                                       # what the AI looks at: a light JPEG (the PNG stays on disk)
                import io
                from PIL import Image
                im = Image.open(io.BytesIO(raw)).convert("RGB")
                im.thumbnail((1280, 1280))
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=85)
                raw, mime = buf.getvalue(), "image/jpeg"
            except ImportError:
                pass
            data = base64.b64encode(raw).decode()
            return {"content": [{"type": "image", "data": data, "mimeType": mime},
                                {"type": "text", "text": f"frame saved: {png}"}], "isError": False}
        if name == "kadans_render":
            from .renderer import render
            out = Path(a.get("out") or base / f"{clean['title'][:40] or 'video'}.mp4".replace(" ", "-"))
            job = f"job{len(_JOBS) + 1}"
            st = {"state": "running", "stage": "start", "done": 0, "total": 0, "out": str(out), "started": time.time()}
            _JOBS[job] = st

            def prog(stage, done, tot, info):
                st.update(stage=stage, done=done, total=tot, info=info)

            def run():
                try:
                    r = render(clean, out, base, tts=_tts(), align=_align(), workers=a.get("workers"),
                               progress=prog, verify=bool(a.get("verify")))   # verify = kontwòl MP4 apre rann
                    st.update(state="done", seconds=r["seconds"], srt=str(r["srt"]) if r["srt"] else None,
                              captured=r["captured"], reused=r["reused"], elapsed=r["elapsed"], qc=r.get("qc"))
                except Exception as e:                          # noqa: BLE001
                    st.update(state="error", error=str(e)[:800])
            threading.Thread(target=run, daemon=True).start()
            return _text(f"rendering in the background: job={job} → {out}. Follow it with kadans_status.")
        return _text(f"unknown tool {name}", error=True)
    except Exception as e:                                       # noqa: BLE001 - one readable error for the AI
        _log(traceback.format_exc())
        return _text(f"{type(e).__name__}: {e}", error=True)


# ----------------------------------------------------------------------------------------------- JSON-RPC (stdio)
def serve() -> int:
    """Newline-delimited JSON-RPC 2.0 on stdin / stdout (MCP stdio transport)."""
    out = sys.stdout
    lock = threading.Lock()

    def send(msg: dict):
        with lock:
            out.write(json.dumps(msg, ensure_ascii=False) + "\n")
            out.flush()

    def handle(msg: dict):
        mid, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
        if mid is None:                                        # notification (initialized, cancelled…)
            return
        try:
            if method == "initialize":
                want = params.get("protocolVersion")
                res = {"protocolVersion": want if want in PROTOCOLS else PROTOCOLS[0],
                       "capabilities": {"tools": {"listChanged": False}},
                       "serverInfo": {"name": "kadans-wasdev", "title": NAME, "version": __version__},
                       "instructions": "Kadans WASDEV makes videos from a JSON spec. Start with kadans_schema."}
            elif method == "ping":
                res = {}
            elif method == "tools/list":
                res = {"tools": TOOLS}
            elif method == "tools/call":
                res = call(params.get("name", ""), params.get("arguments") or {})
            else:
                return send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"no method {method}"}})
            send({"jsonrpc": "2.0", "id": mid, "result": res})
        except Exception as e:                                  # noqa: BLE001
            send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": str(e)}})

    _log(f"{NAME} {__version__} MCP server ready (stdio)")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        for m in (msg if isinstance(msg, list) else [msg]):
            if m.get("method") == "tools/call":                # long calls never block ping / list
                threading.Thread(target=handle, args=(m,), daemon=True).start()
            else:
                handle(m)
    return 0


# ----------------------------------------------------------------------------------------------- client configs
def server_entry() -> dict:
    exe = shutil.which("kadans")
    if exe:
        return {"command": exe, "args": ["mcp"]}
    return {"command": sys.executable, "args": ["-m", "kadans", "mcp"],
            "env": {"PYTHONPATH": str(Path(__file__).resolve().parent.parent)}}


def _home() -> Path:
    return Path.home()


CLIENTS = {
    "claude-desktop": lambda: (Path(os.environ.get("APPDATA", _home() / "AppData/Roaming")) / "Claude"
                               / "claude_desktop_config.json") if os.name == "nt" else
                              (_home() / "Library/Application Support/Claude/claude_desktop_config.json"
                               if sys.platform == "darwin" else _home() / ".config/Claude/claude_desktop_config.json"),
    "claude-code-json": lambda: _home() / ".claude.json",
    "cursor": lambda: _home() / ".cursor" / "mcp.json",
    "gemini": lambda: _home() / ".gemini" / "settings.json",
    "antigravity": lambda: _home() / ".gemini" / "antigravity" / "mcp_config.json",
    "windsurf": lambda: _home() / ".codeium" / "windsurf" / "mcp_config.json",
    "vscode": lambda: Path.cwd() / ".vscode" / "mcp.json",
    "codex": lambda: _home() / ".codex" / "config.toml",
}


def _find_cli_exe(names: list[str]) -> str:
    for n in names:
        w = shutil.which(n)
        if w:
            return w
    if os.name == "nt":
        appdata = Path(os.environ.get("APPDATA", _home() / "AppData" / "Roaming"))
        localapp = Path(os.environ.get("LOCALAPPDATA", _home() / "AppData" / "Local"))
        search_dirs = [
            appdata / "npm",
            localapp / "Programs" / "claude-code",
            localapp / "Programs" / "Antigravity",
            _home() / ".local" / "bin",
            _home() / ".gemini" / "antigravity-cli",
        ]
        for d in search_dirs:
            for n in names:
                for ext in (".cmd", ".exe", ".bat", ""):
                    cand = d / (n + ext)
                    if cand.is_file():
                        return str(cand)
    return ""


def detect_ai_clis() -> list[dict]:
    """Detekte tout CLI AI ki sou PC a (Claude Code, Gemini CLI, Google Antigravity, OpenAI Codex) + estati MCP."""
    claude_exe = _find_cli_exe(["claude", "claude-code"])
    gemini_exe = _find_cli_exe(["gemini"])
    agy_exe = _find_cli_exe(["agy", "antigravity"])
    if not agy_exe and (_home() / ".gemini" / "antigravity-cli").is_dir():
        agy_exe = str(_home() / ".gemini" / "antigravity-cli")
    codex_exe = _find_cli_exe(["codex"])

    def _has_mcp_json(p: Path) -> bool:
        try:
            if not p.is_file():
                return False
            d = json.loads(p.read_text(encoding="utf-8"))
            return "kadans" in (d.get("mcpServers") or d.get("servers") or {})
        except Exception:
            return False

    def _has_mcp_toml(p: Path) -> bool:
        try:
            return p.is_file() and "[mcp_servers.kadans]" in p.read_text(encoding="utf-8")
        except Exception:
            return False

    return [
        {
            "id": "claude-code",
            "label": "Claude Code (Anthropic)",
            "installed": bool(claude_exe or (_home() / ".claude.json").is_file() or (_home() / ".claude").is_dir()),
            "exe": claude_exe or "claude",
            "mcp_active": _has_mcp_json(_home() / ".claude.json"),
        },
        {
            "id": "gemini",
            "label": "Gemini CLI (Google)",
            "installed": bool(gemini_exe or (_home() / ".gemini").is_dir()),
            "exe": gemini_exe or "gemini",
            "mcp_active": _has_mcp_json(_home() / ".gemini" / "settings.json"),
        },
        {
            "id": "antigravity",
            "label": "Google Antigravity (AGY)",
            "installed": bool(agy_exe or (_home() / ".gemini" / "antigravity-cli").is_dir()),
            "exe": agy_exe or "agy",
            "mcp_active": _has_mcp_json(_home() / ".gemini" / "antigravity" / "mcp_config.json")
                          or _has_mcp_json(_home() / ".gemini" / "settings.json"),
        },
        {
            "id": "codex",
            "label": "OpenAI Codex CLI",
            "installed": bool(codex_exe or (_home() / ".codex").is_dir()),
            "exe": codex_exe or "codex",
            "mcp_active": _has_mcp_toml(_home() / ".codex" / "config.toml"),
        },
    ]


def install(client: str) -> str:
    if client == "all":
        res = install_all()
        return json.dumps(res, indent=2, ensure_ascii=False)
    entry = server_entry()
    if client == "claude-code":
        # Write directly to ~/.claude.json so it always succeeds in 1 click, plus try `claude mcp add` if on PATH
        try:
            install("claude-code-json")
        except Exception:
            pass
        exe = _find_cli_exe(["claude", "claude-code"])
        if exe and os.path.isfile(exe):
            try:
                r = subprocess.run([exe, "mcp", "add", "--scope", "user", "kadans", "--", entry["command"], *entry["args"]],
                                   capture_output=True, text=True, timeout=8,
                                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                out_s = (r.stdout + r.stderr).strip()
                if out_s:
                    return out_s
            except Exception:
                pass
        return f"ok: {_home() / '.claude.json'}"
    if client not in CLIENTS:
        raise SystemExit(f"client: {', '.join(['all', 'claude-code', *CLIENTS])}")
    path = CLIENTS[client]()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        try:
            shutil.copy2(path, path.with_name(path.name + ".kadans-backup"))
        except OSError:
            pass
    if client == "codex":                                      # TOML: one table, replaced if it exists
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        lines, skip = [], False
        for ln in text.splitlines():
            if ln.strip().startswith("[mcp_servers.kadans"):
                skip = True
                continue
            if skip and ln.strip().startswith("["):
                skip = False
            if not skip:
                lines.append(ln)
        block = ["", "[mcp_servers.kadans]", f"command = {json.dumps(entry['command'])}",
                 f"args = {json.dumps(entry['args'])}"]
        if entry.get("env"):
            block.append("env = { " + ", ".join(f"{k} = {json.dumps(v)}" for k, v in entry["env"].items()) + " }")
        path.write_text("\n".join(lines + block) + "\n", encoding="utf-8")
        return f"ok: {path}"
    try:
        cfg = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except ValueError:
        cfg = {}
    key = "servers" if client == "vscode" else "mcpServers"
    cfg.setdefault(key, {})["kadans"] = ({"type": "stdio", **entry} if client == "vscode" else entry)
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    return f"ok: {path}"


def install_all() -> dict:
    """Aktive MCP Kadans sou tout CLI AI yo (Claude Code, Gemini CLI, Antigravity, Codex, Claude Desktop, Cursor) an 1 klik."""
    results = {}
    for target in ("claude-code", "gemini", "antigravity", "codex", "claude-desktop", "cursor"):
        try:
            results[target] = install(target)
        except Exception as e:
            results[target] = f"error: {e}"
    return {"ok": True, "activated": results, "clis": detect_ai_clis()}


def main(argv: list[str]) -> int:
    if "--print" in argv:
        print(json.dumps({"mcpServers": {"kadans": server_entry()}}, indent=2))
        return 0
    if "--install" in argv:
        i = argv.index("--install")
        print(install(argv[i + 1] if i + 1 < len(argv) else "all"))
        return 0
    return serve()

