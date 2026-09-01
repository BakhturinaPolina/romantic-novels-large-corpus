"""Prepare tidy presentation dataframes per slide (CSV-before-plot)."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd

from .annotations import write_csv
from .catalogs import (
    build_corpus_stats,
    build_quality_reach_catalog,
    build_representative_examples,
    build_richness_story,
)
from .evidence_metadata import _read_table, build_all_metadata, load_agreement, load_components, load_primaries
from .paths import PARETO_SELECTED_CALL, PresentationPaths, default_paths
from .theme import EFFECT_GATE


def _merge_labels(df: pd.DataFrame, paths: PresentationPaths, feature_col: str = "feature") -> pd.DataFrame:
    theme_path = paths.deck_tables / "theme_dictionary.csv"
    if theme_path.exists():
        theme = pd.read_csv(theme_path)
    else:
        from .catalogs import build_theme_dictionary

        theme = build_theme_dictionary(paths)
    out = df.merge(theme[["feature", "slide_label", "short_label"]], left_on=feature_col, right_on="feature", how="left")
    out["display_label"] = out["slide_label"].fillna(out.get("label", out[feature_col]))
    return out


def _apply_selection(df: pd.DataFrame, slide_id: str, paths: PresentationPaths, feature_col: str = "feature") -> pd.DataFrame:
    sel_path = paths.deck_annotations / "slide_feature_selection.csv"
    if not sel_path.exists():
        return df
    sel = pd.read_csv(sel_path)
    sel = sel.loc[(sel["slide_id"] == slide_id) & (sel["include"] == 1)]
    if sel.empty:
        return df
    order = sel.set_index(feature_col)["display_order"].to_dict()
    emphasis = sel.set_index(feature_col)["emphasis"].to_dict()
    out = df.loc[df[feature_col].isin(sel["feature"])].copy()
    out["display_order"] = out[feature_col].map(order)
    out["emphasis"] = out[feature_col].map(emphasis)
    return out.sort_values("display_order")


def prepare_component_effects(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    meta = build_all_metadata(paths, write=False)
    df = meta["presentation_component_results"].copy()
    df = _merge_labels(df, paths, "feature")
    df = _apply_selection(df, "S08", paths, "feature")
    if "display_order" not in df.columns:
        # Default focus order from storyboard
        default_order = [
            "RAX_emotional_reassurance",
            "RAX_tenderness_core",
            "RAX_appearance_grooming",
            "RAX_external_danger_crisis",
            "RAX_external_protection",
            "RAX_explicit_sex",
        ]
        rank = {f: i for i, f in enumerate(default_order)}
        df["display_order"] = df["feature"].map(rank)
        df = df.sort_values("display_order")
    write_csv(df, paths.deck_data / "slide08_component_effects.csv")
    return df


def prepare_context_measurement(paths: PresentationPaths | None = None) -> Dict[str, pd.DataFrame]:
    paths = paths or default_paths()
    agreement = load_agreement(paths)
    primary = load_primaries(paths)
    write_csv(agreement, paths.deck_data / "slide06_agreement.csv")
    write_csv(primary, paths.deck_data / "slide06_measurement.csv")
    return {"agreement": agreement, "primary": primary}


def prepare_primary_verdicts(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    df = load_primaries(paths)
    write_csv(df, paths.deck_data / "slide07_primary_verdicts.csv")
    return df


def prepare_quality_reach_dumbbell(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    catalog = build_quality_reach_catalog(paths)
    catalog = catalog.loc[catalog["analysis_resolution"] == "taxonomy_leaf"].copy()
    # Strongest disagreements: large |quality_delta - reach_delta|
    catalog["delta_gap"] = catalog["quality_delta"] - catalog["reach_delta"]
    catalog["abs_gap"] = catalog["delta_gap"].abs()
    # Prespecified focal features from storyboard
    focal_features = [
        ("abs_leaf_7.2", "Violence / coercion"),
        ("abs_leaf_3.4", "Moral reflection"),
        ("abs_leaf_1.6", "Appearance / grooming"),
        ("abs_leaf_2.3", "Explicit sexual acts"),
        ("abs_leaf_4.4", "Conflict / breakup"),
        ("abs_leaf_4.5", "HEA / reconciliation"),
    ]
    selected = []
    for feat, short in focal_features:
        match = catalog.loc[catalog["feature"] == feat]
        if not match.empty:
            row = match.iloc[0].to_dict()
            row["short_label"] = short
            selected.append(row)
    if len(selected) < 5:
        top = catalog.nlargest(6, "abs_gap")
        for _, r in top.iterrows():
            if not any(s.get("feature") == r["feature"] for s in selected):
                d = r.to_dict()
                d["short_label"] = str(r["label"])[:35]
                selected.append(d)
    df = pd.DataFrame(selected).drop_duplicates(subset=["feature"])
    df["both_clear_gate"] = df["quality_gate"].astype(bool) & df["reach_gate"].astype(bool)
    write_csv(df, paths.deck_data / "slide10_quality_reach.csv")
    return df


def prepare_attention_shift(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    att = _read_table(paths.table("14_exploratory_presentation_results", "attention_waterfall"))
    att = _merge_labels(att, paths, "feature")
    att = _apply_selection(att, "S09", paths, "feature")
    if "display_order" not in att.columns:
        default_feats = [
            "RAX_tenderness_core",
            "RAX_explicit_sex",
            "RAX_appearance_grooming",
            "RAX_h3_emotional_side",
            "RAX_external_danger_crisis",
        ]
        rank = {f: i for i, f in enumerate(default_feats)}
        att = att.loc[att["feature"].isin(default_feats)].copy()
        att["display_order"] = att["feature"].map(rank)
        att = att.sort_values("display_order")
    write_csv(att, paths.deck_data / "slide09_attention_shift.csv")
    return att


def prepare_richness_evidence(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    df = build_richness_story(paths)
    write_csv(df, paths.deck_data / "slide11_richness_story.csv")
    return df


def prepare_pareto_points(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    trials = pd.read_csv(paths.pareto_trials)
    if "bo_call" in trials.columns:
        trials["is_selected"] = trials["bo_call"] == PARETO_SELECTED_CALL
    else:
        trials["is_selected"] = trials["trial_id"].astype(str).str.contains(f"call_{PARETO_SELECTED_CALL}")
    # Pareto efficient: not dominated on coherence + diversity
    coords = trials[["coherence_c_v", "topic_diversity"]].to_numpy()
    n = len(trials)
    pareto = np.ones(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if (
                coords[j, 0] >= coords[i, 0]
                and coords[j, 1] >= coords[i, 1]
                and (coords[j, 0] > coords[i, 0] or coords[j, 1] > coords[i, 1])
            ):
                pareto[i] = False
                break
    trials["pareto_efficient"] = pareto
    trials["n_topics_ok"] = trials["n_topics"] >= 20
    write_csv(trials, paths.deck_data / "slide04_pareto_points.csv")
    return trials


def prepare_ees_integrated(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    rows = []
    domain_tables = [
        ("emotion", "emotion_effects"),
        ("embodiment", "embodiment_effects"),
        ("social", "family_social_effects"),
    ]
    stability = None
    try:
        stability = _read_table(
            paths.table("15_emotion_embodiment_social_world_exploration", "author_split_stability")
        )
    except Exception:
        pass
    sel_path = paths.deck_annotations / "slide_feature_selection.csv"
    sel_feats = set()
    if sel_path.exists():
        sel = pd.read_csv(sel_path)
        sel_feats = set(sel.loc[(sel["slide_id"] == "S12") & (sel["include"] == 1), "feature"])

    default_feats = {
        "emotion_containment",
        "emotion_coregulation",
        "felt_body",
        "supportive_social_embeddedness",
        "body_grooming",
    }
    target = sel_feats or default_feats

    for domain, table in domain_tables:
        df = _read_table(paths.table("15_emotion_embodiment_social_world_exploration", table))
        for _, r in df.iterrows():
            construct = str(r["construct"])
            if construct not in target:
                continue
            status = str(r.get("status", "measurable"))
            if status == "unmeasurable":
                continue
            stable = True
            if stability is not None and construct in stability.get("construct", pd.Series()).values:
                sr = stability.loc[stability["construct"] == construct].iloc[0]
                da = sr.get("delta_half_A")
                db = sr.get("delta_half_B")
                if pd.notna(da) and pd.notna(db):
                    stable = (da >= 0) == (db >= 0)
            rows.append(
                {
                    "construct": construct,
                    "domain": domain,
                    "cliffs_delta": float(r["cliffs_delta"]),
                    "ci_low": float(r["ci_low"]),
                    "ci_high": float(r["ci_high"]),
                    "status": status,
                    "n_topics": r.get("n_topics"),
                    "author_split_stable": stable,
                }
            )
    out = pd.DataFrame(rows)
    out = _merge_labels(out, paths, "construct")
    write_csv(out, paths.deck_data / "slide12_ees_integrated.csv")
    return out


def prepare_topic_card(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    cards = _read_table(paths.table("14_exploratory_presentation_results", "security_care_topic_cards"))
    # Pick emotional reassurance example (topic 6 Whispered Reassurance)
    pick = cards.loc[cards["topic_label"].str.contains("Reassurance|reassurance", na=False)]
    if pick.empty:
        pick = cards.head(1)
    else:
        pick = pick.head(1)
    write_csv(pick, paths.deck_data / "slide05_topic_card.csv")
    return pick


def prepare_representative_passages(paths: PresentationPaths | None = None) -> pd.DataFrame:
    paths = paths or default_paths()
    sentences = _read_table(
        paths.table("14_exploratory_presentation_results", "representative_topic_sentences")
    )
    rows = []
    # Appearance / grooming — deterministic topic evidence
    app = sentences.loc[sentences["feature"] == "RAX_appearance_grooming"]
    app = app.loc[app["example_sentence"].astype(str).str.len() > 5]
    if not app.empty:
        r = app.iloc[0]
        rows.append(
            {
                "example_id": "appearance_main",
                "construct": "RAX_appearance_grooming",
                "direction": "lower_in_high_rated",
                "effect_label": "δ −0.14",
                "topic_id": r["topic_id"],
                "topic_label": r["topic_label"],
                "sentence": r["example_sentence"],
                "sentence_short": str(r["example_sentence"])[:120],
                "selection_method": "deterministic_seed42",
                "use_main": True,
            }
        )
    # Emotional reassurance — topic card evidence (not in representative_topic_sentences)
    cards = _read_table(paths.table("14_exploratory_presentation_results", "security_care_topic_cards"))
    reass = cards.loc[cards["topic_label"].str.contains("Reassurance|reassurance", na=False)]
    if not reass.empty:
        r = reass.iloc[0]
        rows.append(
            {
                "example_id": "reassurance_main",
                "construct": "RAX_emotional_reassurance",
                "direction": "higher_in_high_rated",
                "effect_label": "δ +0.14",
                "topic_id": r["topic_id"],
                "topic_label": r["topic_label"],
                "sentence": r["example_sentence"],
                "sentence_short": str(r["example_sentence"])[:120],
                "selection_method": "topic_card_whispered_reassurance",
                "use_main": True,
            }
        )
    out = pd.DataFrame(rows)
    write_csv(out, paths.deck_data / "slide13_representative_examples.csv")
    return out


def prepare_all_slide_data(paths: PresentationPaths | None = None) -> Dict[str, pd.DataFrame]:
    paths = paths or default_paths()
    paths.ensure_deck_dirs()
    return {
        "slide04": prepare_pareto_points(paths),
        "slide05": prepare_topic_card(paths),
        "slide06": pd.concat(
            [
                prepare_context_measurement(paths)["agreement"],
                prepare_context_measurement(paths)["primary"],
            ]
        ),
        "slide07": prepare_primary_verdicts(paths),
        "slide08": prepare_component_effects(paths),
        "slide09": prepare_attention_shift(paths),
        "slide10": prepare_quality_reach_dumbbell(paths),
        "slide11": prepare_richness_evidence(paths),
        "slide12": prepare_ees_integrated(paths),
        "slide13": prepare_representative_passages(paths),
        "corpus_stats": build_corpus_stats(paths),
    }
