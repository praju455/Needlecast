# M05 · Quantum diagnostics

**Status** · Planned

## Objective

Measure kernel and circuit behavior.

## Why it matters

Diagnostics explain whether the encoded circuit gives usable discrimination within a reasonable budget.

## Prerequisites and dependencies

[M04](M04-qsvm-core.md)

## Detailed task checklist

1. **S** · `ml/src/needlecast_ml/quantum/diagnostics.py` · Summarize concentration and alignment across widths and bandwidths.
2. **M** · `ml/artifacts/schemas/circuits.json` · Export circuit SVGs with raw and transpiled depth and gate counts.
3. **S** · `ml/experiments/qsvm` · Compare against tuned RBF and random Fourier features on the same rows.

## Deliverables

- Concentration series, class-sorted heatmaps, alignment and circuit statistics.
- Matched classical kernel report.

## Acceptance criteria

- Matrix order and labels agree.
- Heatmaps use a documented common scale.
- Transpiler options and backend are reported.

## Test plan

Recompute a toy alignment example and verify circuit metadata with each SVG export.

## Risks and mitigations

Heatmaps can imply structure from sorting or scale. Record sample IDs, sort rules, and the color scale.

## Exit checklist

- [ ] Check matrix alignment.
- [ ] Validate circuit references.
- [ ] Keep negative findings in the report.

## Related docs

- [Design reference](../experiment-protocol.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
