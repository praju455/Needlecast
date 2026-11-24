"""Apply the M07 cost model and select a validation threshold under a review budget."""

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class OperatingPoint:
    threshold: float
    cost: float
    reviews: int


def expected_cost(
    labels: ArrayLike,
    decisions: ArrayLike,
    amounts: ArrayLike,
    *,
    review_fee: float,
    friction: float,
) -> float:
    """Sum missed-fraud exposure and per-false-alert costs in the configured currency."""
    y, flagged, exposure = np.asarray(labels), np.asarray(decisions), np.asarray(amounts, float)
    if y.ndim != 1 or y.shape != flagged.shape or y.shape != exposure.shape:
        raise ValueError("Labels, decisions, and amounts must be aligned vectors.")
    if not np.isin(y, (0, 1)).all() or not np.isin(flagged, (0, 1)).all():
        raise ValueError("Labels and decisions must be binary.")
    if not np.isfinite(exposure).all() or np.any(exposure < 0):
        raise ValueError("Transaction exposures must be finite and nonnegative.")
    if not np.isfinite([review_fee, friction]).all() or min(review_fee, friction) < 0:
        raise ValueError("Review costs must be finite and nonnegative.")
    return float(
        exposure[(y == 1) & (flagged == 0)].sum()
        + (review_fee + friction) * np.count_nonzero((y == 0) & (flagged == 1))
    )


def review_decision(score: float, threshold: float) -> bool:
    if not 0 <= score <= 1 or not 0 <= threshold <= 1:
        raise ValueError("Score and threshold must be in [0, 1].")
    return score >= threshold


def choose_threshold(
    labels: ArrayLike,
    scores: ArrayLike,
    exposures: ArrayLike,
    candidates: Iterable[float],
    *,
    review_fee: float,
    friction: float,
    max_reviews: int,
) -> OperatingPoint:
    """Minimize cost, then review count, then prefer the higher threshold."""
    values = np.asarray(scores, dtype=float)
    if values.ndim != 1 or not values.size or not np.all((0 <= values) & (values <= 1)):
        raise ValueError("Provide a nonempty vector of scores in [0, 1].")
    points = []
    for threshold in candidates:
        review_decision(0.0, threshold)
        flags = values >= threshold
        reviews = int(flags.sum())
        if reviews <= max_reviews:
            cost = expected_cost(labels, flags, exposures, review_fee=review_fee, friction=friction)
            points.append(OperatingPoint(threshold, cost, reviews))
    if not points:
        raise ValueError("No candidate fits the review budget.")
    return min(points, key=lambda p: (p.cost, p.reviews, -p.threshold))
