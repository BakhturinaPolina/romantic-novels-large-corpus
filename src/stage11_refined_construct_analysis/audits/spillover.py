"""Spillover candidate discovery + cheap Nemo triage (before full Pass A/B/C)."""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set

import pandas as pd

from src.stage11_refined_construct_analysis.audits.llm import chat_json, load_dotenv_key, resolve_api_key
from src.stage11_refined_construct_analysis.audits.prompts import rep_lists
from src.stage11_refined_construct_analysis.config import (
    Stage11Config,
    load_prompt_yaml,
)
from src.stage11_refined_construct_analysis.evidence.packets import (
    lexical_block,
    load_topic_metadata,
    llm_view,
)
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup

LOGGER = logging.getLogger("stage11.spillover")

HYPOTHESIS_FOCUS = {
    "H1": "romantic intimacy / affection / sexual contact function",
    "H3": "emotional vs material/security / status-appearance function",
    "H4": "romantic protection / protective commitment vs possession-control",
}

H4_PROMOTE_FUNCTIONS = {
    "protective_commitment",
    "rescue_search",
    "physical_external_protection",
    "social_legal_external_protection",
}

H3_PROMOTE_FUNCTIONS = {
    "money_provision",
    "housing_provision",
}


def spillover_prompt_path(cfg: Stage11Config, hypothesis: Optional[str] = None) -> Path:
    hyp = str(hypothesis or "").upper()
    if hyp == "H4":
        configured = cfg.section("spillover", "h4_prompt", default=None)
    elif hyp == "H3":
        configured = cfg.section("spillover", "h3_prompt", default=None)
    else:
        configured = cfg.section("spillover", "prompt", default=None)
    if configured:
        path = Path(configured)
        if not path.is_absolute():
            path = cfg.root / path
        return path
    if hyp == "H4":
        return cfg.root / "configs" / "stage11" / "prompts" / "h4_spillover_triage.yaml"
    if hyp == "H3":
        return cfg.root / "configs" / "stage11" / "prompts" / "h3_spillover_triage.yaml"
    return cfg.root / "configs" / "stage11" / "prompts" / "spillover_triage.yaml"


def load_spillover_prompt(cfg: Stage11Config, hypothesis: Optional[str] = None) -> Dict[str, Any]:
    path = spillover_prompt_path(cfg, hypothesis)
    data = load_prompt_yaml(path)
    if not data.get("frozen", False):
        raise ValueError(f"Spillover prompt not frozen: {path}")
    return data


def _mandatory_ids(manifest: Mapping[str, Any]) -> Set[int]:
    return {
        int(e["topic_id"])
        for e in manifest.get("entries", [])
        if e.get("topic_id") is not None and e.get("role") == "mandatory"
    }


def _discovery_ids(manifest: Mapping[str, Any]) -> Set[int]:
    return {
        int(e["topic_id"])
        for e in manifest.get("entries", [])
        if e.get("topic_id") is not None and e.get("role") == "spillover_discovery"
    }


def build_h1_spillover_candidates(
    cfg: Stage11Config,
    lookup: pd.DataFrame,
    manifest: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    """Secondary-in-mandatory + sexual flags outside the H1 mandatory pool."""
    hyp_cfg = cfg.section("hypotheses", "H1")
    mandatory_leaves = set(str(x) for x in hyp_cfg.get("mandatory_leaves", []) or [])
    already = _mandatory_ids(manifest)
    sexual_vals = set(
        str(x).lower()
        for x in cfg.section("spillover", "h1_sexual_explicitness", default=["explicit", "suggestive"])
    )
    function_vals = set(
        str(x).lower()
        for x in cfg.section(
            "spillover",
            "h1_sexual_functions",
            default=["explicit_contact", "erotic_tension", "affection"],
        )
    )
    max_n = int(cfg.section("spillover", "h1_max_candidates", default=40))

    rows: List[Dict[str, Any]] = []
    for r in lookup.itertuples():
        tid = int(r.topic_id)
        if tid in already or tid < 0:
            continue
        main = str(getattr(r, "taxonomy_main_id", "") or "")
        secondary = getattr(r, "taxonomy_secondary_id", None)
        secondary_s = str(secondary) if secondary is not None and str(secondary) not in ("", "None", "nan") else None
        sex = str(getattr(r, "sexual_explicitness", "") or "").lower()
        func = str(getattr(r, "sexual_function", "") or "").lower()
        reasons = []
        if secondary_s and secondary_s in mandatory_leaves:
            reasons.append(f"secondary_in_{secondary_s}")
        if sex in sexual_vals and main not in mandatory_leaves:
            reasons.append(f"sexual_explicitness={sex}")
        if func in function_vals and main not in mandatory_leaves:
            reasons.append(f"sexual_function={func}")
        if not reasons:
            continue
        rows.append(
            {
                "topic_id": tid,
                "taxonomy_main_id": main,
                "taxonomy_secondary_id": secondary_s,
                "sexual_explicitness": sex or None,
                "sexual_function": func or None,
                "heuristic_notes": "; ".join(reasons),
                "source": "h1_secondary_or_sexual_flags",
            }
        )

    # Prefer secondary hits, then sexual flags; stable sort by topic_id
    rows.sort(key=lambda x: (0 if "secondary_in_" in x["heuristic_notes"] else 1, x["topic_id"]))
    return rows[:max_n]


def _proto_pattern(token: str) -> re.Pattern[str]:
    """Word-boundary regex for a lexical prototype (supports multi-word phrases)."""
    parts = [re.escape(p) for p in str(token).lower().split() if p]
    if not parts:
        return re.compile(r"(?!)")
    return re.compile(r"\b" + r"\s+".join(parts) + r"\b")


def _lexical_hits(blob: str, prototypes: Sequence[str]) -> List[str]:
    hits: List[str] = []
    for p in prototypes:
        p = str(p).strip().lower()
        if not p:
            continue
        if _proto_pattern(p).search(blob):
            hits.append(p)
    return hits


def _load_already_material_topic_ids(cfg: Stage11Config) -> Set[int]:
    """Strict S8/S9 topic IDs already in construct coverage (skip LLM triage bill)."""
    out: Set[int] = set()
    for tid in cfg.section("spillover", "h3_already_strict_material_topic_ids", default=[]) or []:
        out.add(int(tid))
    cov_path = cfg.output_path("constructs_dir") / "construct_coverage.json"
    if cov_path.exists():
        try:
            cov = json.loads(cov_path.read_text(encoding="utf-8"))
            atoms = cov.get("atoms") or cov
            for key in ("RAX_material_provision", "RAX_housing_security"):
                block = atoms.get(key) or {}
                for tid in block.get("topic_ids") or []:
                    out.add(int(tid))
            # Composites may nest under a different key
            composites = cov.get("composites") or {}
            for key in ("RAX_h3_material_side",):
                block = composites.get(key) or {}
                for tid in block.get("topic_ids") or []:
                    out.add(int(tid))
        except Exception as exc:
            LOGGER.warning("Could not read already-material from coverage: %s", exc)
    if not out:
        # Fallback: master security_code in {S8, S9}
        master_path = cfg.output_path("constructs_dir") / "master_annotations.parquet"
        if master_path.exists():
            try:
                master = pd.read_parquet(master_path)
                if "topic_id" in master.columns and "security_code" in master.columns:
                    codes = master["security_code"].astype(str).str.upper()
                    mask = codes.isin({"S8", "S9"})
                    out.update(int(t) for t in master.loc[mask, "topic_id"].tolist())
            except Exception as exc:
                LOGGER.warning("Could not read already-material from master: %s", exc)
    return out


def build_h3_spillover_candidates(
    cfg: Stage11Config,
    lookup: pd.DataFrame,
    manifest: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    """Full-corpus multi-signal H3 material-provision candidate generation."""
    discovery_leaves = {
        str(x)
        for x in (
            cfg.section("hypotheses", "H3").get("spillover_discovery_leaves") or []
        )
    }
    tags_want = {
        str(x).lower()
        for x in cfg.section(
            "spillover",
            "h3_mechanic_tags",
            default=["economic_power", "domestic_care"],
        )
    }
    core_protos = [
        str(x).lower()
        for x in cfg.section("spillover", "h3_lexical_prototypes", default=[])
    ]
    weak_protos = [
        str(x).lower()
        for x in cfg.section("spillover", "h3_weak_lexical_prototypes", default=[])
    ]
    max_n = int(cfg.section("spillover", "h3_max_candidates", default=40))
    already_material = _load_already_material_topic_ids(cfg)

    rows: List[Dict[str, Any]] = []
    for r in lookup.itertuples():
        tid = int(r.topic_id)
        if tid < 0 or tid in already_material:
            continue
        main = str(getattr(r, "taxonomy_main_id", "") or "")
        secondary = getattr(r, "taxonomy_secondary_id", None)
        secondary_s = (
            str(secondary)
            if secondary is not None and str(secondary) not in ("", "None", "nan")
            else None
        )
        reasons: List[str] = []
        types: Set[str] = set()
        tags = _parse_mechanic_tags(getattr(r, "taxonomy_mechanic_tags", None))
        if tags & tags_want:
            reasons.append("mechanic:" + ",".join(sorted(tags & tags_want)))
            types.add("mechanic")
        if main in discovery_leaves:
            reasons.append(f"primary_leaf={main}")
            types.add("leaf")
        if secondary_s and secondary_s in discovery_leaves:
            reasons.append(f"secondary_leaf={secondary_s}")
            types.add("leaf")
        blob = _lookup_text_blob(
            {
                "label": getattr(r, "label", None),
                "scene_summary": getattr(r, "scene_summary", None),
                "all_keywords": getattr(r, "all_keywords", None),
                "keywords": getattr(r, "keywords", None),
                "label_rationale": getattr(r, "label_rationale", None),
            }
        )
        core_hits = _lexical_hits(blob, core_protos)
        if core_hits:
            reasons.append("proto:" + ",".join(core_hits[:6]))
            types.add("proto")
        weak_hits = _lexical_hits(blob, weak_protos)
        # Weak lexical alone does not qualify; needs another signal type.
        if weak_hits and types:
            reasons.append("weak_proto:" + ",".join(weak_hits[:4]))
            types.add("weak_proto")
        if not types:
            continue
        # Weak-only should never reach here; if somehow only weak_proto, drop.
        if types == {"weak_proto"}:
            continue
        rows.append(
            {
                "topic_id": tid,
                "taxonomy_main_id": main,
                "taxonomy_secondary_id": secondary_s,
                "sexual_explicitness": getattr(r, "sexual_explicitness", None),
                "sexual_function": getattr(r, "sexual_function", None),
                "heuristic_notes": "; ".join(reasons),
                "n_signals": len(types),
                "source": "h3_full_corpus_material_discovery",
            }
        )

    rows.sort(key=lambda x: (-int(x.get("n_signals") or 0), int(x["topic_id"])))
    return rows[:max_n]


def _parse_mechanic_tags(raw: object) -> Set[str]:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return set()
    if isinstance(raw, (list, tuple, set)):
        return {str(x).strip().lower() for x in raw if str(x).strip()}
    s = str(raw).strip()
    if not s:
        return set()
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return {str(x).strip().lower() for x in parsed if str(x).strip()}
    except Exception:
        pass
    return {x.strip().lower() for x in re.split(r"[,;|]", s) if x.strip()}


def _lookup_text_blob(row: Mapping[str, Any]) -> str:
    parts: List[str] = []
    for key in (
        "label",
        "scene_summary",
        "all_keywords",
        "keywords",
        "label_rationale",
    ):
        val = row.get(key)
        if val is None or (isinstance(val, float) and pd.isna(val)):
            continue
        if isinstance(val, (list, tuple)):
            parts.append(" ".join(str(x) for x in val))
        else:
            parts.append(str(val))
    # Four keyword representations if stored as dict/json
    for key in ("keyword_reps", "representations", "representation_keywords"):
        val = row.get(key)
        if isinstance(val, dict):
            for v in val.values():
                if isinstance(v, (list, tuple)):
                    parts.append(" ".join(str(x) for x in v))
                else:
                    parts.append(str(v))
        elif isinstance(val, str) and val.strip().startswith("{"):
            try:
                d = json.loads(val)
                if isinstance(d, dict):
                    for v in d.values():
                        if isinstance(v, (list, tuple)):
                            parts.append(" ".join(str(x) for x in v))
                        else:
                            parts.append(str(v))
            except Exception:
                parts.append(val)
    return " ".join(parts).lower()


def _load_h5_d3_topic_ids(cfg: Stage11Config) -> Set[int]:
    """Topic IDs coded D3 in the live H5 adjudication / master table."""
    out: Set[int] = set()
    master_path = cfg.output_path("constructs_dir") / "master_annotations.parquet"
    if master_path.exists():
        try:
            master = pd.read_parquet(master_path, columns=["topic_id", "darkness_code"])
            mask = master["darkness_code"].astype(str).str.upper().str.startswith("D3")
            out.update(int(t) for t in master.loc[mask, "topic_id"].tolist())
        except Exception as exc:
            LOGGER.warning("Could not read H5 D3 from master: %s", exc)
    # Also scan live H5 adjudication jsonl
    h5_path = cfg.output_path("audits_dir") / "h5" / "adjudication.jsonl"
    if h5_path.exists():
        for line in h5_path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            code = str(row.get("code") or "")
            resp = row.get("response") or {}
            dark = str(resp.get("darkness_code") or code)
            if dark.upper().startswith("D3"):
                out.add(int(row["topic_id"]))
    return out


def build_h4_spillover_candidates(
    cfg: Stage11Config,
    lookup: pd.DataFrame,
    manifest: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    """Full-corpus multi-signal H4 candidate generation (high recall, pre-triage)."""

    already = _mandatory_ids(manifest)
    discovery_leaves = {
        str(x)
        for x in (
            cfg.section("hypotheses", "H4").get("spillover_discovery_leaves") or []
        )
    }
    tags_want = {
        str(x).lower()
        for x in cfg.section(
            "spillover",
            "h4_mechanic_tags",
            default=["protective_care", "external_threat"],
        )
    }
    prototypes = [
        str(x).lower()
        for x in cfg.section("spillover", "h4_lexical_prototypes", default=[])
    ]
    promise_toks = [
        str(x).lower() for x in cfg.section("spillover", "h4_promise_tokens", default=[])
    ]
    threat_toks = [
        str(x).lower() for x in cfg.section("spillover", "h4_threat_tokens", default=[])
    ]
    max_n = int(cfg.section("spillover", "h4_max_candidates", default=80))
    d3_ids = _load_h5_d3_topic_ids(cfg)

    rows: List[Dict[str, Any]] = []
    for r in lookup.itertuples():
        tid = int(r.topic_id)
        if tid in already or tid < 0:
            continue
        main = str(getattr(r, "taxonomy_main_id", "") or "")
        secondary = getattr(r, "taxonomy_secondary_id", None)
        secondary_s = (
            str(secondary)
            if secondary is not None and str(secondary) not in ("", "None", "nan")
            else None
        )
        reasons: List[str] = []
        tags = _parse_mechanic_tags(getattr(r, "taxonomy_mechanic_tags", None))
        if tags & tags_want:
            reasons.append("mechanic:" + ",".join(sorted(tags & tags_want)))
        if tid in d3_ids:
            reasons.append("h5_d3")
        if main in discovery_leaves:
            reasons.append(f"primary_leaf={main}")
        if secondary_s and secondary_s in discovery_leaves:
            reasons.append(f"secondary_leaf={secondary_s}")
        blob = _lookup_text_blob(
            {
                "label": getattr(r, "label", None),
                "scene_summary": getattr(r, "scene_summary", None),
                "all_keywords": getattr(r, "all_keywords", None),
                "keywords": getattr(r, "keywords", None),
                "label_rationale": getattr(r, "label_rationale", None),
            }
        )
        proto_hits = [p for p in prototypes if p and p in blob]
        if proto_hits:
            reasons.append("proto:" + ",".join(proto_hits[:6]))
        threatish = any(t and t in blob for t in threat_toks)
        promiseish = any(t and t in blob for t in promise_toks)
        if threatish and promiseish:
            reasons.append("threat+promise")
        if not reasons:
            continue
        types = set()
        for note in reasons:
            if note.startswith("mechanic"):
                types.add("mechanic")
            elif note.startswith("h5_d3"):
                types.add("d3")
            elif note.startswith("primary_leaf") or note.startswith("secondary_leaf"):
                types.add("leaf")
            elif note.startswith("proto"):
                types.add("proto")
            elif note.startswith("threat+promise"):
                types.add("threat+promise")
        rows.append(
            {
                "topic_id": tid,
                "taxonomy_main_id": main,
                "taxonomy_secondary_id": secondary_s,
                "sexual_explicitness": getattr(r, "sexual_explicitness", None),
                "sexual_function": getattr(r, "sexual_function", None),
                "heuristic_notes": "; ".join(reasons),
                "n_signals": len(types),
                "source": "h4_full_corpus_discovery",
            }
        )

    rows.sort(key=lambda x: (-int(x.get("n_signals") or 0), int(x["topic_id"])))
    return rows[:max_n]


def format_spillover_messages(
    prompt: Mapping[str, Any],
    *,
    hypothesis: str,
    hypothesis_name: str,
    construct_focus: str,
    packet: Mapping[str, Any],
    flags: Mapping[str, Any],
) -> Dict[str, str]:
    block = prompt["phrasing"]["primary"]
    reps = rep_lists(packet)
    fmt = {
        "hypothesis": hypothesis,
        "hypothesis_name": hypothesis_name,
        "construct_focus": construct_focus,
        "topic_id": packet["topic_id"],
        "main": reps["main"],
        "keybert": reps["keybert"],
        "pos": reps["pos"],
        "mmr": reps["mmr"],
        "secondary_leaf": flags.get("taxonomy_secondary_id") or "(none)",
        "sexual_explicitness": flags.get("sexual_explicitness") or "(none)",
        "sexual_function": flags.get("sexual_function") or "(none)",
        "heuristic_notes": flags.get("heuristic_notes") or "(none)",
    }
    return {
        "system": block["system"].strip(),
        "user": block["user"].format(**fmt).strip(),
    }


def _dry_run_spillover(topic_id: int, hypothesis: str, flags: Mapping[str, Any]) -> Dict[str, Any]:
    """Deterministic triage for dry-run / missing API key."""
    notes = str(flags.get("heuristic_notes") or "")
    if hypothesis == "H1":
        include = "secondary_in_" in notes or (int(topic_id) % 3 != 0)
        return {
            "topic_id": int(topic_id),
            "include": include,
            "confidence": 0.7 if include else 0.4,
            "suggested_code_family": "intimacy",
            "rationale": f"dry-run spillover {hypothesis}",
            "dry_run": True,
        }
    if hypothesis == "H4":
        n_sig = int(flags.get("n_signals") or 0)
        promote = n_sig >= 2 or "h5_d3" in notes or "mechanic:" in notes
        return {
            "topic_id": int(topic_id),
            "external_threat": "unclear" if promote else "no",
            "protective_action": "unclear" if promote else "no",
            "main_couple_target": "unclear",
            "autonomy_effect": "unclear",
            "function": "rescue_search" if promote else "off_target",
            "promote_to_full_H4_audit": promote,
            "include": promote,
            "supporting_cues": [notes[:120]] if notes else [],
            "rationale": f"dry-run spillover {hypothesis}",
            "dry_run": True,
        }
    if hypothesis == "H3":
        n_sig = int(flags.get("n_signals") or 0)
        moneyish = any(
            tok in notes
            for tok in (
                "money",
                "bills",
                "debt",
                "pay for",
                "financial",
                "salary",
                "shelter",
                "housing",
                "rent",
                "economic_power",
            )
        )
        promote = n_sig >= 2 or moneyish or "proto:" in notes
        if promote and moneyish:
            func = "money_provision"
        elif promote and ("shelter" in notes or "housing" in notes):
            func = "housing_provision"
        elif promote:
            func = "money_provision"
        else:
            func = "off_target"
        return {
            "topic_id": int(topic_id),
            "relationship_directed_transfer": "unclear" if promote else "no",
            "provision_function": func,
            "main_couple_target": "unclear",
            "exclude_reason": "none" if promote else "objects_no_provision",
            "promote_to_full_H3_audit": promote,
            "include": promote,
            "supporting_cues": [notes[:120]] if notes else [],
            "rationale": f"dry-run spillover {hypothesis}",
            "dry_run": True,
        }
    include = int(topic_id) % 2 == 1
    return {
        "topic_id": int(topic_id),
        "include": include,
        "confidence": 0.7 if include else 0.4,
        "suggested_code_family": "security",
        "rationale": f"dry-run spillover {hypothesis}",
        "dry_run": True,
    }


def _h4_should_promote(parsed: Mapping[str, Any]) -> bool:
    """High-recall promotion rule for dedicated H4 spillover schema."""
    flagged = bool(parsed.get("promote_to_full_H4_audit", False))
    threat = str(parsed.get("external_threat") or "").lower()
    action = str(parsed.get("protective_action") or "").lower()
    func = str(parsed.get("function") or "").lower()
    rule = (threat in {"yes", "unclear"} and action in {"yes", "unclear"}) or (
        func in H4_PROMOTE_FUNCTIONS
    )
    return flagged or rule


def _h3_material_should_promote(parsed: Mapping[str, Any]) -> bool:
    """Promotion rule for dedicated H3 material-provision spillover schema."""
    flagged = bool(parsed.get("promote_to_full_H3_audit", False))
    transfer = str(parsed.get("relationship_directed_transfer") or "").lower()
    func = str(parsed.get("provision_function") or "").lower()
    rule = transfer in {"yes", "unclear"} and func in H3_PROMOTE_FUNCTIONS
    return flagged or rule


def run_spillover_triage(
    cfg: Stage11Config,
    hypothesis: str,
    candidates: Sequence[Mapping[str, Any]],
    *,
    packets: Optional[Mapping[int, Mapping[str, Any]]] = None,
    dry_run: bool = False,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Triage candidates with Nemo; return promoted topic ids + full rows."""
    hyp = str(hypothesis).upper()
    prompt = load_spillover_prompt(cfg, hyp)
    key = resolve_api_key(api_key) or load_dotenv_key()
    use_dry = bool(dry_run or not key)
    model = str(cfg.section("llm", "primary_model"))
    metadata = load_topic_metadata(cfg) if packets is None else None
    hyp_name = str(cfg.section("hypotheses", hyp).get("name", hyp))
    focus = HYPOTHESIS_FOCUS.get(hyp, hyp_name)

    rows_out: List[Dict[str, Any]] = []
    promoted: List[int] = []
    n_cand = len(candidates)
    t0 = time.time()

    for i, cand in enumerate(candidates, start=1):
        tid = int(cand["topic_id"])
        if packets and tid in packets:
            packet = packets[tid]
            view = llm_view(packet, pass_name="A")
        else:
            assert metadata is not None
            lexical = lexical_block(tid, metadata)
            view = {
                "topic_id": tid,
                "lexical": {
                    "representations": lexical["representations"],
                    "stage08_snippets": lexical.get("stage08_snippets", []),
                },
                "contextual": {"sentences": [], "books_sampled": []},
            }

        messages = format_spillover_messages(
            prompt,
            hypothesis=hyp,
            hypothesis_name=hyp_name,
            construct_focus=focus,
            packet=view,
            flags=cand,
        )
        dry_payload = _dry_run_spillover(tid, hyp, cand) if use_dry else None
        LOGGER.info(
            "[%d/%d] %s spillover topic %s (%.0fs elapsed)",
            i,
            n_cand,
            hyp,
            tid,
            time.time() - t0,
        )
        result = chat_json(
            model=model,
            system=messages["system"],
            user=messages["user"],
            temperature=float(cfg.section("llm", "temperature")),
            max_tokens=int(cfg.section("spillover", "max_tokens", default=400)),
            api_key=key,
            rate_limit_delay_s=float(cfg.section("llm", "rate_limit_delay_s")),
            dry_run_payload=dry_payload,
        )
        parsed = result["parsed"]
        if hyp == "H4":
            include = _h4_should_promote(parsed)
        elif hyp == "H3":
            include = _h3_material_should_promote(parsed)
        else:
            include = bool(parsed.get("include", False))
        row = {
            "hypothesis": hyp,
            "topic_id": tid,
            "include": include,
            "confidence": parsed.get("confidence"),
            "suggested_code_family": parsed.get("suggested_code_family")
            or parsed.get("function")
            or parsed.get("provision_function"),
            "rationale": parsed.get("rationale"),
            "candidate": dict(cand),
            "model": result["model"],
            "dry_run": result["dry_run"],
            "response": parsed,
        }
        rows_out.append(row)
        if include:
            promoted.append(tid)
        done = i
        elapsed = max(1e-3, time.time() - t0)
        rate = done / elapsed
        rem = (n_cand - done) / rate if rate > 0 else 0
        LOGGER.info(
            "  → include=%s  spillover ETA≈%.0fs (%.1f/min)",
            include,
            rem,
            rate * 60,
        )

    payload: Dict[str, Any] = {
        "hypothesis": hyp,
        "n_candidates": len(candidates),
        "n_promoted": len(promoted),
        "promoted_topic_ids": sorted(set(promoted)),
        "rows": rows_out,
        "dry_run": use_dry,
        "model": model,
        "prompt_version": str(prompt.get("version")),
    }
    if hyp == "H3":
        payload["already_material_topic_ids"] = sorted(_load_already_material_topic_ids(cfg))
    return payload


def write_spillover_result(cfg: Stage11Config, payload: Mapping[str, Any]) -> Path:
    out_dir = cfg.output_path("candidates_dir", create=True)
    hyp = str(payload["hypothesis"]).lower()
    path = out_dir / f"{hyp}_spillover.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    jsonl = cfg.output_path("audits_dir", create=True) / hyp / "spillover_triage.jsonl"
    jsonl.parent.mkdir(parents=True, exist_ok=True)
    jsonl.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in payload["rows"]) + "\n",
        encoding="utf-8",
    )
    return path


def load_spillover_promoted(cfg: Stage11Config, hypothesis: str) -> List[int]:
    path = cfg.output_path("candidates_dir") / f"{str(hypothesis).lower()}_spillover.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [int(t) for t in data.get("promoted_topic_ids", [])]
