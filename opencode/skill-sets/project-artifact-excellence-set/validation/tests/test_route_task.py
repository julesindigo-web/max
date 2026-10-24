"""Unit tests for task-orchestrator/scripts/route-task.py (v2.1.0).

Deterministic offline classifier: every run must agree. Covers 100% line and
branch of the script (import side + __main__ side via subprocess).
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
ROOT = TEST_DIR.parents[1]
SCRIPT = ROOT / "task-orchestrator" / "scripts" / "route-task.py"

import importlib.util as _ilu


def _load():
    spec = _ilu.spec_from_file_location("route_task", SCRIPT)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rt = _load()


class NormalizeTests(unittest.TestCase):
    def test_collapses_whitespace_and_casefolds(self):
        self.assertEqual(rt.normalize("  Audit\nARSETEKTUR  "), "audit arsetektur")

    def test_empty_string_normalizes_to_empty(self):
        self.assertEqual(rt.normalize("   "), "")


class ClassifyTests(unittest.TestCase):
    def test_id_audit_routes_to_auditor(self):
        r = rt.classify("Lakukan audit arsitektur layanan pembayaran beserta SLO-nya")
        self.assertEqual(r["status"], "routed")
        self.assertEqual(r["route"], "project-artifact-auditor")

    def test_single_keyword_fails_closed(self):
        r = rt.classify("audit")
        self.assertEqual(r["status"], "clarify")
        self.assertEqual(r["candidates"][0], "project-artifact-auditor")

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            rt.classify("   ")

    def test_oversized_rejected(self):
        with self.assertRaises(ValueError):
            rt.classify("x" * 2001)

    def test_tor_positives_route_to_orchestrator(self):
        prompts = [
            "Route this task to the best skill without a slash command and orchestrate the workflow.",
            "Which skill should handle this multi-capability request? Choose automatically.",
            "Rute tugasku ke skill terbaik tanpa perintah slash dan orkestrasi otomatis.",
            "No slash command was given; auto select the workflow and delegate to the right capabilities.",
            "Skill mana yang harus menangani permintaan multi-kemampuan ini? Pilihkan otomatis.",
        ]
        for p in prompts:
            with self.subTest(prompt=p[:40]):
                r = rt.classify(p)
                self.assertEqual(r["status"], "routed", p)
                self.assertEqual(r["route"], "task-orchestrator", p)

    def test_tor_negatives_do_not_route(self):
        for p in [
            "What is the capital of France?",
            "Jelaskan cara membuat nasi goreng yang enak untuk makan malam.",
            "Translate this paragraph into Indonesian.",
            "How do I meditate for ten minutes?",
            "Sebutkan menu makan malam terenak dengan kentang dan telur.",
        ]:
            with self.subTest(prompt=p[:40]):
                self.assertEqual(rt.classify(p)["status"], "clarify", p)

    def test_global_guard_penalizes_all(self):
        r = rt.classify("audit artefak proyek beserta resep nasi goreng")
        self.assertLessEqual(r["ranking"][0]["score"], 1)

    def test_targeted_guard_penalizes_only_target(self):
        r = rt.classify("meme screenshot for slides about owasp auth model", top=14)
        by_skill = {x["skill"]: x["score"] for x in r["ranking"]}
        self.assertLessEqual(by_skill["test-automation-engineer"], 1)
        self.assertGreaterEqual(by_skill["security-vulnerability-auditor"], 1)

    def test_deterministic_across_runs(self):
        text = "Buatkan API backend yang teruji dengan budget latensi di bawah 100ms"
        self.assertEqual(rt.classify(text), rt.classify(text))


class MainTests(unittest.TestCase):
    def test_json_output_routed(self):
        out = self._run(["--text", "Bandingkan screenshot halaman ini dengan baseline", "--json"])
        data = json.loads(out)
        self.assertEqual(data["route"], "test-automation-engineer")

    def test_plain_output_clarify(self):
        out = self._run(["--text", "audit"])
        self.assertIn("clarify", out)

    def test_missing_text_exits_two(self):
        p = subprocess.run(
            [sys.executable, str(ROOT / "task-orchestrator" / "scripts" / "route-task.py")],
            text=True, capture_output=True, timeout=60,
        )
        self.assertEqual(p.returncode, 2)

    def test_plain_output_routed(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(rt.main(["--text", "Route this task to the best skill and orchestrate the workflow."]), 0)
        self.assertIn("route: task-orchestrator", buf.getvalue())

    def test_main_entry_returns(self):
        import io
        from contextlib import redirect_stdout
        with redirect_stdout(io.StringIO()):
            self.assertEqual(rt.main(["--text", "audit"]), 0)
            self.assertEqual(rt.main(["--text", ""]), 2)

    def _run(self, args):
        p = subprocess.run(
            [sys.executable, str(ROOT / "task-orchestrator" / "scripts" / "route-task.py")] + args,
            text=True, capture_output=True, timeout=60,
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout


if __name__ == "__main__":
    unittest.main(verbosity=2)
