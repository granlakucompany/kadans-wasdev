# Skill: the CC0 sound library (ambience, foley, footsteps)

Kadans ships 68 real recorded sounds, all **CC0** (public domain: free, commercial use OK, no credit required —
credits are in `kadans/assets/sfx/CREDITS.md`). Sources: Kenney (kenney.nl) and Freesound (CC0 filter, license
checked on every sound page).

| Group | Sounds (ids) |
|---|---|
| Night / nature (loops) | `crickets-night` `frogs-night` `night-tropical` `birds-morning` `ocean-waves` `wind-soft` `rain-light` `fire-crackle` `clock-tick` `street-ambience` `children-playing` |
| Animals / weather | `rooster` `dog-bark-distant` `thunder` `wings-flapping` |
| People | `crowd-cheer` `crowd-applause` `gasp-surprise` `kiss-cheek` `heartbeat` |
| Home / foley | `door-creak` `door-open` `door-close` `door-knock` `metal-latch` `book-flip` `book-open` `book-close` `paper-rustle` `pencil-drawing` `paint-brush` `cloth` `coins` `saucepan` `candle-blow` `light-switch` `power-on-hum` |
| Steps / impacts | `footstep-soft` `footstep-wood` `footstep-concrete` `footstep-grass` `footstep-snow` `footstep-carpet` `tin-roof-steps` `running-steps` `jump-land` `impact-wood` `impact-metal` `impact-glass` `impact-soft` |
| Town / music-ish | `church-bell` `bell-heavy` `motorcycle-pass` `drum-rara` |
| Cartoon | `magic-sparkle` `cartoon-pop` `cartoon-boing` |
| Haiti (rara, tap-tap…) | `rara-band` `street-parade` `bamboo-trumpet` (vaksin-like) `conch-shell` (lanbi-like) `truck-horn` `bus-engine` `rain-tin-roof` `goat` `dominoes` `machete` `whistle` |

Many have several **variants** (5 wooden footsteps…): a sound used again plays the next variant.
`kadans sounds <words>` lists them; `--json` for scripts.

## In a spec
```json
{"type": "html", "src": "...", "voice": "Attends-moi, Anima !",
 "ambience": "find:krikèt nwit",
 "sounds": ["find:kòk", {"src": "find:pòt krake", "at": "Anima", "volume": 1.2},
            {"src": "sfx:power-on-hum", "at": 4.5}, {"src": "medya/sfx/my-own.wav", "at": 6, "bus": "fx"}],
 "rig": {"Lina": [{"do": "walk", "to": [1400, 960], "dur": 3, "steps": "wood"}, {"do": "jump", "steps": true}]}}
```
- `src`: `find:<words>` (search in Haitian Creole, French, English — accents and case do not matter), `sfx:<id>`,
  or a file.
- `sounds[]`: `at` (seconds in the scene, or a **spoken word**), `dur`, `volume` 0–2, `loop`, `fade`, `bus`
  (`fx`: short effects on their own bus, limited under the voice peak · `bed`: under the voice like music).
  Defaults: library ambiences loop on the bed, everything else plays once on the fx bus.
- `ambience`: one sound looping under the whole scene (`{src, volume (0.6), fade (0.8)}`), on the bed, ducked
  under the voice. Loops are seamless (the pack's ambiences are cross-faded end → start).
- `rig` actions `walk` / `run` with `"steps": "wood" | "concrete" | "grass" | "snow" | "carpet" | "metal" | "soft"
  | true`: one footstep each time a foot touches the floor — the same phase as the animation, so steps follow the
  feet. `jump` / `hop` with `steps`: one landing sound.

## Your own sounds
Put files in a folder and point `KADANS_SFX_DIRS` to it (several folders: separated by `;` on Windows). A folder
with an `index.json` like `assets/sfx/index.json` gets tags and loops; a plain folder: each file name is its tags.

## Lint
`sound_not_found`: a `find:` that finds nothing, an unknown `sfx:id`, or a missing file.
