"""Rule-based post-hoc topic classification from topic_info.csv exports."""

from __future__ import annotations

import ast
import json
import logging
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.common.config import resolve_path

LOGGER = logging.getLogger("topic_posthoc")

DEFAULT_RULES_CONFIG = Path("configs/topic_posthoc_rules.yaml")

NOISE_ACTION = "flag_noise"
KEEP_ACTION = "keep"


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
    procedural_keywords: tuple[str, ...] = (
        "elevator",
        "parked",
        "doorway",
        "staircase",
        "ignition",
        "meal",
        "meals",
        "raining",
        "temperature",
        "windshield",
    )
    subgenre_keywords: tuple[str, ...] = (
        "werewolves",
        "werewolf",
        "vampire",
        "vampires",
        "shifter",
        "paranormal",
        "medieval",
        "regency",
        "investigator",
        "detectives",
        "supernatural",
        "immortal",
        "fairies",
    )
    noise_rule_ids: tuple[str, ...] = (
        "multilingual_artifact",
        "publisher_boilerplate",
        "tiny_topic",
        "character_name_cluster",
    )
    character_name_min_hits: int = 3
    character_name_top_n: int = 10
    character_name_min_top5_hits: int = 2
    character_name_min_token_len: int = 4
    character_name_exclude_english: bool = True
    character_name_scene_blocklist: tuple[str, ...] = (
        "door",
        "car",
        "room",
        "open",
        "opened",
        "coffee",
        "phone",
        "hand",
        "hands",
        "eyes",
        "hair",
        "know",
        "kiss",
        "kissed",
        "lips",
        "love",
        "bed",
        "voice",
        "look",
        "looked",
    )
    character_name_stoplist_path: Path | None = None
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
    if proc := raw.get("procedural_transition", {}):
        if kws := proc.get("keywords"):
            cfg.procedural_keywords = tuple(str(k).lower() for k in kws)
    if sub := raw.get("subgenre_marker", {}):
        if kws := sub.get("keywords"):
            cfg.subgenre_keywords = tuple(str(k).lower() for k in kws)
    if char := raw.get("character_name_cluster", {}):
        cfg.character_name_min_hits = int(
            char.get("min_hits", cfg.character_name_min_hits)
        )
        cfg.character_name_top_n = int(char.get("top_n", cfg.character_name_top_n))
        cfg.character_name_min_top5_hits = int(
            char.get("min_top5_hits", cfg.character_name_min_top5_hits)
        )
        cfg.character_name_min_token_len = int(
            char.get("min_token_len", cfg.character_name_min_token_len)
        )
        cfg.character_name_exclude_english = bool(
            char.get("exclude_english", cfg.character_name_exclude_english)
        )
        if block := char.get("scene_token_blocklist"):
            cfg.character_name_scene_blocklist = tuple(str(w).lower() for w in block)
        if path := char.get("stoplist_path"):
            cfg.character_name_stoplist_path = resolve_path(Path(str(path)))
    if noise := raw.get("noise_actions"):
        cfg.noise_rule_ids = tuple(str(n) for n in noise)
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


_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


@lru_cache(maxsize=4)
def _load_character_name_stoplist_cached(stoplist_path: str) -> frozenset[str]:
    """Load token-level entries from the Stage02 character-name stoplist."""
    path = Path(stoplist_path)
    if not path.exists():
        LOGGER.warning("Character-name stoplist not found at %s", path)
        return frozenset()
    tokens: set[str] = set()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            for match in _TOKEN_RE.finditer(s.lower()):
                tok = match.group(0).strip("'-")
                if len(tok) >= 2:
                    tokens.add(tok)
    return frozenset(tokens)


def _character_name_stoplist(cfg: PosthocRulesConfig) -> frozenset[str]:
    if cfg.character_name_stoplist_path is not None:
        path = cfg.character_name_stoplist_path
    else:
        try:
            paths_cfg = yaml.safe_load(
                open(resolve_path(Path("configs/paths.yaml")), encoding="utf-8")
            ) or {}
            raw_path = paths_cfg.get("inputs", {}).get("custom_stoplist")
            if not raw_path:
                return frozenset()
            path = resolve_path(Path(raw_path))
        except OSError:
            return frozenset()
    return _load_character_name_stoplist_cached(str(path))


def _stoplist_hits(words: list[str], stoplist: frozenset[str]) -> list[str]:
    return [w for w in words if w in stoplist]


@lru_cache(maxsize=1)
def _english_stopwords() -> frozenset[str]:
    try:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

        return frozenset(w.lower() for w in ENGLISH_STOP_WORDS)
    except ImportError:
        return frozenset()


def _filtered_name_stoplist_hits(
    words: list[str],
    stoplist: frozenset[str],
    cfg: PosthocRulesConfig,
) -> list[str]:
    """Stoplist hits that pass length / English / scene-blocklist filters."""
    block = set(cfg.character_name_scene_blocklist)
    english = _english_stopwords() if cfg.character_name_exclude_english else frozenset()
    hits: list[str] = []
    for w in words:
        if w in block or len(w) < cfg.character_name_min_token_len:
            continue
        if english and w in english:
            continue
        if w in stoplist:
            hits.append(w)
    return hits


_NAME_MORPH_SUFFIXES = ("ed", "ing", "ly", "ness", "ment", "tion", "ship")


def _name_label_tokens(row: pd.Series) -> list[str]:
    name = str(row.get("Name", "") or "")
    if "_" not in name:
        return []
    raw = name.split("_", 1)[1].split("_")[:4]
    shaped: list[str] = []
    for t in raw:
        if any(t.endswith(s) for s in _NAME_MORPH_SUFFIXES):
            continue
        shaped.append(t)
    return shaped


def rule_character_name_cluster(row: pd.Series, cfg: PosthocRulesConfig) -> bool:
    """Flag topics whose BERTopic Name label is dominated by character-name tokens."""
    stoplist = _character_name_stoplist(cfg)
    if not stoplist:
        return False
    label_tokens = _name_label_tokens(row)
    if len(label_tokens) < 4:
        return False
    block = set(cfg.character_name_scene_blocklist)
    if any(t in block for t in label_tokens):
        return False
    hits = _filtered_name_stoplist_hits(label_tokens, stoplist, cfg)
    if len(hits) != 4:
        return False
    long_hits = [h for h in hits if len(h) >= cfg.character_name_min_token_len + 1]
    return len(long_hits) >= 2


def _keyword_hit_ratio(words: list[str], keywords: tuple[str, ...]) -> float:
    if not words:
        return 0.0
    hits = sum(1 for w in words if any(kw in w or w in kw for kw in keywords))
    return hits / len(words)


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


def rule_procedural_transition(words: list[str], cfg: PosthocRulesConfig) -> bool:
    return _keyword_hit_ratio(words, cfg.procedural_keywords) >= 0.20


def rule_subgenre_marker(row: pd.Series, cfg: PosthocRulesConfig) -> bool:
    words = _representation_words(row, max_words=15)
    name = str(row.get("Name", "") or "").lower()
    blob = " ".join(words) + " " + name
    return any(kw in blob for kw in cfg.subgenre_keywords)


def _content_type_for_flags(flags: list[str]) -> str:
    if not flags:
        return "scene"
    if "character_name_cluster" in flags:
        return "character_name"
    if "subgenre_marker" in flags:
        return "subgenre_marker"
    if "procedural_transition" in flags:
        return "procedural_transition"
    noise = {
        "multilingual_artifact",
        "publisher_boilerplate",
        "tiny_topic",
    }
    if any(f in noise for f in flags):
        return "noise"
    return "scene"


def _suggested_action(flags: list[str], cfg: PosthocRulesConfig) -> str:
    if any(f in cfg.noise_rule_ids for f in flags):
        return NOISE_ACTION
    return KEEP_ACTION


def classify_topic_row(row: pd.Series, cfg: PosthocRulesConfig) -> dict[str, Any]:
    """Classify a single topic_info row."""
    topic_id = int(row["Topic"])
    if topic_id == -1:
        return {
            "Topic": topic_id,
            "content_type": "outlier",
            "posthoc_flags": [],
            "posthoc_reason": "",
            "exclude_from_axes": False,
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
    if rule_procedural_transition(words, cfg):
        flags.append("procedural_transition")
    if rule_subgenre_marker(row, cfg):
        flags.append("subgenre_marker")
    if rule_character_name_cluster(row, cfg):
        flags.append("character_name_cluster")

    action = _suggested_action(flags, cfg)
    exclude = action == NOISE_ACTION
    reason = ";".join(flags)

    return {
        "Topic": topic_id,
        "content_type": _content_type_for_flags(flags),
        "posthoc_flags": flags,
        "posthoc_reason": reason,
        "exclude_from_axes": exclude,
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
    n_flagged = int((non_outlier["suggested_action"] == NOISE_ACTION).sum())
    n_total = len(non_outlier)
    rule_counts: dict[str, int] = {}
    for flags in non_outlier["posthoc_flags"]:
        for rule_id in flags:
            rule_counts[rule_id] = rule_counts.get(rule_id, 0) + 1

    log.info(
        "[POSTHOC] classified %d topics (%d outlier rows); flagged %d/%d as noise",
        len(flags_df),
        int((flags_df["Topic"] == -1).sum()),
        n_flagged,
        n_total,
    )
    for rule_id, count in sorted(rule_counts.items(), key=lambda x: -x[1]):
        log.info("[POSTHOC] rule %s: %d hits", rule_id, count)

    return merged


def build_posthoc_summary(classified_df: pd.DataFrame) -> dict[str, Any]:
    """Build JSON-serializable summary for posthoc_summary.json."""
    non_outlier = classified_df[classified_df["Topic"] != -1]
    n_total = len(non_outlier)
    n_flagged = int((non_outlier["suggested_action"] == NOISE_ACTION).sum())
    rule_counts: dict[str, int] = {}
    for flags in non_outlier["posthoc_flags"]:
        if not isinstance(flags, list):
            continue
        for rule_id in flags:
            rule_counts[rule_id] = rule_counts.get(rule_id, 0) + 1

    return {
        "n_topics": n_total,
        "n_flagged_noise": n_flagged,
        "flagged_fraction": round(n_flagged / n_total, 4) if n_total else 0.0,
        "rule_hits": rule_counts,
        "content_type_counts": (
            non_outlier["content_type"].value_counts().to_dict() if n_total else {}
        ),
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
        "content_type",
        "posthoc_flags",
        "posthoc_reason",
        "exclude_from_axes",
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
