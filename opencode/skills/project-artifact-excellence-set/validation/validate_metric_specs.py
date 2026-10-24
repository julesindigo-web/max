#!/usr/bin/env python3
"""Fail-closed semantic validation for the five canonical skill-set metrics.

This validator is intentionally narrow and dependency-free. It checks that each
metric has a definition, units/formula, plausible dimension-specific target,
rationale, data source, sample/population, segmentation, collection method,
owner, and observation window. Presence-only numeric heuristics are not enough.

Usage:
  python3 validation/validate_metric_specs.py --root <skill-set-root>
  python3 validation/validate_metric_specs.py --skill <path-to-SKILL.md>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    from validate_set_manifest import parse_constrained_yaml
except ImportError:  # pragma: no cover - direct isolated use outside packaged tree
    parse_constrained_yaml = None  # type: ignore[assignment]

REQUIRED_METRICS = (
    "Trigger performance",
    "Task completion",
    "Context-token efficiency",
    "Time-to-working-skill",
    "Residual defect density",
)
FIELDS = (
    "Definition",
    "Unit/formula",
    "Target",
    "Rationale",
    "Source",
    "Sample",
    "Segmentation",
    "Method",
    "Owner",
    "Window",
)
FIELD_PATTERN = re.compile(
    r"(?:^|;)\s*(Definition|Unit/formula|Target|Rationale|Source|Sample|Segmentation|Method|Owner|Window)\s*:\s*([^;]+)",
    re.IGNORECASE,
)
PLACEHOLDER = re.compile(r"^(?:tbd|todo|n/?a|unknown|to be defined|pending|placeholder)[.! ]*$", re.I)


class MetricSpecError(ValueError):
    """Metric description is missing or misleadingly underspecified."""


def extract_skill_metrics(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.fullmatch(r"##\s+Success Metrics\s*", line):
            start = index + 1
            break
    if start is None:
        raise MetricSpecError(f"required '## Success Metrics' section missing: {path}")
    metrics: list[str] = []
    for line in lines[start:]:
        if re.match(r"^##\s+", line):
            break
        match = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
        if match:
            metrics.append(match.group(1).strip())
    return metrics


def parse_fields(metric: str, context: str) -> tuple[str, dict[str, str]]:
    if ":" not in metric:
        raise MetricSpecError(f"metric must begin with a canonical dimension and colon ({context}): {metric}")
    dimension, _ = metric.split(":", 1)
    dimension = dimension.strip()
    aliases = {"time-to-working-skill / working-audit": "Time-to-working-skill"}
    canonical = next((item for item in REQUIRED_METRICS if dimension.casefold() == item.casefold()), None)
    canonical = canonical or aliases.get(dimension.casefold())
    if canonical is None:
        raise MetricSpecError(f"unknown or non-canonical metric dimension '{dimension}' ({context})")

    fields: dict[str, str] = {}
    for match in FIELD_PATTERN.finditer(metric.split(":", 1)[1]):
        key, value = match.group(1).casefold(), match.group(2).strip()
        if key in fields:
            raise MetricSpecError(f"duplicate '{key}' field in {canonical} ({context})")
        fields[key] = value

    expected_fields = {field.casefold() for field in FIELDS}
    missing = expected_fields - fields.keys()
    if missing:
        raise MetricSpecError(f"{canonical} missing required field(s) {', '.join(sorted(missing))} ({context})")
    for key, value in fields.items():
        if len(value) < 4 or PLACEHOLDER.fullmatch(value) or not re.search(r"[A-Za-z]", value):
            raise MetricSpecError(f"{canonical} field '{key}' is empty, numeric-only, or placeholder text ({context})")
    validate_dimension_target(canonical, fields["target"], context)
    return canonical, fields


def validate_dimension_target(dimension: str, target: str, context: str) -> None:
    """Reject numeric placeholders that pass a generic number-presence check."""
    target_fold = target.casefold()
    if dimension == "Trigger performance":
        tp = re.search(r"(?:≥|>=)\s*90(?:\.0)?\s*%", target)
        fp = re.search(r"(?:≤|<=)\s*10(?:\.0)?\s*%", target)
        if not (tp and fp and re.search(r"true[- ]positive|recall", target_fold) and re.search(r"false[- ]positive", target_fold)):
            raise MetricSpecError(f"Trigger performance target must specify ≥90% true-positive/recall and ≤10% false-positive rate ({context}): {target}")
    elif dimension == "Task completion":
        if not re.search(r"(?:≥|>=)\s*95(?:\.0)?\s*%", target) or not re.search(r"acceptance|completion|checks pass", target_fold):
            raise MetricSpecError(f"Task completion target must specify ≥95% acceptance/completion ({context}): {target}")
    elif dimension == "Context-token efficiency":
        if not re.search(r"(?:≤|<=)\s*500\s+lines?", target, re.I):
            raise MetricSpecError(f"Context-token efficiency target must bound SKILL.md at ≤500 lines ({context}): {target}")
    elif dimension == "Time-to-working-skill":
        if not re.search(r"(?:≤|<=)\s*60\s+minutes?", target, re.I):
            raise MetricSpecError(f"Time-to-working-skill target must bound time at ≤60 minutes ({context}): {target}")
    elif dimension == "Residual defect density":
        has_zero = bool(re.search(r"\bzero\b|\b0(?:\.0+)?\b", target_fold))
        has_critical = "critical" in target_fold
        has_major = "major" in target_fold
        if not (has_zero and has_critical and has_major):
            raise MetricSpecError(f"Residual defect density target must require zero open Critical and Major defects or documented risk acceptance ({context}): {target}")


def validate_metric_list(metrics: Iterable[str], context: str, *, require_order_independent: bool = True) -> list[str]:
    found: dict[str, tuple[str, dict[str, str]]] = {}
    for metric in metrics:
        dimension, fields = parse_fields(metric, context)
        if dimension in found:
            raise MetricSpecError(f"duplicate metric dimension '{dimension}' ({context})")
        found[dimension] = (metric, fields)
    missing = set(REQUIRED_METRICS) - found.keys()
    if missing:
        raise MetricSpecError(f"missing required metric dimension(s): {', '.join(sorted(missing))} ({context})")
    return [f"{dimension}: definition, target, data source, sample, method, owner, and measurement window validated" for dimension in REQUIRED_METRICS]


def validate_skill_file(path: Path) -> list[str]:
    if not path.is_file():
        raise MetricSpecError(f"SKILL.md not found: {path}")
    return validate_metric_list(extract_skill_metrics(path), str(path))


def validate_root(root: Path) -> list[str]:
    if parse_constrained_yaml is None:
        raise MetricSpecError("cannot import manifest parser; run from the packaged validation directory")
    manifest = root / "manifest.yaml"
    if not manifest.is_file():
        raise MetricSpecError(f"manifest.yaml not found: {manifest}")
    data = parse_constrained_yaml(manifest)
    messages: list[str] = []
    manifest_metrics = data.get("success-metrics", [])
    messages.extend(validate_metric_list(manifest_metrics, str(manifest)))
    set_doc = root / "SET.md"
    if not set_doc.is_file():
        raise MetricSpecError(f"SET.md not found: {set_doc}")
    set_metrics = extract_skill_metrics(set_doc)
    messages.extend(validate_metric_list(set_metrics, str(set_doc)))
    manifest_map = {parse_fields(metric, str(manifest))[0]: parse_fields(metric, str(manifest))[1] for metric in manifest_metrics}
    set_map = {parse_fields(metric, str(set_doc))[0]: parse_fields(metric, str(set_doc))[1] for metric in set_metrics}
    for dimension in REQUIRED_METRICS:
        if manifest_map[dimension] != set_map[dimension]:
            raise MetricSpecError(f"SET.md and manifest.yaml metric definitions drift for '{dimension}'; keep the human-readable and machine-readable set contracts synchronized")
    messages.append("SET.md and manifest.yaml metric definitions are synchronized")
    members = data.get("members", [])
    if not members:
        raise MetricSpecError(f"manifest has no members to validate: {manifest}")
    for member in members:
        member_path = root / member["path"] / "SKILL.md"
        messages.extend(validate_skill_file(member_path))
    return messages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--root", type=Path, help="skill-set root containing manifest.yaml")
    group.add_argument("--skill", type=Path, help="validate one SKILL.md")
    args = parser.parse_args(argv)
    try:
        if args.root:
            result = validate_root(args.root.resolve())
        else:
            result = validate_skill_file(args.skill.resolve())
        for message in result:
            print(f"PASS: {message}")
    except (OSError, KeyError, TypeError, MetricSpecError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: metric specifications are semantically validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
