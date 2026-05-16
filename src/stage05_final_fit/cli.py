"""CLI for Stage 05 final fit."""

from __future__ import annotations

from pathlib import Path

import click

from src.stage05_final_fit.final_fit import run_final_fit


@click.group()
def cli() -> None:
    """Stage 05 final fit commands."""


@cli.command("fit")
@click.option("--winner", "winner_config", type=click.Path(exists=True, path_type=Path), required=True)
@click.option(
    "--policy",
    type=click.Choice(["both", "train_only", "train_plus_val"]),
    default="both",
    show_default=True,
)
def fit(winner_config: Path, policy: str) -> None:
    """Refit selected winner with final-fit policies."""
    outputs = run_final_fit(winner_config=winner_config, policy=policy)
    for k, v in outputs.items():
        click.echo(f"{k}: {v}")


if __name__ == "__main__":
    cli()

