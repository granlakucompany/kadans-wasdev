# Skill: html scene (full freedom)

When the ready-made scenes aren't enough, write raw HTML/CSS/JS:
`{type:"html", html:"<div>...</div><script>...</script>", libs?:[anime|chart|lottie|three|motion]}`
or `{type:"html", src:"scene.html", libs:[...]}`. Libs are vendored locally (MIT).
**Whisper sync:** put `class="a" data-on="word"` on any element → it appears when that word is spoken.
HTML is the engine's base: your scene compiles into the same single page as everything else.
