# 26 - Vector camera, parallax and particles (html scenes)

A Design frame exported with `kadans_scene` is a 100 % vector set in layers. Kadans moves a **camera** over it
and adds **particles** - no hand-written script, the same image on every render.

## Layers and depth
Name each top layer of the Design frame **`fon 1 · …` to `fon 6 · …`** (or set `data-depth="0.4"`).

| layer | depth | moves with the camera |
|---|---|---|
| `fon 1` sky, moon | 0.04 | almost not |
| `fon 2` mountains | 0.15 | |
| `fon 3` sea, bay | 0.3 | |
| `fon 4` distant town | 0.5 | |
| `fon 5` houses | 0.75 | |
| `fon 6` / characters / everything else | 1 | fully |

Draw layers 120 px wider than the frame on each side (WASDEV `DESIGN/DEKO` sets are 2160 px wide at x = -120),
so a pan never shows an edge. `camera.depth` overrides a layer by name: `{"fon 3 · bè a": 0.25}`.

## `camera` (html scene)
```json
"camera": {"pan": 70, "zoom": 1.05, "origin": [960, 700], "ease": "inout",
           "follow": {"rig": "Lina", "amount": 0.4}, "shake": [{"at": 2.6, "force": 7, "dur": 0.35}], "limit": 120}
```
- `pan` px the camera travels over the scene (`70` or `[x, y]`, +x = right).
- `zoom` end zoom (`1.05`) or `[from, to]`; `origin` = zoom point in scene px (default: centre).
- `follow` the camera also follows a rig character's horizontal travel (`amount` 0-1, `offset` [x, y]).
- `shake` impacts: landing, fall, door slam. `limit` keeps the camera within ±px of the start.

## `fx` (any scene)
```json
"fx": [{"type": "dust",   "at": 2.6, "x": 1560, "y": 815},
       {"type": "sparks", "at": 2.6, "x": 1560, "y": 800, "count": 12},
       {"type": "trail",  "follow": "Anima", "offset": [60, 40], "color": "#ffb347"},
       {"type": "rain",   "count": 120, "angle": 12},
       {"type": "smoke",  "at": 0, "dur": 4, "x": 300, "y": 600}]
```
Common keys: `at`, `dur` (s), `color`, `count`, `size`, `seed`, `spread`, `speed`, `opacity`; `rain` also `angle`.
`trail` draws the light trail behind a rig character from its past positions. Positions are scene px, inside the
camera (they move and zoom with the set). An `fx` object WITHOUT `type` stays the editor's colour filter
(blur, brightness...).

## In the Timeline editor
Select a scene, then the **Effects** tab: a **Camera** card (html scenes: pan, start / end zoom, zoom point,
motion, limit, follow a character, shakes with "+ Shake now" at the playhead) and a **Particles** card (add dust,
sparks, light trail, rain, smoke at the playhead; edit time, duration, position, count, size, opacity, colour).
Every change is undoable and writes the same `camera` / `fx` keys an AI writes.
