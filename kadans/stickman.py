"""STICKMAN RIG SVG & CANVAS — Kadans Video Engine & Design WASDEV.

Motè jenerasyon pèsonaj Stickman Rig 100% konpatib ak Kadans (motion.py, compose.py, story_kadans.py).
Konfòm ak 16 zo estanda (ROLES), lipsync bouch (data-mouth), je k ap bat (data-eyes),
ekspresyon sousi (data-brows), ak akseswa entèaktif (laptop, linèt, chapo, krawat, mikwo, telefòn).
"""
from __future__ import annotations

import html
import json
import re
from typing import Any

# 16 zo estanda ki koresponn ak ROLES nan kadans.motion
STICKMAN_BONES = [
    {"id": "hips", "name": "Bassin", "role": "hips", "parent": None, "p": [100.0, 190.0], "a": 0.0},
    {"id": "torso", "name": "Torse", "role": "torso", "parent": "hips", "p": [100.0, 190.0], "a": 0.0},
    {"id": "neck", "name": "Cou", "role": "neck", "parent": "torso", "p": [100.0, 100.0], "a": 0.0},
    {"id": "head", "name": "Tête", "role": "head", "parent": "neck", "p": [100.0, 85.0], "a": 0.0},
    {"id": "arm_l", "name": "Bras G", "role": "arm_l", "parent": "torso", "p": [98.0, 105.0], "a": 0.0},
    {"id": "forearm_l", "name": "Avant-bras G", "role": "forearm_l", "parent": "arm_l", "p": [90.0, 150.0], "a": 0.0},
    {"id": "hand_l", "name": "Main G", "role": "hand_l", "parent": "forearm_l", "p": [85.0, 195.0], "a": 0.0},
    {"id": "arm_r", "name": "Bras D", "role": "arm_r", "parent": "torso", "p": [102.0, 105.0], "a": 0.0},
    {"id": "forearm_r", "name": "Avant-bras D", "role": "forearm_r", "parent": "arm_r", "p": [110.0, 150.0], "a": 0.0},
    {"id": "hand_r", "name": "Main D", "role": "hand_r", "parent": "forearm_r", "p": [115.0, 195.0], "a": 0.0},
    {"id": "thigh_l", "name": "Cuisse G", "role": "thigh_l", "parent": "hips", "p": [100.0, 190.0], "a": 0.0},
    {"id": "shin_l", "name": "Jambe G", "role": "shin_l", "parent": "thigh_l", "p": [95.0, 260.0], "a": 0.0},
    {"id": "foot_l", "name": "Pied G", "role": "foot_l", "parent": "shin_l", "p": [95.0, 335.0], "a": 0.0},
    {"id": "thigh_r", "name": "Cuisse D", "role": "thigh_r", "parent": "hips", "p": [100.0, 190.0], "a": 0.0},
    {"id": "shin_r", "name": "Jambe D", "role": "shin_r", "parent": "thigh_r", "p": [105.0, 260.0], "a": 0.0},
    {"id": "foot_r", "name": "Pied D", "role": "foot_r", "parent": "shin_r", "p": [105.0, 335.0], "a": 0.0},
]

STICKMAN_PALETTES = {
    "cyan": {"primary": "#00E5FF", "glow": "rgba(0, 229, 255, 0.4)", "fill": "rgba(10, 18, 32, 0.95)", "accent": "#7C3AED"},
    "purple": {"primary": "#A855F7", "glow": "rgba(168, 85, 247, 0.4)", "fill": "rgba(18, 13, 31, 0.95)", "accent": "#00E5FF"},
    "orange": {"primary": "#FF7A00", "glow": "rgba(255, 122, 0, 0.4)", "fill": "rgba(26, 14, 8, 0.95)", "accent": "#FFD600"},
    "green": {"primary": "#10B981", "glow": "rgba(16, 185, 129, 0.4)", "fill": "rgba(8, 24, 18, 0.95)", "accent": "#34D399"},
    "gold": {"primary": "#F59E0B", "glow": "rgba(245, 158, 11, 0.4)", "fill": "rgba(26, 20, 8, 0.95)", "accent": "#FDE047"},
    "white": {"primary": "#F8FAFC", "glow": "rgba(255, 255, 255, 0.25)", "fill": "rgba(15, 23, 42, 0.95)", "accent": "#38BDF8"},
    "blue": {"primary": "#3B82F6", "glow": "rgba(59, 130, 246, 0.4)", "fill": "rgba(10, 16, 32, 0.95)", "accent": "#60A5FA"},
    "red": {"primary": "#EF4444", "glow": "rgba(239, 68, 68, 0.4)", "fill": "rgba(28, 10, 12, 0.95)", "accent": "#F87171"},
}


def _pt_attr(w: float = 200.0, h: float = 360.0) -> str:
    """Atribi data-pt pou chak zo (matris idantite + bwat)."""
    pt = {"P": [1.0, 0.0, 0.0, 1.0, 0.0, 0.0], "w": round(w, 2), "h": round(h, 2),
          "rot": 0.0, "fx": 1, "fy": 1}
    return html.escape(json.dumps(pt), quote=True)


def _render_prop(prop_name: str, primary: str, accent: str, sw: float) -> dict[str, str]:
    """Retounen eleman grafik akseswa a pou zo ki koresponn lan."""
    p = (prop_name or "").lower().strip()
    res = {}
    if p in ("laptop", "ordinateur", "pc"):
        # Laptop atache ak forearm_r oswa torso
        laptop_svg = f"""
        <g class="prop prop-laptop" transform="translate(100, 160)">
          <!-- Baz laptop -->
          <polygon points="5,22 45,22 55,27 -5,27" fill="#1E293B" stroke="{primary}" stroke-width="1.8"/>
          <!-- Ekran louvri -->
          <polygon points="5,22 45,22 43,-8 7,-8" fill="#0F172A" stroke="{primary}" stroke-width="1.8"/>
          <!-- Ekran k ap klere ak kòd -->
          <rect x="9" y="-5" width="32" height="24" fill="#080C14" rx="1"/>
          <text x="14" y="8" fill="{accent}" font-family="monospace" font-size="9" font-weight="bold">&lt;/&gt;</text>
          <!-- Ti liy kòd -->
          <line x1="13" y1="13" x2="33" y2="13" stroke="{primary}" stroke-width="1.2" opacity="0.8"/>
        </g>
        """
        res["forearm_r"] = laptop_svg
    elif p in ("glasses", "linèt", "lunettes"):
        # Linèt entelijan sou tèt la
        glasses_svg = f"""
        <g class="prop prop-glasses" transform="translate(0, 0)">
          <rect x="83" y="44" width="14" height="9" rx="2" fill="none" stroke="{accent}" stroke-width="2"/>
          <rect x="103" y="44" width="14" height="9" rx="2" fill="none" stroke="{accent}" stroke-width="2"/>
          <line x1="97" y1="48" x2="103" y2="48" stroke="{accent}" stroke-width="2"/>
          <line x1="77" y1="47" x2="83" y2="47" stroke="{accent}" stroke-width="1.5"/>
          <line x1="117" y1="47" x2="123" y2="47" stroke="{accent}" stroke-width="1.5"/>
        </g>
        """
        res["head"] = glasses_svg
    elif p in ("hat", "chapo", "chapeau", "fedora"):
        # Chapo stil fedora / dev sou tèt la
        hat_svg = f"""
        <g class="prop prop-hat" transform="translate(100, 22)">
          <path d="M -30,0 C -15,-3 15,-3 30,0 C 15,2 -15,2 -30,0 Z" fill="{accent}" stroke="{primary}" stroke-width="1.5"/>
          <path d="M -18,-1 C -18,-18 18,-18 18,-1 Z" fill="#1E293B" stroke="{primary}" stroke-width="2"/>
          <rect x="-18" y="-4" width="36" height="3" fill="{primary}"/>
        </g>
        """
        res["head"] = hat_svg
    elif p in ("tie", "krawat", "cravate"):
        # Krawat biznis anba kou a sou tòs la
        tie_svg = f"""
        <g class="prop prop-tie" transform="translate(100, 100)">
          <polygon points="0,0 -4,6 4,6" fill="{accent}"/>
          <polygon points="-4,6 4,6 5,42 0,52 -5,42" fill="{accent}" stroke="{primary}" stroke-width="1"/>
        </g>
        """
        res["torso"] = tie_svg
    elif p in ("microphone", "mikwo", "mic"):
        # Mikwofòn nan men dwat
        mic_svg = f"""
        <g class="prop prop-mic" transform="translate(115, 195)">
          <rect x="-4" y="-22" width="8" height="15" rx="4" fill="{accent}" stroke="{primary}" stroke-width="1.5"/>
          <line x1="0" y1="-7" x2="0" y2="12" stroke="#475569" stroke-width="3"/>
          <line x1="-3" y1="-12" x2="3" y2="-12" stroke="#FFF" stroke-width="1" opacity="0.6"/>
          <circle cx="0" cy="12" r="2.5" fill="{primary}"/>
        </g>
        """
        res["hand_r"] = mic_svg
    elif p in ("coffee", "kafe", "tasse"):
        # Tas kafe nan men gòch
        coffee_svg = f"""
        <g class="prop prop-coffee" transform="translate(85, 195)">
          <rect x="-8" y="-12" width="16" height="18" rx="2" fill="#F8FAFC" stroke="{primary}" stroke-width="1.5"/>
          <path d="M 8,-8 C 13,-8 13,-2 8,-2" fill="none" stroke="{primary}" stroke-width="1.5"/>
          <path d="M -4,-15 Q -2,-18 -4,-21 M 0,-15 Q 2,-18 0,-21 M 4,-15 Q 6,-18 4,-21" fill="none" stroke="#CBD5E1" stroke-width="1" opacity="0.7"/>
        </g>
        """
        res["hand_l"] = coffee_svg
    elif p in ("phone", "telefòn", "smartphone"):
        # Telefòn entèlijan nan men dwat
        phone_svg = f"""
        <g class="prop prop-phone" transform="translate(115, 195)">
          <rect x="-6" y="-18" width="12" height="22" rx="2" fill="#0F172A" stroke="{primary}" stroke-width="1.5"/>
          <rect x="-4" y="-15" width="8" height="15" rx="1" fill="{accent}" opacity="0.85"/>
          <circle cx="0" cy="1" r="1" fill="#FFF"/>
        </g>
        """
        res["hand_r"] = phone_svg
    return res


def generate_stickman_rig_svg(
    name: str = "Stickman",
    color: str | None = None,
    palette: str = "cyan",
    head_fill: str | None = None,
    stroke_width: float = 5.0,
    accessory: str | list[str] | None = None,
    x: float = 0.0,
    y: float = 0.0,
    scale: float = 1.0,
    drawn: str = "right",
    glow: bool = True,
    width: float = 200.0,
    height: float = 360.0,
) -> str:
    """Jenere balizaj SVG Stickman konplè ak data-rigdef, data-bone, lipsync, ak ekspresyon."""
    pal = STICKMAN_PALETTES.get(palette, STICKMAN_PALETTES["cyan"])
    primary = color or pal["primary"]
    accent = pal.get("accent", "#A855F7")
    fill = head_fill or pal["fill"]
    glow_col = pal["glow"] if glow else "none"
    sw = float(stroke_width)
    uid = re.sub(r"\W", "_", name.lower())

    # Kolekte akseswa yo
    props_map = {}
    if accessory:
        props_list = [accessory] if isinstance(accessory, str) else list(accessory)
        for item in props_list:
            if item:
                props_map.update(_render_prop(str(item), primary, accent, sw))

    # Bati JSON data-rigdef konfòm ak Kadans
    rigdef = {
        "name": name,
        "k": round(scale, 6),
        "ground": [round(100.0 * scale, 2), round(350.0 * scale, 2)],
        "h": round(350.0 * scale, 2),
        "box": [round(width, 2), round(height, 2), 0.0, 1, 1],
        "drawn": drawn,
        "bones": STICKMAN_BONES,
    }
    esc_rigdef = html.escape(json.dumps(rigdef, ensure_ascii=False), quote=True)
    pt_attr = _pt_attr(width, height)

    filter_def = ""
    if glow:
        filter_def = f"""
        <defs>
          <filter id="glow_{uid}" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="3.5" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        """

    # Balizaj chak zo
    head_prop = props_map.get("head", "")
    torso_prop = props_map.get("torso", "")
    hand_r_prop = props_map.get("hand_r", "")
    forearm_r_prop = props_map.get("forearm_r", "")
    hand_l_prop = props_map.get("hand_l", "")

    markup = f"""
    <div class="stickman-rig-container" data-rig="{html.escape(name, quote=True)}" data-rigdef="{esc_rigdef}"
         style="position:absolute;left:{x:.1f}px;top:{y:.1f}px;width:{width:.1f}px;height:{height:.1f}px;pointer-events:none;transform-origin:0 0;">
      <svg class="stickman-svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="overflow:visible;">
        {filter_def}
        <!-- 1. Hips (Bassin) -->
        <g data-bone="hips" data-pt="{pt_attr}">
          <circle cx="100" cy="190" r="{sw * 0.9:.1f}" fill="{primary}"/>
        </g>

        <!-- 2. Torso (Torse) -->
        <g data-bone="torso" data-pt="{pt_attr}">
          <line x1="100" y1="190" x2="100" y2="100" stroke="{primary}" stroke-width="{sw * 1.15:.1f}" stroke-linecap="round"/>
          {torso_prop}
        </g>

        <!-- 3. Neck (Cou) -->
        <g data-bone="neck" data-pt="{pt_attr}">
          <line x1="100" y1="100" x2="100" y2="85" stroke="{primary}" stroke-width="{sw:.1f}" stroke-linecap="round"/>
        </g>

        <!-- 4. Head (Tête) ak Figi, Lip-Sync, Je, Sousi -->
        <g data-bone="head" data-pt="{pt_attr}">
          <!-- Sèk tèt la -->
          <circle cx="100" cy="50" r="32" stroke="{primary}" stroke-width="{sw:.1f}" fill="{fill}" {'filter="url(#glow_' + uid + ')"' if glow else ''}/>

          <!-- Sousi (data-brows) pou ekspresyon: neutral, happy, sad, surprised, angry -->
          <g data-brows="{html.escape(name, quote=True)}">
            <g data-expr="neutral">
              <path d="M 85 39 Q 92 37 97 39 M 103 39 Q 108 37 115 39" stroke="{primary}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            </g>
            <g data-expr="happy" style="display:none;">
              <path d="M 85 37 Q 92 32 97 37 M 103 37 Q 108 32 115 37" stroke="{primary}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
            </g>
            <g data-expr="sad" style="display:none;">
              <path d="M 85 35 Q 92 40 97 37 M 103 37 Q 108 40 115 35" stroke="{primary}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
            </g>
            <g data-expr="surprised" style="display:none;">
              <path d="M 84 33 Q 92 28 98 33 M 102 33 Q 108 28 116 33" stroke="{primary}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
            </g>
            <g data-expr="angry" style="display:none;">
              <path d="M 85 35 L 98 42 M 102 42 L 115 35" stroke="{primary}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
            </g>
          </g>

          <!-- Je (data-eyes): open, blink -->
          <g data-eyes="{html.escape(name, quote=True)}">
            <g data-eye="open">
              <ellipse cx="91" cy="48" rx="4.5" ry="5.5" fill="{primary}"/>
              <ellipse cx="109" cy="48" rx="4.5" ry="5.5" fill="{primary}"/>
              <circle cx="92.5" cy="46" r="1.6" fill="#FFF"/>
              <circle cx="110.5" cy="46" r="1.6" fill="#FFF"/>
            </g>
            <g data-eye="blink" style="display:none;">
              <path d="M 86 50 Q 91 53 96 50 M 104 50 Q 109 53 114 50" stroke="{primary}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            </g>
          </g>

          <!-- Bouch Lip-Sync (data-mouth): Rhubarb phonemes A, B, C, D, E, F, X -->
          <g data-mouth="{html.escape(name, quote=True)}">
            <!-- A: Fèmen / Repoze (P, B, M) -->
            <g data-shape="A">
              <line x1="91" y1="65" x2="109" y2="65" stroke="{primary}" stroke-width="2.8" stroke-linecap="round"/>
            </g>
            <!-- B: Ti kras ouvè / Souri (Konsòn) -->
            <g data-shape="B" style="display:none;">
              <path d="M 90 64 Q 100 69 110 64" stroke="{primary}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
            </g>
            <!-- C: Ouvè mwayen (E, I) -->
            <g data-shape="C" style="display:none;">
              <ellipse cx="100" cy="65" rx="7.5" ry="4.5" stroke="{primary}" stroke-width="2.5" fill="{fill}"/>
            </g>
            <!-- D: Gwo ouvè (A) -->
            <g data-shape="D" style="display:none;">
              <path d="M 90 63 Q 100 75 110 63 Z" stroke="{primary}" stroke-width="2.5" fill="{primary}" fill-opacity="0.35"/>
            </g>
            <!-- E: Wonn (O, U) -->
            <g data-shape="E" style="display:none;">
              <circle cx="100" cy="65" r="5.5" stroke="{primary}" stroke-width="2.5" fill="{fill}"/>
            </g>
            <!-- F: Dan parèt / Gwo souri -->
            <g data-shape="F" style="display:none;">
              <path d="M 89 63 Q 100 71 111 63 Z" stroke="{primary}" stroke-width="2.5" fill="#FFF" fill-opacity="0.95"/>
            </g>
            <!-- X: Repoze nòmal -->
            <g data-shape="X" style="display:none;">
              <line x1="92" y1="65" x2="108" y2="65" stroke="{primary}" stroke-width="2.5" stroke-linecap="round"/>
            </g>
          </g>

          {head_prop}
        </g>

        <!-- 5. Bras Gòch (arm_l, forearm_l, hand_l) -->
        <g data-bone="arm_l" data-pt="{pt_attr}">
          <line x1="98" y1="105" x2="90" y2="150" stroke="{primary}" stroke-width="{sw:.1f}" stroke-linecap="round"/>
        </g>
        <g data-bone="forearm_l" data-pt="{pt_attr}">
          <line x1="90" y1="150" x2="85" y2="195" stroke="{primary}" stroke-width="{sw * 0.95:.1f}" stroke-linecap="round"/>
        </g>
        <g data-bone="hand_l" data-pt="{pt_attr}">
          <circle cx="85" cy="195" r="{sw * 1.15:.1f}" fill="{primary}"/>
          {hand_l_prop}
        </g>

        <!-- 6. Bras Dwat (arm_r, forearm_r, hand_r) -->
        <g data-bone="arm_r" data-pt="{pt_attr}">
          <line x1="102" y1="105" x2="110" y2="150" stroke="{primary}" stroke-width="{sw:.1f}" stroke-linecap="round"/>
        </g>
        <g data-bone="forearm_r" data-pt="{pt_attr}">
          <line x1="110" y1="150" x2="115" y2="195" stroke="{primary}" stroke-width="{sw * 0.95:.1f}" stroke-linecap="round"/>
          {forearm_r_prop}
        </g>
        <g data-bone="hand_r" data-pt="{pt_attr}">
          <circle cx="115" cy="195" r="{sw * 1.15:.1f}" fill="{primary}"/>
          {hand_r_prop}
        </g>

        <!-- 7. Janm Gòch (thigh_l, shin_l, foot_l) -->
        <g data-bone="thigh_l" data-pt="{pt_attr}">
          <line x1="100" y1="190" x2="95" y2="260" stroke="{primary}" stroke-width="{sw * 1.1:.1f}" stroke-linecap="round"/>
        </g>
        <g data-bone="shin_l" data-pt="{pt_attr}">
          <line x1="95" y1="260" x2="95" y2="335" stroke="{primary}" stroke-width="{sw:.1f}" stroke-linecap="round"/>
        </g>
        <g data-bone="foot_l" data-pt="{pt_attr}">
          <path d="M 95 335 L 82 349 L 100 349 Z" fill="{primary}"/>
        </g>

        <!-- 8. Janm Dwat (thigh_r, shin_r, foot_r) -->
        <g data-bone="thigh_r" data-pt="{pt_attr}">
          <line x1="100" y1="190" x2="105" y2="260" stroke="{primary}" stroke-width="{sw * 1.1:.1f}" stroke-linecap="round"/>
        </g>
        <g data-bone="shin_r" data-pt="{pt_attr}">
          <line x1="105" y1="260" x2="105" y2="335" stroke="{primary}" stroke-width="{sw:.1f}" stroke-linecap="round"/>
        </g>
        <g data-bone="foot_r" data-pt="{pt_attr}">
          <path d="M 105 335 L 98 349 L 118 349 Z" fill="{primary}"/>
        </g>
      </svg>
    </div>
    """
    return markup


def build_stickman_scene_body(sc: dict, spec: dict, D: dict, mark_fn) -> str:
    """Jenere kontni HTML sèn Kadans lan lè tip sèn nan se 'stickman'."""
    W = int(spec.get("w", 1920))
    H = int(spec.get("h", 1080))
    is_vertical = H > W

    # Pwopriyete Stickman
    name = sc.get("name") or sc.get("speaker") or "Stickman"
    palette = sc.get("palette") or "cyan"
    color = sc.get("color")
    prop = sc.get("accessory") or sc.get("prop")
    scale = float(sc.get("scale") or (1.4 if is_vertical else 1.25))

    # Kalkile pozisyon stickman
    stick_w = 200.0 * scale
    stick_h = 360.0 * scale
    pos_x = float(sc.get("x") or (W / 2 - stick_w / 2 if is_vertical else W * 0.28 - stick_w / 2))
    pos_y = float(sc.get("y") or (H * 0.42 if is_vertical else H * 0.48))

    stick_svg = generate_stickman_rig_svg(
        name=name,
        color=color,
        palette=palette,
        accessory=prop,
        scale=scale,
        x=pos_x,
        y=pos_y,
        glow=True,
    )

    out = []
    title = sc.get("title")
    subtitle = sc.get("subtitle")
    speech = sc.get("speech") or sc.get("text") or sc.get("voice")

    # Tit ak soutit
    if title:
        out.append(f'<div class="a up" data-d="0.1"><h2 style="font-size:{52 if is_vertical else 58}px;text-align:center;margin-top:40px;">{mark_fn(title)}</h2></div>')
    if subtitle:
        out.append(f'<div class="a fade" data-d="0.4"><div class="sub" style="text-align:center;">{mark_fn(subtitle)}</div></div>')

    # Bwat dyalòg (Speech Bubble) ki pop ak pèsonaj la
    if speech:
        bubble_x = pos_x + stick_w * 0.8 if not is_vertical else W * 0.1
        bubble_y = pos_y - 80 if not is_vertical else pos_y - 120
        bubble_w = min(W * 0.42, 600) if not is_vertical else W * 0.8
        out.append(f"""
        <div class="a pop speech-bubble" data-d="0.5"
             style="position:absolute;left:{bubble_x:.1f}px;top:{bubble_y:.1f}px;width:{bubble_w:.1f}px;
                    background:rgba(18, 13, 31, 0.85);backdrop-filter:blur(16px);border:1.5px solid {STICKMAN_PALETTES.get(palette, {}).get('primary', '#00E5FF')};
                    border-radius:24px;padding:24px 32px;box-shadow:0 12px 40px rgba(0,0,0,0.6);z-index:20;">
          <div style="font-size:15px;text-transform:uppercase;letter-spacing:1px;font-weight:700;color:{STICKMAN_PALETTES.get(palette, {}).get('primary', '#00E5FF')};margin-bottom:8px;">
            ✦ {html.escape(name)}
          </div>
          <div style="font-size:{24 if is_vertical else 28}px;line-height:1.4;color:#F3EEFE;font-weight:500;">
            {mark_fn(speech)}
          </div>
        </div>
        """)

    # Mete Stickman Rig SVG a
    out.append(stick_svg)

    return "\n".join(out)
