# Placeholder data policy

The sample app demonstrates the interface using seeded placeholder data. The sample JSON contains `mode: "stub"`, `disclaimer`, `seed`, and `generated_by`. The UI displays a persistent **Placeholder data** notice. Scores, metrics, and diagnostics illustrate formats and routing behavior and carry no measured-performance claim.

Run `make sample-artifacts` to regenerate the published samples and `make validate-artifacts` to verify their schemas. The generator writes JSON and circuit SVGs to `ml/artifacts/sample/`. Use the same seed for identical bytes. Synthetic fixtures can be checked in. Keep real card data, identifiers, and credentials out of Git.

M08 will add artifact-backed adapters behind the HTTP contract. Verify a new bundle before activation and preserve the mode and bundle ID in the response. See the [stub-to-real diagram](roadmap/M08-serving.md#detailed-task-checklist).
