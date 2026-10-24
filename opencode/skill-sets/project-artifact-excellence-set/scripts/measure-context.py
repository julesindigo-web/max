#!/usr/bin/env python3
"""Estimate context footprint: SKILL.md lines + reference sizes per skill.

Usage: python3 scripts/measure-context.py --root . [--budget-lines 500]
Read-only, deterministic, offline. Exit 1 if any SKILL.md exceeds budget.
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--budget-lines", type=int, default=500)
    args = ap.parse_args(argv)
    root = args.root.resolve()
    skills = sorted([p for p in root.iterdir() if (p / "SKILL.md").is_file()] + ([p for p in (root / "skills").iterdir() if (p / "SKILL.md").is_file()] if (root / "skills").is_dir() else []))
    failed = False
    for s in skills:
        skill_file = s / "SKILL.md"
        n = len(skill_file.read_text(encoding="utf-8").splitlines())
        refs = sorted((s / "references").rglob("*.md")) if (s / "references").is_dir() else []
        ref_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in refs)
        status = "PASS" if n <= args.budget_lines else "FAIL"
        if n > args.budget_lines: failed = True
        print(f"{status}: {s.name}/SKILL.md={n} lines (budget {args.budget_lines}); references: {len(refs)} files / {ref_lines} lines (lazy-loaded, not baseline)")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
