#!/usr/bin/env python3
"""Jenere asset LIGHTS (glow, reyon, flare, bokeh, etensel) - SVG CC0, Gran Laku Company (Getho Guerrier).
   Pwosediral (seed fiks), pou itilize ak blend 'screen'/'plus-lighter'. Pa telechaje anyen."""
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "assets" / "design" / "LIGHTS"
TINTS = ["#ffffff", "#fff3d6", "#ffe3a8", "#ffd27f", "#dff0ff", "#bfe0ff", "#ffd9f0", "#d9ffe8", "#fff7e8"]
VB = 512


def hdr(extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB} {VB}" '
            f'width="{VB}" height="{VB}">{extra}')


def glow(i, rnd):
    c = rnd.choice(TINTS); r = rnd.randint(170, 250); soft = rnd.uniform(0.0, 0.35)
    gid = f"g{i}"
    return (hdr(f'<defs><radialGradient id="{gid}"><stop offset="0%" stop-color="{c}" stop-opacity="1"/>'
               f'<stop offset="{int(soft*100)}%" stop-color="{c}" stop-opacity="0.9"/>'
               f'<stop offset="100%" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>')
            + f'<circle cx="{VB//2}" cy="{VB//2}" r="{r}" fill="url(#{gid})"/></svg>')


def rays(i, rnd):
    c = rnd.choice(TINTS); n = rnd.choice([8, 12, 16, 24, 32]); cx = cy = VB // 2
    gid = f"r{i}"
    parts = [hdr(f'<defs><radialGradient id="{gid}"><stop offset="0%" stop-color="{c}" stop-opacity="0.9"/>'
                 f'<stop offset="100%" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>'
                 f'<circle cx="{cx}" cy="{cy}" r="60" fill="url(#{gid})"/>')]
    for k in range(n):
        a = (k / n) * 2 * math.pi + rnd.uniform(-0.05, 0.05)
        w = rnd.uniform(2, 7); ln = rnd.uniform(160, 240)
        x1 = cx + math.cos(a) * 20; y1 = cy + math.sin(a) * 20
        x2 = cx + math.cos(a) * ln; y2 = cy + math.sin(a) * ln
        op = rnd.uniform(0.25, 0.75)
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{c}" stroke-width="{w:.1f}" stroke-opacity="{op:.2f}" stroke-linecap="round"/>')
    parts.append("</svg>")
    return "".join(parts)


def flare(i, rnd):
    c = rnd.choice(TINTS); cx = cy = VB // 2; gid = f"f{i}"
    parts = [hdr(f'<defs><radialGradient id="{gid}"><stop offset="0%" stop-color="{c}" stop-opacity="1"/>'
                 f'<stop offset="100%" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>'
                 f'<circle cx="{cx}" cy="{cy}" r="120" fill="url(#{gid})"/>')]
    a = rnd.uniform(0, math.pi)
    for k in range(rnd.randint(4, 8)):
        d = rnd.uniform(-220, 220); rr = rnd.uniform(6, 40)
        x = cx + math.cos(a) * d; y = cy + math.sin(a) * d
        op = rnd.uniform(0.12, 0.4)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{c}" fill-opacity="{op:.2f}"/>')
    parts.append("</svg>")
    return "".join(parts)


def bokeh(i, rnd):
    parts = [hdr()]
    for k in range(rnd.randint(10, 22)):
        c = rnd.choice(TINTS); x = rnd.uniform(40, VB - 40); y = rnd.uniform(40, VB - 40)
        rr = rnd.uniform(14, 70); op = rnd.uniform(0.08, 0.3)
        parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="{c}" fill-opacity="{op:.2f}"/>')
    parts.append("</svg>")
    return "".join(parts)


def sparkle(i, rnd):
    c = rnd.choice(TINTS); cx = cy = VB // 2; gid = f"s{i}"; pts = rnd.choice([4, 4, 6, 8])
    R = 230; r = R * rnd.uniform(0.12, 0.25)
    poly = []
    for k in range(pts * 2):
        ang = (k / (pts * 2)) * 2 * math.pi - math.pi / 2
        rad = R if k % 2 == 0 else r
        poly.append(f"{cx + math.cos(ang)*rad:.1f},{cy + math.sin(ang)*rad:.1f}")
    return (hdr(f'<defs><radialGradient id="{gid}"><stop offset="0%" stop-color="{c}" stop-opacity="0.9"/>'
               f'<stop offset="100%" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>'
               f'<circle cx="{cx}" cy="{cy}" r="90" fill="url(#{gid})"/>')
            + f'<polygon points="{" ".join(poly)}" fill="{c}" fill-opacity="0.85"/></svg>')


CATS = [("01 Glows", glow), ("02 Light rays", rays), ("03 Lens flares", flare),
        ("04 Bokeh", bokeh), ("05 Sparkles", sparkle)]


def main(per=50):
    total = 0
    for name, fn in CATS:
        d = ROOT / name; d.mkdir(parents=True, exist_ok=True)
        for i in range(1, per + 1):
            rnd = random.Random(hash((name, i)) & 0xffffffff)
            svg = fn(i, rnd)
            (d / f"{name.split()[1].lower()}-{i:03d}.svg").write_text(svg, encoding="utf-8")
            total += 1
    print(f"OK {total} LIGHTS SVG nan {ROOT}")


if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 50)
