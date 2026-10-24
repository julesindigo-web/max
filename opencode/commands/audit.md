---
description: Run a calibrated end-to-end audit with evidence states and prioritized remediations
agent: auditor
subtask: true
---
Perform a rigorous calibrated audit of $ARGUMENTS across the complete lifecycle (discovery to operations, human factors plus full-stack technical excellence).
Canonical skill: `project-artifact-auditor` (this command is its slash entry; there is no separate `/review-agent` — see AGENTS.md §6a).

Follow the auditor method strictly: ingest and scope, dimensional sweep with exact evidence locations, evidence-state and severity calibration on separate axes, root-cause and impact for Critical/Major findings, concrete ready-to-paste remediations, cross-artifact synthesis with one prioritized backlog, and explicit residual risk with the next validation step.

Deliver the canonical audit report format. Do not edit files; propose diffs only.

Arguments: `$ARGUMENTS` is the audit target (file, directory, PRD path, or artifact description). Examples: `/audit docs/PRD.md`, `/audit src/auth/`, `/audit audit laporan keamanan API`. When the user writes in Indonesian (e.g. `/audit audit arsitektur layanan pembayaran`), cite Indonesian source text verbatim with an English gloss.

Success criteria: every finding carries an evidence state plus confidence basis plus severity basis on separate axes; every Critical/Major finding names root cause, impact, and a regression pointer; the report ends with one prioritized backlog and the exact next validation step.
