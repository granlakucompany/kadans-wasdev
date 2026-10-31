"""Ajoute son Freesound CC0 (picks*.json) nan yon pakè ki deja la (index.json) — menm preparasyon ak build_pack.py.
python -I add_pack.py <ffmpeg> <dl_dir> <pack_dir>"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FF, DL, OUT = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
NOWIN = 0x08000000


def dur_of(p):
    r = subprocess.run([FF, "-hide_banner", "-i", str(p)], capture_output=True, text=True, creationflags=NOWIN)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0


def peak_db(p):
    r = subprocess.run([FF, "-hide_banner", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True, creationflags=NOWIN)
    m = re.search(r"max_volume: (-?[\d.]+) dB", r.stderr)
    return float(m[1]) if m else 0.0


def encode(src, dst, kind, max_len):
    d = dur_of(src)
    tmp = dst.with_suffix(".tmp.wav")
    if kind == "ambience":
        L = min(d, max_len)
        xf = min(1.5, L / 6)
        fc = (f"[0:a]atrim=0:{L:.3f},asetpts=PTS-STARTPTS,asplit[a][b];"
              f"[a]atrim=start={xf:.3f},asetpts=PTS-STARTPTS[m];[b]atrim=0:{xf:.3f},asetpts=PTS-STARTPTS[h];"
              f"[m][h]acrossfade=d={xf:.3f}:c1=tri:c2=tri,loudnorm=I=-22:TP=-3:LRA=11,aresample=44100[o]")
        subprocess.run([FF, "-y", "-v", "error", "-i", str(src), "-filter_complex", fc, "-map", "[o]", str(tmp)],
                       check=True, creationflags=NOWIN)
    else:
        subprocess.run([FF, "-y", "-v", "error", "-i", str(src), "-af",
                        f"silenceremove=start_periods=1:start_threshold=-55dB,atrim=0:{max_len:.3f},aresample=44100",
                        str(tmp)], check=True, creationflags=NOWIN)
        g = -3.0 - peak_db(tmp)
        t2 = dst.with_suffix(".tmp2.wav")
        subprocess.run([FF, "-y", "-v", "error", "-i", str(tmp), "-af", f"volume={g:.2f}dB", str(t2)], check=True,
                       creationflags=NOWIN)
        tmp.unlink()
        t2.rename(tmp)
    subprocess.run([FF, "-y", "-v", "error", "-i", str(tmp), "-c:a", "libvorbis", "-q:a", "5", str(dst)], check=True,
                   creationflags=NOWIN)
    tmp.unlink()
    return round(dur_of(dst), 3)


ix_path = OUT / "index.json"
ix = json.loads(ix_path.read_text(encoding="utf-8"))
have = {e["id"] for e in ix["sounds"]}
picks = {}
for p in sorted(DL.glob("picks*.json")):
    for x in json.loads(p.read_text(encoding="utf-8")):
        if (DL / x["file"]).is_file():
            picks[x["key"]] = x
for key, x in picks.items():
    if key in have:
        continue
    dst = OUT / f"{key}.ogg"
    d = encode(DL / x["file"], dst, x["kind"], 60.0 if x["kind"] == "ambience" else 20.0)
    ix["sounds"].append({"id": key, "files": [dst.name], "kind": x["kind"], "loop": x["kind"] == "ambience",
                         "tags": x["tags"].split(), "dur": d, "title": x["title"], "author": x["author"],
                         "source": x["source"], "license": "CC0-1.0"})
    print("OK", key, d, flush=True)
ix["sounds"].sort(key=lambda e: e["id"])
ix_path.write_text(json.dumps(ix, ensure_ascii=False, indent=1), encoding="utf-8")
cr = OUT / "CREDITS.md"
lines = cr.read_text(encoding="utf-8").splitlines()
head = [l for l in lines if not l.startswith("| ") or l.startswith("| id ")]
head = [l for l in lines if not (l.startswith("| ") and not l.startswith("| id "))]
rows = [f"| {e['id']} | {e['kind']} | {e['title']} | {e['author']} | {e['source']} |" for e in ix["sounds"]]
i = head.index("|---|---|---|---|---|")
cr.write_text("\n".join(head[:i + 1] + rows) + "\n", encoding="utf-8")
print(len(ix["sounds"]), "son")
