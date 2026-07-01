CHARACTER_NAMES_RULES = """
CHARACTER NAMES IN ROMANCE CORPUS (CRITICAL)

Romance novels always name characters. Proper names are interchangeable placeholders — the specific
name does not define the topic.

ALWAYS:
- IGNORE character first/last names when choosing label, scene_summary, and content_type
- Replace names with role placeholders in scene_summary when needed (he, she, a friend, her rival)
- Label the shared narrative beat from snippets and keywords (KeyBERT/MMR/POS), not the shared name
- When snippets differ, label the dominant visible thread from the strongest snippet + keyword evidence

NEVER:
- Use the label "Character Name Artifact" or any variant ("Name Artifact", "Name References", "Name Cluster")
- Set is_noise true or exclude_from_axes true solely because Main is name-heavy
- Invent a plot that stitches unrelated snippets — but still pick the best-supported single beat
- Put proper names in label or scene_summary

Stage07 character_name_cluster / possible_character_residue flags are ADVISORY ONLY.
Override them when snippets or alternate keyword lists show a coherent theme.

When one snippet is clearly dominant (explicit action, setting, or dialogue type), anchor the label there.
Examples: reunion longing → "Frantic Longing After Separation"; romantic rival talk → "Discussing A Romantic Rival";
horses at a ranch → "Horses At Ranch Property".

Name-heavy Main with thin snippets: prefer a broad but grammatical scene label from the best snippet,
not a meta "artifact" label. Reserve is_noise for publisher boilerplate and true non-narrative garbage only.
""".strip()

CHARACTER_NAMES_FEW_SHOTS = """
Example I — name-heavy Main, coherent snippets (NOT noise):
Main keywords: dylan, alec, seneca | Snippets: all discuss time spent with one man vs a new suitor
→ is_noise: false, content_type: scene
→ label: "Discussing A Romantic Rival"

Example J — stage07 flag overridden by shared setting:
Flag: character_name_cluster | Snippets: all mention horses, stable, rural property
→ is_noise: false, content_type: scene
→ label: "Horses At Ranch Property"
→ rationale cites horses/stable, not the shared character name

Example K — mixed snippets; dominant beat wins:
Snippets: injury on crutches; unrelated joke; explicit longing to reunite sexually
→ is_noise: false, content_type: scene, sexual_function: sexual_tension
→ label: "Frantic Longing After Separation"
→ rationale cites the longing snippet as anchor; do NOT use "Character Name Artifact"
""".strip()
