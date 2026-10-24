# Observability Standard (Shared)

Canonical cross-skill telemetry baseline for backend and frontend members.
`continuous-observability-telemetry` implements it; delivery and audit
members verify emission in production.

## Pillars
1. Structured logs with correlation identifiers propagated across service
   boundaries. No secrets or personal data in log fields.
2. Request and saturation metrics with explicit units, SLO thresholds, and
   observation windows. Every critical journey has at least one
   user-outcome metric plus one system-health metric.
3. Distributed tracing following OpenTelemetry conventions, sampled to keep
   overhead within the member skill budget (document the sampling rule).

## SLO Discipline
- Define service-level indicators before alerting. Alert on symptoms that
  affect users, with runbook links and severity tiers.
- Record data source, aggregation window, and owner for every alert.
  An alert without an owner is a Major gap.

## Verification Method
- Pre-release: emit a synthetic trace through the critical path and confirm
  all three pillars arrive in the collector.
- Post-release: review burn-rate visibility within the first observation
  window. Missing health signals after deploy blocks release acceptance.

## Traceability
- Member detail: `continuous-observability-telemetry/references/`.
- Remediation: `unified-remediation-playbook.md`.
