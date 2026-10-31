"""
KADANS WASDEV VIDEO ENGINE — 8-Language Support & Haitian Creole Phonetics Test Suite
Languages: FR, EN, HT, ES, PT, DE, IT, RU
Author: Getho Guerrier · GRAN LAKU COMPANY
"""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kadans
from kadans import audio, compose, spec as kspec

ALL_8_LANGS = ("fr", "en", "ht", "es", "pt", "de", "it", "ru")


class TestEightLanguagesSupport(unittest.TestCase):
    def test_spec_supports_all_8_languages(self):
        self.assertEqual(set(kspec.LANGS), set(ALL_8_LANGS))
        for lang in ALL_8_LANGS:
            raw = {
                "kadans": 1,
                "title": f"Kadans {lang.upper()}",
                "lang": lang,
                "ratio": "16:9",
                "voice": {"lang": lang, "gender": "female"},
                "scenes": [
                    {"type": "hook", "title": f"Hello {lang}"},
                    {"type": "cta", "title": "WASDEV", "subtitle": "wasdev.ai"},
                ],
            }
            validated = kadans.validate(raw)
            self.assertEqual(validated["lang"], lang)
            self.assertEqual(validated["voice"]["lang"], lang)

    def test_compose_credit_and_html_all_8_languages(self):
        for lang in ALL_8_LANGS:
            self.assertIn(lang, compose.CREDIT)
            self.assertTrue(compose.CREDIT[lang].strip())
            raw = {
                "kadans": 1,
                "title": f"Test {lang}",
                "lang": lang,
                "scenes": [{"type": "hook", "title": "Kadans"}],
            }
            validated = kadans.validate(raw)
            tl = kadans.timeline(validated)
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                res = kadans.build_html(validated, tl, tmp_path, {}, tmp_path)
                content = res.read_text(encoding="utf-8") if isinstance(res, Path) else str(res)
                self.assertIn(f'<html lang="{lang}">', content)
                self.assertIn(compose.CREDIT[lang], content)

    def test_studio_editor_i18n_all_8_languages(self):
        i18n_js = (PROJECT_ROOT / "kadans" / "studio_editor" / "kadans_i18n.js").read_text(encoding="utf-8")
        index_html = (PROJECT_ROOT / "kadans" / "studio_editor" / "index.html").read_text(encoding="utf-8")

        for lang in ALL_8_LANGS:
            # Verify language dictionary block or assignment in KADANS_DICT
            self.assertRegex(
                i18n_js,
                rf"(?:\b{lang}\s*:\s*\{{|KADANS_DICT\.{lang}\s*=)",
                f"Missing {lang} block in KADANS_DICT",
            )
            # Verify phrase index in P_IDX
            self.assertRegex(i18n_js, rf"\b{lang}\s*:\s*\d+", f"Missing {lang} in P_IDX")
            # Verify #vlang option in studio_editor/index.html
            self.assertIn(f'<option value="{lang}"', index_html, f"Missing <option value=\"{lang}\"> in #vlang")

        # Extract keys from each language block in KADANS_DICT and ensure parity with 'fr'
        blocks = {lang: set() for lang in ALL_8_LANGS}
        for lang in ("fr", "ht", "en", "es", "de"):
            m = re.search(rf"^\s{{4}}{lang}\s*:\s*\{{(.*?)^\s{{4}}\}}", i18n_js, re.DOTALL | re.MULTILINE)
            self.assertIsNotNone(m, f"Could not parse KADANS_DICT.{lang}")
            blocks[lang].update(re.findall(r'"([a-zA-Z0-9_]+)"\s*:', m.group(1)))
        for lang in ("pt", "it", "ru"):
            m = re.search(rf"KADANS_DICT\.{lang}\s*=\s*Object\.assign\(\{{\}},\s*KADANS_DICT\.en,\s*\{{(.*?)\}}\);", i18n_js, re.DOTALL)
            self.assertIsNotNone(m, f"Could not parse KADANS_DICT.{lang}")
            blocks[lang].update(blocks["en"])
            blocks[lang].update(re.findall(r'"([a-zA-Z0-9_]+)"\s*:', m.group(1)))
        # Also include _EXTRA, _SETTINGS, _STABLE keys assigned to all languages
        for extra_var in ("_EXTRA", "_SETTINGS", "_STABLE"):
            m_var = re.search(rf"const\s+{extra_var}\s*=\s*\{{(.*?)\}}\s*;", i18n_js, re.DOTALL)
            if m_var:
                var_body = m_var.group(1)
                for lang in ALL_8_LANGS:
                    m_ex = re.search(rf"\b{lang}\s*:\s*\{{([^{{}}]*)\}}", var_body)
                    if m_ex:
                        blocks[lang].update(re.findall(r'(?:^|[,{])\s*"?([a-zA-Z0-9_]+)"?\s*:', m_ex.group(1)))

        fr_keys = blocks["fr"]
        self.assertGreater(len(fr_keys), 25)
        for lang in ALL_8_LANGS:
            missing = fr_keys - blocks[lang]
            self.assertFalse(missing, f"Language '{lang}' in kadans_i18n.js is missing keys: {missing}")

    def test_readme_contains_all_8_languages(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        expected_headers = [
            "### 🇫🇷 Français",
            "### 🇬🇧 English",
            "### 🇭🇹 Kreyòl Ayisyen",
            "### 🇪🇸 Español",
            "### 🇵🇹 Português",
            "### 🇩🇪 Deutsch",
            "### 🇮🇹 Italiano",
            "### 🇷🇺 Русский",
        ]
        for header in expected_headers:
            self.assertIn(header, readme, f"Missing language section in README.md: {header}")

    def test_kreyol_phonetics_and_prosody_rule_8(self):
        # Verify mandatory phonetic transformations for Haitian Creole audio synthesis
        self.assertEqual(audio.kreyol_to_phonetic_french("nou"), "nous")
        self.assertEqual(audio.kreyol_to_phonetic_french("kounye a"), "kounyeya")
        self.assertEqual(audio.kreyol_to_phonetic_french("koreksyon"), "corréction")
        self.assertEqual(audio.kreyol_to_phonetic_french("nan"), "nan")
        self.assertEqual(audio.kreyol_to_phonetic_french("an"), "an")
        self.assertEqual(audio.kreyol_to_phonetic_french("animasyon an"), "animation an")
        self.assertEqual(audio.kreyol_to_phonetic_french("bezwen"), "besoin")
        self.assertEqual(audio.kreyol_to_phonetic_french("yo"), "io")
        self.assertEqual(audio.kreyol_to_phonetic_french("tout"), "toute")
        self.assertEqual(audio.kreyol_to_phonetic_french("fèt"), "faite")
        self.assertEqual(audio.kreyol_to_phonetic_french("wout"), "route")
        self.assertEqual(audio.kreyol_to_phonetic_french("kreyasyon"), "kreyation")
        self.assertEqual(audio.kreyol_to_phonetic_french("pale"), "paler")

        # Verify ElevenLabs prosody parameters (stability=0.38, style=0.40) in kadans/audio.py
        audio_src = (PROJECT_ROOT / "kadans" / "audio.py").read_text(encoding="utf-8")
        self.assertIn('"stability": 0.38', audio_src)
        self.assertIn('"style": 0.40', audio_src)
        self.assertIn("kreyol_to_phonetic_french", audio_src)


if __name__ == "__main__":
    unittest.main()
