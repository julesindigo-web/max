"""Regression tests for the design-tokens contract gate (PA-DSY-02)."""
from __future__ import annotations
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parents[1]
SCRIPT = ROOT / "scripts/check-design-tokens.py"


class DesignTokensTests(unittest.TestCase):
    def test_repository_contract_passes(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(ROOT)],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_section_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            contract_dir = temp_root / "human-centric-visual-excellence/references"
            contract_dir.mkdir(parents=True)
            (contract_dir / "design-tokens-and-components.md").write_text(
                "# Design Tokens and Components Contract\n", encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(temp_root)],
                text=True, capture_output=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required section", result.stderr)

    def test_invalid_tokens_json_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            contract_dir = temp_root / "human-centric-visual-excellence/references"
            contract_dir.mkdir(parents=True)
            source = (
                ROOT / "human-centric-visual-excellence/references"
                / "design-tokens-and-components.md"
            ).read_text(encoding="utf-8")
            (contract_dir / "design-tokens-and-components.md").write_text(
                source, encoding="utf-8"
            )
            (temp_root / "tokens.json").write_text("{not valid json", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(temp_root)],
                text=True, capture_output=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("tokens.json", result.stderr)


if __name__ == "__main__":
    unittest.main()
