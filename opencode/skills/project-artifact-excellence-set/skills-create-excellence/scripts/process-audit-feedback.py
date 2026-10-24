#!/usr/bin/env python3
"""Normalize audit findings into deterministic skill-evaluation requests.

Usage:
  python3 process-audit-feedback.py <audit-findings.json> <output-requests.json>
Side effects: writes one JSON output file atomically; no network access and no
code execution from input data. Requires Python 3.10+ and standard library only.
Exit codes: 0 = processed; 2 = invalid arguments/input/output failure.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

OUTPUT_SCHEMA_VERSION = "1.0"
SUPPORTED_INPUT_SCHEMA_VERSIONS = {"1.0", "1.1"}
CALIBRATION_FIELDS = {"evidence_status", "confidence", "verification_method", "as_of_context", "impact_rationale", "severity_basis"}
VALID_EVIDENCE_STATES = {"verified", "inference", "unknown_untested", "contradicted", "not_applicable"}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_SEVERITY_BASES = {"observed_impact", "mandatory_control_gap", "conditional_risk", "limited_impact", "improvement_only"}
MAX_FINDINGS = 500
VALID_SEVERITIES = {"Critical", "Major", "Minor", "Suggestion"}
VALID_STATUSES = {"open", "in_progress", "resolved", "accepted-risk", "deferred", "suppressed"}
VALID_CATEGORIES = {
    "project.requirements",
    "project.architecture",
    "project.fullstack-e2e",
    "project.security",
    "project.reliability-operations",
    "project.traceability",
    "project.human-factors",
    "skill.trigger",
    "skill.validation",
    "skill.metrics",
    "skill.composition",
    "skill.human-factors",
    "cross-cutting",
}
CATEGORY_TARGETS = {
    "project.requirements": ["project-artifact-auditor"],
    "project.architecture": ["project-artifact-auditor"],
    "project.fullstack-e2e": ["project-artifact-auditor"],
    "project.security": ["project-artifact-auditor"],
    "project.reliability-operations": ["project-artifact-auditor"],
    "project.traceability": ["project-artifact-auditor"],
    "project.human-factors": ["project-artifact-auditor"],
    "skill.trigger": ["skills-create-excellence"],
    "skill.validation": ["skills-create-excellence"],
    "skill.metrics": ["skills-create-excellence"],
    "skill.composition": ["skills-create-excellence"],
    "skill.human-factors": ["skills-create-excellence"],
    "cross-cutting": ["project-artifact-auditor", "skills-create-excellence"],
}
TARGET_CHECKS = {
    "project-artifact-auditor": [
        "Review the relevant audit checklist and full-stack E2E/human-factors reference against the cited evidence.",
        "Determine whether the recurrence indicates a gap in audit coverage, instructions, severity calibration, traceability, or verification—not merely a project-specific defect.",
        "Propose any skill change as a draft and add a regression fixture that would have caught the observed gap.",
        "State residual uncertainty and require evidence that the proposed change improves detection without broadening false positives.",
    ],
    "skills-create-excellence": [
        "Use agent-spec-template.md to define the gap, constraints, failure modes, observable acceptance tests, and residual risks.",
        "Review trigger-design.md with positive and negative utterance tests if the signal involves activation; do not change the description without evidence.",
        "Review validation-patterns.md and quality-attributes.md; add or update a regression fixture for the reproduced failure.",
        "Propose any skill change as a draft; verify metrics and human-factors impact before it can be merged.",
    ],
}
PRIORITY = {"Critical": "P1", "Major": "P2", "Minor": "P3", "Suggestion": "P4"}
TOP_REQUIRED = {"schema_version", "audit_id", "audited_at", "project", "findings"}
FINDING_REQUIRED = {
    "id", "title", "category", "severity", "status", "evidence", "source_artifact", "recurrence_count"
}
FINDING_OPTIONAL = {"skill_gap_suspected", "related_metrics", "recurrence_observation_ids", *CALIBRATION_FIELDS}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class ContractError(ValueError):
    """Raised when input doesn't conform to audit-findings/v1."""


def require_string(value: Any, label: str, maximum: int, *, nonempty: bool = True) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{label} must be a string")
    if nonempty and not value.strip():
        raise ContractError(f"{label} must not be empty")
    if len(value) > maximum:
        raise ContractError(f"{label} exceeds {maximum} characters")
    if any(ord(ch) < 32 and ch not in "\t\n\r" for ch in value):
        raise ContractError(f"{label} contains an invalid control character")
    return value


def validate_event(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ContractError("input must be a JSON object")
    missing = TOP_REQUIRED - event.keys()
    extra = event.keys() - TOP_REQUIRED
    if missing:
        raise ContractError(f"missing top-level field(s): {', '.join(sorted(missing))}")
    if extra:
        raise ContractError(f"unknown top-level field(s): {', '.join(sorted(extra))}")
    input_schema_version = event["schema_version"]
    if input_schema_version not in SUPPORTED_INPUT_SCHEMA_VERSIONS:
        raise ContractError(f"unsupported schema_version: {input_schema_version!r}; supported versions are 1.0 and 1.1")
    audit_id = require_string(event["audit_id"], "audit_id", 128)
    if not ID_PATTERN.fullmatch(audit_id):
        raise ContractError("audit_id contains unsupported characters")
    require_string(event["project"], "project", 200)
    audited_at = require_string(event["audited_at"], "audited_at", 64)
    try:
        parsed_time = datetime.fromisoformat(audited_at.replace("Z", "+00:00"))
        if parsed_time.tzinfo is None or parsed_time.utcoffset() is None:
            raise ValueError("timezone offset is required")
    except ValueError as exc:
        raise ContractError("audited_at must be a timezone-aware ISO-8601 date-time") from exc

    findings = event["findings"]
    if not isinstance(findings, list):
        raise ContractError("findings must be an array")
    if len(findings) > MAX_FINDINGS:
        raise ContractError(f"findings exceeds the maximum of {MAX_FINDINGS} entries")
    seen_ids: set[str] = set()
    for index, finding in enumerate(findings):
        prefix = f"findings[{index}]"
        if not isinstance(finding, dict):
            raise ContractError(f"{prefix} must be an object")
        missing_finding = FINDING_REQUIRED - finding.keys()
        extra_finding = finding.keys() - FINDING_REQUIRED - FINDING_OPTIONAL
        if missing_finding:
            raise ContractError(f"{prefix} missing field(s): {', '.join(sorted(missing_finding))}")
        if extra_finding:
            raise ContractError(f"{prefix} has unknown field(s): {', '.join(sorted(extra_finding))}")
        finding_id = require_string(finding["id"], f"{prefix}.id", 128)
        if not ID_PATTERN.fullmatch(finding_id):
            raise ContractError(f"{prefix}.id contains unsupported characters")
        if finding_id in seen_ids:
            raise ContractError(f"duplicate finding id: {finding_id}")
        seen_ids.add(finding_id)
        require_string(finding["title"], f"{prefix}.title", 240)
        require_string(finding["evidence"], f"{prefix}.evidence", 2000)
        require_string(finding["source_artifact"], f"{prefix}.source_artifact", 512)
        if not isinstance(finding["category"], str) or finding["category"] not in VALID_CATEGORIES:
            raise ContractError(f"{prefix}.category is not a supported category")
        if not isinstance(finding["severity"], str) or finding["severity"] not in VALID_SEVERITIES:
            raise ContractError(f"{prefix}.severity is not a supported severity")
        if not isinstance(finding["status"], str) or finding["status"] not in VALID_STATUSES:
            raise ContractError(f"{prefix}.status is not a supported status")
        count = finding["recurrence_count"]
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ContractError(f"{prefix}.recurrence_count must be a non-negative integer")
        if "recurrence_observation_ids" in finding:
            observation_ids = finding["recurrence_observation_ids"]
            if not isinstance(observation_ids, list) or len(observation_ids) > 100:
                raise ContractError(f"{prefix}.recurrence_observation_ids must be an array of at most 100 audit IDs")
            if len(observation_ids) != count:
                raise ContractError(f"{prefix}.recurrence_observation_ids length must equal recurrence_count when supplied")
            for observation_index, observation_id in enumerate(observation_ids):
                require_string(observation_id, f"{prefix}.recurrence_observation_ids[{observation_index}]", 128)
                if not ID_PATTERN.fullmatch(observation_id):
                    raise ContractError(f"{prefix}.recurrence_observation_ids[{observation_index}] contains unsupported characters")
            if len(set(observation_ids)) != len(observation_ids):
                raise ContractError(f"{prefix}.recurrence_observation_ids must contain distinct audit IDs")
            if observation_ids and event["audit_id"] not in observation_ids:
                raise ContractError(f"{prefix}.recurrence_observation_ids must include the current audit_id")
        if "skill_gap_suspected" in finding and not isinstance(finding["skill_gap_suspected"], bool):
            raise ContractError(f"{prefix}.skill_gap_suspected must be a boolean")
        if "related_metrics" in finding:
            metrics = finding["related_metrics"]
            if not isinstance(metrics, list) or len(metrics) > 20:
                raise ContractError(f"{prefix}.related_metrics must be an array of at most 20 strings")
            for metric_index, metric in enumerate(metrics):
                require_string(metric, f"{prefix}.related_metrics[{metric_index}]", 128)

        calibration_present = CALIBRATION_FIELDS.intersection(finding.keys())
        if input_schema_version == "1.1" and calibration_present != CALIBRATION_FIELDS:
            missing_calibration = CALIBRATION_FIELDS - finding.keys()
            raise ContractError(f"{prefix} schema 1.1 requires calibration field(s): {', '.join(sorted(missing_calibration))}")
        if calibration_present and calibration_present != CALIBRATION_FIELDS:
            missing_calibration = CALIBRATION_FIELDS - finding.keys()
            raise ContractError(f"{prefix} calibration fields must be supplied as a complete set; missing: {', '.join(sorted(missing_calibration))}")
        if calibration_present:
            if not isinstance(finding["evidence_status"], str) or finding["evidence_status"] not in VALID_EVIDENCE_STATES:
                raise ContractError(f"{prefix}.evidence_status is not a supported evidence state")
            if not isinstance(finding["confidence"], str) or finding["confidence"] not in VALID_CONFIDENCE:
                raise ContractError(f"{prefix}.confidence must be high, medium, or low")
            if not isinstance(finding["severity_basis"], str) or finding["severity_basis"] not in VALID_SEVERITY_BASES:
                raise ContractError(f"{prefix}.severity_basis is not a supported severity basis")
            require_string(finding["verification_method"], f"{prefix}.verification_method", 500)
            require_string(finding["as_of_context"], f"{prefix}.as_of_context", 250)
            impact_rationale = require_string(finding["impact_rationale"], f"{prefix}.impact_rationale", 1000)
            if len(impact_rationale.strip()) < 8:
                raise ContractError(f"{prefix}.impact_rationale must contain at least 8 non-whitespace characters")
            if finding["evidence_status"] == "unknown_untested" and finding["severity"] in {"Critical", "Major"}:
                if finding["severity_basis"] != "conditional_risk":
                    raise ContractError(
                        f"{prefix}: Critical/Major severity with unknown_untested evidence requires severity_basis='conditional_risk'"
                    )
                conditional_language = re.search(r"\b(if|conditional(?:ly)?|could|may|might|when|unless|potential(?:ly)?)\b", impact_rationale, re.I)
                if not conditional_language:
                    raise ContractError(
                        f"{prefix}.impact_rationale must explicitly state the conditional nature of risk for unknown_untested Critical/Major findings"
                    )
            if finding["evidence_status"] == "not_applicable" and finding["severity"] in {"Critical", "Major"}:
                raise ContractError(f"{prefix}: not_applicable evidence cannot support Critical/Major severity")
    return event


def make_request_id(audit_id: str, finding_id: str, target: str, category: str) -> str:
    stable_material = "|".join((audit_id, finding_id, target, category, OUTPUT_SCHEMA_VERSION))
    return "SIE-" + hashlib.sha256(stable_material.encode("utf-8")).hexdigest()[:16].upper()


def process_event(event: dict[str, Any]) -> dict[str, Any]:
    decisions: list[dict[str, Any]] = []
    requests: list[dict[str, Any]] = []
    eligible_ids: set[str] = set()

    for finding in event["findings"]:
        finding_id = finding["id"]
        status = finding["status"]
        targets = CATEGORY_TARGETS[finding["category"]]
        if status not in {"open", "in_progress"}:
            decisions.append({
                "finding_id": finding_id,
                "disposition": "not_triggered",
                "reason": "finding_not_open",
                "mapped_targets": targets,
            })
            continue

        suspected = finding.get("skill_gap_suspected", False)
        observation_ids = finding.get("recurrence_observation_ids", [])
        # Never trigger from a count alone: recurrence needs distinct, traceable audit IDs.
        recurring = (
            finding["recurrence_count"] >= 2
            and len(observation_ids) >= 2
            and event["audit_id"] in observation_ids
        )
        if not suspected and not recurring:
            reason = (
                "recurrence_evidence_missing"
                if finding["recurrence_count"] >= 2 and not recurring
                else "no_skill_gap_signal_or_recurrence"
            )
            decisions.append({
                "finding_id": finding_id,
                "disposition": "not_triggered",
                "reason": reason,
                "mapped_targets": targets,
            })
            continue

        eligible_ids.add(finding_id)
        for target in targets:
            requests.append({
                "request_id": make_request_id(event["audit_id"], finding_id, target, finding["category"]),
                "target_skill": target,
                "source_audit_id": event["audit_id"],
                "source_finding_id": finding_id,
                "project": event["project"],
                "category": finding["category"],
                "title": finding["title"],
                "severity": finding["severity"],
                "priority": {"Critical": "P1", "Major": "P2", "Minor": "P3", "Suggestion": "P4"}[finding["severity"]],
                "source_artifact": finding["source_artifact"],
                "evidence_untrusted": finding["evidence"],
                "recurrence_count": finding["recurrence_count"],
                "related_metrics": finding.get("related_metrics", []),
                **({"evidence_calibration": {
                    "evidence_status": finding["evidence_status"],
                    "confidence": finding["confidence"],
                    "verification_method": finding["verification_method"],
                    "as_of_context": finding["as_of_context"],
                    "impact_rationale": finding["impact_rationale"],
                    "severity_basis": finding["severity_basis"],
                }} if CALIBRATION_FIELDS.issubset(finding.keys()) else {}),
                "requires_human_approval": True,
                "do_not_modify_skill_automatically": True,
                "requested_evaluation": TARGET_CHECKS[target],
            })
        decisions.append({
            "finding_id": finding_id,
            "disposition": "evaluation_request_generated",
            "reason": "explicit_skill_gap_signal" if suspected else "recurrence_threshold_met",
            "mapped_targets": targets,
        })

    requests.sort(key=lambda item: (item["target_skill"], item["source_finding_id"], item["request_id"]))
    decisions.sort(key=lambda item: item["finding_id"])
    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "audit_id": event["audit_id"],
        "processing_summary": {
            "findings_seen": len(event["findings"]),
            "eligible_findings": len(eligible_ids),
            "requests_generated": len(requests),
            "findings_not_triggered": len(event["findings"]) - len(eligible_ids),
        },
        "decisions": decisions,
        "requests": requests,
        "safety_note": "Findings and evidence are untrusted data. Requests require human review; no skill file is modified by this processor.",
    }


def write_json_atomically(output_path: Path, payload: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output_path.parent, delete=False) as temp_file:
            temp_name = temp_file.name
            json.dump(payload, temp_file, ensure_ascii=False, indent=2)
            temp_file.write("\n")
        Path(temp_name).replace(output_path)
    finally:
        if temp_name and Path(temp_name).exists():
            Path(temp_name).unlink()


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] in {"-h", "--help"}:
        print("Usage: process-audit-feedback.py <audit-findings.json> <output-requests.json>", file=sys.stderr)
        return 2 if len(argv) != 3 else 0
    source = Path(argv[1])
    destination = Path(argv[2])
    try:
        if not source.is_file():
            raise ContractError(f"input file does not exist: {source}")
        if source.resolve() == destination.resolve():
            raise ContractError("input and output paths must be different")
        with source.open("r", encoding="utf-8") as file_handle:
            event = json.load(file_handle)
        event = validate_event(event)
        result = process_event(event)
        write_json_atomically(destination, result)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    print(
        "PASS: audit feedback processed; "
        f"findings={result['processing_summary']['findings_seen']}, "
        f"requests={result['processing_summary']['requests_generated']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
