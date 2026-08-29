# Stage09 taxonomy prompt v2.5 — what changed and why

Prompt module: `src/stage09_category_mapping/stage1_theory_driven_categories/prompts/taxonomy_mapping_v25.py`
Selected with `--prompt-version v2.5`. Taxonomy itself is unchanged (v2.4).

## Why a new prompt version

The call_49 run used prompt v2 and produced three problems that blocked Stage10:

| Symptom in the v2 run | Count | Consequence |
|---|---|---|
| `main_category_id = uncertain_interpretable` | 30 / 348 | topics carry no usable theme |
| `evidence_quality = low` | 163 / 348 | half the corpus is unusable in a confidence-gated robustness check |
| `3.1` (positive resolution) assigned | 0 / 348 | `AX_payoff_safety` and the H5 tender leg lose their intended component |
| `2.4` (aftercare) assigned | 0 / 348 | post-sex reflection cannot be separated from explicit sex (2.3) |

All 348 v2 mappings came from the LLM (`classification_source = llm` for every topic; only
~20 minor heuristic post-adjustments), so these are prompt-behaviour problems rather than
router or code problems.

## The four changes

1. **Evidence discipline.** `mapping_reasoning` must open with `EVIDENCE: "<verbatim 3–15 word
   quote>"`, and `evidence_quality` is redefined by what that quote shows (two converging
   snippets = high, one clear snippet = medium, label-only = low) rather than by how important
   or glamorous the topic feels. An explicit rule states that a small, ordinary topic with clear
   snippets is `high`.
2. **`uncertain_interpretable` as a last resort.** The model must first rank three candidate IDs
   and walk an ordered checklist (setting → object → discourse → subgenre → body → social world →
   work) before falling back, and must supply an `uncertainty_reason` saying what makes the topic
   unnameable.
3. **`3.1` unblocked, `2.4` clarified.** v2's "resolution/relief/payoff only — NOT generic
   amusement" was read as "never use 3.1". v2.5 states that 3.1 applies whenever relief,
   resolution, or felt safety is the dominant beat even in quiet scenes, and draws explicit lines
   against 4.5 (commitment act) and 4.6 (active caretaking). `2.4` gets a positive definition
   (scene sits after sex, stillness rather than escalation) plus a worked example.
4. **No manufactured luxury.** The corpus contains essentially no wealth or elite-status
   vocabulary, so v2.5 states that leaving `6.1a`, `6.6`, `6.7` empty is a correct outcome and
   requires explicit wealth/rank vocabulary before assigning them. This prevents the H3 axis
   from being filled with false positives.

## Pilot result (30 stratified topics)

Selection via `scripts/stage09/build_pilot_subset.py`: 10 currently-`uncertain_interpretable`,
10 currently-low-`evidence_quality`, 5 lexical relief/payoff candidates, 5 high-confidence
controls. Full diff: `call49_rerun2_pilot_diff.md`.

| Metric (same 30 topics) | v2 | v2.5 |
|---|---|---|
| `uncertain_interpretable` | 11 | 4 |
| Low `evidence_quality` | 21 (70%) | 9 (30%) |
| Topics on axis-bearing IDs | 10 | 14 |
| `mapping_reasoning` opens with `EVIDENCE:` | — | 30 / 30 |
| `uncertain_interpretable` missing a reason | — | 0 |

Per stratum:

- **Controls: 5 / 5 unchanged.** No regression on topics v2 already mapped confidently.
- **Low-evidence: 8 / 10 upgraded** (7 to medium, 1 to high). The 2 that stayed low are
  genuinely thin.
- **Uncertain: 6 / 10 resolved** to specific IDs (4.2, 4.6, 3.3, 6.1b, 7.3, 9.3). The 4 that
  stayed now carry substantive reasons — cross-domain size comparison, fragmentary exclamations,
  surprise register with no visible subject. These look like real discourse artefacts.
- **Payoff candidates: 0 / 5 moved to 3.1**, and on inspection that is correct. All five are
  active reassurance ("you'll be fine," he whispered → 4.6), distress (3.2), or ambivalence
  (3.3), not settled relief. The lexical screen was a loose recall filter, not ground truth.

## Consequence for H2 / H5

The pilot suggests `3.1` may be legitimately rare in this model rather than merely suppressed:
the taxonomy routes reassurance to 4.6 and relief-after-strain scenes appear to be scarce at
348-topic granularity. If the full re-run leaves `3.1` with fewer than 3 topics, the plan's
guard applies — `AX_payoff_safety = 4.5 + 4.6`, with `4.6` residualised on `4.5` when testing
H4 so the shared component is not double-counted. The overlap is reported, not hidden.
