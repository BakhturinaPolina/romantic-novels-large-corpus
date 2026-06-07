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


@cli.command("compare")
@click.option(
    "--trials",
    "trials_csv",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="trials_partial.csv with per-BO-call hyperparameters.",
)
@click.option(
    "--bo-calls",
    type=str,
    required=True,
    help="Comma-separated bo_call indices to refit, e.g. 10,64,57,59,62.",
)
@click.option("--run-id", type=str, required=True)
@click.option(
    "--paths-config",
    type=click.Path(exists=True, path_type=Path),
    default="configs/paths_stage03_fit.yaml",
    show_default=True,
)
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    default="configs/train.yaml",
    show_default=True,
    help="Train config providing embeddings_cache.overrides.",
)
@click.option(
    "--fit-indices",
    type=click.Path(path_type=Path),
    default=None,
    help="Stratified fit indices .npy (defaults to inputs.fit_indices_file).",
)
@click.option("--fit-max-docs", type=int, default=500_000, show_default=True)
@click.option(
    "--embedding-cache",
    type=click.Path(path_type=Path),
    default=None,
    help="Override embeddings .npy memmap (defaults to config override).",
)
@click.option("--seed", type=int, default=42, show_default=True)
def compare(
    trials_csv: Path,
    bo_calls: str,
    run_id: str,
    paths_config: Path,
    config_path: Path,
    fit_indices: Path | None,
    fit_max_docs: int,
    embedding_cache: Path | None,
    seed: int,
) -> None:
    """Refit top-N BO trials on the stratified sample and emit topic tables."""
    from src.stage05_final_fit.compare_fit import run_compare_fit

    calls = [int(c.strip()) for c in bo_calls.split(",") if c.strip()]
    out = run_compare_fit(
        trials_csv=trials_csv,
        bo_calls=calls,
        run_id=run_id,
        paths_config=paths_config,
        config_path=config_path,
        fit_indices=fit_indices,
        fit_max_docs=fit_max_docs,
        embedding_cache=embedding_cache,
        seed=seed,
    )
    click.echo(f"compare outputs: {out}")


if __name__ == "__main__":
    cli()

