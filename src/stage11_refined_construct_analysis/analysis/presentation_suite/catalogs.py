"""Build presentation catalog CSVs from upstream notebook tables."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from .evidence_metadata import _read_table, load_components, load_primaries
from .paths import PresentationPaths, default_paths
from .theme import EFFECT_GATE

# Seed human-readable labels for common presentation features
THEME_DICTIONARY_SEED: Dict[str, dict] = {
    "RAX_emotional_reassurance": {
        "short_label": "Emotional reassurance",
        "slide_label": "Emotional reassurance",
        "full_label": "Emotional reassurance / interpersonal support",
        "family": "intimacy",
        "evidence_level": "confirmatory_component",
    },
    "RAX_tenderness_core": {
        "short_label": "Tenderness",
        "slide_label": "Tenderness",
        "full_label": "Tenderness core",
        "family": "darkness_tenderness",
        "evidence_level": "confirmatory_component",
    },
    "RAX_appearance_grooming": {
        "short_label": "Appearance",
        "slide_label": "Appearance & grooming",
        "full_label": "External appearance and grooming",
        "family": "appearance",
        "evidence_level": "confirmatory_component",
    },
    "RAX_external_danger_crisis": {
        "short_label": "External danger",
        "slide_label": "External danger",
        "full_label": "External danger / crisis",
        "family": "darkness_tenderness",
        "evidence_level": "confirmatory_component",
    },
    "RAX_external_protection": {
        "short_label": "External protection",
        "slide_label": "External protection",
        "full_label": "External protection (enacted care)",
        "family": "protection",
        "evidence_level": "confirmatory_component",
    },
    "RAX_explicit_sex": {
        "short_label": "Explicit sex",
        "slide_label": "Explicit sex",
        "full_label": "Explicit sexual acts",
        "family": "intimacy",
        "evidence_level": "confirmatory_component",
    },
    "emotion_containment": {
        "short_label": "Emotional containment",
        "slide_label": "Emotional containment",
        "full_label": "Emotion regulation / containment",
        "family": "emotion",
        "evidence_level": "exploratory_ees",
    },
    "emotion_coregulation": {
        "short_label": "Co-regulation",
        "slide_label": "Emotional co-regulation",
        "full_label": "Interpersonal emotional co-regulation",
        "family": "emotion",
        "evidence_level": "exploratory_ees",
    },
    "felt_body": {
        "short_label": "Felt body",
        "slide_label": "Felt body",
        "full_label": "Interoceptive / felt embodiment",
        "family": "embodiment",
        "evidence_level": "exploratory_ees",
    },
    "supportive_social_embeddedness": {
        "short_label": "Supportive social world",
        "slide_label": "Supportive social world",
        "full_label": "Supportive social embeddedness",
        "family": "social",
        "evidence_level": "exploratory_ees",
    },
    "body_grooming": {
        "short_label": "Body grooming",
        "slide_label": "Body grooming",
        "full_label": "Embodied grooming attention",
        "family": "embodiment",
        "evidence_level": "exploratory_ees",
    },
}


def build_theme_dictionary(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    rows = []
    for feature, meta in THEME_DICTIONARY_SEED.items():
        rows.append({"feature": feature, **meta})
    # Enrich from component effects
    try:
        comp = load_components(paths)
        for _, r in comp.iterrows():
            feat = str(r["feature"])
            if feat not in THEME_DICTIONARY_SEED:
                rows.append(
                    {
                        "feature": feat,
                        "short_label": str(r["label"]),
                        "slide_label": str(r["label"]),
                        "full_label": str(r["label"]),
                        "family": str(r.get("hypothesis", "")),
                        "evidence_level": "confirmatory_component",
                    }
                )
    except Exception:
        pass
    # Stage 10 leaf labels
    try:
        leaves = _read_table(paths.stage10_table("06_goodreads_validation", "leaf_deltas_both_tierings"))
        for _, r in leaves.iterrows():
            feat = str(r["feature"])
            if not any(x["feature"] == feat for x in rows):
                rows.append(
                    {
                        "feature": feat,
                        "short_label": str(r["label"])[:40],
                        "slide_label": str(r["label"]),
                        "full_label": str(r["label"]),
                        "family": "taxonomy_leaf",
                        "evidence_level": "exploratory",
                    }
                )
    except Exception:
        pass
    return pd.DataFrame(rows).drop_duplicates(subset=["feature"], keep="first")


def build_effect_catalog(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    rows: list[dict] = []
    primary = load_primaries(paths)
    for _, r in primary.iterrows():
        rows.append(
            {
                "construct_id": r["feature"],
                "label": r["label"],
                "family": r["hypothesis"],
                "analysis_layer": "confirmatory_primary",
                "hypothesis": r["hypothesis"],
                "effect_type": "cliffs_delta",
                "effect": r["effect_size"],
                "ci_low": r["ci_low"],
                "ci_high": r["ci_high"],
                "adjusted_effect": r["adjusted_coefficient"],
                "adjusted_p": r["adjusted_p_value"],
                "measurement_status": r["measurement_status"],
                "effect_gate": EFFECT_GATE,
                "clears_gate": r["clears_delta_gate"],
                "confirmatory_status": r["verdict"],
                "source_notebook": "13_final_statistical_tests",
                "source_table": "primary_h1_h6_table",
            }
        )
    comp = load_components(paths)
    for _, r in comp.iterrows():
        rows.append(
            {
                "construct_id": r["feature"],
                "label": r["label"],
                "family": r["hypothesis"],
                "analysis_layer": "confirmatory_component",
                "hypothesis": r["hypothesis"],
                "effect_type": "cliffs_delta",
                "effect": r["effect_size"],
                "ci_low": r["ci_low"],
                "ci_high": r["ci_high"],
                "n_topics": r["n_topics"],
                "adjusted_effect": r["adjusted_coefficient"],
                "adjusted_p": r["adjusted_p_value"],
                "measurement_status": r["measurement_status"],
                "effect_gate": EFFECT_GATE,
                "clears_gate": r["clears_delta_gate"],
                "confirmatory_status": r["verdict"],
                "source_notebook": "13_final_statistical_tests",
                "source_table": "component_effects",
            }
        )
    # EES exploratory
    try:
        for domain, table in (
            ("emotion", "emotion_effects"),
            ("embodiment", "embodiment_effects"),
            ("social", "family_social_effects"),
        ):
            df = _read_table(paths.table("15_emotion_embodiment_social_world_exploration", table))
            for _, r in df.iterrows():
                rows.append(
                    {
                        "construct_id": r["construct"],
                        "label": r["construct"],
                        "family": domain,
                        "analysis_layer": "exploratory_ees",
                        "hypothesis": "",
                        "effect_type": "cliffs_delta",
                        "effect": r["cliffs_delta"],
                        "ci_low": r["ci_low"],
                        "ci_high": r["ci_high"],
                        "n_topics": r.get("n_topics"),
                        "adjusted_effect": r.get("ols_beta"),
                        "measurement_status": r.get("status", "measurable"),
                        "effect_gate": EFFECT_GATE,
                        "clears_gate": abs(float(r["cliffs_delta"])) >= EFFECT_GATE,
                        "confirmatory_status": r.get("verdict", ""),
                        "source_notebook": "15_emotion_embodiment_social_world_exploration",
                        "source_table": table,
                    }
                )
    except Exception:
        pass
    return pd.DataFrame(rows)


def build_quality_reach_catalog(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    rows: list[dict] = []
    leaves = _read_table(paths.stage10_table("06_goodreads_validation", "leaf_deltas_both_tierings"))
    betas = _read_table(paths.stage10_table("06_goodreads_validation", "leaf_two_channel_betas"))
    beta_map = betas.set_index("feature") if "feature" in betas.columns else pd.DataFrame()
    for _, r in leaves.iterrows():
        feat = str(r["feature"])
        row = {
            "feature": feat,
            "label": r["label"],
            "analysis_resolution": "taxonomy_leaf",
            "quality_delta": r["delta_rating"],
            "quality_ci_low": r["rating_ci_low"],
            "quality_ci_high": r["rating_ci_high"],
            "reach_delta": r["delta_reach"],
            "reach_ci_low": r["reach_ci_low"],
            "reach_ci_high": r["reach_ci_high"],
            "quality_gate": bool(r["rating_clears_gate"]),
            "reach_gate": bool(r["reach_clears_gate"]),
            "same_direction": bool(r["same_direction"]),
            "quality_beta": np.nan,
            "reach_beta": np.nan,
            "beta_gap": np.nan,
        }
        if feat in beta_map.index:
            b = beta_map.loc[feat]
            row["quality_beta"] = b.get("quality_beta", np.nan)
            row["reach_beta"] = b.get("reach_beta", np.nan)
            row["beta_gap"] = b.get("beta_gap", np.nan)
        rows.append(row)
    # Optional NB16 refined shortlist
    try:
        nb16 = _read_table(
            paths.table("16_refined_goodreads_quality_reach", "presentation_quality_reach_shortlist")
        )
        for _, r in nb16.iterrows():
            rows.append(
                {
                    "feature": r["feature"],
                    "label": r["display_label"],
                    "analysis_resolution": "refined_construct",
                    "quality_delta": r.get("delta_rating", np.nan),
                    "reach_delta": r.get("delta_reach", np.nan),
                    "quality_beta": r.get("quality_beta", np.nan),
                    "reach_beta": r.get("reach_beta", np.nan),
                    "beta_gap": r.get("beta_gap", np.nan),
                    "quality_gate": np.nan,
                    "reach_gate": np.nan,
                    "same_direction": np.nan,
                }
            )
    except Exception:
        pass
    return pd.DataFrame(rows)


def build_richness_story(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    cliffs = _read_table(paths.table("14_exploratory_presentation_results", "thematic_richness_cliffs_delta"))
    ols = _read_table(paths.table("14_exploratory_presentation_results", "thematic_richness_ols"))
    drivers = _read_table(paths.table("14_exploratory_presentation_results", "thematic_richness_vs_drivers"))

    def _cliff(feat: str) -> dict:
        r = cliffs.loc[cliffs["feature"] == feat].iloc[0]
        return {
            "estimate": float(r["cliffs_delta"]),
            "ci_low": float(r["ci_low"]),
            "ci_high": float(r["ci_high"]),
        }

    raw_tax = _cliff("taxonomy_n_eff")
    raw_top = _cliff("topic_n_eff")
    rare = ols.loc[ols["feature"] == "rare_taxonomy_n_eff"].iloc[0]
    m2 = drivers.loc[
        (drivers["model"] == "M2_richness_plus_drivers") & (drivers["term"] == "taxonomy_n_eff")
    ].iloc[0]

    return pd.DataFrame(
        [
            {
                "analysis": "raw_taxonomy_delta",
                "metric": "taxonomy_n_eff",
                "estimate": raw_tax["estimate"],
                "ci_low": raw_tax["ci_low"],
                "ci_high": raw_tax["ci_high"],
                "p_value": np.nan,
                "interpretation": "Higher-rated books look more diverse (taxonomy)",
            },
            {
                "analysis": "raw_topic_delta",
                "metric": "topic_n_eff",
                "estimate": raw_top["estimate"],
                "ci_low": raw_top["ci_low"],
                "ci_high": raw_top["ci_high"],
                "p_value": np.nan,
                "interpretation": "Higher-rated books look more diverse (topics)",
            },
            {
                "analysis": "rarefied_taxonomy",
                "metric": "rare_taxonomy_n_eff",
                "estimate": float(rare["coefficient"]),
                "ci_low": float(rare["ci_low"]),
                "ci_high": float(rare["ci_high"]),
                "p_value": float(rare["p_value"]),
                "interpretation": "No remaining association after equal sentence budget",
            },
            {
                "analysis": "controlled_taxonomy",
                "metric": "taxonomy_n_eff",
                "estimate": float(
                    drivers.loc[
                        (drivers["model"] == "M1_richness_only") & (drivers["term"] == "taxonomy_n_eff")
                    ].iloc[0]["coefficient"]
                ),
                "p_value": float(
                    drivers.loc[
                        (drivers["model"] == "M1_richness_only") & (drivers["term"] == "taxonomy_n_eff")
                    ].iloc[0]["p_value"]
                ),
                "ci_low": np.nan,
                "ci_high": np.nan,
                "interpretation": "Raw OLS before thematic drivers",
            },
            {
                "analysis": "controlled_plus_drivers",
                "metric": "taxonomy_n_eff",
                "estimate": float(m2["coefficient"]),
                "ci_low": float(m2["ci_low"]),
                "ci_high": float(m2["ci_high"]),
                "p_value": float(m2["p_value"]),
                "interpretation": "Suppression: richness strengthens after controlling drivers",
            },
        ]
    )


def build_representative_examples(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    sentences = _read_table(
        paths.table("14_exploratory_presentation_results", "representative_topic_sentences")
    )
    rows = []
    for _, r in sentences.iterrows():
        sent = str(r.get("example_sentence", ""))
        rows.append(
            {
                "example_id": f"{r['feature']}_{r.get('topic_id', '')}",
                "construct": r["feature"],
                "topic_id": r.get("topic_id"),
                "topic_label": r.get("topic_label"),
                "sentence": sent,
                "sentence_short": sent[:120] if sent else "",
                "selection_method": "deterministic_seed42",
                "seed": 42,
                "use_main": r["feature"]
                in ("RAX_emotional_reassurance", "RAX_appearance_grooming", "RAX_h3_emotional_side"),
            }
        )
    return pd.DataFrame(rows)


def build_corpus_stats(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    return pd.DataFrame(
        [
            {"metric": "novels", "value": 16000, "label": "16,000 novels"},
            {"metric": "authors", "value": 8264, "label": "8,264 authors"},
            {"metric": "sentences", "value": 115_600_000, "label": "115.6M sentences"},
            {"metric": "years", "value": "2000–2017", "label": "2000–2017 publication years"},
        ]
    )


def build_all_catalogs(
    paths: PresentationPaths | None = None,
    *,
    write: bool = True,
) -> Dict[str, pd.DataFrame]:
    paths = paths or default_paths()
    paths.ensure_deck_dirs()
    frames = {
        "theme_dictionary": build_theme_dictionary(paths),
        "effect_catalog": build_effect_catalog(paths),
        "quality_reach_catalog": build_quality_reach_catalog(paths),
        "richness_story": build_richness_story(paths),
        "representative_examples": build_representative_examples(paths),
        "corpus_stats": build_corpus_stats(paths),
    }
    if write:
        for name, df in frames.items():
            df.to_csv(paths.deck_tables / f"{name}.csv", index=False)
    return frames
