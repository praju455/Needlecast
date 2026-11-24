# M11 · Hardening and release

**Status** · Planned

## Objective

Prepare a reproducible controlled release.

## Why it matters

A release needs repeatable builds, rollback evidence, and a scope decision anchored in measured results.

## Prerequisites and dependencies

[M08](M08-serving.md), [M09](M09-dashboard-completion.md), [M10](M10-robustness-and-scale.md)

## Detailed task checklist

1. **M** · `docker-compose.yml and .github/workflows` · Build clean images and exercise health checks, artifact mounts, and rollback.
2. **M** · `backend/app and docs/serving-and-deployment.md` · Review permissions, retention, secrets, operational limits and audit fields.
3. **S** · `README.md and docs/roadmap/quality-gates.md` · Publish the benchmark report, agree license and release notes, and tag the verified revision.

## Deliverables

- Benchmark report, release notes, validated image and artifact manifests.
- Signed-off rollout and rollback checklist.

## Acceptance criteria

- CI checks run clean on the candidate revision.
- Rollback rehearsal restores the previous validated model bundle.
- Release note identifies the matching image and artifact digests.

## Test plan

Start from a clean checkout, run the report and CI gates, then rehearse rollback in a controlled environment.

## Risks and mitigations

Configuration and artifact values can diverge between environments. Record known digests and keep the prior bundle available.

## Exit checklist

- [ ] Confirm documented license decision.
- [ ] Record release evidence.
- [ ] Rehearse rollback and confirm tags.

## Related docs

- [Design reference](../serving-and-deployment.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
