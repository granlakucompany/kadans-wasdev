# Sevo lokal Edite Timeline "Kadans Timeline" - 127.0.0.1 + token, Python pur (stdlib, 0 depandans).
# Sevi edite a (fichye estatik) + API moteu a. AI ak moun edite menm spec.json la (version/409).
from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import posixpath
import re
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from . import layout


from ._fresh import fresh_engine  # noqa: E402 — pa janm rann ak ansyen kòd ki rete an memwa


def reveal_in_folder(p: Path) -> bool:
    """Louvri dosye fichye a nan eksploratè sistèm nan AK fichye a deja chwazi (klik moun nan sèlman)."""
    import subprocess
    import sys
    p = Path(p).resolve()
    if not p.exists():
        return False
    try:
        if os.name == "nt":
            subprocess.Popen(["explorer", f"/select,{p}"], creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-R", str(p)])
        else:
            subprocess.Popen(["xdg-open", str(p.parent)])
        return True
    except OSError:
        return False


def _hash(spec) -> str:
    return hashlib.sha1(json.dumps(spec, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


# v3.12 — ISTORIK MONTAJ: chak vèsyon spec.json (Timeline, AI deyò, restorasyon) kopye nan .kadans-history/ anvan
# yo ranplase l. Konsa pyès chanjman pa janm pèdi, menm apre yon rechajman paj la (anvan: Ctrl+Z nan navigatè a sèlman).
HISTORY_DIR = ".kadans-history"
HISTORY_KEEP = 60
AUTHORS = {"timeline", "outside", "restore", "ids", "ai", "script"}


def write_atomic(path: Path, text: str) -> None:
    """Ekri yon fichye an yon sèl kou: fichye tanporè + os.replace. Yon lòt lektè (rann, AI, yon lòt onglet) pa janm
    wè yon spec.json mwatye ekri, menm si WASDEV fèmen nan mitan an."""
    path = Path(path)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    for i in range(5):                                   # Windows: yon lektè ka kenbe fichye a yon ti moman
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if i == 4:
                tmp.unlink(missing_ok=True)
                raise
            time.sleep(0.05 * (i + 1))


def history_add(work: Path, text: str, author: str) -> str | None:
    """Mete yon vèsyon spec.json nan istorik la (menm kontni ak dènye a → anyen). Retounen id a."""
    try:
        sp = json.loads(text)
    except ValueError:
        return None
    d = Path(work) / HISTORY_DIR
    try:
        d.mkdir(exist_ok=True)
        old = sorted(d.glob("*.json"))
        h = _hash(sp)
        if old and old[-1].stem.rsplit("-", 1)[-1] == h:
            return old[-1].stem
        author = author if author in AUTHORS else "outside"
        stamp = time.strftime("%Y%m%d-%H%M%S") + f"{int(time.time() * 1000) % 1000:03d}"
        hid = f"{stamp}-{author}-{h}"
        write_atomic(d / f"{hid}.json", text)
        for p in old[:max(0, len(old) + 1 - HISTORY_KEEP)]:
            p.unlink(missing_ok=True)
        return hid
    except OSError:
        return None


def history_list(work: Path) -> list[dict]:
    out = []
    for p in sorted((Path(work) / HISTORY_DIR).glob("*.json"), reverse=True):
        parts = p.stem.split("-")
        if len(parts) < 4:
            continue
        try:
            sp = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        sc = [s for s in (sp.get("scenes") or []) if isinstance(s, dict)]
        out.append({"id": p.stem, "time": f"{parts[0][:4]}-{parts[0][4:6]}-{parts[0][6:]} "
                                         f"{parts[1][:2]}:{parts[1][2:4]}:{parts[1][4:6]}",
                    "author": parts[2], "version": parts[3], "scenes": len(sc),
                    "tracks": len(sp.get("tracks") or []),
                    "title": str(sp.get("title") or (sc[0].get("title") if sc else "") or "")[:60]})
    return out


_BAD_ITEM = re.compile(r"^(?:scenes\[(\d+)\]\.)?(overlays\[(\d+)\]|background)\.src: ")


def _drop_bad_items(sp: dict, errors: list[str]) -> tuple[dict, list[str]]:
    """Copy of the spec without the overlay / background pictures the validator refused (a WAV dropped on the
    preview, a file that is gone). Only these media layers are dropped: any other error stays an error."""
    sp = json.loads(json.dumps(sp))
    drop: dict = {}
    dropped = []
    for e in errors:
        if "total_duration:" in e:
            if "total_duration" in sp:
                sp.pop("total_duration", None)
                dropped.append(e)
            continue
        m = _BAD_ITEM.match(e)
        if not m:
            continue
        sc = int(m.group(1)) if m.group(1) is not None else None
        drop.setdefault((sc, "background" if m.group(2) == "background" else "overlays"), set()).add(
            int(m.group(3)) if m.group(3) is not None else -1)
        dropped.append(e)
    for (sc, key), idx in drop.items():
        owner = sp if sc is None else ((sp.get("scenes") or [None] * (sc + 1))[sc] if sc < len(sp.get("scenes") or []) else None)
        if not isinstance(owner, dict):
            continue
        if key == "background":
            owner.pop("background", None)
        elif isinstance(owner.get("overlays"), list):
            owner["overlays"] = [o for j, o in enumerate(owner["overlays"]) if j not in idx]
    return sp, dropped



# Estrikti dosye (Gran Laku Company, 2026-10-20): <dosye>/Analyseur-Kadans/<pwojè> + Analyseur-Kadans/exported videos
PROJECTS_NAME = "Analyseur-Kadans"
EXPORTS_NAME = "exported videos"
LEGACY_PROJECTS, LEGACY_EXPORTS = "kadans-projects", "exported-videos"

class StudioServer:
    def __init__(self, work_dir, spec_path=None, base=None, host="127.0.0.1", port=0, editor_dir=None, tts_fn=None, audio_bridge=None, token=None):
        self.work = Path(work_dir).resolve()
        self.work.mkdir(parents=True, exist_ok=True)
        self.spec_path = Path(spec_path).resolve() if spec_path else (self.work / "spec.json")
        self.base = Path(base).resolve() if base else self.work
        self.workspace_root = self.base
        self.editor_dir = (Path(editor_dir).resolve() if editor_dir
                           else (Path(__file__).resolve().parent / "studio_editor"))
        self.token = token or secrets.token_urlsafe(16)
        self.host, self.port = host, port
        self.tts_fn = tts_fn
        self.audio_bridge = audio_bridge
        self._httpd = None
        self._lock = threading.Lock()
        self._version = 0                  # monte chak fwa spec la chanje (SSE)
        self._render = {"active": False, "done": 0, "total": 0, "info": "", "error": "", "mp4": ""}
        self._asset_cache = None
        self._audio_map = None
        self._frame_br = None
        self._frame_pg = None
        self._frame_url = None
        self._media_rev = 0                # goes up each time a media lands in medya/ (the editor polls it)
        self._build_lock = threading.RLock()
        self._compose_timer = None         # debounced composition.html rebuild after each save
        self._compose_busy = False
        self._compose_again = False
        self._build_errors: list[str] = []   # dènye build la echwe: erè spec la (editè a montre yo)
        self._build_warnings: list[str] = [] # sa build la te kite deyò (son mete kòm imaj…)
        self._disk_seen = None               # (mtime, hash) spec.json sou disk la, pou SSE
        self._built = 0                      # build ki fini (editè a rechaje aperçu a lè l chanje)
        self._last_author = "timeline"       # v3.12: kiyès ki te ekri spec.json dènye fwa (timeline / outside / restore)
        self._timing = None                  # v3.12: dire sèn dènye build la [{id, start, dur, need, measured}]

    # --------------------------------------------------------------- spec
    def load_spec(self) -> dict:
        try:
            return json.loads(self.spec_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def spec_state(self) -> dict:
        sp = self.load_spec()
        try:                                             # v3.12: sèn san id (spec AI) → id estab, sove yon fwa
            from kadans.spec import ensure_ids
            if ensure_ids(sp):
                fresh0 = self.fresh()
                with self._lock:
                    self._write_spec(sp, "ids")
                if fresh0:                               # sèlman id ajoute: composition la toujou a jou
                    os.utime(self.work / "composition.html")
        except Exception:                                # noqa: BLE001 - spec la rete jan l ye
            pass
        if self._audio_map is None and self.fresh():
            self._audio_map = self._saved_audio_map()        # composition already up to date: open instantly
        if self._audio_map is None or not (self.work / "composition.html").is_file():
            try:
                self.build(sp)
            except Exception:
                pass
            if self._audio_map is None:               # build la echwe: kenbe dènye son ki te bon yo
                self._audio_map = self._saved_audio_map() or {"voices": {}, "music": "", "mix": "", "rev": int(time.time() * 1000)}
        tot = 0.0
        try:
            from kadans.spec import total as _stot
            tot = _stot([], sp)
        except Exception:
            pass
        # embedded = louvri anndan WASDEV (pon odyo a la): lang UI a swiv lang sistèm WASDEV la, pa gen selektè
        return {"spec": sp, "version": _hash(sp), "rev": self._version, "audio": self._audio_map or {},
                "embedded": callable(self.audio_bridge), "errors": self._build_errors,
                "warnings": self._build_warnings, "timing": self._timing, "total": tot}

    def disk_version(self) -> str:
        """Hash of spec.json as it is on disk now (cached on its mtime): the editor compares it with the version it
        loaded, so a change made outside it (AI, another tab, a script) is seen within a second."""
        try:
            st = self.spec_path.stat()
            key = (st.st_mtime_ns, st.st_size)
        except OSError:
            return ""
        if self._disk_seen and self._disk_seen[0] == key:
            return self._disk_seen[1]
        try:
            text = self.spec_path.read_text(encoding="utf-8")
            sp = json.loads(text)
        except (OSError, ValueError):
            text, sp = "", {}
        h = _hash(sp)
        if self._disk_seen and self._disk_seen[1] != h:
            self.schedule_compose()                    # chanjman deyò (AI, script): aperçu a rebati tou
            if text:                                   # v3.12: chanjman deyò a antre nan istorik la tou
                history_add(self.work, text, "outside")
            self._last_author = "outside"
        self._disk_seen = (key, h)
        return h

    def _write_spec(self, spec: dict, author: str = "timeline") -> None:
        """v3.12: ekri spec.json ATOMIK, apre yon kopi vèsyon ki te la a nan istorik la (si l poko ladan l)."""
        text = json.dumps(spec, ensure_ascii=False, indent=2)
        try:
            prev = self.spec_path.read_text(encoding="utf-8")
        except OSError:
            prev = ""
        if prev:                                       # deja nan istorik la (dènye antre a) → history_add pa double l
            history_add(self.work, prev, "outside")
        write_atomic(self.spec_path, text)
        history_add(self.work, text, author)
        self._last_author = author
        try:
            write_atomic(self.work / (self.work.name + ".kadans"), text)
        except OSError:
            pass
        try:                                           # pwòp sove pa l: disk_version pa konte l kòm «deyò»
            st = self.spec_path.stat()
            self._disk_seen = ((st.st_mtime_ns, st.st_size), _hash(spec))
        except OSError:
            pass

    def save_spec(self, spec: dict, version=None, author: str = "timeline") -> dict:
        with self._lock:
            cur = _hash(self.load_spec())
            if version is not None and version != cur:
                return {"conflict": True, "current": cur}       # 409: editè a gen yon vèsyon perime
            try:
                self._write_spec(spec, author)
            except (OSError, ValueError) as e:
                return {"ok": False, "error": f"{type(e).__name__}: {e}"}
            self._version += 1
            self.schedule_compose()
            return {"ok": True, "version": _hash(spec), "rev": self._version}

    def restore_history(self, hid: str) -> dict:
        """Remete yon ansyen vèsyon kòm vèsyon AKTYÈL la (vèsyon ki te la a rete nan istorik la: pa gen anyen ki pèdi)."""
        if not re.fullmatch(r"[0-9a-z-]{10,80}", hid or ""):
            return {"ok": False, "error": "id"}
        p = self.work / HISTORY_DIR / f"{hid}.json"
        try:
            sp = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {"ok": False, "error": "not found"}
        return self.save_spec(sp, None, "restore")

    def fresh(self) -> bool:
        """composition.html (+ audio_map.json) newer than spec.json: no rebuild needed to open the project."""
        try:
            c, m = self.work / "composition.html", self.work / "audio_map.json"
            return c.is_file() and m.is_file() and c.stat().st_mtime >= self.spec_path.stat().st_mtime
        except OSError:
            return False

    def _saved_audio_map(self):
        try:
            amap = json.loads((self.work / "audio_map.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        if not isinstance(amap, dict):
            return None
        if amap.get("mix") and not (self.work / amap["mix"]).is_file():
            amap["mix"] = ""
        return amap

    def schedule_compose(self, delay: float = 1.5):
        """Autosave → composition.html is rebuilt from the spec in a background thread, debounced (one build at a
        time, the last save wins). Offline: cached voices only, never a TTS call. The editor never waits on it."""
        t = self._compose_timer
        if t is not None:
            t.cancel()
        t = threading.Timer(delay, self._compose_now)
        t.daemon = True
        self._compose_timer = t
        t.start()

    def _compose_now(self):
        if self._compose_busy:
            self._compose_again = True
            return
        self._compose_busy = True
        try:
            while True:
                self._compose_again = False
                try:
                    self.build(offline=True)
                except Exception:                                # noqa: BLE001 - next save tries again
                    pass
                if not self._compose_again:
                    break
        finally:
            self._compose_busy = False

    # --------------------------------------------------------------- media panel
    def add_media(self, src, kind: str = "") -> dict:
        """COPY a file (never moved, never trimmed) into medya/<kind>/ of the active project; the open editor's
        media panel refreshes by itself (media_rev)."""
        from . import media_preview as MP
        dst, k = MP.import_file(self.work, src, kind)
        self._media_rev += 1
        return {"ok": True, "rel": self.media_rel(dst), "name": dst.name, "kind": k, "path": str(dst)}

    @staticmethod
    def _has_sound(clean: dict, voice_map: dict, cues=None) -> bool:
        """Anything to mix? voices, music, SFX cues, track clips, scene video / voice file / sounds / ambience."""
        if voice_map or clean.get("music") or cues:
            return True
        if any((tk.get("clips") or []) for tk in (clean.get("tracks") or []) if isinstance(tk, dict)):
            return True
        for sc in clean.get("scenes") or []:
            if sc.get("type") == "video" or sc.get("voice_file") or sc.get("sounds") or sc.get("ambience") or sc.get("voice"):
                return True
        return False

    def media_cache(self) -> Path:
        return self.work / ".kadans-cache" / "thumbs"

    # --------------------------------------------------------------- pwoje
    @property
    def projects_root(self):
        if self.work.name in (PROJECTS_NAME, LEGACY_PROJECTS):
            return self.work
        return self.work.parent

    @property
    def exports_root(self):
        """MP4 final yo: <dosye pwojè yo>/exported videos (Analyseur-Kadans/exported videos — WASDEV ak repo a).
        Ansyen estrikti (kadans-projects/ + exported-videos/ akote l) toujou mache pou pwojè ki la deja."""
        if self.projects_root.name == LEGACY_PROJECTS:
            return self.projects_root.parent / LEGACY_EXPORTS
        return self.projects_root / EXPORTS_NAME

    def _safe_name(self, name):
        import re
        n = re.sub(r"[^A-Za-z0-9 _-]", "", (name or "").strip())[:60].strip()
        return n or "Pwoje"

    def _starter(self, name, ratio="16:9", lang="fr", total_duration=30.0, empty=True):
        l = lang or "fr"
        welcome_txt = {
            "ht": ("Byenveni", "Komanse", "Ann komanse"),
            "fr": ("Bienvenue", "Commencer", "Commençons"),
            "en": ("Welcome", "Get Started", "Let's start"),
            "es": ("Bienvenido", "Comenzar", "Empecemos"),
            "pt": ("Bem-vindo", "Começar", "Vamos começar"),
            "ru": ("Добро пожаловать", "Начать", "Давайте начнем"),
            "it": ("Benvenuti", "Inizia", "Iniziamo"),
            "de": ("Willkommen", "Starten", "Lass uns beginnen"),
        }.get(l, ("Byenveni", "Komanse", "Ann komanse"))
        try:
            tot_sec = max(5.0, float(total_duration if total_duration is not None else 30.0))
        except (TypeError, ValueError):
            tot_sec = 30.0
        scenes = []
        if not empty:
            d1 = round(max(2.5, tot_sec * 0.55), 1)
            d2 = round(max(2.0, tot_sec - d1), 1)
            scenes = [{"type": "hook", "id": "s1", "title": welcome_txt[0], "subtitle": name, "voice": welcome_txt[0], "duration": d1},
                       {"type": "cta", "id": "s2", "title": welcome_txt[1], "voice": welcome_txt[2], "duration": d2}]
        return {"title": name,
                "lang": l,
                "total_duration": tot_sec,
                "brand": {"name": name, "colors": {"bg": "#0b0816", "primary": "#8b5cf6", "accent": "#0098ff", "text": "#f3eefe"}},
                "ratio": ratio or "16:9", "voice": {"engine": "elevenlabs", "gender": "female", "enhance": True, "lang": l},
                "scenes": scenes,
                "tracks": []}

    def list_projects(self):
        out = []
        root = self.projects_root
        if root.is_dir():
            for d in sorted([x for x in root.iterdir() if x.is_dir()], key=lambda x: x.stat().st_mtime, reverse=True):  # sak pi nouvo anlè
                sp = d / "spec.json"
                kad = d / f"{d.name}.kadans"
                if not sp.is_file() and kad.is_file():
                    try:
                        sp.write_text(kad.read_text(encoding="utf-8"), encoding="utf-8")
                    except OSError:
                        pass
                if sp.is_file():
                    try:
                        s = json.loads(sp.read_text(encoding="utf-8"))
                    except (OSError, ValueError):
                        s = {}
                    out.append({"name": d.name,
                                "title": s.get("title") or (s.get("brand") or {}).get("name") or d.name,
                                "scenes": len(s.get("scenes") or []),
                                "active": d.resolve() == self.work})
        if self.work and self.work.is_dir() and not any(p.get("active") for p in out):
            sp = self.work / "spec.json"
            if sp.is_file():
                try:
                    s = json.loads(sp.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    s = {}
                out.insert(0, {
                    "name": self.work.name,
                    "title": s.get("title") or (s.get("brand") or {}).get("name") or self.work.name,
                    "scenes": len(s.get("scenes") or []),
                    "active": True
                })
        return out

    def media_rel(self, p) -> str:
        """Chemen yon medya pou SPEC la: relatif a BASE rann lan (WASDEV: pwojè lokal la) — konsa rann lan jwenn li.
        (Anvan: «media/x.png» relatif a dosye pwojè Kadans la → rann WASDEV la pa t jwenn li.)"""
        p = Path(p).resolve()
        for root in (self.base, self.work):
            try:
                return p.relative_to(Path(root).resolve()).as_posix()
            except ValueError:
                continue
        return str(p)

    def ensure_layout(self):
        """Estrikti pwojè a (01-senaryo, 02-storyboard, medya/vwa|mizik|sfx|imaj|videyo, Exported Videos) — toujou la."""
        try:
            if self.work != self.projects_root and (self.spec_path.is_file() or not any(self.work.iterdir())):
                layout.ensure(self.work)
        except OSError:
            pass

    def _switch(self, d):
        if self._compose_timer is not None:          # a pending autosave rebuild belongs to the old project
            self._compose_timer.cancel()
        self.work = d.resolve()
        self.work.mkdir(parents=True, exist_ok=True)
        self.spec_path = self.work / "spec.json"
        self._audio_map = None
        self._frame_pg = None
        self._frame_url = None
        self._disk_seen = None                       # v3.12: lòt pwojè a pa yon «chanjman deyò» (ni istorik «outside»)
        self._timing = None
        self._build_errors, self._build_warnings = [], []
        self._last_author = "timeline"
        self._version += 1

    def new_project(self, name, ratio="16:9", lang="fr", total_duration=30.0, empty=True):
        n = self._safe_name(name)
        d = self.projects_root / n
        k = 1
        while d.exists():
            d = self.projects_root / (n + "-" + str(k)); k += 1
        d.mkdir(parents=True, exist_ok=True)
        layout.ensure(d)
        starter = self._starter(d.name, ratio=ratio, lang=lang, total_duration=total_duration, empty=empty)
        (d / "spec.json").write_text(json.dumps(starter, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            (d / f"{d.name}.kadans").write_text(json.dumps(starter, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass
        self._switch(d)
        try:
            self.build()
        except Exception:
            pass
        return {"ok": True, "name": d.name, "total_duration": starter.get("total_duration", 30.0)}

    def open_project(self, name):
        d = self.projects_root / self._safe_name(name)
        sp = d / "spec.json"
        kad = d / f"{d.name}.kadans"
        if not sp.is_file() and kad.is_file():
            try:
                sp.write_text(kad.read_text(encoding="utf-8"), encoding="utf-8")
            except OSError:
                pass
        if not sp.is_file():
            return {"error": "pwoje pa jwenn"}
        self._switch(d)
        try:
            self.build()
        except Exception:
            pass
        return {"ok": True, "name": d.name}

    def duplicate_project(self, name, new_name=None):
        import shutil
        d = self.projects_root / self._safe_name(name)
        if not (d / "spec.json").is_file():
            return {"error": "pwoje pa jwenn"}
        base = new_name or (d.name + "-kopi")
        target = self.projects_root / self._safe_name(base)
        k = 1
        while target.exists():
            target = self.projects_root / (self._safe_name(base) + f"-{k}")
            k += 1
        shutil.copytree(d, target)
        return {"ok": True, "name": target.name}

    def delete_project(self, name):
        import shutil
        d = self.projects_root / self._safe_name(name)
        if not d.is_dir():
            return {"error": "pwoje pa jwenn"}
        if d.resolve() == self.work.resolve():
            others = [x for x in self.projects_root.iterdir() if x.is_dir() and x != d and (x / "spec.json").is_file()]
            if others:
                self._switch(others[0])
            else:
                return {"error": "pa ka efase sel pwoje ki rete a"}
        shutil.rmtree(d, ignore_errors=True)
        return {"ok": True, "active": self.work.name}

    def import_external_file(self, filename: str, content: str = "", path: str | None = None) -> dict:
        """Enpòte yon fichye ekstèn (.html, .xml, .fcpxml, .edl, .json, .kadans) kòm nouvo pwojè oswa sekans."""
        import json
        import re
        import shutil
        from pathlib import Path
        from kadans import layout

        file_p = None
        if path:
            p_cand = Path(path).resolve()
            if p_cand.is_file():
                file_p = p_cand
                if not content:
                    try:
                        content = file_p.read_text(encoding="utf-8", errors="ignore")
                    except OSError:
                        pass

        fn = filename or (file_p.name if file_p else "import")
        suf = Path(fn).suffix.lower()

        # -------------------------------------------------------------
        # 1. KADANS SPEC (.json, .kadans)
        # -------------------------------------------------------------
        if suf in (".json", ".kadans") or (content.strip().startswith("{") and '"scenes"' in content):
            try:
                sp = json.loads(content)
            except Exception as e:
                return {"error": f"Fichye JSON pa valab: {e}"}
            pname = self._safe_name(sp.get("title") or Path(fn).stem or "kadans-pwoje")
            d = self.projects_root / pname
            k = 1
            while d.exists():
                d = self.projects_root / f"{pname}-{k}"
                k += 1
            d.mkdir(parents=True, exist_ok=True)
            layout.ensure(d)
            (d / "spec.json").write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8")
            try:
                (d / f"{d.name}.kadans").write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8")
            except OSError:
                pass
            self._switch(d)
            try:
                self.build()
            except Exception:
                pass
            return {"ok": True, "name": d.name, "type": "kadans", "spec": sp}

        # -------------------------------------------------------------
        # 2. XML / TIMELINE INTERCHANGE (.xml, .fcpxml, .edl)
        # -------------------------------------------------------------
        if suf in (".xml", ".fcpxml", ".edl") or ("<xmeml" in content or "<fcpxml" in content or "TITLE:" in content):
            from .interchange import import_timeline
            try:
                sp = import_timeline(content or (str(file_p) if file_p else ""))
            except Exception as e:
                return {"error": f"Erè enpòte XML/EDL: {e}"}
            pname = self._safe_name(sp.get("title") or Path(fn).stem or "sequence-xml")
            d = self.projects_root / pname
            k = 1
            while d.exists():
                d = self.projects_root / f"{pname}-{k}"
                k += 1
            d.mkdir(parents=True, exist_ok=True)
            layout.ensure(d)
            (d / "spec.json").write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8")
            try:
                (d / f"{d.name}.kadans").write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8")
            except OSError:
                pass
            self._switch(d)
            try:
                self.build()
            except Exception:
                pass
            return {"ok": True, "name": d.name, "type": "xml", "spec": sp}

        # -------------------------------------------------------------
        # 3. HTML ANIMASYON (.html, .htm)
        # -------------------------------------------------------------
        if suf in (".html", ".htm") or ("<html" in content.lower() or "<!doctype" in content.lower() or "<div" in content.lower() or "<svg" in content.lower()):
            title_m = re.search(r"<title[^>]*>([^<]+)</title>", content, re.IGNORECASE)
            title = title_m.group(1).strip() if title_m else Path(fn).stem

            # Deteksyon dire
            dur = 10.0
            dur_m = re.search(r'''(?:name=["'](?:kadans:)?duration["']\s+content=["']([\d.]+)["']|data-duration=["']([\d.]+)["'])''', content, re.IGNORECASE)
            if dur_m:
                val = dur_m.group(1) or dur_m.group(2)
                try:
                    dur = max(1.0, float(val))
                except ValueError:
                    dur = 10.0
            else:
                css_durs = [float(x) for x in re.findall(r'''(?:animation(?:-duration)?\s*:\s*|duration\s*:\s*)([\d.]+)\s*s''', content, re.IGNORECASE)]
                if css_durs:
                    dur = max(2.0, max(css_durs))

            # Deteksyon ratio
            ratio = "16:9"
            if re.search(r'''(?:1080\s*[,x]\s*1920|9\s*:\s*16|aspect-ratio\s*:\s*9\s*/\s*16)''', content, re.IGNORECASE):
                ratio = "9:16"
            elif re.search(r'''(?:1080\s*[,x]\s*1080|1\s*:\s*1|aspect-ratio\s*:\s*1\s*/\s*1)''', content, re.IGNORECASE):
                ratio = "1:1"
            elif re.search(r'''(?:1080\s*[,x]\s*1350|4\s*:\s*5|aspect-ratio\s*:\s*4\s*/\s*5)''', content, re.IGNORECASE):
                ratio = "4:5"

            pname = self._safe_name(title or Path(fn).stem or "html-animasyon")
            d = self.projects_root / pname
            k = 1
            while d.exists():
                d = self.projects_root / f"{pname}-{k}"
                k += 1
            d.mkdir(parents=True, exist_ok=True)
            layout.ensure(d)

            # Sove fichye HTML la nan medya/html/
            html_dir = d / "medya" / "html"
            html_dir.mkdir(parents=True, exist_ok=True)
            safe_html_name = re.sub(r'[\\/*?:"<>| ]', "_", Path(fn).stem) + suf
            dst_html = html_dir / safe_html_name
            dst_html.write_text(content, encoding="utf-8")

            # Kopye fichye frè yo si sou disk
            if file_p and file_p.is_file():
                src_parent = file_p.parent
                for sibling in src_parent.iterdir():
                    if sibling.is_file() and sibling != file_p and sibling.suffix.lower() in ('.png', '.jpg', '.jpeg', '.svg', '.webp', '.css', '.js', '.woff', '.woff2', '.mp3', '.wav', '.mp4'):
                        try:
                            shutil.copy2(sibling, html_dir / sibling.name)
                        except OSError:
                            pass

            rel_path = f"medya/html/{safe_html_name}"
            sp = {
                "title": title or d.name,
                "lang": "fr",
                "total_duration": round(dur, 2),
                "brand": {
                    "name": title or d.name,
                    "font": "Inter",
                    "font_title": "Inter",
                    "font_code": "JetBrains Mono",
                    "colors": {"bg": "#0b0816", "primary": "#8b5cf6", "accent": "#0098ff", "text": "#f3eefe"}
                },
                "ratio": ratio,
                "scenes": [
                    {
                        "type": "html",
                        "id": "s1",
                        "title": title or d.name,
                        "src": rel_path,
                        "duration": round(dur, 2)
                    }
                ],
                "tracks": [
                    {
                        "id": "trk_v1",
                        "type": "video",
                        "name": "HTML Animation",
                        "clips": [
                            {
                                "id": "c_html_1",
                                "name": safe_html_name,
                                "type": "html",
                                "src": rel_path,
                                "start": 0.0,
                                "dur": round(dur, 2),
                                "duration": round(dur, 2),
                                "in": 0.0,
                                "out": round(dur, 2)
                            }
                        ]
                    }
                ]
            }

            (d / "spec.json").write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8")
            try:
                (d / f"{d.name}.kadans").write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8")
            except OSError:
                pass
            self._switch(d)
            try:
                self.build()
            except Exception:
                pass
            return {"ok": True, "name": d.name, "type": "html", "file": rel_path, "total_duration": round(dur, 2), "ratio": ratio}

        return {"error": f"Fòma fichye pa sipòte ({suf}). Chwazi .html, .xml, .fcpxml, .edl, oswa .kadans"}

    # --------------------------------------------------------------- moteu
    def _kadans(self):
        import kadans as K
        return K

    def _resolve_tts(self):
        if self.tts_fn is not None:
            return self.tts_fn
        try:
            from wasdev.app.video.studio_engine import voice_tts
            self.tts_fn = voice_tts(self.workspace_root)
        except Exception:
            try:
                from kadans.audio import default_tts
                self.tts_fn = default_tts()
            except Exception:
                self.tts_fn = None
        return self.tts_fn

    def _chat_file(self) -> Path:
        return self.work / "chat_history.json"

    def load_chat_history(self) -> list:
        p = self._chat_file()
        if p.is_file():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
            except Exception:
                pass
        return []

    def save_chat_history(self, messages: list) -> list:
        clean_msgs = [m for m in (messages or []) if isinstance(m, dict)][-200:]
        try:
            self._chat_file().write_text(json.dumps(clean_msgs, indent=2, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass
        return clean_msgs

    def handle_ai_chat(self, prompt: str, cli: str = "auto", lang: str = "fr") -> dict:
        import re
        import subprocess
        prompt = (prompt or "").strip()
        if not prompt:
            return {"ok": False, "error": "Mesaj vid"}
        msgs = self.load_chat_history()
        ts = time.strftime("%H:%M:%S")
        msgs.append({"role": "user", "text": prompt, "cli": cli, "time": ts})

        sp = self._sanitize_spec_for_build(self.load_spec())
        p_low = prompt.lower()
        spec_updated = False
        reply_lines = []

        # VRÈ AI: nan «auto» tou, chwazi premye AI CLI ki disponib la (Claude → Gemini → Codex). Si gen youn, se li
        # k ap reponn (pa fo matcher mo-kle a). Matcher la rete SÈLMAN kòm filè lè pa gen okenn vrè AI enstale.
        _exe_map = {"claude-code": ["claude", "claude-code"], "gemini": ["gemini"],
                    "antigravity": ["agy", "antigravity"], "codex": ["codex"]}
        ai_exe = ai_cli = None
        try:
            from kadans.mcp_server import _find_cli_exe
            order = ([cli] if cli not in ("auto", "kadans-ai") else ["claude-code", "gemini", "codex"])
            for _c in order:
                _e = _find_cli_exe(_exe_map.get(_c, [_c]))
                if _e and os.path.isfile(_e):
                    ai_exe, ai_cli = _e, _c
                    break
        except Exception:
            ai_exe = ai_cli = None

        # 1. Check direct ratio changes
        for r_tok in ("9:16", "16:9", "1:1", "4:5", "21:9"):
            if r_tok in p_low:
                sp["ratio"] = r_tok
                spec_updated = True
                reply_lines.append(f"📐 Fòma (Ratio) videyo a chanje an **{r_tok}**.")
                break

        # 2. Check language changes
        lang_map = {
            "kreyol": "ht", "kreyòl": "ht", "creole": "ht", "créole": "ht",
            "francais": "fr", "français": "fr", "french": "fr", "franse": "fr",
            "english": "en", "anglais": "en", "angle": "en", "anglè": "en",
            "espanol": "es", "español": "es", "spanish": "es", "espagnol": "es", "panyol": "es", "panyòl": "es",
            "portugues": "pt", "português": "pt", "portuguese": "pt", "portugais": "pt", "potige": "pt", "pòtigè": "pt",
            "deutsch": "de", "german": "de", "allemand": "de", "alman": "de",
            "italiano": "it", "italian": "it", "italien": "it", "italyen": "it",
            "russian": "ru", "russe": "ru", "русский": "ru", "ris": "ru",
        }
        for kw, lcode in lang_map.items():
            if f" an {kw}" in p_low or f" en {kw}" in p_low or f" in {kw}" in p_low:
                sp["lang"] = lcode
                sp.setdefault("voice", {})["lang"] = lcode
                spec_updated = True
                reply_lines.append(f"🌐 Lang videyo & vwa chanje an **{lcode}**.")
                break

        # 3. Check scene additions or edits from natural language
        # PA konfonn yon AJISTEMAN (vwa pi fò, volim, vitès…) ak yon kreyasyon sèn: «mete vwa a pi fò» pa dwe ajoute
        # yon sèn. (Travay 5: ranplase mo-kle sa yo ak vrè AI — isit la n anpeche fo pozitif ki pi klè yo.)
        _adjust = any(w in p_low for w in ("pi fò", "pi fo", "pi ba", "pi wo", "louder", "quieter", "pi dousman",
                                           "volim", "volume", " vwa a", " son an", "mute", "koupe son", "pi vit",
                                           "pi lan", "faster", "slower", "ralanti", "akselere"))
        if ai_exe is None and (not _adjust) and any(w in p_low for w in ("ajoute", "kreye", "mete", "add", "create",
                "nouvo sen", "nouvo sèn", " nouvelle scène", "new scene", "fe yon videyo", "fè yon videyo", "make a video")):
            scenes = list(sp.get("scenes") or [])
            sc_type = "text"
            for cand_t in ("hook", "cta", "features", "list", "stat", "code", "compare", "logo", "video", "image", "social", "chart"):
                if cand_t in p_low:
                    sc_type = cand_t
                    break
            q_match = re.findall(r'["«“]([^"»”]+)["»”]', prompt)
            title_txt = q_match[0] if q_match else prompt[:48].strip()
            sub_txt = q_match[1] if len(q_match) > 1 else (sp.get("title") or self.work.name)
            voice_txt = q_match[-1] if q_match else title_txt
            new_sc = {
                "type": sc_type,
                "id": f"{sc_type}_{len(scenes) + 1}_{int(time.time()) % 1000}",
                "title": title_txt,
                "subtitle": sub_txt,
                "voice": voice_txt,
                "duration": 3.0,
                "transition": "fade",
            }
            if sc_type in ("features", "list"):
                new_sc["items"] = [
                    {"title": title_txt, "text": sub_txt},
                    {"title": "Kalite Studio", "text": "Kadans WASDEV Video Engine"},
                    {"title": "Rann MP4 Rapid", "text": "Son ElevenLabs + FFmpeg"},
                ]
            elif sc_type == "stat":
                new_sc["value"] = "100%"
                new_sc["label"] = title_txt
            scenes.append(new_sc)
            sp["scenes"] = scenes
            spec_updated = True
            reply_lines.append(f"🎬 Sèn **{sc_type.upper()}** (`{title_txt}`) ajoute nan timeline lan avèk narasyon vwa!")

        # 4. Try external CLI if explicitly chosen and installed
        cli_output = ""
        tot_dur = float(sp.get("total_duration") or sum(float(s.get("duration") or 2.5) for s in (sp.get("scenes") or [])) or 30.0)
        dur_m = int(tot_dur) // 60
        dur_s = int(round(tot_dur - dur_m * 60))
        dur_label = f"{dur_m}m {dur_s:02d}s ({tot_dur:.1f}s)" if dur_m > 0 else f"{dur_s}s ({tot_dur:.1f}s)"
        if ai_exe is not None:                               # vrè AI (auto oswa chwazi): li reponn + ka edite spec la
            try:
                cli_prompt = (
                    f"You are editing a Kadans video spec at {self.spec_path} "
                    f"(target duration: {dur_label}, ratio: {sp.get('ratio', '16:9')}, lang: {sp.get('lang', lang)}). "
                    f"User request: {prompt}. Reply concisely in {lang}."
                )
                cmd = [ai_exe, "-p", cli_prompt] if ai_cli in ("claude-code", "gemini") else [ai_exe, cli_prompt]
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=240,
                                   cwd=str(self.work), creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                cli_output = (r.stdout or r.stderr or "").strip()[:1800]
            except Exception:
                cli_output = ""

        if spec_updated:
            self.save_spec(sp)
            try:
                self.build(sp)
            except Exception:
                pass

        if cli_output:
            reply_lines.append(cli_output)
        elif not reply_lines:
            sc_count = len(sp.get("scenes") or [])
            v_eng = (sp.get("voice") or {}).get("engine") or "elevenlabs"
            reply_lines.append(
                f"✅ **Kadans AI ({cli.upper()})** resevwa mesaj ou a.\n"
                f"• Pwojè aktif: **{sp.get('title') or self.work.name}** ({sc_count} sèn, fòma `{sp.get('ratio', '16:9')}`, dire konfigire: **{dur_label}**, vwa: `{v_eng}`).\n"
                f"• Konsèy: Ekri pa egzanp *«Ajoute yon sèn hook \"Byenveni nan Konpayi Nou\"»* oswa klike **Voye nan AI CODER WASDEV** pou AI a bati tout videyo a selon dire **{dur_label}** la!"
            )

        reply = "\n".join(reply_lines)
        msgs.append({"role": "assistant", "text": reply, "cli": cli, "time": time.strftime("%H:%M:%S"), "spec_updated": spec_updated})
        self.save_chat_history(msgs)
        return {"ok": True, "reply": reply, "spec_updated": spec_updated, "spec": sp, "messages": msgs}

    def _sanitize_spec_for_build(self, sp: dict) -> dict:
        valid_tr = {"none", "fade", "slide", "slideright", "slideup", "slidedown", "wipe", "wipeup", "zoom", "zoomout", "flip", "rotate", "blur"}
        if not isinstance(sp, dict):
            sp = {}
        out = dict(sp)
        out["kadans"] = 1
        out["title"] = out.get("title") or self.work.name
        out["lang"] = out.get("lang") or "fr"
        out["ratio"] = out.get("ratio") or "16:9"
        out["fps"] = int(out.get("fps") or 30)
        top_t = str(out.get("transition") or "").lower().strip()
        if top_t and top_t not in valid_tr:
            out["transition"] = "fade"
        scenes = []
        for i, sc in enumerate(out.get("scenes") or []):
            if not isinstance(sc, dict):
                continue
            scc = dict(sc)
            if not scc.get("type"):
                scc["type"] = "text"
            tval = str(scc.get("transition") or "").lower().strip()
            if tval and tval not in valid_tr:
                scc["transition"] = "fade"
            scenes.append(scc)
        # blank project: kenbe scenes = [] vid nèt
        out["scenes"] = scenes
        td = out.get("total_duration")
        if td is not None and scenes:
            try:
                td_val = float(td)
                fixed_dur = sum(float(sc.get("duration") or 0) for sc in scenes if sc.get("duration"))
                if fixed_dur > td_val:
                    out["total_duration"] = round(fixed_dur, 2)
            except (ValueError, TypeError):
                out.pop("total_duration", None)
        return out

    def _fallback_composition_html(self, clean: dict) -> str:
        title = clean.get("title") or "Kadans Studio"
        return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
html,body{{margin:0;width:100%;height:100%;background:#090614;display:flex;align-items:center;justify-content:center;color:#fff;font-family:system-ui,sans-serif;overflow:hidden}}
#stage{{width:90%;max-width:960px;aspect-ratio:16/9;background:#150f28;border:2px solid #3b1d70;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,0.5)}}
h1{{font-size:26px;color:#a78bfa;margin:0 0 8px}}
p{{color:#c4b5fd;font-size:14px;margin:0}}
</style></head><body>
<div id="stage">
  <h1>{title}</h1>
  <p>Aper\u00e7u Kadans Studio pare</p>
</div>
<script>
window.__kadans = {{w: 1920, h: 1080, fps: 30, total: 5, scenes: [{{id: "sc0", spec_index: 0, start: 0, dur: 5}}]}};
const EDTARGET = window.parent !== window ? window.parent : window;
function post(m) {{ try {{ EDTARGET.postMessage(m, "*"); }} catch (e) {{}} }}
window.addEventListener("message", e => {{
  const m = e.data || {{}};
  if (m.cmd === "seek") post({{ evt: "time", t: +m.t || 0 }});
}});
post({{ evt: "ready", kadans: window.__kadans }});
</script></body></html>"""

    def build(self, spec=None, offline: bool = False, mix: bool = True) -> dict:
        """spec.json -> composition.html + audio. offline=True (autosave / fast open): cached voices only, no host
        callback. mix=False: no FFmpeg preview soundtrack (the host runs a full build right after)."""
        with self._build_lock:
            return self._build(spec, offline, mix)

    def _validate_repaired(self, K, sp: dict) -> tuple[dict, list[str]]:
        """Validate the spec for a build. An item the editor could not have meant (a sound dropped as an overlay /
        background picture, a missing file…) is left out of THIS build and reported - the spec on disk is never
        touched. Returns (clean spec, warnings); raises SpecError when the spec still has errors after that."""
        sp = self._sanitize_spec_for_build(sp)
        warnings: list[str] = []
        for _ in range(3):
            try:
                return K.validate(sp), warnings
            except K.SpecError as e:
                errs = list(getattr(e, "errors", None) or [str(e)])
                sp, dropped = _drop_bad_items(sp, errs)
                if not dropped:
                    raise
                warnings += dropped
        return K.validate(sp), warnings

    def _build(self, spec=None, offline: bool = False, mix: bool = True) -> dict:
        K = self._kadans()
        from kadans import audio, media
        # v3.10: dosye pwojè a FIKSE pou tout build la. Anvan, chanje pwojè nan Timeline pandan yon build (~30 s)
        # te fè vwa / composition / mix ansyen pwojè a tonbe nan nouvo a (vwa Nova Fold nan tutoryèl la).
        work, spec_path = self.work, self.spec_path
        if spec is not None:
            sp = spec
        else:
            try:
                sp = json.loads(spec_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                sp = {}
        self.ensure_layout()
        try:
            clean, self._build_warnings = self._validate_repaired(K, sp)
            self._build_errors = []
        except Exception as e:                       # noqa: BLE001
            # RÈG (devlopè a, 2026-10-20): yon erè nan spec la PA JANM ranplase montaj la ak yon pwojè egzanp
            # (anvan: «Bienvenue / Commençons» te pran plas 17 sèn yo san okenn mesaj). Dènye composition.html ki
            # bon an rete, erè yo ale nan editè a (bann wouj) pou moun nan oswa AI a korije yo.
            errs = list(getattr(e, "errors", None) or [f"{type(e).__name__}: {e}"])
            has_scenes = isinstance(sp, dict) and any(isinstance(s, dict) for s in (sp.get("scenes") or []))
            has_tracks = isinstance(sp, dict) and any((t.get("clips") or []) for t in (sp.get("tracks") or []))
            if has_scenes or has_tracks:
                self._build_errors = errs
                return {"ok": False, "errors": errs}
            self._build_errors = []
            try:
                clean = K.validate(self._starter(work.name, empty=True))
            except Exception:
                clean = {"kadans": 1, "title": work.name, "scenes": [], "w": 1920, "h": 1080, "fps": 30, "ratio": "16:9", "lang": "fr", "brand": {"name": work.name, "colors": {"primary": "#8b5cf6", "accent": "#0098ff"}, "font_title": "Inter"}, "credit": True}

        cache_root = self.base / ".kadans-cache"
        if not cache_root.exists() and (self.workspace_root / ".wasdev" / "kadans-cache").exists():
            cache_root = self.workspace_root / ".wasdev" / "kadans-cache"
        try:
            media_s, clips = media.prepare(clean, self.base, cache_root / "clips")
        except Exception:
            media_s, clips = {}, {}
        voice_map = {}
        try:
            voice_map = audio.voices(clean, layout.voices_dir(work), self._resolve_tts(), offline=offline)
        except Exception:
            voice_map = {}
        try:                                         # vwa pre-anrejistre (voice_file): vrè dire + lè mo yo, kou rann lan
            voice_map.update(audio.voice_files(clean, self.work))
            voice_map.update(audio.voice_files(clean, self.base))
        except Exception:
            pass
        try:
            words_s = audio.word_times(clean, voice_map, layout.voices_dir(work)) if voice_map else None
        except Exception:
            words_s = None
        try:
            tl = K.timeline(clean, audio.voice_seconds(voice_map) if voice_map else None, media_s, words_s)
        except Exception:
            tl = []
        tot = K.total(tl, clean)
        if self.work == work:                        # v3.12: editè a konnen vrè dire yo depi l louvri (pa 2 s)
            self._timing = [{k: x.get(k) for k in ("id", "start", "dur", "need", "measured")} for x in tl]
        try:                                         # son aperçu WASDEV la (preview-sounds.m4a) RETE nan composition.html
            pa_ = "preview-sounds.m4a" if (work / "preview-sounds.m4a").is_file() else None
            html = __import__("kadans.compose", fromlist=["build_html"]).build_html(clean, tl, self.base, clips, work, pa_)
        except Exception:
            html = self._fallback_composition_html(clean)
        (work / "composition.html").write_text(html, encoding="utf-8")
        amap = {"voices": {}, "music": "", "mix": "", "rev": int(time.time() * 1000)}
        for sc in tl:
            sid = sc.get("id")
            vp = voice_map.get(sid)
            if vp and Path(vp).is_file():
                try:
                    rel_v = Path(vp).resolve().relative_to(work).as_posix()
                except ValueError:
                    rel_v = Path(vp).name
                if sid:
                    amap["voices"][sid] = rel_v
                if sc.get("spec_index") is not None:
                    amap["voices"][str(sc.get("spec_index"))] = rel_v
        # v3.89: fiks vwa ElevenLabs nan spec.json pou refresh browser pa janm pedi li
        try:
            sp_updated = False
            for s in sp.get("scenes", []):
                sid = s.get("id")
                vf = s.get("voice_file")
                vp = voice_map.get(sid)
                if sid and sid in amap["voices"] and not vf:
                    s["voice_file"] = self.media_rel(vp) if vp else amap["voices"][sid]
                    sp_updated = True
                elif vf:
                    vf_p = self.work / vf
                    if not (self.base / vf).is_file() and vf_p.is_file():
                        s["voice_file"] = self.media_rel(vf_p)
                        sp_updated = True
            if sp_updated:
                (work / "spec.json").write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8")
                try:
                    (work / f"{work.name}.kadans").write_text(json.dumps(sp, ensure_ascii=False, indent=2), encoding="utf-8")
                except OSError:
                    pass
        except Exception:
            pass
        try:
            if clean.get("music") and not (clean["music"].get("file")):
                mp = audio.music_loop(clean["music"].get("mood", "upbeat"), int(clean["music"].get("seed", 0) or 0), layout.music_dir(work))
            else:
                mp = None
            if mp and Path(mp).is_file():
                try:
                    amap["music"] = Path(mp).resolve().relative_to(work).as_posix()
                except ValueError:
                    amap["music"] = Path(mp).name
        except Exception:
            mp = None
        try:                                         # menm SFX otomatik ak rann final la (renderer.py)
            from kadans.compose import events as _events
            cues = _events(clean, tl) if clean.get("sfx") else None
        except Exception:
            cues = None
        if not mix:
            pass
        elif not self._has_sound(clean, voice_map, cues):  # nothing to hear (blank project): no FFmpeg mix (~2 s)
            try:
                (work / "preview-audio.wav").unlink(missing_ok=True)   # never replay an old soundtrack
            except OSError:
                pass
        else:
          try:
            mix_p = work / "preview-audio.wav"
            audio.mix(clean, tl, tot, mix_p, self.base, voice_map, cache_root, cues)
            if mix_p.is_file():
                amap["mix"] = "preview-audio.wav"
                try:                                     # composition.html louvri poukont li (onglet) jwe mix la tou
                    (work / "composition.html").write_text(
                        __import__("kadans.compose", fromlist=["build_html"]).build_html(
                            clean, tl, self.base, clips, work, "preview-audio.wav"), encoding="utf-8")
                except Exception:
                    pass
          except Exception:
            pass
        if self.work == work:                        # pwojè a pa chanje pandan build la
            self._audio_map = amap
        try:
            (work / "audio_map.json").write_text(json.dumps(amap, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass
        if callable(self.audio_bridge) and not offline:
            try:
                self.audio_bridge({"cmd": "built", "work": str(work), "mix": str(work / "preview-audio.wav")})
            except Exception:
                pass
        self._frame_pg = None
        self._frame_url = None
        if self.work == work:
            self._built += 1
        return {"ok": True, "total": tot, "html": "composition.html", "audio": amap, "built": self._built,
                "timing": [{k: x.get(k) for k in ("id", "start", "dur", "need", "measured")} for x in tl]}

    def capture_frame(self, t: float, w: int = 1920, h: int = 1080, out_file: Path | None = None) -> Path:
        with self._lock:
            comp = self.work / "composition.html"
            if not comp.is_file():
                self.build()
            url = comp.resolve().as_uri() + "#render"

            if self._frame_br is None or (self._frame_br.proc and self._frame_br.proc.poll() is not None):
                from kadans.cdp import Browser
                self._frame_br = Browser(no_gpu=True)
                self._frame_pg = None
                self._frame_url = None

            if self._frame_pg is None or self._frame_url != url:
                try:
                    self._frame_pg = self._frame_br.pages(url, 1, w, h)[0]
                    self._frame_url = url
                except Exception:
                    try:
                        self._frame_br.close()
                    except Exception:
                        pass
                    from kadans.cdp import Browser
                    self._frame_br = Browser(no_gpu=True)
                    self._frame_pg = self._frame_br.pages(url, 1, w, h)[0]
                    self._frame_url = url

            from kadans.cdp import screenshot
            self._frame_pg.eval(f"window.__seek({max(0.0, float(t)):.4f})")
            data = screenshot(self._frame_pg, w, h, "png")
            if out_file is None:
                fdir = self.work / "frames"
                fdir.mkdir(parents=True, exist_ok=True)
                out_file = fdir / ("frame-%.2f.png" % t)
            else:
                out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_bytes(data)
            return out_file

    def safe_path(self, rel: str):
        if not rel:
            return None
        rel_clean = posixpath.normpath("/" + rel.replace("\\", "/")).lstrip("/")
        for root in (self.work, self.base, self.workspace_root):
            if not root:
                continue
            p = (root / rel_clean).resolve()
            try:
                p.relative_to(root.resolve())
                if p.is_file() and not p.is_symlink():
                    return p
            except ValueError:
                continue
        return None

    def editor_path(self, rel: str):
        if not self.editor_dir:
            return None
        rel = posixpath.normpath("/" + rel).lstrip("/")
        q = (self.editor_dir / rel).resolve()
        try:
            q.relative_to(self.editor_dir)
        except ValueError:
            return None
        return q

    # ------------------------------------------------------------- asset yo (10k design SVG)
    @property
    def assets_dir(self):
        return Path(__file__).resolve().parent.parent / "assets"

    def asset_index(self):
        if self._asset_cache is None:
            root = self.assets_dir
            items = []
            if root.is_dir():
                exts = (".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm", ".mov", ".wav", ".mp3", ".m4a", ".ogg")
                for f in root.rglob("*"):
                    if f.is_file() and f.suffix.lower() in exts:
                        rel = f.relative_to(root).as_posix()
                        parts = rel.split("/")
                        cat = "/".join(parts[1:-1]) if len(parts) > 2 else (parts[0] if len(parts) > 1 else "")
                        items.append((rel, cat, f.suffix.lower().lstrip(".")))
            items.sort(key=lambda x: x[0].lower())
            self._asset_cache = items
        return self._asset_cache

    def asset_file(self, rel: str):
        rel = posixpath.normpath("/" + rel).lstrip("/")
        q = (self.assets_dir / rel).resolve()
        try:
            q.relative_to(self.assets_dir.resolve())
        except ValueError:
            return None
        return q if q.is_file() and not q.is_symlink() else None

    def url(self) -> str:
        return f"http://{self.host}:{self.port}/?token={self.token}"

    def start(self):
        srv = self
        httpd = _Server((self.host, self.port), _Handler)
        httpd.studio = srv                                       # type: ignore[attr-defined]
        self.port = httpd.server_address[1]
        self._httpd = httpd
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        return self.url()

    def stop(self):
        if self._frame_br:
            try:
                self._frame_br.close()
            except Exception:
                pass
            self._frame_br = None
            self._frame_pg = None
            self._frame_url = None
        if self._httpd:
            self._httpd.shutdown()
            self._httpd = None


class _Server(ThreadingHTTPServer):
    """HTTPServer.server_bind() calls socket.getfqdn() (reverse DNS): 2-4 s on some Windows networks before the
    editor could even open. 127.0.0.1 never needs it."""
    daemon_threads = True

    def server_bind(self):
        import socketserver
        socketserver.TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name, self.server_port = host, port

    def handle_error(self, request, client_address):
        """Onglè preview la fèmen / rechaje → koneksyon keep-alive la fèmen pandan sèvè a ap li pwochen demann lan
        (WinError 10053/10054). Sa PA yon erè: pa enprime traceback la (li te fè bri nan jounal la pou granmesi)."""
        import sys
        e = sys.exc_info()[1]
        if isinstance(e, (ConnectionError, BrokenPipeError)) or \
                (isinstance(e, OSError) and getattr(e, "winerror", None) in (10053, 10054, 10038, 10058)):
            return
        super().handle_error(request, client_address)


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    @property
    def S(self) -> StudioServer:
        return self.server.studio                                # type: ignore[attr-defined]

    def _authed(self, q) -> bool:
        tok = (q.get("token", [""])[0] or self.headers.get("X-Kadans-Token", ""))
        return secrets.compare_digest(tok, self.S.token)

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except ValueError:
            return {}

    def _upload(self, q):
        name = (q.get("name", ["medya"])[0] or "medya").replace("\\", "/").rsplit("/", 1)[-1][-120:] or "medya"
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > 8 * 1024 * 1024 * 1024:
            return self._json({"error": "fichye vid oswa two gwo"}, 400)
        hint = q.get("kind", [""])[0] or ""
        if hint:
            kind = layout.kind_of(name, hint)
        else:                                            # no hint: name / folder decide (vwa, mizik, sfx...)
            from . import media_preview
            kind = media_preview.import_kind(name)
        mdir = layout.media_dir(self.S.work, kind)       # medya/<kalite>/ (vwa, mizik, sfx, imaj, videyo)
        dst = layout.unique(mdir, layout.clean_filename(Path(name).stem, Path(name).suffix.lower()))
        tmp = dst.with_name(dst.stem + ".part" + dst.suffix)
        left = n
        with open(tmp, "wb") as fh:                      # streamed to disk (big videos never sit in RAM)
            while left > 0:
                chunk = self.rfile.read(min(left, 1 << 20))
                if not chunk:
                    break
                fh.write(chunk)
                left -= len(chunk)
        if left:
            tmp.unlink(missing_ok=True)
            return self._json({"error": "upload interrupted"}, 400)
        tmp.replace(dst)
        self.S._media_rev += 1
        return self._json({"ok": True, "rel": self.S.media_rel(dst), "name": dst.name, "kind": kind})

    # ------------------------------------------------------------- GET
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        path = unquote(u.path)
        if path.startswith("/api/"):
            if not self._authed(q):
                return self._json({"error": "forbidden"}, 403)
            if path == "/api/remotion/status":
                try:
                    from wasdev.app.video.remotion_server import is_remotion_installed, RemotionServerManager, find_node
                    rem_dir = self.S.work / "remotion"
                    installed = is_remotion_installed(rem_dir)
                    mgr = RemotionServerManager.get_instance()
                    running = mgr.is_running(rem_dir)
                    info = mgr.get_server_info(rem_dir) or {}
                    return self._json({
                        "ok": True,
                        "node": bool(find_node()),
                        "installed": installed,
                        "running": running,
                        "url": info.get("url", ""),
                        "port": info.get("port", 3333),
                    })
                except Exception as e:
                    return self._json({"ok": False, "installed": False, "error": str(e)})
            if path == "/api/spec":
                return self._json(self.S.spec_state())
            if path == "/api/peaks":
                from kadans import audio
                f = self.S.safe_path(q.get("file", [""])[0])
                return self._json({"peaks": audio.peaks(f) if f and f.is_file() else []})
            if path == "/api/status":
                return self._sse()
            if path == "/api/disk":                       # editè a poll sa (1-2 s): chanjman deyò + erè build
                S = self.S
                return self._json({"disk": S.disk_version(), "errors": S._build_errors,
                                   "warnings": S._build_warnings, "built": S._built, "author": S._last_author})
            if path == "/api/history":                    # v3.12: tout vèsyon montaj la (kiyès, kilè)
                return self._json({"ok": True, "items": history_list(self.S.work)})
            if path == "/api/assets":
                idx = self.S.asset_index()
                cat = (q.get("cat", [""])[0] or "").strip()
                term = (q.get("q", [""])[0] or "").strip().lower()
                off = int(q.get("offset", ["0"])[0] or 0)
                lim = min(400, int(q.get("limit", ["120"])[0] or 120))
                cats = sorted({c for _, c, _ in idx if c})
                sel = [it for it in idx if (not cat or it[1] == cat or it[1].startswith(cat + "/")) and (not term or term in it[0].lower())]
                page = [{"path": r, "cat": c, "ext": e} for r, c, e in sel[off:off + lim]]
                return self._json({"cats": cats, "items": page, "total": len(sel)})
            if path == "/api/sounds":                     # bibliyotèk son CC0 (panèl SFX la)
                from kadans import sounds as SO
                term = (q.get("q", [""])[0] or "").strip()
                hits = SO.search(term, limit=80) if term else SO.library()
                return self._json({"items": [{"id": e["id"], "kind": e.get("kind"), "loop": bool(e.get("loop")),
                                              "dur": e.get("dur"), "tags": (e.get("tags") or [])[:8],
                                              "author": e.get("author", ""), "n": len(e["files"])} for e in hits],
                                   "total": len(SO.library())})
            if path == "/api/html":
                f = self.S.work / "composition.html"
                return self._json({"ok": f.is_file(), "html": f.read_text(encoding="utf-8") if f.is_file() else ""})
            if path == "/api/projects":
                return self._json({"active": self.S.work.name, "projects": self.S.list_projects()})
            if path == "/api/montage":                    # MONTAJ AN DIRÈK: plan AI a (yon sèl fwa, apre sa efase)
                mf = self.S.work / ".kadans-montage.json"
                try:
                    plan = json.loads(mf.read_text(encoding="utf-8")) if mf.is_file() else {}
                except (OSError, ValueError):
                    plan = {}
                try:
                    mf.unlink(missing_ok=True)
                except OSError:
                    pass
                return self._json(plan if isinstance(plan, dict) else {})
            if path == "/api/media":
                items = [dict(it, rel=self.S.media_rel(self.S.work / it["rel"])) for it in layout.list_media(self.S.work)]
                return self._json({"media": items, "kinds": list(layout.KINDS), "rev": self.S._media_rev,
                                   "project": self.S.work.name})
            if path == "/api/media-rev":                  # cheap poll: the media panel refreshes when it moves
                return self._json({"rev": self.S._media_rev, "project": self.S.work.name})
            if path in ("/api/thumb", "/api/media-info", "/api/preview-audio"):  # media panel: frame / length / sound
                from . import media_preview
                f = self.S.safe_path(q.get("file", [""])[0])
                if not f:
                    return self._json({"error": "not found"}, 404)
                if path == "/api/media-info":
                    return self._json(media_preview.info(f, self.S.media_cache()))
                if path == "/api/preview-audio":
                    pw = media_preview.preview_wav(f, self.S.media_cache())
                    return self._serve_file(pw) if pw else self._json({"error": "no preview"}, 404)
                t = media_preview.thumb(f, self.S.media_cache())
                if t is None:
                    return self._json({"error": "no thumbnail"}, 404)
                return self._serve_file(t)
            if path == "/api/fonts":
                try:
                    from kadans import fonts
                    names = [f.get("family") for f in fonts.families() if f.get("family")]
                except Exception:                                # noqa: BLE001
                    names = []
                return self._json({"fonts": names})
            if path == "/api/audio-map":
                if self.S._audio_map is None:
                    self.S.spec_state()
                return self._json({"ok": True, "audio": self.S._audio_map or {}})
            if path == "/api/audio-settings":
                try:
                    from wasdev.app import settings as wset
                    in_id = wset.get("audio/input") or wset.get("voice/input") or ""
                    in_name = wset.get("audio/input_name") or wset.get("rec/mic") or ""
                    out_id = wset.get("audio/output") or wset.get("voice/output") or ""
                    out_name = wset.get("audio/output_name") or ""
                except Exception:
                    in_id, in_name, out_id, out_name = "", "", "", ""
                return self._json({
                    "ok": True,
                    "input": {"id": in_id, "name": in_name},
                    "output": {"id": out_id, "name": out_name},
                })
            if path == "/api/settings":
                from kadans.audio import ELEVENLABS_VOICES, load_kadans_settings
                from kadans.mcp_server import detect_ai_clis
                try:
                    from wasdev.app import settings as wset
                    in_id = wset.get("audio/input") or wset.get("voice/input") or ""
                    in_name = wset.get("audio/input_name") or wset.get("rec/mic") or ""
                    out_id = wset.get("audio/output") or wset.get("voice/output") or ""
                    out_name = wset.get("audio/output_name") or ""
                except Exception:
                    in_id, in_name, out_id, out_name = "", "", "", ""
                return self._json({
                    "ok": True,
                    "settings": load_kadans_settings(),
                    "voices": ELEVENLABS_VOICES,
                    "clis": detect_ai_clis(),
                    "audio_in": {"id": in_id, "name": in_name},
                    "audio_out": {"id": out_id, "name": out_name},
                })
            if path == "/api/ai/status":
                from kadans.audio import load_kadans_settings
                from kadans.mcp_server import detect_ai_clis
                return self._json({"ok": True, "clis": detect_ai_clis(), "settings": load_kadans_settings()})
            if path == "/api/ai/history":
                return self._json({"ok": True, "messages": self.S.load_chat_history()})
            if path == "/api/render-status":
                return self._json({"ok": True, "render": self.S._render})
            if path == "/api/download-render":
                cf = self.S.work / f"{self.S.work.name}.mp4"      # ansyen pwojè: MP4 nan rasin lan
                if self.S._render.get("mp4"):
                    p = Path(self.S._render["mp4"])
                    if p.is_file():
                        cf = p
                if cf.is_file():
                    if q.get("inline"):                          # lektè aperçu a: streaming + Range (chèche nan videyo a)
                        return self._serve_file(cf)
                    return self._serve_download(cf, cf.name)
                return self._json({"error": "Fichye MP4 pa jwenn"}, 404)
            return self._json({"error": "unknown"}, 404)
        # fichye estatik (edite index + composition + vendor + media) - limite nan work dir
        if path in ("/", "/index.html"):
            return self._serve_index()
        if path in ("/favicon.ico", "/favicon.svg", "/wasdev-icon.svg"):
            return self._serve_favicon()
        norm_p = path.strip("/").split("?")[0]
        if norm_p == "composition.html":
            cf = self.S.work / "composition.html"
            if not cf.is_file():
                try:
                    self.S.build()
                except Exception:
                    pass
            if cf.is_file():
                return self._serve_file(cf)
            return self._serve_preview_fallback()
        ep = self.S.editor_path(path)
        if ep and ep.is_file():                          # asset editè a (editor.js, elatriye)
            return self._serve_file(ep)
        if path.startswith("/sfxlib/"):                  # tande yon son CC0 nan panèl la (premye varyant)
            from kadans import sounds as SO
            e = SO.by_id(path[len("/sfxlib/"):].strip("/"))
            if e:
                return self._serve_file(e["files"][0])
        if path.startswith("/assets/"):                  # 10k design asset yo (drag-and-drop)
            af = self.S.asset_file(path[len("/assets/"):])
            if af:
                return self._serve_file(af)
        p = self.S.safe_path(path)
        if p and p.is_file():                            # composition.html + vendor + media (dosye pwojè a)
            return self._serve_file(p)
        return self._json({"error": "not found"}, 404)

    def do_POST(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._authed(q):
            return self._json({"error": "forbidden"}, 403)
        if u.path == "/api/upload":
            return self._upload(q)
        b = self._body()
        try:
            if u.path == "/api/media/add":               # a file of the host project (WASDEV tree drop / menu)
                src = Path(str(b.get("path") or ""))
                if not src.is_absolute():
                    src = self.S.base / src
                src = src.resolve()
                inside = False
                for root in (self.S.base, self.S.workspace_root, self.S.work):
                    try:
                        src.relative_to(Path(root).resolve())
                        inside = True
                        break
                    except ValueError:
                        continue
                if not inside or not src.is_file():          # only files of the open project, never elsewhere
                    return self._json({"error": "fichye a pa nan pwojè a"}, 403)
                return self._json(self.S.add_media(src, str(b.get("kind") or "")))
            if u.path == "/api/audio-settings":
                try:
                    from wasdev.app.ai.voice import set_official_audio_input, set_official_audio_output
                    in_id = str(b.get("input_id") or "").strip()
                    in_name = str(b.get("input_name") or "").strip()
                    out_id = str(b.get("output_id") or "").strip()
                    out_name = str(b.get("output_name") or "").strip()
                    if in_id or in_name:
                        set_official_audio_input(in_id, in_name)
                    if out_id or out_name:
                        set_official_audio_output(out_id, out_name)
                except Exception as e:
                    return self._json({"ok": False, "error": str(e)}, 500)
                return self._json({
                    "ok": True,
                    "input": {"id": in_id, "name": in_name},
                    "output": {"id": out_id, "name": out_name},
                })
            if u.path == "/api/settings":
                from kadans.audio import save_kadans_settings
                cfg = save_kadans_settings(b)
                # Reset cached tts_fn so new ElevenLabs key/voice takes effect immediately
                self.S.tts_fn = None
                try:
                    from wasdev.app import settings as wset
                    from wasdev.app.ai.voice import set_official_audio_input, set_official_audio_output
                    if b.get("elevenlabs_api_key"):
                        wset.put("elevenlabs/api_key", str(b["elevenlabs_api_key"]).strip())
                    if b.get("voice_engine"):
                        wset.put("voice/engine", str(b["voice_engine"]).strip())
                    if b.get("audio_input_id") or b.get("audio_input_name"):
                        set_official_audio_input(str(b.get("audio_input_id") or ""), str(b.get("audio_input_name") or ""))
                    if b.get("audio_output_id") or b.get("audio_output_name"):
                        set_official_audio_output(str(b.get("audio_output_id") or ""), str(b.get("audio_output_name") or ""))
                except Exception:
                    pass
                return self._json({"ok": True, "settings": cfg})
            if u.path == "/api/elevenlabs/test":
                from kadans.audio import elevenlabs_synthesize, save_kadans_settings
                if b.get("api_key"):
                    save_kadans_settings({"elevenlabs_api_key": str(b["api_key"]).strip()})
                txt = (b.get("text") or "Bonjou! Vwa ElevenLabs aktif nan Kadans Timeline.").strip()
                gender = (b.get("gender") or "female").strip()
                vid = (b.get("voice_id") or "").strip() or None
                vdir = layout.voices_dir(self.S.work)
                out_w = vdir / "test-elevenlabs.wav"
                ok_el = elevenlabs_synthesize(txt, out_w, lang=b.get("lang") or "fr", gender=gender,
                                              voice_id=vid, api_key=b.get("api_key"), model_id=b.get("model"))
                if not ok_el:
                    return self._json({"ok": False, "error": "ElevenLabs pa ka pale (tcheke kle oswa kredi nan AI Hub).", "engine": "elevenlabs"})
                return self._json({"ok": True, "engine": "elevenlabs", "rel": self.S.media_rel(out_w)})
            if u.path == "/api/ai/setup-all":
                from kadans.mcp_server import install_all
                return self._json(install_all())
            if u.path == "/api/ai/history":
                if b.get("clear"):
                    self.S.save_chat_history([])
                    return self._json({"ok": True, "messages": []})
                msgs = self.S.save_chat_history(b.get("messages") or [])
                return self._json({"ok": True, "messages": msgs})
            if u.path == "/api/ai/chat":
                return self._json(self.S.handle_ai_chat(b.get("prompt") or "", cli=b.get("cli") or "auto", lang=b.get("lang") or "fr"))
            if u.path == "/api/audio-bridge":
                res = {"ok": True, "work": str(self.S.work), "mix": str(self.S.work / "preview-audio.wav")}
                if callable(self.S.audio_bridge):
                    try:
                        payload = dict(b)
                        payload["work"] = str(self.S.work)
                        payload["mix"] = str(self.S.work / "preview-audio.wav")
                        br = self.S.audio_bridge(payload)
                        if isinstance(br, dict):
                            res.update(br)
                    except Exception as ex:
                        res["bridge_error"] = str(ex)[:200]
                return self._json(res)
            if u.path == "/api/send-to-chat":
                sp = self.S.load_spec()
                title = b.get("title") or sp.get("title") or self.S.work.name
                comp = self.S.work / "composition.html"
                spec_p = self.S.work / "spec.json"
                mp4 = self.S.work.parent / f"{self.S.work.name}.mp4"
                target = mp4 if mp4.is_file() else (comp if comp.is_file() else spec_p)
                res = {"ok": True, "title": title, "path": str(target)}
                if callable(self.S.audio_bridge):
                    try:
                        self.S.audio_bridge({
                            "cmd": "send_to_chat",
                            "title": title,
                            "path": str(target),
                            "url": f"http://{self.S.host}:{self.S.port}/?token={self.S.token}",
                        })
                    except Exception as ex:
                        res["bridge_error"] = str(ex)[:200]
                return self._json(res)
            K = self.S._kadans()
            if u.path == "/api/validate":
                try:
                    K.validate(b.get("spec") or {})
                    return self._json({"ok": True, "errors": []})
                except K.SpecError as e:
                    return self._json({"ok": False, "errors": e.errors})
            if u.path == "/api/lint":
                from kadans.lint import lint
                return self._json(lint(K.validate(b.get("spec") or {}), self.S.base))
            if u.path == "/api/build":
                return self._json(self.S.build(b.get("spec")))
            if u.path == "/api/history/restore":
                return self._json(self.S.restore_history(str(b.get("id") or "")))
            if u.path == "/api/export":
                from .export import export_html
                out = self.S.work / "export.html"
                export_html(b.get("spec") or self.S.load_spec(), out, self.S.base)
                try:
                    import shutil
                    dst = layout.renders_dir(self.S.work) / (self.S.work.name + ".html")
                    shutil.copy2(out, dst)
                    return self._json({"ok": True, "file": "export.html", "exported": str(dst)})
                except OSError:
                    return self._json({"ok": True, "file": "export.html"})
            if u.path == "/api/interchange/export":
                from .interchange import export_timeline
                fmt = str(b.get("format") or "fcpxml").lower()
                ext = ".xml" if fmt in ("fcpxml", "xml") else ".edl"
                out_name = f"{self.S.work.name}{ext}"
                out_file = self.S.work / out_name
                sp = b.get("spec") or self.S.load_spec()
                res_content = export_timeline(sp, fmt=fmt, out_path=out_file, base=self.S.base)
                return self._json({"ok": True, "format": fmt, "file": out_name, "path": str(out_file), "length": len(res_content)})
            if u.path == "/api/interchange/import":
                from .interchange import import_timeline
                content = b.get("content") or ""
                p_arg = b.get("path")
                if p_arg:
                    src_p = Path(p_arg) if Path(p_arg).is_absolute() else self.S.base / p_arg
                    if src_p.is_file():
                        content = src_p.read_text(encoding="utf-8", errors="ignore")
                if not content:
                    return self._json({"error": "Pa gen kontni ni fichye pou enpòte"}, 400)
                sp = import_timeline(content, fmt=b.get("format") or "auto")
                if b.get("apply"):
                    self.S.save_spec(sp)
                return self._json({"ok": True, "spec": sp})
            if u.path == "/api/audio/loudness":
                from .lint import measure_loudness
                p_arg = b.get("path")
                if p_arg:
                    src_p = Path(p_arg) if Path(p_arg).is_absolute() else self.S.base / p_arg
                else:
                    src_p = self.S.work / "preview-audio.wav"
                return self._json(measure_loudness(src_p))
            if u.path == "/api/render":
                return self._json(self._start_render())
            if u.path == "/api/render-cancel":
                return self._json(self._cancel_render())
            if u.path == "/api/remotion/open":
                try:
                    from wasdev.app.video.remotion_server import (
                        is_remotion_installed,
                        RemotionServerManager,
                        open_in_edge,
                        install_remotion,
                    )
                    from .remotion_bridge import export_to_remotion
                    rem_dir = self.S.work / "remotion"
                    auto_install = bool(b.get("install"))

                    if not is_remotion_installed(rem_dir):
                        if not auto_install:
                            return self._json({
                                "ok": False,
                                "need_install": True,
                                "message": "Motè Remotion pa enstale sou PC sa a."
                            })
                        ok_inst, msg_inst = install_remotion()
                        if not ok_inst:
                            return self._json({"ok": False, "error": msg_inst})

                    sp = b.get("spec") or self.S.load_spec()
                    export_to_remotion(sp, rem_dir, base_dir=self.S.base)
                    mgr = RemotionServerManager.get_instance()
                    ok_start, url, msg_start = mgr.start_preview(rem_dir)
                    if not ok_start:
                        return self._json({"ok": False, "error": msg_start})

                    if b.get("open_browser", True):
                        open_in_edge(url)

                    return self._json({"ok": True, "url": url, "message": "Remotion Studio pare nan Edge!"})
                except Exception as e:
                    return self._json({"ok": False, "error": str(e)})

            if u.path == "/api/remotion/export":
                from .remotion_bridge import export_to_remotion
                rem_dir = self.S.work / "remotion"
                sp = b.get("spec") or self.S.load_spec()
                res = export_to_remotion(sp, rem_dir, base_dir=self.S.base)
                return self._json(res)

            if u.path == "/api/reveal-render":            # bouton «Ouvri kote fichye a ye a» (klik moun nan)
                mp4 = Path(self.S._render.get("mp4") or "")
                if not str(mp4) or not mp4.is_file():
                    return self._json({"ok": False, "error": "Fichye MP4 la pa jwenn"}, 404)
                return self._json({"ok": reveal_in_folder(mp4), "path": str(mp4), "folder": str(mp4.parent)})
            if u.path == "/api/frame":
                tt = float(b.get("t") or 0)
                sp_clean = b.get("spec") or self.S.load_spec()
                ratio = str(sp_clean.get("ratio") or "16:9").strip()
                w, h = 1920, 1080
                if ratio == "9:16":
                    w, h = 1080, 1920
                elif ratio == "1:1":
                    w, h = 1080, 1080
                elif ratio == "4:5":
                    w, h = 1080, 1350
                elif ratio == "21:9":
                    w, h = 2560, 1080
                fdir = self.S.work / "frames"
                fdir.mkdir(parents=True, exist_ok=True)
                name = "frame-%.2f.png" % tt
                out_path = fdir / name
                try:
                    self.S.capture_frame(tt, w, h, out_path)
                except Exception:
                    from kadans.cdp import Browser, screenshot
                    comp = self.S.work / "composition.html"
                    if not comp.is_file():
                        self.S.build(sp_clean)
                    with Browser(no_gpu=True) as br:
                        pg = br.pages(comp.resolve().as_uri() + "#render", 1, w, h)[0]
                        pg.eval(f"window.__seek({tt:.4f})")
                        out_path.write_bytes(screenshot(pg, w, h, "png"))
                return self._json({"ok": True, "file": "frames/" + name})
            if u.path == "/api/projects/new":
                return self._json(self.S.new_project(b.get("name"), b.get("ratio") or "16:9", lang=b.get("lang") or "fr", total_duration=b.get("total_duration"), empty=b.get("empty", True)))
            if u.path == "/api/projects/open":
                return self._json(self.S.open_project(b.get("name")))
            if u.path == "/api/projects/open-file":
                return self._json(self.S.import_external_file(b.get("filename") or "", b.get("content") or "", b.get("path")))
            if u.path == "/api/projects/duplicate":
                return self._json(self.S.duplicate_project(b.get("name"), b.get("new_name")))
            if u.path == "/api/projects/delete":
                return self._json(self.S.delete_project(b.get("name")))
            if u.path == "/api/sounds/take":             # son CC0 → kopi nan medya/sfx/ pwojè a (cc0-<id>.ogg)
                from kadans import layout as LY, sounds as SO
                e = SO.by_id(str(b.get("id") or ""))
                if not e:
                    return self._json({"error": "son pa jwenn"}, 404)
                dst = LY.collect(self.S.work, e["files"][0], "sfx", f"cc0-{e['id']}")
                return self._json({"ok": True, "rel": self.S.media_rel(dst),
                                   "dur": e.get("dur") or 2, "loop": bool(e.get("loop")), "kind": e.get("kind")})
            if u.path == "/api/use-asset":
                import shutil
                import re as _re
                raw_path = (b.get("path") or "").lstrip("/")
                custom_name = (b.get("name") or "").strip()
                src = None
                p_work = (self.S.work / raw_path).resolve()
                try:
                    p_work.relative_to(self.S.work.resolve())
                    if p_work.is_file():
                        src = p_work
                except ValueError:
                    pass
                if not src:
                    src = self.S.asset_file(raw_path)
                if not src:
                    src = self.S.safe_path(raw_path)
                if not src or not src.is_file():
                    return self._json({"error": "asset pa jwenn"}, 400)

                mdir = layout.media_dir(self.S.work, layout.kind_of(src))
                target_name = custom_name if custom_name else src.name
                if not _re.search(r"\.[a-zA-Z0-9]+$", target_name):
                    target_name += src.suffix
                target_name = _re.sub(r'[\\/*?:"<>|]', "_", target_name)
                dst = mdir / target_name
                shutil.copy2(src, dst)
                return self._json({"ok": True, "rel": self.S.media_rel(dst), "name": dst.name})
        except Exception as e:                                   # noqa: BLE001
            return self._json({"error": str(e)[:300]}, 400)
        return self._json({"error": "unknown"}, 404)

    def do_PUT(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._authed(q):
            return self._json({"error": "forbidden"}, 403)
        if u.path == "/api/spec":
            b = self._body()
            r = self.S.save_spec(b.get("spec") or {}, b.get("version"))
            return self._json(r, 409 if r.get("conflict") else 200)
        return self._json({"error": "unknown"}, 404)

    # ------------------------------------------------------------- SSE
    def _sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        last_rev = -1
        try:
            while True:
                S = self.S
                payload = {"rev": S._version, "render": S._render, "disk": S.disk_version(),
                           "errors": S._build_errors, "warnings": S._build_warnings}
                data = ("data: " + json.dumps(payload, ensure_ascii=False) + "\n\n").encode("utf-8")
                self.wfile.write(data)
                self.wfile.flush()
                last_rev = S._version
                time.sleep(0.4 if S._render["active"] else 1.0)
        except (BrokenPipeError, ConnectionResetError, OSError):
            return

    # ------------------------------------------------------------- render
    def _start_render(self) -> dict:
        S = self.S
        if S._render.get("active"):
            return {"ok": False, "error": "yon rann ap kouri deja"}
        start_t = time.time()
        S._render = {
            "active": True, "done": 0, "total": 0, "stage": "start",
            "info": "Kòmanse...", "error": "", "mp4": "", "rel_mp4": "",
            "started": start_t, "elapsed": 0.0, "eta": None
        }

        def run():
            try:
                fresh_engine()                                   # pa janm rann ak ansyen kòd ki rete an memwa
                K = S._kadans()
                from kadans.renderer import render

                def prog(stage, done, tot, info):
                    now = time.time()
                    elapsed = now - start_t
                    eta = None
                    if tot > 0 and done > 0 and elapsed > 0.5:
                        rate = done / elapsed
                        if rate > 0:
                            eta = (tot - done) / rate
                    S._render.update(
                        stage=stage, done=done, total=tot, info=f"{info}",
                        elapsed=round(elapsed, 1), eta=round(eta, 1) if eta is not None else None
                    )
                out_mp4 = layout.next_render(S.work)       # Exported Videos/<non>_v<N>.mp4 — pa janm ekrase yon ansyen rann
                # menm tolerans ak aperçu a: yon son mete kòm imaj (elatriye) kite deyò, pa yon rann ki echwe
                clean, _warn = S._validate_repaired(K, S.load_spec())
                from kadans import media
                for sc in clean.get("scenes", []):
                    vf = sc.get("voice_file")
                    if vf:
                        p_base = media.resolve(vf, S.base)
                        p_work = media.resolve(vf, S.work)
                        if not p_base.is_file() and p_work.is_file():
                            sc["voice_file"] = S.media_rel(p_work)
                tts_func = S._resolve_tts()
                r = render(clean, out_mp4, S.base, progress=prog, tts=tts_func, tts_fn=tts_func)
                final_mp4 = Path(r.get("mp4", out_mp4)).resolve()
                if not final_mp4.is_file() or final_mp4.stat().st_size < 1024:
                    raise RuntimeError(f"MP4 final la pa t kreye: {final_mp4}")
                rel = S.media_rel(final_mp4)
                tot_elapsed = round(time.time() - start_t, 1)

                # Senkronizasyon nan tout kote obligatwa yo: dosye espesifik pwojè a + rasin workspace orijinal kotel monte a
                import shutil
                mirror_targets = set()
                mirror_targets.add((S.work / "Exported Videos").resolve())
                candidates = []
                if getattr(S, "workspace_root", None):
                    candidates.append(Path(S.workspace_root).resolve())
                if getattr(S, "base", None):
                    candidates.append(Path(S.base).resolve())
                if S.work.parent.name in ("Analyseur-Kadans", "kadans-projects", "videos"):
                    candidates.append(S.work.parent.parent.resolve())
                    candidates.append(S.work.parent.resolve())
                for c in candidates:
                    if c.is_dir():
                        mirror_targets.add((c / "Exported Videos").resolve())
                        if (c / "Analyseur-Kadans").is_dir() or c.name != "Analyseur-Kadans":
                            mirror_targets.add((c / "Analyseur-Kadans" / "Exported Videos").resolve())

                srt_file = final_mp4.with_suffix(".srt")
                ws_mp4_path = ""
                for mt in mirror_targets:
                    try:
                        dest_f = mt / final_mp4.name
                        if dest_f.resolve() != final_mp4.resolve():
                            mt.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(final_mp4, dest_f)
                            if srt_file.is_file():
                                shutil.copy2(srt_file, dest_f.with_suffix(".srt"))
                            if not ws_mp4_path and "Analyseur-Kadans" not in mt.name:
                                ws_mp4_path = str(dest_f)
                    except Exception:
                        pass

                S._render.update(
                    mp4=str(final_mp4), rel_mp4=rel, stage="done", folder=str(final_mp4.parent),
                    workspace_mp4=ws_mp4_path or str(final_mp4),
                    size=final_mp4.stat().st_size, encoder=r.get("encoder", ""),
                    resolution=f"{clean.get('w', '')}x{clean.get('h', '')}" if isinstance(clean, dict) else "",
                    info="Fini avèk siksè!", elapsed=tot_elapsed, eta=0.0
                )
            except Exception as e:                               # noqa: BLE001
                S._render.update(error=str(e)[:300], stage="error", info="Erè rann")
            finally:
                S._render["active"] = False
        threading.Thread(target=run, daemon=True).start()
        return {"ok": True}

    def _cancel_render(self) -> dict:
        S = self.S
        if S._render.get("active"):
            S._render["active"] = False
            S._render["error"] = "Rann lan kanpe."
            return {"ok": True, "cancelled": True}
        return {"ok": True, "active": False}

    def _serve_download(self, p: Path, filename: str):
        try:
            data = p.read_bytes()
        except OSError:
            return self._json({"error": "io"}, 404)
        self.send_response(200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass

    # ------------------------------------------------------------- static
    _NOSTORE_EXT = (".html", ".htm", ".js", ".mjs", ".css", ".json", ".txt")
    _CHUNK = 256 * 1024

    def _serve_file(self, p: Path):
        """Fichye an STREAMING (pa janm tout fichye a nan RAM): Range pa moso + ETag (mtime+gwosè).
        Kòd editè a (html/js/css/json) rete no-store; medya yo: no-cache + ETag (navigatè a revalide, 304 si
        fichye a pa chanje — menm non tankou preview-audio.wav refè → nouvo ETag)."""
        try:
            st = p.stat()
            f = open(p, "rb")
        except OSError:
            return self._json({"error": "io"}, 404)
        with f:
            ctype = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
            size = st.st_size
            nostore = p.suffix.lower() in self._NOSTORE_EXT
            etag = f'"{st.st_mtime_ns:x}-{size:x}"'
            if not nostore and self.headers.get("If-None-Match") == etag:
                self.send_response(304)
                self.send_header("ETag", etag)
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                return
            start, end, partial = 0, size - 1, False
            rng = self.headers.get("Range")
            if rng and rng.startswith("bytes=") and size > 0:
                try:
                    spec = rng[6:].split(",")[0].strip()
                    s_str, e_str = (spec.split("-", 1) + [""])[:2]
                    if s_str:
                        start = int(s_str)
                        end = int(e_str) if e_str else size - 1
                    else:                                    # bytes=-N: dènye N okte yo
                        start, end = max(0, size - int(e_str)), size - 1
                    start = max(0, min(start, size - 1))
                    end = max(start, min(end, size - 1))
                    partial = True
                except ValueError:
                    start, end, partial = 0, size - 1, False
            length = max(0, end - start + 1)
            self.send_response(206 if partial else 200)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            if partial:
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(length))
            if nostore:
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
            else:
                self.send_header("Cache-Control", "no-cache")
                self.send_header("ETag", etag)
            self.end_headers()
            if self.command == "HEAD":
                return
            try:
                f.seek(start)
                left = length
                while left > 0:
                    buf = f.read(min(self._CHUNK, left))
                    if not buf:
                        break
                    self.wfile.write(buf)
                    left -= len(buf)
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass

    def _serve_favicon(self):
        body = _WASDEV_FAVICON_SVG.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass

    def _serve_preview_fallback(self):
        try:
            sp = self.S.load_spec()
        except Exception:
            sp = {}
        title = sp.get("title") or self.S.work.name or "Kadans Studio"
        html = self.S._fallback_composition_html({"title": title})
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass

    def _serve_index(self):
        if self.S.editor_dir and (self.S.editor_dir / "index.html").is_file():
            return self._serve_file(self.S.editor_dir / "index.html")
        html = _BUILTIN_INDEX.replace("__TOKEN__", self.S.token)
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


_WASDEV_FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#0098ff"/></linearGradient></defs>
<rect x="4" y="4" width="56" height="56" rx="14" fill="#1d1230"/>
<path d="M24 20L12 32l12 12" fill="none" stroke="url(#g)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M40 20l12 12-12 12" fill="none" stroke="url(#g)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M36 14L28 50" fill="none" stroke="#b794ff" stroke-width="5" stroke-linecap="round"/>
</svg>"""


_BUILTIN_INDEX = """<!doctype html><html><head><meta charset=utf-8><title>Kadans Timeline — WASDEV</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>body{margin:0;font:14px system-ui;background:#0b0816;color:#f3eefe;display:flex;height:100vh}
#side{width:240px;overflow:auto;border-right:1px solid #2a2440;padding:8px}
#side h3{color:#8b5cf6;margin:6px 4px}.sc{padding:6px 8px;border-radius:8px;cursor:pointer}.sc:hover{background:#1a1530}
.sc.sel{background:#2a1745;outline:1px solid #8b5cf6}#main{flex:1;display:flex;flex-direction:column}
iframe{flex:1;border:0;background:#000}#bar{padding:6px 10px;color:#b9addb;border-top:1px solid #2a2440}</style>
</head><body>
<div id=side><h3>Kadans Timeline</h3><div style="color:#b9addb;font-size:12px;margin:4px">Editè React: Faz 2. Isit la = prèv pon an.</div><div id=list></div></div>
<div id=main><iframe id=fr></iframe><div id=bar>—</div></div>
<script>
const TOK="__TOKEN__", fr=document.getElementById("fr"), list=document.getElementById("list"), bar=document.getElementById("bar");
fr.src="composition.html?token="+TOK;
let scenes=[];
addEventListener("message",e=>{const m=e.data||{};
 if(m.evt==="ready"){scenes=m.kadans.scenes||[];draw();bar.textContent="pare · "+scenes.length+" sèn · "+(m.kadans.total||0).toFixed(1)+" s";}
 if(m.evt==="time"){bar.textContent="t = "+(+m.t).toFixed(2)+" s";}
 if(m.evt==="click"){sel(m.scene);}
});
function draw(){list.innerHTML="";scenes.forEach(s=>{const d=document.createElement("div");d.className="sc";d.dataset.id=s.id;
 d.textContent=(s.spec_index+1)+". "+s.id+"  ("+(s.dur||0).toFixed(1)+"s)";d.onclick=()=>{seek(s.start);sel(s.id);};list.appendChild(d);});}
function sel(id){document.querySelectorAll(".sc").forEach(x=>x.classList.toggle("sel",x.dataset.id===id));
 fr.contentWindow.postMessage({cmd:"highlight",scene:id},"*");}
function seek(t){fr.contentWindow.postMessage({cmd:"seek",t:t},"*");}
</script></body></html>"""


def open_studio(work_dir, spec_path=None, base=None, host="127.0.0.1", port=0, editor_dir=None, tts_fn=None, audio_bridge=None, token=None) -> StudioServer:
    """Louvri sèvè a epi retounen l (ak .url()). Kadans Timeline / kadans studio."""
    s = StudioServer(work_dir, spec_path, base, host, port, editor_dir, tts_fn=tts_fn, audio_bridge=audio_bridge, token=token)
    s.start()
    return s
