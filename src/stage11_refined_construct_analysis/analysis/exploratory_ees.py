"""Exploratory emotion / embodiment / social-world analysis helpers (NB15).

Does not alter confirmatory H1–H6 constructs. Reuses exploratory_security share
machinery and Stage 10 arc tertile helpers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import yaml

from src.stage10_correlation_analysis.analysis.arc import (
    TERTILE_ORDER,
    pivot_tertiles,
    tertile_deltas,
)
from src.stage11_refined_construct_analysis.analysis import exploratory_security as ex
from src.stage11_refined_construct_analysis.analysis.ees_discovery import (
    DEFAULT_EES_CONFIG,
    load_ees_config,
    load_stage11_from_ees,
)
from src.stage11_refined_construct_analysis.config import Stage11Config

DEFAULT_CONTROLS = ("log_pages", "n_sentences", "publication_year")


def load_exploratory_ees_config(path: Optional[Path] = None) -> Dict[str, Any]:
    return load_ees_config(path or DEFAULT_EES_CONFIG)


def is_frozen(ees_cfg: Mapping[str, Any]) -> bool:
    return bool(ees_cfg.get("frozen"))


def is_provisional(ees_cfg: Mapping[str, Any]) -> bool:
    return bool(ees_cfg.get("provisional", not is_frozen(ees_cfg)))


def construct_dictionary_frame(ees_cfg: Mapping[str, Any]) -> pd.DataFrame:
    """Flatten code_membership + families into a construct dictionary table."""
    rows: List[Dict[str, Any]] = []
    for family, codes in (ees_cfg.get("code_membership") or {}).items():
        if not isinstance(codes, dict):
            continue
        for code, tids in codes.items():
            for tid in tids or []:
                rows.append(
                    {
                        "layer": "code",
                        "family": family,
                        "construct": str(code),
                        "topic_id": int(tid),
                    }
                )
    for name, levels in (ees_cfg.get("families") or {}).items():
        if not isinstance(levels, dict):
            continue
        for level in ("strict", "moderate", "broad"):
            for tid in levels.get(level) or []:
                rows.append(
                    {
                        "layer": "family",
                        "family": name,
                        "construct": f"{name}_{level}",
                        "level": level,
                        "topic_id": int(tid),
                    }
                )
    for name, block in (ees_cfg.get("composites") or {}).items():
        codes = block.get("codes") or []
        fams = block.get("families") or []
        rows.append(
            {
                "layer": "composite",
                "family": name,
                "construct": name,
                "topic_id": -1,
                "codes": ",".join(str(c) for c in codes),
                "source_families": ",".join(str(f) for f in fams),
            }
        )
    return pd.DataFrame(rows)


def topic_ids_for_codes(
    ees_cfg: Mapping[str, Any],
    family: str,
    codes: Sequence[str],
) -> List[int]:
    membership = (ees_cfg.get("code_membership") or {}).get(family) or {}
    out: List[int] = []
    seen = set()
    for code in codes:
        for tid in membership.get(str(code)) or []:
            tid = int(tid)
            if tid not in seen:
                seen.add(tid)
                out.append(tid)
    return out


def topic_ids_for_family_level(
    ees_cfg: Mapping[str, Any],
    family: str,
    level: str = "moderate",
) -> List[int]:
    block = (ees_cfg.get("families") or {}).get(family) or {}
    return [int(t) for t in (block.get(level) or [])]


def composite_topic_ids(
    ees_cfg: Mapping[str, Any],
    composite: str,
    *,
    level: str = "moderate",
) -> List[int]:
    block = (ees_cfg.get("composites") or {}).get(composite) or {}
    seen = set()
    out: List[int] = []
    for fam in block.get("families") or []:
        for tid in topic_ids_for_family_level(ees_cfg, str(fam), level):
            if tid not in seen:
                seen.add(tid)
                out.append(tid)
    return out


def add_ees_share_columns(
    frame: pd.DataFrame,
    shares: pd.DataFrame,
    ees_cfg: Mapping[str, Any],
    *,
    level: str = "moderate",
    prefix: str = "EES",
) -> pd.DataFrame:
    """Add family, code, and composite share columns."""
    out = frame.copy()
    families = ees_cfg.get("families") or {}
    nested = {
        name: levels
        for name, levels in families.items()
        if isinstance(levels, dict) and any(k in levels for k in ("strict", "moderate", "broad"))
    }
    if nested:
        out = ex.add_topic_set_columns(out, shares, nested)
        for name in nested:
            src = f"EXP_{name}_{level}"
            dst = f"{prefix}_{name}"
            if src in out.columns:
                out[dst] = out[src]

    book_ids = out["book_id"].values if "book_id" in out.columns else out.index
    extra: Dict[str, np.ndarray] = {}

    for family, codes in (ees_cfg.get("code_membership") or {}).items():
        if not isinstance(codes, dict):
            continue
        for code, tids in codes.items():
            col = f"{prefix}_{code}"
            series = ex.topic_set_share(shares, [int(t) for t in (tids or [])])
            extra[col] = series.reindex(book_ids).fillna(0.0).to_numpy(dtype=float)

    for name in (ees_cfg.get("composites") or {}):
        tids = composite_topic_ids(ees_cfg, name, level=level)
        col = f"{prefix}_{name}"
        series = ex.topic_set_share(shares, tids)
        extra[col] = series.reindex(book_ids).fillna(0.0).to_numpy(dtype=float)

    if extra:
        out = pd.concat([out, pd.DataFrame(extra, index=out.index)], axis=1)

    eps = float(ees_cfg.get("epsilon", 1e-6))
    felt = f"{prefix}_felt_body"
    looked = f"{prefix}_looked_at_body"
    if felt in out.columns and looked in out.columns:
        out[f"{prefix}_felt_vs_looked_logratio"] = np.log(
            (out[felt].astype(float) + eps) / (out[looked].astype(float) + eps)
        )
    return out.copy()


def corpus_p75_threshold(share: pd.Series) -> float:
    return float(share.astype(float).quantile(0.75))


def presence_and_intensity_p75(
    share: pd.Series,
    *,
    threshold: Optional[float] = None,
) -> Dict[str, float]:
    """Presence above corpus-wide 75th percentile; intensity among those present."""
    s = share.astype(float)
    thr = float(threshold) if threshold is not None else corpus_p75_threshold(s)
    present = s > thr
    return {
        "threshold": thr,
        "prevalence": float(present.mean()),
        "conditional_intensity_mean": float(s[present].mean()) if present.any() else float("nan"),
        "conditional_intensity_median": float(s[present].median()) if present.any() else float("nan"),
        "unconditional_mean": float(s.mean()),
        "unconditional_median": float(s.median()),
        "n_present": int(present.sum()),
        "n_total": int(len(s)),
    }


def presence_intensity_by_group(
    frame: pd.DataFrame,
    share_col: str,
    *,
    group_col: str = "rating_class",
    high_label: str = "high_rate",
    low_label: str = "low_rate",
    threshold: Optional[float] = None,
) -> pd.DataFrame:
    """Corpus p75 gate; report P(present) and median(share|present) by rating group."""
    if share_col not in frame.columns:
        return pd.DataFrame()
    share = frame[share_col].astype(float)
    thr = float(threshold) if threshold is not None else corpus_p75_threshold(share)
    masks: List[Tuple[str, pd.Series]] = [("all", pd.Series(True, index=frame.index))]
    if group_col in frame.columns:
        masks.append(("high", frame[group_col] == high_label))
        masks.append(("low", frame[group_col] == low_label))
    rows = []
    for label, mask in masks:
        sub = share[mask]
        stats = presence_and_intensity_p75(sub, threshold=thr)
        stats["group"] = label
        stats["feature"] = share_col
        rows.append(stats)
    return pd.DataFrame(rows)


def load_tertile_topic_counts(cfg: Stage11Config) -> pd.DataFrame:
    path = cfg.input_path("tertile_topic_counts", required=False)
    if path is None or not path.exists():
        # Fallback beside book_topic_counts
        book_path = cfg.input_path("book_topic_counts", required=False)
        if book_path is not None:
            alt = book_path.parent / "tertile_topic_counts.parquet"
            if alt.exists():
                path = alt
    if path is None or not path.exists():
        raise FileNotFoundError("tertile_topic_counts.parquet not found")
    return pd.read_parquet(path)


def construct_tertile_shares(
    tertile_counts: pd.DataFrame,
    topic_ids: Sequence[int],
    *,
    feature_name: str,
) -> pd.DataFrame:
    """Aggregate topic shares within book×tertile for a construct."""
    tids = {int(t) for t in topic_ids}
    if not tids:
        return pd.DataFrame(columns=["book_id", "tertile", "feature", "share"])
    sub = tertile_counts[tertile_counts["topic_id"].isin(tids)].copy()
    if sub.empty:
        # Still emit zero rows for books present in tertile file
        books = tertile_counts[["book_id", "tertile"]].drop_duplicates()
        books = books.copy()
        books["feature"] = feature_name
        books["share"] = 0.0
        return books
    grouped = (
        sub.groupby(["book_id", "tertile"], as_index=False)["share"]
        .sum()
    )
    grouped["feature"] = feature_name
    return grouped[["book_id", "tertile", "feature", "share"]]


def position_effects_table(
    tertile_counts: pd.DataFrame,
    constructs: Mapping[str, Sequence[int]],
    frame: pd.DataFrame,
    *,
    test_fn,
    group_col: str = "rating_class",
    high_label: str = "high_rate",
    low_label: str = "low_rate",
    hyp: str = "EES",
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return (long tertile means by group, delta effects, trajectory means)."""
    long_parts = []
    for name, tids in constructs.items():
        long_parts.append(construct_tertile_shares(tertile_counts, tids, feature_name=name))
    if not long_parts:
        empty = pd.DataFrame()
        return empty, empty, empty
    long = pd.concat(long_parts, ignore_index=True)
    wide = pivot_tertiles(long)
    deltas = tertile_deltas(wide, list(constructs.keys()), contrasts=(("end", "begin"),))

    # Attach rating tier + covariates needed by test_axis / OLS
    meta_cols = ["book_id"]
    for c in (
        group_col,
        "rating_shrunk",
        "author_id",
        "reliability",
        "log_pages",
        "n_sentences",
        "publication_year",
        "genre_group",
        "log_n_ratings",
        "analysable",
    ):
        if c in frame.columns and c not in meta_cols:
            meta_cols.append(c)
    meta = frame[meta_cols].drop_duplicates("book_id")
    delta_frame = deltas.reset_index()
    if "book_id" not in delta_frame.columns:
        delta_frame = delta_frame.rename(columns={delta_frame.columns[0]: "book_id"})
    delta_frame = delta_frame.merge(meta, on="book_id", how="left")

    effect_rows = []
    for name in constructs:
        col = f"{name}__end_minus_begin"
        if col not in delta_frame.columns:
            continue
        tmp = delta_frame.dropna(subset=[col, group_col]).copy()
        if tmp.columns.duplicated().any():
            tmp = tmp.loc[:, ~tmp.columns.duplicated()].copy()
        res = test_fn(tmp, col, hyp, label=f"{name}_arc")
        effect_rows.append(
            {
                "construct": name,
                "contrast": "end_minus_begin",
                "cliffs_delta": res.get("cliffs_delta"),
                "ci_low": res.get("ci_low"),
                "ci_high": res.get("ci_high"),
                "verdict": res.get("verdict"),
            }
        )
    effects = pd.DataFrame(effect_rows)

    # Mean trajectories by group
    long_meta = long.merge(meta[["book_id", group_col]], on="book_id", how="left")
    traj = (
        long_meta.groupby(["feature", "tertile", group_col], observed=True)["share"]
        .mean()
        .reset_index()
    )
    return traj, effects, delta_frame


def coherence_gate(
    shares: pd.DataFrame,
    topic_ids: Sequence[int],
    *,
    construct: str,
    mass_flag: float = 0.50,
) -> Dict[str, Any]:
    """0 topics → unmeasurable; 1–2 → thin; ≥3 → measurable; flag single-topic dominance."""
    tids = [int(t) for t in topic_ids if int(t) in shares.columns]
    n = len(tids)
    if n == 0:
        status = "unmeasurable"
    elif n <= 2:
        status = "thin"
    else:
        status = "measurable"

    masses = {}
    total = 0.0
    for tid in tids:
        m = float(shares[tid].sum())
        masses[tid] = m
        total += m
    largest_tid = None
    largest_share = float("nan")
    if total > 0 and masses:
        largest_tid = max(masses, key=masses.get)
        largest_share = masses[largest_tid] / total

    return {
        "construct": construct,
        "n_topics": n,
        "topic_ids": ",".join(str(t) for t in tids),
        "status": status,
        "largest_topic_id": largest_tid,
        "largest_topic_mass_share": largest_share,
        "single_topic_dominated": bool(
            n > 0 and np.isfinite(largest_share) and largest_share > mass_flag
        ),
        "total_mass": total,
    }


def coherence_table(
    shares: pd.DataFrame,
    constructs: Mapping[str, Sequence[int]],
) -> pd.DataFrame:
    return pd.DataFrame(
        [coherence_gate(shares, tids, construct=name) for name, tids in constructs.items()]
    )


def author_half_split(
    frame: pd.DataFrame,
    *,
    author_col: str = "author_id",
    seed: int = 42,
) -> pd.Series:
    """Assign each author to half A or B; return book-aligned series of 'A'/'B'."""
    if author_col not in frame.columns:
        raise KeyError(author_col)
    authors = sorted({a for a in frame[author_col].dropna().unique()})
    rng = np.random.default_rng(seed)
    perm = list(authors)
    rng.shuffle(perm)
    mid = len(perm) // 2
    assign = {a: ("A" if i < mid else "B") for i, a in enumerate(perm)}
    return frame[author_col].map(assign)


def author_split_stability(
    frame: pd.DataFrame,
    features: Sequence[str],
    *,
    test_fn,
    author_col: str = "author_id",
    seed: int = 42,
    hyp: str = "EES",
) -> pd.DataFrame:
    """Cliff's δ on full sample and author-disjoint halves A/B."""
    halves = author_half_split(frame, author_col=author_col, seed=seed)
    work = frame.copy()
    work["_author_half"] = halves.values
    rows = []
    for feat in features:
        if feat not in work.columns:
            continue
        row: Dict[str, Any] = {"construct": feat}
        for label, mask in (
            ("full", pd.Series(True, index=work.index)),
            ("half_A", work["_author_half"] == "A"),
            ("half_B", work["_author_half"] == "B"),
        ):
            sub = work.loc[mask]
            if len(sub) < 20:
                row[f"delta_{label}"] = float("nan")
                row[f"n_{label}"] = int(len(sub))
                continue
            res = test_fn(sub, feat, hyp, label=f"{feat}_{label}")
            row[f"delta_{label}"] = res.get("cliffs_delta")
            row[f"ci_low_{label}"] = res.get("ci_low")
            row[f"ci_high_{label}"] = res.get("ci_high")
            row[f"n_{label}"] = int(len(sub))
        rows.append(row)
    return pd.DataFrame(rows)


def social_domain_richness(
    frame: pd.DataFrame,
    shares: pd.DataFrame,
    domains: Mapping[str, Sequence[int]],
    *,
    threshold_mode: str = "corpus_p75",
) -> pd.Series:
    """Count domains with book share above corpus p75 (meaningful presence)."""
    present_mat = []
    for name, tids in domains.items():
        series = ex.topic_set_share(shares, [int(t) for t in (tids or [])])
        if "book_id" in frame.columns:
            aligned = series.reindex(frame["book_id"].values).fillna(0.0)
        else:
            aligned = series.reindex(frame.index).fillna(0.0)
        if not (tids or []):
            present_mat.append(pd.Series(False, index=aligned.index))
            continue
        thr = corpus_p75_threshold(aligned) if threshold_mode == "corpus_p75" else 1e-5
        present_mat.append(aligned > thr)
    if not present_mat:
        return pd.Series(0, index=frame.index)
    stacked = pd.concat(present_mat, axis=1)
    return stacked.sum(axis=1).astype(int)


def interaction_ols(
    frame: pd.DataFrame,
    x_col: str,
    y_col: str,
    *,
    quality: str = "rating_shrunk",
    controls: Optional[Sequence[str]] = None,
    name: str = "interaction",
) -> Dict[str, Any]:
    """Standardized x + y + x×y OLS with Stage 10 controls."""
    from src.stage10_correlation_analysis.analysis import models as mdl

    controls = list(controls or DEFAULT_CONTROLS)
    controls = [c for c in controls if c in frame.columns]
    categorical = [c for c in ["genre_group"] if c in frame.columns]
    if x_col not in frame.columns or y_col not in frame.columns:
        return {"status": "absent", "x": x_col, "y": y_col}
    work = frame.copy()
    def _z(s: pd.Series) -> pd.Series:
        x = s.astype(float)
        sd = float(x.std(ddof=0))
        if not np.isfinite(sd) or sd <= 0:
            return pd.Series(0.0, index=s.index)
        return (x - float(x.mean())) / sd

    work["z_x"] = _z(work[x_col].fillna(0.0))
    work["z_y"] = _z(work[y_col].fillna(0.0))
    work["z_x_z_y"] = work["z_x"] * work["z_y"]
    fit = mdl.fit_ols(
        work.reset_index() if work.index.name else work,
        quality,
        ["z_x", "z_y", "z_x_z_y", *controls],
        categorical=categorical,
        cluster="author_id" if "author_id" in work.columns else None,
        weights="reliability" if "reliability" in work.columns else None,
        name=name,
    )
    coef = fit.coefficients
    out: Dict[str, Any] = {"status": "ok", "x": x_col, "y": y_col, "name": name}
    for term, label in (("z_x", "z_x"), ("z_y", "z_y"), ("z_x_z_y", "interaction")):
        row = coef[coef["term"] == term]
        if len(row):
            out[label] = {
                "beta": float(row.iloc[0]["coefficient"]),
                "se": float(row.iloc[0]["std_error"]),
                "p": float(row.iloc[0]["p_value"]),
                "ci_low": float(row.iloc[0]["ci_low"]),
                "ci_high": float(row.iloc[0]["ci_high"]),
            }
    return out


def median_split_quadrants(
    frame: pd.DataFrame,
    x_col: str,
    y_col: str,
    *,
    quality: str = "rating_shrunk",
    x_high: str = "high_x",
    x_low: str = "low_x",
    y_high: str = "high_y",
    y_low: str = "low_y",
) -> pd.DataFrame:
    """Descriptive 2×2 mean ratings (not causal)."""
    if x_col not in frame.columns or y_col not in frame.columns or quality not in frame.columns:
        return pd.DataFrame()
    tmp = frame[[x_col, y_col, quality]].dropna().copy()
    x_med = float(tmp[x_col].median())
    y_med = float(tmp[y_col].median())
    tmp["x_bin"] = np.where(tmp[x_col] >= x_med, x_high, x_low)
    tmp["y_bin"] = np.where(tmp[y_col] >= y_med, y_high, y_low)
    rows = []
    for (xb, yb), sub in tmp.groupby(["x_bin", "y_bin"], observed=True):
        rows.append(
            {
                "x_bin": xb,
                "y_bin": yb,
                "n": int(len(sub)),
                "mean_rating": float(sub[quality].mean()),
                "median_rating": float(sub[quality].median()),
                "x_median_cut": x_med,
                "y_median_cut": y_med,
            }
        )
    return pd.DataFrame(rows)


def forest_plot(
    effects: pd.DataFrame,
    *,
    label_col: str = "construct",
    delta_col: str = "cliffs_delta",
    ci_low_col: str = "ci_low",
    ci_high_col: str = "ci_high",
    title: str = "",
    ax=None,
):
    """Horizontal forest plot of Cliff's δ with CIs."""
    import matplotlib.pyplot as plt

    df = effects.dropna(subset=[delta_col]).copy()
    if df.empty:
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.set_title(title or "No effects")
        return fig, ax
    df = df.sort_values(delta_col)
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, max(2.5, 0.35 * len(df) + 1)))
    else:
        fig = ax.figure
    y = np.arange(len(df))
    lo = df[ci_low_col].astype(float) if ci_low_col in df.columns else df[delta_col]
    hi = df[ci_high_col].astype(float) if ci_high_col in df.columns else df[delta_col]
    # Replace non-finite CIs with the point estimate so errorbar does not fail
    lo = lo.where(np.isfinite(lo), df[delta_col])
    hi = hi.where(np.isfinite(hi), df[delta_col])
    ax.errorbar(
        df[delta_col],
        y,
        xerr=[
            (df[delta_col] - lo).clip(lower=0),
            (hi - df[delta_col]).clip(lower=0),
        ],
        fmt="o",
        color="0.2",
        ecolor="0.5",
        capsize=3,
    )
    ax.axvline(0.0, color="0.6", lw=1)
    ax.set_yticks(y)
    ax.set_yticklabels(df[label_col].astype(str).tolist())
    ax.set_xlabel("Cliff's δ (high vs low rated)")
    if title:
        ax.set_title(title)
    fig.tight_layout()
    return fig, ax


def trajectory_plot(
    traj: pd.DataFrame,
    *,
    feature: str,
    group_col: str = "rating_class",
    title: str = "",
    ax=None,
):
    """Begin–middle–end mean share lines for high vs low."""
    import matplotlib.pyplot as plt

    sub = traj[traj["feature"] == feature].copy()
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 3.5))
    else:
        fig = ax.figure
    order = list(TERTILE_ORDER)
    for group, g in sub.groupby(group_col, observed=True):
        g = g.set_index("tertile").reindex(order)
        ax.plot(order, g["share"].values, marker="o", label=str(group))
    ax.set_xlabel("Narrative position")
    ax.set_ylabel("Mean theme share")
    ax.set_title(title or feature)
    ax.legend(title=group_col)
    fig.tight_layout()
    return fig, ax


def active_constructs(
    ees_cfg: Mapping[str, Any],
    *,
    level: str = "moderate",
) -> Dict[str, List[int]]:
    """Family name → topic ids at the chosen breadth level."""
    out: Dict[str, List[int]] = {}
    for name in (ees_cfg.get("families") or {}):
        out[name] = topic_ids_for_family_level(ees_cfg, name, level)
    for name in (ees_cfg.get("composites") or {}):
        out[name] = composite_topic_ids(ees_cfg, name, level=level)
    return out
