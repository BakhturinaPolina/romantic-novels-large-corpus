# Stoplist cleaning + honest topic representations (2026-08-11)

## What was done

1. **Full stoplist audit** (`src/stage02_preprocessing/scripts/audit_stoplist_non_names.py`,
   full list vs empty backup, `--zipf-threshold 3.5`): 8,270 of 72,745 tokens are real
   English words, including core vocabulary (`just`, `time`, `know`, `said`, `love`,
   `kiss`, `wedding`, `money`, `kill`). Audit CSV: `data/processed/stoplist_non_name_audit_20260811_220306.csv`.
2. **Cleaning** (`src/stage02_preprocessing/scripts/clean_stoplist_common_words.py`):
   - Remove if zipf ≥ 5.0 (hyper-common), or zipf ≥ 3.5 **and** lowercase-usage share ≥ 0.5
     in a 3M-sentence case-preserving sample of `sentences_train.csv` (sentence-initial
     tokens excluded from case stats).
   - Names are protected by capitalized usage: kept `jack` (lc share 0.02), `grace` (0.27),
     `daisy`, `peter`, `smith`; also title-names `duke`, `prince`, `queen`, `daddy`, `angel`.
   - Freed vocabulary: `love`, `kiss`, `wedding`, `marry`, `money`, `husband`, `wife`,
     `cock`, `gun`, `danger`, `doctor`, `boss`, `vampire`, `wolf`, `dad`, `alpha`, …
   - Result: **72,745 → 66,740 lines (−6,005)**. Backup:
     `data/processed/custom_stoplist.txt.bak_20260811_220719`. Report:
     `data/processed/stoplist_cleaning_report_20260811_220653.csv`.
3. **Representation recompute** (`src/stage05_final_fit/scripts/recompute_topic_representations.py`
   via `scripts/stage05/recompute_repr_stoplist_v2.sh`): Phase 2 compare-fit saved no model
   artifacts, so each shortlist candidate was refit once with its original median export
   seed (stoplist only affects the c-TF-IDF/KeyBERT layer, not UMAP/HDBSCAN clustering).
   Outputs in `final_compare/call_N/repr_stoplist_v2/`; original exports untouched.

## Honest metrics vs original (same clustering)

| model | n_topics (new/orig) | c_v honest | c_v orig | diversity honest | diversity orig |
|---|---|---|---|---|---|
| L6_16 | 86 / 86 | **0.526** | 0.703 | 0.715 | 0.259 |
| MPNet_131 | 94 / 87 | **0.533** | 0.700 | 0.719 | 0.306 |
| MPNet_133 | 171 / 171 | **0.600** | 0.676 | 0.686 | 0.652 |
| L12_73 | 330 / 329 | **0.639** | 0.657 | **0.927** | 0.669 |

Clustering reproduced exactly for L6_16 / MPNet_133 / L12_73 (±1 topic); MPNet_131
drifted 87→94 (same cuML seed nondeterminism seen in Phase 2 itself).

**Key finding: the contaminated stoplist inflated coherence of the coarse models.**
Honest c_v *increases* with granularity — the ranking inverts. The coarse models'
apparent 0.70 coherence came from rare-word residue, not interpretable topics.

## Hypothesis-axis coverage (topics with ≥2 bucket words in top-10, honest keywords)

| bucket | L6_16 | MPNet_131 | MPNet_133 | L12_73 |
|---|---|---|---|---|
| explicit_sex (2.3) | 1 | 3 | 2 | 3 |
| commit_HEA (4.5) | 2 | 1 | 1 | 3 |
| protective_care (4.6) | 1 | 1 | 1 | 1 |
| possessive_jealousy (4.7) | 0 | 0 | 0 | **1** (T246 `jealous…`; +belong-topics) |
| wealth_luxury (6.x) | ≤1 | ≤1 | 2 | **6** (money/finance, hotel, private jet ×2) |
| danger_dark (7.x) | 2 | 1 | 2 | 1 |
| conflict_negemo (3.x) | 3 | 3 | 2 | 4 |
| family_children | 3 | 3 | 3 | 4 |
| paranormal | 1 | 2 | 1 | 2 (incl. `wolf, pack, alpha, shifting`) |
| profession | 1 | 0 | 1 | 2 |

Example contrast (MPNet_133 T16): before `engaged, buying, example, notion, appointment,
arranged, ya, apparent` → after `marry, married, wedding, marriage, baby, wife, family, engaged`.

## Extension: high-topic-count stable candidates (2026-08-12)

Same recompute applied to the three remaining high-n stable Pareto models.
Clustering reproduced within ±2 topics in every case.

| model | n_topics | c_v honest | c_v orig | div honest | outlier | flagged | usable topics |
|---|---|---|---|---|---|---|---|
| MPNet_38 | 446 | 0.581 | 0.542 | 0.937 | 0.730 | 72% | 126 |
| L12_11 | 388 | 0.556 | 0.516 | 0.869 | 0.719 | 55% | 174 |
| L12_49 | 373 | **0.635** | 0.654 | 0.809 | 0.693 | **43%** | **212** |
| L12_73 | 330 | **0.639** | 0.657 | 0.927 | 0.705 | 48% | 170 |
| MPNet_133 | 171 | 0.600 | 0.676 | 0.686 | 0.770 | 19% | 138 |

For the two largest models honest c_v is *higher* than the contaminated value
(+0.04), the opposite of the coarse models (−0.17): the stoplist had been
suppressing exactly the vocabulary these fine topics are built on.

Rare-axis coverage (≥1 keyword in top-10) — the axes H3/H4 depend on:

| model | jealousy/possessiveness (4.7) | wealth/luxury (6.x) |
|---|---|---|
| MPNet_38 | 1 (`envy, jealous, jealousy`) | 3 (`designer`, `jet`, `billionaire`) |
| L12_11 | 1 (`envy, jealous, jealousy`) | 5 (`diamond`, `yacht`, `fortune`, `jet`) |
| **L12_49** | **7** (`claiming` ×2, `possession`, `jealous`, …) | 4 (`designer`, `jet`, `rich`, `expensive`) |
| L12_73 | 2 (`jealous`, `possession`) | 3 (`jet` ×2, `rich`) |
| MPNet_133 | 0 | 1 (`expensive`) |

**Revised recommendation: L12 call 49 (373 topics).** Best combination of honest
coherence (0.635, tied with L12_73), the most axis-bearing topics for 4.7/6.x,
the lowest tiny-topic overhead of the high-n group (43% flagged, 212 usable
topics vs L12_73's 170), no topics under 100 docs, and tighter refit stability
(std 3.6 vs 7.1). MPNet_38 buys 73 more topics at the cost of 319 tiny topics.

## Implications for the production-model decision

- Only **L12_73 (330 topics)** populates the rare axes H3/H4 depend on
  (wealth/luxury 6.x, possessiveness 4.7). MPNet_133 (171) partially covers 6.x, none of 4.7.
- With honest keywords L12_73 also has the best coherence (0.639) and diversity (0.927),
  removing the main argument for the coarse models.
- Caveat: Stage03 BO optimized coherence under the contaminated stoplist, so all Phase 1
  c_v values (and the BO objective itself) were inflated; relative comparisons *within*
  an embedding remain informative, but the honest recompute above is the number to trust.
- Any Stage05+ production fit must use the cleaned stoplist
  (`custom_stoplist.txt`, sha256 prefix `4f5304203a09de2d`, 66,740 lines).
