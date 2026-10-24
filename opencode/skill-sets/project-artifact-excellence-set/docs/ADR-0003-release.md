# ADR-0003 — Deterministic Release with Additive Gates

- Status: Accepted (v2.0.0)
- Context: reproducibility and link/TOC/context-budget drift needed machine checks.
- Decision: keep SOURCE_DATE_EPOCH deterministic ZIP + SHA-256 manifest; add task-ledger, trigger-scorer, link/TOC, and context-budget gates as gate 7 (now 7/8) without breaking 1.3.0 validators.
- Consequences: 8-gate `validate-set.sh`; new executables listed in release_artifact_utils.py.
