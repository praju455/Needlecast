# Evaluation protocol

The experiment asks whether conditional quantum re-scoring improves fraud decisions enough to justify its cost. Results are to be measured after the prototype is implemented.

## Compare models and policies

| Comparison | Controls |
| --- | --- |
| Matched model comparison | Use identical eligible features, chronological folds, training IDs, and evaluation rows. Start with 1,000–3,000 matched training examples where feasible. Publish total rows, fraud counts, class weights, and tuning budgets. |
| Quantum contribution | Compare the QSVM against a tuned RBF kernel and random Fourier features. Measure alignment and detection quality on matched data. |
| Operational baseline | Compare the full cascade against the full-data classical screen and the cascade with re-scoring disabled. |
| Ablations | Vary the reducer, uncertainty band, circuit settings, or HQNN data re-uploading under a recorded budget. |
| Repeatability | Run at least five seeds. Report each result, the mean and standard deviation, and paired time-block intervals when there are enough independent time blocks and fraud cases. |

Fit the logistic score combiner on chronological out-of-fold predictions. Select calibration, the inclusive routing band, and decision thresholds on validation. Keep the last test period untouched until the models and policies are frozen. Evaluate the complete population, including cases that bypass or fall back from the quantum stage.

## Choose an operating point

For each candidate threshold, add estimated per-transaction fraud exposure for missed cases and review cost plus customer friction for false alerts. Apply any review-volume constraint before selecting the lowest-cost eligible threshold. Use INR consistently and record currency conversion, review-cost assumptions, and the tie rule. Evaluate sensitivity to those assumptions and report total and per-transaction cost.

## Report results

| Measure | Required evidence |
| --- | --- |
| Average precision and precision–recall curve | Publish the test prevalence and positive count alongside the curve. |
| Fraud recall at a fixed false-positive rate | Choose the operating point on validation. Report achieved test recall, false-positive rate, and confusion counts. |
| F1 and Matthews correlation coefficient | Use frozen thresholds with fraud as the positive class. |
| Cost and workload | Report both policy cost and alert volume, with assumptions and sensitivity. |
| Compute and routing | Record end-to-end p50, p95, and p99 latency, peak memory, routed share, and fallback rate. Show recall versus routed share across candidate bands. |

## Diagnose failure modes

- **Kernel concentration.** Compare off-diagonal variance and label alignment across circuit widths and bandwidths. Record sample IDs and use a common color scale for heatmaps.
- **Training instability.** Measure HQNN gradient variance by layer across initializations and fixed batches. Compare circuit widths, depths, and held-out performance.
- **Noisy re-scoring.** Compare ideal, noisy, and finite-shot simulations on paired inputs. Record shot count, circuit depth, two-qubit gates, score variation, and latency. Treat optional hardware measurements as a separate feasibility check.
- **Drift and uncertainty.** Use later windows with mature labels and record class prevalence, calibration, routed share, and error rates. Report negative and inconclusive findings with their limitations.

Record code and dataset versions, splits, seeds, software, and hardware with every result. See the [research references](../README.md#research-references) for the motivation behind these checks.
