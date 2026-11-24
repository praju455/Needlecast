import json

from fastapi.testclient import TestClient
from needlecast_ml.evaluation.sample import make_samples

from backend.app.config import ApiSettings
from backend.app.main import create_app
from backend.app.schemas.api import ScoreResponse
from backend.app.services.scoring_service import LOWER, UPPER
from backend.scripts.export_openapi import export


def test_all_artifact_routes(tmp_path):
    make_samples(tmp_path, 42)
    client = TestClient(create_app(ApiSettings(artifact_dir=tmp_path)))
    paths = (
        "/api/datasets",
        "/api/pipeline/reduction",
        "/api/models/comparison",
        "/api/models/ablations",
        "/api/diagnostics/circuits",
        "/api/diagnostics/kernel",
        "/api/diagnostics/hqnn",
        "/api/diagnostics/noise",
    )
    assert client.get("/health").json()["status"] == "ok"
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200
        body = response.json()
        assert body["mode"] == "stub" and body["disclaimer"] and body["schema_version"] == "1"
        assert client.get(path, params={"run_id": body["run_id"]}).status_code == 200
        assert client.get(path, params={"run_id": "missing"}).json()["code"] == "run_missing"
    svg = client.get("/api/circuit-assets/angle.svg")
    assert svg.status_code == 200 and svg.headers["content-type"] == "image/svg+xml"
    assert "Placeholder" in svg.text
    assert client.get("/api/circuit-assets/missing.svg").status_code == 404


def test_missing_and_validation_errors(tmp_path):
    client = TestClient(create_app(ApiSettings(artifact_dir=tmp_path)))
    missing = client.get("/api/datasets")
    assert missing.status_code == 404
    assert missing.json()["code"] == "artifact_missing"
    assert missing.json()["request_id"] == missing.headers["x-request-id"]
    assert client.post("/api/score", json={"transaction": {}}).status_code == 422
    live = {"feature_schema_id": "sample-v1", "transaction": {"amount": 1}, "mode": "live"}
    assert client.post("/api/score", json=live).status_code == 503
    invalid = {"feature_schema_id": "sample-v1", "transaction": {"amount": -1}}
    invalid_result = client.post("/api/score", json=invalid)
    assert invalid_result.status_code == 422
    assert invalid_result.json()["code"] == "feature_values_invalid"
    angles = dict.fromkeys(("angle_1", "angle_2", "angle_3", "angle_4"), 0.5)
    assert client.post("/api/score", json={**invalid, "transaction": angles}).status_code == 200


def test_score_routes_and_is_deterministic():
    client = TestClient(create_app())
    routes = set()
    for amount in range(24):
        body = {"feature_schema_id": "sample-v1", "transaction": {"amount": amount}, "mode": "stub"}
        response = client.post("/api/score", json=body)
        assert response.status_code == 200
        result = ScoreResponse.model_validate(response.json())
        assert result.stages[1].invoked == (LOWER <= result.classical.score <= UPPER)
        assert (result.quantum is not None) == result.stages[1].invoked
        assert client.post("/api/score", json=body).json()["final_score"] == result.final_score
        routes.add(result.route)
    assert routes == {"classical_only", "quantum_rescored"}


def test_in_band_timeout_preserves_the_classical_score(monkeypatch):
    app = create_app()

    def timeout(payload):
        raise TimeoutError

    monkeypatch.setattr(app.state.scorer, "_quantum_score", timeout)
    result = TestClient(app).post(
        "/api/score",
        json={
            "feature_schema_id": "sample-v1",
            "transaction": {"amount": 5},
            "mode": "stub",
        },
    )
    assert result.status_code == 200
    body = result.json()
    assert body["route"] == "classical_fallback"
    assert body["fallback_reason"] == "quantum_timeout"
    assert body["quantum"] is None and body["stages"][1]["invoked"] is True
    assert body["final_score"] == body["classical"]["score"]


def test_jobs_simulate_and_honor_retry_keys():
    client = TestClient(create_app())
    payload = {"preset": "sample-comparison", "mode": "stub"}
    headers = {"Idempotency-Key": "sample-1"}
    first = client.post("/api/jobs/run", json=payload, headers=headers)
    assert first.status_code == 202
    assert first.json()["status"] == "queued"
    result = client.get(first.json()["status_url"]).json()
    assert result["status"] == "succeeded" and result["progress"] == 100
    # The job links to a pre-existing fixture and creates no trained model or new run.
    assert result["result_url"] == "/api/models/comparison"
    assert result["published_run_id"] == "sample-bundle"
    assert client.post("/api/jobs/run", json=payload, headers=headers).json()["id"] == result["id"]
    assert (
        client.post(
            "/api/jobs/run", json={"preset": "sample-diagnostics"}, headers=headers
        ).status_code
        == 409
    )
    assert client.get("/api/jobs/missing").status_code == 404


def test_export_openapi(tmp_path):
    target = tmp_path / "openapi.json"
    export(target)
    data = json.loads(target.read_text())
    assert len(data["paths"]) == 13
    assert "ScoreResponse" in data["components"]["schemas"]
