"""Regression tests for required positive/negative trigger-case coverage."""
from __future__ import annotations
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parents[1]
VALIDATOR = ROOT / "validation/validate_trigger_matrices.py"
MATRIX = ROOT / "evaluation/trigger-evaluation-matrix.json"
SAMPLE_MATRIX = ROOT / "shared/examples/trigger-evaluation-cases.json"

class TriggerMatrixTests(unittest.TestCase):
    def test_repository_matrix_passes(self):
        result = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), str(MATRIX)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_documentation_sample_v1_is_still_supported(self):
        result = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), str(SAMPLE_MATRIX)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_duplicate_case_id_fails(self):
        data = json.loads(MATRIX.read_text(encoding="utf-8"))
        data["skills"]["project-artifact-auditor"]["negative"][0]["id"] = data["skills"]["project-artifact-auditor"]["positive"][0]["id"]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "matrix.json"
            temp_file.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), str(temp_file)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate trigger case id", result.stderr)

    def test_authoritative_matrix_cannot_claim_runtime_results(self):
        data = json.loads(MATRIX.read_text(encoding="utf-8"))
        data["evaluation_type"] = "measured-runtime-results"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "matrix.json"
            temp_file.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), str(temp_file)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("candidate test set", result.stderr)

    def test_missing_negative_prompt_fails(self):
        data = json.loads(MATRIX.read_text(encoding="utf-8"))
        data["skills"]["project-artifact-auditor"]["negative"] = data["skills"]["project-artifact-auditor"]["negative"][:4]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "matrix.json"
            temp_file.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), str(temp_file)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("at least five negative prompts", result.stderr)

    def test_overlap_between_positive_negative_fails(self):
        data = json.loads(MATRIX.read_text(encoding="utf-8"))
        data["skills"]["skills-create-excellence"]["negative"][0]["prompt"] = data["skills"]["skills-create-excellence"]["positive"][0]["prompt"]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "matrix.json"
            temp_file.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), str(temp_file)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prompt appears more than once", result.stderr)

if __name__ == "__main__":
    unittest.main(verbosity=2)
