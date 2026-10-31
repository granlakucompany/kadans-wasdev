"""Motè a toujou ajou: yon pwosesis ki louvri depi lontan (WASDEV, Kadans Timeline) pa janm rann ak ANSYEN kòd.

2026-10-26: yon koreksyon nan audio.py (mx_cfg) te deja sou disk, men WASDEV ak sèvè Timeline la te kenbe
ansyen modil la an memwa → chak rann te echwe nan etap «sound» epi MP4 final la pa t janm kreye.
Referans tan an pran lè pakè `kadans` la enpòte (premye bagay __init__ fè).
"""
from __future__ import annotations

import importlib
import sys
import threading
from pathlib import Path

# nan lòd depandans (sa ki enpòte lòt yo vini apre)
ENGINE_MODS = ("spec", "media", "motion", "lipsync", "sounds", "audio", "blend", "compose", "renderer")
_DIR = Path(__file__).resolve().parent
_LOCK = threading.Lock()


def _mtimes() -> dict[str, float]:
    out = {}
    for n in ENGINE_MODS:
        try:
            out[n] = (_DIR / f"{n}.py").stat().st_mtime
        except OSError:
            pass
    return out


_SEEN = _mtimes()


def changed() -> list[str]:
    """Fichye motè ki chanje sou disk depi yo te chaje."""
    now = _mtimes()
    return [n for n, t in now.items() if t > _SEEN.get(n, 0) + 0.5]


def fresh_engine() -> list[str]:
    """Rechaje modil motè yo (nan lòd) si youn chanje sou disk. Retounen sa ki rechaje (vid = deja ajou)."""
    with _LOCK:
        if not changed():
            return []
        now = _mtimes()
        done = []
        for n in ENGINE_MODS:
            m = sys.modules.get(f"kadans.{n}")
            if m is None:
                continue
            try:
                importlib.reload(m)
                done.append(n)
            except Exception:                                    # noqa: BLE001 — yon modil kase pa bloke rès la
                pass
        pkg = sys.modules.get("kadans")
        if pkg is not None:
            try:
                importlib.reload(pkg)                            # kadans.validate / build_html / render ajou tou
            except Exception:                                    # noqa: BLE001
                pass
        _SEEN.update(now)
        return done
