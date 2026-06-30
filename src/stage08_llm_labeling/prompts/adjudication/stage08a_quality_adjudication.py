"""Stage 08A: LLM quality adjudication prompt (no romance theme labels)."""

from __future__ import annotations

PROMPT_VERSION = "v2_snippets_first_ignore_names"

SYSTEM_PROMPT = """You are a topic-quality auditor for a BERTopic model trained on English romance novels.

Your job is ONLY to decide whether a topic is technically worth sending to descriptive LLM labeling.

Do NOT assign romance themes, subgenre labels, courtship categories, or axis membership.
Do NOT invent a descriptive topic title.

## Evidence priority (highest → lowest)

1. SNIPPETS — representative sentences; strongest signal of what documents share
2. KeyBERT — salient distilled keywords
3. MMR — diverse salient keywords
4. POS — content-word (noun/verb/adj) keywords
5. ALL KEYWORDS — combined union across KeyBERT, MMR, and POS
6. Main — lowest weight; often high-frequency tokens, dialogue glue, or character names

Weight higher-priority evidence more heavily. A weak or name-heavy Main representation does NOT
by itself justify exclusion when snippets or alternate representations show a coherent theme.

## Character names

Romance novels always name characters. Treat proper names as interchangeable placeholders
(he/she/they); the specific name does not matter for quality assessment.

- IGNORE character first/last names when judging interpretability
- Do NOT exclude or downgrade a topic because Main contains character names
- Do NOT use content_status=character_residue unless virtually ALL evidence (snippets AND
  all keyword lists) is names with no other semantic content
- Stage07 flag possible_character_residue is advisory only; override it when other evidence
  supports a coherent topic

## When to exclude (exclude_noise)

Exclude ONLY when the topic is clearly not worth labeling:
- Snippets are extremely short or fragmentary AND do not cohere with each other
- Keyword lists are extremely sparse (roughly 1–2 meaningful words) across multiple
  representations AND snippets do not clarify a theme
- Nearly every keyword across ALL representations is a character name with no thematic words
- Obvious non-narrative garbage: publisher/paratext boilerplate, chapter-number residue,
  multilingual or encoding artifacts, or incoherent unrelated word salad with no snippet support

## When to pass (pass_to_labeling)

Pass when snippets OR KeyBERT/MMR/POS (or the combined keyword union) reveal an interpretable
theme, even if Main looks generic, name-heavy, or weak. Use weak_but_interpretable when the
signal is thin but usable.

Return strict JSON matching the schema."""

USER_PROMPT_TEMPLATE = """TOPIC ID: {topic_id}
ASSIGNED DOCUMENTS: {n_assigned_docs}
SNIPPETS AVAILABLE: {n_snippets_available}

STAGE07 FLAGS: {stage07_flags}
STAGE07 REASON: {stage07_reason}
RECOMMENDED NEXT STEP: {recommended_next_step}

## Evidence (priority order)

### 1. SNIPPETS (highest weight)
{snippets_block}

### 2. KeyBERT
{keybert_words}

### 3. MMR
{mmr_words}

### 4. POS
{pos_words}

### 5. ALL KEYWORDS (KeyBERT + MMR + POS union)
{all_keywords_words}

### 6. Main (lowest weight)
{main_words}

Decide whether this topic should proceed to descriptive labeling (Stage 08B).

Allowed llm_quality_decision values:
- pass_to_labeling
- exclude_noise
- manual_review_needed

Allowed content_status values:
- coherent_topic
- weak_but_interpretable
- publisher_or_paratext_noise
- multilingual_or_encoding_noise
- character_residue
- incoherent_mixed_topic

Return JSON only."""

QUALITY_ADJUDICATION_SCHEMA: dict = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "topic_id": {"type": "integer"},
        "llm_quality_decision": {
            "type": "string",
            "enum": [
                "pass_to_labeling",
                "exclude_noise",
                "manual_review_needed",
            ],
        },
        "content_status": {
            "type": "string",
            "enum": [
                "coherent_topic",
                "weak_but_interpretable",
                "publisher_or_paratext_noise",
                "multilingual_or_encoding_noise",
                "character_residue",
                "incoherent_mixed_topic",
            ],
        },
        "reason": {"type": "string"},
        "manual_review_needed": {"type": "boolean"},
    },
    "required": [
        "topic_id",
        "llm_quality_decision",
        "content_status",
        "reason",
        "manual_review_needed",
    ],
}


def format_snippets_block(snippets: list[str]) -> str:
    lines = []
    for i, s in enumerate(snippets, 1):
        text = (s or "").strip()
        if text:
            lines.append(f"{i}. {text}")
    return "\n".join(lines) if lines else "(none)"


def _words_from_rep(reps: dict, name: str) -> list[str]:
    raw = (reps.get(name) or {}).get("words") or []
    return [str(w).strip() for w in raw if str(w).strip()]


def format_all_keywords(reps: dict) -> str:
    """Union of KeyBERT, MMR, POS keywords (Main excluded), preserving first-seen order."""
    seen: set[str] = set()
    ordered: list[str] = []
    for rep in ("KeyBERT", "MMR", "POS"):
        for word in _words_from_rep(reps, rep):
            key = word.lower()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(word)
    return ", ".join(ordered) if ordered else "(none)"


def format_user_prompt(packet: dict) -> str:
    reps = packet.get("representations") or {}
    return USER_PROMPT_TEMPLATE.format(
        topic_id=packet.get("topic_id", ""),
        n_assigned_docs=packet.get("n_assigned_docs", 0),
        n_snippets_available=packet.get("n_snippets_available", 0),
        stage07_flags=", ".join(packet.get("stage07_flags") or []) or "(none)",
        stage07_reason=packet.get("stage07_reason") or "(none)",
        recommended_next_step=packet.get("recommended_next_step") or "(none)",
        snippets_block=format_snippets_block(packet.get("snippets") or []),
        keybert_words=", ".join(_words_from_rep(reps, "KeyBERT")) or "(none)",
        mmr_words=", ".join(_words_from_rep(reps, "MMR")) or "(none)",
        pos_words=", ".join(_words_from_rep(reps, "POS")) or "(none)",
        all_keywords_words=format_all_keywords(reps),
        main_words=", ".join(_words_from_rep(reps, "Main")) or "(none)",
    )
