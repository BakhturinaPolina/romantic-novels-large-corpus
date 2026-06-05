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
@click.option(
    "--embedding-model",
    default=None,
    type=str,
    help="Optional single-model run override (for quick perf/smoke runs).",
)
@click.option(
    "--paths-config",
    default=None,
    type=click.Path(exists=True, path_type=Path),
    help="Optional paths.yaml override (defaults to train config paths_config).",
)
def tune(
    config: Path,
    run_id: str | None,
    embedding_model: str | None,
    paths_config: Path | None,
) -> None:
    """Run BERTopic tuning over embedding models."""
    rid = run_id or uuid.uuid4().hex[:12]
    embedding_models = [embedding_model] if embedding_model else None
    trials_csv = run_tuning(config, rid, embedding_models_override=embedding_models, paths_config=paths_config)
    click.echo(f"Stage03 tuning complete. trials.csv: {trials_csv}")


@cli.command("sample")
@click.option("--train-csv", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--val-csv", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--metadata-train", default=None, type=click.Path(path_type=Path))
@click.option("--metadata-val", default=None, type=click.Path(path_type=Path))
@click.option("--out-dir", default=Path("data/stage03_samples"), type=click.Path(path_type=Path))
@click.option("--seed", default=42, type=int)
@click.option("--train-target", default=500_000, type=int)
@click.option("--val-target", default=100_000, type=int)
@click.option("--progress-every", default=5_000_000, type=int)
@click.option("--resume", is_flag=True, default=False)
def sample(
    train_csv: Path,
    val_csv: Path,
    metadata_train: Path | None,
    metadata_val: Path | None,
    out_dir: Path,
    seed: int,
    train_target: int,
    val_target: int,
    progress_every: int,
    resume: bool,
) -> None:
    """Select stratified fit/eval row indices into the full corpus for Stage 03."""
    import json

    import numpy as np

    from src.stage03_train.make_fit_sample import (
        _checkpoint_pass1_path,
        load_metadata_map,
        select_stratified_indices,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    progress_every = max(0, progress_every)
    fit_indices, train_manifest, n_train = select_stratified_indices(
        train_csv,
        target_rows=train_target,
        seed=seed,
        metadata_map=load_metadata_map(metadata_train),
        index_offset=0,
        progress_every=progress_every,
        checkpoint_dir=out_dir,
        checkpoint_split="train",
        resume=resume,
    )
    eval_indices, val_manifest, n_val = select_stratified_indices(
        val_csv,
        target_rows=val_target,
        seed=seed + 1,
        metadata_map=load_metadata_map(metadata_val),
        index_offset=n_train,
        min_rows_per_book=5,
        max_rows_per_book=40,
        max_rows_per_author=300,
        progress_every=progress_every,
        checkpoint_dir=out_dir,
        checkpoint_split="val",
        resume=resume,
    )
    fit_path = out_dir / f"fit_indices_seed{seed}.npy"
    eval_path = out_dir / f"eval_indices_seed{seed}.npy"
    np.save(fit_path, fit_indices)
    np.save(eval_path, eval_indices)
    manifest_path = out_dir / f"sample_manifest_seed{seed}.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "seed": seed,
                "n_train_clean": int(n_train),
                "n_val_clean": int(n_val),
                "n_total_clean": int(n_train + n_val),
                "fit_indices_file": str(fit_path),
                "eval_indices_file": str(eval_path),
                "fit_partition": "train",
                "eval_partition": "val",
                "progress_every": progress_every,
                "pass1_checkpoints": {
                    "train": str(_checkpoint_pass1_path(out_dir, seed, "train")),
                    "val": str(_checkpoint_pass1_path(out_dir, seed, "val")),
                },
                "train": train_manifest,
                "validation": val_manifest,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    click.echo(f"Stage03 sampling complete. manifest: {manifest_path}")


if __name__ == "__main__":
    cli()

