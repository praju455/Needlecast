"""Define the M00 HTTP contract for health, scoring, jobs, and errors."""

from typing import Annotated, Literal

from needlecast_ml.evaluation.artifacts import DISCLAIMER, Probability, Record
from pydantic import Field

Mode = Literal["stub", "live"]


class ModeEnvelope(Record):
    mode: Mode = "stub"
    disclaimer: str | None = DISCLAIMER


class Health(ModeEnvelope):
    status: Literal["ok"] = "ok"
    version: str


class Error(ModeEnvelope):
    code: str
    message: str
    request_id: str


class ScoreRequest(Record):
    feature_schema_id: str = Field(min_length=1, max_length=100)
    transaction: dict[Annotated[str, Field(pattern=r"^[A-Za-z_][A-Za-z0-9_]{0,49}$")], float] = (
        Field(min_length=1, max_length=32)
    )
    mode: Mode = "stub"


class ScoredModel(Record):
    model_id: str
    score: Probability
    elapsed_ms: float | None


class TraceStage(Record):
    name: str
    invoked: bool
    score: Probability | None
    latency_ms: float | None
    notes: str


class Evidence(Record):
    classical: list[str] = Field(default_factory=list)
    quantum: list[str] = Field(default_factory=list)


class ScoreResponse(ModeEnvelope):
    schema_version: Literal["1"] = "1"
    request_id: str
    bundle_id: str
    policy_id: str
    classical: ScoredModel
    quantum: ScoredModel | None
    final_score: Probability
    threshold: Probability
    decision: Literal["clear", "review"]
    route: Literal["classical_only", "quantum_rescored", "classical_fallback"]
    fallback_reason: str | None = None
    evidence: Evidence = Field(default_factory=Evidence)
    stages: list[TraceStage]


class JobRequest(Record):
    preset: str = Field(min_length=1, max_length=100)
    dataset_id: str = Field(default="sample-ulb", min_length=1, max_length=100)
    mode: Mode = "stub"


class Job(ModeEnvelope):
    id: str
    status: Literal["queued", "running", "succeeded", "failed"] = "queued"
    progress: int = Field(default=0, ge=0, le=100)
    status_url: str
    result_url: str | None = None
    published_run_id: str | None = None
    error_code: str | None = None
