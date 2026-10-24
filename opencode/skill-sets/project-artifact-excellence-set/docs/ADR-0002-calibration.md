# ADR-0002 — Evidence Calibration Kept Separate from Severity

- Status: Accepted (v1.3.0, reaffirmed v2.0.0)
- Context: missing evidence was at risk of being scored as pass or as automatic Critical.
- Decision: keep evidence-state, confidence, severity, and impact as independent axes; Critical/Major on unknown evidence only as explicit conditional risk.
- Consequences: checklists, playbook, feedback-loop, and validators all enforce the same rule; synchronized in v2.0.0.
