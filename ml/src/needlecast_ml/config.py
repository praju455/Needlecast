"""Configure M00 paths, random seeds, currency, and quantum width limits."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ARTIFACT_ROOT = Path(__file__).resolve().parents[2] / "artifacts"


class Settings(BaseSettings):
    """Validated settings shared by the command line and the ML utilities."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    data_dir: Path = Path("datasets")
    artifact_dir: Path = ARTIFACT_ROOT / "sample"
    seed: int = Field(default=42, ge=0)
    qubit_cap: int = Field(default=12, ge=1, le=12)
    currency: str = "INR"
