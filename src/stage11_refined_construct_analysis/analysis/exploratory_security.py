"""Exploratory security/care/appearance helpers (non-confirmatory)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set

import numpy as np
import pandas as pd
import yaml

from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code
from src.stage11_refined_construct_analysis.audits.runner import audit_dir, load_jsonl
from src.stage11_refined_construct_analysis.config import Stage11Config, load_stage11_config

DEFAULT_EXPLORATORY_CONFIG = Path("configs/stage11/exploratory_security_care_appearance.yaml")

PROTECTION_CODES = {"H4_5", "H4_6"}


def load_exploratory_config(path: Optional[Path] = None) -> Dict[str, Any]:
    p = path or DEFAULT_EXPLORATORY_CONFIG
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def topic_share_matrix(cfg: Stage11Config) -> pd.DataFrame:
    """Book × topic hard shares."""
    path = cfg.input_path("book_topic_counts", required=True)
    assert path is not None
    counts = pd.read_parquet(path)
    counts = counts[counts["topic_id"] >= 0]
    wide = counts.pivot_table(
        index="book_id",
        columns="topic_id",
        values="share",
        aggfunc="sum",
        fill_value=0.0,
    )
    wide.columns = [int(c) for c in wide.columns]
    return wide


def pass_b_protection_weight(
    cfg: Stage11Config,
    topic_id: int,
    *,
    protection_codes: Set[str] = PROTECTION_CODES,
) -> float:
    """Fraction of Pass-B sentences coded as external protection (H4_5/H4_6)."""
    path = audit_dir(cfg, "H4") / "contextual.jsonl"
    if not path.exists():
        return 0.0
    for rec in load_jsonl(path):
        if int(rec.get("topic_id", -1)) != int(topic_id):
            continue
        resp = rec.get("response") or {}
        props = resp.get("proportions") or {}
        if props:
            total = 0.0
            for code, share in props.items():
                canon = normalize_code(code) or str(code)
                if canon in protection_codes:
                    total += float(share)
            return min(1.0, total)
        codes = resp.get("sentence_codes") or []
        if not codes:
            return 0.0
        n_prot = 0
        for sc in codes:
            canon = normalize_code(sc.get("code")) or str(sc.get("code") or "")
            if canon in protection_codes:
                n_prot += 1
        return n_prot / len(codes)
    return 0.0


def build_fractional_protection_weights(
    cfg: Stage11Config,
    *,
    candidate_topics: Sequence[int],
    protection_codes: Optional[Sequence[str]] = None,
) -> Dict[int, float]:
    codes = {normalize_code(c) or c for c in (protection_codes or PROTECTION_CODES)}
    out: Dict[int, float] = {}
    for tid in candidate_topics:
        w = pass_b_protection_weight(cfg, int(tid), protection_codes=codes)
        if w > 0:
            out[int(tid)] = w
    return out


def topic_set_share(
    shares: pd.DataFrame,
    topic_ids: Sequence[int],
    *,
    topic_weights: Optional[Mapping[int, float]] = None,
) -> pd.Series:
    """Sum weighted topic shares per book."""
    if not topic_ids:
        return pd.Series(0.0, index=shares.index)
    acc = pd.Series(0.0, index=shares.index)
    for tid in topic_ids:
        if tid not in shares.columns:
            continue
        w = float((topic_weights or {}).get(int(tid), 1.0))
        acc = acc + shares[tid] * w
    return acc


def presence_and_intensity(
    share: pd.Series,
    *,
    threshold: float = 1e-5,
) -> Dict[str, float]:
    present = share > threshold
    return {
        "prevalence": float(present.mean()),
        "conditional_intensity": float(share[present].mean()) if present.any() else float("nan"),
        "unconditional_mean": float(share.mean()),
    }


def _align_series_to_frame(series: pd.Series, frame: pd.DataFrame) -> pd.Series:
    """Align a book_id-indexed series onto frame rows."""
    if "book_id" in frame.columns:
        return series.reindex(frame["book_id"].values).fillna(0.0).reset_index(drop=True)
    if frame.index.name == "book_id" or frame.index.name is None:
        return series.reindex(frame.index).fillna(0.0)
    return series.reindex(frame.index).fillna(0.0)


def add_topic_set_columns(
    frame: pd.DataFrame,
    shares: pd.DataFrame,
    families: Mapping[str, Mapping[str, Any]],
    *,
    fractional_weights: Optional[Mapping[int, float]] = None,
) -> pd.DataFrame:
    """Add EXP_* columns for strict/moderate/broad family levels."""
    out = frame.copy()
    frac = fractional_weights or {}
    for family, levels in families.items():
        if not isinstance(levels, dict):
            continue
        for level in ("strict", "moderate", "broad"):
            tids = levels.get(level) or []
            weights = None
            if family == "enacted_protection" and level in ("moderate", "broad"):
                weights = {}
                for t in tids:
                    tid = int(t)
                    if tid in frac:
                        weights[tid] = frac[tid]
                    elif tid == 119:
                        weights[tid] = 1.0
                    else:
                        weights[tid] = 0.0
            col = f"EXP_{family}_{level}"
            share = topic_set_share(shares, tids, topic_weights=weights)
            out[col] = _align_series_to_frame(share, out).values
    return out


def trajectory_effects(
    frame: pd.DataFrame,
    families: Mapping[str, Mapping[str, Any]],
    *,
    test_fn,
    hyp: str = "EXP",
) -> pd.DataFrame:
    """Run Cliff's δ for strict → moderate → broad per family.

    Empty topic sets are **unmeasurable** (NaN δ), not δ = 0.
    """
    rows = []
    for family, levels in families.items():
        if not isinstance(levels, dict):
            continue
        for level in ("strict", "moderate", "broad"):
            col = f"EXP_{family}_{level}"
            n_topics = len(levels.get(level) or [])
            if n_topics == 0:
                rows.append(
                    {
                        "family": family,
                        "level": level,
                        "feature": col,
                        "n_topics": 0,
                        "cliffs_delta": float("nan"),
                        "ci_low": float("nan"),
                        "ci_high": float("nan"),
                        "verdict": "unmeasurable",
                        "note": "zero topics",
                    }
                )
                continue
            if col not in frame.columns:
                continue
            res = test_fn(frame, col, hyp, label=f"{family} ({level})")
            rows.append(
                {
                    "family": family,
                    "level": level,
                    "feature": col,
                    "n_topics": n_topics,
                    "cliffs_delta": res.get("cliffs_delta"),
                    "ci_low": res.get("ci_low"),
                    "ci_high": res.get("ci_high"),
                    "verdict": res.get("verdict"),
                    "note": "",
                }
            )
    return pd.DataFrame(rows)


def topic_level_forest(
    shares: pd.DataFrame,
    frame: pd.DataFrame,
    topic_ids: Sequence[int],
    master: pd.DataFrame,
    *,
    test_fn,
    hyp: str = "EXP",
) -> pd.DataFrame:
    """Per-topic δ within a broad family."""
    rows = []
    for tid in topic_ids:
        if tid not in shares.columns:
            continue
        col = f"EXP_topic_{tid}"
        tmp = frame.copy()
        share = shares[tid] if tid in shares.columns else pd.Series(0.0, index=shares.index)
        tmp[col] = _align_series_to_frame(share, tmp).values
        res = test_fn(tmp, col, hyp, label=str(tid))
        label_row = master[master.topic_id == tid]
        label = label_row.current_topic_label.iloc[0] if len(label_row) else ""
        tax = label_row.current_taxonomy_id.iloc[0] if len(label_row) else ""
        rows.append(
            {
                "topic_id": tid,
                "topic_label": label,
                "taxonomy_id": tax,
                "cliffs_delta": res.get("cliffs_delta"),
                "ci_low": res.get("ci_low"),
                "ci_high": res.get("ci_high"),
                "verdict": res.get("verdict"),
            }
        )
    return pd.DataFrame(rows)


def _zscore(series: pd.Series) -> pd.Series:
    x = series.astype(float)
    sd = float(x.std(ddof=0))
    if not np.isfinite(sd) or sd <= 0:
        return pd.Series(0.0, index=series.index)
    return (x - float(x.mean())) / sd


def danger_protection_interaction(
    frame: pd.DataFrame,
    *,
    danger_col: str = "RAX_external_danger_crisis",
    protection_col: str,
    quality: str = "rating_shrunk",
    controls: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """OLS with z-scored danger × protection interaction (presentation-readable β)."""
    from src.stage10_correlation_analysis.analysis import models as mdl

    controls = list(controls or ["log_pages", "n_sentences", "publication_year"])
    controls = [c for c in controls if c in frame.columns]
    categorical = [c for c in ["genre_group"] if c in frame.columns]
    work = frame.copy()
    if danger_col not in work.columns or protection_col not in work.columns:
        return {"status": "absent", "danger": danger_col, "protection": protection_col}
    work["z_danger"] = _zscore(work[danger_col].fillna(0.0))
    work["z_protection"] = _zscore(work[protection_col].fillna(0.0))
    work["z_danger_x_z_protection"] = work["z_danger"] * work["z_protection"]
    fit = mdl.fit_ols(
        work.reset_index() if work.index.name else work,
        quality,
        ["z_danger", "z_protection", "z_danger_x_z_protection", *controls],
        categorical=categorical,
        cluster="author_id" if "author_id" in work.columns else None,
        weights="reliability" if "reliability" in work.columns else None,
        name=f"{protection_col}_x_danger_z",
    )
    coef = fit.coefficients
    out: Dict[str, Any] = {
        "status": "ok",
        "danger": danger_col,
        "protection": protection_col,
        "standardized": True,
    }
    for term in ("z_danger", "z_protection", "z_danger_x_z_protection"):
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


def danger_protection_quadrants(
    frame: pd.DataFrame,
    *,
    danger_col: str = "RAX_external_danger_crisis",
    protection_col: str,
    quality: str = "rating_shrunk",
    protection_label: str = "",
) -> pd.DataFrame:
    """Median-split 2×2: lower/higher danger × lower/higher protection."""
    if danger_col not in frame.columns or protection_col not in frame.columns:
        return pd.DataFrame()
    tmp = frame[[danger_col, protection_col, quality]].dropna(subset=[danger_col, protection_col]).copy()
    if quality not in tmp.columns:
        return pd.DataFrame()
    d_med = float(tmp[danger_col].median())
    p_med = float(tmp[protection_col].median())
    tmp["danger_bin"] = np.where(tmp[danger_col] >= d_med, "higher_danger", "lower_danger")
    tmp["protection_bin"] = np.where(
        tmp[protection_col] >= p_med, "higher_protection", "lower_protection"
    )
    rows = []
    for (db, pb), sub in tmp.groupby(["danger_bin", "protection_bin"], observed=True):
        rows.append(
            {
                "protection_index": protection_label or protection_col,
                "protection_col": protection_col,
                "danger_bin": db,
                "protection_bin": pb,
                "n": int(len(sub)),
                "mean_rating": float(sub[quality].mean()),
                "median_rating": float(sub[quality].median()),
                "danger_median_cut": d_med,
                "protection_median_cut": p_med,
            }
        )
    return pd.DataFrame(rows)


def protection_danger_topic_overlap(
    protection_topic_ids: Sequence[int],
    danger_topic_ids: Sequence[int],
) -> pd.DataFrame:
    """Topic-id intersection between enacted-protection and external-danger sets."""
    prot = {int(t) for t in protection_topic_ids}
    dang = {int(t) for t in danger_topic_ids}
    overlap = sorted(prot & dang)
    return pd.DataFrame(
        [
            {
                "n_protection_topics": len(prot),
                "n_danger_topics": len(dang),
                "n_overlap": len(overlap),
                "overlap_topic_ids": ",".join(str(t) for t in overlap) if overlap else "",
                "note": (
                    "empty topic-id overlap"
                    if not overlap
                    else "shared topics — interpret broad protection with caution"
                ),
            }
        ]
    )


def construct_topic_ids_from_w_tk(
    cfg: Stage11Config,
    construct: str,
    *,
    mode: str = "strict",
) -> List[int]:
    """Topic ids with positive W_tk weight mapping to a RAX construct."""
    from src.stage11_refined_construct_analysis.analysis.constructs import (
        normalize_code,
        rax_for_code,
    )

    path = cfg.output_path("constructs_dir") / f"W_tk_{mode}.parquet"
    if not path.exists():
        return []
    w = pd.read_parquet(path)
    tids: Set[int] = set()
    for _, r in w.iterrows():
        if float(r.get("weight") or 0.0) <= 0:
            continue
        code = normalize_code(r.get("construct_code")) or str(r.get("construct_code") or "")
        if construct in rax_for_code(code):
            tids.add(int(r["topic_id"]))
    return sorted(tids)


def quadrant_summary(
    frame: pd.DataFrame,
    x_col: str,
    y_col: str,
    *,
    quality: str = "rating_shrunk",
) -> pd.DataFrame:
    """2×2 quadrant means for care × appearance."""
    x = frame[x_col].fillna(0.0)
    y = frame[y_col].fillna(0.0)
    x_med = x.median()
    y_med = y.median()
    labels = []
    for xv, yv in zip(x, y):
        if xv >= x_med and yv < y_med:
            labels.append("high_care_low_appearance")
        elif xv >= x_med and yv >= y_med:
            labels.append("high_care_high_appearance")
        elif xv < x_med and yv < y_med:
            labels.append("low_care_low_appearance")
        else:
            labels.append("low_care_high_appearance")
    tmp = frame.copy()
    tmp["_quad"] = labels
    agg = (
        tmp.groupby("_quad")[quality]
        .agg(["mean", "median", "count"])
        .reset_index()
        .rename(columns={"mean": f"{quality}_mean", "median": f"{quality}_median"})
    )
    return agg


def save_fractional_weights_json(
    weights: Mapping[int, float],
    out_path: Path,
) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "description": "Exploratory fractional external-protection weights from H4 Pass B",
        "weights": {str(k): float(v) for k, v in sorted(weights.items())},
    }
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path


def load_stage11_from_exploratory(exp_cfg: Mapping[str, Any]) -> Stage11Config:
    rel = exp_cfg.get("inputs", {}).get("stage11_config", "configs/stage11/refined_constructs.yaml")
    return load_stage11_config(rel)
