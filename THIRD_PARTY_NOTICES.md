# Third-party notices — KADANS WASDEV VIDEO ENGINE

**Kadans WASDEV** (© 2026 **GRAN LAKU COMPANY** · **Getho Guerrier**) is free and open-source software released under the **MIT License** (see [`LICENSE`](LICENSE) and [`LICENSE.txt`](LICENSE.txt)).

Kadans has **no required Python dependencies**: the core package uses only the Python standard library.
**No GPL component is ever selected, imported, or distributed with Kadans WASDEV.** Automatic compliance verification is enforced by [`tools/check_licenses.py`](tools/check_licenses.py) and [`tests/test_license_policy.py`](tests/test_license_policy.py) before every release and pull request (see [`DOCS/06_LICENCES_ET_DISTRIBUTION.md`](DOCS/06_LICENCES_ET_DISTRIBUTION.md)).

## External programs used at runtime (not distributed in this repository)

| Program | Used for | License | Notes |
|---|---|---|---|
| [FFmpeg (LGPL build)](https://ffmpeg.org) | probing and cutting clips, encoding MP4, mixing sound, generating music | LGPL-2.1+ / LGPL-3.0 (configured **without** `--enable-gpl`, `libx264` or `libx265`) | **Not distributed with Kadans.** `kadans setup` downloads an official LGPL build (`github.com/BtbN/FFmpeg-Builds`, verified by SHA-256 checksums) into Kadans' user cache folder, and runs it as a separate subprocess. Hardware GPU encoders (`h264_mf`, `h264_nvenc`, `h264_amf`, `h264_qsv`, `h264_videotoolbox`, `h264_vaapi`), Cisco `libopenh264` (BSD-2-Clause) or native `mpeg4` (LGPL) are used. GPL encoders (`libx264`, `libx265`, `libxvid`) are strictly blocked by `FORBIDDEN_ENCODERS`. |
| Microsoft Edge / Google Chrome / Chromium (`chrome-headless-shell`) | capturing frames of the HTML composition (headless, private temporary profile) | Proprietary (Edge, Chrome) / BSD-3-Clause (Chromium) | **Not distributed in the package.** `kadans setup` downloads Google's *chrome-headless-shell* (Chrome for Testing, BSD-3-Clause license, with its `LICENSE.headless_shell` preserved next to it) into Kadans' user cache folder; otherwise the browser already installed on the machine is used. |
| [Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) (Daniel S. Wolf) | mouth shapes of `lipsync` scenes from the voice WAV (phonetic recognizer, any language) | MIT (bundles CMU PocketSphinx, BSD-style) | **Not distributed with Kadans.** Point `KADANS_RHUBARB` to `rhubarb.exe` or put `rhubarb` on the `PATH`. Without it, mouth shapes are estimated from the words. |
| [PySide6 / Qt WebEngine](https://doc.qt.io/qtforpython/) | optional fallback browser when no Edge / Chrome is installed (`kadans.qt_host`) | LGPL-3.0 | Optional, not installed or distributed by Kadans. |

## Optional Python packages (`pip install "kadans-wasdev[blend]"`)

| Component | License | Purpose |
|---|---|---|
| `NumPy` | BSD-3-Clause | Pixel-by-pixel compositing for the 10 advanced blend modes not natively supported by browsers |
| `Pillow` | MIT-CMU (HPND) | Image buffer decoding / encoding for advanced blend modes |

## Used by host applications (not part of Kadans)

Kadans calls a pluggable text-to-speech callable and (optionally) a word-timing callable provided by the host application (such as **WASDEV IDE**):

| Program | Used for | License |
|---|---|---|
| faster-whisper / Whisper (OpenAI) models | word timing of the voice lines | MIT |

Fonts are the ones installed on the machine (by default Segoe UI and the system emoji font); no proprietary font file is shipped.

## Bundled animation libraries (`kadans/assets/vendor/`) — all MIT

Vendored locally so renders stay 100% offline (no CDN). Each is MIT-licensed (commercial use + redistribution permitted):

- **anime.js** 3.2.1 — MIT — https://github.com/juliangarnier/anime
- **Chart.js** 4.4.1 — MIT — https://github.com/chartjs/Chart.js
- **lottie-web** 5.12.2 — MIT — https://github.com/airbnb/lottie-web
- **three.js** 0.160.0 — MIT — https://github.com/mrdoob/three.js
- **motion** 10.18.0 — MIT — https://github.com/motiondivision/motion

## Sound library (`kadans/assets/sfx/`) — CC0 1.0 (Public Domain)

- [Kenney](https://kenney.nl) (RPG Audio, Impact Sounds) and [Freesound](https://freesound.org) contributors (see `kadans/assets/sfx/CREDITS.md`) — CC0 1.0 Public Domain Dedication.

## Patents

The licenses above govern software copyright. Certain audio/video compression standards (such as H.264 and AAC) may be subject to third-party patent pools independent of software licenses: see [`DOCS/06_LICENCES_ET_DISTRIBUTION.md`](DOCS/06_LICENCES_ET_DISTRIBUTION.md).
