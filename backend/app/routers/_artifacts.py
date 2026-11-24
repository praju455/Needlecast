"""Register typed M00 artifact reads and check the published sample run ID."""

from fastapi import APIRouter
from needlecast_ml.evaluation.artifacts import ARTIFACTS, Artifact, ArtifactKind

from backend.app.deps import ArtifactDep
from backend.app.services.errors import ERROR_RESPONSES, ServiceError


def add_artifact(router: APIRouter, path: str, kind: ArtifactKind, summary: str) -> None:
    def endpoint(store: ArtifactDep, run_id: str | None = None) -> Artifact:
        result = store.get(kind)
        if run_id is not None and result.run_id != run_id:
            raise ServiceError(404, "run_missing", "The requested sample run is unavailable.")
        return result

    router.add_api_route(
        path,
        endpoint,
        methods=["GET"],
        name=kind,
        response_model=ARTIFACTS[kind],
        summary=summary,
        responses={n: ERROR_RESPONSES[n] for n in (404, 503)},
    )
