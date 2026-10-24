# Container Optimization

## Purpose
Define minimal, fast, and secure container image practices.

## Base Image Selection
- Choose distroless or slim variants compatible with the runtime.
- Pin base images by digest.
- Rebuild images at least every 30 days.

## Dockerfile Layering
- Use multi-stage builds separating dependencies, build, test, and runtime.
- Copy lockfiles first and install dependencies before copying source.
- Order instructions from stable to volatile to maximize cache hits.

## Minimization
- Remove package caches, docs, build tools, and test fixtures from final stage.
- Install only production dependencies in runtime image.
- Keep final image under team budget, for example under 200 MB for services.

## Security
- Run as non-root user with explicit UID.
- Use read-only filesystem and drop unnecessary capabilities.
- Scan every build and block High and Critical vulnerabilities.

## Performance
- Set memory and CPU requests and limits matching load tests.
- Configure startup, readiness, and liveness probes.
- Measure cold-start time and alert on 20 percent regression.

## Verification
- Inspect image layers and SBOM before promotion.
- Confirm no secrets exist in layers or environment defaults.
- Test runtime smoke checks from the final image, not the build image.
