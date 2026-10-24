"""Regression tests for semantically meaningful, dimension-specific metrics."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent
sys.path.insert(0, str(ROOT / "validation"))
from validate_metric_specs import MetricSpecError, extract_skill_metrics, validate_metric_list, validate_root, validate_skill_file  # noqa: E402


class MetricSpecTests(unittest.TestCase):
    def test_repository_metric_contracts_pass(self):
        messages = validate_root(ROOT)
        self.assertGreaterEqual(len(messages), 15)

    def test_set_doc_and_manifest_metric_drift_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for item in ("manifest.yaml", "SET.md"):
                shutil.copy2(ROOT / item, root / item)
            for member in ("project-artifact-auditor", "skills-create-excellence"):
                (root / member).mkdir()
                shutil.copy2(ROOT / member / "SKILL.md", root / member / "SKILL.md")
            doc = root / "SET.md"
            content = doc.read_text(encoding="utf-8").replace("Rationale: preserves intended coverage without broad unrelated activation", "Rationale: modified but valid rationale for test purposes")
            doc.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(MetricSpecError, "metric definitions drift"):
                validate_root(root)

    def test_metric_with_all_fields_but_generic_numeric_target_fails(self):
        metrics = extract_skill_metrics(ROOT / "project-artifact-auditor/SKILL.md")
        metrics[0] = metrics[0].replace("Target: ≥90% true-positive/recall and ≤10% false-positive rate", "Target: 123")
        with self.assertRaisesRegex(MetricSpecError, "numeric-only"):
            validate_metric_list(metrics, "mutated fixture")

    def test_trigger_thresholds_are_checked_semantically(self):
        metrics = extract_skill_metrics(ROOT / "project-artifact-auditor/SKILL.md")
        metrics[0] = metrics[0].replace("Target: ≥90% true-positive/recall and ≤10% false-positive rate", "Target: ≥50% true-positive/recall and ≤50% false-positive rate")
        with self.assertRaisesRegex(MetricSpecError, "Trigger performance target must specify"):
            validate_metric_list(metrics, "mutated fixture")

    def test_context_target_must_be_dimension_specific(self):
        metrics = extract_skill_metrics(ROOT / "skills-create-excellence/SKILL.md")
        index = next(i for i, metric in enumerate(metrics) if metric.startswith("Context-token efficiency:"))
        metrics[index] = metrics[index].replace("Target: each SKILL.md ≤500 lines and only task-relevant references are loaded", "Target: 123")
        with self.assertRaisesRegex(MetricSpecError, "numeric-only"):
            validate_metric_list(metrics, "mutated fixture")

    def test_missing_field_fails_closed(self):
        metrics = extract_skill_metrics(ROOT / "project-artifact-auditor/SKILL.md")
        metrics[1] = metrics[1].replace("; Method:", "; Method:", 1)
        # Deliberately remove the data-source label rather than relying on a number check.
        metrics[1] = metrics[1].replace("Source: ", "Data source: ", 1)
        with self.assertRaisesRegex(MetricSpecError, "missing required field.*source"):
            validate_metric_list(metrics, "mutated fixture")

    def test_duplicate_dimension_fails(self):
        metrics = extract_skill_metrics(ROOT / "project-artifact-auditor/SKILL.md")
        metrics.append(metrics[0])
        with self.assertRaisesRegex(MetricSpecError, "duplicate metric dimension"):
            validate_metric_list(metrics, "mutated fixture")

    def test_residual_defects_cannot_be_numeric_placeholder(self):
        metrics = extract_skill_metrics(ROOT / "project-artifact-auditor/SKILL.md")
        index = next(i for i, metric in enumerate(metrics) if metric.startswith("Residual defect density:"))
        metrics[index] = metrics[index].replace("Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance", "Target: 123")
        with self.assertRaisesRegex(MetricSpecError, "numeric-only"):
            validate_metric_list(metrics, "mutated fixture")


if __name__ == "__main__":
    unittest.main(verbosity=2)
