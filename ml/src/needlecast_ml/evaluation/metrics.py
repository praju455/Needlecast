"""Compute the M02 binary model comparison metrics with an explicit operating point."""

import numpy as np
from numpy.typing import ArrayLike
from sklearn.metrics import average_precision_score, f1_score, matthews_corrcoef, roc_curve


def binary_metrics(
    labels: ArrayLike, scores: ArrayLike, *, threshold: float, fpr_limit: float
) -> dict[str, float]:
    """Return average precision, maximum ROC recall within the FPR limit, F1, and MCC."""
    y, p = np.asarray(labels), np.asarray(scores, dtype=float)
    if y.ndim != 1 or y.shape != p.shape or set(y.tolist()) != {0, 1}:
        raise ValueError("Provide aligned vectors with both binary classes.")
    if not np.all((0 <= p) & (p <= 1)) or not 0 <= threshold <= 1 or not 0 <= fpr_limit <= 1:
        raise ValueError("Scores, threshold and FPR limit must be in [0, 1].")
    false_rate, recall, _ = roc_curve(y, p, drop_intermediate=False)
    prediction = p >= threshold
    return {
        "pr_auc": float(average_precision_score(y, p)),
        "recall_at_fixed_fpr": float(recall[false_rate <= fpr_limit].max()),
        "f1": float(f1_score(y, prediction, zero_division=0)),
        "mcc": float(matthews_corrcoef(y, prediction)),
    }
