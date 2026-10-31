# Skill: talking characters (lipsync + blinking eyes)

A character's mouth follows the scene's voice, and its eyes blink. Works in any scene whose markup you control
(mostly `html` scenes holding an inline SVG drawn in a design tool).

## 1. Draw the mouth shapes (Preston Blair set)
Put every mouth of one character in a group `data-mouth`, one child per shape `data-shape`. Only one is shown
at a time; draw them at the same place.

| Shape | Mouth | Sounds |
|---|---|---|
| A | closed | M B P |
| B | slightly open, teeth together | S T K, "i" |
| C | open | "è", "é" |
| D | wide open | "a" |
| E | slightly rounded | "o", "eu" |
| F | puckered | "ou", W |
| G (optional) | upper teeth on lower lip | F V (falls back to B) |
| H (optional) | tongue up | L (falls back to C) |
| X (optional) | rest / silence | (falls back to A) |

A child may hold several shapes: `data-shape="G B"`.

## 2. Eyes
A group `data-eyes` with children `data-eye="open"`, `"closed"` and optionally `"half"`. Blinks follow a fixed
schedule (every 2–5 s): the same frames at every render. Eyes blink in every scene; `"lipsync": {"blink": false}`
keeps them open.

## 3. The spec
```json
{"type": "html", "voice": "Anima… c'est comme ça que je vais t'appeler.", "lipsync": true,
 "html": "<svg viewBox='0 0 1920 1080'> … <g data-mouth='Lina'><g data-shape='A'>…</g> … <g data-shape='X'>…</g></g>
          <g data-eyes='Lina'><g data-eye='open'>…</g><g data-eye='half'>…</g><g data-eye='closed'>…</g></g></svg>"}
```
`voice` or `voice_file` (your own recording) both work. Several characters in one scene share the scene's voice
line: give each its own scene (or cut) when they talk in turn.

## 4. Expressions (happy, sad, surprised, angry)
Optional variants, chosen while the character is in that mood (speech and blinks keep working):
- eyebrows: a group `data-brows="Lina"` with children `data-expr="neutral|happy|sad|surprised|angry"`;
- a rest mouth / open eyes for a mood: add `data-expr` next to the shape (`data-shape="X" data-expr="happy"`,
  `data-eye="open" data-expr="surprised"`).
The mood comes from the scene `rig` (`{"Lina": {"expr": [{"at": 0, "expr": "happy"}, {"at": "Anima", "expr":
"surprised"}]}}` or `"expr"` on an action — see `24-rig-characters.md`); a face without a body works too. WASDEV
Design `face_set` draws all of it (layers «sousi: Lina», «X kontan», «ouvè sezi»…).

## How the mouths are timed
At render, **Rhubarb Lip Sync** (MIT, local) reads the voice WAV with its language-independent phonetic recognizer
and returns the shapes with their times (cached as `<voice>.mouth.json`). Set `KADANS_RHUBARB` to `rhubarb.exe`
or put it on the PATH. Without Rhubarb — and in the live preview, which has no voice yet — the shapes are
estimated from the letters of each spoken word.

## Lint
`lipsync_no_mouth` (no `data-mouth` / `data-shape` in the scene), `lipsync_no_voice` (nothing to say),
`mouth_shape_missing` (one of A–F not drawn: the closest shape is shown instead).
