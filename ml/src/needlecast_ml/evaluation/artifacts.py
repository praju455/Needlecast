"""Define M00 typed artifact contracts shared by the generator and HTTP API."""

from enum import StrEnum
from typing import Annotated, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

DISCLAIMER = "Placeholder data. Scores, metrics, and diagnostics are illustrative."
Probability = Annotated[float, Field(ge=0, le=1)]


class ArtifactKind(StrEnum):
    DATASETS = "datasets"
    REDUCTION = "reduction"
    COMPARISON = "comparison"
    ABLATIONS = "ablations"
    CIRCUITS = "circuits"
    KERNEL = "kernel"
    HQNN = "hqnn"
    NOISE = "noise"


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Counts(Record):
    window: str
    rows: int
    fraud: int


class Dataset(Record):
    id: str
    name: str
    source: str
    splits: list[Counts]


class Datasets(Record):
    datasets: list[Dataset]


class Reduction(Record):
    schema_id: str
    reducer: str
    input_dimensions: int
    output_dimensions: int
    features: list[str]
    explained_variance: list[Probability]


class Metric(Record):
    model: str
    pr_auc: Probability
    recall_at_fixed_fpr: Probability
    f1: Probability
    mcc: Annotated[float, Field(ge=-1, le=1)]


class CurvePoint(Record):
    x: Probability
    y: Probability
    low: Probability | None = None
    high: Probability | None = None


class Cost(Record):
    policy: str
    expected_cost_inr: float


class Comparison(Record):
    metrics: list[Metric]
    pr_curve: list[CurvePoint]
    roc_curve: list[CurvePoint]
    routing: list[CurvePoint]
    costs: list[Cost]


class Ablation(Record):
    policy: str
    pr_auc_delta: float
    routed_share: Probability
    interval: str


class Ablations(Record):
    rows: list[Ablation]


class Circuit(Record):
    name: str
    svg_url: str
    width: int
    depth: int
    gates: int
    transpiled_depth: int


class Circuits(Record):
    circuits: list[Circuit]


class Trend(Record):
    label: str
    value: float


class Kernel(Record):
    matrix: list[list[Probability]]
    classes: list[Literal[0, 1]]
    variance: float
    alignment: float
    concentration: list[Trend]


class HQNN(Record):
    loss: list[Trend]
    gradient_variance: list[Trend]


class Noise(Record):
    ideal_recall: Probability
    shot_recall: list[Trend]


T = TypeVar("T", bound=Record)


class Artifact(Record, Generic[T]):
    mode: Literal["stub", "live"]
    disclaimer: str | None = None
    generated_by: str
    seed: int
    schema_version: Literal["1"]
    run_id: str
    created_at: str
    dataset_id: str
    split_id: str
    data: T


ARTIFACTS: dict[ArtifactKind, type[Artifact]] = {
    ArtifactKind.DATASETS: Artifact[Datasets],
    ArtifactKind.REDUCTION: Artifact[Reduction],
    ArtifactKind.COMPARISON: Artifact[Comparison],
    ArtifactKind.ABLATIONS: Artifact[Ablations],
    ArtifactKind.CIRCUITS: Artifact[Circuits],
    ArtifactKind.KERNEL: Artifact[Kernel],
    ArtifactKind.HQNN: Artifact[HQNN],
    ArtifactKind.NOISE: Artifact[Noise],
}
