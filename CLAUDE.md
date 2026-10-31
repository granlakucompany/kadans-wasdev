# Kadans WASDEV VIDEO ENGINE

This repo is an open-source video engine by **Gran Laku Company (Getho Guerrier)**:
**one JSON spec -> HTML -> MP4**, plus a pro **timeline editor that runs in any browser**
(edit a whole video with AI or fully by hand, then export). Local only: no API keys, no network at render.

**To see every tool, type `/kadans`** (or just start by reading `AGENTS.md` and `skills/README.md`).

## Fast start
- FIRST: `python -m kadans new "<Real-Name>"` — mandatory layout (01-senaryo, 02-storyboard, medya/vwa|mizik|sfx|imaj|videyo, Exported Videos); every media goes in `medya/<kind>/` with a clear name (see `AGENTS.md`).
- Make a video: write a spec JSON, then `python -m kadans validate` -> `lint` -> `render out.mp4`.
- Open the editor: `python -m kadans timeline <folder>` or double-click `RUN.cmd` / `RUN.command` / `run.sh`.
- Scene types: hook text logo features list stat code compare cta video image chart social html.
- HTML is the base for anything custom. Voice langs: fr|en|ht|es|pt|de|it|ru (Haitian Creole first-class).

## Map
- `AGENTS.md` - one-page contract for any coding agent.
- `skills/` - 22 capability guides + 12 per-agent guides (`skills/README.md` is the index).
- `kadans/` - the engine (spec, compose, renderer, audio, blend, lint) + `studio_editor/` and `studio_server.py` (the browser editor).
- `.claude/commands/kadans.md` - the `/kadans` command. `.claude/skills/kadans/` - the auto-discovered skill.
- `assets/design/` - 10,001 CC0 design SVG (designer: Getho Guerrier, Gran Laku Company).
