# API Documentation Standards

## Purpose
Define consistent rules for generated OpenAPI contracts and endpoint references.

## Naming Rules
- Use kebab-case for path segments and snake_case or camelCase consistently for fields per codebase convention.
- Name operations with verb plus resource, for example listOrders or createUser.
- Keep schema names singular and domain-aligned.

## Contract Structure
- Define info title, version, and contact for every document.
- Group paths by resource tag.
- Define reusable schemas under components/schemas.
- Define shared errors under components/responses.
- Document authentication under components/securitySchemes.

## Operations
- Specify operationId, summary, parameters, requestBody, responses, and security for each operation.
- List success codes plus 400, 401, 403, 404, 409, 422, 429, and 500 where applicable.
- Provide one request example and one response example per operation.

## Versioning
- Apply semantic versioning to contracts.
- Mark breaking changes explicitly with migration notes.
- Retain prior major version notes for at least 2 releases.

## Validation
- Parse every contract with an OpenAPI parser before publishing.
- Reject missing types, dangling references, and duplicate operationIds.
- Confirm examples validate against declared schemas.

## Review Checklist
- Confirm every route in inventory appears in the contract.
- Confirm auth, pagination, idempotency, and rate-limit fields are complete.
- Confirm error catalog matches implementation.
