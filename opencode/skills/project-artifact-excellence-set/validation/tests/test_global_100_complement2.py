"""Complement-2: reachable-branch coverage for release/validation/trigger modules.

Direct-import tests (no subprocess) exercising error paths, edge cases,
and negative fixtures. Meaningful assertions on return codes and messages.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent
sys.path.insert(0, str(ROOT / "validation"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skills-create-excellence" / "scripts"))

import importlib.util


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BUILD = load("build_release_mod", "scripts/build-release.py")
VERIFY = load("verify_release_mod", "scripts/verify-release.py")
TOKENS = load("check_design_tokens_mod", "scripts/check-design-tokens.py")
TRIGEVAL = load("run_trigger_eval_mod", "scripts/run-trigger-evaluation.py")
RAU = load("rau_mod", "scripts/release_artifact_utils.py")


class BuildReleaseTests(unittest.TestCase):
    def test_collect_symlink_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "real.txt").write_text("x", encoding="utf-8")
            (root / "link.txt").symlink_to(root / "real.txt")
            with self.assertRaisesRegex(ValueError, "symlink"):
                BUILD.collect_files(root)

    def test_build_rejects_bad_root_and_inside_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "proj"
            root.mkdir()
            (root / "f.txt").write_text("x", encoding="utf-8")
            # Output inside tree.
            with self.assertRaisesRegex(ValueError, "outside the source tree"):
                BUILD.build(root, root / "out.zip", 946684800)
            with self.assertRaisesRegex(ValueError, "outside the source tree"):
                BUILD.build(root, root, 946684800)
            # Root not a directory (file).
            with self.assertRaises(Exception):
                BUILD.build(root / "f.txt", Path(temp) / "o.zip", 946684800)
            # Empty tree.
            empty = Path(temp) / "empty"
            empty.mkdir()
            with self.assertRaisesRegex(ValueError, "no package files"):
                BUILD.build(empty, Path(temp) / "o2.zip", 946684800)

    def test_build_temp_exists_and_main_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "proj"
            root.mkdir()
            (root / "a.txt").write_text("hello", encoding="utf-8")
            out = Path(temp) / "r.zip"
            # Pre-create .tmp to hit unlink-before-write branch.
            tmp = out.with_name(out.name + ".tmp")
            tmp.write_text("stale", encoding="utf-8")
            res = BUILD.build(root, out, 946684800)
            self.assertIn("sha256", res)
            self.assertTrue(out.is_file())
            # main success + failure.
            self.assertEqual(BUILD.main(["--root", str(root), "--output", str(Path(temp) / "m.zip")]), 0)
            self.assertEqual(BUILD.main(["--root", str(root), "--output", str(root / "inside.zip")]), 1)
            # sha256 helper.
            self.assertEqual(BUILD.sha256(b"abc"), hashlib.sha256(b"abc").hexdigest())
            # main with bad epoch string via env.
            import os
            old = os.environ.get("SOURCE_DATE_EPOCH")
            os.environ["SOURCE_DATE_EPOCH"] = "not-an-int"
            try:
                # Must fail gracefully (ValueError -> caught? main catches OSError/ValueError/zipfile).
                # int("not-an-int") raises ValueError before build; main catches? It catches
                # OSError/ValueError/zipfile around build, but int() is inside try, so returns 1.
                rc = BUILD.main(["--root", str(root), "--output", str(Path(temp) / "e.zip")])
                self.assertEqual(rc, 1)
            finally:
                if old is None:
                    os.environ.pop("SOURCE_DATE_EPOCH", None)
                else:
                    os.environ["SOURCE_DATE_EPOCH"] = old


class VerifyReleaseTests(unittest.TestCase):
    @staticmethod
    def _fixture_src(tmpdir):
        # Hermetic source tree with every path verify() requires, so these
        # tests pass on any root (canonical or pruned runtime mirror).
        src = Path(tmpdir) / "src"
        (src / "evaluation").mkdir(parents=True)
        (src / "SET.md").write_text("# T\n", encoding="utf-8")
        (src / "manifest.yaml").write_text("name: t\n", encoding="utf-8")
        (src / "evaluation" / "trigger-evaluation-matrix.json").write_text("{}", encoding="utf-8")
        for rel in RAU.EXECUTABLE_PATHS:
            p = src / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("#!/bin/sh\n", encoding="utf-8")
        return src

    def _good_zip(self, tmpdir):
        out = Path(tmpdir) / "good.zip"
        rc = BUILD.main(["--root", str(self._fixture_src(tmpdir)), "--output", str(out), "--epoch", "946684800"])
        self.assertEqual(rc, 0)
        return out

    def test_verify_good_and_main(self):
        with tempfile.TemporaryDirectory() as temp:
            good = self._good_zip(temp)
            msgs = VERIFY.verify(good)
            self.assertEqual(len(msgs), 3)
            self.assertEqual(VERIFY.main([str(good)]), 0)
            self.assertEqual(VERIFY.main([str(Path(temp) / "missing.zip")]), 1)

    def test_verify_rejects_duplicates_unsafe_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            good = self._good_zip(temp)
            # Duplicate entry names.
            dup = Path(temp) / "dup.zip"
            with zipfile.ZipFile(good) as src, zipfile.ZipFile(dup, "w") as dst:
                for info in src.infolist():
                    dst.writestr(info, src.read(info.filename))
                # Write SET.md again as duplicate.
                dst.writestr("SET.md", b"dup")
            with self.assertRaisesRegex(ValueError, "duplicate entry"):
                VERIFY.verify(dup)
            # Unsafe absolute path.
            unsafe = Path(temp) / "unsafe.zip"
            with zipfile.ZipFile(unsafe, "w") as z:
                z.writestr("/abs.txt", b"x")
            with self.assertRaisesRegex(ValueError, "unsafe"):
                VERIFY.verify(unsafe)
            # Missing required file (drop manifest).
            miss = Path(temp) / "miss.zip"
            with zipfile.ZipFile(good) as src, zipfile.ZipFile(miss, "w") as dst:
                for info in src.infolist():
                    if info.filename == "RELEASE-MANIFEST.sha256":
                        continue
                    dst.writestr(info, src.read(info.filename))
            with self.assertRaisesRegex(ValueError, "required release file"):
                VERIFY.verify(miss)
            # Missing executable bit: rewrite one executable without mode.
            nobit = Path(temp) / "nobit.zip"
            with zipfile.ZipFile(good) as src, zipfile.ZipFile(nobit, "w") as dst:
                for info in src.infolist():
                    data = src.read(info.filename)
                    ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                    ni.compress_type = zipfile.ZIP_DEFLATED
                    ni.external_attr = (0o644 << 16)
                    dst.writestr(ni, data)
            with self.assertRaisesRegex(ValueError, "executable"):
                VERIFY.verify(nobit)
            # Bad manifest line + duplicate checksum + missing entry + mismatch.
            for mutate, expect in [
                ("badline", "invalid checksum manifest"),
                ("dupentry", "duplicate checksum"),
                ("missingref", "refers to missing"),
                ("mismatch", "coverage mismatch"),
                ("shamismatch", "SHA-256 mismatch"),
            ]:
                mz = Path(temp) / f"{mutate}.zip"
                with zipfile.ZipFile(good) as src:
                    names = src.namelist()
                    manifest = src.read("RELEASE-MANIFEST.sha256").decode()
                    if mutate == "badline":
                        manifest = "NOTHEX  foo\n" + manifest
                    elif mutate == "dupentry":
                        first = manifest.splitlines()[0] + "\n"
                        manifest = manifest + first
                    elif mutate == "missingref":
                        manifest += "0" * 64 + "  phantom.txt\n"
                    elif mutate == "mismatch":
                        manifest = "\n".join(manifest.splitlines()[1:]) + "\n"
                    elif mutate == "shamismatch":
                        # Corrupt one file but keep manifest (need to rebuild zip with corrupted content
                        # but original manifest).
                        pass
                    with zipfile.ZipFile(mz, "w") as dst:
                        for info in src.infolist():
                            data = src.read(info.filename)
                            if info.filename == "RELEASE-MANIFEST.sha256":
                                data = manifest.encode()
                            if mutate == "shamismatch" and info.filename == "SET.md":
                                data = data + b"TAMPER"
                            ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                            ni.compress_type = info.compress_type
                            ni.external_attr = info.external_attr
                            ni.create_system = info.create_system
                            dst.writestr(ni, data)
                with self.assertRaises(ValueError, msg=mutate):
                    VERIFY.verify(mz)
            # Non-UTF8 manifest.
            nz = Path(temp) / "noutf8.zip"
            with zipfile.ZipFile(good) as src, zipfile.ZipFile(nz, "w") as dst:
                for info in src.infolist():
                    data = src.read(info.filename)
                    if info.filename == "RELEASE-MANIFEST.sha256":
                        data = b"\xff\xfe bad\n"
                    ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                    ni.compress_type = info.compress_type
                    ni.external_attr = info.external_attr
                    ni.create_system = info.create_system
                    dst.writestr(ni, data)
            with self.assertRaisesRegex(ValueError, "not UTF-8"):
                VERIFY.verify(nz)


class CheckDesignTokensTests(unittest.TestCase):
    def test_missing_contract_and_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # No contract at all.
            self.assertEqual(TOKENS.main(["--root", str(root)]), 1)
            # Contract without sections.
            cdir = root / "human-centric-visual-excellence" / "references"
            cdir.mkdir(parents=True)
            (cdir / "design-tokens-and-components.md").write_text("# T\n", encoding="utf-8")
            # Skills without reference.
            for rel in ("human-centric-visual-excellence/SKILL.md",
                        "frontend-engineering-excellence/SKILL.md"):
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("# S\nno contract here\n", encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 1)

    def test_tokens_json_variants(self):
        import shutil
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "human-centric-visual-excellence",
                            root / "human-centric-visual-excellence")
            shutil.copytree(ROOT / "frontend-engineering-excellence",
                            root / "frontend-engineering-excellence")
            # Invalid JSON.
            (root / "tokens.json").write_text("{bad", encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 1)
            # Root not object.
            (root / "tokens.json").write_text('["a"]', encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 1)
            # Empty tokens.
            (root / "tokens.json").write_text('{}', encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 1)
            (root / "tokens.json").write_text('{"tokens": {}}', encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 1)
            # Bad name pattern.
            (root / "tokens.json").write_text(
                json.dumps({"tokens": {"BAD NAME!": "#fff"}}), encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 1)
            # Valid with version + nested tokens (covers version-present branch, no INFO).
            (root / "tokens.json").write_text(
                json.dumps({"version": "1.0", "tokens": {"tier-role-state-scale": "#fff"}}),
                encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 0)
            # Valid nested without version (covers INFO branch).
            (root / "tokens.json").write_text(
                json.dumps({"tokens": {"tier-role-state-scale": "#fff"}}),
                encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 0)
            # Flat dict form (tokens = root dict itself).
            (root / "tokens.json").write_text(
                json.dumps({"tier-role-state-scale": "#fff"}), encoding="utf-8")
            self.assertEqual(TOKENS.main(["--root", str(root)]), 0)


class RunTriggerEvalTests(unittest.TestCase):
    def test_matrix_validation_and_observations(self):
        with tempfile.TemporaryDirectory() as temp:
            matrix = Path(temp) / "m.json"
            # Bad schema.
            matrix.write_text(json.dumps({"schema_version": "9"}), encoding="utf-8")
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix)]), 1)
            # Missing file (load_matrix raises SystemExit, not return 1).
            with self.assertRaises(SystemExit):
                TRIGEVAL.main(["--matrix", str(Path(temp) / "no.json")])
            # Too few cases.
            matrix.write_text(json.dumps({
                "schema_version": "1.1", "evaluation_type": "candidate-test-set-not-runtime-results",
                "skills": {"s": {"positive": [], "negative": []}}}), encoding="utf-8")
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix)]), 1)
            # Bad id / duplicate / empty prompt / overlap.
            def mk(pos, neg):
                return {"schema_version": "1.1",
                        "evaluation_type": "candidate-test-set-not-runtime-results",
                        "skills": {"s": {"positive": pos, "negative": neg}}}
            good_pos = [{"id": f"p{i}", "prompt": f"prompt positive {i} unik-{i}", "expected": "trigger"} for i in range(5)]
            good_neg = [{"id": f"n{i}", "prompt": f"prompt negative {i} unik-{i}", "expected": "no-trigger"} for i in range(5)]
            bad = mk([{"id": "BAD", "prompt": "x", "expected": "trigger"}] + good_pos[1:], good_neg)
            matrix.write_text(json.dumps(bad), encoding="utf-8")
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix)]), 1)
            dup = mk(good_pos, good_pos[:5])  # duplicate ids across groups? use same ids
            dup["skills"]["s"]["negative"] = [{"id": "p0", "prompt": "different negative", "expected": "no-trigger"}] + good_neg[1:]
            matrix.write_text(json.dumps(dup), encoding="utf-8")
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix)]), 1)
            empty = mk([{"id": "e0", "prompt": "", "expected": "trigger"}] + good_pos[1:], good_neg)
            matrix.write_text(json.dumps(empty), encoding="utf-8")
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix)]), 1)
            # Fresh lists to avoid cross-case mutation.
            fresh_pos = [{"id": f"p{i}", "prompt": f"prompt positive {i} unik-{i}", "expected": "trigger"} for i in range(5)]
            fresh_neg = [{"id": f"n{i}", "prompt": f"prompt negative {i} unik-{i}", "expected": "no-trigger"} for i in range(5)]
            over = mk(fresh_pos, fresh_neg)
            over["skills"]["s"]["negative"][0] = {"id": "n0", "prompt": fresh_pos[0]["prompt"], "expected": "no-trigger"}
            # Overlap is per skill with key skill:norm, but positive vs negative same prompt in same skill
            # uses same key? key = f"{skill}:{norm}" so same norm collides across groups -> overlap fail.
            matrix.write_text(json.dumps(over), encoding="utf-8")
            # Note: current impl checks overlap per skill across groups via `seen` dict keyed skill:norm,
            # so this should fail.
            rc = TRIGEVAL.main(["--matrix", str(matrix)])
            self.assertEqual(rc, 1)
            # Good coverage-only.
            matrix.write_text(json.dumps(mk(good_pos, good_neg)), encoding="utf-8")
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix)]), 0)
            # Observations: missing file, missing obs, runtime grading + warn + out.
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix),
                                            "--observations", str(Path(temp) / "no.json")]), 1)
            obs = {"method": "manual", "activations": [
                {"id": c["id"], "activated": c["expected"] == "trigger"}
                for grp in ("positive", "negative") for c in mk(good_pos, good_neg)["skills"]["s"][grp]]}
            # Actually need ids from good matrix.
            obs_path = Path(temp) / "obs.json"
            obs_path.write_text(json.dumps(obs), encoding="utf-8")
            out = Path(temp) / "rep.md"
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix),
                                            "--observations", str(obs_path),
                                            "--out", str(out)]), 0)
            self.assertTrue(out.is_file())
            # Missing observation for one id.
            obs2 = {"activations": [{"id": "p0", "activated": True}]}
            obs2_path = Path(temp) / "obs2.json"
            obs2_path.write_text(json.dumps(obs2), encoding="utf-8")
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix),
                                            "--observations", str(obs2_path)]), 1)
            # Low recall triggers WARN but still 0 (need matrix where observations cause low recall).
            obs_bad = {"method": "m", "activations": [
                {"id": c["id"], "activated": False} for c in good_pos
            ] + [{"id": c["id"], "activated": True} for c in good_neg]}
            obs_bad_path = Path(temp) / "obsbad.json"
            obs_bad_path.write_text(json.dumps(obs_bad), encoding="utf-8")
            self.assertEqual(TRIGEVAL.main(["--matrix", str(matrix),
                                            "--observations", str(obs_bad_path)]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
