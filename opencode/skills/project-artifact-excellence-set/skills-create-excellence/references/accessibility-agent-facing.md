# Accessibility & Inclusive Design — Agent-Facing Checklist

Apply when authoring or reviewing skills, agent specs, or the interaction surface that skill authors and operators use.

## Scope
- Skill authors / editors
- Agent runtime operators
- Downstream end users of agent outputs (where the skill influences language, structure, or recovery)

## Minimum Checklist (pass / N/A + rationale)

### Cognitive load & predictability
- [ ] Trigger phrases and description are concrete; no hidden “magic” activation conditions.
- [ ] Process steps are numbered and sequential; branching is explicit.
- [ ] Failure modes and recovery steps are stated near the point of failure, not only at the end.
- [ ] Long reference files have a table of contents when >100 lines.

### Language & terminology
- [ ] Inclusive, plain language; avoid jargon without definition.
- [ ] No idioms that rely on cultural knowledge unless domain-specific and defined.
- [ ] Error messages describe the problem and the next safe action.

### Structure & navigation
- [ ] Progressive disclosure: SKILL.md ≤500 lines; depth in references/.
- [ ] Relative links to references are correct and one level deep.
- [ ] Consistent heading hierarchy (H1 → H2 → H3).

### Error prevention & recovery
- [ ] Risky or irreversible actions are called out with confirmation guidance.
- [ ] Validator and scripts fail closed with actionable error text.
- [ ] Recovery path does not require re-entering large amounts of lost context.

### Inclusive contexts
- [ ] Consider authors using screen readers, keyboard-only, or reduced-motion preferences when the skill produces interactive or UI-related output.
- [ ] Color is never the sole carrier of meaning in any generated diagram or status.
- [ ] Time estimates and cognitive-effort notes are provided for complex authoring tasks.

### Residual accessibility risk
- [ ] Untested contexts are listed (e.g. “screen-reader verification of generated Markdown tables not yet performed”).
- [ ] External accessibility review is recommended before major public release when the skill produces user-facing UI guidance.

## Residual Risk Statement Template

```markdown
## Residual Risk (Accessibility / Human Factors)
- Measured / reviewed: <what was checked and on which date>
- Untested contexts: <list>
- Known limitations: <list>
- Recommended next validation: <user research, AT testing, etc.>
- Risk acceptance (if any): <owner + date + rationale>
```
