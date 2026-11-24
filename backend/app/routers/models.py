"""Expose M00 model comparisons and ablations."""

from fastapi import APIRouter
from needlecast_ml.evaluation.artifacts import ArtifactKind

from backend.app.routers._artifacts import add_artifact

router = APIRouter(tags=["Models"])
add_artifact(router, "/api/models/comparison", ArtifactKind.COMPARISON, "Read model comparisons")
add_artifact(router, "/api/models/ablations", ArtifactKind.ABLATIONS, "Read matched ablations")
