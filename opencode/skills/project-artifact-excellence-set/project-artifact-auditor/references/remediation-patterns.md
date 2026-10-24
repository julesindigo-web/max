# Remediation Patterns — Project Artifact Focus

Canonical shared protocol and matrix live in `../../shared/references/unified-remediation-playbook.md`.  
This file supplies project-audit-specific ready-to-paste patterns and acceptance evidence.

## Project-Audit Pattern Map (quick index)

| Signal | Playbook row(s) to apply |
|--------|---------------------------|
| Ambiguous requirement / weak user story | Ambiguous requirement or user story |
| Missing acceptance criteria | Missing acceptance criteria |
| Missing / vague NFR | Missing or vague non-functional requirement |
| Traceability gap / orphan artifact | Broken traceability or orphan artifact |
| Contradictory documents / API contracts | Contradictory documents or interface contracts |
| Weak architecture / reliability / security | Weak architecture / reliability / security coverage |
| E2E performance or delivery regression | E2E performance or delivery regression |
| Cognitive overload / poor recovery / accessibility | Poor usability, cognitive overload, or inaccessible journey + Weak personas or human-factors assumptions |
| Residual defect / no ownership / reopens | Residual defect, no ownership, or issue repeatedly reopens |

## Ready-to-paste Finding Template

```markdown
### [ID] Title
- **Evidence:** <exact location + observed text/state>
- **Root cause:** <why it escaped + failed assumption/control>
- **Impact (Human / Tech / Ops):** <concrete consequence>
- **Recommended remediation:** <ready-to-paste text or structural change>
- **Effort / Priority:** L|M|H / P0|P1|P2
- **Suggested metric or AC:** <observable pass/fail>
- **Residual risk:** <what remains uncertain>
```

## Concrete Remediation Snippets

### Ambiguous requirement
**Before:** “The system should be fast and easy to use.”  
**After:** “Given a 95th-percentile authenticated user on a mid-range mobile device over 4G, the primary dashboard must reach LCP ≤ 2.5 s and the user must complete the ‘view account balance’ task in ≤ 3 taps with SEQ ≥ 5 (1–7) on a sample of 8 representative users.”

### Missing acceptance criteria
Add under each major requirement:
- Success: observable outcome + measurement method
- Error: expected error state + recovery path
- Boundary: empty, max, concurrent, offline
- Accessibility: keyboard + screen-reader path must succeed
- Security: least-privilege and data classification constraints

### Broken bidirectional traceability
Create a one-page matrix:
`User Outcome ID → Requirement ID → Design/Contract ID → Test ID → Runtime Signal / Telemetry`

Any critical-path cell that is empty is a Major finding until filled or explicitly scoped out with rationale.

### Weak human-factors coverage
For every critical journey record:
1. Persona / context (including extreme / situational users)
2. Task success definition
3. Cognitive load notes (steps, memory, decision points)
4. Error prevention & recovery
5. Accessibility checks performed (or N/A + reason)

## Skill-Gap Escalation Rule
When the same pattern appears in ≥2 distinct audits **or** a finding carries `skill_gap_suspected: true`, emit a schema-1.1 normalized event conforming to `../../shared/contracts/audit-findings.schema.json`, including evidence state, confidence, verification method, as-of context, impact rationale, and severity basis and route via `../../shared/references/feedback-loop.md`. Never auto-edit a live skill.

## Verification Checklist (after remediation)
- [ ] Old failure is reproducible
- [ ] Change applied and reviewed
- [ ] Regression + cross-artifact checks pass
- [ ] Human impact inspected
- [ ] Evidence retained
- [ ] Residual risk recorded
- [ ] If skill gap suspected → feedback event created
