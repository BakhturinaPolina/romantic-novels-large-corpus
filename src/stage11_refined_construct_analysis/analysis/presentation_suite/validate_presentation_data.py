"""Validate presentation metadata and generated figure files."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd

from .paths import PresentationPaths, default_paths
from .theme import EFFECT_GATE, HYPOTHESIS_ORDER

ALLOWED_MEASUREMENT = {"viable", "thin", "unmeasurable"}

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
    errors = validate_frames(frames) + validate_outputs(paths)
    if errors and raise_on_error:
        raise PresentationValidationError("\n".join(errors))
    return errors
