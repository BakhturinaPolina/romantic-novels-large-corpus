"""Canonical code normalisation and code → RAX construct maps for Stage 11.

Live Nemo adjudications sometimes return aliases (HEA, PROTECT, Conflict, …).
This module maps those onto the frozen codebook IDs, then onto atomic RAX
constructs used in the refined analysis frame.
"""

from __future__ import annotations

import re
from typing import Dict, List, Mapping, Optional, Set

# ---------------------------------------------------------------------------
# Alias → canonical code
# ---------------------------------------------------------------------------

_CODE_ALIASES: Dict[str, str] = {
    # H1
    "I0": "I0", "I1": "I1", "I2": "I2", "I3": "I3", "I4": "I4",
    "I5": "I5", "I6": "I6", "I7": "I7", "I8": "I8", "I9": "I9", "I10": "I10",
    # H2 — IDs match configs/stage11/prompts/h2_hea.yaml (not the old +1 RAX offset)
    "H2_0": "H2_0", "H2_1": "H2_1", "H2_2": "H2_2", "H2_3": "H2_3",
    "H2_4": "H2_4", "H2_5": "H2_5", "H2_6": "H2_6", "H2_7": "H2_7", "H2_8": "H2_8",
    "HEA": "H2_4",
    "HEA_CONFIRMED": "H2_4",
    "FINAL_PAYOFF": "H2_4",
    "FINAL_RELATIONAL_PAYOFF": "H2_4",
    "HEA_CONDITIONAL_TRAJECTORY": "H2_3",
    "HEA_PUBLIC_UNION": "H2_5",
    "REPAIR": "H2_2",
    "RECONCILIATION": "H2_2",
    "COMMITMENT": "H2_3",
    "MUTUAL_COMMITMENT": "H2_3",
    "PUBLIC_UNION": "H2_5",
    "WEDDING": "H2_5",
    "LOVE_TOKEN": "H2_6",
    "COMMITMENT_SYMBOL": "H2_6",
    "CONFESSION": "H2_1",
    "APOLOGY": "H2_1",
    "4.5": "H2_2",
    "4.5.1": "H2_2",
    # H3
    **{f"S{i}": f"S{i}" for i in range(17)},
    "EMOTIONAL_SECURITY": "S1",
    "MATERIAL_PROVISION": "S8",
    "STATUS_DISPLAY": "S12",
    "APPEARANCE": "S13",
    # H4
    **{f"H4_{i}": f"H4_{i}" for i in range(14)},
    "H4_5a": "H4_5a",
    "H4_5A": "H4_5a",
    "PROTECTIVE_COMMITMENT": "H4_5a",
    "PROTECT": "H4_5",
    "PROTECTION": "H4_5",
    "EXTERNAL_PROTECTION": "H4_5",
    "REASSURANCE": "H4_1",
    "JEALOUSY": "H4_8",
    "CLAIMING": "H4_7",
    "CONTROL": "H4_9",
    "COERCIVE_CONTROL": "H4_9",
    "4.6.1": "H4_1",
    "H4.6.1": "H4_1",
    "P4.6.1": "H4_1",
    "H4-4.6.1": "H4_1",
    "H4.1": "H4_1",
    # H5
    **{f"D{i}": f"D{i}" for i in range(7)},
    "RELATIONAL_DARKNESS": "D1",
    "PARTNER_HARM": "D2",
    "EXTERNAL_DANGER": "D3",
    "INDIVIDUAL_DISTRESS": "D4",
    "TENDERNESS": "D5",
    # H6 — frozen h6_arc.yaml: ARC_1–4 falling, ARC_5–8 rising, ARC_9 external
    **{f"ARC_{i}": f"ARC_{i}" for i in range(11)},
    "CONFLICT": "ARC_2",
    "MAIN_COUPLE_CONFLICT": "ARC_2",
    "OBSTACLE": "ARC_9",
    "EXTERNAL_PLOT_CONFLICT": "ARC_9",
    "HIDDEN INFORMATION": "ARC_1",
    "HIDDEN_INFORMATION": "ARC_1",
    "SECRET": "ARC_1",
    "MISUNDERSTANDING": "ARC_1",
    "SEPARATION": "ARC_3",
    "BREAKUP": "ARC_3",
    "RELATIONSHIP_CAUSED_DISTRESS": "ARC_4",
    "DISCLOSURE": "ARC_5",
    "REVELATION": "ARC_5",
    "CONFLICT RESOLUTION": "ARC_6",
    "CONFLICT_RESOLUTION": "ARC_6",
    "REPAIR_ARC": "ARC_6",
    "REASSURANCE_ARC": "ARC_7",
    "RESTORED_TRUST": "ARC_7",
    "MUTUAL_COMMITMENT_FINAL_PAYOFF": "ARC_8",
    "FALLING": "ARC_2",
    "REFINED_FALLING": "ARC_2",
    "RISING": "ARC_5",
    "REFINED_RISING": "ARC_5",
    "INNER_CONFLICT": "ARC_2",
    "INTERNAL STRUGGLE": "ARC_2",
    "INTERNAL_STRUGGLE": "ARC_2",
    "ANTAGONIST": "ARC_9",
    "INSTIGATOR": "ARC_2",
    "CATALYST": "ARC_2",
    "COMPLICATING FACTOR": "ARC_2",
    "INTRO": "ARC_0",
}


def normalize_code(raw: object) -> Optional[str]:
    """Map a free-form audit code onto a canonical codebook ID, or None if unusable."""
    if raw is None:
        return None
    if isinstance(raw, dict):
        return None
    s = str(raw).strip()
    if not s or s.upper() in ("NONE", "NAN", "UNKNOWN", "MIXED", "NULL"):
        return None
    # Exact alias
    key = s.upper() if not re.match(r"^[A-Za-z]+\d+$", s) else s
    # Prefer case-sensitive for I3/H2_1/S1 style
    if s in _CODE_ALIASES:
        return _CODE_ALIASES[s]
    if s.upper() in _CODE_ALIASES:
        return _CODE_ALIASES[s.upper()]
    # Soft match: leading code token
    m = re.match(r"^(I\d{1,2}|H2_\d|S\d{1,2}|H4_\d{1,2}a?|D\d|ARC_\d{1,2})\b", s, re.I)
    if m:
        tok = m.group(1)
        # Normalise ARC_01 → ARC_1 etc.
        parts = tok.upper().split("_")
        if len(parts) == 2 and parts[1].isdigit():
            tok = f"{parts[0]}_{int(parts[1])}"
        elif tok.upper().startswith("I"):
            tok = "I" + str(int(tok[1:]))
        elif tok.upper().startswith("S"):
            tok = "S" + str(int(tok[1:]))
        elif tok.upper().startswith("D"):
            tok = "D" + str(int(tok[1:]))
        if tok in _CODE_ALIASES:
            return _CODE_ALIASES[tok]
        return tok
    # Title-case phrase aliases already uppercased above
    phrase = re.sub(r"\s+", " ", s).strip().upper()
    if phrase in _CODE_ALIASES:
        return _CODE_ALIASES[phrase]
    return None


# ---------------------------------------------------------------------------
# Code → atomic RAX constructs (plan-aligned)
# ---------------------------------------------------------------------------

CODE_TO_RAX: Dict[str, List[str]] = {
    # H1 intimacy
    "I1": ["RAX_emotional_intimacy"],
    "I2": ["RAX_emotional_reassurance"],
    "I3": ["RAX_nonexplicit_affection"],
    "I4": ["RAX_sexual_tension"],
    "I5": ["RAX_erotic_escalation"],
    "I6": ["RAX_explicit_sex"],
    "I7": ["RAX_postsex_aftercare"],
    "I8": ["RAX_sexual_negotiation"],
    "I9": ["RAX_coercive_sexuality"],
    # I0 / I10 intentionally omitted from primary RAX atoms
    # H2 HEA (aligned to prompt codebook labels)
    "H2_1": ["RAX_generic_confession_apology"],
    "H2_2": ["RAX_repair"],
    "H2_3": ["RAX_mutual_commitment"],
    "H2_4": ["RAX_final_relational_payoff"],
    "H2_5": ["RAX_public_union"],
    "H2_6": ["RAX_commitment_symbols"],
    # H2_0 off_target, H2_7 intense talk, H2_8 non-main-couple: no primary RAX atom
    # H3 security
    "S1": ["RAX_emotional_security"],
    "S2": ["RAX_emotional_security"],
    "S3": ["RAX_emotional_security"],
    "S4": ["RAX_commitment_security"],
    "S5": ["RAX_practical_care"],
    "S6": ["RAX_medical_care"],
    "S7": ["RAX_physical_protection"],
    "S8": ["RAX_material_provision"],
    "S9": ["RAX_housing_security"],
    "S10": ["RAX_economic_dependency"],
    "S11": ["RAX_practical_care"],
    "S12": ["RAX_status_display"],
    "S13": ["RAX_appearance_grooming"],
    "S14": ["RAX_gift_romance_token"],
    "S15": ["RAX_workplace_status"],
    # H4 protection / possession
    "H4_1": ["RAX_emotional_reassurance", "RAX_emotional_security"],
    "H4_2": ["RAX_practical_care"],
    "H4_3": ["RAX_material_provision"],
    "H4_4": ["RAX_emotional_reassurance"],
    "H4_5": ["RAX_external_protection"],
    "H4_5a": ["RAX_protective_commitment"],
    "H4_6": ["RAX_external_protection"],
    "H4_7": ["RAX_possessive_claiming"],
    "H4_8": ["RAX_possessive_claiming"],
    "H4_9": ["RAX_coercive_control"],
    "H4_10": ["RAX_coercive_control"],
    "H4_11": ["RAX_coercive_control"],
    "H4_12": ["RAX_reciprocal_support"],
    # H5 darkness
    "D1": ["RAX_relational_darkness"],
    "D2": ["RAX_partner_harm_control", "RAX_relational_darkness"],
    "D3": ["RAX_external_danger_crisis"],
    "D4": ["RAX_individual_distress"],
    "D5": ["RAX_tenderness_core"],
    # H6 arc (also used in W_tkr): ARC_1–4 falling, ARC_5–8 rising, ARC_9 external
    "ARC_1": ["RAX_arc_falling"],
    "ARC_2": ["RAX_arc_falling"],
    "ARC_3": ["RAX_arc_falling"],
    "ARC_4": ["RAX_arc_falling"],
    "ARC_5": ["RAX_arc_rising"],
    "ARC_6": ["RAX_arc_rising"],
    "ARC_7": ["RAX_arc_rising"],
    "ARC_8": ["RAX_arc_rising"],
    "ARC_9": ["RAX_external_plot_conflict"],
}

# Codes treated as off-target / non-construct for W_tk inclusion
OFF_TARGET_CODES: Set[str] = {
    "I0", "H2_0", "H2_7", "H2_8", "S0", "S16", "H4_0", "H4_13", "D0", "D6",
    "ARC_0", "ARC_10", "MIXED", "UNKNOWN",
}

# H5 tenderness bridge: H1/H4 codes reused into RAX_tenderness_core
# (H4_2 practical care excluded — generic caretaking ≠ tenderness)
H5_TENDERNESS_H1_CODES: Set[str] = {"I1", "I2", "I3", "I7"}
H5_TENDERNESS_H4_CODES: Set[str] = {"H4_1", "H4_4", "H4_12"}
# Stage 09 leaves kept as interpersonal/conflict-darkness anchors (skip_full_relabel).
# Partner-vs-external source for 7.2 was not topic-audited.
H5_DARKNESS_ANCHOR_LEAVES: Set[str] = {"7.2", "4.4"}

# Composite definitions (sums of atoms; built after atom columns exist)
COMPOSITE_DEFS: Dict[str, List[str]] = {
    "RAX_h1_emotional_side": [
        "RAX_emotional_intimacy",
        "RAX_emotional_reassurance",
        "RAX_nonexplicit_affection",
    ],
    "RAX_h1_explicit_side": ["RAX_explicit_sex"],
    "RAX_h2_strict": ["RAX_final_relational_payoff"],
    "RAX_h2_broad": [
        "RAX_repair",
        "RAX_mutual_commitment",
        "RAX_final_relational_payoff",
    ],
    "RAX_h3_emotional_side": [
        "RAX_emotional_security",
        "RAX_commitment_security",
    ],
    # Material side = mutual provision only (S8/S9); exclude S10 dependency & S14 gifts
    "RAX_h3_material_side": [
        "RAX_material_provision",
        "RAX_housing_security",
    ],
    "RAX_social_presentation": [
        "RAX_status_display",
        "RAX_appearance_grooming",
        "RAX_workplace_status",
    ],
    "RAX_h4_protection_side": ["RAX_external_protection"],
    "RAX_protective_care_broad": [
        "RAX_external_protection",
        "RAX_protective_commitment",
    ],
    "RAX_h4_possession_side": [
        "RAX_possessive_claiming",
        "RAX_coercive_control",
    ],
    "RAX_h5_relational_darkness_side": ["RAX_relational_darkness"],
    "RAX_h5_tenderness_side": ["RAX_tenderness_core"],
}

LOG_RATIO_DEFS: Dict[str, tuple] = {
    # name: (numerator_cols, denominator_cols)
    "RLR_emotional_vs_explicit": (
        "RAX_h1_emotional_side",
        "RAX_h1_explicit_side",
    ),
    "RLR_emotional_vs_material_security": (
        "RAX_h3_emotional_side",
        "RAX_h3_material_side",
    ),
    "RLR_protection_vs_control": (
        "RAX_h4_protection_side",
        "RAX_h4_possession_side",
    ),
    "RLR_darkness_vs_tenderness": (
        "RAX_h5_relational_darkness_side",
        "RAX_h5_tenderness_side",
    ),
}


def rax_for_code(code: Optional[str]) -> List[str]:
    if not code:
        return []
    canon = normalize_code(code) or code
    return list(CODE_TO_RAX.get(canon, []))


def all_rax_atoms() -> List[str]:
    atoms: Set[str] = set()
    for xs in CODE_TO_RAX.values():
        atoms.update(xs)
    return sorted(atoms)
