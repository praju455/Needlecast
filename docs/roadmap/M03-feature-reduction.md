# M03 · Feature reduction

**Status** · Planned

## Objective

Freeze an ordered, versioned angle transform.

## Why it matters

Train-only reduction keeps the quantum comparisons manageable and serving reproducible.

## Prerequisites and dependencies

[M01](M01-data-layer.md)

## Detailed task checklist

1. **M** · `ml/src/needlecast_ml/features/reduction.py` · Fit PCA, mutual information selection, and an autoencoder within training folds.
2. **S** · `ml/src/needlecast_ml/features/scaling.py` · Fit ordered bounds that clip held-out inputs into [0, π] and map constants to zero.
3. **S** · `ml/artifacts/schemas/reduction.json` · Persist the feature order, reducer state, qubit mapping, and clipping rates.

## Deliverables

- Fitted reducers and angle scales.
- Versioned feature schema and qubit mapping.

## Acceptance criteria

- Reducers use training IDs exclusively.
- Reloaded transforms produce the same ordered angles.
- All outputs respect the configured cap and scaling range.

## Test plan

Compare transform parity after serialization and exercise constant columns, unseen extrema, and schema mismatches.

## Risks and mitigations

Feature order can drift when reloading models. Persist and validate a schema ID with ordered names and dimensions.

## Exit checklist

- [ ] Verify clipping and constants.
- [ ] Check fitted row scope.
- [ ] Freeze the reducer per run.

## Related docs

- [Design reference](../data-and-models.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
