"""Queue M00 simulated jobs behind an in-memory, thread-safe store."""

from threading import Lock
from typing import Literal, Protocol
from uuid import uuid4

from backend.app.schemas.api import Job, JobRequest
from backend.app.services.errors import ServiceError


class JobStore(Protocol):
    def submit(self, request: JobRequest, key: str | None) -> tuple[Job, bool]: ...
    def get(self, job_id: str) -> Job: ...
    def simulate(self, job_id: str, preset: str) -> None: ...


class InMemoryJobStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._jobs: dict[str, Job] = {}
        self._keys: dict[str, tuple[JobRequest, str]] = {}

    def submit(self, request: JobRequest, key: str | None) -> tuple[Job, bool]:
        if request.mode != "stub":
            raise ServiceError(503, "mode_unavailable", "Live experiment jobs are not configured.")
        if (
            request.preset not in {"sample-comparison", "sample-diagnostics"}
            or request.dataset_id != "sample-ulb"
        ):
            raise ServiceError(
                422, "job_preset_invalid", "Use an available sample preset and dataset."
            )
        with self._lock:
            if key and key in self._keys:
                original, job_id = self._keys[key]
                if request != original:
                    raise ServiceError(
                        409, "idempotency_conflict", "Use a new key for a different request."
                    )
                return self._jobs[job_id], False
            job_id = uuid4().hex
            job = Job(id=job_id, status_url=f"/api/jobs/{job_id}")
            self._jobs[job_id] = job
            if key:
                self._keys[key] = (request, job_id)
            return job, True

    def get(self, job_id: str) -> Job:
        with self._lock:
            try:
                return self._jobs[job_id]
            except KeyError as error:
                raise ServiceError(404, "job_missing", "The sample job is unavailable.") from error

    def _update(
        self,
        job_id: str,
        status: Literal["running", "succeeded"],
        progress: int,
        result_url: str | None = None,
    ) -> None:
        with self._lock:
            self._jobs[job_id] = self._jobs[job_id].model_copy(
                update={
                    "status": status,
                    "progress": progress,
                    "result_url": result_url,
                    "published_run_id": "sample-bundle" if result_url else None,
                }
            )

    def simulate(self, job_id: str, preset: str) -> None:
        # The background task only selects existing fixtures and never runs training.
        self._update(job_id, "running", 50)
        result = (
            "/api/models/comparison" if preset == "sample-comparison" else "/api/diagnostics/kernel"
        )
        self._update(job_id, "succeeded", 100, result)
