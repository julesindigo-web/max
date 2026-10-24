---
name: continuous-observability-telemetry
description: Instrument backend and frontend with OpenTelemetry logs and metrics and tracing for production health. Use when adding observability or diagnosing production incidents or defining SLO signals or tracing distributed flows. Triggers include add observability or instrument tracing or monitor production or debug latency or configure telemetry.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
  provides: []
---

# Continuous Observability Telemetry

## Purpose
Instrument backend and frontend with OpenTelemetry logs, metrics, and tracing to protect production health. Provide procedural guidance for instrumentation, SLO and SLI definition, alert thresholds, and incident diagnosis that base model knowledge leaves underspecified. Treat measurable quality attributes as release gates and treat human factors as first-class for on-call operators under pressure. Make every critical flow explainable in production.
Use this skill when adding new telemetry, diagnosing latency or error incidents, defining SLOs, tracing distributed flows, or hardening alerting. Cover both backend services and frontend views with correlated signals so any alert leads to a trace, any trace leads to logs, and any incident leads to a documented fix.
When signal volume and signal value compete, keep the signals that explain user impact and remove the rest, even when removal feels like losing visibility. Record SLO rationale, sampling choices, and alert ownership so responders and future maintainers can trust every page without second-guessing the pipeline.

## Core Operating Principles
- Instrument once with OpenTelemetry and reuse signals across logs, metrics, and traces.
- Define SLOs before tuning alerts so paging reflects user impact.
- Correlate backend spans with frontend timing through shared trace context.
- Alert on symptoms with clear severity and ownership, not on every anomaly.
- Keep cardinality bounded so telemetry stays fast and affordable.
- Document runbooks alongside dashboards so diagnosis starts in one click.
- Demand evidence from production signals before declaring health restored.
- Protect operator attention with quiet hours, deduplication, and actionable pages.
- Name telemetry with domain language shared by developers and responders.
- Version dashboards, alerts, and runbooks in code with owners and review dates.
- Sample high-volume success aggressively while keeping 100 percent of errors.
- Review telemetry cost, volume, and alert noise on a fixed monthly cadence.
- Keep runbook commands copy-paste ready with expected output for each step.
- Tag every dashboard panel with owner, freshness, and linked alert or SLO.
- Test paging paths end to end, including rotations, escalations, and quiet hours.
- Treat flaky or unactionable alerts as defects and fix or delete them promptly.
- Keep staging telemetry faithful to production so pre-release signals stay trustworthy.

## Process
1. **Clarify health goals** — Capture critical journeys, user expectations, error tolerance, and latency targets. Declare SLO owners.
   - List the top 5 user journeys that must never go dark silently.
   - Record latency and availability expectations per journey.
   - Assign one owner per SLO with review authority.
2. **Map instrumentation points** — List services, routes, queues, jobs, and frontend views that must emit spans, metrics, and logs.
   - Mark required span names, attributes, and status rules per operation.
   - Identify queue wait versus processing segments for async flows.
   - Confirm frontend views that must report Web Vitals and client errors.
3. **Instrument with OpenTelemetry** — Add SDKs, propagators, span names, attributes, structured logs, and metric instruments with consistent naming.
   - Enable W3C trace context and baggage propagators everywhere.
   - Attach trace ID and span ID to every structured log line.
   - Keep attribute count under 15 per span and drop personal data.
4. **Define SLIs and SLOs** — Specify availability, latency, error rate, and freshness indicators with windows and burn-rate rules.
   - Window SLOs over 28 days with fast-burn windows at 1 hour and 6 hours.
   - Hold core availability at 99.9 percent or higher on critical journeys.
   - Document users, consequences, and review dates for each SLO.
5. **Set alerts and dashboards** — Configure thresholds, evaluation windows, severity levels, owners, and links to runbooks and traces.
   - Page only on fast burn with 14x over 1 hour or 6x over 6 hours.
   - Ticket slow burn for next-business-day review with context links.
   - Build one health view with SLO status, burn rate, and top failing spans.
6. **Validate end to end** — Inject test traffic, confirm trace continuity, check log correlation, and fire test alerts without paging users.
   - Verify browser-to-backend-to-datastore continuity on sampled flows.
   - Confirm log-to-trace jumps work from dashboards and alerts.
   - Test alert routing, severity, and runbook links before enabling paging.
7. **Diagnose incidents** — Follow the runbook from symptom to span to log to fix, record timeline, and preserve query links.
   - Start from SLO burn chart, then open top failing spans.
   - Record detection, triage, mitigation, and resolution timestamps.
   - Declare recovery only after burn rate stays normal for 30 minutes.
8. **Review and improve** — Hold post-incident review within 5 days, update SLOs and alerts, and track action closure within 30 days.
   - File actions with owners and due dates and verify closure.
   - Update thresholds, dashboards, and runbooks from findings.
   - Report residual risk and monitoring gaps after each major incident.
9. **Record and hand off** — Publish SLO definitions, dashboard links, and runbooks where responders and stakeholders can find them.
   - Attach SLI queries, alert thresholds, and drill records to each SLO definition.
   - Name owners and review dates for every SLO, alert, and sampling decision.

## Quality Attributes
Maintain these quality attributes as binding constraints for every observability change.
- Completeness — Cover 100 percent of critical journeys with traces, RED metrics, and structured logs in production.
- Accuracy — Keep span names, status codes, and attributes truthful so at least 95 percent of sampled traces match real execution.
- Freshness — Deliver metrics within 60 seconds and logs within 90 seconds of emission during normal load.
- Reliability — Sustain telemetry pipeline availability at 99.9 percent or higher with buffering for short outages.
- Cost control — Hold per-service cardinality under approved limits and sample high-volume spans to cap ingest growth under 10 percent per month.
- Testability — Verify instrumentation with contract tests, trace assertions, and alert simulations before release.
- Maintainability — Version dashboards, alerts, and runbooks in code with ownership and review dates.
- Actionability — Link every alert to a runbook so responders reach diagnosis within 5 minutes of paging.
- Privacy — Exclude passwords, tokens, and personal data from spans, attributes, and logs by construction.
- Operability — Ship runbook links, dashboard ownership, and escalation paths with every alert so responders never start from a blank search.
- Compatibility — Standardize telemetry naming across backend and frontend so cross-service queries work without translation tables.
- Auditability — Record SLO changes, threshold edits, and sampling decisions with dates, owners, and rationale for traceability.

## Human Factors and Usability
Design for tired operators, stressed responders, and curious developers alike.
- Name services, spans, and alerts with domain language that matches mental models.
- Show health at a glance with SLO status, burn rate, and top failing spans on one screen.
- Link every alert to a runbook with preconditions, queries, commands, and expected results.
- Reduce cognitive load with progressive disclosure from overview to span to log detail.
- Write post-incident notes in plain language with timeline, cause, fix, and follow-up owners.
- Protect focus with severity discipline so pages wake people only for user-impacting harm.
- Support accessibility in dashboards with readable contrast, keyboard navigation, and text alternatives for color-coded status.
- Measure time-to-detect and time-to-mitigate and improve the operator path, not only the tool output.
- Deduplicate alerts by service, operation, and error class to keep on-call load sustainable.
- Practice with game-day drills so the first real page never meets an untested runbook.
- Rotate on-call feedback into alert tuning so lived pain drives threshold changes.
- Celebrate quiet weeks by reviewing what stayed green and why, not only what paged.

## Success Metrics
- Trigger performance: Definition: correct activation on observability instrumentation, incident-diagnosis, and SLO-signal requests (member samples at least 20 observability prompts per 30-day window); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 20 sampled observability prompts per 30-day window; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: scoped instrumentation plus SLO plus alerting tasks completed with passing verification per engagement; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: instrumentation and alert-verification records; Sample: scoped engagements with SLO and alerting tasks; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for production-health instrumentation (member keeps SKILL.md near 190 lines and cuts context use by at least 30 percent versus full manual review); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: typical instrumentation tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a competent engineer instruments a service with SLOs and alerts on a bounded system; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: bounded-system instrumentation sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: missing-signal incidents remaining per quarter with zero known critical flows lacking traces within 30 days; Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: incident and trace-coverage records; Sample: all production flows in the observation window; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Missing traces — Check SDK setup, propagator config, sampler rules, and context headers. Redeploy one service at a time and confirm continuity.
- Noisy alerts — Raise thresholds to symptom SLOs, extend evaluation windows, deduplicate by service and error class, then measure page volume weekly.
- High cardinality — Audit label values, drop unbounded IDs, aggregate histograms, adjust sampling, then confirm cost and query speed improve.
- Log without correlation — Add trace and span IDs to every log line, align field names, backfill dashboards, then verify jump from alert to trace to log.
- Silent SLO breach — Recompute SLI queries, align windows with user journeys, add burn-rate alerts, then test with synthetic failing traffic.
- Dashboard confusion — Consolidate to one health view, clarify ownership, link runbooks, remove stale panels, then validate with on-call drill.
- Pipeline lag — Scale collectors, add local buffering for 15 minutes, prioritize error traffic, then confirm freshness returns within targets.
- Stale runbooks — Rehearse each runbook quarterly, fix broken queries and links, reassign owners, then attach the drill record to the alert.
- Sampling blind spot — Keep 100 percent of errors and slow traces, raise sampling on new releases, then verify error capture within one deploy.
- Retention gap — Align log, metric, and trace retention with post-incident needs, extend critical journey retention, then document windows publicly.
- Ownership vacuum — Assign one owner per SLO and alert, publish rotation and escalation paths, then verify pages reach a human within 5 minutes.
- Query rot — Revalidate saved dashboard and alert queries quarterly, fix renamed fields, then confirm panels render without errors.

## References
- OpenTelemetry instrumentation standard: references/opentelemetry-standard.md
- SLOs, SLIs, and alerting thresholds: references/slo-and-alerting.md
- Shared telemetry contract: ../shared/contracts/audit-findings.schema.json
- Unified remediation playbook: ../shared/references/unified-remediation-playbook.md
