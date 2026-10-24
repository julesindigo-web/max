"""Complement-9: VSM 174/293/296 via mock + indented."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1].parent
sys.path.insert(0, str(ROOT / "validation"))

import importlib.util
spec = importlib.util.spec_from_file_location("vsm9", str(ROOT / "validation" / "validate_set_manifest.py"))
VSM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VSM)


class VSMMockTests(unittest.TestCase):
    def test_indented_before_metadata(self):
        with tempfile.TemporaryDirectory() as t:
            s = Path(t) / "SKILL.md"
            s.write_text("---\nname: x\n  indented-before-metadata: 1\nmetadata:\n  version: 1.0.0\n", encoding="utf-8")
            # Should hit `if not in_metadata: continue` (174).
            md = VSM.read_frontmatter_metadata(s)
            self.assertIn("version", md)

    def test_nonlist_dependencies_via_mock(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "manifest.yaml").write_text("x: 1\n", encoding="utf-8")
            fake_data = {
                "name": "test-set", "version": "1.0.0", "purpose": "p",
                "last-reviewed": "2026-10-15",
                "success-metrics": [
                    "Trigger performance: \u226590% x", "Task completion: \u226595% y",
                    "Context-token efficiency: z \u2264500 lines", "Time-to-working-skill: w \u226460 minutes",
                    "Residual defect density: zero open Critical and Major q",
                ],
                "members": [{"name": "a", "version": "1.0.0", "path": "a",
                             "depends-on": "notalist", "provides": []}],
                "composition-rules": ["r"], "shared-contracts": ["c"],
                "validation-entry": "v", "deprecation-policy": "d", "migration-notes": "m",
            }
            with mock.patch.object(VSM, "parse_constrained_yaml", return_value=fake_data):
                # Need safe_member_path to pass? It will fail at member path (no SKILL), but first hits depends-type?
                # Actually validate checks name/version/path before depends-type; need valid path to reach depends-type.
                # Create path a with SKILL to pass earlier checks.
                (root / "a").mkdir()
                (root / "a" / "SKILL.md").write_text(
                    "---\nname: a\nmetadata:\n  version: \"1.0.0\"\n  set-membership: test-set\n"
                    "  depends-on: []\n  provides: []\n---\n", encoding="utf-8")
                (root / "SET.md").write_text("# s\n", encoding="utf-8")
                with self.assertRaises(VSM.ManifestError):
                    VSM.validate(root)
            fake_data2 = dict(fake_data)
            fake_data2["members"] = [{"name": "a", "version": "1.0.0", "path": "a",
                                      "depends-on": [], "provides": "notalist"}]
            with mock.patch.object(VSM, "parse_constrained_yaml", return_value=fake_data2):
                with self.assertRaises(VSM.ManifestError):
                    VSM.validate(root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
