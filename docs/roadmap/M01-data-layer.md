# M01 · Data layer

**Status** · Planned

## Objective

Produce leakage-checked chronological splits.

## Why it matters

Reliable model comparisons start with eligible features and an untouched final test window.

## Prerequisites and dependencies

[M00](M00-foundation.md)

## Detailed task checklist

1. **S** · `ml/src/needlecast_ml/data/loaders.py` · Read the ULB CSV only from an explicitly supplied local path and validate the schema.
2. **S** · `ml/src/needlecast_ml/data/splits.py` · Record release IDs, cutoffs, tie handling, and label maturity assumptions.
3. **M** · `ml/tests and docs/data-and-models.md` · Add leakage edge cases, a data card, and pre- and post-split prevalence tables.

## Deliverables

- ULB loader and dataset card.
- Versioned split manifest and class-imbalance report.

## Acceptance criteria

- Train, validation, and test IDs are disjoint.
- Both classes occur in each split and timestamps progress chronologically.
- Reported raw counts match the validated release.

## Test plan

Exercise missing columns, duplicate IDs, timestamp ties, delayed labels, and single-class windows on tiny local fixtures.

## Risks and mitigations

Delayed outcomes can leak information. Record an eligibility cutoff and a label-maturity gap before splitting.

## Exit checklist

- [ ] Verify release terms and checksum.
- [ ] Record split provenance.
- [ ] Freeze the test IDs.

## Related docs

- [Design reference](../data-and-models.md)
- [Quality gates](quality-gates.md)
- [Dependency map](dependency-map.md)
