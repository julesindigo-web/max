#!/usr/bin/env python3
"""Check relative links, one-level references depth, TOC for long files, headings.

Usage: python3 scripts/check-links-toc.py --root .
Read-only; no network. Exit 0 on PASS, 1 on FAIL.
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
SKIP = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    args = ap.parse_args(argv)
    root = args.root.resolve()
    errors: list[str] = []
    md_files = [p for p in root.rglob("*.md") if "/fixtures/" not in p.relative_to(root).as_posix() and not any(part in SKIP or part.startswith(".") and part != ".github" for part in p.relative_to(root).parts) and ".git" not in p.parts]
    for f in sorted(md_files):
        raw = f.read_text(encoding="utf-8", errors="replace")
        # strip fenced code blocks and inline code spans before link/heading scans
        import re as _re
        no_fence = _re.sub(r"```.*?```", "", raw, flags=_re.DOTALL)
        text = _re.sub(r"`[^`\n]+`", "", no_fence)
        lines = text.splitlines()
        if len(lines) > 100 and "Table of Contents" not in text and "## Contents" not in text and f.name != "AUDIT-REPORT-MASTERPIECE.md":
            # TOC required for references/ files >100 lines; top-level reports exempt if they have heading hierarchy
            rel = f.relative_to(root).as_posix()
            if "/references/" in rel:
                errors.append(f"{rel}: >100 lines but no TOC marker")
        # heading hierarchy: first heading must be H1, no jumps >1
        prev = 0
        for i, ln in enumerate(lines, 1):
            m = re.match(r"^(#{1,6})\s+\S", ln)
            if m:
                lvl = len(m.group(1))
                if prev == 0 and lvl != 1:
                    errors.append(f"{f.relative_to(root).as_posix()}:{i}: first heading must be H1")
                if prev and lvl > prev + 1:
                    errors.append(f"{f.relative_to(root).as_posix()}:{i}: heading jump H{prev}->H{lvl}")
                prev = lvl
        for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
            _t = m.group(2).strip()
            if "(?" in _t or _t.startswith("?") or _t.startswith(":"):
                continue  # regex fragment, not a markdown link
            target = _t
            if re.match(r"^(https?://|mailto:|#|data:)", target):
                continue
            target_path = target.split("#")[0]
            cand = (f.parent / target_path).resolve()
            try:
                cand.relative_to(root)
            except ValueError:
                errors.append(f"{f.relative_to(root).as_posix()}: link escapes root: {target}")
                continue
            if not cand.exists():
                errors.append(f"{f.relative_to(root).as_posix()}: broken relative link: {target}")
        # references depth: only one level under references/
        rel = f.relative_to(root).as_posix()
        if "/references/" in rel:
            rest = rel.split("/references/", 1)[1]
            if "/" in rest:
                errors.append(f"{rel}: references must be one level deep")
    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(f"PASS: links/TOC/headings checked across {len(md_files)} markdown files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
