# Hardened Sonnet re-audit — what changed
Comparison of adjudication codes **before** (archived weak-prompt / free-form run) vs **after** (v1.1 codebook schemas).
H1 was already on v1.2 and is unchanged here.
## H2
- Old archive: `archive_before_rerun_20260830_214425` (n=10, codebook-mapped=5)
- New: n=10, usable (mapped+MIXED)=10

| code | old | new |
|------|----:|----:|
| `H2_0` | 0 | 4 |
| `UNKNOWN` | 4 | 0 |
| `HEA_CONFIRMED` | 3 | 0 |
| `H2_7` | 0 | 2 |
| `CONDITIONAL_HEA — qualifies under 4.5 only if romantic co...` | 1 | 0 |
| `H2_1` | 0 | 1 |
| `H2_3` | 0 | 1 |
| `H2_5` | 0 | 1 |
| `H2_6` | 0 | 1 |
| `HEA_CONDITIONAL_TRAJECTORY` | 1 | 0 |
| `HEA_PUBLIC_UNION` | 1 | 0 |

**Topic flips:** 10 / 10

- topic 29: `HEA_CONFIRMED` → `H2_7`
- topic 61: `HEA_CONFIRMED` → `H2_6`
- topic 62: `UNKNOWN` → `H2_0`
- topic 65: `HEA_CONFIRMED` → `H2_3`
- topic 128: `UNKNOWN` → `H2_7`
- topic 157: `HEA_CONDITIONAL_TRAJECTORY` → `H2_0`
- topic 167: `HEA_PUBLIC_UNION` → `H2_5`
- topic 204: `CONDITIONAL_HEA — qualifies under 4.5 on` → `H2_0`
- topic 242: `UNKNOWN` → `H2_1`
- topic 305: `UNKNOWN` → `H2_0`

## H3
- Old archive: `archive_before_rerun_20260830_195953` (n=82, codebook-mapped=0)
- New: n=82, usable (mapped+MIXED)=82

| code | old | new |
|------|----:|----:|
| `UNKNOWN` | 56 | 0 |
| `S0` | 0 | 42 |
| `MIXED` | 26 | 1 |
| `S1` | 0 | 17 |
| `S13` | 0 | 7 |
| `S4` | 0 | 4 |
| `S5` | 0 | 3 |
| `S2` | 0 | 2 |
| `S9` | 0 | 2 |
| `S11` | 0 | 1 |
| `S15` | 0 | 1 |
| `S3` | 0 | 1 |
| `S7` | 0 | 1 |

**Topic flips:** 82 / 82

- topic 6: `UNKNOWN` → `S0`
- topic 17: `MIXED` → `S9`
- topic 18: `UNKNOWN` → `S13`
- topic 27: `MIXED` → `S0`
- topic 29: `MIXED` → `S1`
- topic 31: `UNKNOWN` → `S0`
- topic 36: `MIXED` → `S11`
- topic 38: `UNKNOWN` → `S1`
- topic 45: `MIXED` → `S1`
- topic 46: `UNKNOWN` → `S3`
- topic 49: `UNKNOWN` → `S0`
- topic 52: `UNKNOWN` → `S0`
- … +70 more

## H4
- Old archive: `archive_before_rerun_20260830_204700` (n=32, codebook-mapped=0)
- New: n=32, usable (mapped+MIXED)=32

| code | old | new |
|------|----:|----:|
| `UNKNOWN` | 21 | 0 |
| `H4_0` | 0 | 13 |
| `H4_1` | 0 | 12 |
| `MIXED` | 11 | 1 |
| `H4_2` | 0 | 3 |
| `H4_8` | 0 | 2 |
| `H4_5` | 0 | 1 |

**Topic flips:** 32 / 32

- topic 6: `UNKNOWN` → `H4_0`
- topic 31: `UNKNOWN` → `H4_0`
- topic 36: `MIXED` → `H4_2`
- topic 45: `MIXED` → `H4_1`
- topic 46: `UNKNOWN` → `H4_1`
- topic 56: `MIXED` → `H4_1`
- topic 70: `UNKNOWN` → `H4_0`
- topic 83: `UNKNOWN` → `H4_2`
- topic 88: `UNKNOWN` → `H4_0`
- topic 96: `UNKNOWN` → `H4_1`
- topic 119: `UNKNOWN` → `H4_5`
- topic 161: `UNKNOWN` → `H4_0`
- … +20 more

## H5
- Old archive: `archive_before_rerun_20260830_210738` (n=22, codebook-mapped=1)
- New: n=22, usable (mapped+MIXED)=22

| code | old | new |
|------|----:|----:|
| `UNKNOWN` | 21 | 0 |
| `D4` | 1 | 13 |
| `D3` | 0 | 6 |
| `D0` | 0 | 2 |
| `MIXED` | 0 | 1 |

**Topic flips:** 21 / 22

- topic 27: `UNKNOWN` → `D0`
- topic 64: `UNKNOWN` → `D4`
- topic 92: `UNKNOWN` → `D4`
- topic 102: `UNKNOWN` → `D4`
- topic 133: `UNKNOWN` → `D4`
- topic 145: `UNKNOWN` → `D4`
- topic 152: `UNKNOWN` → `D4`
- topic 179: `UNKNOWN` → `D4`
- topic 184: `UNKNOWN` → `D3`
- topic 220: `UNKNOWN` → `D4`
- topic 223: `UNKNOWN` → `D3`
- topic 244: `UNKNOWN` → `D4`
- … +9 more

## H6
- Old archive: `archive_before_rerun_20260830_212208` (n=2, codebook-mapped=0)
- New: n=29, usable (mapped+MIXED)=29

| code | old | new |
|------|----:|----:|
| `ARC_1` | 0 | 7 |
| `ARC_0` | 0 | 6 |
| `MIXED` | 0 | 5 |
| `ARC_5` | 0 | 4 |
| `ARC_10` | 0 | 3 |
| `ARC_4` | 0 | 2 |
| `UNKNOWN` | 2 | 0 |
| `ARC_2` | 0 | 1 |
| `ARC_6` | 0 | 1 |

**Topic flips:** 2 / 2

- topic 3: `UNKNOWN` → `ARC_5`
- topic 24: `UNKNOWN` → `MIXED`

## Takeaways

- Free-form / `UNKNOWN` / invented tags collapsed to real codebook IDs (`H2_*`, `S*`, `H4_*`, `D*`, `ARC_*`).
- H3: majority now `S0` (off-target for security) or `S1` (emotional reassurance) — appearance topics get `S13` where warranted.
- H4: mostly `H4_0`/`H4_1` (off-target / reassurance) rather than false “protection”.
- H5: `D4` individual distress and `D3` external danger dominate; little forced tenderness.
- H2: few true HEA payoffs; several `H2_0` / intense-talk (`H2_7`); rings→`H2_6`, wedding→`H2_5`.
- H6 pool size is **29** topics (not 42); all completed on v1.1.
