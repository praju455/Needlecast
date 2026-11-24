"""Build M01 chronological train, validation, and test partitions."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class TimeSplit:
    """Integer row positions in chronological order."""

    train: NDArray[np.intp]
    validation: NDArray[np.intp]
    test: NDArray[np.intp]


def chronological_split(
    timestamps: ArrayLike,
    labels: ArrayLike,
    train_fraction: float = 0.60,
    validation_fraction: float = 0.20,
) -> TimeSplit:
    """Split without shuffling or separating identical timestamps."""
    times = np.asarray(timestamps)
    target = np.asarray(labels)
    if times.ndim != 1 or target.shape != times.shape or times.size < 6:
        raise ValueError("Provide at least six aligned timestamps and labels.")
    if times.dtype.kind not in "uifM" or not np.isfinite(times).all():
        raise ValueError("Use finite numeric timestamps or valid datetime values.")
    if not np.isin(target, (0, 1)).all():
        raise ValueError("Labels must be binary.")
    if not 0 < train_fraction < train_fraction + validation_fraction < 1:
        raise ValueError("Train and validation fractions must leave a test window.")

    order = np.argsort(times, kind="stable")
    sorted_times = times[order]
    n = len(order)
    first = int(np.searchsorted(sorted_times, sorted_times[int(n * train_fraction)]))
    second = int(
        np.searchsorted(sorted_times, sorted_times[int(n * (train_fraction + validation_fraction))])
    )
    split = TimeSplit(order[:first], order[first:second], order[second:])
    for name in ("train", "validation", "test"):
        if len(np.unique(target[getattr(split, name)])) != 2:
            raise ValueError(f"The {name} window must contain both classes.")
    return split
