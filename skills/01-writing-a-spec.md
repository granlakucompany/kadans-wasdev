# Skill: Writing a Kadans spec

A spec is one JSON object. Minimum: `brand.name` + `scenes[]`.
```json
{"title":"Demo","lang":"en","ratio":"16:9","brand":{"name":"WASDEV"},
 "voice":{"lang":"en","gender":"female"},"music":{"mood":"upbeat","seed":3},
 "scenes":[{"type":"hook","title":"What if *one app* did it all?","voice":"What if one app did it all?"},
           {"type":"cta","title":"Try it today","subtitle":"wasdev.ai","voice":"Try it today."}]}
```
Then: `kadans validate` → fix `path: message` errors → `kadans lint` → `kadans render out.mp4`.
`*word*` highlights a word; it pulses when spoken. Durations follow the voice/clip automatically.
