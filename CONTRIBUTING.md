# Contributing to KADANS WASDEV VIDEO ENGINE

Thank you for helping improve **KADANS WASDEV VIDEO ENGINE**! Bug reports, new scene types, FFmpeg & GPU optimisations, Studio Editor improvements, skills and translations are all welcome. You can write issues and pull requests in **English**, **French** or **Haitian Creole**.

## Ways to contribute
- Report a bug or suggest a feature with the [issue forms](.github/ISSUE_TEMPLATE).
- Ask a question or share an idea in Discussions.
- Send code with a pull request (see below).

## Development setup

Requirements: Python 3.10+ (Recommended: Python 3.12 x64), FFmpeg (LGPL) and Chromium / Edge.

```bash
git clone https://github.com/<your-account>/kadans-wasdev.git
cd kadans-wasdev
python -m venv venv
venv\Scripts\activate
pip install -e .
kadans doctor
```

## Before opening a pull request

1. Create a branch from `main` for your change.
2. Run the automated test suite and the license check:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python tools/check_licenses.py
```

The same checks run automatically on GitHub Actions for every pull request.

3. Open the pull request against `main` and describe what changed and how you tested it.

## Project rules & Principles that don't bend
- **No GPL components.** Kadans is distributed under the **MIT License**, so the engine and repository must never select, import, or ship GPL encoders (`libx264`, `libx265`, `libxvid`, `libxavs`, `libxavs2`, `libfdk_aac`) or GPL packages (`pillow_heif`). `python tools/check_licenses.py` must pass. Details: [`DOCS/06_LICENCES_ET_DISTRIBUTION.md`](DOCS/06_LICENCES_ET_DISTRIBUTION.md).
- **100% local & deterministic.** No telemetry, no network calls at render time, no required API keys. `window.__seek(t)` must draw any instant identically on every machine.
- **Reject the unknown.** The spec validator refuses unknown keys and bad values — never silently accept.
- **New capabilities.** New scene type → `kadans/spec.py` (types/keys/validation/help) + `kadans/compose.py` (body) + a `skills/` guide + a unit test in `tests/`.
- **No secrets or personal data in the code:** no API keys, passwords, tokens or local paths.

## License

By contributing, you agree that your contributions are released under the [MIT License](LICENSE) of the project.

**KADANS WASDEV VIDEO ENGINE** is developed by **GETHO GUERRIER** for **GRAN LAKU COMPANY** (`https://wasdev.ai` · `https://granlaku.com`).
