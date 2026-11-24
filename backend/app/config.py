"""Load M00 service configuration and the workspace version."""

from pathlib import Path
from typing import Literal

from needlecast_ml.config import Settings

ROOT = Path(__file__).resolve().parents[2]
VERSION = (ROOT / "VERSION").read_text().strip()


class ApiSettings(Settings):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    allowed_origins: list[str] = []
