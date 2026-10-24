# Validation and Test Patterns

## Layers of Validation
1. Structural (frontmatter, name rules, description constraints, body non-empty, control tokens)
2. Semantic (no TODO, presence of success metrics, quality attributes, contracts)
3. Coverage (use-case → instruction → resource mapping)
4. Quality (human-factors checklist, trigger design tests, composability)
5. Runtime (scripts execute cleanly, produce expected side-effects within bounds)

## Structural Validation
Run the validator's built-in structural checks first. If a canonical external validator is configured or installed, run it too; absence of an external validator must never skip mandatory structural checks.

## Semantic and Excellence Checklist (run after structural)
- [ ] Description passes positive/negative trigger test set
- [ ] Exactly the five canonical metric dimensions are present; each has Definition, Unit/formula, Target, Rationale, Source, Sample, Segmentation, Method, Owner, and Window
- [ ] Dimension-specific targets pass semantic checks (not just generic numeric or presence checks)
- [ ] Quality attributes section or metadata present
- [ ] Human-factors considerations addressed
- [ ] Contracts and depends-on/provides declared if composable
- [ ] Version present for non-trivial skills
- [ ] Residual risks and next actions stated
- [ ] SKILL.md ≤500 lines or properly split
- [ ] References one level deep with TOC if >100 lines
- [ ] Scripts have usage comments and basic smoke test

## Set-Level Validation
- All members pass individual validation
- Dependency graph resolves without cycles
- Shared contracts are consistent
- Set success metrics are measurable
- Cross-skill terminology and process alignment checked

## Script Testing Pattern
Every validator and every script in scripts/ should:
- Contain a usage comment at the top
- Be executable
- Have automated tests for at least one valid fixture and one invalid fixture; valid fixtures must exit 0 and invalid fixtures must exit non-zero
- Declare side-effects and required permissions

## Continuous Improvement
After first real use, capture defects, update metrics, and raise the quality bar for the next iteration. Document changes in metadata last-reviewed and version.


## Set-Level CI Gate and Feedback Processor
Use `bash validation/validate-set.sh` from the set root. The gate validates the manifest and dependency DAG, all ten-field metric contracts and dimension-specific targets, each manifest member, the authoritative versioned trigger matrix, positive/negative validator fixtures, feedback-processor tests, release-package reproducibility, and release-integrity verification. GitHub Actions runs this gate on pushes and pull requests with read-only repository permissions. An optional local hook can be installed with `bash scripts/install-git-hook.sh`; CI remains the authoritative merge gate.

When a JSON event is added to `audit-feedback/inbox/`, the workflow runs `scripts/process-audit-feedback.py` and publishes generated evaluation requests as an artifact. Unknown categories/fields, duplicate IDs, malformed payloads, or unsupported values fail closed. Requests require human review and do not edit production skill files. The automated gate validates structure and contract behavior; representative runtime tasks, user testing, accessibility, and engineering judgment remain necessary for semantic quality.
