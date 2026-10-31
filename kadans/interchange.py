"""Kadans WASDEV — Timeline Interchange: FCP7 XML (xmeml v5) & EDL CMX 3600.

Universal bidirectional timeline exchange between Kadans WASDEV and professional NLEs
(Adobe Premiere Pro, DaVinci Resolve, Final Cut Pro, Avid Media Composer).

By Getho Guerrier · GRAN LAKU COMPANY · https://wasdev.ai
"""
from __future__ import annotations

import os
import re
import urllib.parse
from pathlib import Path
from xml.etree import ElementTree as ET

from .spec import (
    RATIOS,
    TICKS_PER_SECOND,
    parse_timecode,
    quantize_time,
    sec_to_ticks,
    ticks_to_frames,
    ticks_to_sec,
    timecode,
    timeline as make_timeline,
)


def _ratio_from_dimensions(w: int, h: int) -> str:
    """Jwenn ratio ki pi pre gwosè w x h a."""
    if not w or not h:
        return "16:9"
    current_ratio = w / h
    best_name = "16:9"
    best_diff = 999.0
    for name, (rw, rh) in RATIOS.items():
        diff = abs((rw / rh) - current_ratio)
        if diff < best_diff:
            best_diff = diff
            best_name = name
    return best_name


def _file_url(p: str | Path | None) -> str:
    if not p:
        return ""
    p_str = str(p).replace("\\", "/")
    if not p_str.startswith("file://"):
        return f"file://localhost/{p_str.lstrip('/')}"
    return p_str


def _path_from_file_url(url: str) -> str:
    if not url:
        return ""
    u = urllib.parse.unquote(url)
    if u.startswith("file://localhost/"):
        u = u[len("file://localhost/"):]
    elif u.startswith("file:///"):
        u = u[len("file:///"):]
    elif u.startswith("file://"):
        u = u[len("file://"):]
    # Windows drive letter fix (e.g. C:/path)
    if len(u) >= 2 and u[1] == ":" or (len(u) >= 3 and u[0] == "/" and u[2] == ":"):
        u = u.lstrip("/")
    return os.path.normpath(u)


# ===============================================================================================
# FCP7 XML (xmeml v5) EXPORT & IMPORT
# ===============================================================================================

def export_fcp7_xml(spec: dict, out_path: str | Path | None = None, base: Path | None = None) -> str:
    """Ekspòte yon pwojè Kadans spec.json an FCP7 XML (xmeml version 5) pou Premiere Pro ak DaVinci Resolve."""
    title = str(spec.get("title") or "Kadans Timeline").strip()
    fps = float(spec.get("fps") or 30.0)
    int_fps = int(round(fps))
    ratio = str(spec.get("ratio") or "16:9")
    w, h = RATIOS.get(ratio, (1920, 1080))
    if spec.get("w") and spec.get("h"):
        w, h = int(spec["w"]), int(spec["h"])

    base_p = Path(base).resolve() if base else Path.cwd()

    # Kalkile timeline sèn yo
    scenes = spec.get("scenes") or []
    tl = []
    if scenes:
        try:
            tl = make_timeline(spec)
        except Exception:
            # Fallback senp si make_timeline rankontre yon mank
            cur_t = 0.0
            for idx, sc in enumerate(scenes):
                d = float(sc.get("duration") or 3.0)
                tl.append({"id": sc.get("id", f"scene_{idx+1}"), "start": cur_t, "dur": d, "voice_dur": 0})
                cur_t += d

    total_dur_sec = float(spec.get("total_duration") or 0.0)
    if not total_dur_sec:
        if tl:
            total_dur_sec = max(t["start"] + t["dur"] for t in tl)
        for tk in (spec.get("tracks") or []):
            for c in (tk.get("clips") or []):
                st = float(c.get("start", 0) or 0)
                du = float(c.get("dur", 0) or 0)
                if st + du > total_dur_sec:
                    total_dur_sec = st + du
    if total_dur_sec <= 0:
        total_dur_sec = 10.0

    total_frames = int(round(total_dur_sec * fps))

    # Rasin XML
    xmeml = ET.Element("xmeml", version="5")
    seq = ET.SubElement(xmeml, "sequence", id="sequence-1")
    ET.SubElement(seq, "name").text = title
    ET.SubElement(seq, "duration").text = str(total_frames)

    rate_el = ET.SubElement(seq, "rate")
    ET.SubElement(rate_el, "timebase").text = str(int_fps)
    ET.SubElement(rate_el, "ntsc").text = "FALSE"

    tc_el = ET.SubElement(seq, "timecode")
    tc_rate = ET.SubElement(tc_el, "rate")
    ET.SubElement(tc_rate, "timebase").text = str(int_fps)
    ET.SubElement(tc_rate, "ntsc").text = "FALSE"
    ET.SubElement(tc_el, "string").text = "00:00:00:00"
    ET.SubElement(tc_el, "frame").text = "0"
    ET.SubElement(tc_el, "displayformat").text = "NDF"

    media_el = ET.SubElement(seq, "media")

    # ------------------ VIDEO ------------------
    video_el = ET.SubElement(media_el, "video")
    fmt_el = ET.SubElement(video_el, "format")
    sc_el = ET.SubElement(fmt_el, "samplecharacteristics")
    sc_rate = ET.SubElement(sc_el, "rate")
    ET.SubElement(sc_rate, "timebase").text = str(int_fps)
    ET.SubElement(sc_el, "width").text = str(w)
    ET.SubElement(sc_el, "height").text = str(h)
    ET.SubElement(sc_el, "anamorphic").text = "FALSE"
    ET.SubElement(sc_el, "pixelaspectratio").text = "square"

    # Track 1: Sèn Kadans prensipal yo
    trk1 = ET.SubElement(video_el, "track")
    ET.SubElement(trk1, "enabled").text = "TRUE"
    ET.SubElement(trk1, "locked").text = "FALSE"

    for i, sc in enumerate(scenes):
        t_info = tl[i] if i < len(tl) else {"start": i * 3.0, "dur": 3.0}
        sc_st = float(t_info.get("start", 0.0))
        sc_dur = float(t_info.get("dur", 3.0))
        st_frame = int(round(sc_st * fps))
        end_frame = int(round((sc_st + sc_dur) * fps))
        dur_frame = end_frame - st_frame

        in_sec = float(sc.get("in", 0.0) or 0.0)
        in_frame = int(round(in_sec * fps))
        out_frame = in_frame + dur_frame

        clip_name = sc.get("title") or f"Scene {i+1} ({sc.get('type', 'scene')})"

        ci = ET.SubElement(trk1, "clipitem", id=f"clipitem-scene-{i+1}")
        ET.SubElement(ci, "name").text = str(clip_name)
        ET.SubElement(ci, "enabled").text = "TRUE"
        ET.SubElement(ci, "duration").text = str(dur_frame)
        ci_rate = ET.SubElement(ci, "rate")
        ET.SubElement(ci_rate, "timebase").text = str(int_fps)
        ET.SubElement(ci, "start").text = str(st_frame)
        ET.SubElement(ci, "end").text = str(end_frame)
        ET.SubElement(ci, "in").text = str(in_frame)
        ET.SubElement(ci, "out").text = str(out_frame)

        # File referans si gen fichye medya
        src_path = sc.get("src")
        if src_path:
            full_path = (base_p / src_path).resolve() if not Path(src_path).is_absolute() else Path(src_path)
            fi = ET.SubElement(ci, "file", id=f"file-scene-{i+1}")
            ET.SubElement(fi, "name").text = Path(src_path).name
            ET.SubElement(fi, "pathurl").text = _file_url(full_path)
            fi_rate = ET.SubElement(fi, "rate")
            ET.SubElement(fi_rate, "timebase").text = str(int_fps)
            ET.SubElement(fi, "duration").text = str(dur_frame)
            fi_media = ET.SubElement(fi, "media")
            fi_video = ET.SubElement(fi_media, "video")
            fi_sc = ET.SubElement(fi_video, "samplecharacteristics")
            ET.SubElement(fi_sc, "width").text = str(w)
            ET.SubElement(fi_sc, "height").text = str(h)

    # Track adisyonèl video ki nan spec.tracks
    video_tracks = [tk for tk in (spec.get("tracks") or []) if str(tk.get("kind") or "").lower() == "video"]
    for trk_idx, tk in enumerate(video_tracks):
        vtrk = ET.SubElement(video_el, "track")
        ET.SubElement(vtrk, "enabled").text = "FALSE" if tk.get("muted") else "TRUE"
        ET.SubElement(vtrk, "locked").text = "TRUE" if tk.get("locked") else "FALSE"
        for clip_idx, c in enumerate(tk.get("clips") or []):
            st = float(c.get("start", 0) or 0)
            du = float(c.get("dur", 2) or 2)
            c_in = float(c.get("in", 0) or 0)
            sf = int(round(st * fps))
            ef = int(round((st + du) * fps))
            df = ef - sf
            inf = int(round(c_in * fps))
            outf = inf + df
            ci = ET.SubElement(vtrk, "clipitem", id=f"clipitem-vtrk-{trk_idx+1}-{clip_idx+1}")
            c_name = c.get("name") or Path(c.get("src", "clip")).name
            ET.SubElement(ci, "name").text = str(c_name)
            ET.SubElement(ci, "enabled").text = "TRUE"
            ET.SubElement(ci, "duration").text = str(df)
            ci_r = ET.SubElement(ci, "rate")
            ET.SubElement(ci_r, "timebase").text = str(int_fps)
            ET.SubElement(ci, "start").text = str(sf)
            ET.SubElement(ci, "end").text = str(ef)
            ET.SubElement(ci, "in").text = str(inf)
            ET.SubElement(ci, "out").text = str(outf)
            if c.get("src"):
                fp = (base_p / c["src"]).resolve() if not Path(c["src"]).is_absolute() else Path(c["src"])
                fi = ET.SubElement(ci, "file", id=f"file-vtrk-{trk_idx+1}-{clip_idx+1}")
                ET.SubElement(fi, "name").text = fp.name
                ET.SubElement(fi, "pathurl").text = _file_url(fp)

    # ------------------ AUDIO ------------------
    audio_el = ET.SubElement(media_el, "audio")

    # Audio Track 1: Vwa sèn yo (ElevenLabs / Voice)
    atrk1 = ET.SubElement(audio_el, "track")
    ET.SubElement(atrk1, "enabled").text = "TRUE"
    ET.SubElement(atrk1, "locked").text = "FALSE"

    for i, sc in enumerate(scenes):
        vf = sc.get("voice_file")
        v_text = sc.get("voice")
        if vf or v_text:
            t_info = tl[i] if i < len(tl) else {"start": i * 3.0, "dur": 3.0}
            sc_st = float(t_info.get("start", 0.0))
            v_dur = float(t_info.get("voice_dur", 0.0) or t_info.get("dur", 3.0))
            sf = int(round(sc_st * fps))
            ef = int(round((sc_st + v_dur) * fps))
            df = max(1, ef - sf)

            ci = ET.SubElement(atrk1, "clipitem", id=f"clipitem-voice-{i+1}")
            ET.SubElement(ci, "name").text = f"Voice {i+1}: {sc.get('id', '')}"
            ET.SubElement(ci, "enabled").text = "TRUE"
            ET.SubElement(ci, "duration").text = str(df)
            ci_r = ET.SubElement(ci, "rate")
            ET.SubElement(ci_r, "timebase").text = str(int_fps)
            ET.SubElement(ci, "start").text = str(sf)
            ET.SubElement(ci, "end").text = str(ef)
            ET.SubElement(ci, "in").text = "0"
            ET.SubElement(ci, "out").text = str(df)
            if vf:
                v_path = (base_p / vf).resolve() if not Path(vf).is_absolute() else Path(vf)
                fi = ET.SubElement(ci, "file", id=f"file-voice-{i+1}")
                ET.SubElement(fi, "name").text = v_path.name
                ET.SubElement(fi, "pathurl").text = _file_url(v_path)

    # Audio Track 2: Mizik (Music bed) si genyen
    music = spec.get("music")
    if music and isinstance(music, dict) and music.get("src"):
        m_src = music["src"]
        m_path = (base_p / m_src).resolve() if not Path(m_src).is_absolute() else Path(m_src)
        atrk_m = ET.SubElement(audio_el, "track")
        ET.SubElement(atrk_m, "enabled").text = "TRUE"
        ET.SubElement(atrk_m, "locked").text = "FALSE"
        ci_m = ET.SubElement(atrk_m, "clipitem", id="clipitem-music-bed")
        ET.SubElement(ci_m, "name").text = f"Music: {Path(m_src).name}"
        ET.SubElement(ci_m, "duration").text = str(total_frames)
        ci_mr = ET.SubElement(ci_m, "rate")
        ET.SubElement(ci_mr, "timebase").text = str(int_fps)
        ET.SubElement(ci_m, "start").text = "0"
        ET.SubElement(ci_m, "end").text = str(total_frames)
        ET.SubElement(ci_m, "in").text = "0"
        ET.SubElement(ci_m, "out").text = str(total_frames)
        fi_m = ET.SubElement(ci_m, "file", id="file-music-bed")
        ET.SubElement(fi_m, "name").text = m_path.name
        ET.SubElement(fi_m, "pathurl").text = _file_url(m_path)

    # Audio Tracks ki soti nan spec.tracks (audio, sfx)
    audio_tracks = [tk for tk in (spec.get("tracks") or []) if str(tk.get("kind") or "").lower() in ("audio", "sfx")]
    for trk_idx, tk in enumerate(audio_tracks):
        atrk = ET.SubElement(audio_el, "track")
        ET.SubElement(atrk, "enabled").text = "FALSE" if tk.get("muted") else "TRUE"
        ET.SubElement(atrk, "locked").text = "TRUE" if tk.get("locked") else "FALSE"
        for clip_idx, c in enumerate(tk.get("clips") or []):
            st = float(c.get("start", 0) or 0)
            du = float(c.get("dur", 2) or 2)
            c_in = float(c.get("in", 0) or 0)
            sf = int(round(st * fps))
            ef = int(round((st + du) * fps))
            df = max(1, ef - sf)
            inf = int(round(c_in * fps))
            outf = inf + df
            ci = ET.SubElement(atrk, "clipitem", id=f"clipitem-atrk-{trk_idx+1}-{clip_idx+1}")
            c_name = c.get("name") or Path(c.get("src", "audio_clip")).name
            ET.SubElement(ci, "name").text = str(c_name)
            ET.SubElement(ci, "enabled").text = "TRUE"
            ET.SubElement(ci, "duration").text = str(df)
            ci_r = ET.SubElement(ci, "rate")
            ET.SubElement(ci_r, "timebase").text = str(int_fps)
            ET.SubElement(ci, "start").text = str(sf)
            ET.SubElement(ci, "end").text = str(ef)
            ET.SubElement(ci, "in").text = str(inf)
            ET.SubElement(ci, "out").text = str(outf)
            if c.get("src"):
                fp = (base_p / c["src"]).resolve() if not Path(c["src"]).is_absolute() else Path(c["src"])
                fi = ET.SubElement(ci, "file", id=f"file-atrk-{trk_idx+1}-{clip_idx+1}")
                ET.SubElement(fi, "name").text = fp.name
                ET.SubElement(fi, "pathurl").text = _file_url(fp)

    # ------------------ MARKERS ------------------
    for m in (spec.get("markers") or []):
        if isinstance(m, dict) and "at" in m:
            mf = int(round(float(m["at"]) * fps))
            m_el = ET.SubElement(seq, "marker")
            ET.SubElement(m_el, "name").text = str(m.get("label") or "Marker")
            ET.SubElement(m_el, "comment").text = str(m.get("comment") or "")
            ET.SubElement(m_el, "in").text = str(mf)
            ET.SubElement(m_el, "out").text = str(mf)

    # Serializasyon XML
    raw_xml = ET.tostring(xmeml, encoding="utf-8")
    # Formatting pwòp
    try:
        from xml.dom import minidom
        dom = minidom.parseString(raw_xml)
        pretty = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
    except Exception:
        pretty = raw_xml.decode("utf-8")

    # Header xmeml
    if "<!DOCTYPE xmeml>" not in pretty:
        lines = pretty.split("\n")
        if lines and lines[0].startswith("<?xml"):
            lines.insert(1, "<!DOCTYPE xmeml>")
        else:
            lines.insert(0, "<!DOCTYPE xmeml>")
        pretty = "\n".join(lines)

    if out_path:
        out_p = Path(out_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(pretty, encoding="utf-8")

    return pretty


def import_fcp7_xml(xml_content_or_path: str | Path) -> dict:
    """Enpòte yon fichye FCP7 XML (xmeml) epi kreye yon spec.json Kadans konplè."""
    content = ""
    if isinstance(xml_content_or_path, (str, Path)) and os.path.exists(str(xml_content_or_path)):
        content = Path(xml_content_or_path).read_text(encoding="utf-8", errors="ignore")
    else:
        content = str(xml_content_or_path)

    # Netwaye doctype pou ET pa bloke
    clean_xml = re.sub(r"<!DOCTYPE[^>]*>", "", content)
    root = ET.fromstring(clean_xml)

    seq = root.find(".//sequence")
    if seq is None:
        seq = root

    title = "Imported Sequence"
    name_el = seq.find("name")
    if name_el is not None and name_el.text:
        title = name_el.text.strip()

    fps = 30.0
    rate_el = seq.find(".//rate/timebase")
    if rate_el is not None and rate_el.text:
        try:
            fps = float(rate_el.text.strip())
        except ValueError:
            fps = 30.0

    w, h = 1920, 1080
    w_el = seq.find(".//media/video/format/samplecharacteristics/width")
    h_el = seq.find(".//media/video/format/samplecharacteristics/height")
    if w_el is not None and h_el is not None:
        try:
            w, h = int(w_el.text.strip()), int(h_el.text.strip())
        except (ValueError, TypeError):
            pass

    ratio = _ratio_from_dimensions(w, h)

    scenes = []
    tracks = []
    markers = []

    # Li video tracks
    v_tracks = seq.findall(".//media/video/track")
    for trk_idx, vtrk in enumerate(v_tracks):
        clipitems = vtrk.findall("clipitem")
        if trk_idx == 0:
            # Track prensipal -> sèn Kadans
            for ci_idx, ci in enumerate(clipitems):
                ci_name = ci.findtext("name") or f"Scene {ci_idx+1}"
                st_f = int(ci.findtext("start") or 0)
                end_f = int(ci.findtext("end") or (st_f + int(fps * 3)))
                in_f = int(ci.findtext("in") or 0)
                dur_sec = max(0.5, (end_f - st_f) / fps)
                in_sec = in_f / fps

                file_el = ci.find("file")
                src_val = None
                if file_el is not None:
                    pathurl = file_el.findtext("pathurl")
                    if pathurl:
                        src_val = _path_from_file_url(pathurl)

                sc_type = "video" if src_val else "text"
                sc_obj = {
                    "id": f"scene_{ci_idx+1}",
                    "type": sc_type,
                    "title": ci_name,
                    "duration": round(dur_sec, 3),
                }
                if src_val:
                    sc_obj["src"] = src_val
                    if in_sec > 0.001:
                        sc_obj["in"] = round(in_sec, 3)
                scenes.append(sc_obj)
        else:
            # Track segondè -> video layer track
            clips = []
            for ci_idx, ci in enumerate(clipitems):
                ci_name = ci.findtext("name") or f"Clip {ci_idx+1}"
                st_f = int(ci.findtext("start") or 0)
                end_f = int(ci.findtext("end") or (st_f + int(fps * 3)))
                in_f = int(ci.findtext("in") or 0)
                file_el = ci.find("file")
                src_val = ""
                if file_el is not None:
                    pathurl = file_el.findtext("pathurl")
                    if pathurl:
                        src_val = _path_from_file_url(pathurl)
                clips.append({
                    "name": ci_name,
                    "src": src_val,
                    "start": round(st_f / fps, 3),
                    "dur": round((end_f - st_f) / fps, 3),
                    "in": round(in_f / fps, 3),
                    "kind": "video",
                })
            if clips:
                tracks.append({"name": f"Video {trk_idx+1}", "kind": "video", "clips": clips})

    # Li audio tracks
    a_tracks = seq.findall(".//media/audio/track")
    for trk_idx, atrk in enumerate(a_tracks):
        clipitems = atrk.findall("clipitem")
        clips = []
        for ci_idx, ci in enumerate(clipitems):
            ci_name = ci.findtext("name") or f"Audio {ci_idx+1}"
            st_f = int(ci.findtext("start") or 0)
            end_f = int(ci.findtext("end") or (st_f + int(fps * 3)))
            in_f = int(ci.findtext("in") or 0)
            file_el = ci.find("file")
            src_val = ""
            if file_el is not None:
                pathurl = file_el.findtext("pathurl")
                if pathurl:
                    src_val = _path_from_file_url(pathurl)
            clips.append({
                "name": ci_name,
                "src": src_val,
                "start": round(st_f / fps, 3),
                "dur": round((end_f - st_f) / fps, 3),
                "in": round(in_f / fps, 3),
                "kind": "audio",
            })
        if clips:
            tracks.append({"name": f"Audio {trk_idx+1}", "kind": "audio", "clips": clips})

    # Li markers
    for m in seq.findall(".//marker"):
        m_name = m.findtext("name") or "Marker"
        m_in = int(m.findtext("in") or 0)
        markers.append({"at": round(m_in / fps, 3), "label": m_name})

    if not scenes:
        scenes.append({"type": "hook", "title": title, "duration": 5.0})

    int_fps = int(round(fps))
    tot_dur = round(sum(float(s.get("duration", 3.0)) for s in scenes), 3)
    spec = {
        "kadans": 1,
        "title": title,
        "lang": "fr",
        "fps": int_fps if abs(fps - int_fps) < 0.01 else fps,
        "ratio": ratio,
        "total_duration": tot_dur,
        "brand": {
            "name": title,
            "colors": {"bg": "#0b0816", "primary": "#8b5cf6", "accent": "#0098ff", "text": "#f3eefe"}
        },
        "scenes": scenes,
    }
    if tracks:
        spec["tracks"] = tracks
    if markers:
        spec["markers"] = markers

    return spec


def _parse_fcpx_time(t_str: str | None, default: float = 0.0) -> float:
    """Konvèti yon tan FCPX (egz. '5s', '100/3000s', '12.5s') an segonn (float)."""
    if not t_str:
        return default
    t_clean = str(t_str).strip()
    if t_clean.endswith("s"):
        t_clean = t_clean[:-1]
    if "/" in t_clean:
        try:
            num, den = t_clean.split("/", 1)
            return float(num) / float(den)
        except (ValueError, ZeroDivisionError):
            return default
    try:
        return float(t_clean)
    except ValueError:
        return default


def import_fcpxml(fcpxml_content_or_path: str | Path) -> dict:
    """Enpòte yon fichye Final Cut Pro X (fcpxml) epi kreye yon spec Kadans konplè."""
    content = ""
    if isinstance(fcpxml_content_or_path, (str, Path)) and os.path.exists(str(fcpxml_content_or_path)):
        content = Path(fcpxml_content_or_path).read_text(encoding="utf-8", errors="ignore")
    else:
        content = str(fcpxml_content_or_path)

    clean_xml = re.sub(r"<!DOCTYPE[^>]*>", "", content)
    root = ET.fromstring(clean_xml)

    # Resous
    res_map = {}
    for res in root.findall(".//resources/*"):
        rid = res.get("id")
        if rid:
            res_map[rid] = res

    proj = root.find(".//project")
    seq = root.find(".//sequence")
    title = proj.get("name") if (proj is not None and proj.get("name")) else "FCPX Sequence"

    w, h = 1920, 1080
    fps = 30.0
    fmt_ref = seq.get("format") if seq is not None else None
    if fmt_ref and fmt_ref in res_map:
        f_el = res_map[fmt_ref]
        try:
            w = int(f_el.get("width") or 1920)
            h = int(f_el.get("height") or 1080)
        except (ValueError, TypeError):
            pass
        fd = f_el.get("frameDuration")
        if fd:
            f_dur = _parse_fcpx_time(fd)
            if f_dur > 0:
                fps = round(1.0 / f_dur, 3)

    ratio = _ratio_from_dimensions(w, h)
    scenes = []
    tracks = []
    main_clips = []

    spine = root.find(".//spine")
    curr_t = 0.0
    if spine is not None:
        for idx, item in enumerate(spine):
            c_tag = item.tag
            c_name = item.get("name") or f"Clip {idx+1}"
            c_dur = _parse_fcpx_time(item.get("duration"), 3.0)
            c_offset = _parse_fcpx_time(item.get("offset"), curr_t)
            c_start = _parse_fcpx_time(item.get("start"), 0.0)

            ref_id = item.get("ref")
            src_path = None
            if ref_id and ref_id in res_map:
                asset = res_map[ref_id]
                raw_src = asset.get("src")
                if not raw_src:
                    mrep = asset.find("media-rep")
                    if mrep is not None:
                        raw_src = mrep.get("src")
                if raw_src:
                    src_path = _path_from_file_url(raw_src)

            sc_type = "video" if (src_path or c_tag in ("video", "asset-clip")) else "text"
            sc_obj = {
                "id": f"scene_{idx+1}",
                "type": sc_type,
                "title": c_name,
                "duration": round(c_dur, 3),
            }
            if src_path:
                sc_obj["src"] = src_path
            if c_start > 0.001:
                sc_obj["in"] = round(c_start, 3)
            scenes.append(sc_obj)

            clip_obj = {
                "id": f"clip_{idx+1}",
                "type": sc_type,
                "name": c_name,
                "start": round(c_offset, 3),
                "dur": round(c_dur, 3),
                "duration": round(c_dur, 3),
                "in": round(c_start, 3),
                "out": round(c_start + c_dur, 3),
            }
            if src_path:
                clip_obj["src"] = src_path
            main_clips.append(clip_obj)
            curr_t = max(curr_t + c_dur, c_offset + c_dur)

    if not scenes:
        scenes.append({"id": "scene_1", "type": "hook", "title": title, "duration": 5.0})

    if main_clips:
        tracks.append({
            "id": "trk_v1",
            "type": "video",
            "name": "V1",
            "clips": main_clips
        })

    int_fps = int(round(fps))
    tot_dur = round(max(3.0, curr_t if curr_t > 0 else sum(float(s.get("duration", 3.0)) for s in scenes)), 3)
    return {
        "kadans": 1,
        "title": title,
        "lang": "fr",
        "fps": int_fps if abs(fps - int_fps) < 0.01 else fps,
        "ratio": ratio,
        "total_duration": tot_dur,
        "brand": {
            "name": title,
            "colors": {"bg": "#0b0816", "primary": "#8b5cf6", "accent": "#0098ff", "text": "#f3eefe"}
        },
        "scenes": scenes,
        "tracks": tracks
    }


# ===============================================================================================
# EDL CMX 3600 EXPORT & IMPORT
# ===============================================================================================

def export_edl(spec: dict, out_path: str | Path | None = None, title: str | None = None) -> str:
    """Ekspòte pwojè a an fòma CMX 3600 Edit Decision List (EDL universal)."""
    t_name = str(title or spec.get("title") or "KADANS_TIMELINE").strip().replace(" ", "_")[:32].upper()
    fps = float(spec.get("fps") or 30.0)

    scenes = spec.get("scenes") or []
    tl = []
    if scenes:
        try:
            tl = make_timeline(spec)
        except Exception:
            cur_t = 0.0
            for idx, sc in enumerate(scenes):
                d = float(sc.get("duration") or 3.0)
                tl.append({"id": sc.get("id", f"scene_{idx+1}"), "start": cur_t, "dur": d})
                cur_t += d

    lines = [
        f"TITLE: {t_name}",
        "FCM: NON-DROP FRAME",
        "",
    ]

    event_num = 1
    # Video sèn yo
    for i, sc in enumerate(scenes):
        t_info = tl[i] if i < len(tl) else {"start": i * 3.0, "dur": 3.0}
        sc_st = float(t_info.get("start", 0.0))
        sc_dur = float(t_info.get("dur", 3.0))
        src_in = float(sc.get("in", 0.0) or 0.0)
        src_out = src_in + sc_dur

        dst_in_tc = timecode(sc_st, fps)
        dst_out_tc = timecode(sc_st + sc_dur, fps)
        src_in_tc = timecode(src_in, fps)
        src_out_tc = timecode(src_out, fps)

        reel = "AX"
        clip_name = sc.get("src") or sc.get("title") or f"SCENE_{i+1}"
        clip_basename = Path(str(clip_name)).name.replace(" ", "_")

        # Fòma CMX 3600: 001  AX       V     C        00:00:00:00 00:00:05:00 00:00:00:00 00:00:05:00
        lines.append(f"{event_num:03d}  {reel:<8} V     C        {src_in_tc} {src_out_tc} {dst_in_tc} {dst_out_tc}")
        lines.append(f"* FROM CLIP NAME: {clip_basename}")
        event_num += 1

    # Audio clips ki sou tracks
    for tk in (spec.get("tracks") or []):
        is_audio = str(tk.get("kind") or "").lower() in ("audio", "sfx")
        track_char = "A" if is_audio else "V"
        for c in (tk.get("clips") or []):
            st = float(c.get("start", 0) or 0)
            du = float(c.get("dur", 2) or 2)
            c_in = float(c.get("in", 0) or 0)
            dst_in_tc = timecode(st, fps)
            dst_out_tc = timecode(st + du, fps)
            src_in_tc = timecode(c_in, fps)
            src_out_tc = timecode(c_in + du, fps)
            c_name = Path(str(c.get("src") or c.get("name") or "AUDIO")).name.replace(" ", "_")
            lines.append(f"{event_num:03d}  AX       {track_char:<5} C        {src_in_tc} {src_out_tc} {dst_in_tc} {dst_out_tc}")
            lines.append(f"* FROM CLIP NAME: {c_name}")
            event_num += 1

    edl_text = "\n".join(lines) + "\n"

    if out_path:
        out_p = Path(out_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(edl_text, encoding="utf-8")

    return edl_text


def import_edl(edl_content_or_path: str | Path, fps: float = 30.0) -> dict:
    """Enpòte yon fichye EDL CMX 3600 epi pwodui yon spec.json Kadans."""
    content = ""
    if isinstance(edl_content_or_path, (str, Path)) and os.path.exists(str(edl_content_or_path)):
        content = Path(edl_content_or_path).read_text(encoding="utf-8", errors="ignore")
    else:
        content = str(edl_content_or_path)

    title = "EDL Imported Project"
    scenes = []
    audio_clips = []

    # Regex pou liy evènman CMX 3600
    ev_re = re.compile(
        r"^(\d+)\s+([\w\d]+)\s+([VA\d]+)\s+([CWD])\s+"
        r"(\d{2}:\d{2}:\d{2}[:;]\d{2})\s+(\d{2}:\d{2}:\d{2}[:;]\d{2})\s+"
        r"(\d{2}:\d{2}:\d{2}[:;]\d{2})\s+(\d{2}:\d{2}:\d{2}[:;]\d{2})"
    )

    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("TITLE:"):
            title = line[6:].strip()
            i += 1
            continue

        m = ev_re.match(line)
        if m:
            ev_id, reel, track_type, trans, src_in_tc, src_out_tc, dst_in_tc, dst_out_tc = m.groups()
            src_in = parse_timecode(src_in_tc, fps)
            src_out = parse_timecode(src_out_tc, fps)
            dst_in = parse_timecode(dst_in_tc, fps)
            dst_out = parse_timecode(dst_out_tc, fps)
            dur = max(0.1, dst_out - dst_in)

            # Chèche liy kòmantè ki swiv la pou jwenn non fichye a
            clip_name = f"Event_{ev_id}"
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith("* FROM CLIP NAME:"):
                    clip_name = next_line[17:].strip()
                    i += 1

            if "V" in track_type:
                sc = {
                    "id": f"scene_{ev_id}",
                    "type": "video" if ("." in clip_name) else "text",
                    "title": clip_name,
                    "duration": round(dur, 3),
                }
                if "." in clip_name:
                    sc["src"] = clip_name
                    if src_in > 0.001:
                        sc["in"] = round(src_in, 3)
                scenes.append(sc)
            elif "A" in track_type:
                audio_clips.append({
                    "name": clip_name,
                    "src": clip_name if ("." in clip_name) else "",
                    "start": round(dst_in, 3),
                    "dur": round(dur, 3),
                    "in": round(src_in, 3),
                    "kind": "audio",
                })
        i += 1

    if not scenes:
        scenes.append({"type": "hook", "title": title, "duration": 5.0})

    spec = {
        "kadans": 1,
        "title": title,
        "fps": fps,
        "ratio": "16:9",
        "scenes": scenes,
    }
    if audio_clips:
        spec["tracks"] = [{"name": "Audio 1", "kind": "audio", "clips": audio_clips}]

    return spec


# ===============================================================================================
# UNIVERSAL CONVENIENCE WRAPPERS
# ===============================================================================================

def export_timeline(spec: dict, fmt: str = "fcpxml", out_path: str | Path | None = None, base: Path | None = None) -> str:
    """Ekspòte timeline Kadans la an fòma demann lan ('fcpxml' oswa 'edl')."""
    fmt_clean = str(fmt or "fcpxml").lower().strip()
    if fmt_clean in ("fcpxml", "fcp7", "fcp", "xml", "xmeml"):
        return export_fcp7_xml(spec, out_path, base)
    if fmt_clean in ("edl", "cmx", "cmx3600"):
        return export_edl(spec, out_path)
    raise ValueError(f"Fòma interchange enkoni: {fmt}. Fòma sipòte yo se 'fcpxml' ak 'edl'.")


def import_timeline(content_or_path: str | Path, fmt: str = "auto", fps: float = 30.0) -> dict:
    """Enpòte yon timeline ekstèn ('fcpxml', 'edl', oswa 'auto' deteksyon)."""
    text = ""
    if isinstance(content_or_path, (str, Path)) and os.path.exists(str(content_or_path)):
        text = Path(content_or_path).read_text(encoding="utf-8", errors="ignore")
    else:
        text = str(content_or_path)

    fmt_clean = str(fmt or "auto").lower().strip()
    if fmt_clean == "auto":
        if "<fcpxml" in text:
            fmt_clean = "fcpxml"
        elif "<xmeml" in text or "<?xml" in text or "<sequence" in text:
            fmt_clean = "fcp7"
        elif "TITLE:" in text or "FCM:" in text:
            fmt_clean = "edl"
        else:
            fmt_clean = "fcpxml" if "<spine" in text else "fcp7"

    if fmt_clean in ("fcpxml", "fcpx"):
        return import_fcpxml(text)
    if fmt_clean in ("fcp7", "fcp", "xml", "xmeml"):
        return import_fcp7_xml(text)
    if fmt_clean in ("edl", "cmx", "cmx3600"):
        return import_edl(text, fps)
    raise ValueError(f"Fòma interchange enkoni: {fmt}.")
