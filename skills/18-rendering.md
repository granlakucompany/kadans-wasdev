# Skill: rendering

`python -m kadans render spec.json out.mp4`. The page draws any instant with `window.__seek(t)`; the
renderer captures frames in a local Chromium/Edge and encodes with FFmpeg. Unchanged scenes come from
cache (fast re-render). Add `verify=True` to QC the voice against the script with Whisper.
