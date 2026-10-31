# Skill: Haitian Creole voice (ht)

Kadans is the first video engine that speaks **Haitian Creole**. Set `voice:{lang:"ht"}` and write the
narration in Creole. Creole orthography is phonetic, so the French phonemizer approximates it well;
refine specific words with `voice.lexicon` or a `prononciation_ht.json`.
```json
{"voice":{"lang":"ht","gender":"female"},
 "scenes":[{"type":"hook","title":"Yon sèl app","voice":"Yon sèl app pou tout bagay."}]}
```
