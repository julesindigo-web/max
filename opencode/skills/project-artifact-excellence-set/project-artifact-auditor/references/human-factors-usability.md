# Human Factors, Usability, Accessibility & Inclusive Design — Deep Audit Reference


## Contents
- [1. Usability goals](#1-core-usability-goals-iso-9241-11--modern-extensions)
- [2. Cognitive ergonomics](#2-cognitive-ergonomics--human-information-processing)
- [3. Heuristics](#3-nielsens-heuristics--modern-extensions-mandatory-evaluation-lens)
- [4. Accessibility](#4-accessibility--inclusive-design-wcag-22--beyond)
- [5. Research and personas](#5-user-research--persona-depth)
- [6. Journeys](#6-user-journeys-task-flows--interaction-design)
- [7. Trust and ethics](#7-comfort-trust-emotion--ethics)
- [8. Completeness](#8-functionality-completeness-from-human-perspective)
- [9. Severity](#9-severity-calibration-specific-to-human-factors)
- [10. Validation methods](#10-recommended-validation-methods-to-list-in-residual-risks--next-actions)
- [Cross-milestone integration](#cross-milestone-evidence-integration)

Use this together with `../../shared/references/holistic-evaluation.md` at discovery, design, implementation, release, and post-release milestones. Keep human-outcome evidence distinct from technical E2E evidence and label untested claims as unknown.

## 1. Core Usability Goals (ISO 9241-11 / modern extensions)
Evaluate whether the artifact defines or supports:
- **Effectiveness** — Can users complete their goals accurately and completely?
- **Efficiency** — Can users complete goals with appropriate speed and effort once learned?
- **Satisfaction** — Is the experience free of discomfort and positively regarded?
- **Learnability** — How quickly can a new user become productive?
- **Memorability** — Can infrequent users return without re-learning everything?
- **Error rate & severity** — Frequency, recoverability and consequence of user errors.
- **Flexibility** — Support for different user strategies, expertise levels and contexts.

Target metrics (when measurable targets are expected in the artifact):
- Task success rate ≥ 90–95% for primary tasks (depending on criticality)
- Time-on-task and clicks/steps for frequent tasks explicitly optimized
- System Usability Scale (SUS) target or equivalent
- Customer Effort Score (CES) or Single Ease Question (SEQ) targets. For the usual 7-point SEQ scale, 1 = Very difficult and 7 = Very easy; higher scores indicate an easier task. Set the acceptance threshold for the specific task and study rather than treating an example threshold as universal.
- Error recovery success without external help

## 2. Cognitive Ergonomics & Human Information Processing
Check for explicit consideration of:
- Cognitive load (intrinsic, extraneous, germane) — is complexity managed?
- Working memory limits — are users required to remember too many items or steps?
- Mental model alignment — does the system match how target users already think about the domain?
- Information scent and wayfinding — can users predict where to go and what will happen?
- Progressive disclosure vs overwhelming initial complexity
- Attention management — visual hierarchy, distraction control, focus support
- Decision complexity — number of choices, clarity of consequences, support for comparison
- Fatigue and sustained attention factors (especially for long sessions or high-stakes tasks)
- Multi-tasking and interruption tolerance

## 3. Nielsen’s Heuristics + Modern Extensions (mandatory evaluation lens)
1. Visibility of system status
2. Match between system and real world (language, concepts, metaphors)
3. User control and freedom (undo, exit, cancel, escape hatches)
4. Consistency and standards (internal + platform)
5. Error prevention (better than good error messages)
6. Recognition rather than recall
7. Flexibility and efficiency of use (accelerators for experts, simplicity for novices)
8. Aesthetic and minimalist design (signal-to-noise)
9. Help users recognize, diagnose and recover from errors
10. Help and documentation (when needed, contextual and actionable)

Additional modern checks:
- Clear affordances and signifiers
- Immediate and informative feedback
- Forgiveness and graceful degradation
- Respect for user time and attention

## 4. Accessibility & Inclusive Design (WCAG 2.2 + beyond)
- Perceivable, Operable, Understandable, Robust (POUR)
- Target conformance level explicitly stated (A / AA / AAA) and justified
- Cognitive accessibility (clear language, consistent navigation, reduced complexity, memory aids)
- Motor accessibility (target sizes, timing, alternative inputs)
- Vision (contrast, text resizing, non-color cues, screen-reader structure)
- Hearing (captions, transcripts, visual alternatives)
- Literacy, language and cultural diversity
- Situational impairments (bright sunlight, noisy environments, one-handed use, low bandwidth)
- Equitable experience — no separate “accessible mode” that provides inferior functionality
- Testing plan with actual assistive technology and diverse users

## 5. User Research & Persona Depth
Artifacts should contain or reference:
- Primary, secondary and extreme / edge personas (not just “average” users)
- Jobs-to-be-done or goal hierarchies
- Context of use (environment, devices, interruptions, emotional state, time pressure)
- Current pain points and workarounds
- Success metrics from the user’s point of view (not only business metrics)
- Explicit exclusion statement — which users or contexts are intentionally out of scope

## 6. User Journeys, Task Flows & Interaction Design
- End-to-end primary journeys mapped with entry points, happy path, decision points, error paths and exit points
- Secondary and edge journeys considered
- Onboarding / first-time experience designed, not left as afterthought
- Empty states, loading states, partial states and error states designed with care
- Feedback quality (timing, clarity, tone, next-action guidance)
- Consistency of interaction patterns across the product
- Support for both novice and expert modes without forcing either

## 7. Comfort, Trust, Emotion & Ethics
- Identification of likely frustration, anxiety or confusion points
- Trust signals (transparency, predictability, competence, benevolence)
- Absence of dark patterns, manipulative defaults, forced actions or deceptive affordances
- Privacy respect visible in the interaction design (not only in the privacy policy)
- Emotional tone of microcopy, error messages and success states
- Delight and positive emotion opportunities (without sacrificing clarity)
- Support burden implications (will this design generate high support tickets?)

## 8. Functionality Completeness from Human Perspective
- Every primary user goal has a complete, coherent path
- Dead ends, circular flows and unsupported secondary goals are identified
- Power-user / frequent-task efficiency is explicitly addressed
- Novice safety nets exist without slowing experts
- System is operable under realistic conditions (stress, partial knowledge, interruptions)

## 9. Severity Calibration Specific to Human Factors
- **Critical (Human)**: Likely to cause significant user harm, exclusion of protected or core user groups, high abandonment of primary tasks, legal accessibility exposure, or irreversible errors.
- **Major (Human)**: High cognitive load or error rate on frequent tasks, substantial efficiency loss, noticeable exclusion, or persistent frustration that damages trust or satisfaction.
- **Minor (Human)**: Polish, consistency or learnability issues that accumulate into friction.
- **Suggestion**: Opportunities for delight, further reduction of effort, or excellence beyond baseline usability.

## 10. Recommended Validation Methods (to list in residual risks / next actions)
- Cognitive walkthrough
- Heuristic evaluation (multiple evaluators)
- Usability testing (moderated / unmoderated) with representative and extreme users
- Accessibility audit + assistive technology testing
- Inclusive design review
- Analytics instrumentation plan for key usability metrics
- SUS / SEQ / CES measurement plan


## Cross-Milestone Evidence Integration
For each critical task, record who performs it, task/context, expected outcome, task-success/error definition, method/sample, observed friction, accessibility conditions tested, and decision made. Pair these observations with latency/error/reliability traces for the same journey without conflating the signals. Usability scores are not universal product guarantees: justify targets for the use case and population. SEQ's conventional 1–7 scale runs from 1 = very difficult to 7 = very easy, so lower is worse; note any adapted wording/scale. Use both automated and manual accessibility evidence and document scope limitations.
