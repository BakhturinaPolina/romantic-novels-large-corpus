"""Single-pass LLM coding for EES exploratory families (rating-blind)."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

import pandas as pd

from src.stage11_refined_construct_analysis.analysis.ees_discovery import (
    FAMILY_KEYS,
    ees_output_dir,
    load_ees_config,
    load_stage11_from_ees,
)
from src.stage11_refined_construct_analysis.audits.llm import (
    chat_json,
    load_dotenv_key,
    resolve_api_key,
)
from src.stage11_refined_construct_analysis.config import (  # noqa: E501
    Stage11Config,
    load_prompt_yaml,
)
from src.stage11_refined_construct_analysis.evidence.packets import (
    REP_NAMES,
    lexical_block,
    load_representative_docs,
    load_topic_metadata,
)
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup

LOGGER = logging.getLogger("stage11.ees_coding")

# Map discovery family → prompt config key
FAMILY_PROMPT_KEY = {
    "emotion_embodiment": "emotion",  # dual-coded: run emotion then embodiment
    "family_social": "social",
    "cognition_screen": "cognition",
    "work_screen": "work",
}

# emotion_embodiment candidates are coded twice (emotion + embodiment)
DUAL_CODE_FAMILIES = {
    "emotion_embodiment": ("emotion", "embodiment"),
}


def _format_list(items: Sequence[Any], *, limit: int = 12) -> str:
    vals = [str(x) for x in items if str(x).strip()][:limit]
    return ", ".join(vals) if vals else "(none)"


def _packet_path(cfg: Stage11Config, topic_id: int) -> Path:
    return cfg.output_path("evidence_packets_dir") / f"topic_{int(topic_id):04d}.json"


def load_blind_evidence(
    cfg: Stage11Config,
    topic_id: int,
    *,
    metadata: Mapping[int, Mapping[str, Any]],
    rep_docs: Mapping[int, Sequence[str]],
    lookup_row: Optional[Mapping[str, Any]] = None,
    max_sentences: int = 16,
) -> Dict[str, Any]:
    """Build rating-blind evidence dict for a topic (packets preferred)."""
    lex = lexical_block(topic_id, metadata, representation_names=REP_NAMES)
    reps = lex.get("representations") or {}
    docs = list(rep_docs.get(int(topic_id), []) or [])[:6]
    sentences: List[str] = []

    packet_file = _packet_path(cfg, topic_id)
    if packet_file.exists():
        packet = json.loads(packet_file.read_text(encoding="utf-8"))
        # Prefer novel sentences; strip book_id / rating fields if present
        for key in ("novel_sentences", "sentences", "contextual_sentences"):
            raw = packet.get(key) or []
            if not raw:
                continue
            for item in raw:
                if isinstance(item, dict):
                    text = str(item.get("text") or item.get("sentence") or "").strip()
                else:
                    text = str(item).strip()
                if text:
                    sentences.append(text)
            if sentences:
                break
        if not docs:
            docs = list(packet.get("representative_docs") or [])[:6]
        if packet.get("label_public") and not lex.get("label_public"):
            lex["label_public"] = packet.get("label_public")

    if not sentences:
        sentences = list(lex.get("stage08_snippets") or [])[:max_sentences]
    sentences = sentences[:max_sentences]

    label = ""
    tax_main = ""
    tax_sec = ""
    if lookup_row:
        label = str(lookup_row.get("label") or "")
        tax_main = str(lookup_row.get("taxonomy_main_id") or "")
        tax_sec = str(lookup_row.get("taxonomy_secondary_id") or "")
    if not label:
        label = str(lex.get("label_public") or "")

    return {
        "topic_id": int(topic_id),
        "label": label,
        "taxonomy_main": tax_main,
        "taxonomy_secondary": tax_sec,
        "main": _format_list(reps.get("Main") or []),
        "keybert": _format_list(reps.get("KeyBERT") or []),
        "pos": _format_list(reps.get("POS") or []),
        "mmr": _format_list(reps.get("MMR") or []),
        "rep_docs": " | ".join(str(d) for d in docs) if docs else "(none)",
        "sentences": "\n".join(f"- {s}" for s in sentences) if sentences else "(none)",
    }


def render_prompt(
    prompt_cfg: Mapping[str, Any],
    evidence: Mapping[str, Any],
) -> tuple[str, str]:
    phrasing = (prompt_cfg.get("phrasing") or {}).get("primary") or {}
    system = str(phrasing.get("system") or "")
    user_tmpl = str(phrasing.get("user") or "")
    user = user_tmpl.format(**{k: evidence.get(k, "") for k in (
        "topic_id", "label", "taxonomy_main", "taxonomy_secondary",
        "main", "keybert", "pos", "mmr", "rep_docs", "sentences",
    )})
    return system, user


def dry_run_code(prompt_cfg: Mapping[str, Any], topic_id: int) -> Dict[str, Any]:
    codes = list(prompt_cfg.get("valid_codes") or ["OFF"])
    primary = codes[0]
    return {
        "topic_id": int(topic_id),
        "primary_code": primary,
        "secondary_codes": [],
        "confidence": "low",
        "breadth": "broad",
        "supporting_cues": ["dry_run"],
        "rationale": "dry-run placeholder; no LLM call",
        "coherent_cognition": False,
        "coherent_work_family": False,
        "parse_error": False,
        "dry_run": True,
    }


def code_topic(
    *,
    cfg: Stage11Config,
    prompt_cfg: Mapping[str, Any],
    evidence: Mapping[str, Any],
    api_key: str,
    dry_run: bool = False,
) -> Dict[str, Any]:
    topic_id = int(evidence["topic_id"])
    if dry_run or not api_key:
        out = dry_run_code(prompt_cfg, topic_id)
        if not api_key and not dry_run:
            out["rationale"] = "missing OPENROUTER_API_KEY; dry-run placeholder"
        return out

    system, user = render_prompt(prompt_cfg, evidence)
    llm_cfg = cfg.section("llm")
    payload = chat_json(
        model=str(llm_cfg.get("primary_model")),
        system=system,
        user=user,
        temperature=float(llm_cfg.get("temperature", 0.0)),
        max_tokens=int(llm_cfg.get("max_tokens", 1200)),
        api_key=api_key,
        rate_limit_delay_s=float(llm_cfg.get("rate_limit_delay_s", 0.0)),
        max_retries=int(llm_cfg.get("max_retries", 10)),
        retry_backoff_s=float(llm_cfg.get("retry_backoff_s", 5.0)),
        request_timeout_s=float(llm_cfg.get("request_timeout_s", 180.0)),
    )
    payload.setdefault("topic_id", topic_id)
    payload["dry_run"] = False
    return payload


def iter_coding_jobs(
    candidates_payload: Mapping[str, Any],
    ees_cfg: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    """Expand discovery families into (code_family, topic_id) jobs."""
    prompt_paths = ees_cfg.get("prompts") or {}
    jobs: List[Dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()

    for disc_family, entries in (candidates_payload.get("candidates") or {}).items():
        if disc_family in DUAL_CODE_FAMILIES:
            code_families = DUAL_CODE_FAMILIES[disc_family]
        else:
            key = FAMILY_PROMPT_KEY.get(disc_family, disc_family)
            code_families = (key,)
        for code_family in code_families:
            if code_family not in prompt_paths:
                continue
            for entry in entries:
                tid = int(entry["topic_id"])
                key = (code_family, tid)
                if key in seen:
                    continue
                seen.add(key)
                jobs.append(
                    {
                        "discovery_family": disc_family,
                        "code_family": code_family,
                        "topic_id": tid,
                        "prompt_path": prompt_paths[code_family],
                    }
                )
    return jobs


def run_ees_coding(
    cfg: Stage11Config,
    ees_cfg: Mapping[str, Any],
    *,
    dry_run: bool = False,
    limit: Optional[int] = None,
    families: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    out_dir = ees_output_dir(cfg, ees_cfg)
    cand_path = out_dir / "candidate_topics.json"
    if not cand_path.exists():
        raise FileNotFoundError(
            f"Missing candidates at {cand_path}. Run pipeline/09_build_ees_candidates.py first."
        )
    payload = json.loads(cand_path.read_text(encoding="utf-8"))
    jobs = iter_coding_jobs(payload, ees_cfg)
    if families:
        want = {str(f) for f in families}
        jobs = [j for j in jobs if j["code_family"] in want or j["discovery_family"] in want]
    if limit is not None:
        jobs = jobs[: int(limit)]

    load_dotenv_key()
    api_key = resolve_api_key()
    metadata = load_topic_metadata(cfg)
    rep_docs = load_representative_docs(cfg)
    lookup = load_topic_lookup(cfg).set_index("topic_id")

    prompt_cache: Dict[str, Dict[str, Any]] = {}
    rows: List[Dict[str, Any]] = []
    llm_cfg = cfg.section("llm")
    delay = float(llm_cfg.get("rate_limit_delay_s", 0.0))

    for i, job in enumerate(jobs, start=1):
        path = Path(job["prompt_path"])
        if not path.is_absolute():
            path = cfg.root / path
        cache_key = str(path)
        if cache_key not in prompt_cache:
            prompt_cache[cache_key] = load_prompt_yaml(path)
            if not prompt_cache[cache_key].get("frozen", False):
                raise ValueError(f"Prompt not frozen: {path}")
        prompt_cfg = prompt_cache[cache_key]
        tid = int(job["topic_id"])
        lookup_row = lookup.loc[tid].to_dict() if tid in lookup.index else {}
        evidence = load_blind_evidence(
            cfg, tid, metadata=metadata, rep_docs=rep_docs, lookup_row=lookup_row
        )
        LOGGER.info(
            "[%d/%d] coding %s topic %d",
            i,
            len(jobs),
            job["code_family"],
            tid,
        )
        resp = code_topic(
            cfg=cfg,
            prompt_cfg=prompt_cfg,
            evidence=evidence,
            api_key=api_key,
            dry_run=dry_run,
        )
        # chat_json may nest fields under "parsed"
        flat = dict(resp)
        if isinstance(resp.get("parsed"), dict):
            flat = {**resp, **resp["parsed"]}
        rows.append(
            {
                "discovery_family": job["discovery_family"],
                "code_family": job["code_family"],
                "topic_id": tid,
                "label": evidence.get("label"),
                "taxonomy_main_id": evidence.get("taxonomy_main"),
                "primary_code": flat.get("primary_code"),
                "secondary_codes": json.dumps(flat.get("secondary_codes") or []),
                "confidence": flat.get("confidence"),
                "breadth": flat.get("breadth"),
                "supporting_cues": json.dumps(flat.get("supporting_cues") or []),
                "rationale": flat.get("rationale"),
                "coherent_cognition": flat.get("coherent_cognition"),
                "coherent_work_family": flat.get("coherent_work_family"),
                "dry_run": bool(resp.get("dry_run")),
                "raw_json": json.dumps(resp),
            }
        )
        if not dry_run and api_key and delay > 0:
            time.sleep(delay)

    return pd.DataFrame(rows)


def write_semantic_codes(
    frame: pd.DataFrame,
    out_dir: Path,
) -> Dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "semantic_codes.csv"
    jsonl_path = out_dir / "semantic_codes.jsonl"
    frame.to_csv(csv_path, index=False)
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for _, row in frame.iterrows():
            f.write(json.dumps(row.to_dict(), default=str) + "\n")
    return {"csv": csv_path, "jsonl": jsonl_path}


def codes_to_membership(
    frame: pd.DataFrame,
    *,
    exclude_off_target: Sequence[str] = ("E0", "B0", "S0", "generic_off_target"),
) -> Dict[str, Dict[str, List[int]]]:
    """Collapse coded frame into code_family → code → topic_ids."""
    out: Dict[str, Dict[str, List[int]]] = {}
    exclude = {str(x) for x in exclude_off_target}
    for _, row in frame.iterrows():
        family = str(row.get("code_family") or "")
        code = str(row.get("primary_code") or "").strip()
        if not family or not code or code in exclude:
            continue
        tid = int(row["topic_id"])
        out.setdefault(family, {}).setdefault(code, [])
        if tid not in out[family][code]:
            out[family][code].append(tid)
    for family in out:
        for code in out[family]:
            out[family][code] = sorted(out[family][code])
    return out
