# Provisional notes: taxonomy & labeling after call_59 (294 topics)

**Status:** Working memo for future Stage 08 / Stage 09 iteration — **not** the final topic list or frozen taxonomy.  
**Date:** 2026-06-18  
**Trigger:** Manual review of `stratified_minilm12v2_seed42_v2/final_compare/call_59/topic_info.csv` (294 non-outlier topics) against pilot/pretest design, Stage 11 macro-axes, and current Stage 08–09 schemas.

**Related artifacts**

| Artifact | Path / note |
|----------|-------------|
| Provisional topic model | `results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/` |
| Pretest corpus | 100 billionaire-romance novels (external project; logs not in repo) |
| Pilot analysis corpus | ~368 topics on `paraphrase-MiniLM-L6-v2` (SCIENTIFIC_README, notebooks) |
| Stage 09 taxonomy (frozen in code) | `src/stage09_category_mapping/stage1_theory_driven_categories/scripts/zeroshot_taxonomy_openrouter.py` → `TAXONOMY_NODES` |
| Stage 08 labeling prompts | `src/stage08_llm_labeling/openrouter_experiments/core/generate_labels_openrouter.py` |
| Macro-axis schema | `configs/stage09/theory_aligned_index_schema.yaml`, `results/reports/stage11/stage11_power_analysis_report.md` |
| Theory notebook structure | `notebooks/07_analysis/topic_analysis_all_STRUCTURE.md` |

---

## 1. What call_59 looks like (vs pretest expectations)

| Metric | call_59 (`all-MiniLM-L12-v2`) | Pretest (100 billionaire novels) | Large-corpus implication |
|--------|-------------------------------|----------------------------------|---------------------------|
| Non-outlier topics | 294 | ~fewer, more homogeneous themes | Fine-grained micro-clusters |
| Outlier rate | **70.9%** | not reported here | Most sentences land in `-1`; assigned topics are a selective slice |
| Assigned docs (excl. −1) | 125,772 | small pilot | Heterogeneous multi-genre mix |
| Fit docs | 432,319 / 500k cap | ~100 books | Scale changes cluster semantics |
| Coherence C_V | 0.583 (eval) | pretest best ~0.463 (mpnet) | Higher coherence, still high diversity (0.89) |
| Genre mix | paranormal, historical, YA, mystery, other (16k v3 corpus) | billionaire subgenre only | Status/wealth signals diluted |

**Size distribution (294 topics):**

| Tier | Topics | Share of topics |
|------|--------|-----------------|
| ≥2,000 docs | 8 | 3% |
| 500–1,999 | 37 | 13% |
| 200–499 | 123 | 42% |
| &lt;200 docs | 126 | **43%** |

126 small topics hold ~15% of assigned mass — many are unstable for confirmatory axis aggregation unless prevalence-filtered first (cf. `topic_analysis_all_STRUCTURE.md` §0.6).

**Largest topics (sanity check):**

| Topic | Count | Auto-name signal | Interpretation |
|-------|------:|------------------|----------------|
| 0 | 10,066 | `sa du ha ne yo…` | Multilingual / OCR / encoding artifact (~8% of assigned docs) |
| 1 | 6,451 | cupped, caressed, licking, erection | Explicit physical intimacy |
| 2 | 6,216 | elevator, parked, stormed, ignition | Movement / transit / chase |
| 3 | 3,494 | despised, rejection, hated | Love–hate emotional conflict |
| 4 | 2,774 | phones, texted, buzzed | Communication technology |
| 8 | 1,773 | breathlessly, hoarsely, mumbled | **Dialogue-delivery adverbs** (not a scene type) |

---

## 2. Full 294-topic landscape (heuristic pass)

Automated keyword heuristics over `Representation` + snippet text — **provisional buckets only**, for gap-finding (not for publication).

| Heuristic bucket | Topics | Doc mass | % assigned docs | Maps to current taxonomy? |
|------------------|-------:|---------:|------------------:|---------------------------|
| Speech acts / future tense (`I'll`, `mustn`, `dont`) | 51 | 13,888 | 11.0% | **Poorly** — forced into 3.x / 4.x |
| Dialogue delivery adverbs (mumbled, hoarsely, retorted) | 28 | 10,949 | 8.7% | **Poorly** — no Group 9 |
| Multilingual / encoding fragments | 17 | 12,958 | 10.3% | Should be `noise`; often mislabeled |
| Unclassified micro-clusters | 56 | 15,779 | 12.5% | High LLM mapping variance |
| Movement / transit / vehicles | 7 | 7,693 | 6.1% | Partial 8.2 / 8.3 |
| Physical intimacy (non-explicit keyword hit) | 4 | 8,820 | 7.0% | 2.1–2.2 (but topic 1 alone is 6.4k) |
| Negative emotion / conflict | 10 | 6,303 | 5.0% | 3.2 / 4.4 |
| Work / money / housing | 15 | 5,897 | 4.7% | 6.x (6.1 billionaire-biased name) |
| Gaze / appearance | 17 | 6,009 | 4.8% | 1.1 + 2.1 |
| Paranormal subgenre | 4 | 1,510 | 1.2% | **No dedicated node** → scattered in 7.3 |
| Explicit erotic (strict keyword hit) | 4 | 557 | 0.4% | 2.3 (under-segmented vs pilot) |
| Publisher / paratext boilerplate | 2 | 1,199 | 1.0% | `noise` (under-used in practice) |

**Combined style / discourse / noise buckets ≈ 59% of topics** (172/294 by broad rule). The current 8-group taxonomy assumes **scene-level romance content**; call_59 frequently clusters **how things are said** rather than **what happens**.

---

## 3. Three-way comparison: pretest → pilot taxonomy → call_59 reality

### 3.1 Pretest (100 billionaire novels)

Evidence in repo ([`stage03_bertopic_search_space_prior.md`](../stage03/stage03_bertopic_search_space_prior.md), SCIENTIFIC_README):

- Embedding shortlist and HDBSCAN priors tuned on **homogeneous billionaire subgenre**.
- Pareto winner emphasized **coherence**; taxonomy and hypotheses built around **status/dominance** as backbone (`AX_status_dominance` = 6.1 + 6.4).
- Pilot power analysis ([`stage11_power_analysis_report.md`](../stage11/stage11_power_analysis_report.md)) confirms status/dominance predicts **reach**, not quality — sensible for billionaire pilot, but **6.1 category naming and examples remain CEO/billionaire-centric** in Stage 09 code.

### 3.2 Pilot labeling & mapping (~368 topics, MiniLM-L6-v2)

From SCIENTIFIC_README / notebooks:

- 8 taxonomy groups, ~30 leaf nodes + `noise`.
- 272 topics → Radway; 96 background/contextual.
- Macro-axes (`theory_aligned_index_schema.yaml`) anchor on taxonomy IDs: 4.5, 3.1, 2.3, 2.1, 3.2, 6.1, 6.4, 7.2.
- Discriminative findings emphasize **psychological credibility**, **embodied intimacy**, and trash-associated **explicit sex + procedural scenes** — aligned with scene-level taxonomy.

### 3.3 call_59 on 16k multi-genre corpus

**Convergences with pilot design**

| Pilot theme | call_59 signal | Taxonomy home |
|-------------|----------------|---------------|
| Payoff / safety / repair | cherish, gratitude, commitment dialogue | 4.5, 3.1 |
| Negative affect | rejection, resentment, loneliness | 3.2, 4.4 |
| Attraction / chemistry | gaze, smirk, tension beats | 2.1, 1.1 |
| Explicitness (quality-negative) | topic 1 + scattered explicit clusters | 2.3 |
| Protective caretaking | medical, healing, reassurance topics | 6.5, 3.1, 4.2 |
| Drama / obstacle | secrets, choices, conflict | 4.3, 4.4 |

**Divergences (new corpus exposes gaps)**

| Gap | Evidence in call_59 | Risk if unaddressed |
|-----|---------------------|---------------------|
| **Discourse/style clusters dominate** | Topics 8, 20, 183; ~20% doc mass in adverbs / speech acts | Inflates 3.x and 4.x; weakens macro-axis interpretability |
| **Multilingual & paratext** | Topic 0 (10k docs); topic 21-style publisher blocks | Pollutes attraction / status axes |
| **Subgenre markers** | Werewolves, medieval combat, mystery suspense | Forced into 7.x or misfit 6.x |
| **Procedural / transition scenes** | Elevators, phones, meals, weather | Valid narrative glue but not theory targets |
| **Status/wealth under-represented in topic mass** | Only ~7% doc-weighted heuristic hit vs pilot centrality | `AX_status_dominance` may be **sparse at topic level** even if sentence-level signal exists in outliers |
| **Explicit sex fragmented** | One giant intimacy topic + few small explicit clusters | `AX_love_over_sex` denominator unstable if 2.3 mapping inconsistent |

---

## 4. Macro-axis ↔ taxonomy alignment stress test

From `configs/stage09/theory_aligned_index_schema.yaml` and [`stage11_power_analysis_report.md`](../stage11/stage11_power_analysis_report.md):

| Macro-axis | Taxonomy anchors | call_59 stress |
|------------|-------------------|----------------|
| `AX_payoff_safety` | 4.5, 3.1 | OK if repair topics not tagged as dialogue-noise |
| `AX_love_over_sex` | num 4.5+3.1 / den 2.3 | Denominator small; numerator contaminated by speech-act topics |
| `AX_attraction` | 2.1 | Gaze topics OK; needs exclusion of smirk/wink **pure style** topics |
| `AX_dysregulated_negative_affect` | 3.2 | Sigh/breakdown topics OK; worry topics may need 3.2 vs 3.3 split |
| `AX_status_dominance` | 6.1, 6.4 | **Under-powered for quality** (Stage 11) — do not over-fit taxonomy to billionaire hero work |
| `AX_external_obstacle` | 7.2 | Paranormal action often misclassified as 7.2 vs subgenre |

**Recommendation:** treat macro-axes as **aggregation layer over mapped leaf categories**, not as direct BERTopic topic names. Add an explicit **`exclude_from_axes`** flag in Stage 08/09 for discourse, noise, and procedural clusters.

---

## 5. Stage 08 (`llm_labeling`) — proposed improvements

### 5.1 Extend `primary_categories` (prompt + JSON schema)

Current set (`generate_labels_openrouter.py`) is romance-scene oriented. Add:

| New primary tag | When to use | Purpose |
|-----------------|-------------|---------|
| `narrative_style` | Top keywords are adverbs of saying, dialogue tags, tense/aspect particles | Keep out of 4.x / 3.x in Stage 09 |
| `procedural_transition` | Movement between spaces, object handling, meals, weather without relational beat | Map to 8.x without pretending it is conflict |
| `subgenre_paranormal` | Shifters, magic, immortal beings | Route to new Stage 09 nodes |
| `subgenre_historical` | Regency/medieval markers | Same |
| `subgenre_suspense` | Investigation, threat, crime procedural | Distinct from 4.4 couple conflict |
| `multilingual_artifact` | Non-English fragments, encoding garbage | Force `is_noise: true` |
| `communication_medium` | Phones, texting, email as **medium**, not plot | Finer 8.3 use |

Keep existing tags; document that **`romance_core` must not be applied to pure dialogue-delivery topics**.

### 5.2 Split label vs register in output schema (optional v2 JSON)

Consider adding:

```json
{
  "content_type": "scene | discourse | paratext | subgenre_marker",
  "register": "explicit | suggestive | neutral",
  "subgenre_hints": ["paranormal", "historical"]
}
```

This gives Stage 09 deterministic pre-routing before LLM taxonomy mapping.

### 5.3 Prompt `is_noise` rules (prompt hardening)

Auto-flag when **any** of:

- Publisher / copyright / TOC / chapter-list keywords in top-10 words or snippets.
- Top keywords are predominantly 2-letter tokens or non-English function words (topic 0 pattern).
- ≥60% of top keywords are dialogue adverbs (`*ly` speech tags) **without** scene nouns.
- Representative docs are >50% identical boilerplate across books.

Cross-reference: Stage 09 already respects Stage 08 `is_noise` — **noise detection belongs primarily in Stage 08**.

### 5.4 Corpus context block in user prompt

Add static corpus descriptor to Stage 08 system prompt (one paragraph):

> Multi-genre English romance 2000–2017: contemporary, paranormal, historical, YA, mystery; **not** billionaire-only.

Reduces default CEO/boardroom labels inherited from pretest examples in few-shots.

### 5.5 Script changes (implementation backlog)

| File | Change |
|------|--------|
| `generate_labels_openrouter.py` | Update `ROMANCE_AWARE_SYSTEM_PROMPT` categories + noise rules above |
| `generate_labels.py` | Keep local/HF path in sync if still used |
| `validate_label_quality.py` | Add checks: `% narrative_style`, duplicate labels, billionaire-label rate on non-6.x topics |
| `inspect_random_topics.py` | Stratified inspect by doc count tier and heuristic bucket |
| New util (optional) | `preclassify_topics.py`: rule-based `content_type` before LLM call (saves API cost) |

---

## 6. Stage 09 (`category_mapping`) — proposed taxonomy revisions

### 6.1 Add Group 9 — Narrative style & discourse (new)

| ID | Name | Description |
|----|------|-------------|
| 9.1 | Dialogue delivery & speech tags | Adverbs of saying, volume, tone (`mumbled`, `hoarsely`) |
| 9.2 | Future-tense commitment / promise speech acts | `I'll`, `we'll`, vows, threats of leaving |
| 9.3 | Humor register | chuckles, snorts, banter tone without event |
| 9.4 | Interior monologue particles | Hesitation, filler (`uh`, `hm`), rhetorical self-talk |

**Aggregation rule:** exclude 9.x from all macro-axes in `theory_aligned_index_schema.yaml`.

### 6.2 Add Group 10 — Subgenre & plot engine (new)

| ID | Name | Description |
|----|------|-------------|
| 10.1 | Paranormal / immortal beings | Shifters, vampires, magic systems |
| 10.2 | Historical / period setting | Regency, medieval, titled nobility |
| 10.3 | Mystery / suspense / investigation | Detectives, clues, procedural danger |
| 10.4 | Action / weaponized conflict | Gunfights, combat set-pieces (non-couple) |

Distinguishes **genre furniture** from **couple conflict** (4.4) and **institutional** scenes (6.5).

### 6.3 Refine existing nodes (rename / split, no ID churn if possible)

| Current ID | Issue | Proposed adjustment |
|------------|-------|---------------------|
| 6.1 Hero's elite work | Billionaire-pretest naming | Rename → **"High-status / elite profession & business"**; add non-CEO examples (surgeon, royalty, athlete) |
| 1.1 Body reactions | Misses scent clusters (topic 19) | Add smell/taste to description or add **1.3 Sensory atmosphere (scent, sound, texture)** |
| 3.2 Negative emotions | Absorbs worry + acute grief | Split optional **3.5 Rumination / worry** for anxiety topics vs breakdown/screaming |
| 8.2 Public & leisure | Absorbs chase/transit | Split **8.5 Movement & transit** (vehicles, elevators, stalking through halls) |
| 8.3 Objects & technology | Phones overlap | Clarify: communication **medium** vs **plot event** (use Stage 08 `communication_medium`) |
| `noise` | Under-assigned | Expand description; allow multi-label `noise` + secondary 9.x |

### 6.4 Heuristic & routing script updates

| File | Change |
|------|--------|
| `zeroshot_taxonomy_openrouter.py` | Extend `TAXONOMY_NODES`; add pre-router on Stage 08 `content_type` / `primary_categories` |
| `apply_domain_heuristics()` | Add: if `narrative_style` → main 9.x; if `multilingual_artifact` → noise; if `subgenre_*` → 10.x |
| `zeroshot_radway_openrouter.py` | Radway Phases I–III **exclude** 9.x and `noise` from romance-core overrides |
| `aggregate_taxonomy_by_book.py` | Support `exclude_from_axes` category list; min topic mass threshold (e.g. 200 docs or prevalence ε) |
| `theory_aligned_index_schema.yaml` | Document exclusions; consider **sentence-level fallback** for sparse 6.1 topics |

### 6.5 Stage 1 before Stage 2 (process note)

With 294 micro-topics, zero-shot mapping is expensive and noisy. Recommended pipeline:

1. **Stage 1:** hierarchical reduction → 40–80 meta-topics (`stage1_natural_clusters/`).
2. **Stage 08:** label meta-topics + representative micro-topic exemplars.
3. **Stage 09:** map meta-topics to theory taxonomy; propagate to micro-topics with inheritance + spot checks on high-mass outliers.

---

## 7. Pretest vs large-corpus: what to keep vs revise

| Element | Keep | Revise |
|---------|------|--------|
| 8-group romance theory skeleton | ✅ | Add Groups 9–10 for discourse & subgenre |
| Radway 13-function overlay | ✅ | Exclude non-scene topics first |
| Stage 08 snippet-first labeling | ✅ | Stronger noise + style detection |
| Billionaire-flavored 6.1 examples in prompts | ❌ | Generalize to elite/status professions |
| Pretest HDBSCAN / embedding priors | ✅ as BO prior | Already widened in Stage 03 |
| `AX_status_dominance` as quality predictor | ❌ (Stage 11) | Keep as **reach** axis only |
| Topic-count guards (`n_topics ≥ 20`) | ✅ | Add **max micro-topic prevalence audit** post-fit |
| Single-pass 294-topic LLM mapping | ❌ | Hierarchical + rule pre-router |

---

## 8. Suggested validation before locking taxonomy v2

1. **Manual audit:** 30 topics stratified by size tier + heuristic bucket (see prior 50-topic review pattern).
2. **Inter-rater spot check:** 20 topics × 2 human coders vs Mistral-Nemo taxonomy mapping.
3. **Axis sensitivity:** Recompute book-level `AX_payoff_safety`, `AX_love_over_sex` with vs without 9.x topics excluded.
4. **Genre stratification:** Compare taxonomy proportions in paranormal vs historical vs contemporary subsamples (metadata `genre_group`).
5. **Pretest replay:** Map call_59 topics that **would** appear in billionaire-only corpus vs rest — quantify label drift.

---

## 9. Open questions (defer to next iteration)

- Should **topic 0** be dropped at model level (re-fit with stronger `min_df` / language filter) vs handled only in labeling?
- Is **70% outlier rate** acceptable for sentence-level axes, or do we need outlier-reduction pass (`outliers_reduced/` pattern from v3 runs)?
- Align embedding model for labeling (`MiniLM-L12-v2` winner) with Stage 08 model paths still pointing at `paraphrase-MiniLM-L6-v2` defaults in READMEs.
- Version **`TAXONOMY_NODES`** in a JSON config file (not only Python constant) for reproducibility and prompt injection.

---

## 10. Immediate action checklist (when revisiting Stage 08–09)

- [ ] Add `content_type` + extended `primary_categories` to Stage 08 prompt/schema
- [ ] Draft `TAXONOMY_NODES` v2 with Groups 9–10 in JSON under `configs/`
- [ ] Implement pre-router in `zeroshot_taxonomy_openrouter.py` before OpenRouter call
- [ ] Update `theory_aligned_index_schema.yaml` with `exclude_categories: [9.1, 9.2, …, noise]`
- [ ] Run Stage 08 on call_59 `topic_info.csv` subset (pilot n=50) before full 294-topic spend
- [ ] Compare axis stability vs pilot 368-topic mappings

---

## 11. Addendum: taxonomy v2.3 axis/context split (2026-07-01)

Pilot review on call73 (`taxonomy_mappings_v22_pilot30.json`) confirmed **4.2 inflation** and **sexual-tension → appearance** heuristic bugs. v2.3 introduces:

- `axis_bearing_ids` allowlist for Stage10 only
- `uncertain_interpretable` fallback (replaces default 4.2)
- Split **8.3a/8.3b**, **5.3a/5.3b**
- `axis_hint=no_hypothesis_signal` for `sexual_function=none`

See **[taxonomy_v23_axis_context_design.md](../stage09/taxonomy_v23_axis_context_design.md)**.

---

*This memo compares a **provisional** 294-topic BERTopic fit to theory developed on a billionaire pretest and a ~368-topic pilot. Final topic inventory will come from Stage 04–05 winner selection and may differ from call_59.*
