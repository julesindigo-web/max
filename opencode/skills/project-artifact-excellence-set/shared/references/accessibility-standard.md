# Accessibility Standard (Shared)

Canonical cross-skill accessibility baseline for the set. Member skills
(`accessibility-inclusive-design`, `frontend-engineering-excellence`,
`human-centric-visual-excellence`) implement this standard; auditors verify
against it.

## Target Level
- Meet WCAG 2.1 Level AA on every shipped interface. Level AAA where the
  member skill explicitly claims it. Never claim AAA from a checklist alone;
  record test evidence or mark the criterion unknown with rationale.

## Non-Negotiable Checks
1. Correct ARIA roles, states, and properties on custom controls. Native
   elements are preferred over ARIA workarounds.
2. Full keyboard operation with a visible focus indicator and a logical focus
   order. No keyboard traps. Skip links on content-heavy pages.
3. Text contrast at least 4.5 to 1 (3 to 1 for large text). Non-text UI
   indicators at least 3 to 1 against adjacent colors.
4. Visible labels for form fields, error identification in text, and
   status messages exposed to assistive technology.
5. Motion safety: honor reduced-motion preferences for decorative animation
   and vestibular-risky effects.

## Verification Method
- Automated scan plus manual keyboard walkthrough plus assistive-technology
  spot check on critical journeys. Record tool, version, date, and scope.
- Silence on any check above is a Major gap. A decorative-only claim must
  still verify contrast and focus visibility.

## Traceability
- Findings use `../contracts/audit-findings.schema.json`. Remediation follows
  `unified-remediation-playbook.md`. Member detail lives in
  `accessibility-inclusive-design/references/wcag-checklist.md`.
