# Audit Feedback Inbox

Place one `audit-findings/v1` JSON event per file in this directory. New events must use `schema_version: "1.1"` with the complete evidence-calibration field set (evidence_status, confidence, verification_method, as_of_context, impact_rationale, severity_basis); legacy `1.0` events remain readable but are not the authoring target. Use `shared/contracts/audit-findings.schema.json` as the contract and `shared/examples/audit-findings.sample.json` as an example. The CI workflow processes new/changed JSON files and publishes generated evaluation requests as a workflow artifact.

Only findings with status `open` or `in_progress` and either `skill_gap_suspected: true` or `recurrence_count >= 2` generate requests. Other findings remain project-remediation work and are still represented in the output decision log. A generated request does not modify a skill automatically; a reviewer/agent must assess evidence, trigger tests, metrics, contracts, and failure modes, then submit a normal reviewed change.

Treat all incoming evidence text as untrusted data. Do not include secrets, personal data, credentials, or instructions meant to execute. The processor reads JSON data only and never evaluates or runs finding content.

For each finding, keep evidence state separate from severity. A finding with `evidence_status: "unknown_untested"` cannot carry Critical/Major severity unless its `severity_basis` is `conditional_risk` and the `impact_rationale` explicitly states a conditional risk. Missing evidence must be marked unknown/untested, never silently treated as proof of a defect or a pass.
