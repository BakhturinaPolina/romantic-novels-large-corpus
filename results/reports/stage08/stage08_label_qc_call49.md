# Stage08 label QC — placeholder v4 call 49

**Date:** 2026-08-12
**Labels:** `results/stage08_llm_labeling/placeholder_v4_call49/production/labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v3_topic_labeling.json`
**Model / prompt:** `anthropic/claude-sonnet-4.6`, `v3_topic_labeling`
**Verdict:** pass — cleared for Stage09.

## Coverage

| Step | Topics |
|------|--------|
| Stage05 compare-fit | 373 |
| Stage07 hard exclude | 1 (topic 8, publisher boilerplate) |
| Stage08a exclude / manual review | 21 / 2 |
| Routed to labeling | 349 |
| Labeled | **348** |

One routed topic is unlabeled: **topic 149** (261 docs). Its POS representation is empty
(`POS_words = []`), and the labeling pipeline streams topics from the POS representation, so it
was skipped silently before any API call. Its Main representation is entirely function words
(`can, do, course, if, cannot, don, want, know, sure, think`, c_v 0.41), i.e. a discourse residue
topic. Treated as excluded; no re-label attempted.

## Field distributions (call 49 vs call 73)

| Field | call 49 (n=348) | call 73 (n=322) |
|-------|-----------------|-----------------|
| content_type | scene 306 / discourse 32 / subgenre_marker 10 | scene 257 / discourse 56 / subgenre 7 / noise 2 |
| sexual_explicitness | none 307 / suggestive 20 / affection_only 12 / explicit 9 | none 291 / suggestive 17 / affection_only 9 / explicit 5 |
| consent_status | not_applicable 309 / consensual_implied 32 / coercion_watchlist 5 / unclear 2 | 294 / 25 / 2 / 1 |

Call 49 yields more usable sexual-axis signal than call 73: explicit 9 vs 5, suggestive 20 vs 17,
`explicit_contact` 7 vs 2, and a lower discourse share (9.2% vs 17.4%). This matches the
granularity rationale for choosing call 49.

## Quality checks

| Check | Result |
|-------|--------|
| Empty labels / summaries / rationales | 0 |
| Generic placeholder labels ("topic", "misc", "unclear") | 0 |
| Label length | 2–6 words, mean 4.6 |
| Duplicate labels | 1 pair (topics 231, 282 both *Struggling to Surrender Control*) |
| Character-name leakage | 0 (6 lexicon hits are common nouns: doctor, mug, grace, officer, lady, sister) |
| Schema inconsistencies | 5 / 348 (1.4%) |
| Snippet-faithfulness spot check (16 topics, stratified by size) | all labels and summaries supported by snippets |

### Schema inconsistencies

| Topic | Label | explicitness / function / consent |
|-------|-------|-----------------------------------|
| 11 | Eyes Meeting Across The Room | affection_only / sexual_tension / not_applicable |
| 78 | Swearing War Before He Takes Her | none / consent_boundary / coercion_watchlist |
| 82 | Touch Her and Your Family Suffers | none / consent_boundary / coercion_watchlist |
| 98 | Stepping Out of The Shower | suggestive / presex_escalation / not_applicable |
| 139 | Admiring Her Grace and Beauty | none / sexual_tension / not_applicable |

Each is individually defensible from its rationale (gaze charge without contact; verbal coercion
without sexual content; towel scene with no named consent partner). They are left as produced.

### Other observations

- Topic 368 (*Lips Curving Into A Smile*) has one mojibake snippet (`в corner of sevinгўв‚¬в„ўs mouth`)
  — a corpus encoding artifact, not a labeling error; label is correct.
- Small topics (~100–250 docs) get labels anchored on 3 snippets, so some are narrower than the
  underlying cluster (e.g. topic 367 *Sorting Out Concert Tickets*). Same behaviour as call 73.

## Downstream finding (Stage09)

A 20-topic Stage09 diagnostic run (`taxonomy_mappings_diag20.json`, taxonomy v2.4) shows the
`consent_status = coercion_watchlist` heuristic forcing `main = 7.4` (*Unwanted or Coercive Sexual
Contact*) regardless of sexual context, overriding the LLM:

| Topic | LLM main | Forced main | Stage08 explicitness |
|-------|----------|-------------|----------------------|
| 78 | 4.7 (possessive conflict) | 7.4 | none |
| 82 | 7.2 (non-sexual coercion) | 7.4 (secondary also 7.4) | none |
| 117 | — | 7.4 | none |
| 199 | 7.4 | 7.4 (correct) | explicit |
| 294 | — | 7.4 | none |

Both 7.4 and 7.2 feed `coercion_risk_watchlist` (weights 1.0 / 0.8), so axis totals shift only
slightly, but the leaf assignment reads non-sexual threats as sexual coercion, and topic 82 gets
`secondary == main`. Affects 5 of 348 topics in call 49 (2 of 322 in call 73).

**Fix applied** in `stage1_theory_driven_categories/taxonomy_v2.py`: `_has_sexual_context()` gates
the coercion override, so `coercion_watchlist` routes to 7.4 only when the topic is sexual
(explicitness explicit/suggestive, a sexual `sexual_function`, or sexual-contact vocabulary) and to
7.2 otherwise; `secondary` is cleared when it equals the new main. Covered by three cases in
`tests/stage09/test_taxonomy_v2_intimacy.py`. All 5 affected topics have ids > 27, so they are
mapped with the fix in place on the first pass.
