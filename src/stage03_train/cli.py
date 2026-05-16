"""CLI for Stage 03 training/tuning."""

from __future__ import annotations

import uuid
from pathlib import Path

import click

from src.stage03_train.tune import run_tuning


@click.group()
def cli() -> None:
    """Stage 03 train/eval tuning commands."""


@cli.command("tune")
@click.option("--config", default="configs/train.yaml", type=click.Path(exists=True, path_type=Path))
@click.option("--run-id", default=None, type=str)
def tune(config: Path, run_id: str | None) -> None:
    """Run BERTopic tuning over embedding models."""
    rid = run_id or uuid.uuid4().hex[:12]
    trials_csv = run_tuning(config, rid)
    click.echo(f"Stage03 tuning complete. trials.csv: {trials_csv}")


if __name__ == "__main__":
    cli()

