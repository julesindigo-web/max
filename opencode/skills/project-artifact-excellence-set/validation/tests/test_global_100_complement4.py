"""Complement-4: validate_set_manifest full reachable coverage."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent
sys.path.insert(0, str(ROOT / "validation"))

import importlib.util
spec = importlib.util.spec_from_file_location("vsm_c4", str(ROOT / "validation" / "validate_set_manifest.py"))
VSM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VSM)


VALID = """name: test-set
version: "1.0.0"
purpose: Test set.
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
  - rule one
shared-contracts:
  - shared/contracts/audit-findings.schema.json
validation-entry: validation/validate_set_manifest.py
deprecation-policy: none
migration-notes: none
"""

SKILL_T = """---
name: {name}
metadata:
  version: "1.0.0"
  set-membership: test-set
  depends-on: {depends}
  provides:
    - {provides}
---
# {name}
"""


class VSMTests(unittest.TestCase):
    def _root(self, tmp, manifest=VALID, skills=("skill-alpha", "skill-beta")):
        root = Path(tmp)
        (root / "manifest.yaml").write_text(manifest, encoding="utf-8")
        (root / "SET.md").write_text("# S\n", encoding="utf-8")
        (root / "validation").mkdir(exist_ok=True)
        (root / "validation" / "validate_set_manifest.py").write_text("# x\n", encoding="utf-8")
        (root / "shared" / "contracts").mkdir(parents=True, exist_ok=True)
        (root / "shared" / "contracts" / "audit-findings.schema.json").write_text("{}", encoding="utf-8")
        depends_map = {"skill-alpha": "[]", "skill-beta": "[skill-alpha]"}
        provides_map = {"skill-alpha": "alpha/v1", "skill-beta": "beta/v1"}
        for name in skills:
            d = root / "skills" / name
            d.mkdir(parents=True, exist_ok=True)
            (d / "SKILL.md").write_text(
                SKILL_T.format(name=name, depends_yaml=depends_map.get(name, "[]"),
                               depends=depends_map.get(name, "[]"),
                               provides=provides_map.get(name, "x/v1")),
                encoding="utf-8")
        return root

    def test_scalar_and_parse_tabs_and_top_errors(self):
        self.assertEqual(VSM.scalar("'hi'"), "hi")
        self.assertEqual(VSM.scalar('"hi"'), "hi")
        self.assertEqual(VSM.scalar("  hi  "), "hi")
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "m.yaml"
            p.write_text("name: x\n\tbad: 1\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)
            p.write_text("bad line without colon\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)
            p.write_text("name: a\nname: b\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)
            p.write_text("members: notalist\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)
            p.write_text("success-metrics:\n-notwo spaces\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)
            # Duplicate member field, bad list, empty field, bad nested, unexpected indent.
            p.write_text("members:\n  - name: a\n    version: 1.0.0\n    version: 2.0.0\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)

    def test_member_sublist_and_nested_errors(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "m.yaml"
            # depends-on inline bad (not list).
            p.write_text("members:\n  - name: a\n    depends-on: bad\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)
            # depends-on inline ok with values.
            p.write_text("members:\n  - name: a\n    depends-on: [x, y]\n", encoding="utf-8")
            d = VSM.parse_constrained_yaml(p)
            self.assertEqual(d["members"][0]["depends-on"], ["x", "y"])
            # Empty field.
            p.write_text("members:\n  - name: a\n    version:\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)
            # Invalid member syntax.
            p.write_text("members:\n  - name: a\n    bogus: x\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)
            # Unexpected indented outside list.
            p.write_text("name: x\n  bad: 1\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.parse_constrained_yaml(p)

    def test_safe_path_and_frontmatter_and_metadata(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            with self.assertRaises(VSM.ManifestError):
                VSM.safe_member_path(root, "")
            with self.assertRaises(VSM.ManifestError):
                VSM.safe_member_path(root, "/abs")
            with self.assertRaises(VSM.ManifestError):
                VSM.safe_member_path(root, "a\\b")
            with self.assertRaises(VSM.ManifestError):
                VSM.safe_member_path(root, "a/../b")
            with self.assertRaises(VSM.ManifestError):
                VSM.safe_member_path(root, "missing")
            s = root / "s"
            s.mkdir()
            (s / "SKILL.md").write_text("---\nname: s\n---\n", encoding="utf-8")
            self.assertEqual(VSM.safe_member_path(root, "s"), s.resolve())
            # Outside root via symlink.
            outside = Path(t) / "out"
            outside.mkdir()
            (root / "link").symlink_to(outside)
            with self.assertRaises(VSM.ManifestError):
                VSM.safe_member_path(root, "link")
            # No SKILL.md.
            (root / "empty").mkdir()
            with self.assertRaises(VSM.ManifestError):
                VSM.safe_member_path(root, "empty")
            # Frontmatter errors.
            (s / "SKILL.md").write_text("nope\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.read_frontmatter_name(s / "SKILL.md")
            (s / "SKILL.md").write_text("---\nfoo: bar\n---\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.read_frontmatter_name(s / "SKILL.md")
            self.assertEqual(VSM.read_frontmatter_name(
                Path(ROOT / "project-artifact-auditor" / "SKILL.md")),
                "project-artifact-auditor")
            # Metadata errors.
            with self.assertRaises(VSM.ManifestError):
                VSM.read_frontmatter_metadata(s / "SKILL.md")
            (s / "SKILL.md").write_text("---\nname: s\nmetadata:\n  version: 1.0.0\n---\n", encoding="utf-8")
            md = VSM.read_frontmatter_metadata(s / "SKILL.md")
            self.assertIn("depends-on", md)
            # Bad metadata list.
            (s / "SKILL.md").write_text(
                "---\nname: s\nmetadata:\n  depends-on: bad\n---\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.read_frontmatter_metadata(s / "SKILL.md")
            # Duplicate metadata field.
            (s / "SKILL.md").write_text(
                "---\nname: s\nmetadata:\n  version: 1\n  version: 2\n---\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.read_frontmatter_metadata(s / "SKILL.md")
            # dependency_name bad + acyclic.
            with self.assertRaises(VSM.ManifestError):
                VSM.dependency_name("BAD NAME!", "m")
            self.assertEqual(VSM.dependency_name("a@1.0", "m"), "a")
            with self.assertRaises(VSM.ManifestError):
                VSM.check_acyclic({"a": ["b"], "b": ["a"]})
            VSM.check_acyclic({"a": [], "b": ["a"]})

    def test_validate_top_and_members(self):
        with tempfile.TemporaryDirectory() as t:
            root = self._root(t)
            msgs = VSM.validate(root)
            self.assertGreaterEqual(len(msgs), 2)
            # Missing file.
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(Path(t) / "nope")
            # Missing top field.
            (root / "manifest.yaml").write_text("name: x\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
            # Unknown field.
            m = VALID + "extra-field: 1\n"
            (root / "manifest.yaml").write_text(m, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
            # Empty required.
            m2 = VALID.replace("purpose: Test set.", "purpose: ")
            (root / "manifest.yaml").write_text(m2, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
            # Bad kebab/semver/date.
            for bad, expect in [
                (VALID.replace("name: test-set", "name: Bad_Name"), "kebab"),
                (VALID.replace('version: "1.0.0"', 'version: "bad"'), "semantic"),
                (VALID.replace('last-reviewed: "2026-10-15"', 'last-reviewed: "15-10-2026"'), "YYYY-MM-DD"),
            ]:
                (root / "manifest.yaml").write_text(bad, encoding="utf-8")
                with self.assertRaises(VSM.ManifestError, msg=expect):
                    VSM.validate(root)
            # Missing SET.md.
            (root / "manifest.yaml").write_text(VALID, encoding="utf-8")
            (root / "SET.md").unlink()
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
            (root / "SET.md").write_text("# S\n", encoding="utf-8")
            # Empty metrics/members/rules/contracts.
            for needle in ["Trigger performance:", "members:\n  - name: skill-alpha",
                           "composition-rules:", "shared-contracts:"]:
                bad = VALID.replace(needle, "REMOVED:")
                (root / "manifest.yaml").write_text(bad, encoding="utf-8")
                with self.assertRaises(VSM.ManifestError, msg=needle):
                    VSM.validate(root)
            (root / "manifest.yaml").write_text(VALID, encoding="utf-8")
            # Duplicate member, bad version, duplicate path, name mismatch, version mismatch,
            # set-membership, depends type, provides type, metadata mismatch, repeats, self, undeclared.
            dup = VALID.replace("- name: skill-beta", "- name: skill-alpha")
            (root / "manifest.yaml").write_text(dup, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
            (root / "manifest.yaml").write_text(VALID, encoding="utf-8")
            # Undeclared dep.
            bad_dep = VALID.replace("      - skill-alpha\n    provides:\n      - beta/v1",
                                    "      - ghost\n    provides:\n      - beta/v1")
            # Need matching SKILL metadata to reach undeclared check (not metadata mismatch first).
            # Update beta SKILL to depend on ghost as well.
            (root / "skills" / "skill-beta" / "SKILL.md").write_text(
                SKILL_T.format(name="skill-beta", depends="[ghost]", provides="beta/v1"),
                encoding="utf-8")
            (root / "manifest.yaml").write_text(bad_dep, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        # Main.
        with tempfile.TemporaryDirectory() as t:
            root = self._root(t)
            self.assertEqual(VSM.main(["prog", str(root)]), 0)
            self.assertEqual(VSM.main(["prog", str(Path(t) / "missing")]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
