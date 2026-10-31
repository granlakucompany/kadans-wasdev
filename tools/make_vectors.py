# -*- coding: utf-8 -*-
"""Build the vector library of the Design page: splashes and design shapes, as SVG.

    python tools/make_vectors.py --shapes   # only SHAPES (20 x 250 = 5000) + atlases: WASDEV DESIGN/,
                                            # RADA "VECTOR for DESIGN/"
    python tools/make_vectors.py [folder]   # the whole set (SPLASH + SHAPES) into a folder

Same file in WASDEV and RADA RETOUCH (extended 2026-10-15: 14 new shape categories, 250 shapes in every
category; the first 60 of the six original categories are unchanged).

Every file is generated here from fixed seeds - nothing is downloaded, traced or
adapted from anyone's artwork, so Gran Laku Company owns the set outright. The
same seeds give the same files on every run.

SVG, because a splash drawn at 300 DPI on an A3 poster must stay sharp: the
Design page renders these with QtSvg at whatever size the sheet needs. The
coordinates are whole numbers in a 1000 unit box, which keeps a file to a few
kilobytes.
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "VECTOR for DESIGN")

SPLASH_CATEGORIES = [
    "01 Ink splash", "02 Paint drips", "03 Brush strokes", "04 Watercolour blots", "05 Spray",
    "06 Burst", "07 Liquid blobs", "08 Grunge stains", "09 Halftone splash", "10 Torn paper",
    "11 Smoke and clouds", "12 Comic bursts", "13 Rings and stains", "14 Drops", "15 Swooshes",
    "16 Confetti", "17 Sparkles", "18 Ribbons", "19 Gradient blobs", "20 Scribbles",
]
PER_SPLASH_CATEGORY = 250

SHAPE_CATEGORIES = [
    "01 Separators", "02 Stripes", "03 Broken and torn", "04 Frames", "05 Arrows", "06 Badges",
    "07 Circles and rings", "08 Polygons and stars", "09 Organic blobs", "10 Wave dividers", "11 Dots and halftones",
    "12 Speech bubbles", "13 Ribbons and banners", "14 Corners", "15 Underlines and highlights",
    "16 Geometric patterns", "17 Starbursts", "18 Lines and squiggles", "19 Masks and windows", "20 Hearts and symbols",
]
PER_SHAPE_CATEGORY = 250                  # 20 x 250 = 5000 (WASDEV, 2026-10-15; was 6 x 60)


# ------------------------------------------------------------------ path pieces

def n(v: float) -> str:
    return str(int(round(v)))


def closed_smooth(points, tension: float = 1.0) -> str:
    """A closed Catmull-Rom curve through the points, as cubic Beziers."""
    pts = [(float(x), float(y)) for x, y in points]
    count = len(pts)
    if count < 3:
        return ""
    out = ["M%s %s" % (n(pts[0][0]), n(pts[0][1]))]
    k = tension / 6.0
    for i in range(count):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % count], pts[(i + 2) % count]
        c1 = (p1[0] + (p2[0] - p0[0]) * k, p1[1] + (p2[1] - p0[1]) * k)
        c2 = (p2[0] - (p3[0] - p1[0]) * k, p2[1] - (p3[1] - p1[1]) * k)
        out.append("C%s %s %s %s %s %s" % (n(c1[0]), n(c1[1]), n(c2[0]), n(c2[1]), n(p2[0]), n(p2[1])))
    return "".join(out) + "Z"


def polygon(points) -> str:
    pts = list(points)
    if len(pts) < 3:
        return ""
    return "M" + "L".join("%s %s" % (n(x), n(y)) for x, y in pts) + "Z"


def clip_box(points, w: float = 1000.0, h: float = 1000.0):
    """The polygon cut to the box (Sutherland-Hodgman): QtSvg draws no clip paths."""
    pts = [(float(x), float(y)) for x, y in points]
    edges = ((lambda p: p[0] >= 0, lambda a, b: (0.0, a[1] + (b[1] - a[1]) * (0 - a[0]) / (b[0] - a[0]))),
             (lambda p: p[0] <= w, lambda a, b: (w, a[1] + (b[1] - a[1]) * (w - a[0]) / (b[0] - a[0]))),
             (lambda p: p[1] >= 0, lambda a, b: (a[0] + (b[0] - a[0]) * (0 - a[1]) / (b[1] - a[1]), 0.0)),
             (lambda p: p[1] <= h, lambda a, b: (a[0] + (b[0] - a[0]) * (h - a[1]) / (b[1] - a[1]), h)))
    for inside, cross in edges:
        out = []
        for i, cur in enumerate(pts):
            prev = pts[i - 1]
            if inside(cur):
                if not inside(prev):
                    out.append(cross(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cross(prev, cur))
        pts = out
        if not pts:
            break
    return pts


def circle(cx, cy, r) -> str:
    r = max(1.0, r)
    return "M%s %sa%s %s 0 1 0 %s 0a%s %s 0 1 0 %s 0" % (
        n(cx - r), n(cy), n(r), n(r), n(2 * r), n(r), n(r), n(-2 * r))


def rounded_rect(x, y, w, h, r) -> str:
    r = max(0.0, min(r, w / 2, h / 2))
    return ("M%s %sH%sA%s %s 0 0 1 %s %sV%sA%s %s 0 0 1 %s %sH%sA%s %s 0 0 1 %s %sV%sA%s %s 0 0 1 %s %sZ"
            % (n(x + r), n(y), n(x + w - r), n(r), n(r), n(x + w), n(y + r), n(y + h - r), n(r), n(r),
               n(x + w - r), n(y + h), n(x + r), n(r), n(r), n(x), n(y + h - r), n(y + r), n(r), n(r),
               n(x + r), n(y)))


def ellipse(cx, cy, rx, ry, angle, steps=10) -> str:
    a = math.radians(angle)
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return closed_smooth(pts)


def harmonics(rng, count: int, lo: int, hi: int, amp: float):
    ks = rng.integers(lo, hi + 1, size=count)
    amps = rng.uniform(0.2, 1.0, size=count) * amp / np.maximum(1, ks) ** 0.35
    phases = rng.uniform(0, 2 * math.pi, size=count)
    return ks, amps, phases


def polar(rng, cx, cy, radius, steps, wobble, lo=2, hi=7, terms=5, squash=1.0, turn=0.0):
    ks, amps, phases = harmonics(rng, terms, lo, hi, wobble)
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        r = radius * (1.0 + float(np.sum(amps * np.sin(ks * t + phases))))
        x, y = r * math.cos(t), r * math.sin(t) * squash
        a = math.radians(turn)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return pts


def svg(body: str, box=(1000, 1000)) -> str:
    """The file. Plain path data is split at each M into paths of their own, so
    pieces that overlap add up instead of cutting holes in each other whichever
    way round they were drawn; bodies that are already elements (even-odd holes,
    see-through layers) are kept as they are."""
    if not body.startswith("<"):
        if "<" in body:                              # plain path data mixed with elements: wrap only the data
            import re
            body = "".join(chunk if chunk.startswith("<") else
                           "".join('<path d="M%s"/>' % piece for piece in chunk.split("M") if piece)
                           for chunk in re.split(r"(<[^>]*/>)", body) if chunk)
        else:
            body = "".join('<path d="M%s"/>' % piece for piece in body.split("M") if piece)
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">%s</svg>' % (box[0], box[1], body)


# ------------------------------------------------------------------ splashes

def ink_splash(rng):
    cx, cy = rng.uniform(440, 560), rng.uniform(440, 560)
    arms = int(rng.integers(7, 18))
    core = rng.uniform(150, 230)
    pts, drops = [], []
    steps = arms * 6
    lengths = rng.uniform(1.15, 2.1, size=arms)
    widths = rng.uniform(0.25, 0.55, size=arms)
    offset = rng.uniform(0, 2 * math.pi)
    for i in range(steps):
        t = offset + 2 * math.pi * i / steps
        arm = i // 6
        local = (i % 6) / 6.0
        bump = math.exp(-((local - 0.5) / widths[arm]) ** 2 * 3)
        r = core * (0.85 + 0.12 * math.sin(3 * t) + (lengths[arm] - 0.85) * bump ** 2.2)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    for _ in range(int(rng.integers(6, 26))):
        t = rng.uniform(0, 2 * math.pi)
        dist = core * rng.uniform(1.5, 2.3)
        rr = rng.uniform(6, 30) * (2.3 - dist / core) ** 1.2
        drops.append(circle(cx + dist * math.cos(t), cy + dist * math.sin(t), max(4, rr)))
    return closed_smooth(pts) + "".join(drops)


def paint_drips(rng):
    top = rng.uniform(80, 260)
    cols = int(rng.integers(6, 14))
    xs = np.linspace(0, 1000, cols * 4 + 1)
    edge = []
    lengths = rng.uniform(0.0, 1.0, size=cols) ** 1.7 * rng.uniform(350, 760)
    for j, x in enumerate(xs):
        col = min(cols - 1, j // 4)
        local = (j % 4) / 4.0
        base = top + 25 * math.sin(x / rng.uniform(60, 140))
        if 0.25 <= local <= 0.75 and lengths[col] > 60:
            base += lengths[col] * math.sin((local - 0.25) * 2 * math.pi) ** 0.5
        edge.append((x, base))
    d = ["M0 0L1000 0"]
    d.append("L1000 %s" % n(edge[-1][1]))
    for x, y in reversed(edge):
        d.append("L%s %s" % (n(x), n(y)))
    d.append("Z")
    blobs = []
    for col in range(cols):
        if lengths[col] > 120:
            x = (col + 0.5) * 1000.0 / cols
            y = top + lengths[col]
            blobs.append(circle(x, y, rng.uniform(14, 30)))
    return "".join(d) + "".join(blobs)


def brush_stroke(rng):
    p0 = np.array([rng.uniform(40, 160), rng.uniform(300, 700)])
    p3 = np.array([rng.uniform(840, 960), rng.uniform(300, 700)])
    p1 = np.array([rng.uniform(250, 450), rng.uniform(150, 850)])
    p2 = np.array([rng.uniform(550, 750), rng.uniform(150, 850)])
    width = rng.uniform(60, 170)
    steps = 40
    upper, lower = [], []
    for i in range(steps + 1):
        t = i / steps
        pt = ((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3
        dt = 3 * ((1 - t) ** 2) * (p1 - p0) + 6 * (1 - t) * t * (p2 - p1) + 3 * t * t * (p3 - p2)
        normal = np.array([-dt[1], dt[0]]) / (np.linalg.norm(dt) + 1e-9)
        taper = math.sin(math.pi * min(1.0, max(0.0, t * 1.05))) ** 0.45
        w = width * taper * (1 + rng.uniform(-0.12, 0.12))
        upper.append(pt + normal * w / 2)
        lower.append(pt - normal * w / 2 * (1 + rng.uniform(-0.1, 0.1)))
    outline = polygon([tuple(p) for p in upper + lower[::-1]])
    streaks = []
    for _ in range(int(rng.integers(2, 6))):
        i = int(rng.integers(steps - 8, steps))
        base = upper[i] * rng.uniform(0.3, 0.7) + lower[i] * 0.5
        streaks.append(ellipse(base[0] + rng.uniform(10, 60), base[1], rng.uniform(20, 60), rng.uniform(3, 8), 0, 8))
    return outline + "".join(streaks)


def watercolour(rng):
    layers = []
    for i in range(int(rng.integers(2, 5))):
        pts = polar(rng, rng.uniform(380, 620), rng.uniform(380, 620), rng.uniform(170, 330), 36, 0.28,
                    lo=2, hi=9, terms=6, squash=rng.uniform(0.7, 1.0), turn=rng.uniform(0, 180))
        layers.append('<path d="%s" fill-opacity="%.2f"/>' % (closed_smooth(pts), rng.uniform(0.35, 0.75)))
    return "".join(layers)


def spray(rng):
    # a plume: sprayed from one side, stretched along a direction of its own
    turn = rng.uniform(0, 2 * math.pi)
    stretch = rng.uniform(1.0, 2.4)
    spread = rng.uniform(110, 220)
    shift = rng.uniform(0, 160)
    cx, cy = 500 - shift * math.cos(turn), 500 - shift * math.sin(turn)
    big = rng.uniform(10, 26)
    dots = []
    for _ in range(int(rng.integers(110, 200))):
        u, v = rng.normal(0, spread * stretch), rng.normal(0, spread)
        u += abs(rng.normal(0, spread)) * rng.uniform(0, 1.2)        # leaning one way
        dx = u * math.cos(turn) - v * math.sin(turn)
        dy = u * math.sin(turn) + v * math.cos(turn)
        x, y = cx + dx, cy + dy
        if not (15 < x < 985 and 15 < y < 985):
            continue
        dist = math.hypot(u / stretch, v)
        r = max(2.0, big * math.exp(-dist / (spread * 0.9)) * rng.uniform(0.3, 1.2))
        dots.append(circle(x, y, r))
    core = polar(rng, cx, cy, spread * rng.uniform(0.2, 0.5), 18, 0.25, lo=2, hi=6, terms=4,
                 squash=1.0 / stretch ** 0.5, turn=math.degrees(turn))
    return closed_smooth(core) + "".join(dots)


def burst(rng):
    cx, cy = 500 + rng.uniform(-30, 30), 500 + rng.uniform(-30, 30)
    spikes = int(rng.integers(12, 42))
    outer, inner = rng.uniform(380, 480), rng.uniform(0.45, 0.75)
    pts = []
    offset = rng.uniform(0, 2 * math.pi)
    for i in range(spikes * 2):
        t = offset + math.pi * i / spikes
        r = outer * (rng.uniform(0.75, 1.0) if i % 2 == 0 else inner * rng.uniform(0.85, 1.1))
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return polygon(pts)


def liquid(rng):
    main = polar(rng, rng.uniform(430, 570), rng.uniform(430, 570), rng.uniform(220, 320), 30, 0.22,
                 lo=2, hi=5, terms=4, squash=rng.uniform(0.75, 1.0), turn=rng.uniform(0, 180))
    out = [closed_smooth(main)]
    for _ in range(int(rng.integers(1, 4))):
        t = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(330, 420)
        small = polar(rng, 500 + dist * math.cos(t), 500 + dist * math.sin(t), rng.uniform(25, 70), 14, 0.15,
                      lo=2, hi=4, terms=3)
        out.append(closed_smooth(small))
    return "".join(out)


def grunge(rng):
    main = polar(rng, 500, 500, rng.uniform(260, 360), 90, 0.32, lo=3, hi=34, terms=12,
                 squash=rng.uniform(0.7, 1.0), turn=rng.uniform(0, 180))
    out = [polygon(main)]
    for _ in range(int(rng.integers(3, 9))):
        hole = polar(rng, 500 + rng.uniform(-170, 170), 500 + rng.uniform(-150, 150), rng.uniform(12, 45), 12,
                     0.3, lo=2, hi=6, terms=3)
        out.append(polygon(hole[::-1]))
    for _ in range(int(rng.integers(15, 45))):
        t, dist = rng.uniform(0, 2 * math.pi), rng.uniform(330, 480)
        out.append(circle(500 + dist * math.cos(t), 500 + dist * math.sin(t), rng.uniform(2, 10)))
    return '<path fill-rule="evenodd" d="%s"/>' % "".join(out)


def halftone(rng):
    pts = polar(rng, 500, 500, rng.uniform(260, 380), 24, 0.28, lo=2, hi=7, terms=5)
    cell = int(rng.integers(34, 56))
    angle = math.radians(rng.uniform(0, 45))
    out = []
    xs = np.array([p[0] for p in pts])
    ys = np.array([p[1] for p in pts])
    radius = np.hypot(xs - 500, ys - 500)
    angles = np.arctan2(ys - 500, xs - 500)
    order = np.argsort(angles)
    angles, radius = angles[order], radius[order]
    for gy in range(-12, 13):
        for gx in range(-12, 13):
            x = 500 + (gx * math.cos(angle) - gy * math.sin(angle)) * cell
            y = 500 + (gx * math.sin(angle) + gy * math.cos(angle)) * cell
            if not (0 <= x <= 1000 and 0 <= y <= 1000):
                continue
            a = math.atan2(y - 500, x - 500)
            edge = float(np.interp(a, angles, radius, period=2 * math.pi))
            d = math.hypot(x - 500, y - 500)
            size = (1.0 - d / (edge * 1.35)) * cell * 0.55
            if size > 2.5:
                out.append(circle(x, y, size))
            if len(out) > 240:
                break
    # the dots never touch: one path for all of them keeps the file small
    return '<path d="%s"/>' % "".join(out)


def torn_paper(rng):
    # a scrap of any proportion: a long strip, a square note, a tall label
    width, height = rng.uniform(260, 900), rng.uniform(120, 860)
    cx, cy = 500 + rng.uniform(-1, 1) * (950 - width) / 2, 500 + rng.uniform(-1, 1) * (950 - height) / 2
    left, right = cx - width / 2, cx + width / 2
    top, bottom = cy - height / 2, cy + height / 2

    def ragged(a, b, fixed, horizontal, depth):
        count = int(rng.integers(26, 48))
        pts = []
        for i in range(count + 1):
            t = a + (b - a) * i / count
            jag = fixed + rng.uniform(-depth, depth) + math.sin(i * rng.uniform(0.3, 0.9)) * depth * 0.4
            pts.append((t, jag) if horizontal else (jag, t))
        return pts

    torn = rng.random(4) < np.array([0.8, 0.8, 0.35, 0.35])
    top_edge = ragged(left, right, top, True, 18) if torn[0] else [(left, top), (right, top)]
    right_edge = ragged(top, bottom, right, False, 14) if torn[3] else [(right, top), (right, bottom)]
    bottom_edge = ragged(right, left, bottom, True, 18) if torn[1] else [(right, bottom), (left, bottom)]
    left_edge = ragged(bottom, top, left, False, 14) if torn[2] else [(left, bottom), (left, top)]
    turn = math.radians(rng.uniform(-28, 28))
    pts = []
    for x, y in top_edge + right_edge + bottom_edge + left_edge:
        dx, dy = x - 500, y - 500
        pts.append((500 + dx * math.cos(turn) - dy * math.sin(turn), 500 + dx * math.sin(turn) + dy * math.cos(turn)))
    return polygon(pts)


def smoke(rng):
    out = []
    count = int(rng.integers(7, 16))
    x0, x1 = rng.uniform(120, 260), rng.uniform(740, 880)
    base = rng.uniform(560, 700)
    for i in range(count):
        t = i / max(1, count - 1)
        x = x0 + (x1 - x0) * t
        hump = math.sin(math.pi * t)
        r = rng.uniform(70, 150) * (0.55 + 0.6 * hump)
        y = base - hump * rng.uniform(80, 200) + rng.uniform(-30, 30)
        out.append(circle(x, y, r))
    out.append(polygon([(x0, base), (x1, base), (x1, base + 60), (x0, base + 60)]))
    return "".join(out)


def comic(rng):
    cx, cy = 500, 480
    spikes = int(rng.integers(10, 22))
    pts = []
    for i in range(spikes * 2):
        t = 2 * math.pi * i / (spikes * 2)
        rx, ry = rng.uniform(380, 460), rng.uniform(280, 380)
        k = rng.uniform(0.9, 1.15) if i % 2 == 0 else rng.uniform(0.62, 0.8)
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)))
    out = polygon(pts)
    if rng.random() < 0.6:
        tail = rng.uniform(-math.pi * 0.9, -math.pi * 0.1) + math.pi
        bx, by = cx + 260 * math.cos(tail), cy + 200 * math.sin(tail)
        tip = (cx + 470 * math.cos(tail) + rng.uniform(-60, 60), cy + 470 * math.sin(tail))
        out += polygon([(bx - 40, by), tip, (bx + 40, by)])
    return out


def rings(rng):
    out = []
    for _ in range(int(rng.integers(1, 3))):
        cx, cy, r = rng.uniform(380, 620), rng.uniform(380, 620), rng.uniform(220, 360)
        outer = polar(rng, cx, cy, r, 40, 0.05, lo=2, hi=9, terms=5)
        thick = rng.uniform(12, 40)
        inner = [(cx + (x - cx) * (1 - thick / r), cy + (y - cy) * (1 - thick / r)) for x, y in outer]
        gap = int(rng.integers(0, 12))
        out.append(closed_smooth(outer) + closed_smooth(inner[::-1]))
        if gap:
            pass
    for _ in range(int(rng.integers(2, 10))):
        out.append(circle(rng.uniform(80, 920), rng.uniform(80, 920), rng.uniform(5, 24)))
    return '<path fill-rule="evenodd" d="%s"/>' % "".join(out)


def drops(rng):
    out = []
    for _ in range(int(rng.integers(1, 12))):
        size = rng.uniform(40, 260)
        cx, cy = rng.uniform(size, 1000 - size), rng.uniform(size * 1.4, 1000 - size * 0.6)
        turn = rng.uniform(-35, 35)
        pts = []
        for i in range(24):
            t = 2 * math.pi * i / 24
            x = size * 0.6 * math.sin(t) * (1 - math.cos(t)) ** 0.5 * 0.75
            y = -size * math.cos(t)
            a = math.radians(turn)
            pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
        out.append(closed_smooth(pts))
    return "".join(out)


def swoosh(rng):
    out = []
    for _ in range(int(rng.integers(1, 4))):
        y = rng.uniform(250, 750)
        lift = rng.uniform(-260, 260)
        thick = rng.uniform(40, 150)
        a = (rng.uniform(30, 200), y + rng.uniform(-80, 80))
        b = (rng.uniform(800, 970), y + rng.uniform(-80, 80))
        c = ((a[0] + b[0]) / 2, y + lift)
        top, bottom = [], []
        for i in range(31):
            t = i / 30.0
            x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0]
            yy = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]
            w = thick * math.sin(math.pi * t) ** rng.uniform(0.8, 1.6)
            top.append((x, yy - w / 2))
            bottom.append((x, yy + w / 2))
        out.append(polygon(top + bottom[::-1]))
    return "".join(out)


def confetti(rng):
    """Little pieces thrown in the air: bars, discs and triangles."""
    out = []
    for _ in range(int(rng.integers(26, 70))):
        x, y = rng.uniform(40, 960), rng.uniform(40, 960)
        kind = int(rng.integers(0, 3))
        if kind == 0:
            out.append(circle(x, y, rng.uniform(6, 22)))
        elif kind == 1:
            w, h = rng.uniform(16, 54), rng.uniform(6, 18)
            a = math.radians(rng.uniform(0, 180))
            pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
            out.append(polygon([(x + px * math.cos(a) - py * math.sin(a),
                                 y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]))
        else:
            r = rng.uniform(10, 30)
            a = math.radians(rng.uniform(0, 360))
            out.append(polygon([(x + r * math.cos(a + i * 2.094), y + r * math.sin(a + i * 2.094))
                                for i in range(3)]))
    return "".join(out)


def sparkle(rng):
    """Four-pointed stars and glints, the way a sparkle is drawn."""
    out = []
    for _ in range(int(rng.integers(4, 14))):
        cx, cy = rng.uniform(80, 920), rng.uniform(80, 920)
        r = rng.uniform(40, 230)
        waist = rng.uniform(0.06, 0.22)
        pts = []
        for i in range(8):
            a = math.radians(i * 45 - 90)
            rr = r if i % 2 == 0 else r * waist
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        out.append(closed_smooth(pts, tension=0.35))
    for _ in range(int(rng.integers(0, 14))):
        out.append(circle(rng.uniform(60, 940), rng.uniform(60, 940), rng.uniform(3, 12)))
    return "".join(out)


def ribbon(rng):
    """A band that folds over itself, like a banner or a streamer."""
    out = []
    for _ in range(int(rng.integers(1, 4))):
        y = rng.uniform(260, 740)
        thick = rng.uniform(50, 160)
        waves = rng.uniform(1.0, 2.4)
        lift = rng.uniform(60, 220)
        phase = rng.uniform(0, math.pi)          # ONE phase: a ribbon is smooth, not jagged
        top, bottom = [], []
        for i in range(61):
            t = i / 60.0
            x = 40 + t * 920
            yy = y + math.sin(t * math.pi * waves + phase) * lift
            w = thick * (0.7 + 0.3 * math.sin(t * math.pi))
            top.append((x, yy - w / 2))
            bottom.append((x, yy + w / 2))
        out.append(polygon(top + bottom[::-1]))
        if rng.random() < 0.6:                      # a folded end
            ex = 40 if rng.random() < 0.5 else 960
            out.append(polygon([(ex, y - thick / 2), (ex + (60 if ex < 500 else -60), y),
                                (ex, y + thick / 2)]))
    return "".join(out)


def gradient_blob(rng):
    """A soft heap of round shapes - the backdrop blob of a modern layout."""
    out = []
    # each blob is its own path: piled into one path they cut holes in each other.
    # The shape, the number of lobes and where they sit all move, or 250 of these
    # would be the same soft circle over and over.
    count = int(rng.integers(1, 5))
    spread = rng.uniform(40, 260)
    rough = rng.uniform(0.05, 0.3)
    lobes = int(rng.integers(3, 9))
    stretch = rng.uniform(0.55, 1.8)
    cx, cy = rng.uniform(330, 670), rng.uniform(330, 670)
    for i in range(count):
        r = rng.uniform(170, 430) * (1 - i * rng.uniform(0.05, 0.3))
        pts = polar(rng, cx + rng.uniform(-spread, spread), cy + rng.uniform(-spread, spread),
                    r, 22, rough, lo=2, hi=max(3, lobes), terms=int(rng.integers(2, 5)))
        pts = [(x, cy + (y - cy) * stretch) for x, y in pts]
        turn = math.radians(rng.uniform(0, 360))
        pts = [(cx + (x - cx) * math.cos(turn) - (y - cy) * math.sin(turn),
                cy + (x - cx) * math.sin(turn) + (y - cy) * math.cos(turn)) for x, y in pts]
        out.append('<path d="%s"/>' % closed_smooth(pts, tension=rng.uniform(0.75, 1.15)))
    return "".join(out)


def scribble(rng):
    """Hand-drawn lines: a loop, an underline, a circled word."""
    out = []
    for _ in range(int(rng.integers(2, 5))):
        thick = rng.uniform(18, 46)
        steps = int(rng.integers(30, 60))
        x, y = rng.uniform(60, 200), rng.uniform(220, 780)
        ang = rng.uniform(-0.3, 0.3)
        wobble = rng.uniform(1.0, 3.0)
        top, bottom = [], []
        for i in range(steps):
            t = i / float(steps - 1)
            ang += rng.uniform(-0.12, 0.12)
            x += math.cos(ang) * (860.0 / steps)
            y += math.sin(ang) * (200.0 / steps) + math.sin(t * math.pi * wobble) * 6
            x, y = min(970, max(30, x)), min(970, max(30, y))
            w = thick * (0.55 + 0.45 * math.sin(t * math.pi))
            top.append((x, y - w / 2))
            bottom.append((x, y + w / 2))
        out.append(closed_smooth(top + bottom[::-1], tension=0.6))
    return "".join(out)


SPLASH_MAKERS = [ink_splash, paint_drips, brush_stroke, watercolour, spray, burst, liquid, grunge, halftone,
                 torn_paper, smoke, comic, rings, drops, swoosh,
                 confetti, sparkle, ribbon, gradient_blob, scribble]


# ------------------------------------------------------------------ design shapes

def separators(rng, i):
    kind = i % 12
    h = 120
    y = 60
    out = []
    t = rng.uniform(4, 14)
    if kind == 0:
        out.append("M0 %sL1000 %sL1000 %sL0 %sZ" % (n(y - t / 2), n(y - t / 2), n(y + t / 2), n(y + t / 2)))
    elif kind == 1:
        gap = rng.uniform(10, 26)
        for yy in (y - gap / 2, y + gap / 2):
            out.append("M0 %sL1000 %sL1000 %sL0 %sZ" % (n(yy - t / 3), n(yy - t / 3), n(yy + t / 3), n(yy + t / 3)))
    elif kind == 2:
        dash, space = rng.uniform(30, 90), rng.uniform(15, 40)
        x = 0.0
        while x < 1000:
            out.append("M%s %sL%s %sL%s %sL%s %sZ" % (n(x), n(y - t / 2), n(min(1000, x + dash)), n(y - t / 2),
                                                     n(min(1000, x + dash)), n(y + t / 2), n(x), n(y + t / 2)))
            x += dash + space
    elif kind == 3:
        r = rng.uniform(5, 14)
        step = r * rng.uniform(2.6, 4.5)
        x = r
        while x < 1000:
            out.append(circle(x, y, r))
            x += step
    elif kind == 4:
        amp, waves = rng.uniform(10, 40), int(rng.integers(4, 16))
        top = [(x, y + amp * math.sin(x / 1000 * waves * 2 * math.pi) - t / 2) for x in np.linspace(0, 1000, 120)]
        bot = [(x, yy + t) for x, yy in top]
        out.append(polygon(top + bot[::-1]))
    elif kind == 5:
        amp, teeth = rng.uniform(12, 40), int(rng.integers(8, 30))
        top = [(1000 * k / teeth, y + (amp if k % 2 else -amp) - t / 2) for k in range(teeth + 1)]
        bot = [(x, yy + t) for x, yy in top]
        out.append(polygon(top + bot[::-1]))
    elif kind == 6:
        size = rng.uniform(18, 36)
        out.append(polygon([(500 - size, y), (500, y - size), (500 + size, y), (500, y + size)]))
        for side in (-1, 1):
            x0 = 500 + side * (size + 20)
            x1 = 500 + side * 480
            out.append(polygon([(x0, y - t / 3), (x1, y - t / 6), (x1, y + t / 6), (x0, y + t / 3)]))
    elif kind == 7:
        out.append(polygon([(0, y), (500, y - t), (1000, y), (500, y + t)]))
    elif kind == 8:
        for side in (-1, 1):
            out.append(polygon([(500 + side * 40, y - t / 2), (500 + side * 490, y - t / 2),
                                (500 + side * 490, y + t / 2), (500 + side * 40, y + t / 2)]))
        out.append(circle(500, y, rng.uniform(10, 22)))
    elif kind == 9:
        dash, dot = rng.uniform(40, 80), rng.uniform(5, 10)
        x = 0.0
        while x < 1000:
            out.append("M%s %sL%s %sL%s %sL%s %sZ" % (n(x), n(y - t / 2), n(min(1000, x + dash)), n(y - t / 2),
                                                     n(min(1000, x + dash)), n(y + t / 2), n(x), n(y + t / 2)))
            out.append(circle(min(995, x + dash + 20), y, dot))
            x += dash + 40
    elif kind == 10:
        leaves = int(rng.integers(3, 7))
        for k in range(leaves):
            x = 500 + (k - (leaves - 1) / 2) * 50
            out.append(ellipse(x, y, 20, 9, 45 if k % 2 else -45, 8))
        for side in (-1, 1):
            out.append(polygon([(500 + side * (leaves * 25 + 20), y - 2), (500 + side * 480, y - 1),
                                (500 + side * 480, y + 1), (500 + side * (leaves * 25 + 20), y + 2)]))
    else:
        for k in range(3):
            w = t * (1.0 - k * 0.3)
            yy = y + (k - 1) * rng.uniform(16, 26)
            span = 500 - k * 120
            out.append(polygon([(500 - span, yy), (500, yy - w), (500 + span, yy), (500, yy + w)]))
    return "".join(out), (1000, h)


def stripes(rng, i):
    kind = i % 10
    out = []
    count = int(rng.integers(5, 22))
    if kind in (0, 1, 2):
        angle = (0, 45, -30)[kind] + rng.uniform(-8, 8)
        a = math.radians(angle)
        w = rng.uniform(0.2, 0.6) * 1400 / count
        for k in range(-count, count * 2):
            off = -700 + k * 1400 / count
            cx, cy = 500 + off * -math.sin(a), 500 + off * math.cos(a)
            dx, dy = 900 * math.cos(a), 900 * math.sin(a)
            nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
            out.append(polygon(clip_box([(cx - dx - nx, cy - dy - ny), (cx + dx - nx, cy + dy - ny),
                                         (cx + dx + nx, cy + dy + ny), (cx - dx + nx, cy - dy + ny)])))
        return "".join(out), (1000, 1000)
    if kind == 3:                                   # speed lines
        for _ in range(count * 2):
            y = rng.uniform(40, 960)
            length = rng.uniform(250, 900)
            x = rng.uniform(0, 1000 - length)
            w = rng.uniform(3, 16)
            out.append(polygon([(x, y), (x + length, y - w / 2), (x + length, y + w / 2)]))
        return "".join(out), (1000, 1000)
    if kind == 4:                                   # chevrons
        depth, w = rng.uniform(60, 200), rng.uniform(20, 60)
        for k in range(count // 2 + 2):
            y = k * 1000.0 / (count // 2 + 1)
            out.append(polygon([(0, y), (500, y + depth), (1000, y), (1000, y + w), (500, y + depth + w), (0, y + w)]))
        return "".join(out), (1000, 1000)
    if kind == 5:                                   # grid
        w = rng.uniform(3, 12)
        for k in range(count + 1):
            p = k * 1000.0 / count
            out.append("M%s 0L%s 0L%s 1000L%s 1000Z" % (n(p - w / 2), n(p + w / 2), n(p + w / 2), n(p - w / 2)))
            out.append("M0 %sL1000 %sL1000 %sL0 %sZ" % (n(p - w / 2), n(p - w / 2), n(p + w / 2), n(p + w / 2)))
        return "".join(out), (1000, 1000)
    if kind == 6:                                   # rays
        rays = count * 2
        for k in range(rays):
            t0 = 2 * math.pi * k / rays
            t1 = t0 + math.pi / rays * rng.uniform(0.4, 0.9)
            out.append(polygon(clip_box([(500, 500), (500 + 900 * math.cos(t0), 500 + 900 * math.sin(t0)),
                                         (500 + 900 * math.cos(t1), 500 + 900 * math.sin(t1))])))
        return "".join(out), (1000, 1000)
    if kind == 7:                                   # hand-drawn hatching
        for k in range(count * 2):
            x = k * 1000.0 / (count * 2) + rng.uniform(-8, 8)
            w = rng.uniform(4, 10)
            out.append(polygon([(x, 0), (x + w, 0), (x + w + 120 + rng.uniform(-30, 30), 1000),
                                (x + 120 + rng.uniform(-30, 30), 1000)]))
        return "".join(out), (1000, 1000)
    if kind == 8:                                   # pinstripes, thin and thick
        x = 0.0
        while x < 1000:
            w = rng.choice([4.0, 4.0, 18.0])
            out.append("M%s 0L%s 0L%s 1000L%s 1000Z" % (n(x), n(x + w), n(x + w), n(x)))
            x += w + rng.uniform(14, 40)
        return "".join(out), (1000, 1000)
    waves = int(rng.integers(4, 12))                # wavy stripes
    for k in range(count // 2 + 2):
        y0 = k * 1000.0 / (count // 2 + 1)
        amp, w = rng.uniform(15, 50), rng.uniform(12, 40)
        top = [(x, y0 + amp * math.sin(x / 1000 * waves * math.pi)) for x in np.linspace(0, 1000, 60)]
        out.append(polygon(top + [(x, y + w) for x, y in top[::-1]]))
    return "".join(out), (1000, 1000)


def broken(rng, i):
    kind = i % 8
    out = []
    if kind == 0:                                   # torn strip
        top = [(x, 60 + rng.uniform(-22, 22)) for x in np.linspace(0, 1000, 50)]
        bottom = [(x, 240 + rng.uniform(-22, 22)) for x in np.linspace(1000, 0, 50)]
        return polygon(top + bottom), (1000, 300)
    if kind == 1:                                   # cracked line
        x, pieces = 0.0, []
        while x < 1000:
            length = rng.uniform(60, 180)
            y0, y1 = 50 + rng.uniform(-18, 18), 50 + rng.uniform(-18, 18)
            w = rng.uniform(6, 14)
            pieces.append(polygon([(x, y0 - w / 2), (min(1000, x + length), y1 - w / 3),
                                   (min(1000, x + length), y1 + w / 3), (x, y0 + w / 2)]))
            x += length + rng.uniform(8, 30)
        return "".join(pieces), (1000, 100)
    if kind == 2:                                   # shattered pieces
        for _ in range(int(rng.integers(8, 20))):
            cx, cy, r = rng.uniform(80, 920), rng.uniform(80, 920), rng.uniform(30, 120)
            sides = int(rng.integers(3, 6))
            pts = [(cx + r * rng.uniform(0.5, 1) * math.cos(2 * math.pi * k / sides + rng.uniform(0, 0.8)),
                    cy + r * rng.uniform(0.5, 1) * math.sin(2 * math.pi * k / sides + rng.uniform(0, 0.8)))
                   for k in range(sides)]
            out.append(polygon(pts))
        return "".join(out), (1000, 1000)
    if kind == 3:                                   # broken circle
        r0, r1 = rng.uniform(330, 420), rng.uniform(20, 60)
        a = rng.uniform(0, 2 * math.pi)
        while a < rng.uniform(0, 2 * math.pi) + 2 * math.pi:
            span = rng.uniform(0.3, 1.1)
            pts_o = [(500 + (r0 + r1 / 2) * math.cos(t), 500 + (r0 + r1 / 2) * math.sin(t))
                     for t in np.linspace(a, a + span, 12)]
            pts_i = [(500 + (r0 - r1 / 2) * math.cos(t), 500 + (r0 - r1 / 2) * math.sin(t))
                     for t in np.linspace(a + span, a, 12)]
            out.append(polygon(pts_o + pts_i))
            a += span + rng.uniform(0.08, 0.3)
        return "".join(out), (1000, 1000)
    if kind == 4:                                   # torn edge band (top of a page)
        edge = [(x, 700 + rng.uniform(-40, 40) + 30 * math.sin(x / 70)) for x in np.linspace(1000, 0, 70)]
        return polygon([(0, 0), (1000, 0)] + edge), (1000, 800)
    if kind == 5:                                   # torn corner
        pts = [(0, 0), (1000, 0)]
        for k in range(1, 30):
            t = k / 30.0
            pts.append((1000 * (1 - t) + rng.uniform(-25, 25), 1000 * t + rng.uniform(-25, 25)))
        pts.append((0, 1000))
        return polygon(pts), (1000, 1000)
    if kind == 6:                                   # lightning crack
        pts, x, y = [], 500.0, 0.0
        while y < 1000:
            pts.append((x, y))
            x = min(950, max(50, x + rng.uniform(-120, 120)))
            y += rng.uniform(50, 140)
        pts.append((x, 1000))
        w = rng.uniform(10, 30)
        left = [(px - w * (1 - py / 1100), py) for px, py in pts]
        right = [(px + w * (1 - py / 1100), py) for px, py in pts[::-1]]
        return polygon(left + right), (1000, 1000)
    # broken dashed frame
    for side in range(4):
        pos = 0.0
        while pos < 900:
            length = rng.uniform(80, 240)
            end = min(900, pos + length)
            w = 16
            if side == 0:
                out.append(polygon([(50 + pos, 50), (50 + end, 50), (50 + end, 50 + w), (50 + pos, 50 + w)]))
            elif side == 1:
                out.append(polygon([(950 - w, 50 + pos), (950, 50 + pos), (950, 50 + end), (950 - w, 50 + end)]))
            elif side == 2:
                out.append(polygon([(50 + pos, 950 - w), (50 + end, 950 - w), (50 + end, 950), (50 + pos, 950)]))
            else:
                out.append(polygon([(50, 50 + pos), (50 + w, 50 + pos), (50 + w, 50 + end), (50, 50 + end)]))
            pos = end + rng.uniform(20, 70)
    return "".join(out), (1000, 1000)


def frames(rng, i):
    kind = i % 6
    t = rng.uniform(14, 60)
    if kind == 0:
        return '<path fill-rule="evenodd" d="%s%s"/>' % (
            polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)]),
            polygon([(t, t), (t, 1000 - t), (1000 - t, 1000 - t), (1000 - t, t)])), (1000, 1000)
    if kind == 1:
        g = t * 1.8
        return ('<path fill-rule="evenodd" d="%s%s%s%s"/>'
                % (polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)]),
                   polygon([(t / 2, t / 2), (1000 - t / 2, t / 2), (1000 - t / 2, 1000 - t / 2), (t / 2, 1000 - t / 2)]),
                   polygon([(g, g), (1000 - g, g), (1000 - g, 1000 - g), (g, 1000 - g)]),
                   polygon([(g + t / 2, g + t / 2), (1000 - g - t / 2, g + t / 2), (1000 - g - t / 2, 1000 - g - t / 2),
                            (g + t / 2, 1000 - g - t / 2)]))), (1000, 1000)
    if kind == 2:
        arm = rng.uniform(120, 300)
        out = []
        for sx, sy in ((0, 0), (1, 0), (1, 1), (0, 1)):
            x0, y0 = sx * 1000, sy * 1000
            dx, dy = (1 if sx == 0 else -1), (1 if sy == 0 else -1)
            out.append(polygon([(x0, y0), (x0 + dx * arm, y0), (x0 + dx * arm, y0 + dy * t), (x0 + dx * t, y0 + dy * t),
                                (x0 + dx * t, y0 + dy * arm), (x0, y0 + dy * arm)]))
        return "".join(out), (1000, 1000)
    if kind == 3:
        r = rng.uniform(40, 200)
        return '<path fill-rule="evenodd" d="%s%s"/>' % (
            rounded_rect(0, 0, 1000, 1000, r), rounded_rect(t, t, 1000 - 2 * t, 1000 - 2 * t, max(0.0, r - t))), \
            (1000, 1000)
    if kind == 4:
        return '<path fill-rule="evenodd" d="%s%s"/>' % (circle(500, 500, 500), circle(500, 500, 500 - t)), (1000, 1000)
    dots = []
    r = t / 2.5
    step = r * 3
    for side in range(4):
        pos = r
        while pos < 1000 - r:
            x, y = [(pos, r), (1000 - r, pos), (1000 - pos, 1000 - r), (r, 1000 - pos)][side]
            dots.append(circle(x, y, r))
            pos += step
    return "".join(dots), (1000, 1000)


def arrows(rng, i):
    kind = i % 5
    t = rng.uniform(40, 110)
    head = rng.uniform(1.8, 3.2) * t
    if kind == 0:
        return polygon([(0, 200 - t / 2), (1000 - head, 200 - t / 2), (1000 - head, 200 - head / 1.3), (1000, 200),
                        (1000 - head, 200 + head / 1.3), (1000 - head, 200 + t / 2), (0, 200 + t / 2)]), (1000, 400)
    if kind == 1:
        return polygon([(head, 200 - t / 2), (1000 - head, 200 - t / 2), (1000 - head, 200 - head / 1.3), (1000, 200),
                        (1000 - head, 200 + head / 1.3), (1000 - head, 200 + t / 2), (head, 200 + t / 2),
                        (head, 200 + head / 1.3), (0, 200), (head, 200 - head / 1.3)]), (1000, 400)
    if kind == 2:
        out = []
        count = int(rng.integers(1, 4))
        for k in range(count):
            x = 150 + k * 250
            out.append(polygon([(x, 0), (x + 250, 250), (x, 500), (x - 90, 500), (x + 160, 250), (x - 90, 0)]))
        return "".join(out), (1000, 500)
    if kind == 3:
        lift = rng.uniform(150, 400)
        top, bottom = [], []
        for k in range(31):
            s = k / 30.0
            x = 60 + 760 * s
            y = 600 - lift * math.sin(math.pi * s * 0.85)
            top.append((x, y - t / 2))
            bottom.append((x, y + t / 2))
        ex, ey = top[-1][0], (top[-1][1] + bottom[-1][1]) / 2
        return polygon(top + [(ex, ey - head / 1.3), (ex + head, ey + head * 0.3), (ex, ey + head / 1.3)]
                       + bottom[::-1]), (1000, 800)
    pts = []
    for k in range(24):
        s = k / 23.0
        pts.append((80 + 700 * s + rng.uniform(-6, 6), 200 + math.sin(s * 6) * 30 + rng.uniform(-6, 6)))
    upper = [(x, y - t / 4) for x, y in pts]
    lower = [(x, y + t / 4) for x, y in pts[::-1]]
    ex, ey = pts[-1]
    return polygon(upper + [(ex, ey - head / 2), (ex + head, ey), (ex, ey + head / 2)] + lower), (1000, 400)


def badges(rng, i):
    kind = i % 5
    if kind == 0:
        spikes = int(rng.integers(16, 40))
        pts = []
        for k in range(spikes * 2):
            a = math.pi * k / spikes
            r = 500 if k % 2 == 0 else 500 * rng.uniform(0.84, 0.93)
            pts.append((500 + r * math.cos(a), 500 + r * math.sin(a)))
        return polygon(pts), (1000, 1000)
    if kind == 1:
        notch = rng.uniform(60, 160)
        return polygon([(0, 100), (1000, 100), (1000 - notch, 250), (1000, 400), (0, 400), (notch, 250)]), (1000, 500)
    if kind == 2:
        waves = int(rng.integers(10, 26))
        pts = [(500 + (470 + 30 * math.cos(waves * a)) * math.cos(a), 500 + (470 + 30 * math.cos(waves * a)) * math.sin(a))
               for a in np.linspace(0, 2 * math.pi, waves * 6, endpoint=False)]
        return closed_smooth(pts), (1000, 1000)
    if kind == 3:
        r = rng.uniform(40, 160)
        return polygon([(r, 0), (1000 - r, 0), (1000, 250), (1000 - r, 500), (r, 500), (0, 250)]), (1000, 500)
    shield = [(500, 0), (950, 120), (900, 600), (500, 1000), (100, 600), (50, 120)]
    return closed_smooth(shield, tension=rng.uniform(0.3, 0.9)), (1000, 1000)


# ------------------------------------------------------------------ more design shapes (WASDEV, 2026-10-15)
# Same rules as above: whole numbers in the box, fills only (QtSvg draws no clip paths), holes with even-odd.

def arc_points(cx, cy, r, a0, a1, steps=24):
    return [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(a0, a1, steps)]


def arc_band(cx, cy, r_out, r_in, a0, a1, steps=24) -> str:
    return polygon(arc_points(cx, cy, r_out, a0, a1, steps) + arc_points(cx, cy, r_in, a1, a0, steps))


def band(points, width) -> str:
    """A filled band along a centre line; width is a number or a function of the position 0..1."""
    pts = [(float(x), float(y)) for x, y in points]
    left, right = [], []
    for k, (x, y) in enumerate(pts):
        x0, y0 = pts[max(0, k - 1)]
        x1, y1 = pts[min(len(pts) - 1, k + 1)]
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1.0
        w = width(k / max(1, len(pts) - 1)) if callable(width) else width
        nx, ny = -dy / ln * w / 2, dx / ln * w / 2
        left.append((x + nx, y + ny))
        right.append((x - nx, y - ny))
    return polygon(left + right[::-1])


def evenodd(*parts) -> str:
    return '<path fill-rule="evenodd" d="%s"/>' % "".join(parts)


def regular(cx, cy, r, sides, turn=-90.0):
    return [(cx + r * math.cos(math.radians(turn) + 2 * math.pi * k / sides),
             cy + r * math.sin(math.radians(turn) + 2 * math.pi * k / sides)) for k in range(sides)]


def star_points(cx, cy, r_out, r_in, points, turn=-90.0):
    out = []
    for k in range(points * 2):
        r = r_out if k % 2 == 0 else r_in
        a = math.radians(turn) + math.pi * k / points
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def heart_points(cx, cy, s, steps=60):
    pts = []
    for t in np.linspace(0, 2 * math.pi, steps, endpoint=False):
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s / 17, cy + y * s / 17))
    return pts


def circles(rng, i):
    kind = i % 8
    t = rng.uniform(30, 120)
    if kind == 0:
        return evenodd(circle(500, 500, 500), circle(500, 500, 500 - t)), (1000, 1000)
    if kind == 1:
        rings, parts, r = int(rng.integers(3, 8)), [], 500.0
        step = 500.0 / (rings * 2)
        for _ in range(rings * 2):
            parts.append(circle(500, 500, r))
            r -= step * rng.uniform(0.7, 1.3)
            if r < 20:
                break
        return evenodd(*parts), (1000, 1000)
    if kind == 2:
        count, rr = int(rng.integers(12, 48)), rng.uniform(12, 40)
        return "".join(circle(500 + (480 - rr) * math.cos(2 * math.pi * k / count),
                              500 + (480 - rr) * math.sin(2 * math.pi * k / count), rr) for k in range(count)), (1000, 1000)
    if kind == 3:
        count = int(rng.integers(6, 24))
        gap = rng.uniform(0.15, 0.6) * 2 * math.pi / count
        return "".join(arc_band(500, 500, 500, 500 - t, 2 * math.pi * k / count, 2 * math.pi * (k + 1) / count - gap, 12)
                       for k in range(count)), (1000, 1000)
    if kind == 4:
        count = int(rng.integers(3, 9))
        gap = rng.uniform(0.04, 0.2)
        r_in = rng.uniform(150, 380)
        return "".join(arc_band(500, 500, 500, r_in, 2 * math.pi * k / count, 2 * math.pi * (k + 1) / count - gap, 20)
                       for k in range(count)), (1000, 1000)
    if kind == 5:
        return polygon(arc_points(500, 500, 500, math.pi, 2 * math.pi, 40)), (1000, 520)
    if kind == 6:                                   # crescent
        off = rng.uniform(0.25, 0.55)
        outer = arc_points(500, 500, 480, -math.pi / 2, math.pi / 2, 40)
        inner = [(500 + 480 * math.cos(a) * (1 - 2 * off), 500 + 480 * math.sin(a)) for a in np.linspace(math.pi / 2, -math.pi / 2, 40)]
        return polygon(outer + inner), (1000, 1000)
    orbit = 480 - t / 2
    a = rng.uniform(0, 2 * math.pi)
    return (evenodd(circle(500, 500, 480), circle(500, 500, 480 - t / 3))
            + '<path d="%s"/>' % circle(500 + orbit * math.cos(a), 500 + orbit * math.sin(a), t * 0.9)), (1000, 1000)


def polygons(rng, i):
    kind = i % 8
    sides = int(rng.integers(3, 9))
    turn = rng.choice([-90.0, -90.0 + 180.0 / sides, 0.0])
    if kind == 0:
        return polygon(regular(500, 500, 490, sides, turn)), (1000, 1000)
    if kind == 1:
        t = rng.uniform(30, 110)
        return evenodd(polygon(regular(500, 500, 490, sides, turn)), polygon(regular(500, 500, 490 - t, sides, turn))), (1000, 1000)
    if kind == 2:
        return closed_smooth(regular(500, 500, 470, sides, turn), tension=rng.uniform(0.15, 0.45)), (1000, 1000)
    if kind == 3:
        pts = int(rng.integers(4, 10))
        return polygon(star_points(500, 500, 490, 490 * rng.uniform(0.35, 0.6), pts)), (1000, 1000)
    if kind == 4:
        pts = int(rng.integers(5, 9))
        ro, ri = 490, 490 * rng.uniform(0.4, 0.55)
        t = rng.uniform(30, 70)
        return evenodd(polygon(star_points(500, 500, ro, ri, pts)),
                       polygon(star_points(500, 500, ro - t * 2, ri - t, pts))), (1000, 1000)
    if kind == 5:                                   # hexagon cluster
        r = rng.uniform(70, 120)
        out = []
        for q in range(-3, 4):
            for s in range(-3, 4):
                x = 500 + r * 1.75 * (q + s / 2)
                y = 500 + r * 1.52 * s
                if math.hypot(x - 500, y - 500) < 470 - r and rng.random() < 0.8:
                    out.append(polygon(regular(x, y, r * 0.92, 6, 30)))
        return "".join(out) or polygon(regular(500, 500, 300, 6, 30)), (1000, 1000)
    if kind == 6:                                   # nested triangles
        out, r = [], 490.0
        while r > 60:
            out.append(polygon(regular(500, 560, r, 3)))
            r *= rng.uniform(0.55, 0.75)
            out.append(polygon(regular(500, 560, r, 3)))
            r *= rng.uniform(0.6, 0.8)
        return evenodd(*out), (1000, 1000)
    w = rng.uniform(0.35, 0.65)                    # gem: the facet is cut out
    return evenodd(polygon([(500, 980), (20, 360), (200, 60), (800, 60), (980, 360)]),
                   polygon([(500, 900), (500 - 440 * w, 380), (500 + 440 * w, 380)])), (1000, 1000)


def organic(rng, i):
    kind = i % 6
    if kind == 0:
        return closed_smooth(polar(rng, 500, 500, 380, 14, rng.uniform(0.12, 0.3))), (1000, 1000)
    if kind == 1:
        outer = polar(rng, 500, 500, 400, 14, 0.2)
        inner = [(500 + (x - 500) * 0.8, 500 + (y - 500) * 0.8) for x, y in outer]
        return evenodd(closed_smooth(outer), closed_smooth(inner)), (1000, 1000)
    if kind == 2:
        return (closed_smooth(polar(rng, 400, 450, 280, 12, 0.22)) + closed_smooth(polar(rng, 640, 580, 220, 12, 0.25))), (1000, 1000)
    if kind == 3:
        return closed_smooth(polar(rng, 500, 500, 430, 16, 0.18, squash=rng.uniform(0.35, 0.6), turn=rng.uniform(-30, 30))), (1000, 1000)
    if kind == 4:
        out = []
        for _ in range(int(rng.integers(5, 14))):
            out.append(closed_smooth(polar(rng, rng.uniform(150, 850), rng.uniform(150, 850), rng.uniform(40, 130), 10, 0.25)))
        return "".join(out), (1000, 1000)
    return evenodd(closed_smooth(polar(rng, 500, 500, 420, 14, 0.15)),
                   closed_smooth(polar(rng, rng.uniform(420, 580), rng.uniform(420, 580), rng.uniform(90, 200), 10, 0.25))), (1000, 1000)


def waves(rng, i):
    kind = i % 7
    w, h = 1000, 300
    if kind in (0, 1):
        layers = 1 if kind == 0 else int(rng.integers(2, 4))
        out = []
        for k in range(layers):
            amp, nwave, ph = rng.uniform(20, 70), rng.uniform(1, 4), rng.uniform(0, 2 * math.pi)
            base = 120 + k * 50
            top = [(x, base + amp * math.sin(x / w * nwave * 2 * math.pi + ph)) for x in np.linspace(0, w, 80)]
            out.append('<path fill-opacity="%.2f" d="%s"/>' % (1.0 - 0.3 * (layers - 1 - k), polygon(top + [(w, h), (0, h)])))
        return "".join(out), (w, h)
    if kind == 2:                                   # one soft curve
        lift = rng.uniform(60, 220)
        top = [(x, 260 - lift * math.sin(math.pi * x / w)) for x in np.linspace(0, w, 60)]
        return polygon(top + [(w, h), (0, h)]), (w, h)
    if kind == 3:                                   # slanted cut
        a, b = rng.uniform(40, 260), rng.uniform(40, 260)
        return polygon([(0, a), (w, b), (w, h), (0, h)]), (w, h)
    if kind == 4:                                   # mountains
        pts, x = [(0, h)], 0.0
        while x < w:
            pts.append((x, rng.uniform(40, 220)))
            x += rng.uniform(60, 180)
        pts += [(w, rng.uniform(60, 220)), (w, h)]
        return polygon(pts), (w, h)
    if kind == 5:                                   # drips
        pts = [(0, 0), (w, 0)]
        x = w
        while x > 0:
            dw = rng.uniform(40, 120)
            depth = rng.uniform(40, 260)
            pts += [(x, 60), (x - dw * 0.2, 60 + depth * 0.7), (x - dw / 2, 60 + depth), (x - dw * 0.8, 60 + depth * 0.7),
                    (x - dw, 60)]
            x -= dw + rng.uniform(0, 60)
        return closed_smooth(pts, tension=0.6) if rng.random() < 0.5 else polygon(pts), (w, h)
    bumps, pts = int(rng.integers(6, 16)), []        # clouds
    for k in range(bumps):
        x0, x1 = w * k / bumps, w * (k + 1) / bumps
        r = (x1 - x0) / 2 * rng.uniform(1.0, 1.6)
        pts += arc_points((x0 + x1) / 2, 200, r, math.pi, 2 * math.pi, 10)
    return polygon([(0, h)] + pts + [(w, h)]), (w, h)


def dots(rng, i):
    kind = i % 6
    out = []
    if kind == 0:                                   # halftone gradient
        n_ = int(rng.integers(10, 26))
        step = 1000.0 / n_
        for a in range(n_):
            for b in range(n_):
                r = step * 0.48 * (b + 0.5) / n_
                if r > 2:
                    out.append(circle(a * step + step / 2, b * step + step / 2, r))
    elif kind == 1:
        n_ = int(rng.integers(8, 22))
        step, r = 1000.0 / n_, rng.uniform(0.12, 0.38) * 1000.0 / n_
        out = [circle(a * step + step / 2 + (step / 2 if b % 2 else 0) * (rng.random() < 2), b * step + step / 2, r)
               for a in range(n_) for b in range(n_) if a * step + step / 2 + (step / 2 if b % 2 else 0) < 1000 - r]
    elif kind == 2:
        out = [circle(rng.uniform(20, 980), rng.uniform(20, 980), rng.uniform(4, 30)) for _ in range(int(rng.integers(60, 260)))]
    elif kind == 3:                                 # radial halftone
        rings = int(rng.integers(6, 14))
        for k in range(1, rings + 1):
            rad = 480 * k / rings
            count = max(6, int(2 * math.pi * rad / (480 / rings)))
            rr = (480 / rings) * 0.45 * (1 - k / (rings + 1))
            out += [circle(500 + rad * math.cos(2 * math.pi * j / count), 500 + rad * math.sin(2 * math.pi * j / count), rr)
                    for j in range(count)]
        out.append(circle(500, 500, (480 / rings) * 0.5))
    elif kind == 4:                                 # dotted waves
        for row in range(int(rng.integers(4, 10))):
            y0 = 100 + row * 800 / 9
            for x in np.arange(20, 990, rng.uniform(20, 40)):
                out.append(circle(x, y0 + 40 * math.sin(x / 120 + row), rng.uniform(5, 10)))
    else:                                           # triangle of dots
        n_ = int(rng.integers(8, 18))
        for row in range(n_):
            for col in range(row + 1):
                out.append(circle(500 + (col - row / 2) * 900 / n_, 60 + row * 880 / n_, 900 / n_ * 0.32))
    return "".join(out), (1000, 1000)


def bubbles(rng, i):
    kind = i % 6
    side = rng.choice([-1, 1])
    if kind == 0:
        r = rng.uniform(40, 160)
        tail = polygon([(500 + side * 120, 640), (500 + side * 320, 980), (500 + side * 320, 640)])
        return rounded_rect(40, 40, 920, 620, r) + tail, (1000, 1000)
    if kind == 1:
        tail = polygon([(500 + side * 60, 700), (500 + side * 300, 990), (500 + side * 250, 640)])
        return ellipse(500, 400, 460, 320, 0, 16) + tail, (1000, 1000)
    if kind == 2:                                   # thought bubble
        out = [closed_smooth(polar(rng, 500, 380, 340, 22, 0.06, lo=8, hi=12, terms=3, squash=0.75))]
        for k, rr in enumerate((70, 45, 25)):
            out.append(circle(500 + side * (180 + k * 90), 760 + k * 80, rr))
        return "".join(out), (1000, 1000)
    if kind == 3:                                   # shout
        pts = star_points(500, 420, 470, 360, int(rng.integers(12, 22)))
        pts = [(x + rng.uniform(-25, 25), 420 + (y - 420) * 0.75 + rng.uniform(-20, 20)) for x, y in pts]
        return polygon(pts) + polygon([(500 + side * 80, 650), (500 + side * 330, 990), (500 + side * 260, 600)]), (1000, 1000)
    if kind == 4:                                   # outline bubble
        t = rng.uniform(25, 60)
        return evenodd(rounded_rect(40, 40, 920, 620, 120), rounded_rect(40 + t, 40 + t, 920 - 2 * t, 620 - 2 * t, max(0, 120 - t))) + \
            polygon([(500 + side * 120, 640), (500 + side * 300, 960), (500 + side * 300, 640)]), (1000, 1000)
    return rounded_rect(40, 300, 920, 400, 200) + polygon([(40 + 60 if side < 0 else 960 - 60, 620), (0 if side < 0 else 1000, 760),
                                                          (40 + 180 if side < 0 else 960 - 180, 650)]), (1000, 1000)


def banners(rng, i):
    kind = i % 6
    if kind == 0:                                   # banner with folded ends
        h1, fold = rng.uniform(140, 220), rng.uniform(60, 120)
        y0 = 250 - h1 / 2
        out = [polygon([(150, y0), (850, y0), (850, y0 + h1), (150, y0 + h1)])]
        for sx in (-1, 1):
            x0 = 150 if sx < 0 else 850
            out.append('<path fill-opacity="0.7" d="%s"/>' % polygon(
                [(x0, y0 + fold * 0.6), (x0 + sx * 140, y0 + fold * 0.6), (x0 + sx * 100, y0 + fold * 0.6 + h1 / 2),
                 (x0 + sx * 140, y0 + fold * 0.6 + h1), (x0, y0 + fold * 0.6 + h1)]))
        return "".join(out), (1000, 500)
    if kind == 1:                                   # V-cut ribbon
        cut = rng.uniform(40, 120)
        return polygon([(0, 150), (1000, 150), (1000 - cut, 250), (1000, 350), (0, 350), (cut, 250)]), (1000, 500)
    if kind == 2:                                   # curved ribbon
        lift = rng.uniform(80, 220)
        mid = [(x, 330 - lift * math.sin(math.pi * x / 1000)) for x in np.linspace(40, 960, 40)]
        return band(mid, rng.uniform(90, 160)), (1000, 500)
    if kind == 3:                                   # tag with a hole
        pts = [(80, 250), (260, 70), (940, 70), (940, 430), (260, 430)]
        return evenodd(closed_smooth(pts, 0.15) if rng.random() < 0.4 else polygon(pts), circle(250, 250, 40)), (1000, 500)
    if kind == 4:                                   # pill label
        return rounded_rect(40, 150, 920, 200, 100), (1000, 500)
    w = rng.uniform(120, 220)                        # corner ribbon
    return polygon(clip_box([(1000 - 2.2 * w, 0), (1000 - 1.2 * w, 0), (1000, 1.2 * w), (1000, 2.2 * w)])), (1000, 1000)


def corners(rng, i):
    kind = i % 7
    t = rng.uniform(16, 50)
    if kind == 0:                                   # L with a curl
        r = rng.uniform(80, 180)
        return polygon([(0, 0), (900, 0), (900, t), (t, t), (t, 900), (0, 900)]) + \
            evenodd(circle(r + t, r + t, r), circle(r + t, r + t, r - t)), (1000, 1000)
    if kind == 1:
        return polygon([(0, 0), (rng.uniform(300, 700), 0), (0, rng.uniform(300, 700))]), (1000, 1000)
    if kind == 2:                                   # quarter circles
        out, r = [], 950.0
        while r > 80:
            out.append(arc_band(0, 0, r, max(0.0, r - t), 0, math.pi / 2, 24))
            r -= t * rng.uniform(1.8, 3.2)
        return "".join(out), (1000, 1000)
    if kind == 3:                                   # spiral flourish
        pts = [(150 + 600 * math.exp(-0.25 * a) * math.cos(a), 150 + 600 * math.exp(-0.25 * a) * math.sin(a))
               for a in np.linspace(0, 4 * math.pi, 160)]
        return band(pts, lambda p: t * (1.2 - p)), (1000, 1000)
    if kind == 4:                                   # stepped corner
        steps, out = int(rng.integers(3, 7)), []
        for k in range(steps):
            s = 1000 * (k + 1) / steps
            out.append(polygon([(0, 0), (s, 0), (s, 1000 / steps), (0, 1000 / steps)]) if k == 0 else
                       polygon([(0, 1000 * k / steps), (1000 - s + 1000 / steps, 1000 * k / steps),
                                (1000 - s + 1000 / steps, 1000 * (k + 1) / steps), (0, 1000 * (k + 1) / steps)]))
        return "".join(out), (1000, 1000)
    if kind == 5:
        return polygon(arc_points(0, 0, rng.uniform(500, 950), 0, math.pi / 2, 30) + [(0, 0)]), (1000, 1000)
    arm = rng.uniform(250, 600)                      # bracket corner with a dot
    return polygon([(0, 0), (arm, 0), (arm, t), (t, t), (t, arm), (0, arm)]) + circle(arm + t * 2, t / 2, t * 0.8), (1000, 1000)


def underlines(rng, i):
    kind = i % 7
    w, h = 1000, 200
    if kind == 0:                                   # brush underline
        f, amp = rng.uniform(1, 2.5), rng.uniform(10, 30)
        pts = [(x, 110 + amp * math.sin(x / 1000 * math.pi * f)) for x in np.linspace(20, 980, 50)]
        thick = rng.uniform(26, 44)
        return band(pts, lambda p: thick * (0.25 + math.sin(math.pi * p) ** 0.6)), (w, h)
    if kind == 1:
        return band([(x, 80 + 6 * math.sin(x / 90)) for x in np.linspace(20, 980, 40)], 18) + \
            band([(x, 130 + 6 * math.cos(x / 110)) for x in np.linspace(60, 940, 40)], 14), (w, h)
    if kind == 2:                                   # hand-drawn circle around a word
        pts = [(500 + 470 * math.cos(a) * rng.uniform(0.98, 1.02), 100 + 85 * math.sin(a) * rng.uniform(0.95, 1.05))
               for a in np.linspace(-0.3, 2 * math.pi + 0.5, 70)]
        return band(pts, lambda p: 6 + 10 * math.sin(math.pi * p)), (w, h)
    if kind == 3:                                   # marker highlight
        top = [(x, 40 + rng.uniform(-8, 8)) for x in np.linspace(0, w, 30)]
        bot = [(x, 160 + rng.uniform(-8, 8)) for x in np.linspace(w, 0, 30)]
        return '<path fill-opacity="0.55" d="%s"/>' % polygon(top + bot), (w, h)
    if kind == 4:                                   # swoosh
        pts = [(x, 150 - 90 * math.sin(math.pi * (x - 20) / 960) ** 0.8) for x in np.linspace(20, 980, 60)]
        return band(pts, lambda p: 4 + 36 * math.sin(math.pi * p) ** 2), (w, h)
    if kind == 5:                                   # zigzag
        teeth = int(rng.integers(10, 30))
        return band([(20 + 960 * k / teeth, 70 if k % 2 else 130) for k in range(teeth + 1)], rng.uniform(10, 22)), (w, h)
    pts = [(x, 110) for x in np.linspace(20, 880, 30)]  # underline with arrow
    return band(pts, 14) + polygon([(860, 70), (980, 110), (860, 150)]), (w, h)


def patterns(rng, i):
    kind = i % 8
    n_ = int(rng.integers(5, 14))
    s = 1000.0 / n_
    out = []
    if kind == 0:
        out = [polygon([(a * s, b * s), ((a + 1) * s, b * s), ((a + 1) * s, (b + 1) * s), (a * s, (b + 1) * s)])
               for a in range(n_) for b in range(n_) if (a + b) % 2 == 0]
    elif kind == 1:
        out = [polygon([(a * s, (b + 1) * s), ((a + 0.5) * s, b * s), ((a + 1) * s, (b + 1) * s)]) for a in range(n_) for b in range(n_)]
    elif kind == 2:
        r = s / 2
        for b in range(n_ + 2):
            for a in range(n_ + 2):
                x, y = a * r * 1.75 + (r * 0.875 if b % 2 else 0), b * r * 1.52
                pts = [(px, py) for px, py in regular(x, y, r * 0.85, 6, 30)]
                cl = clip_box(pts)
                if len(cl) >= 3:
                    out.append(polygon(cl))
    elif kind == 3:
        out = [polygon([((a + 0.5) * s, b * s), ((a + 1) * s, (b + 0.5) * s), ((a + 0.5) * s, (b + 1) * s), (a * s, (b + 0.5) * s)])
               for a in range(n_) for b in range(n_)]
        return evenodd(polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)]), *out), (1000, 1000)
    elif kind == 4:                                 # scales
        for b in range(n_ + 1):
            for a in range(n_ + 1):
                x = a * s + (s / 2 if b % 2 else 0)
                y = b * s * 0.7
                cl = clip_box(arc_points(x, y, s / 2, 0, math.pi, 12))
                if len(cl) >= 3:
                    out.append(polygon(cl))
    elif kind == 5:                                 # herringbone
        for b in range(n_ * 2):
            for a in range(n_):
                x, y = a * s, b * s / 2
                d = 1 if a % 2 else -1
                cl = clip_box([(x, y), (x + s, y + d * s / 2), (x + s, y + d * s / 2 + s / 5), (x, y + s / 5)])
                if len(cl) >= 3:
                    out.append(polygon(cl))
    elif kind == 6:                                 # crosses
        t = s * rng.uniform(0.12, 0.25)
        for a in range(n_):
            for b in range(n_):
                cx, cy, k = (a + 0.5) * s, (b + 0.5) * s, s * 0.3
                out.append(polygon([(cx - t, cy - k), (cx + t, cy - k), (cx + t, cy - t), (cx + k, cy - t), (cx + k, cy + t),
                                    (cx + t, cy + t), (cx + t, cy + k), (cx - t, cy + k), (cx - t, cy + t), (cx - k, cy + t),
                                    (cx - k, cy - t), (cx - t, cy - t)]))
    else:                                           # wave lines
        for b in range(n_ * 2):
            y0 = b * 1000 / (n_ * 2)
            out.append(band([(x, y0 + s * 0.2 * math.sin(x / s * math.pi)) for x in np.linspace(0, 1000, 60)], s * 0.12))
    return "".join(out), (1000, 1000)


def starbursts(rng, i):
    kind = i % 6
    if kind == 0:
        spikes = int(rng.integers(12, 40))
        return polygon(star_points(500, 500, 490, 490 * rng.uniform(0.7, 0.88), spikes)), (1000, 1000)
    if kind == 1:                                   # rounded seal
        spikes = int(rng.integers(10, 24))
        return closed_smooth(star_points(500, 500, 480, 480 * rng.uniform(0.8, 0.9), spikes), tension=0.8), (1000, 1000)
    if kind == 2:                                   # sunburst
        rays = int(rng.integers(12, 36))
        out = [circle(500, 500, rng.uniform(120, 220))]
        for k in range(rays):
            a = 2 * math.pi * k / rays
            da = math.pi / rays * rng.uniform(0.3, 0.7)
            out.append(polygon([(500 + 250 * math.cos(a - da), 500 + 250 * math.sin(a - da)), (500 + 490 * math.cos(a), 500 + 490 * math.sin(a)),
                                (500 + 250 * math.cos(a + da), 500 + 250 * math.sin(a + da))]))
        return "".join(out), (1000, 1000)
    if kind == 3:                                   # comic explosion
        spikes = int(rng.integers(10, 20))
        pts = []
        for k in range(spikes * 2):
            r = rng.uniform(380, 490) if k % 2 == 0 else rng.uniform(200, 300)
            a = math.pi * k / spikes + rng.uniform(-0.08, 0.08)
            pts.append((500 + r * math.cos(a), 500 + r * math.sin(a)))
        return polygon(pts), (1000, 1000)
    if kind == 4:
        return polygon(star_points(500, 530, 490, 490 * 0.38, 5)), (1000, 1000)
    pts = []                                        # four-point sparkle with curved sides
    for a in np.linspace(0, 2 * math.pi, 120, endpoint=False):
        r = 490 * (abs(math.cos(2 * a)) ** rng.uniform(4, 9)) + 40
        pts.append((500 + r * math.cos(a), 500 + r * math.sin(a)))
    return closed_smooth(pts), (1000, 1000)


def squiggles(rng, i):
    kind = i % 6
    t = rng.uniform(12, 40)
    if kind == 0:
        f, amp = rng.uniform(3, 9), rng.uniform(40, 140)
        return band([(x, 250 + amp * math.sin(x / 1000 * f * 2 * math.pi)) for x in np.linspace(20, 980, 120)],
                    lambda p: t * (0.3 + math.sin(math.pi * p))), (1000, 500)
    if kind == 1:                                   # spiral
        turns = rng.uniform(2.5, 5)
        pts = [(500 + 460 * (a / (turns * 2 * math.pi)) * math.cos(a), 500 + 460 * (a / (turns * 2 * math.pi)) * math.sin(a))
               for a in np.linspace(0.3, turns * 2 * math.pi, 220)]
        return band(pts, t), (1000, 1000)
    if kind == 2:                                   # loops
        loops = int(rng.integers(3, 8))
        pts = [(60 + 880 * s + 60 * math.cos(s * loops * 2 * math.pi), 250 + 90 * math.sin(s * loops * 2 * math.pi))
               for s in np.linspace(0, 1, 200)]
        return band(pts, t * 0.8), (1000, 500)
    if kind == 3:                                   # zigzag band
        teeth = int(rng.integers(5, 16))
        return band([(40 + 920 * k / teeth, 120 if k % 2 else 380) for k in range(teeth + 1)], t), (1000, 500)
    if kind == 4:                                   # scribble
        pts, x, y = [], 100.0, 250.0
        for _ in range(int(rng.integers(30, 60))):
            x = min(940, max(60, x + rng.uniform(-60, 90)))
            y = min(440, max(60, y + rng.uniform(-120, 120)))
            pts.append((x, y))
        return band(pts, t * 0.5), (1000, 500)
    out = []                                        # dashed curve
    pts = [(x, 250 + 120 * math.sin(x / 1000 * math.pi * 2)) for x in np.linspace(20, 980, 200)]
    step = int(rng.integers(8, 16))
    for k in range(0, len(pts) - step, step * 2):
        out.append(band(pts[k:k + step], t * 0.7))
    return "".join(out), (1000, 500)


def masks(rng, i):
    kind = i % 7
    if kind == 0:                                   # arch window
        return polygon([(100, 1000)] + arc_points(500, 400, 400, math.pi, 2 * math.pi, 40) + [(900, 1000)]), (1000, 1000)
    if kind == 1:
        return rounded_rect(250, 0, 500, 1000, 250), (1000, 1000)
    if kind == 2:                                   # ticket
        r = rng.uniform(50, 110)
        pts = [(0, 0), (1000, 0), (1000, 500 - r)] + arc_points(1000, 500, r, -math.pi / 2, -3 * math.pi / 2, 20) + \
              [(1000, 1000), (0, 1000), (0, 500 + r)] + arc_points(0, 500, r, math.pi / 2, -math.pi / 2, 20)
        return polygon([(x, y * 0.6 + 200) for x, y in pts]), (1000, 1000)
    if kind == 3:                                   # square with a round window
        return evenodd(polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)]), circle(500, 500, rng.uniform(260, 430))), (1000, 1000)
    if kind == 4:
        return closed_smooth(polar(rng, 500, 500, 440, 18, 0.1)), (1000, 1000)
    if kind == 5:
        return closed_smooth([(500, 0), (1000, 500), (500, 1000), (0, 500)], tension=rng.uniform(0.3, 0.7)), (1000, 1000)
    r = rng.uniform(60, 200)                         # leaf / petal window
    return polygon(arc_points(1000 - r, 1000 - r, 1000 - 2 * r, math.pi, 1.5 * math.pi, 30)
                   + arc_points(r, r, 1000 - 2 * r, 0, 0.5 * math.pi, 30)), (1000, 1000)


def symbols(rng, i):
    kind = i % 10
    t = rng.uniform(140, 240)
    if kind == 0:
        return polygon(heart_points(500, 520, 470)), (1000, 1000)
    if kind == 1:
        return polygon([(500 - t / 2, 40), (500 + t / 2, 40), (500 + t / 2, 500 - t / 2), (960, 500 - t / 2), (960, 500 + t / 2),
                        (500 + t / 2, 500 + t / 2), (500 + t / 2, 960), (500 - t / 2, 960), (500 - t / 2, 500 + t / 2),
                        (40, 500 + t / 2), (40, 500 - t / 2), (500 - t / 2, 500 - t / 2)]), (1000, 1000)
    if kind == 2:                                   # check mark
        return band([(80, 520), (380, 820), (930, 200)], t * 0.7), (1000, 1000)
    if kind == 3:
        return band([(100, 100), (900, 900)], t * 0.7) + band([(900, 100), (100, 900)], t * 0.7), (1000, 1000)
    if kind == 4:                                   # lightning
        return polygon([(600, 0), (180, 560), (470, 560), (360, 1000), (820, 400), (530, 400)]), (1000, 1000)
    if kind == 5:                                   # location pin
        pts = arc_points(500, 380, 340, math.radians(150), math.radians(390), 40) + [(500, 980)]
        return evenodd(closed_smooth(pts, 0.4), circle(500, 380, 130)), (1000, 1000)
    if kind == 6:                                   # drop
        return closed_smooth(arc_points(500, 620, 340, math.radians(-20), math.radians(200), 30) + [(500, 20)], 0.5), (1000, 1000)
    if kind == 7:                                   # moon
        return polygon(arc_points(500, 500, 460, math.radians(60), math.radians(300), 40)
                       + arc_points(640, 500, 380, math.radians(250), math.radians(110), 40)), (1000, 1000)
    if kind == 8:                                   # play button
        return evenodd(circle(500, 500, 480), polygon([(390, 280), (750, 500), (390, 720)])), (1000, 1000)
    pts = [(500 + 460 * math.cos(a) / (1 + math.sin(a) ** 2), 500 + 460 * math.sin(a) * math.cos(a) / (1 + math.sin(a) ** 2))
           for a in np.linspace(0, 2 * math.pi, 160)]                      # infinity
    return band(pts, t * 0.4), (1000, 1000)


SHAPE_MAKERS = [separators, stripes, broken, frames, arrows, badges, circles, polygons, organic, waves, dots, bubbles,
                banners, corners, underlines, patterns, starbursts, squiggles, masks, symbols]


# ------------------------------------------------------------------ writing

def splash_svg(category_index: int, index: int) -> str:
    rng = np.random.default_rng(1_000_003 * (category_index + 1) + index * 7919)
    body = SPLASH_MAKERS[category_index](rng)
    return svg(body)


def shape_svg(category_index: int, index: int) -> str:
    rng = np.random.default_rng(2_000_029 * (category_index + 1) + index * 104729)
    body, box = SHAPE_MAKERS[category_index](rng, index)
    return svg(body, box)


THUMB_PX = 64
ATLAS_COLUMNS = 16


def write_atlas(out: str, group: str, category: str, names) -> str:
    """Every preview of a category in one small grey PNG (the drawer reads one
    file instead of drawing hundreds of vectors), with the order beside it."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtCore import QRectF, Qt
    from PySide6.QtGui import QGuiApplication, QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer
    if QGuiApplication.instance() is None:
        write_atlas.app = QGuiApplication([])
    rows = (len(names) + ATLAS_COLUMNS - 1) // ATLAS_COLUMNS
    atlas = QImage(ATLAS_COLUMNS * THUMB_PX, max(1, rows) * THUMB_PX, QImage.Format_ARGB32_Premultiplied)
    atlas.fill(Qt.transparent)
    painter = QPainter(atlas)
    painter.setRenderHint(QPainter.Antialiasing)
    for i, name in enumerate(names):
        renderer = QSvgRenderer(os.path.join(out, group, category, name))
        box = renderer.viewBoxF()
        k = (THUMB_PX - 4) / max(box.width(), box.height())
        w, h = box.width() * k, box.height() * k
        x = (i % ATLAS_COLUMNS) * THUMB_PX + (THUMB_PX - w) / 2.0
        y = (i // ATLAS_COLUMNS) * THUMB_PX + (THUMB_PX - h) / 2.0
        renderer.render(painter, QRectF(x, y, w, h))
    painter.end()
    folder = os.path.join(out, "_thumbs", group)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, category + ".png")
    # keep only the coverage, as grey: a quarter of the bytes of RGBA
    from PIL import Image
    ptr = atlas.convertToFormat(QImage.Format_RGBA8888)
    arr = np.frombuffer(ptr.constBits(), np.uint8, count=ptr.sizeInBytes()).reshape(ptr.height(), -1, 4)
    Image.fromarray(arr[:, :ptr.width(), 3].copy(), "L").save(path, optimize=True)
    with open(os.path.join(folder, category + ".json"), "w", encoding="utf-8") as fh:
        json.dump({"px": THUMB_PX, "columns": ATLAS_COLUMNS, "names": list(names)}, fh)
    return path


def build(out: str = OUT, splash_count: int = PER_SPLASH_CATEGORY, shape_count: int = PER_SHAPE_CATEGORY,
          quiet: bool = False) -> dict:
    manifest = {"SPLASH": {}, "SHAPES": {}}
    for group, categories, count, make in (("SPLASH", SPLASH_CATEGORIES, splash_count, splash_svg),
                                           ("SHAPES", SHAPE_CATEGORIES, shape_count, shape_svg)):
        for ci, category in enumerate(categories):
            folder = os.path.join(out, group, category)
            os.makedirs(folder, exist_ok=True)
            slug = category.split(" ", 1)[1].lower().replace(" and ", "-").replace(" ", "-")
            names = []
            for i in range(count):
                name = "%s-%03d.svg" % (slug, i + 1)
                with open(os.path.join(folder, name), "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(make(ci, i))
                names.append(name)
            manifest[group][category] = len(names)
            write_atlas(out, group, category, names)
            if not quiet:
                print("%-8s %-24s %d" % (group, category, len(names)))
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    readme = os.path.join(out, "README.md")
    with open(readme, "w", encoding="utf-8") as fh:
        fh.write("# Vector library for the Design page\n\n"
                 "SVG files for the **Splash** and **Shapes** drawers of RADA's Design page.\n\n"
                 "```\nSPLASH/   %d splashes in %d categories\nSHAPES/   %d design shapes in %d categories\n```\n\n"
                 "Every file was **generated by `tools/make_vectors.py`** in this project from fixed seeds. "
                 "Nothing was downloaded, traced or adapted from anyone else's artwork, so Gran Laku Company "
                 "owns the whole set outright.\n\nYour own `.svg` (or `.png`) files dropped into a category "
                 "folder appear in the drawer too.\n"
                 % (splash_count * len(SPLASH_CATEGORIES), len(SPLASH_CATEGORIES),
                    shape_count * len(SHAPE_CATEGORIES), len(SHAPE_CATEGORIES)))
    return manifest


def build_shapes(out: str, quiet: bool = False) -> dict:
    """WASDEV: (re)write only SHAPES (20 categories x PER_SHAPE_CATEGORY) and their atlases; SPLASH and every other\n    folder are left as they are. The first files of the six original categories come out identical (same seeds)."""
    man_path = os.path.join(out, "manifest.json")
    try:
        with open(man_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, ValueError):
        manifest = {}
    manifest["SHAPES"] = {}
    for ci, category in enumerate(SHAPE_CATEGORIES):
        folder = os.path.join(out, "SHAPES", category)
        os.makedirs(folder, exist_ok=True)
        slug = category.split(" ", 1)[1].lower().replace(" and ", "-").replace(" ", "-")
        names = []
        for i in range(PER_SHAPE_CATEGORY):
            name = "%s-%03d.svg" % (slug, i + 1)
            with open(os.path.join(folder, name), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(shape_svg(ci, i))
            names.append(name)
        manifest["SHAPES"][category] = len(names)
        write_atlas(out, "SHAPES", category, names)
        if not quiet:
            print("SHAPES   %-30s %d" % (category, len(names)))
    with open(man_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    sp_dir = os.path.join(out, "SPLASH")                  # what is really on disk (not what an old manifest says)
    splash = {c: len([f for f in os.listdir(os.path.join(sp_dir, c)) if f.endswith(".svg")])
              for c in sorted(os.listdir(sp_dir)) if os.path.isdir(os.path.join(sp_dir, c))} if os.path.isdir(sp_dir) else {}
    manifest["SPLASH"] = splash
    with open(man_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    with open(os.path.join(out, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# Vector library for the Design page\n\n"
                 "SVG files for the **Splash** and **Shapes** drawers of the Design page.\n\n"
                 "```\nSPLASH/   %d splashes in %d categories\nSHAPES/   %d design shapes in %d categories\n```\n\n"
                 "Every file was **generated by `tools/make_vectors.py`** from fixed seeds. Nothing was downloaded, "
                 "traced or adapted from anyone else's artwork, so Gran Laku Company owns the whole set outright.\n\n"
                 "Your own `.svg` (or `.png`) files dropped into a category folder appear in the drawer too.\n"
                 % (sum(splash.values()), len(splash), PER_SHAPE_CATEGORY * len(SHAPE_CATEGORIES), len(SHAPE_CATEGORIES)))
    return manifest


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--shapes":
        default = os.path.join(ROOT, "DESIGN")              # WASDEV: DESIGN/ · RADA: VECTOR for DESIGN/
        build_shapes(sys.argv[2] if len(sys.argv) > 2 else (default if os.path.isdir(default) else OUT))
    else:
        build(sys.argv[1] if len(sys.argv) > 1 else OUT)
