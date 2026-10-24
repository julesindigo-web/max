---
name: architecture-documentation-generator
description: Parse source and data flows to generate synchronized architecture docs and OpenAPI contracts. Use when documenting systems or syncing docs after code changes or publishing API references or visualizing data flow. Triggers include generate docs or sync documentation or create OpenAPI spec or diagram architecture or document API.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
  provides: []
---
# Architecture Documentation Generator

## Purpose
Parse implementation source and data flows to generate synchronized architecture documentation and OpenAPI contracts. Deliver accurate system overviews, interface references, and data-flow diagrams that remain aligned with code after every change. Treat measurable quality attributes as first-class outputs and apply human factors discipline so docs stay scannable, trustworthy, and actionable for engineers and operators.
Execute layer by layer from inventory through extraction, contract generation, diagram rendering, consistency checks, and publication. Use deterministic tooling and review gates to prevent drift and to preserve traceability from every doc claim back to source evidence.

## Core Operating Principles
- Derive every claim from source evidence. Never invent components, endpoints, or flows.
- Generate docs deterministically. Identical source produces identical output.
- Keep contracts and diagrams synchronized with code on every change.
- Prefer explicit interface definitions over prose descriptions.
- Optimize for reader task completion. Structure docs for lookup, onboarding, and incident response.
- Enforce consistent terminology across code, docs, diagrams, and contracts.
- Record provenance for each generated artifact including source revision and generator version.
- Fail visibly on drift. Report stale docs as defects, not warnings.
- Version every artifact. Retain prior outputs for at least 5 releases to support forensics.
- Design for maintainability. Keep generation logic simple, reviewable, and dependency-free.

## Process
1. Inventory the target codebase. Run scripts/ast-doc-sync.py inventory against the target directory to list files and symbols.
2. Extract component relations. Parse imports, calls, routes, schemas, and queue topics to build a dependency graph.
3. Classify data flows. Label synchronous requests, asynchronous events, batch jobs, and storage access with direction and payload shape.
4. Generate OpenAPI contracts. Emit paths, operations, schemas, errors, and authentication requirements from route and handler evidence.
5. Render system diagrams. Produce Mermaid.js graphs for context, container, component, and data-flow views.
6. Cross-check consistency. Compare generated contracts against implementation and flag missing, stale, or contradictory entries.
7. Publish synchronized outputs. Write docs, contracts, and diagrams with revision stamps and update the baseline inventory.
8. Verify on every code change. Run scripts/ast-doc-sync.py check in CI and block merge on drift until docs are regenerated.
9. Record audit evidence. Attach inventory diffs, parser results, and review approvals to the release record.

## Source Parsing and Component Extraction
- Walk the target tree and parse Python files with abstract syntax tree analysis. Record qualified function names, arguments, and line numbers.
- Scan JavaScript and TypeScript files with deterministic export patterns. Record exported functions, classes, and route registrations.
- Map module dependencies from import statements and cross-file references.
- Identify entry points including HTTP handlers, CLI commands, workers, schedulers, and event subscribers.
- Capture persistence access including queries, migrations, and cache keys with owning component attribution.
- Emit a JSON inventory shaped as files count plus symbols list for downstream diffing.
- Normalize file paths to repository-relative form for stable cross-machine comparison.
- Sort inventory symbols by file, name, and line number to guarantee deterministic output.
- Exclude generated artifacts, vendored code, and build outputs from parsing scope.
- Consult references/api-documentation-standards.md for field naming, versioning, and error-model conventions.

## OpenAPI Contract Generation
- Generate one OpenAPI document per service boundary from verified route evidence.
- Define each path with operation identifier, parameters, request schema, response schemas, and error codes.
- Reuse shared schema components for domain models and envelope types.
- Document authentication, rate limits, pagination, idempotency keys, and retry semantics explicitly.
- Validate generated contracts with a parser before publishing. Reject unresolvable references and ambiguous types.
- Version contracts with semantic versioning and record breaking changes in release notes.
- Keep examples minimal, realistic, and synchronized with schemas.
- Enforce consistent error shape with code, message, details, and correlation identifier fields.
- Document webhook and event payloads alongside synchronous paths where applicable.

## System Diagrams with Mermaid.js
- Render a context diagram showing external actors, this system, and external dependencies.
- Render a container diagram showing services, datastores, queues, and edge gateways.
- Render component diagrams per service showing handlers, domain modules, and adapters.
- Render data-flow diagrams tracing request paths and event chains end to end.
- Use consistent node naming matching the source inventory. Avoid aliases that diverge from code.
- Keep each diagram focused on one level. Link levels with explicit navigation notes.
- Annotate edges with protocol, payload type, and sync versus async behavior.
- Mark trust boundaries, validation points, and persistence touchpoints on flows.
- Consult references/system-diagram-templates.md for starter templates and layout rules.

## Doc-Sync Workflow
- Store the baseline inventory JSON alongside generated docs in version control.
- Execute inventory on every pull request and compare against the baseline.
- Treat added symbols as required doc additions and removed symbols as required doc removals.
- Treat changed signatures as contract review triggers requiring human confirmation.
- Regenerate affected docs and contracts before merging the code change.
- Log sync decisions with file, symbol, and rationale for audit traceability.
- Fail the build on drift with a readable added, removed, and changed summary.
- Update the baseline in the same commit as the code change to keep history atomic.

## Contract Review Checklist
- Confirm every route in the inventory appears exactly once in the generated contract.
- Confirm request schemas match handler validation models field by field.
- Confirm response schemas cover success plus documented error cases.
- Confirm authentication requirements state scheme, scope, and failure codes.
- Confirm pagination, filtering, sorting, and idempotency semantics where applicable.
- Confirm examples validate against schemas without manual patching.
- Confirm version bump and changelog entry reflect breaking versus additive changes.
- Request project-artifact-auditor review for contract completeness before publication.

## Diagram Review and Publishing
- Validate node names against the inventory before rendering diagrams.
- Limit each diagram to a single abstraction level with explicit scope label.
- Add numbered flow steps on data-flow edges for traceable walkthroughs.
- Provide a text table equivalent for every diagram to support accessibility.
- Export diagrams in versioned artifacts with source revision stamps.
- Publish context, container, component, and data-flow views as a linked set.
- Archive prior versions for at least 5 releases to support incident forensics.

## Integration with Audit and Operations
- Submit generated docs, contracts, and diagrams for audit scoring on accuracy and traceability.
- Link each doc section to owning code paths with file and line references.
- Surface drift reports in pull-request summaries with added, removed, and changed lists.
- Track doc freshness as an operational metric with target 100 percent in-sync merges.
- Schedule quarterly doc usability reviews with onboarding, integration, and on-call participants.
- Record follow-up actions with owners and due dates until closure.

## Quality Attributes
Address quality attributes explicitly in every generated artifact. Cover accuracy against source, completeness of endpoints and flows, consistency of naming, traceability from doc to line number, maintainability through deterministic generation, evolvability through versioned contracts, observability through provenance stamps, security through auth and data-classification notes, performance through latency annotations where known, and testability through verifiable examples. Reject any doc set that claims coverage without evidence.

## Human Factors and Usability
Apply human factors and usability discipline to doc structure and presentation. Organize for progressive disclosure with summary first and detail on demand. Use descriptive headings, searchable operation identifiers, and stable anchors. Reduce cognitive load with one concept per section, consistent tables, and scannable error catalogs. Support accessibility with high-contrast diagram themes, text equivalents for every diagram, and keyboard-navigable output. Validate with task-based checks covering onboarding, integration, and incident lookup.

## Success Metrics
- Trigger performance: Definition: correct activation on doc generation, doc-sync, OpenAPI publishing, and data-flow visualization requests (member evaluates across at least 20 positive and 20 negative prompts); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 20 positive and 20 negative prompts; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: representative documentation tasks accepted with docs and contracts synchronized to source including deterministic AST doc-sync output; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: documentation tasks with source-to-doc diff evidence; Sample: at least 10 representative documentation tasks; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for doc generation (member completes tasks loading at most 2 reference files); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: representative documentation tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a new operator produces verified docs and contracts in a guided evaluation; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: guided documentation sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: documentation defects remaining after final validation (member baseline is zero Critical with at most 1 Major per 10 tasks tracked as an explicit exception when present); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: documentation review records and exception log; Sample: all documentation tasks in the release candidate; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Stale baseline inventory causes false in-sync reports. Recover by regenerating inventory from the current tree and recommitting the baseline.
- Dynamic route registration escapes static parsing. Recover by adding explicit route manifests and annotating dynamic loaders for manual review.
- Ambiguous handler signatures produce incomplete schemas. Recover by requiring typed models or validation schemas before contract generation.
- Oversized diagrams obscure system structure. Recover by splitting by bounded context and linking levels with navigation indexes.
- Contract drift merged without doc updates breaks consumers. Recover by enforcing check-gate failures in CI and reverting undocumented interface changes.
- Missing auth metadata weakens security posture. Recover by blocking publication until authentication and data-classification fields are complete.
- Unparsable files silently reduce coverage. Recover by surfacing parse warnings as CI annotations and fixing encoding or syntax issues.
- Alias drift between code and diagrams confuses readers. Recover by enforcing inventory-based naming checks before publishing diagrams.

## References
- references/api-documentation-standards.md describes OpenAPI structure, naming, versioning, and error-model rules.
- references/system-diagram-templates.md provides Mermaid.js templates for context, container, component, and data-flow views.
- scripts/ast-doc-sync.py implements deterministic inventory and drift detection for continuous doc synchronization.
- Submit outputs to project-artifact-auditor for completeness, traceability, and usability scoring.
- Retain generated artifacts with revision stamps for at least 5 releases.
- Record generation command, source revision, and reviewer approval with each publish.
