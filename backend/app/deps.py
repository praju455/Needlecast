"""Provide the M00 API service dependencies from application state."""

from typing import Annotated

from fastapi import Depends, Request

from backend.app.services.artifact_store import LocalArtifactStore
from backend.app.services.job_service import JobStore
from backend.app.services.scoring_service import ScoringService


def artifacts(request: Request) -> LocalArtifactStore:
    return request.app.state.artifacts


def scorer(request: Request) -> ScoringService:
    return request.app.state.scorer


def jobs(request: Request) -> JobStore:
    return request.app.state.jobs


ArtifactDep = Annotated[LocalArtifactStore, Depends(artifacts)]
ScoringDep = Annotated[ScoringService, Depends(scorer)]
JobDep = Annotated[JobStore, Depends(jobs)]
