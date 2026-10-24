#!/usr/bin/env python3
"""Validate evaluation/task-evaluation-ledger.json against its contract.

Usage: python3 validation/validate_task_ledger.py [set-root]
Structure gate only; task success requires independent runtime evidence.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

def main(argv) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    ledger_p = root / "evaluation/task-evaluation-ledger.json"
    try:
        data = json.loads(ledger_p.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read task ledger: {exc}", file=sys.stderr); return 1
    if data.get("schema_version") != "1.0" or not isinstance(data.get("tasks"), list):
        print("FAIL: ledger must use schema_version 1.0 with a tasks array", file=sys.stderr); return 1
    if len(data["tasks"]) < 5:
        print("FAIL: ledger needs >=5 representative tasks", file=sys.stderr); return 1
    ids: set[str] = set()
    for t in data["tasks"]:
        for k in ("id", "skill", "task", "acceptance", "status"):
            if k not in t:
                print(f"FAIL: task missing {k}: {t}", file=sys.stderr); return 1
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", t["id"]):
            print(f"FAIL: bad task id {t['id']!r}", file=sys.stderr); return 1
        if t["id"] in ids:
            print(f"FAIL: duplicate task id {t['id']}", file=sys.stderr); return 1
        ids.add(t["id"])
        if t["skill"] not in {"project-artifact-auditor", "skills-create-excellence", "set"}:
            print(f"FAIL: unknown task skill {t['skill']}", file=sys.stderr); return 1
        if len(t["task"]) < 20 or len(t["acceptance"]) < 20:
            print(f"FAIL: task/acceptance too short for {t['id']}", file=sys.stderr); return 1
        if t["status"] not in {"planned", "passed", "failed", "waived"}:
            print(f"FAIL: bad task status {t['status']}", file=sys.stderr); return 1
    print(f"PASS: task-evaluation ledger validated: {len(data['tasks'])} tasks")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
