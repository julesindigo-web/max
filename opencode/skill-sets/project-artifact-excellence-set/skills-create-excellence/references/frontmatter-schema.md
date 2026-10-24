# Frontmatter and Metadata Schema

## Required Top-Level Keys
- name: string, kebab-case, 2-64 chars, matches directory name, ^[a-z0-9](?:[a-z0-9]|-(?!-))*[a-z0-9]$
- description: plain unquoted YAML scalar, single line, ≤1024 characters, no colon-space, no angle brackets, no TODO, contains what + when + triggers

## Optional Top-Level Keys
- license
- compatibility (≤500 chars, unquoted)
- metadata (map)
- allowed-tools
- user-invocable (boolean, default true)

## Recommended Metadata Fields for Excellence
```yaml
metadata:
  version: "1.0.0"
  type: skill | plugin | agent-spec | skill-set
  depends-on: []          # list of skill names or name@version
  provides: []            # capabilities or contracts offered
  quality-attributes: []  # list of attributes claimed at high level
  set-membership: ""      # name of parent set if any
  success-metrics: []     # short list of measurable criteria
  author: ""
  last-reviewed: "YYYY-MM-DD"
```

## Rules
- Custom fields must live under metadata.
- version follows semver.
- depends-on entries should be resolvable within the set or known registry.
- Never put trigger information only in the body; the description is the sole always-visible trigger.

## Validation Failures (must be rejected)
- Quoted name or description
- Colon-space inside description
- Angle brackets inside description
- Name mismatch with directory
- Consecutive hyphens or invalid characters in name
- Empty or TODO description
- Unknown top-level keys outside the allowed list
