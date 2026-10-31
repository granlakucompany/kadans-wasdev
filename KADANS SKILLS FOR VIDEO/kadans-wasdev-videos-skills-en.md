# Kadans WASDEV — 201 Professional Video Skills (English Edition)

> Complete official documentation of all 201 Kadans video skills for WASDEV.

---

## Category A: Studio Modes & Production Formats

### 001. `/videostudiopro` — Professional Studio Production

- **Role** : Elevate the video to the standards of a high-end broadcast television studio.
- **Kadans Composition** : 3-point lighting (Key light, Fill light, purple Rim light), soft shadows `box-shadow: 0 30px 60px rgba(0,0,0,0.5)`, micro-reflections on elements, 60 FPS kinetic animated titles, professional color grading.
- **AI Obligation** : Inject the `.studio-pro` class into `spec.json` with advanced CSS for color grading, refined framing, and centered titles with generous breathing room.

### 002. `/effectdocumentary` — Cinematic Documentary Style

- **Role** : Create an immersive documentary atmosphere (Netflix / National Geographic quality).
- **Kadans Composition** : Ken Burns effect (smooth 1.05x zoom over 6 seconds on images and archives), elegant serif or grotesque typography, warm color tones with softened contrast, lower-right title with date/location.
- **AI Obligation** : All images must feature a smooth `ken-burns` animation, the voiceover must include natural pauses between sentences, and the soundscape must be calm with subtle reverberation.

### 003. `/effectcinema` — Anamorphic Cinematic 21:9

- **Role** : Give the video the look and feel of a true widescreen cinematic film.
- **Kadans Composition** : Anamorphic 2.39:1 aspect ratio with black letterbox bars top and bottom, smooth 24 FPS or 60 FPS frame rate, Teal & Orange color grade (`#0284c7` in shadows, `#f97316` in highlights), subtle 35mm film grain.
- **AI Obligation** : Add the `.cinematic-letterbox` overlay layer, cinematic color filters, and smooth camera pans without abrupt cuts.

### 004. `/effectcommercial` — High-Impact Product Commercial

- **Role** : Structure high-impact personal or product advertising that captivates and converts fast.
- **Kadans Composition** : Fast-paced rhythm (1.5 to 2.5 seconds per scene), punchy bold headlines, dynamic brand colors, quick-zoom product showcase, vibrant end-card CTA.
- **AI Obligation** : Scenes must be concise, phrasing direct and punchy, and every shot must feature continuous visual motion.

### 005. `/effectsocialreel` — Vertical Format 9:16 (Shorts, Reels, TikTok)

- **Role** : Optimize the video for vertical mobile consumption.
- **Kadans Composition** : 1080x1920 resolution (9:16), central safe zone (clearing side like/comment UI overlays), prominent dynamic subtitles in the center, snappy eye-catching animations.
- **AI Obligation** : Enforce `ratio: "9:16"` in the spec, positioning all key elements between 20% and 80% of screen height.

### 006. `/effectexplainer` — Explainer & Educational Video

- **Role** : Explain a complex system, idea, or application clearly and simply.
- **Kadans Composition** : Clean neutral background, step-by-step appearing SVG vector icons, connector arrows linking concepts, highlight summary callouts.
- **AI Obligation** : Use `.draw-path` animations on connecting lines, grouping ideas into clear 1, 2, 3 blocks.

### 007. `/effectnewsroom` — Broadcast Newsroom & Breaking News

- **Role** : Give the video the look and feel of a major live broadcast news channel.
- **Kadans Composition** : Continuous lower-third news ticker, pulsing red `FLASH INFO` or `LIVE` badge, split-screen window for interviews.
- **AI Obligation** : Insert the `.news-ticker-bar` scrolling ticker with right-to-left text, timestamp badge, and lower-third headline bars.

### 008. `/effectpodcastclip` — Podcast Clip & Audio Visualizer

- **Role** : Turn an audio conversation into an engaging, dynamic social video.
- **Kadans Composition** : Speaker photo or video portraits in circular or frosted-glass frames, animated central audio waveform, word-by-word color-highlighted subtitles.
- **AI Obligation** : Integrate `.audio-waveform-canvas`, framing each speaker's name and episode title with polished styling.

### 009. `/effecttutorialpro` — Software Walkthrough & Step-by-Step Tutorial

- **Role** : Demonstrate how to operate software or systems with exact precision.
- **Kadans Composition** : Full-screen software interface capture, animated mouse cursor navigating and clicking with yellow/blue click-halo, focal zoom-ins on active areas.
- **AI Obligation** : Add the `.cursor-pointer` element with `translate` and `scale(0.9)` click animations, alongside a contextual callout box.

### 010. `/effectproductshowcase` — 3D Product Showcase with Turntable Rotation

- **Role** : Showcase a physical product or software box from every perspective.
- **Kadans Composition** : Centered object rotating smoothly in 3D space (`transform: rotateY()`), specular light glints sweeping across its surface, glowing contextual hotspots around it.
- **AI Obligation** : Utilize CSS 3D perspective (`perspective: 1200px`), gradient lighting on the object, and callout pointer lines connected to technical specifications.

---

## Category B: Visual Effects, UI & Glass Widgets

### 011. `/effectglasswidget` — Frosted Glass Cards (Glassmorphism)

- **Role** : Give all informational containers a modern frosted translucent glass aesthetic.
- **Kadans Composition** : `background: rgba(255, 255, 255, 0.07)`, `backdrop-filter: blur(25px)`, border `1px solid rgba(255, 255, 255, 0.18)`, diffused shadow `0 20px 40px rgba(0,0,0,0.37)`.
- **AI Obligation** : Wrap cards and sections in the `.glass-card` class with a subtle white specular highlight along the top edge.

### 012. `/effectchecklist` — Animated Checklist with Auto-Checkmark

- **Role** : Display a sequence of milestones validated one after the other.
- **Kadans Composition** : Each row slides in from below, the box checks with a vibrant green animation (`#10b981`), a stroke drawing the checkmark (`✓`), and the text glowing with success.
- **AI Obligation** : Create `.checklist-item` elements with staggered sequential animation delays (`delay: index * 0.4s`).

### 013. `/effectorbit` — 3D Orbiting Elements Around a Central Core

- **Role** : Symbolize an ecosystem, satellites, or interconnected technologies.
- **Kadans Composition** : A central core (logo or product) with 3 to 6 icons or mini-cards revolving along a 3D elliptical orbit with Z-depth.
- **AI Obligation** : Integrate `.orbit-container` with `keyframes orbit3d` animation where element scale and opacity vary depending on whether they pass in front of or behind the core.

### 014. `/effectisometric3d` — Stacked Layer 3D Isometric View

- **Role** : Visualize software architecture, security layers, or data tiers in 3D.
- **Kadans Composition** : `transform: rotateX(60deg) rotateZ(-45deg)`, planes separated along the Z-axis (`translateZ(40px)`), cast shadows beneath each tier.
- **AI Obligation** : Draw 3 to 4 isometric layers rising from the base to reveal how the system is constructed.

### 015. `/effectdeviceframe` — Realistic Phone or Laptop Device Mockup

- **Role** : Showcase a web or mobile application inside a realistic device frame.
- **Kadans Composition** : iPhone 16 Pro or MacBook Pro mockup featuring metallic bezels, screen glare reflections, and a scrolling video/web capture inside the display.
- **AI Obligation** : Place the `.device-mockup` frame with cleanly clipped screen viewport (`overflow: hidden; border-radius: 40px`).

### 016. `/effectdatabubbles` — Floating Data Bubbles with Metrics

- **Role** : Convey an intelligent system processing real-time data streams.
- **Kadans Composition** : Glowing spheres or luminescence pills gently drifting upward with subtle sway, each displaying key figures (e.g., `+45%`, `99.9%`, `4K`, `AI`).
- **AI Obligation** : Generate `.data-bubble` particles with natural sinusoidal `sine` floating animations at varying velocities.

### 017. `/effectcardstack` — Sliding Card Stack

- **Role** : Present multiple testimonials, features, or images that cycle through like a deck of playing cards.
- **Kadans Composition** : 3 cards stacked in perspective depth, the top card sliding aside or upward to reveal the next.
- **AI Obligation** : Use dynamic `translateY` and `rotate` transitions to produce a natural tactile physics feel.

### 018. `/effecttimelineprog` — Step-by-Step Progress Timeline

- **Role** : Illustrate the evolution of a project, roadmap milestones, or process workflow stages.
- **Kadans Composition** : Glowing track drawing from left to right or top to bottom, each node illuminating as the trace reaches it alongside dates or milestone titles.
- **AI Obligation** : Integrate `.timeline-track` with a `.timeline-fill` progress line expanding from 0% to 100%.

### 019. `/effectglowbadge` — Luminescent Glowing Edge Badge

- **Role** : Highlight a key callout such as 'NEW', 'OFFICIAL', 'PREMIUM', or 'PRO'.
- **Kadans Composition** : Compact label bordered by neon pulsing glow (`box-shadow: 0 0 20px var(--neon-color)`), bold uppercase typography.
- **AI Obligation** : Attach the `.badge-glow` badge featuring an infinite 2-second `pulse-glow` animation to the focal element.

### 020. `/effectstatscounter` — Fast-Incrementing Statistics Counter

- **Role** : Showcase impressive quantifiable results with numerical counters rolling from 0 up to final values.
- **Kadans Composition** : Oversized numbers ticking up rapidly over 1.5 seconds with an ease-out deceleration, flanked by vibrant `%`, `+`, or `$` symbols.
- **AI Obligation** : Use a WAAPI counter script or Kadans numerical sequences to synchronize number rollout with a subtle tick sound effect.

### 021. `/effectnotifalert` — Drop-Down Mobile / Desktop Push Notification

- **Role** : Simulate an incoming priority message, sale notification, or system alert.
- **Kadans Composition** : Rectangular frosted-glass notification popup sliding down from top screen with subtle elastic bounce, featuring app icon, sender, message snippet, and timestamp.
- **AI Obligation** : Create `.notification-popup` with `cubic-bezier(0.175, 0.885, 0.32, 1.275)` easing for the elastic bounce.

### 022. `/effectsearchbar` — Self-Typing Search Bar

- **Role** : Simulate a query a prospective client searches online or depict an active solution lookup.
- **Kadans Composition** : Sleek search bar with magnifying glass icon, text typing character-by-character with blinking cursor, search button click trigger, and reveal of search results beneath.
- **AI Obligation** : Implement `.typing-input` sequences with per-character staggered delays followed by an immediate result container expansion transition.

### 023. `/effectcomparecards` — Before / After Comparison Cards with Slider Splitter

- **Role** : Highlight the radical contrast between legacy methods and the new WASDEV solution.
- **Kadans Composition** : Side-by-side cards (Red / Green or Grayscale / Color), or a single view with a sliding vertical splitter line revealing the transformation.
- **AI Obligation** : Create a clear-cut comparison leveraging `✗` icons for legacy pain points and `✓` icons for modern solutions.

### 024. `/effectpiechart3d` — Animated Bar & Donut / Pie Charts

- **Role** : Visualize market metrics, profitability margins, or key performance indicators.
- **Kadans Composition** : Bar charts rising upward from the baseline with distinct color palettes, or SVG circular charts drawing sectors with floating callout tags.
- **AI Obligation** : Render the chart using SVG `stroke-dasharray` animated from 0 to the target percentage value.

### 025. `/effectmatrixgrid` — Technical Matrix Grid & Futuristic Coordinates

- **Role** : Evoke a high-tech cybersecurity, advanced computing, or command center aesthetic.
- **Kadans Composition** : Fine-line cyan or green matrix grid over a dark background, glowing junction intersection points, streaming numerical coordinates along margins.
- **AI Obligation** : Add a `.tech-grid-overlay` layer with perspective gliding smoothly along the Y-axis.

---

## Category C: Typographic Animation & Kinetic Text

### 026. `/effectkinetictext` — Explosive Kinetic Text on the Beat

- **Role** : Make each word appear with high-impact energy tightly synchronized with the musical beat.
- **Kadans Composition** : Words bounce, expand, rotate, and shift weight (Light -> Black 900) on each musical beat.
- **AI Obligation** : Split text word by word, applying fast sequential `scale` and `rotation` animations.

### 027. `/effecttypewriter` — Mechanical Typewriter

- **Role** : Type out text like a confidential report, a code terminal, or a story in progress.
- **Kadans Composition** : Letters appear one by one at a fixed pace (~40ms per letter), with a flashing black/green rectangular cursor at the end of the sentence.
- **AI Obligation** : Use the `.char-reveal` sequence with synchronized keyboard click sounds.

### 028. `/effecttextgradient` — Moving Aurora Gradient Text

- **Role** : Give large headlines an extraordinary aesthetic with a flowing liquid spectrum within the letters.
- **Kadans Composition** : `background: linear-gradient(135deg, #10b981, #0098ff, #ec4899, #8b5cf6)`, `background-clip: text`, `-webkit-text-fill-color: transparent`, 8-second `background-position` animation.
- **AI Obligation** : Apply the `.gradient-text-animated` class to all major headlines.

### 029. `/effectmaskedtext` — Geometric Mask Text Reveal

- **Role** : Slide text up from beneath an invisible threshold without overflowing.
- **Kadans Composition** : A container with `overflow: hidden`, where text rises from `translateY(100%)` to `translateY(0)` with an ultra-smooth motion.
- **AI Obligation** : Wrap each text line in a `.mask-container` element for a clean reveal without overflow.

### 030. `/effectwordhighlight` — Real-Time Voice Word Highlight (Karaoke Pro)

- **Role** : Guide audience focus to each word exactly as the speaker utters it.
- **Kadans Composition** : The full sentence appears in light gray, and each word lights up in vivid yellow, green, or blue when spoken (based on Whisper timestamps).
- **AI Obligation** : Use `.words.json` data to apply the `.active-word` class at the exact millisecond.

### 031. `/effect3dtextfloat` — Floating 3D Headline

- **Role** : Create a sense of power and physical weight for key headlines.
- **Kadans Composition** : Text with multi-layered `text-shadow` creating realistic 3D extrusion, gently orbiting in 3D space.
- **AI Obligation** : Add `text-shadow: 0 1px 0 #ccc, 0 2px 0 #c9c9c9, 0 3px 0 #bbb, 0 4px 0 #b9b9b9, 0 10px 20px rgba(0,0,0,0.4)` and 3D rotation.

### 032. `/effectneontext` — Flickering Glowing Neon Text

- **Role** : Nighttime street ambience, futuristic city, or retro-wave style.
- **Kadans Composition** : Pink, cyan, or orange glow with deep illumination and an initial flickering pulse resembling an igniting neon tube.
- **AI Obligation** : Apply `@keyframes neon-flicker` with multi-layered `text-shadow: 0 0 10px, 0 0 20px, 0 0 40px`.

### 033. `/effectglitchtext` — Digital Glitch Text (RGB Split)

- **Role** : Hacking scenes, security codes, system alerts, or high-octane tech action.
- **Kadans Composition** : Text splits into two chromatic copies (red and cyan) horizontally offset for milliseconds with horizontal slicing lines.
- **AI Obligation** : Use `::before` and `::after` pseudo-classes with `clip-path` to render the glitch slice effect.

### 034. `/effectoutlinetext` — Outline Text with Fill Reveal

- **Role** : Trendy fashion typography or minimalist architectural aesthetic.
- **Kadans Composition** : Text starts as an outline `-webkit-text-stroke: 2px white` with no fill, then liquid-like color rises from the bottom to fill it.
- **AI Obligation** : Animate color fill with a bottom-to-top gradient over 1 second.

### 035. `/effectflipboard` — Split-Flap Mechanical Letters (Airport Board)

- **Role** : Transition from one word to another with a satisfying mechanical flip effect.
- **Kadans Composition** : Each letter is divided into two halves that flip in 3D from top to bottom to reveal the new character.
- **AI Obligation** : Create a `.flip-char` container with sequential `rotateX(-90deg)` rotations on each character.

### 036. `/effectsupersize` — Giant Background Word Behind Subject

- **Role** : Add scene depth with an oversized word positioned behind the character or product.
- **Kadans Composition** : Text scaled to 200px to 300px at 10% opacity, subtly drifting in the opposite direction of camera movement.
- **AI Obligation** : Position text with `z-index: 1`, opacity `0.08`, and continuous parallax motion.

### 037. `/effectstampbold` — Heavy Stamp Impact Word with Camera Shake

- **Role** : Affirm a decision, indisputable truth, or milestone victory ("GUARANTEED", "APPROVED", "CERTIFIED").
- **Kadans Composition** : The word starts oversized at full opacity, slamming down rapidly with a screen shake and heavy impact sound.
- **AI Obligation** : Apply `scale(3) -> scale(1)` animation and 0.2-second `camerashake` on impact.

---

## Category D: Particles, Atmospheres & Special Effects

### 038. `/effectparticles` — Floating Stardust & Sparkles

- **Role** : Breathe life into the scene with magical sparkle or calm technological serenity.
- **Kadans Composition** : 40 to 60 glowing white and purple micro-particles gently rising via Brownian motion on a 2D Canvas.
- **AI Obligation** : Embed `.particles-canvas` in the background with minimal CPU overhead.

### 039. `/effectsmoke` — Dense Smoke & Realistic Vapor

- **Role** : Create mystery, dramatic depth, or live stage concert atmosphere.
- **Kadans Composition** : Soft smoke layers drifting upward with fractal turbulence and `mix-blend-mode: screen` blending.
- **AI Obligation** : Add `.smoke-overlay` layer with smooth blur and opacity transitions.

### 040. `/effectsplashemboss` — Liquid Splash & Ink Splatter

- **Role** : Energetic transition or artistic showcase with bursts of paint and liquid.
- **Kadans Composition** : Liquid SVG shapes forming droplets or ink splatters rapidly blooming outward from the center.
- **AI Obligation** : Embed `.splash-blob` vectors with elastic physics to unveil the scene.

### 041. `/effectcyberpunkcity` — Cyberpunk Night City with Neon Lights

- **Role** : High-tech nighttime atmosphere with hot pink and cyan glow.
- **Kadans Composition** : Deep dark/navy background, wet ground reflections, vertical neon beams, and suspended overhead powerlines.
- **AI Obligation** : Blend colors `#ec4899` and `#0098ff` across all shadows and highlights.

### 042. `/effectmatrixrain` — Vertical Matrix Code Rain

- **Role** : Convey code execution, algorithms, or background security operations.
- **Kadans Composition** : Columns of green katakana or alphanumeric glyphs cascading down a black backdrop with luminous trails.
- **AI Obligation** : Embed `.matrix-rain` Canvas with green `#10b981` glyphs and bright glowing white leads.

### 043. `/effectlightrays` — Volumetric Sunbeams (God Rays)

- **Role** : Evoke hope, grandeur, triumph, or spiritual illumination.
- **Kadans Composition** : Conical shafts of light beaming from upper right or left across the frame, carrying illuminated dust motes.
- **AI Obligation** : Add `.volumetric-rays` layer with `mix-blend-mode: color-dodge` and micro-rotation animation.

### 044. `/effectfireflare` — Optical Lens Flare (Anamorphic Streak)

- **Role** : Add realistic cinematic flair as the camera sweeps across a direct light source.
- **Kadans Composition** : Horizontal blue anamorphic streaks and halo discs sweeping the screen during camera movement.
- **AI Obligation** : Apply `.anamorphic-flare` sliding horizontally across scene transitions.

### 045. `/effectspacecosmos` — Galaxies, Nebulae & Deep Space

- **Role** : For visionary projects, large-scale ambitions, or future concepts.
- **Kadans Composition** : Twinkling starfield, slowly rotating purple and blue nebulae, and shooting stars periodically crossing the frame.
- **AI Obligation** : Build multi-depth parallax with 3 star layers (small, medium, large) moving at differential speeds.

### 046. `/effectglitchcyber` — Signal Static & CRT Scanlines

- **Role** : Disruption scenes, sudden shock, rhythm breaks, or retro-futuristic mood.
- **Kadans Composition** : Horizontal scanlines, subtle TV static noise, and a 0.3-second vertical sync roll.
- **AI Obligation** : Apply `.crt-scanlines` overlay with rapid vertical jitter.

### 047. `/effectbokehglow` — Soft Light Circles (Bokeh f/1.4)

- **Role** : Warm, intimate, high-end atmosphere with prime lens shallow depth of field.
- **Kadans Composition** : Soft blurred light discs gently drifting upward in the background with warm pastel tones.
- **AI Obligation** : Generate `.bokeh-orb` elements with `filter: blur(12px)` and varying opacities.

### 048. `/effectshockwave` — Circular Shockwave on Impact

- **Role** : Emphasize a decisive climax, explosive announcement, or pivotal moment.
- **Kadans Composition** : A transparent circle expanding rapidly from center screen with subtle refractive distortion of the background.
- **AI Obligation** : Animate `.shockwave-ring` with `transform: scale(0) -> scale(4)` and opacity fading out within 0.4s.

### 049. `/effectembersfire` — Flying Red-Orange Fire Embers

- **Role** : Infuse passion, raw power, fiery warmth, and high-stakes action.
- **Kadans Composition** : Flickering red, yellow, and orange embers ascending through the air like sparks from a bonfire or forge.
- **AI Obligation** : Integrate `.fire-embers` particles with warm edge lighting along the bottom of the screen.

---

## Category E: Camera Movements & Spatial Dynamics

### 050. `/effectdollyzoom` — Hitchcock Vertigo Effect (Dolly Zoom)

- **Role** : Trigger a sense of psychological disorientation or dramatic revelation.
- **Kadans Composition** : Camera dollies back while zooming in on the subject: subject size remains constant while the background perspective warps and recedes.
- **AI Obligation** : Combine inverse `scale()` transforms between the foreground subject and background layer.

### 051. `/effectcamerashake` — Dynamic Camera Shake

- **Role** : Simulate a physical impact, an earthquake, or a heavy musical bass drop.
- **Kadans Composition** : The camera vibrates along the X and Y axes for 0.2 to 0.5 seconds with rapid decay.
- **AI Obligation** : Apply `@keyframes camera-shake` and `transform: translate(random, random)` to the entire main container.

### 052. `/effectparallaxdepth` — Layer-by-Layer 2.5D Parallax

- **Role** : Transform a flat image or illustration into a true 3D world with depth.
- **Kadans Composition** : The foreground moves rapidly, the midground moves at normal speed, and the background moves very slowly as the camera pans.
- **AI Obligation** : Separate elements into 3 layers `.layer-fg`, `.layer-mg`, `.layer-bg` with distinct velocity coefficients.

### 053. `/effectpanoramicsweep` — Wide Panoramic Sweep

- **Role** : Showcase the scale of a project, an office, a landscape, or a full team.
- **Kadans Composition** : The camera glides steadily from left to right across an ultra-wide canvas at constant speed, with smooth deceleration at the end.
- **AI Obligation** : Animate `translateX()` on the wide container over 4 to 6 seconds.

### 054. `/effectcrashzoom` — Crash Zoom on a Detail

- **Role** : Shift from a wide shot to land abruptly on a key detail (a button, a face, a line of code).
- **Kadans Composition** : Zoom from 1x to 4x in under 0.4 seconds with subtle motion blur.
- **AI Obligation** : Apply `scale(4)` and `transform-origin` precisely on the coordinates of the target element.

### 055. `/effectorbitcam` — Orbiting Camera Around Subject

- **Role** : Dynamic presentation of a character or product while keeping it centered.
- **Kadans Composition** : The camera orbits 180° or 360° around the subject while lighting shifts across its surface.
- **AI Obligation** : Use centered 3D perspective and continuous `rotateY` animation.

### 056. `/effectfirstperson` — First-Person View (POV)

- **Role** : Put the viewer in the shoes of the user or main character.
- **Kadans Composition** : Subtle natural walking sway (head bobbing), with hands appearing at the bottom of the screen to click or touch objects.
- **AI Obligation** : Add subtle 0.2-degree rotation movements and vertical Y displacement synced to the walking rhythm.

### 057. `/effectdroneflyover` — Drone Aerial Flyover

- **Role** : Breathtaking introduction descending from the clouds to land on the subject.
- **Kadans Composition** : High-angle camera looking down while descending, leveling its angle to face the project horizontally.
- **AI Obligation** : Combine `translateY`, `rotateX(45deg) -> rotateX(0)` and smooth zoom.

### 058. `/effecttiltshift` — Miniature Model Effect (Tilt-Shift)

- **Role** : Make a real city or large vehicle appear like a miniature toy model on a table.
- **Kadans Composition** : A narrow, ultra-sharp horizontal strip at screen center flanked by intense blur top and bottom, with boosted color saturation.
- **AI Obligation** : Apply vertical blur masking and color saturation `saturate(1.4)`.

### 059. `/effectwhipcamera` — Fast Whip Pan Camera

- **Role** : Energetic transition between two actions where the camera turns so fast that everything blurs.
- **Kadans Composition** : A sharp 0.2-second horizontal sweep with heavy directional blur `blur(30px, 0px)` landing on the new scene.
- **AI Obligation** : Integrate the `.whip-pan-transition` class between the two scenes.

### 060. `/effectcameraroll` — Camera Roll on Axis

- **Role** : Extreme action scenes, outer space sequences, or moments where everything flips upside down.
- **Kadans Composition** : The camera rotates 180° or 360° around the Z-axis while the action continues playing in the center.
- **AI Obligation** : Animate `rotateZ()` with a fast pace at mid-point and smooth deceleration at the end.

### 061. `/effectslowmotion` — Extreme Slow Motion (Slow-Mo 120 FPS)

- **Role** : Deconstruct a brief, rapid action (a water droplet, a smile, a keystroke) to reveal its beauty.
- **Kadans Composition** : The action plays at 25% of its normal speed with 60 FPS fluidity and zero stutter.
- **AI Obligation** : Extend the scene duration in the spec and slow down all WAAPI animations by 4x.

---

## Category F: Kadans Pro Transitions

### 062. `/effectseamlesszoom` — Infinite Seamless Zoom Transition

- **Role** : The camera dives into a letter, window, or eye in the first scene to become the entire background of the second scene.
- **Kadans Composition** : Zoom 1x -> 50x onto a precise point until its color fills the entire screen to reveal the next scene.
- **AI Obligation** : Synchronize the vanish point of the first scene with the opening point of the second scene.

### 063. `/effectmorphshape` — Fluid Shape Morphing

- **Role** : A logo transforming into a button, or an icon melting into another shape.
- **Kadans Composition** : An SVG `path` smoothly interpolating its coordinates from shape A to shape B with an identical vertex count.
- **AI Obligation** : Use SVG morphing animations on the vector paths.

### 064. `/effectinkbleed` — Spreading Ink Bleed on Paper

- **Role** : Organic, artistic, or historic transition where black or colored ink unveils the scene.
- **Kadans Composition** : An SVG mask expanding with irregular organic contours like water bleeding on parchment paper to reveal the image.
- **AI Obligation** : Apply a `mask-image` with a fluid shape expanding outward from the center.

### 065. `/effectglitchwipe` — Digital Tear Transition (Glitch Wipe)

- **Role** : Switch scenes like a satellite feed glitching out and reconnecting instantly.
- **Kadans Composition** : The first scene shatters into horizontal pixel blocks for 0.2 seconds, followed by a clean reveal of the second scene.
- **AI Obligation** : Integrate the `.glitch-wipe` transition with a short electronic glitch sound.

### 066. `/effectflashwhite` — Energetic White Flash

- **Role** : Mark a major temporal shift or high-impact revelation.
- **Kadans Composition** : The screen turns pure white for 3 frames (~50ms) and quickly fades out to reveal the new scene.
- **AI Obligation** : Add a white overlay layer `.flash-overlay` with an `opacity: 1 -> 0` transition in 0.3s.

### 067. `/effectdooropen` — Center Split Door or Curtain Opening

- **Role** : Introduce a new chapter or welcome the audience into a new space.
- **Kadans Composition** : Two frosted glass or dark panels sliding apart horizontally (left and right) from the center dividing line.
- **AI Obligation** : Create two panels `.split-door-left` and `.split-door-right` with `translateX` animations.

### 068. `/effectpapertear` — Center Paper Tear

- **Role** : Tear down an old rule, discard an outdated contract, or reveal the hidden truth behind it.
- **Kadans Composition** : An irregular tear line travelling from top to bottom, with both paper pieces parting sideways accompanied by a tearing sound effect.
- **AI Obligation** : Integrate an SVG mask with realistic torn edges and subtle drop shadows beneath each piece.

### 069. `/effectblurzoom` — Fast Radial Blur Zoom

- **Role** : Switch scenes in a fraction of a second without the eye catching the seam.
- **Kadans Composition** : Strong circular blur `filter: blur(20px)` coupled with a quick zoom snap that vanishes immediately upon entering the new scene.
- **AI Obligation** : Apply the `.blur-zoom-in` transition over 0.35 seconds.

### 070. `/effectgeometricwipe` — Geometric Shape Wipe Transition

- **Role** : Clean, fresh, modern design styling (triangles, diamonds, or hexagons).
- **Kadans Composition** : An array of small rotating hexagons or triangles tiling across the screen to reveal the next scene.
- **AI Obligation** : Use an SVG mask grid expanding sequentially from the center.

### 071. `/effectlumaabsorb` — Luminance Fade Transition (Luma Fade)

- **Role** : The brightest parts of the first scene dissolve first, followed progressively by the darker areas.
- **Kadans Composition** : Transition using each pixel's black-and-white values to produce a textured fade rather than a flat cross-dissolve.
- **AI Obligation** : Apply a luma mask filter in the Kadans composition.

---

## Category G: Sound, Audio & Rhythmic Sync

### 072. `/effectaudiowaveform` — Dynamic Dancing Audio Waveform

- **Role** : Visually represent voice or music dynamics in real time.
- **Kadans Composition** : Vertical bars or curved waves oscillating according to voice frequencies at every point in the video.
- **AI Obligation** : Integrate `.audio-waveform-bars` with height animation synchronized to the audio stream.

### 073. `/effectbeatdrop` — Bass Drop Beat Synchronization

- **Role** : Trigger an explosive visual burst or scene swap precisely on the heavy bass drop.
- **Kadans Composition** : Scene change, camera shake, light flash, and title entrance locked strictly to the bass drop timestamp.
- **AI Obligation** : Align the transition point in `spec.json` to the exact second where the music drops the beat.

### 074. `/effectsubbasshit` — Deep Sub-Bass Impact (Sub-Bass Boom)

- **Role** : Convey a sense of extreme power when unveiling a major solution or logo.
- **Kadans Composition** : Heavy 30-40Hz sub-bass sound sustaining for 2 seconds, accompanied by a subtle screen shake.
- **AI Obligation** : Integrate the bass SFX into the project and schedule the visual shake at the exact same instant.

### 075. `/effectsoundwhoosh` — Fast Motion Whoosh Sound Effect

- **Role** : Give every card shift, text slide, or camera pan an authentic wind whoosh sound.
- **Kadans Composition** : Short whoosh sound synchronized with the beginning of every `translateX/Y` movement.
- **AI Obligation** : Place the whoosh sound into the `medya/sfx/` folder and trigger it on every major transition.

### 076. `/effectsoundui` — Subtle Click and Pop Sound Effects for UI Elements

- **Role** : Provide a satisfying tactile feel when a card appears, a button is clicked, or a counter increments.
- **Kadans Composition** : High-quality subtle sound effects (pop, subtle click, bell chime, soft tap).
- **AI Obligation** : Integrate UI sound effects on every card appearance, badge reveal, or checkbox toggle.

### 077. `/effectvinylwarmth` — Analog Warmth and Vinyl Crackle

- **Role** : Create a nostalgic, retro, and warm human atmosphere, ideal for jazz or lo-fi music.
- **Kadans Composition** : Vinyl record soundscape with soft, subtle crackle in the background behind the music.
- **AI Obligation** : Add the `.vinyl-crackle` audio layer at 15% volume beneath the main background music.

### 078. `/effectvoiceisolate` — Clean Voice Isolation and Auto-Ducking

- **Role** : Guarantee 100% crystal-clear vocal intelligibility without the background music overpowering the speaker.
- **Kadans Composition** : Music automatically attenuates to 20% volume whenever the voice speaks, and returns to 70% during pauses.
- **AI Obligation** : Configure the music volume curve (`volume_keyframes`) in the spec according to the voice timeline.

### 079. `/effectcrowdambience` — Crowd Ambience and Applause

- **Role** : Create the atmosphere of a major event, a successful keynote, or a packed auditorium.
- **Kadans Composition** : Soft crowd murmurs at the beginning, swelling into enthusiastic applause and cheers on victory reveals or the final CTA.
- **AI Obligation** : Place crowd sound effects in the introduction scene and the conclusion scene.

### 080. `/effectheartbeatfx` — Accelerating Heartbeat Sound & Visual Pulse for Tension

- **Role** : Build suspense and keep the audience on edge while awaiting a critical outcome or solution.
- **Kadans Composition** : Heartbeat sound effect starting slow and accelerating, accompanied by a subtle red/black flash on each pulse.
- **AI Obligation** : Synchronize the `scale(1.03) -> scale(1)` animation with every audio heartbeat pulse.

### 081. `/effectreverbtrail` — Spatial Reverb Trail on the Final Word

- **Role** : Leave the final tagline or brand name lingering in the viewer's mind long after the video ends.
- **Kadans Composition** : The voiceover's final syllable decays into an expansive spatial reverb tail while the logo gleams.
- **AI Obligation** : Apply a reverb effect to the final audio segment along with a visual fade to black.

---

## Category H: Character Animation & Rigging

### 082. `/effectstickmanrig` — 16-Bone SVG Stickman Rig with Lipsync

- **Role** : Tell a simple, engaging, and clear story using a professionally animated stick figure.
- **Kadans Composition** : Full 16-bone SVG stickman rig (head, neck, torso, arms, elbows, hands, pelvis, thighs, knees, feet) walking, jumping, pointing at the screen, and talking with WAAPI phoneme lipsync at 60 FPS.
- **AI Obligation** : Integrate the SVG Rig module with movement commands (`walk`, `jump`, `point`, `explain`).

### 083. `/effectcutout2d` — 2D Cut-Out Illustrated Character Animation

- **Role** : Modern 2D cut-out animation style where character limbs move with organic elasticity.
- **Kadans Composition** : Character divided into separate segments (arms, body, head) linked at natural pivot points with expressive facial reactions.
- **AI Obligation** : Position the character on the side of the screen interacting with the central graphics.

### 084. `/effectavatarhost` — Virtual Presenter Host in Side Frame

- **Role** : Guide the viewer throughout the video like a professional television host.
- **Kadans Composition** : Polished avatar framed in a circular badge or standing on the right edge of the screen, speaking with natural hand gestures while introducing each feature.
- **AI Obligation** : Keep the avatar docked to the side so it never obscures onscreen text or product demos.

### 085. `/effecttalkinghead` — Animated Talking Head with Word-Level Lipsync

- **Role** : Bring an illustration or character to life by synchronizing mouth shapes with the spoken words.
- **Kadans Composition** : SVG mouth transitioning across phonemes `A`, `E`, `O`, `M`, `L` based on the timestamps in the `.words.json` file.
- **AI Obligation** : Bind the character's mouth morphs to the Whisper transcription phoneme data.

### 086. `/effectemojipop` — 3D Pop-Up Emojis Around Character

- **Role** : Inject humor, emotion, and vibrant visual reactions into what the character is saying.
- **Kadans Composition** : 3D emojis (fire 🔥, rocket 🚀, heart ❤️, thinking face 🤔, money bag 💰) popping up around the character's head with a snappy bounce.
- **AI Obligation** : Trigger emojis on emotionally charged keywords.

### 087. `/effectshadowpuppet` — Shadow Puppet Silhouette Aesthetics

- **Role** : Traditional shadow puppet theater style for storytelling, cultural legends, or allegories.
- **Kadans Composition** : Characters and trees depicted in solid black silhouettes against a bright sunset backdrop of vibrant oranges and yellows.
- **AI Obligation** : Use pure black `#000000` SVG paths over a warm sunset gradient background.

### 088. `/effectmascotdance` — Celebrating Mascot Dance on Final CTA

- **Role** : Leave a joyful, engaging, and positive lasting impression on the audience.
- **Kadans Composition** : Project mascot performing a celebratory victory dance or waving at the audience alongside the final CTA button.
- **AI Obligation** : Add the `.dance-bounce` animation to the mascot during the final 5 seconds of the video.

### 089. `/effectspeechbubble` — Comic Speech Bubble with Animated Text

- **Role** : Display a character's internal thoughts or spoken dialogue in a clean comic-strip style.
- **Kadans Composition** : Crisp white speech bubble surfacing from the character's mouth with a directional pointer, displaying animated text inside.
- **AI Obligation** : Create an SVG `.speech-bubble` with a `scale(0) -> scale(1)` entrance animation.

### 090. `/effectgesturesmart` — Smart Animated Hand Gesture (Point and Click)

- **Role** : Direct viewer attention toward a high-value button, price point, or critical link.
- **Kadans Composition** : Illustrated hand gliding into view, pointing at the target element, performing a tap or swipe gesture, and smoothly fading out.
- **AI Obligation** : Deploy the `.gesture-hand` element with translate animation and a tap gesture on the target area.

### 091. `/effectcrowdsilhouette` — Bottom Crowd Silhouette Overlay

- **Role** : Simulate a massive live audience in a stadium or conference hall watching the presentation.
- **Kadans Composition** : Bottom silhouette layer of cheering heads and hands clapping or holding up smartphones to record.
- **AI Obligation** : Add `.crowd-silhouette-layer` anchored to the bottom with subtle organic sway.

---

## Category I: Narrative Sections & Story Structure

### 092. `/effecthookpunch` — Punchy 3-Second Hook

- **Role** : Prevent viewers from swiping away during the crucial opening seconds of the video.
- **Kadans Composition** : A provocative question, intense visual, shocking statement, and rapid impact sound effect within the first 3 seconds.
- **AI Obligation** : Scene 1 must be concise, punchy, visually dense, and jump straight to the point without any slow preamble.

### 093. `/effectproblemstatement` — Problem & Frustration Statement

- **Role** : Make the audience instantly recognize their own pain points and feel deeply understood.
- **Kadans Composition** : Darker color palette, tense background score, and visuals of exhausted users or bottlenecked workflows.
- **AI Obligation** : Highlight the key obstacles and friction encountered by the customer prior to finding the solution.

### 094. `/effectsolutionswitch` — The Solution Reveal & Tonal Pivot

- **Role** : Mark the pivotal transformation moment where clarity and relief are unlocked by the product.
- **Kadans Composition** : Burst of bright light, vibrant colors replacing the dark tones, and an upbeat soundtrack conveying relief and momentum.
- **AI Obligation** : Transition sharply from dark moods to luminous radiance accompanied by a bold product name reveal.

### 095. `/effectfeaturecarousel` — 3 to 5 Core Feature Carousel

- **Role** : Showcase the product's full range of capabilities with speed and absolute clarity.
- **Kadans Composition** : 3 to 5 horizontally sliding cards, each featuring a polished 3D icon, a 3-word title, and a crisp summary sentence.
- **AI Obligation** : Spend 2 to 3 seconds on each feature with a smooth slide transition in between.

### 096. `/effectsocialproof` — Customer Testimonials & 5-Star Social Proof

- **Role** : Build unshakable trust by proving real customers are already thrilled with their results.
- **Kadans Composition** : Testimonial cards with client portraits, 5 glowing gold stars (`★★★★★`), and bite-sized quotes from companies or developers.
- **AI Obligation** : Illuminate `.star-gold` elements sequentially paired with genuine user photos and names.

### 097. `/effectpricingtable` — Pricing Table with Highlighted Popular Plan

- **Role** : Help customers effortlessly choose the ideal subscription plan.
- **Kadans Composition** : 2 or 3 side-by-side pricing cards; the recommended plan stands taller with a 'MOST POPULAR' badge and a luminous neon border glow.
- **AI Obligation** : Visually prioritize the featured tier over the other pricing options.

### 098. `/effectguaranteebadge` — 100% Satisfaction Guarantee Shield Badge

- **Role** : Eliminate hesitation and purchase friction by eliminating customer risk.
- **Kadans Composition** : Polished gold and green shield with a security seal and '100% MONEY-BACK GUARANTEE' text.
- **AI Obligation** : Display the `.guarantee-shield` element popping into place with a confident slight rotation.

### 099. `/effecturgencytimer` — Urgency Countdown Timer

- **Role** : Drive immediate customer action instead of leaving the decision for later.
- **Kadans Composition** : Digital countdown clock ticking down minutes and seconds, accompanied by a 'LIMITED-TIME OFFER' tag.
- **AI Obligation** : Integrate the `.countdown-timer` component actively counting down as the scene plays.

### 100. `/effectctaultimate` — High-Impact Ultimate Call to Action (CTA)

- **Role** : Tell the viewer exactly what next step to take immediately as the video ends.
- **Kadans Composition** : Prominent glowing button emitting light pulse rings, bold high-contrast website URL, arrow pointing to the button, and direct voiceover directive.
- **AI Obligation** : Center the CTA button with the `.btn-cta-pulse` class, enlarge the link text, and configure the click action.

### 101. `/effectoutrologos` — Outro Logo and Audio Signature (Audio Brand)

- **Role** : Conclude the video with grandeur on the official brand identity.
- **Kadans Composition** : Logo rising in the center of the screen with a light sheen passing across it, slogan underneath, social media links, and the company's audio signature.
- **AI Obligation** : The final scene must be clean and calm, with the logo centered on a dark background accompanied by the closing sound.

---

## Category J: Motion Design & Motion Graphics

### 102. `/motiondesign` — Complete Professional Motion Design

- **Role** : Transform the entire video into an agency-quality motion design production (Buck / Ordinary Folk level).
- **Kadans Composition** : 12-column grid, fixed 3-4 color palette, each element enters with `cubic-bezier(0.65,0,0.35,1)` easing, subtle overshoot, 60-90 ms stagger between elements, no element remaining static for more than 1.2 s.
- **AI Obligation** : All scenes must be editable HTML/SVG vectors (not images), with a constant animation rhythm; add the `.motion-pro` class in `spec.json` and use the same easing throughout.

### 103. `/motiongraphic` — Infographic Motion Graphics

- **Role** : Explain data and ideas using animated graphics (icons, numbers, arrows, diagrams).
- **Kadans Composition** : Flat icons appearing with `scale 0→1.08→1`, self-drawing arrows (`stroke-dashoffset`), counting numbers, short text of 3-6 words per screen.
- **AI Obligation** : Every point spoken by the voice must have a corresponding graphic on screen at that exact second (sync with voice); never use long paragraphs.

### 104. `/morphism` — Vector Shape Morphing (Shape Morph)

- **Role** : Seamlessly transform one shape into another without cuts (circle → square → logo → icon).
- **Kadans Composition** : SVG `path` morphing with identical vertex counts (flubber / path interpolation), simultaneous color change, 0.6-1.2 s duration, `easeInOutQuart` easing.
- **AI Obligation** : Each transition between scenes must emerge from a shape morphing into the next element; never use a hard cut between 2 scenes using /morphism.

### 105. `/shapelayers` — Shape Layer Animation

- **Role** : Build compositions using geometric shapes that enter, rotate, and stack.
- **Kadans Composition** : Circles, rectangles, triangles, lines entering one after another (stagger), 90°/180° rotations, masks between shapes, flat solid colors without gradients.
- **AI Obligation** : Use only primitive SVG shapes; each shape must be a separate layer in the spec so the developer can edit it.

### 106. `/liquidmotion` — Liquid & Blob Motion

- **Role** : Give the video an organic, soft, liquid feel.
- **Kadans Composition** : Deforming SVG blob (filter `feTurbulence` + `feDisplacementMap` or morph path), merging droplets (gooey effect), smooth 4-8 s looped movement.
- **AI Obligation** : Do not use sharp corners; all shapes must feature smooth curves; combine with /gradientmotion if gradients are used.

### 107. `/linedraw` — Self-Drawing Line (Stroke Draw)

- **Role** : Display illustrations, maps, or logos drawing themselves before the viewer's eyes.
- **Kadans Composition** : `stroke-dasharray` + `stroke-dashoffset` animated from 100% → 0, constant line weight, fill appearing AFTER the stroke completes (0.3 s fade).
- **AI Obligation** : All drawings must be SVG paths; drawing order follows natural logic (from top-left → to bottom-right) or the voiceover.

### 108. `/flatmotion` — Animated 2D Flat Design

- **Role** : Modern flat illustration style (Kurzgesagt / startup explainer quality).
- **Kadans Composition** : Flat colors, 45° long shadows, no textures, clean characters and objects, subtle bouncy motion.
- **AI Obligation** : Maximum 5-color palette; all elements strictly vector; maintain identical line weight throughout the video.

### 109. `/isomotion` — Isometric Motion

- **Role** : Display systems, cities, offices, or processes in a 30° isometric perspective.
- **Kadans Composition** : Isometric grid, blocks falling or rising into position, miniature characters and vehicles moving along isometric paths, static camera.
- **AI Obligation** : Strictly respect the exact 30° angle (`transform: rotateX(60deg) rotateZ(45deg)` or isometric SVG); never blend with standard perspective.

### 110. `/logoreveal` — Motion Logo Reveal

- **Role** : Reveal the logo with impactful presence at the beginning or end.
- **Kadans Composition** : Opening mask, particles converging to assemble the logo, or lines drawing it; subtle light flash + whoosh, 2-3 s duration.
- **AI Obligation** : Always use the client's ORIGINAL logo (SVG if available); never distort its aspect ratio; sync whoosh/impact sound to the exact moment it completes.

### 111. `/logoanimation` — Full Animated Logo (Build-up)

- **Role** : Deconstruct the logo into individual pieces and rebuild it through animation.
- **Kadans Composition** : Each logo part (symbol, letters, slogan) enters separately, bounces, and settles into place; optional 3-5 s loop.
- **AI Obligation** : Split the logo into SVG layers; also export a short 1.5 s version for social media openers.

### 112. `/iconmotion` — Animated Icons (Micro-animation)

- **Role** : Breathe life into every icon (ringing bell, beating heart, drawing checkmark).
- **Kadans Composition** : Short 0.4-0.8 s animation, motion that aligns naturally with the icon's meaning, stroke + fill.
- **AI Obligation** : Each icon must have an animation tailored to its meaning; never use the same generic animation for all.

### 113. `/datamotion` — Animated Data Charts (Bar, Pie, Line)

- **Role** : Bring figures to life through dynamic, growing charts.
- **Kadans Composition** : Bars rising from 0, curves drawing out, pie charts filling up, value labels counting up simultaneously, clean axes.
- **AI Obligation** : Data must be REAL (provided by the developer or the source); do not fabricate numbers; show the source in small text at the bottom.

### 114. `/countermotion` — Animated Number Counter

- **Role** : Highlight a critical number (clients, sales, %, price).
- **Kadans Composition** : Large numbers (120-200 px), counting from 0 to the target value with `easeOutExpo` easing, unit/syntax appearing afterwards, subtle pulse at the end.
- **AI Obligation** : The count must resolve on a crisp 'tick'/impact sound; format numbers according to language conventions (1 000 / 1,000).

### 115. `/explainer` — Motion Explainer Video

- **Role** : Classic explainer structure: problem → how it works → benefits → CTA.
- **Kadans Composition** : 4-6 s scenes each, flat characters, icons, arrows, clear voiceover, light optimistic music.
- **AI Obligation** : Strictly follow the 4-part structure; one single idea per scene; ElevenLabs voiceover with subtitles.

### 116. `/lowerthirdpro` — Professional Motion Lower Third

- **Role** : Introduce names, titles, or lower-screen contextual information.
- **Kadans Composition** : Sliding color bar + text revealed with mask, left alignment, 3-5 s on-screen duration, reverse-motion exit.
- **AI Obligation** : Never cover the subject's face; strictly respect the 5% safe margins at the bottom and sides.

### 117. `/titlesequence` — Cinematic Title Sequence

- **Role** : Create an opening title sequence reminiscent of a television series or movie.
- **Kadans Composition** : Large, creative typography aligned with the subject, consecutive title scenes set to rhythmic music, cuts on the beats.
- **AI Obligation** : Include project name, creators, and a final title card; sync each cut with the musical beat (/effectbeatdrop if available).

### 118. `/swisstype` — Swiss Typography / Grid Motion

- **Role** : Swiss graphic style: strict grid, grotesque typography, flawless alignment.
- **Kadans Composition** : Sans-serif font (Inter / Helvetica-like), text blocks aligned to grid, restricted palette (black, white, red), linear sliding motion.
- **AI Obligation** : No useless ornamentation; every motion must follow the grid precisely.

### 119. `/bouncemotion` — Elastic Bounce (Squash & Stretch)

- **Role** : Give objects a playful character using the 12 principles of animation.
- **Kadans Composition** : Squash & stretch upon impact, anticipation before movement, follow-through, elastic easing `easeOutElastic`.
- **AI Obligation** : Use for lightweight objects and playful tones; do not apply to serious copy or financial data.

### 120. `/maskreveal` — Mask Reveal

- **Role** : Reveal text and images from behind a sliding mask.
- **Kadans Composition** : `clip-path` or moving SVG mask, text rising from beneath an invisible line, image revealed via strips.
- **AI Obligation** : All reveals within the same scene must maintain a consistent direction.

### 121. `/splitscreen` — Animated Split Screen

- **Role** : Display 2-4 elements simultaneously (comparisons, multiple products, multiple people).
- **Kadans Composition** : Panels separated by animated lines, each panel entering with a staggered delay, moving divider dynamically shifting proportions.
- **AI Obligation** : Each panel must remain legible on mobile; no more than 4 panels.

### 122. `/loopmotion` — Seamless Loop Animation

- **Role** : Create an animation that can loop endlessly without visible seams (GIFs, backgrounds, social media).
- **Kadans Composition** : First and last frames identical, cyclical movement (360° rotation, wave, pulsation), 2-8 s duration.
- **AI Obligation** : Verify that frame 0 = final frame; set `loop: true` in the spec.

### 123. `/3dmotion` — CSS 3D Motion (Perspective)

- **Role** : Add depth with cards, text blocks, and screens rotating in 3D space.
- **Kadans Composition** : `perspective: 1200px`, `rotateY/rotateX`, flipping cards, camera moving through depth, reactive dynamic shadows.
- **AI Obligation** : Stay legible: do not rotate text beyond 35° during reading.

### 124. `/gradientmotion` — Animated Mesh Gradient

- **Role** : Living, dynamic gradient background smoothly drifting over time.
- **Kadans Composition** : 3-5 color mesh gradient moving across positions (animated positions), heavy blur, light film grain on top.
- **AI Obligation** : Contrast against overlaid text must strictly remain ≥ 4.5:1 at all times.

### 125. `/halftonemotion` — Halftone & Retro Print Motion

- **Role** : Retro print style (halftone dots, vintage comic books, retro posters) in motion.
- **Kadans Composition** : SVG halftone pattern, CMYK color offset misregistration, paper texture, 12 fps 'stop-motion' animation cadence.
- **AI Obligation** : Operate at a 12 fps frame rate for the components, while ensuring the final export is rendered at 60 FPS.

### 126. `/uimotion` — Product UI Animation (App Walkthrough)

- **Role** : Show how an app or software works with clean interface animations.
- **Kadans Composition** : Clicking cursor/finger, sliding screens, appearing UI elements, zoom on key areas, device mockup (/effectdeviceframe).
- **AI Obligation** : Use real captures or a real UI reconstructed in HTML; do not invent non-existent features.

---

## Category K: Advertising & Professional Commercials

### 127. `/pubstore` — Store / Shop Commercial (Retail Promo)

- **Role** : Promote a retail store, shop, or supermarket.
- **Kadans Composition** : Products appearing on animated shelves, dropping prices and price tags, address + hours, store logo, CTA 'Visit today'.
- **AI Obligation** : Display prices and discounts in LARGE text; local contact details (address, phone, WhatsApp) mandatory in the final scene.

### 128. `/zoommap` — Map Zoom (Location Map Zoom)

- **Role** : Show where a business, event, or location is situated.
- **Kadans Composition** : Map zooming from country view → city → neighborhood → dropping bouncing pin, drawn route, location name tag.
- **AI Obligation** : Use SVG/OpenStreetMap maps (no copyrighted Google Maps captures without attribution); the pin must match the brand colors.

### 129. `/pubproduct` — Hero Product 360°

- **Role** : Spotlight a product as the centerpiece of the ad.
- **Kadans Composition** : Centered product on a clean background, rotation/parallax, rim lighting, features popping up with callout lines pointing to parts.
- **AI Obligation** : The product must occupy at least 50% of the screen in the main scene; do not distort the product's actual colors.

### 130. `/pubfood` — Restaurant & Food Commercial

- **Role** : Whet the appetite: restaurants, fast food, bakeries.
- **Kadans Composition** : Food close-ups, rising steam, drizzling sauce, slow motion, warm colors, sizzling/cooking sound design.
- **AI Obligation** : Warm color palette (red, yellow, orange); include menu / prices / delivery options at the end.

### 131. `/pubrealestate` — Real Estate Commercial

- **Role** : Showcase houses, apartments, or land for sale/rent.
- **Kadans Composition** : Drone/exterior aerial shots, room-by-room walkthrough, bedroom/bathroom/sq ft icons, location map, pricing.
- **AI Obligation** : Sequence: exterior → main rooms → details → map → price + agent contact info.

### 132. `/pubcar` — Automotive / Car Commercial

- **Role** : Commercial for vehicles, car dealerships, auto parts, or repair shops.
- **Kadans Composition** : Dynamic camera movement, light reflections across bodywork, speed, engine roar, bold typography.
- **AI Obligation** : Specify model, year, pricing, or financing offers; preserve the vehicle's authentic paint color.

### 133. `/pubfashion` — Fashion & Apparel Commercial

- **Role** : Commercial for clothing stores, footwear, accessories, and fashion collections.
- **Kadans Composition** : Cuts on the beat, editorial typography, rapid succession of looks, flash transitions, trending soundtrack.
- **AI Obligation** : Fast-paced rhythm (0.5–1s per shot) synced to the music; collection name + shop link at the end.

### 134. `/pubbeauty` — Cosmetics & Beauty Commercial

- **Role** : Commercial for beauty products, salons, and spas.
- **Kadans Composition** : Macro cream textures, water droplets, soft lighting, pastel/gold tones, glowing skin.
- **AI Obligation** : Elegant, serene tone; make no unsubstantiated medical claims.

### 135. `/pubtech` — Tech / Gadget Commercial

- **Role** : Commercial for phones, computers, gadgets, and tech services.
- **Kadans Composition** : Dark background, neon blue/purple lighting, detail zooms, tech specs appearing with callout lines.
- **AI Obligation** : Specifications must be authentic; include pricing + where to buy.

### 136. `/pubapp` — Mobile App Commercial (App Promo)

- **Role** : Drive mobile app downloads.
- **Kadans Composition** : 3D smartphone mockup running the app UI, 3 core features, App Store / Google Play badges, QR code.
- **AI Obligation** : Show genuine app UI screens; conclude with store badges + CTA 'Download now'.

### 137. `/pubevent` — Event / Concert Commercial

- **Role** : Promote concerts, festivals, conferences, or fairs.
- **Kadans Composition** : Artist/speaker names, large date & time display, venue location (/zoommap if needed), countdown timer, energetic music.
- **AI Obligation** : Date, time, location, ticket prices, and ticketing link = mandatory.

### 138. `/pubflashsale` — Flash Sale / Percentage Promo

- **Role** : Create urgency for a limited-time promotional offer.
- **Kadans Composition** : Large discount percentage (-50%), strikethrough original price, countdown timer, red/yellow palette, vibrating/pulsing text.
- **AI Obligation** : State the promo expiration date; before and after prices must be clearly visible.

### 139. `/pubblackfriday` — Black Friday / Mega Discounts

- **Role** : Dedicated commercial for Black Friday, Cyber Monday, and year-end sales.
- **Kadans Composition** : Deep black backdrop, bold gold/white typography, light flashes, explosive discount bursts, product showcase with prices.
- **AI Obligation** : Premium yet urgent tone; event dates are mandatory.

### 140. `/pubbank` — Banking & Fintech Commercial

- **Role** : Commercial for banks, money transfers, payment apps, and microfinance.
- **Kadans Composition** : Trust-inducing color palette (blue, green), 3D bank card, growth charts, security badges, smiling customers.
- **AI Obligation** : Legal disclaimers / terms in small print whenever interest rates or fees are mentioned.

### 141. `/pubhealth` — Healthcare / Clinic Commercial

- **Role** : Commercial for clinics, pharmacies, hospitals, and healthcare services.
- **Kadans Composition** : Clean white/blue/green palette, medical icons, smiling healthcare team, service breakdown, emergency contact info.
- **AI Obligation** : Never make guarantees of a cure; ensure clear, legible contact information.

### 142. `/pubschool` — Education & Training Commercial

- **Role** : Commercial for schools, universities, professional training, and online courses.
- **Kadans Composition** : Engaged students, book/diploma icons, curriculum lists, enrollment deadlines, testimonials.
- **AI Obligation** : Registration deadline + contact info are mandatory.

### 143. `/pubtravel` — Travel & Tourism Commercial

- **Role** : Commercial for travel agencies, hotels, and tourist destinations (Haiti, Caribbean…).
- **Kadans Composition** : Scenic landscape shots, airplane tracing flight path on map (/zoommap), package prices, featured activities.
- **AI Obligation** : Display 'starting from' pricing + travel dates; show genuine landscapes of the actual destination.

### 144. `/pubrestaurantmenu` — Animated Digital Menu (Menu Board)

- **Role** : Digital menu board display for restaurants (in-store TV screens).
- **Kadans Composition** : Columns of items + prices, rotating dishes in sequence, featured daily special/promotion, 15–30s loop.
- **AI Obligation** : 16:9 or vertical 9:16 format; prices legible from 3 meters away; automatic /loopmotion.

### 145. `/pubtestimonial` — UGC Testimonial Commercial

- **Role** : Customer testimonial ad (social media UGC style).
- **Kadans Composition** : Vertical 9:16 framing, customer face, word-by-word dynamic subtitles, 5-star rating, product in-frame.
- **AI Obligation** : Testimonials must be GENUINE (supplied by the developer); never fabricate fictitious clients.

### 146. `/pubbeforeafter` — Before / After

- **Role** : Demonstrate the tangible results of a product or service.
- **Kadans Composition** : Split screen with sliding wipe bar, BEFORE/AFTER labels, perfectly aligned identical framing for both images.
- **AI Obligation** : Both images must share the exact same camera angle and lighting; do not fabricate or alter the results.

### 147. `/pubunboxing` — Product Unboxing

- **Role** : Unbox the product packaging on camera.
- **Kadans Composition** : Box opening, illuminated product reveal, unboxing components one by one, crisp ASMR paper/packaging sound design.
- **AI Obligation** : Show all box contents; conclude with pricing + where to buy.

### 148. `/pubbumper` — 6-Second Bumper Ad

- **Role** : Short, punchy ad tailored for YouTube bumper ads / Stories.
- **Kadans Composition** : 1 single message, logo, CTA — EXACT 6s duration, hook within the first 1s.
- **AI Obligation** : Maximum duration of 6.0s; single focal idea; logo visible throughout or on the end card.

### 149. `/pubtv30` — 30-Second TV Spot

- **Role** : Classic 30-second television / visual radio commercial.
- **Kadans Composition** : Structure: hook (3s) → problem (5s) → solution (12s) → proof (5s) → CTA + logo (5s).
- **AI Obligation** : Exact 30s duration; 16:9 1080p format; -23 LUFS broadcast audio loudness standard.

### 150. `/pubbillboard` — Billboard / DOOH Digital Screen

- **Role** : Advertising for digital out-of-home screens (DOOH), shopping malls, and airports.
- **Kadans Composition** : 5–7 word maximum message, bold display typography, high contrast, 8–15s soundless loop.
- **AI Obligation** : Must not rely on audio; readable from afar; aspect ratio matched to screen specs (portrait or landscape).

### 151. `/pubjingle` — Jingle & Brand Sound

- **Role** : Create the brand's audio signature in the commercial.
- **Kadans Composition** : Jingle 3-5 s, sung or spoken slogan (ElevenLabs), logo sound, sync with the logo animation.
- **AI Obligation** : Use ElevenLabs for voice/sfx; the jingle must be repeated at the end of each ad (/effectoutrologos).

---

## Category L: Visual Transitions & Audio Transitions

### 152. `/zoomin` — Zoom In

- **Role** : Enter the next scene via an advancing zoom in.
- **Kadans Composition** : Kadans: `"transition": "zoom"` on the incoming scene; duration 0.4-0.6 s; easing `inout`.
- **AI Obligation** : Every cut between scenes featuring /zoomin MUST have `"transition": "zoom"`; set `"skills": ["/zoomin"]` on these scenes.

### 153. `/zoomout` — Zoom Out

- **Role** : Exit a scene as if the camera is pulling back.
- **Kadans Composition** : Kadans: `"transition": "zoomout"`; duration 0.4-0.7 s.
- **AI Obligation** : Use exact `"transition": "zoomout"`; do not replace with fade.

### 154. `/spiral` — Spiral (Spin + Zoom)

- **Role** : The scene spins in a spiral during entrance/exit.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes: `rotate(0→720deg)` + `scale(1→0.1)` on exiting scene, inverse on incoming scene; duration 0.8 s; or `"transition": "rotate"` + zoom if the scene is not html.
- **AI Obligation** : Rotation must be at least 360°; set `"skills": ["/spiral"]` on the transition scene.

### 155. `/whippan` — Whip Pan (Fast Pan)

- **Role** : The camera whips sideways with motion blur between 2 scenes.
- **Kadans Composition** : Kadans: `"transition": "slide"` + `"blur"` (motion_blur enabled) or scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes `translateX(-120%)` + `filter: blur(18px)`; duration 0.25-0.35 s; whoosh sound (`sfx.whoosh: true`).
- **AI Obligation** : Duration ≤ 0.35 s; whoosh mandatory on the cut.

### 156. `/spinblur` — Spin Blur

- **Role** : Fast rotational transition with blur.
- **Kadans Composition** : Kadans: `"transition": "rotate"` with `"motion_blur"` enabled; duration 0.4 s.
- **AI Obligation** : Rotation + blur combined; not a dry rotate.

### 157. `/crossfade` — Crossfade

- **Role** : Smooth, classic, calm transition.
- **Kadans Composition** : Kadans: `"transition": "fade"`; duration 0.6-1.0 s.
- **AI Obligation** : Use for emotional / documentary tone; not for fast-paced ads.

### 158. `/dipblack` — Dip to Black

- **Role** : Close one chapter and open another.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes with `#000` background ramping 0→1 (0.3 s), holding for 0.2 s, decreasing (0.3 s); or short scene `background: #000` 0.4 s with `"transition": "fade"`.
- **AI Obligation** : The screen must become completely BLACK for at least 0.15 s.

### 159. `/dipwhite` — Dip to White / Flash

- **Role** : Bright transition evoking dreams, memories, or burst of energy.
- **Kadans Composition** : Kadans: same as /dipblack but with `#fff`; total duration 0.5-0.8 s.
- **AI Obligation** : The screen must become completely WHITE for at least 1 frame.

### 160. `/slideleft` — Push Left

- **Role** : The next scene pushes the previous one to the left.
- **Kadans Composition** : Kadans: `"transition": "slide"`; duration 0.4-0.5 s.
- **AI Obligation** : Exact value `slide`; consistent direction across the entire series.

### 161. `/slideright` — Push Right

- **Role** : The next scene enters from the left.
- **Kadans Composition** : Kadans: `"transition": "slideright"`.
- **AI Obligation** : Exact value `slideright`.

### 162. `/slideup` — Push Up

- **Role** : Vertical transition (Reel / TikTok style).
- **Kadans Composition** : Kadans: `"transition": "slideup"`; ideal for 9:16.
- **AI Obligation** : Exact value `slideup`.

### 163. `/slidedown` — Push Down

- **Role** : Vertical downward transition.
- **Kadans Composition** : Kadans: `"transition": "slidedown"`.
- **AI Obligation** : Exact value `slidedown`.

### 164. `/wipeline` — Line Wipe

- **Role** : A line sweeps across the screen and reveals the next scene.
- **Kadans Composition** : Kadans: `"transition": "wipe"` (horizontal) or `"wipeup"` (vertical); brand-colored line along the edge (html).
- **AI Obligation** : Exact `wipe`/`wipeup` value; line in brand color if a brand is specified.

### 165. `/circlereveal` — Circle Reveal

- **Role** : A circle expanding from a point to reveal the scene.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes `clip-path: circle(0% at X Y) → circle(150% at X Y)`; duration 0.6 s; centered on the subject.
- **AI Obligation** : The center of the circle must be on the important subject, not in the center by default.

### 166. `/irisclose` — Iris Close (Vintage Film Style)

- **Role** : Circle closing in on a detail (classic ending, comedy).
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes `clip-path: circle(150%) → circle(0%)` over black background; duration 0.8 s.
- **AI Obligation** : Close on the final detail (face, logo).

### 167. `/cubeflip` — 3D Cube (Cube Rotate)

- **Role** : 2 scenes on 2 faces of a rotating cube.
- **Kadans Composition** : Kadans: `"transition": "flip"` or scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes `perspective: 1200px` + `rotateY(-90deg)` across 2 faces; duration 0.7 s.
- **AI Obligation** : 3D effect must be visible (perspective), not a flat flip.

### 168. `/pageturn` — Page Turn

- **Role** : Transition like a turning book page.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes `rotateY(0→-180deg)` with `transform-origin: left` + shadow; sound `sfx:book-flip`.
- **AI Obligation** : Sound `sfx:book-flip` mandatory when the page turns.

### 169. `/lightleak` — Light Leak

- **Role** : Warm organic light flash between 2 scenes.
- **Kadans Composition** : Kadans: orange/pink gradient overlay `mix-blend-mode: screen` traversing (0.8 s) + `"transition": "fade"`.
- **AI Obligation** : Warm colors; transparent overlay, not a solid color block.

### 170. `/filmburn` — Film Burn

- **Role** : Vintage transition like burning film stock.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes with expanding orange/white spots (radial-gradient + blur) + grain; duration 0.8-1 s.
- **AI Obligation** : Film grain + warm colors mandatory.

### 171. `/pixelate` — Pixelate

- **Role** : The scene pixelates and reassembles into the next one.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes (canvas or `image-rendering: pixelated` + scale), blocks 4→48 px→4; duration 0.6 s.
- **AI Obligation** : Pixels must be clearly visible in the middle of the transition.

### 172. `/rgbsplit` — RGB Split (Chromatic Aberration)

- **Role** : Red/green/blue channels separate for a tech cut.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes with 3 copies using `mix-blend-mode: screen` shifted ±8 px; duration 0.3 s; sound `sfx.hit`.
- **AI Obligation** : Visible displacement of all 3 colors; short duration.

### 173. `/glitchcut` — Glitch Cut

- **Role** : Sharp cut with digital glitch.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes with shifting bands (`clip-path` + random translateX), 6-10 frames; sound /soundglitch.
- **AI Obligation** : Duration 0.2-0.4 s; stack with /soundglitch if sound is active.

### 174. `/shatter` — Screen Shatter

- **Role** : The scene shatters into glass pieces.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes with polygon `clip-path` (12-20 pieces) falling with rotation; sound `sfx:impact-glass`.
- **AI Obligation** : Sound `sfx:impact-glass` mandatory.

### 175. `/liquidmelt` — Liquid Melt

- **Role** : The scene melts like liquid.
- **Kadans Composition** : Kadans: scene `type: "html"` (CSS @keyframes / WAAPI, 60 FPS) executing transition between the 2 scenes with SVG `feTurbulence` + `feDisplacementMap` (scale 0→80→0); duration 0.8 s.
- **AI Obligation** : Visible organic distortion; not a fade.

### 176. `/ripple` — Water Ripple

- **Role** : Waves propagating outward from a point like a stone dropped in water.
- **Kadans Composition** : Kadans: `type: "html"` scene (CSS @keyframes / WAAPI, 60 FPS) executing the transition between 2 scenes via animated radial displacement; duration 0.8 s.
- **AI Obligation** : Waves must originate from a specific point (click / subject).

### 177. `/swirl` — Swirl

- **Role** : The scene twists into a dynamic swirl.
- **Kadans Composition** : Kadans: `type: "html"` scene (CSS @keyframes / WAAPI, 60 FPS) executing the transition between 2 scenes (canvas / WebGL swirl or `rotate` + `blur` + scale); duration 0.7 s.
- **AI Obligation** : Twisting distortion clearly visible.

### 178. `/kaleidoscope` — Kaleidoscope

- **Role** : Psychedelic symmetrical mirror transition.
- **Kadans Composition** : Kadans: `type: "html"` scene (CSS @keyframes / WAAPI, 60 FPS) executing the transition between 2 scenes using 6-8 copies with triangle `clip-path` + rotation; duration 1 s.
- **AI Obligation** : Use for music / events; clearly visible symmetry.

### 179. `/stretchwarp` — Stretch Warp

- **Role** : The scene stretches in the direction of motion.
- **Kadans Composition** : Kadans: `type: "html"` scene (CSS @keyframes / WAAPI, 60 FPS) executing the transition between 2 scenes via `scaleX(1→4)` + `blur` on the outgoing scene, inverse on the incoming scene; duration 0.35 s; whoosh.
- **AI Obligation** : Whoosh mandatory (`sfx.whoosh: true`).

### 180. `/blinds` — Venetian Blinds

- **Role** : Horizontal slats rotating to reveal the scene.
- **Kadans Composition** : Kadans: `type: "html"` scene (CSS @keyframes / WAAPI, 60 FPS) executing the transition between 2 scenes with 8-12 strips `rotateX(90→0deg)` in a 30 ms stagger.
- **AI Obligation** : Visible stagger effect between strips.

### 181. `/checkerboard` — Checkerboard

- **Role** : Squares appearing sequentially like a checkerboard.
- **Kadans Composition** : Kadans: `type: "html"` scene (CSS @keyframes / WAAPI, 60 FPS) executing the transition between 2 scenes with an 8×6 square grid `scale(0→1)` in diagonal stagger.
- **AI Obligation** : Diagonal stagger mandatory.

### 182. `/splitreveal` — Split Screen Reveal

- **Role** : The scene splits in two (like doors) to reveal the next one.
- **Kadans Composition** : Kadans: `type: "html"` scene (CSS @keyframes / WAAPI, 60 FPS) executing the transition between 2 scenes with 2 halves `translateX(∓100%)`; optional `sfx:door-open` sound.
- **AI Obligation** : Both halves must move in opposite directions.

### 183. `/matchcut` — Match Cut

- **Role** : Cut between 2 similar shapes or movements (circle → moon).
- **Kadans Composition** : Kadans: `"transition": "none"` but subject position/shape is IDENTICAL in the last frame of scene A and the first frame of scene B.
- **AI Obligation** : Shape, size, and position must match; explain in the report which elements correspond.

### 184. `/smashcut` — Smash Cut

- **Role** : Abrupt cut from calm to noise (or vice versa) for comedic or shock effect.
- **Kadans Composition** : Kadans: `"transition": "none"`; sound abruptly cut or sharply increased; total contrast between the 2 scenes.
- **AI Obligation** : NO smooth transition; brutal audio shift.

### 185. `/speedramp` — Speed Ramp

- **Role** : Video slows down then accelerates (or vice versa) near the cut.
- **Kadans Composition** : Kadans: `"speed"` on video scenes (e.g. 1 → 0.3 → 2) + `"transition": "zoom"`; whoosh.
- **AI Obligation** : Use Kadans's `speed` key; only on scenes containing real video footage.

### 186. `/brushstroke` — Brush Stroke Reveal

- **Role** : Brush stroke painting the next scene.
- **Kadans Composition** : Kadans: `type: "html"` scene (CSS @keyframes / WAAPI, 60 FPS) executing the transition between 2 scenes via an SVG brush mask (`stroke-dashoffset`) revealing the scene; sound `sfx:paint-brush`.
- **AI Obligation** : Sound `sfx:paint-brush` mandatory.

### 187. `/soundhot` — Hot Hit / Sizzle Sound

- **Role** : Warm, energetic punch sound on the cut (products, food, commercials).
- **Kadans Composition** : Kadans: `sfx.hit: true` + ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "sizzle hot impact, short punchy"; volume -6 dB.
- **AI Obligation** : The sound must land EXACTLY on the cut (`at` = transition time).

### 188. `/soundepic` — Cinematic Epic Boom

- **Role** : Massive cinematic boom for key moments (revelation, logo, title).
- **Kadans Composition** : Kadans: ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "epic cinematic boom with deep sub and reverb tail" + background `sfx:thunder`; voice ducking.
- **AI Obligation** : Use 1-3 times maximum per video; reserved for major reveals.

### 189. `/soundtyping` — Keyboard Typing Sound

- **Role** : Keyboard typing sound as text appears.
- **Kadans Composition** : Kadans: `sfx.type: true` (keystroke sound on each letter) + `sfx.text: true`; synced with /effecttypewriter.
- **AI Obligation** : Each displayed letter = one click; do not play sound when no text is being typed.

### 190. `/soundriser` — Tension Riser

- **Role** : Sound building up tension before a big moment.
- **Kadans Composition** : Kadans: ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "cinematic riser 2 seconds building tension"; ends EXACTLY on the cut.
- **AI Obligation** : The end of the riser = the cut / the drop.

### 191. `/sounddrop` — Bass Drop

- **Role** : Heavy bass drop following a riser or upon revelation.
- **Kadans Composition** : Kadans: `sfx.hit: true` + ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "deep bass drop impact"; stacked with /effectbeatdrop.
- **AI Obligation** : Sync with a strong visual change.

### 192. `/soundboom` — Impact Boom

- **Role** : Heavy impact punch on titles, numbers, or logos.
- **Kadans Composition** : Kadans: `"sounds": [{"src": "sfx:impact-metal"}]` or `sfx:impact-wood` + `sfx.hit: true`.
- **AI Obligation** : Trigger on each major title / large number hitting the screen.

### 193. `/soundglitch` — Digital Glitch Sound

- **Role** : Choppy digital noise for tech/glitch transitions.
- **Kadans Composition** : Kadans: ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "digital glitch stutter short"; duration 0.2-0.4 s.
- **AI Obligation** : Always combined with a visual glitch effect (/glitchcut, /effectglitchtext…).

### 194. `/soundcamera` — Camera Shutter

- **Role** : Camera shutter sound for image changes / slideshows.
- **Kadans Composition** : Kadans: ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "camera shutter click" + short /dipwhite flash.
- **AI Obligation** : One shutter click per photo displayed.

### 195. `/soundpop` — Graphic Pop

- **Role** : Subtle pop sound for appearing elements (icons, speech bubbles, chips).
- **Kadans Composition** : Kadans: `sfx.pop: true` or `sfx:cartoon-pop`.
- **AI Obligation** : One pop sound per appearing element; low volume (-12 dB) to avoid fatigue.

### 196. `/soundswipe` — Fast Swipe / Swoosh

- **Role** : Sliding sound for slides, whip pans, and cards.
- **Kadans Composition** : Kadans: `sfx.whoosh: true` (on each transition) or `sfx:cloth` for smooth sliding.
- **AI Obligation** : Every slide/whip transition must include the swoosh.

### 197. `/soundreverse` — Reverse Swell Sound

- **Role** : Reverse swelling sound leading into the cut (reverse cymbal).
- **Kadans Composition** : Kadans: ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "reverse cymbal swell 1.5 seconds"; ends on the cut.
- **AI Obligation** : The end of the sound must match the cut moment exactly.

### 198. `/soundmagic` — Magic Sound (Shimmer)

- **Role** : Sparkling shimmer sound for reveals, transformations, before/after.
- **Kadans Composition** : Kadans: `"sounds": [{"src": "sfx:magic-sparkle"}]`.
- **AI Obligation** : Sync with appearing particles / light.

### 199. `/soundcash` — Cash Register / Coin Sound

- **Role** : Sound for prices, discounts, sales, fintech.
- **Kadans Composition** : Kadans: `"sounds": [{"src": "sfx:coins"}]` + ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "cash register ka-ching".
- **AI Obligation** : Trigger on each displayed price / discount.

### 200. `/soundtapestop` — Tape Stop

- **Role** : Music slows down and halts like a cassette tape (comedic / shock effect).
- **Kadans Composition** : Kadans: ElevenLabs SFX (was_voice_engine sfx) saved in `medya/son/`, then `"sounds": [{"src": "medya/son/<non>.mp3", "at": <s>}]` with prompt "tape stop slow down effect"; cut the music (`music` fade 0.1 s) at the exact same moment.
- **AI Obligation** : The music MUST genuinely stop after the effect.

### 201. `/soundsilence` — Dramatic Silence

- **Role** : Mute all audio for 0.5-1.5 s before a major reveal.
- **Kadans Composition** : Kadans: music `fade` → 0 and voice paused, no sfx during silence, followed by /soundepic or /sounddrop afterwards.
- **AI Obligation** : Silence must be total (music + sfx); no more than 1.5 s.

---
