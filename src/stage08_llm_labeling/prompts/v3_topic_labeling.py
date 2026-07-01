"""Stage 08 v3 production prompt — topic labeling + scene summary + sexual-precision fields."""

from src.stage08_llm_labeling.prompts.blocks.character_names import (
    CHARACTER_NAMES_FEW_SHOTS,
    CHARACTER_NAMES_RULES,
)
from src.stage08_llm_labeling.prompts.blocks.corpus_context import (
    CORPUS_CONTEXT,
    EVIDENCE_HIERARCHY,
    STAGE07_EMPHASIZE,
)
from src.stage08_llm_labeling.prompts.blocks.few_shots_general import GENERAL_FEW_SHOTS
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
    EVIDENCE_HIERARCHY,
    V3_SCHEMA_EXTENSION,
    NATURAL_LABEL_VOICE,
    ROUTING_RULES,
    STAGE07_EMPHASIZE,
    CHARACTER_NAMES_RULES,
    GENERAL_FEW_SHOTS,
    CHARACTER_NAMES_FEW_SHOTS,
    SEXUAL_LABELING_RULES,
    SEXUAL_FEW_SHOTS,
])

USER_PROMPT_TEMPLATE = """
### TOPIC DATA (evidence priority: snippets first, Main lowest)

REPRESENTATIVE SNIPPETS (read first — primary evidence):
{snippets}

### 2. KeyBERT
{keybert}

### 3. MMR
{mmr}

### 4. POS
{pos}

POS CUES (from POS keywords):
{pos_cues}

### 5. ALL KEYWORDS (KeyBERT + MMR + POS union; Main excluded)
{all_keywords}

### 6. Main (lowest weight — do not label from Main alone when snippets disagree)
{main}

STAGE07 POST-HOC HINTS (advisory, may be overridden with rationale):
{stage07_hints}

OPTIONAL EXISTING LABELS (avoid reusing exactly):
{existing_labels}

### TASK

Using ONLY the evidence above, produce one JSON object matching the v3 schema.

OUTPUT ORDER:
1. content_type, is_noise, exclude_from_axes
2. sexual_explicitness, sexual_function, consent_status
3. label (2–6 words, scene-visible beat only — picture test; function lives in JSON)
4. scene_summary (one sentence, 12–25 words: who + action + object; no analytic jargon)
5. rationale (1–3 sentences citing snippets first)

Snippets trump Main when they conflict. Classify sexual JSON fields before writing the label.
""".strip()

ROMANCE_AWARE_SYSTEM_PROMPT = SYSTEM_PROMPT
ROMANCE_AWARE_USER_PROMPT = USER_PROMPT_TEMPLATE
