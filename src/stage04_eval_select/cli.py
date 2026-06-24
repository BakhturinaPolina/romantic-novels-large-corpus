"""CLI for Stage 04 eval-select (Pareto then weighted ranking)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import click
import pandas as pd

from src.common.config import load_config, resolve_path
from src.stage04_eval_select.pareto_analysis import analyze_pareto_efficiency
from src.stage04_eval_select.weighted_score import apply_weighted_score


def _json_safe(value: object) -> object:
    """Convert pandas/numpy missing values to JSON-null."""
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


def _normalize_for_pareto(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ("coherence_c_v", "topic_diversity"):
        min_v = float(out[col].min())
        max_v = float(out[col].max())
        if max_v > min_v:
            out[f"{col}_norm"] = (out[col] - min_v) / (max_v - min_v)
        else:
            out[f"{col}_norm"] = 0.0
    return out


@click.group()
def cli() -> None:
    """Stage 04 eval-select commands."""


@cli.command("select")
@click.option("--trials", "trials_csv", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--config", type=click.Path(exists=True, path_type=Path), default="configs/eval_select.yaml")
@click.option("--run-id", type=str, required=True)
def select_cmd(trials_csv: Path, config: Path, run_id: str) -> None:
    """Select one winning trial from trials.csv."""
    cfg = load_config(config)
    paths_cfg = load_config(Path("configs/paths.yaml"))
    selection_dir = resolve_path(Path(paths_cfg["outputs"]["selection"])) / run_id
    selection_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(trials_csv)

    min_n_topics = int(cfg["selection"].get("min_n_topics", 0))
    if min_n_topics > 0 and "n_topics" in df.columns:
        before = len(df)
        df = df[df["n_topics"].fillna(0) >= min_n_topics].copy()
        click.echo(
            f"Topic-count floor: kept {len(df)}/{before} trials "
            f"(min_n_topics={min_n_topics})"
        )
        if df.empty:
            raise ValueError(
                f"No trials meet min_n_topics={min_n_topics}. "
                "Lower the floor in eval_select.yaml or revisit the Stage 03 search space."
            )

    max_n_topics = int(cfg["selection"].get("max_n_topics", 0))
    if max_n_topics > 0 and "n_topics" in df.columns:
        before = len(df)
        df = df[df["n_topics"].fillna(0) <= max_n_topics].copy()
        click.echo(
            f"Topic-count ceiling: kept {len(df)}/{before} trials "
            f"(max_n_topics={max_n_topics})"
        )

    max_outlier_rate = float(cfg["selection"].get("max_outlier_rate", 0))
    if max_outlier_rate > 0 and "outlier_rate" in df.columns:
        before = len(df)
        df = df[df["outlier_rate"].fillna(1.0) <= max_outlier_rate].copy()
        click.echo(
            f"Outlier-rate filter (max={max_outlier_rate}): kept {len(df)}/{before} trials"
        )

    max_largest_share = float(cfg["selection"].get("max_largest_topic_share", 0))
    if max_largest_share > 0 and "largest_topic_share" in df.columns:
        before = len(df)
        df = df[df["largest_topic_share"].fillna(1.0) <= max_largest_share].copy()
        click.echo(
            f"Largest-topic-share filter (max={max_largest_share}): "
            f"kept {len(df)}/{before} trials"
        )

    max_n_topics_std = float(cfg["selection"].get("max_n_topics_std", 0))
    require_stability = bool(cfg["selection"].get("require_topic_stability", False))
    if require_stability and "topic_stability_pass" in df.columns:
        before = len(df)
        df = df[df["topic_stability_pass"].fillna(True).astype(bool)].copy()
        click.echo(
            f"Topic stability pass filter: kept {len(df)}/{before} trials"
        )
    if max_n_topics_std > 0 and "n_topics_std" in df.columns:
        before = len(df)
        std_ok = df["n_topics_std"].isna() | (df["n_topics_std"] <= max_n_topics_std)
        df = df[std_ok].copy()
        click.echo(
            f"Topic-count std filter (max={max_n_topics_std}): kept {len(df)}/{before} trials"
        )
    if df.empty:
        raise ValueError(
            "No trials remained after topic stability filters. "
            "Relax eval_select.yaml selection.max_n_topics_std or require_topic_stability."
        )

    df = _normalize_for_pareto(df)
    df_p = df.rename(
        columns={
            "coherence_c_v_norm": "Coherence_norm",
            "topic_diversity_norm": "Topic_Diversity_norm",
            "embedding_model": "Embeddings_Model",
        }
    )
    df_p = analyze_pareto_efficiency(
        df_p,
        metrics=["Coherence_norm", "Topic_Diversity_norm"],
        per_model=False,
    )
    pareto_mask = df_p["Pareto_Efficient_All"] if cfg["selection"]["pareto_first"] else pd.Series([True] * len(df_p))
    candidates = df_p[pareto_mask].copy()

    w = cfg["weights"]
    candidates = apply_weighted_score(
        candidates,
        w_coherence=float(w["coherence"]),
        w_diversity=float(w["diversity"]),
        w_outlier=float(w["outlier"]),
        w_stability=float(w["stability"]),
        w_topic_count_floor=float(w.get("topic_count_floor", 0.0)),
    )
    candidates = candidates.sort_values("weighted_score", ascending=False).reset_index(drop=True)

    top_k = int(cfg["selection"]["top_k"])
    top_k_df = candidates.head(top_k)
    top_k_path = selection_dir / "top_k.csv"
    top_k_df.to_csv(top_k_path, index=False)

    if top_k_df.empty:
        raise ValueError("No candidates remained after selection.")
    winner = top_k_df.iloc[0].to_dict()
    hyper = {k: v for k, v in winner.items() if "__" in k}
    embedding_model = winner.get("embedding_model") or winner.get("Embeddings_Model")
    winner_payload = {
        "run_id": run_id,
        "selected_at": datetime.utcnow().isoformat() + "Z",
        "trial_id": winner["trial_id"],
        "embedding_model": embedding_model,
        "selection_metrics": {
            "coherence_c_v": _json_safe(winner.get("coherence_c_v")),
            "topic_diversity": _json_safe(winner.get("topic_diversity")),
            "outlier_rate": _json_safe(winner.get("outlier_rate")),
            "stability_score": _json_safe(winner.get("stability_score")),
            "weighted_score": _json_safe(winner.get("weighted_score")),
            "n_topics": _json_safe(winner.get("n_topics")),
            "bo_call": _json_safe(winner.get("bo_call")),
        },
        "hyperparameters": hyper,
        "train_csv": winner.get("train_csv"),
        "eval_csv": winner.get("eval_csv"),
        "test_csv": winner.get("test_csv"),
    }
    winner_path = selection_dir / "winner_config.json"
    with open(winner_path, "w", encoding="utf-8") as f:
        json.dump(winner_payload, f, indent=2)

    report_path = selection_dir / "selection_report.md"
    report_path.write_text(
        "\n".join(
            [
                f"# Selection Report ({run_id})",
                "",
                f"- Trials input: `{trials_csv}`",
                f"- Pareto-first: `{cfg['selection']['pareto_first']}`",
                f"- Top-K saved: `{top_k_path}`",
                f"- Winner config: `{winner_path}`",
                "",
                "## Winner",
                f"- Trial ID: `{winner_payload['trial_id']}`",
                f"- Embedding: `{winner_payload['embedding_model']}`",
                f"- Weighted score: `{winner_payload['selection_metrics']['weighted_score']}`",
            ]
        ),
        encoding="utf-8",
    )
    click.echo(f"Selection complete. Winner: {winner_path}")


if __name__ == "__main__":
    cli()

