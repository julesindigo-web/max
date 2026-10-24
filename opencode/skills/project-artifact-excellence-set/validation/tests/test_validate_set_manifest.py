"""Negative and positive tests for set manifest composition rules."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parents[1]
VALIDATOR = ROOT / "validation/validate_set_manifest.py"

VALID_MANIFEST = '''name: test-set
version: "1.0.0"
purpose: Test set for manifest checks.
last-reviewed: "2026-10-15"
success-metrics:
  - Trigger performance: ≥90% true positives and ≤10% false positives
  - Task completion: ≥95% of checks pass
  - Context-token efficiency: each SKILL.md remains ≤500 lines
  - Time-to-working-skill: within ≤60 minutes
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
  - Dependency graph must be acyclic.
shared-contracts:
  - shared/contracts/example.json
validation-entry: validation/validate-set.sh
deprecation-policy: Test policy.
migration-notes: Test migration notes.
'''

SKILL_TEMPLATE = '''---
name: {name}
description: Audit or create skill artifacts with measurable quality attributes and trigger rules. Use when a skill validation is requested and trigger phrases identify this work.
metadata:
  version: "1.0.0"
  set-membership: test-set
{depends_yaml}  provides:
{provides}---

## Purpose
Test skill content.

## Core Principles
Apply quality attributes and human factors.

## Success Metrics
- Trigger performance: ≥90% true positive rate and ≤10% false positive rate on at least five positive and five negative prompts.
- Task completion: ≥95% acceptance checks pass.
- Context-token efficiency: SKILL.md remains ≤500 lines.
- Time-to-working-skill: working first result within ≤60 minutes.
- Residual defect density: zero open Critical or Major defects.
'''


class ManifestValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "SET.md").write_text("# Test set\n", encoding="utf-8")
        (self.root / "validation").mkdir()
        (self.root / "validation/validate-set.sh").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        (self.root / "shared/contracts").mkdir(parents=True)
        (self.root / "shared/contracts/example.json").write_text("{}\n", encoding="utf-8")
        for name in ["skill-alpha", "skill-beta"]:
            path = self.root / "skills" / name
            path.mkdir(parents=True)
            if name == "skill-alpha":
                depends = "  depends-on: []\n"
                provides = "    - alpha/v1\n"
            else:
                depends = "  depends-on:\n    - skill-alpha@>=1.0.0\n"
                provides = "    - beta/v1\n"
            (path / "SKILL.md").write_text(SKILL_TEMPLATE.format(name=name, depends_yaml=depends, provides=provides), encoding="utf-8")
        (self.root / "manifest.yaml").write_text(VALID_MANIFEST, encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(self.root)],
            text=True, capture_output=True, check=False,
        )

    def test_valid_manifest_and_dag_pass(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_dependency_cycle_fails(self):
        manifest = VALID_MANIFEST.replace(
            "    depends-on: []\n    provides:\n      - alpha/v1",
            "    depends-on:\n      - skill-beta\n    provides:\n      - alpha/v1",
        )
        (self.root / "manifest.yaml").write_text(manifest, encoding="utf-8")
        alpha_path = self.root / "skills/skill-alpha/SKILL.md"
        alpha_text = alpha_path.read_text(encoding="utf-8").replace("  depends-on: []", "  depends-on:\n    - skill-beta@>=1.0.0")
        alpha_path.write_text(alpha_text, encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dependency cycle detected", result.stderr)

    def test_undeclared_dependency_fails(self):
        manifest = VALID_MANIFEST.replace("      - skill-alpha\n    provides:\n      - beta/v1", "      - not-declared\n    provides:\n      - beta/v1")
        (self.root / "manifest.yaml").write_text(manifest, encoding="utf-8")
        beta_path = self.root / "skills/skill-beta/SKILL.md"
        beta_text = beta_path.read_text(encoding="utf-8").replace("skill-alpha@>=1.0.0", "not-declared@>=1.0.0")
        beta_path.write_text(beta_text, encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("depends on undeclared member", result.stderr)

    def test_unsafe_member_path_fails(self):
        manifest = VALID_MANIFEST.replace("path: skills/skill-alpha", "path: ../skill-alpha")
        (self.root / "manifest.yaml").write_text(manifest, encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe component", result.stderr)

    def test_missing_metric_dimension_fails(self):
        manifest = VALID_MANIFEST.replace("Context-token efficiency:", "Copied metric:")
        (self.root / "manifest.yaml").write_text(manifest, encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required set metric is missing: Context-token efficiency", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
