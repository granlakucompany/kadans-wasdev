"""
KADANS WASDEV VIDEO ENGINE — Automated Unit Test Suite
Author: Getho Guerrier · GRAN LAKU COMPANY
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kadans


class TestKadansSuite(unittest.TestCase):
    def test_validate_valid_spec(self):
        raw = {
            "kadans": 1,
            "title": "WASDEV Launch",
            "lang": "ht",
            "ratio": "16:9",
            "brand": {"name": "WAS*DEV*"},
            "scenes": [
                {"type": "hook", "title": "Kreye videyo ak *Kreyòl*"},
                {"type": "cta", "title": "Eseye WASDEV", "subtitle": "wasdev.ai"},
            ],
        }
        spec = kadans.validate(raw)
        self.assertEqual(spec["lang"], "ht")
        self.assertEqual(len(spec["scenes"]), 2)

    def test_validate_rejects_unknown_keys(self):
        raw = {
            "kadans": 1,
            "title": "Bad Spec",
            "unknown_key_xyz": True,
            "scenes": [{"type": "text", "title": "Hello"}],
        }
        with self.assertRaises(kadans.SpecError):
            kadans.validate(raw)

    def test_timeline_and_html_composition(self):
        raw = {
            "kadans": 1,
            "title": "Test Composition",
            "lang": "fr",
            "ratio": "9:16",
            "brand": {"name": "GRAN LAKU"},
            "scenes": [
                {"type": "hook", "title": "Bienvenue dans *Kadans*"},
                {"type": "features", "title": "Fonctionnalités", "items": [
                    {"icon": "🎬", "title": "Vidéo 100% locale"},
                    {"icon": "🎙", "title": "Voix 5 langues"},
                ]},
                {"type": "cta", "title": "Découvrir", "subtitle": "wasdev.ai"},
            ],
        }
        spec = kadans.validate(raw)
        tl = kadans.timeline(spec)
        self.assertEqual(len(tl), 3)
        self.assertGreater(kadans.total(tl), 5.0)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            res = kadans.build_html(spec, tl, tmp_path, {}, tmp_path)
            content = res.read_text(encoding="utf-8") if isinstance(res, Path) else str(res)
            self.assertIn("window.__seek", content)
            self.assertIn("GRAN LAKU", content)
            # HTML Player Rule: centered Play button only, bottom playbar hidden
            self.assertIn('id="kplay_center"', content)
            self.assertIn('id="kbar" style="display:none !important"', content)
            self.assertIn("body.is-render #kplay_center", content)
            self.assertIn(".ineditor #kplay_center{display:none !important", content)

    def test_json_schema_generation(self):
        schema = kadans.json_schema()
        self.assertIsInstance(schema, dict)
        self.assertIn("properties", schema)
        self.assertIn("scenes", schema["properties"])

    def test_security_no_secrets_or_personal_paths(self):
        from tools import check_licenses
        self.assertEqual(check_licenses.check_no_secrets_or_personal_paths(), [])


if __name__ == "__main__":
    unittest.main()
