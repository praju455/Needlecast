"""Expose M00 dataset provenance and class balance."""

from fastapi import APIRouter
from needlecast_ml.evaluation.artifacts import ArtifactKind

from backend.app.routers._artifacts import add_artifact

router = APIRouter(tags=["Datasets"])
add_artifact(router, "/api/datasets", ArtifactKind.DATASETS, "Read dataset provenance and splits")
