"""Stage 08 v2 OVAT prompt variants (call 73 sweep). Baseline remains v2_multi_genre."""

from __future__ import annotations

from src.stage08_llm_labeling.prompts.legacy.v1_scene_only import (
    SYSTEM_PROMPT as _V1_SYSTEM,
    USER_PROMPT_TEMPLATE as _V1_USER,
)
from src.stage08_llm_labeling.prompts.legacy.v2_multi_genre_full import (
    SYSTEM_PROMPT as V2_SYSTEM,
    USER_PROMPT_TEMPLATE as V2_USER,
    _CORPUS_CONTEXT,
    _FEW_SHOTS,
    _TAXONOMY_ALIGNMENT,
    _V2_SCHEMA_EXTENSION,
)

_USER_V2_BODY = _V1_USER.replace(
    "You are labeling topics in a corpus of modern heterosexual romantic and erotic fiction.",
    "You are labeling topics in a multi-genre English romance corpus (2000–2017).",
)

_USER_WITH_STAGE07 = _USER_V2_BODY.replace(
    "TOPIC KEYWORDS (most important first):\n{kw}{hints}",
    "STAGE07 POST-HOC HINTS (optional, may be overridden with rationale):\n{stage07_hints}\n\n"
    "TOPIC KEYWORDS (most important first):\n{kw}{hints}",
)

_USER_SNIPPETS_FIRST = _USER_WITH_STAGE07.replace(
    "### TOPIC DATA\n\nSTAGE07 POST-HOC HINTS",
    "### TOPIC DATA\n\n"
    "REPRESENTATIVE SNIPPETS (read first — primary evidence; keywords are secondary when they conflict):\n"
    "{snippets}\n\n"
    "STAGE07 POST-HOC HINTS",
).replace(
    "REPRESENTATIVE SNIPPETS (short excerpts from the corpus):\n{snippets}\n\n",
    "",
)

_USER_NO_STAGE07 = _USER_V2_BODY

_STAGE07_EMPHASIZE = """
STAGE07 HINTS (IMPORTANT): Post-hoc flags are often correct for publisher_boilerplate topics,
but may false-positive on real scenes. Override only when snippets clearly contradict the flag;
cite evidence in rationale.
""".strip()

_FEW_SHOT_EXPANDED = _FEW_SHOTS + """

Example G — chuckle / amusement delivery (T13 style):
Keywords: chuckle, amusement, pathetic, notion
→ content_type: discourse, primary_categories: [narrative_style]
→ label: "Amused Chuckle Response", exclude_from_axes: false

Example H — sensory scent thread (T12 style):
Keywords: mixture, damp, lungs, combination (heterogeneous) | Snippets: smell, scent, faction
→ content_type: scene (NOT noise if snippets share olfactory thread)
→ label: "Lingering Scent Awareness", primary_categories: [romance_core or sensory beat]
"""

_LABEL_FIRST = """
OUTPUT ORDER (MANDATORY): Decide content_type and exclude_from_axes FIRST, then label and
scene_summary, then categories, then rationale last. Do not rationalize routing after writing the label.
""".strip()

_CHECKLIST = """
PRE-OUTPUT CHECKLIST (apply before JSON):
1. Did snippets agree on a concrete action? If yes, do not mark noise.
2. Are top keywords mostly abstract nouns / speech tags with no setting? → discourse (exclude_from_axes false).
3. Publisher/chapter/author boilerplate in snippets? → paratext or noise + exclude.
4. Label is 2–6 words, Title Case, not a keyword chain?
""".strip()

_C1_DISCOURSE_STRICT = """
DISCOURSE ROUTING (STRICT): Route content_type discourse when ANY hold:
- Top keywords are mostly abstract (choices, possibility, percent, explanation) without setting nouns.
- Speech-tag verbs dominate (whispered, chuckled, uttered, sighed) without a sustained scene action.
- Snippets are short quoted lines without shared location/object.
Set exclude_from_axes false for discourse (feeds Stage09 axes); true only for noise/paratext.
""".strip()

_C2_NOISE_CONSERVATIVE = """
NOISE ROUTING (CONSERVATIVE): Mark is_noise true only when TWO OR MORE signals agree:
(1) boilerplate/encoding garbage, (2) snippets unrelated to each other AND to keywords,
(3) no repeatable action across snippets. A single odd keyword (lungs, rear) is NOT enough for noise.
""".strip()

_C3_SNIPPET_GROUNDING = """
SNIPPET-FIRST GROUNDING: When representative snippets agree on a thread (smell, kiss, phone call),
that thread defines the label and content_type even if top keywords look incoherent. Keywords are
secondary evidence only when snippets conflict or are missing.
""".strip()

_C4_ABSTRACT_DISCOURSE = """
ABSTRACT INNER SPEECH: Topics with love/hate swings, choices, or possibility language but no
shared setting across snippets → discourse (not scene), exclude_from_axes false, narrative_style.
Labels may describe the emotional pattern ("Conflicted Feelings") without inventing a physical scene.
""".strip()

_C5_MERGE_LADDER = """
INTIMACY MERGE LADDER (merge_group_hint):
- "intimacy_kiss_cluster": lip/temple tender kisses without explicit genital terms
- "intimacy_deep_kiss_cluster": kissed + tongue/mouth emphasis
- "intimacy_explicit_touch_cluster": explicit body-part touch (cock, pussy, etc.)
Use distinct labels per tier; do not collapse tiers.
""".strip()

_C6_LABEL_ANTIPATTERNS = """
EXTRA BAD LABELS (never use):
- "Incoherent Keyword Cluster", "Statistical Possibility Speech", "Damp Lungs And Rear"
- Any label that lists 3+ raw keywords joined by "And"
Prefer the central human-readable beat from snippets.
""".strip()

_C7_DISCOURSE_PRIOR = """
CORPUS PRIOR: Roughly 40% of call-73 topics are discourse, paratext, or noise — not scene inventory.
When uncertain between scene and discourse, favor discourse if keywords lack setting nouns.
""".strip()

_C8_CHARACTER_NAMES = """
CHARACTER-NAME CLUSTER RULES (CRITICAL)

A topic is a character-name artifact when ALL hold:
1. The only clear shared element across snippets is a proper name (or title+name), AND
2. Snippets describe different settings, actions, or plot situations, AND
3. Top keywords are mostly abstract nouns (choices, possibility, measure, screen) without a scene anchor.

When true:
- is_noise: true
- content_type: noise (do NOT invent "character_name" — not in schema)
- exclude_from_axes: true
- label: use the fixed phrase "Character Name Artifact" (never embed the name)
- scene_summary: one sentence noting incoherent name co-occurrence; do not invent a plot
- primary_categories: ["narrative_style"]

NEVER put proper names in "label" or "scene_summary":
- BAD: "Negotiating Cole's Future", "Reassurance About Ryan", "Scattered Caleb Name References"
- GOOD: "Character Name Artifact", "Negotiating a Child's Future", "Reassurance About a Friend"

FORBIDDEN label patterns for name artifacts:
- "Scattered … Name References/Cluster", "X Name-Clustered Exchanges", "Aunt Character References"

Override stage07 character_name_cluster ONLY when snippets share a concrete repeated beat
(same setting + same action), e.g. horses at a ranch, shower before leaving, shared meal planning.
Cite the shared setting/action in rationale; do not cite the shared name alone.

Honorifics (sir, aunt as isolated token) → treat like name artifacts unless snippets share
one scene type beyond the title word.
""".strip()

_C8_FEW_SHOT_APPEND = """

Example I — name artifact (character-name cluster):
Keywords: choices, inevitable, president, folks | Snippets: mention "Marcus" in unrelated arguments
→ is_noise: true, content_type: noise, exclude_from_axes: true
→ label: "Character Name Artifact"
→ NOT "Group Conflict and Choices" unless snippets share one argument type + setting

Example J — valid stage07 override (real scene despite flag):
Flag: character_name_cluster | Snippets: all mention horses, stable, rural property
→ is_noise: false, content_type: scene, exclude_from_axes: false
→ label: "Horses at Ranch Property"
→ rationale must cite horses/stable, not the shared character name
"""


def _build_system(*extra_blocks: str, few_shots: str | None = None) -> str:
    base = _V1_SYSTEM.replace(
        "You are RomanceTopicLabeler, an expert assistant for automatic topic labelling in modern heterosexual romantic and erotic fiction.",
        "You are RomanceTopicLabeler, an expert assistant for automatic topic labelling in modern English romance fiction across multiple subgenres.",
    )
    parts = [base, _CORPUS_CONTEXT, _V2_SCHEMA_EXTENSION, _TAXONOMY_ALIGNMENT]
    parts.extend(extra_blocks)
    parts.append(few_shots if few_shots is not None else _FEW_SHOTS)
    return "\n\n".join(parts)


def _conceptual_system(*concept_blocks: str) -> str:
    return _build_system(*concept_blocks)


VARIANTS: dict[str, tuple[str, str]] = {
    "v2_s1_snippets_first": (_build_system(), _USER_SNIPPETS_FIRST),
    "v2_s4_no_stage07": (_build_system(), _USER_NO_STAGE07),
    "v2_s4_stage07_emphasize": (_build_system(_STAGE07_EMPHASIZE), _USER_WITH_STAGE07),
    "v2_s5_no_fewshot": (_build_system(few_shots=""), _USER_WITH_STAGE07),
    "v2_s5_expanded_fewshot": (_build_system(few_shots=_FEW_SHOT_EXPANDED), _USER_WITH_STAGE07),
    "v2_s6_label_first": (_build_system(_LABEL_FIRST), _USER_WITH_STAGE07),
    "v2_s7_checklist": (_build_system(_CHECKLIST), _USER_WITH_STAGE07),
    "v2_c1_discourse_strict": (_conceptual_system(_C1_DISCOURSE_STRICT), V2_USER),
    "v2_c2_noise_conservative": (_conceptual_system(_C2_NOISE_CONSERVATIVE), V2_USER),
    "v2_c3_snippet_grounding": (_conceptual_system(_C3_SNIPPET_GROUNDING), V2_USER),
    "v2_c4_abstract_discourse": (_conceptual_system(_C4_ABSTRACT_DISCOURSE), V2_USER),
    "v2_c5_merge_ladder": (_conceptual_system(_C5_MERGE_LADDER), V2_USER),
    "v2_c6_label_antipatterns": (_conceptual_system(_C6_LABEL_ANTIPATTERNS), V2_USER),
    "v2_c7_discourse_prior": (_conceptual_system(_C7_DISCOURSE_PRIOR), V2_USER),
    "v2_c8_character_names": (
        _build_system(
            _STAGE07_EMPHASIZE,
            _C8_CHARACTER_NAMES,
            few_shots=_FEW_SHOTS + _C8_FEW_SHOT_APPEND,
        ),
        _USER_SNIPPETS_FIRST,
    ),
}


def load_variant(version: str) -> tuple[str, str]:
    key = version.lower()
    if key not in VARIANTS:
        raise ValueError(f"Unknown v2 variant: {version!r}")
    return VARIANTS[key]
