# Release Artifact Hardening and Reproducibility

## Purpose and trust boundary

A release ZIP is a transport artifact, not proof that the content is trustworthy or behaviorally correct. The build and verification utilities detect accidental corruption, preserve required executable bits, reject unsafe archive paths and symlinks, and make equivalent source trees produce the same archive bytes under the same build inputs. The included SHA-256 manifest and detached archive checksum provide integrity checks only; they do not authenticate the publisher against a malicious party capable of replacing both the archive and its checksum. Use a trusted release channel and, where required by the deployment environment, a separately managed signature or attestation.

## Deterministic build contract

`scripts/build-release.py` packages all eligible files under the source root in lexicographic POSIX-path order. It normalizes timestamps to `SOURCE_DATE_EPOCH` (default 2000-01-01 UTC), uses fixed compression settings, strips transient caches and pre-existing ZIP files, rejects symbolic links, and writes a normalized Unix mode for each file. Expected CLI entrypoints are explicitly allowlisted as executable; other package files are mode `0644`. The output must be outside the source tree so that it cannot include itself or vary because of an older build.

Build with:

```bash
python3 scripts/build-release.py --root . --output ../project-artifact-excellence-skill-set.zip
```

Set `SOURCE_DATE_EPOCH` to an integer Unix epoch when a controlled timestamp is needed, or pass `--epoch` explicitly. The archive's `RELEASE-MANIFEST.sha256` covers every packaged file except itself to avoid a self-referential digest. The builder also writes a detached checksum beside the archive as `<archive>.sha256`.

## Verification contract

Verify before extraction:

```bash
python3 scripts/verify-release.py ../project-artifact-excellence-skill-set.zip
```

The verifier rejects duplicate entry names, absolute paths, parent traversal, backslashes, unexpected directory entries, missing required package entrypoints, absent executable mode bits, malformed checksum manifests, missing/unlisted files, and content-hash mismatches. Independently verify the detached archive checksum against the actual archive bytes using a trusted local SHA-256 utility. Only then extract into a dedicated destination and run:

```bash
bash validation/validate-set.sh
```

The validation gates are read-only over production source files. Tests may use temporary directories and create temporary archives, but must not mutate member skills or reference files.

## Compatibility and release policy

- Keep `manifest.yaml`, `SET.md`, member metadata versions, and release notes aligned.
- Preserve reference files unless a replacement has equal or better coverage and explicit link verification.
- Breaking changes to machine-readable contracts require a version/migration note. The trigger-matrix validator accepts legacy schema `1.0` for the lightweight documentation sample and requires schema `1.1` for the authoritative evaluation matrix.
- A clean archive and passing static gates do not establish runtime trigger precision/recall, task success, accessibility, security, or production performance; those require independent, context-appropriate evaluation.
- Capture the archive checksum, validation command, environment/tool versions, and release decision in the release record. Do not reuse a prior result after code or archive changes.
- Optional authenticity upgrade (PA-REL-12): where the deployment environment requires publisher authentication beyond the trusted channel, sign the archive with `cosign sign-blob` and publish an SBOM via `syft`; record signature and SBOM digests in the release record alongside the SHA-256 checksum.
