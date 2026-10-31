"""Kadans WASDEV — Kadans HTML Animation Bridge.

Pèmèt nenpòt kòd HTML/GSAP/Three.js/Canvas depoze dirèkteman
nan yon sèn `html` Kadans san okenn modifikasyon, pandan l ap benefisye otomatikman de:
- Vwa natirèl ElevenLabs (klonaj vwa ak OpenVoice)
- Sou-tit otomatik ak Whisper (QC)
- Senkronizasyon data-on / data-at
- Ducking odyo ak mizik
- Rann paralèl GPU akselere (NVENC/QuickSync/AMF)

By Getho Guerrier · GRAN LAKU COMPANY · https://wasdev.ai
"""
from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


def detect_libraries(code: str) -> List[str]:
    """Detekte otomatikman libreri animasyon ki nesesè pou kòd la."""
    code_lower = code.lower()
    libs: List[str] = []

    # GSAP detection
    if any(k in code for k in ("gsap", "TimelineMax", "TweenMax", "TimelineLite", "TweenLite", "ScrollTrigger")):
        libs.append("gsap")

    # Three.js
    if any(k in code for k in ("THREE.", "new THREE", "WebGLRenderer")):
        libs.append("three")

    # Lottie
    if any(k in code_lower for k in ("lottie", "bodymovin", "loadanimation")):
        libs.append("lottie")

    # Anime.js
    if any(k in code for k in ("anime(", "anime.timeline", "anime.set")):
        libs.append("anime")

    # Chart.js
    if any(k in code for k in ("new Chart(", "Chart.register")):
        libs.append("chart")

    # Motion
    if any(k in code for k in ("animate(", "timeline(")) and "motion" not in libs:
        if "motion" in code_lower:
            libs.append("motion")

    # Asire gsap ladan l pa defo pou animasyon entèaktif
    if not libs or "gsap" not in libs:
        libs.insert(0, "gsap")

    return libs


def extract_html_bundle(source: Union[str, Path]) -> Tuple[str, List[str], Optional[float]]:
    """Li yon fichye HTML oswa dosye animasyon Kadans epi retounen (html_kontni, libreri_detekte, dire_estime)."""
    p = Path(source)
    if p.is_dir():
        # Chèche index.html oswa template.html
        for c in ("index.html", "template.html", "main.html", "render.html"):
            cand = p / c
            if cand.is_file():
                p = cand
                break
        else:
            # Pran premye fichye .html nan dosye a
            htmls = list(p.glob("*.html"))
            if htmls:
                p = htmls[0]
            else:
                raise FileNotFoundError(f"Pa gen fichye HTML nan dosye {source}")

    raw = p.read_text(encoding="utf-8", errors="replace")

    # Detekte dire si li espesifye nan config oswa meta
    duration = None
    dur_match = re.search(r'(?:duration|data-duration|durationInFrames)\s*[:=]\s*["\']?([\d.]+)["\']?', raw, re.I)
    if dur_match:
        try:
            val = float(dur_match.group(1))
            # Si se frames (e.g. 150 frames @ 30fps = 5s)
            duration = (val / 30.0) if val > 60 else val
        except ValueError:
            pass

    libs = detect_libraries(raw)

    # Si se yon paj HTML konplè ak <html>...<body>, nou ka kenbe kò a oswa tout paj la
    # Nan Kadans sèn `html`, tout sa ki andedan <style> ak <script> ak <body> egzekite nan .htmlwrap
    return raw, libs, duration


def import_kadans_html(
    source: Union[str, Path],
    title: str = "",
    lang: str = "fr",
    voice_engine: str = "elevenlabs",
    voice_text: str = "",
    ratio: str = "16:9",
    fps: int = 30,
    duration: Optional[float] = None,
) -> dict:
    """Konvèti yon pwojè oswa fichye animasyon HTML nan yon spec Kadans 100% natif.

    Rezilta a se yon dokiman JSON Kadans ki ka rann imedyatman nan Kadans Studio oswa WASDEV.
    """
    raw_html, libs, detected_dur = extract_html_bundle(source)
    dur = duration or detected_dur or 5.0

    src_path = Path(source)
    clean_title = title or src_path.stem.replace("-", " ").replace("_", " ").title()
    if clean_title.lower() == "index":
        clean_title = src_path.parent.name.replace("-", " ").replace("_", " ").title() or "Kadans Animation"

    spec = {
        "kadans": 1,
        "title": clean_title,
        "lang": lang,
        "ratio": ratio,
        "fps": fps,
        "voice": {
            "engine": voice_engine,
            "gender": "female",
            "lang": lang,
        },
        "music": {
            "mood": "upbeat",
            "volume": 0.18,
        },
        "credit": False,
        "scenes": [
            {
                "type": "html",
                "id": "scene_kadans_html_1",
                "title": clean_title,
                "html": raw_html,
                "libs": libs,
                "duration": round(float(dur), 2),
                "voice": voice_text or {
                    "ht": "Byenvini nan kreyasyon videyo avèk Kadans.",
                    "fr": "Bienvenue dans Kadans WASDEV, moteur vidéo professionnel.",
                    "en": "Welcome to Kadans WASDEV, the professional video engine.",
                    "es": "Bienvenido a Kadans WASDEV, el motor de vídeo profesional.",
                    "pt": "Bem-vindo ao Kadans WASDEV, o motor de vídeo profissional.",
                    "de": "Willkommen bei Kadans WASDEV, der professionellen Video-Engine.",
                    "it": "Benvenuto in Kadans WASDEV, il motore video professionale.",
                    "ru": "Добро пожаловать в Kadans WASDEV, профессиональный видеодвижок.",
                }.get(lang, "Bienvenue dans Kadans WASDEV, moteur vidéo professionnel."),
            }
        ],
    }
    return spec


def export_kadans_html(spec: dict, out_dir: Union[str, Path]) -> Path:
    """Ekspòte yon sèn Kadans an fichye HTML/CSS/JS otonòm."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    scenes = spec.get("scenes", [])
    html_scenes = [sc for sc in scenes if sc.get("type") == "html" or sc.get("html")]
    content = html_scenes[0].get("html", "") if html_scenes else "<div>Kadans Animation Export</div>"

    index_file = out / "index.html"
    index_file.write_text(content, encoding="utf-8")

    # Kreye metadata Kadans
    meta = {
        "generator": "Kadans WASDEV Video Engine",
        "title": spec.get("title", "Export"),
        "ratio": spec.get("ratio", "16:9"),
        "fps": spec.get("fps", 30),
        "scenes_count": len(scenes),
    }
    (out / "kadans_animation.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return index_file


# Aliases pou konpatibilite entèn san kase kòd
import_hyperframes = import_kadans_html
export_to_hyperframes = export_kadans_html
