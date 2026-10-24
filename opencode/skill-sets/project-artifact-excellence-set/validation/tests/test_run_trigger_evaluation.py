"""Regression tests for honest trigger-evaluation headers (PA-COV-02)."""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parents[1]
SCORER = ROOT / "scripts/run-trigger-evaluation.py"
MATRIX = ROOT / "evaluation/trigger-evaluation-matrix.json"


def _build_observations(with_method: bool) -> dict:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    activations = []
    for cases in data["skills"].values():
        for c in cases.get("positive", []):
            activations.append({"id": c["id"], "activated": True})
        for c in cases.get("negative", []):
            activations.append({"id": c["id"], "activated": False})
    obs: dict = {"activations": activations}
    if with_method:
        obs["method"] = "independent-semantic-adjudication test sentinel; NOT live-runtime activation"
    return obs


class RunTriggerEvaluationTests(unittest.TestCase):
    def test_runtime_header_is_honest_and_coverage_mode_passes(self):
        # Coverage mode (no observations) must PASS with the frozen wording.
        result = subprocess.run(
            [sys.executable, str(SCORER), "--matrix", str(MATRIX)],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("coverage-only scoring complete", result.stdout)

        # Runtime mode with an explicit method field must echo mode plus method
        # plus the NOT-live-runtime warning.
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            obs_file = temp_root / "obs-with-method.json"
            obs_file.write_text(json.dumps(_build_observations(True)), encoding="utf-8")
            out_file = temp_root / "results-with-method.md"
            result = subprocess.run(
                [sys.executable, str(SCORER), "--matrix", str(MATRIX),
                 "--observations", str(obs_file), "--out", str(out_file)],
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = out_file.read_text(encoding="utf-8")
            self.assertIn("# Trigger Evaluation Results (observation-graded)", report)
            self.assertIn("Adjudication method:", report)
            self.assertIn("independent-semantic-adjudication test sentinel", report)
            self.assertIn("NOT live-runtime", report)

            # Runtime mode without a method field must still carry an honest
            # header via the fallback method line, never the old runtime title.
            obs_no_method = temp_root / "obs-no-method.json"
            obs_no_method.write_text(json.dumps(_build_observations(False)), encoding="utf-8")
            out_no_method = temp_root / "results-no-method.md"
            result = subprocess.run(
                [sys.executable, str(SCORER), "--matrix", str(MATRIX),
                 "--observations", str(obs_no_method), "--out", str(out_no_method)],
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            fallback_report = out_no_method.read_text(encoding="utf-8")
            self.assertIn("# Trigger Evaluation Results (observation-graded)", fallback_report)
            self.assertIn("Adjudication method:", fallback_report)
            self.assertIn("method not declared", fallback_report)
            self.assertIn("NOT live-runtime", fallback_report)
            self.assertNotIn("# Runtime Evaluation Results\n", fallback_report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
