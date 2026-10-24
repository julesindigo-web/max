# Risk Register — accepted residuals (PA-GOV-11)

Signed register of open Critical/Major findings carrying explicit authorized
risk acceptance, as required by the SET.md release gate ("no open
Critical/Major skill-quality finding lacks an explicit decision").

## Entries

| Finding | Disposition | Owner | Date | Authorizer |
|---|---|---|---|---|
| (none open — template row) | accept / mitigate / transfer | named owner | YYYY-MM-DD | named authorizer |
| PA-OBS-02 telemetry verbose log (2026-10-15) | mitigate — log quarantined, shape gate added to validate-plugins.sh; writer identification pending | release approver | 2026-10-15 | release-approver (role acceptance 2026-10-15; named human countersign required at release gate) |
| Mirror gate 4/6 + 2 release tests fail by-design | accept — provenance runtime exclusions (anti-phantom-skill) | set maintainer | 2026-10-15 | release-approver (role acceptance 2026-10-15; named human countersign required at release gate) |
| Live-runtime TPR/FPR + task completion UNVERIFIED | accept — tracked; closes only via runtime-protocol.md run | evaluation lead | 2026-10-15 | release-approver (role acceptance 2026-10-15; named human countersign required at release gate) |
| JS line/branch <100% (plugin 93.23%/85.16%, 2026-10-15) | accept — validator-exec lines (199-207, 242-246) + never-throw catches tracked as integration-track residual; closing via unit theater rejected | test-runner (measure) / set maintainer | 2026-10-15 | release-approver (role acceptance 2026-10-15; named human countersign required at release gate) |

## Rule

No release candidate ships with an open Critical/Major finding missing a row
here. Rows stay until verified closed against evidence and acceptance
criteria, then move to REMEDIATION-CHANGELOG.md with the closure date.
