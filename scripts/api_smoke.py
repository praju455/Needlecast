"""Check the running M00 backend over HTTP and print a compact evidence summary."""

import argparse
import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen

BASE = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


def fetch_http(path, payload=None):
    request = Request(
        BASE + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=15) as response:
        return response.status, json.load(response)


def smoke(fetch):
    for path in (
        "/health",
        "/api/models/comparison",
        "/api/datasets",
        "/api/pipeline/reduction",
        "/api/models/ablations",
        "/api/diagnostics/circuits",
        "/api/diagnostics/kernel",
        "/api/diagnostics/hqnn",
        "/api/diagnostics/noise",
    ):
        status, body = fetch(path)
        assert status == 200 and body["mode"] == "stub"
        print(path, status, body["mode"], body.get("status", body.get("run_id")))
    routes = {}
    for amount in range(24):
        status, body = fetch(
            "/api/score",
            {"feature_schema_id": "sample-v1", "transaction": {"amount": amount}, "mode": "stub"},
        )
        assert status == 200 and body["mode"] == "stub"
        route = body["route"]
        if route not in routes:
            quantum = body["stages"][1]["invoked"]
            assert quantum == (0.35 <= body["classical"]["score"] <= 0.65)
            routes[route] = quantum
            print(
                "/api/score",
                status,
                json.dumps(
                    {
                        "mode": body["mode"],
                        "amount": amount,
                        "classical": body["classical"]["score"],
                        "route": route,
                        "quantum_invoked": quantum,
                    }
                ),
            )
        if len(routes) == 2:
            break
    assert routes == {"classical_only": False, "quantum_rescored": True}
    status, job = fetch("/api/jobs/run", {"preset": "sample-comparison", "mode": "stub"})
    assert status == 202
    status, result = fetch(job["status_url"])
    assert status == 200 and result["status"] == "succeeded" and result["mode"] == "stub"
    print("/api/jobs", status, result["status"], result["mode"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--in-process",
        action="store_true",
        help="Use the ASGI test transport without a server socket.",
    )
    args = parser.parse_args()
    if args.in_process:
        from fastapi.testclient import TestClient

        from backend.app.main import app

        with TestClient(app) as client:

            def fetch_local(path, payload=None):
                result = client.get(path) if payload is None else client.post(path, json=payload)
                return result.status_code, result.json()

            print("Transport: in-process FastAPI TestClient")
            smoke(fetch_local)
    else:
        try:
            smoke(fetch_http)
        except URLError as error:
            raise SystemExit(f"Unable to reach the configured backend: {error.reason}") from None


if __name__ == "__main__":
    main()
