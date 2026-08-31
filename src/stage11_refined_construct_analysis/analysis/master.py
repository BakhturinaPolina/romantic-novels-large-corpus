"""Build Stage 11 master annotation table + W_tk / W_tkr weights.

Weights are family-specific (per hypothesis):
  strict    — dominant code share ≥ threshold → 1; else exclude
  weighted  — retain all credible Pass B code proportions
  inclusive — primary at 1.0 + secondary runners-up at sensitivity weight
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import pandas as pd

from src.stage11_refined_construct_analysis.analysis.constructs import (
    H5_DARKNESS_ANCHOR_LEAVES,
    H5_TENDERNESS_H1_CODES,
    H5_TENDERNESS_H4_CODES,
    OFF_TARGET_CODES,
    normalize_code,
)
from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
    apply_h4_manual_freeze_to_master,
)
from src.stage11_refined_construct_analysis.audits.runner import (
    CODE_FIELD,
    PASS_FILES,
    audit_dir,
    load_jsonl,
    load_evidence_packet,
)
from src.stage11_refined_construct_analysis.config import Stage11Config
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup

LOGGER = logging.getLogger("stage11.master")

HYPOTHESES = ("H1", "H2", "H3", "H4", "H5", "H6")
TERTILES = ("begin", "middle", "end")

# Master column → (hypothesis, construct_family)
CODE_COL_META: Dict[str, Tuple[str, str]] = {
    "intimacy_code": ("H1", "intimacy"),
    "hea_code": ("H2", "hea"),
    "security_code": ("H3", "security"),
    "care_protection_code": ("H4", "care_protection"),
    "darkness_code": ("H5", "darkness"),
    "arc_role": ("H6", "arc"),
}

INCLUSIVE_SECONDARY_WEIGHT = 0.5
INCLUSIVE_RUNNER_FLOOR = 0.15


def _code_from_row(row: Mapping[str, Any], hyp: str) -> str:
    resp = row.get("response") or {}
    field = CODE_FIELD.get(hyp, "")
    for key in (field, "consensus_code", "dominant_code", "code"):
        if key and row.get(key):
            return str(row[key])
        if key and resp.get(key):
            return str(resp[key])
    return str(row.get("code") or "UNKNOWN")


def _share_for_code(proportions: Any, code: str) -> float:
    """Extract a code's share from Pass B proportions (dict preferred)."""
    if isinstance(proportions, dict):
        try:
            return float(proportions.get(code, 0.0) or 0.0)
        except (TypeError, ValueError):
            return 0.0
    return 0.0


def _proportions_dict(proportions: Any) -> Dict[str, float]:
    """Normalise Pass B proportions to {canonical_code: float}."""
    if not isinstance(proportions, dict):
        return {}
    out: Dict[str, float] = {}
    for raw, share in proportions.items():
        try:
            w = float(share)
        except (TypeError, ValueError):
            continue
        if w <= 0:
            continue
        canon = normalize_code(raw) or str(raw)
        if not canon or canon in OFF_TARGET_CODES:
            continue
        out[canon] = out.get(canon, 0.0) + w
    return out


def _is_off_target(code: Optional[str]) -> bool:
    if code is None:
        return True
    s = str(code)
    if s in OFF_TARGET_CODES or s in ("None", "nan", ""):
        return True
    canon = normalize_code(s)
    return canon is None or canon in OFF_TARGET_CODES


def _load_pass_map(cfg: Stage11Config, hyp: str, pass_name: str) -> Dict[int, Dict[str, Any]]:
    path = audit_dir(cfg, hyp) / PASS_FILES[pass_name]
    out: Dict[int, Dict[str, Any]] = {}
    for row in load_jsonl(path):
        if "topic_id" not in row:
            continue
        out[int(row["topic_id"])] = row
    return out


def _keyword_lists(packet: Optional[Mapping[str, Any]]) -> Dict[str, List[str]]:
    if not packet:
        return {"main": [], "keybert": [], "pos": [], "mmr": []}
    reps = packet.get("lexical", {}).get("reps", {}) or {}
    return {
        "main": list(reps.get("Main") or []),
        "keybert": list(reps.get("KeyBERT") or []),
        "pos": list(reps.get("POS") or []),
        "mmr": list(reps.get("MMR") or []),
    }


def _main_couple_probs(
    row_b: Optional[Mapping[str, Any]], row_c: Optional[Mapping[str, Any]]
) -> Tuple[float, float, float]:
    """Return (main_couple_prob, non_couple_prob, unclear_prob)."""
    for row in (row_c, row_b):
        if not row:
            continue
        resp = row.get("response") or {}
        if "main_couple_prob" in resp:
            p = float(resp["main_couple_prob"])
            return p, max(0.0, 1.0 - p), 0.0
        mc = resp.get("main_couple")
        if mc is True or str(mc).lower() in ("yes", "true", "main"):
            return 0.85, 0.10, 0.05
        if mc is False or str(mc).lower() in ("no", "false", "non"):
            return 0.10, 0.80, 0.10
        if mc is not None:
            return 0.33, 0.33, 0.34
    return 0.0, 0.0, 1.0


def _family_pass_b_props(
    by_hyp: Mapping[str, Mapping[str, Dict[int, Dict[str, Any]]]],
    tid: int,
    hyp: str,
) -> Dict[str, float]:
    b = by_hyp[hyp]["B"].get(tid)
    if not b:
        return {}
    return _proportions_dict((b.get("response") or {}).get("proportions"))


def _family_primary_share(
    by_hyp: Mapping[str, Mapping[str, Dict[int, Dict[str, Any]]]],
    tid: int,
    hyp: str,
    primary_code: str,
) -> float:
    """Share of the adjudicated primary code within that family's Pass B props."""
    props = _family_pass_b_props(by_hyp, tid, hyp)
    canon = normalize_code(primary_code) or primary_code
    share = props.get(canon, 0.0)
    if share > 0:
        return share
    # If Pass B missing this code but primary is clean, use dominant mass if any
    if props:
        return 0.0
    # Vacuous Pass B with a clean adjudicated code: treat as fully dominant
    return 1.0 if not _is_off_target(primary_code) else 0.0


def build_master_annotations(cfg: Stage11Config) -> pd.DataFrame:
    """Combine H1–H6 audits into the master annotation table."""
    lookup = load_topic_lookup(cfg)
    dominance = float(cfg.section("weights", "strict_dominance"))

    by_hyp: Dict[str, Dict[str, Dict[int, Dict[str, Any]]]] = {}
    topic_ids: Set[int] = set(int(t) for t in lookup["topic_id"].tolist() if int(t) >= 0)
    for hyp in HYPOTHESES:
        by_hyp[hyp] = {
            "A": _load_pass_map(cfg, hyp, "A"),
            "B": _load_pass_map(cfg, hyp, "B"),
            "C": _load_pass_map(cfg, hyp, "C"),
        }
        for p in ("A", "B", "C"):
            topic_ids.update(by_hyp[hyp][p].keys())

    # Persist per-topic Pass B proportion maps for W_tk (JSON column)
    rows: List[Dict[str, Any]] = []
    for tid in sorted(topic_ids):
        lu = lookup.loc[lookup["topic_id"] == tid]
        if lu.empty:
            continue
        meta = lu.iloc[0]
        packet = load_evidence_packet(cfg, tid)
        kws = _keyword_lists(packet)

        codes: Dict[str, Optional[str]] = {}
        family_props: Dict[str, Dict[str, float]] = {}
        family_strict: Dict[str, float] = {}
        family_weighted_primary: Dict[str, float] = {}
        mixed_flags: List[str] = []
        agree_flags: List[str] = []
        actions: List[str] = []
        proposed: List[str] = []
        review = False
        for hyp in HYPOTHESES:
            a = by_hyp[hyp]["A"].get(tid)
            b = by_hyp[hyp]["B"].get(tid)
            c = by_hyp[hyp]["C"].get(tid)
            field = CODE_FIELD[hyp]
            if not any((a, b, c)):
                codes[field] = None
                continue
            code_a = _code_from_row(a, hyp) if a else None
            code_b = _code_from_row(b, hyp) if b else None
            code_c = _code_from_row(c, hyp) if c else (code_b or code_a)
            codes[field] = code_c
            props = _family_pass_b_props(by_hyp, tid, hyp)
            family_props[hyp] = props
            if code_b == "MIXED" or code_c == "MIXED":
                mixed_flags.append(hyp)
            if code_a and code_b and code_a == code_b and code_b != "MIXED":
                agree_flags.append(hyp)
            resp_c = (c or {}).get("response") or {}
            if resp_c.get("action"):
                actions.append(f"{hyp}:{resp_c['action']}")
            if resp_c.get("proposed_constructs"):
                proposed.extend(str(x) for x in resp_c["proposed_constructs"])
            if resp_c.get("manual_review_required"):
                review = True

            if code_c and not _is_off_target(code_c):
                share = _family_primary_share(by_hyp, tid, hyp, str(code_c))
                props_mass = sum(props.values()) if props else 0.0
                if props_mass < 0.50:
                    share = 1.0
                family_weighted_primary[hyp] = share
                family_strict[hyp] = 1.0 if share >= dominance else 0.0
            else:
                family_weighted_primary[hyp] = 0.0
                family_strict[hyp] = 0.0

        mc, nc, uc = _main_couple_probs(
            by_hyp["H6"]["B"].get(tid) or by_hyp["H5"]["B"].get(tid),
            by_hyp["H6"]["C"].get(tid) or by_hyp["H5"]["C"].get(tid),
        )

        rows.append(
            {
                "topic_id": int(tid),
                "current_topic_label": meta.get("label"),
                "main_keywords": kws["main"],
                "keybert_keywords": kws["keybert"],
                "pos_keywords": kws["pos"],
                "mmr_keywords": kws["mmr"],
                "main_couple_prob": mc,
                "non_couple_prob": nc,
                "unclear_prob": uc,
                "intimacy_code": codes.get("intimacy_code"),
                "hea_code": codes.get("hea_code"),
                "security_code": codes.get("security_code"),
                "care_protection_code": codes.get("care_protection_code"),
                "darkness_code": codes.get("darkness_code"),
                "arc_role": codes.get("arc_role"),
                "mixed_topic": bool(mixed_flags),
                "mixed_hypotheses": ",".join(mixed_flags),
                "lexical_context_agreement": ",".join(agree_flags),
                "review_status": (
                    "manual_review"
                    if review
                    else ("audited" if any(codes.values()) else "unaudited")
                ),
                "current_taxonomy_id": str(meta.get("taxonomy_main_id")),
                "current_taxonomy_name": meta.get("taxonomy_main_name"),
                "secondary_id": meta.get("taxonomy_secondary_id"),
                "secondary_name": meta.get("taxonomy_secondary_name"),
                "proposed_constructs": sorted(set(proposed)),
                "adjudication_actions": actions,
                # Diagnostics only — NOT used for cross-family W_tk
                "strict_weight": float(max(family_strict.values()) if family_strict else 0.0),
                "weighted_weight": float(
                    max(family_weighted_primary.values()) if family_weighted_primary else 0.0
                ),
                "family_proportions_json": json.dumps(family_props),
                "family_strict_json": json.dumps(family_strict),
                "manual_review_required": bool(review),
            }
        )

    return pd.DataFrame(rows)


def _parse_family_props(row: Mapping[str, Any], hyp: str) -> Dict[str, float]:
    raw = row.get("family_proportions_json")
    if isinstance(raw, dict):
        blob = raw
    elif isinstance(raw, str) and raw:
        try:
            blob = json.loads(raw)
        except json.JSONDecodeError:
            blob = {}
    else:
        blob = {}
    props = blob.get(hyp) or {}
    return {str(k): float(v) for k, v in props.items() if float(v) > 0}


def _emit_row(
    rows: List[Dict[str, Any]],
    *,
    tid: int,
    family: str,
    code: str,
    weight: float,
    mode: str,
) -> None:
    if weight <= 0 or _is_off_target(code):
        return
    rows.append(
        {
            "topic_id": int(tid),
            "construct_family": family,
            "construct_code": str(code),
            "weight": float(weight),
            "mode": mode,
        }
    )


def build_W_tk(
    master: pd.DataFrame,
    *,
    mode: str = "strict",
    dominance: float = 0.70,
    inclusive_secondary: float = INCLUSIVE_SECONDARY_WEIGHT,
    runner_floor: float = INCLUSIVE_RUNNER_FLOOR,
) -> pd.DataFrame:
    """Topic×construct weights — family-specific strict / weighted / inclusive."""
    rows: List[Dict[str, Any]] = []
    for _, r in master.iterrows():
        tid = int(r["topic_id"])
        for col, (hyp, family) in CODE_COL_META.items():
            primary = r.get(col)
            if primary is None or (isinstance(primary, float) and pd.isna(primary)):
                continue
            primary_s = str(primary)
            if primary_s in ("None", "nan", "UNKNOWN"):
                continue
            primary_canon = normalize_code(primary_s) or primary_s
            props = _parse_family_props(r, hyp)

            if mode == "strict":
                if _is_off_target(primary_canon):
                    continue
                share = props.get(primary_canon, 0.0)
                props_mass = sum(props.values()) if props else 0.0
                # Vacuous / unreliable Pass B (empty or tiny total mass): Pass C primary
                # is authoritative — admit as fully dominant rather than exclude on noise.
                if props_mass < 0.50:
                    share = 1.0
                if share >= dominance:
                    _emit_row(
                        rows, tid=tid, family=family, code=primary_canon, weight=1.0, mode=mode
                    )

            elif mode == "weighted":
                emitted_primary = False
                if props:
                    for code, share in props.items():
                        _emit_row(
                            rows, tid=tid, family=family, code=code, weight=share, mode=mode
                        )
                        if code == primary_canon:
                            emitted_primary = True
                # Always retain adjudicated primary even when Pass B proportions omit it
                # (Pass C override / vacuous Pass B).
                if not _is_off_target(primary_canon) and not emitted_primary:
                    fallback = 0.85 if props else 1.0
                    _emit_row(
                        rows,
                        tid=tid,
                        family=family,
                        code=primary_canon,
                        weight=fallback,
                        mode=mode,
                    )

            else:  # inclusive
                if not _is_off_target(primary_canon):
                    _emit_row(
                        rows, tid=tid, family=family, code=primary_canon, weight=1.0, mode=mode
                    )
                # Secondary: Pass B runners-up above floor (excluding primary)
                for code, share in props.items():
                    if code == primary_canon:
                        continue
                    if share >= runner_floor:
                        _emit_row(
                            rows,
                            tid=tid,
                            family=family,
                            code=code,
                            weight=inclusive_secondary,
                            mode=mode,
                        )
                # Also honour proposed_constructs from adjudication when present
                proposed = r.get("proposed_constructs") or []
                if isinstance(proposed, str):
                    try:
                        proposed = json.loads(proposed)
                    except json.JSONDecodeError:
                        proposed = [proposed]
                for raw in proposed:
                    canon = normalize_code(raw) or str(raw)
                    if canon == primary_canon or _is_off_target(canon):
                        continue
                    # Only add if it belongs to this family's code prefix
                    prefixes = {
                        "H1": "I",
                        "H2": "H2_",
                        "H3": "S",
                        "H4": "H4_",
                        "H5": "D",
                        "H6": "ARC_",
                    }
                    pref = prefixes[hyp]
                    if not str(canon).startswith(pref):
                        continue
                    _emit_row(
                        rows,
                        tid=tid,
                        family=family,
                        code=canon,
                        weight=inclusive_secondary,
                        mode=mode,
                    )

    # H5 bridging: darkness anchors + tenderness from H1/H4
    rows.extend(_h5_bridge_rows(master, mode=mode, dominance=dominance))

    if not rows:
        return pd.DataFrame(
            columns=["topic_id", "construct_family", "construct_code", "weight", "mode"]
        )
    out = pd.DataFrame(rows)
    # Deduplicate: same topic/family/code → max weight
    out = out.groupby(
        ["topic_id", "construct_family", "construct_code", "mode"], as_index=False
    )["weight"].max()
    return out


def _h5_bridge_rows(
    master: pd.DataFrame,
    *,
    mode: str,
    dominance: float,
) -> List[Dict[str, Any]]:
    """Inject 7.2/4.4 darkness anchors and H1/H4 tenderness into H5 constructs."""
    rows: List[Dict[str, Any]] = []
    for _, r in master.iterrows():
        tid = int(r["topic_id"])
        leaf = str(r.get("current_taxonomy_id") or "")
        # Darkness anchors from skip_full_relabel leaves
        if leaf in H5_DARKNESS_ANCHOR_LEAVES:
            _emit_row(
                rows,
                tid=tid,
                family="darkness_bridge",
                code="D1",
                weight=1.0,
                mode=mode,
            )

        # Tenderness from H1
        h1 = r.get("intimacy_code")
        h1_c = normalize_code(h1) if h1 is not None and not (isinstance(h1, float) and pd.isna(h1)) else None
        if h1_c and h1_c in H5_TENDERNESS_H1_CODES:
            props = _parse_family_props(r, "H1")
            share = props.get(h1_c, 0.0)
            if mode == "strict":
                if share >= dominance or (share <= 0 and not props):
                    _emit_row(
                        rows,
                        tid=tid,
                        family="tenderness_bridge",
                        code="D5",
                        weight=1.0,
                        mode=mode,
                    )
            elif mode == "weighted":
                w = share if share > 0 else (1.0 if not props else 0.0)
                if w > 0:
                    _emit_row(
                        rows,
                        tid=tid,
                        family="tenderness_bridge",
                        code="D5",
                        weight=w,
                        mode=mode,
                    )
            else:
                _emit_row(
                    rows,
                    tid=tid,
                    family="tenderness_bridge",
                    code="D5",
                    weight=1.0,
                    mode=mode,
                )

        # Tenderness from H4
        h4 = r.get("care_protection_code")
        h4_c = (
            normalize_code(h4)
            if h4 is not None and not (isinstance(h4, float) and pd.isna(h4))
            else None
        )
        if h4_c and h4_c in H5_TENDERNESS_H4_CODES:
            props = _parse_family_props(r, "H4")
            share = props.get(h4_c, 0.0)
            if mode == "strict":
                if share >= dominance or (share <= 0 and not props):
                    _emit_row(
                        rows,
                        tid=tid,
                        family="tenderness_bridge",
                        code="D5",
                        weight=1.0,
                        mode=mode,
                    )
            elif mode == "weighted":
                w = share if share > 0 else (1.0 if not props else 0.0)
                if w > 0:
                    _emit_row(
                        rows,
                        tid=tid,
                        family="tenderness_bridge",
                        code="D5",
                        weight=w,
                        mode=mode,
                    )
            else:
                _emit_row(
                    rows,
                    tid=tid,
                    family="tenderness_bridge",
                    code="D5",
                    weight=1.0,
                    mode=mode,
                )
    return rows


def build_W_tkr_from_h6(cfg: Stage11Config) -> pd.DataFrame:
    """Topic × construct × tertile weights from H6 Pass B proportions_by_tertile."""
    rows = []
    for row in load_jsonl(audit_dir(cfg, "H6") / PASS_FILES["B"]):
        tid = int(row["topic_id"])
        resp = row.get("response") or {}
        by_t = resp.get("proportions_by_tertile") or {}
        dominant = str(row.get("code") or resp.get("dominant_code") or "ARC_10")
        if not by_t:
            props = resp.get("proportions")
            if not isinstance(props, dict):
                props = {dominant: 0.7}
            by_t = {t: props for t in TERTILES}
        for tertile, props in by_t.items():
            if not isinstance(props, dict):
                continue
            tname = str(tertile)
            if tname in ("1", "begin", "start"):
                tname = "begin"
            elif tname in ("2", "middle", "mid"):
                tname = "middle"
            elif tname in ("3", "end", "final"):
                tname = "end"
            for code, share in props.items():
                try:
                    w = float(share)
                except (TypeError, ValueError):
                    continue
                canon = normalize_code(code) or str(code)
                rows.append(
                    {
                        "topic_id": tid,
                        "tertile": tname,
                        "construct_code": canon,
                        "weight": w,
                    }
                )
    return pd.DataFrame(rows)


def write_master_artifacts(cfg: Stage11Config) -> Dict[str, Path]:
    out_dir = cfg.output_path("constructs_dir", create=True)
    master = build_master_annotations(cfg)
    master = apply_h4_manual_freeze_to_master(master, cfg)
    master_path = out_dir / "master_annotations.parquet"
    master.to_parquet(master_path, index=False)
    (out_dir / "master_annotations.json").write_text(
        master.to_json(orient="records", indent=2),
        encoding="utf-8",
    )

    dominance = float(cfg.section("weights", "strict_dominance"))
    paths: Dict[str, Path] = {"master": master_path}
    for mode in ("strict", "weighted", "inclusive"):
        w = build_W_tk(master, mode=mode, dominance=dominance)
        p = out_dir / f"W_tk_{mode}.parquet"
        w.to_parquet(p, index=False)
        paths[f"W_tk_{mode}"] = p

    wtkr = build_W_tkr_from_h6(cfg)
    wtkr_path = out_dir / "W_tkr.parquet"
    wtkr.to_parquet(wtkr_path, index=False)
    paths["W_tkr"] = wtkr_path

    # Coverage for measurement gates
    coverage = _construct_coverage(master, paths)
    cov_path = out_dir / "construct_coverage.json"
    cov_path.write_text(json.dumps(coverage, indent=2), encoding="utf-8")
    paths["coverage"] = cov_path

    freeze = {
        "run_id": cfg.run_id,
        "n_topics": int(len(master)),
        "n_audited": int((master["review_status"] == "audited").sum()),
        "n_manual_review": int(master["manual_review_required"].sum()),
        "code_coverage": {
            col: int(master[col].notna().sum())
            for col in (
                "intimacy_code",
                "hea_code",
                "security_code",
                "care_protection_code",
                "darkness_code",
                "arc_role",
            )
        },
        "construct_coverage": coverage,
        "paths": {k: str(v.relative_to(cfg.root)) for k, v in paths.items()},
        "frozen": True,
        "weight_design": "family_specific_v2",
    }
    freeze_path = out_dir / "dictionary_freeze.json"
    freeze_path.write_text(json.dumps(freeze, indent=2), encoding="utf-8")
    paths["freeze"] = freeze_path
    LOGGER.info(
        "Master table: %d topics (%d audited) → %s",
        freeze["n_topics"],
        freeze["n_audited"],
        master_path,
    )
    return paths


def _construct_coverage(
    master: pd.DataFrame, paths: Mapping[str, Path]
) -> Dict[str, Any]:
    """Count mapped topics per construct family under strict W_tk (+ bridges)."""
    from src.stage11_refined_construct_analysis.analysis.constructs import (
        CODE_TO_RAX,
        COMPOSITE_DEFS,
        all_rax_atoms,
        rax_for_code,
    )

    w_path = paths.get("W_tk_strict")
    if w_path is None or not w_path.exists():
        return {}
    w = pd.read_parquet(w_path)
    # Expand codes → RAX atoms
    atom_topics: Dict[str, Set[int]] = {a: set() for a in all_rax_atoms()}
    for _, r in w.iterrows():
        if float(r.get("weight") or 0) <= 0:
            continue
        tid = int(r["topic_id"])
        for rax in rax_for_code(str(r["construct_code"])):
            atom_topics.setdefault(rax, set()).add(tid)

    def gate(n: int) -> str:
        if n <= 0:
            return "unmeasurable"
        if n <= 2:
            return "thin"
        return "viable"

    atoms = {
        k: {"n_topics": len(v), "gate": gate(len(v)), "topic_ids": sorted(v)}
        for k, v in sorted(atom_topics.items())
    }
    composites: Dict[str, Any] = {}
    for name, parts in COMPOSITE_DEFS.items():
        tids: Set[int] = set()
        for p in parts:
            tids |= atom_topics.get(p, set())
        composites[name] = {
            "n_topics": len(tids),
            "gate": gate(len(tids)),
            "topic_ids": sorted(tids),
            "parts": parts,
        }
    # Log-ratio sides
    ratios = {
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
    ratio_gates: Dict[str, Any] = {}
    for rname, (num, den) in ratios.items():
        n_n = composites.get(num, {}).get("n_topics", 0)
        n_d = composites.get(den, {}).get("n_topics", 0)
        if n_n <= 0 or n_d <= 0:
            g = "unmeasurable"
        elif n_n <= 2 or n_d <= 2:
            g = "thin"
        else:
            g = "viable"
        ratio_gates[rname] = {
            "gate": g,
            "numerator_topics": n_n,
            "denominator_topics": n_d,
        }
    return {"atoms": atoms, "composites": composites, "ratios": ratio_gates}
