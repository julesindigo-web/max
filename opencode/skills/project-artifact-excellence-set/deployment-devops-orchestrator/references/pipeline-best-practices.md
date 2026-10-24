# Pipeline Best Practices

## Purpose
Define reliable CI/CD stage design and gating modeled on deterministic validation.

## Stage Order
- Implement stages in this order: validate, test, scan, build, deploy.
- Block later stages on earlier failures. Never skip gates for speed.
- Publish artifacts and logs for each stage.

## Validate Stage
- Run lint, format checks, schema validation, and structural checks.
- Mirror .github/workflows/validate-skills.yml philosophy with deterministic exit codes.
- Fail fast with file and line references.

## Test Stage
- Run unit, integration, and contract tests.
- Publish pass rate, duration, and coverage.
- Quarantine flaky tests with owner and expiry date.

## Scan Stage
- Run dependency audit, image scan, secret scan, and IaC policy checks.
- Block High and Critical findings without approved exception.
- Retain reports with build identifier.

## Build Stage
- Produce immutable tags including commit digest and semantic version.
- Generate SBOM and provenance attestation.
- Enable registry cache and lockfile-based restores.

## Deploy Stage
- Promote only gated artifacts through development, staging, then production.
- Require health checks and automatic rollback triggers.
- Record approver, gate evidence, and release notes.

## Operability
- Measure stage duration, cache-hit rate, and failure rate weekly.
- Alert on 20 percent duration regression or repeated gate failures.
- Keep runbooks linked from pipeline failure messages.
