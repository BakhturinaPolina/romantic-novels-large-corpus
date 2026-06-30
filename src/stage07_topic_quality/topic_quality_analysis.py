"""Topic quality analysis and noisy topic detection for BERTopic models."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd
from bertopic import BERTopic
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel

from src.common.topic_posthoc.rules import (
    HARD_EXCLUDE_ACTION,
    SOFT_REVIEW_ACTION,
    classify_topics_from_info,
)
from src.stage06_topic_exploration.explore_retrained_model import (
    LOGGER,
    extract_all_topics,
    stage_timer,
)
from src.stage07_topic_quality.config import Stage07Config, load_stage07_config

logger = LOGGER

_CONTENT_POS_TAGS = frozenset({"NOUN", "VERB", "ADJ"})
_SPACY_NLP = None


def _get_spacy_nlp():
    global _SPACY_NLP
    if _SPACY_NLP is not None:
        return _SPACY_NLP
    try:
        import spacy

        _SPACY_NLP = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer"])
        return _SPACY_NLP
    except OSError:
        logger.warning("spaCy en_core_web_sm unavailable; content POS counts use word length")
        return None


def count_content_pos_words(words: list[str]) -> int:
    """Count NOUN/VERB/ADJ among topic keywords via spaCy."""
    if not words:
        return 0
    nlp = _get_spacy_nlp()
    if nlp is None:
        return len(words)
    doc = nlp(" ".join(words))
    return sum(1 for tok in doc if tok.pos_ in _CONTENT_POS_TAGS)


def load_topic_snippets(csv_path: Path, *, max_per_topic: int = 6) -> dict[int, list[str]]:
    """Load representative snippets grouped by topic from cleaned CSV."""
    if not Path(csv_path).is_file():
        logger.warning("Representative docs CSV not found: %s", csv_path)
        return {}

    df = pd.read_csv(csv_path)
    if "topic" not in df.columns or "sentence" not in df.columns:
        logger.warning("Representative docs CSV missing topic/sentence columns")
        return {}

    sort_cols = ["topic"]
    if "doc_rank" in df.columns:
        sort_cols.append("doc_rank")
    df = df.sort_values(sort_cols)

    grouped: dict[int, list[str]] = {}
    for topic, group in df.groupby("topic"):
        tid = int(topic)
        if tid == -1:
            continue
        sentences = [
            str(s).strip()
            for s in group["sentence"].tolist()
            if str(s).strip()
        ]
        grouped[tid] = sentences[:max_per_topic]
    return grouped


def attach_snippet_columns(
    df: pd.DataFrame,
    snippets_by_topic: dict[int, list[str]],
    *,
    snippets_per_topic: int = 6,
) -> pd.DataFrame:
    """Add n_snippets_available and snippet_1..snippet_N columns."""
    out = df.copy()
    n_cols = snippets_per_topic

    def _snippet_list(topic_id: int) -> list[str]:
        return snippets_by_topic.get(int(topic_id), [])

    out["n_snippets_available"] = out["Topic"].apply(
        lambda t: len(snippets_by_topic.get(int(t), []))
    )
    for i in range(1, n_cols + 1):
        col = f"snippet_{i}"
        out[col] = out["Topic"].apply(
            lambda t, idx=i: _snippet_list(int(t))[idx - 1]
            if len(_snippet_list(int(t))) >= idx
            else ""
        )
    return out


def get_representation_stats(
    topic_model: BERTopic,
    *,
    representations: tuple[str, ...],
    top_k: int = 10,
) -> pd.DataFrame:
    """Per-topic stats for each BERTopic representation aspect."""
    all_topics = extract_all_topics(topic_model, top_k=top_k)
    topic_ids = sorted(
        {
            tid
            for rep in representations
            for tid in all_topics.get(rep, {}).keys()
        }
    )

    rows: list[dict[str, Any]] = []
    for topic_id in topic_ids:
        row: dict[str, Any] = {"Topic": topic_id}
        for rep_name in representations:
            word_list = all_topics.get(rep_name, {}).get(topic_id, [])
            words = [str(w.get("word", "")).strip() for w in word_list if w.get("word")]
            n_words = len(words)
            n_unique = len(set(words))
            row[f"{rep_name}_words"] = words
            row[f"{rep_name}_n_words"] = n_words
            row[f"{rep_name}_n_unique_words"] = n_unique
            row[f"{rep_name}_n_content_pos"] = (
                count_content_pos_words(words) if words else 0
            )
            row[f"{rep_name}_diversity_simple"] = (
                n_unique / n_words if n_words else None
            )
        rows.append(row)

    if not rows:
        return pd.DataFrame(columns=["Topic"])
    return pd.DataFrame(rows).sort_values("Topic").reset_index(drop=True)


def compute_coherence_per_representation(
    topic_model: BERTopic,
    docs_tokens: list[list[str]],
    dictionary: Dictionary,
    *,
    representations: tuple[str, ...],
    top_k: int = 10,
) -> pd.DataFrame:
    """Per-topic c_v coherence for each representation aspect."""
    all_topics = extract_all_topics(topic_model, top_k=top_k)
    topic_ids = sorted(
        {
            tid
            for rep in representations
            for tid in all_topics.get(rep, {}).keys()
        }
    )

    out = pd.DataFrame({"Topic": topic_ids})
    for rep_name in representations:
        rep_topics = all_topics.get(rep_name, {})
        coh_topic_ids: list[int] = []
        topics_as_ids: list[list[int]] = []

        for topic_id in topic_ids:
            word_dicts = rep_topics.get(topic_id, [])
            words = [w["word"] for w in word_dicts]
            ids = [dictionary.token2id[w] for w in words if w in dictionary.token2id]
            if len(ids) >= 2:
                coh_topic_ids.append(topic_id)
                topics_as_ids.append(ids)

        col = f"{rep_name}_coherence_c_v"
        if not topics_as_ids:
            out[col] = None
            continue

        with stage_timer(f"Computing per-topic {rep_name} coherence (c_v)"):
            cm = CoherenceModel(
                topics=topics_as_ids,
                texts=docs_tokens,
                dictionary=dictionary,
                coherence="c_v",
            )
            scores = cm.get_coherence_per_topic()

        coh_df = pd.DataFrame({"Topic": coh_topic_ids, col: scores})
        out = out.merge(coh_df, on="Topic", how="left")

    return out.sort_values("Topic").reset_index(drop=True)


def get_topic_distribution(topic_model: BERTopic, min_size: int = 30) -> pd.DataFrame:
    """Topic counts from get_topic_info (excludes topic -1)."""
    info = topic_model.get_topic_info()
    info = info[info["Topic"] != -1].copy()
    info["keep_by_size"] = info["Count"] >= min_size
    return info


def _parse_flags_list(value: Any) -> list[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(x) for x in value if str(x)]
    text = str(value).strip()
    if not text or text == "[]":
        return []
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
    return [p for p in text.replace("|", ";").split(";") if p]


def _all_reps_weak_content_pos(row: pd.Series, reps: tuple[str, ...], min_pos: int) -> bool:
    for rep in reps:
        val = row.get(f"{rep}_n_content_pos")
        if pd.isna(val) or int(val) >= min_pos:
            return False
    return True


def _all_reps_low_coherence(
    row: pd.Series, reps: tuple[str, ...], min_coh: float
) -> bool:
    for rep in reps:
        val = row.get(f"{rep}_coherence_c_v")
        if pd.isna(val):
            continue
        if float(val) >= min_coh:
            return False
    return True


def _all_reps_low_diversity(
    row: pd.Series, reps: tuple[str, ...], min_div: float
) -> bool:
    for rep in reps:
        val = row.get(f"{rep}_diversity_simple")
        if pd.isna(val):
            continue
        if float(val) >= min_div:
            return False
    return True


def _all_reps_empty(row: pd.Series, reps: tuple[str, ...]) -> bool:
    return all(int(row.get(f"{rep}_n_words", 0) or 0) == 0 for rep in reps)


def _all_reps_low_info(
    row: pd.Series,
    reps: tuple[str, ...],
    cfg: Stage07Config,
) -> bool:
    th = cfg.thresholds
    return _all_reps_weak_content_pos(row, reps, th.min_content_pos_per_rep) and (
        _all_reps_low_coherence(row, reps, th.min_coherence_c_v)
        or _all_reps_low_diversity(row, reps, th.min_representation_diversity)
    )


def apply_stage07_routing_flags(
    df: pd.DataFrame,
    cfg: Stage07Config,
) -> pd.DataFrame:
    """Compute stage07_flags, hard/soft candidates, and recommended_next_step."""
    reps = cfg.representations
    th = cfg.thresholds
    out = df.copy()

    out["flag_ultra_tiny_docs"] = out["Count"] < th.ultra_tiny_docs
    out["flag_small_docs"] = out["Count"] < th.small_docs
    out["flag_low_support_docs"] = out["Count"] < th.low_support_docs
    out["flag_empty_all_representations"] = out.apply(
        lambda r: _all_reps_empty(r, reps), axis=1
    )
    out["flag_few_words_all_representations"] = out.apply(
        lambda r: _all_reps_weak_content_pos(r, reps, th.min_content_pos_per_rep),
        axis=1,
    )
    out["flag_low_coherence_all_representations"] = out.apply(
        lambda r: _all_reps_low_coherence(r, reps, th.min_coherence_c_v),
        axis=1,
    )
    out["flag_low_diversity_all_representations"] = out.apply(
        lambda r: _all_reps_low_diversity(r, reps, th.min_representation_diversity),
        axis=1,
    )
    if "n_snippets_available" in out.columns:
        out["flag_missing_or_too_few_snippets"] = (
            out["n_snippets_available"].fillna(0) < th.min_snippets
        )
    else:
        out["flag_missing_or_too_few_snippets"] = False

    posthoc_flags_col = out.get("posthoc_flags")
    if posthoc_flags_col is not None:
        out["flag_publisher_boilerplate"] = posthoc_flags_col.apply(
            lambda f: "publisher_boilerplate" in _parse_flags_list(f)
        )
        out["flag_multilingual_artifact"] = posthoc_flags_col.apply(
            lambda f: "multilingual_artifact" in _parse_flags_list(f)
        )
        out["flag_tiny_topic_posthoc"] = posthoc_flags_col.apply(
            lambda f: "tiny_topic" in _parse_flags_list(f)
        )
    else:
        out["flag_publisher_boilerplate"] = False
        out["flag_multilingual_artifact"] = False
        out["flag_tiny_topic_posthoc"] = False

    out["flag_possible_character_residue"] = False
    if "posthoc_flags" in out.columns:
        out["flag_possible_character_residue"] = out["posthoc_flags"].apply(
            lambda f: "possible_character_residue" in _parse_flags_list(f)
            or "name_contaminated_review" in _parse_flags_list(f)
        )

    def _collect_flags(row: pd.Series) -> list[str]:
        flags: list[str] = []
        mapping = {
            "flag_publisher_boilerplate": "publisher_boilerplate",
            "flag_multilingual_artifact": "multilingual_artifact",
            "flag_empty_all_representations": "empty_all_representations",
            "flag_ultra_tiny_docs": "ultra_tiny_topic",
            "flag_small_docs": "small_topic",
            "flag_few_words_all_representations": "few_words_all_representations",
            "flag_low_coherence_all_representations": "low_coherence_all_representations",
            "flag_low_diversity_all_representations": "low_diversity_all_representations",
            "flag_possible_character_residue": "possible_character_residue",
            "flag_missing_or_too_few_snippets": "missing_or_too_few_snippets",
        }
        for col, name in mapping.items():
            if bool(row.get(col)):
                flags.append(name)
        if bool(row.get("flag_tiny_topic_posthoc")) and "small_topic" not in flags:
            flags.append("tiny_topic")
        return flags

    out["stage07_flags"] = out.apply(_collect_flags, axis=1)
    out["stage07_reason"] = out["stage07_flags"].apply(
        lambda flags: ";".join(flags) if flags else ""
    )

    def _hard_exclude(row: pd.Series) -> bool:
        if bool(row.get("hard_exclude_candidate_posthoc")):
            return True
        flags = row.get("stage07_flags") or []
        hard_hits = set(flags) & set(cfg.hard_exclude_rules)
        if hard_hits:
            return True
        if bool(row.get("flag_ultra_tiny_docs")) and bool(
            row.get("flag_missing_or_too_few_snippets")
        ):
            return True
        return False

    def _soft_review(row: pd.Series) -> bool:
        if bool(row.get("soft_review_candidate_posthoc")):
            return True
        if bool(row.get("hard_exclude_candidate")):
            return False
        flags = row.get("stage07_flags") or []
        soft_hits = set(flags) & set(cfg.soft_review_rules)
        return bool(soft_hits)

    if "hard_exclude_candidate_posthoc" not in out.columns:
        out["hard_exclude_candidate_posthoc"] = False
    if "soft_review_candidate_posthoc" not in out.columns:
        out["soft_review_candidate_posthoc"] = False

    out["hard_exclude_candidate"] = out.apply(_hard_exclude, axis=1)
    out["soft_review_candidate"] = out.apply(_soft_review, axis=1)

    def _next_step(row: pd.Series) -> str:
        if bool(row.get("hard_exclude_candidate")):
            return "exclude_before_llm"
        if bool(row.get("soft_review_candidate")):
            return "stage08_quality_adjudication"
        return "stage08_labeling"

    out["recommended_next_step"] = out.apply(_next_step, axis=1)

    # Legacy aliases
    out["exclude_from_axes"] = out["hard_exclude_candidate"]
    out["noise_candidate"] = out["hard_exclude_candidate"] | out["soft_review_candidate"]
    out["noise_reason"] = out["stage07_reason"]

    # Legacy POS columns for downstream notebooks
    if "POS_n_words" in out.columns:
        out["n_pos_words"] = out["POS_n_words"]
    if "POS_words" in out.columns:
        out["pos_words"] = out["POS_words"]
    if "POS_coherence_c_v" in out.columns:
        out["coherence_c_v_pos"] = out["POS_coherence_c_v"]
    out["flag_small"] = out["flag_small_docs"]
    out["flag_few_pos"] = out["flag_few_words_all_representations"]
    out["flag_low_coh"] = out["flag_low_coherence_all_representations"]

    def _inspection_label(row: pd.Series) -> str:
        base_name = str(row.get("Name", "") or "").strip()
        if bool(row.get("hard_exclude_candidate")):
            flags = row.get("stage07_flags") or []
            tag = flags[0] if flags else "hard_exclude"
            return f"[HARD_EXCLUDE:{tag}] {base_name}"
        if bool(row.get("soft_review_candidate")):
            flags = row.get("stage07_flags") or []
            tag = flags[0] if flags else "soft_review"
            return f"[SOFT_REVIEW:{tag}] {base_name}"
        return base_name

    out["inspection_label"] = out.apply(_inspection_label, axis=1)
    return out


def merge_name_cleaning_flags(
    quality_df: pd.DataFrame,
    ratio_csv: Path,
) -> pd.DataFrame:
    """Merge character-name cleaning flags into quality table (soft review only)."""
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
        "posthoc_flags",
        "posthoc_reason",
        "name_cleaned",
        "suggested_action",
    ]
    merge_cols = [c for c in merge_cols if c in ratio_df.columns]
    name_subset = ratio_df[merge_cols].copy()
    name_subset = name_subset[name_subset["Topic"] != -1]

    merged = quality_df.merge(name_subset, on="Topic", how="left", suffixes=("_old", ""))

    for col in ("posthoc_flags", "posthoc_reason", "suggested_action"):
        old_col = f"{col}_old"
        if old_col in merged.columns:
            if col == "posthoc_flags":
                def _combine_flags(row: pd.Series) -> list:
                    old = _parse_flags_list(row.get(old_col))
                    new = _parse_flags_list(row.get(col))
                    combined: list[str] = []
                    for f in old + new:
                        if f and f not in combined:
                            combined.append(f)
                    return combined

                merged[col] = merged.apply(_combine_flags, axis=1)
            elif col == "posthoc_reason":
                merged[col] = merged.apply(
                    lambda r: ";".join(
                        p
                        for p in (
                            str(r.get(f"{col}_old", "") or ""),
                            str(r.get(col, "") or ""),
                        )
                        if p
                    ),
                    axis=1,
                )
            else:
                merged[col] = merged[col].fillna(merged[old_col])
            merged.drop(columns=[old_col], inplace=True)

    if "name_cleaned" in merged.columns:
        merged["name_cleaned"] = merged["name_cleaned"].fillna(False)
    if "character_name_ratio" in merged.columns:
        merged["character_name_ratio"] = merged["character_name_ratio"].fillna(0.0)

    logger.info("[NAME_CLEANING] merged character-name flags into quality table")
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
        "posthoc_flags",
        "posthoc_reason",
        "exclude_from_axes",
        "hard_exclude_candidate",
        "soft_review_candidate",
        "suggested_action",
    ]
    posthoc_cols = [c for c in posthoc_cols if c in classified.columns]
    posthoc_subset = classified[posthoc_cols].copy()
    posthoc_subset = posthoc_subset[posthoc_subset["Topic"] != -1]
    posthoc_subset = posthoc_subset.rename(
        columns={
            "hard_exclude_candidate": "hard_exclude_candidate_posthoc",
            "soft_review_candidate": "soft_review_candidate_posthoc",
        }
    )

    merged = quality_df.merge(posthoc_subset, on="Topic", how="left")
    merged["posthoc_reason"] = merged["posthoc_reason"].fillna("")
    merged["posthoc_flags"] = merged["posthoc_flags"].apply(
        lambda x: _parse_flags_list(x) if not isinstance(x, list) else x
    )
    merged["hard_exclude_candidate_posthoc"] = merged[
        "hard_exclude_candidate_posthoc"
    ].fillna(False)
    merged["soft_review_candidate_posthoc"] = merged[
        "soft_review_candidate_posthoc"
    ].fillna(False)
    n_hard = int(merged["hard_exclude_candidate_posthoc"].sum())
    logger.info("[POSTHOC] merged into quality table: %d hard-exclude topics", n_hard)
    return merged


def build_topic_quality_table(
    topic_model: BERTopic,
    docs_tokens: list[list[str]],
    dictionary: Dictionary,
    *,
    stage07_config: Stage07Config | None = None,
    stage07_config_path: Path | None = None,
    topic_info_path: Path | None = None,
    rules_config: Path | None = None,
    name_cleaning_csv: Path | None = None,
    representative_docs_csv: Path | None = None,
    # Legacy CLI overrides
    min_size: int | None = None,
    min_pos_words: int | None = None,
    min_pos_coherence: float | None = None,
    top_k: int | None = None,
) -> pd.DataFrame:
    """Build enriched Stage 07 audit table with multi-representation metrics."""
    cfg = stage07_config or load_stage07_config(stage07_config_path)
    if min_size is not None:
        cfg.thresholds.small_docs = min_size
    if min_pos_words is not None:
        cfg.thresholds.min_content_pos_per_rep = min_pos_words
    if min_pos_coherence is not None:
        cfg.thresholds.min_coherence_c_v = min_pos_coherence
    if top_k is not None:
        cfg.top_k = top_k

    reps = cfg.representations
    th = cfg.thresholds

    with stage_timer("Building topic quality table"):
        topic_info = get_topic_distribution(topic_model, min_size=th.small_docs)
        rep_stats = get_representation_stats(
            topic_model, representations=reps, top_k=cfg.top_k
        )
        rep_coh = compute_coherence_per_representation(
            topic_model,
            docs_tokens=docs_tokens,
            dictionary=dictionary,
            representations=reps,
            top_k=cfg.top_k,
        )

        df = topic_info[["Topic", "Count", "Name", "Representation"]].merge(
            rep_stats, on="Topic", how="left"
        )
        df = df.merge(rep_coh, on="Topic", how="left")

        if representative_docs_csv is not None:
            snippets = load_topic_snippets(
                representative_docs_csv,
                max_per_topic=cfg.snippets_per_topic,
            )
            df = attach_snippet_columns(
                df, snippets, snippets_per_topic=cfg.snippets_per_topic
            )

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

        df = apply_stage07_routing_flags(df, cfg)

        sort_col = "POS_coherence_c_v" if "POS_coherence_c_v" in df.columns else "Count"
        df.sort_values(
            ["hard_exclude_candidate", "soft_review_candidate", sort_col, "Count"],
            ascending=[False, False, True, True],
            inplace=True,
        )
        df.reset_index(drop=True, inplace=True)

    return df


# Backward-compatible wrappers for legacy imports


def get_pos_representation_stats(
    topic_model: BERTopic, top_k: int = 10
) -> pd.DataFrame:
    """Legacy: POS-only representation stats."""
    df = get_representation_stats(
        topic_model, representations=("POS",), top_k=top_k
    )
    if df.empty:
        return pd.DataFrame(columns=["Topic", "n_pos_words", "pos_words"])
    out = pd.DataFrame(
        {
            "Topic": df["Topic"],
            "n_pos_words": df["POS_n_words"],
            "pos_words": df["POS_words"],
        }
    )
    return out


def compute_pos_coherence_per_topic(
    topic_model: BERTopic,
    docs_tokens: list[list[str]],
    dictionary: Dictionary,
    top_k: int = 10,
) -> pd.DataFrame:
    """Legacy: POS-only per-topic coherence."""
    df = compute_coherence_per_representation(
        topic_model,
        docs_tokens,
        dictionary,
        representations=("POS",),
        top_k=top_k,
    )
    if df.empty:
        return pd.DataFrame(columns=["Topic", "coherence_c_v_pos"])
    return df.rename(columns={"POS_coherence_c_v": "coherence_c_v_pos"})[
        ["Topic", "coherence_c_v_pos"]
    ]


def apply_noise_labels_to_model(
    topic_model: BERTopic,
    quality_df: pd.DataFrame,
    only_noise_candidates: bool = True,
) -> dict[int, str]:
    """Build a label dictionary for topics based on quality analysis."""
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
