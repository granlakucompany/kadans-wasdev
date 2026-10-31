"""Kadans WASDEV — one-time folder migration (Gran Laku Company, Getho Guerrier).

New layout (2026-10-20), the same in WASDEV and in this repo:

    Analyseur-Kadans/
        <project>/            spec.json, composition.html, voice, images…
        exported videos/      final MP4s

Old layout: kadans-projects/<project>/ + exported-videos/ next to it.
This script MOVES the old folders into the new layout. It never deletes or overwrites anything: an item that already
exists in the new place is left where it is (and reported). Safe to run many times (nothing to do = no-op).

    python tools/migrate_folders.py [root]      (root = this repo by default)
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

NEW, EXPORTS = "Analyseur-Kadans", "exported videos"
OLD_PROJECTS, OLD_EXPORTS = "kadans-projects", "exported-videos"


def migrate(root: Path) -> list[str]:
    log = []
    new = root / NEW
    pairs = [(root / OLD_PROJECTS, new), (root / OLD_EXPORTS, new / EXPORTS)]
    for src_dir, dst_dir in pairs:
        if not src_dir.is_dir():
            continue
        dst_dir.mkdir(parents=True, exist_ok=True)
        for item in sorted(src_dir.iterdir()):
            target = dst_dir / item.name
            if target.exists():
                log.append(f"skip (already exists): {target.relative_to(root)}")
                continue
            try:
                shutil.move(str(item), str(target))
                log.append(f"moved: {item.relative_to(root)} -> {target.relative_to(root)}")
            except OSError as e:                       # file in use (an editor is open on it): try again later
                log.append(f"NOT moved (in use?): {item.relative_to(root)} — {e}")
        try:
            src_dir.rmdir()                            # only if now empty
            log.append(f"removed empty folder: {src_dir.relative_to(root)}")
        except OSError:
            pass
    return log


if __name__ == "__main__":
    r = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    for line in migrate(r):
        print(line)
