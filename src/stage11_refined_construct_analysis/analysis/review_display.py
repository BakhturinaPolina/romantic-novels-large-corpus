"""Human-readable display helpers for Stage 11 audit notebooks.

Mirrors Stage 10 NB07 close-reading style: topic id with label, taxonomy id with
name, wrapped novel sentences, and Pass A/B/C rationales. Rating cells stay
blinded (CELL_* / book_id_anon); no books_meta join.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set

import numpy as np
import pandas as pd

from src.stage11_refined_construct_analysis.audits.runner import CODE_FIELD, load_evidence_packet
from src.stage11_refined_construct_analysis.config import Stage11Config

MIN_SENTENCE_CHARS = 60
DEFAULT_MAX_SENTENCES = 8
DEFAULT_PER_CODE = 3
BANNER_WIDTH = 92


def fmt_topic(tid: Any, label: Any = None) -> str:
    """Format ``12 — Whispered Reassurance`` (falls back to id alone)."""
    try:
        tid_s = str(int(tid))
    except (TypeError, ValueError):
        tid_s = str(tid)
    lab = (str(label).strip() if label is not None and not (isinstance(label, float) and pd.isna(label)) else "")
    if lab and lab.lower() not in ("nan", "none", "?"):
        return f"{tid_s} — {lab}"
    return tid_s


def fmt_leaf(leaf_id: Any, name: Any = None) -> str:
    """Format ``4.6 — Emotional Safety…``."""
    lid = "" if leaf_id is None or (isinstance(leaf_id, float) and pd.isna(leaf_id)) else str(leaf_id)
    nm = (str(name).strip() if name is not None and not (isinstance(name, float) and pd.isna(name)) else "")
    if nm and nm.lower() not in ("nan", "none", "?"):
        return f"{lid} — {nm}" if lid else nm
    return lid or "?"


def _response_dict(row: Mapping[str, Any] | None) -> Dict[str, Any]:
    if not row:
        return {}
    resp = row.get("response")
    if isinstance(resp, dict):
        return resp
    return {}


def extract_code(row: Mapping[str, Any] | None, hyp: str = "H1") -> Optional[str]:
    """Pull dominant/consensus code from an audit JSONL row."""
    if not row:
        return None
    resp = _response_dict(row)
    field = CODE_FIELD.get(hyp, "")
    for key in (field, "consensus_code", "dominant_code", "code", "hea_code", "arc_role"):
        if key and row.get(key):
            return str(row[key])
        if key and resp.get(key):
            return str(resp[key])
    return None


def extract_rationale(row: Mapping[str, Any] | None) -> str:
    if not row:
        return ""
    resp = _response_dict(row)
    for key in ("rationale", "reason", "notes", "comment"):
        val = resp.get(key) or row.get(key)
        if val:
            return str(val).strip()
    return ""


def extract_action(row: Mapping[str, Any] | None) -> str:
    if not row:
        return ""
    resp = _response_dict(row)
    return str(resp.get("action") or row.get("action") or "").strip()


def audit_index(frame: pd.DataFrame) -> Dict[int, Dict[str, Any]]:
    """Map topic_id → raw audit row dict.

    Prefer non-dry-run rows when duplicates exist (pipeline re-runs can append
    dry-run stubs after live results).
    """
    out: Dict[int, Dict[str, Any]] = {}
    if frame is None or frame.empty or "topic_id" not in frame.columns:
        return out
    # Stable order: dry-run first, then live — so live overwrites.
    ordered = frame
    if "dry_run" in frame.columns:
        ordered = frame.sort_values("dry_run", ascending=False, kind="mergesort")
    for _, row in ordered.iterrows():
        tid = int(row["topic_id"])
        as_dict = row.to_dict()
        prev = out.get(tid)
        if prev is None:
            out[tid] = as_dict
            continue
        prev_dry = bool(prev.get("dry_run"))
        cur_dry = bool(as_dict.get("dry_run"))
        if prev_dry and not cur_dry:
            out[tid] = as_dict
    return out


def audit_rows_for_topic(
    lex_idx: Mapping[int, Mapping[str, Any]],
    ctx_idx: Mapping[int, Mapping[str, Any]],
    adj_idx: Mapping[int, Mapping[str, Any]],
    topic_id: int,
    *,
    hyp: str = "H1",
) -> Dict[str, Any]:
    """Flatten Pass A/B/C code + rationale for one topic."""
    tid = int(topic_id)
    a = lex_idx.get(tid)
    b = ctx_idx.get(tid)
    c = adj_idx.get(tid)
    code_a = extract_code(a, hyp)
    code_b = extract_code(b, hyp)
    code_c = extract_code(c, hyp)
    action = extract_action(c)
    manual = bool(_response_dict(c).get("manual_review_required"))
    return {
        "topic_id": tid,
        "code_a": code_a,
        "code_b": code_b,
        "code_c": code_c,
        "rationale_a": extract_rationale(a),
        "rationale_b": extract_rationale(b),
        "rationale_c": extract_rationale(c),
        "action": action,
        "manual_review_required": manual,
        "agree_ab": bool(code_a and code_b and code_a == code_b),
    }


def load_topic_review(cfg: Stage11Config, topic_id: int) -> Dict[str, Any]:
    """Prefer human_review JSON; fall back to evidence packet shaped the same way."""
    tid = int(topic_id)
    hr_path = cfg.output_path("human_review_dir") / f"topic_{tid:04d}.json"
    if hr_path.exists():
        return json.loads(hr_path.read_text(encoding="utf-8"))

    packet = load_evidence_packet(cfg, tid) or {}
    lexical = packet.get("lexical", {}) or {}
    reveal = packet.get("pass_c_reveal", {}) or {}
    sentences = (packet.get("contextual", {}) or {}).get("sentences") or []
    return {
        "topic_id": tid,
        "label": lexical.get("label_public"),
        "taxonomy_main_id": reveal.get("taxonomy_main_id"),
        "taxonomy_main_name": reveal.get("taxonomy_main_name"),
        "taxonomy_secondary_id": reveal.get("taxonomy_secondary_id"),
        "taxonomy_secondary_name": reveal.get("taxonomy_secondary_name"),
        "exhaustive": bool(packet.get("exhaustive")),
        "representations": lexical.get("representations", {}),
        "stage08_snippets": lexical.get("stage08_snippets", []),
        "representative_sentences": [
            {
                "sid": s.get("sid"),
                "cell": s.get("cell"),
                "tertile": s.get("tertile"),
                "normalized_position": s.get("normalized_position"),
                "max_topic_prob": s.get("max_topic_prob"),
                "book_id_anon": s.get("book_id_anon"),
                "sentence": s.get("sentence"),
            }
            for s in sentences[:12]
        ],
        "classification_codes": {},
        "review_status": "from_evidence_packet",
    }


def annotation_overview(
    df: pd.DataFrame,
    code_col: str,
    *,
    code_norm_col: str = "code_norm",
    extra_cols: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """Build a human-readable overview: topic / taxonomy labels, not bare IDs."""
    rows = []
    extras = list(extra_cols or [])
    for _, r in df.iterrows():
        row = {
            "topic": fmt_topic(r.get("topic_id"), r.get("current_topic_label")),
            "topic_id": int(r["topic_id"]),
            "taxonomy": fmt_leaf(r.get("current_taxonomy_id"), r.get("current_taxonomy_name")),
            "taxonomy_id": r.get("current_taxonomy_id"),
            "code": r.get(code_col),
            "code_norm": r.get(code_norm_col),
            "mixed": bool(r.get("mixed_topic")),
            "agree": r.get("lexical_context_agreement"),
            "label": r.get("current_topic_label"),
        }
        for c in extras:
            if c in r.index:
                row[c] = r.get(c)
        rows.append(row)
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["taxonomy_id", "topic_id"], kind="mergesort").reset_index(drop=True)


def _keyword_line(reps: Mapping[str, Any], *, n: int = 8) -> str:
    main = list((reps or {}).get("Main") or [])[:n]
    kb = list((reps or {}).get("KeyBERT") or [])[:n]
    parts = []
    if main:
        parts.append("Main: " + ", ".join(str(x) for x in main))
    if kb:
        parts.append("KeyBERT: " + ", ".join(str(x) for x in kb))
    return " | ".join(parts)


def _filter_sentences(
    sentences: Sequence[Mapping[str, Any]],
    *,
    min_chars: int = MIN_SENTENCE_CHARS,
    max_n: int = DEFAULT_MAX_SENTENCES,
) -> List[Dict[str, Any]]:
    kept: List[Dict[str, Any]] = []
    for s in sentences:
        text = " ".join(str(s.get("sentence") or "").split())
        if len(text) < min_chars:
            continue
        item = dict(s)
        item["sentence"] = text
        kept.append(item)
        if len(kept) >= max_n:
            break
    # If everything was short, show the longest few anyway
    if not kept and sentences:
        ranked = sorted(
            sentences,
            key=lambda s: len(str(s.get("sentence") or "")),
            reverse=True,
        )
        for s in ranked[: min(3, max_n)]:
            text = " ".join(str(s.get("sentence") or "").split())
            if not text:
                continue
            item = dict(s)
            item["sentence"] = text
            kept.append(item)
    return kept


def show_topic_card(
    cfg: Stage11Config,
    topic_id: int,
    *,
    hyp: str = "H1",
    label: Any = None,
    taxonomy_id: Any = None,
    taxonomy_name: Any = None,
    code: Any = None,
    code_norm: Any = None,
    audit: Optional[Mapping[str, Any]] = None,
    max_sentences: int = DEFAULT_MAX_SENTENCES,
    min_chars: int = MIN_SENTENCE_CHARS,
) -> Dict[str, Any]:
    """Print one topic in NB07-style readable form; return pack for markdown export."""
    review = load_topic_review(cfg, topic_id)
    lab = label if label is not None else review.get("label")
    tax_id = taxonomy_id if taxonomy_id is not None else review.get("taxonomy_main_id")
    tax_name = taxonomy_name if taxonomy_name is not None else review.get("taxonomy_main_name")

    print("=" * BANNER_WIDTH)
    print(f"  TOPIC {fmt_topic(topic_id, lab)}")
    print("=" * BANNER_WIDTH)
    print(f"  Taxonomy : {fmt_leaf(tax_id, tax_name)}")
    if code is not None or code_norm is not None:
        print(f"  Code     : {code}" + (f"  (norm: {code_norm})" if code_norm is not None else ""))
    if review.get("exhaustive"):
        print("  Evidence : EXHAUSTIVE packet")

    kw = _keyword_line(review.get("keywords") or {})
    if kw:
        print(f"  Keywords : {kw}")

    snippets = list(review.get("stage08_snippets") or [])[:4]
    if snippets:
        print("  Stage08 snippets:")
        for sn in snippets:
            text = " ".join(str(sn).split())
            for line in textwrap.wrap(text, width=84)[:2]:
                print(f"      · {line}")

    sents = _filter_sentences(
        review.get("representative_sentences") or [],
        min_chars=min_chars,
        max_n=max_sentences,
    )
    if sents:
        print("  Novel sentences:")
        for s in sents:
            meta_bits = []
            if s.get("book_id_anon"):
                meta_bits.append(str(s["book_id_anon"]))
            elif s.get("sid"):
                sid = str(s["sid"])
                # sid like BOOK_001_1 → BOOK_001
                parts = sid.rsplit("_", 1)
                meta_bits.append(parts[0] if len(parts) == 2 else sid)
            if s.get("cell"):
                meta_bits.append(str(s["cell"]))
            if s.get("tertile"):
                meta_bits.append(f"tertile={s['tertile']}")
            if s.get("max_topic_prob") is not None:
                try:
                    meta_bits.append(f"p={float(s['max_topic_prob']):.2f}")
                except (TypeError, ValueError):
                    pass
            meta = ", ".join(meta_bits)
            print(f"    · [{meta}]" if meta else "    ·")
            for line in textwrap.wrap(s["sentence"], width=84)[:4]:
                print(f"        {line}")
    else:
        print("  Novel sentences: (none available in packet)")

    if audit:
        print("  Pass A/B/C:")
        for pass_name, code_key, rat_key in (
            ("A lexical", "code_a", "rationale_a"),
            ("B contextual", "code_b", "rationale_b"),
            ("C adjudicate", "code_c", "rationale_c"),
        ):
            c = audit.get(code_key)
            r = audit.get(rat_key) or ""
            action = f" action={audit.get('action')}" if pass_name.startswith("C") and audit.get("action") else ""
            print(f"    {pass_name}: {c}{action}")
            if r:
                for line in textwrap.wrap(r, width=80)[:5]:
                    print(f"        {line}")
        if audit.get("manual_review_required"):
            print("    !! manual_review_required")
    print()

    return {
        "topic_id": int(topic_id),
        "label": lab,
        "taxonomy_id": tax_id,
        "taxonomy_name": tax_name,
        "code": code,
        "code_norm": code_norm,
        "keywords": review.get("keywords") or {},
        "stage08_snippets": snippets,
        "sentences": sents,
        "audit": dict(audit) if audit else {},
        "exhaustive": bool(review.get("exhaustive")),
    }


def select_review_topics(
    df: pd.DataFrame,
    *,
    hyp: str,
    lex_idx: Mapping[int, Mapping[str, Any]],
    ctx_idx: Mapping[int, Mapping[str, Any]],
    adj_idx: Mapping[int, Mapping[str, Any]],
    force_ids: Optional[Iterable[int]] = None,
    per_code: int = DEFAULT_PER_CODE,
    seed: int = 42,
    show_all_if_n_le: int = 12,
) -> List[int]:
    """Priority queue for close-reading: disagreements, mixed, manual, then stratified sample."""
    if df.empty or "topic_id" not in df.columns:
        return []
    all_ids = [int(t) for t in df["topic_id"].tolist()]
    if len(all_ids) <= show_all_if_n_le:
        return sorted(set(all_ids))

    priority: List[int] = []
    seen: Set[int] = set()

    def _add(tid: int, reason_bucket: List[int]) -> None:
        if tid not in seen:
            seen.add(tid)
            reason_bucket.append(tid)
            priority.append(tid)

    forced = [int(t) for t in (force_ids or [])]
    for tid in forced:
        if tid in all_ids:
            _add(tid, [])

    for tid in all_ids:
        info = audit_rows_for_topic(lex_idx, ctx_idx, adj_idx, tid, hyp=hyp)
        row = df.loc[df["topic_id"] == tid].iloc[0]
        mixed = bool(row.get("mixed_topic"))
        disagree = bool(info["code_a"] and info["code_b"] and info["code_a"] != info["code_b"])
        action = (info.get("action") or "").upper()
        manual = bool(info.get("manual_review_required") or row.get("manual_review_required"))
        if disagree or mixed or manual or action in ("SPLIT", "EXCLUDE", "DROP"):
            _add(tid, [])

    # Stratified sample by code_norm
    rng = np.random.default_rng(seed)
    code_col = "code_norm" if "code_norm" in df.columns else None
    if code_col:
        for code, grp in df.groupby(code_col, dropna=False):
            candidates = [int(t) for t in grp["topic_id"].tolist() if int(t) not in seen]
            if not candidates:
                continue
            k = min(per_code, len(candidates))
            pick = rng.choice(candidates, size=k, replace=False).tolist()
            for tid in pick:
                _add(int(tid), [])

    return priority


def agreement_table(
    df: pd.DataFrame,
    lex_idx: Mapping[int, Mapping[str, Any]],
    ctx_idx: Mapping[int, Mapping[str, Any]],
    adj_idx: Mapping[int, Mapping[str, Any]],
    *,
    hyp: str,
) -> pd.DataFrame:
    """Labeled lexical vs contextual agreement with short rationales."""
    rows = []
    for _, r in df.iterrows():
        tid = int(r["topic_id"])
        info = audit_rows_for_topic(lex_idx, ctx_idx, adj_idx, tid, hyp=hyp)
        rows.append(
            {
                "topic": fmt_topic(tid, r.get("current_topic_label")),
                "topic_id": tid,
                "taxonomy": fmt_leaf(r.get("current_taxonomy_id"), r.get("current_taxonomy_name")),
                "code_a": info["code_a"],
                "code_b": info["code_b"],
                "code_c": info["code_c"],
                "agree": info["agree_ab"],
                "action": info["action"],
                "rationale_a": (info["rationale_a"] or "")[:180],
                "rationale_b": (info["rationale_b"] or "")[:180],
                "rationale_c": (info["rationale_c"] or "")[:180],
            }
        )
    return pd.DataFrame(rows)


def render_review_markdown(packs: Sequence[Mapping[str, Any]], *, title: str = "Close-reading pack") -> str:
    """Export NB07-style markdown with blockquoted sentences."""
    lines = [f"# {title}", ""]
    for p in packs:
        lines.append(f"## Topic {fmt_topic(p.get('topic_id'), p.get('label'))}")
        lines.append("")
        lines.append(f"- **Taxonomy:** {fmt_leaf(p.get('taxonomy_id'), p.get('taxonomy_name'))}")
        if p.get("code") is not None:
            cn = p.get("code_norm")
            lines.append(f"- **Code:** {p.get('code')}" + (f" (norm: {cn})" if cn is not None else ""))
        if p.get("exhaustive"):
            lines.append("- **Evidence:** exhaustive packet")
        kw = _keyword_line(p.get("keywords") or {})
        if kw:
            lines.append(f"- **Keywords:** {kw}")
        lines.append("")
        for sn in p.get("stage08_snippets") or []:
            lines.append(f"> {sn}")
            lines.append("")
        for s in p.get("sentences") or []:
            meta_bits = []
            if s.get("book_id_anon"):
                meta_bits.append(str(s["book_id_anon"]))
            if s.get("cell"):
                meta_bits.append(str(s["cell"]))
            if s.get("tertile"):
                meta_bits.append(f"tertile={s['tertile']}")
            meta = ", ".join(meta_bits)
            prefix = f"*({meta})* " if meta else ""
            lines.append(f"> {prefix}{s.get('sentence', '')}")
            lines.append("")
        audit = p.get("audit") or {}
        if audit:
            lines.append("### Pass A/B/C")
            lines.append("")
            for label, ck, rk in (
                ("A lexical", "code_a", "rationale_a"),
                ("B contextual", "code_b", "rationale_b"),
                ("C adjudicate", "code_c", "rationale_c"),
            ):
                lines.append(f"- **{label}:** `{audit.get(ck)}`")
                if audit.get(rk):
                    lines.append(f"  - {audit.get(rk)}")
            if audit.get("action"):
                lines.append(f"- **Action:** {audit.get('action')}")
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def show_review_set(
    cfg: Stage11Config,
    df: pd.DataFrame,
    topic_ids: Sequence[int],
    *,
    hyp: str,
    lex_idx: Mapping[int, Mapping[str, Any]],
    ctx_idx: Mapping[int, Mapping[str, Any]],
    adj_idx: Mapping[int, Mapping[str, Any]],
    code_col: str,
    max_sentences: int = DEFAULT_MAX_SENTENCES,
) -> List[Dict[str, Any]]:
    """Render cards for a list of topic ids; return packs for markdown export."""
    packs: List[Dict[str, Any]] = []
    by_id = {int(r["topic_id"]): r for _, r in df.iterrows()}
    print(f"Close-reading {len(topic_ids)} of {len(df)} topics "
          f"(disagreements / mixed / manual / stratified sample).\n")
    for tid in topic_ids:
        row = by_id.get(int(tid))
        if row is None:
            continue
        audit = audit_rows_for_topic(lex_idx, ctx_idx, adj_idx, tid, hyp=hyp)
        pack = show_topic_card(
            cfg,
            tid,
            hyp=hyp,
            label=row.get("current_topic_label"),
            taxonomy_id=row.get("current_taxonomy_id"),
            taxonomy_name=row.get("current_taxonomy_name"),
            code=row.get(code_col),
            code_norm=row.get("code_norm"),
            audit=audit,
            max_sentences=max_sentences,
        )
        packs.append(pack)
    return packs


def labeled_topic_list(lookup: pd.DataFrame, topic_ids: Sequence[int]) -> List[str]:
    """Format a pool of topic ids as ``id — label`` strings from lookup."""
    out = []
    for tid in topic_ids:
        hit = lookup.loc[lookup["topic_id"] == int(tid)]
        label = hit.iloc[0]["label"] if not hit.empty and "label" in hit.columns else None
        if label is None and not hit.empty and "current_topic_label" in hit.columns:
            label = hit.iloc[0]["current_topic_label"]
        out.append(fmt_topic(tid, label))
    return out
