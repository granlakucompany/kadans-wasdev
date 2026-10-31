# AGENTS.md — driving KADANS WASDEV VIDEO ENGINE

Kadans is built so an AI agent produces a finished video from one JSON spec. This file is the contract
any agent (Claude Code, Codex, Cursor, Gemini, Copilot, Windsurf, Aider, Continue, Cline, Zed…) follows.

## The loop
1. **Write a spec** (JSON): `brand`, `scenes[]`, optional `voice`, `music`, `ratio`, `transition`, `libs`.
2. **Validate**: `python -m kadans validate spec.json` → it returns EVERY problem as `path: message`.
   Fix them and re-validate. Unknown keys are rejected on purpose (a typo is an error, not silence).
3. **Lint**: `python -m kadans lint spec.json` → catches cut text, unsafe zones, voice-too-long, etc.
4. **Render**: `python -m kadans render spec.json out.mp4`.

## Scene types
`hook · text · logo · features · list · stat · code · compare · cta · video · image · chart · social · html`
See `skills/` for one focused guide per capability.

## Golden rules for agents
- **One spec → one video.** Don't shell out to other tools; Kadans owns validate → lint → render.
- **HTML is the base.** For anything the ready-made scenes can't do, use an `html` scene (full HTML/CSS/JS +
  vendored MIT libs: anime, chart, lottie, three, motion). Reveal on a spoken word with `class="a" data-on="word"`.
- **Speak.** Set `voice` (lang: fr|en|ht|es|pt|de|it|ru, gender). Haitian Creole (`ht`) is first-class.
- **Stay local.** No API keys, no network at render time.
- **Read errors literally.** The validator's `path: message` tells you exactly what to change.

## Project layout (MANDATORY for every video, ad, reel, short film)
Start every job with `python -m kadans new "<Real-Name>"` (or create the same tree yourself). The name must say
what the project is (`Lanmou-nan-Jakmel`, `Rara-Jacmel-2026-ad`): an id like `gslmmfs5sjm`, `project1`,
`video` or `test` is refused.

```
Analyseur-Kadans/<Real-Name>/
    spec.json  composition.html       the edit — open it with `python -m kadans timeline <folder>`
    01-senaryo/                       script, characters, synopsis
    02-storyboard/                    shot by shot (images + PDF)
    medya/vwa  medya/mizik  medya/sfx  medya/imaj  medya/videyo
    Exported Videos/                  final renders: <Real-Name>_v1.mp4, _v2 … (inside THIS project folder)
```
- **Every media you make or use goes into `medya/<kind>/`** — voices, music, SFX, AI images, clips — with a
  name that says what it is (`sen02-plan01-marie-bonjou.wav`, `poster-rara-jacmel.png`). Never leave a file only
  in a temp / app-data folder: copy it into `medya/` and point the spec at the copy.
- The timeline editor's **Media** panel shows `medya/` grouped by kind, so a person without WASDEV sees every
  file the agent used. Its uploads and generated voices / music go there too; renders go to
  `Exported Videos/` and are numbered, never overwritten (an old `rann/` folder is still read, never moved).
- Short film order: `01-senaryo` → `02-storyboard` → `medya` → `spec.json` (edit) → `Exported Videos`.

## Skills index
`skills/README.md` lists every skill. Load the one that matches your task.
