"""Expose the versioned M00 transaction-scoring contract."""

from fastapi import APIRouter, Request

from backend.app.deps import ScoringDep
from backend.app.schemas.api import ScoreRequest, ScoreResponse
from backend.app.services.errors import ERROR_RESPONSES

router = APIRouter(tags=["Scoring"])


@router.post("/api/score", responses={n: ERROR_RESPONSES[n] for n in (422, 503)})
def score(payload: ScoreRequest, request: Request, scorer: ScoringDep) -> ScoreResponse:
    return scorer.score(payload, request.state.request_id)
