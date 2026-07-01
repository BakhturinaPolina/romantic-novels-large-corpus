"""Rule-based post-hoc topic classification from topic_info.csv exports."""

from __future__ import annotations

import ast
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.common.config import resolve_path

LOGGER = logging.getLogger("topic_posthoc")

DEFAULT_RULES_CONFIG = Path("configs/call73/topic_posthoc_rules.yaml")

HARD_EXCLUDE_ACTION = "hard_exclude"
SOFT_REVIEW_ACTION = "soft_review"
KEEP_ACTION = "keep"
# Backward-compatible alias
NOISE_ACTION = HARD_EXCLUDE_ACTION


@dataclass
class PosthocRulesConfig:
    tiny_topic_min_size: int = 200
    multilingual_short_token_max_len: int = 2
    multilingual_short_token_ratio: float = 0.50
    multilingual_non_ascii_ratio: float = 0.50
    publisher_keywords: tuple[str, ...] = (
        "copyright",
        "copyrighted",
        "publisher",
        "harpercollins",
        "penguin",
        "trademark",
        "isbn",
        "acknowledgments",
        "document outline",
        "dedication page",
        "chapter one",
        "table of contents",
        "unauthorized reproduction",
        "published by",
    )
    publisher_keyword_patterns: tuple[re.Pattern[str], ...] = field(default_factory=tuple)
    hard_exclude_rule_ids: tuple[str, ...] = (
        "multilingual_artifact",
        "publisher_boilerplate",
    )
    soft_review_rule_ids: tuple[str, ...] = ("tiny_topic",)
    publisher_name_keywords: tuple[str, ...] = (
        "chapter",
        "book",
        "books",
        "author",
        "reading",
        "www",
        "com",
        "series",
    )


def _compile_publisher_patterns(keywords: tuple[str, ...]) -> tuple[re.Pattern[str], ...]:
    patterns: list[re.Pattern[str]] = []
    for kw in keywords:
        escaped = re.escape(kw.lower())
        if " " in kw:
            body = escaped.replace(r"\ ", r"\s+")
        else:
            body = escaped
        patterns.append(re.compile(rf"(?<!\w){body}(?!\w)", re.IGNORECASE))
    return tuple(patterns)


def load_rules_config(config_path: Path | None = None) -> PosthocRulesConfig:
    """Load thresholds from YAML; fall back to dataclass defaults."""
    path = resolve_path(config_path or DEFAULT_RULES_CONFIG)
    if not path.exists():
        LOGGER.warning("Rules config not found at %s; using defaults", path)
        return _finalize_config(PosthocRulesConfig())

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    cfg = PosthocRulesConfig()
    if tiny := raw.get("tiny_topic", {}):
        cfg.tiny_topic_min_size = int(tiny.get("min_size", cfg.tiny_topic_min_size))
    if ml := raw.get("multilingual_artifact", {}):
        cfg.multilingual_short_token_max_len = int(
            ml.get("short_token_max_len", cfg.multilingual_short_token_max_len)
        )
        cfg.multilingual_short_token_ratio = float(
            ml.get("short_token_ratio", cfg.multilingual_short_token_ratio)
        )
        cfg.multilingual_non_ascii_ratio = float(
            ml.get("non_ascii_ratio", cfg.multilingual_non_ascii_ratio)
        )
    if pub := raw.get("publisher_boilerplate", {}):
        if kws := pub.get("keywords"):
            cfg.publisher_keywords = tuple(str(k).lower() for k in kws)
        if name_kws := pub.get("name_keywords"):
            cfg.publisher_name_keywords = tuple(str(k).lower() for k in name_kws)
    if hard := raw.get("hard_exclude_actions"):
        cfg.hard_exclude_rule_ids = tuple(str(n) for n in hard)
    elif noise := raw.get("noise_actions"):
        cfg.hard_exclude_rule_ids = tuple(str(n) for n in noise)
    if soft := raw.get("soft_review_actions"):
        cfg.soft_review_rule_ids = tuple(str(n) for n in soft)
    return _finalize_config(cfg)


def _finalize_config(cfg: PosthocRulesConfig) -> PosthocRulesConfig:
    if not cfg.publisher_keyword_patterns:
        cfg.publisher_keyword_patterns = _compile_publisher_patterns(cfg.publisher_keywords)
    return cfg


def _parse_word_list(value: Any) -> list[str]:
    """Parse Representation/KeyBERT columns from topic_info.csv."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(w).strip().lower() for w in value if str(w).strip()]
    text = str(value).strip()
    if not text:
        return []
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            return [str(w).strip().lower() for w in parsed if str(w).strip()]
    except (ValueError, SyntaxError):
        pass
    return [w.strip().lower() for w in text.replace(",", " ").split() if w.strip()]


def _topic_words(row: pd.Series, *, max_words: int = 40) -> list[str]:
    words: list[str] = []
    for col in ("Representation", "KeyBERT", "MMR", "POS", "Name"):
        if col in row.index:
            words.extend(_parse_word_list(row.get(col)))
    if "Name" in row.index:
        name = str(row.get("Name", "") or "")
        if "_" in name:
            parts = name.split("_", 1)
            if len(parts) == 2 and parts[1]:
                words.extend(parts[1].split("_"))
    seen: set[str] = set()
    deduped: list[str] = []
    for w in words:
        if w and w not in seen:
            seen.add(w)
            deduped.append(w)
    return deduped[:max_words]


def _representation_words(row: pd.Series, *, max_words: int = 15) -> list[str]:
    words = _parse_word_list(row.get("Representation"))
    if not words and "Name" in row.index:
        name = str(row.get("Name", "") or "")
        if "_" in name:
            parts = name.split("_", 1)
            if len(parts) == 2:
                words = parts[1].split("_")
    return words[:max_words]


def _repr_docs_text(row: pd.Series) -> str:
    raw = row.get("Representative_Docs", "")
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return ""
    text = str(raw).lower()
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            return " ".join(str(d).lower() for d in parsed)
    except (ValueError, SyntaxError):
        pass
    return text


def _text_has_publisher_keywords(text: str, patterns: tuple[re.Pattern[str], ...]) -> bool:
    if not text.strip():
        return False
    return any(pattern.search(text) for pattern in patterns)


def rule_multilingual_artifact(words: list[str], cfg: PosthocRulesConfig) -> bool:
    if len(words) < 3:
        return False
    short = sum(1 for w in words if len(w) <= cfg.multilingual_short_token_max_len)
    short_ratio = short / len(words)
    if short_ratio >= cfg.multilingual_short_token_ratio:
        return True
    non_ascii = sum(1 for w in words if any(ord(c) > 127 for c in w))
    return (non_ascii / len(words)) >= cfg.multilingual_non_ascii_ratio


def rule_publisher_boilerplate(
    words: list[str], repr_text: str, cfg: PosthocRulesConfig
) -> bool:
    patterns = cfg.publisher_keyword_patterns or _compile_publisher_patterns(
        cfg.publisher_keywords
    )
    if _text_has_publisher_keywords(repr_text, patterns):
        return True
    rep_words = words[:10] if words else []
    if not rep_words:
        return False
    name_hits = sum(1 for w in rep_words if w in cfg.publisher_name_keywords)
    return name_hits >= 3


def rule_tiny_topic(count: int, cfg: PosthocRulesConfig) -> bool:
    return count < cfg.tiny_topic_min_size


def _suggested_action(flags: list[str], cfg: PosthocRulesConfig) -> str:
    if any(f in cfg.hard_exclude_rule_ids for f in flags):
        return HARD_EXCLUDE_ACTION
    if any(f in cfg.soft_review_rule_ids for f in flags):
        return SOFT_REVIEW_ACTION
    return KEEP_ACTION


def classify_topic_row(row: pd.Series, cfg: PosthocRulesConfig) -> dict[str, Any]:
    """Classify a single topic_info row."""
    topic_id = int(row["Topic"])
    if topic_id == -1:
        return {
            "Topic": topic_id,
            "posthoc_flags": [],
            "posthoc_reason": "",
            "exclude_from_axes": False,
            "hard_exclude_candidate": False,
            "soft_review_candidate": False,
            "suggested_action": KEEP_ACTION,
        }

    count = int(row.get("Count", 0) or 0)
    words = _topic_words(row)
    repr_text = _repr_docs_text(row)
    flags: list[str] = []

    if rule_multilingual_artifact(words, cfg):
        flags.append("multilingual_artifact")
    if rule_publisher_boilerplate(_representation_words(row), repr_text, cfg):
        flags.append("publisher_boilerplate")
    if rule_tiny_topic(count, cfg):
        flags.append("tiny_topic")

    action = _suggested_action(flags, cfg)
    hard_exclude = action == HARD_EXCLUDE_ACTION
    soft_review = action == SOFT_REVIEW_ACTION
    reason = ";".join(flags)

    return {
        "Topic": topic_id,
        "posthoc_flags": flags,
        "posthoc_reason": reason,
        "exclude_from_axes": hard_exclude,
        "hard_exclude_candidate": hard_exclude,
        "soft_review_candidate": soft_review and not hard_exclude,
        "suggested_action": action,
    }


def classify_topics_from_info(
    df: pd.DataFrame,
    *,
    config_path: Path | None = None,
    logger: logging.Logger | None = None,
) -> pd.DataFrame:
    """Classify all topics in a topic_info DataFrame."""
    log = logger or LOGGER
    cfg = load_rules_config(config_path)

    work = df.copy()
    if "Topic" not in work.columns:
        raise ValueError("topic_info DataFrame must contain a Topic column")

    rows = [classify_topic_row(row, cfg) for _, row in work.iterrows()]
    flags_df = pd.DataFrame(rows)

    merged = work.merge(flags_df, on="Topic", how="left", suffixes=("", "_posthoc"))

    non_outlier = flags_df[flags_df["Topic"] != -1]
    n_hard = int(non_outlier["hard_exclude_candidate"].sum())
    n_soft = int(non_outlier["soft_review_candidate"].sum())
    n_total = len(non_outlier)
    rule_counts: dict[str, int] = {}
    for flags in non_outlier["posthoc_flags"]:
        for rule_id in flags:
            rule_counts[rule_id] = rule_counts.get(rule_id, 0) + 1

    log.info(
        "[POSTHOC] classified %d topics (%d outlier rows); hard=%d soft=%d / %d",
        len(flags_df),
        int((flags_df["Topic"] == -1).sum()),
        n_hard,
        n_soft,
        n_total,
    )
    for rule_id, count in sorted(rule_counts.items(), key=lambda x: -x[1]):
        log.info("[POSTHOC] rule %s: %d hits", rule_id, count)

    return merged


def build_posthoc_summary(classified_df: pd.DataFrame) -> dict[str, Any]:
    """Build JSON-serializable summary for posthoc_summary.json."""
    non_outlier = classified_df[classified_df["Topic"] != -1]
    n_total = len(non_outlier)
    n_hard = int(non_outlier.get("hard_exclude_candidate", pd.Series(dtype=bool)).sum())
    n_soft = int(non_outlier.get("soft_review_candidate", pd.Series(dtype=bool)).sum())
    rule_counts: dict[str, int] = {}
    for flags in non_outlier["posthoc_flags"]:
        if not isinstance(flags, list):
            continue
        for rule_id in flags:
            rule_counts[rule_id] = rule_counts.get(rule_id, 0) + 1

    return {
        "n_topics": n_total,
        "n_hard_exclude": n_hard,
        "n_soft_review": n_soft,
        "flagged_fraction": round((n_hard + n_soft) / n_total, 4) if n_total else 0.0,
        "rule_hits": rule_counts,
    }


def write_posthoc_artifacts(
    topic_info_path: Path,
    out_dir: Path | None = None,
    *,
    config_path: Path | None = None,
    logger: logging.Logger | None = None,
) -> tuple[Path, Path]:
    """Read topic_info.csv, classify, write posthoc_flags.csv and posthoc_summary.json."""
    log = logger or LOGGER
    topic_info_path = Path(topic_info_path)
    out_dir = Path(out_dir or topic_info_path.parent)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(topic_info_path)
    classified = classify_topics_from_info(df, config_path=config_path, logger=log)

    flags_path = out_dir / "posthoc_flags.csv"
    summary_path = out_dir / "posthoc_summary.json"

    export_cols = [
        "Topic",
        "Count",
        "Name",
        "posthoc_flags",
        "posthoc_reason",
        "exclude_from_axes",
        "hard_exclude_candidate",
        "soft_review_candidate",
        "suggested_action",
    ]
    export_cols = [c for c in export_cols if c in classified.columns]
    export_df = classified[export_cols].copy()
    export_df["posthoc_flags"] = export_df["posthoc_flags"].apply(
        lambda x: "|".join(x) if isinstance(x, list) else str(x)
    )
    export_df.to_csv(flags_path, index=False)

    summary = build_posthoc_summary(classified)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    log.info("[POSTHOC] wrote %s and %s", flags_path, summary_path)
    return flags_path, summary_path
