# Changelog — Kadans WASDEV

## Unreleased — 2026-10-20

- **Character light (`rig.<name>.light`).** Cut-out characters take the light of the picture they stand in:
  `auto` reads the scene's background image (ambient colour, strength, rim-light colour and side, floor shadow),
  presets `night`, `moon`, `candle`, `dusk`, `day`, `indoor`, `none` (Creole / French names accepted), or your own
  `{tint, amount, bright, rim, rim_side, rim_w, shadow, glow, glow_w}`. The page applies an SVG colour filter, a
  one-sided rim drop-shadow, an optional glow (aura) and a contact shadow under the feet that stays on the floor
  and shrinks / fades while the character jumps (`kadans.motion.normalize_light`, `light_from_image`,
  `resolve_lights`; `rigLight` in the page). Characters without legs get no floor shadow.
- **Media server streams, never loads whole files.** `_serve_file` reads Range requests chunk by chunk (256 KB) instead of `read_bytes()` on the whole file for every seek (a 500 MB video was read whole on each request); `bytes=-N` and `HEAD` supported. Media get `Cache-Control: no-cache` + `ETag` (mtime+size) so the browser revalidates and gets `304` when unchanged; editor code (html/js/css/json) stays `no-store`.
- **Waveform peaks cached.** `audio.peaks()` decodes a file with FFmpeg once and caches the result in memory and on disk (`%LOCALAPPDATA%/Kadans/peaks`, key = path + mtime + size): 20 s file 3.6 s → 0.8 ms (disk) / 0.07 ms (memory). Before, every timeline redraw ran FFmpeg on every audio block.
- **Media panel: preview, thumbnails, live list.** Every audio / video tile in the Timeline media panel has a small
  play button: click to hear the sound or watch the clip inside the tile, click again to stop — nothing is added to
  the timeline. Video tiles show their first frame (`GET /api/thumb`, a 320 px JPEG made once by FFmpeg and cached by
  path + size + mtime in `<project>/.kadans-cache/thumbs/`); audio tiles show a 24-bar waveform and every audio /
  video tile its length (`GET /api/media-info`, cached; at most 2 requests at a time). The list refreshes by itself
  when a file lands in `medya/` from outside the page (`GET /api/media-rev`, polled every 2.5 s while the page is
  visible) — `studio_editor/media_panel.js`, phrases in `kadans_phrases4.js`.
- **Add a host file to the project media.** `POST /api/media/add {path}` and `StudioServer.add_media(path)` COPY a
  file of the host project (never moved, never trimmed; files outside the project are refused with 403) into
  `medya/<kind>/`. The kind comes from `media_preview.import_kind`: images → `imaj`, videos → `videyo`, audio →
  `vwa` when the name / folder says voice (vwa, voice, voix, narr…), `sfx` when it says sound effect (sfx, whoosh,
  click, hit…), otherwise `mizik`. A file dropped twice is not copied twice. `KMP.hostDrop(paths, x, y)` lets a host
  app (WASDEV: drag from its project tree) drop files on the page: they are copied, then placed where they were
  dropped (media panel, timeline track or viewer) exactly like a media dragged from the panel.
- **Track heads say what each track is, with a number.** Every track head shows its kind and its number per kind,
  top to bottom — «Vwa 1», «Vwa 2», «Odyo 1», «SFX 1», «Mizik 1», «Videyo 1», «Tèks 1», «Sen 1» — recomputed on every
  render (adding / removing a track renumbers). An audio track counts as Vwa / Mizik / SFX from its name or the
  `medya/` folder of its clips. A custom name stays, on a second smaller line under the number (ellipsis + full name
  in the tooltip only when really too long); auto names like «Audio 1» given to every new track no longer show.
  The track-name column is wider (214 px) and the bold kind + number is never squeezed by the record / mute / lock
  buttons.
- **A media dropped on a track keeps its EXACT length.** Audio / video clips used to land as tiny 2 s clips: now
  `dropAssetOnTrack` (media panel tile, host drop, file drop, viewer audio drop, recorded voice) waits for the real
  file length (`KMP.duration`: `/api/media-info`, then the browser's own metadata) — a 7.3 s sound becomes a 7.3 s
  clip (block width = dur × PPS); several dropped files are laid end to end at their real lengths. Images keep the
  2 s default.
- **Host drops on the Edge / WebView2 engine.** A file dropped from outside the page first asks the host
  (`POST /api/audio-bridge {cmd: "host_drop", names}`): a host that recognises its own drag (WASDEV project tree)
  answers with the full paths (copied server-side, any size) or handles the copy itself; anything else goes on to
  the normal upload.
- **MP3 / AAC preview fallback.** When the browser cannot decode a file, the play button falls back to
  `GET /api/preview-audio` (a cached mono 22 kHz WAV made by FFmpeg).
- **Uploads are streamed to disk** (no 200 MB cap, nothing held in RAM) and, without a `kind` hint, sorted with the
  same `import_kind` rule.
- **Autosave also rebuilds `composition.html`.** Each `PUT /api/spec` schedules a debounced (1.5 s) rebuild in a
  background thread — one at a time, the last save wins, the editor never waits. It is offline: only voices already
  in the cache are used (`audio.voices(..., offline=True)`), never a TTS call.
- **Faster open.** A project whose `composition.html` + `audio_map.json` are newer than `spec.json` opens without a
  rebuild (`StudioServer.fresh()`); `/api/spec` no longer rebuilds everything when a project simply has no
  `preview-audio.wav`. Builds are serialized (`_build_lock`). The server no longer does a reverse-DNS lookup when it
  binds (`HTTPServer.server_bind` → `getfqdn()`, 2-4 s on some Windows networks). A project with nothing to hear
  skips the FFmpeg preview mix (and drops a stale one). `build(offline=True, mix=False)` gives hosts a fast
  composition-only build (cached voices, no soundtrack) to open the editor at once and run the full build after;
  `audio.voices` returns before touching the TTS engine when no scene has a voice line.
- **Blank projects.** A spec with no scene now builds as one empty black scene (before: a title card with
  «Kadans WASDEV»), so a project can start from zero.

- **Cuts are exact.** Three bugs made a trimmed clip "jump back": (1) the editor set the clip's `in` only when the
  clip already had one, so splitting / deleting the left part / dragging the left edge restarted the file at 0 s;
  (2) the mix decoded only `dur` seconds of the source, so `atrim=in:…` found nothing; (3) with FFmpeg 8.1, a trimmed
  stream mixed by `amix` lost its `adelay` padding and landed at 0 s (`aresample=async=1:first_pts=0` fixes it).
  Clip speed is now applied in the editor preview too.

- **Live AI montage in the Timeline.** When an AI writes a video, the editor replays every media it added
  (track clips: voice, music, SFX, video, image; scene overlays) in front of the developer: an AI cursor picks the
  item in the media / SFX panel, drags it along a smooth curve onto the right track at the right time and drops it;
  cuts (`in`) are shown as a live left-edge trim. One-shot plan `.kadans-montage.json` (`GET /api/montage`), banner
  with "2x faster" / "Finish now". `spec.json` on disk is already final and autosave pauses during the montage, so
  closing the page mid-way loses nothing (`studio_editor/ai_montage.js`).
- **Track clip in-points are rendered.** The final mix and the page now honour a clip's `in` (trim start in the
  source file); before, the editor preview used it but the MP4 always started the file at 0 s.

- **Voices are never cut.** A scene `duration` is now a minimum: a longer voice line (plus lead-in and tail)
  extends the scene (before, the duration won and the end of the line was cut). Voices are mixed with 150 ms of
  silence before (the denoiser / compressor no longer eat the first sound) and 0.35 s after. Track clips that are
  voices (track/clip named voice / vwa / voix / narration / dialogue, or `"voice": true`) always play to their end and
  never fade in. TTS text gets a final full stop when it has none (models tend to clip the last syllable).
- **Voice speed.** `voice.speed` (0.5-2, whole video) and scene `voice_speed`; pitch kept (`atempo`). Timings use the
  real sped-up file, so words / captions stay in sync.
- **Video speed.** `speed` (0.25-4) on a `video` scene and on track clips: frames, scene length and clip sound follow.
- **Faster preview.** `preview_sounds()` caches its mix (key = only what changes the sound): reopening the preview
  went from 10-36 s to 0.01 s.

- **French by default.** A spec without `lang` is French (`KADANS_LANG` changes it); the CLI, the cloud server, the
  Timeline (new projects) and HyperFrames import follow.
- **Each character its own voice.** Scene key `speaker`: `"male"` / `"female"` / `{name, gender, voice_id}`
  overrides the video voice for that scene's line (dialogue).
- **Facial expressions.** `rig` characters get a mood: `expr` list per character (`[{at: s | spoken word, expr}]`)
  or `expr` on an action (alone = face only). Moods `neutral happy sad surprised angry` (kontan, tris, sezi, fache…).
  The page shows `[data-brows] > [data-expr]` and the `data-expr` variants of the rest mouth / open eyes; speech and
  blinks keep working. Lint: a face without a body is not `rig_missing`.
- **Bones that follow** (`follow: {role, k}`): a dress front panel follows the near thigh — sitting covers the lap.
- **Scene sounds in the preview.** `audio.preview_sounds()` mixes ambience, sounds, footsteps, music and automatic
  SFX without voices (`preview-sounds.m4a`); `build_html(..., preview_audio=)` makes the standalone page play it in
  sync (the Timeline's page plays its `preview-audio.wav`).
- **11 Haitian-flavoured CC0 sounds** (68 in all): street drums / rara band, marching band, wooden horn (vaksin-like),
  cow horn (lanbi-like), car horn, old bus engine, rain on a tin roof, goat, dominoes, machete, whistle. Recordings
  with speech were checked with Whisper (wrong-language chatter removed). `tools/sfx/fs_pick_ht.py`, `add_pack.py`.
- **CC0 sound library.** 57 real recorded sounds ship in `kadans/assets/sfx/` (Kenney + Freesound, all CC0, license
  checked per sound, credits in `CREDITS.md`): night / nature ambiences (seamless loops), animals, weather, crowds,
  doors, paper, pencil, footsteps on 7 surfaces, impacts, bells, cartoon. New scene keys `sounds` (`find:<words>` in
  Haitian Creole / French / English, `sfx:<id>` or a file; `at` in seconds or at a spoken word; `volume`, `loop`,
  `fade`, `bus fx|bed`) and `ambience` (one loop under the whole scene, on the bed). Rig actions get `steps`:
  footsteps on the animation's foot contacts, landing sounds for jump / hop. Variants rotate. `KADANS_SFX_DIRS` adds
  your own folders. `kadans sounds <words>`. Kadans Timeline: the SFX panel lists, plays and adds library sounds
  (copied into `medya/sfx/`). Lint: `sound_not_found`. Guide: `skills/25-sound-library.md`. Rebuild the pack:
  `tools/sfx/`.
- **Characters that move (cut-out rig).** New scene key `rig: {name: [actions]}`: characters exported from WASDEV
  Design (`[data-rig]` group, parts `[data-bone]` with their joints and standard roles) walk, run, jump, hop, sit,
  stand, wave, talk, nod, point, cheer, fall, fly and glide. Actions start at a time or at a spoken word, move the
  feet `to` / `by` / along a `path` (video pixels), turn the character toward where it goes, and layer (a motion
  only moves the bones it knows). Walk / run cycles follow the distance travelled, the lowest point stays on the
  floor. New module `kadans/motion.py`: the motion table and the same evaluator in Python and JavaScript (tested
  equal to 1e-13). Scenes last until the last action ends. Lint: `rig_missing`, `rig_no_roles`. Guide:
  `skills/24-rig-characters.md`.
- **Talking characters (lipsync).** New scene key `lipsync: true | {blink: false}`. In the scene markup, a mouth is
  `[data-mouth]` with one child per shape `[data-shape="A".."H"|"X"]` (Preston Blair set) and eyes are `[data-eyes]`
  with `[data-eye="open|half|closed"]`. At render, Rhubarb Lip Sync (MIT, local, phonetic recognizer: any language)
  reads the voice WAV and the matching mouth is shown at every frame (cached `<voice>.mouth.json`); without Rhubarb,
  and in the live preview, shapes are estimated from the letters of the spoken words. Eyes blink on a fixed
  schedule (same frames every render). `__busy` reports talking / blinking so frame deduplication never freezes a
  mouth. `KADANS_RHUBARB` points to the program. Lint: `lipsync_no_mouth`, `lipsync_no_voice`,
  `mouth_shape_missing`. Guide: `skills/23-lipsync-characters.md`.
- **Voice always on top.** Everything that is not the voice (music, SFX on tracks or automatic, clip sound) is mixed
  into one bed, measured against the voice (EBU R128) and capped: loudest 400 ms moment ≤ voice level − 4 LU, peaks
  ≤ 60 % of the voice peak (lookahead limiter), then ducked while the voice speaks. Before, only the music was ducked
  and SFX on tracks were not limited at all. New spec key `mix: {cap, bed_ceiling, bed_peak, duck}`.
  `KADANS_KEEP_STEMS=1` keeps the voice / bed stems and a `.mix.json` report. Measured on a 50 s demo: bed louder
  than the voice in 310 of 358 speech windows before, 0 of 329 clear-speech windows after.
- Subtitles: `*highlight*` stars no longer leak into the `.srt` file.
- **SFX have their own bus.** Automatic SFX, Timeline SFX clips (`kind: "sfx"`) and clips on tracks with
  `kind: "sfx"` (or named `SFX …`) no longer go through the 9:1 music duck that made short hits vanish: they are
  limited to `fx_peak` × the voice peak (default 0.9) with a light 2.5:1 duck while the voice speaks
  (`mix: {fx_peak, fx_duck}`). The Timeline preview audio now includes the automatic SFX, like the final render.
- **Many clips no longer break the mix on Windows.** Every clip used to add one `-i` input: 100+ SFX clips made the
  FFmpeg command line longer than the Windows limit (32 767 chars, WinError 206). Now one input per file (asplit for
  repeats) and a long filter graph goes through a file (`-/filter_complex`, FFmpeg ≥ 7.1; `-filter_complex_script`
  before).

## 0.6.0 — 2026-10-15

- No more leaked browsers: Windows job object (kill on close), DevTools `Browser.close`, then taskkill; process
  groups on Linux / macOS. Look filter: bloom blur at 1/4 size, vignette + grain in YUV (3x less CPU); GPU / OpenH264
  preset `faster`; one browser per CPU core by default.

- `kadans doctor` (checks + exact fixes + one test frame) and `kadans setup` (FFmpeg LGPL + pinned Chromium
  155.0.8059.84 into Kadans' folder, SHA-256 checked); MCP tool `kadans_doctor`. The first render downloads what is
  missing by itself (one download even with 8 render threads; KADANS_NO_AUTO_SETUP=1 = off). Order: KADANS_CHROME, the pinned
  Chromium, then Edge / Chrome.

- Faster render: every scene is cut in 2 s pieces (the cache unit) so ALL browsers work, even on a 3-scene video;
  default browsers = 2 per CPU core, max 8, limited by free RAM; `optimizeForSpeed` screenshots.
  Measured: 23 s video with motion blur 4 — 388 s → 176 s; unchanged re-render 12 s.

- `kadans mcp`: MCP server (JSON-RPC over stdio, standard library only) — the same 9 tools for every AI client:
  `kadans_schema`, `kadans_validate`, `kadans_lint`, `kadans_frame` (image content: the AI sees the frame, JPEG
  ≤ 1280 px), `kadans_preview`, `kadans_render` (background job, never times a client out) + `kadans_status`,
  `kadans_fonts`, `kadans_media`. Long calls run in threads (ping / list stay instant).
- `kadans mcp --install claude-desktop | claude-code | codex | gemini | cursor | vscode | windsurf` writes the
  client config (keeps the other entries, writes a `.kadans-backup`); `kadans mcp --print` for any other client.
- Standalone voice: `KADANS_TTS_CMD`; word timing: faster-whisper if installed.
- `h264_mf` (Windows encoder, for LGPL FFmpeg builds): constant bitrate ~8 Mbit/s at 1080p30 (SSIM 0.995) instead of
  "quality 100" (34 Mbit/s).

## 0.5.0 — 2026-10-15

- **27 blend modes** for overlays (names of photo editors accepted: "Linear Dodge (Add)", "Pin Light"…). 17 drawn by
  the browser (`linear-dodge` = `plus-lighter`); 10 composited exactly by the renderer (`kadans.blend`, optional
  numpy + Pillow): the frame is captured in layers (under, the layer alone on a transparent background — only its
  rectangle, reused while unchanged —, above — only the rectangle that holds something), then blended pixel by pixel.
- **Fonts:** `kadans.fonts` scans every installed font (Windows / macOS / Linux + a project `fonts/` folder; TTF,
  OTF, TTC name tables; cached). `brand.font_title` and `brand.font_code` join `brand.font`; chosen fonts are
  embedded with `@font-face`. `kadans fonts [word]`. Lint checks all three fonts.

## 0.4.0 — 2026-10-15

- `background` for the whole video or any scene: photo, looping video (frame-exact JPEG sequence) or design asset;
  `fit`, `opacity`, `dim`, slow `zoom`, brand-colour `tint`, `color` (recolour a one-colour SVG).
- `overlays` (max 8 per level): atmosphere layers behind (`back`) or in front of (`front`) the content, with
  `blend` modes, position / size, `rotate`, `color`, and animations `drift`, `pulse`, `spin`, `float`, `reveal`,
  `sweep` on the video clock.
- SVG recolouring keeps opacity and gradients (only paint values change); inline SVG ids are made unique.
- `media.set_root(tag, folder)`: `"tag:relative/path"` sources point into a host app's asset library.
- Lint: `overlay_covers_text`.

## 0.3.0 — 2026-10-15

- **Everything follows the voice.** Word timing per voice line from a pluggable recognizer (`align`, e.g. Whisper),
  cached; the script's own words keep their spelling and take the heard timings (difflib alignment), missed words
  are interpolated; without a recognizer the timing is estimated.
- Items, list entries, numbers, chips and compare columns appear on the spoken word that names them (`on` to choose
  the word); `*highlighted*` words pulse when spoken.
- Animated captions (`captions`: karaoke / pop, bottom / top / middle); `.srt` lines start on their first word.
- Automatic sound effects (`sfx`): whoosh on cuts, pop on entrances, hit on logo reveals — generated by FFmpeg.

## 0.2.0 — 2026-10-15

- License: **MIT** (was Apache-2.0), with `TRADEMARKS.md` (names and logo are not covered) and
  `THIRD_PARTY_NOTICES.md` (FFmpeg and the browser are used, never shipped).

- `kadans render`: headless Edge / Chrome (or PySide6 QtWebEngine) through a built-in DevTools client (standard
  library only), one cached chunk per scene (re-render only what changed, resume after a crash), parallel browsers,
  JPEG frames piped to FFmpeg, H.264 (NVENC / AMF / QSV / h264_mf / OpenH264), BT.709 tags, faststart.
- Sound: voice per scene through a pluggable TTS callable (cached per line), music generated by FFmpeg from a mood +
  seed (cached loop), ducking under the voice, clip sound, two-pass loudness to -14 LUFS, `.srt` subtitles.
- Cinematic finish after capture (`look`: bloom, grain, vignette) and `motion_blur` (2-6 sub-frames).
- `kadans lint` (safe area, long / clipped text, overlaps, missing images and fonts, voice longer than its scene),
  `kadans frame`.
- Faster pages: radial gradients instead of CSS blur; emoji font fallbacks; progress bar now optional.
- Fix: a URL opened through `/json/new` lost its `#render` hash (the page played in real time instead of seeking).

## 0.1.0 — 2026-10-15

First version, by Getho Guerrier — GRAN LAKU COMPANY.

- Spec format v1 (JSON) with validation that lists every problem as `path: message`, and a JSON Schema.
- 11 scene types: hook, logo, text, features, list, stat, code, compare, cta, video, image.
- 7 frame formats: 16:9, 9:16, 1:1, 4:5, 21:9, 1.91:1, 4K — layouts adapt automatically.
- Your own videos (trim, cover / contain, captions, sound level) as frame-exact cached image sequences; photos with
  a slow push-in.
- Deterministic `window.__seek(t)` (async: waits for fonts and images); real clock frozen while rendering.
- Live preview with a time bar (play / pause, scrub, frame by frame) = the same drawing code as the render.
- "Made with Kadans WASDEV" credit on the last scene (localized, `"credit": false` to remove).
- CLI: `kadans validate`, `kadans html`, `kadans schema`.
