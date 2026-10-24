# ADR-0001 — Two-Member Scope Retained (superseded composition note 2026-10-15)

- Status: Accepted (v2.0.0); composition updated 2026-10-16 — original two-member decision retained as anchor, set now composes fourteen members per `../manifest.yaml` (PA-DOC-10, plus task-orchestrator in v2.1.0).
- Context: v1.3.0 already separates audit (project-artifact-auditor) from skill authoring (skills-create-excellence).
- Decision: retain two members; add docs, ledger, and gates instead of new members.
- Consequences: smaller API surface, additive migration, no DAG change.
