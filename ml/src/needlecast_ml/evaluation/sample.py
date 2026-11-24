"""Generate, describe, and validate deterministic M00 placeholder fixtures."""

import json
from collections.abc import Mapping
from pathlib import Path
from xml.etree import ElementTree

import numpy as np
from jsonschema import Draft202012Validator

from needlecast_ml.evaluation.artifacts import ARTIFACTS, DISCLAIMER, ArtifactKind


def write_json(path: Path, data: Mapping) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n")


def write_schemas(schema_dir: Path) -> None:
    for kind, contract in ARTIFACTS.items():
        schema = contract.model_json_schema()
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        write_json(schema_dir / f"{kind}.json", schema)


def make_samples(directory: Path, seed: int) -> None:
    rng = np.random.default_rng(seed)
    models = [
        "Logistic regression",
        "Random forest",
        "XGBoost",
        "RBF-SVM",
        "Random Fourier features",
        "Isolation forest",
        "MLP",
        "QSVM",
        "HQNN",
        "Cascade",
    ]
    metrics = [
        dict(
            zip(
                ("pr_auc", "recall_at_fixed_fpr", "f1", "mcc"),
                rng.uniform(0.35, 0.85, size=4).round(3),
                strict=True,
            ),
            model=model,
        )
        for model in models
    ]
    grid = np.linspace(0, 1, 21)
    pr = [
        {
            "x": float(x),
            "y": float(y),
            "low": float(max(0, y - 0.05)),
            "high": float(min(1, y + 0.05)),
        }
        for x, y in zip(grid, 0.98 - 0.85 * grid, strict=True)
    ]
    groups = np.repeat([0, 1], [155, 45])
    embeddings = rng.normal(size=(200, 6)) + groups[:, None]
    dist = ((embeddings[:, None] - embeddings) ** 2).mean(axis=-1)
    matrix = np.exp(-0.3 * dist)
    variance = matrix[~np.eye(200, dtype=bool)].var()
    alignment = np.corrcoef(matrix.ravel(), (groups[:, None] == groups).ravel())[0, 1]

    def series(labels, values):
        return [
            {"label": str(label), "value": float(value)}
            for label, value in zip(labels, values, strict=True)
        ]

    circuits = []
    for slug, name, gates, depth in (("angle", "Angle map", 4, 1), ("zz", "ZZ map", 8, 4)):
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="460" height="112" viewBox="0 0 460 112" '
            f'role="img" aria-label="{name} placeholder illustration">'
            '<rect width="460" height="112" rx="12" fill="#f1f5fa"/>'
            f'<text x="16" y="28" fill="#14283b" font-family="sans-serif">Placeholder · {name}</text>'
            '<path d="M16 59h425m-425 31h425" stroke="#26465f"/>'
            '<rect x="130" y="47" width="68" height="25" fill="#bae5d9" stroke="#26465f"/>'
            '<text x="147" y="64" font-family="sans-serif">Rᵧ(θ)</text></svg>\n'
        )
        path = directory / "circuits" / f"{slug}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg)
        circuits.append(
            {
                "name": name,
                "svg_url": f"/api/circuit-assets/{slug}.svg",
                "width": 4,
                "gates": gates,
                "depth": depth,
                "transpiled_depth": depth + 1,
            }
        )
    datasets = [
        {
            "id": name,
            "name": title,
            "source": "Synthetic preview",
            "splits": [
                {"window": window, "rows": count, "fraud": int(rng.integers(8, 45))}
                for window, count in (("Train", 12000), ("Validation", 4000), ("Test", 4000))
            ],
        }
        for name, title in (("sample-ulb", "Card transactions"), ("sample-scale", "Scale preview"))
    ]
    data = {
        ArtifactKind.DATASETS: {"datasets": datasets},
        ArtifactKind.REDUCTION: {
            "schema_id": "sample-v1",
            "reducer": "PCA preview",
            "input_dimensions": 30,
            "output_dimensions": 4,
            "features": ["angle_1", "angle_2", "angle_3", "angle_4"],
            "explained_variance": [0.31, 0.21, 0.12, 0.07],
        },
        ArtifactKind.COMPARISON: {
            "metrics": metrics,
            "pr_curve": pr,
            "roc_curve": [{"x": float(x), "y": float(x**0.4)} for x in grid],
            "routing": [{"x": float(x), "y": float(0.51 + 0.27 * x**0.6)} for x in grid],
            "costs": [
                {"policy": "Classical", "expected_cost_inr": 34000},
                {"policy": "Cascade", "expected_cost_inr": 33000},
            ],
        },
        ArtifactKind.ABLATIONS: {
            "rows": [
                {
                    "policy": "Disable quantum",
                    "pr_auc_delta": -0.01,
                    "routed_share": 0,
                    "interval": "Illustrative paired block interval",
                }
            ],
        },
        ArtifactKind.CIRCUITS: {"circuits": circuits},
        ArtifactKind.KERNEL: {
            "matrix": matrix.round(3).tolist(),
            "classes": groups.tolist(),
            "variance": round(float(variance), 8),
            "alignment": round(float(alignment), 8),
            "concentration": series(range(4, 11), np.linspace(0.09, 0.01, 7)),
        },
        ArtifactKind.HQNN: {
            "loss": series(range(1, 7), np.linspace(0.8, 0.4, 6)),
            "gradient_variance": series(("Layer 1", "Layer 2", "Layer 3"), [0.07, 0.04, 0.02]),
        },
        ArtifactKind.NOISE: {
            "ideal_recall": 0.76,
            "shot_recall": series((128, 512, 1024, 4096), [0.62, 0.69, 0.71, 0.74]),
        },
    }
    for kind, payload in data.items():
        model = ARTIFACTS[kind].model_validate(
            {
                "mode": "stub",
                "generated_by": "needlecast-ml make-sample-artifacts",
                "seed": seed,
                "schema_version": "1",
                "run_id": "sample-bundle",
                "dataset_id": "sample-ulb",
                "split_id": "sample-chronological",
                "created_at": "2000-01-01T00:00:00Z",
                "disclaimer": DISCLAIMER,
                "data": payload,
            }
        )
        write_json(directory / f"{kind}.json", model.model_dump(mode="json"))


def validate_samples(directory: Path, schema_dir: Path) -> None:
    for kind, contract in ARTIFACTS.items():
        data = json.loads((directory / f"{kind}.json").read_text())
        schema = json.loads((schema_dir / f"{kind}.json").read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(data)
        model = contract.model_validate(data)
        if model.mode != "stub" or model.disclaimer != DISCLAIMER:
            raise ValueError(f"{kind}: sample artifacts require the placeholder label.")
    for circuit in (
        ARTIFACTS[ArtifactKind.CIRCUITS]
        .model_validate_json((directory / "circuits.json").read_bytes())
        .data.circuits
    ):
        prefix = "/api/circuit-assets/"
        name = circuit.svg_url.removeprefix(prefix)
        if circuit.svg_url != prefix + name or name != Path(name).name or not name.endswith(".svg"):
            raise ValueError("Each sample circuit must refer to a generated SVG filename.")
        root = ElementTree.parse(directory / "circuits" / name).getroot()
        if (
            root.tag != "{http://www.w3.org/2000/svg}svg"
            or "placeholder" not in root.get("aria-label", "").lower()
        ):
            raise ValueError(f"{name}: sample circuit requires a placeholder label.")
