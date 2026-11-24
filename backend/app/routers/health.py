"""Expose the M00 health and version endpoint."""

from fastapi import APIRouter

from backend.app.config import VERSION
from backend.app.schemas.api import Health

router = APIRouter(tags=["Health"])


@router.get("/health")
def health() -> Health:
    return Health(version=VERSION)
