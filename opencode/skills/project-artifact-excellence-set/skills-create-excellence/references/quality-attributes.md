# Quality Attributes for Exceptional Skills and Plugin Sets

## 1. Functional Completeness
- Every declared use case has corresponding imperative instructions.
- Edge cases and failure modes are explicitly handled.
- Acceptance criteria are binary or measurable.

## 2. Trigger Precision & Recall
- Description yields high true-positive rate on intended utterances.
- Low false-positive rate on unrelated tasks.
- Contains concrete trigger phrases and scenarios.
- Tested with at least 5 positive and 5 negative examples.

## 3. Cognitive Ergonomics
- Author cognitive load is minimized by clear process and checklists.
- End-user (agent) load is minimized by progressive disclosure and concise imperative language.
- Error messages and recovery paths are explicit.
- Inclusive of varying expertise levels.

## 4. Architectural Clarity
- Clear separation of concerns (instructions vs scripts vs references vs assets).
- Explicit interfaces and contracts for composition.
- Dependency graph is acyclic and declared.
- No hidden coupling.

## 5. Measurable Success Metrics
Minimum set required for every skill or skill set: **five measurable success metrics**, one for each dimension below. Targets may be adapted to the skill's purpose, but a dimension may not be omitted:
- **Trigger performance** — trigger hit rate / precision / recall proxy, using positive and negative examples.
- **Task completion** — completion rate against explicit acceptance criteria.
- **Context-token efficiency** — `SKILL.md` size plus the reference material loaded for representative tasks.
- **Time-to-working-skill** — time for a new author or operator to produce the first valid, usable result.
- **Residual defect density** — defects remaining after the first and final validation passes, with Critical/Major defects reported separately.

Every canonical metric must declare all ten fields using the validator-recognized labels: `Definition`, `Unit/formula`, `Target`, `Rationale`, `Source`, `Sample`, `Segmentation`, `Method`, `Owner`, and `Window`. The validator checks semantic fit of dimension-specific targets as well as field presence. A generic number (for example, `123`) or a label without a reproducible scoring rule is not measurable.

## 6. Observability & Diagnostics
- Clear statements of what success and failure look like.
- Guidance for diagnosing why a skill did not trigger or produced suboptimal output.
- Logging or status reporting patterns for scripts.

## 7. Security & Least Privilege
- Scripts declare required permissions and side-effects.
- No unconstrained code execution without bounds.
- Secrets and sensitive data handling rules if applicable.
- Supply-chain considerations for external resources.

## 8. Maintainability & Evolvability
- Version field in metadata.
- Deprecation and migration notes.
- Clear ownership of each resource.
- Technical debt explicitly flagged if present.

## 9. Composability
- Provides and requires declarations.
- Conflict resolution rules.
- Shared contract schemas when part of a set.
- No breaking changes without version bump.

## 10. Testability
- Structural validation always passes.
- Semantic and coverage checks defined.
- Scripts have at least smoke tests or usage examples.
- Critical paths have acceptance tests.

## 11. Production Readiness
- Correct location (/home/workdir/.grok/skills/)
- Persistence and discovery rules followed.
- Validation harness present for sets.
- Residual risks documented.

## 12. Human Factors Excellence
- Trust, predictability and low frustration for both author and runtime agent.
- Accessibility of language (clear, unambiguous, inclusive).
- Emotional experience of using the skill is positive (confidence, control).

## Scoring Guidance
Rate each attribute 1-5. Exceptional requires ≥4.5 average with no attribute below 3. Residual risks must be listed for any attribute <5.
