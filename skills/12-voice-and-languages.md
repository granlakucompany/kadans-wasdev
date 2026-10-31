# Skill: voice and 5 languages

`voice: {lang, gender, enhance?, lexicon?, retries?, verify?}`. Languages: **fr, en, es, pt, ht** —
female and male, from the voice engine the host app plugs in (WASDEV: ElevenLabs; `sample` = clone with OpenVoice). `enhance` (default on) cleans the voice (EQ, de-ess, compressor).
Per scene, `voice:"the narration line"`. Mix is -14 LUFS. Music, SFX, clip sound and track clips are **never
louder than the voice**: the loudest moment of that bed stays 4 LU under the voice level, its peaks under 60 % of the
voice peak, and it is ducked while the voice speaks. Tune with `mix: {bed_ceiling: -4, bed_peak: 0.6, duck: true}`
(`cap: false` = off).
`lexicon: {"WASDEV":"wazdˈɛv"}` fixes a pronunciation (espeak-ng IPA).

Default language: **French** (`lang` missing → `fr`; `KADANS_LANG` changes it). In WASDEV the voice engine is
**ElevenLabs** — the only one (no key / no credits: stop and tell the developer). A `sample` is cloned with OpenVoice.

## Dialogue: each character its own voice
A scene's `speaker` overrides the video voice for that scene's line: `"speaker": "male"` or
`{"name": "Grand-père Jo", "gender": "male", "voice_id": "JBFqnCBsd6RMkjVDRZzb"}` (ElevenLabs voice id). One
voice line per scene: cut a dialogue into one scene per line. WASDEV Storyteller `{op:kadans}` does it for you.
