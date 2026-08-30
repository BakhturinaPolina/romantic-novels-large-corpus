"""Build the Stage 11 refined book-level analysis frame.

C_bk = sum_t p_bt * W_tk   (hard topic shares × construct weights)
H6 also uses tertile-specific shares × W_tkr.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence

import numpy as np
import pandas as pd

from src.stage11_refined_construct_analysis.analysis.constructs import (
    COMPOSITE_DEFS,
    LOG_RATIO_DEFS,
    all_rax_atoms,
    normalize_code,
    rax_for_code,
)
from src.stage11_refined_construct_analysis.config import Stage11Config

LOGGER = logging.getLogger("stage11.frame")

# Stage 10 outcome / control columns joined onto the refined frame
_META_COLS = [
    "avg_rating",
    "rating_shrunk",
    "reliability",
    "log_n_ratings",
    "log_pages",
    "n_sentences",
    "publication_year",
    "genre_group",
    "author_id",
    "series_id",
    "rating_class",
    "analysable",
    "split",
]


def _load_stage10_frame(cfg: Stage11Config) -> pd.DataFrame:
    path = cfg.input_path("analysis_frame", required=True)
    assert path is not None
    frame = pd.read_parquet(path)
    if "book_id" in frame.columns:
        frame = frame.set_index("book_id")
    return frame


def _topic_share_matrix(cfg: Stage11Config, book_ids: Sequence) -> pd.DataFrame:
    """Wide book × topic hard shares (missing → 0)."""
    path = cfg.input_path("book_topic_counts", required=True)
    assert path is not None
    counts = pd.read_parquet(path)
    counts = counts[counts["topic_id"] >= 0]
    # Restrict to books in the Stage 10 frame
    counts = counts[counts["book_id"].isin(book_ids)]
    wide = counts.pivot_table(
        index="book_id",
        columns="topic_id",
        values="share",
        aggfunc="sum",
        fill_value=0.0,
    )
    wide.columns = [int(c) for c in wide.columns]
    return wide


def _weights_to_topic_rax(
    w_tk: pd.DataFrame,
    *,
    atoms: Sequence[str],
) -> pd.DataFrame:
    """Return topic_id × RAX weight matrix from W_tk long frame."""
    rows = []
    for _, r in w_tk.iterrows():
        code = normalize_code(r.get("construct_code")) or str(r.get("construct_code") or "")
        w = float(r.get("weight") or 0.0)
        if w <= 0:
            continue
        for rax in rax_for_code(code):
            rows.append({"topic_id": int(r["topic_id"]), "rax": rax, "weight": w})
    if not rows:
        return pd.DataFrame(0.0, index=[], columns=list(atoms))
    long = pd.DataFrame(rows)
    # If a topic maps to the same RAX via multiple codes, take max weight
    long = long.groupby(["topic_id", "rax"], as_index=False)["weight"].max()
    wide = long.pivot_table(index="topic_id", columns="rax", values="weight", fill_value=0.0)
    for a in atoms:
        if a not in wide.columns:
            wide[a] = 0.0
    return wide[list(atoms)]


def _book_constructs_from_shares(
    shares: pd.DataFrame,
    topic_rax: pd.DataFrame,
) -> pd.DataFrame:
    """C = shares @ topic_rax  (books × RAX)."""
    # Align topic columns
    topics = [t for t in topic_rax.index if t in shares.columns]
    if not topics:
        return pd.DataFrame(0.0, index=shares.index, columns=topic_rax.columns)
    S = shares[topics].to_numpy(dtype=float)
    W = topic_rax.loc[topics].to_numpy(dtype=float)
    C = S @ W
    return pd.DataFrame(C, index=shares.index, columns=topic_rax.columns)


def _add_composites_and_ratios(frame: pd.DataFrame, eps: float) -> pd.DataFrame:
    out = frame.copy()
    for name, parts in COMPOSITE_DEFS.items():
        cols = [c for c in parts if c in out.columns]
        out[name] = out[cols].sum(axis=1) if cols else 0.0
    for name, (num, den) in LOG_RATIO_DEFS.items():
        n = out[num] if num in out.columns else 0.0
        d = out[den] if den in out.columns else 0.0
        out[name] = np.log((n + eps) / (d + eps))
    return out


def _h6_arc_deltas(cfg: Stage11Config, book_ids: Sequence, eps: float) -> pd.DataFrame:
    """Build RARC = Δ_rising − Δ_falling from tertile shares × W_tkr."""
    wtkr_path = cfg.output_path("constructs_dir") / "W_tkr.parquet"
    if not wtkr_path.exists():
        return pd.DataFrame(index=pd.Index(book_ids, name="book_id"))

    wtkr = pd.read_parquet(wtkr_path)
    if wtkr.empty:
        return pd.DataFrame(index=pd.Index(book_ids, name="book_id"))

    # Map construct_code → rising/falling/external
    rows = []
    for _, r in wtkr.iterrows():
        code = normalize_code(r.get("construct_code"))
        if not code:
            # try phrase
            code = normalize_code(str(r.get("construct_code") or ""))
        rax_list = rax_for_code(code) if code else []
        role = None
        if "RAX_arc_rising" in rax_list:
            role = "rising"
        elif "RAX_arc_falling" in rax_list:
            role = "falling"
        elif "RAX_external_plot_conflict" in rax_list:
            role = "external"
        if role is None:
            continue
        rows.append(
            {
                "topic_id": int(r["topic_id"]),
                "tertile": str(r["tertile"]),
                "role": role,
                "weight": float(r["weight"]),
            }
        )
    if not rows:
        return pd.DataFrame(index=pd.Index(book_ids, name="book_id"))

    role_w = pd.DataFrame(rows)
    role_w = role_w.groupby(["topic_id", "tertile", "role"], as_index=False)["weight"].max()

    tertile_path = (
        cfg.root
        / "results/stage10_correlation_analysis"
        / cfg.run_id
        / "topic_counts_hard/tertile_topic_counts.parquet"
    )
    if not tertile_path.exists():
        LOGGER.warning("Missing tertile_topic_counts at %s", tertile_path)
        return pd.DataFrame(index=pd.Index(book_ids, name="book_id"))

    # Load only needed topics
    needed = sorted(role_w["topic_id"].unique())
    tert = pd.read_parquet(tertile_path)
    tert = tert[(tert["book_id"].isin(book_ids)) & (tert["topic_id"].isin(needed))]
    if tert.empty:
        return pd.DataFrame(index=pd.Index(book_ids, name="book_id"))

    merged = tert.merge(role_w, on=["topic_id", "tertile"], how="inner")
    merged["contrib"] = merged["share"] * merged["weight"]
    book_role = (
        merged.groupby(["book_id", "tertile", "role"], as_index=False)["contrib"]
        .sum()
    )
    pivot = book_role.pivot_table(
        index="book_id",
        columns=["role", "tertile"],
        values="contrib",
        fill_value=0.0,
    )
    # Flatten columns
    pivot.columns = [f"{role}_{tert}" for role, tert in pivot.columns]

    def col(role: str, tertile: str) -> pd.Series:
        name = f"{role}_{tertile}"
        if name in pivot.columns:
            return pivot[name]
        return pd.Series(0.0, index=pivot.index)

    out = pd.DataFrame(index=pivot.index)
    out["RAX_arc_rising_begin"] = col("rising", "begin")
    out["RAX_arc_rising_end"] = col("rising", "end")
    out["RAX_arc_falling_begin"] = col("falling", "begin")
    out["RAX_arc_falling_end"] = col("falling", "end")
    out["RAX_external_plot_begin"] = col("external", "begin")
    out["RAX_external_plot_end"] = col("external", "end")
    out["DELTA_rising"] = out["RAX_arc_rising_end"] - out["RAX_arc_rising_begin"]
    out["DELTA_falling"] = out["RAX_arc_falling_end"] - out["RAX_arc_falling_begin"]
    out["RARC"] = out["DELTA_rising"] - out["DELTA_falling"]
    return out.reindex(book_ids).fillna(0.0)


def build_refined_frame(
    cfg: Stage11Config,
    *,
    mode: str = "strict",
) -> pd.DataFrame:
    """Join Stage 10 metadata with refined RAX constructs for one weight mode."""
    eps = float(cfg.section("weights", "epsilon"))
    stage10 = _load_stage10_frame(cfg)
    book_ids = stage10.index

    w_path = cfg.output_path("constructs_dir") / f"W_tk_{mode}.parquet"
    if not w_path.exists():
        raise FileNotFoundError(f"Missing weights: {w_path}")
    w_tk = pd.read_parquet(w_path)
    atoms = all_rax_atoms()
    topic_rax = _weights_to_topic_rax(w_tk, atoms=atoms)

    shares = _topic_share_matrix(cfg, book_ids)
    constructs = _book_constructs_from_shares(shares, topic_rax)
    constructs = constructs.reindex(book_ids).fillna(0.0)
    constructs = _add_composites_and_ratios(constructs, eps)

    # Prefix mode so multiple modes can live side by side if needed; primary
    # frame uses unprefixed names for the selected mode.
    meta_cols = [c for c in _META_COLS if c in stage10.columns]
    # Also keep a few Stage 10 axes for side-by-side comparison in NB09
    stage10_compare = [
        c
        for c in stage10.columns
        if c.startswith(("AX_", "LR_", "abs_leaf_"))
        and not c.endswith(("_z", "_clr"))
    ]
    # Limit compare columns to headline leaves / axes
    keep_compare = [
        c
        for c in stage10_compare
        if any(
            k in c
            for k in (
                "love_over_sex",
                "hea_index",
                "material_social",
                "protective",
                "dark_vs_tender",
                "narrative_arc",
                "abs_leaf_1.6",
                "abs_leaf_2.3",
                "abs_leaf_4.5",
                "abs_leaf_4.6",
                "abs_leaf_4.7",
                "abs_leaf_4.4",
                "abs_leaf_7.2",
            )
        )
    ]

    out = stage10[meta_cols + keep_compare].join(constructs, how="left")
    out = out.join(_h6_arc_deltas(cfg, book_ids, eps), how="left")
    out["weight_mode"] = mode
    return out


def write_refined_frame(cfg: Stage11Config) -> Dict[str, Path]:
    out_dir = cfg.output_path("book_features_dir", create=True)
    paths: Dict[str, Path] = {}
    primary = None
    for mode in ("strict", "weighted", "inclusive"):
        LOGGER.info("Building refined frame mode=%s …", mode)
        frame = build_refined_frame(cfg, mode=mode)
        path = out_dir / f"book_refined_analysis_frame_{mode}.parquet"
        frame.to_parquet(path)
        paths[mode] = path
        if mode == "strict":
            primary = frame
            primary_path = out_dir / "book_refined_analysis_frame.parquet"
            frame.to_parquet(primary_path)
            paths["primary"] = primary_path

    # Manifest
    assert primary is not None
    rax_cols = [c for c in primary.columns if c.startswith("RAX_") or c.startswith("RLR_") or c in ("RARC", "DELTA_rising", "DELTA_falling")]
    manifest = pd.DataFrame(
        {
            "column": rax_cols,
            "nonzero_books": [(primary[c] > 0).sum() for c in rax_cols],
            "mean": [float(primary[c].mean()) for c in rax_cols],
            "median": [float(primary[c].median()) for c in rax_cols],
        }
    )
    man_path = out_dir / "refined_frame_manifest.parquet"
    manifest.to_parquet(man_path, index=False)
    paths["manifest"] = man_path

    meta = {
        "run_id": cfg.run_id,
        "n_books": int(len(primary)),
        "n_rax_columns": len(rax_cols),
        "modes": ["strict", "weighted", "inclusive"],
        "paths": {k: str(v.relative_to(cfg.root)) for k, v in paths.items()},
    }
    meta_path = out_dir / "refined_frame_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    paths["meta"] = meta_path
    LOGGER.info("Refined frames written under %s", out_dir)
    return paths
