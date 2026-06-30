"""Orchestrate character-name cleaning pipeline and write audit artifacts."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

from src.common.character_name_cleaning.lexicon import CleaningLexicon, load_lexicon
from src.common.character_name_cleaning.ner_pass import get_spacy_nlp
from src.common.character_name_cleaning.seed_pass import (
    character_name_ratio,
    classify_topic_by_ratio,
    clean_snippet_text,
    clean_topic_words,
    replace_seed_names_in_snippet,
)

LOGGER = logging.getLogger("character_name_cleaning.pipeline")

REPRESENTATIONS = ("Main", "KeyBERT", "POS", "MMR")


def _extend_lexicon_from_topics(
    lexicon: CleaningLexicon,
    topics: dict[str, dict[str, list[dict[str, Any]]]],
) -> CleaningLexicon:
    """Add topic words that co-occur with seed hits in the same topic."""
    if not lexicon.extend_lexicon_from_topics:
        return lexicon

    derived: set[str] = set()
    for aspect in ("POS", "Main"):
        aspect_topics = topics.get(aspect, {})
        for word_list in aspect_topics.values():
            words_lower = [
                str(w.get("word", "")).lower().strip()
                for w in word_list
                if str(w.get("word", "")).strip()
            ]
            if not any(w in lexicon.high_confidence_names for w in words_lower):
                continue
            for w in words_lower:
                if (
                    len(w) >= 4
                    and w not in lexicon.keep_role_tokens
                    and w not in lexicon.ambiguous_review
                    and w not in lexicon.high_confidence_names
                ):
                    derived.add(w)

    if not derived:
        return lexicon

    lexicon.topic_derived_names = frozenset(derived)
    LOGGER.info("Extended lexicon with %d topic-derived names", len(derived))
    return lexicon


def load_topics_json(path: Path) -> dict[str, dict[str, list[dict[str, Any]]]]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return {
        aspect: {str(tid): words for tid, words in topics.items()}
        for aspect, topics in raw.items()
    }


def load_representative_docs_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def run_cleaning_pipeline(
    *,
    topics_json: Path,
    representative_docs_csv: Path,
    out_dir: Path,
    config_path: Path | None = None,
    run_ner: bool = True,
) -> dict[str, Path]:
    """Run full cleaning pipeline; return paths to written artifacts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    lexicon = load_lexicon(config_path)
    topics = load_topics_json(topics_json)
    lexicon = _extend_lexicon_from_topics(lexicon, topics)

    nlp = get_spacy_nlp() if run_ner else None

    cleaned_topics: dict[str, dict[str, list[dict[str, Any]]]] = {}
    removed_audit: list[dict[str, str]] = []
    ambiguous_review: list[dict[str, str]] = []
    ratio_rows: list[dict[str, Any]] = []
    topic_flags: dict[str, dict[str, Any]] = {}

    for aspect in REPRESENTATIONS:
        cleaned_topics[aspect] = {}
        for topic_id, word_list in topics.get(aspect, {}).items():
            original = [dict(w) for w in word_list]
            cleaned, removed, reviews = clean_topic_words(original, lexicon)
            cleaned_topics[aspect][topic_id] = cleaned
            for w in removed:
                removed_audit.append(
                    {
                        "topic_id": topic_id,
                        "representation": aspect,
                        "word": w,
                        "reason": "seed_name",
                    }
                )
            for rev in reviews:
                ambiguous_review.append(
                    {
                        "topic_id": topic_id,
                        "representation": aspect,
                        "word": rev["word"],
                        "reason": rev["reason"],
                    }
                )

    pos_topics = topics.get("POS", {})
    main_topics = topics.get("Main", {})
    for topic_id in sorted(
        set(pos_topics.keys()) | set(main_topics.keys()),
        key=lambda x: int(x) if str(x).lstrip("-").isdigit() else x,
    ):
        pos_original = pos_topics.get(topic_id, [])
        main_original = main_topics.get(topic_id, [])
        ratio_pos = character_name_ratio(pos_original, lexicon, original_words=pos_original)
        ratio_main = character_name_ratio(main_original, lexicon, original_words=main_original)
        ratio = max(ratio_pos, ratio_main)
        names_removed = sum(
            1
            for row in removed_audit
            if row["topic_id"] == topic_id and row["representation"] == "POS"
        )
        flags = classify_topic_by_ratio(ratio, lexicon, names_removed=names_removed)
        flags["Topic"] = int(topic_id)
        flags["character_name_ratio_pos"] = ratio_pos
        flags["character_name_ratio_main"] = ratio_main
        flags["posthoc_flags"] = "|".join(flags.get("posthoc_flags", []))
        ratio_rows.append(flags)
        topic_flags[topic_id] = flags

    rep_df = load_representative_docs_csv(representative_docs_csv)
    title_audit: list[dict[str, str]] = []
    cleaned_rows: list[dict[str, Any]] = []

    for _, row in rep_df.iterrows():
        original = str(row.get("sentence", "") or "")
        before_seed = replace_seed_names_in_snippet(original, lexicon)
        cleaned = clean_snippet_text(
            original, lexicon, nlp=nlp, run_ner=run_ner and nlp is not None
        )
        if before_seed != original or (
            cleaned != before_seed and lexicon.person_placeholder in cleaned
        ):
            title_audit.append(
                {
                    "topic": str(row.get("topic", "")),
                    "doc_rank": str(row.get("doc_rank", "")),
                    "before": original[:500],
                    "after": cleaned[:500],
                }
            )
        cleaned_rows.append(
            {
                "topic": row["topic"],
                "doc_rank": row["doc_rank"],
                "sentence": cleaned,
            }
        )

    seed_lexicon_path = out_dir / "character_name_seed_lexicon.json"
    with open(seed_lexicon_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "keep_role_tokens": sorted(lexicon.keep_role_tokens),
                "high_confidence_names": sorted(lexicon.high_confidence_names),
                "topic_derived_names": sorted(lexicon.topic_derived_names),
                "auto_replace_names": sorted(lexicon.auto_replace_names),
                "ambiguous_review": sorted(lexicon.ambiguous_review),
                "surname_review": sorted(lexicon.surname_review),
            },
            f,
            indent=2,
        )

    cleaned_topics_path = out_dir / "cleaned_topics_all_representations.json"
    with open(cleaned_topics_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_topics, f, indent=2)

    cleaned_csv_path = out_dir / "cleaned_representative_docs.csv"
    pd.DataFrame(cleaned_rows).to_csv(cleaned_csv_path, index=False)

    _write_csv(out_dir / "ambiguous_name_review.csv", ambiguous_review)
    _write_csv(out_dir / "removed_topic_words_audit.csv", removed_audit)
    _write_csv(out_dir / "title_preservation_audit.csv", title_audit)

    ratio_df = pd.DataFrame(ratio_rows)
    ratio_path = out_dir / "character_name_ratio_by_topic.csv"
    ratio_df.to_csv(ratio_path, index=False)

    flags_path = out_dir / "topic_name_flags.json"
    with open(flags_path, "w", encoding="utf-8") as f:
        json.dump(topic_flags, f, indent=2)

    LOGGER.info("Wrote cleaned artifacts to %s", out_dir)
    return {
        "seed_lexicon": seed_lexicon_path,
        "cleaned_topics": cleaned_topics_path,
        "cleaned_snippets": cleaned_csv_path,
        "ratio_csv": ratio_path,
        "topic_flags": flags_path,
    }


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
