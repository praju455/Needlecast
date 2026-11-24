"""Expose M00 diagnostics and known generated circuit SVGs."""

from fastapi import APIRouter
from fastapi.responses import FileResponse
from needlecast_ml.evaluation.artifacts import ArtifactKind

from backend.app.deps import ArtifactDep
from backend.app.routers._artifacts import add_artifact

router = APIRouter(tags=["Diagnostics"])
for kind, title in (
    (ArtifactKind.CIRCUITS, "Circuit statistics"),
    (ArtifactKind.KERNEL, "Kernel diagnostics"),
    (ArtifactKind.HQNN, "Hybrid network diagnostics"),
    (ArtifactKind.NOISE, "Noise and shot comparisons"),
):
    add_artifact(router, f"/api/diagnostics/{kind}", kind, title)


@router.get("/api/circuit-assets/{name}", response_class=FileResponse)
def circuit_svg(name: str, store: ArtifactDep) -> FileResponse:
    return FileResponse(
        store.circuit(name),
        media_type="image/svg+xml",
        headers={"Content-Security-Policy": "default-src 'none'; sandbox"},
    )
