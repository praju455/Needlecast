# M10 · Robustness and scale

**Status** · Planned

## Objective

Stress-test drift, noise and scale.

## Why it matters

Model behavior can change when data or the simulation conditions shift.

## Prerequisites and dependencies

[M05](M05-quantum-diagnostics.md), [M06](M06-hqnn.md), [M07](M07-cascade-and-cost.md)

## Detailed task checklist

1. **M** · `ml/experiments/robustness` · Evaluate later chronological windows, drift, calibration, shot sensitivity and noise.
2. **M** · `ml/src/needlecast_ml/data` · Use approved IEEE-CIS data for reduction and document scale with PaySim or Sparkov on classical baselines.
3. **S** · `docs/experiment-protocol.md` · Record optional hardware feasibility separately with hardware and simulator settings.

## Deliverables

- Versioned drift, noise, and scale evidence.
- Optional hardware feasibility note.

## Acceptance criteria

- Metrics include operating points and workload for each period.
- Noise comparisons share paired input samples.
- Scale measurements record provenance and resources.

## Test plan

Freeze ID lists and seed simulator settings; repeat workloads and confirm both failure and drift indicators appear when injected.

## Risks and mitigations

Dataset access and hardware scheduling can differ. Record availability and prioritize simulator and classical reproducibility.

## Exit checklist

- [ ] Record drift and resource metrics.
- [ ] Validate shot and simulator settings.
- [ ] List incomplete datasets with reasons.

## Related docs

- [Design reference](../experiment-protocol.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
