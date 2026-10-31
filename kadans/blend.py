"""Kadans WASDEV — the 31 layer blend modes of photo editors (27 Photoshop + 4 Paint.NET), pixel by pixel (numpy).

Browsers draw 17 of them natively (CSS mix-blend-mode). The other fourteen — dissolve, linear burn, darker colour,
lighter colour, vivid light, linear light, pin light, hard mix, subtract, divide, reflect, glow, negation, xor —
exist in no browser, so the renderer captures the frame in layers (what is under the layer, the layer alone on
a transparent background, what is above it) and composites them here. Formulas follow the W3C compositing spec
and the ISO 32000-2 standard.
Deterministic dither noise (PhotoCraft 32-bit integer hash) eliminates gradient and video banding.

Optional dependencies: numpy and Pillow (pip install "kadans-wasdev[blend]"). Without them the renderer falls back
to the nearest native mode, like the live preview.
"""
from __future__ import annotations

import io

try:
    import numpy as np
    from PIL import Image, ImageFilter
    AVAILABLE = True
except ImportError:                                          # pragma: no cover - optional
    np = Image = ImageFilter = None
    AVAILABLE = False


def decode(data: bytes, alpha: bool = False):
    """PNG / JPEG bytes -> float32 array (h, w, 3|4) in 0..1."""
    im = Image.open(io.BytesIO(data)).convert("RGBA" if alpha else "RGB")
    return np.asarray(im, dtype=np.float32) / 255.0


def to_bytes(rgb) -> bytes:
    return (np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes()


def _lum(c):
    return c[..., 0:1] * 0.3 + c[..., 1:2] * 0.59 + c[..., 2:3] * 0.11


def _clip_color(c):
    lum = _lum(c)
    n = c.min(axis=-1, keepdims=True)
    x = c.max(axis=-1, keepdims=True)
    c = np.where(n < 0, lum + (c - lum) * lum / np.maximum(lum - n, 1e-6), c)
    return np.where(x > 1, lum + (c - lum) * (1 - lum) / np.maximum(x - lum, 1e-6), c)


def _set_lum(c, lum):
    return _clip_color(c + (lum - _lum(c)))


def _sat(c):
    return c.max(axis=-1, keepdims=True) - c.min(axis=-1, keepdims=True)


def _set_sat(c, s):
    mn, mx = c.min(axis=-1, keepdims=True), c.max(axis=-1, keepdims=True)
    rng = mx - mn
    return np.where(rng > 1e-6, (c - mn) * s / np.maximum(rng, 1e-6), 0.0)


def _soft_light(a, b):
    d = np.where(a <= 0.25, ((16 * a - 12) * a + 4) * a, np.sqrt(a))
    return np.where(b <= 0.5, a - (1 - 2 * b) * a * (1 - a), a + (2 * b - 1) * (d - a))


def _dodge(a, b):
    return np.where(b >= 1, 1.0, np.minimum(1.0, a / np.maximum(1 - b, 1e-6)))


def _burn(a, b):
    return np.where(b <= 0, 0.0, 1 - np.minimum(1.0, (1 - a) / np.maximum(b, 1e-6)))


def _vivid(a, b):
    return np.where(b <= 0.5, _burn(a, 2 * b), _dodge(a, 2 * (b - 0.5)))


def mix(a, b, mode: str):
    """f(backdrop a, layer b) for every mode (RGB 0..1, no alpha)."""
    if mode in ("normal", "dissolve"):
        return b
    if mode == "multiply":
        return a * b
    if mode == "screen":
        return a + b - a * b
    if mode == "darken":
        return np.minimum(a, b)
    if mode == "lighten":
        return np.maximum(a, b)
    if mode == "overlay":
        return np.where(a <= 0.5, 2 * a * b, 1 - 2 * (1 - a) * (1 - b))
    if mode == "hard-light":
        return np.where(b <= 0.5, 2 * a * b, 1 - 2 * (1 - a) * (1 - b))
    if mode == "soft-light":
        return _soft_light(a, b)
    if mode == "color-dodge":
        return np.where(a <= 0, 0.0, _dodge(a, b))
    if mode == "color-burn":
        return np.where(a >= 1, 1.0, _burn(a, b))
    if mode == "linear-dodge":
        return np.minimum(1.0, a + b)
    if mode == "linear-burn":
        return np.maximum(0.0, a + b - 1)
    if mode == "difference":
        return np.abs(a - b)
    if mode == "exclusion":
        return a + b - 2 * a * b
    if mode == "subtract":
        return np.maximum(0.0, a - b)
    if mode == "divide":
        return np.where(b <= 0, 1.0, np.minimum(1.0, a / np.maximum(b, 1e-6)))
    if mode == "vivid-light":
        return _vivid(a, b)
    if mode == "linear-light":
        return np.clip(a + 2 * b - 1, 0, 1)
    if mode == "pin-light":
        return np.where(b <= 0.5, np.minimum(a, 2 * b), np.maximum(a, 2 * b - 1))
    if mode == "hard-mix":
        return (_vivid(a, b) >= 0.5).astype(np.float32)
    if mode == "darker-color":
        return np.where(_lum(b) < _lum(a), b, a)
    if mode == "lighter-color":
        return np.where(_lum(b) > _lum(a), b, a)
    if mode == "hue":
        return _set_lum(_set_sat(b, _sat(a)), _lum(a))
    if mode == "saturation":
        return _set_lum(_set_sat(a, _sat(b)), _lum(a))
    if mode == "color":
        return _set_lum(b, _lum(a))
    if mode == "luminosity":
        return _set_lum(a, _lum(b))

    # Paint.NET modes (REA PhotoCraft crates/color/src/blend.rs)
    if mode == "reflect":
        return np.where(b >= 1.0, 1.0, np.minimum(1.0, (a * a) / np.maximum(1.0 - b, 1e-6)))
    if mode == "glow":
        return np.where(a >= 1.0, 1.0, np.minimum(1.0, (b * b) / np.maximum(1.0 - a, 1e-6)))
    if mode == "negation":
        return 1.0 - np.abs(1.0 - a - b)
    if mode == "xor":
        a_u8 = np.clip(a * 255.0 + 0.5, 0, 255).astype(np.uint8)
        b_u8 = np.clip(b * 255.0 + 0.5, 0, 255).astype(np.uint8)
        return (a_u8 ^ b_u8).astype(np.float32) / 255.0

    raise ValueError(f"unknown blend mode: {mode}")


# ------------------------------------------------------------------ Deterministic Dithering (PhotoCraft)
def dither_noise(x: int, y: int) -> float:
    """Deterministic noise with no visible pattern (PhotoCraft 32-bit hash algorithm)
    for broadcast video and gradients without banding. Returns float in [0, 1)."""
    ux = int(x) & 0xFFFFFFFF
    uy = int(y) & 0xFFFFFFFF
    h = ((ux * 0x9E3779B1) & 0xFFFFFFFF) ^ ((uy * 0x85EBCA77) & 0xFFFFFFFF)
    h ^= (h >> 15)
    h = (h * 0x2C1B3C6D) & 0xFFFFFFFF
    h ^= (h >> 12)
    return float(h & 0xFFFF) / 65535.0


def dither_noise_grid(width: int, height: int) -> np.ndarray:
    """Generate a dither noise grid (height, width) in float32 [0..1) for frames and backgrounds."""
    w = max(1, int(width))
    h = max(1, int(height))
    xs = (np.arange(w, dtype=np.uint32) * np.uint32(0x9E3779B1))
    ys = (np.arange(h, dtype=np.uint32) * np.uint32(0x85EBCA77))
    grid = xs[None, :] ^ ys[:, None]
    grid ^= (grid >> 15)
    grid = grid * np.uint32(0x2C1B3C6D)
    grid ^= (grid >> 12)
    return (grid & np.uint32(0xFFFF)).astype(np.float32) / 65535.0


_DISSOLVE: dict = {}


def composite(a, layer, mode: str, seed: int = 0):
    """Backdrop a (h, w, 3|4) + layer (h, w, 4, straight alpha incl. its opacity) blended with `mode`.
    Applies ISO 32000-2 / W3C Compositing formula with straight alpha."""
    b, al = layer[..., :3], layer[..., 3:4]
    if mode == "dissolve":                                  # each pixel is either fully the layer or the backdrop
        key = (seed, al.shape)
        noise = _DISSOLVE.get(key)
        if noise is None:
            noise = np.random.default_rng(seed).random(al.shape, dtype=np.float32)
            _DISSOLVE[key] = noise
        return np.where(noise < al, b, a[..., :3] if a.shape[-1] >= 3 else a)

    blend_val = mix(a[..., :3], b, mode)
    if a.shape[-1] == 4:
        # Full W3C compositing with RGBA backdrop
        ab = a[..., 3:4]
        ao = al + ab * (1.0 - al)
        safe_ao = np.maximum(ao, 1e-6)
        rgb_o = ((1.0 - al) * ab * a[..., :3] + (1.0 - ab) * al * b + al * ab * blend_val) / safe_ao
        return np.concatenate([np.clip(rgb_o, 0.0, 1.0), np.clip(ao, 0.0, 1.0)], axis=-1)

    return a * (1 - al) + blend_val * al


def over(a, layer):
    """Plain alpha-over (what is above the blended layer)."""
    al = layer[..., 3:4]
    return a * (1 - al) + layer[..., :3] * al


# ------------------------------------------------------------------ Algoritm Avanse PhotoCraft (Kadans Parity)
def _fast_blur(arr_rgb: np.ndarray, radius: float) -> np.ndarray:
    """Flou rapid Gaussyen sou RGB [0..1] float32 ak Pillow C backend."""
    if radius <= 0.05 or ImageFilter is None:
        return arr_rgb
    u8 = np.clip(arr_rgb * 255.0 + 0.5, 0, 255).astype(np.uint8)
    im = Image.fromarray(u8).filter(ImageFilter.GaussianBlur(float(radius)))
    return np.asarray(im, dtype=np.float32) / 255.0


def color_to_alpha(
    arr: np.ndarray,
    key_color=(0.0, 1.0, 0.0),
    transparency: float = 0.0,
    opacity: float = 1.0
) -> np.ndarray:
    """Kalkil unmixing PhotoCraft (crates/algo/src/color_to_alpha.rs) pou retire yon koulè fon
    (fon vèt chroma, fon blan, fon nwa) epi kreye yon kouch transparan san franj ak zewo alo."""
    if isinstance(key_color, str):
        s = key_color.lstrip("#")
        if len(s) == 6:
            c = np.array([int(s[:2], 16), int(s[2:4], 16), int(s[4:], 16)], dtype=np.float32) / 255.0
        else:
            c = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    else:
        c = np.array(key_color[:3], dtype=np.float32)

    p = arr[..., :3]
    diff = p - c
    pos_denom = np.maximum(1.0 - c, 1e-7)
    neg_denom = np.maximum(c, 1e-7)

    a_pos = np.where(c < 1.0, diff / pos_denom, 1.0)
    a_neg = np.where(c > 0.0, -diff / neg_denom, 1.0)
    ai = np.where(diff > 0.0, a_pos, np.where(diff < 0.0, a_neg, 0.0))
    a = np.clip(np.max(ai, axis=-1), 0.0, 1.0)

    if transparency > 0.0 or opacity < 1.0:
        span = max(1e-6, opacity - transparency)
        a_m = np.clip((a - transparency) / span, 0.0, 1.0)
    else:
        a_m = a

    safe_am = np.maximum(a_m[..., None], 1e-6)
    q = np.clip(c + (p - c) / safe_am, 0.0, 1.0)
    q = np.where(a_m[..., None] <= 0.0, c, q)

    orig_a = arr[..., 3] if arr.shape[-1] >= 4 else np.ones(arr.shape[:2], dtype=np.float32)
    out_a = np.clip(orig_a * a_m, 0.0, 1.0)
    return np.concatenate([q, out_a[..., None]], axis=-1)


def high_pass(arr: np.ndarray, radius: float = 3.0) -> np.ndarray:
    """Filtre Passe-Haut pou detay teksti videyo: 0.5 + (o - b)."""
    b = _fast_blur(arr[..., :3], float(radius))
    hp = np.clip(0.5 + (arr[..., :3] - b), 0.0, 1.0)
    if arr.shape[-1] >= 4:
        return np.concatenate([hp, arr[..., 3:4]], axis=-1)
    return hp


def unsharp_mask(
    arr: np.ndarray,
    amount: float = 1.0,
    radius: float = 1.0,
    threshold: float = 0.0
) -> np.ndarray:
    """Netteté unsharp mask ak papòt pou anpeche bri sou fon ak po."""
    b = _fast_blur(arr[..., :3], float(radius))
    diff = arr[..., :3] - b
    mask = np.abs(diff) >= float(threshold)
    sharpened = np.clip(np.where(mask, arr[..., :3] + float(amount) * diff, arr[..., :3]), 0.0, 1.0)
    if arr.shape[-1] >= 4:
        return np.concatenate([sharpened, arr[..., 3:4]], axis=-1)
    return sharpened


def smart_sharpen(
    arr: np.ndarray,
    amount: float = 1.0,
    radius: float = 1.0,
    reduce_noise: float = 0.25
) -> np.ndarray:
    """Netteté entèlijan ak sipresyon bwi eksponansyèl PhotoCraft."""
    b = _fast_blur(arr[..., :3], float(radius))
    diff = arr[..., :3] - b
    keep = 1.0 - float(np.clip(reduce_noise, 0.0, 1.0)) * np.exp(-np.abs(diff) * 40.0)
    sharpened = np.clip(arr[..., :3] + float(amount) * diff * keep, 0.0, 1.0)
    if arr.shape[-1] >= 4:
        return np.concatenate([sharpened, arr[..., 3:4]], axis=-1)
    return sharpened


def auto_levels(arr: np.ndarray, clip_percent: float = 0.005) -> np.ndarray:
    """Etalonnage otomatik dinamik pou videyo ak kouch grafik."""
    out = arr.copy()
    h, w = arr.shape[:2]
    has_alpha = arr.shape[-1] >= 4
    mask = (arr[..., 3] > 0.02) if has_alpha else np.ones((h, w), dtype=bool)

    if not np.any(mask):
        return arr

    for c in range(3):
        ch = arr[..., c]
        valid_vals = ch[mask]
        if valid_vals.size == 0:
            continue
        lo = float(np.percentile(valid_vals, clip_percent * 100.0))
        hi = float(np.percentile(valid_vals, (1.0 - clip_percent) * 100.0))
        if hi - lo > 1e-5:
            out[..., c] = np.clip((ch - lo) / (hi - lo), 0.0, 1.0)

    return out


def rgb_histogram(arr: np.ndarray) -> dict:
    """Kalkile istogram 256 nivo pou chanèl R, G, B ak lumimans."""
    h, w = arr.shape[:2]
    has_alpha = arr.shape[-1] >= 4
    mask = (arr[..., 3] > 0.02) if has_alpha else np.ones((h, w), dtype=bool)

    hist = {"r": [0] * 256, "g": [0] * 256, "b": [0] * 256, "luma": [0] * 256}
    if not np.any(mask):
        return hist

    r_vals = np.clip(arr[..., 0][mask] * 255.0 + 0.5, 0, 255).astype(np.int32)
    g_vals = np.clip(arr[..., 1][mask] * 255.0 + 0.5, 0, 255).astype(np.int32)
    b_vals = np.clip(arr[..., 2][mask] * 255.0 + 0.5, 0, 255).astype(np.int32)
    l_vals = np.clip((0.299 * arr[..., 0][mask] + 0.587 * arr[..., 1][mask] + 0.114 * arr[..., 2][mask]) * 255.0 + 0.5, 0, 255).astype(np.int32)

    hist["r"] = np.bincount(r_vals, minlength=256).tolist()
    hist["g"] = np.bincount(g_vals, minlength=256).tolist()
    hist["b"] = np.bincount(b_vals, minlength=256).tolist()
    hist["luma"] = np.bincount(l_vals, minlength=256).tolist()
    return hist
