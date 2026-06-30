"""Orchestrate NER-based character-name cleaning and write audit artifacts."""

from __future__ import annotations

import csv
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

from src.common.character_name_cleaning.lexicon import CleaningLexicon, load_lexicon
from src.common.character_name_cleaning.ner_pass import (
    build_topic_person_lexicon,
    clean_snippet_text,
    extract_person_tokens_from_snippets,
    extract_person_tokens_from_topic_words,
    get_spacy_nlp,
)
from src.common.character_name_cleaning.seed_pass import (
    character_name_ratio,
    classify_topic_by_ratio,
    clean_topic_words,
)

LOGGER = logging.getLogger("character_name_cleaning.pipeline")

REPRESENTATIONS = ("Main", "KeyBERT", "POS", "MMR")


def load_topics_json(path: Path) -> dict[str, dict[str, list[dict[str, Any]]]]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return {
        aspect: {str(tid): words for tid, words in topics.items()}
        for aspect, topics in raw.items()
    }


def load_topic_snippets(csv_path: Path) -> dict[str, list[str]]:
    df = pd.read_csv(csv_path)
    grouped: dict[str, list[str]] = defaultdict(list)
    for _, row in df.iterrows():
        topic = str(row.get("topic", ""))
        sentence = str(row.get("sentence", "") or "").strip()
        if topic and sentence:
            grouped[topic].append(sentence)
    return dict(grouped)


def run_cleaning_pipeline(
    *,
    topics_json: Path,
    representative_docs_csv: Path,
    out_dir: Path,
    config_path: Path | None = None,
    run_ner: bool = True,
) -> dict[str, Path]:
    """Run full NER cleaning pipeline; return paths to written artifacts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    lexicon = load_lexicon(config_path)
    topics = load_topics_json(topics_json)
    nlp = get_spacy_nlp() if run_ner else None
    if nlp is None:
        raise RuntimeError(
            "spaCy en_core_web_sm with NER is required for character name cleaning"
        )

    topic_snippets = load_topic_snippets(representative_docs_csv)
    topic_person_lexicon = build_topic_person_lexicon(topic_snippets, nlp, lexicon)
    global_person_tokens = extract_person_tokens_from_snippets(
        (s for snippets in topic_snippets.values() for s in snippets),
        nlp,
        lexicon,
    )

    cleaned_topics: dict[str, dict[str, list[dict[str, Any]]]] = {}
    removed_audit: list[dict[str, str]] = []
    ner_word_audit: list[dict[str, str]] = []
    ratio_rows: list[dict[str, Any]] = []
    topic_flags: dict[str, dict[str, Any]] = {}

    for aspect in REPRESENTATIONS:
        cleaned_topics[aspect] = {}
        for topic_id, word_list in topics.get(aspect, {}).items():
            snippet_persons = topic_person_lexicon.get(topic_id, set())
            keyword_persons = extract_person_tokens_from_topic_words(
                word_list,
                nlp,
                lexicon,
                snippet_persons=snippet_persons,
            )
            person_tokens = snippet_persons | keyword_persons
            original = [dict(w) for w in word_list]
            cleaned, removed, audits = clean_topic_words(
                original,
                lexicon,
                topic_person_tokens=person_tokens,
                nlp=nlp,
            )
            cleaned_topics[aspect][topic_id] = cleaned
            for w in removed:
                removed_audit.append(
                    {
                        "topic_id": topic_id,
                        "representation": aspect,
                        "word": w,
                        "reason": "ner_person",
                    }
                )
            for row in audits:
                ner_word_audit.append(
                    {
                        "topic_id": topic_id,
                        "representation": aspect,
                        "word": row["word"],
                        "reason": row["reason"],
                    }
                )

    pos_topics = topics.get("POS", {})
    main_topics = topics.get("Main", {})
    for topic_id in sorted(
        set(pos_topics.keys()) | set(main_topics.keys()),
        key=lambda x: int(x) if str(x).lstrip("-").isdigit() else x,
    ):
        snippet_persons = topic_person_lexicon.get(topic_id, set())
        main_original = main_topics.get(topic_id, [])
        keyword_persons = extract_person_tokens_from_topic_words(
            main_original,
            nlp,
            lexicon,
            snippet_persons=snippet_persons,
        )
        person_tokens = snippet_persons | keyword_persons
        pos_original = pos_topics.get(topic_id, [])
        ratio_pos = character_name_ratio(
            pos_original,
            lexicon,
            topic_person_tokens=person_tokens,
            nlp=nlp,
            original_words=pos_original,
        )
        ratio_main = character_name_ratio(
            main_original,
            lexicon,
            topic_person_tokens=person_tokens,
            nlp=nlp,
            original_words=main_original,
        )
        ratio = max(ratio_pos, ratio_main)
        names_removed = sum(
            1
            for row in removed_audit
            if row["topic_id"] == topic_id and row["representation"] == "Main"
        )
        flags = classify_topic_by_ratio(ratio, lexicon, names_removed=names_removed)
        flags["Topic"] = int(topic_id)
        flags["character_name_ratio_pos"] = ratio_pos
        flags["character_name_ratio_main"] = ratio_main
        flags["posthoc_flags"] = "|".join(flags.get("posthoc_flags", []))
        flags["ner_person_tokens"] = "|".join(sorted(person_tokens))
        ratio_rows.append(flags)
        topic_flags[topic_id] = flags

    rep_df = pd.read_csv(representative_docs_csv)
    title_audit: list[dict[str, str]] = []
    cleaned_rows: list[dict[str, Any]] = []

    for _, row in rep_df.iterrows():
        original = str(row.get("sentence", "") or "")
        cleaned = clean_snippet_text(original, lexicon, nlp=nlp)
        if cleaned != original:
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
                "global_person_tokens_ner": sorted(global_person_tokens),
                "topic_person_lexicon": {
                    k: sorted(v) for k, v in sorted(topic_person_lexicon.items())
                },
            },
            f,
            indent=2,
        )

    cleaned_topics_path = out_dir / "cleaned_topics_all_representations.json"
    with open(cleaned_topics_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_topics, f, indent=2)

    cleaned_csv_path = out_dir / "cleaned_representative_docs.csv"
    pd.DataFrame(cleaned_rows).to_csv(cleaned_csv_path, index=False)

    _write_csv(out_dir / "ner_topic_word_audit.csv", ner_word_audit)
    _write_csv(out_dir / "removed_topic_words_audit.csv", removed_audit)
    _write_csv(out_dir / "title_preservation_audit.csv", title_audit)

    ratio_df = pd.DataFrame(ratio_rows)
    ratio_path = out_dir / "character_name_ratio_by_topic.csv"
    ratio_df.to_csv(ratio_path, index=False)

    flags_path = out_dir / "topic_name_flags.json"
    with open(flags_path, "w", encoding="utf-8") as f:
        json.dump(topic_flags, f, indent=2)

    LOGGER.info(
        "Wrote cleaned artifacts to %s (%d global NER person tokens)",
        out_dir,
        len(global_person_tokens),
    )
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
