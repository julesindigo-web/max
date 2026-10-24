#!/usr/bin/env python3
"""Deterministic scorer for excellence-ops routing probes (no LLM).

Checks probe-set hygiene only: per-group 5+5 coverage, stable IDs, unique
casefolded texts (no cross-label overlap), Indonesian + near-miss presence,
and field validity. Exit 0 = pass, 1 = fail. Read-only.

Usage: python3 score-routing-probes.py [probes.json]
"""
import json
import re
import sys
from collections import Counter

EXPECTED_GROUPS = ["auditor", "skill-builder", "test-runner", "audit", "new-skill", "validate-set"]
ID_RE = re.compile(r"^(auditor|skill-builder|test-runner|audit|new-skill|validate-set)-(pos|neg)-\d{2}$")


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "routing-probes.json"
    try:
        with open(src, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        fail(f"cannot load {src}: {e}")
    probes = data.get("probes")
    if not isinstance(probes, list) or not probes:
        fail("probes list missing or empty")
    # Stable IDs unique.
    ids = [p.get("id") for p in probes]
    dup_ids = [k for k, v in Counter(ids).items() if v > 1]
    if dup_ids:
        fail(f"duplicate probe ids: {sorted(dup_ids)}")
    for p in probes:
        pid = p.get("id", "")
        if not ID_RE.fullmatch(pid):
            fail(f"unstable id format: {pid!r} (want <group>-<pos|neg>-NN)")
        if p.get("polarity") not in ("positive", "negative"):
            fail(f"bad polarity in {pid}")
        if ("pos-" in pid and p.get("polarity") != "positive") or ("neg-" in pid and p.get("polarity") != "negative"):
            fail(f"id/polarity mismatch in {pid}")
        if p.get("lang") not in ("en", "id"):
            fail(f"bad lang in {pid}")
        if p.get("family") not in ("standard", "indonesian", "near-miss"):
            fail(f"bad family in {pid}")
        text = p.get("text", "")
        if not isinstance(text, str) or not text.strip() or len(text) > 300:
            fail(f"bad text in {pid}")
    # Per-group 5+5 coverage with Indonesian + near-miss in each group.
    by_group = {}
    for p in probes:
        by_group.setdefault(p.get("group"), []).append(p)
    if sorted(by_group) != sorted(EXPECTED_GROUPS):
        fail(f"group mismatch: have {sorted(by_group)}, want {sorted(EXPECTED_GROUPS)}")
    for g in EXPECTED_GROUPS:
        items = by_group[g]
        npos = sum(1 for p in items if p["polarity"] == "positive")
        nneg = sum(1 for p in items if p["polarity"] == "negative")
        if npos < 5 or nneg < 5:
            fail(f"group {g}: need 5+5, have {npos}+{nneg}")
        if not any(p["lang"] == "id" and p["polarity"] == "positive" for p in items):
            fail(f"group {g}: missing Indonesian positive")
        if not any(p["lang"] == "id" and p["polarity"] == "negative" for p in items):
            fail(f"group {g}: missing Indonesian negative")
        if not any(p["family"] == "near-miss" for p in items):
            fail(f"group {g}: missing near-miss case")
    # Cross-label overlap: no identical normalized text under two probes.
    seen = {}
    for p in probes:
        norm = " ".join(p["text"].casefold().split())
        if norm in seen:
            fail(f"overlap: {p['id']} duplicates text of {seen[norm]}")
        seen[norm] = p["id"]
    npos = sum(1 for p in probes if p["polarity"] == "positive")
    nneg = sum(1 for p in probes if p["polarity"] == "negative")
    nid = sum(1 for p in probes if p["lang"] == "id")
    nnm = sum(1 for p in probes if p["family"] == "near-miss")
    print(f"PASS: routing probes ok ({len(probes)} total: {npos}+{nneg}; {nid} Indonesian; {nnm} near-miss; 6 groups 5+5).")


if __name__ == "__main__":
    main()
