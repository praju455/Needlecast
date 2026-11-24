"""Enforce M01 partition disjointness and train-only fitting by row ID."""

from collections.abc import Hashable, Iterable


def assert_disjoint(*partitions: Iterable[Hashable]) -> None:
    seen: set[Hashable] = set()
    for partition in partitions:
        rows = list(partition)
        unique = set(rows)
        if len(unique) != len(rows) or seen.intersection(unique):
            raise ValueError("Row IDs must occur exactly once across partitions.")
        seen.update(unique)


def assert_fit_on_train(fit_ids: Iterable[Hashable], train_ids: Iterable[Hashable]) -> None:
    requested = set(fit_ids)
    if not requested or not requested.issubset(train_ids):
        raise ValueError("Fit rows must be a nonempty subset of the training IDs.")
