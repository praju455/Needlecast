# Project status

Needlecast is a hybrid fraud-detection research project. The classical screen handles every sample and routes eligible cases for a bounded second opinion. The M00 scaffold demonstrates the HTTP and UI contracts on seeded placeholders.

| Component | Status | Evidence or next milestone |
| --- | --- | --- |
| Chronological splits, leakage guards, metrics, cost and band utilities, NumPy angle kernel | Implemented | Base ML unit tests |
| Seeded sample artifacts, API, jobs, dashboard, Compose, and CI definitions | Scaffolded (stub) | [M00](roadmap/M00-foundation.md) and its quality gates |
| Dataset ingestion, classical training, feature transformation, QSVM, and HQNN | Planned | [M01 through M07](roadmap/README.md#milestones) |
| Artifact-backed inference, PostgreSQL metadata, and controlled operation | Planned | [M08 through M11](roadmap/README.md#milestones) |

For usage, see the [developer guide](21-developer-guide.md) and the [placeholder data policy](stub-data-policy.md).
