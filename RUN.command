#!/usr/bin/env bash
# Kadans Timeline - Gran Laku Company (Getho Guerrier)
cd "$(dirname "$0")"
echo "Ap louvri Kadans Timeline nan navigate ou a..."
(python3 tools/migrate_folders.py || python tools/migrate_folders.py) 2>/dev/null
python3 -m kadans timeline "Analyseur-Kadans/Pwoje-1" || python -m kadans timeline "Analyseur-Kadans/Pwoje-1"
