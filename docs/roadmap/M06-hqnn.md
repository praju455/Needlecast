# M06 · Hybrid quantum neural network

**Status** · Planned

## Objective

Run a matched HQNN comparison.

## Why it matters

The optional trainable circuit provides an offline comparison with a classical MLP at the same data budget.

## Prerequisites and dependencies

[M02](M02-classical-baselines.md), [M03](M03-feature-reduction.md)

## Detailed task checklist

1. **M** · `ml/src/needlecast_ml/quantum/hqnn.py` · Wire a PennyLane TorchLayer with an encoder and classifier head, then compare weighted and focal loss.
2. **M** · `ml/experiments/hqnn` · Run matched seeds and log initialization, stopping rules, runtime, and gradient variance.
3. **S** · `ml/artifacts/schemas/hqnn.json` · Store loss and per-layer gradient diagnostics with model and split provenance.

## Deliverables

- HQNN and MLP experiment summaries plus gradient diagnostics.

## Acceptance criteria

- Models share eligible data and split IDs.
- Gradient variance is present for each trainable layer and seed.
- Results identify simulator and width.

## Test plan

Check gradient propagation on tiny batches, then verify reproducibility within declared numerical tolerance.

## Risks and mitigations

Small gradients or simulation cost can make runs inconclusive. Set a width and circuit-depth budget before training.

## Exit checklist

- [ ] Verify gradients and seeds.
- [ ] Validate matched settings.
- [ ] Publish all scheduled outcomes.

## Related docs

- [Design reference](../data-and-models.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
