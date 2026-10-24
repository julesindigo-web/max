---
name: sensitive-change-safety
description: Harden a sensitive product change. Use when work affects auth, access control, sensitive data, payments, uploads, or third-party trust boundaries.
---

# Sensitive Change Safety

Use this skill only when the requested change touches an elevated trust boundary: authentication, authorization, tenancy, secrets, personal data, money, files, webhooks, outbound requests, or a third-party integration.

1. State the assets, actors, trust boundaries, abuse cases, and change-specific mitigations in a short threat assessment. Distinguish observed facts from assumptions.
2. Use least privilege and deny-by-default authorization. Check object-level and tenant-level access server-side; never rely on client role, price, identifier, MIME type, redirect target, or model output without validation.
3. Avoid secret and sensitive-data exposure in code, browser bundles, logs, errors, fixtures, or telemetry. Do not open or reproduce credential values.
4. Apply the relevant boundary controls: parameterized data access; output encoding; CSRF defenses for cookie authentication; upload size/type/content checks; webhook signature and replay checks; outbound allowlists and private-address blocking; idempotency for retried side effects.
5. Add or run focused negative tests for the abuse cases the change can introduce. Review the diff for new auth bypasses, sensitive logs, unsafe parsing, unbounded work, or loosened headers and permissions.

Ask before credential rotation, production/shared-system actions, retention changes, destructive data operations, external communication, or a compliance conclusion. This skill provides engineering safeguards, not legal advice.
