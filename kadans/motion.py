"""MOTION — pèsonaj cut-out 2D ki mache, kouri, sote, chita, fè siy, vole (rig Design WASDEV la).

Yon pèsonaj = yon gwoup `data-rig="Lina"` ak pati ki tache ak zo (`data-bone`); chak zo gen yon WOL estanda
(ROLES: hips, torso, head, arm_r, forearm_r, thigh_l…). Mouvman yo se DONE (MOTIONS): pou chak wòl, ang (degre,
pozitif = nan sans ègwi yon mont, y anba) sou yon faz 0..1, entèpole Catmull-Rom (bouk pou sik yo: mache, kouri,
vole…; yon sèl fwa pou lòt yo: sote, chita…). Pèsonaj la desine BÒ KOTE (pwofil / 3/4) e li gade ADWAT pa defo.

Menm tab la sèvi nan Python (sa a: tès, aperçu Design) ak nan JavaScript paj la (compose.py: K.rigm) — youn pa
ka diferan de lòt. Paj la ajoute sa Python pa ka konnen: pye yo rete ATÈ (pi ba pwen pèsonaj la rete sou tè a),
pozisyon an piksèl videyo, vire (face) ak echèl la.

Spec (sèn): "rig": {"Lina": [{"do": "walk", "to": [1400, 980], "dur": 3}, {"do": "sit"}]}
         oswa "rig": {"Lina": {"face": "right", "idle": true, "ground": true, "do": [...]}}
Aksyon: do (MOTIONS), at (segonn nan sèn nan, oswa yon MO vwa a di: «at»: "attends"), dur, to [x, y] (pwen pye yo,
piksèl videyo), by [dx, dy], path [[x, y]…] (vole pase sou pwen yo), face right|left|auto, speed, amount (0-2),
side r|l (ki bra: wave, point, talk), ease linear|inout|ramp, angles {wòl: deg} (do: pose).
"""
from __future__ import annotations

import math

ROLES = ("hips", "torso", "neck", "head", "arm_l", "forearm_l", "hand_l", "arm_r", "forearm_r", "hand_r",
         "thigh_l", "shin_l", "foot_l", "thigh_r", "shin_r", "foot_r", "wing_l", "wing_r", "tail")
BLEND = 0.25                     # segonn: yon aksyon kòmanse → pòz la glise soti nan sa ki te la
ACTION_KEYS = {"do", "at", "dur", "to", "by", "path", "face", "speed", "amount", "side", "ease", "angles", "steps",
               "expr"}
CHAR_KEYS = {"do", "face", "idle", "ground", "drawn", "expr", "light"}
# LIMYÈ: pèsonaj cut-out la pran limyè dekò a (koulè sèn nan, liy limyè sou yon bò, lonbraj anba pye l, aura) —
# san sa, yon pèsonaj vektè plat sanble l kole sou yon fon Pixar ki gen limyè nwit / bouji.
LIGHTS = {
    "none":   {"tint": None, "amount": 0.0, "bright": 1.0, "rim": None, "shadow": 0.0},
    "day":    {"tint": "#fff2d8", "amount": 0.08, "bright": 1.0, "rim": None, "shadow": 0.38},
    "indoor": {"tint": "#ffd6a0", "amount": 0.16, "bright": 0.96, "rim": None, "shadow": 0.42},
    "dusk":   {"tint": "#d27c58", "amount": 0.24, "bright": 0.94, "rim": "#ffd08a", "rim_side": "right", "rim_w": 4,
               "shadow": 0.45},
    "night":  {"tint": "#3a4f9a", "amount": 0.36, "bright": 0.84, "rim": "#a8c4ff", "rim_side": "right", "rim_w": 4,
               "shadow": 0.5},
    "moon":   {"tint": "#34478f", "amount": 0.34, "bright": 0.86, "rim": "#cfe0ff", "rim_side": "right", "rim_w": 6,
               "shadow": 0.5},
    "candle": {"tint": "#ff9a45", "amount": 0.3, "bright": 0.9, "rim": "#ffb766", "rim_side": "left", "rim_w": 5,
               "shadow": 0.55},
}
LIGHT_ALIAS = {"jou": "day", "jour": "day", "maten": "day", "matin": "day", "dia": "day", "morning": "day",
               "anndan": "indoor", "intérieur": "indoor", "interieur": "indoor", "interior": "indoor",
               "solèy kouche": "dusk", "crépuscule": "dusk", "crepuscule": "dusk", "sunset": "dusk",
               "nwit": "night", "nuit": "night", "noche": "night", "lannwit": "night",
               "lalin": "moon", "lune": "moon", "luna": "moon", "moonlight": "moon",
               "bouji": "candle", "bougie": "candle", "vela": "candle", "candlelight": "candle", "off": "none"}
LIGHT_KEYS = {"preset", "tint", "amount", "bright", "rim", "rim_side", "rim_w", "shadow", "glow", "glow_w"}
# EKSPRESYON figi (kit Design: sousi + vèsyon «X kontan», «ouvè sezi»…): non → kle
EXPRS = {"neutral": "neutral", "nòmal": "neutral", "nomal": "neutral", "normal": "neutral", "neutre": "neutral",
         "happy": "happy", "kontan": "happy", "content": "happy", "joyeux": "happy", "feliz": "happy",
         "sad": "sad", "tris": "sad", "triste": "sad",
         "surprised": "surprised", "sezi": "surprised", "surpris": "surprised", "sorprendido": "surprised",
         "angry": "angry", "fache": "angry", "fâché": "angry", "faché": "angry", "colère": "angry", "enojado": "angry"}
FACES = ("right", "left", "auto")
EASES = ("linear", "inout", "ramp")


def _sample(keys, ph, cycle) -> float:
    """Catmull-Rom sou pwen [faz, ang] yo (faz 0..1). Bouk: pwen anvan / apre yo pran lòt bò a."""
    n = len(keys)
    if n == 0:
        return 0.0
    if n == 1:
        return float(keys[0][1])
    if cycle:
        ph = ph - math.floor(ph)
    else:
        ph = min(1.0, max(0.0, ph))
    i = 0
    while i < n - 2 and keys[i + 1][0] <= ph:
        i += 1
    p1, p2 = keys[i], keys[i + 1]
    span = (p2[0] - p1[0]) or 1e-9
    u = min(1.0, max(0.0, (ph - p1[0]) / span))
    if i > 0:
        p0 = keys[i - 1][1]
    elif cycle and n > 2:
        p0 = keys[n - 2][1]
    else:
        p0 = p1[1]
    if i + 2 < n:
        p3 = keys[i + 2][1]
    elif cycle and n > 2:
        p3 = keys[1][1]
    else:
        p3 = p2[1]
    a, b = p1[1], p2[1]
    u2, u3 = u * u, u * u * u
    return 0.5 * (2 * a + (-p0 + b) * u + (2 * p0 - 5 * a + 4 * b - p3) * u2 + (-p0 + 3 * a - 3 * b + p3) * u3)


def _shift(keys, d):
    """Menm koub la deplase sou faz la (bouk): janm goch = janm dwat + 0.5."""
    out = sorted(((p + d) % 1.0, a) for p, a in keys if p < 1.0)
    if out[0][0] > 0:
        a0 = _sample(keys, (-d) % 1.0, True)
        out.insert(0, (0.0, a0))
    out.append((1.0, out[0][1]))
    return [[round(p, 4), round(a, 3)] for p, a in out]


def _pair(keys_r, cycle_shift=0.5, **other):
    """{role_r: k, role_l: k décalé} pou bra / janm (wòl yo ki fini an _r)."""
    out = dict(other)
    for role, keys in keys_r.items():
        out[role] = keys
        out[role[:-1] + "l"] = _shift(keys, cycle_shift) if cycle_shift else keys
    return out


def _both(keys_r, **other):
    """Menm koub la pou de bò yo (sote, chita: de janm ansanm)."""
    return _pair(keys_r, 0, **other)


def _m(cycle, keys, period=1.0, dur=1.0, stride=0.0, hold=False, move="inout", lift=None, idle=False):
    return {"cycle": cycle, "period": period, "dur": dur, "stride": stride, "hold": hold, "move": move,
            "keys": keys, "lift": lift or [[0, 0], [1, 0]], "idle": idle}


MOTIONS: dict = {
    # ---- sik (bouk)
    "idle": _m(True, {"torso": [[0, 0], [0.5, 1.2], [1, 0]], "head": [[0, 0], [0.5, -1.6], [1, 0]],
                      "arm_r": [[0, 1.5], [0.5, -1], [1, 1.5]], "arm_l": [[0, -1], [0.5, 1.5], [1, -1]],
                      "forearm_r": [[0, -3], [0.5, -5], [1, -3]], "forearm_l": [[0, -3], [0.5, -5], [1, -3]],
                      "tail": [[0, -2], [0.5, 3], [1, -2]], "wing_r": [[0, 0], [0.5, -3], [1, 0]],
                      "wing_l": [[0, 0], [0.5, -3], [1, 0]]}, period=3.4, idle=True),
    "walk": _m(True, _pair({"thigh_r": [[0, -24], [0.5, 18], [1, -24]],
                            "shin_r": [[0, 4], [0.12, 16], [0.32, 4], [0.5, 10], [0.66, 52], [0.85, 22], [1, 4]],
                            "foot_r": [[0, -14], [0.12, 0], [0.42, 6], [0.56, 20], [0.72, 4], [0.9, -8], [1, -14]],
                            "arm_r": [[0, 16], [0.5, -18], [1, 16]],
                            "forearm_r": [[0, -10], [0.5, -30], [1, -10]]},
                           torso=[[0, 4], [0.25, 2], [0.5, 4], [0.75, 2], [1, 4]],
                           head=[[0, -3], [0.25, -1], [0.5, -3], [0.75, -1], [1, -3]],
                           tail=[[0, -4], [0.5, 4], [1, -4]]),
               period=1.1, dur=2.0, stride=0.66, move="ramp"),
    "run": _m(True, _pair({"thigh_r": [[0, -48], [0.45, 26], [0.6, 30], [1, -48]],
                           "shin_r": [[0, 18], [0.15, 34], [0.4, 28], [0.55, 60], [0.7, 105], [0.88, 70], [1, 18]],
                           "foot_r": [[0, -8], [0.15, 4], [0.45, 30], [0.7, 10], [1, -8]],
                           "arm_r": [[0, 42], [0.5, -48], [1, 42]],
                           "forearm_r": [[0, -62], [0.5, -95], [1, -62]]},
                          torso=[[0, 12], [0.25, 14], [0.5, 12], [0.75, 14], [1, 12]],
                          head=[[0, -8], [0.25, -6], [0.5, -8], [0.75, -6], [1, -8]]),
              period=0.62, dur=2.0, stride=1.25, move="ramp",
              lift=[[0, 0], [0.2, 0], [0.3, 0.035], [0.4, 0], [0.7, 0], [0.8, 0.035], [0.9, 0], [1, 0]]),
    "wave": _m(True, {"arm_r": [[0, -92], [0.5, -86], [1, -92]], "forearm_r": [[0, -50], [0.5, -18], [1, -50]],
                      "hand_r": [[0, -15], [0.5, 15], [1, -15]], "head": [[0, -4], [0.5, -2], [1, -4]],
                      "torso": [[0, -1], [1, -1]]}, period=0.9),
    "talk": _m(True, {"arm_r": [[0, -8], [0.5, -22], [1, -8]],
                      "forearm_r": [[0, -15], [0.25, -48], [0.5, -20], [0.75, -52], [1, -15]],
                      "hand_r": [[0, 0], [0.25, -15], [0.5, 5], [1, 0]],
                      "head": [[0, 0], [0.3, -4], [0.6, 3], [1, 0]], "torso": [[0, 0], [0.5, 1.5], [1, 0]]},
               period=2.4),
    "nod": _m(True, {"head": [[0, 0], [0.3, 12], [0.6, -2], [1, 0]], "neck": [[0, 0], [0.3, 4], [1, 0]]},
              period=0.8),
    "fly": _m(True, {"wing_r": [[0, -50], [0.5, 40], [1, -50]], "wing_l": _shift([[0, -50], [0.5, 40], [1, -50]], 0.08),
                     "torso": [[0, -3], [0.5, 3], [1, -3]], "tail": [[0, -6], [0.5, 6], [1, -6]],
                     "head": [[0, 2], [0.5, -2], [1, 2]]},
              period=0.36, dur=2.0, lift=[[0, 0.012], [0.5, -0.012], [1, 0.012]]),
    "glide": _m(True, {"wing_r": [[0, -18], [0.5, -8], [1, -18]], "wing_l": [[0, -16], [0.5, -6], [1, -16]],
                       "tail": [[0, -3], [0.5, 3], [1, -3]], "torso": [[0, 2], [0.5, -2], [1, 2]]},
                period=2.0, dur=2.0, lift=[[0, 0.01], [0.5, -0.01], [1, 0.01]]),
    # ---- yon sèl fwa
    "jump": _m(False, _both({"thigh_r": [[0, 0], [0.22, -45], [0.38, 8], [0.55, -38], [0.75, -12], [0.88, -40], [1, 0]],
                             "shin_r": [[0, 0], [0.22, 75], [0.38, 0], [0.55, 60], [0.75, 15], [0.88, 70], [1, 0]],
                             "foot_r": [[0, 0], [0.22, -28], [0.38, 30], [0.55, 10], [0.75, -5], [0.88, -28], [1, 0]],
                             "arm_r": [[0, 0], [0.22, 45], [0.38, -120], [0.55, -105], [0.75, -40], [0.88, 30], [1, 0]],
                             "forearm_r": [[0, 0], [0.22, -10], [0.38, -10], [0.55, -30], [0.75, -20], [0.88, -15],
                                           [1, 0]]},
                            torso=[[0, 0], [0.22, 26], [0.38, -4], [0.55, 6], [0.75, 10], [0.88, 24], [1, 0]],
                            head=[[0, 0], [0.22, -12], [0.38, -8], [0.55, 0], [0.88, -10], [1, 0]]),
               dur=1.1, move="linear",
               lift=[[0, 0], [0.32, 0], [0.4, 0.06], [0.55, 0.3], [0.7, 0.06], [0.75, 0], [1, 0]]),
    "hop": _m(False, _both({"thigh_r": [[0, 0], [0.3, -25], [0.55, -10], [0.8, -22], [1, 0]],
                            "shin_r": [[0, 0], [0.3, 40], [0.55, 10], [0.8, 38], [1, 0]]},
                           torso=[[0, 0], [0.3, 10], [0.55, 0], [0.8, 8], [1, 0]],
                           tail=[[0, 0], [0.4, -12], [0.8, 8], [1, 0]]),
              dur=0.55, move="linear", lift=[[0, 0], [0.38, 0], [0.55, 0.09], [0.72, 0], [1, 0]]),
    "sit": _m(False, _both({"thigh_r": [[0, 0], [0.4, -30], [1, -88]], "shin_r": [[0, 0], [0.4, 40], [1, 88]],
                            "arm_r": [[0, 0], [0.5, 20], [1, -24]], "forearm_r": [[0, 0], [1, -42]]},
                           torso=[[0, 0], [0.4, 20], [1, 4]], head=[[0, 0], [0.4, -10], [1, 0]]),
              dur=0.9, hold=True),
    "stand": _m(False, _both({"thigh_r": [[0, -88], [0.45, -40], [1, 0]], "shin_r": [[0, 88], [0.45, 50], [1, 0]],
                              "arm_r": [[0, -24], [0.5, 15], [1, 0]], "forearm_r": [[0, -42], [1, 0]]},
                             torso=[[0, 4], [0.4, 22], [1, 0]], head=[[0, 0], [0.4, -8], [1, 0]]),
                dur=0.9, hold=True),
    "point": _m(False, {"arm_r": [[0, 0], [1, -85]], "forearm_r": [[0, 0], [0.5, -20], [1, -5]],
                        "hand_r": [[0, 0], [1, -5]], "head": [[0, 0], [1, -3]], "torso": [[0, 0], [1, -2]]},
                dur=0.6, hold=True),
    "cheer": _m(False, _both({"arm_r": [[0, 0], [1, -105]], "forearm_r": [[0, 0], [1, -50]]},
                             head=[[0, 0], [1, -12]], torso=[[0, 0], [1, -4]]),
                dur=0.7, hold=True, lift=[[0, 0], [0.6, 0.03], [1, 0]]),
    "fall": _m(False, _both({"arm_r": [[0, 0], [0.6, -120], [1, -60]], "thigh_r": [[0, 0], [0.6, -20], [1, -10]],
                             "shin_r": [[0, 0], [1, 20]]},
                            hips=[[0, 0], [0.6, -70], [1, -90]], torso=[[0, 0], [1, 10]],
                            head=[[0, 0], [0.6, 20], [1, -10]]),
               dur=0.8, hold=True, lift=[[0, 0], [0.3, 0.05], [1, 0]]),
    "pose": _m(False, {}, dur=0.4, hold=True),
}
CYCLES = tuple(k for k, v in MOTIONS.items() if v["cycle"])


# ------------------------------------------------------------------ entèpolasyon (menm kalkil ak JS la)
def sample(name: str, ph: float, amount: float = 1.0, side: str = "r", angles: dict | None = None) -> dict:
    """Pòz yon mouvman nan faz ph: {wòl: deg, "_lift": fraksyon wotè}. side "l" = bra / janm goch yo fè travay
    bra / janm dwat yo (wave ak men goch…)."""
    m = MOTIONS[name]
    out = {}
    for role, keys in m["keys"].items():
        if side == "l" and role[-2:] in ("_r", "_l"):
            role = role[:-1] + ("l" if role[-1] == "r" else "r")
        out[role] = _sample(keys, ph, m["cycle"]) * amount
    for role, a in (angles or {}).items():
        out[role] = float(a) * (min(1.0, max(0.0, ph)) if not m["cycle"] else 1.0)
    out["_lift"] = _sample(m["lift"], ph, m["cycle"]) * amount
    return out


def _lerp_pose(a: dict, b: dict, u: float) -> dict:
    return {k: a.get(k, 0.0) + (b.get(k, 0.0) - a.get(k, 0.0)) * u for k in set(a) | set(b)}


def _smooth(u: float) -> float:
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def ease(kind: str, s: float) -> float:
    s = min(1.0, max(0.0, s))
    if kind == "linear":
        return s
    if kind == "ramp":                                   # vitès konstan, ti demaraj / ti frenaj (pye pa glise)
        r = 0.12
        if s < r:
            return s * s / (2 * r * (1 - r))
        if s > 1 - r:
            return 1 - (1 - s) * (1 - s) / (2 * r * (1 - r))
        return (s - r / 2) / (1 - r)
    return s * s * (3 - 2 * s) if s < 1 else 1.0


# ------------------------------------------------------------------ spec
def _num(v, path, err, lo=None, hi=None):
    try:
        x = float(v)
    except (TypeError, ValueError):
        err.append(f"{path}: number")
        return None
    if lo is not None:
        x = max(lo, x)
    if hi is not None:
        x = min(hi, x)
    return x


def _pt(v, path, err):
    if isinstance(v, (list, tuple)) and len(v) == 2:
        a, b = _num(v[0], path, err), _num(v[1], path, err)
        if a is not None and b is not None:
            return [round(a, 2), round(b, 2)]
        return None
    err.append(f"{path}: [x, y] (video pixels)")
    return None


def normalize(rig, path: str, err: list) -> dict | None:
    """Kle `rig` yon sèn → {non: {face, idle, ground, drawn, do: [aksyon…]}}; erè klè pou chak fot."""
    if rig in (None, False, {}, []):
        return None
    if not isinstance(rig, dict):
        err.append(f"{path}: {{\"Lina\": [{{\"do\": \"walk\", \"to\": [1400, 980], \"dur\": 3}}]}}")
        return None
    out = {}
    for name, ch in rig.items():
        p = f"{path}.{name}"
        if isinstance(ch, list):
            ch = {"do": ch}
        if not isinstance(ch, dict):
            err.append(f"{p}: list of actions or {{face, idle, ground, do: [...]}}")
            continue
        bad = set(ch) - CHAR_KEYS
        if bad:
            err.append(f"{p}: unknown key(s) {', '.join(sorted(bad))} (use {', '.join(sorted(CHAR_KEYS))})")
        face = ch.get("face", "right")
        if face not in ("right", "left"):
            err.append(f"{p}.face: right | left")
            face = "right"
        drawn = ch.get("drawn", "right")
        if drawn not in ("right", "left"):
            err.append(f"{p}.drawn: right | left (the way the character was drawn)")
            drawn = "right"
        idle = ch.get("idle", True)
        if idle not in (True, False):
            err.append(f"{p}.idle: true | false")
            idle = True
        ground = ch.get("ground")
        if ground not in (None, True, False):
            err.append(f"{p}.ground: true | false (feet stay on the floor)")
            ground = None
        faces = []                                       # EKSPRESYON: [{at (s / mo vwa a), expr}]
        ex = ch.get("expr")
        for j, f in enumerate([ex] if isinstance(ex, (str, dict)) else (ex or [])):
            f = {"expr": f} if isinstance(f, str) else f
            e_ = EXPRS.get(str((f or {}).get("expr", "")).strip().lower()) if isinstance(f, dict) else None
            if e_ is None or set(f) - {"at", "expr"}:
                err.append(f"{p}.expr[{j}]: {{\"at\": s | word, \"expr\": neutral|happy|sad|surprised|angry "
                           f"(nòmal|kontan|tris|sezi|fache)}}")
                continue
            at = f.get("at", 0)
            faces.append({"at": at.strip() if isinstance(at, str) else (_num(at, f"{p}.expr[{j}].at", err, 0, 600)
                                                                         or 0.0), "expr": e_})
        acts = []
        for i, a in enumerate(ch.get("do") or []):
            ap = f"{p}.do[{i}]"
            if isinstance(a, str):
                a = {"do": a}
            if not isinstance(a, dict):
                err.append(f"{ap}: {{\"do\": \"walk\", ...}}")
                continue
            if "do" not in a and "expr" in a:              # sèlman yon ekspresyon (pa yon mouvman)
                e_ = EXPRS.get(str(a["expr"]).strip().lower())
                if e_ is None:
                    err.append(f"{ap}.expr: neutral|happy|sad|surprised|angry (nòmal|kontan|tris|sezi|fache)")
                else:
                    at = a.get("at")
                    faces.append({"at": at.strip() if isinstance(at, str) else (None if at is None else
                                  _num(at, f"{ap}.at", err, 0, 600)), "expr": e_, "after": len(acts)})
                continue
            bad = set(a) - ACTION_KEYS
            if bad:
                err.append(f"{ap}: unknown key(s) {', '.join(sorted(bad))} (use {', '.join(sorted(ACTION_KEYS))})")
            do = a.get("do")
            if do not in MOTIONS:
                err.append(f"{ap}.do: '{do}' — one of {', '.join(MOTIONS)}")
                continue
            m = MOTIONS[do]
            x = {"do": do, "speed": 1.0, "amount": 1.0, "side": "r", "ease": m["move"], "face": None}
            at = a.get("at")
            if isinstance(at, str) and at.strip():
                x["at"] = at.strip()                         # yon mo vwa a: timeline() jwenn lè l
            elif at is not None:
                x["at"] = _num(at, f"{ap}.at", err, 0.0, 600.0)
            else:
                x["at"] = None
            x["dur"] = _num(a["dur"], f"{ap}.dur", err, 0.1, 120.0) if a.get("dur") is not None else None
            for k in ("to", "by"):
                if a.get(k) is not None:
                    x[k] = _pt(a[k], f"{ap}.{k}", err)
            if a.get("path") is not None:
                pts = a["path"] if isinstance(a["path"], list) else []
                x["path"] = [q for q in (_pt(v, f"{ap}.path[{j}]", err) for j, v in enumerate(pts)) if q]
                if not x["path"]:
                    err.append(f"{ap}.path: [[x, y], [x, y], ...] (video pixels)")
                    x.pop("path")
            if sum(k in x for k in ("to", "by", "path")) > 1:
                err.append(f"{ap}: use only one of to / by / path")
            if a.get("face") is not None:
                if a["face"] in FACES:
                    x["face"] = a["face"]
                else:
                    err.append(f"{ap}.face: right | left | auto")
            if a.get("speed") is not None:
                x["speed"] = _num(a["speed"], f"{ap}.speed", err, 0.1, 5.0) or 1.0
            if a.get("amount") is not None:
                v = _num(a["amount"], f"{ap}.amount", err, 0.0, 2.0)
                x["amount"] = 1.0 if v is None else v
            if a.get("side") is not None:
                if a["side"] in ("r", "l", "right", "left"):
                    x["side"] = a["side"][0]
                else:
                    err.append(f"{ap}.side: r | l (which arm / leg)")
            if a.get("ease") is not None:
                if a["ease"] in EASES:
                    x["ease"] = a["ease"]
                else:
                    err.append(f"{ap}.ease: {' | '.join(EASES)}")
            if a.get("angles") is not None:
                if isinstance(a["angles"], dict) and all(r in ROLES for r in a["angles"]):
                    x["angles"] = {r: _num(v, f"{ap}.angles.{r}", err) or 0.0 for r, v in a["angles"].items()}
                else:
                    err.append(f"{ap}.angles: {{role: degrees}} — roles: {', '.join(ROLES)}")
            if a.get("expr") is not None:                   # ekspresyon an chanje lè aksyon an kòmanse
                e_ = EXPRS.get(str(a["expr"]).strip().lower())
                if e_ is None:
                    err.append(f"{ap}.expr: neutral|happy|sad|surprised|angry (nòmal|kontan|tris|sezi|fache)")
                else:
                    x["expr"] = e_
            st = a.get("steps")                              # son pa yo (bibliyotèk SFX la): true | sifas
            if st not in (None, False):
                from .sounds import SURFACES
                if st is True:
                    st = "soft"
                if do not in STEP_PHASES and do not in LAND_PHASE:
                    err.append(f"{ap}.steps: only for {', '.join([*STEP_PHASES, *LAND_PHASE])}")
                elif st not in SURFACES:
                    err.append(f"{ap}.steps: true | {' | '.join(SURFACES)}")
                else:
                    x["steps"] = st
            acts.append(x)
        out[str(name)] = {"face": face, "drawn": drawn, "idle": idle, "ground": ground, "do": acts, "expr": faces}
        lt = normalize_light(ch.get("light"), f"{p}.light", err)
        if lt is not None:
            out[str(name)]["light"] = lt
    return out or None


def _hex(v) -> str | None:
    if isinstance(v, str) and len(v.strip()) in (4, 7) and v.strip().startswith("#"):
        v = v.strip().lower()
        if len(v) == 4:
            v = "#" + "".join(c * 2 for c in v[1:])
        try:
            int(v[1:], 16)
            return v
        except ValueError:
            return None
    return None


def normalize_light(v, path: str, err: list) -> dict | None:
    """`light` yon pèsonaj: "auto" (koulè dekò a, kalkile sou imaj fon sèn nan) | preset (night, moon, candle, dusk,
    day, indoor, none — kreyòl / franse aksepte) | {preset?, tint, amount 0-1, bright, rim, rim_side left|right|top,
    rim_w px, shadow 0-1, glow, glow_w px}. → diksyonè konplè (oswa {"auto": True, …}) / None."""
    if v in (None, False):
        return None
    if v is True:
        v = "auto"
    if isinstance(v, str):
        v = {"preset": v}
    if not isinstance(v, dict):
        err.append(f"{path}: \"auto\" | {' | '.join(LIGHTS)} | {{preset, tint, amount, rim, rim_side, shadow, glow}}")
        return None
    bad = set(v) - LIGHT_KEYS
    if bad:
        err.append(f"{path}: unknown key(s) {', '.join(sorted(bad))} (use {', '.join(sorted(LIGHT_KEYS))})")
    pre = str(v.get("preset") or "").strip().lower()
    out: dict = {}
    if pre in ("auto", "otomatik", "automatique"):
        out["auto"] = True
        base = dict(LIGHTS["night"])
    elif pre:
        pre = LIGHT_ALIAS.get(pre, pre)
        if pre not in LIGHTS:
            err.append(f"{path}.preset: auto | {' | '.join(LIGHTS)}")
            pre = "none"
        base = dict(LIGHTS[pre])
    else:
        base = dict(LIGHTS["none"])
    base.setdefault("rim_side", "right")
    base.setdefault("rim_w", 4)
    base.setdefault("glow", None)
    base.setdefault("glow_w", 16)
    for k in ("tint", "rim", "glow"):
        if k in v:
            if v[k] in (None, False, ""):
                base[k] = None
                out.setdefault("set", []).append(k)
            elif _hex(v[k]):
                base[k] = _hex(v[k])
                out.setdefault("set", []).append(k)
            else:
                err.append(f"{path}.{k}: #rrggbb")
    for k, lo, hi in (("amount", 0, 1), ("bright", 0.2, 1.6), ("shadow", 0, 1), ("rim_w", 0, 40), ("glow_w", 0, 120)):
        if v.get(k) is not None:
            n = _num(v[k], f"{path}.{k}", err, lo, hi)
            if n is not None:
                base[k] = n
                out.setdefault("set", []).append(k)
    if v.get("rim_side") is not None:
        if v["rim_side"] in ("left", "right", "top"):
            base["rim_side"] = v["rim_side"]
            out.setdefault("set", []).append("rim_side")
        else:
            err.append(f"{path}.rim_side: left | right | top")
    out.update(base)
    return out


def light_from_image(data: bytes) -> dict | None:
    """LIMYÈ OTOMATIK: imaj fon sèn nan → koulè ambyans (mwayèn), fòs (pi fonse = pi fò), liy limyè (koulè piksèl ki
    pi klere yo) ak bò li soti (gòch / dwat). Pillow (opsyonèl); san li → None."""
    try:
        import io
        from PIL import Image
        im = Image.open(io.BytesIO(data)).convert("RGB").resize((64, 36))
    except Exception:                                    # noqa: BLE001 — pa Pillow / imaj kase: limyè fiks
        return None
    px = list(im.getdata())
    n = len(px)
    lum = [0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2] for p in px]
    mean = [sum(p[i] for p in px) / n for i in range(3)]
    luma = sum(lum) / n / 255
    top = sorted(range(n), key=lambda i: -lum[i])[:max(4, n // 30)]
    hi = [sum(px[i][c] for i in top) / len(top) for c in range(3)]
    xs = sum(i % 64 for i in top) / len(top) / 63
    peak = max(mean) or 1
    tint = "#" + "".join(f"{int(min(255, c / peak * 255)):02x}" for c in mean)      # koulè san fènwa a
    rim = "#" + "".join(f"{int(min(255, c * 1.08)):02x}" for c in hi)
    dark = 1 - min(1.0, luma / 0.55)
    return {"tint": tint, "amount": round(0.1 + 0.3 * dark, 3), "bright": round(1 - 0.18 * dark, 3),
            "rim": rim if dark > 0.25 else None, "rim_side": "left" if xs < 0.45 else "right",
            "rim_w": 4 + round(3 * dark), "shadow": round(0.38 + 0.17 * dark, 3)}


def scene_image(sc: dict, base=None) -> bytes | None:
    """Pi gwo imaj fon sèn nan (Design HTML: data URI / src, oswa background spec la) — pou limyè otomatik."""
    import base64
    import re
    bg = sc.get("background")
    src = (bg.get("src") or bg.get("image")) if isinstance(bg, dict) else (bg if isinstance(bg, str) else None)
    best = None
    markup = _scene_markup(sc, base)
    for m in re.finditer(r"data:image/(?:png|jpe?g|webp);base64,([A-Za-z0-9+/=]+)", markup or ""):
        if best is None or len(m.group(1)) > len(best):
            best = m.group(1)
    if best:
        try:
            return base64.b64decode(best)
        except ValueError:
            pass
    cands = [src] if isinstance(src, str) and not src.startswith("#") else []
    cands += re.findall(r'<img[^>]+src="([^"]+)"', markup or "")
    from .media import resolve as _res
    for c in cands:
        try:
            p = _res(c, base)
            if p and p.is_file():
                return p.read_bytes()
        except Exception:                                # noqa: BLE001
            continue
    return None


def resolve_lights(rig: dict | None, sc: dict, base=None) -> dict | None:
    """`light: auto` → valè kalkile sou imaj fon sèn nan (sa devlopè a mete alamen yo rete)."""
    if not rig or not any((ch.get("light") or {}).get("auto") is True for ch in rig.values()):
        return rig
    data = scene_image(sc, base)
    auto = light_from_image(data) if data else None
    out = {}
    for name, ch in rig.items():
        lt = ch.get("light")
        if lt and lt.get("auto") is True:
            keep = {k: lt[k] for k in lt.get("set", [])}
            lt = {**lt, **(auto or {}), **keep, "auto": "done" if auto else "none"}
        out[name] = dict(ch, light=lt) if lt else ch
    return out


def resolve(rig: dict | None, words: list | None = None, scene_start: float = 0.0) -> dict | None:
    """Lè aksyon yo (segonn nan sèn nan): «at» yon mo → lè vwa a di l; pa gen «at» → apre aksyon anvan an.
    words = [{w, s, e}] (lè videyo a). Retounen yon kopi ak at / dur chif."""
    if not rig:
        return None
    from .compose import _find_word
    out = {}

    def when(at, default):
        if isinstance(at, str):
            wd = _find_word(words or [], at, scene_start) if words else None
            return round(wd["s"] - scene_start, 3) if wd else default
        return round(default if at is None else float(at), 3)
    for name, ch in rig.items():
        t, acts, ends = 0.0, [], [0.0]
        for a in ch["do"]:
            a = dict(a)
            at = a.get("at")
            if isinstance(at, str):
                wd = _find_word(words or [], at, scene_start) if words else None
                at = round(wd["s"] - scene_start, 3) if wd else None
                a["word"] = a["at"]
            a["at"] = round(t if at is None else float(at), 3)
            m = MOTIONS[a["do"]]
            a["dur"] = round(a["dur"] if a.get("dur") else (2.0 if m["cycle"] else m["dur"]), 3)
            t = a["at"] + a["dur"]
            ends.append(t)
            acts.append(a)
        faces = [{"at": a["at"], "expr": a["expr"]} for a in acts if a.get("expr")]
        for f in ch.get("expr") or []:                   # «after» = pozisyon l nan lis aksyon an (pa gen «at»)
            faces.append({"at": when(f["at"], ends[min(f.get("after", 0), len(ends) - 1)]), "expr": f["expr"]})
        acts.sort(key=lambda a: a["at"])
        out[name] = dict(ch, do=acts, expr=sorted(faces, key=lambda f: f["at"]))
    return out


def expr_at(ch: dict, loc: float) -> str:
    """Ekspresyon figi a nan lè loc (dènye chanjman ki deja fèt; «neutral» anvan)."""
    e = "neutral"
    for f in ch.get("expr") or []:
        if f["at"] <= loc + 1e-9:
            e = f["expr"]
    return e


def need(rig: dict | None) -> float:
    """Dire minimòm sèn nan pou tout aksyon yo fini (+ yon ti tan pou pòz la rete)."""
    if not rig:
        return 0.0
    ends = [a["at"] + a["dur"] for ch in rig.values() for a in ch["do"]] + \
        [f["at"] + 0.8 for ch in rig.values() for f in ch.get("expr") or []]
    return round(max(ends) + 0.6, 3) if ends else 0.0


# ------------------------------------------------------------------ pòz nan yon moman (aperçu, tès)
def _phase(a: dict, m: dict, loc: float, dist: float | None, height: float) -> float:
    if not m["cycle"]:
        return (loc - a["at"]) / a["dur"]
    if dist is not None and m["stride"] and height > 0:
        return dist / (m["stride"] * height)            # pye yo swiv distans lan: yo pa glise sou tè a
    return (loc - a["at"]) * a["speed"] / m["period"]


def _base(ch: dict, loc: float) -> dict:
    return sample("idle", loc / MOTIONS["idle"]["period"]) if ch.get("idle", True) else {"_lift": 0.0}


def _own(ch: dict, i: int, t: float, height: float, dists) -> dict:
    a = ch["do"][i]
    d = dists(i, t) if dists else None
    return sample(a["do"], _phase(a, MOTIONS[a["do"]], t, d, height), a["amount"], a["side"], a.get("angles"))


def _state(ch: dict, i: int, loc: float, height: float, dists) -> dict:
    """Pòz la apre aksyon 0..i. Yon mouvman chanje SÈLMAN wòl li konnen yo: rès kò a kenbe pòz anvan an (Lina
    chita epi l fè siy: janm yo rete chita). Yon sik ki fini → tounen nan pòz anba a; yon «hold» rete."""
    under = _state(ch, i - 1, loc, height, dists) if i > 0 else _base(ch, loc)
    if i < 0:
        return under
    a = ch["do"][i]
    m = MOTIONS[a["do"]]
    end = a["at"] + a["dur"]
    if loc <= end or m["hold"]:
        cur = {**under, **_own(ch, i, min(loc, end), height, dists)}
    else:
        last = {**under, **_own(ch, i, end, height, dists)}
        cur = _lerp_pose(last, under, _smooth((loc - end) / BLEND))
    u = (loc - a["at"]) / BLEND
    return _lerp_pose(under, cur, _smooth(u)) if u < 1 else cur


def pose_at(ch: dict, loc: float, height: float = 0.0, dists=None) -> dict:
    """Ang chak wòl + "_lift" nan lè loc (segonn nan sèn nan) pou yon pèsonaj (normalize + resolve). dists(i, t)
    = distans pèsonaj la deja fè nan aksyon i (pou mache / kouri); None = faz la swiv tan an."""
    i = -1
    for k, a in enumerate(ch["do"]):
        if a["at"] <= loc:
            i = k
    return _state(ch, i, loc, height, dists)


def _catmull_line(pts: list, steps: int = 16) -> list:
    """Pwen yo → yon liy ki koube dous (Catmull-Rom) pase sou chak pwen; 2 pwen = liy dwat."""
    if len(pts) <= 2:
        return [list(p) for p in pts]
    out = [list(pts[0])]
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(0, i - 1)], pts[i], pts[i + 1]
        p3 = pts[min(len(pts) - 1, i + 2)]
        for s in range(1, steps + 1):
            u = s / steps
            u2, u3 = u * u, u * u * u
            out.append([0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2
                               + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in (0, 1)])
    return out


def plan(ch: dict, ground: tuple, face0: str | None = None) -> list:
    """Chemen pèsonaj la pou chak aksyon: [{line, len, cum, face}] — line = pwen yo (piksèl videyo), face = 1
    (adwat) / -1 (agoch). ground = pwen pye yo nan Design la (piksèl videyo)."""
    cur = [float(ground[0]), float(ground[1])]
    face = 1 if (face0 or ch.get("face", "right")) == "right" else -1
    out = []
    for a in ch["do"]:
        if a.get("to"):
            pts = [cur, list(a["to"])]
        elif a.get("by"):
            pts = [cur, [cur[0] + a["by"][0], cur[1] + a["by"][1]]]
        elif a.get("path"):
            pts = [cur] + [list(p) for p in a["path"]]
        else:
            pts = [cur]
        line = _catmull_line(pts)
        cum = [0.0]
        for p, q in zip(line, line[1:]):
            cum.append(cum[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
        dx = line[-1][0] - line[0][0]
        f = a.get("face") or ("auto" if cum[-1] > 1 else None)
        if f == "right":
            face = 1
        elif f == "left":
            face = -1
        elif f == "auto" and abs(dx) > 1:
            face = 1 if dx > 0 else -1
        out.append({"line": line, "len": cum[-1], "cum": cum, "face": face})
        cur = list(line[-1])
    return out


def _along(seg: dict, d: float) -> list:
    line, cum = seg["line"], seg["cum"]
    if len(line) == 1 or d <= 0:
        return list(line[0])
    if d >= cum[-1]:
        return list(line[-1])
    i = 0
    while cum[i + 1] < d:
        i += 1
    u = (d - cum[i]) / ((cum[i + 1] - cum[i]) or 1e-9)
    return [line[i][k] + (line[i + 1][k] - line[i][k]) * u for k in (0, 1)]


def dist_in(ch: dict, segs: list, i: int, t: float) -> float | None:
    """Distans pèsonaj la fè nan aksyon i nan lè t (None = li pa deplase)."""
    a, s = ch["do"][i], segs[i]
    if s["len"] <= 1e-6:
        return None
    return ease(a["ease"], (t - a["at"]) / a["dur"]) * s["len"]


def root_at(ch: dict, segs: list, loc: float, ground: tuple, face0: str | None = None) -> tuple:
    """(x, y, face) pye pèsonaj la nan lè loc (piksèl videyo). Yon aksyon ki pa deplase (fè siy pandan l ap
    kouri) pa chanje pozisyon an: se aksyon ki deplase yo ki konte."""
    x, y = float(ground[0]), float(ground[1])
    face = 1 if (face0 or ch.get("face", "right")) == "right" else -1
    for k, a in enumerate(ch["do"]):
        if a["at"] > loc:
            continue
        if segs[k]["len"] > 1e-6:
            x, y = _along(segs[k], dist_in(ch, segs, k, min(loc, a["at"] + a["dur"])))
        face = segs[k]["face"]
    return x, y, face


def frame_at(ch: dict, loc: float, ground: tuple, height: float) -> dict:
    """Tout sa paj la bezwen nan yon moman: {pose: {wòl: deg}, lift (piksèl), x, y, face} — referans pou tès JS la."""
    segs = plan(ch, ground)
    pose = pose_at(ch, loc, height, lambda i, t: dist_in(ch, segs, i, t))
    x, y, face = root_at(ch, segs, loc, ground)
    lift = pose.pop("_lift", 0.0) * height
    return {"pose": pose, "lift": lift, "x": x, "y": y, "face": face, "expr": expr_at(ch, loc)}


# ------------------------------------------------------------------ MENM KALKIL LA AN JAVASCRIPT (paj Kadans la)
# Fonksyon pi (pa gen DOM): compose.py mete yo nan paj la; tès la kouri yo ak Node epi konpare ak Python an.
# RIGM = MOTIONS (K.rigm nan paj la).
JS = r"""
const RIG_BLEND = %(blend)s;
function rigSample(keys, ph, cycle) {
  const n = keys.length; if (!n) return 0; if (n === 1) return +keys[0][1];
  ph = cycle ? ph - Math.floor(ph) : Math.min(1, Math.max(0, ph));
  let i = 0; while (i < n - 2 && keys[i + 1][0] <= ph) i++;
  const p1 = keys[i], p2 = keys[i + 1], span = (p2[0] - p1[0]) || 1e-9;
  const u = Math.min(1, Math.max(0, (ph - p1[0]) / span));
  const p0 = i > 0 ? keys[i - 1][1] : (cycle && n > 2 ? keys[n - 2][1] : p1[1]);
  const p3 = i + 2 < n ? keys[i + 2][1] : (cycle && n > 2 ? keys[1][1] : p2[1]);
  const a = p1[1], b = p2[1], u2 = u * u, u3 = u2 * u;
  return 0.5 * (2 * a + (-p0 + b) * u + (2 * p0 - 5 * a + 4 * b - p3) * u2 + (-p0 + 3 * a - 3 * b + p3) * u3);
}
function rigMotion(M, name, ph, amount, side, angles) {
  const m = M[name], out = {};
  for (let role in m.keys) {
    const k = m.keys[role];
    if (side === "l" && /_[rl]$/.test(role)) role = role.slice(0, -1) + (role.slice(-1) === "r" ? "l" : "r");
    out[role] = rigSample(k, ph, m.cycle) * amount;
  }
  if (angles) for (const r in angles) out[r] = +angles[r] * (m.cycle ? 1 : Math.min(1, Math.max(0, ph)));
  out._lift = rigSample(m.lift, ph, m.cycle) * amount;
  return out;
}
function rigLerp(a, b, u) {
  const o = {};
  for (const k in a) o[k] = a[k] + ((k in b ? b[k] : 0) - a[k]) * u;
  for (const k in b) if (!(k in a)) o[k] = b[k] * u;
  return o;
}
const rigSmooth = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };
function rigEase(kind, s) {
  s = Math.min(1, Math.max(0, s));
  if (kind === "linear") return s;
  if (kind === "ramp") { const r = 0.12;
    if (s < r) return s * s / (2 * r * (1 - r));
    if (s > 1 - r) return 1 - (1 - s) * (1 - s) / (2 * r * (1 - r));
    return (s - r / 2) / (1 - r); }
  return s < 1 ? s * s * (3 - 2 * s) : 1;
}
function rigBase(M, ch, loc) { return ch.idle !== false ? rigMotion(M, "idle", loc / M.idle.period, 1, "r") : { _lift: 0 }; }
function rigPhase(a, m, t, d, height) {
  if (!m.cycle) return (t - a.at) / a.dur;
  if (d !== null && m.stride && height > 0) return d / (m.stride * height);
  return (t - a.at) * a.speed / m.period;
}
function rigOwn(M, ch, i, t, height, dists) {
  const a = ch.do[i], d = dists ? dists(i, t) : null;
  return rigMotion(M, a.do, rigPhase(a, M[a.do], t, d, height), a.amount, a.side, a.angles);
}
function rigState(M, ch, i, loc, height, dists) {
  const under = i > 0 ? rigState(M, ch, i - 1, loc, height, dists) : rigBase(M, ch, loc);
  if (i < 0) return under;
  const a = ch.do[i], m = M[a.do], end = a.at + a.dur;
  let cur;
  if (loc <= end || m.hold) cur = Object.assign({}, under, rigOwn(M, ch, i, Math.min(loc, end), height, dists));
  else cur = rigLerp(Object.assign({}, under, rigOwn(M, ch, i, end, height, dists)), under, rigSmooth((loc - end) / RIG_BLEND));
  const u = (loc - a.at) / RIG_BLEND;
  return u < 1 ? rigLerp(under, cur, rigSmooth(u)) : cur;
}
function rigActive(ch, loc) { let i = -1; ch.do.forEach((a, k) => { if (a.at <= loc) i = k; }); return i; }
function rigLine(pts) {
  if (pts.length <= 2) return pts.map(p => [p[0], p[1]]);
  const out = [[pts[0][0], pts[0][1]]], steps = 16;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let s = 1; s <= steps; s++) {
      const u = s / steps, u2 = u * u, u3 = u2 * u, q = [];
      for (const k of [0, 1]) q.push(0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2
                                       + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3));
      out.push(q);
    }
  }
  return out;
}
function rigPlan(ch, ground) {
  let cur = [+ground[0], +ground[1]], face = (ch.face || "right") === "right" ? 1 : -1;
  return ch.do.map(a => {
    let pts = [cur];
    if (a.to) pts = [cur, a.to]; else if (a.by) pts = [cur, [cur[0] + a.by[0], cur[1] + a.by[1]]];
    else if (a.path) pts = [cur].concat(a.path);
    const line = rigLine(pts), cum = [0];
    for (let i = 1; i < line.length; i++) cum.push(cum[i - 1] + Math.hypot(line[i][0] - line[i - 1][0], line[i][1] - line[i - 1][1]));
    const len = cum[cum.length - 1], dx = line[line.length - 1][0] - line[0][0];
    const f = a.face || (len > 1 ? "auto" : null);
    if (f === "right") face = 1; else if (f === "left") face = -1; else if (f === "auto" && Math.abs(dx) > 1) face = dx > 0 ? 1 : -1;
    cur = line[line.length - 1].slice();
    return { line, cum, len, face };
  });
}
function rigAlong(s, d) {
  const L = s.line, C = s.cum;
  if (L.length === 1 || d <= 0) return L[0].slice();
  if (d >= C[C.length - 1]) return L[L.length - 1].slice();
  let i = 0; while (C[i + 1] < d) i++;
  const u = (d - C[i]) / ((C[i + 1] - C[i]) || 1e-9);
  return [L[i][0] + (L[i + 1][0] - L[i][0]) * u, L[i][1] + (L[i + 1][1] - L[i][1]) * u];
}
function rigDist(ch, segs, i, t) {
  const a = ch.do[i], s = segs[i];
  return s.len <= 1e-6 ? null : rigEase(a.ease, (t - a.at) / a.dur) * s.len;
}
// tout sa yon imaj bezwen: {pose, lift (px), x, y, face} — menm rezilta ak motion.frame_at() nan Python
function rigFrame(M, ch, loc, ground, height, segs) {
  segs = segs || rigPlan(ch, ground);
  const pose = rigState(M, ch, rigActive(ch, loc), loc, height, (i, t) => rigDist(ch, segs, i, t));
  const lift = (pose._lift || 0) * height; delete pose._lift;
  let x = +ground[0], y = +ground[1], face = (ch.face || "right") === "right" ? 1 : -1;
  ch.do.forEach((a, k) => {
    if (a.at > loc) return;
    if (segs[k].len > 1e-6) { const p = rigAlong(segs[k], rigDist(ch, segs, k, Math.min(loc, a.at + a.dur))); x = p[0]; y = p[1]; }
    face = segs[k].face;
  });
  return { pose, lift, x, y, face, expr: rigExpr(ch, loc) };
}
function rigExpr(ch, loc) {                          // ekspresyon figi a nan lè loc (motion.expr_at)
  let e = "neutral";
  for (const f of (ch && ch.expr) || []) if (f.at <= loc + 1e-9) e = f.expr;
  return e;
}
""" % {"blend": BLEND}


# ------------------------------------------------------------------ SON PA YO (bibliyotèk SFX la)
STEP_PHASES = {"walk": 0.42, "run": 0.62}            # volim; yon pye touche tè a chak demi sik (faz 0, 0.5, 1…)
LAND_PHASE = {"jump": 0.75, "hop": 0.72}             # faz kote l ateri


def rig_defs(markup: str) -> dict:
    """{non: rigdef} li nan HTML Design la (data-rigdef: pwen pye yo, wotè an piksèl videyo…)."""
    import html as _h
    import json as _j
    import re as _re
    out = {}
    for m in _re.finditer(r'data-rigdef="([^"]*)"', markup or ""):
        try:
            d = _j.loads(_h.unescape(m.group(1)))
            out[d.get("name", "")] = d
        except ValueError:
            pass
    return out


def _scene_markup(sc: dict, base) -> str:
    if sc.get("html"):
        return sc["html"]
    if sc.get("src"):
        from .media import resolve as _res
        p = _res(sc["src"], base)
        try:
            return p.read_text(encoding="utf-8") if p.suffix.lower() in (".html", ".htm") else ""
        except OSError:
            return ""
    return ""


def step_cues(sc: dict, t: dict, base=None) -> list[dict]:
    """Son chak pa (walk / run: chak fwa yon pye touche tè a, menm faz ak animasyon an) ak chak aterisaj
    (jump / hop) pou aksyon ki gen «steps» — lè videyo a."""
    rig = t.get("rig")
    if not rig or not any(a.get("steps") for ch in rig.values() for a in ch["do"]):
        return []
    from .sounds import SURFACES
    defs = rig_defs(_scene_markup(sc, base))
    low = {k.lower(): v for k, v in defs.items()}
    out = []
    for name, ch in rig.items():
        d = defs.get(name) or low.get(name.lower())
        if not d:
            continue
        segs = plan(ch, d["ground"], None)
        height = float(d.get("h") or 0)
        for i, a in enumerate(ch["do"]):
            if not a.get("steps"):
                continue
            src = "sfx:" + SURFACES[a["steps"]]
            m = MOTIONS[a["do"]]
            if a["do"] in LAND_PHASE:
                out.append({"src": src, "t": round(t["start"] + a["at"] + LAND_PHASE[a["do"]] * a["dur"], 3),
                            "dur": None, "volume": 0.8 * a["amount"], "loop": False, "fade": None, "bus": "fx"})
                continue
            n_prev, k = None, 0
            steps = int(a["dur"] * 200)
            for j in range(steps + 1):
                tt = a["at"] + a["dur"] * j / steps
                ph = _phase(a, m, tt, dist_in(ch, segs, i, tt), height)
                n = int(math.floor(ph * 2 + 1e-9))
                if n_prev is not None and n > n_prev:
                    out.append({"src": src, "t": round(t["start"] + tt, 3), "dur": None,
                                "volume": STEP_PHASES[a["do"]] * (0.85 + 0.3 * (k % 2)), "loop": False, "fade": None,
                                "bus": "fx"})
                    k += 1
                n_prev = n
    return out


def doc() -> str:
    """Lis mouvman yo pou dokimantasyon / zouti AI yo."""
    cyc = ", ".join(CYCLES)
    one = ", ".join(k for k in MOTIONS if k not in CYCLES)
    return f"loops: {cyc} · once: {one} (hold = sit, stand, point, cheer, fall, pose stay)"
