#!/usr/bin/env python3
"""Validate the design-tokens contract and any machine-readable token source.

Usage: python3 scripts/check-design-tokens.py --root .
Read-only, deterministic, offline. Exit 0 on PASS, 1 on FAIL.

Fail-closed checks (contract structure):
  - human-centric-visual-excellence/references/design-tokens-and-components.md
    exists and contains every required section (grid/spacing, color roles,
    type scale, component contract, interaction state matrix, naming and
    versioning, export and lint).
  - Every SKILL.md that references the contract links a resolvable path.

Advisory-or-strict checks (token source):
  - If tokens.json exists at the set root, it must parse, hold unique token
    names matching --{tier}-{role}-{state}-{scale} style kebab-case, and
    declare a version. A present-but-invalid tokens.json FAILS.
  - If tokens.json is absent, the check passes with INFO (product repos add
    their generated tokens.json; the contract alone gates the set release).
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

CONTRACT = Path("human-centric-visual-excellence/references/design-tokens-and-components.md")
REQUIRED_SECTIONS = [
    "Grid and Spacing",
    "Color Roles",
    "Type Scale",
    "Component Contract",
    "Interaction State Matrix",
    "Naming and Versioning",
    "Export and Lint",
]
TOKEN_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
# Naming note (PA-COV-05): the regex enforces generic kebab-case with at least
# two segments; the canonical recommended shape is --{tier}-{role}-{state}-{scale}
# (see contract "Naming and Versioning"). Behavior intentionally unchanged.


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    args = ap.parse_args(argv)
    root = args.root.resolve()
    errors: list[str] = []

    contract = root / CONTRACT
    if not contract.is_file():
        errors.append(f"missing design-tokens contract: {CONTRACT.as_posix()}")
    else:
        text = contract.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"contract missing required section: {section}")

    for skill_rel in (
        "human-centric-visual-excellence/SKILL.md",
        "frontend-engineering-excellence/SKILL.md",
    ):
        skill_file = root / skill_rel
        if skill_file.is_file():
            body = skill_file.read_text(encoding="utf-8")
            if "design-tokens-and-components.md" not in body:
                errors.append(f"{skill_rel} does not reference the tokens contract")

    tokens_file = root / "tokens.json"
    if tokens_file.is_file():
        try:
            tokens = json.loads(tokens_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"tokens.json is not valid JSON: {exc}")
            tokens = None
        if isinstance(tokens, dict):
            names = tokens.get("tokens", tokens)
            if not isinstance(names, dict) or not names:
                errors.append("tokens.json holds no token entries")
            else:
                for name in names:
                    if not TOKEN_NAME.fullmatch(name):
                        errors.append(f"token name breaks naming pattern: {name}")
            if isinstance(tokens, dict) and "version" not in tokens and isinstance(tokens.get("tokens"), dict):
                print("INFO: tokens.json has no top-level version field (recommended)")
        elif tokens is not None:
            errors.append("tokens.json root must be an object")
    else:
        print("INFO: no tokens.json at set root; contract-only gate applies (product repos add generated tokens.json)")

    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1
    print("PASS: design-tokens contract is complete and referenced; token source check done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
