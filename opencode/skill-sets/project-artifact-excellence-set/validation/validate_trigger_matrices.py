#!/usr/bin/env python3
"""Validate trigger test-set coverage and the authoritative evaluation matrix.

Schema 1.0 is supported for the lightweight documentation sample (arrays of
strings). Schema 1.1 is used by evaluation/trigger-evaluation-matrix.json and
requires stable IDs plus explicit expected labels for every prompt. This is a
coverage/schema check, not a runtime/model activation test.

Usage: python3 validation/validate_trigger_matrices.py [set-root] [cases-json]
If cases-json is omitted, the authoritative evaluation/ matrix is used.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


class TriggerMatrixError(ValueError):
    pass


def frontmatter_name(skill_file: Path) -> str:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise TriggerMatrixError(f"frontmatter missing: {skill_file}")
    for line in lines[1:]:
        if line == "---":
            break
        match = re.fullmatch(r"name:[ \t]*(.+)", line)
        if match:
            return match.group(1).strip().strip("\"'")
    raise TriggerMatrixError(f"frontmatter name missing: {skill_file}")


def discover_skills(root: Path) -> dict[str, Path]:
    if (root / "manifest.yaml").is_file():
        # In this repository, members are top-level directories. Discovery is
        # constrained to manifest members' conventional path-bearing entries;
        # the manifest validator separately checks exact declarations.
        candidates = [p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]
        if (root / "skills").is_dir():
            candidates.extend(p for p in (root / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    elif (root / "skills").is_dir():
        candidates = [p for p in (root / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]
    else:
        candidates = [p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]
    actual: dict[str, Path] = {}
    for path in candidates:
        name = frontmatter_name(path / "SKILL.md")
        if name in actual:
            raise TriggerMatrixError(f"duplicate member skill name discovered: {name}")
        actual[name] = path
    if not actual:
        raise TriggerMatrixError(f"no member SKILL.md files found under {root}")
    return actual


def extract_case(case: Any, schema_version: str, group: str, skill_name: str) -> tuple[str | None, str, str]:
    expected_for_group = "trigger" if group == "positive" else "no-trigger"
    if schema_version == "1.0":
        if not isinstance(case, str):
            raise TriggerMatrixError(f"{skill_name}: schema 1.0 {group} cases must be strings")
        prompt = case.strip()
        case_id = None
    else:
        if not isinstance(case, dict) or set(case) != {"id", "prompt", "expected"}:
            raise TriggerMatrixError(f"{skill_name}: schema 1.1 {group} cases require exactly id, prompt, expected")
        case_id, prompt, expected = case.get("id"), case.get("prompt"), case.get("expected")
        if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", case_id):
            raise TriggerMatrixError(f"{skill_name}: case id must use lowercase kebab-case: {case_id!r}")
        if expected != expected_for_group:
            raise TriggerMatrixError(f"{skill_name}: case {case_id!r} has expected={expected!r}; {group} cases require {expected_for_group!r}")
        if not isinstance(prompt, str):
            raise TriggerMatrixError(f"{skill_name}: case {case_id!r} prompt must be a string")
        prompt = prompt.strip()
    if not prompt:
        raise TriggerMatrixError(f"{skill_name}: every {group} prompt must be non-empty")
    return case_id, prompt, expected_for_group


def validate(root: Path, matrix_path: Path) -> int:
    actual = discover_skills(root)
    try:
        data = json.loads(matrix_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TriggerMatrixError(f"cannot read valid JSON matrix {matrix_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise TriggerMatrixError("trigger matrix root must be a JSON object")
    schema_version = data.get("schema_version")
    if schema_version not in {"1.0", "1.1"} or not isinstance(data.get("skills"), dict):
        raise TriggerMatrixError("trigger matrix must use supported schema_version '1.0' or '1.1' and contain a skills object")
    if schema_version == "1.1":
        if not isinstance(data.get("as_of"), str):
            raise TriggerMatrixError("schema 1.1 matrix must declare as_of as YYYY-MM-DD")
        try:
            dt.date.fromisoformat(data["as_of"])
        except ValueError as exc:
            raise TriggerMatrixError("schema 1.1 matrix as_of must be a real YYYY-MM-DD date") from exc
        if not isinstance(data.get("evaluation_protocol"), str) or len(data["evaluation_protocol"].strip()) < 20:
            raise TriggerMatrixError("schema 1.1 matrix must describe its evaluation_protocol")
        if data.get("evaluation_type") != "candidate-test-set-not-runtime-results":
            raise TriggerMatrixError("schema 1.1 matrix evaluation_type must explicitly identify a candidate test set, not runtime results")
    cases = data["skills"]
    missing = set(actual) - set(cases)
    unknown = set(cases) - set(actual)
    if missing:
        raise TriggerMatrixError(f"missing trigger matrix for member(s): {', '.join(sorted(missing))}")
    if unknown:
        raise TriggerMatrixError(f"trigger matrix refers to unknown member(s): {', '.join(sorted(unknown))}")

    all_ids: set[str] = set()
    for skill_name, case_set in cases.items():
        if not isinstance(case_set, dict) or set(case_set) != {"positive", "negative"}:
            raise TriggerMatrixError(f"{skill_name}: must contain exactly positive and negative arrays")
        seen_prompts: dict[str, str] = {}
        for group in ("positive", "negative"):
            prompts = case_set[group]
            if not isinstance(prompts, list) or len(prompts) < 5:
                raise TriggerMatrixError(f"{skill_name}: at least five {group} prompts are required")
            for case in prompts:
                case_id, prompt, _ = extract_case(case, schema_version, group, skill_name)
                normalized = re.sub(r"\s+", " ", prompt).casefold()
                if normalized in seen_prompts:
                    raise TriggerMatrixError(f"{skill_name}: prompt appears more than once across labels ({seen_prompts[normalized]} / {group})")
                seen_prompts[normalized] = group
                if case_id:
                    if case_id in all_ids:
                        raise TriggerMatrixError(f"duplicate trigger case id: {case_id}")
                    all_ids.add(case_id)
        print(f"PASS: {skill_name} has {len(case_set['positive'])} positive and {len(case_set['negative'])} negative trigger cases (schema {schema_version})")
    print(f"PASS: trigger matrix validated: {matrix_path}")
    return 0


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    matrix = Path(argv[2]).resolve() if len(argv) > 2 else root / "evaluation/trigger-evaluation-matrix.json"
    if len(argv) > 3:
        print("Usage: validate_trigger_matrices.py [set-root] [cases-json]", file=sys.stderr)
        return 2
    try:
        validate(root, matrix)
    except (OSError, TriggerMatrixError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
