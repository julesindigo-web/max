"""Complement-8: VSM final 10."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent
sys.path.insert(0, str(ROOT / "validation"))

import importlib.util
spec = importlib.util.spec_from_file_location("vsm8", str(ROOT / "validation" / "validate_set_manifest.py"))
VSM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VSM)

VALID = (ROOT / "manifest.yaml").read_text(encoding="utf-8")


def make_root(tmp, manifest_text, top_level=False):
    root = Path(tmp)
    (root / "manifest.yaml").write_text(manifest_text, encoding="utf-8")
    shutil.copy2(ROOT / "SET.md", root / "SET.md")
    if top_level:
        for member in ("project-artifact-auditor", "skills-create-excellence"):
            (root / member).mkdir(exist_ok=True)
            shutil.copy2(ROOT / member / "SKILL.md", root / member / "SKILL.md")
    else:
        for member in ("skill-alpha", "skill-beta"):
            d = root / "skills" / member
            d.mkdir(parents=True, exist_ok=True)
            # Minimal valid SKILL.
            depends = "[]" if member == "skill-alpha" else "[skill-alpha]"
            provides = "alpha/v1" if member == "skill-alpha" else "beta/v1"
            (d / "SKILL.md").write_text(
                f"---\nname: {member}\nmetadata:\n  version: \"1.0.0\"\n"
                f"  set-membership: test-set\n  depends-on: {depends}\n  provides:\n    - {provides}\n---\n# {member}\n",
                encoding="utf-8")
    for rel in ("shared/contracts/audit-findings.schema.json", "validation/validate_set_manifest.py"):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text("# x\n" if rel.endswith(".py") else "{}", encoding="utf-8")
    return root


MINI_VALID = """name: test-set
version: "1.0.0"
purpose: p
last-reviewed: "2026-10-15"
success-metrics:
  - Trigger performance: \u226590% true positives and \u226410% false positives
  - Task completion: \u226595% of checks pass
  - Context-token efficiency: each SKILL.md remains \u2264500 lines
  - Time-to-working-skill: within \u226460 minutes
  - Residual defect density: zero open Critical or Major findings
members:
  - name: skill-alpha
    version: "1.0.0"
    path: skills/skill-alpha
    depends-on: []
    provides:
      - alpha/v1
  - name: skill-beta
    version: "1.0.0"
    path: skills/skill-beta
    depends-on:
      - skill-alpha
    provides:
      - beta/v1
composition-rules:
  - r
shared-contracts:
  - shared/contracts/audit-findings.schema.json
validation-entry: validation/validate_set_manifest.py
deprecation-policy: d
migration-notes: m
"""


class VSMFinal10Tests(unittest.TestCase):
    def test_metric_without_target_and_lists(self):
        with tempfile.TemporaryDirectory() as t:
            m = MINI_VALID.replace(
                "  - Trigger performance: \u226590% true positives and \u226410% false positives",
                "  - Trigger performance: foo bar")
            root = make_root(t, m)
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)

    def test_depends_mismatch_and_provides_mismatch(self):
        with tempfile.TemporaryDirectory() as t:
            root = make_root(t, MINI_VALID)
            # Manifest says skill-beta depends on skill-alpha, but SKILL says [].
            p = root / "skills" / "skill-beta" / "SKILL.md"
            txt = p.read_text(encoding="utf-8").replace("[skill-alpha]", "[]")
            p.write_text(txt, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            root = make_root(t, MINI_VALID)
            p = root / "skills" / "skill-alpha" / "SKILL.md"
            txt = p.read_text(encoding="utf-8").replace("- alpha/v1", "- other/v9")
            p.write_text(txt, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)

    def test_repeats_self_shared_entry_unlisted(self):
        with tempfile.TemporaryDirectory() as t:
            m = MINI_VALID.replace("      - skill-alpha\n    provides:\n      - beta/v1",
                                   "      - skill-alpha\n      - skill-alpha\n    provides:\n      - beta/v1")
            # Need matching SKILL with duplicate dep.
            root = make_root(t, m)
            p = root / "skills" / "skill-beta" / "SKILL.md"
            # SKILL depends-on block form with duplicate.
            p.write_text(
                "---\nname: skill-beta\nmetadata:\n  version: \"1.0.0\"\n"
                "  set-membership: test-set\n  depends-on:\n    - skill-alpha\n    - skill-alpha\n"
                "  provides:\n    - beta/v1\n---\n# b\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            # Self-dependency.
            m = MINI_VALID.replace(
                "  - name: skill-beta\n    version: \"1.0.0\"\n    path: skills/skill-beta\n    depends-on:\n      - skill-alpha",
                "  - name: skill-beta\n    version: \"1.0.0\"\n    path: skills/skill-beta\n    depends-on:\n      - skill-beta")
            root = make_root(t, m)
            p = root / "skills" / "skill-beta" / "SKILL.md"
            p.write_text(
                "---\nname: skill-beta\nmetadata:\n  version: \"1.0.0\"\n"
                "  set-membership: test-set\n  depends-on:\n    - skill-beta\n"
                "  provides:\n    - beta/v1\n---\n# b\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            m = MINI_VALID.replace("  - shared/contracts/audit-findings.schema.json",
                                   "  - /abs/path.json")
            root = make_root(t, m)
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            m = MINI_VALID.replace("validation-entry: validation/validate_set_manifest.py",
                                   "validation-entry: /abs/entry.py")
            root = make_root(t, m)
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            root = make_root(t, MINI_VALID)
            (root / "skills" / "ghost-skill").mkdir()
            (root / "skills" / "ghost-skill" / "SKILL.md").write_text(
                "---\nname: ghost-skill\n---\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            # Top-level layout (no skills/ dir) to hit 326 false branch: validate real set root.
            msgs = VSM.validate(ROOT)
            self.assertTrue(any("member valid" in m for m in msgs))


if __name__ == "__main__":
    unittest.main(verbosity=2)
