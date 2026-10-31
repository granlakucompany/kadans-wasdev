# Skill: characters that walk, run, sit, wave and fly (cut-out rig)

A cut-out character is drawn in parts (head, torso, upper arm, forearm, hand, thigh, shin, foot, wings…). Each
part hangs on a **bone** that turns around its joint (shoulder, elbow, knee…). Kadans moves the bones with a
library of motions, keeps the feet on the floor and moves / turns the character across the frame. Works with
`lipsync` (the mouth talks while the character walks).

## 1. Make the character (WASDEV Design)
- Ready-made, already rigged: `{op: "character", kind: "lina" | "rose" | "anima", parent: "SC02-P03", x, y, h}`
  (girl, grandmother, paper bird; vector layers you can redraw, talking face included).
- Your own drawing: group the parts, `rig2d_create`, then one `rig2d_bone` per part with its joint. Name the
  bones like the body part — `bra dwat`, `avant-bras gauche`, `left thigh`, `tèt`, `jip` — or set the roles
  with `rig2d_role`. Draw the character **from the side, looking right**: `right` = the side nearer the camera.
- Preview a motion on the canvas: `{op: "rig2d_motion", rig, do: "walk", t: 0.55}`.
- Export the frame: `{op: "kadans_scene", uid: "SC02-P03"}` → an HTML file with `data-rig="Lina"` on the
  character and `data-bone` on every part.

Roles: `hips torso neck head arm_l forearm_l hand_l arm_r forearm_r hand_r thigh_l shin_l foot_l thigh_r shin_r
foot_r wing_l wing_r tail`.

## 2. The spec
```json
{"type": "html", "src": "Analyseur-Kadans/sen-design/SC02-P03.html",
 "voice": "Attends-moi, Anima !", "lipsync": true,
 "rig": {
   "Lina":  [{"do": "run", "to": [1400, 960], "dur": 2.4}, {"do": "wave", "at": "Anima", "side": "r"}],
   "Grann Rose": [{"do": "talk", "at": 0.5, "dur": 3}, {"do": "point", "at": 4}],
   "Anima": {"idle": false, "do": [{"do": "fly", "path": [[1100, 300], [1400, 180], [1000, 120]], "dur": 3.4}]}}}
```

| Key | Meaning |
|---|---|
| `do` | `walk run wave talk nod fly glide idle` (loops) · `jump hop sit stand point cheer fall pose` (once; `sit stand point cheer fall pose` keep their last pose) |
| `at` | start, in seconds from the scene start — or a **word of the voice line** (`"at": "Anima"`). Default: after the previous action |
| `dur` | seconds (loops default 2 s) |
| `to` / `by` / `path` | where the **feet** go, in video pixels: `[x, y]`, `[dx, dy]`, or a curve through points (flying) |
| `face` | `right`, `left`, `auto` (moving actions turn the character toward where it goes) |
| `speed`, `amount` | loop speed when standing still · size of the motion (0–2) |
| `side` | `r` / `l`: which arm waves / points / talks |
| `ease` | `ramp` (walk / run: steady speed), `inout`, `linear` |
| `angles` | `{"head": -10, "arm_r": -90}` with `do: "pose"`: a pose of your own |
| `expr` | the face mood from this action on: `happy`, `sad`, `surprised`, `angry`, `neutral` (or kontan, tris, sezi, fache, nòmal). An action with only `expr` (no `do`) changes the face without moving |
| `steps` | `walk` / `run`: a footstep sound on every foot contact (`wood`, `concrete`, `grass`, `snow`, `carpet`, `metal`, `soft` or `true`); `jump` / `hop`: a landing sound — see `25-sound-library.md` |

Per character: `{"face": "right", "idle": true, "ground": true, "drawn": "right", "expr": [{"at": 0, "expr":
"happy"}, {"at": "Anima", "expr": "surprised"}], "do": [...]}` — `idle: false`
stops breathing between actions, `ground: false` lets the feet leave the floor (flying), `drawn: "left"` if you
drew the character looking left.

Ready-made characters: `lina` (girl), `rose` (grandmother), `woman`, `man`, `boy`, `anima` (paper bird) —
`{op: "crowd", n: 5}` adds neighbours with different colours, `{op: "prop", kind: chair|stool|table|candle|
streetlamp|sketchbook|mask}` the set. Dresses have a front panel that **follows** the near thigh (bone
`follow: {role: "thigh_r", k: 0.9}`): when the character sits, the skirt covers the lap.

## Light: put the character INTO the picture
A flat vector character on a painted night (or candle-lit) background looks pasted on. Give each character a
`light` (per character, next to `do`):

| `light` | effect |
|---|---|
| `"auto"` | reads the scene's background image: ambient colour, strength (darker = stronger), rim light colour + side, floor shadow |
| `"night"` · `"moon"` · `"candle"` · `"dusk"` · `"day"` · `"indoor"` · `"none"` | presets (also nwit / nuit, lalin / lune, bouji / bougie, jou / jour, anndan…) |
| `{preset, tint, amount, bright, rim, rim_side, rim_w, shadow, glow, glow_w}` | your own: `tint` #rrggbb + `amount` 0-1 (colour of the light on the character), `bright` 0.2-1.6, `rim` #rrggbb (a thin edge of light on `rim_side` left / right / top, `rim_w` px), `shadow` 0-1 (contact shadow under the feet: it stays on the floor, smaller and lighter when the character jumps), `glow` #rrggbb (an aura — Anima's wings), `glow_w` px |

Keys you set win over `auto`. Characters without legs (flying) get no floor shadow. The Storyteller montage
(`{op: kadans}`) puts `light: "auto"` on every rigged character.

**Background without the character**: a storyboard picture usually already contains the character. Before you
place the moving cut-out character on it, run Design `{op: clean_plate, uid: <shot frame>}` (AI cut-out finds the
people, Codex repaints the same set without them, the original stays in `fill.orig`; `boxes` removes small
things the cut-out missed). Otherwise you see two Linas: one painted, one moving.

## How it behaves
- A motion only moves the bones it knows: Lina sits, then waves — her legs stay seated.
- Walking / running cycles follow the distance travelled (stride ≈ 0.66 / 1.25 × height per cycle): the feet do
  not slide. The lowest point of the character stays on the floor (feet planted, sitting lowers the body).
- The same motion table runs in Python (`kadans.motion.frame_at`) and in the page (`rigFrame`): the preview, the
  Design canvas and the render are identical.

## Lint
`rig_missing` (no `[data-rig]` with that name in the scene) · `rig_no_roles` (the action needs limbs the
character does not have: walking without legs, flying without wings).
