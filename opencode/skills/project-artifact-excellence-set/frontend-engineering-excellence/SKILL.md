---
name: frontend-engineering-excellence
description: Build responsive interfaces with optimized Core Web Vitals and resilient client state. Use when crafting user interfaces or improving load performance or managing client state or ensuring cross-browser quality. Triggers include build frontend UI or improve Web Vitals or fix layout shift or manage client state or optimize rendering.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
    - accessibility-inclusive-design@>=1.0.0
  provides: []
---

# Frontend Engineering Excellence

## Purpose
Build responsive interfaces that load fast, stay stable, and recover gracefully. Provide procedural guidance for layout, rendering, client state, and cross-browser verification that base model knowledge leaves underspecified. Treat measurable quality attributes as release gates and treat human factors as first-class for users on varied devices, networks, and abilities. Keep interaction latency low and visual stability high.
Use this skill when crafting new screens, repairing Web Vitals regressions, stabilizing client state, or certifying cross-browser quality. Cover the full path from performance budget to verified release, including rendering strategy, resilience patterns, and handoff to accessibility-inclusive-design for inclusive verification.
When speed and richness compete, protect interaction responsiveness and layout stability first, then layer richness behind budgets. Record budget decisions, state ownership, and verification results so reviewers and future maintainers can reason about trade-offs without reverse-engineering the interface.

## Core Operating Principles
- Optimize for Core Web Vitals on real devices and throttled networks, not only on fast desktops.
- Keep client state explicit, minimal, and resilient to reloads, offline gaps, and race conditions.
- Isolate failures with error boundaries so one widget never breaks the whole page.
- Verify across target browsers and viewports before declaring work complete.
- Hand off accessibility checks to accessibility-inclusive-design and fix findings before release.
- Measure rendering cost and network cost on every significant interface change.
- Prefer progressive enhancement over fragile client-only assumptions.
- Demand evidence from field and lab data before claiming performance gains.
- Reserve layout space for media and dynamic regions to prevent visible shift.
- Defer non-critical work until after first meaningful paint and first interaction.
- Keep data fetching separate from presentation so each layer stays testable.
- Write loading and error states first, before the happy path, for every data view.
- Keep tap targets at least 44px and spacing generous for touch and pointer users.
- Preserve scroll position and focus across re-renders, filters, and pagination.
- Lazy-load images below the fold with explicit dimensions to prevent shift.
- Confirm offline and degraded-network behavior before calling a flow complete.
- Keep analytics and consent handling transparent so tracking never surprises the user.

## Process
1. **Clarify interface scope** — Capture routes, user goals, data sources, target browsers, and device constraints. Declare non-goals.
   - List the 5 most critical journeys and their entry points.
   - Record network assumptions including throttled 4G and offline gaps.
   - Confirm which browsers and viewport widths define the support matrix.
2. **Establish performance budget** — Set limits for bundle size, image weight, request count, LCP, INP, and CLS. Record baselines.
   - Cap route JavaScript under 200KB compressed where feasible.
   - Limit third-party scripts to 3 per page with deferred loading.
   - Store baseline LCP, INP, and CLS values with device and network notes.
3. **Design client state** — Map server state, UI state, and cached state. Define ownership, invalidation, and conflict rules.
   - Separate server cache from form drafts and ephemeral UI flags.
   - Define cache keys, staleness windows, and retry behavior per query.
   - Plan optimistic updates only where rollback stays safe and simple.
4. **Build rendering path** — Structure components, code-split routes, defer non-critical work, stabilize layout slots, and reserve media space.
   - Split by route and defer below-fold components until needed.
   - Enforce the component budget (PA-FE-03): at most one component per visual role per route; prefer composition over new abstraction; a new component ships only with a written reason why composition is insufficient.
   - Preload the LCP image and one critical font; defer the rest.
   - Animate only transform and opacity to protect frame rates.
5. **Add resilience** — Implement loading states, empty states, error boundaries, retry controls, and offline messaging.
   - Place boundaries at route level and around third-party widgets.
   - Preserve user input across failures and reloads for longer forms.
   - Provide retry, go-back, and support actions on every failure panel.
6. **Verify cross-browser** — Test current Chrome, Safari, Firefox, and Edge plus one small viewport and one large viewport. Record defects.
   - Test 360px and 1440px widths plus one tablet width.
   - Log rendering, input, and navigation defects with browser and version.
   - Confirm zero blocking defects on declared browsers before rollout.
7. **Complete accessibility handoff** — Run keyboard pass, focus check, contrast check, and screen-reader pass with accessibility-inclusive-design guidance.
   - Confirm full keyboard completion on at least 10 core journeys.
   - Verify focus visibility during route changes, dialogs, and async updates.
   - File remaining gaps with severity and fix dates before release.
8. **Measure and release** — Collect lab and field Web Vitals, review regressions, fix layout shifts, then approve rollout with rollback plan.
   - Block release when any vital regresses by more than 10 percent versus baseline.
   - Export Web Vitals and client errors to shared telemetry by route.
   - Schedule a post-release field-data review within 14 days.
9. **Record and hand off** — Publish budgets, state maps, verification matrices, and rollback notes where the team can find them.
   - Attach lab and field Web Vitals snapshots with device and network context.
   - Name owners and review dates for every budget, flag, and cached query.

## Quality Attributes
Maintain these quality attributes as binding constraints for every interface change.
- Performance — Hold LCP at or under 2500ms, INP at or under 200ms, and CLS under 0.1 on the 75th percentile of page loads.
- Responsiveness — Keep input response under 100ms for common actions and show feedback within 200ms for slower tasks.
- Resilience — Recover from failed fetches, expired sessions, and malformed data without full-page loss in at least 99 percent of sampled failures.
- Testability — Cover state transitions, error paths, and critical journeys with component plus integration plus end-to-end tests.
- Maintainability — Keep components small, typed, and documented. Isolate data fetching from presentation logic. Hold cyclomatic complexity at or under 10 per component and review test-code duplication with the same rigor as production code.
- Compatibility — Support declared browsers with zero blocking defects and degrade gracefully outside that matrix.
- Observability — Emit client timing, route changes, error counts, and Web Vitals to shared telemetry with session correlation.
- Accessibility readiness — Arrive at handoff with semantic markup, labeled controls, and logical focus order already in place.
- Cost awareness — Constrain bundle size, image weight, and third-party cost per route against the declared budget.
- Operability — Ship route-level dashboards, client error triage notes, and rollback steps with every release.
- Compatibility — Version cached payloads and feature flags so staged rollouts never strand users on mixed states.
- Auditability — Record budget decisions, browser matrices, and verification results with dates for traceability.

## Human Factors and Usability
Protect attention, comprehension, and control across diverse users and contexts.
- Preserve layout stability so controls never jump under the pointer during load.
- Provide immediate feedback for taps, saves, and navigation even when the network lags.
- Write loading and error messages that explain status, next action, and expected wait.
- Keep focus visible and predictable during route changes, dialogs, and async updates.
- Reduce cognitive load with progressive disclosure, consistent patterns, and reversible actions.
- Support low-vision, keyboard-only, and reduced-motion needs through the accessibility handoff.
- Build trust with honest status, preserved input on failure, and clear recovery paths that respect user effort.
- Keep primary actions prominent with at most two secondary actions per view.
- Confirm destructive actions explicitly and offer undo where the platform allows it.
- Test comprehension with at least 5 task walkthroughs before declaring polish complete.
- Announce async results politely so screen-reader and sighted users share the same understanding of state.
- Keep undo and navigation stable so exploration never punishes the user with lost work.

## Success Metrics
- Trigger performance: Definition: correct activation on interface crafting, load-performance, client-state, and cross-browser requests (member samples at least 20 frontend prompts per 30-day window); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 20 sampled frontend prompts per 30-day window; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: scoped interface plus state plus verification tasks completed with passing checks per engagement; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: interface verification records with Core Web Vitals evidence; Sample: scoped engagements with verification tasks; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for interface delivery (member keeps SKILL.md near 190 lines and cuts context use by at least 30 percent versus full manual review); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: typical interface tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a competent engineer ships a measured interface improvement on a bounded page; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: bounded-page improvement sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: visual plus state regressions remaining per release with zero known blocking cross-browser defects within 14 days (member standard is at most 2 regressions per release); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: regression and cross-browser records; Sample: all releases in the observation window; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Degraded Web Vitals — Audit bundle, images, fonts, and third parties. Defer non-critical scripts, compress media, split routes, then re-measure LCP, INP, and CLS.
- Layout shift — Reserve width and height for media and embeds, stabilize fonts, avoid late injection above content, then verify CLS under 0.1.
- Fragile client state — Centralize ownership, normalize entities, add invalidation rules, handle race with request IDs, then add state transition tests.
- Load lag on slow networks — Add skeletons, prioritize above-fold data, paginate lists, cache repeated queries, then test on throttled 4G.
- Cross-browser breakage — Isolate failing browser, reduce to minimal case, replace unsupported APIs with guarded fallbacks, then expand verification matrix.
- Error boundary gaps — Map component tree, add boundaries at route and widget levels, log caught errors with context, then test failure injection.
- Stale cache confusion — Shorten time-to-live, add version keys, surface refresh status, then verify fresh data within one refresh cycle.
- Third-party drag — Defer or remove heavy embeds, facade social widgets until interaction, then confirm vital recovery in lab and field.
- Hydration mismatch — Align server and client rendering inputs, remove nondeterministic content from first paint, then verify with strict-mode double render.
- Focus loss on navigation — Restore focus to the new view heading, announce the change politely, then test keyboard journeys across routes.
- Bundle regression — Diff bundle output per route, flag additions over 10KB compressed, then split or defer the new weight.
- Component-budget violation — Reject new components without written composition rationale; fold into composition or tokens; add a token lint check when drift appears.
- Stale verification matrix — Reconfirm browser versions quarterly, retire unsupported targets, then update the support statement.

## References
- Design tokens and components contract (grid, state matrix, naming): ../human-centric-visual-excellence/references/design-tokens-and-components.md
- Web Vitals optimization playbook: references/web-vitals-playbook.md
- Client state resilience patterns: references/client-state-patterns.md
- Accessibility handoff checks: ../accessibility-inclusive-design/references/wcag-checklist.md
- Unified remediation playbook: ../shared/references/unified-remediation-playbook.md
