"""Validation script to flag potential hallucination patterns in topic labels and summaries.

This script checks for common hallucination patterns identified in manual review:
- "Invitations" without explicit invitation keywords/snippets
- "Acting out of character" without explicit evidence in snippets
- "Past relationships" without relationship keywords/snippets
- Generic romance tropes ("struggles with feelings")
- Life-changing stakes without evidence
- Truncated summaries

The script checks both keywords AND snippets (representative documents) to validate labels,
since the labeling process uses snippets as primary evidence.

Usage:
    python -m src.stage08_llm_labeling.openrouter_experiments.tools.validate_label_quality \
        --labels-json results/stage08_llm_labeling/labels_pos_openrouter_mistralai_mistral-nemo_romance_aware_paraphrase-MiniLM-L6-v2.json \
        --bertopic-model-path models/retrained/paraphrase-MiniLM-L6-v2/model_1_with_noise_labels.pkl \
        --output-csv results/stage08_llm_labeling/validation_report.csv
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from src.common.config import load_config
from src.stage08_llm_labeling.generate_labels import load_bertopic_model
from src.stage06_topic_exploration.explore_retrained_model import (
    DEFAULT_BASE_DIR,
    DEFAULT_EMBEDDING_MODEL,
)
from src.stage08_llm_labeling.lexicon import (
    explicit_sexual_terms,
    forbidden_genre_cliche_phrases,
)
from src.stage08_llm_labeling.openrouter_experiments.core.generate_labels_openrouter import (
    extract_representative_docs_per_topic,
)


# Hallucination pattern definitions
INVITATION_KEYWORDS = {"invite", "invited", "invitation", "yes", "no", "refused", "proposal", "asked", "asking"}
INVITATION_PATTERNS = [
    (r"\binvit(e|ed|ing|ation)\b", "Uses 'invite/invitation' without invitation keywords"),
    (r"\bpropos(e|ed|al)\b", "Uses 'propose/proposal' without proposal keywords"),
]

OUT_OF_CHARACTER_PATTERNS = [
    (r"\bact(ing|s)?\s+out\s+of\s+character\b", "Uses 'acting out of character' without explicit evidence"),
    (r"\bunusual(ly)?\s+behavior\b", "Uses 'unusual behavior' without explicit evidence"),
    (r"\bstrange(ly)?\s+act(ing|s)?\b", "Uses 'strange/strangely' without explicit evidence"),
]

PAST_RELATIONSHIPS_PATTERNS = [
    (r"\bpast\s+relationship(s)?\b", "Uses 'past relationships' without relationship keywords"),
    (r"\bprevious\s+relationship(s)?\b", "Uses 'previous relationships' without relationship keywords"),
    (r"\bher\s+past\b", "Uses 'her past' (likely referring to relationships) without evidence"),
]

ROMANCE_TROPES_PATTERNS = [
    (r"\bstruggles?\s+with\s+(her|his|their)\s+feelings?\b", "Generic romance trope: 'struggles with feelings'"),
    (r"\bhearts?\s+(are|is)\s+torn\b", "Generic romance trope: 'hearts are torn'"),
    (r"\bemotionally\s+torn\b", "Generic romance trope: 'emotionally torn'"),
]

LIFE_CHANGING_PATTERNS = [
    (r"\blife[- ]?changing\b", "Uses 'life-changing' without clear evidence"),
    (r"\bcould\s+change\s+their\s+situation\b", "Uses 'could change their situation' without evidence"),
    (r"\btheir\s+whole\s+life\s+changes?\b", "Uses 'their whole life changes' without evidence"),
]

TRUNCATION_INDICATORS = [
    "to", "for", "a", "the", "an", "in", "on", "at", "with", "by", "from",
    "this", "that", "these", "those", "it", "they", "she", "he", "we",
]

GENRE_CLICHE_PATTERNS = [
    (phrase, f"Genre cliché label phrase: {phrase!r}")
    for phrase in forbidden_genre_cliche_phrases()
]


def _label_token_overlap(actual: str, expected: str) -> float:
    a = {w.lower() for w in re.findall(r"[a-zA-Z]+", actual)}
    b = {w.lower() for w in re.findall(r"[a-zA-Z]+", expected)}
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def check_genre_cliche_labels(label: str) -> list[str]:
    issues = []
    label_lower = label.lower()
    for phrase, message in GENRE_CLICHE_PATTERNS:
        if phrase in label_lower:
            issues.append(message)
    return issues


def check_v3_explicitness_keywords(
    entry: dict[str, Any], keywords: list[str]
) -> list[str]:
    """Soft advisory checks for v3 sexual fields (warnings only in gold compare)."""
    issues = []
    kw_lower = {k.lower() for k in keywords}
    explicitness = str(entry.get("sexual_explicitness", "none"))
    if explicit_sexual_terms().intersection(kw_lower) and explicitness in ("none", "affection_only"):
        issues.append(
            f"sexual_explicitness={explicitness} but explicit sexual keywords present"
        )
    return issues


def compare_against_gold_yaml(
    labels_data: dict[str, Any],
    gold_path: Path,
    categorization_path: Path | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    gold = load_config(gold_path)
    gold_topics = dict(gold.get("topics", {}))
    criteria = dict(gold.get("pass_criteria", {}))
    manual_review = set(gold.get("manual_review_topics", []))

    if categorization_path is not None:
        cat = load_config(categorization_path)
        criteria.update(cat.get("pass_criteria", {}))
        manual_review |= set(cat.get("manual_review_topics", []))
        for tid_str, cat_expected in cat.get("topics", {}).items():
            merged = dict(gold_topics.get(tid_str, {}))
            merged.update(cat_expected)
            gold_topics[tid_str] = merged

    label_overlap_min = criteria.get("label_overlap_min", 0.35)
    label_agreement_min = criteria.get("label_agreement_min")

    rows = []
    fn_match = 0
    routing_match = 0
    routing_n = 0
    label_pass = 0
    n = 0

    for tid_str, expected in gold_topics.items():
        tid = int(tid_str)
        entry = labels_data.get(tid_str) or labels_data.get(tid)
        if not entry:
            rows.append({
                "topic_id": tid,
                "status": "missing",
                "has_issues": True,
                "issues": "topic not in labels JSON",
            })
            continue
        n += 1
        issues: list[str] = []
        exp_fn = expected.get("sexual_function")
        act_fn = entry.get("sexual_function")
        if exp_fn and act_fn == exp_fn:
            fn_match += 1
        elif exp_fn:
            issues.append(f"sexual_function: expected {exp_fn}, got {act_fn}")
        exp_consent = expected.get("consent_status")
        if exp_consent and entry.get("consent_status") != exp_consent:
            issues.append(
                f"consent_status: expected {exp_consent}, got {entry.get('consent_status')}"
            )
        routing_fields = ("content_type", "is_noise", "exclude_from_axes")
        if any(f in expected for f in routing_fields):
            routing_n += 1
            routing_ok = True
            for field in routing_fields:
                if field not in expected:
                    continue
                if entry.get(field) != expected[field]:
                    routing_ok = False
                    issues.append(
                        f"{field}: expected {expected[field]!r}, got {entry.get(field)!r}"
                    )
            if routing_ok:
                routing_match += 1
        exp_label = expected.get("gold_label") or expected.get("label", "")
        act_label = entry.get("label", "")
        overlap = _label_token_overlap(act_label, exp_label) if exp_label else 1.0
        if exp_label and overlap < label_overlap_min:
            issues.append(f"label overlap {overlap:.2f} vs gold {exp_label!r}")
        elif exp_label:
            label_pass += 1
        exp_summary = expected.get("gold_scene_summary", "")
        act_summary = entry.get("scene_summary", "")
        summary_overlap = (
            _label_token_overlap(act_summary, exp_summary) if exp_summary else None
        )
        issues.extend(check_genre_cliche_labels(act_label))
        issues.extend(check_v3_explicitness_keywords(entry, entry.get("keywords", [])))
        if tid in manual_review:
            issues.append("MANUAL_REVIEW: snippet-dependent topic")

        rows.append({
            "topic_id": tid,
            "label": act_label,
            "expected_label": exp_label,
            "label_overlap": overlap,
            "scene_summary": act_summary,
            "expected_scene_summary": exp_summary,
            "scene_summary_overlap": summary_overlap,
            "sexual_function": act_fn,
            "expected_sexual_function": exp_fn,
            "num_issues": len(issues),
            "issues": "; ".join(issues),
            "has_issues": len(issues) > 0,
        })

    fn_rate = fn_match / n if n else 0.0
    routing_rate = routing_match / routing_n if routing_n else 1.0
    label_rate = label_pass / n if n else 0.0
    cliche_count = sum(
        1 for r in rows if "Genre cliché" in str(r.get("issues", ""))
    )
    pass_label = (
        label_rate >= label_agreement_min
        if label_agreement_min is not None
        else True
    )
    has_cat_criteria = any(
        expected.get("sexual_function")
        for expected in gold_topics.values()
    )
    pass_fn = (
        fn_rate >= criteria.get("sexual_function_agreement_min", 0.85)
        if has_cat_criteria
        else True
    )
    pass_routing = (
        routing_rate >= criteria.get("routing_agreement_min", 1.0)
        if routing_n
        else True
    )
    summary = {
        "topics_compared": n,
        "label_agreement": label_rate,
        "sexual_function_agreement": fn_rate,
        "routing_agreement": routing_rate,
        "genre_cliche_count": cliche_count,
        "pass_label": pass_label,
        "pass_fn": pass_fn,
        "pass_routing": pass_routing,
        "pass_cliches": cliche_count == 0 if criteria.get("zero_genre_cliches") else True,
        "overall_pass": (
            pass_label
            and pass_fn
            and pass_routing
            and (cliche_count == 0 if criteria.get("zero_genre_cliches") else True)
        ),
    }
    return pd.DataFrame(rows), summary


def check_invitation_hallucination(
    label: str, summary: str, keywords: list[str], snippets: list[str] | None = None
) -> list[str]:
    """Check if label/summary uses invitation language without invitation keywords/snippets."""
    issues = []
    
    # Check if invitation keywords are present
    keywords_lower = {kw.lower() for kw in keywords}
    has_invitation_keywords = bool(keywords_lower & INVITATION_KEYWORDS)
    
    # Check if invitation language appears in snippets
    has_invitation_in_snippets = False
    if snippets:
        snippets_text = " ".join(snippets).lower()
        # Check for explicit invitation keywords
        for keyword in INVITATION_KEYWORDS:
            if keyword in snippets_text:
                has_invitation_in_snippets = True
                break
        # Check for invitation patterns in snippets
        for pattern, _ in INVITATION_PATTERNS:
            if re.search(pattern, snippets_text, re.IGNORECASE):
                has_invitation_in_snippets = True
                break
        # Check for invitation-like phrases (e.g., "have dinner with me", "come to dinner")
        invitation_phrases = [
            r"have\s+(dinner|lunch|breakfast|drinks?)\s+with",
            r"come\s+(to|for)\s+(dinner|lunch|breakfast)",
            r"(let'?s|we should)\s+(go|have)\s+(to|for)?\s*(dinner|lunch|breakfast)",
            r"(want|wants|wanted)\s+(to\s+)?(have|go)\s+(to|for)?\s*(dinner|lunch|breakfast)",
        ]
        for pattern in invitation_phrases:
            if re.search(pattern, snippets_text, re.IGNORECASE):
                has_invitation_in_snippets = True
                break
    
    # Check for invitation patterns in label and summary
    text = f"{label} {summary}".lower()
    
    for pattern, message in INVITATION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            if not has_invitation_keywords and not has_invitation_in_snippets:
                issues.append(message)
    
    return issues


def check_out_of_character_hallucination(
    summary: str, snippets: list[str] | None = None
) -> list[str]:
    """Check if summary uses 'out of character' language without evidence in snippets."""
    issues = []
    
    # Check if snippets contain evidence of unusual behavior
    has_evidence_in_snippets = False
    if snippets:
        snippets_text = " ".join(snippets).lower()
        # Look for phrases that indicate unusual behavior
        evidence_patterns = [
            r"never\s+(seen|done|been)",
            r"unusual(ly)?",
            r"strange(ly)?",
            r"different\s+from",
            r"out\s+of\s+character",
            r"not\s+like\s+(him|her|them)",
        ]
        for pattern in evidence_patterns:
            if re.search(pattern, snippets_text, re.IGNORECASE):
                has_evidence_in_snippets = True
                break
    
    for pattern, message in OUT_OF_CHARACTER_PATTERNS:
        if re.search(pattern, summary, re.IGNORECASE):
            if not has_evidence_in_snippets:
                issues.append(message)
    
    return issues


def check_past_relationships_hallucination(
    summary: str, keywords: list[str], snippets: list[str] | None = None
) -> list[str]:
    """Check if summary mentions past relationships without relationship keywords/snippets."""
    issues = []
    
    # Check if relationship keywords are present
    relationship_keywords = {"relationship", "relationships", "together", "couple", "dating", "married"}
    keywords_lower = {kw.lower() for kw in keywords}
    has_relationship_keywords = bool(keywords_lower & relationship_keywords)
    
    # Check if snippets contain evidence of past relationships
    has_evidence_in_snippets = False
    if snippets:
        snippets_text = " ".join(snippets).lower()
        # Look for phrases that indicate past relationships
        evidence_patterns = [
            r"ex[- ]?(boyfriend|girlfriend|husband|wife|fianc[éeé]|partner)",
            r"past\s+relationship",
            r"previous\s+relationship",
            r"old\s+(boyfriend|girlfriend|flame)",
            r"used\s+to\s+(date|be\s+with)",
            r"given\s+(her|his|their)\s+heart\s+away",
            r"long\s+time\s+ago",  # Often used with past relationships context
            r"back\s+to\s+(her|his)\s+ex",
        ]
        for pattern in evidence_patterns:
            if re.search(pattern, snippets_text, re.IGNORECASE):
                has_evidence_in_snippets = True
                break
        # Also check for relationship keywords in snippets
        for keyword in relationship_keywords:
            if keyword in snippets_text:
                has_evidence_in_snippets = True
                break
    
    for pattern, message in PAST_RELATIONSHIPS_PATTERNS:
        if re.search(pattern, summary, re.IGNORECASE):
            if not has_relationship_keywords and not has_evidence_in_snippets:
                issues.append(message)
    
    return issues


def check_romance_tropes(summary: str) -> list[str]:
    """Check for generic romance trope language."""
    issues = []
    
    for pattern, message in ROMANCE_TROPES_PATTERNS:
        if re.search(pattern, summary, re.IGNORECASE):
            issues.append(message)
    
    return issues


def check_life_changing_hallucination(summary: str) -> list[str]:
    """Check if summary uses 'life-changing' language without evidence."""
    issues = []
    
    for pattern, message in LIFE_CHANGING_PATTERNS:
        if re.search(pattern, summary, re.IGNORECASE):
            issues.append(message)
    
    return issues


def check_truncation(summary: str) -> list[str]:
    """Check if summary appears truncated (ends with function word)."""
    issues = []
    
    if not summary:
        return issues
    
    summary_clean = summary.strip()
    if not summary_clean:
        return issues
    
    # Check if ends with period (good sign)
    ends_with_period = summary_clean.endswith(".")
    
    # Get last word
    words = summary_clean.split()
    if not words:
        return issues
    
    last_word = words[-1].rstrip(".,!?;:").lower()
    
    # If ends with function word and no period, likely truncated
    if last_word in TRUNCATION_INDICATORS and not ends_with_period:
        issues.append(f"Possibly truncated: ends with function word '{last_word}'")
    elif not ends_with_period:
        issues.append("Missing period at end (may indicate truncation)")
    
    return issues


def validate_topic(
    topic_id: int,
    label: str,
    scene_summary: str,
    keywords: list[str],
    snippets: list[str] | None = None,
) -> dict[str, Any]:
    """Validate a single topic for hallucination patterns."""
    all_issues = []
    
    # Run all checks (now with snippets support)
    all_issues.extend(check_invitation_hallucination(label, scene_summary, keywords, snippets))
    all_issues.extend(check_out_of_character_hallucination(scene_summary, snippets))
    all_issues.extend(check_past_relationships_hallucination(scene_summary, keywords, snippets))
    all_issues.extend(check_romance_tropes(scene_summary))
    all_issues.extend(check_life_changing_hallucination(scene_summary))
    all_issues.extend(check_truncation(scene_summary))
    all_issues.extend(check_genre_cliche_labels(label))

    return {
        "topic_id": topic_id,
        "label": label,
        "scene_summary": scene_summary,
        "keywords": ", ".join(keywords),
        "num_snippets": len(snippets) if snippets else 0,
        "num_issues": len(all_issues),
        "issues": "; ".join(all_issues) if all_issues else "",
        "has_issues": len(all_issues) > 0,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate topic labels and summaries for hallucination patterns.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    parser.add_argument(
        "--labels-json",
        type=str,
        required=True,
        help="Path to labels JSON file produced by the OpenRouter labeling pipeline.",
    )
    
    parser.add_argument(
        "--bertopic-model-path",
        type=str,
        default=None,
        help="Path to BERTopic model (pickle file or directory). If provided, extracts snippets for validation. "
             "If not provided, validation uses keywords only.",
    )
    
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=DEFAULT_BASE_DIR,
        help="Base directory for retrained models (used when --bertopic-model-path is not a full path).",
    )
    
    parser.add_argument(
        "--embedding-model",
        type=str,
        default=DEFAULT_EMBEDDING_MODEL,
        help="Embedding model name (used when loading via project's load_bertopic_model).",
    )
    
    parser.add_argument(
        "--pareto-rank",
        type=int,
        default=1,
        help="Pareto rank of model (used when loading via project's load_bertopic_model).",
    )
    
    parser.add_argument(
        "--use-native",
        action="store_true",
        help="Use native safetensors (used when loading via project's load_bertopic_model).",
    )
    
    parser.add_argument(
        "--model-suffix",
        type=str,
        default="_with_noise_labels",
        help="Model suffix (used when loading via project's load_bertopic_model).",
    )
    
    parser.add_argument(
        "--max-docs-per-topic",
        type=int,
        default=10,
        help="Maximum representative docs per topic to extract for snippet validation.",
    )
    
    parser.add_argument(
        "--output-csv",
        type=str,
        default=None,
        help="Path to output CSV file with validation results. If not provided, prints to stdout.",
    )
    
    parser.add_argument(
        "--limit-topics",
        type=int,
        default=None,
        help="Limit processing to first N topics (useful for testing).",
    )
    
    parser.add_argument(
        "--gold-yaml",
        type=str,
        default=None,
        help="Path to labeling gold YAML (gold_label, gold_scene_summary).",
    )

    parser.add_argument(
        "--gold-categorization-yaml",
        type=str,
        default=None,
        help="Optional path to categorization gold YAML (sexual_function, consent, routing).",
    )

    parser.add_argument(
        "--show-only-issues",
        action="store_true",
        help="Only show topics with issues (filter out clean topics).",
    )
    
    args = parser.parse_args()

    labels_path = Path(args.labels_json)
    if not labels_path.is_file():
        raise FileNotFoundError(f"Labels JSON not found: {labels_path}")

    with labels_path.open("r", encoding="utf-8") as f:
        labels_data = json.load(f)

    if args.gold_yaml:
        gold_path = Path(args.gold_yaml)
        if not gold_path.is_file():
            raise FileNotFoundError(f"Gold YAML not found: {gold_path}")
        cat_path = None
        if args.gold_categorization_yaml:
            cat_path = Path(args.gold_categorization_yaml)
            if not cat_path.is_file():
                raise FileNotFoundError(
                    f"Gold categorization YAML not found: {cat_path}"
                )
        df, summary = compare_against_gold_yaml(
            labels_data, gold_path, categorization_path=cat_path
        )
        print("\n" + "=" * 80)
        print("V3 GOLD COMPARISON SUMMARY")
        print("=" * 80)
        for k, v in summary.items():
            print(f"  {k}: {v}")
        if args.show_only_issues:
            df = df[df["has_issues"]].copy()
        if args.output_csv:
            out = Path(args.output_csv)
            out.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(out, index=False)
            print(f"\nGold comparison saved to: {out}")
        else:
            print("\n", df.to_string(index=False))
        return

    # Load labels
    print(f"Loading labels from: {labels_path}")
    # Load BERTopic model and extract snippets if model path provided
    topic_to_snippets: dict[int, list[str]] = {}
    if args.bertopic_model_path:
        print(f"\nLoading BERTopic model to extract snippets...")
        model_path = Path(args.bertopic_model_path)
        
        # Try to infer parameters from path structure (similar to inspect_random_topics.py)
        import re
        if model_path.is_file() or model_path.suffix == ".pkl":
            model_name = model_path.stem if model_path.suffix == ".pkl" else model_path.name
            base_dir_path = model_path.parent
            
            if len(base_dir_path.parts) >= 2 and base_dir_path.parts[-2] == "retrained":
                inferred_embedding_model = base_dir_path.parts[-1]
                inferred_base_dir = base_dir_path.parent
            else:
                inferred_embedding_model = args.embedding_model
                inferred_base_dir = args.base_dir if args.base_dir else DEFAULT_BASE_DIR
            
            rank_match = re.search(r"model_(\d+)", model_name)
            inferred_rank = int(rank_match.group(1)) if rank_match else args.pareto_rank
            
            suffix_match = re.search(r"model_\d+(.+)", model_name)
            inferred_suffix = suffix_match.group(1) if suffix_match else args.model_suffix
            
            print(f"  Using base_dir: {inferred_base_dir}")
            print(f"  Embedding model: {inferred_embedding_model}")
            print(f"  Pareto rank: {inferred_rank}")
            print(f"  Model suffix: {inferred_suffix}")
            _, topic_model = load_bertopic_model(
                base_dir=inferred_base_dir,
                embedding_model=inferred_embedding_model,
                pareto_rank=inferred_rank,
                use_native=args.use_native,
                model_suffix=inferred_suffix,
            )
        else:
            from bertopic import BERTopic
            print(f"  Loading from directory: {model_path}")
            topic_model = BERTopic.load(str(model_path))
        
        print(f"Extracting up to {args.max_docs_per_topic} representative docs per topic...")
        topic_to_snippets = extract_representative_docs_per_topic(
            topic_model,
            max_docs_per_topic=args.max_docs_per_topic,
        )
        snippets_count = len([tid for tid, docs in topic_to_snippets.items() if docs])
        print(f"  Extracted snippets for {snippets_count} topics")
    else:
        print("\nNo BERTopic model provided - validation will use keywords only (snippets not checked)")
    
    # Validate all topics
    results = []
    topic_items = sorted(labels_data.items(), key=lambda x: int(x[0]))
    
    if args.limit_topics:
        topic_items = topic_items[:args.limit_topics]
    
    print(f"\nValidating {len(topic_items)} topics...")
    
    for topic_id_str, entry in topic_items:
        topic_id = int(topic_id_str)
        label = entry.get("label", "")
        scene_summary = entry.get("scene_summary", "")
        keywords = entry.get("keywords", [])
        snippets = topic_to_snippets.get(topic_id, []) if topic_to_snippets else None
        
        result = validate_topic(topic_id, label, scene_summary, keywords, snippets)
        results.append(result)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Filter if requested
    if args.show_only_issues:
        df = df[df["has_issues"]].copy()
    
    # Sort by number of issues (descending), then by topic_id
    df = df.sort_values(["num_issues", "topic_id"], ascending=[False, True])
    
    # Print summary
    total_topics = len(results)
    topics_with_issues = df["has_issues"].sum()
    total_issues = df["num_issues"].sum()
    
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total topics validated: {total_topics}")
    print(f"Topics with issues: {topics_with_issues} ({topics_with_issues/total_topics*100:.1f}%)")
    print(f"Total issues found: {total_issues}")
    print()
    
    # Print top issues
    if topics_with_issues > 0:
        print("Topics with issues:")
        print("-" * 80)
        for _, row in df.head(20).iterrows():
            if row["has_issues"]:
                print(f"Topic {row['topic_id']}: {row['num_issues']} issue(s)")
                print(f"  Label: {row['label']}")
                print(f"  Summary: {row['scene_summary']}")
                print(f"  Issues: {row['issues']}")
                print()
        
        if len(df) > 20:
            print(f"... ({len(df) - 20} more topics with issues)")
    
    # Save to CSV if requested
    if args.output_csv:
        output_path = Path(args.output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nValidation results saved to: {output_path}")
    else:
        # Print full table to stdout
        print("\nFull validation results:")
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()

