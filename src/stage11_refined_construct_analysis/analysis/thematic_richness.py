"""Book-level thematic richness / concentration metrics (exploratory).

Shannon entropy, effective number of themes (e^H), top-k concentration, and
rarefaction — used by Notebook 14. These analyses do **not** redefine constructs
or change confirmatory H1–H6 verdicts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from src.stage11_refined_construct_analysis.analysis.presentation import ATTENTION_THEMES
from src.stage11_refined_construct_analysis.config import Stage11Config
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup

# Presentation construct columns for resolution C (row-renormalized).
CONSTRUCT_RICHNESS_COLS: Tuple[str, ...] = tuple(col for col, _ in ATTENTION_THEMES)

NON_INTERPRETABLE_LEAVES = {"noise", "uncertain_interpretable", "unmapped"}


def shannon_entropy(p: np.ndarray, *, base: float = np.e) -> float:
    """Shannon entropy H = -∑ p_i log p_i on a probability vector (zeros ignored)."""
    x = np.asarray(p, dtype=float)
    x = x[np.isfinite(x) & (x > 0)]
    if x.size == 0:
        return 0.0
    s = float(x.sum())
    if s <= 0:
        return 0.0
    x = x / s
    if base == np.e:
        return float(-np.sum(x * np.log(x)))
    return float(-np.sum(x * np.log(x) / np.log(base)))


def effective_n(h: float) -> float:
    """Effective number of categories: e^H."""
    if not np.isfinite(h) or h < 0:
        return 0.0
    return float(np.exp(h))


def topk_concentration(p: np.ndarray, k: int = 10) -> float:
    """Share of mass in the k largest categories (after normalizing)."""
    x = np.asarray(p, dtype=float)
    x = x[np.isfinite(x) & (x > 0)]
    if x.size == 0:
        return 0.0
    s = float(x.sum())
    if s <= 0:
        return 0.0
    x = np.sort(x / s)[::-1]
    return float(x[: min(k, x.size)].sum())


def diversity_from_shares(
    wide: pd.DataFrame,
    *,
    prefix: str = "",
    k: int = 10,
) -> pd.DataFrame:
    """Book-level H, n_eff, top-k, and diagnostic n_nonzero from a share matrix."""
    if wide.empty:
        return pd.DataFrame(
            columns=[
                f"{prefix}H",
                f"{prefix}n_eff",
                f"{prefix}top{k}",
                f"{prefix}n_nonzero",
            ]
        )
    mat = wide.to_numpy(dtype=float)
    rows = []
    for i in range(mat.shape[0]):
        p = mat[i]
        h = shannon_entropy(p)
        rows.append(
            {
                f"{prefix}H": h,
                f"{prefix}n_eff": effective_n(h),
                f"{prefix}top{k}": topk_concentration(p, k=k),
                f"{prefix}n_nonzero": int(np.sum(np.isfinite(p) & (p > 0))),
            }
        )
    out = pd.DataFrame(rows, index=wide.index)
    out.index.name = wide.index.name or "book_id"
    return out


def row_normalize(wide: pd.DataFrame) -> pd.DataFrame:
    """Row-normalize a non-negative share matrix (zeros stay zero rows)."""
    out = wide.astype(float).copy()
    totals = out.sum(axis=1)
    nonzero = totals > 0
    out.loc[nonzero] = out.loc[nonzero].div(totals.loc[nonzero], axis=0)
    return out


def load_topic_share_wide(cfg: Stage11Config) -> pd.DataFrame:
    """Book × topic hard shares (topic_id >= 0)."""
    from src.stage11_refined_construct_analysis.analysis.exploratory_security import (
        topic_share_matrix,
    )

    return topic_share_matrix(cfg)


def load_topic_counts_long(cfg: Stage11Config) -> pd.DataFrame:
    """Long book_topic_counts with topic_id >= 0."""
    path = cfg.input_path("book_topic_counts", required=True)
    assert path is not None
    counts = pd.read_parquet(path)
    return counts[counts["topic_id"] >= 0].copy()


def load_leaf_share_wide(cfg: Stage11Config) -> pd.DataFrame:
    """Conditional taxonomy leaf shares (~45 interpretable leaves)."""
    # Prefer dedicated cond parquet; fall back to analysis-frame leaf_* columns.
    base = cfg.input_path("analysis_frame", required=True)
    assert base is not None
    cond_path = base.parent / "book_leaf_shares_cond.parquet"
    if cond_path.exists():
        leaf = pd.read_parquet(cond_path)
        if "book_id" in leaf.columns:
            leaf = leaf.set_index("book_id")
        cols = [
            c
            for c in leaf.columns
            if str(c).startswith("leaf_")
            and str(c).replace("leaf_", "") not in NON_INTERPRETABLE_LEAVES
        ]
        return leaf[cols].astype(float)

    frame = pd.read_parquet(base)
    if "book_id" in frame.columns:
        frame = frame.set_index("book_id")
    cols = [
        c
        for c in frame.columns
        if str(c).startswith("leaf_")
        and not str(c).startswith("leaf_un")
        and str(c).replace("leaf_", "") not in NON_INTERPRETABLE_LEAVES
    ]
    return frame[cols].astype(float)


def construct_share_wide(
    frame: pd.DataFrame,
    cols: Sequence[str] = CONSTRUCT_RICHNESS_COLS,
) -> pd.DataFrame:
    """Presentation construct columns, row-renormalized to a probability simplex."""
    present = [c for c in cols if c in frame.columns]
    if not present:
        return pd.DataFrame(index=frame.index)
    wide = frame[list(present)].astype(float).fillna(0.0)
    # Ensure book_id index when present as a column
    if "book_id" in frame.columns and frame.index.name != "book_id":
        wide = wide.copy()
        wide.index = frame["book_id"].to_numpy()
        wide.index.name = "book_id"
    return row_normalize(wide)


def topic_to_leaf_map(cfg: Stage11Config) -> Dict[int, str]:
    """topic_id → taxonomy_main_id (string leaf id)."""
    lookup = load_topic_lookup(cfg)
    out: Dict[int, str] = {}
    for _, r in lookup.iterrows():
        tid = int(r["topic_id"])
        leaf = str(r.get("taxonomy_main_id") or "")
        if leaf and leaf.lower() not in NON_INTERPRETABLE_LEAVES and leaf.lower() != "nan":
            out[tid] = leaf
    return out


def rarefaction_depth(
    n_sentences: pd.Series,
    *,
    quantile: float = 0.10,
) -> int:
    """Floor of the given quantile of book lengths (eligible books must have ≥ depth)."""
    s = pd.to_numeric(n_sentences, errors="coerce").dropna()
    s = s[s > 0]
    if s.empty:
        raise ValueError("No positive n_sentences for rarefaction depth")
    return int(np.floor(float(s.quantile(quantile))))


def rarefy_topic_counts(
    counts_long: pd.DataFrame,
    *,
    depth: int,
    seed: int = 42,
    book_ids: Optional[Sequence] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Without-replacement rarefaction of topic sentence counts.

    Returns
    -------
    rarefied_shares : DataFrame
        Wide book × topic shares from the rarefied sample (rows = eligible books).
    summary : DataFrame
        Per-book `n_eff`, `H`, `top10`, `n_unique`, `depth`, `n_sentences_total`.
    """
    if depth < 1:
        raise ValueError(f"rarefaction depth must be >= 1, got {depth}")

    df = counts_long[counts_long["topic_id"] >= 0].copy()
    if book_ids is not None:
        wanted = set(book_ids)
        df = df[df["book_id"].isin(wanted)]

    totals = df.groupby("book_id")["n_sentences"].sum()
    eligible = totals[totals >= depth].index
    df = df[df["book_id"].isin(eligible)]
    if df.empty:
        empty = pd.DataFrame()
        return empty, empty

    rng = np.random.default_rng(seed)
    share_rows: List[Dict[Any, float]] = []
    summary_rows: List[Dict[str, Any]] = []

    for book_id, sub in df.groupby("book_id", sort=False):
        topics = sub["topic_id"].astype(int).to_numpy()
        counts = sub["n_sentences"].astype(int).to_numpy()
        total = int(counts.sum())
        if total < depth:
            continue
        if total == depth:
            sampled = counts
        else:
            sampled = rng.multivariate_hypergeometric(counts, depth)
        mass = float(sampled.sum())
        shares = sampled / mass if mass > 0 else sampled.astype(float)
        row = {int(t): float(s) for t, s in zip(topics, shares) if s > 0}
        row_idx = {"book_id": book_id, **row}
        share_rows.append(row_idx)

        h = shannon_entropy(shares)
        summary_rows.append(
            {
                "book_id": book_id,
                "depth": depth,
                "n_sentences_total": total,
                "H": h,
                "n_eff": effective_n(h),
                "top10": topk_concentration(shares, k=10),
                "n_unique": int(np.sum(sampled > 0)),
            }
        )

    if not share_rows:
        return pd.DataFrame(), pd.DataFrame()

    rare_long = pd.DataFrame(share_rows).set_index("book_id")
    # Columns may be mixed; coerce topic cols to int where possible
    topic_cols = [c for c in rare_long.columns if c != "book_id"]
    rare_wide = rare_long[topic_cols].fillna(0.0)
    rare_wide.columns = [int(c) for c in rare_wide.columns]
    summary = pd.DataFrame(summary_rows).set_index("book_id")
    return rare_wide, summary


def map_rarefied_to_leaves(
    rarefied_topic_shares: pd.DataFrame,
    topic_leaf: Mapping[int, str],
) -> pd.DataFrame:
    """Aggregate rarefied topic shares to taxonomy leaves; row-normalize."""
    if rarefied_topic_shares.empty:
        return pd.DataFrame()
    records: Dict[Any, Dict[str, float]] = {}
    for book_id, row in rarefied_topic_shares.iterrows():
        leaf_mass: Dict[str, float] = {}
        for tid, share in row.items():
            s = float(share)
            if s <= 0:
                continue
            leaf = topic_leaf.get(int(tid))
            if not leaf:
                continue
            leaf_mass[leaf] = leaf_mass.get(leaf, 0.0) + s
        records[book_id] = leaf_mass
    if not records:
        return pd.DataFrame()
    wide = pd.DataFrame.from_dict(records, orient="index").fillna(0.0)
    wide.index.name = rarefied_topic_shares.index.name or "book_id"
    # Prefix leaf_ for consistency with Stage 10 naming
    wide.columns = [f"leaf_{c}" if not str(c).startswith("leaf_") else str(c) for c in wide.columns]
    return row_normalize(wide)


def _load_w_tk_strict(cfg: Stage11Config) -> pd.DataFrame:
    path = cfg.output_path("constructs_dir") / "W_tk_strict.parquet"
    if not path.exists():
        # Fallback relative to notebook outputs
        alt = Path(cfg.output_path("base_dir")) / "constructs" / "W_tk_strict.parquet"
        path = alt if alt.exists() else path
    if not path.exists():
        raise FileNotFoundError(f"Missing W_tk_strict: {path}")
    return pd.read_parquet(path)


def map_rarefied_to_constructs(
    rarefied_topic_shares: pd.DataFrame,
    cfg: Stage11Config,
    *,
    cols: Sequence[str] = CONSTRUCT_RICHNESS_COLS,
) -> pd.DataFrame:
    """Project rarefied topic shares through W_tk → presentation constructs; renormalize."""
    from src.stage11_refined_construct_analysis.analysis.constructs import (
        COMPOSITE_DEFS,
        all_rax_atoms,
    )
    from src.stage11_refined_construct_analysis.analysis.frame import (
        _book_constructs_from_shares,
        _weights_to_topic_rax,
    )

    if rarefied_topic_shares.empty:
        return pd.DataFrame()

    w_tk = _load_w_tk_strict(cfg)
    atoms = all_rax_atoms()
    topic_rax = _weights_to_topic_rax(w_tk, atoms=atoms)
    C = _book_constructs_from_shares(rarefied_topic_shares, topic_rax)
    # Add composites needed by ATTENTION_THEMES
    for name, parts in COMPOSITE_DEFS.items():
        present = [p for p in parts if p in C.columns]
        C[name] = C[present].sum(axis=1) if present else 0.0
    present_cols = [c for c in cols if c in C.columns]
    if not present_cols:
        return pd.DataFrame(index=rarefied_topic_shares.index)
    return row_normalize(C[present_cols].astype(float).fillna(0.0))


def compute_all_richness(
    cfg: Stage11Config,
    work: pd.DataFrame,
    *,
    seed: int = 42,
    length_quantile: float = 0.10,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Compute topic / taxonomy / construct richness and rarefied variants; join to work.

    Returns enriched work frame and a meta dict (depth, n_eligible, etc.).
    """
    topic_wide = load_topic_share_wide(cfg)
    leaf_wide = load_leaf_share_wide(cfg)
    # Align construct shares to work's book ids
    work_idx = work.set_index("book_id") if "book_id" in work.columns else work
    construct_wide = construct_share_wide(work_idx)

    topic_div = diversity_from_shares(topic_wide, prefix="topic_")
    leaf_div = diversity_from_shares(leaf_wide, prefix="taxonomy_")
    construct_div = diversity_from_shares(construct_wide, prefix="construct_")

    # Rarefaction
    meta: Dict[str, Any] = {}
    n_sent = work_idx["n_sentences"] if "n_sentences" in work_idx.columns else None
    rare_topic_summary = pd.DataFrame()
    rare_leaf_div = pd.DataFrame()
    rare_construct_div = pd.DataFrame()
    depth = None
    if n_sent is not None:
        depth = rarefaction_depth(n_sent, quantile=length_quantile)
        counts = load_topic_counts_long(cfg)
        book_ids = work_idx.index.tolist()
        rare_wide, rare_topic_summary = rarefy_topic_counts(
            counts, depth=depth, seed=seed, book_ids=book_ids
        )
        meta["rarefaction_depth"] = depth
        meta["n_rarefaction_eligible"] = int(len(rare_topic_summary))
        if not rare_wide.empty:
            t2l = topic_to_leaf_map(cfg)
            rare_leaf_shares = map_rarefied_to_leaves(rare_wide, t2l)
            rare_leaf_div = diversity_from_shares(rare_leaf_shares, prefix="rare_taxonomy_")
            try:
                rare_c_shares = map_rarefied_to_constructs(rare_wide, cfg)
                rare_construct_div = diversity_from_shares(
                    rare_c_shares, prefix="rare_construct_"
                )
            except FileNotFoundError:
                meta["rare_construct_skipped"] = "W_tk_strict missing"

    enriched = work.copy()
    if "book_id" not in enriched.columns:
        enriched = enriched.reset_index()

    for div in (topic_div, leaf_div, construct_div, rare_leaf_div, rare_construct_div):
        if div is None or div.empty:
            continue
        piece = div.copy()
        piece.index.name = "book_id"
        enriched = enriched.merge(piece.reset_index(), on="book_id", how="left")

    if rare_topic_summary is not None and not rare_topic_summary.empty:
        piece = rare_topic_summary.rename(
            columns={
                "H": "rare_topic_H",
                "n_eff": "rare_topic_n_eff",
                "top10": "rare_topic_top10",
                "n_unique": "rare_topic_n_unique",
                "depth": "rarefaction_depth",
                "n_sentences_total": "rare_n_sentences_total",
            }
        )
        keep = [c for c in piece.columns if c.startswith("rare_") or c == "rarefaction_depth"]
        enriched = enriched.merge(
            piece[keep].reset_index(), on="book_id", how="left"
        )

    meta["n_topics"] = int(topic_wide.shape[1])
    meta["n_leaves"] = int(leaf_wide.shape[1])
    meta["n_constructs"] = int(construct_wide.shape[1])
    meta["length_quantile"] = length_quantile
    meta["seed"] = seed
    return enriched, meta


def richness_decile_table(
    frame: pd.DataFrame,
    richness_col: str,
    outcome_col: str = "rating_shrunk",
    *,
    n_bins: int = 10,
) -> pd.DataFrame:
    """Mean outcome by richness decile (1 = narrowest, 10 = richest)."""
    if richness_col not in frame.columns or outcome_col not in frame.columns:
        return pd.DataFrame()
    tmp = frame[[richness_col, outcome_col]].dropna().copy()
    if tmp.empty:
        return pd.DataFrame()
    try:
        tmp["decile"] = pd.qcut(tmp[richness_col], q=n_bins, labels=False, duplicates="drop") + 1
    except ValueError:
        tmp["decile"] = pd.cut(tmp[richness_col], bins=n_bins, labels=False) + 1
    out = (
        tmp.groupby("decile", observed=True)
        .agg(
            n=("decile", "size"),
            richness_mean=(richness_col, "mean"),
            outcome_mean=(outcome_col, "mean"),
            outcome_median=(outcome_col, "median"),
        )
        .reset_index()
    )
    out["richness_col"] = richness_col
    out["outcome_col"] = outcome_col
    return out


def richness_security_quadrants(
    frame: pd.DataFrame,
    *,
    richness_col: str = "taxonomy_n_eff",
    security_col: str = "RAX_h3_emotional_side",
    outcome_col: str = "rating_shrunk",
) -> pd.DataFrame:
    """Median-split richness × security; cell means of rating."""
    need = [richness_col, security_col, outcome_col]
    if any(c not in frame.columns for c in need):
        return pd.DataFrame()
    tmp = frame[need].dropna().copy()
    r_med = tmp[richness_col].median()
    s_med = tmp[security_col].median()
    tmp["richness_bin"] = np.where(tmp[richness_col] >= r_med, "high_richness", "low_richness")
    tmp["security_bin"] = np.where(tmp[security_col] >= s_med, "high_security", "low_security")
    rows = []
    for (rb, sb), sub in tmp.groupby(["richness_bin", "security_bin"], observed=True):
        rows.append(
            {
                "richness_bin": rb,
                "security_bin": sb,
                "n": int(len(sub)),
                "mean_rating": float(sub[outcome_col].mean()),
                "median_rating": float(sub[outcome_col].median()),
                "mean_richness": float(sub[richness_col].mean()),
                "mean_security": float(sub[security_col].mean()),
                "richness_median_cut": float(r_med),
                "security_median_cut": float(s_med),
            }
        )
    return pd.DataFrame(rows)


RICHNESS_CLIFF_FEATURES: Tuple[str, ...] = (
    "topic_n_eff",
    "taxonomy_n_eff",
    "construct_n_eff",
    "topic_top10",
    "taxonomy_top10",
    "construct_top10",
    "rare_topic_n_eff",
    "rare_taxonomy_n_eff",
    "rare_construct_n_eff",
)
