# Four high-granularity models — what they actually add to H1–H6

**Date:** 2026-08-12
**Fits:** phase2 compare-fit, same 432,145-sentence sample
**Question:** among the four longest shortlist models, which (if any) improve hypothesis testing over the frozen L12 call 73?

| # | Model | Call | Topics | c_v | Diversity | Outlier | n_topics std (range) |
|---|---|---|---|---|---|---|---|
| 1 | MPNet | 38 | 444 | 0.542 | 0.950 | 0.73 | 5.73 (440–454) |
| 2 | L12 | 11 | 387 | 0.516 | 0.959 | 0.72 | **1.25 (386–389)** |
| 3 | L12 | 49 | 373 | 0.654 | 0.686 | 0.69 | 3.56 (366–374) |
| 4 | L12 | 73 | 329 | **0.657** | 0.669 | 0.70 | 7.13 (320–337) |

These are **two different clustering regimes**, not four points on one granularity axis.

## 1. Two regimes, split by `min_df`

| | High-diversity pair (MPNet-38, L12-11) | Coherent pair (L12-49, L12-73) |
|---|---|---|
| `vectorizer__min_df` | **3–4** | **15–16** |
| `hdbscan__min_cluster_size` | 69–84 | 104–106 |
| Diversity ~0.95 | Almost unique rare words per topic | Shared mid-frequency vocab |
| Coherence | 0.52–0.54 (words do not hang together) | **0.65** |
| Tiny topics (<200 docs) | 319 / 214 | 160 / 159 |

Diversity 0.95 is a `min_df` artifact, not a romance-theme inventory. Topics are tagged with rare tokens (`nuzzled`, `kallista`, `fitzgelder`, `safeword`) that c-TF-IDF can separate even when the underlying scenes are the same. That is why these two sit on the Pareto frontier and why they are the worst of the four for Stage10.

`reduce_outliers` on MPNet-38 drops c_v from 0.54 to **0.36**. Do not use it.

## 2. Usable yield (the number that matters)

A topic is usable if it is ≥200 docs and not flagged tiny/boilerplate/multilingual.

| Model | Topics | Usable | Docs in usable | Tiny docs wasted | Core (≥800) |
|---|---|---|---|---|---|
| MPNet-38 | 444 | 126 | 78,721 | **37,189 (32% of assigned)** | 18 |
| L12-11 | 387 | 173 | 93,278 | 26,777 | 26 |
| **L12-49** | 373 | **213** | **110,279** | 22,570 | **28** |
| L12-73 (frozen) | 330 | 171 | 104,801 | 22,766 | 24 |

Call 49 is the only model that turns extra topics into extra **usable** axes. MPNet-38 is the worst: 72% of its topics fall below the floor that Stage10 already uses.

## 3. What the large topics actually are

KeyBERT + representative sentences, not c-TF-IDF names (those downweight `kiss`/`cock`/`gun` because they appear in too many romance topics).

**MPNet-38 — false granularity.** H1 is two mega-clusters, not 444 distinct scenes:

- T0 (9,324): *nuzzled / buttocks / nipple in his mouth* — kiss + oral + body in one topic
- T1 (4,824): *wraps arms / wet heat / fingers / kiss* — another intimacy mega-cluster
- T2 (4,032): mixed vow/protect/safeword/dialogue (`I'll never leave you` / `I don't do crying`)
- T23 (618): the one genuinely new H1/consent topic — *paddle / dicks / climaxing / safeword* (BDSM)

Jealousy exists only as tiny T274 (111 docs). Luxury and dark/threat have **no usable topic**.

**L12-11 — cleanest scene inventory, contaminated book mixture.**

- T0 (6,504) transit/car; T2 food; T3 phones; T7 rain; T9 family; T10 lawyers; **T13 (1,165) debt/finances** — the only usable H3-adjacent topic in the four
- T4 (2,315) kiss/breast (H1, one cluster)
- T22 (867) snuggled-in-bed vs T85 (310) hug — the only clean tenderness split
- T23 (845) marriages/divorced/engaged
- **T8 (1,635) publisher copyright** (`reproduction / unauthorized / ellorascave`) is usable and will leak into every book mixture. Posthoc missed it because it is not tiny.

**L12-49 vs L12-73 — near-duplicates; 49 splits H1, 73 dumps it.**

Both open with the same doorway/ride topic (T0 ~8k) and the same smirk/phone/gaze clusters. Difference that matters for H1:

| | L12-49 H1 sex/escalation | L12-73 H1 sex/escalation |
|---|---|---|
| Usable topics | **7** (4,553 docs) | 3 (6,342 docs) |
| Structure | T7 kiss 1,886 / T25 bedside 808 / T41 stroking 529 / T63 moaned 459 / … | **T1 5,632** (Stage08: *Soft Kiss Turning Urgent*) + T56 438 + T118 272 |

Call 73’s extra “granularity” over call 55 was real. Call 49’s extra granularity over call 73 is also real, and it is specifically H1 sub-scene splits — the thing the 200-doc floor kept discarding as tiny explicit topics on call 73.

Call 73 still wins H4 protective care (6 usable / 2,939 docs vs 49’s 3 / 1,029) and is the only one with Stage08 labels, including the H5 dark/threat topics that KeyBERT cannot see (`gun`/`knife` never rank).

## 4. Hypothesis by hypothesis

| Hypothesis | MPNet-38 | L12-11 | L12-49 | L12-73 |
|---|---|---|---|---|
| **H1 Love-over-Sex** | Worse than 117-topic call 55. Sex+kiss fused in T0+T1 (14k docs). 12 extra explicit topics are tiny. | One 2,315 kiss/breast topic + one 208 `intimacy/taboo/erection`. Tenderness split is good. | **Best H1 split of the four.** 7 usable escalation topics; hug separate (T124). | Operational (labeled) but H1 is two 5k-class topics. 4 explicit leftovers are tiny. |
| **H2 HEA** | One 301-doc `engaged` topic. | One 845-doc marriage/divorce topic. | **5 usable** (engaged / rings / partners). | 5 usable, but T3 (3,707) is a mixed affection dump. Labeled ring-as-bargain exists. |
| **H3 Luxury × Love** | Luxury only in tiny topics. | **Only usable money topic** (T13 debt, 1,165). Still no glamour/duke/yacht. | None. | None in KeyBERT; Stage08 also found almost no 6.1a/6.6. |
| **H4 Protect vs Possess** | Protect exists (T49); jealousy only tiny. | Protect T117 (263); jealousy absent. | 3 protect topics; jealousy absent. | **Best protect coverage** (T18 *Keep Her Safe* 1,001 + 5 more). Possessive still thin (labels found 2). |
| **H5 Dark vs Tender** | Dark = 0 usable. Tender = 1 (513). | Dark = 0. Tender split exists. | Dark = 0 by KeyBERT (same min_df blind spot). Tender thin. | Stage08: 14 dark topics. KeyBERT misses them. Do not drop 73 on this scan. |
| **H6 Arc / repair** | Apology split (T22, T113) plus a 4k mixed T2. | Clean apologize / forgive pair (T115, T156). | **Most repair topics (7).** | 6, including labeled *Admitting Love After Denial*. |
| Consent / coercion | **Only model with a usable BDSM/safeword topic (T23).** | Absent. | Weak (copyright-like `permission` cluster). | Labeled (`Stop When Asked`, `Rifle Pointed at Captive`) — not visible in KeyBERT. |

**None of the four solve H3.** Status/glamour is not a function of topic count. If H3 stays in the confirmatory set, it needs a different representation (book metadata, luxury composite from non-topic features), not a 400-topic refit.

## 5. Stability

L12-11 is the only rock-solid refit (range 3 topics). L12-73 is the least stable of the four (range 17) — that is why it sat near the old `max_n_topics_std: 3` gate. L12-49 (std 3.56, range 8) is acceptable for a Stage05 refit. MPNet-38 (range 14) is not.

## 6. Recommendation

1. **Do not promote MPNet-38 or L12-11 to Stage08/10.** Their diversity scores are `min_df` artifacts. MPNet-38 is the worst H1 model of the four. L12-11 is useful only as a *source of extra scene types* (debt, phones, rain, lawyers) and must drop T8 copyright first.

2. **If you can spend one more Stage08 batch: label L12-49, not another 300-topic L12 lookalike.** It is the only model that converts extra topics into extra usable H1/H2/H6 axes, with the best document coverage (110k) and acceptable stability. Call 73 stays the labeled fallback.

3. **If you cannot spend Stage08:** keep frozen call 73. Its H4/H5/consent labels are not recoverable from KeyBERT on any of these fits, and call 49 is not labeled.

4. **Do not chase 400+ topics further** (L12-11, MPNet-38, or call 68 at 395). Past ~370 with `min_df≥15`, extra topics become the tiny tail you already throw away.

## Reproduce

```bash
.venv/bin/python scripts/analysis/analyze_four_granular_models.py
```

Tables: `yield_comparison.csv`, `axis_coverage.csv`, `top15_topics.csv`.
