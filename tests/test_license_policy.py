"""
Non-régression licences : KADANS WASDEV VIDEO ENGINE est distribué sous licence MIT.
Aucun encodeur GPL (libx264, libx265, libxvid…) ni binaire GPL ne doit être choisi ni livré.
"""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kadans import deps, renderer
from tools import check_licenses


class TestLicensePolicy(unittest.TestCase):
    def test_source_never_names_a_gpl_encoder(self):
        self.assertEqual(check_licenses.check_source_gpl_encoders(), [])

    def test_forbidden_encoders_constant_present(self):
        for bad in ("libx264", "libx265", "libxvid", "libxavs", "libxavs2", "libfdk_aac"):
            self.assertIn(bad, renderer.FORBIDDEN_ENCODERS)

    def test_forbidden_encoder_rejected_via_env(self):
        for bad in ("libx264", "libx265", "libxvid"):
            with self.subTest(encoder=bad):
                with mock.patch.dict(os.environ, {"KADANS_ENCODER": bad}):
                    with mock.patch("kadans.media.find_tool", return_value="fake_ffmpeg"):
                        renderer._ENC["fake_ffmpeg"] = ["h264_mf", "libopenh264", "mpeg4", bad]
                        with self.assertRaises(renderer.RenderError):
                            renderer.encoder(1920, 1080, 30)

    def test_encoder_never_picks_forbidden_gpl_encoder(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("KADANS_ENCODER", None)
            with mock.patch("kadans.media.find_tool", return_value="fake_ffmpeg_gpl"):
                renderer._ENC["fake_ffmpeg_gpl"] = ["libx264", "libx265", "libopenh264", "mpeg4"]
                renderer._WORKING_ENC.pop("fake_ffmpeg_gpl", None)
                with mock.patch("kadans.renderer._test_encoder", return_value=True):
                    enc_name, _ = renderer.encoder(1920, 1080, 30)
                    self.assertNotIn(enc_name, renderer.FORBIDDEN_ENCODERS)
                    self.assertIn(enc_name, ("libopenh264", "mpeg4"))

    def test_deps_uses_only_lgpl_ffmpeg(self):
        self.assertEqual(check_licenses.check_deps_ffmpeg_lgpl(), [])
        for asset in deps.FFMPEG_ASSET.values():
            self.assertIn("-lgpl-", asset)

    def test_source_does_not_import_gpl_packages(self):
        self.assertEqual(check_licenses.check_source_imports(), [])

    def test_no_shipped_binaries(self):
        self.assertEqual(check_licenses.check_no_shipped_binaries(), [])

    def test_all_license_checks_pass(self):
        self.assertEqual(check_licenses.run_checks(), [])


if __name__ == "__main__":
    unittest.main()
