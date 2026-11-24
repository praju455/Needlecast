"""Write the deterministic M00 OpenAPI contract for the generated frontend types."""

import json
from pathlib import Path

from backend.app.config import ROOT
from backend.app.main import app


def export(path: Path) -> None:
    path.write_text(json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    export(ROOT / "backend" / "openapi.json")
