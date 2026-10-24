# Remediation and Iteration — Skill & Set Focused Patterns

Canonical shared protocol lives in `../../shared/references/unified-remediation-playbook.md`.  
This file provides skill/set-specific ready-to-paste patterns, acceptance evidence, and residual-risk statements.

## Required Five Metric Dimensions (always present)

Every SKILL.md and SET.md must contain measurable targets for:

1. Trigger performance  
2. Task completion  
3. Context-token efficiency  
4. Time-to-working-skill  
5. Residual defect density  

### Ready-to-paste metric block (copy into Success Metrics section)

```markdown
## Success Metrics
- Trigger performance: Definition: correct activation on labeled prompts; Unit/formula: TPR = TP/(TP+FN) and FPR = FP/(FP+TN); Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: balance coverage and precision; Source: authoritative trigger matrix plus target-runtime logs; Sample: at least 5 positive and 5 negative prompts; Segmentation: skill and prompt class; Method: run frozen prompts and log activations; Owner: evaluator; Window: each release candidate
- Task completion: Definition: acceptance-check pass rate; Unit/formula: passed applicable checks / applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: verify task utility; Source: task rubric and logs; Sample: at least 5 representative tasks; Segmentation: by task type; Method: score binary criteria with evidence; Owner: evaluator; Window: each release candidate
- Context-token efficiency: Definition: instruction footprint and reference relevance; Unit/formula: lines per SKILL.md plus references loaded; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: constrain baseline overhead; Source: repository and task traces; Sample: all members plus representative traces; Segmentation: member/task; Method: count lines and inspect traces; Owner: maintainer; Window: each release candidate
- Time-to-working-skill: Definition: elapsed time to first valid tested skill; Unit/formula: minutes from starter brief to acceptance; Target: ≤60 minutes; Rationale: authoring usability; Source: timed guided evaluation; Sample: at least 5 first-time authors or labeled pilot; Segmentation: experience and task complexity; Method: use fixed brief and record time/assistance; Owner: human-factors evaluator; Window: each major release
- Residual defect density: Definition: unresolved Critical/Major defects after final validation; Unit/formula: open Critical and Major finding count; Target: zero open Critical and Major defects unless explicitly authorized risk acceptance is recorded; Rationale: prevent material defects being averaged away; Source: findings register, CI, and risk record; Sample: all release-candidate Critical/Major findings; Segmentation: severity and impact; Method: reproduce and verify fixes or approved risk acceptance; Owner: release approver; Window: final release gate and post-release review
```

## Pattern Catalog (skill-level)

### P-S1 Missing or unmeasurable metrics
- **Signal:** Success Metrics section lacks one of the five dimensions or uses qualitative language only.
- **Remediation:** Insert the ready-to-paste block above; replace placeholders with actual measured values when available.
- **Acceptance:** `validate-excellence.sh` and `validate_set_manifest.py` pass; evaluation results file exists.
- **Residual risk:** Author-side measurement only until live runtime data is collected.

### P-S2 Weak trigger precision/recall
- **Signal:** Description does not contain concrete trigger phrases or negative-case discrimination is weak.
- **Remediation:**  
  1. Add 3–5 concrete positive phrases into the frontmatter description.  
  2. Expand `evaluation/trigger-evaluation-matrix.json`.  
  3. Re-measure and update results file.
- **Acceptance:** TP ≥90%, FP ≤10% on ≥12+12 authored cases (minimum 5+5).
- **Residual risk:** Semantic matching ≠ live agent routing; schedule runtime A/B after description change.

### P-S3 Bloated SKILL.md (>500 lines)
- **Signal:** Line count exceeds limit.
- **Remediation:** Move stable domain depth, long checklists, and examples into `references/`. Keep process + decision rules in SKILL.md. Update relative links.
- **Acceptance:** `wc -l SKILL.md` ≤500 and validator still passes.
- **Residual risk:** Over-fragmentation can raise cognitive load; keep TOC in long reference files.

### P-S4 Missing contracts / dependency ambiguity
- **Signal:** `depends-on` or `provides` missing or inconsistent with manifest.
- **Remediation:** Align frontmatter metadata, `manifest.yaml`, and shared/contracts schemas in one atomic change. Add regression fixture.
- **Acceptance:** `validate_set_manifest.py` and full `validate-set.sh` pass; dependency graph remains acyclic.
- **Residual risk:** Schema version bump may require migration note.

### P-S5 Untested script or validator bypass
- **Signal:** Script lacks positive + negative fixtures or fails open.
- **Remediation:** Add fixtures under `scripts/tests/fixtures/`, ensure mandatory failures exit non-zero, cover in `test-validate-excellence.sh` or Python unittest.
- **Acceptance:** Regression suite green; new fixture fails closed when broken.
- **Residual risk:** Environment-specific failures (e.g. missing /dev/fd) — prefer portable constructs.

### P-S6 Human-factors or recovery guidance missing
- **Signal:** No explicit failure modes, recovery steps, or cognitive-load considerations.
- **Remediation:** Add subsection “Failure Modes & Recovery” and reference `human-factors.md`. Document untested contexts.
- **Acceptance:** Human-factors checklist items addressed or marked N/A with rationale.
- **Residual risk:** Accessibility for agent authors with disabilities still needs external review.

### P-S7 Recurrent audit finding suggests skill gap
- **Signal:** Same pattern appears in ≥2 distinct audits or `skill_gap_suspected: true`.
- **Remediation:** Emit structured audit-findings event → process-audit-feedback.py → evaluation request. Do **not** auto-edit production skill.
- **Acceptance:** Request contains proposed diff, regression test, metric impact, human-factors impact, residual-risk statement.
- **Residual risk:** Feedback volume; keep eligibility rules strict (open + explicit or recurrence with observation IDs).

## After Any Change
1. Run `bash validation/validate-set.sh`.  
2. Update evaluation results if triggers or metrics changed.  
3. Record residual risk and reviewer.  
4. Bump version + migration note when contracts or required structure change.
