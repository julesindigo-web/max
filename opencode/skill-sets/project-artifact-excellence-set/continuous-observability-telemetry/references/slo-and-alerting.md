# SLO and Alerting

Define SLOs that reflect user pain and alert only on real harm.

## Define SLIs

- Measure availability as successful responses divided by valid requests.
- Measure latency as p95 and p99 per critical operation.
- Measure error rate by operation and error class, not only globally.
- Measure freshness for pipelines as event age at delivery.
- Window SLIs over 28 days for SLOs and 1 hour and 6 hours for fast burn.

## Set SLO Targets

- Hold core read availability at 99.9% or higher over 28 days.
- Hold p95 latency under 100ms for standard backend operations.
- Hold frontend LCP under 2500ms and INP under 200ms at 75th percentile.
- Hold pipeline freshness within 5 minutes of event time for 99% of events.
- Document owners, users, and consequences for each SLO breach.

## Configure Alerts

- Page only when burn rate exceeds 14x over 1 hour or 6x over 6 hours.
- Ticket lower burn rates for next-business-day review.
- Attach runbook, dashboard, and trace query links to every alert.
- Deduplicate by service, operation, and error class to cut noise.
- Review alert volume weekly and keep pages under 2 per on-call shift.

## Run Incident Diagnosis

- Start from SLO burn chart, then open top failing spans.
- Pivot from span to correlated logs with one click.
- Record detection, triage, mitigation, and resolution timestamps.
- Preserve queries and trace links in the incident record.
- Declare recovery only after burn rate returns to normal for 30 minutes.

## Learn and Improve

- Hold post-incident review within 5 days with blameless notes.
- File actions with owners and due dates within 30 days.
- Update SLOs, thresholds, and runbooks from findings.
- Track time-to-detect under 5 minutes and time-to-mitigate under 30 minutes.
- Report residual risk and monitoring gaps after each major incident.
