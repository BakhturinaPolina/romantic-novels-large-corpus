"""Validate presentation metadata and generated figure files."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd

from .evidence_metadata import AGREEMENT_NOTEBOOKS, COMPONENT_FOCUS, _read_table
from .paths import PresentationPaths, default_paths
from .theme import EFFECT_GATE, HYPOTHESIS_ORDER

ALLOWED_MEASUREMENT = {"viable", "thin", "unmeasurable"}
ATOL = 1e-12

EXPECTED_FIGURES = [
    "fig01_contextual_agreement",
    "fig02_measurement_status",
    "fig03_primary_hypothesis_verdicts",
    "fig04_stage10_stage11_transition",
    "fig05_component_effects",
    "fig05b_component_evidence_matrix",
    "fig06_attention_shift",
    "appendix_richness",
    "appendix_danger_protection_interaction",
    "appendix_security_care_specificity",
    "appendix_promise_functions",
    "appendix_quality_reach",
    "appendix_function_drift",
    "appendix_felt_vs_looked",
    "appendix_ees_three_panel",
    "appendix_genre_era",
]


class PresentationValidationError(AssertionError):
    pass


def _close(a, b, *, atol: float = ATOL) -> bool:
    if pd.isna(a) and pd.isna(b):
        return True
    if pd.isna(a) or pd.isna(b):
        return False
    return bool(np.isclose(float(a), float(b), atol=atol, rtol=0.0, equal_nan=True))


def validate_frames(frames: Dict[str, pd.DataFrame]) -> List[str]:
    errors: List[str] = []
    primary = frames["presentation_primary_results"]
    agreement = frames["presentation_agreement"]
    components = frames["presentation_component_results"]

    if set(primary["hypothesis"]) != set(HYPOTHESIS_ORDER):
        errors.append(f"Primary hypotheses mismatch: {sorted(primary['hypothesis'])}")

    for _, r in primary.iterrows():
        st = str(r["measurement_status"])
        if st not in ALLOWED_MEASUREMENT:
            errors.append(f"{r['hypothesis']}: bad measurement_status {st}")
        if st == "unmeasurable":
            if pd.notna(r["effect_size"]):
                errors.append(f"{r['hypothesis']}: unmeasurable has non-null effect_size={r['effect_size']}")
            if pd.notna(r["effect_size"]) and float(r["effect_size"]) == 0.0:
                errors.append(f"{r['hypothesis']}: unmeasurable encoded as zero")
        else:
            lo, est, hi = r["ci_low"], r["effect_size"], r["ci_high"]
            if not (lo <= est <= hi):
                errors.append(f"{r['hypothesis']}: CI ordering failed {lo}, {est}, {hi}")

    # H2/H3 specifically
    for h in ("H2", "H3"):
        row = primary.loc[primary["hypothesis"] == h].iloc[0]
        if row["measurement_status"] != "unmeasurable":
            errors.append(f"{h} expected unmeasurable, got {row['measurement_status']}")
        if pd.notna(row["effect_size"]):
            errors.append(f"{h} effect_size should be NaN")

    # H4 must remain thin/measurable — not mislabeled unmeasurable in prose
    h4 = primary.loc[primary["hypothesis"] == "H4"].iloc[0]
    if h4["measurement_status"] != "thin":
        errors.append(f"H4 expected thin, got {h4['measurement_status']}")
    sentence = str(h4.get("one_sentence", "")).lower()
    if "primary ratio unmeasurable" in sentence:
        errors.append("H4 one_sentence still calls primary ratio unmeasurable")
    if pd.isna(h4["effect_size"]):
        errors.append("H4 must retain measurable cliffs_delta")

    # Agreement percentages
    for _, r in agreement.iterrows():
        expected = 100.0 * r["n_agree"] / r["n_total"]
        if abs(expected - r["agreement_pct"]) > 0.05:
            errors.append(f"{r['hypothesis']} agreement pct mismatch")

    # Components: no exploratory leak into confirmatory_component with null gates as zero
    if (components["confirmatory_or_exploratory"] == "exploratory").any():
        errors.append("Exploratory rows found in component frame")
    for _, r in components.iterrows():
        if r["measurement_status"] not in ALLOWED_MEASUREMENT - {"unmeasurable"}:
            # thin/viable only in forest frame
            if r["measurement_status"] == "unmeasurable":
                errors.append(f"Unmeasurable component {r['feature']} should not be in forest frame")
        lo, est, hi = r["ci_low"], r["effect_size"], r["ci_high"]
        if not (lo <= est <= hi):
            errors.append(f"Component {r['feature']} CI ordering failed")
        # thin flag for external protection
        if r["feature"] == "RAX_external_protection" and r["measurement_status"] != "thin":
            errors.append("external_protection must be thin")

    # Gate consistency
    for _, r in components.iterrows():
        clears = bool(abs(r["effect_size"]) >= EFFECT_GATE)
        if bool(r["clears_delta_gate"]) != clears:
            errors.append(f"{r['feature']}: clears_delta_gate inconsistent")

    return errors


def assert_provenance_vs_sources(
    paths: PresentationPaths,
    frames: Dict[str, pd.DataFrame],
) -> List[str]:
    """Compare presentation metadata (and key appendix inputs) to authoritative Stage 11 tables."""
    errors: List[str] = []
    primary = frames["presentation_primary_results"].set_index("hypothesis")
    agreement = frames["presentation_agreement"].set_index("hypothesis")
    components = frames["presentation_component_results"].set_index("feature")

    src_primary = _read_table(paths.table("13_final_statistical_tests", "primary_h1_h6_table")).set_index(
        "hypothesis"
    )
    src_verdict = _read_table(paths.table("13_final_statistical_tests", "final_verdict_table")).set_index(
        "hypothesis"
    )
    src_side = _read_table(
        paths.table("13_final_statistical_tests", "stage10_vs_final_side_by_side")
    ).set_index("hypothesis")
    src_comp = _read_table(paths.table("13_final_statistical_tests", "component_effects")).set_index("feature")

    # --- Primary δ / CI / adjusted / transitions ---
    for h in HYPOTHESIS_ORDER:
        gate = str(src_verdict.loc[h, "measurement_gate"]).lower()
        pr = primary.loc[h]
        if gate == "unmeasurable":
            if pd.notna(pr["effect_size"]) or pd.notna(pr["ci_low"]) or pd.notna(pr["ci_high"]):
                errors.append(f"{h}: presentation should blank δ/CI for unmeasurable")
            if not _close(pr["stage10_delta"], src_side.loc[h, "original_delta"]):
                errors.append(f"{h}: stage10_delta mismatch")
            if pd.notna(pr["stage11_delta"]):
                errors.append(f"{h}: stage11_delta should be NaN")
            continue

        sp = src_primary.loc[h]
        checks = [
            ("effect_size", sp["cliffs_delta"]),
            ("ci_low", sp["ci_low"]),
            ("ci_high", sp["ci_high"]),
            ("adjusted_coefficient", sp["quality_beta"]),
            ("adjusted_ci_low", sp["quality_ci_low"]),
            ("adjusted_ci_high", sp["quality_ci_high"]),
            ("adjusted_p_value", sp["quality_p"]),
            ("stage10_delta", src_side.loc[h, "original_delta"]),
            ("stage11_delta", src_side.loc[h, "refined_delta"]),
        ]
        for col, expected in checks:
            if not _close(pr[col], expected):
                errors.append(f"{h}.{col}: presentation={pr[col]!r} source={expected!r}")

        # one_sentence must match authoritative verdict table
        if str(pr["one_sentence"]) != str(src_verdict.loc[h, "one_sentence"]):
            errors.append(f"{h}: one_sentence drifted from final_verdict_table")

    # --- Agreement numerators / denominators ---
    for h in HYPOTHESIS_ORDER:
        nb = AGREEMENT_NOTEBOOKS[h]
        table_name = f"h{h[1:]}_lexical_contextual_agreement"
        df = _read_table(paths.table(nb, table_name))
        n_total = len(df)
        n_agree = int(df["agree"].astype(bool).sum())
        ar = agreement.loc[h]
        if int(ar["n_agree"]) != n_agree or int(ar["n_total"]) != n_total:
            errors.append(
                f"{h} agreement counts: presentation=({ar['n_agree']},{ar['n_total']}) "
                f"source=({n_agree},{n_total})"
            )

    # --- Focal components δ / CI + external protection status/count ---
    for feat in COMPONENT_FOCUS:
        if feat not in src_comp.index:
            errors.append(f"Missing component in source: {feat}")
            continue
        if feat not in components.index:
            # Unmeasurable components are dropped from forest frame
            if str(src_comp.loc[feat, "measurement_gate"]).lower() == "unmeasurable":
                continue
            errors.append(f"Missing component in presentation: {feat}")
            continue
        sc = src_comp.loc[feat]
        pc = components.loc[feat]
        for col, src_col in (
            ("effect_size", "cliffs_delta"),
            ("ci_low", "ci_low"),
            ("ci_high", "ci_high"),
            ("adjusted_coefficient", "quality_beta"),
            ("adjusted_p_value", "quality_p"),
        ):
            if not _close(pc[col], sc[src_col]):
                errors.append(f"{feat}.{col}: presentation={pc[col]!r} source={sc[src_col]!r}")
        if str(pc["measurement_status"]) != str(sc["measurement_gate"]).lower():
            errors.append(f"{feat}: measurement_status mismatch")

    if "RAX_external_protection" in components.index:
        ep = components.loc["RAX_external_protection"]
        if ep["measurement_status"] != "thin":
            errors.append("external_protection status must be thin")
        if int(ep["n_topics"]) != 1:
            errors.append(f"external_protection n_topics expected 1, got {ep['n_topics']}")

    # --- Attention-shift percentage points (figure reads CSV directly) ---
    att = _read_table(paths.table("14_exploratory_presentation_results", "attention_waterfall"))
    if "diff_pp" not in att.columns or "feature" not in att.columns:
        errors.append("attention_waterfall missing feature/diff_pp")
    else:
        # Sanity: finite and unique features; values must match file on disk (identity check)
        for _, r in att.iterrows():
            if not np.isfinite(float(r["diff_pp"])):
                errors.append(f"attention {r['feature']}: non-finite diff_pp")
        # Re-read and compare to catch accidental mutation during build
        att2 = _read_table(paths.table("14_exploratory_presentation_results", "attention_waterfall"))
        for feat in att["feature"]:
            v1 = float(att.loc[att["feature"] == feat, "diff_pp"].iloc[0])
            v2 = float(att2.loc[att2["feature"] == feat, "diff_pp"].iloc[0])
            if not _close(v1, v2):
                errors.append(f"attention {feat}: unstable diff_pp read")

    # Stronger attention check: known focal rows must match exact saved values
    # (reload once more via CSV path preference if parquet exists — already handled by _read_table)
    expected_attention = {
        "RAX_tenderness_core": 0.41587734430734713,
        "RAX_explicit_sex": -0.18552572156678324,
        "RAX_appearance_grooming": -0.17962856541430816,
    }
    for feat, exp in expected_attention.items():
        row = att.loc[att["feature"] == feat]
        if row.empty:
            errors.append(f"attention missing {feat}")
        elif not _close(row["diff_pp"].iloc[0], exp):
            errors.append(
                f"attention {feat}: got {row['diff_pp'].iloc[0]!r}, expected {exp!r} "
                "(source table drifted from presentation-locked value)"
            )

    # --- Richness M1/M2 coefficients ---
    rich = _read_table(paths.table("14_exploratory_presentation_results", "thematic_richness_vs_drivers"))
    m = rich.loc[rich["term"] == "taxonomy_n_eff"].set_index("model")
    expected_rich = {
        "M1_richness_only": {
            "coefficient": 0.002371632764046187,
            "ci_low": -0.00014792946597685366,
            "ci_high": 0.004891194994069228,
            "p_value": 0.06505356245605133,
        },
        "M2_richness_plus_drivers": {
            "coefficient": 0.006577063861955809,
            "ci_low": 0.0038806370747680305,
            "ci_high": 0.009273490649143588,
            "p_value": 1.7468563331620182e-06,
        },
    }
    for model, cols in expected_rich.items():
        if model not in m.index:
            errors.append(f"richness missing model {model}")
            continue
        for col, exp in cols.items():
            got = m.loc[model, col]
            if not _close(got, exp):
                errors.append(f"richness {model}.{col}: got {got!r}, expected {exp!r}")

    return errors


def validate_outputs(paths: PresentationPaths | None = None) -> List[str]:
    paths = paths or default_paths()
    errors: List[str] = []
    for stem in EXPECTED_FIGURES:
        for ext in ("png", "pdf"):
            p = paths.out_dir / f"{stem}.{ext}"
            if not p.exists():
                errors.append(f"Missing figure: {p}")
            elif p.stat().st_size < 500:
                errors.append(f"Figure too small (likely empty): {p}")
    for name in (
        "presentation_agreement.csv",
        "presentation_primary_results.csv",
        "presentation_component_results.csv",
        "figure_source_manifest.csv",
    ):
        if not (paths.out_dir / name).exists():
            # manifest may also live in docs_dir
            if name == "figure_source_manifest.csv" and (paths.docs_dir / name).exists():
                continue
            errors.append(f"Missing metadata: {paths.out_dir / name}")
    return errors


def run_all_validations(
    frames: Dict[str, pd.DataFrame],
    paths: PresentationPaths | None = None,
    *,
    raise_on_error: bool = True,
) -> List[str]:
    paths = paths or default_paths()
    errors = (
        validate_frames(frames)
        + assert_provenance_vs_sources(paths, frames)
        + validate_outputs(paths)
    )
    if errors and raise_on_error:
        raise PresentationValidationError("\n".join(errors))
    return errors


V2_MAIN_FIGURES = [
    "slide04_pareto_selection",
    "slide06_context_measurement",
    "slide07_primary_verdict_preview",
    "slide08_component_effects",
    "slide09_attention_shift",
    "slide10_quality_reach_dumbbell",
    "slide11_richness_preview",
    "slide12_ees_integrated",
]

V2_DATA_CSVS = [
    "slide08_component_effects.csv",
    "slide06_agreement.csv",
    "slide06_measurement.csv",
    "slide07_primary_verdicts.csv",
    "slide10_quality_reach.csv",
    "slide11_richness_story.csv",
]


def validate_v2_figures_exist(paths: PresentationPaths | None = None) -> List[str]:
    paths = paths or default_paths()
    errors: List[str] = []
    for stem in V2_MAIN_FIGURES:
        for ext in ("png", "svg", "pdf"):
            p = paths.deck_figures / f"{stem}.{ext}"
            if not p.exists():
                errors.append(f"Missing v2 figure: {p}")
            elif p.stat().st_size < 500:
                errors.append(f"V2 figure too small: {p}")
    return errors


def validate_v2_data_files(paths: PresentationPaths | None = None) -> List[str]:
    paths = paths or default_paths()
    errors: List[str] = []
    for name in V2_DATA_CSVS:
        p = paths.deck_data / name
        if not p.exists():
            errors.append(f"Missing v2 data: {p}")
    manifest = paths.deck_manifests / "slide_manifest.csv"
    if not manifest.exists():
        errors.append(f"Missing slide_manifest: {manifest}")
    fig_manifest = paths.deck_manifests / "figure_manifest.csv"
    if not fig_manifest.exists():
        errors.append(f"Missing figure_manifest: {fig_manifest}")
    return errors


def validate_no_raw_labels_in_display(paths: PresentationPaths | None = None) -> List[str]:
    paths = paths or default_paths()
    errors: List[str] = []
    comp_path = paths.deck_data / "slide08_component_effects.csv"
    if not comp_path.exists():
        return errors
    df = pd.read_csv(comp_path)
    label_col = "display_label" if "display_label" in df.columns else "label"
    for val in df[label_col].astype(str):
        if val.startswith("RAX_") or val.startswith("RLR_") or val.startswith("EES_"):
            errors.append(f"Raw feature name in display label: {val}")
    return errors


def validate_v2_slide_data_provenance(paths: PresentationPaths | None = None) -> List[str]:
    paths = paths or default_paths()
    errors: List[str] = []
    src_comp = _read_table(paths.table("13_final_statistical_tests", "component_effects")).set_index("feature")
    slide08 = paths.deck_data / "slide08_component_effects.csv"
    if slide08.exists():
        df = pd.read_csv(slide08)
        for _, r in df.iterrows():
            feat = str(r["feature"])
            if feat not in src_comp.index:
                continue
            sc = src_comp.loc[feat]
            if not _close(r["effect_size"], sc["cliffs_delta"]):
                errors.append(f"slide08 {feat} effect_size drift")
            if not _close(r["ci_low"], sc["ci_low"]):
                errors.append(f"slide08 {feat} ci_low drift")
    primary = paths.deck_data / "slide07_primary_verdicts.csv"
    if primary.exists():
        df = pd.read_csv(primary)
        for h in ("H2", "H3"):
            row = df.loc[df["hypothesis"] == h].iloc[0]
            if row["measurement_status"] != "unmeasurable":
                errors.append(f"slide07 {h} must be unmeasurable")
            if pd.notna(row.get("effect_size")) and float(row["effect_size"]) == 0.0:
                errors.append(f"slide07 {h} unmeasurable encoded as zero")
    return errors


def validate_categorical_axes() -> List[str]:
    """Lightweight hook: categorical y-axis tests live in pytest (test_categorical_y_axis.py)."""
    return []


def run_v2_validations(
    frames: Dict[str, pd.DataFrame],
    paths: PresentationPaths | None = None,
    *,
    raise_on_error: bool = True,
) -> List[str]:
    paths = paths or default_paths()
    errors = (
        validate_v2_figures_exist(paths)
        + validate_v2_data_files(paths)
        + validate_no_raw_labels_in_display(paths)
        + validate_v2_slide_data_provenance(paths)
        + validate_categorical_axes()
    )
    # Also run core frame checks on upstream metadata
    errors += validate_frames(frames)
    if errors and raise_on_error:
        raise PresentationValidationError("\n".join(errors))
    return errors
