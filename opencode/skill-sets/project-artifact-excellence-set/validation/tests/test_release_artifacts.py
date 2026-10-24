"""Tests for deterministic ZIP packaging, hashes, permissions, and tamper detection."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent
BUILDER = ROOT / "scripts/build-release.py"
VERIFIER = ROOT / "scripts/verify-release.py"


class ReleaseArtifactTests(unittest.TestCase):
    def test_two_builds_are_byte_identical_and_verify(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            one = out / "one.zip"
            two = out / "two.zip"
            for target in (one, two):
                result = subprocess.run([sys.executable, str(BUILDER), "--root", str(ROOT), "--output", str(target), "--epoch", "946684800"], text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                verify = subprocess.run([sys.executable, str(VERIFIER), str(target)], text=True, capture_output=True)
                self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)
            self.assertEqual(one.read_bytes(), two.read_bytes(), "builds must be byte-for-byte reproducible")

    def test_archive_preserves_executable_mode_and_checksums(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "release.zip"
            result = subprocess.run([sys.executable, str(BUILDER), "--root", str(ROOT), "--output", str(target)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with zipfile.ZipFile(target) as archive:
                info = archive.getinfo("validation/validate-set.sh")
                mode = (info.external_attr >> 16) & 0o777
                self.assertEqual(mode, 0o755)
                self.assertIn("RELEASE-MANIFEST.sha256", archive.namelist())


    def test_verifier_rejects_symbolic_link_entries(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "symlink.zip"
            result = subprocess.run([sys.executable, str(BUILDER), "--root", str(ROOT), "--output", str(Path(temp) / "good.zip")], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            good = Path(temp) / "good.zip"
            with zipfile.ZipFile(good, "r") as source, zipfile.ZipFile(target, "w") as dest:
                for info in source.infolist():
                    payload = source.read(info.filename)
                    if info.filename == "SET.md":
                        info = zipfile.ZipInfo("evil-link", date_time=info.date_time)
                        info.create_system = 3
                        info.external_attr = (0o120777 << 16)
                        payload = b"../../outside"
                    dest.writestr(info, payload)
            verify = subprocess.run([sys.executable, str(VERIFIER), str(target)], text=True, capture_output=True)
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("symbolic-link", verify.stderr)

    def test_verifier_rejects_file_parent_path_collisions(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "collision.zip"
            result = subprocess.run([sys.executable, str(BUILDER), "--root", str(ROOT), "--output", str(Path(temp) / "good.zip")], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            good = Path(temp) / "good.zip"
            with zipfile.ZipFile(good, "r") as source, zipfile.ZipFile(target, "w") as dest:
                for info in source.infolist():
                    dest.writestr(info, source.read(info.filename))
                dest.writestr("SET.md/child.txt", b"collision")
            verify = subprocess.run([sys.executable, str(VERIFIER), str(target)], text=True, capture_output=True)
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("path collision", verify.stderr)

    def test_tampered_content_fails_integrity_check(self):
        with tempfile.TemporaryDirectory() as temp:
            good = Path(temp) / "good.zip"
            bad = Path(temp) / "bad.zip"
            result = subprocess.run([sys.executable, str(BUILDER), "--root", str(ROOT), "--output", str(good)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with zipfile.ZipFile(good, "r") as source, zipfile.ZipFile(bad, "w", compression=zipfile.ZIP_DEFLATED) as dest:
                for info in source.infolist():
                    payload = source.read(info.filename)
                    if info.filename == "SET.md":
                        payload += b"\nTAMPERED\n"
                    dest.writestr(info, payload)
            verify = subprocess.run([sys.executable, str(VERIFIER), str(bad)], text=True, capture_output=True)
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("SHA-256 mismatch: SET.md", verify.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
