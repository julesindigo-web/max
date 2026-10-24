"""Regression tests for the audit-to-skill feedback processor (stdlib only)."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parents[2]
PROCESSOR = ROOT / "skills-create-excellence/scripts/process-audit-feedback.py"
SAMPLE = ROOT / "shared/examples/audit-findings.sample.json"


class FeedbackProcessorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name)
        self.input_path = self.work / "input.json"
        self.output_path = self.work / "output.json"
        self.event = json.loads(SAMPLE.read_text(encoding="utf-8"))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_processor(self, event=None):
        if event is not None:
            self.input_path.write_text(json.dumps(event), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(PROCESSOR), str(self.input_path), str(self.output_path)],
            text=True, capture_output=True, check=False,
        )

    def test_sample_generates_only_eligible_request(self):
        self.input_path.write_text(json.dumps(self.event), encoding="utf-8")
        result = self.run_processor()
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual(output["processing_summary"]["findings_seen"], 2)
        self.assertEqual(output["processing_summary"]["requests_generated"], 1)
        self.assertEqual(output["requests"][0]["target_skill"], "project-artifact-auditor")
        self.assertTrue(output["requests"][0]["requires_human_approval"])
        self.assertTrue(output["requests"][0]["do_not_modify_skill_automatically"])
        decisions = {item["finding_id"]: item for item in output["decisions"]}
        self.assertEqual(decisions["AUD-013"]["reason"], "no_skill_gap_signal_or_recurrence")

    def test_cross_cutting_finding_maps_to_both_skills(self):
        event = copy.deepcopy(self.event)
        event["findings"] = [event["findings"][0]]
        event["findings"][0]["category"] = "cross-cutting"
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual({r["target_skill"] for r in output["requests"]}, {
            "project-artifact-auditor", "skills-create-excellence"
        })

    def test_resolved_finding_does_not_trigger(self):
        event = copy.deepcopy(self.event)
        event["findings"] = [event["findings"][0]]
        event["findings"][0]["status"] = "resolved"
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual(output["requests"], [])
        self.assertEqual(output["decisions"][0]["reason"], "finding_not_open")

    def test_repeated_finding_triggers_without_explicit_suspicion(self):
        event = copy.deepcopy(self.event)
        finding = copy.deepcopy(event["findings"][1])
        finding["recurrence_count"] = 2
        finding["recurrence_observation_ids"] = ["AUD-2026-10-08-001", event["audit_id"]]
        event["findings"] = [finding]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual(len(output["requests"]), 1)
        self.assertEqual(output["decisions"][0]["reason"], "recurrence_threshold_met")

    def test_recurrence_count_without_observation_evidence_does_not_trigger(self):
        event = copy.deepcopy(self.event)
        finding = copy.deepcopy(event["findings"][1])
        finding["recurrence_count"] = 2
        finding.pop("recurrence_observation_ids", None)
        event["findings"] = [finding]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual(output["requests"], [])
        self.assertEqual(output["decisions"][0]["reason"], "recurrence_evidence_missing")

    def test_duplicate_or_mismatched_observation_evidence_fails_closed(self):
        event = copy.deepcopy(self.event)
        finding = copy.deepcopy(event["findings"][0])
        finding["recurrence_observation_ids"] = [event["audit_id"], event["audit_id"]]
        event["findings"] = [finding]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("must contain distinct audit IDs", result.stderr)

    def test_malformed_observation_id_type_fails_closed(self):
        event = copy.deepcopy(self.event)
        finding = copy.deepcopy(event["findings"][0])
        finding["recurrence_observation_ids"] = [event["audit_id"], {"not": "an id"}]
        finding["recurrence_count"] = 2
        event["findings"] = [finding]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be a string", result.stderr)

    def test_recurrence_observations_must_include_current_audit(self):
        event = copy.deepcopy(self.event)
        finding = copy.deepcopy(event["findings"][0])
        finding["recurrence_observation_ids"] = ["AUD-2026-10-01-001", "AUD-2026-10-08-001"]
        event["findings"] = [finding]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("must include the current audit_id", result.stderr)

    def test_explicit_skill_gap_signal_can_trigger_without_recurrence_ids(self):
        event = copy.deepcopy(self.event)
        finding = copy.deepcopy(event["findings"][0])
        finding["skill_gap_suspected"] = True
        finding.pop("recurrence_observation_ids", None)
        event["findings"] = [finding]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual(len(output["requests"]), 1)
        self.assertEqual(output["decisions"][0]["reason"], "explicit_skill_gap_signal")

    def test_invalid_category_fails_closed(self):
        event = copy.deepcopy(self.event)
        event["findings"][0]["category"] = "run-shell-command"
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("not a supported category", result.stderr)
        self.assertFalse(self.output_path.exists())

    def test_unknown_top_level_field_fails_closed(self):
        event = copy.deepcopy(self.event)
        event["auto_apply"] = True
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown top-level field", result.stderr)

    def test_duplicate_finding_id_fails_closed(self):
        event = copy.deepcopy(self.event)
        event["findings"][1]["id"] = event["findings"][0]["id"]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate finding id", result.stderr)

    def test_output_is_deterministic(self):
        self.input_path.write_text(json.dumps(self.event), encoding="utf-8")
        result1 = self.run_processor()
        self.assertEqual(result1.returncode, 0, result1.stderr)
        first = self.output_path.read_bytes()
        result2 = self.run_processor()
        self.assertEqual(result2.returncode, 0, result2.stderr)
        self.assertEqual(first, self.output_path.read_bytes())

    def test_empty_findings_list_succeeds_with_empty_requests(self):
        event = copy.deepcopy(self.event)
        event["findings"] = []
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual(output.get("requests", []), [])

    def test_unsupported_schema_version_fails_closed(self):
        event = copy.deepcopy(self.event)
        event["schema_version"] = "9.9"
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(
            "schema_version" in result.stderr.lower() or "unsupported" in result.stderr.lower() or "const" in result.stderr.lower(),
            result.stderr,
        )

    def test_missing_required_top_level_field_fails_closed(self):
        event = copy.deepcopy(self.event)
        del event["audit_id"]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(
            "audit_id" in result.stderr.lower() or "required" in result.stderr.lower(),
            result.stderr,
        )

    def test_calibration_metadata_is_propagated_to_generated_requests(self):
        event = copy.deepcopy(self.event)
        event["findings"] = [event["findings"][0]]
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        calibration = output["requests"][0]["evidence_calibration"]
        self.assertEqual(calibration["evidence_status"], "verified")
        self.assertEqual(calibration["severity_basis"], "observed_impact")
        self.assertTrue(calibration["verification_method"])

    def test_unknown_evidence_cannot_use_unconditional_major_severity(self):
        event = copy.deepcopy(self.event)
        finding = event["findings"][0]
        finding["evidence_status"] = "unknown_untested"
        finding["severity_basis"] = "mandatory_control_gap"
        finding["impact_rationale"] = "This is a severe issue with broad impact."
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires severity_basis='conditional_risk'", result.stderr)

    def test_unknown_major_conditional_risk_requires_conditional_rationale(self):
        event = copy.deepcopy(self.event)
        finding = event["findings"][0]
        finding["evidence_status"] = "unknown_untested"
        finding["severity_basis"] = "conditional_risk"
        finding["impact_rationale"] = "Major impact has not been established."
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicitly state the conditional nature", result.stderr)

    def test_unknown_major_with_explicit_conditional_risk_is_accepted(self):
        event = copy.deepcopy(self.event)
        finding = event["findings"][0]
        finding["evidence_status"] = "unknown_untested"
        finding["severity_basis"] = "conditional_risk"
        finding["impact_rationale"] = "If the untested control is absent, this could materially affect release safety."
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_legacy_schema_10_input_remains_supported(self):
        event = copy.deepcopy(self.event)
        event["schema_version"] = "1.0"
        for finding in event["findings"]:
            for field in ("evidence_status", "confidence", "verification_method", "as_of_context", "impact_rationale", "severity_basis"):
                finding.pop(field, None)
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertNotIn("evidence_calibration", output["requests"][0])

    def test_schema_11_fails_closed_when_calibration_field_missing(self):
        event = copy.deepcopy(self.event)
        event["findings"][0].pop("evidence_status")
        result = self.run_processor(event)
        self.assertEqual(result.returncode, 2)
        self.assertIn("schema 1.1 requires calibration field", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
