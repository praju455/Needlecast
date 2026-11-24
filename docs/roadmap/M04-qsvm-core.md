# M04 · QSVM core

**Status** · Planned

## Objective

Train matched and one-class kernel comparisons.

## Why it matters

Stable training-kernel column order and bounded scoring are essential to evaluate the second opinion.

## Prerequisites and dependencies

[M02](M02-classical-baselines.md), [M03](M03-feature-reduction.md)

## Detailed task checklist

1. **M** · `ml/src/needlecast_ml/quantum/feature_maps.py` · Implement angle, ZZ-style and IQP-style feature maps with lazy simulator imports.
2. **M** · `ml/src/needlecast_ml/quantum/kernels.py` · Batch statevectors and overlaps, cache fitted states, and record a complete feature-map fingerprint.
3. **M** · `ml/src/needlecast_ml/quantum/qsvm.py` · Fit supervised precomputed SVC and an optional one-class variant. Tune bandwidth on validation.

## Deliverables

- Versioned quantum kernels, fitted SVM assets, cache fingerprints and reference IDs.

## Acceptance criteria

- The ideal training kernel is finite, symmetric and near-unit diagonal.
- Serving preserves the fitted query-to-training column order.
- Optional simulator imports stay out of the base test path.

## Test plan

Compare exact overlap with an analytic small circuit and verify training/inference parity after persisting the reference set.

## Risks and mitigations

Kernel caching can mix incompatible transforms or simulator settings. Key caches by complete configuration and ordered input fingerprints.

## Exit checklist

- [ ] Check ideal kernel invariants.
- [ ] Record CPU/memory budget.
- [ ] Repeat matched validation.

## Related docs

- [Design reference](../data-and-models.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
