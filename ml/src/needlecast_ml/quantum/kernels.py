"""Compute M04 reference angle-embedding fidelity using bounded NumPy batches."""

import hashlib
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
from numpy.typing import ArrayLike, NDArray

from needlecast_ml.config import Settings


def _states(angles: NDArray[np.float64]) -> NDArray[np.float64]:
    states = np.ones((len(angles), 1))
    for column in angles.T:
        single = np.stack((np.cos(column / 2), np.sin(column / 2)), axis=1)
        states = (states[:, :, None] * single[:, None, :]).reshape(len(angles), -1)
    return states


def angle_fidelity_kernel(
    inputs: ArrayLike,
    reference: ArrayLike | None = None,
    *,
    qubit_cap: int | None = None,
    batch_size: int = 128,
    cache_dir: Path | None = None,
) -> NDArray[np.float64]:
    """Return squared state overlaps in reference-row order and optionally cache to .npy."""
    limit = Settings().qubit_cap if qubit_cap is None else qubit_cap
    x = np.ascontiguousarray(inputs, dtype="<f8")
    y = x if reference is None else np.ascontiguousarray(reference, dtype="<f8")
    if (
        x.ndim != 2
        or y.ndim != 2
        or not len(x)
        or not len(y)
        or x.shape[1] != y.shape[1]
        or not 1 <= x.shape[1] <= limit <= 12
        or batch_size < 1
        or not np.isfinite(x).all()
        or not np.isfinite(y).all()
    ):
        raise ValueError("Use finite angle matrices with a shared width within the qubit cap.")

    cache = None
    if cache_dir is not None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        key = hashlib.sha256(f"angle-ry-v1:{x.shape}:{y.shape}".encode())
        key.update(x.tobytes())
        key.update(y.tobytes())
        cache = cache_dir / f"{key.hexdigest()}.npy"
        if cache.is_file():
            return np.load(cache, allow_pickle=False)

    kernel = np.empty((len(x), len(y)))
    for i in range(0, len(x), batch_size):
        left = _states(x[i : i + batch_size])
        for j in range(0, len(y), batch_size):
            right = _states(y[j : j + batch_size])
            kernel[i : i + len(left), j : j + len(right)] = (left @ right.T) ** 2
    np.clip(kernel, 0, 1, out=kernel)

    if cache is not None:
        with NamedTemporaryFile(dir=cache.parent, suffix=".npy", delete=False) as handle:
            tmp = Path(handle.name)
            try:
                np.save(handle, kernel, allow_pickle=False)
                handle.flush()
                os.replace(tmp, cache)
            finally:
                tmp.unlink(missing_ok=True)
    return kernel
