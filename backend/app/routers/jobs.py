"""Expose M00 simulated experiment submission and status endpoints."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Header

from backend.app.deps import JobDep
from backend.app.schemas.api import Job, JobRequest
from backend.app.services.errors import ERROR_RESPONSES

router = APIRouter(tags=["Jobs"])


@router.post(
    "/api/jobs/run", status_code=202, responses={n: ERROR_RESPONSES[n] for n in (409, 422, 503)}
)
def run_job(
    payload: JobRequest,
    store: JobDep,
    tasks: BackgroundTasks,
    key: Annotated[
        str | None, Header(alias="Idempotency-Key", min_length=1, max_length=128)
    ] = None,
) -> Job:
    job, created = store.submit(payload, key)
    if created:
        tasks.add_task(store.simulate, job.id, payload.preset)
    return job


@router.get("/api/jobs/{id}", responses={404: ERROR_RESPONSES[404]})
def read_job(id: str, store: JobDep) -> Job:
    return store.get(id)
