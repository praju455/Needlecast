"""Expose M00 fixture generation and interfaces for planned experiment runners."""

from pathlib import Path

import typer

from needlecast_ml.config import ARTIFACT_ROOT, Settings
from needlecast_ml.evaluation.sample import make_samples, validate_samples, write_schemas

app = typer.Typer(no_args_is_help=True)


@app.command()
def make_sample_artifacts(directory: Path | None = None, seed: int | None = None) -> None:
    settings = Settings()
    destination = directory if directory is not None else settings.artifact_dir
    make_samples(destination, seed if seed is not None else settings.seed)
    typer.echo(f"Generated eight seeded placeholder JSON artifacts in {destination}")


@app.command()
def export_schemas(directory: Path = ARTIFACT_ROOT / "schemas") -> None:
    write_schemas(directory)


@app.command()
def validate_artifacts(directory: Path | None = None) -> None:
    validate_samples(
        directory if directory is not None else Settings().artifact_dir, ARTIFACT_ROOT / "schemas"
    )
    typer.echo("Validated eight placeholder artifact schemas")


def _planned(milestone: str) -> None:
    typer.echo(f"Experiment runner is planned for {milestone}.", err=True)
    raise typer.Exit(code=2)


@app.command()
def run_baselines() -> None:
    _planned("M02")


@app.command()
def run_qsvm() -> None:
    _planned("M04")


@app.command()
def run_hqnn() -> None:
    _planned("M06")


@app.command()
def run_cascade() -> None:
    _planned("M07")


if __name__ == "__main__":
    app()
