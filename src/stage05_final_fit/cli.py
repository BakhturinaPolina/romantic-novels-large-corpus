"""CLI for Stage 05 final fit."""

from __future__ import annotations

from pathlib import Path

import click


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
    from src.stage05_final_fit.final_fit import run_final_fit

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
@click.option(
    "--stability-runs",
    type=int,
    default=0,
    show_default=True,
    help="If >0, refit each call N times with umap_random_state=seed+i and gate on topic std.",
)
@click.option(
    "--stability-tolerance",
    type=float,
    default=3.0,
    show_default=True,
    help="Max allowed n_topics std across stability runs.",
)
@click.option(
    "--reduce-outliers",
    is_flag=True,
    default=False,
    help="After fit, run reduce_outliers and export tables under outliers_reduced/.",
)
@click.option(
    "--save-model",
    is_flag=True,
    default=False,
    help="Save BERTopic native artifact under call_<N>/model_compare/ for Stage05b holdout.",
)
@click.option(
    "--force-refit",
    is_flag=True,
    default=False,
    help="Refit even when metrics.json exists (recompute tables/metrics).",
)
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
    stability_runs: int,
    stability_tolerance: float,
    reduce_outliers: bool,
    save_model: bool,
    force_refit: bool,
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
        stability_runs=stability_runs,
        stability_tolerance=stability_tolerance,
        reduce_outliers=reduce_outliers,
        save_model=save_model,
        force_refit=force_refit,
    )
    click.echo(f"compare outputs: {out}")


@cli.command("infer-corpus")
@click.option(
    "--model-dir",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Compare-fit call directory containing model_compare/ (or model_compare itself).",
)
@click.option("--run-id", type=str, required=True)
@click.option(
    "--paths-config",
    type=click.Path(exists=True, path_type=Path),
    default="configs/paths_stage03_fit_v3.yaml",
    show_default=True,
)
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    default="configs/train_v4_l12_final_call73.yaml",
    show_default=True,
)
@click.option(
    "--splits",
    type=str,
    default="train,val,test",
    show_default=True,
    help="Comma-separated splits to transform.",
)
@click.option("--batch-size", type=int, default=8192, show_default=True)
@click.option("--chunk-size", type=int, default=50_000, show_default=True)
@click.option("--output-dir", type=click.Path(path_type=Path), default=None)
def infer_corpus(
    model_dir: Path,
    run_id: str,
    paths_config: Path,
    config_path: Path,
    splits: str,
    batch_size: int,
    chunk_size: int,
    output_dir: Path | None,
) -> None:
    """Chunked full-corpus transform (train + val + test) to parquet."""
    from src.stage05_final_fit.full_corpus_infer import run_full_corpus_infer

    split_tuple = tuple(s.strip() for s in splits.split(",") if s.strip())
    out = run_full_corpus_infer(
        model_dir=model_dir,
        run_id=run_id,
        paths_config=paths_config,
        train_config=config_path,
        splits=split_tuple,
        batch_size=batch_size,
        chunk_size=chunk_size,
        output_dir=output_dir,
    )
    click.echo(f"full-corpus infer outputs: {out}")


@cli.command("pareto")
@click.option(
    "--selection-config",
    type=click.Path(exists=True, path_type=Path),
    default="configs/selection_notebooks.yaml",
    show_default=True,
)
@click.option(
    "--paths-config",
    type=click.Path(exists=True, path_type=Path),
    default="configs/paths_stage03_fit_v3.yaml",
    show_default=True,
)
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    default="configs/train_v3.yaml",
    show_default=True,
)
@click.option("--stability-runs", type=int, default=0, show_default=True)
@click.option("--stability-tolerance", type=float, default=3.0, show_default=True)
@click.option("--reduce-outliers", is_flag=True, default=False)
@click.option("--force-refit", is_flag=True, default=False)
@click.option("--skip-holdout", is_flag=True, default=False)
@click.option("--allow-rerun", is_flag=True, default=False)
def pareto(
    selection_config: Path,
    paths_config: Path,
    config_path: Path,
    stability_runs: int,
    stability_tolerance: float,
    reduce_outliers: bool,
    force_refit: bool,
    skip_holdout: bool,
    allow_rerun: bool,
) -> None:
    """Compare-fit pareto notebook top-k models and run Stage05b test holdout."""
    from src.stage05_final_fit.pareto_pipeline import run_pareto_stage05

    result = run_pareto_stage05(
        selection_config=selection_config,
        paths_config=paths_config,
        train_config=config_path,
        stability_runs=stability_runs,
        stability_tolerance=stability_tolerance,
        reduce_outliers=reduce_outliers,
        force_refit=force_refit,
        run_holdout=not skip_holdout,
        allow_rerun=allow_rerun,
    )
    click.echo(f"bo_calls: {result['bo_calls']}")
    click.echo(f"compare_root: {result['compare_root']}")
    if not skip_holdout:
        click.echo(f"holdout_summary: {result['holdout_summary_csv']}")


if __name__ == "__main__":
    cli()

