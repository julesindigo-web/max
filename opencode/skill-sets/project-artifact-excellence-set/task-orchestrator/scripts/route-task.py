#!/usr/bin/env python3
"""Deterministic offline task-to-skill classifier for task-orchestrator.

Usage:
  route-task.py --text "<utterance>" [--json] [--top N]
  route-task.py --help

Behavior (deterministic, stdlib only, no network):
  - Lowercases + collapses whitespace, matches fixed phrase families per skill.
  - Score = number of distinct matched phrases (corroboration count).
  - Single-skill route requires score >= 2; otherwise status is `clarify`
    with the top two candidates (fail closed, never guess).
  - Ties break by fixed manifest order (stable, reproducible).
  - Empty input or input > 2000 chars fails closed with exit code 2.
Exit codes: 0 routed/clarify with output, 2 invalid input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Fixed manifest order for stable tie-breaking (13 members + task-orchestrator).
SKILL_ORDER = [
    "project-artifact-auditor",
    "skills-create-excellence",
    "code-refactoring-optimizer",
    "security-vulnerability-auditor",
    "test-automation-engineer",
    "architecture-documentation-generator",
    "accessibility-inclusive-design",
    "continuous-observability-telemetry",
    "backend-engineering-excellence",
    "frontend-engineering-excellence",
    "human-centric-visual-excellence",
    "deployment-devops-orchestrator",
    "fullstack-e2e-mastery",
    "task-orchestrator",
]

# Corroborating signal phrases per skill (EN + ID). Substring match on
# normalized text. Deliberately multi-word to avoid single-keyword hits.
SIGNALS = {
    "project-artifact-auditor": [
        "audit", "gap analysis", "traceability gap", "prd", "acceptance criteria",
        "arsitektur layanan", "audit arsitektur", "kesenjangan ketertelusuran",
        "remediation backlog", "severity basis", "evidence state",
    ],
    "skills-create-excellence": [
        "create skill", "new skill", "upgrade skill", "skill set", "agent spec",
        "buatkan skill", "tingkatkan skill", "standar excellence",
        "plugin", "skill package",
    ],
    "code-refactoring-optimizer": [
        "refactor", "code smell", "cyclomatic", "duplication", "legacy code",
        "refaktor", "kompleksitas", "duplikasi",
    ],
    "security-vulnerability-auditor": [
        "owasp", "vulnerability", "secrets leakage", "penetration",
        "authentication", "authorization", "kerentanan", "kebocoran secret",
        "otentikasi", "otorisasi",
    ],
    "test-automation-engineer": [
        "e2e", "regression test", "test coverage", "flaky", "visual regression",
        "baseline", "screenshot", "pengujian", "uji e2e", "cakupan pengujian",
    ],
    "architecture-documentation-generator": [
        "openapi", "architecture doc", "system diagram", "data flow",
        "dokumentasi arsitektur", "kontrak openapi", "diagram aliran",
    ],
    "accessibility-inclusive-design": [
        "wcag", "aria", "keyboard navigation", "screen reader", "contrast",
        "fokus", "aksesibilitas", "navigasi keyboard", "keterbacaan",
        "kontras",
    ],
    "continuous-observability-telemetry": [
        "opentelemetry", "observability", "slo", "alerting", "tracing",
        "telemetri", "observabilitas", "peringatan produksi",
    ],
    "backend-engineering-excellence": [
        "backend api", "latency budget", "domain service", "database query",
        "encryption", "api backend", "latensi", "enkripsi",
    ],
    "frontend-engineering-excellence": [
        "web vitals", "layout shift", "cls", "client state", "loading state",
        "empty state", "error state", "pergeseran layout", "tampilan data",
    ],
    "human-centric-visual-excellence": [
        "art direction", "art brief", "visual design", "motion",
        "typography", "arah visual", "art brief", "merek",
    ],
    "deployment-devops-orchestrator": [
        "ci/cd", "pipeline", "container", "docker image", "deployment gate",
        "kontainer", "citata rilis", "gerbang deployment",
    ],
    "fullstack-e2e-mastery": [
        "end-to-end slice", "api contract", "interface through data",
        "irisan e2e", "kontrak api", "pendaftaran pengguna",
    ],
    "task-orchestrator": [
        "route this task", "choose the best skill", "which skill",
        "orchestrate", "auto select", "no slash command",
        "rute tugas", "skill mana", "orkestrasi", "tanpa slash",
        "tanpa perintah slash", "which capability", "multi-kemampuan", "multi-capability",
    ],
}

# Negative guards: (guard phrase, penalized skill or None=all).
# A guard hit subtracts 2 from the penalized skill (floor 0).
NEGATIVES = [
    ("nasi goreng", None),
    ("recipe", None),
    ("meme", "test-automation-engineer"),
    ("slide presentasi", "test-automation-engineer"),
    ("physics", None),
    ("fisika", None),
]

MAX_CHARS = 2000
MIN_SCORE = 2


def normalize(text: str) -> str:
    text = text.casefold()
    return re.sub(r"\s+", " ", text).strip()


def _phrase_hit(phrase: str, norm: str) -> bool:
    # Word-boundary match so short signals (e.g. "aria") never fire inside
    # longer words (e.g. Indonesian "pencarian"). Boundaries are alphanumeric;
    # phrases themselves may contain spaces, slashes, or hyphens.
    return re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", norm) is not None


def classify(text: str, top: int = 3) -> dict:
    norm = normalize(text)
    if not norm:
        raise ValueError("empty utterance: provide 1-2000 characters")
    if len(text) > MAX_CHARS:
        raise ValueError(f"oversized input ({len(text)} chars, max {MAX_CHARS})")
    scored = []
    for skill in SKILL_ORDER:
        hits = [p for p in SIGNALS[skill] if _phrase_hit(p, norm)]
        score = len(hits)
        for guard, target in NEGATIVES:
            if guard in norm and (target is None or target == skill):
                score -= 2
        scored.append({"skill": skill, "score": max(score, 0), "evidence": hits})
    scored.sort(key=lambda r: (-r["score"], SKILL_ORDER.index(r["skill"])))
    best = scored[0]
    if best["score"] >= MIN_SCORE:
        return {"status": "routed", "route": best["skill"], "ranking": scored[:top]}
    return {
        "status": "clarify",
        "route": None,
        "candidates": [r["skill"] for r in scored[:2]],
        "ranking": scored[:top],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Route a task utterance to set skills.")
    ap.add_argument("--text", default="", help="verbatim user utterance")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--top", type=int, default=3, help="ranking depth (1-14)")
    args = ap.parse_args(argv)
    try:
        result = classify(args.text, top=max(1, min(args.top, len(SKILL_ORDER))))
    except ValueError as exc:
        print(f"route-task: input rejected: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["status"] == "routed":
            ev = ", ".join(result["ranking"][0]["evidence"][:4])
            print(f"route: {result['route']} (score {result['ranking'][0]['score']}; {ev})")
        else:
            print(f"clarify: low confidence; candidates: {', '.join(result['candidates'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
