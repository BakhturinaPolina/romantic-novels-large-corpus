"""Spillover candidate discovery + cheap Nemo triage (before full Pass A/B/C)."""

from __future__ import annotations

import json
import logging
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
}


def spillover_prompt_path(cfg: Stage11Config) -> Path:
    configured = cfg.section("spillover", "prompt", default=None)
    if configured:
        path = Path(configured)
        if not path.is_absolute():
            path = cfg.root / path
        return path
    return cfg.root / "configs" / "stage11" / "prompts" / "spillover_triage.yaml"


def load_spillover_prompt(cfg: Stage11Config) -> Dict[str, Any]:
    data = load_prompt_yaml(spillover_prompt_path(cfg))
    if not data.get("frozen", False):
        raise ValueError(f"Spillover prompt not frozen: {spillover_prompt_path(cfg)}")
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


def build_h3_spillover_candidates(
    cfg: Stage11Config,
    lookup: pd.DataFrame,
    manifest: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    """Triage pool = configured spillover_discovery leaves (already lookup-derived)."""
    discovery = _discovery_ids(manifest)
    leaf_of = {
        int(r.topic_id): str(r.taxonomy_main_id) for r in lookup.itertuples()
    }
    rows = []
    for tid in sorted(discovery):
        row = lookup.loc[lookup["topic_id"] == tid]
        if row.empty:
            continue
        r = row.iloc[0]
        secondary = r.get("taxonomy_secondary_id")
        secondary_s = (
            str(secondary)
            if secondary is not None and str(secondary) not in ("", "None", "nan")
            else None
        )
        rows.append(
            {
                "topic_id": int(tid),
                "taxonomy_main_id": leaf_of.get(tid),
                "taxonomy_secondary_id": secondary_s,
                "sexual_explicitness": r.get("sexual_explicitness"),
                "sexual_function": r.get("sexual_function"),
                "heuristic_notes": f"spillover_discovery_leaf={leaf_of.get(tid)}",
                "source": "h3_spillover_discovery_leaves",
            }
        )
    return rows


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
    """Deterministic triage: include secondary hits and discovery leaves with odd topic ids."""
    notes = str(flags.get("heuristic_notes") or "")
    if hypothesis == "H1":
        include = "secondary_in_" in notes or (int(topic_id) % 3 != 0)
    else:
        include = int(topic_id) % 2 == 1
    return {
        "topic_id": int(topic_id),
        "include": include,
        "confidence": 0.7 if include else 0.4,
        "suggested_code_family": "intimacy" if hypothesis == "H1" else "security",
        "rationale": f"dry-run spillover {hypothesis}",
        "dry_run": True,
    }


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
    prompt = load_spillover_prompt(cfg)
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
        include = bool(parsed.get("include", False))
        row = {
            "hypothesis": hyp,
            "topic_id": tid,
            "include": include,
            "confidence": parsed.get("confidence"),
            "suggested_code_family": parsed.get("suggested_code_family"),
            "rationale": parsed.get("rationale"),
            "candidate": dict(cand),
            "model": result["model"],
            "dry_run": result["dry_run"],
            "response": parsed,
        }
        rows_out.append(row)
        if include:
            promoted.append(tid)
        # Rolling ETA for remaining spillover candidates
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

    return {
        "hypothesis": hyp,
        "n_candidates": len(candidates),
        "n_promoted": len(promoted),
        "promoted_topic_ids": sorted(set(promoted)),
        "rows": rows_out,
        "dry_run": use_dry,
        "model": model,
        "prompt_version": str(prompt.get("version")),
    }


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
