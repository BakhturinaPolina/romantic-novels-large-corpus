#!/usr/bin/env python3
"""Assemble the single book-level analysis frame that every notebook reads.

One table, 16,000 rows, so that no notebook has to re-derive a variable and no two notebooks
can disagree about what `rating_shrunk` means. Columns fall into five blocks:

  topic_<id>       374 hard-assignment topic shares
  leaf_<id>        taxonomy leaf shares (conditional on interpretable mass)
  group_<name>     taxonomy main-group shares
  AX_*             theory axes: raw, `_z` z-scored, `_clr` on the CLR scale
  outcomes         quality (rating, shrunk rating, weight) and reach (log ratings)
  controls         log_pages, n_sentences, publication_year, genre_group, author_id, series_id

Two decisions are worth reading before using the frame.

*Shrinkage.* A book with 3 ratings averaging 4.9 is not better than one with 3,000 averaging
4.3, but a raw mean says it is. `rating_shrunk = (v*R + m*C)/(v + m)` pulls thin books toward
the corpus mean (C = 3.910) with m = 263, the corpus median rating count, so a book needs
about the median amount of evidence before it is trusted at face value. The raw rating is kept
alongside it; notebook 06 shows both.

*Two channels, not one.* Quality (star rating) and reach (rating count) correlate at only
r = 0.124 in this corpus. Collapsing them into "success" would average two nearly independent
things, so they stay separate throughout.

Usage:
  .venv/bin/python src/stage10_correlation_analysis/data_preparation/06_build_analysis_frame.py
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage10_correlation_analysis.analysis import compositional as comp  # noqa: E402
from src.stage10_correlation_analysis.analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_analysis_config,
)

LOGGER = logging.getLogger("stage10.analysis_frame")


def setup_logging(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    for handler in (
        logging.FileHandler(output_dir / "06_build_analysis_frame.log", mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ):
        handler.setFormatter(fmt)
        LOGGER.addHandler(handler)


# ---------------------------------------------------------------------------
# Blocks
# ---------------------------------------------------------------------------

def topic_share_wide(book_topic_counts: pd.DataFrame, prefix: str = "topic_") -> pd.DataFrame:
    """374 topic shares per book. Absent topics are genuine zeros, not missing data."""
    wide = (
        book_topic_counts
        .pivot(index="book_id", columns="topic_id", values="share")
        .fillna(0.0)
    )
    wide.columns = [f"{prefix}{int(c)}" for c in wide.columns]
    return wide


def build_outcomes(meta: pd.DataFrame, cfg) -> pd.DataFrame:
    """Both outcome channels, plus the reliability weight for the quality channel."""
    quality = cfg.section("outcomes", "quality")
    reach = cfg.section("outcomes", "reach")
    shrink = quality["shrinkage"]

    v = meta[shrink["count_column"]].astype(float)
    R = meta[quality["raw"]].astype(float)
    m = float(shrink["m_prior_count"])
    C = float(shrink["c_prior_mean"])

    out = pd.DataFrame(index=meta.index)
    out["avg_rating"] = R
    out["n_ratings"] = v
    out[quality["shrunk"]] = (v * R + m * C) / (v + m)
    # Reliability in [0, 1): the share of the shrunk estimate that comes from the book's own
    # ratings rather than from the prior. Used as the WLS weight.
    out["reliability"] = v / (v + m)
    out[reach["transformed"]] = np.log1p(v)
    out["n_text_reviews"] = meta.get("text_reviews_count_sum", pd.Series(np.nan, index=meta.index))

    r = float(np.corrcoef(out["avg_rating"], out[reach["transformed"]])[0, 1])
    LOGGER.info("Quality vs reach correlation: r = %.3f — kept as separate channels", r)
    LOGGER.info("Shrinkage: m = %.0f, C = %.3f; mean |shrunk - raw| = %.4f",
                m, C, float((out[quality["shrunk"]] - out["avg_rating"]).abs().mean()))
    thin = int((v < cfg.section("outcomes", "quality", "sensitivity_min_ratings")).sum())
    LOGGER.info("Books below the %d-rating sensitivity threshold: %s (%.1f%%)",
                cfg.section("outcomes", "quality", "sensitivity_min_ratings"),
                f"{thin:,}", 100 * thin / len(out))
    return out


def build_controls(meta: pd.DataFrame, book_totals: pd.DataFrame, cfg) -> pd.DataFrame:
    """Length, era, genre and the clustering keys."""
    out = pd.DataFrame(index=meta.index)
    pages = meta["num_pages_median"].astype(float)
    # Length enters as a log because the effect of 100 extra pages differs enormously between
    # a 150-page category romance and a 700-page saga.
    out["num_pages"] = pages
    out["log_pages"] = np.log1p(pages)
    out["publication_year"] = meta["publication_year"].astype(float)
    out["genre_group"] = meta["genre_group"].astype(str)
    out["year_bin"] = meta.get("year_bin", pd.Series("unknown", index=meta.index)).astype(str)
    out["author_id"] = meta["author_id"]
    out["author_name"] = meta.get("author_name")
    # `series_id` is a string key and is complete for every book, which makes it usable as an
    # alternative clustering level in the robustness notebook.
    out["series_id"] = meta["series_id"].astype(str)
    out["title"] = meta.get("title")
    out["split"] = book_totals["split"] if "split" in book_totals.columns else None

    totals = book_totals.set_index("book_id")
    out["n_sentences"] = totals["n_sentences"].reindex(out.index)
    out["n_chapters"] = totals["n_chapters"].reindex(out.index)
    out["log_sentences"] = np.log1p(out["n_sentences"])
    out["outlier_share"] = totals["outlier_share"].reindex(out.index)
    out["n_topics_present"] = totals["n_topics_present"].reindex(out.index)

    n_authors = out["author_id"].nunique()
    repeat = out["author_id"].value_counts()
    LOGGER.info(
        "Clustering: %s authors over %s books; %s authors have 2+ books (%s books). "
        "%s singleton authors make author fixed effects infeasible, hence cluster-robust SEs.",
        f"{n_authors:,}", f"{len(out):,}", f"{int((repeat >= 2).sum()):,}",
        f"{int(repeat[repeat >= 2].sum()):,}", f"{int((repeat == 1).sum()):,}",
    )
    LOGGER.info("Series: %s distinct series ids", f"{out['series_id'].nunique():,}")
    return out


def add_axis_transforms(
    axes: pd.DataFrame,
    *,
    epsilon: float,
) -> pd.DataFrame:
    """Raw axes plus two rescalings, because different questions need different scales.

    Raw values are interpretable ("2.4 percentage points more"). The `_z` version makes
    coefficients comparable across axes of different natural size. The `_clr` version is what
    the regressions use: shares are compositional, so a difference of shares is not a free
    quantity, and CLR maps the simplex to a space where a linear model is meaningful. Axes
    that already contain negative values (differences, products) cannot take a log, so they
    get z-scored only.
    """
    out = pd.DataFrame(index=axes.index)
    for col in axes.columns:
        values = axes[col].astype(float)
        out[col] = values
        out[f"{col}_z"] = comp.zscore(values)
        if (values >= 0).all():
            logged = np.log(values + epsilon)
            out[f"{col}_clr"] = comp.zscore(logged)
        else:
            # Signed axes get a symmetric log so that both tails are compressed equally.
            out[f"{col}_clr"] = comp.zscore(np.sign(values) * np.log1p(values.abs() / epsilon))
    return out


def add_hypothesis_log_ratios(
    leaf_shares: pd.DataFrame,
    cfg,
    epsilon: float,
) -> pd.DataFrame:
    """Explicit log-ratio forms for the balance hypotheses (H1, H4).

    "Love over sex" is a claim about a ratio, not a difference. A difference of shares depends
    on the overall level (0.20 - 0.05 and 0.35 - 0.20 are both 0.15 but mean different things),
    whereas log(love / sex) is scale-free and is the natural statistic for a composition.
    """
    out = pd.DataFrame(index=leaf_shares.index)
    for name, block in cfg.section("hypotheses").items():
        ratio = block.get("log_ratio")
        if not ratio:
            continue
        num_cols = [f"leaf_{leaf}" for leaf in ratio["numerator"] if f"leaf_{leaf}" in leaf_shares]
        den_cols = [f"leaf_{leaf}" for leaf in ratio["denominator"] if f"leaf_{leaf}" in leaf_shares]
        if not num_cols or not den_cols:
            LOGGER.warning("%s log-ratio skipped: numerator %d cols, denominator %d cols",
                           name, len(num_cols), len(den_cols))
            continue
        col = f"LR_{name}_{block['name'].lower().replace(' ', '_').replace('-', '_')}"
        out[col] = comp.log_ratio(leaf_shares, num_cols, den_cols, epsilon=epsilon)
        LOGGER.info("%s log-ratio %s = log((%s) / (%s)); mean %.3f, sd %.3f",
                    name, col, " + ".join(ratio["numerator"]), " + ".join(ratio["denominator"]),
                    out[col].mean(), out[col].std())
    return out


def apply_payoff_guard(
    leaf_inventory: pd.DataFrame,
    leaf_shares: pd.DataFrame,
    cfg,
) -> Tuple[Dict[str, object], pd.DataFrame]:
    """Check the 3.1 guard and record the verdict rather than deciding it silently.

    `AX_payoff_safety` is defined as 4.5 + 3.1. If the Stage09 re-run leaves 3.1 nearly empty,
    the axis is really just 4.5 and the fallback in the config applies. Because 4.6 is also
    H4's positive leg, the fallback also switches H4 to a residualised form so the shared
    component is stated instead of counted twice.
    """
    guard = cfg.section("guards", "payoff_safety_fallback")
    leaf = str(guard["trigger_leaf"])
    counts = dict(zip(leaf_inventory["leaf_id"].astype(str), leaf_inventory["n_topics"]))
    n = int(counts.get(leaf, 0))
    triggered = n < int(guard["min_topics"])

    verdict = {
        "trigger_leaf": leaf,
        "n_topics": n,
        "min_topics": int(guard["min_topics"]),
        "fallback_active": triggered,
        "fallback_leaves": ", ".join(str(x) for x in guard["fallback_leaves"]),
        "residualise_h4_on": ", ".join(str(x) for x in guard["residualise_h4_on"]),
    }

    extra = pd.DataFrame(index=leaf_shares.index)
    if not triggered:
        LOGGER.info("Guard not triggered: leaf %s has %d topics", leaf, n)
        return verdict, extra

    fallback_cols = [f"leaf_{x}" for x in guard["fallback_leaves"] if f"leaf_{x}" in leaf_shares]
    resid_cols = [f"leaf_{x}" for x in guard["residualise_h4_on"] if f"leaf_{x}" in leaf_shares]
    extra["AX_payoff_safety_fallback"] = leaf_shares[fallback_cols].sum(axis=1)

    # 4.6 is both H4's positive leg and part of the payoff fallback. Residualising it on 4.5
    # gives H4 the part of protective care that is *not* already commitment/reconciliation, so
    # the shared component is stated once rather than counted in both hypotheses.
    if "leaf_4.6" in leaf_shares and resid_cols:
        extra["AX_protective_care_resid"] = comp.residualise(
            leaf_shares["leaf_4.6"], leaf_shares[resid_cols]
        )
        r = float(leaf_shares["leaf_4.6"].corr(leaf_shares[resid_cols].sum(axis=1)))
        LOGGER.info("  4.6 correlates with %s at r = %.3f; residualised version added",
                    " + ".join(resid_cols), r)

    LOGGER.warning(
        "Guard TRIGGERED: leaf %s has %d topics (< %d). AX_payoff_safety rests on 4.5 alone, "
        "so AX_payoff_safety_fallback (%s) is added, and H4 also gets "
        "AX_protective_care_resid (4.6 residualised on %s) so the shared component is not "
        "double-counted.",
        leaf, n, guard["min_topics"], " + ".join(guard["fallback_leaves"]),
        ", ".join(guard["residualise_h4_on"]),
    )
    return verdict, extra


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=str, default=DEFAULT_CONFIG_PATH)
    ap.add_argument("--variant", type=str, default=None,
                    help="Axis mapping variant to place in the frame (default: config primary).")
    args = ap.parse_args()

    cfg = load_analysis_config(args.config)
    features_dir = cfg.output_path("book_features_dir")
    out_path = cfg.output_path("analysis_frame")
    setup_logging(features_dir)

    LOGGER.info("=" * 78)
    LOGGER.info("Stage10 analysis frame — run %s", cfg.run_id)
    LOGGER.info("=" * 78)
    started = time.perf_counter()

    counts_dir = cfg.output_path("hard_counts_dir")
    book_topic_counts = pd.read_parquet(counts_dir / "book_topic_counts.parquet")
    book_totals = pd.read_parquet(counts_dir / "book_totals.parquet")
    meta = pd.read_csv(cfg.input_path("books_meta", required=True)).set_index("book_id")
    leaf_abs = pd.read_parquet(features_dir / "book_leaf_shares_abs.parquet").set_index("book_id")
    leaf_cond = pd.read_parquet(features_dir / "book_leaf_shares_cond.parquet").set_index("book_id")
    group_shares = pd.read_parquet(features_dir / "book_group_shares.parquet").set_index("book_id")
    inventory = pd.read_parquet(features_dir / "leaf_topic_inventory.parquet")
    mapping_cov = pd.read_parquet(features_dir / "mapping_coverage.parquet").set_index("book_id")

    variant = args.variant or cfg.section("axes", "primary_variant")
    axes = pd.read_parquet(features_dir / f"book_axes_{variant}.parquet").set_index("book_id")
    LOGGER.info("Using the %r axis mapping variant (%d axes)", variant, axes.shape[1])

    # Everything is keyed on the books that have both topic counts and metadata.
    book_ids = sorted(set(book_totals["book_id"]) & set(meta.index))
    LOGGER.info("Spine: %s books (topic counts %s, metadata %s)",
                f"{len(book_ids):,}", f"{len(book_totals):,}", f"{len(meta):,}")
    meta = meta.loc[book_ids]

    epsilon = comp.epsilon_from_counts(
        book_totals["n_sentences"],
        mode=cfg.section("compositional", "epsilon_mode"),
        fallback=float(cfg.section("compositional", "epsilon_fallback")),
    )
    LOGGER.info("Compositional epsilon = %.3e (half of one sentence at the median book length)", epsilon)

    topics = topic_share_wide(book_topic_counts).reindex(book_ids).fillna(0.0)
    LOGGER.info("Topic block: %d columns", topics.shape[1])
    comp.check_share_sums(topics, name="topic shares", tolerance=1e-6)

    leaf_cond = leaf_cond.reindex(book_ids).fillna(0.0)
    leaf_abs = leaf_abs.reindex(book_ids).fillna(0.0)
    leaf_block = leaf_cond.add_suffix("")            # conditional is the analysis default
    leaf_abs_block = leaf_abs.add_prefix("abs_")      # absolute kept for description
    LOGGER.info("Leaf block: %d conditional + %d absolute columns",
                leaf_block.shape[1], leaf_abs_block.shape[1])

    guard, guard_axes = apply_payoff_guard(inventory, leaf_cond, cfg)
    axes_all = pd.concat([axes.reindex(book_ids), guard_axes.reindex(book_ids)], axis=1)
    axis_block = add_axis_transforms(axes_all, epsilon=epsilon)
    LOGGER.info("Axis block: %d columns (raw + _z + _clr for %d axes)",
                axis_block.shape[1], axes_all.shape[1])

    ratio_block = add_hypothesis_log_ratios(leaf_cond, cfg, epsilon)
    outcomes = build_outcomes(meta, cfg)
    controls = build_controls(meta, book_totals, cfg)

    tier_col = cfg.tier_column
    tiers = meta[tier_col].astype(str)
    LOGGER.info("Tier sizes: %s", tiers.value_counts().reindex(cfg.tier_order).to_dict())

    # A book with no interpretable sentence has undefined leaf shares, so leaf- and
    # axis-level analyses filter on this flag instead of quietly treating it as all-zero.
    analysable = pd.Series(leaf_cond.sum(axis=1) > 0.5, index=book_ids, name="analysable")
    n_dropped = int((~analysable).sum())
    if n_dropped:
        LOGGER.warning("%d book(s) flagged not analysable (no interpretable leaf mass): %s",
                       n_dropped, list(analysable.index[~analysable])[:10])

    frame = pd.concat(
        [
            pd.DataFrame({tier_col: tiers}),
            analysable,
            outcomes, controls,
            mapping_cov.reindex(book_ids),
            group_shares.reindex(book_ids).fillna(0.0),
            axis_block, ratio_block,
            leaf_block, leaf_abs_block,
            topics,
        ],
        axis=1,
    )
    frame.index.name = "book_id"

    duplicated = frame.columns[frame.columns.duplicated()].tolist()
    if duplicated:
        raise ValueError(f"Duplicate columns in the analysis frame: {duplicated}")

    frame.attrs["payoff_guard"] = guard
    frame.attrs["epsilon"] = epsilon
    frame.attrs["axis_variant"] = variant

    out_path.parent.mkdir(parents=True, exist_ok=True)
    frame.reset_index().to_parquet(out_path, index=False)
    LOGGER.info("Wrote analysis frame: %s rows x %d columns -> %s",
                f"{len(frame):,}", frame.shape[1], out_path)

    # A small sidecar so notebooks can read the guard verdict and the column blocks without
    # re-deriving them from column-name prefixes.
    manifest = pd.DataFrame([
        {"block": "tier", "prefix": tier_col, "n_columns": 1},
        {"block": "outcome", "prefix": "-", "n_columns": outcomes.shape[1]},
        {"block": "control", "prefix": "-", "n_columns": controls.shape[1]},
        {"block": "mapping_coverage", "prefix": "-", "n_columns": mapping_cov.shape[1]},
        {"block": "group_share", "prefix": "group_", "n_columns": group_shares.shape[1]},
        {"block": "axis", "prefix": "AX_", "n_columns": axis_block.shape[1]},
        {"block": "log_ratio", "prefix": "LR_", "n_columns": ratio_block.shape[1]},
        {"block": "leaf_share_cond", "prefix": "leaf_", "n_columns": leaf_block.shape[1]},
        {"block": "leaf_share_abs", "prefix": "abs_leaf_", "n_columns": leaf_abs_block.shape[1]},
        {"block": "topic_share", "prefix": "topic_", "n_columns": topics.shape[1]},
    ])
    manifest.to_parquet(features_dir / "analysis_frame_manifest.parquet", index=False)
    pd.DataFrame([guard]).to_parquet(features_dir / "payoff_guard_verdict.parquet", index=False)
    LOGGER.info("Column blocks:\n%s", manifest.to_string(index=False))

    LOGGER.info("=" * 78)
    LOGGER.info("Done in %.1fs", time.perf_counter() - started)
    LOGGER.info("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
