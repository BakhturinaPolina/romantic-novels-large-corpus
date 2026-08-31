"""Presentation / exploratory helpers for Stage 11 notebooks 13–16.

All functions here support *exploratory* or *display* analyses unless called from
notebook 13's confirmatory battery. Residual Goodreads outcomes live only in Stage 11.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from src.stage11_refined_construct_analysis.config import Stage11Config

# Fixed presentation set for attention waterfall (refined atoms; not a full partition).
ATTENTION_THEMES: Tuple[Tuple[str, str], ...] = (
    ("RAX_h3_emotional_side", "emotional reassurance/security"),
    ("RAX_external_danger_crisis", "external danger"),
    ("RAX_tenderness_core", "tenderness"),
    ("RAX_nonexplicit_affection", "non-explicit affection"),
    ("RAX_external_protection", "enacted protection"),
    ("RAX_repair", "repair"),
    ("RAX_relational_darkness", "relational darkness / conflict"),
    ("RAX_explicit_sex", "explicit sex"),
    ("RAX_appearance_grooming", "appearance / grooming"),
    ("RAX_h4_possession_side", "possession / control"),
)

DOSE_RESPONSE_FEATURES: Tuple[str, ...] = (
    "RAX_h3_emotional_side",
    "RAX_appearance_grooming",
    "RAX_tenderness_core",
    "RAX_external_danger_crisis",
    "RAX_explicit_sex",
    "RAX_external_protection",
    "RAX_relational_darkness",
)

HEADLINE_THEMES_FOR_HEATMAP: Tuple[str, ...] = (
    "RAX_h3_emotional_side",
    "RAX_appearance_grooming",
    "RAX_external_danger_crisis",
    "RAX_tenderness_core",
    "RAX_explicit_sex",
    "RAX_external_protection",
    "RAX_h4_possession_side",
    "RAX_nonexplicit_affection",
    "RARC",
)


def notebook_tables_dir(cfg: Stage11Config, notebook: str) -> Path:
    return cfg.output_path("notebook_dir", create=False) / notebook / "tables"


def load_notebook_table(
    cfg: Stage11Config,
    notebook: str,
    name: str,
) -> pd.DataFrame:
    """Load a parquet/csv table written by a prior Stage 11 notebook."""
    base = notebook_tables_dir(cfg, notebook)
    pq = base / f"{name}.parquet"
    csv = base / f"{name}.csv"
    if pq.exists():
        return pd.read_parquet(pq)
    if csv.exists():
        return pd.read_csv(csv)
    raise FileNotFoundError(f"Missing notebook table: {pq} (or .csv)")


def add_year_bin(
    frame: pd.DataFrame,
    *,
    year_col: str = "publication_year",
    bins: Sequence[float] = (1999.5, 2010.5, 2014.5, 2018.5),
    labels: Sequence[str] = ("2000-2010", "2011-2014", "2015-2017"),
) -> pd.DataFrame:
    """Coarse era bins matching the 2000–2017 corpus window."""
    out = frame.copy()
    if year_col not in out.columns:
        out["year_bin"] = "unknown"
        return out
    out["year_bin"] = pd.cut(
        out[year_col].astype(float),
        bins=list(bins),
        labels=list(labels),
        include_lowest=True,
    ).astype(str)
    return out


def residualize_outcomes(
    frame: pd.DataFrame,
    *,
    quality: str = "rating_shrunk",
    reach: str = "log_n_ratings",
    numeric_controls: Sequence[str] = ("publication_year", "log_pages", "n_sentences"),
    genre_col: str = "genre_group",
) -> pd.DataFrame:
    """Residual quality/reach after year, length, and genre.

    A residual answers: how much better/worse did this book perform than expected
    from basic background characteristics?
    """
    from src.stage10_correlation_analysis.analysis.compositional import residualise

    out = frame.copy()
    controls = [c for c in numeric_controls if c in out.columns]
    cov_parts: List[pd.DataFrame] = []
    if controls:
        cov_parts.append(out[list(controls)].astype(float))
    if genre_col in out.columns:
        dummies = pd.get_dummies(out[genre_col].astype(str), prefix="genre", drop_first=True)
        cov_parts.append(dummies.astype(float))
    if not cov_parts:
        out["quality_resid"] = out[quality] - out[quality].mean() if quality in out.columns else np.nan
        out["reach_resid"] = out[reach] - out[reach].mean() if reach in out.columns else np.nan
        return out

    cov = pd.concat(cov_parts, axis=1)
    # Drop rows with missing covariates for residualisation; fill others with NaN.
    valid = cov.notna().all(axis=1)
    if quality in out.columns:
        resid_q = pd.Series(np.nan, index=out.index, name="quality_resid")
        if valid.any():
            r = residualise(out.loc[valid, quality].astype(float), cov.loc[valid])
            resid_q.loc[valid] = r.values
        out["quality_resid"] = resid_q
    if reach in out.columns:
        resid_r = pd.Series(np.nan, index=out.index, name="reach_resid")
        if valid.any():
            r = residualise(out.loc[valid, reach].astype(float), cov.loc[valid])
            resid_r.loc[valid] = r.values
        out["reach_resid"] = resid_r
    return out


def residual_goodreads_quadrants(
    frame: pd.DataFrame,
    *,
    quality_resid: str = "quality_resid",
    reach_resid: str = "reach_resid",
) -> pd.DataFrame:
    """Median-split residual quality × residual reach into four labels."""
    out = frame.copy()
    q = out[quality_resid]
    r = out[reach_resid]
    q_med = q.median()
    r_med = r.median()
    labels = []
    for qv, rv in zip(q, r):
        if not (np.isfinite(qv) and np.isfinite(rv)):
            labels.append("missing")
            continue
        high_q = qv >= q_med
        high_r = rv >= r_med
        if high_q and high_r:
            labels.append("stars")
        elif high_q and not high_r:
            labels.append("hidden_gems")
        elif (not high_q) and high_r:
            labels.append("popular_but_poor")
        else:
            labels.append("low_low")
    out["residual_quadrant"] = labels
    return out


def quadrant_theme_means(
    frame: pd.DataFrame,
    themes: Sequence[str],
    *,
    quadrant_col: str = "residual_quadrant",
) -> pd.DataFrame:
    """Mean theme share by residual Goodreads quadrant."""
    present = [t for t in themes if t in frame.columns]
    if not present or quadrant_col not in frame.columns:
        return pd.DataFrame()
    usable = frame[frame[quadrant_col] != "missing"]
    rows = []
    for quad, sub in usable.groupby(quadrant_col, observed=True):
        row: Dict[str, Any] = {"quadrant": quad, "n_books": int(len(sub))}
        for t in present:
            row[t] = float(sub[t].mean())
        rows.append(row)
    return pd.DataFrame(rows)


def attention_waterfall(
    frame: pd.DataFrame,
    themes: Sequence[Tuple[str, str]] = ATTENTION_THEMES,
    *,
    tier_col: str = "rating_class",
    high: str = "high_rate",
    low: str = "low_rate",
) -> pd.DataFrame:
    """High − low mean share for a fixed presentation theme list."""
    rows = []
    for col, label in themes:
        if col not in frame.columns:
            continue
        hi = frame.loc[frame[tier_col] == high, col].dropna()
        lo = frame.loc[frame[tier_col] == low, col].dropna()
        if hi.empty or lo.empty:
            continue
        mean_hi = float(hi.mean())
        mean_lo = float(lo.mean())
        rows.append(
            {
                "feature": col,
                "label": label,
                "mean_high": mean_hi,
                "mean_low": mean_lo,
                "diff_pp": 100.0 * (mean_hi - mean_lo),
                "diff": mean_hi - mean_lo,
                "n_high": int(hi.size),
                "n_low": int(lo.size),
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values("diff", ascending=False).reset_index(drop=True)


def dose_response_curve(
    frame: pd.DataFrame,
    feature: str,
    *,
    outcome: str = "quality_resid",
    n_bins: int = 10,
) -> pd.DataFrame:
    """Decile of theme share → mean adjusted quality (or other residual outcome)."""
    if feature not in frame.columns or outcome not in frame.columns:
        return pd.DataFrame()
    work = frame[[feature, outcome]].dropna().copy()
    if len(work) < n_bins * 5:
        return pd.DataFrame()
    try:
        work["decile"] = pd.qcut(work[feature], q=n_bins, labels=False, duplicates="drop") + 1
    except ValueError:
        return pd.DataFrame()
    rows = []
    for dec, g in work.groupby("decile", observed=True):
        rows.append(
            {
                "decile": int(dec),
                "n": int(len(g)),
                "feature_mean": float(g[feature].mean()),
                "outcome_mean": float(g[outcome].mean()),
                "outcome_median": float(g[outcome].median()),
                "feature": feature,
                "outcome": outcome,
            }
        )
    return pd.DataFrame(rows)


def dose_response_panel(
    frame: pd.DataFrame,
    features: Sequence[str] = DOSE_RESPONSE_FEATURES,
    *,
    outcome: str = "quality_resid",
    n_bins: int = 10,
) -> pd.DataFrame:
    parts = [dose_response_curve(frame, f, outcome=outcome, n_bins=n_bins) for f in features]
    parts = [p for p in parts if not p.empty]
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()


def conflict_repair_interaction(
    frame: pd.DataFrame,
    *,
    conflict_col: str = "RAX_relational_darkness",
    repair_col: str = "RAX_repair",
    quality: str = "rating_shrunk",
    controls: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """OLS with conflict × repair interaction (exploratory; mirrors danger × protection)."""
    from src.stage10_correlation_analysis.analysis import models as mdl

    controls = list(controls or ["log_pages", "n_sentences", "publication_year"])
    controls = [c for c in controls if c in frame.columns]
    categorical = [c for c in ["genre_group"] if c in frame.columns]
    work = frame.copy()
    if conflict_col not in work.columns or repair_col not in work.columns:
        return {"status": "absent", "conflict": conflict_col, "repair": repair_col}
    work["_conflict"] = work[conflict_col].fillna(0.0)
    work["_repair"] = work[repair_col].fillna(0.0)
    work["_conflict_x_repair"] = work["_conflict"] * work["_repair"]
    fit = mdl.fit_ols(
        work.reset_index() if work.index.name else work,
        quality,
        ["_conflict", "_repair", "_conflict_x_repair", *controls],
        categorical=categorical,
        cluster="author_id" if "author_id" in work.columns else None,
        weights="reliability" if "reliability" in work.columns else None,
        name=f"{conflict_col}_x_{repair_col}",
    )
    coef = fit.coefficients
    out: Dict[str, Any] = {"status": "ok", "conflict": conflict_col, "repair": repair_col}
    for term in ("_conflict", "_repair", "_conflict_x_repair"):
        row = coef[coef["term"] == term]
        if len(row):
            out[term] = {
                "beta": float(row.iloc[0]["coefficient"]),
                "se": float(row.iloc[0]["std_error"]),
                "p": float(row.iloc[0]["p_value"]),
                "ci_low": float(row.iloc[0]["ci_low"]),
                "ci_high": float(row.iloc[0]["ci_high"]),
            }
    return out


def interaction_to_frame(result: Mapping[str, Any], *, name: str) -> pd.DataFrame:
    rows = []
    for term, payload in result.items():
        if not isinstance(payload, dict) or "beta" not in payload:
            continue
        rows.append({"interaction": name, "term": term, **payload})
    return pd.DataFrame(rows)


def subgroup_cliffs_heatmap(
    frame: pd.DataFrame,
    features: Sequence[str],
    *,
    group_cols: Sequence[str] = ("genre_group", "year_bin"),
    tier_col: str = "rating_class",
    high: str = "high_rate",
    low: str = "low_rate",
    min_n_per_tier: int = 80,
) -> pd.DataFrame:
    """Cliff's δ for each feature within genre and era subgroups."""
    from src.stage10_correlation_analysis.analysis.effects import cliffs_delta

    rows = []
    for gcol in group_cols:
        if gcol not in frame.columns:
            continue
        for gval, subset in frame.groupby(gcol, observed=True):
            a = subset.loc[subset[tier_col] == high]
            b = subset.loc[subset[tier_col] == low]
            if len(a) < min_n_per_tier or len(b) < min_n_per_tier:
                continue
            for feat in features:
                if feat not in subset.columns:
                    continue
                aa = a[feat].dropna().to_numpy(dtype=float)
                bb = b[feat].dropna().to_numpy(dtype=float)
                if aa.size < 20 or bb.size < 20:
                    continue
                try:
                    d = cliffs_delta(aa, bb)
                except ValueError:
                    continue
                rows.append(
                    {
                        "feature": feat,
                        "group_type": gcol,
                        "group": str(gval),
                        "cliffs_delta": float(d),
                        "n_high": int(aa.size),
                        "n_low": int(bb.size),
                    }
                )
    return pd.DataFrame(rows)


def standardized_two_channel_betas(
    frame: pd.DataFrame,
    features: Sequence[str],
    *,
    quality: str = "rating_shrunk",
    reach: str = "log_n_ratings",
    controls: Optional[Sequence[str]] = None,
    quality_weights: Optional[str] = "reliability",
    reach_weights: Optional[str] = None,
    cluster: Optional[str] = "author_id",
) -> pd.DataFrame:
    """Standardised partial betas on quality and reach for quadrant plots.

    By default the quality channel uses reliability WLS (matching Stage 10
    Notebook 06) while reach remains unweighted OLS. Pass ``quality_weights=None``
    to recover the older unweighted behaviour.
    """
    from src.stage10_correlation_analysis.analysis import models as mdl

    controls = list(controls or ["log_pages", "n_sentences", "publication_year"])
    controls = [c for c in controls if c in frame.columns]
    categorical = [c for c in ["genre_group"] if c in frame.columns]
    work = frame.copy()
    cluster_col = cluster if cluster and cluster in work.columns else None
    q_w = quality_weights if quality_weights and quality_weights in work.columns else None
    r_w = reach_weights if reach_weights and reach_weights in work.columns else None

    # Standardise continuous columns used in the model
    for col in [quality, reach, *features, *controls]:
        if col in work.columns and pd.api.types.is_numeric_dtype(work[col]):
            mu, sd = work[col].mean(), work[col].std(ddof=0)
            if sd and np.isfinite(sd) and sd > 0:
                work[f"{col}__z"] = (work[col] - mu) / sd
            else:
                work[f"{col}__z"] = np.nan

    rows = []
    for feat in features:
        if feat not in frame.columns:
            continue
        pred = f"{feat}__z"
        if pred not in work.columns:
            continue
        # Skip zero-variance / all-missing predictors (never fabricate beta=0).
        feat_sd = float(frame[feat].std(ddof=0)) if pd.api.types.is_numeric_dtype(frame[feat]) else 0.0
        if not (np.isfinite(feat_sd) and feat_sd > 0):
            continue
        if work[pred].notna().sum() < 10:
            continue
        ctrl_z = [f"{c}__z" for c in controls if f"{c}__z" in work.columns]
        channel_specs = (
            (f"{quality}__z", "quality", q_w),
            (f"{reach}__z", "reach", r_w),
        )
        for outcome, label, weights in channel_specs:
            if outcome not in work.columns or work[outcome].notna().sum() < 10:
                continue
            fit = mdl.fit_ols(
                work.reset_index() if work.index.name else work,
                outcome,
                [pred, *ctrl_z],
                categorical=categorical,
                cluster=cluster_col,
                weights=weights,
                name=f"{feat}->{label}",
            )
            row = fit.coefficients[fit.coefficients["term"] == pred]
            if row.empty:
                continue
            r0 = row.iloc[0]
            rows.append(
                {
                    "feature": feat,
                    "channel": label,
                    "beta_std": float(r0["coefficient"]),
                    "se": float(r0["std_error"]),
                    "p": float(r0["p_value"]),
                    "ci_low": float(r0["ci_low"]),
                    "ci_high": float(r0["ci_high"]),
                    "n_obs": int(fit.n_obs),
                    "n_clusters": int(fit.n_clusters) if fit.n_clusters is not None else np.nan,
                }
            )
    return pd.DataFrame(rows)


def pivot_two_channel_betas(long: pd.DataFrame) -> pd.DataFrame:
    """Pivot long two-channel betas to wide quality_/reach_ columns + gaps."""
    if long is None or long.empty:
        return pd.DataFrame()
    parts = []
    for channel, prefix in (("quality", "quality"), ("reach", "reach")):
        sub = long.loc[long["channel"] == channel].copy()
        if sub.empty:
            continue
        keep = {
            "feature": "feature",
            "beta_std": f"{prefix}_beta",
            "se": f"{prefix}_se",
            "p": f"{prefix}_p",
            "ci_low": f"{prefix}_ci_low",
            "ci_high": f"{prefix}_ci_high",
            "n_obs": f"{prefix}_n_obs",
            "n_clusters": f"{prefix}_n_clusters",
        }
        present = {k: v for k, v in keep.items() if k in sub.columns}
        parts.append(sub[list(present)].rename(columns=present))
    if not parts:
        return pd.DataFrame()
    wide = parts[0]
    for part in parts[1:]:
        wide = wide.merge(part, on="feature", how="outer")
    if "quality_beta" in wide.columns and "reach_beta" in wide.columns:
        wide["beta_gap"] = wide["quality_beta"] - wide["reach_beta"]
        wide["abs_beta_gap"] = wide["beta_gap"].abs()
    return wide.reset_index(drop=True)


def flag_channel_reliability(
    wide: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """BH-FDR within each channel + reliable flags (q < alpha and CI excludes 0).

    Descriptive screening only — does not alter Notebook 13 confirmatory FDR.
    """
    from src.stage10_correlation_analysis.analysis import tests as tst

    out = wide.copy()
    for channel in ("quality", "reach"):
        p_col = f"{channel}_p"
        if p_col not in out.columns:
            out[f"{channel}_q"] = np.nan
            out[f"{channel}_reliable"] = False
            continue
        out[f"{channel}_q"] = tst.benjamini_hochberg(out[p_col].to_numpy(dtype=float))
        ci_lo = out.get(f"{channel}_ci_low")
        ci_hi = out.get(f"{channel}_ci_high")
        if ci_lo is None or ci_hi is None:
            out[f"{channel}_reliable"] = False
            continue
        ci_excludes_zero = np.sign(ci_lo.to_numpy(dtype=float)) == np.sign(
            ci_hi.to_numpy(dtype=float)
        )
        # Treat CI that includes exact zeros / NaNs as not excluding zero.
        finite_ci = np.isfinite(ci_lo.to_numpy(dtype=float)) & np.isfinite(
            ci_hi.to_numpy(dtype=float)
        )
        touches_zero = (ci_lo.to_numpy(dtype=float) <= 0) & (ci_hi.to_numpy(dtype=float) >= 0)
        out[f"{channel}_reliable"] = (
            (out[f"{channel}_q"] < alpha) & finite_ci & (~touches_zero) & ci_excludes_zero
        )
    return out


def classify_channel_pattern(row: Mapping[str, Any] | pd.Series) -> str:
    """Reliability-aware quality/reach pattern (NB06-style; not raw-sign only)."""
    q_ok = bool(row.get("quality_reliable", False))
    r_ok = bool(row.get("reach_reliable", False))
    q_beta = row.get("quality_beta", np.nan)
    r_beta = row.get("reach_beta", np.nan)
    if q_ok and r_ok:
        if np.sign(float(q_beta)) == np.sign(float(r_beta)):
            return "both_same_sign"
        return "opposite_signs"
    if q_ok:
        return "quality_only"
    if r_ok:
        return "reach_only"
    return "neither"


def classify_quality_reach_quadrant(quality_beta: float, reach_beta: float) -> str:
    """Legacy sign-only quadrant label (kept for NB14 callers). Prefer
    :func:`classify_channel_pattern` for reliability-aware classification.
    """
    q_pos = quality_beta > 0
    r_pos = reach_beta > 0
    if q_pos and not r_pos:
        return "quality_only"
    if r_pos and not q_pos:
        return "reach_only"
    if q_pos and r_pos:
        return "both"
    return "neither_or_opposite"


def topic_presentation_card(
    cfg: Stage11Config,
    topic_id: int,
    master: Optional[pd.DataFrame] = None,
    *,
    n_sentences: int = 1,
) -> Dict[str, Any]:
    """Topic id + label + taxonomy + words + one deterministic example sentence."""
    from src.stage11_refined_construct_analysis.audits.runner import load_evidence_packet

    packet = load_evidence_packet(cfg, int(topic_id)) or {}
    lexical = (packet.get("lexical") or {}).get("representations") or {}
    words = list(lexical.get("Main") or [])[:12]
    sents = (packet.get("contextual") or {}).get("sentences") or []
    example = ""
    if sents:
        # Deterministic: first sentence sorted by sid
        ordered = sorted(sents, key=lambda s: str(s.get("sid") or ""))
        example = str(ordered[0].get("sentence") or "")

    label = ""
    tax = ""
    if master is not None and len(master):
        row = master[master["topic_id"] == int(topic_id)]
        if len(row):
            label = str(row.iloc[0].get("current_topic_label") or "")
            tax = str(row.iloc[0].get("current_taxonomy_id") or "")

    return {
        "topic_id": int(topic_id),
        "topic_label": label,
        "taxonomy_id": tax,
        "top_words": ", ".join(words),
        "example_sentence": example[:400],
    }


def sample_theme_book_cells(
    frame: pd.DataFrame,
    feature: str,
    *,
    tier_col: str = "rating_class",
    high: str = "high_rate",
    low: str = "low_rate",
    books_per_cell: int = 3,
    seed: int = 42,
) -> pd.DataFrame:
    """Deterministic 2×2 extreme books for qualitative presentation."""
    from src.stage10_correlation_analysis.analysis import qual

    work = frame
    if "book_id" in work.columns:
        work = work.set_index("book_id")
    extras = [c for c in ("rating_shrunk", "log_n_ratings", "genre_group", "publication_year", "author_id") if c in work.columns]
    return qual.sample_extreme_books(
        work,
        feature,
        tier_col,
        tier_high=high,
        tier_low=low,
        quantiles=(0.1, 0.9),
        books_per_cell=books_per_cell,
        seed=seed,
        extra_columns=extras,
    )


def traffic_light_from_stability(
    stability: pd.DataFrame,
    *,
    gate: float = 0.11,
) -> pd.DataFrame:
    """Compact traffic-light table from NB11 stability_summary."""
    rows = []
    for _, r in stability.iterrows():
        feat = r.get("feature")
        sign_ok = bool(r.get("sign_stable"))
        clears = bool(r.get("any_clears_gate"))
        mgate = str(r.get("measurement_gate") or "")
        if mgate == "unmeasurable":
            overall = "unmeasurable"
            light = "—"
        elif mgate == "thin":
            overall = "thin / provisional"
            light = "⚠"
        elif sign_ok and clears:
            overall = "strong"
            light = "✓"
        elif sign_ok:
            overall = "moderate (below gate in some specs)"
            light = "⚠"
        else:
            overall = "sensitive"
            light = "✗"
        rows.append(
            {
                "feature": feat,
                "measurement_gate": mgate,
                "sign_stable": sign_ok,
                "clears_gate_any_spec": clears,
                "min_abs_delta": r.get("min_abs_delta"),
                "max_abs_delta": r.get("max_abs_delta"),
                "light": light,
                "overall": overall,
            }
        )
    return pd.DataFrame(rows)


def final_verdict_rows(
    primary_effects: pd.DataFrame,
    *,
    claim_notes: Optional[Mapping[str, str]] = None,
) -> pd.DataFrame:
    """One-sentence final verdict table for H1–H6 primaries."""
    notes = dict(claim_notes or {})
    rows = []
    for _, r in primary_effects.iterrows():
        hyp = r.get("hypothesis")
        verdict = str(r.get("verdict") or "")
        if "unmeasurable" in verdict:
            bucket = "unmeasurable"
        elif verdict.startswith("thin:"):
            bucket = "inconclusive"
            verdict = verdict.split(":", 1)[-1]
        elif verdict == "supported":
            bucket = "supported"
        elif "directionally" in verdict:
            bucket = "directional"
        elif verdict == "contradicted":
            bucket = "contradicted"
        else:
            bucket = "inconclusive"
        sentence = notes.get(str(hyp), "")
        if not sentence:
            feat = r.get("feature")
            d = r.get("cliffs_delta")
            sentence = f"{feat}: verdict={verdict}; δ={d}"
        rows.append(
            {
                "hypothesis": hyp,
                "feature": r.get("feature"),
                "measurement_gate": r.get("measurement_gate"),
                "cliffs_delta": r.get("cliffs_delta"),
                "verdict_raw": r.get("verdict"),
                "final_bucket": bucket,
                "one_sentence": sentence,
            }
        )
    return pd.DataFrame(rows)
