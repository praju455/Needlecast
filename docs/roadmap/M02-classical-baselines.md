# M02 · Classical baselines and metrics

**Status** · Planned

## Objective

Publish matched classical baselines.

## Why it matters

A strong classical reference is necessary to estimate the value of re-scoring.

## Prerequisites and dependencies

[M01](M01-data-layer.md)

## Detailed task checklist

1. **M** · `ml/src/needlecast_ml/classical` · Fit LR, RF, XGBoost, RBF-SVM, random Fourier features, Isolation Forest and MLP with fixed budgets.
2. **M** · `ml/src/needlecast_ml/evaluation` · Run at least five seeds and record average precision, recall at a fixed FPR, F1, MCC, cost, and workload.
3. **S** · `ml/artifacts/schemas` · Validate model metrics, folds, IDs, and threshold provenance.

## Deliverables

- Versioned baseline results, curve data, and reproducible runner configuration.

## Acceptance criteria

- The matched variants share feature budget and row IDs.
- Each run records model and reducer parameters and seed.
- The selected operating threshold comes from validation.

## Test plan

Verify metrics against small known examples and run one split twice with the same seed before running the full comparison.

## Risks and mitigations

Class imbalance can make accuracy misleading. Use average precision and false-alert operating points with the original prevalence.

## Exit checklist

- [ ] Lock scoring orientation.
- [ ] Publish per-seed metrics.
- [ ] Validate comparison artifacts.

## Related docs

- [Design reference](../experiment-protocol.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
