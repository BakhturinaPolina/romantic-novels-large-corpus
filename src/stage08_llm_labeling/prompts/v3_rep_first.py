"""Stage 08 v3 rep-first prompt — keyword thread (KeyBERT/MMR/POS) primary; snippets ground the beat."""

from src.stage08_llm_labeling.prompts.blocks.character_names import (
    CHARACTER_NAMES_FEW_SHOTS,
    CHARACTER_NAMES_RULES,
)
from src.stage08_llm_labeling.prompts.blocks.corpus_context import CORPUS_CONTEXT
from src.stage08_llm_labeling.prompts.blocks.evidence_hierarchy_rep_first import (
    CHARACTER_NAMES_REP_FIRST_ADDENDUM,
    EVIDENCE_HIERARCHY_REP_FIRST,
    STAGE07_EMPHASIZE_REP_FIRST,
)
from src.stage08_llm_labeling.prompts.blocks.few_shots_general import GENERAL_FEW_SHOTS
from src.stage08_llm_labeling.prompts.blocks.few_shots_rep_first import REP_FIRST_FEW_SHOTS
from src.stage08_llm_labeling.prompts.blocks.natural_label_voice import NATURAL_LABEL_VOICE
from src.stage08_llm_labeling.prompts.blocks.routing_rules import (
    ROLE_AND_TASK,
    ROUTING_RULES,
    V3_SCHEMA_EXTENSION,
)
from src.stage08_llm_labeling.prompts.blocks.sexual_precision import (
    SEXUAL_FEW_SHOTS,
    SEXUAL_LABELING_RULES,
)

SYSTEM_PROMPT = "\n\n".join([
    ROLE_AND_TASK,
    CORPUS_CONTEXT,
    EVIDENCE_HIERARCHY_REP_FIRST,
    V3_SCHEMA_EXTENSION,
    NATURAL_LABEL_VOICE,
    ROUTING_RULES,
    STAGE07_EMPHASIZE_REP_FIRST,
    CHARACTER_NAMES_RULES,
    CHARACTER_NAMES_REP_FIRST_ADDENDUM,
    GENERAL_FEW_SHOTS,
    REP_FIRST_FEW_SHOTS,
    CHARACTER_NAMES_FEW_SHOTS,
    SEXUAL_LABELING_RULES,
    SEXUAL_FEW_SHOTS,
])

USER_PROMPT_TEMPLATE = """
### TOPIC DATA (label from keyword thread first; snippets ground the beat)

### 1. ALL KEYWORDS (KeyBERT + MMR + POS union — read first; defines topic thread)
{all_keywords}

### 2. KeyBERT
{keybert}

### 3. MMR
{mmr}

### 4. POS
{pos}

POS CUES (from POS keywords):
{pos_cues}

### 5. REPRESENTATIVE SNIPPETS (secondary — concretize the keyword thread; do not label from one snippet alone)
{snippets}

### 6. Main (lowest weight — glue words and names; never override keyword thread)
{main}

STAGE07 POST-HOC HINTS (advisory, may be overridden with rationale):
{stage07_hints}

OPTIONAL EXISTING LABELS (avoid reusing exactly):
{existing_labels}

### TASK

Using ONLY the evidence above, produce one JSON object matching the v3 schema.

MANDATORY REASONING (internal — do not output separately):
A. What semantic field do KeyBERT + MMR + POS + ALL KEYWORDS share?
B. Is that field broader than what any single snippet shows?
C. Which snippet best exemplifies that field (not necessarily the most literal)?

OUTPUT ORDER:
1. content_type, is_noise, exclude_from_axes
2. sexual_explicitness, sexual_function, consent_status
3. label (2–6 words — must pass picture test AND reflect the keyword thread)
4. scene_summary (one sentence grounded in the best-fitting snippet)
5. rationale (1–3 sentences: cite KeyBERT/MMR/POS or ALL KEYWORDS first, then snippets)

Classify sexual JSON fields before writing the label.
""".strip()

ROMANCE_AWARE_SYSTEM_PROMPT = SYSTEM_PROMPT
ROMANCE_AWARE_USER_PROMPT = USER_PROMPT_TEMPLATE
