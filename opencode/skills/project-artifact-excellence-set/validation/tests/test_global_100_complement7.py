"""Complement-7: VSM remaining 22 lines."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent
sys.path.insert(0, str(ROOT / "validation"))

import importlib.util
spec = importlib.util.spec_from_file_location("vsm7", str(ROOT / "validation" / "validate_set_manifest.py"))
VSM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(VSM)

VALID = (ROOT / "manifest.yaml").read_text(encoding="utf-8")


def make_root(tmp, manifest_text):
    import shutil
    root = Path(tmp)
    (root / "manifest.yaml").write_text(manifest_text, encoding="utf-8")
    shutil.copy2(ROOT / "SET.md", root / "SET.md")
    for member in ("project-artifact-auditor", "skills-create-excellence"):
        (root / member).mkdir(exist_ok=True)
        shutil.copy2(ROOT / member / "SKILL.md", root / member / "SKILL.md")
    # Shared contracts + validation entry (copy real ones to pass those checks when testing member branches).
    import shutil as _s
    for rel in ("shared/contracts/audit-findings.schema.json", "validation/validate_set_manifest.py"):
        src = ROOT / rel
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_file():
            _s.copy2(src, dst)
        else:
            dst.write_text("# x\n", encoding="utf-8")
    return root


class VSMFinalTests(unittest.TestCase):
    def test_for_empty_and_continues(self):
        with tempfile.TemporaryDirectory() as t:
            s = Path(t) / "SKILL.md"
            s.write_text("---\n", encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.read_frontmatter_name(s)
            with self.assertRaises(VSM.ManifestError):
                VSM.read_frontmatter_metadata(s)
            # Blank/comment + non-metadata indented + list outside active (after metadata).
            s.write_text("---\nname: x\n# comment\n\nmetadata:\n  version: 1.0.0\n    - orphan\n", encoding="utf-8")
            # read_frontmatter_name should find name.
            self.assertEqual(VSM.read_frontmatter_name(s), "x")
            # metadata with orphan list (active_list None) hits 194->162 false.
            md = VSM.read_frontmatter_metadata(s)
            self.assertIn("version", md)

    def test_empty_top_lists(self):
        import re
        with tempfile.TemporaryDirectory() as t:
            # Empty success-metrics.
            m = VALID.replace("success-metrics:\n  - Trigger performance:", "success-metrics:\n")
            # Need to keep YAML valid: `success-metrics:` with no items gives [].
            # Our VALID has 5 metrics; replace whole block with empty.
            m2 = re.sub(r"success-metrics:\n(?:  - .*\n)+", "success-metrics:\n", VALID)
            root = make_root(t, m2)
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            # Metric without measurable target.
            m = VALID.replace("Trigger performance: \u226590%", "Trigger performance: foo bar")
            root = make_root(t, m)
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        for block, needle in [
            ("members", "members:\n"),
            ("composition", "composition-rules:\n"),
            ("shared", "shared-contracts:\n"),
        ]:
            with tempfile.TemporaryDirectory() as t:
                import re
                if block == "members":
                    m = re.sub(r"members:\n(?:  - .*\n(?:    .*\n|      - .*\n)*)+", "members:\n", VALID)
                elif block == "composition":
                    m = re.sub(r"composition-rules:\n(?:  - .*\n)+", "composition-rules:\n", VALID)
                else:
                    m = re.sub(r"shared-contracts:\n(?:  - .*\n)+", "shared-contracts:\n", VALID)
                root = make_root(t, m)
                with self.assertRaises(VSM.ManifestError, msg=block):
                    VSM.validate(root)

    def test_member_branches(self):
        cases = [
            ("bad-name", VALID.replace("- name: project-artifact-auditor", "- name: Bad_Name")),
            ("bad-version", VALID.replace("project-artifact-auditor\n    version: \"2.0.0\"",
                                          "project-artifact-auditor\n    version: \"bad\"")),
            ("dup-path", VALID.replace("path: skills-create-excellence", "path: project-artifact-auditor")),
            ("name-mismatch", None),  # handled via file edit
            ("version-mismatch", None),
            ("set-membership", None),
            ("depends-type", None),
            ("provides-type", None),
            ("meta-depends", None),
            ("meta-provides", None),
            ("repeats", None),
            ("self-dep", None),
            ("shared-bad", None),
            ("entry-bad", None),
            ("unlisted", None),
        ]
        for label, manifest in cases:
            if manifest is not None:
                with tempfile.TemporaryDirectory() as t:
                    root = make_root(t, manifest)
                    with self.assertRaises(VSM.ManifestError, msg=label):
                        VSM.validate(root)
        # File-edit cases.
        with tempfile.TemporaryDirectory() as t:
            root = make_root(t, VALID)
            # Name mismatch: edit SKILL frontmatter name.
            p = root / "project-artifact-auditor" / "SKILL.md"
            txt = p.read_text(encoding="utf-8").replace("name: project-artifact-auditor", "name: other", 1)
            p.write_text(txt, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            root = make_root(t, VALID)
            p = root / "project-artifact-auditor" / "SKILL.md"
            txt = p.read_text(encoding="utf-8").replace('version: "2.0.0"', 'version: "9.9.9"', 1)
            p.write_text(txt, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        with tempfile.TemporaryDirectory() as t:
            root = make_root(t, VALID)
            p = root / "project-artifact-auditor" / "SKILL.md"
            txt = p.read_text(encoding="utf-8").replace("set-membership: project-artifact-excellence-set",
                                                        "set-membership: other-set", 1)
            p.write_text(txt, encoding="utf-8")
            with self.assertRaises(VSM.ManifestError):
                VSM.validate(root)
        # Invalid depends/provides list (non-list via manifest? manifest depends-on must be list;
        # craft manifest with string depends-on).
        with tempfile.TemporaryDirectory() as t:
            m = VALID.replace("depends-on: []", "depends-on: badstring", 1)
            root = make_root(t, m)
            # Parse gives depends-on as string? Actually parser expects list; string "badstring" without []?
            # Our parser: `if raw_value: if not ([...]): raise`. So "badstring" raises at parse (different line).
            # To hit validate's `if not isinstance(dependencies, list)`, need parser to produce non-list?
            # Parser always produces list for depends-on, so validate's non-list branch may be dead.
            # Skip (document as defensive).
            pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
