# 06 — Licences et distribution (MIT / LGPL — Politique sans GPL)

**Kadans WASDEV Video Engine** est un logiciel libre sous licence **MIT** (voir [`LICENSE`](../LICENSE) et [`LICENSE.txt`](../LICENSE.txt)), conçu et développé par **GETHO GUERRIER** pour **GRAN LAKU COMPANY** (`https://wasdev.ai` · `https://granlaku.com`).

Pour que le moteur et les applications qui l'intègrent (comme **WASDEV IDE**) restent distribuables sous licence MIT ou commerciale sans contamination copyleft, **aucun composant sous licence GPL ne doit être sélectionné, importé ou livré avec Kadans**.

---

## 1. Règles strictes du code (`kadans/renderer.py`)

1. **Encodeurs interdits (`FORBIDDEN_ENCODERS`)** :
   - `libx264`, `libx265`, `libxvid`, `libxavs`, `libxavs2` (sous licence **GPL**) et `libfdk_aac` (non redistribuable) sont **strictement exclus** de la chaîne d'encodage de [`kadans/renderer.py`](../kadans/renderer.py).
   - Même si la variable d'environnement `KADANS_ENCODER` demande l'un de ces encodeurs, `kadans.renderer.encoder()` lève une erreur explicite (`RenderError`).
2. **Ordre de priorité des encodeurs autorisés** :
   - **Accélération matérielle GPU / OS** : Windows Media Foundation (`h264_mf`), NVIDIA NVENC (`h264_nvenc`), AMD AMF (`h264_amf`), Intel QuickSync (`h264_qsv`), Apple VideoToolbox (`h264_videotoolbox`), Linux VAAPI (`h264_vaapi`).
   - **Encodeurs logiciels permissifs / LGPL** : Cisco OpenH264 (`libopenh264`, licence BSD-2-Clause) → encodeur natif FFmpeg (`mpeg4`, licence LGPL-2.1+).
   - Chaque encodeur candidat est réellement testé sur une courte séquence avant d'être retenu (`_test_encoder`).
3. **Zéro dépendance Python GPL** :
   - Le cœur de Kadans utilise exclusivement la bibliothèque standard de Python (`dependencies = []` dans [`pyproject.toml`](../pyproject.toml)).
   - Les dépendances optionnelles (`kadans-wasdev[blend]`) utilisent uniquement `numpy` (BSD-3-Clause) et `Pillow` (MIT-CMU). L'import de paquets GPL comme `pillow_heif` est interdit.
4. **Tests de non-régression automatiques** :
   - [`tools/check_licenses.py`](../tools/check_licenses.py) et [`tests/test_license_policy.py`](../tests/test_license_policy.py) bloquent toute régression localement et dans GitHub Actions (`.github/workflows/tests.yml`).

---

## 2. FFmpeg (LGPL uniquement) et Chromium

Kadans **n'embarque aucun exécutable binaire** dans son dépôt Git ni dans son paquet Python :

- **FFmpeg LGPL** : la commande `kadans setup` télécharge une archive officielle **LGPL** depuis `github.com/BtbN/FFmpeg-Builds` (`ffmpeg-n8.1-latest-win64-lgpl-8.1.zip` / `linux64-lgpl`, compilée **sans** `--enable-gpl`, **sans** `libx264` et **sans** `libx265`), vérifiée par empreinte SHA-256, et l'installe dans le dossier cache local de l'utilisateur (`%LOCALAPPDATA%\kadans\ffmpeg`). Kadans l'exécute uniquement comme processus externe séparé (`subprocess`).
- **Chromium (`chrome-headless-shell`)** : `kadans setup` télécharge la version épinglée de *Chrome for Testing* (licence BSD-3-Clause, avec son fichier `LICENSE.headless_shell`), vérifiée par SHA-256, ou utilise le navigateur Microsoft Edge / Google Chrome déjà présent sur la machine.

---

## 3. Bibliothèques JavaScript et effets sonores embarqués

Tout ce qui est distribué dans `kadans/assets/` est sous licence permissive compatible MIT :

- **Bibliothèques Web (`kadans/assets/vendor/`) — 100 % MIT** :
  - `anime.min.js` (3.2.1 — MIT)
  - `chart.umd.min.js` (4.4.1 — MIT)
  - `lottie.min.js` (5.12.2 — MIT)
  - `three.min.js` (0.160.0 — MIT)
  - `motion.min.js` (10.18.0 — MIT)
- **Effets sonores (`kadans/assets/sfx/`) — CC0 1.0 (Domaine public)** :
  - Sons Kenney.nl et contributeurs Freesound sous CC0 1.0 (voir `kadans/assets/sfx/CREDITS.md`).

---

## 4. Vérification avant chaque commit ou publication

```bash
python tools/check_licenses.py
python -m unittest discover -s tests -p "test_*.py" -v
```

Le script `tools/check_licenses.py` retourne un code `1` (échec) si :
- un fichier source de `kadans/` sélectionne un encodeur GPL (`libx264`, `libx265`, `libxvid`, `libxavs`, `libfdk_aac`) ou importe un paquet GPL (`pillow_heif`) ;
- un binaire (`.exe`, `.dll`, `ffmpeg*`) est présent dans l'arbre du projet ;
- les fichiers de licence obligatoires (`LICENSE`, `LICENSE.txt`, `THIRD_PARTY_NOTICES.md`, `TRADEMARKS.md`) sont absents.

---

## 5. Marques déposées et brevets

- **Marques** : « Kadans », « Kadans WASDEV », « WASDEV », « The AI WorkShop » et le logo WASDEV sont des marques de **GRAN LAKU COMPANY** (voir [`TRADEMARKS.md`](../TRADEMARKS.md)).
- **Brevets des formats audio/vidéo** : Le retrait du GPL règle les licences logicielles, pas les brevets éventuels des standards H.264 / AAC (couverts par des pools de brevets comme Via LA selon les juridictions et volumes de distribution).
