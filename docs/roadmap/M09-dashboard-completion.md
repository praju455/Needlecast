# M09 · Dashboard completion

**Status** · Planned

## Objective

Make artifacts and traces usable for analysts.

## Why it matters

Analysts need the evidence, dataset references and decisions in context.

## Prerequisites and dependencies

[M00](M00-foundation.md), [M08](M08-serving.md)

Start page development against M00. Validate live-artifact integration after M08.

## Detailed task checklist

1. **M** · `frontend/src/app` · Build accessible charts, sorting, and error and empty states against the M00 sample contract.
2. **M** · `frontend/src/components/scoring` · Show trace transitions, thresholds, fallback status, SHAP evidence and approved support examples.
3. **S** · `frontend/e2e` · Switch sample tests to validated artifact-backed fixtures and review keyboard, contrast, and motion behavior.

## Deliverables

- Dashboard with reviewed loading, failure, and live-result states.
- Browser and accessibility test results.

## Acceptance criteria

- Every page works across sample and validated fixtures.
- All controls have keyboard focus and labeled equivalents.
- Scores clearly identify mode and active bundle.

## Test plan

Use browser smoke tests against seeded stubs during development and validated results at integration.

## Risks and mitigations

Charts can overstate simulated numbers. Preserve separate placeholder or live modes throughout presentation.

## Exit checklist

- [ ] Check mobile navigation.
- [ ] Test fallback states.
- [ ] Record accessibility review.

## Related docs

- [Design reference](../serving-and-deployment.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
