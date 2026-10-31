# Skill: animation libraries

Vendored locally (MIT), loaded on demand via `libs` (page-level or on an html scene):
**anime** (timeline animation), **chart** (Chart.js), **lottie** (After Effects JSON), **three** (3D/WebGL),
**motion** (motion.one). They are copied next to the page at render (same-origin, 100% offline).

## Plain CSS animations are frame-accurate (no library needed)
Inside an `html` scene, every browser animation — CSS `@keyframes`, CSS `transition`, `element.animate()`
(Web Animations API) — is paused and driven by the video clock: time 0 = the scene's start. What you see in the
preview is exactly what the MP4 contains, frame by frame (a slow frame capture can no longer make it drift).

```html
<style>
  .logo { animation: rise .8s cubic-bezier(0,0,.58,1) .5s both; }
  @keyframes rise { from { translate: 0 60px; opacity: 0 } to { translate: 0 0; opacity: 1 } }
</style>
<div class="logo">WASDEV</div>
```

- Prefer the independent `translate` / `scale` / `rotate` properties: they do not overwrite an element's
  existing `transform` (rotation, mirror).
- `__busy(t)` reports a running CSS animation, so motion blur sub-frames are captured while it moves.
- To drive animations yourself (custom `onSeek`), put `data-waapi="off"` on the scene root or any element.
- WASDEV Design layers with an animation (`{op:animate}`) export to exactly this CSS via `{op:kadans_scene}`.
