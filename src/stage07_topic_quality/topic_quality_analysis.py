"""Topic quality analysis and noisy topic detection for BERTopic models."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from bertopic import BERTopic
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel

from src.common.topic_posthoc.rules import (
    NOISE_ACTION,
    classify_topics_from_info,
)

from src.stage06_topic_exploration.explore_retrained_model import (
    LOGGER,
    extract_all_topics,
    stage_timer,
)

# Use the same logger as stage06_topic_exploration for consistency
logger = LOGGER


def merge_name_cleaning_flags(
    quality_df: pd.DataFrame,
    ratio_csv: Path,
) -> pd.DataFrame:
    """Merge character-name cleaning flags from ratio CSV into quality table."""
    if not Path(ratio_csv).is_file():
        logger.warning("Name cleaning ratio CSV not found: %s", ratio_csv)
        return quality_df

    ratio_df = pd.read_csv(ratio_csv)
    if "Topic" not in ratio_df.columns:
        logger.warning("Name cleaning CSV missing Topic column: %s", ratio_csv)
        return quality_df

    merge_cols = [
        "Topic",
        "character_name_ratio",
        "content_type",
        "posthoc_flags",
        "posthoc_reason",
        "exclude_from_axes",
        "name_cleaned",
        "suggested_action",
    ]
    merge_cols = [c for c in merge_cols if c in ratio_df.columns]
    name_subset = ratio_df[merge_cols].copy()
    name_subset = name_subset[name_subset["Topic"] != -1]

    merged = quality_df.merge(name_subset, on="Topic", how="left", suffixes=("_old", ""))

    for col in ("content_type", "posthoc_flags", "posthoc_reason", "exclude_from_axes", "suggested_action"):
        old_col = f"{col}_old"
        if old_col in merged.columns:
            if col == "posthoc_flags":
                def _combine_flags(row: pd.Series) -> list:
                    old = row.get(old_col)
                    new = row.get(col)
                    old_list = old if isinstance(old, list) else []
                    new_list = new if isinstance(new, list) else []
                    if isinstance(old, str) and old:
                        old_list = [p for p in old.split("|") if p]
                    if isinstance(new, str) and new:
                        new_list = [p for p in new.split("|") if p]
                    combined: list[str] = []
                    for f in list(old_list) + list(new_list):
                        if f and f not in combined:
                            combined.append(f)
                    return combined

                merged[col] = merged.apply(_combine_flags, axis=1)
            elif col == "posthoc_reason":
                merged[col] = merged.apply(
                    lambda r: ";".join(
                        p
                        for p in (str(r.get(f"{col}_old", "") or ""), str(r.get(col, "") or ""))
                        if p
                    ),
                    axis=1,
                )
            elif col == "exclude_from_axes":
                merged[col] = merged[old_col].fillna(False) | merged[col].fillna(False)
            else:
                merged[col] = merged[col].fillna(merged[old_col])
            merged.drop(columns=[old_col], inplace=True)

    if "name_cleaned" in merged.columns:
        merged["name_cleaned"] = merged["name_cleaned"].fillna(False)
    if "character_name_ratio" in merged.columns:
        merged["character_name_ratio"] = merged["character_name_ratio"].fillna(0.0)

    def _combined_reason(row: pd.Series) -> str:
        parts = []
        for key in ("noise_reason", "posthoc_reason"):
            val = str(row.get(key, "") or "").strip()
            if val:
                parts.extend(p for p in val.split(";") if p)
        seen: set[str] = set()
        deduped = []
        for p in parts:
            if p not in seen:
                seen.add(p)
                deduped.append(p)
        return ";".join(deduped)

    merged["noise_reason"] = merged.apply(_combined_reason, axis=1)
    merged["noise_candidate"] = (
        merged["noise_candidate"].astype(bool)
        | merged["exclude_from_axes"].astype(bool)
    )

    def _inspection_label(row: pd.Series) -> str:
        base_name = str(row.get("Name", "") or "").strip()
        posthoc_flags = row.get("posthoc_flags")
        if isinstance(posthoc_flags, list):
            noise_rules = [f for f in posthoc_flags if f]
        elif isinstance(posthoc_flags, str) and posthoc_flags:
            noise_rules = [p for p in posthoc_flags.split("|") if p]
        else:
            noise_rules = []
        if noise_rules and row.get("suggested_action") == NOISE_ACTION:
            rule_tag = noise_rules[0]
            return f"[NOISE:{rule_tag}] {base_name}"
        if row.get("name_cleaned"):
            return f"[NAME_CLEANED] {base_name}"
        reasons = row.get("noise_reason", "")
        if reasons:
            return f"[NOISE_CANDIDATE:{reasons}] {base_name}"
        return base_name

    merged["inspection_label"] = merged.apply(_inspection_label, axis=1)
    n_exclude = int(merged["exclude_from_axes"].sum())
    logger.info(
        "[NAME_CLEANING] merged into quality table: %d topics exclude_from_axes",
        n_exclude,
    )
    return merged


def merge_posthoc_flags(
    quality_df: pd.DataFrame,
    *,
    topic_info_path: Path | None = None,
    topic_info_df: pd.DataFrame | None = None,
    rules_config: Path | None = None,
) -> pd.DataFrame:
    """Merge rule-based post-hoc flags into a topic quality table."""
    if topic_info_df is not None:
        info_df = topic_info_df
    elif topic_info_path is not None:
        info_df = pd.read_csv(topic_info_path)
    else:
        logger.warning("No topic_info source for post-hoc merge; skipping rules")
        return quality_df

    classified = classify_topics_from_info(
        info_df, config_path=rules_config, logger=logger
    )
    posthoc_cols = [
        "Topic",
        "content_type",
        "posthoc_flags",
        "posthoc_reason",
        "exclude_from_axes",
        "suggested_action",
    ]
    posthoc_cols = [c for c in posthoc_cols if c in classified.columns]
    posthoc_subset = classified[posthoc_cols].copy()
    posthoc_subset = posthoc_subset[posthoc_subset["Topic"] != -1]

    merged = quality_df.merge(posthoc_subset, on="Topic", how="left")
    merged["posthoc_reason"] = merged["posthoc_reason"].fillna("")
    merged["exclude_from_axes"] = merged["exclude_from_axes"].fillna(False)

    def _combined_reason(row: pd.Series) -> str:
        parts = [p for p in (row.get("noise_reason", ""), row.get("posthoc_reason", "")) if p]
        return ";".join(parts)

    merged["noise_reason"] = merged.apply(_combined_reason, axis=1)
    merged["noise_candidate"] = (
        merged["noise_candidate"].astype(bool)
        | merged["exclude_from_axes"].astype(bool)
    )

    def _inspection_label(row: pd.Series) -> str:
        base_name = str(row.get("Name", "") or "").strip()
        posthoc_flags = row.get("posthoc_flags")
        if isinstance(posthoc_flags, list):
            noise_rules = [f for f in posthoc_flags if f]
        else:
            noise_rules = []
        if noise_rules and row.get("suggested_action") == NOISE_ACTION:
            rule_tag = noise_rules[0]
            return f"[NOISE:{rule_tag}] {base_name}"
        reasons = row.get("noise_reason", "")
        if reasons:
            return f"[NOISE_CANDIDATE:{reasons}] {base_name}"
        return base_name

    merged["inspection_label"] = merged.apply(_inspection_label, axis=1)
    n_posthoc = int(merged["exclude_from_axes"].sum())
    logger.info("[POSTHOC] merged into quality table: %d topics exclude_from_axes", n_posthoc)
    return merged


def get_topic_distribution(topic_model: BERTopic, min_size: int = 30) -> pd.DataFrame:
    """
    Get topic counts and a 'keep_by_size' flag.
    
    Args:
        topic_model: BERTopic model instance
        min_size: Minimum number of documents per topic to be considered valid
        
    Returns:
        DataFrame with columns: Topic, Count, Name, Representation, keep_by_size
    """
    info = topic_model.get_topic_info()
    # Exclude outlier topic -1
    info = info[info["Topic"] != -1].copy()
    info["keep_by_size"] = info["Count"] >= min_size
    return info


def get_pos_representation_stats(
    topic_model: BERTopic, top_k: int = 10
) -> pd.DataFrame:
    """
    Extract POS representation topics and basic stats.
    
    Args:
        topic_model: BERTopic model instance
        top_k: Number of top words per topic to consider
        
    Returns:
        DataFrame with columns: Topic, n_pos_words, pos_words
    """
    all_topics = extract_all_topics(topic_model, top_k=top_k)
    pos_topics = all_topics.get("POS", {})

    rows = []
    for topic_id, word_list in pos_topics.items():
        n_words = len(word_list)
        rows.append(
            {
                "Topic": topic_id,
                "n_pos_words": n_words,
                "pos_words": [w["word"] for w in word_list],
            }
        )

    if not rows:
        logger.warning("No POS topics found in extracted aspects.")
        return pd.DataFrame(columns=["Topic", "n_pos_words", "pos_words"])

    df = pd.DataFrame(rows).sort_values("Topic").reset_index(drop=True)
    return df


def compute_pos_coherence_per_topic(
    topic_model: BERTopic,
    docs_tokens: list[list[str]],
    dictionary: Dictionary,
    top_k: int = 10,
) -> pd.DataFrame:
    """
    Compute c_v coherence per topic, using POS representation words.
    
    We convert words to ids to align with Stage 06's dictionary usage.
    
    Args:
        topic_model: BERTopic model instance
        docs_tokens: List of tokenized documents
        dictionary: Gensim dictionary for coherence computation
        top_k: Number of top words per topic to consider
        
    Returns:
        DataFrame with columns: Topic, coherence_c_v_pos
    """
    all_topics = extract_all_topics(topic_model, top_k=top_k)
    pos_topics = all_topics.get("POS", {})

    topic_ids = []
    topic_ids_lists = []

    for topic_id, word_dicts in pos_topics.items():
        words = [w["word"] for w in word_dicts]
        ids = [dictionary.token2id[w] for w in words if w in dictionary.token2id]
        if not ids:
            continue
        topic_ids.append(topic_id)
        topic_ids_lists.append(ids)

    if not topic_ids_lists:
        logger.warning("No POS topics with valid dictionary tokens for coherence.")
        return pd.DataFrame(columns=["Topic", "coherence_c_v_pos"])

    with stage_timer("Computing per-topic POS coherence (c_v)"):
        cm = CoherenceModel(
            topics=topic_ids_lists,
            texts=docs_tokens,
            dictionary=dictionary,
            coherence="c_v",
        )
        scores = cm.get_coherence_per_topic()

    df = pd.DataFrame(
        {
            "Topic": topic_ids,
            "coherence_c_v_pos": scores,
        }
    ).sort_values("Topic").reset_index(drop=True)

    return df


def build_topic_quality_table(
    topic_model: BERTopic,
    docs_tokens: list[list[str]],
    dictionary: Dictionary,
    min_size: int = 30,
    min_pos_words: int = 3,
    min_pos_coherence: float = 0.0,
    top_k: int = 10,
    *,
    topic_info_path: Path | None = None,
    rules_config: Path | None = None,
    name_cleaning_csv: Path | None = None,
) -> pd.DataFrame:
    """
    Combine size, POS stats, and POS coherence; flag candidate noisy topics.
    
    This function does NOT remove topics from the model; it only flags them
    for manual inspection.
    
    Args:
        topic_model: BERTopic model instance
        docs_tokens: List of tokenized documents
        dictionary: Gensim dictionary for coherence computation
        min_size: Minimum number of documents per topic
        min_pos_words: Minimum number of POS words per topic
        min_pos_coherence: Minimum per-topic POS coherence threshold
        top_k: Number of top words per topic to consider
        topic_info_path: Optional path to topic_info.csv for post-hoc rule merge
        rules_config: Optional path to topic_posthoc_rules.yaml
        name_cleaning_csv: Optional path to character_name_ratio_by_topic.csv
        
    Returns:
        DataFrame with topic quality metrics and noise candidate flags
    """
    with stage_timer("Building topic quality table"):
        topic_info = get_topic_distribution(topic_model, min_size=min_size)
        pos_stats = get_pos_representation_stats(topic_model, top_k=top_k)
        pos_coh = compute_pos_coherence_per_topic(
            topic_model,
            docs_tokens=docs_tokens,
            dictionary=dictionary,
            top_k=top_k,
        )

        df = (
            topic_info[["Topic", "Count", "Name", "Representation"]]
            .merge(
                pos_stats[["Topic", "n_pos_words", "pos_words"]],
                on="Topic",
                how="left",
            )
            .merge(
                pos_coh[["Topic", "coherence_c_v_pos"]],
                on="Topic",
                how="left",
            )
        )

        # Flag conditions
        df["flag_small"] = df["Count"] < min_size
        df["flag_few_pos"] = df["n_pos_words"].fillna(0) < min_pos_words
        df["flag_low_coh"] = df["coherence_c_v_pos"].fillna(-1.0) < min_pos_coherence

        # Aggregate into noise_candidate + reason
        def _noise_reason(row) -> str:
            reasons = []
            if row["flag_small"]:
                reasons.append(f"small<{min_size}")
            if row["flag_few_pos"]:
                reasons.append(f"few_pos<{min_pos_words}")
            if row["flag_low_coh"]:
                reasons.append(f"low_coh<{min_pos_coherence:.2f}")
            return ";".join(reasons)

        df["noise_reason"] = df.apply(_noise_reason, axis=1)
        df["noise_candidate"] = df["noise_reason"].str.len() > 0

        # Label for manual inspection: prepend reason to topic name
        def _inspection_label(row) -> str:
            base_name = str(row.get("Name", "") or "").strip()
            reasons = row["noise_reason"]
            if not reasons:
                return base_name
            return f"[NOISE_CANDIDATE:{reasons}] {base_name}"

        df["inspection_label"] = df.apply(_inspection_label, axis=1)

        info_source = topic_info_path
        if info_source is None:
            try:
                full_info = topic_model.get_topic_info()
                df = merge_posthoc_flags(
                    df,
                    topic_info_df=full_info,
                    rules_config=rules_config,
                )
            except Exception as ex:
                logger.warning("Could not merge post-hoc flags from model: %s", ex)
        else:
            df = merge_posthoc_flags(
                df,
                topic_info_path=info_source,
                rules_config=rules_config,
            )

        if name_cleaning_csv is not None:
            df = merge_name_cleaning_flags(df, name_cleaning_csv)

        # Sort for easier EDA
        df.sort_values(
            ["noise_candidate", "coherence_c_v_pos", "Count"],
            ascending=[False, True, True],
            inplace=True,
        )
        df.reset_index(drop=True, inplace=True)

    return df


def apply_noise_labels_to_model(
    topic_model: BERTopic,
    quality_df: pd.DataFrame,
    only_noise_candidates: bool = True,
) -> dict[int, str]:
    """
    Build a label dictionary for topics based on quality analysis.
    
    Args:
        topic_model: BERTopic model instance
        quality_df: DataFrame from build_topic_quality_table
        only_noise_candidates: If True, only label noisy topics; if False, label all
        
    Returns:
        Dictionary mapping topic_id -> label string
    """
    if only_noise_candidates:
        candidates_df = quality_df[quality_df["noise_candidate"]]
    else:
        candidates_df = quality_df

    labels = {
        int(row.Topic): str(row.inspection_label)
        for row in candidates_df.itertuples(index=False)
    }

    logger.info(
        "Prepared %d labels for %s",
        len(labels),
        "noise candidates" if only_noise_candidates else "all topics",
    )

    return labels

