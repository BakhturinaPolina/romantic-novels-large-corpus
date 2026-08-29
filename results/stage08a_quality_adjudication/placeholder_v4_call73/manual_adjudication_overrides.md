# Stage 08A manual adjudication overrides (call 73)

Prompt: `v2_snippets_first_ignore_names` · Updated: 2026-06-30

Human overrides applied after LLM v2 adjudication. Evidence policy: snippets → KeyBERT → MMR → POS → combined keywords → Main (names ignored).

| Topic | Docs | Prior LLM | Round | Proposed label hint | Rationale |
|------:|-----:|-----------|-------|---------------------|-----------|
| 113 | 286 | exclude_noise | v2 audit (first batch) | assumptions / expectations | Manual override after v2 audit: snippets share 'assume'; KeyBERT/MMR/POS show assumption and emotional context (distraction, disappointment, happiness, painful). Main name tokens ignored per policy. |
| 240 | 143 | manual_review_needed | manual-review queue | age / life-stage | Manual override: age/life-stage theme supported by snippets (twelve years old, victoria's age, aging woman) and Main keywords; alt-rep noise discounted. |
| 260 | 131 | exclude_noise | exclude list second pass | secrecy / risk of being seen | Manual override: snippet 3 ('if he catches one glimpse of you, he'll know') plus MMR/POS (privacy, glimpse, upset, pressure, wound) support secrecy / risk-of-being-seen; Jared and other Main names ignored per v2 policy. |
| 302 | 114 | manual_review_needed | manual-review queue | hesitation / social caution | Manual override: hesitation/social dynamics in snippets and KeyBERT/MMR/POS (hesitate, council, member, exchange); character names in Main ignored per policy. |
| 307 | 112 | exclude_noise | v2 audit (first batch) | acquaintance / introduction | Manual override after v2 audit: thin but labelable acquaintance/introduction theme (terrified, introduced, recently, admitted) supported by snippets about knowing someone. |
| 308 | 112 | exclude_noise | exclude list second pass | hidden identity / supernatural or group secret | Manual override: snippet 2 ('doesn't discover what we are') plus alt reps (pretending, embarrassed, horrified, tearing) support hidden identity / group secret; Rory and other Main names ignored per v2 policy. |
| 313 | 110 | manual_review_needed | manual-review queue | interpersonal pressure / social conflict | Manual override: snippets and KeyBERT/MMR/POS cohere on interpersonal pressure, backing off, and meeting for a meal; religious Main tokens (corinthians, apostle) discounted as misleading high-frequency residue. |
| 316 | 109 | exclude_noise | v2 audit (first batch) | rodeo / bull riding | Manual override after v2 audit: snippet 3 describes bull-riding/rodeo (chute, bull); MMR includes charged/climbed. Theme is interpretable despite name-heavy Main. |

## Counts after overrides

- **pass_to_labeling:** 148
- **exclude_noise:** 20
- **manual_review_needed:** 0
- **manual overrides:** 8
