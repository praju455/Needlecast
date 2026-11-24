"""Load M00 validated artifact envelopes from an in-memory cache backed by local files."""

from functools import lru_cache
from pathlib import Path

from needlecast_ml.evaluation.artifacts import ARTIFACTS, Artifact, ArtifactKind
from pydantic import ValidationError

from backend.app.services.errors import ServiceError


class LocalArtifactStore:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.get = lru_cache(maxsize=len(ARTIFACTS))(self._read)

    def _resolve(self, relative: str) -> Path:
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root) or not path.is_file():
            raise ServiceError(404, "artifact_missing", "Generate the sample artifacts and retry.")
        return path

    def _read(self, kind: ArtifactKind) -> Artifact:
        path = self._resolve(f"{kind}.json")
        try:
            artifact = ARTIFACTS[kind].model_validate_json(path.read_bytes())
        except (OSError, ValidationError) as error:
            raise ServiceError(
                503, "artifact_invalid", "The sample artifact could not be loaded."
            ) from error
        if artifact.mode != "stub" or not artifact.disclaimer:
            raise ServiceError(
                503, "artifact_invalid", "The sample artifact requires placeholder labels."
            )
        return artifact

    def circuit(self, name: str) -> Path:
        allowed = {
            i.svg_url.rsplit("/", 1)[-1] for i in self.get(ArtifactKind.CIRCUITS).data.circuits
        }
        if name not in allowed:
            raise ServiceError(404, "artifact_missing", "The requested circuit is unavailable.")
        return self._resolve(f"circuits/{name}")
