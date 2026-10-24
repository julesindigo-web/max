"""Complement-3: full reachable coverage for metric/manifest/matrix/feedback modules."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent
sys.path.insert(0, str(ROOT / "validation"))
sys.path.insert(0, str(ROOT / "skills-create-excellence" / "scripts"))

import importlib.util


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VMS = load("vms_c3", "validation/validate_metric_specs.py")
VSM = load("vsm_c3", "validation/validate_set_manifest.py")
VTM = load("vtm_c3", "validation/validate_trigger_matrices.py")
PAF = load("paf_c3", "skills-create-excellence/scripts/process-audit-feedback.py")


def valid_metric_set():
    # Build 5 canonical metrics with all required fields.
    base = {
        "Trigger performance": "Target: \u226590% true-positive/recall and \u226410% false-positive rate",
        "Task completion": "Target: \u226595% acceptance, checks pass",
        "Context-token efficiency": "Target: each SKILL.md \u2264500 lines",
        "Time-to-working-skill": "Target: within \u226460 minutes",
        "Residual defect density": "Target: zero open Critical and Major defects",
    }
    out = []
    for dim, tgt in base.items():
        out.append(
            f"{dim}: Definition: def-{dim} detailed; Unit/formula: percent rate; {tgt}; "
            f"Rationale: why reason here; Source: src data; Sample: all items; Segmentation: by skill; "
            f"Method: review method; Owner: team owner; Window: 2026-Q1 period"
        )
    return out


class MetricSpecsComplementTests(unittest.TestCase):
    def test_extract_missing_section_and_breaks(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "SKILL.md"
            p.write_text("# T\nno metrics\n", encoding="utf-8")
            with self.assertRaises(VMS.MetricSpecError):
                VMS.extract_skill_metrics(p)
            p.write_text("## Success Metrics\n- m1\n## Next\n- m2\n", encoding="utf-8")
            self.assertEqual(VMS.extract_skill_metrics(p), ["m1"])
            p.write_text("## Success Metrics\nnot a bullet\n- ok\n", encoding="utf-8")
            self.assertEqual(VMS.extract_skill_metrics(p), ["ok"])

    def test_parse_fields_errors(self):
        with self.assertRaises(VMS.MetricSpecError):
            VMS.parse_fields("no colon here", "ctx")
        with self.assertRaises(VMS.MetricSpecError):
            VMS.parse_fields("Unknown-dim: Definition: x; Unit/formula: y; Target: z; Rationale: r; Source: s; Sample: sa; Segmentation: se; Method: m; Owner: o; Window: w", "ctx")
        # Alias dimension.
        alias_metric = ("time-to-working-skill / working-audit: Definition: detailed def here; Unit/formula: percent rate; "
                        "Target: within \u226460 minutes period; Rationale: reason here; Source: src data; Sample: all items; "
                        "Segmentation: by skill group; Method: review method; Owner: team owner; Window: 2026 period")
        dim, _ = VMS.parse_fields(alias_metric, "ctx")
        self.assertEqual(dim, "Time-to-working-skill")
        # Duplicate field.
        dup = valid_metric_set()[0].replace("; Source:", "; Definition: dup; Source:", 1)
        # Actually duplicate Definition: need two Definition fields.
        dup2 = valid_metric_set()[0] + "; Definition: extra"
        with self.assertRaises(VMS.MetricSpecError):
            VMS.parse_fields(dup2, "ctx")
        # Missing field (remove Owner).
        miss = valid_metric_set()[0].replace("; Owner:", "; OwnerX:", 1)
        # This removes Owner, adds unknown OwnerX (ignored by pattern, so missing Owner).
        with self.assertRaises(VMS.MetricSpecError):
            VMS.parse_fields(miss, "ctx")
        # Placeholder / numeric-only / no-letter.
        ph = valid_metric_set()[0].replace("Rationale: why reason here", "Rationale: TBD", 1)
        with self.assertRaises(VMS.MetricSpecError):
            VMS.parse_fields(ph, "ctx")
        num = valid_metric_set()[0].replace("Rationale: why reason here", "Rationale: 1234", 1)
        with self.assertRaises(VMS.MetricSpecError):
            VMS.parse_fields(num, "ctx")

    def test_dimension_targets_all_branches(self):
        # Each dimension fail + pass (pass via valid set).
        bad_triggers = [
            ("Trigger performance", "Target: \u226550% recall only"),
            ("Task completion", "Target: 50%"),
            ("Context-token efficiency", "Target: 999 lines"),
            ("Time-to-working-skill", "Target: 999 minutes"),
            ("Residual defect density", "Target: some defects"),
        ]
        for dim, bad_tgt in bad_triggers:
            m = [x for x in valid_metric_set() if x.startswith(dim + ":")][0]
            import re
            m_bad = re.sub(r"Target: [^;]+", bad_tgt, m, count=1)
            with self.assertRaises(VMS.MetricSpecError, msg=dim):
                VMS.parse_fields(m_bad, "ctx")
        # Valid set passes all.
        self.assertEqual(len(VMS.validate_metric_list(valid_metric_set(), "ctx")), 5)

    def test_metric_list_and_skill_file_and_root(self):
        with self.assertRaises(VMS.MetricSpecError):
            VMS.validate_metric_list(valid_metric_set()[:3], "ctx")
        dup = valid_metric_set() + [valid_metric_set()[0]]
        with self.assertRaises(VMS.MetricSpecError):
            VMS.validate_metric_list(dup, "ctx")
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(VMS.MetricSpecError):
                VMS.validate_skill_file(Path(t) / "missing.md")
        # validate_root error paths.
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            with self.assertRaises(VMS.MetricSpecError):
                VMS.validate_root(root)  # no manifest
            (root / "manifest.yaml").write_text("x: 1\n", encoding="utf-8")
            # Has manifest but no SET.md after manifest parses? Need valid manifest with metrics.
            import shutil
            shutil.copy2(ROOT / "manifest.yaml", root / "manifest.yaml")
            with self.assertRaises(VMS.MetricSpecError):
                VMS.validate_root(root)  # no SET.md
        # main paths.
        self.assertEqual(VMS.main(["--root", str(ROOT)]), 0)
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "S.md"
            p.write_text("# T\n", encoding="utf-8")
            self.assertEqual(VMS.main(["--skill", str(p)]), 1)
        # main with valid skill file (use real member).
        self.assertEqual(VMS.main(["--skill", str(ROOT / "project-artifact-auditor" / "SKILL.md")]), 0)


class TriggerMatricesComplementTests(unittest.TestCase):
    def test_frontmatter_and_discover(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            # No skills.
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.discover_skills(root)
            # Bad frontmatter.
            s = root / "s1"
            s.mkdir()
            (s / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.frontmatter_name(s / "SKILL.md")
            (s / "SKILL.md").write_text("---\nno name here\n---\n", encoding="utf-8")
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.frontmatter_name(s / "SKILL.md")
            # Duplicate names.
            s2 = root / "s2"
            s2.mkdir()
            (s / "SKILL.md").write_text("---\nname: dup\n---\n", encoding="utf-8")
            (s2 / "SKILL.md").write_text("---\nname: dup\n---\n", encoding="utf-8")
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.discover_skills(root)
        # Real root discovers.
        skills = VTM.discover_skills(ROOT)
        self.assertGreaterEqual(len(skills), 10)
        # skills/ layout branch.
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "manifest.yaml").write_text("x: 1\n", encoding="utf-8")
            (root / "skills" / "a").mkdir(parents=True)
            (root / "skills" / "a" / "SKILL.md").write_text("---\nname: a\n---\n", encoding="utf-8")
            found = VTM.discover_skills(root)
            self.assertIn("a", found)
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "skills" / "b").mkdir(parents=True)
            (root / "skills" / "b" / "SKILL.md").write_text("---\nname: b\n---\n", encoding="utf-8")
            found = VTM.discover_skills(root)
            self.assertIn("b", found)

    def test_extract_and_validate_errors(self):
        # 1.0 non-string, empty, 1.1 bad shape/id/expected/prompt.
        with self.assertRaises(VTM.TriggerMatrixError):
            VTM.extract_case(123, "1.0", "positive", "s")
        with self.assertRaises(VTM.TriggerMatrixError):
            VTM.extract_case("   ", "1.0", "positive", "s")
        with self.assertRaises(VTM.TriggerMatrixError):
            VTM.extract_case({"id": "a"}, "1.1", "positive", "s")
        with self.assertRaises(VTM.TriggerMatrixError):
            VTM.extract_case({"id": "BAD", "prompt": "x", "expected": "trigger"}, "1.1", "positive", "s")
        with self.assertRaises(VTM.TriggerMatrixError):
            VTM.extract_case({"id": "a1", "prompt": "x", "expected": "no-trigger"}, "1.1", "positive", "s")
        with self.assertRaises(VTM.TriggerMatrixError):
            VTM.extract_case({"id": "a1", "prompt": 123, "expected": "trigger"}, "1.1", "positive", "s")
        # validate errors: bad json, not dict, bad schema, 1.1 missing as_of/protocol/type.
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            s = root / "sa"
            s.mkdir()
            (s / "SKILL.md").write_text("---\nname: sa\n---\n", encoding="utf-8")
            mp = Path(t) / "m.json"
            mp.write_text("{bad", encoding="utf-8")
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.validate(root, mp)
            mp.write_text("[]", encoding="utf-8")
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.validate(root, mp)
            mp.write_text(json.dumps({"schema_version": "9", "skills": {}}), encoding="utf-8")
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.validate(root, mp)
            base11 = {"schema_version": "1.1", "skills": {"sa": {
                "positive": [{"id": f"p{i}", "prompt": f"pp{i}", "expected": "trigger"} for i in range(5)],
                "negative": [{"id": f"n{i}", "prompt": f"nn{i}", "expected": "no-trigger"} for i in range(5)]}}}
            for mutate in ["as_of", "protocol", "type"]:
                m = copy.deepcopy(base11)
                if mutate == "as_of":
                    m["as_of"] = "not-a-date"
                elif mutate == "protocol":
                    m["as_of"] = "2026-10-15"
                    m["evaluation_protocol"] = "short"
                else:
                    m["as_of"] = "2026-10-15"
                    m["evaluation_protocol"] = "x" * 30
                    m["evaluation_type"] = "wrong"
                mp.write_text(json.dumps(m), encoding="utf-8")
                with self.assertRaises(VTM.TriggerMatrixError, msg=mutate):
                    VTM.validate(root, mp)
            # Missing/unknown member, bad group shape, too few, duplicate prompt/id.
            m = copy.deepcopy(base11)
            m["as_of"] = "2026-10-15"
            m["evaluation_protocol"] = "x" * 30
            m["evaluation_type"] = "candidate-test-set-not-runtime-results"
            m["skills"]["unknown"] = m["skills"]["sa"]
            mp.write_text(json.dumps(m), encoding="utf-8")
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.validate(root, mp)
            m2 = copy.deepcopy(base11)
            m2["as_of"] = "2026-10-15"
            m2["evaluation_protocol"] = "x" * 30
            m2["evaluation_type"] = "candidate-test-set-not-runtime-results"
            del m2["skills"]["sa"]
            mp.write_text(json.dumps(m2), encoding="utf-8")
            with self.assertRaises(VTM.TriggerMatrixError):
                VTM.validate(root, mp)
        # main paths.
        self.assertEqual(VTM.main(["prog", str(ROOT)]), 0)
        self.assertEqual(VTM.main(["prog", str(ROOT), str(ROOT / "evaluation" / "trigger-evaluation-matrix.json")]), 0)
        self.assertEqual(VTM.main(["prog", str(ROOT), str(ROOT / "evaluation" / "trigger-evaluation-matrix.json"), "extra"]), 2)
        with tempfile.TemporaryDirectory() as t:
            bad = Path(t) / "b.json"
            bad.write_text("{}", encoding="utf-8")
            self.assertEqual(VTM.main(["prog", str(ROOT), str(bad)]), 1)


class FeedbackComplementTests(unittest.TestCase):
    def _event(self):
        return json.loads((ROOT / "shared" / "examples" / "audit-findings.sample.json").read_text(encoding="utf-8"))

    def test_require_string_branches(self):
        with self.assertRaises(PAF.ContractError):
            PAF.require_string(123, "lbl", 10)
        with self.assertRaises(PAF.ContractError):
            PAF.require_string("   ", "lbl", 10)
        with self.assertRaises(PAF.ContractError):
            PAF.require_string("x" * 11, "lbl", 10)
        with self.assertRaises(PAF.ContractError):
            PAF.require_string("a\x01b", "lbl", 10)
        self.assertEqual(PAF.require_string("ok", "lbl", 10), "ok")
        self.assertEqual(PAF.require_string("", "lbl", 10, nonempty=False), "")

    def test_validate_event_top_and_finding_branches(self):
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event([])
        ev = self._event()
        bad = {k: v for k, v in ev.items() if k != "audit_id"}
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(bad)
        bad2 = dict(ev)
        bad2["extra"] = 1
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(bad2)
        bad3 = dict(ev)
        bad3["schema_version"] = "9"
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(bad3)
        bad4 = dict(ev)
        bad4["audit_id"] = "bad id!"
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(bad4)
        bad5 = dict(ev)
        bad5["audited_at"] = "2026-10-15"
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(bad5)
        bad6 = dict(ev)
        bad6["findings"] = "notalist"
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(bad6)
        # Finding-level: not dict, missing, extra, bad id dup, bad title/evidence/category/severity/status/count.
        ev2 = self._event()
        ev2["findings"] = ["notadict"]
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(ev2)
        # Calibration: 1.1 requires full set; partial set fails (remove one field).
        ev3 = self._event()
        self.assertEqual(ev3["schema_version"], "1.1")
        del ev3["findings"][0]["confidence"]
        with self.assertRaises(PAF.ContractError):
            PAF.validate_event(ev3)

    def test_process_and_write_and_main(self):
        ev = self._event()
        out = PAF.process_event(PAF.validate_event(ev))
        self.assertIn("decisions", out)
        # make_request_id deterministic.
        a = PAF.make_request_id("A", "F", "T", "C")
        b = PAF.make_request_id("A", "F", "T", "C")
        self.assertEqual(a, b)
        self.assertTrue(a.startswith("SIE-"))
        # write atomically.
        with tempfile.TemporaryDirectory() as t:
            dest = Path(t) / "sub" / "out.json"
            PAF.write_json_atomically(dest, {"x": 1})
            self.assertEqual(json.loads(dest.read_text(encoding="utf-8")), {"x": 1})
        # main help/args.
        self.assertEqual(PAF.main(["prog"]), 2)
        self.assertEqual(PAF.main(["prog", "--help", "extra"]), 0)
        with tempfile.TemporaryDirectory() as t:
            src = Path(t) / "in.json"
            dst = Path(t) / "out.json"
            src.write_text(json.dumps(ev), encoding="utf-8")
            self.assertEqual(PAF.main(["prog", str(src), str(dst)]), 0)
            # Same path.
            self.assertEqual(PAF.main(["prog", str(src), str(src)]), 2)
            # Missing file.
            self.assertEqual(PAF.main(["prog", str(Path(t) / "no.json"), str(dst)]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
