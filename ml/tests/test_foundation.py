import hashlib

import numpy as np
import pytest
from needlecast_ml.cascade.cost_model import choose_threshold, expected_cost
from needlecast_ml.cascade.uncertain_band import in_uncertain_band, quantile_band
from needlecast_ml.data.leakage import assert_disjoint, assert_fit_on_train
from needlecast_ml.data.splits import chronological_split
from needlecast_ml.evaluation.metrics import binary_metrics
from needlecast_ml.evaluation.sample import make_samples, validate_samples, write_schemas
from needlecast_ml.quantum.kernels import angle_fidelity_kernel


def test_split_keeps_timestamps_and_classes():
    split = chronological_split(np.repeat(np.arange(10), 2)[::-1], [0, 1] * 10)
    assert [len(group) for group in (split.train, split.validation, split.test)] == [12, 4, 4]
    assert_disjoint(split.train, split.validation, split.test)
    assert_fit_on_train(split.train[:3], split.train)
    with pytest.raises(ValueError, match="both classes"):
        chronological_split(np.arange(10), [0] * 9 + [1])


def test_leakage_rejects_cross_split_rows():
    with pytest.raises(ValueError, match="exactly once"):
        assert_disjoint([1, 2], [2, 3])
    with pytest.raises(ValueError, match="training"):
        assert_fit_on_train([1, 3], [1, 2])


def test_metrics_and_cost():
    assert binary_metrics([0, 1], [0.1, 0.9], threshold=0.5, fpr_limit=0) == dict.fromkeys(
        ("pr_auc", "recall_at_fixed_fpr", "f1", "mcc"), 1
    )
    assert expected_cost([0, 1], [1, 0], [20, 100], review_fee=10, friction=5) == 115
    assert (
        choose_threshold(
            [0, 1],
            [0.4, 0.7],
            [20, 100],
            [0.3, 0.6, 0.8],
            review_fee=10,
            friction=5,
            max_reviews=1,
        ).threshold
        == 0.6
    )


def test_band_includes_endpoints():
    low, high = quantile_band([0, 0.25, 0.5, 0.75, 1], 0.25, 0.75)
    assert (low, high) == (0.25, 0.75)
    assert in_uncertain_band(0.25, low, high)
    assert in_uncertain_band(0.75, low, high)
    assert not in_uncertain_band(0.24, low, high)


def test_kernel_agrees_with_product_and_caches(tmp_path, monkeypatch):
    x = np.random.default_rng(5).uniform(0, np.pi, (7, 4))
    k = angle_fidelity_kernel(x, batch_size=3, cache_dir=tmp_path)
    expected = np.cos((x[:, None] - x[None, :]) / 2).prod(axis=2) ** 2
    assert np.allclose(k, k.T)
    assert np.allclose(np.diag(k), 1)
    assert np.all((0 <= k) & (k <= 1))
    assert np.allclose(k, expected)
    assert np.array_equal(k, angle_fidelity_kernel(x, cache_dir=tmp_path))
    assert np.allclose(angle_fidelity_kernel(x[:2], x[2:]), expected[:2, 2:])
    assert len(list(tmp_path.glob("*.npy"))) == 1
    with pytest.raises(ValueError, match="qubit cap"):
        angle_fidelity_kernel(x, qubit_cap=3)
    monkeypatch.setenv("QUBIT_CAP", "3")
    with pytest.raises(ValueError, match="qubit cap"):
        angle_fidelity_kernel(x)


def test_fixtures_are_exactly_reproducible(tmp_path):
    schemas = tmp_path / "schemas"
    write_schemas(schemas)
    make_samples(tmp_path / "a", 10)
    make_samples(tmp_path / "b", 10)
    validate_samples(tmp_path / "a", schemas)
    for path in (tmp_path / "a").rglob("*"):
        if path.is_file():
            other = tmp_path / "b" / path.relative_to(tmp_path / "a")
            assert (
                hashlib.sha256(path.read_bytes()).digest()
                == hashlib.sha256(other.read_bytes()).digest()
            )
