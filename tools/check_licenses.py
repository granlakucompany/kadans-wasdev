"""
KADANS WASDEV VIDEO ENGINE — Vérification des licences avant empaquetage / publication
Éditeur : GRAN LAKU COMPANY (Getho Guerrier) | https://wasdev.ai · https://granlaku.com

Kadans WASDEV est distribué sous licence MIT. Aucun composant GPL (libx264, libx265,
libxvid, libpostproc, pillow_heif, binaires FFmpeg GPL…) ne doit être utilisé ni livré
dans ce dépôt.

Usage : python tools/check_licenses.py
Code de sortie 0 = conforme MIT/LGPL ; 1 = problème de licence à corriger.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

FORBIDDEN_ENCODERS = ("libx264", "libx265", "libxvid", "libxavs", "libxavs2", "libfdk_aac")
FORBIDDEN_IMPORTS = ("pillow_heif",)
FORBIDDEN_BINARIES = (".exe", ".dll", ".pyd", ".so", ".msi")
REQUIRED_FILES = (
    "LICENSE",
    "LICENSE.txt",
    "THIRD_PARTY_NOTICES.md",
    "TRADEMARKS.md",
    "DOCS/06_LICENCES_ET_DISTRIBUTION.md",
)


def check_required_license_files() -> list[str]:
    problems = []
    for rel in REQUIRED_FILES:
        p = PROJECT_ROOT / rel
        if not p.is_file():
            problems.append(f"Fichier de licence manquant : {rel}")
    return problems


def check_source_gpl_encoders() -> list[str]:
    """Vérifie qu'aucun fichier de kadans/ ne sélectionne un encodeur GPL hors de FORBIDDEN_ENCODERS."""
    problems = []
    names = "|".join(re.escape(n) for n in FORBIDDEN_ENCODERS)
    pattern = re.compile(r"[\"'](" + names + r")[\"']")
    for path in (PROJECT_ROOT / "kadans").rglob("*.py"):
        for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if "FORBIDDEN_ENCODERS" in line:
                continue
            if pattern.search(line):
                problems.append(f"Encodeur GPL cité dans {path.relative_to(PROJECT_ROOT)}:{line_no} -> {line.strip()}")
    return problems


def check_source_imports() -> list[str]:
    """Vérifie qu'aucun paquet Python embarquant du GPL n'est importé."""
    problems = []
    pattern = re.compile(r"^\s*(?:import|from)\s+(" + "|".join(FORBIDDEN_IMPORTS) + r")\b", re.MULTILINE)
    for path in (PROJECT_ROOT / "kadans").rglob("*.py"):
        if pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
            problems.append(f"Import interdit (GPL) dans {path.relative_to(PROJECT_ROOT)}")
    return problems


def check_deps_ffmpeg_lgpl() -> list[str]:
    """Vérifie que kadans/deps.py télécharge uniquement des builds FFmpeg LGPL."""
    problems = []
    from kadans import deps
    for plat_name, asset in getattr(deps, "FFMPEG_ASSET", {}).items():
        if "-lgpl-" not in asset.lower():
            problems.append(f"kadans/deps.py ({plat_name}) ne pointe pas vers un build LGPL : {asset}")
    return problems


def check_no_shipped_binaries() -> list[str]:
    """Aucun exécutable ou DLL ne doit être livré dans le paquet kadans/."""
    problems = []
    root = PROJECT_ROOT / "kadans"
    if root.is_dir():
        for path in root.rglob("*"):
            if path.is_file():
                low = path.name.lower()
                if path.suffix.lower() in FORBIDDEN_BINARIES or low.startswith("ffmpeg"):
                    problems.append(f"Binaire interdit dans le dépôt : {path.relative_to(PROJECT_ROOT)}")
    return problems


def check_no_secrets_or_personal_paths() -> list[str]:
    """Vérifie qu'aucune clé API, jeton secret ou chemin personnel n'est présent dans les fichiers suivis."""
    problems = []
    secret_patterns = [
        (re.compile(r"ghp_[A-Za-z0-9]{30,}"), "Jeton GitHub (ghp_)"),
        (re.compile(r"github_pat_[A-Za-z0-9_]{30,}"), "Jeton GitHub PAT"),
        (re.compile(r"sk-[A-Za-z0-9]{28,}"), "Clé API (sk-)"),
        (re.compile(r"xi-[A-Za-z0-9]{24,}"), "Clé ElevenLabs (xi-)"),
        (re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9_.-]+", re.IGNORECASE), "Chemin utilisateur local Windows"),
    ]
    import subprocess
    try:
        tracked = subprocess.check_output(["git", "ls-files"], cwd=PROJECT_ROOT, text=True).splitlines()
        files_to_scan = [
            PROJECT_ROOT / rel for rel in tracked
            if Path(rel).suffix.lower() in (".py", ".js", ".html", ".md", ".yml", ".json", ".toml")
        ]
    except Exception:
        scan_dirs = [PROJECT_ROOT / "kadans", PROJECT_ROOT / "tools", PROJECT_ROOT / "tests", PROJECT_ROOT / ".github", PROJECT_ROOT / "DOCS"]
        files_to_scan = [p for p in PROJECT_ROOT.glob("*.toml")]
        for d in scan_dirs:
            if d.is_dir():
                for ext in ("*.py", "*.js", "*.html", "*.md", "*.yml", "*.json"):
                    files_to_scan.extend(d.rglob(ext))
    this_file = Path(__file__).resolve()
    for path in files_to_scan:
        if path.resolve() == this_file:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for rx, label in secret_patterns:
            if rx.search(text):
                problems.append(f"Sécurité ({label}) détecté dans {path.relative_to(PROJECT_ROOT)}")
    return problems


def run_checks() -> list[str]:
    return (
        check_required_license_files()
        + check_source_gpl_encoders()
        + check_source_imports()
        + check_deps_ffmpeg_lgpl()
        + check_no_shipped_binaries()
        + check_no_secrets_or_personal_paths()
    )


def main() -> int:
    problems = run_checks()
    if problems:
        print("ÉCHEC — composants incompatibles avec la politique de licence MIT / LGPL :")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("OK — aucune dépendance ni encodeur GPL détecté (conforme MIT / LGPL GRAN LAKU COMPANY).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
