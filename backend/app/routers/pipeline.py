"""Expose M00 feature reduction and circuit input metadata."""

from fastapi import APIRouter
from needlecast_ml.evaluation.artifacts import ArtifactKind

from backend.app.routers._artifacts import add_artifact

router = APIRouter(tags=["Pipeline"])
add_artifact(router, "/api/pipeline/reduction", ArtifactKind.REDUCTION, "Read feature reduction")
