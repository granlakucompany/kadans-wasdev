# Skill: use Kadans with Aider

**Goal:** have Aider produce a finished video from one JSON spec, 100% locally.

**Setup:** `aider AGENTS.md skills/01-writing-a-spec.md` then: "create spec.json for a 20s product teaser".

**The loop (same for every agent):**
1. Write `spec.json` (see `skills/01-writing-a-spec.md`).
2. `python -m kadans validate spec.json` → fix every `path: message`.
3. `python -m kadans lint spec.json`.
4. `python -m kadans render spec.json out.mp4`.

Kadans speaks **fr/en/es/pt/ht** (Haitian Creole included). No API keys, no network at render time.
