---
name: deployment-devops-orchestrator
description: Build secure and efficient container images and CI/CD pipelines with verified deployment gates. Use when containerizing services or designing release pipelines or optimizing build time or hardening deployment security. Triggers include deploy service or build pipeline or containerize app or configure CI/CD or optimize Docker image.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
    - security-vulnerability-auditor@>=1.0.0
    - test-automation-engineer@>=1.0.0
  provides: []
---
# Deployment DevOps Orchestrator

## Purpose
Build secure and efficient container images and CI/CD pipelines with verified deployment gates. Deliver reproducible IaC, minimized images, fast cached builds, and safe releases that pass security and test checks before promotion. Treat measurable quality attributes as release criteria and apply human factors discipline so pipelines stay readable, debuggable, and operable under pressure.
Execute from service modeling through image authoring, pipeline construction, caching, scanning, gated promotion, progressive delivery, and operability verification. Extend proven validation philosophy with deterministic evidence at every stage.

## Core Operating Principles
- Define every environment as code. Never allow manual console drift.
- Gate every promotion on evidence. Require passing validate, test, scan, build, and deploy stages.
- Minimize images and privileges by default. Ship only required runtime artifacts.
- Optimize build time through layering and cache reuse, not by skipping checks.
- Scan early and continuously. Block vulnerable artifacts before they reach clusters.
- Make pipeline failures diagnosable within minutes with structured logs and artifacts.
- Keep deployment operations reversible with versioned releases and tested rollback paths.
- Extend proven validation philosophy from .github/workflows/validate-skills.yml with deterministic gates.
- Measure pipeline quality attributes on every run and trend results weekly.
- Design for usability under incident pressure with clear signals and safe defaults.

## Process
1. Model the service boundary. Record runtime, ports, volumes, configuration, secrets, and dependencies.
2. Author Dockerfiles and IaC. Create minimized images plus Kubernetes manifests or equivalent IaC with pinned versions.
3. Design the pipeline. Implement validate, test, scan, build, and deploy stages with explicit inputs and outputs.
4. Wire build caching. Order layers for stability, enable registry caching, and isolate dependency installation.
5. Integrate security scanning. Add image, dependency, secret, and IaC scans as blocking gates.
6. Define deployment gates. Require security and test skill checks to pass before staging and production promotion.
7. Implement progressive delivery. Roll out with health checks, automatic rollback triggers, and traffic controls.
8. Verify operability. Confirm dashboards, alerts, runbooks, and restore procedures before declaring release complete.
9. Record release evidence. Attach SBOM, scan reports, gate decisions, and rollback test results to the release.

## Container and IaC Authoring
- Author multi-stage Dockerfiles separating build, test, and runtime layers.
- Pin base images by digest and rebuild on a defined cadence.
- Run containers as non-root with read-only filesystems where feasible.
- Declare resources, probes, security contexts, network policies, and autoscaling in Kubernetes manifests.
- Manage configuration through environment-specific values and secret references. Never commit secrets.
- Validate IaC with lint, policy, and dry-run checks before apply.
- Separate build arguments from runtime secrets with distinct handling paths.
- Document port, volume, and privilege requirements with justification notes.
- Consult references/container-optimization.md for minimization and caching patterns.

## Pipeline Stages and Gates
- Implement validate stage running lint, format, schema, and structural checks mirroring validate-skills philosophy.
- Implement test stage running unit, integration, and contract tests with published coverage and timing.
- Implement scan stage running dependency audit, image vulnerability scan, secret scan, and IaC policy scan.
- Implement build stage producing immutable tagged artifacts with SBOM and provenance attestation.
- Implement deploy stage promoting only gated artifacts through development, staging, and production.
- Require deployment gates confirming security checks and test checks pass with recorded evidence.
- Store gate decisions as machine-readable artifacts linked to commit and image digest.
- Enforce deterministic stage ordering with explicit dependencies and no implicit promotion.
- Publish stage timing, cache-hit rate, and gate outcomes on every run.
- Consult references/pipeline-best-practices.md for stage design, caching, and failure-handling rules.

## Security Gate Enforcement
- Require security-vulnerability-auditor checks to pass before staging promotion.
- Require test-automation-engineer checks to pass before production promotion.
- Block High and Critical vulnerabilities without a time-boxed approved exception.
- Block unreviewed IaC policy violations with owner assignment and remediation date.
- Record scanner name, version, database date, and finding counts with each gate.
- Audit gate bypasses weekly and expire exceptions after at most 30 days.
- Coordinate with project-artifact-auditor for release readiness scoring.

## Observability and Rollback Readiness
- Emit deployment events with service, version, image digest, actor, and gate evidence.
- Maintain dashboards for deployment frequency, lead time, failure rate, and recovery time.
- Configure alerts for failed gates, stalled pipelines, and rollback triggers.
- Implement one-command rollback restoring prior image, config, and migration state.
- Test rollback quarterly with measured recovery time under 15 minutes.
- Attach runbooks to alerts with diagnosis steps and escalation paths.

## Build-Time and Cache Efficiency
- Order Dockerfile instructions from least to most frequently changed.
- Cache dependency layers separately from source layers.
- Enable registry-backed layer caching and reproducible dependency lockfiles.
- Parallelize independent pipeline jobs and isolate flaky tests with quarantine and retry budgets.
- Measure build time per stage and cache-hit rate on every run.
- Set budgets for clean-build time and incremental-build time and alert on regression.
- Prune unused layers, artifacts, and old images on a retention schedule.
- Pin toolchain versions to keep cache keys stable across runner updates.
- Document cache scope, key strategy, and invalidation triggers for maintainers.

## Image Minimization and Vulnerability Management
- Select minimal base images such as distroless or slim variants compatible with the runtime.
- Remove build tools, docs, caches, and sample data from final images.
- Scan runtime images for operating-system and language-package vulnerabilities on every build.
- Define severity thresholds blocking promotion on High and Critical findings without approved exception.
- Rotate base images and dependencies promptly and record fix versions.
- Generate SBOM for every image and retain scan reports with the release.
- Verify no embedded secrets exist in layers, history, or default environment values.
- Measure final image size and cold-start latency against team budgets on every release.

## Release Verification Checklist
- Confirm validate, test, scan, build, and deploy stages all show passing status.
- Confirm SBOM, provenance, and scan reports attach to the immutable artifact.
- Confirm staging smoke tests pass with production-equivalent configuration.
- Confirm dashboards, alerts, and runbooks reference the new version.
- Confirm rollback was rehearsed within the last 90 days with recorded timing.
- Confirm audit log links commit, image digest, approver, and gate evidence.
- Block production promotion until every checklist item carries evidence.

## Quality Attributes
Address quality attributes explicitly for every pipeline and image. Cover security through least privilege and scanning, reliability through health checks and rollback, performance through build-time budgets and startup latency, efficiency through cache-hit rate and image size, observability through pipeline metrics and deployment events, maintainability through versioned IaC, testability through staged gates, portability across environments, and recoverability through backup and restore drills. Reject releases lacking evidence for claimed quality attributes.

## Human Factors and Usability
Apply human factors and usability discipline to pipeline experience and operations. Provide clear stage names, concise failure summaries, and direct links to logs and remediation guidance. Reduce cognitive load with consistent job layouts, standardized status signals, and actionable error messages. Support accessibility with readable dashboards, sufficient contrast, and text alternatives for status color. Design for on-call usability with runbooks, one-command rollback, and rehearsed recovery flows.

## Success Metrics
- Trigger performance: Definition: correct activation on image minimization, pipeline construction, and gated-deployment requests (member evaluates across at least 20 positive and 20 negative prompts); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 20 positive and 20 negative prompts; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: representative pipeline tasks accepted with security and test gates passing before orchestration per composition rule; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: pipeline runs with gate evidence; Sample: at least 10 representative pipeline tasks; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for pipeline delivery (member completes tasks loading at most 2 reference files); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: representative pipeline tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a new operator ships a gated pipeline and minimized image in a guided evaluation; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: guided pipeline sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: pipeline defects remaining after final validation (member baseline is zero Critical with at most 1 Major per 10 tasks tracked as an explicit exception when present); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: pipeline validation records and exception log; Sample: all pipeline tasks in the release candidate; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Cache poisoning produces inconsistent builds. Recover by invalidating caches, rebuilding from lockfiles, and pinning digests.
- Flaky tests block releases unpredictably. Recover by quarantining flaky cases, enforcing retry budgets, and fixing root causes within 7 days.
- Oversized images slow deployment and widen attack surface. Recover by re-applying multi-stage minimization and removing unneeded layers.
- Skipped scans allow vulnerable images to promote. Recover by making scans blocking, auditing bypasses, and redeploying patched images.
- Failed deployment without rollback plan extends outage. Recover by triggering automatic rollback, restoring prior revision, and completing a post-incident review.
- Secret leakage in images or logs creates exposure. Recover by revoking affected credentials, purging artifacts, and adding secret-scan gates.
- Configuration drift between environments causes staging-only passes. Recover by diffing rendered manifests and enforcing environment parity checks.
- Missing health probes delay failure detection. Recover by adding readiness and liveness probes with verified failure thresholds.
- Expired base images accumulate vulnerabilities. Recover by enforcing rebuild cadence and automated patch pull requests.

## References
- references/pipeline-best-practices.md defines stage order, gating evidence, caching, and operability rules.
- references/container-optimization.md defines Dockerfile minimization, layer ordering, and vulnerability controls.
- Submit pipeline designs to project-artifact-auditor for reliability and operability scoring.
- Retain gate evidence and release records for at least 5 releases.
