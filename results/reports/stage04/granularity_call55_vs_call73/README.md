# What granular topics add to hypothesis testing — call 73 (329) vs call 55 (117)

**Date:** 2026-08-11
**Question:** does the granular fit buy anything for H1–H6 (`SCIENTIFIC_README.md`) that the ~100-topic fit does not?

Both fits are `all-MiniLM-L12-v2` compare-fits over the **same 432,145-sentence** stratified fit sample in the same order, so everything below is computed on **document-level assignments**, not keyword overlap.

| | call 55 | call 73 |
|---|---|---|
| Topics | 117 | 329 |
| Coherence c_v | **0.694** | 0.657 |
| Topic diversity | 0.285 | **0.669** |
| Docs assigned (not `-1`) | 27.8% | 29.5% |
| Usable topics (≥200 docs, not name/boilerplate flagged) | 116 | **161** |
| Docs inside usable topics | **27.3%** | 23.3% |
| Tiny topics (<200 docs) | 0 | 159 (22,766 docs) |

Caveat on the usable counts: Stage07 flagged **0** name-contaminated topics for call 55 but **28** for call 73, because the two runs used different rule versions. A manual audit of the call 55 representations finds ~20 topics that are generic-function-word or character-name clusters (`79_michael_mike`, `83_adam_eve_penn`, `47_jake_logan_zach`, `8_want_do_you_can`, `113_wrong_right_re_guess`, …). The honest comparison is closer to **~96 vs 161 usable axes**, not 117 vs 329.

## 1. The two fits are not nested

| Document state | Share |
|---|---|
| Outlier in both | 63.7% |
| Outlier in call 55, assigned by call 73 | **8.4%** |
| Outlier in call 73, assigned by call 55 | 6.7% |
| Assigned in both | 21.1% |

**32 of the 161 usable granular topics take ≥50% of their documents from the coarse model's outlier pool** — content the 117-topic fit has no topic for at all.

## 2. Where the granular fit refines vs where it adds

Median dominant-parent share is ~0.9: each granular topic sits *inside* one coarse topic. **No coarse topic hosts two opposing hypothesis axes at the dominant-parent level.** So granularity is not fixing axis-confused coarse topics; it is doing two other things.

**(a) Sub-scene splits that change axis assignment**

| Coarse topic | Granular children | Why it matters |
|---|---|---|
| `17_marry_wedding_married_marriage` | *Agreeing to Marry Again* (1000) / *Planning The Wedding Reception* (254) / *Engagement Ring As A Bargaining Chip* (285) | `AX_hea_index` should load the commitment act, not reception logistics — and a bargaining-chip ring is arguably anti-HEA |
| `22_gun_knife_sword_pistol` | *Knife Threat and Blade Training* (330) / *Rifle Pointed at The Captive* (269) | training scenes should not load `AX_dark_vs_tender`; the captive scene is `coercion_watchlist` |
| `21_kill_safe_protect_killed` | *Promising to Keep Her Safe* (1001) | separates the protective promise from the violence that frames it (H4) |
| `2_her_his_kissed_kiss`, `6_my_kiss_me_his` | *Soft Kiss Turning Urgent* (5632, `presex_escalation`) / *Hand Raised to Caress Her Cheek* (288, `affection_only`) | H1 needs `affection_only` separated from escalation; the coarse fit merges them |
| `106_touch_touching_touched_me` | *Touch Her and I'll Break Your* (400, `coercion_watchlist`) | possessive threat pulled out of a neutral touch topic |

**(b) Whole scene types recovered from the coarse outlier pool** — hypothesis-relevant, and absent from call 55 entirely:

| Granular topic | Size | Axis relevance |
|---|---|---|
| *Pounded Into The Plush Mattress* | 272 | H1, `explicit` |
| *Fumbling With Zippers and Buttons* | 383 | H1, `presex_escalation` |
| *Leaning in For A Hug* | 266 | H1/H5, `affection_only` |
| *Promising to Stop When Asked* | 246 | consent negotiation |
| *Offering to Buy Condoms* | 247 | H1, `suggestive` |
| *Reassuring Squeeze on The Shoulder* | 251 | H4 protective care |
| *Claiming You As Mine* | 248 | H4 possessiveness |
| *Blaming You For What Follows* | 331 | `coercion_watchlist` |
| *Threatening to Ruin Your Name* | 253 | H5 |
| *Defending A Man's Worth* | 332 | H4 protective care |

## 3. Axis coverage of the granular fit

54 of 161 usable granular topics carry a hypothesis-relevant Stage08 label; 13 of those came from the coarse outlier pool.

| Axis bucket | Topics | Docs | New from c55 outliers |
|---|---|---|---|
| H4 protective care | 20 | 9,994 | 5 |
| H5 dark / threat | 14 | 5,852 | 3 |
| H6 conflict / repair | 11 | 6,340 | 1 |
| H2 HEA / commitment | 9 | 4,288 | 1 |
| H1 kiss / affection | 4 | 6,404 | 1 |
| consent negotiation | 3 | 1,107 | 1 |
| H1 presex escalation | 3 | 1,068 | 2 |
| H1 explicit sex | 2 | 710 | 1 |
| H4 possessive / jealous | 2 | 628 | 1 |

**H4 is the clearest win** (20 protective-care topics vs 2 possessive — a contrast the coarse fit cannot draw at all). **Consent/coercion becomes measurable only at this resolution**, which is what `AX_coercion_risk_watchlist` (7.4+7.2) depends on.

Direct lexicon matching on top words + representative docs (same inputs for both models, so it is a fair but low-power test) gives: explicit sex 0→2, tenderness 2→5, conflict/repair 3→5, dark/threat 4→5, kiss 5→4, HEA 5→4. Luxury/status and possessiveness score 0 in **both** — H3 and the possessiveness half of H4 are under-served regardless of granularity.

## 4. The costs

- **Coverage drops**: 23.3% of the fit sample lands in a usable granular topic vs 27.3% coarse. Book-level mixtures analyze less text.
- **69.1%** of documents in usable coarse topics land in a usable granular topic. The 17 worst-retained coarse topics are, however, mostly noise the granular fit correctly dissolves: `10_book_chapter_books_read` (boilerplate), `63_kate_maggie_charlotte_lily`, `79_michael_mike`, `105_sam_sarah` (character names), `8_want_do_you_can`, `57_bad_idea_good_worse`, `115_start_done_ready_finish` (function words). Best-retained are the semantically distinctive ones (wolf 99.7%, vampire 99.4%, kiss 99.1%, money 98.2%).
- **159 tiny topics strand 22,766 documents** below the 200-doc floor — including **9 explicit/suggestive topics** (*Eyes Shut Nearing Climax*, *Erection Straining Against His Pants*, *Savoring Her Taste*, *Overheard Pleasure Sounds*, …). This is exactly the H1 content the granular fit was supposed to buy, thrown away by the usability rule.
- **Diversity**: the coarse fit's 0.285 means heavy vocabulary reuse across topics, i.e. collinear predictors in any book-level regression. This hurts H3's interaction term and H1's difference score more than it hurts single-axis tests.

## 5. Usable-topic yield does not peak at call 73

| Call | Topics | Usable | Docs in usable | Median usable size |
|---|---|---|---|---|
| 55 | 117 | 116 | 117,963 | 576 |
| 19 | 302 | 173 | 98,605 | 353 |
| **73 (frozen)** | 329 | 161 | 100,769 | 379 |
| **49** | 373 | **213** | **110,279** | 348 |
| 68 | 395 | 202 | 104,741 | 357 |

Call 49 — the longest stable-Pareto entry in `cross_embedding_stable_shortlist.csv` — yields **52 more usable topics and ~9,500 more analyzable documents** than the frozen call 73 at nearly identical coherence (0.654 vs 0.657). It has no Stage08 labels, so this is a yield comparison only.

## Reproduce

```bash
.venv/bin/python scripts/analysis/compare_granularity_call55_call73.py
.venv/bin/python scripts/analysis/granularity_axis_separation.py
.venv/bin/python scripts/analysis/granularity_costs.py
```

Outputs: `call73_to_call55_doc_alignment.csv`, `call55_fanout.csv`, `hypothesis_topic_provenance.csv`, `call55_retention_in_call73.csv`, `axis_coverage.csv`.
