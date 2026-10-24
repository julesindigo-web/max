---
name: accessibility-inclusive-design
description: Ensure WCAG 2.1 AA interfaces with correct ARIA and keyboard navigation for all users. Use when auditing accessibility or adding ARIA semantics or fixing contrast or enabling keyboard flows. Triggers include accessibility audit or fix ARIA or check contrast or enable keyboard navigation or meet WCAG standard.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
  provides: []
---

# Accessibility Inclusive Design

## Purpose
Ensure interfaces work for all users, including keyboard-only, screen-reader, low-vision, motor-limited, and cognitively diverse people. Provide procedural guidance for WCAG 2.1 AA conformance, ARIA semantics, keyboard flows, contrast, and inclusive language that base model knowledge leaves underspecified. Treat measurable quality attributes as release gates and treat human factors as the definition of done. Remove exclusion risks before release.
Use this skill when auditing a flow, adding semantics to custom controls, repairing contrast, enabling keyboard operation, or certifying WCAG conformance. Pair automated scans with manual assistive-technology verification on every scoped flow, and file remaining gaps with severity and fix dates.
When aesthetics and access compete, change the design until both hold, and never ship a known barrier as a polish trade-off. Record conformance evidence, assistive-technology results, and open gaps so auditors, operators, and future maintainers can verify inclusion without re-running the full audit.

## Core Operating Principles
- Design keyboard-first and confirm every action works without a pointer.
- Apply native semantics first and add ARIA only where native elements fall short.
- Meet WCAG 2.1 AA as the minimum bar and aim for AAA where feasible.
- Verify with assistive technology, not only with automated checkers.
- Write inclusive language that respects identity, ability, and culture.
- Keep focus visible, predictable, and never trapped.
- Treat accessibility defects as functional defects with severity and fix dates.
- Demand evidence from manual and automated checks before claiming conformance.
- Preserve meaning when styles, scripts, or images fail to load.
- Support 200 percent zoom, high-contrast modes, and reduced-motion settings.
- Announce dynamic changes politely without stealing focus unexpectedly.
- Involve disabled users in testing where feasible and compensate fairly.
- Keep touch targets generous and operable with switch, voice, and alternative input.
- Provide text alternatives for charts, diagrams, and status conveyed by shape alone.
- Confirm form autocomplete, error prevention, and review steps for high-stakes input.
- Never remove visible focus for aesthetic reasons in any theme or state.
- Test error prevention on every destructive and financial step before sign-off.

## Process
1. **Clarify conformance scope** — List pages, flows, components, target level AA, and assistive technology matrix. Declare exclusions with rationale.
   - Name the screen reader, browser, and version matrix for verification.
   - Confirm which flows must meet AA and which aim for AAA.
   - Record known limits and planned remediation dates up front.
2. **Audit baseline** — Run automated checks plus keyboard pass plus screen-reader pass. Record violations with location and impact.
   - Log page, component, criterion, result, and tool version per check.
   - Mark any barrier that blocks task completion as critical.
   - Capture screenshots and accessibility-tree snapshots for evidence.
3. **Fix semantics** — Replace div-buttons with buttons, label every input, group related controls, and correct heading order.
   - Give every control an accessible name from visible text where possible.
   - Keep heading levels ordered without skips for structure.
   - Group related inputs with fieldset and legend or equivalent roles.
4. **Enable keyboard flows** — Define tab order, focus targets, skip links, dialog traps with escape, and visible focus styles.
   - Keep focus order matched to visual order across breakpoints.
   - Move focus into dialogs on open and return it on close.
   - Provide skip links that become visible on focus.
5. **Repair contrast and visuals** — Adjust text, icon, and focus-indicator contrast. Support 200 percent zoom and reduced-motion needs.
   - Meet 4.5 to 1 for normal text and 3 to 1 for large text and essential graphics.
   - Hold focus indicators at 3 to 1 contrast against adjacent colors.
   - Reflow content without horizontal scrolling at 400 percent equivalent widths where required.
6. **Verify with assistive technology** — Test with at least one screen reader and one magnification workflow. Confirm announcements and order.
   - Confirm roles, names, and states match visual meaning on sampled controls.
   - Check error, loading, and success announcements for politeness and clarity.
   - Test magnification at 200 percent with high-contrast themes enabled.
7. **Check language and cognition** — Simplify instructions, define jargon, keep error guidance concrete, and confirm reading level suits audience.
   - Write one idea per instruction with consistent verbs across the flow.
   - Pair icons with text labels instead of relying on icon-only meaning.
   - Offer extra time or pause controls where timing could exclude users.
8. **Certify and monitor** — Record pass and fail evidence, file remaining gaps with severity, add regression checks, and schedule re-audit within 90 days.
   - Store the evidence log with the release record for audit traceability.
   - Add automated plus manual regression checks to the release pipeline.
   - Assign owners and dates for every open accessibility gap.
9. **Record and hand off** — Publish the evidence log, patterns, and retest scripts where the team and auditors can find them.
   - Attach tool versions, assistive-technology matrices, and pass or fail notes per criterion.
   - Name owners and re-audit dates for every open barrier and regression check.

## Quality Attributes
Maintain these quality attributes as binding constraints for every accessibility change.
- Conformance — Meet 100 percent of applicable WCAG 2.1 AA criteria on scoped flows with evidence per criterion.
- Keyboard operability — Support full task completion by keyboard alone with zero traps across at least 10 core journeys.
- Screen-reader clarity — Provide correct roles, names, and states so announcements match visual meaning in at least 95 percent of sampled controls.
- Visual adaptability — Sustain usability at 200 percent zoom, high-contrast modes, and reduced-motion settings with zero loss of function.
- Understandability — Keep instructions, labels, and errors plain, consistent, and actionable for diverse cognitive needs.
- Testability — Pair automated scans with manual keyboard and screen-reader scripts that run on every release.
- Maintainability — Document patterns, ARIA usage rationale, and known limits so future changes preserve conformance.
- Robustness — Expose correct name, role, and value for custom controls and keep status messages programmatically determinable.
- Accountability — Track open barriers with severity, owner, and fix date until verified closed.
- Operability — Ship evidence logs, retest scripts, and assistive-technology matrices with every release for audit traceability.
- Compatibility — Confirm conformance across declared browsers, screen readers, magnification, and contrast themes.
- Privacy — Handle accessibility test recordings and personal data with consent, minimization, and fixed retention windows.

## Human Factors and Usability
Center dignity, autonomy, and ease for people with diverse abilities and contexts.
- Announce what changed, where focus moved, and what to do next after async updates.
- Keep error recovery kind and specific with field-level guidance and preserved input.
- Offer multiple input paths where motion, timing, or precision creates barriers.
- Respect cognitive load with short sentences, consistent terms, and one idea per instruction.
- Support situational limits such as glare, noise, one-handed use, and low bandwidth.
- Use inclusive language free of idioms, ableist terms, and gendered defaults unless user data requires it.
- Co-design with disabled users where feasible and compensate testers fairly for their expertise.
- Measure task success and satisfaction separately for assistive-technology users to catch hidden exclusion.
- Avoid flashing content above 3Hz and provide pause controls for moving content.
- Confirm confirmation and undo patterns for high-stakes actions across input modalities.
- Test with real devices, real keyboards, and real assistive technology instead of emulators alone.
- Publish an accessibility statement with scope, level, contact path, and re-audit date for scoped flows.

## Success Metrics
- Trigger performance: Definition: correct activation on accessibility audit, ARIA, contrast, and keyboard-flow requests (member samples at least 20 accessibility prompts per 30-day window); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 20 sampled accessibility prompts per 30-day window; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: scoped audit plus remediation plus verification tasks completed with passing checks per engagement; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: engagement checklists with WCAG 2.1 AA evidence; Sample: scoped engagements with verification tasks; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for inclusive delivery (member keeps SKILL.md near 190 lines and cuts context use by at least 30 percent versus full manual review); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: typical audit tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a competent practitioner completes a bounded accessibility audit on a representative flow; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: representative-flow audit sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: accessibility escapes remaining after release (member standard is at most 1 per release with zero known critical barriers within 14 days); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: escape register and barrier review; Sample: all releases in the observation window; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Incorrect ARIA — Remove redundant roles, match ARIA to visual state, test announcements, then prefer native elements where possible.
- Keyboard trap — Map tab order, add escape and focus return, restore logical sequence, then verify full keyboard completion.
- Low contrast — Raise foreground or background contrast to AA ratios, test across themes, then verify with contrast tools and user checks.
- Missing labels — Add programmatic labels, associate help and error text, confirm name computation in accessibility tree, then retest with screen reader.
- Focus loss on update — Set focus to status region or restored control, announce outcome politely, preserve scroll context, then test async flows.
- Motion or timing barrier — Extend or remove time limits, honor reduced-motion, provide pause controls, then confirm task completion without time pressure.
- Heading disorder — Reorder headings to a logical outline, expose one h1 per page, then verify navigation by headings in a screen reader.
- Icon-only meaning — Add visible text or accessible names to icon buttons, then confirm comprehension without color or shape alone.
- Table confusion — Add captions, scope headers, and linearize complex tables for small screens and screen readers, then verify cell announcements.
- Form timeout loss — Preserve input on timeout, warn before expiry, offer extension, then test recovery without data loss.
- Status silence — Add live regions for async results, confirm announcements in testing, then verify focus stays predictable.
- Regression drift — Re-run the full manual script quarterly, diff results against baseline, then file new gaps before they accumulate.

## References
- WCAG 2.1 AA checklist and evidence log: references/wcag-checklist.md
- ARIA roles and keyboard patterns: references/aria-and-keyboard-patterns.md
- Human factors deep reference: ../project-artifact-auditor/references/human-factors-usability.md
- Unified remediation playbook: ../shared/references/unified-remediation-playbook.md
