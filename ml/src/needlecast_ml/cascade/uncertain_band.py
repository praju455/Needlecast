"""Use the inclusive M07 routing policy and select a validation quantile band."""

import numpy as np
from numpy.typing import ArrayLike


def in_uncertain_band(score: float, lower: float, upper: float) -> bool:
    if not 0 <= lower <= upper <= 1 or not 0 <= score <= 1:
        raise ValueError("Scores and ordered band bounds must lie in [0, 1].")
    return lower <= score <= upper


def quantile_band(scores: ArrayLike, lower: float, upper: float) -> tuple[float, float]:
    values = np.asarray(scores, dtype=float)
    if values.ndim != 1 or values.size == 0 or not np.all((0 <= values) & (values <= 1)):
        raise ValueError("Provide a nonempty vector of probabilities.")
    if not 0 <= lower <= upper <= 1:
        raise ValueError("Quantiles must be ordered and lie in [0, 1].")
    bounds = np.quantile(values, [lower, upper])
    return float(bounds[0]), float(bounds[1])
