"""Expose the M00 scorer interface and deterministic placeholder implementation."""

import hashlib
import json
import math
from typing import Protocol

from needlecast_ml.cascade.cost_model import choose_threshold, review_decision
from needlecast_ml.cascade.uncertain_band import in_uncertain_band

from backend.app.schemas.api import ScoredModel, ScoreRequest, ScoreResponse, TraceStage
from backend.app.services.errors import ServiceError

LOWER = 0.35
UPPER = 0.65
THRESHOLD = choose_threshold(
    [0, 0, 1, 1],
    [0.08, 0.52, 0.61, 0.92],
    [100, 200, 500, 900],
    [0.35, 0.50, 0.60, 0.75],
    review_fee=20,
    friction=10,
    max_reviews=2,
).threshold


class ScoringService(Protocol):
    def score(self, payload: ScoreRequest, request_id: str) -> ScoreResponse: ...


def _score(payload: ScoreRequest, stage: str) -> float:
    normalized = {key: value or 0.0 for key, value in payload.transaction.items()}
    value = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(f"{payload.feature_schema_id}:{stage}:{value}".encode()).digest()
    return round(int.from_bytes(digest[:8], "big") / (2**64 - 1), 6)


class StubScoringService:
    def _quantum_score(self, payload: ScoreRequest) -> float:
        return _score(payload, "quantum")

    def score(self, payload: ScoreRequest, request_id: str) -> ScoreResponse:
        if payload.mode != "stub":
            raise ServiceError(503, "mode_unavailable", "Live scoring is not configured.")
        if payload.feature_schema_id != "sample-v1":
            raise ServiceError(422, "feature_schema_unknown", "Use the sample-v1 feature schema.")
        fields = payload.transaction
        if set(fields) == {"amount"}:
            valid = fields["amount"] >= 0
        else:
            valid = set(fields) == {"angle_1", "angle_2", "angle_3", "angle_4"} and all(
                0 <= value <= math.pi for value in fields.values()
            )
        if not valid:
            raise ServiceError(
                422,
                "feature_values_invalid",
                "Use a nonnegative amount or four ordered angles in [0, π].",
            )
        classical = _score(payload, "classical")
        routed = in_uncertain_band(classical, LOWER, UPPER)
        quantum = None
        fallback_reason = None
        quantum_notes = "Outside the uncertainty band."
        if routed:
            try:
                quantum = self._quantum_score(payload)
                quantum_notes = "Placeholder second score."
            except TimeoutError:
                fallback_reason = "quantum_timeout"
                quantum_notes = "Second-stage timeout. Used the classical policy."
        final_score = round((classical + quantum) / 2, 6) if quantum is not None else classical
        return ScoreResponse(
            request_id=request_id,
            bundle_id="sample-bundle",
            policy_id="sample-policy",
            classical=ScoredModel(model_id="sample-classical", score=classical, elapsed_ms=1.0),
            quantum=ScoredModel(model_id="sample-qsvm", score=quantum, elapsed_ms=4.0)
            if quantum is not None
            else None,
            route=(
                "classical_fallback"
                if fallback_reason
                else "quantum_rescored"
                if routed
                else "classical_only"
            ),
            fallback_reason=fallback_reason,
            final_score=final_score,
            threshold=THRESHOLD,
            decision="review" if review_decision(final_score, THRESHOLD) else "clear",
            stages=[
                TraceStage(
                    name="Classical screen",
                    invoked=True,
                    score=classical,
                    latency_ms=1,
                    notes="Placeholder first score.",
                ),
                TraceStage(
                    name="Quantum re-score",
                    invoked=routed,
                    score=quantum,
                    latency_ms=4 if quantum is not None else None,
                    notes=quantum_notes,
                ),
                TraceStage(
                    name="Review policy",
                    invoked=True,
                    score=final_score,
                    latency_ms=1,
                    notes="Uses the placeholder validation cost threshold.",
                ),
            ],
        )
