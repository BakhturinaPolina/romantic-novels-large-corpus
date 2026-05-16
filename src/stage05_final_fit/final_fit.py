"""Final fit stage: produce train-only and train+val model artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.common.config import load_config, resolve_path
from src.stage05_retraining.retrain_models import retrain_single_model


def load_winner_config(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _to_model_config(winner: dict[str, Any]) -> dict[str, Any]:
    return {
        "embedding_model": winner["embedding_model"],
        "pareto_rank": 1,
        "hyperparameters": winner["hyperparameters"],
        "coherence": winner.get("selection_metrics", {}).get("coherence_c_v", 0.0),
        "topic_diversity": winner.get("selection_metrics", {}).get("topic_diversity", 0.0),
        "combined_score": winner.get("selection_metrics", {}).get("weighted_score", 0.0),
        "iteration": 0,
    }


def _merge_train_eval(train_csv: Path, eval_csv: Path, out_csv: Path) -> Path:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    train_df = pd.read_csv(train_csv)
    eval_df = pd.read_csv(eval_csv)
    merged = pd.concat([train_df, eval_df], ignore_index=True)
    merged.to_csv(out_csv, index=False)
    return out_csv


def run_final_fit(winner_config: Path, policy: str = "both") -> dict[str, Path]:
    winner = load_winner_config(winner_config)
    model_config = _to_model_config(winner)
    run_id = winner["run_id"]

    paths_cfg = load_config(Path("configs/paths.yaml"))
    output_root = resolve_path(Path(paths_cfg["outputs"]["final_models"])) / run_id
    octis_root = resolve_path(Path(paths_cfg["inputs"]["octis_dataset"])) / f"{run_id}_finalfit"
    output_root.mkdir(parents=True, exist_ok=True)
    octis_root.mkdir(parents=True, exist_ok=True)

    train_csv = resolve_path(Path(winner["train_csv"]))
    eval_csv = resolve_path(Path(winner["eval_csv"]))
    outputs: dict[str, Path] = {}

    if policy in {"both", "train_only"}:
        train_only_dir = output_root / "train_only"
        train_only_dir.mkdir(parents=True, exist_ok=True)
        ok = retrain_single_model(
            model_config=model_config,
            dataset_path=train_csv,
            octis_dataset_path=octis_root / "train_only",
            output_dir=train_only_dir,
        )
        if not ok:
            raise RuntimeError("Final fit train_only failed.")
        outputs["train_only"] = train_only_dir

    if policy in {"both", "train_plus_val"}:
        merged_csv = output_root / "tmp_train_plus_val.csv"
        _merge_train_eval(train_csv, eval_csv, merged_csv)
        train_plus_val_dir = output_root / "train_plus_val"
        train_plus_val_dir.mkdir(parents=True, exist_ok=True)
        ok = retrain_single_model(
            model_config=model_config,
            dataset_path=merged_csv,
            octis_dataset_path=octis_root / "train_plus_val",
            output_dir=train_plus_val_dir,
        )
        if not ok:
            raise RuntimeError("Final fit train_plus_val failed.")
        outputs["train_plus_val"] = train_plus_val_dir

    manifest = output_root / "final_fit_manifest.json"
    with open(manifest, "w", encoding="utf-8") as f:
        json.dump(
            {
                "run_id": run_id,
                "policy": policy,
                "winner_config": str(winner_config),
                "outputs": {k: str(v) for k, v in outputs.items()},
            },
            f,
            indent=2,
        )
    return outputs

