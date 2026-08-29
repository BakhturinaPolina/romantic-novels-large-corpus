#!/usr/bin/env python3
"""Roll hard topic counts up to taxonomy leaves and main groups, then build the theory axes.

Replaces the soft-probability version (now `src/legacy/stage10_correlation_analysis/`), which
had three problems this script fixes:

1. It pivoted a hardcoded 15-entry dict of taxonomy IDs, covering only 20% of topic mass.
   `3.2`, `7.3` and `6.6` had topics in the lookup table and were dropped anyway. Here every
   leaf present in `topic_lookup.parquet` gets a column.
2. It kept its own copy of the axis definitions, which drifted from the frozen schema and
   emitted four axes that were exactly 0.0 for all 16,000 books. Axes now come from
   `configs/stage09/theory_aligned_index_schema.yaml` via `analysis/axes.py`, and an empty
   component raises instead of silently zeroing.
3. It gave no way to see how thin an axis was. `axis_coverage.parquet` reports topics and mass
   per component, so "AX_hea_index is really just leaf 4.5" is visible in a table.

Outputs (under `outputs.book_features_dir`):
  book_leaf_shares_abs.parquet     leaf_<id>: share of all assigned sentences
  book_leaf_shares_cond.parquet    leaf_<id>: share of *interpretable* mass (excludes noise
                                   and context-only leaves), so leaves are comparable across
                                   books with different amounts of unmappable text
  book_group_shares.parquet        one column per taxonomy main group
  book_axes_strict.parquet         axes from primary topic mapping only
  book_axes_generous.parquet       axes with secondary mappings at half weight
  axis_coverage.parquet            per-component topic count, mass, verdict
  axis_definitions.parquet         the signed leaf weights actually used
  leaf_topic_inventory.parquet     per leaf: topics, mass, prevalence, confidence, evidence
  mapping_coverage.parquet         how much corpus mass is mapped, axis-bearing, noise

Usage:
  .venv/bin/python src/stage10_correlation_analysis/data_preparation/02_book_aggregation.py
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

from src.stage10_correlation_analysis.analysis import axes as axes_mod  # noqa: E402
from src.stage10_correlation_analysis.analysis.config import (  # noqa: E402
    DEFAULT_CONFIG_PATH,
    load_analysis_config,
)

LOGGER = logging.getLogger("stage10.book_aggregation")

# Leaves that carry no interpretable narrative content. Excluded from the conditional
# denominator so that `cond_share` answers "of the text we can interpret, how much is this?"
NON_INTERPRETABLE_LEAVES = {"noise", "uncertain_interpretable", "unmapped"}


def setup_logging(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    for logger in (LOGGER, axes_mod.LOGGER):
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        for handler in (
            logging.FileHandler(output_dir / "02_book_aggregation.log", mode="w", encoding="utf-8"),
            logging.StreamHandler(),
        ):
            handler.setFormatter(fmt)
            logger.addHandler(handler)


def write(frame: pd.DataFrame, path: Path, label: str, *, index: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(path, index=index)
    LOGGER.info("Wrote %-28s %6s rows x %3d cols -> %s",
                label, f"{len(frame):,}", frame.shape[1], path.name)


# ---------------------------------------------------------------------------
# Topic -> leaf mapping
# ---------------------------------------------------------------------------

def build_topic_leaf_map(
    topic_lookup: pd.DataFrame,
    *,
    secondary_weight: float,
    drop_noise_topics: bool,
) -> pd.DataFrame:
    """Long topic -> leaf table with weights: primary at 1.0, optionally secondary at 0.5.

    239 of 348 topics carry a secondary taxonomy ID. Ignoring them throws away real signal
    (a kiss scene in a hotel is both `2.2` and `8.2`); counting them at full weight would
    double-count mass. Both variants are produced so the notebooks can show that conclusions
    do not hinge on the choice.
    """
    lookup = topic_lookup.copy()
    if drop_noise_topics:
        noise_mask = lookup.get("taxonomy_is_noise", pd.Series(False, index=lookup.index)).fillna(False)
        n_noise = int(noise_mask.sum())
        if n_noise:
            LOGGER.info("Excluding %d topics flagged as noise by Stage09", n_noise)
        lookup = lookup[~noise_mask.astype(bool)]

    primary = lookup[["topic_id", "taxonomy_main_id"]].rename(columns={"taxonomy_main_id": "leaf_id"})
    primary = primary.dropna(subset=["leaf_id"]).assign(weight=1.0, role="primary")

    parts = [primary]
    if secondary_weight > 0 and "taxonomy_secondary_id" in lookup.columns:
        secondary = (
            lookup[["topic_id", "taxonomy_secondary_id"]]
            .rename(columns={"taxonomy_secondary_id": "leaf_id"})
            .dropna(subset=["leaf_id"])
            .assign(weight=float(secondary_weight), role="secondary")
        )
        # A topic whose secondary repeats its primary would otherwise get 1.5x weight.
        secondary = secondary.merge(
            primary[["topic_id", "leaf_id"]].assign(_dupe=True),
            on=["topic_id", "leaf_id"], how="left",
        )
        secondary = secondary[secondary["_dupe"].isna()].drop(columns=["_dupe"])
        LOGGER.info("Adding %d secondary mappings at weight %.2f", len(secondary), secondary_weight)
        parts.append(secondary)

    out = pd.concat(parts, ignore_index=True)
    out["leaf_id"] = out["leaf_id"].astype(str)
    out["topic_id"] = out["topic_id"].astype(int)
    return out


def leaf_inventory(
    topic_lookup: pd.DataFrame,
    book_topic_counts: pd.DataFrame,
    topic_leaf: pd.DataFrame,
) -> pd.DataFrame:
    """Per leaf: how many topics, how much mass, how prevalent, how well evidenced.

    This is the table to read before trusting any leaf-level result. A leaf resting on one
    topic is a single cluster's idiosyncrasies, not a theme.
    """
    corpus_mass = book_topic_counts.groupby("topic_id")["n_sentences"].sum()
    total = float(corpus_mass.sum())
    prevalence = (
        book_topic_counts[book_topic_counts["n_sentences"] > 0]
        .groupby("topic_id")["book_id"].nunique()
    )
    n_books = book_topic_counts["book_id"].nunique()

    primary = topic_leaf[topic_leaf["role"] == "primary"]
    merged = primary.merge(
        topic_lookup[[c for c in [
            "topic_id", "taxonomy_main_name", "taxonomy_main_group", "taxonomy_confidence",
            "taxonomy_evidence_quality", "taxonomy_use_in_macro_axes",
        ] if c in topic_lookup.columns]],
        on="topic_id", how="left",
    )
    merged["mass"] = merged["topic_id"].map(corpus_mass).fillna(0.0)
    merged["prevalence"] = merged["topic_id"].map(prevalence).fillna(0) / max(n_books, 1)

    agg = merged.groupby("leaf_id").agg(
        leaf_name=("taxonomy_main_name", "first"),
        main_group=("taxonomy_main_group", "first"),
        n_topics=("topic_id", "size"),
        mass_sentences=("mass", "sum"),
        mean_prevalence=("prevalence", "mean"),
        mean_confidence=("taxonomy_confidence", "mean"),
        n_low_evidence=("taxonomy_evidence_quality", lambda s: int((s == "low").sum())),
        n_axis_bearing=("taxonomy_use_in_macro_axes", lambda s: int(s.fillna(False).sum())),
    ).reset_index()
    agg["mass_share"] = agg["mass_sentences"] / total
    return agg.sort_values("mass_share", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Book-level pivots
# ---------------------------------------------------------------------------

def pivot_leaf_shares(
    book_topic_counts: pd.DataFrame,
    topic_leaf: pd.DataFrame,
    *,
    prefix: str = "leaf_",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Absolute and conditional leaf shares, one row per book.

    Absolute: share of the book's assigned sentences. Comparable to "3.3% of this book".
    Conditional: share of the book's *interpretable* sentences. Two books can differ in how
    much of their text the taxonomy can speak about at all; the conditional form removes that
    nuisance so leaf comparisons are not driven by mapping coverage.
    """
    joined = book_topic_counts.merge(topic_leaf, on="topic_id", how="left")
    joined["leaf_id"] = joined["leaf_id"].fillna("unmapped")
    joined["weight"] = joined["weight"].fillna(1.0)
    joined["weighted"] = joined["n_sentences"] * joined["weight"]

    leaf_counts = joined.groupby(["book_id", "leaf_id"])["weighted"].sum().unstack(fill_value=0.0)

    denom_abs = leaf_counts.sum(axis=1)
    interpretable = [c for c in leaf_counts.columns if c not in NON_INTERPRETABLE_LEAVES]
    denom_cond = leaf_counts[interpretable].sum(axis=1)

    abs_shares = leaf_counts.div(denom_abs.replace(0.0, np.nan), axis=0).fillna(0.0)
    cond_shares = (
        leaf_counts[interpretable].div(denom_cond.replace(0.0, np.nan), axis=0).fillna(0.0)
    )

    abs_shares.columns = [f"{prefix}{c}" for c in abs_shares.columns]
    cond_shares.columns = [f"{prefix}{c}" for c in cond_shares.columns]

    abs_shares["interpretable_mass"] = (denom_cond / denom_abs.replace(0.0, np.nan)).fillna(0.0)

    # A book with no interpretable sentence at all has undefined conditional shares. In this
    # corpus that is one single-sentence book whose only topic was the outlier; it is flagged
    # rather than dropped here, and excluded downstream by `analysable`.
    degenerate = int((denom_cond <= 0).sum())
    if degenerate:
        LOGGER.warning(
            "%d book(s) have zero interpretable mass; their conditional leaf shares are all "
            "zero and they are flagged as not analysable in the frame", degenerate,
        )
    return abs_shares, cond_shares


def pivot_group_shares(
    book_topic_counts: pd.DataFrame,
    topic_lookup: pd.DataFrame,
    *,
    prefix: str = "group_",
) -> pd.DataFrame:
    """Main-group shares — the coarse level that Chapter 2 of the report opens with."""
    groups = topic_lookup[["topic_id", "taxonomy_main_group"]].dropna()
    joined = book_topic_counts.merge(groups, on="topic_id", how="left")
    joined["taxonomy_main_group"] = joined["taxonomy_main_group"].fillna("Unmapped")

    counts = joined.groupby(["book_id", "taxonomy_main_group"])["n_sentences"].sum().unstack(fill_value=0)
    shares = counts.div(counts.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    shares.columns = [f"{prefix}{c.replace(' ', '_').replace(',', '').replace('&', 'and').lower()}"
                      for c in shares.columns]
    return shares


def mapping_coverage(
    book_topic_counts: pd.DataFrame,
    topic_lookup: pd.DataFrame,
    id_sets: Dict[str, set],
) -> pd.DataFrame:
    """How much of each book the taxonomy can actually speak about.

    The old pipeline's `mapped_mass` averaged 0.2004, which meant every leaf-level statement
    was about a fifth of the text. This table is how that number gets checked rather than
    assumed.
    """
    flags = topic_lookup[["topic_id", "taxonomy_main_id"]].copy()
    flags["is_axis_bearing"] = flags["taxonomy_main_id"].astype(str).isin(id_sets["axis_bearing"])
    flags["is_context"] = flags["taxonomy_main_id"].astype(str).isin(id_sets["secondary_context"])
    flags["is_noise_leaf"] = flags["taxonomy_main_id"].astype(str).isin(NON_INTERPRETABLE_LEAVES)

    joined = book_topic_counts.merge(flags, on="topic_id", how="left")
    joined["is_mapped"] = joined["taxonomy_main_id"].notna()
    for col in ("is_axis_bearing", "is_context", "is_noise_leaf"):
        joined[col] = joined[col].fillna(False)

    total = joined.groupby("book_id")["n_sentences"].sum()
    out = pd.DataFrame({
        "mapped_mass": joined[joined["is_mapped"]].groupby("book_id")["n_sentences"].sum() / total,
        "axis_bearing_mass": joined[joined["is_axis_bearing"]].groupby("book_id")["n_sentences"].sum() / total,
        "context_mass": joined[joined["is_context"]].groupby("book_id")["n_sentences"].sum() / total,
        "noise_leaf_mass": joined[joined["is_noise_leaf"]].groupby("book_id")["n_sentences"].sum() / total,
    }).fillna(0.0)

    LOGGER.info(
        "Corpus mapping coverage: mapped %.3f, axis-bearing %.3f, context %.3f, non-interpretable %.3f",
        out["mapped_mass"].mean(), out["axis_bearing_mass"].mean(),
        out["context_mass"].mean(), out["noise_leaf_mass"].mean(),
    )
    return out.reset_index()


# ---------------------------------------------------------------------------
# Axis construction
# ---------------------------------------------------------------------------

def build_variant(
    variant: str,
    book_topic_counts: pd.DataFrame,
    topic_lookup: pd.DataFrame,
    specs: Dict[str, axes_mod.AxisSpec],
    weights: Dict[str, float],
    *,
    out_dir: Path,
    fail_on_empty: bool,
    allow_empty: Sequence[str],
    write_shares: bool,
) -> pd.DataFrame:
    LOGGER.info("-" * 70)
    LOGGER.info("Variant %r: primary weight %.2f, secondary weight %.2f",
                variant, weights["primary_weight"], weights["secondary_weight"])

    topic_leaf = build_topic_leaf_map(
        topic_lookup,
        secondary_weight=weights["secondary_weight"],
        drop_noise_topics=True,
    )
    abs_shares, cond_shares = pivot_leaf_shares(book_topic_counts, topic_leaf)

    if write_shares:
        write(abs_shares.reset_index(), out_dir / "book_leaf_shares_abs.parquet", "leaf_shares_abs")
        write(cond_shares.reset_index(), out_dir / "book_leaf_shares_cond.parquet", "leaf_shares_cond")

    # Axes use conditional shares: a book with more unmappable text should not appear to have
    # weaker themes purely because of that.
    axis_values = axes_mod.build_axis_values(
        cond_shares, specs,
        fail_on_empty_component=fail_on_empty,
        allow_empty_axes=allow_empty,
    )
    skipped = axis_values.attrs.get("skipped_axes", {})
    if skipped:
        LOGGER.warning("Variant %r skipped %d axes: %s", variant, len(skipped), ", ".join(skipped))

    write(axis_values.reset_index(), out_dir / f"book_axes_{variant}.parquet", f"axes_{variant}")
    return axis_values


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=str, default=DEFAULT_CONFIG_PATH)
    ap.add_argument("--allow-empty-axes", action="store_true",
                    help="Warn instead of raising when an axis has no measurable component.")
    args = ap.parse_args()

    cfg = load_analysis_config(args.config)
    out_dir = cfg.output_path("book_features_dir")
    setup_logging(out_dir)

    LOGGER.info("=" * 78)
    LOGGER.info("Stage10 book aggregation (hard assignments) — run %s", cfg.run_id)
    LOGGER.info("=" * 78)
    started = time.perf_counter()

    counts_dir = cfg.output_path("hard_counts_dir")
    book_topic_counts = pd.read_parquet(counts_dir / "book_topic_counts.parquet")
    LOGGER.info("Loaded %s book x topic rows over %s books",
                f"{len(book_topic_counts):,}", f"{book_topic_counts['book_id'].nunique():,}")

    topic_lookup = pd.read_parquet(cfg.input_path("topic_lookup", required=True))
    LOGGER.info("Loaded %d topics from the Stage09 lookup", len(topic_lookup))

    excluded = cfg.excluded_book_ids()
    if excluded:
        before = book_topic_counts["book_id"].nunique()
        book_topic_counts = book_topic_counts[~book_topic_counts["book_id"].isin(excluded)]
        LOGGER.info("Excluded %d books (%d -> %d)", len(excluded), before,
                    book_topic_counts["book_id"].nunique())

    # ---- inventory and coverage, before any axis maths ----
    strict_map = build_topic_leaf_map(topic_lookup, secondary_weight=0.0, drop_noise_topics=True)
    inventory = leaf_inventory(topic_lookup, book_topic_counts, strict_map)
    write(inventory, out_dir / "leaf_topic_inventory.parquet", "leaf_topic_inventory")
    LOGGER.info("Leaves present: %d; mass covered by top 10: %.3f",
                len(inventory), inventory["mass_share"].head(10).sum())

    id_sets = axes_mod.taxonomy_id_sets(cfg.input_path("taxonomy_config", required=True))
    coverage_by_book = mapping_coverage(book_topic_counts, topic_lookup, id_sets)
    write(coverage_by_book, out_dir / "mapping_coverage.parquet", "mapping_coverage")

    group_shares = pivot_group_shares(book_topic_counts, topic_lookup)
    write(group_shares.reset_index(), out_dir / "book_group_shares.parquet", "group_shares")

    # ---- resolve the axis schema and audit it ----
    schema = axes_mod.load_axis_schema(cfg.input_path("axis_schema", required=True))
    composites = axes_mod.load_composites(cfg.input_path("taxonomy_config", required=True))
    additional = cfg.section("axes", "additional", default={}) or {}
    specs = axes_mod.resolve_axes(schema, composites, additional=additional)

    leaf_topic_counts = dict(zip(inventory["leaf_id"], inventory["n_topics"]))
    leaf_mass = dict(zip(inventory["leaf_id"], inventory["mass_share"]))
    verdicts = cfg.section("axes", "coverage_verdicts")
    coverage = axes_mod.audit_coverage(
        specs, leaf_topic_counts, leaf_mass,
        viable_min_topics=int(verdicts["viable_min_topics"]),
        weak_min_topics=int(verdicts["weak_min_topics"]),
    )
    write(coverage, out_dir / "axis_coverage.parquet", "axis_coverage")
    summary = axes_mod.summarise_coverage(coverage)
    write(summary, out_dir / "axis_coverage_summary.parquet", "axis_coverage_summary")
    write(axes_mod.leaf_weight_table(specs), out_dir / "axis_definitions.parquet", "axis_definitions")

    empty_axes = summary.loc[summary["axis_verdict"] == "empty", "axis"].tolist()
    weak_axes = summary.loc[summary["axis_verdict"] == "weak", "axis"].tolist()
    LOGGER.info("Axis verdicts: %d viable, %d weak, %d empty",
                int((summary["axis_verdict"] == "viable").sum()), len(weak_axes), len(empty_axes))
    for axis in weak_axes:
        row = summary[summary["axis"] == axis].iloc[0]
        LOGGER.warning("  WEAK  %-42s %d viable / %d weak / %d empty components%s",
                       axis, row["n_viable"], row["n_weak"], row["n_empty"],
                       f" (empty: {row['empty_leaves']})" if row["empty_leaves"] else "")
    for axis in empty_axes:
        LOGGER.warning("  EMPTY %-42s no component has any topic", axis)

    # ---- build both mapping variants ----
    fail_on_empty = bool(cfg.section("axes", "fail_on_empty_component")) and not args.allow_empty_axes
    allow_empty = list(empty_axes)  # documented above; skipped rather than emitted as zeros
    variants = cfg.section("axes", "variants")
    primary_variant = cfg.section("axes", "primary_variant")

    axis_frames: Dict[str, pd.DataFrame] = {}
    for variant, weights in variants.items():
        axis_frames[variant] = build_variant(
            variant, book_topic_counts, topic_lookup, specs, weights,
            out_dir=out_dir, fail_on_empty=fail_on_empty, allow_empty=allow_empty,
            write_shares=(variant == primary_variant),
        )

    # ---- how much does the mapping choice matter? ----
    if len(axis_frames) == 2:
        (a_name, a), (b_name, b) = list(axis_frames.items())
        shared = sorted(set(a.columns) & set(b.columns))
        rows = [{
            "axis": col,
            "pearson_r": float(a[col].corr(b[col])),
            "spearman_r": float(a[col].corr(b[col], method="spearman")),
            f"mean_{a_name}": float(a[col].mean()),
            f"mean_{b_name}": float(b[col].mean()),
        } for col in shared]
        stability = pd.DataFrame(rows).sort_values("spearman_r")
        write(stability, out_dir / "axis_mapping_stability.parquet", "axis_mapping_stability")
        LOGGER.info("Strict vs generous mapping: median Spearman %.3f, minimum %.3f (%s)",
                    stability["spearman_r"].median(), stability["spearman_r"].min(),
                    stability.iloc[0]["axis"])

    LOGGER.info("=" * 78)
    LOGGER.info("Done in %.1fs", time.perf_counter() - started)
    LOGGER.info("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
