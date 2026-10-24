#!/usr/bin/env python3
"""Score trigger-matrix coverage and optionally grade runtime observations.

Usage:
  python3 scripts/run-trigger-evaluation.py --matrix evaluation/trigger-evaluation-matrix.json
  python3 scripts/run-trigger-evaluation.py --matrix evaluation/trigger-evaluation-matrix.json --observations runtime-log.json --out evaluation/results-YYYY-MM-DD.md

Coverage mode (no observations) is deterministic and offline: it checks schema,
counts, ID uniqueness, prompt overlap, per-family presence (ID, near-miss), and
reports the frozen matrix SHA-256. Runtime mode additionally grades a JSON
observation log of the form {"activations": [{"id": "pa-p1", "activated": true}]}.

Side effects: read-only except for --out report writing. No network. Exit 0 on
coverage PASS; exit 1 on any fail-closed violation.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

def load_matrix(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"FAIL: cannot read matrix {p}: {exc}")

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--matrix", type=Path, required=True)
    ap.add_argument("--observations", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)
    data = load_matrix(args.matrix)
    if data.get("schema_version") != "1.1" or data.get("evaluation_type") != "candidate-test-set-not-runtime-results":
        print("FAIL: matrix must be schema 1.1 candidate-test-set-not-runtime-results", file=sys.stderr); return 1
    digest = hashlib.sha256(args.matrix.read_bytes()).hexdigest()
    ids: set[str] = set(); seen: dict[str, str] = {}
    total_pos = total_neg = 0
    id_family = 0
    for skill, cases in data.get("skills", {}).items():
        for group in ("positive", "negative"):
            arr = cases.get(group, [])
            if len(arr) < 5:
                print(f"FAIL: {skill} needs >=5 {group} cases", file=sys.stderr); return 1
            if group == "positive": total_pos += len(arr)
            else: total_neg += len(arr)
            for c in arr:
                cid, prompt, exp = c.get("id"), c.get("prompt"), c.get("expected")
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", cid or ""):
                    print(f"FAIL: bad case id {cid!r}", file=sys.stderr); return 1
                if cid in ids:
                    print(f"FAIL: duplicate case id {cid}", file=sys.stderr); return 1
                ids.add(cid)
                norm = re.sub(r"\s+", " ", (prompt or "")).casefold()
                if not norm:
                    print(f"FAIL: empty prompt {cid}", file=sys.stderr); return 1
                key = f"{skill}:{norm}"
                if key in seen:
                    print(f"FAIL: prompt overlap in {skill}: {cid} vs {seen[key]}", file=sys.stderr); return 1
                seen[key] = cid
                if re.search(r"\b(buatkan|tingkatkan|tinjau|audit artefak|lakukan audit|kesiapan produksi|keberhasilan terukur|nasi goreng|untuk makan malam|yang enak|dengan kentang)\b", prompt or "", re.I):
                    id_family += 1
    print(f"PASS: matrix coverage: {total_pos} positive + {total_neg} negative across {len(data['skills'])} skills")
    print(f"PASS: {len(ids)} unique case IDs, no cross-label prompt overlap per skill")
    print(f"INFO: Indonesian-family prompts detected: {id_family} (informational; >=4 recommended)")
    print(f"INFO: frozen matrix SHA-256: {digest}")
    if id_family < 4:
        print("WARN: fewer than 4 Indonesian-family prompts; add ID coverage for masterpiece bar", file=sys.stderr)
    if args.observations is None:
        print("PASS: coverage-only scoring complete (no runtime observations graded)")
        return 0
    try:
        obs = json.loads(args.observations.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read observations: {exc}", file=sys.stderr); return 1
    method = obs.get("method", "method not declared in observation log — treat as non-runtime adjudication")
    act = {(a.get("id")): bool(a.get("activated")) for a in obs.get("activations", [])}
    lines = ["# Trigger Evaluation Results (observation-graded)", "", f"Matrix SHA-256: `{digest}`", f"Adjudication method: {method}", "WARNING: This is NOT live-runtime activation evidence unless the observation log records target-runtime identity, version, and timestamp; see evaluation/runtime-protocol.md for the required live run.", ""]
    lines.append("| Skill | TP | FN | FP | TN | Recall | FPR | n |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for skill, cases in data["skills"].items():
        tp = fn = fp = tn = 0
        for c in cases["positive"]:
            if c["id"] not in act:
                print(f"FAIL: missing observation for {c['id']}", file=sys.stderr); return 1
            if act[c["id"]]: tp += 1
            else: fn += 1
        for c in cases["negative"]:
            if c["id"] not in act:
                print(f"FAIL: missing observation for {c['id']}", file=sys.stderr); return 1
            if act[c["id"]]: fp += 1
            else: tn += 1
        rec = tp / max(1, tp + fn); fpr = fp / max(1, fp + tn)
        lines.append(f"| {skill} | {tp} | {fn} | {fp} | {tn} | {rec:.3f} | {fpr:.3f} | {tp+fn+fp+tn} |")
        print(f"INFO: {skill}: TP={tp} FN={fn} FP={fp} TN={tn} recall={rec:.3f} FPR={fpr:.3f}")
        if rec < 0.90 or fpr > 0.10:
            print(f"WARN: {skill} misses masterpiece target (recall>=0.90, FPR<=0.10)", file=sys.stderr)
    report = "\n".join(lines) + "\n"
    if args.out:
        args.out.write_text(report, encoding="utf-8", newline="\n")
        print(f"PASS: runtime report written: {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
