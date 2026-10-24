# Project Artifact Audit Report (Sample — Canonical v2.0.0)

**Artifacts audited:** sample PRD v0.3 (2026-10-10), architecture doc v0.3, OpenAPI 3.1 excerpt
**Audit date / as-of:** 2026-10-15
**Lifecycle stages covered:** discovery, architecture, implementation readiness
**Overall maturity assessment:** 3/5 — core journeys defined; NFRs and traceability incomplete
**Human Factors maturity:** 3/5
**Full-Stack Technical maturity:** 3/5

## Executive Summary
- Strengths: clear problem statement; versioned contracts draft.
- Critical & Major: 0 Critical, 2 Major (1 human, 1 technical), 2 Minor, 1 Suggestion.
- Themes: make NFRs measurable; close traceability orphans.
- Residual risk: performance and accessibility claims remain UNVERIFIED pending runtime/user evidence.

## Findings Matrix
| ID | Location | Dimension | Severity | Finding (1-sentence) | Impact (Human / Tech / Ops) |
|---|---|---|---|---|---|
| PA-REQ-01 | PRD §3.2 | Outcome metrics | Major | Dashboard latency target lacks percentile, device, and window. | User waits unpredictably / cannot verify / SLO gap |
| PA-TRC-01 | Arch §2 vs PRD R-07 | Traceability | Major | Checkout recovery has no design element or test mapping. | User data-loss risk / unverified path / release risk |

## Detailed Findings & Remediations
### PA-REQ-01 — Unmeasurable latency target
- Evidence state: `Verified`
- Confidence: high — quoted text inspected on 2026-10-15.
- Evidence/source: PRD §3.2: The system should be fast.
- Verification method: direct inspection + weasel-word scan.
- Severity basis: mandatory-control gap with conditional user-harm exposure on the critical path.
- Impact rationale: users face unpredictable waits; team cannot verify; SLO cannot be set.
- Root cause: NFR written as adjective without scenario (inference).
- Recommended remediation: Given p95 authenticated users on mid-range mobile over 4G, dashboard LCP ≤2.5 s, measured by RUM p75 segmented mobile/desktop over a 28-day window.
- Effort / Priority / AC: S / P1 / RUM dashboard shows p75 LCP with segment + window.
- Residual uncertainty: field baseline not yet collected; lab check first.

## Cross-Artifact / Cross-Layer Consistency & Traceability
Matrix excerpt: `checkout-recovery (user outcome) → R-07 → (missing design) → (missing test) → (no signal)` = orphan → Major.

## Prioritized Remediation Backlog
1. PA-REQ-01, 2. PA-TRC-01, 3. minors/suggestions.

## Residual Risks & Recommended Next Actions
- Load-test design, accessibility audit with AT, and threat-model review before release.
- No skill-gap escalation: single-project issues without recurrence or explicit gap evidence.
