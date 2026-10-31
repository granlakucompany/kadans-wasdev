"""Bati pakè SFX CC0 WASDEV / Kadans: OGG Vorbis, volim nòmalize, ambyans an bouk san koupi, index.json.
python -I build_pack.py <ffmpeg> <freesound_dir> <kenney_dir> <out_dir>"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FF, FS, KN, OUT = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
NOWIN = 0x08000000


def dur_of(p: Path) -> float:
    r = subprocess.run([FF, "-hide_banner", "-i", str(p)], capture_output=True, text=True, creationflags=NOWIN)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0


def peak_db(p: Path) -> float:
    r = subprocess.run([FF, "-hide_banner", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True, creationflags=NOWIN)
    m = re.search(r"max_volume: (-?[\d.]+) dB", r.stderr)
    return float(m[1]) if m else 0.0


def encode(src: Path, dst: Path, kind: str, max_len: float = 60.0):
    d = dur_of(src)
    tmp = dst.with_suffix(".tmp.wav")
    if kind == "ambience":                                # bouk san koupi: fen an melanje ak kòmansman an
        L = min(d, max_len)
        xf = min(1.5, L / 6)
        fc = (f"[0:a]atrim=0:{L:.3f},asetpts=PTS-STARTPTS,asplit[a][b];"
              f"[a]atrim=start={xf:.3f},asetpts=PTS-STARTPTS[m];[b]atrim=0:{xf:.3f},asetpts=PTS-STARTPTS[h];"
              f"[m][h]acrossfade=d={xf:.3f}:c1=tri:c2=tri,loudnorm=I=-22:TP=-3:LRA=11,aresample=44100[o]")
        subprocess.run([FF, "-y", "-v", "error", "-i", str(src), "-filter_complex", fc, "-map", "[o]", str(tmp)],
                       check=True, creationflags=NOWIN)
    else:                                                 # SFX: silans devan retire, pik = -3 dBFS
        subprocess.run([FF, "-y", "-v", "error", "-i", str(src), "-af",
                        f"silenceremove=start_periods=1:start_threshold=-55dB,atrim=0:{max_len:.3f},aresample=44100",
                        str(tmp)], check=True, creationflags=NOWIN)
        g = -3.0 - peak_db(tmp)
        tmp2 = dst.with_suffix(".tmp2.wav")
        subprocess.run([FF, "-y", "-v", "error", "-i", str(tmp), "-af", f"volume={g:.2f}dB", str(tmp2)],
                       check=True, creationflags=NOWIN)
        tmp.unlink()
        tmp2.rename(tmp)
    subprocess.run([FF, "-y", "-v", "error", "-i", str(tmp), "-c:a", "libvorbis", "-q:a", "5", str(dst)],
                   check=True, creationflags=NOWIN)
    tmp.unlink()
    return round(dur_of(dst), 3)


KENNEY = [  # id, fichye (varyant), tag, kalite
    ("door-creak", ["rpg-audio/Audio/creak1.ogg", "rpg-audio/Audio/creak2.ogg", "rpg-audio/Audio/creak3.ogg"],
     "pòt porte door krake grince creak"),
    ("door-open", ["rpg-audio/Audio/doorOpen_1.ogg", "rpg-audio/Audio/doorOpen_2.ogg"], "pòt porte door louvri ouvrir open"),
    ("door-close", [f"rpg-audio/Audio/doorClose_{i}.ogg" for i in range(1, 5)], "pòt porte door fèmen fermer close"),
    ("footstep-soft", [f"rpg-audio/Audio/footstep0{i}.ogg" for i in range(5)], "pa pas footstep steps mache marcher walk tè terre dirt"),
    *[(f"footstep-{s}", [f"impact-sounds/Audio/footstep_{s}_00{i}.ogg" for i in range(5)],
       f"pa pas footstep steps mache marcher walk {t}") for s, t in
      (("concrete", "beton béton concrete"), ("grass", "zèb herbe grass"), ("wood", "bwa bois wood planche"),
       ("snow", "nèj neige snow"), ("carpet", "tapi tapis carpet"))],
    ("cloth", [f"rpg-audio/Audio/cloth{i}.ogg" for i in range(1, 5)], "twal tissu cloth rad vêtement"),
    ("book-flip", [f"rpg-audio/Audio/bookFlip{i}.ogg" for i in range(1, 4)], "paj page liv livre book kaye cahier"),
    ("book-open", ["rpg-audio/Audio/bookOpen.ogg"], "liv livre book louvri ouvrir open kaye cahier"),
    ("book-close", ["rpg-audio/Audio/bookClose.ogg"], "liv livre book fèmen fermer close kaye cahier"),
    ("metal-latch", ["rpg-audio/Audio/metalLatch.ogg"], "takèt loquet latch metal pòt porte"),
    ("coins", ["rpg-audio/Audio/handleCoins.ogg", "rpg-audio/Audio/handleCoins2.ogg"], "lajan argent money pyès pièces coins"),
    ("saucepan", [f"rpg-audio/Audio/metalPot{i}.ogg" for i in range(1, 4)], "chodyè casserole saucepan kizin cuisine kitchen metal"),
    ("impact-wood", [f"impact-sounds/Audio/impactPlank_medium_00{i}.ogg" for i in range(5)], "bwa bois wood frape choc impact"),
    ("impact-metal", [f"impact-sounds/Audio/impactMetal_light_00{i}.ogg" for i in range(5)], "metal tòl tôle frape choc impact"),
    ("impact-glass", [f"impact-sounds/Audio/impactGlass_light_00{i}.ogg" for i in range(5)], "vè verre glass frape choc impact"),
    ("impact-soft", [f"impact-sounds/Audio/impactGeneric_light_00{i}.ogg" for i in range(5)], "tonbe tomber thud frape choc impact"),
    ("bell-heavy", [f"impact-sounds/Audio/impactBell_heavy_00{i}.ogg" for i in range(5)], "klòch cloche bell"),
]

index = []
for key, files, tags in KENNEY:
    outs = []
    for j, f in enumerate(files):
        dst = OUT / (f"{key}.ogg" if len(files) == 1 else f"{key}-{j + 1}.ogg")
        d = encode(KN / f, dst, "sfx", 10)
        outs.append((dst.name, d))
    index.append({"id": key, "files": [o[0] for o in outs], "kind": "sfx", "loop": False, "tags": tags.split(),
                  "dur": max(o[1] for o in outs), "title": Path(files[0]).stem, "author": "Kenney (kenney.nl)",
                  "source": "https://kenney.nl/assets/" + files[0].split("/")[0], "license": "CC0-1.0"})
    print("OK", key, len(outs), flush=True)

picks = {}
for name in ("picks.json", "picks2.json", "picks3.json"):     # picks2/3: dènye eseye yo (pi resan genyen)
    p = FS / name
    if p.is_file():
        for x in json.loads(p.read_text(encoding="utf-8")):
            picks[x["key"]] = x
for key, x in picks.items():
    kind = x["kind"]
    dst = OUT / f"{key}.ogg"
    d = encode(FS / x["file"], dst, kind, 60.0 if kind == "ambience" else 20.0)
    index.append({"id": key, "files": [dst.name], "kind": kind, "loop": kind == "ambience", "tags": x["tags"].split(),
                  "dur": d, "title": x["title"], "author": x["author"], "source": x["source"], "license": "CC0-1.0"})
    print("OK", key, d, flush=True)
index.sort(key=lambda e: e["id"])
(OUT / "index.json").write_text(json.dumps({"version": 1, "license": "CC0-1.0", "sounds": index}, ensure_ascii=False,
                                           indent=1), encoding="utf-8")
print(len(index), "son")
