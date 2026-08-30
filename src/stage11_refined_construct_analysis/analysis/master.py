"""Build Stage 11 master annotation table + W_tk / W_tkr weights."""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import pandas as pd

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
    """Extract dominant-code share from Pass B proportions (dict preferred).

    Live Nemo responses sometimes return lists/bools instead of {code: float};
    treat those as missing so the caller can apply the lexical fallback.
    """
    if isinstance(proportions, dict):
        try:
            return float(proportions.get(code, 0.0) or 0.0)
        except (TypeError, ValueError):
            return 0.0
    return 0.0


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
    reps = packet.get("lexical", {}).get("representations", {}) or {}
    return {
        "main": list(reps.get("Main") or []),
        "keybert": list(reps.get("KeyBERT") or []),
        "pos": list(reps.get("POS") or []),
        "mmr": list(reps.get("MMR") or []),
    }


def _main_couple_probs(row_b: Optional[Mapping[str, Any]], row_c: Optional[Mapping[str, Any]]) -> Tuple[float, float, float]:
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

    rows: List[Dict[str, Any]] = []
    for tid in sorted(topic_ids):
        lu = lookup.loc[lookup["topic_id"] == tid]
        if lu.empty:
            continue
        meta = lu.iloc[0]
        packet = load_evidence_packet(cfg, tid)
        kws = _keyword_lists(packet)

        codes = {}
        mixed_flags = []
        agree_flags = []
        actions = []
        proposed: List[str] = []
        review = False
        for hyp in HYPOTHESES:
            a = by_hyp[hyp]["A"].get(tid)
            b = by_hyp[hyp]["B"].get(tid)
            c = by_hyp[hyp]["C"].get(tid)
            if not any((a, b, c)):
                codes[CODE_FIELD[hyp]] = None
                continue
            code_a = _code_from_row(a, hyp) if a else None
            code_b = _code_from_row(b, hyp) if b else None
            code_c = _code_from_row(c, hyp) if c else (code_b or code_a)
            codes[CODE_FIELD[hyp]] = code_c
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

        mc, nc, uc = _main_couple_probs(
            by_hyp["H6"]["B"].get(tid) or by_hyp["H5"]["B"].get(tid),
            by_hyp["H6"]["C"].get(tid) or by_hyp["H5"]["C"].get(tid),
        )

        # Contextual share for weighted weight: prefer Pass B proportions of dominant code
        strict_w = 0.0
        weighted_w = 0.0
        for hyp in HYPOTHESES:
            c = by_hyp[hyp]["C"].get(tid)
            b = by_hyp[hyp]["B"].get(tid)
            if not c and not b:
                continue
            code = codes[CODE_FIELD[hyp]]
            if not code or code in ("MIXED", "UNKNOWN", None):
                continue
            props = ((b or {}).get("response") or {}).get("proportions")
            share = _share_for_code(props, str(code))
            if share <= 0 and code != "MIXED":
                share = 0.85  # lexical-only fallback when Pass B vacuous historically
            if share >= dominance:
                strict_w = max(strict_w, 1.0)
            weighted_w = max(weighted_w, share)

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
                "review_status": "manual_review" if review else ("audited" if any(codes.values()) else "unaudited"),
                "current_taxonomy_id": str(meta.get("taxonomy_main_id")),
                "current_taxonomy_name": meta.get("taxonomy_main_name"),
                "secondary_id": meta.get("taxonomy_secondary_id"),
                "secondary_name": meta.get("taxonomy_secondary_name"),
                "proposed_constructs": sorted(set(proposed)),
                "adjudication_actions": actions,
                "strict_weight": float(strict_w),
                "weighted_weight": float(weighted_w),
                "manual_review_required": bool(review),
            }
        )

    return pd.DataFrame(rows)


def build_W_tk(master: pd.DataFrame, *, mode: str = "strict") -> pd.DataFrame:
    """Topic×construct weights from master codes.

    mode: strict | weighted | inclusive
    Returns long frame: topic_id, construct, weight
    """
    construct_maps = {
        "intimacy_code": "intimacy",
        "hea_code": "hea",
        "security_code": "security",
        "care_protection_code": "care_protection",
        "darkness_code": "darkness",
        "arc_role": "arc",
    }
    rows = []
    for _, r in master.iterrows():
        for col, family in construct_maps.items():
            code = r.get(col)
            if code is None or (isinstance(code, float) and pd.isna(code)):
                continue
            code_s = str(code)
            if code_s in ("None", "nan", "UNKNOWN"):
                continue
            if mode == "strict":
                w = float(r.get("strict_weight") or 0.0)
                if code_s == "MIXED":
                    w = 0.0
                elif w <= 0 and code_s not in ("MIXED",):
                    # audited but proportions missing: keep if not mixed
                    w = 1.0 if r.get("review_status") == "audited" else 0.0
            elif mode == "weighted":
                w = float(r.get("weighted_weight") or 0.0)
                if w <= 0 and code_s != "MIXED":
                    w = 0.5
                if code_s == "MIXED":
                    w = 0.0
            else:  # inclusive
                w = 1.0 if code_s != "MIXED" else 0.25
            rows.append(
                {
                    "topic_id": int(r["topic_id"]),
                    "construct_family": family,
                    "construct_code": code_s,
                    "weight": float(w),
                    "mode": mode,
                }
            )
    return pd.DataFrame(rows)


def build_W_tkr_from_h6(cfg: Stage11Config) -> pd.DataFrame:
    """Topic × construct × tertile weights from H6 Pass B proportions_by_tertile."""
    rows = []
    for row in load_jsonl(audit_dir(cfg, "H6") / PASS_FILES["B"]):
        tid = int(row["topic_id"])
        resp = row.get("response") or {}
        by_t = resp.get("proportions_by_tertile") or {}
        # Fallback: same dominant code mass split equally if tertile detail missing
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
                rows.append(
                    {
                        "topic_id": tid,
                        "tertile": tname,
                        "construct_code": str(code),
                        "weight": w,
                    }
                )
    return pd.DataFrame(rows)


def write_master_artifacts(cfg: Stage11Config) -> Dict[str, Path]:
    out_dir = cfg.output_path("constructs_dir", create=True)
    master = build_master_annotations(cfg)
    master_path = out_dir / "master_annotations.parquet"
    master.to_parquet(master_path, index=False)
    (out_dir / "master_annotations.json").write_text(
        master.to_json(orient="records", indent=2),
        encoding="utf-8",
    )

    paths = {"master": master_path}
    for mode in ("strict", "weighted", "inclusive"):
        w = build_W_tk(master, mode=mode)
        p = out_dir / f"W_tk_{mode}.parquet"
        w.to_parquet(p, index=False)
        paths[f"W_tk_{mode}"] = p

    wtkr = build_W_tkr_from_h6(cfg)
    wtkr_path = out_dir / "W_tkr.parquet"
    wtkr.to_parquet(wtkr_path, index=False)
    paths["W_tkr"] = wtkr_path

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
        "paths": {k: str(v.relative_to(cfg.root)) for k, v in paths.items()},
        "frozen": True,
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
