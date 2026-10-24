---
name: human-centric-visual-excellence
description: Craft premium human-centric interfaces with spatial harmony and luxury motion design. Use when elevating visual quality or reducing cognitive load or designing micro-interactions or building emotional resonance. Triggers include improve visual design or polish interface or design motion or refine typography or elevate luxury feel.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
    - accessibility-inclusive-design@>=1.0.0
  provides: []
---

# Human Centric Visual Excellence

## Purpose
Craft premium interfaces that feel calm, clear, and trustworthy. Provide procedural guidance for visual hierarchy, spacing, typography, color, progressive disclosure, and luxury motion that base model knowledge leaves underspecified. Treat measurable quality attributes as release gates and treat human factors as the primary design constraint. Reduce cognitive load while building emotional resonance through restraint and precision.
Use this skill when elevating an existing screen, launching a premium surface, or repairing a cluttered flow. Extend the human-factors guidance from project-artifact-auditor with concrete visual tokens, spacing rhythms, and motion rules that reviewers can verify without guesswork.
When beauty and clarity compete, choose clarity first and earn beauty through restraint, rhythm, and precise tokens. Record token decisions, disclosure rationale, and motion purposes so reviewers and future designers can extend the system without diluting its premium feel.

## Core Operating Principles
- Lead with hierarchy so the eye lands on the primary action within 3 seconds.
- Use whitespace strategically to separate meaning, not merely to decorate.
- Hold color contrast and readability above decoration in every decision.
- Disclose complexity progressively and keep the default view focused on one task.
- Choreograph micro-interactions with organic easing that confirms cause and effect.
- Align palette, type, and motion with trust, calm, and premium feel.
- Extend human-factors guidance from project-artifact-auditor with visual specifics.
- Demand evidence from usability checks before declaring polish complete.
- Reuse design tokens for type, spacing, color, and motion with zero one-off values.
- Honor reduced-motion preferences and never let animation block task completion.
- Test readability at small sizes, high zoom, and outdoor glare conditions.
- Keep the default path obvious so first-time users succeed without instruction.
- Pair every color meaning with text or icon cues for color-blind and low-vision users.
- Scale touch targets and spacing generously on mobile without crowding content.
- Test designs in both light and dark themes where the product supports them.
- Archive explorations and keep production tokens clean, named, and documented.
- Review copy alongside visuals since words carry half the hierarchy weight.

## Process
0. **Freeze art direction before code (PA-ART-01)** — Publish a one-page Art Brief and get it signed before any implementation. No code without it.
   - Name 3 brand adjectives plus 1 anti-adjective (what this product is NOT) and 3 concrete differentiators versus named generic-template competitors.
   - Declare type voice (at most 1 display plus 1 body family), palette roles with the emotion each carries, and imagery rules: photo versus illustration, masking or duotone treatment, and forbidden stock tropes.
   - Define page rhythm as a repeatable cadence (for example hero, proof, detail, call-to-action) and attach 2 reference screens: one aspirational, one anti-reference.
   - Gate: a reviewer who sees only a grayscale wireframe plus swapped copy can still name the brand; target brand-recall at least 80 percent on 5 respondents per brief. Version the brief per release.
1. **Clarify emotional intent** — Capture audience, brand promise, primary task, and desired feeling. Declare what luxury means for this context.
   - Record adjectives for the target feeling such as calm, confident, and refined.
   - List competing products and note where restraint can differentiate.
   - Confirm which user task defines success for this screen.
2. **Audit current hierarchy** — Map headings, actions, and feedback by visual weight. Flag competing focal points and noisy regions.
   - Rank every element by size, weight, color, and position prominence.
   - Mark elements that fight the primary action for demotion or removal.
   - Photograph the small-viewport layout to catch collapsed hierarchy faults.
3. **Apply type and spacing system** — Set modular type scale, line height, and golden-ratio spacing steps. Align to an 8px grid.
   - Assign one size per role across body, label, heading, and display.
   - Hold body at 16px or larger with line height 1.5 or higher.
   - Keep section spacing at least twice the inner element spacing.
4. **Refine color and contrast** — Choose a restrained palette, assign semantic roles, verify contrast ratios, and test readability at small sizes.
   - Define roles for background, surface, text, border, accent, success, warning, and danger.
   - Restrict interactive accents to one color used consistently.
   - Verify AA contrast for text and essential controls in every theme.
5. **Simplify with disclosure** — Collapse secondary options, stage complex flows, preserve context, and keep undo visible.
   - Show only fields required for the current step.
   - Add progress, headers, and summaries on multi-step flows.
   - Keep back, save, and undo reachable without hunting.
6. **Design motion** — Define duration, easing, and purpose for hover, press, appear, and transition states. Keep motion under 300ms for feedback.
   - End feedback motion between 120ms and 300ms with eased curves.
   - Animate only transform and opacity for smooth frame rates.
   - Document each motion token with duration, curve, and purpose.
7. **Verify human response** — Test comprehension, task time, error rate, and comfort with at least 5 users or reviewers. Fix overload points.
   - Measure correct first-click choice on core flows against a 90 percent bar.
   - Record task time before and after simplification.
   - Treat confusion clusters as defects with severity and fix dates.
8. **Confirm accessibility alignment** — Check contrast, focus visibility, motion sensitivity, and screen-reader order with accessibility-inclusive-design.
   - Test keyboard completion and visible focus on interactive prototypes.
   - Confirm announcements match visual meaning for dynamic regions.
   - Honor reduced-motion settings with instant final states.
9. **Record and hand off** — Publish tokens, rationale, and acceptance checks where engineers and reviewers can find them.
   - Attach before-and-after captures with task-time and first-click evidence.
   - Name token owners and review dates for every scale, palette, and motion decision.

## Quality Attributes
Maintain these quality attributes as binding constraints for every visual change.
- Clarity — Achieve correct first-click choice in at least 90 percent of sampled tasks on core flows.
- Readability — Hold body text at 16px or larger with line height 1.5 or higher and contrast that meets AA targets.
- Consistency — Reuse type, spacing, color, and motion tokens with zero one-off values in production styles.
- Responsiveness — Preserve hierarchy and spacing rhythm from 360px to 1440px without overlap or truncation.
- Motion quality — Keep feedback motion between 120ms and 300ms with eased curves and honor reduced-motion preferences.
- Testability — Record design tokens, decisions, and acceptance checks so reviewers can verify without guesswork.
- Observability — Track task success, task time, and rage-click or backtrack signals where instrumentation exists.
- Inclusivity — Sustain comprehension across low vision, magnification, and reduced-motion contexts with zero loss of function.
- Craft durability — Keep styles maintainable with named tokens, documented roles, and versioned updates.
- Operability — Ship token documentation, theme notes, and rollback guidance so visual updates stay safe to review and revert.
- Compatibility — Preserve hierarchy and motion intent across supported browsers, themes, and text-scaling settings.
- Auditability — Record visual decisions, token changes, and review outcomes with dates for traceability.

## Human Factors and Usability
Design for attention, memory, comfort, and trust across diverse users.
- Limit each view to one primary action and at most two secondary actions.
- Group related controls by proximity and separate unrelated groups with generous space.
- Use progressive disclosure to keep working memory load under 4 concurrent choices.
- Write labels in plain language that predict outcome before interaction.
- Provide calm confirmation for success and clear recovery for errors without blame.
- Respect reduced motion, low vision, and situational glare with adaptable visual settings.
- Build emotional resonance through rhythm, restraint, and tactile-quality transitions that never delay task completion.
- Validate with cognitive walkthroughs that trace perception, comprehension, decision, and action for each critical step.
- Keep line length between 45 and 75 characters for comfortable reading on desktop.
- Preserve context during staged flows so users never wonder where they are or what remains.
- Test designs with at least 3 users under real lighting, glare, and device constraints where feasible.
- Keep empty states helpful with guidance, examples, and a clear next action instead of blank space.

## Success Metrics
- Trigger performance: Definition: correct activation on hierarchy, typography, motion, and spatial-harmony requests (member samples at least 20 visual-design prompts per 30-day window); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 20 sampled visual-design prompts per 30-day window; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: scoped hierarchy plus typography plus motion tasks completed with passing review per engagement; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: design review records with human-factors evidence; Sample: scoped engagements with review tasks; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for premium visual delivery (member keeps SKILL.md near 190 lines and cuts context use by at least 30 percent versus full manual review); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: typical design tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a competent designer produces a polished mock or style fix on a bounded screen; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: bounded-screen design sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: visual regressions remaining per release with zero known contrast or focus-visibility failures within 14 days (member standard is at most 2 regressions per release); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: regression and contrast/focus records; Sample: all releases in the observation window; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Cluttered hierarchy — Remove competing emphasis, resize to one dominant focal point, increase whitespace by one spacing step, then retest first-click choice.
- Weak readability — Raise size, weight, or contrast one step, shorten line length to 45 to 75 characters, then verify contrast and legibility.
- Over-animation — Cut duration under 300ms, replace bouncy curves with gentle ease, remove non-essential motion, then test with reduced-motion enabled.
- Palette mistrust — Reduce saturated colors, assign one accent for action, align neutrals for calm, then validate emotional response with reviewers.
- Disclosure confusion — Restore context headers, add breadcrumbs or progress, keep back and undo reachable, then test task completion without help.
- Motion-induced discomfort — Provide instant final state, honor reduced-motion setting, avoid parallax and autoplay, then confirm comfort reports.
- Token drift — Audit styles for one-off values, fold them into tokens, document roles, then add a token lint check to review.
- Missing or divergent Art Brief — Halt implementation; freeze the one-page brief with signature; run the grayscale-wireframe brand-recall check before proceeding.
- Glare and zoom failure — Test at 200 percent zoom and high brightness, raise contrast one step, then confirm zero loss of function.
- Flat feedback — Add tactile press states, loading shimmer that matches layout, and quiet success confirmation, then measure perceived responsiveness.
- Theme breakage — Audit light and dark themes for contrast, elevation, and focus visibility, then fix token gaps before release.
- Inconsistent density — Standardize spacing steps across breakpoints, remove ad-hoc padding, then verify rhythm at 360px and 1440px.
- Copy-hierarchy mismatch — Align headline promise with primary action, cut competing messages, then retest first-click choice.

## References
- Design tokens and components contract (grid, states, naming, lint): references/design-tokens-and-components.md
- Visual hierarchy and spacing system: references/visual-hierarchy-system.md
- Motion and micro-interaction craft: references/motion-and-micro-interactions.md
- Human factors deep reference: ../project-artifact-auditor/references/human-factors-usability.md
- Contrast and focus checks: ../accessibility-inclusive-design/references/wcag-checklist.md
