# Skill: use Kadans with Windsurf

**Goal:** have Windsurf produce a finished video from one JSON spec, 100% locally.

**Setup:** Index the repo; add AGENTS.md to Cascade memory. Ask Cascade to build and render a spec.

**The loop (same for every agent):**
1. Write `spec.json` (see `skills/01-writing-a-spec.md`).
2. `python -m kadans validate spec.json` → fix every `path: message`.
3. `python -m kadans lint spec.json`.
4. `python -m kadans render spec.json out.mp4`.

Kadans speaks **fr/en/es/pt/ht** (Haitian Creole included). No API keys, no network at render time.
