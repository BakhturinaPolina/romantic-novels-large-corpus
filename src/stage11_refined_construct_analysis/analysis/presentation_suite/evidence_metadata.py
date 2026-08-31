"""Build canonical evidence metadata frames from saved Stage 11 tables."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

import numpy as np
import pandas as pd

from .paths import PresentationPaths, default_paths
from .theme import EFFECT_GATE, HYPOTHESIS_ORDER

AGREEMENT_NOTEBOOKS = {
    "H1": "01_h1_intimacy_audit",
    "H2": "02_h2_hea_payoff_audit",
    "H3": "03_h3_security_material_audit",
    "H4": "04_h4_protection_possession_audit",
    "H5": "05_h5_darkness_tenderness_audit",
    "H6": "06_h6_arc_semantics_audit",
}

MEASUREMENT_NOTES = {
    "H1": "Viable emotional-vs-explicit ratio after refinement",
    "H2": "Strict HEA/payoff has zero mapped topics",
    "H3": "Material-side denominator empty after freeze",
    "H4": "Thin protection atom (t119); ratio provisional",
    "H5": "Viable darkness-vs-tenderness contrast",
    "H6": "Viable refined arc contrast (RARC)",
}

# Confirmatory components to highlight in fig05 (grouped by parent)
COMPONENT_FOCUS = (
    "RAX_emotional_reassurance",
    "RAX_explicit_sex",
    "RAX_nonexplicit_affection",
    "RAX_h3_emotional_side",
    "RAX_appearance_grooming",
    "RAX_external_protection",
    "RAX_h4_possession_side",
    "RAX_tenderness_core",
    "RAX_external_danger_crisis",
    "RAX_relational_darkness",
)


def _read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _coverage_lookup(paths: PresentationPaths) -> Dict[str, Dict[str, Any]]:
    cov_path = paths.constructs / "construct_coverage.json"
    raw = json.loads(cov_path.read_text())
    flat: Dict[str, Dict[str, Any]] = {}
    for section in raw.values():
        if isinstance(section, dict):
            for feat, info in section.items():
                if isinstance(info, dict):
                    flat[feat] = info
    return flat


def _topic_count_str(info: Mapping[str, Any] | None, *, feature: str | None = None, cov: Mapping[str, Mapping[str, Any]] | None = None) -> str:
    if feature == "RARC" and cov is not None:
        n_r = cov.get("RAX_arc_rising", {}).get("n_topics")
        n_f = cov.get("RAX_arc_falling", {}).get("n_topics")
        if n_r is not None and n_f is not None:
            return f"{int(n_r)} rising / {int(n_f)} falling"
    if not info:
        return "—"
    if "n_topics" in info and info["n_topics"] is not None:
        return str(int(info["n_topics"]))
    n_num = info.get("numerator_topics")
    n_den = info.get("denominator_topics")
    if n_num is not None and n_den is not None:
        return f"{int(n_num)} / {int(n_den)}"
    return "—"


def _sign(x: float | None) -> Optional[int]:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def load_agreement(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    rows = []
    for h in HYPOTHESIS_ORDER:
        nb = AGREEMENT_NOTEBOOKS[h]
        table_name = f"h{h[1:]}_lexical_contextual_agreement"
        table_path = paths.table(nb, table_name)
        df = _read_table(table_path)
        n = len(df)
        k = int(df["agree"].astype(bool).sum())
        rows.append(
            {
                "hypothesis": h,
                "n_agree": k,
                "n_total": n,
                "agreement_pct": 100.0 * k / n if n else np.nan,
                "label": f"{k}/{n} ({100.0 * k / n:.0f}%)" if n else "—",
                "result_level": "primary",
                "confirmatory_or_exploratory": "methodological",
                "table_source": str(table_path),
            }
        )
    return pd.DataFrame(rows)


def load_primaries(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    verdict = _read_table(paths.table("13_final_statistical_tests", "final_verdict_table"))
    primary = _read_table(paths.table("13_final_statistical_tests", "primary_h1_h6_table"))
    side = _read_table(paths.table("13_final_statistical_tests", "stage10_vs_final_side_by_side"))
    traffic = _read_table(paths.table("13_final_statistical_tests", "robustness_traffic_light"))
    cov = _coverage_lookup(paths)

    keep_pri = [
        "hypothesis",
        "feature",
        "label",
        "cliffs_delta",
        "ci_low",
        "ci_high",
        "quality_beta",
        "quality_p",
        "quality_ci_low",
        "quality_ci_high",
        "verdict",
    ]
    primary_slim = primary[[c for c in keep_pri if c in primary.columns]]
    out = verdict.merge(primary_slim, on=["hypothesis", "feature"], how="left", suffixes=("", "_drop"))
    out = out.merge(
        side[["hypothesis", "original_delta", "refined_delta"]],
        on="hypothesis",
        how="left",
    )
    out = out.merge(
        traffic[["feature", "sign_stable", "clears_gate_any_spec", "light", "overall"]],
        on="feature",
        how="left",
    )

    rows = []
    for h in HYPOTHESIS_ORDER:
        r = out.loc[out["hypothesis"] == h].iloc[0]
        feat = str(r["feature"])
        gate = str(r["measurement_gate"]).lower()
        delta = r.get("cliffs_delta")
        if gate == "unmeasurable" or (pd.isna(delta) if delta is not None else True):
            delta = np.nan
            ci_lo = np.nan
            ci_hi = np.nan
        else:
            delta = float(delta)
            ci_lo = float(r["ci_low"]) if pd.notna(r.get("ci_low")) else np.nan
            ci_hi = float(r["ci_high"]) if pd.notna(r.get("ci_high")) else np.nan

        q_beta = float(r["quality_beta"]) if pd.notna(r.get("quality_beta")) else np.nan
        q_p = float(r["quality_p"]) if pd.notna(r.get("quality_p")) else np.nan
        d_sign = _sign(delta)
        q_sign = _sign(q_beta)
        aligned = (
            bool(d_sign is not None and q_sign is not None and d_sign == q_sign and d_sign != 0)
            if gate != "unmeasurable"
            else np.nan
        )

        info = cov.get(feat)
        rows.append(
            {
                "hypothesis": h,
                "feature": feat,
                "label": r.get("label") if pd.notna(r.get("label")) else feat,
                "result_level": "primary",
                "measurement_status": gate,
                "n_topics_display": _topic_count_str(info, feature=feat, cov=cov),
                "measurement_note": MEASUREMENT_NOTES.get(h, ""),
                "effect_size": delta,
                "ci_low": ci_lo,
                "ci_high": ci_hi,
                "adjusted_coefficient": q_beta,
                "adjusted_ci_low": float(r["quality_ci_low"]) if pd.notna(r.get("quality_ci_low")) else np.nan,
                "adjusted_ci_high": float(r["quality_ci_high"]) if pd.notna(r.get("quality_ci_high")) else np.nan,
                "adjusted_p_value": q_p,
                "adjusted_sign": q_sign,
                "adjusted_sign_aligned": aligned,
                "adjusted_p_lt_05": (q_p < 0.05) if pd.notna(q_p) else np.nan,
                "clears_delta_gate": (abs(delta) >= EFFECT_GATE) if pd.notna(delta) else False,
                "specification_stable": bool(r["sign_stable"]) if pd.notna(r.get("sign_stable")) else np.nan,
                "confirmatory_or_exploratory": "confirmatory",
                "verdict": str(r["final_bucket"]),
                "verdict_raw": str(r.get("verdict_raw", "")),
                "one_sentence": str(r.get("one_sentence", "")),
                "stage10_delta": float(r["original_delta"]) if pd.notna(r.get("original_delta")) else np.nan,
                "stage11_delta": delta,
                "notes": str(r.get("overall", "")),
            }
        )
    return pd.DataFrame(rows)


def load_components(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    comp = _read_table(paths.table("13_final_statistical_tests", "component_effects"))
    traffic = _read_table(paths.table("13_final_statistical_tests", "robustness_traffic_light"))
    cov = _coverage_lookup(paths)

    # Keep measurable components (and thin); drop unmeasurable atoms with no estimate
    rows = []
    for _, r in comp.iterrows():
        gate = str(r["measurement_gate"]).lower()
        feat = str(r["feature"])
        delta = r.get("cliffs_delta")
        if gate == "unmeasurable" or pd.isna(delta):
            # retain row only if we want inventory; for forest we skip plotting zeros
            continue
        delta = float(delta)
        q_beta = float(r["quality_beta"]) if pd.notna(r.get("quality_beta")) else np.nan
        q_p = float(r["quality_p"]) if pd.notna(r.get("quality_p")) else np.nan
        d_sign = _sign(delta)
        q_sign = _sign(q_beta)
        tr = traffic.loc[traffic["feature"] == feat]
        sign_stable = bool(tr.iloc[0]["sign_stable"]) if len(tr) else np.nan
        info = cov.get(feat, {})
        n_topics = info.get("n_topics")
        rows.append(
            {
                "hypothesis": str(r["hypothesis"]),
                "feature": feat,
                "label": str(r["label"]),
                "result_level": "component",
                "measurement_status": gate,
                "n_topics": int(n_topics) if n_topics is not None else np.nan,
                "n_topics_display": _topic_count_str(info) if info else "—",
                "effect_size": delta,
                "ci_low": float(r["ci_low"]) if pd.notna(r.get("ci_low")) else np.nan,
                "ci_high": float(r["ci_high"]) if pd.notna(r.get("ci_high")) else np.nan,
                "adjusted_coefficient": q_beta,
                "adjusted_ci_low": float(r["quality_ci_low"]) if pd.notna(r.get("quality_ci_low")) else np.nan,
                "adjusted_ci_high": float(r["quality_ci_high"]) if pd.notna(r.get("quality_ci_high")) else np.nan,
                "adjusted_p_value": q_p,
                "adjusted_sign": q_sign,
                "adjusted_sign_aligned": bool(
                    d_sign is not None and q_sign is not None and d_sign == q_sign and d_sign != 0
                ),
                "adjusted_p_lt_05": (q_p < 0.05) if pd.notna(q_p) else np.nan,
                "clears_delta_gate": abs(delta) >= EFFECT_GATE,
                "specification_stable": sign_stable,
                "confirmatory_or_exploratory": "confirmatory_component",
                "verdict": str(r["verdict"]),
                "focus": feat in COMPONENT_FOCUS,
                "notes": "",
            }
        )
    df = pd.DataFrame(rows)
    # Stable order: by hypothesis then by absolute effect within focus set preference
    h_rank = {h: i for i, h in enumerate(HYPOTHESIS_ORDER)}
    df["_h"] = df["hypothesis"].map(h_rank)
    df = df.sort_values(["_h", "focus", "effect_size"], ascending=[True, False, False]).drop(columns="_h")
    return df.reset_index(drop=True)


def build_all_metadata(
    paths: PresentationPaths | None = None,
    *,
    write: bool = True,
) -> Dict[str, pd.DataFrame]:
    paths = paths or default_paths()
    frames = {
        "presentation_agreement": load_agreement(paths),
        "presentation_primary_results": load_primaries(paths),
        "presentation_component_results": load_components(paths),
    }
    if write:
        paths.out_dir.mkdir(parents=True, exist_ok=True)
        for name, df in frames.items():
            df.to_csv(paths.out_dir / f"{name}.csv", index=False)
            try:
                df.to_parquet(paths.out_dir / f"{name}.parquet", index=False)
            except Exception:
                pass
    return frames
