"""CLI for Stage 05b test holdout scoring."""

from __future__ import annotations

from pathlib import Path

import click

from src.stage05b_test_holdout.test_runner import run_holdout_score


@click.group()
def cli() -> None:
    """Stage 05b holdout scoring commands."""


@cli.command("score")
@click.option("--final-model", "final_model_dir", type=click.Path(exists=True, path_type=Path), required=True)
@click.option(
    "--policy",
    type=click.Choice(["train_only", "train_plus_val"]),
    required=True,
)
@click.option("--run-id", type=str, required=True)
@click.option("--bo-call", type=int, default=None, help="Optional BO call id for per-call evaluation output.")
@click.option("--allow-rerun", is_flag=True, default=False)
def score_cmd(final_model_dir: Path, policy: str, run_id: str, bo_call: int | None, allow_rerun: bool) -> None:
    """Run one-shot final test scoring."""
    metrics_json = run_holdout_score(
        final_model_dir=final_model_dir,
        policy=policy,
        run_id=run_id,
        allow_rerun=allow_rerun,
        bo_call=bo_call,
    )
    click.echo(f"Holdout scoring complete: {metrics_json}")


if __name__ == "__main__":
    cli()

