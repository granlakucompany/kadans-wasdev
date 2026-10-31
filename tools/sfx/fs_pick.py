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
WANT = [
    ("crickets-night", "crickets night", ["cricket"], 15, 120, "ambience", "krikèt grillons crickets nwit nuit night"),
    ("frogs-night", "frogs night", ["frog"], 15, 120, "ambience", "krapo grenouilles frogs nwit nuit night"),
    ("night-tropical", "tropical night ambience", ["night"], 20, 180, "ambience", "nwit nuit night twopikal tropical"),
    ("rooster", "rooster crow", ["rooster", "cock"], 1.5, 8, "sfx", "kòk coq rooster maten matin morning"),
    ("dog-bark-distant", "dog barking distant", ["dog", "bark"], 2, 20, "sfx", "chen chien dog jape aboie bark lwen loin"),
    ("birds-morning", "birds morning chirping", ["bird"], 15, 120, "ambience", "zwazo oiseaux birds maten matin morning"),
    ("ocean-waves", "ocean waves beach", ["wave", "ocean", "sea", "surf"], 20, 180, "ambience", "lanmè mer vagues waves plaj plage beach"),
    ("wind-soft", "wind gentle", ["wind"], 15, 120, "ambience", "van vent wind"),
    ("rain-light", "light rain", ["rain"], 15, 180, "ambience", "lapli pluie rain"),
    ("thunder", "thunder", ["thunder"], 3, 25, "sfx", "loraj tonnerre thunder"),
    ("fire-crackle", "fire crackling", ["fire", "crackl"], 10, 120, "ambience", "dife feu fire bouji bougie candle"),
    ("candle-blow", "blow out candle", ["candle"], 0.5, 6, "sfx", "bouji bougie candle soufle souffle blow"),
    ("crowd-cheer", "crowd cheering", ["cheer", "crowd"], 3, 30, "sfx", "foul foule crowd kontan joie cheer"),
    ("crowd-applause", "applause", ["applau", "clap"], 3, 30, "sfx", "bat bravo applaudissements applause"),
    ("street-ambience", "street ambience people", ["street", "town", "city"], 20, 180, "ambience", "lari rue street vil ville"),
    ("children-playing", "children playing", ["child", "kid"], 10, 120, "ambience", "timoun enfants children jwe jouer play"),
    ("motorcycle-pass", "motorcycle pass by", ["motorcycle", "motorbike", "scooter"], 3, 20, "sfx", "moto motorcycle pase passe"),
    ("church-bell", "church bell", ["bell"], 3, 30, "sfx", "klòch cloche bell legliz église church"),
    ("power-on-hum", "fluorescent light", ["fluorescent", "neon", "light", "tube"], 0.5, 20, "sfx", "kouran courant electricity limyè lumière on hum"),
    ("light-switch", "light switch", ["switch"], 0.2, 3, "sfx", "switch entèriptè interrupteur limyè lumière"),
    ("paper-rustle", "paper rustle", ["paper"], 0.5, 8, "sfx", "papye papier paper"),
    ("pencil-drawing", "pencil writing", ["pencil", "writ", "sketch", "draw"], 1, 30, "sfx", "kreyon crayon pencil desen dessin draw"),
    ("wings-flapping", "bird wings flapping", ["wing", "flap"], 0.5, 10, "sfx", "zèl ailes wings vole voler fly"),
    ("tin-roof-steps", "footsteps metal", ["metal", "roof", "tin", "step"], 1, 30, "sfx", "twati toit roof tòl tôle tin pa pas steps"),
    ("running-steps", "running footsteps", ["run"], 2, 20, "sfx", "kouri courir run pa pas steps"),
    ("jump-land", "jump landing thud", ["land", "jump", "thud"], 0.2, 4, "sfx", "sote sauter jump ateri atterrir land"),
    ("door-knock", "knock wooden door", ["knock"], 0.5, 6, "sfx", "frape frapper knock pòt porte door"),
    ("paint-brush", "paint brush stroke", ["brush", "paint"], 0.5, 15, "sfx", "penso pinceau brush penti peinture paint"),
    ("magic-sparkle", "magic sparkle chime", ["magic", "sparkle", "chime", "twinkle"], 0.5, 6, "sfx", "majik magie magic zetensèl étincelle sparkle"),
    ("cartoon-pop", "cartoon pop", ["pop"], 0.1, 2, "sfx", "pop dessin cartoon"),
    ("cartoon-boing", "boing", ["boing", "spring"], 0.2, 3, "sfx", "boing resò ressort spring"),
    ("heartbeat", "heartbeat", ["heart"], 2, 20, "sfx", "kè cœur heart bat battement beat"),
    ("clock-tick", "clock ticking", ["clock", "tick"], 3, 30, "ambience", "revèy horloge clock tik tac tick"),
    ("drum-rara", "hand drum", ["drum"], 2, 30, "sfx", "tanbou tambour drum rara"),
    ("kiss-cheek", "kiss", ["kiss"], 0.2, 3, "sfx", "bo bisou kiss"),
    ("gasp-surprise", "gasp surprise", ["gasp"], 0.3, 4, "sfx", "sezi surpris gasp surprise"),
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
