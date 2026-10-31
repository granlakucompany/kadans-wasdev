# Security Policy

## Reporting a vulnerability
Email **wasdevsecurity@granlaku.com** (or wasdevsupport@granlaku.com). Do **not** open a public issue for a
vulnerability. We aim to acknowledge within 72 hours and to agree a disclosure timeline with you.

## Scope
Kadans runs locally and does no network I/O at render time. Relevant concerns:
- Spec parsing (malformed JSON / adversarial values) causing crashes or path escapes.
- `html` scenes execute author-provided HTML/JS in the render engine — treat specs from untrusted sources
  as untrusted code. Render such specs in a sandbox.
- Media/asset path resolution escaping the project folder.

## Good practice
Keep FFmpeg and the render browser updated. Review third-party specs before rendering.
