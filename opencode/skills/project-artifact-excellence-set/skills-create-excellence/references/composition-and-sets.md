# Skill-Set and Plugin Composition Patterns

## Definitions
- Skill: single capability package.
- Plugin: skill that declares extension points or integration contracts.
- Skill Set / Plugins Set: coherent collection delivering a higher-order capability.

## Set Manifest Requirements
Every set must contain a SET.md or manifest.yaml with:
- name and version (semver)
- purpose and success metrics for the set as a whole
- list of member skills with their versions
- dependency graph (directed acyclic)
- composition rules and conflict resolution policy
- shared contracts and schemas
- validation entry point
- deprecation and migration policy

## Recommended Directory Layout
```
set-name/
├── SET.md
├── manifest.yaml
├── skills/
│   ├── member-a/
│   └── member-b/
├── shared/
│   ├── contracts/
│   ├── schemas/
│   └── references/
└── validation/
    └── validate-set.sh
```

## Composition Rules
1. Explicit depends-on and provides in each skill’s metadata.
2. No circular dependencies.
3. Shared contracts live in shared/ and are referenced, never duplicated.
4. Version conflicts resolved by explicit policy (highest compatible, pin, fail).
5. Loading order determined by topological sort of the dependency graph.
6. Set-level validation must pass before any member is considered production-ready.

## Contract Patterns
- Input/output schemas for scripts
- Event or message shapes if skills communicate
- Quality-attribute guarantees each skill provides
- Failure mode contracts (what errors are returned and how)

## Migration and Versioning
- Breaking changes require major version bump and migration notes.
- Deprecated skills remain loadable for one major cycle with warnings.
- Set version advances when any member has a breaking change or when composition rules change.

## Validation for Sets
- Structural validity of every member
- Dependency resolution success
- Contract compatibility
- Cross-skill consistency of terminology and metrics
- End-to-end traceability from set goals to member instructions


## Operational Integration Contract
The composed `project-artifact-excellence-set` uses a root `manifest.yaml`, `SET.md`, and `shared/contracts/`. Member skill directories may be listed at set root or under `skills/`, provided each manifest `path` is relative, safe, unique, and contains a matching `SKILL.md`. Dependencies must name declared members and form a DAG. The standard entry point is `validation/validate-set.sh`, which validates the manifest, members, dependency graph, and regression tests.

For cross-member feedback, `project-artifact-auditor` emits an event conforming to `shared/contracts/audit-findings.schema.json`; `skills-create-excellence` evaluates any generated request conforming to `shared/contracts/skill-improvement-requests.schema.json`. These are explicit versioned contracts. Feedback generates a reviewable proposal, not an autonomous production edit or merge. See `shared/references/feedback-loop.md` and `shared/references/unified-remediation-playbook.md`.
