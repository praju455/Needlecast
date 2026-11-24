"""Create the M00 FastAPI scaffold and mount its placeholder routes."""

import json
import logging
from collections.abc import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from backend.app.config import VERSION, ApiSettings
from backend.app.routers import datasets, diagnostics, health, jobs, models, pipeline, score
from backend.app.schemas.api import Error
from backend.app.services.artifact_store import LocalArtifactStore
from backend.app.services.errors import ServiceError
from backend.app.services.job_service import InMemoryJobStore
from backend.app.services.scoring_service import StubScoringService


def create_app(settings: ApiSettings | None = None) -> FastAPI:
    settings = settings or ApiSettings()
    service = FastAPI(
        title="Needlecast", version=VERSION, description="Needlecast placeholder API."
    )
    service.state.artifacts = LocalArtifactStore(settings.artifact_dir)
    service.state.scorer = StubScoringService()
    service.state.jobs = InMemoryJobStore()
    log = logging.getLogger("uvicorn.error").getChild("needlecast")
    log.setLevel(settings.log_level)
    if settings.allowed_origins:
        service.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_methods=["GET", "POST"],
            allow_headers=["Content-Type", "Idempotency-Key"],
            expose_headers=["X-Request-ID"],
        )

    @service.middleware("http")
    async def request_id(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request.state.request_id = uuid4().hex
        try:
            response = await call_next(request)
        except Exception:
            log.error(
                json.dumps({"event": "request_failed", "request_id": request.state.request_id})
            )
            response = error_response(
                request, 500, "internal_error", "The request could not be completed."
            )
        response.headers["X-Request-ID"] = request.state.request_id
        route = request.scope.get("route")
        log.info(
            json.dumps(
                {
                    "event": "response",
                    "request_id": request.state.request_id,
                    "method": request.method,
                    "route": getattr(route, "path", None),
                    "status": response.status_code,
                }
            )
        )
        return response

    def error_response(request: Request, status: int, code: str, message: str) -> JSONResponse:
        payload = Error(code=code, message=message, request_id=request.state.request_id)
        return JSONResponse(status_code=status, content=payload.model_dump())

    @service.exception_handler(ServiceError)
    async def service_error(request: Request, error: ServiceError) -> JSONResponse:
        return error_response(request, error.status, error.code, error.message)

    @service.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, error: RequestValidationError) -> JSONResponse:
        return error_response(
            request, 422, "invalid_request", "Check the request schema and supplied values."
        )

    @service.exception_handler(HTTPException)
    async def http_error(request: Request, error: HTTPException) -> JSONResponse:
        return error_response(
            request, error.status_code, "http_error", "The requested operation is unavailable."
        )

    for module in (health, datasets, pipeline, models, diagnostics, score, jobs):
        service.include_router(module.router)
    return service


app = create_app()
