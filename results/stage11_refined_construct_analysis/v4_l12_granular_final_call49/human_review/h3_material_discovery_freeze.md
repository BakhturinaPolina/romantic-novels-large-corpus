# H3 material-provision discovery — freeze note

**Date:** 2026-08-31  
**Run:** `v4_l12_granular_final_call49`  
**Scope:** One-day full-corpus material spillover (H4-shaped, cap 40), not a full H3 re-audit.

## Question

After appearance vs material separation, is H3’s thin material side a **recall** problem (missed provision topics across leaves) or true under-representation at topic level?

## Method

1. Multi-signal candidate gen over all 348 topics (`economic_power` / `domestic_care` tags; discovery leaves `6.2–6.6, 5.1, 7.3, 8.1`; core lexical prototypes). Cap 40. Already-strict material topic **17** excluded from triage bill.
2. Dedicated Nemo triage (`h3_spillover_triage.yaml`) promoting only relationship-directed `money_provision` / `housing_provision`.
3. Pass A/B/C on 12 promoted IDs (Nemo).
4. **Credible material gate (this discovery):** Pass C ∈ {S8, S9} **and** Pass B share of that code ≥ 0.70.

## Results

| Stage | Count / IDs |
|---|---|
| Candidates | 40 |
| Promoted | 12 → `10, 22, 27, 112, 137, 140, 141, 143, 191, 193, 316, 345` |
| Pass C S8/S9 among promoted | `22` (S8), `112` (S8), `191` (S8) |
| **Credible (B share ≥ 0.70)** | **`112` only** (S8 @ 0.778) — plus pre-existing **`17`** (S9 @ 1.0) |
| Near miss | `22` S8 @ **0.667** (below 0.70) |
| Not credible | `191` Pass C S8 but Pass B S8 share **0.131** (enters pipeline strict only via vacuous `props_mass < 0.50` rule after stripping S0 — not treated as a discovery success) |

Promoted rejects / non-material adjudications included medical care (S6), physical protection (S7), emotional (S1/S2), gift tokens (S14), and off-target (S0).

**Caveat on 112:** label *Desperate Need For A Job*; Pass B rationale is employment-heavy. Borderline vs the stated exclusion of general workplace talk — kept as the sole new strict S8 under the numeric gate, but not strong evidence of abundant hidden provision content.

## Interpretation (frozen)

- **New credible material topics found: 1** (within the 0–2 band).
- Material/economic-security content remains **poorly represented at topic level**.
- Emotional-security side remains measurable (viable).
- Direct **emotional-vs-material comparison stays underpowered** — do not treat Stage 11 H3 ratio as confirmatory.
- Appearance vs material separation stands; this pass does **not** reopen that design.

## Artifacts

- Config / prompt: `configs/stage11/refined_constructs.yaml` (`spillover.h3_*`), `configs/stage11/prompts/h3_spillover_triage.yaml`
- Spillover: `candidates/h3_spillover.json`, `audits/h3/spillover_triage.jsonl`
- Targeted audits: H3 `lexical.jsonl` / `contextual.jsonl` / `adjudication.jsonl` (12 promoted)
- Master / `W_tk_*` / `construct_coverage.json` rebuilt for consistency with new adjudications
- **NB08–09 not re-run** for confirmatory H3 claims (still underpowered by discovery criterion)

## Decision

**Freeze H3 material discovery.** No further spillover expansion unless a future design deliberately relaxes the Pass B ≥ 0.70 rule or merges near-miss topic 22 under an explicit measurement change.
