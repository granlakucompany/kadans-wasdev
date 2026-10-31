"""Chwazi + telechaje apèsi HQ son CC0 Freesound pou bibliyotèk SFX WASDEV la (lisans lan verifye sou paj son an).
Itilizasyon: python -I tools/sfx/fs_pick.py <dosye_sòti>  (rechèch 2026-10-20; rezilta ka chanje si Freesound chanje)   → <dosye>/<id>.mp3 + picks.json"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "WASDEV-sfx-library/1.0 (CC0 curation)"}

# id, rechèch, mo ki dwe nan tit la (youn), dire min, max, kalite, tag (fr / ht / en)
WANT = [   # son AYISYEN (rechèch final 2026-10-20; «vendor-shout» / «market-crowd» retire: pawòl an arab / angle)
    ("rara-band", "street drums", ["drum", "percussion", "batucada", "samba"], 10, 120, "ambience", "rara kanaval carnaval tanbou tambour drums percussion parade"),
    ("street-parade", "marching band", ["band", "parade", "march"], 10, 120, "ambience", "rara kanaval carnaval fanfare parade defile"),
    ("conch-shell", "cow horn blowing", ["horn", "conch", "shell"], 1, 15, "sfx", "lanbi conque conch kòn corne horn"),
    ("truck-horn", "car horn", ["horn"], 0.3, 6, "sfx", "kòn klaksonn klaxon horn taptap tap-tap machin voiture car"),
    ("bus-engine", "old bus engine idle", ["bus", "engine", "truck", "diesel"], 5, 60, "ambience", "taptap tap-tap bis bus kamyon moto motè moteur engine"),
    ("rain-tin-roof", "rain shed", ["shed", "roof", "metal", "tin", "porch", "awning"], 15, 180, "ambience", "lapli pluie rain tòl tôle twati toit roof"),
    ("bamboo-trumpet", "wooden horn", ["horn", "trumpet", "flute", "bamboo"], 1, 20, "sfx", "vaksin bambou bamboo twonpèt trompette horn rara"),
    ("goat", "goat bleat", ["goat"], 0.5, 8, "sfx", "kabrit chèvre goat"),
    ("dominoes", "dominoes", ["domino"], 0.5, 15, "sfx", "domino dominos dominoes jwe jouer"),
    ("machete", "machete", ["machete"], 0.3, 6, "sfx", "manchèt machette machete koupe couper"),
    ("whistle", "whistle blow", ["whistle"], 0.3, 5, "sfx", "fichèt sifflet whistle"),
]
FILTER = 'license:"Creative Commons 0" duration:[{a} TO {b}]'


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def results(page: str):
    for m in re.finditer(r'data-sound-id="(\d+)"\s+data-username="([^"]+)".*?data-mp3="([^"]+)".*?data-title="([^"]*)"'
                         r'\s+data-duration="([\d.]+)".*?data-num-downloads="(\d+)"', page, re.S):
        sid, user, mp3, title, dur, dl = m.groups()
        yield {"id": int(sid), "user": html.unescape(user), "mp3": mp3, "title": html.unescape(title).strip(),
               "dur": float(dur), "downloads": int(dl)}


picks = []
for key, q, words, a, b, kind, tags in WANT:
    url = ("https://freesound.org/search/?" + urllib.parse.urlencode(
        {"q": q, "f": FILTER.format(a=a, b=b), "s": "Downloads (most first)"}))
    try:
        cands = list(results(get(url)))
    except Exception as e:                                   # noqa: BLE001
        print("ECHEK rechèch", key, e)
        continue
    pick = next((c for c in cands if any(w in c["title"].lower() for w in words)), None)
    if pick is None:
        print("PA JWENN", key, [c["title"] for c in cands[:5]])
        continue
    time.sleep(1.2)
    page = get(f"https://freesound.org/people/{urllib.parse.quote(pick['user'])}/sounds/{pick['id']}/")
    lic_ok = ("publicdomain/zero" in page) or ("Creative Commons 0" in page)
    if not lic_ok:
        print("LISANS PA CC0", key, pick["id"])
        continue
    hq = pick["mp3"].replace("-lq.mp3", "-hq.mp3")
    dst = OUT / f"{key}.mp3"
    req = urllib.request.Request(hq, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        dst.write_bytes(r.read())
    picks.append({"key": key, "kind": kind, "tags": tags, "title": pick["title"], "author": pick["user"],
                  "source": f"https://freesound.org/people/{pick['user']}/sounds/{pick['id']}/", "license": "CC0-1.0",
                  "dur": pick["dur"], "file": dst.name})
    print("OK", key, "<-", pick["title"][:60], f"({pick['dur']:.1f} s, {pick['user']})", flush=True)
    time.sleep(1.2)
(OUT / "picks.json").write_text(json.dumps(picks, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(picks), "/", len(WANT))
