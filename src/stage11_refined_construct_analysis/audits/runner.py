"""Pass A/B/C hypothesis audit runner (Nemo primary model)."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set

import pandas as pd

from src.stage11_refined_construct_analysis.audits.llm import (
    chat_json,
    consensus_code,
    load_dotenv_key,
    resolve_api_key,
)
from src.stage11_refined_construct_analysis.audits.prompts import (
    format_pass_messages,
    list_code_ids,
    load_hypothesis_prompt,
)
from src.stage11_refined_construct_analysis.audits.spillover import load_spillover_promoted
from src.stage11_refined_construct_analysis.config import Stage11Config
from src.stage11_refined_construct_analysis.evidence.packets import (
    llm_view,
    load_topic_metadata,
)
from src.stage11_refined_construct_analysis.lookup import load_topic_lookup

LOGGER = logging.getLogger("stage11.audits")

PASS_FILES = {
    "A": "lexical.jsonl",
    "B": "contextual.jsonl",
    "C": "adjudication.jsonl",
}

CODE_FIELD = {
    "H1": "intimacy_code",
    "H2": "hea_code",
    "H3": "security_code",
    "H4": "care_protection_code",
    "H5": "darkness_code",
    "H6": "arc_role",
}


def audit_dir(cfg: Stage11Config, hypothesis: str) -> Path:
    path = cfg.output_path("audits_dir", create=True) / str(hypothesis).lower()
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_manifest(cfg: Stage11Config, hypothesis: str) -> Dict[str, Any]:
    path = cfg.output_path("candidates_dir") / f"{str(hypothesis).lower()}_candidates.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing candidate manifest: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_evidence_packet(cfg: Stage11Config, topic_id: int) -> Optional[Dict[str, Any]]:
    path = cfg.output_path("evidence_packets_dir") / f"topic_{int(topic_id):04d}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_packet(
    cfg: Stage11Config,
    topic_id: int,
    *,
    metadata: Optional[Mapping[int, Mapping[str, Any]]] = None,
    lookup: Optional[pd.DataFrame] = None,
    require_contextual: bool = True,
) -> Dict[str, Any]:
    """Load on-disk packet; rebuild contextual if missing/empty when required."""
    existing = load_evidence_packet(cfg, topic_id)
    if existing is not None:
        n_sent = len(existing.get("contextual", {}).get("sentences", []) or [])
        if (not require_contextual) or n_sent > 0:
            return existing
        LOGGER.warning(
            "Evidence packet topic %s has %d sentences; rebuilding with contextual fetch",
            topic_id,
            n_sent,
        )

    # Rebuild (lexical + contextual) via shared builder when disk packet is empty/missing.
    from src.stage11_refined_construct_analysis.evidence.packets import (
        build_evidence_packet,
        load_representative_docs,
    )
    from src.stage11_refined_construct_analysis.evidence.blinding import (
        load_or_create_cell_key,
    )

    meta = metadata or load_topic_metadata(cfg)
    lu = lookup if lookup is not None else load_topic_lookup(cfg)
    counts = pd.read_parquet(cfg.input_path("book_topic_counts", required=True))
    frame = pd.read_parquet(
        cfg.input_path("analysis_frame", required=True),
        columns=["book_id", "rating_class"],
    )
    packet = build_evidence_packet(
        cfg,
        int(topic_id),
        lookup=lu,
        metadata=meta,
        representative_docs=load_representative_docs(cfg),
        book_topic_counts=counts,
        analysis_frame=frame,
        cell_key=load_or_create_cell_key(cfg),
        sentence_files=cfg.sentence_topic_files() if require_contextual else None,
        include_contextual=require_contextual,
    )
    # Persist without clobbering the full evidence index.
    out_dir = cfg.output_path("evidence_packets_dir", create=True)
    path = out_dir / f"topic_{int(topic_id):04d}.json"
    public = json.loads(json.dumps(packet, default=str))
    book_map = public.get("contextual", {}).pop("_book_id_map", None)
    path.write_text(json.dumps(public, indent=2, ensure_ascii=False), encoding="utf-8")
    if book_map:
        sealed = out_dir / "sealed" / f"topic_{int(topic_id):04d}_book_map.json"
        sealed.parent.mkdir(parents=True, exist_ok=True)
        sealed.write_text(json.dumps(book_map, indent=2), encoding="utf-8")
    return packet



def resolve_audit_topic_ids(
    cfg: Stage11Config,
    hypothesis: str,
    *,
    include_spillover: bool = True,
    include_comparators: bool = True,
) -> List[int]:
    """Mandatory (+ comparators for H3) + focus (H5) + Nemo-promoted spillover.

    H6 also inherits H5-flagged 3.2 topics when H5 adjudication exists.
    """
    hyp = str(hypothesis).upper()
    manifest = load_manifest(cfg, hyp)
    ids: Set[int] = set()
    for entry in manifest.get("entries", []):
        tid = entry.get("topic_id")
        if tid is None:
            continue
        role = entry.get("role")
        if role == "mandatory":
            ids.add(int(tid))
        elif role == "comparator" and include_comparators:
            ids.add(int(tid))
        elif role == "focus":
            ids.add(int(tid))
        # spillover_discovery: only if promoted by triage
    if include_spillover:
        for tid in load_spillover_promoted(cfg, hyp):
            ids.add(int(tid))

    # H6: add 3.2 topics flagged relational by H5 (or all 3.2 focus if H5 not done yet)
    if hyp == "H6":
        ids.update(_h6_inherit_topic_ids(cfg))
    return sorted(ids)


def _h6_inherit_topic_ids(cfg: Stage11Config) -> Set[int]:
    """3.2 topics that H5 marks as relational darkness / partner harm (or all 3.2 if pending)."""
    from src.stage11_refined_construct_analysis.lookup import topics_for_leaves

    lookup = load_topic_lookup(cfg)
    t32 = set(topics_for_leaves(lookup, ["3.2"]))
    h5_path = audit_dir(cfg, "H5") / PASS_FILES["C"]
    if not h5_path.exists():
        return t32
    flagged: Set[int] = set()
    relational = {"D1", "D2", "MIXED"}
    for row in load_jsonl(h5_path):
        tid = int(row["topic_id"])
        if tid not in t32:
            continue
        code = str(row.get("code") or (row.get("response") or {}).get("darkness_code") or "")
        if code in relational:
            flagged.add(tid)
    return flagged if flagged else t32


def load_tenderness_priors_for_h5(cfg: Stage11Config) -> Dict[int, Dict[str, Any]]:
    """Reuse H1 intimacy + H4 care codes for tenderness-side topics."""
    priors: Dict[int, Dict[str, Any]] = {}
    tenderness_h1 = {"I1", "I2", "I3", "I7"}
    tenderness_h4 = {"H4_1", "H4_4", "H4_12"}
    for hyp, allowed in (("H1", tenderness_h1), ("H4", tenderness_h4)):
        path = audit_dir(cfg, hyp) / PASS_FILES["C"]
        if not path.exists():
            continue
        for row in load_jsonl(path):
            tid = int(row["topic_id"])
            code = str(row.get("code") or "")
            resp = row.get("response") or {}
            priors.setdefault(tid, {})[f"{hyp.lower()}_code"] = code
            if code in allowed:
                priors[tid]["tenderness_candidate"] = True
                priors[tid]["source"] = hyp
            if resp.get("proposed_constructs"):
                priors[tid]["proposed_constructs"] = resp.get("proposed_constructs")
    return priors


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip().lstrip("\x00")
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            LOGGER.warning("Skipping corrupt jsonl line in %s: %s…", path.name, line[:80])
            continue
    return rows


def append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def completed_topic_ids(path: Path) -> Set[int]:
    return {int(r["topic_id"]) for r in load_jsonl(path) if "topic_id" in r}


def load_h3_priors_for_h4(cfg: Stage11Config) -> Dict[int, Dict[str, Any]]:
    """Reuse H3 security decomposition for overlapping 4.6 topics (single H4 project)."""
    path = audit_dir(cfg, "H3") / PASS_FILES["C"]
    if not path.exists():
        return {}
    lookup = load_topic_lookup(cfg)
    leaf46 = set(
        int(t)
        for t in lookup.loc[lookup["taxonomy_main_id"].astype(str) == "4.6", "topic_id"].tolist()
    )
    priors: Dict[int, Dict[str, Any]] = {}
    for row in load_jsonl(path):
        tid = int(row["topic_id"])
        if tid not in leaf46:
            continue
        parsed = row.get("response") or {}
        priors[tid] = {
            "security_code": parsed.get("security_code")
            or parsed.get("consensus_code")
            or row.get("code"),
            "action": parsed.get("action"),
            "proposed_constructs": parsed.get("proposed_constructs"),
            "rationale": parsed.get("rationale"),
        }
    return priors


def _dry_run_pass(
    *,
    hypothesis: str,
    topic_id: int,
    pass_name: str,
    valid_codes: Sequence[str],
    prior_h3: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    codes = [c for c in valid_codes if c]
    if not codes:
        codes = ["UNKNOWN"]
    idx = (int(topic_id) * 17 + ord(pass_name.upper()[0])) % len(codes)
    code = codes[idx]
    # Known H1 trap topic 1 → I3 (kissing, not I6) for dry-run realism
    if hypothesis == "H1" and int(topic_id) in (1, 7) and pass_name.upper() in ("A", "B", "C"):
        code = "I3"
    if hypothesis == "H2" and int(topic_id) == 167:
        code = "H2_5"  # wedding / public union (prompt-aligned)
    if hypothesis == "H2" and int(topic_id) in (29, 62):
        code = "H2_1"
    if hypothesis == "H4" and int(topic_id) in (293, 315):
        code = "H4_7"
    if hypothesis == "H3" and int(topic_id) == 18:
        code = "S13"

    base: Dict[str, Any] = {
        "topic_id": int(topic_id),
        "consensus_code": code,
        "dominant_code": code if pass_name.upper() == "B" else None,
        "disagreement": False,
        "proportions": {code: 0.85, "MIXED": 0.0},
        "rationale": f"dry-run {hypothesis} pass {pass_name}",
        "dry_run": True,
    }
    field = CODE_FIELD.get(hypothesis)
    if field and pass_name.upper() == "C":
        base[field] = code
        base["action"] = "REINTERPRET" if hypothesis == "H1" and code == "I3" else "KEEP"
        base["proposed_constructs"] = [code]
        base["manual_review_required"] = False
    if hypothesis == "H2" and pass_name.upper() == "B":
        base.update(
            {
                "main_couple": True,
                "mutuality": "partial",
                "future_orientation": False,
                "rupture_resolved": False,
                "finality": "low",
            }
        )
    if hypothesis == "H4" and prior_h3:
        base["prior_h3_security_code"] = prior_h3.get("security_code")
    if pass_name.upper() == "A":
        base["per_rep"] = {name: code for name in ("Main", "KeyBERT", "POS", "MMR")}
    if pass_name.upper() == "B":
        base["sentence_codes"] = []
    return base


def run_pass(
    cfg: Stage11Config,
    *,
    hypothesis: str,
    packet: Mapping[str, Any],
    pass_name: str,
    lexical_consensus: str = "",
    contextual_dominant: str = "",
    prior_h3: Optional[Mapping[str, Any]] = None,
    prior_notes: Optional[Mapping[str, Any]] = None,
    dry_run: bool = False,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    prompt_override: Optional[Path] = None,
) -> Dict[str, Any]:
    hyp = str(hypothesis).upper()
    prompt = load_hypothesis_prompt(cfg, hyp, prompt_path=prompt_override)
    valid = list(list_code_ids(prompt)) + ["MIXED"]
    view = llm_view(packet, pass_name=pass_name)
    max_sent = None
    if pass_name.upper() == "B":
        max_sent = int(cfg.section("llm", "pass_b_max_sentences", default=20))
        n_pkt = len(packet.get("contextual", {}).get("sentences", []) or [])
        design = (
            (packet.get("contextual") or {}).get("sampling") or {}
        ).get("design")
        if design == "position_x_books" and n_pkt > max_sent:
            max_sent = min(int(n_pkt), 48)
    messages = format_pass_messages(
        prompt,
        view,
        phrasing="primary",
        pass_name=pass_name,
        lexical_consensus=lexical_consensus,
        contextual_dominant=contextual_dominant,
        max_sentences=max_sent,
    )
    # Cross-audit reuse notes (do not alter frozen template text).
    extras = []
    if hyp == "H4" and prior_h3 and pass_name.upper() == "C":
        extras.append(
            "Prior H3 security decomposition for this 4.6 topic (reuse; one H4 project): "
            + json.dumps(prior_h3, ensure_ascii=False)
        )
    if hyp == "H5" and prior_notes and pass_name.upper() in ("B", "C"):
        extras.append(
            "Prior H1/H4 tenderness signals (reuse; do not relabel all 4.6 as tenderness): "
            + json.dumps(prior_notes, ensure_ascii=False)
        )
    if extras:
        messages = dict(messages)
        messages["user"] = messages["user"] + "\n\n" + "\n".join(extras)

    key = resolve_api_key(api_key) or load_dotenv_key()
    use_dry = bool(dry_run or not key)
    dry_payload = (
        _dry_run_pass(
            hypothesis=hyp,
            topic_id=int(packet["topic_id"]),
            pass_name=pass_name,
            valid_codes=list(list_code_ids(prompt)),
            prior_h3=prior_h3,
        )
        if use_dry
        else None
    )
    model_id = str(model or cfg.section("llm", "primary_model"))
    result = chat_json(
        model=model_id,
        system=messages["system"],
        user=messages["user"],
        temperature=float(cfg.section("llm", "temperature")),
        max_tokens=int(cfg.section("llm", "max_tokens")),
        api_key=key,
        rate_limit_delay_s=float(cfg.section("llm", "rate_limit_delay_s")),
        max_retries=int(cfg.section("llm", "max_retries") or 10),
        retry_backoff_s=float(cfg.section("llm", "retry_backoff_s") or 5.0),
        request_timeout_s=float(cfg.section("llm", "request_timeout_s") or 180.0),
        dry_run_payload=dry_payload,
    )
    parsed = result["parsed"]
    code = consensus_code(parsed, valid)
    return {
        "hypothesis": hyp,
        "topic_id": int(packet["topic_id"]),
        "pass": pass_name.upper(),
        "code": code,
        "response": parsed,
        "model": result["model"],
        "dry_run": result["dry_run"],
        "prompt_version": messages["prompt_version"],
        "exhaustive": bool(packet.get("exhaustive")),
        "synthesized_lexical_only": bool(packet.get("synthesized_lexical_only")),
        "n_sentences": len(packet.get("contextual", {}).get("sentences", [])),
        "prior_h3": prior_h3,
        "prior_notes": prior_notes,
        "raw": result["raw"] if not result["dry_run"] else None,
    }


def run_hypothesis_audit(
    cfg: Stage11Config,
    hypothesis: str,
    *,
    topic_ids: Optional[Sequence[int]] = None,
    dry_run: bool = False,
    resume: bool = True,
    api_key: Optional[str] = None,
    limit: int = 0,
    model: Optional[str] = None,
    prompt_override: Optional[Path] = None,
    archive_on_no_resume: bool = True,
) -> Dict[str, Any]:
    """Run Pass A → B → C for each topic; write lexical/contextual/adjudication jsonl."""
    hyp = str(hypothesis).upper()
    out = audit_dir(cfg, hyp)
    paths = {p: out / fname for p, fname in PASS_FILES.items()}

    if topic_ids is None:
        ids = resolve_audit_topic_ids(cfg, hyp)
    else:
        ids = [int(t) for t in topic_ids]
    if limit and limit > 0:
        ids = ids[:limit]

    lookup = load_topic_lookup(cfg)
    metadata = load_topic_metadata(cfg)
    priors_h3 = load_h3_priors_for_h4(cfg) if hyp == "H4" else {}
    priors_tend = load_tenderness_priors_for_h5(cfg) if hyp == "H5" else {}
    if hyp == "H4":
        LOGGER.info("H4 reuse: loaded %d H3 priors for 4.6 topics", len(priors_h3))
    if hyp == "H5":
        LOGGER.info("H5 reuse: loaded %d H1/H4 tenderness priors", len(priors_tend))

    model_id = str(model or cfg.section("llm", "primary_model"))
    LOGGER.info("%s audit model: %s", hyp, model_id)
    if prompt_override:
        LOGGER.info("%s prompt override: %s", hyp, prompt_override)

    # Fresh re-run: archive prior jsonl so new prompt/model results are not mixed with old.
    if not resume and archive_on_no_resume:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        archive = out / f"archive_before_rerun_{stamp}"
        archive.mkdir(parents=True, exist_ok=True)
        for path in paths.values():
            if path.exists():
                dest = archive / path.name
                path.replace(dest)
                LOGGER.info("Archived %s → %s", path.name, dest.relative_to(cfg.root))
        done_c = set()
        pending = list(ids)
    elif not resume:
        # Selective re-audit: drop only the requested topic ids from existing jsonl
        pending = list(ids)
        drop = set(ids)
        for path in paths.values():
            if not path.exists():
                continue
            keep = [r for r in load_jsonl(path) if int(r["topic_id"]) not in drop]
            path.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in keep)
                + ("\n" if keep else ""),
                encoding="utf-8",
            )
        done_c = set()
    else:
        done_c = completed_topic_ids(paths["C"])
        pending = [t for t in ids if t not in done_c]
    LOGGER.info(
        "%s audit: %d topics (%d already adjudicated, %d pending)",
        hyp,
        len(ids),
        len(ids) - len(pending),
        len(pending),
    )

    # Drop partial A/B rows for pending topics so resume is clean
    if resume and pending:
        for pass_name, path in paths.items():
            if not path.exists():
                continue
            keep = [r for r in load_jsonl(path) if int(r["topic_id"]) not in set(pending)]
            path.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in keep)
                + ("\n" if keep else ""),
                encoding="utf-8",
            )

    n_run = 0
    t0 = time.time()
    for i, tid in enumerate(pending, start=1):
        packet = ensure_packet(cfg, tid, metadata=metadata, lookup=lookup)
        prior = priors_h3.get(tid)
        prior_notes = priors_tend.get(tid)
        elapsed = max(1e-3, time.time() - t0)
        rate = (i - 1) / elapsed if i > 1 else 0.0
        eta = ((len(pending) - i + 1) / rate) if rate > 0 else float("nan")
        LOGGER.info(
            "[%d/%d] %s topic %s (exhaustive=%s n_sent=%d) elapsed=%.0fs ETA≈%.0fs",
            i,
            len(pending),
            hyp,
            tid,
            packet.get("exhaustive"),
            len(packet.get("contextual", {}).get("sentences", [])),
            elapsed,
            eta if eta == eta else -1,
        )

        try:
            row_a = run_pass(
                cfg,
                hypothesis=hyp,
                packet=packet,
                pass_name="A",
                dry_run=dry_run,
                api_key=api_key,
                prior_h3=prior,
                prior_notes=prior_notes,
                model=model_id,
                prompt_override=prompt_override,
            )
            row_b = run_pass(
                cfg,
                hypothesis=hyp,
                packet=packet,
                pass_name="B",
                lexical_consensus=str(row_a["code"]),
                dry_run=dry_run,
                api_key=api_key,
                prior_h3=prior,
                prior_notes=prior_notes,
                model=model_id,
                prompt_override=prompt_override,
            )
            row_c = run_pass(
                cfg,
                hypothesis=hyp,
                packet=packet,
                pass_name="C",
                lexical_consensus=str(row_a["code"]),
                contextual_dominant=str(row_b["code"]),
                dry_run=dry_run,
                api_key=api_key,
                prior_h3=prior,
                prior_notes=prior_notes,
                model=model_id,
                prompt_override=prompt_override,
            )
        except Exception as exc:
            # Keep the batch alive across transient OpenRouter 504s; resume will retry.
            LOGGER.exception(
                "%s topic %s failed (will remain pending for resume): %s",
                hyp,
                tid,
                exc,
            )
            time.sleep(15.0)
            continue
        append_jsonl(paths["A"], row_a)
        append_jsonl(paths["B"], row_b)
        append_jsonl(paths["C"], row_c)
        n_run += 1

    summary = {
        "hypothesis": hyp,
        "n_topics": len(ids),
        "topic_ids": ids,
        "n_newly_audited": n_run,
        "n_adjudicated_total": len(completed_topic_ids(paths["C"])),
        "dry_run": bool(dry_run or not resolve_api_key(api_key)),
        "model": model_id,
        "outputs": {k: str(v.relative_to(cfg.root)) for k, v in paths.items()},
        "n_h3_priors_reused": len(priors_h3) if hyp == "H4" else 0,
        "n_tenderness_priors": len(priors_tend) if hyp == "H5" else 0,
        "exhaustive_topic_ids": [
            int(t)
            for t in ids
            if bool((load_evidence_packet(cfg, t) or {}).get("exhaustive"))
            or (
                not lookup.loc[lookup["topic_id"] == t].empty
                and str(lookup.loc[lookup["topic_id"] == t].iloc[0]["taxonomy_main_id"])
                in set(str(x) for x in cfg.section("evidence", "exhaustive_leaves"))
            )
        ],
    }
    summary["n_exhaustive"] = len(summary["exhaustive_topic_ids"])
    (out / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
