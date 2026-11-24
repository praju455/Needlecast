# M07 · Cascade, ensemble, and cost

**Status** · Planned

## Objective

Freeze a calibrated routed policy.

## Why it matters

The policy should justify its review burden and additional compute on representative data.

## Prerequisites and dependencies

[M02](M02-classical-baselines.md), [M04](M04-qsvm-core.md)

## Detailed task checklist

1. **M** · `ml/src/needlecast_ml/cascade/ensemble.py` · Fit score calibration and logistic stacking on chronological out-of-fold predictions.
2. **M** · `ml/src/needlecast_ml/cascade` · Select the inclusive band and per-route thresholds by validation cost and review budget.
3. **S** · `ml/artifacts/schemas/comparison.json` · Publish recall versus quantum load, workload, fallback, and sensitivity to explicit INR costs.

## Deliverables

- Versioned combiner and policy bundle.
- Validation cost and routing-load evidence.

## Acceptance criteria

- In-band boundary cases execute the quantum route.
- Timeouts use the separately validated classical policy.
- The final policy and test IDs are frozen before evaluation.

## Test plan

Verify threshold ties, capacity caps, disjoint model-fitting rows, and classical fallback on unavailable quantum inputs.

## Risks and mitigations

Using fitted training predictions for stacking gives optimistic results. Track chronological out-of-fold provenance.

## Exit checklist

- [ ] Lock thresholds and calibration.
- [ ] Test bypass and fallback.
- [ ] Seal the held-out evaluation.

## Related docs

- [Design reference](../experiment-protocol.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
