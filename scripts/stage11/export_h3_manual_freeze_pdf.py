#!/usr/bin/env python3
"""Export a lean H3 manual-freeze checklist PDF for emotional vs material review.

Topics: emotional (S1–S4), material (S8/S9 incl. near-misses), appearance/status
(S12–S15). No Pass A/B/C rationales. Human fills function + KEEP/REMOVE.

Usage:
  .venv/bin/python scripts/stage11/export_h3_manual_freeze_pdf.py
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh
from src.stage11_refined_construct_analysis.analysis import review_display as rd
from src.stage11_refined_construct_analysis.analysis.constructs import normalize_code
from src.stage11_refined_construct_analysis.analysis.h3_manual_freeze import (
    BUCKET_ORDER,
    H3_MANUAL_FREEZE_CODES,
    bucket_for_code,
    default_freeze_path,
    resolve_h3_freeze_topic_ids,
    seed_decisions_worksheet,
)
from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
    FREEZE_CELLS,
    load_freeze_review_sentences,
    preload_freeze_neighbor_cache,
)
from src.stage11_refined_construct_analysis.config import DEFAULT_CONFIG_PATH, load_stage11_config
from src.stage11_refined_construct_analysis.evidence.packets import load_representative_docs


def _load_human_review_export():
    path = Path(__file__).resolve().parent / "export_human_review_pdf.py"
    spec = importlib.util.spec_from_file_location("stage11_export_human_review_pdf", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_hr = _load_human_review_export()
_esc = _hr._esc
codebook_lookup = _hr.codebook_lookup
fmt_code = _hr.fmt_code
load_book_map = _hr.load_book_map
load_books_index = _hr.load_books_index
load_cell_meanings = _hr.load_cell_meanings
load_codebook = _hr.load_codebook
sentence_source_line = _hr.sentence_source_line

BUCKET_TITLES = {
    "emotional": "1. Emotional security (S1–S4)",
    "material": "2. Material / economic provision (S8–S9)",
    "appearance_status": "3. Appearance / status confounders (S12–S15)",
}

DECISION_RULES = """\
Decision rules (manual freeze — emotional vs material dichotomy)

1. Classify FUNCTION, not object. A house/gown/paycheck may be emotional
   belonging, material provision, appearance/status, or off-target.
2. Emotional (S1–S4): reassurance, belonging, trust, commitment-as-safety.
   KEEP on emotional side only if the topic primarily soothes / affirms /
   binds the relationship emotionally — not money or housing transfer.
3. Material (S8/S9): relationship-directed transfer of money/housing/
   necessities as security for a partner. REJECT merely being rich,
   luxury display, occupational status, workplace talk, or objects
   without a provision function.
4. Appearance / status (S12–S15): display, grooming, prestige, gifts-as-
   tokens, workplace rank — keep SEPARATE from material provision.
5. Contradiction trap: do not KEEP a topic on the material side if
   sentences show only appearance, status, or job-seeking without
   provision-to-partner.
6. KEEP = retain under final_code. REMOVE = drop from H3 atoms (S0).
"""


def _kw_list(val: Any, *, n: int = 12) -> List[str]:
    if val is None:
        return []
    if isinstance(val, str):
        parts = [p.strip() for p in val.split(",") if p.strip()]
        return parts[:n]
    try:
        return [str(x) for x in list(val)[:n] if str(x).strip()]
    except TypeError:
        return []


def four_keyword_reps(row: Mapping[str, Any], review: Mapping[str, Any]) -> Dict[str, List[str]]:
    """Prefer review lexical representations (key: representations); fall back to master."""
    reps = (
        review.get("representations")
        or review.get("reps")
        or review.get("keywords")
        or review.get("keyword_reps")
        or {}
    )
    if not isinstance(reps, dict):
        reps = {}
    out = {
        "Main": _kw_list(reps.get("Main")),
        "KeyBERT": _kw_list(reps.get("KeyBERT")),
        "POS": _kw_list(reps.get("POS")),
        "MMR": _kw_list(reps.get("MMR")),
    }
    if not any(out.values()):
        out = {
            "Main": _kw_list(row.get("main_keywords")),
            "KeyBERT": _kw_list(row.get("keybert_keywords")),
            "POS": _kw_list(row.get("pos_keywords")),
            "MMR": _kw_list(row.get("mmr_keywords")),
        }
    return out


def bertopic_sentences(
    review: Mapping[str, Any],
    *,
    rep_docs_by_topic: Mapping[int, Sequence[str]],
    topic_id: int,
    max_n: int = 8,
) -> Dict[str, List[str]]:
    """BERTopic / labeling sentences (not the stratified book CELL sample)."""
    stage08 = [
        " ".join(str(x).split())
        for x in (review.get("stage08_snippets") or [])
        if str(x).strip()
    ][:max_n]
    from_csv = [
        " ".join(str(x).split())
        for x in (rep_docs_by_topic.get(int(topic_id)) or [])
        if str(x).strip()
    ][:max_n]
    # Packet representative_sentences are often the same as stratified samples;
    # still useful when stage08/csv are thin.
    from_packet: List[str] = []
    for s in review.get("representative_sentences") or []:
        if isinstance(s, dict):
            text = " ".join(str(s.get("sentence") or "").split())
        else:
            text = " ".join(str(s).split())
        if text and text not in from_packet:
            from_packet.append(text)
        if len(from_packet) >= max_n:
            break
    return {
        "stage08_snippets": stage08,
        "bertopic_representative_docs": from_csv,
        "packet_representatives": from_packet,
    }

def collect_freeze_rows(cfg, master: pd.DataFrame) -> pd.DataFrame:
    ids = resolve_h3_freeze_topic_ids(cfg, master)
    sub = master[master["topic_id"].isin(ids)].copy()
    sub["code_norm"] = sub["security_code"].map(normalize_code)
    order = {tid: i for i, tid in enumerate(ids)}
    sub["_ord"] = sub["topic_id"].map(order)
    return sub.sort_values("_ord").drop(columns=["_ord"]).reset_index(drop=True)


def _coverage_note(meta: Mapping[str, Any]) -> str:
    bits = []
    empty = meta.get("empty_cells") or []
    thin = meta.get("thin_cells") or []
    if empty:
        bits.append(f"no packet sentences for {', '.join(empty)}")
    if thin:
        bits.append(f"thin cells {', '.join(thin)}")
    present = meta.get("cells_present") or []
    missing = [c for c in FREEZE_CELLS if c not in present]
    if missing and not empty:
        bits.append(f"not shown: {', '.join(missing)}")
    n_books = meta.get("n_books")
    if n_books is not None:
        bits.append(f"{meta.get('n_selected', 0)} examples from {n_books} books")
    ctx = meta.get("n_with_context")
    if ctx:
        bits.append(f"±1 context on {ctx}")
    return "; ".join(bits) if bits else ""


def topic_markdown_block(
    cfg,
    row,
    *,
    lookup: Mapping[str, Mapping[str, str]],
    meanings: Mapping[str, str],
    books: pd.DataFrame,
    neighbor_cache=None,
    rep_docs_by_topic: Optional[Mapping[int, Sequence[str]]] = None,
) -> str:
    tid = int(row["topic_id"])
    review = rd.load_topic_review(cfg, tid)
    book_map = load_book_map(cfg, tid)
    sents, meta = load_freeze_review_sentences(
        cfg, tid, book_map, neighbor_cache=neighbor_cache
    )
    code = fmt_code(row.get("security_code"), lookup)
    kws = four_keyword_reps(row, review)
    bt = bertopic_sentences(
        review, rep_docs_by_topic=rep_docs_by_topic or {}, topic_id=tid
    )
    cov = _coverage_note(meta)
    suggested = normalize_code(row.get("security_code")) or str(row.get("security_code") or "")
    lines = [
        f"### Topic {rd.fmt_topic(tid, row.get('current_topic_label'))}",
        "",
        f"- **Taxonomy:** {rd.fmt_leaf(row.get('current_taxonomy_id'), row.get('current_taxonomy_name'))}",
        f"- **Current code (LLM):** **{code}**",
        "",
        "**Four keyword representations** (BERTopic / labeling)",
        "",
        f"- **Main:** {', '.join(kws['Main']) or '—'}",
        f"- **KeyBERT:** {', '.join(kws['KeyBERT']) or '—'}",
        f"- **POS:** {', '.join(kws['POS']) or '—'}",
        f"- **MMR:** {', '.join(kws['MMR']) or '—'}",
        "",
        "**BERTopic representative docs**",
        "",
    ]
    if bt["bertopic_representative_docs"]:
        for i, text in enumerate(bt["bertopic_representative_docs"], start=1):
            lines.append(f"> {i}. {text}")
            lines.append("")
    else:
        lines.append("_No BERTopic representative_docs for this topic._")
        lines.append("")

    lines.append("**Stage-08 labeling snippets**")
    lines.append("")
    if bt["stage08_snippets"]:
        for i, text in enumerate(bt["stage08_snippets"], start=1):
            lines.append(f"> {i}. {text}")
            lines.append("")
    else:
        lines.append("_No stage08 snippets._")
        lines.append("")

    lines.extend(
        [
            "**Sampled book sentences** (stratified CELL_A–D, different books, ±1 context)",
            "",
        ]
    )
    if cov:
        lines.append(f"_{cov}_")
        lines.append("")

    by_cell: Dict[str, List[Any]] = {c: [] for c in FREEZE_CELLS}
    for s in sents:
        cell = str(s.get("cell") or "")
        if cell in by_cell:
            by_cell[cell].append(s)

    for cell in FREEZE_CELLS:
        meaning = meanings.get(cell, "")
        header = f"**{cell}**" + (f" — {meaning}" if meaning else "")
        cell_sents = by_cell.get(cell) or []
        if not cell_sents:
            lines.append(f"> {header} — _no usable sentences in packet_")
            lines.append("")
            continue
        lines.append(f"{header}")
        lines.append("")
        for s in cell_sents:
            src = sentence_source_line(
                s, topic_id=tid, cfg=cfg, meanings=meanings, books=books, book_map=book_map
            )
            lines.append(f"> **{src}**")
            lines.append(">")
            lines.append(
                f"> {' '.join(str(s.get('display_sentence') or s.get('sentence') or '').split())}"
            )
            lines.append("")

    # If stratified sample is empty, fall back to packet representatives
    if not sents and bt["packet_representatives"]:
        lines.append("**Packet representative sentences** (fallback when CELL sample empty)")
        lines.append("")
        for i, text in enumerate(bt["packet_representatives"], start=1):
            lines.append(f"> {i}. {text}")
            lines.append("")

    lines.extend(
        [
            "**Manual checklist** (fill in)",
            "",
            "- Relationship-directed transfer / security act: yes / no",
            "- Function: emotional / material_money / material_housing / appearance_status / other",
            f"- Security code: ________ (suggestion: `{suggested}`)",
            "- Decision: KEEP / REMOVE",
            "",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def build_markdown(
    cfg,
    df: pd.DataFrame,
    *,
    meanings: Mapping[str, str],
    books: pd.DataFrame,
    neighbor_cache=None,
    rep_docs_by_topic: Optional[Mapping[int, Sequence[str]]] = None,
) -> str:
    codes = load_codebook(cfg, "H3")
    lookup = codebook_lookup(codes)
    focus = [c for c in codes if c["id"] in H3_MANUAL_FREEZE_CODES]
    lines = [
        f"# H3 manual freeze — emotional vs material ({len(df)} topics)",
        "",
        f"Run: `{cfg.run_id}` — {len(df)} topics.",
        "",
        "No LLM adjudication on this pack. Fill KEEP/REMOVE after reading evidence.",
        "Focus: does each topic belong on the emotional side, the material side, "
        "or appearance/status (kept separate)?",
        "",
        "```",
        DECISION_RULES.strip(),
        "```",
        "",
        "### Codes in scope",
        "",
        "| Code | Category | Definition |",
        "| --- | --- | --- |",
    ]
    for c in focus:
        lines.append(f"| `{c['id']}` | **{c['label']}** | {c['definition'] or '—'} |")
    lines.append("")

    for bucket in BUCKET_ORDER:
        bucket_df = df[df["code_norm"].map(lambda c: bucket_for_code(c) == bucket)]
        if bucket_df.empty:
            continue
        lines.append(f"## {BUCKET_TITLES[bucket]}")
        lines.append("")
        lines.append(f"_{len(bucket_df)} topics_")
        lines.append("")
        for _, row in bucket_df.iterrows():
            lines.append(
                topic_markdown_block(
                    cfg,
                    row,
                    lookup=lookup,
                    meanings=meanings,
                    books=books,
                    neighbor_cache=neighbor_cache,
                    rep_docs_by_topic=rep_docs_by_topic,
                )
            )
    return "\n".join(lines)


def _styles():
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle(
            "H3FreezeTitle",
            parent=base["Title"],
            fontSize=16,
            leading=20,
            spaceAfter=8,
        ),
        "H1": ParagraphStyle(
            "H3FreezeH1",
            parent=base["Heading1"],
            fontSize=13,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "H2": ParagraphStyle(
            "H3FreezeH2",
            parent=base["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "Body": ParagraphStyle(
            "H3FreezeBody",
            parent=base["BodyText"],
            fontSize=9,
            leading=12,
            spaceAfter=3,
        ),
        "Meta": ParagraphStyle(
            "H3FreezeMeta",
            parent=base["BodyText"],
            fontSize=9,
            leading=11,
            spaceAfter=2,
        ),
        "Quote": ParagraphStyle(
            "H3FreezeQuote",
            parent=base["BodyText"],
            fontSize=8.5,
            leading=11,
            leftIndent=8,
            spaceAfter=2,
        ),
        "CodeBlock": ParagraphStyle(
            "H3FreezeCode",
            parent=base["Code"],
            fontSize=7.5,
            leading=9.5,
            spaceAfter=6,
        ),
        "Checklist": ParagraphStyle(
            "H3FreezeCheck",
            parent=base["BodyText"],
            fontSize=9.5,
            leading=13,
            spaceBefore=4,
            spaceAfter=2,
            borderPadding=4,
        ),
    }


def build_pdf(
    cfg,
    df: pd.DataFrame,
    pdf_path: Path,
    *,
    meanings: Mapping[str, str],
    books: pd.DataFrame,
    neighbor_cache=None,
    rep_docs_by_topic: Optional[Mapping[int, Sequence[str]]] = None,
) -> None:
    codes = load_codebook(cfg, "H3")
    lookup = codebook_lookup(codes)
    styles = _styles()
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )
    story: List[Any] = []
    story.append(
        Paragraph(
            _esc(f"H3 manual freeze — emotional vs material ({len(df)} topics)"),
            styles["Title"],
        )
    )
    story.append(
        Paragraph(
            _esc(
                f"Run: {cfg.run_id} — {len(df)} topics. "
                "No LLM adjudication. Review material vs emotional dichotomy."
            ),
            styles["Meta"],
        )
    )
    story.append(Preformatted(DECISION_RULES.strip(), styles["CodeBlock"]))
    story.append(PageBreak())

    for bucket in BUCKET_ORDER:
        bucket_df = df[df["code_norm"].map(lambda c: bucket_for_code(c) == bucket)]
        if bucket_df.empty:
            continue
        story.append(Paragraph(_esc(BUCKET_TITLES[bucket]), styles["H1"]))
        story.append(Paragraph(_esc(f"{len(bucket_df)} topics"), styles["Meta"]))

        for _, row in bucket_df.iterrows():
            tid = int(row["topic_id"])
            review = rd.load_topic_review(cfg, tid)
            book_map = load_book_map(cfg, tid)
            sents, meta = load_freeze_review_sentences(
                cfg, tid, book_map, neighbor_cache=neighbor_cache
            )
            kws = four_keyword_reps(row, review)
            bt = bertopic_sentences(
                review, rep_docs_by_topic=rep_docs_by_topic or {}, topic_id=tid
            )
            code = fmt_code(row.get("security_code"), lookup)
            suggested = normalize_code(row.get("security_code")) or str(
                row.get("security_code") or ""
            )
            cov = _coverage_note(meta)

            block: List[Any] = []
            block.append(
                Paragraph(
                    _esc(f"Topic {rd.fmt_topic(tid, row.get('current_topic_label'))}"),
                    styles["H2"],
                )
            )
            block.append(
                Paragraph(
                    _esc(
                        f"Taxonomy: {rd.fmt_leaf(row.get('current_taxonomy_id'), row.get('current_taxonomy_name'))}"
                    ),
                    styles["Meta"],
                )
            )
            block.append(Paragraph(_esc(f"Current code (LLM): {code}"), styles["Meta"]))
            block.append(
                Paragraph(
                    "<b>Four keyword representations</b> (BERTopic / labeling)",
                    styles["Meta"],
                )
            )
            for name in ("Main", "KeyBERT", "POS", "MMR"):
                block.append(
                    Paragraph(
                        _esc(f"{name}: {', '.join(kws[name]) or '—'}"),
                        styles["Body"],
                    )
                )
            block.append(Paragraph("<b>BERTopic representative docs</b>", styles["Meta"]))
            if bt["bertopic_representative_docs"]:
                for i, text in enumerate(bt["bertopic_representative_docs"], start=1):
                    block.append(Paragraph(_esc(f"{i}. {text}"), styles["Quote"]))
            else:
                block.append(
                    Paragraph(_esc("No BERTopic representative_docs for this topic."), styles["Meta"])
                )
            block.append(Paragraph("<b>Stage-08 labeling snippets</b>", styles["Meta"]))
            if bt["stage08_snippets"]:
                for i, text in enumerate(bt["stage08_snippets"], start=1):
                    block.append(Paragraph(_esc(f"{i}. {text}"), styles["Quote"]))
            else:
                block.append(Paragraph(_esc("No stage08 snippets."), styles["Meta"]))
            block.append(
                Paragraph(
                    "<b>Sampled book sentences</b> (CELL_A–D · different books · ±1 context)",
                    styles["Meta"],
                )
            )
            if cov:
                block.append(Paragraph(_esc(cov), styles["Meta"]))
            by_cell: Dict[str, List[Any]] = {c: [] for c in FREEZE_CELLS}
            for s in sents:
                cell = str(s.get("cell") or "")
                if cell in by_cell:
                    by_cell[cell].append(s)
                else:
                    by_cell.setdefault(cell, []).append(s)
            for cell in FREEZE_CELLS:
                meaning = meanings.get(cell, "")
                header = f"{cell}" + (f" ({meaning})" if meaning else "")
                cell_sents = by_cell.get(cell) or []
                if not cell_sents:
                    block.append(
                        Paragraph(
                            _esc(f"{header}: no usable sentences in packet"),
                            styles["Meta"],
                        )
                    )
                    continue
                block.append(Paragraph(_esc(header), styles["Meta"]))
                for s in cell_sents:
                    src = sentence_source_line(
                        s,
                        topic_id=tid,
                        cfg=cfg,
                        meanings=meanings,
                        books=books,
                        book_map=book_map,
                    )
                    block.append(Paragraph(_esc(src), styles["Quote"]))
                    block.append(
                        Paragraph(
                            _esc(
                                " ".join(
                                    str(
                                        s.get("display_sentence") or s.get("sentence") or ""
                                    ).split()
                                )
                            ),
                            styles["Quote"],
                        )
                    )
            if not sents and bt["packet_representatives"]:
                block.append(
                    Paragraph(
                        "<b>Packet representative sentences</b> (fallback)",
                        styles["Meta"],
                    )
                )
                for i, text in enumerate(bt["packet_representatives"], start=1):
                    block.append(Paragraph(_esc(f"{i}. {text}"), styles["Quote"]))
            block.append(Spacer(1, 4))
            block.append(
                Paragraph(
                    _esc(
                        "CHECKLIST — Relationship-directed: [ yes / no ]   "
                        "Function: [ emotional / material_money / material_housing / "
                        "appearance_status / other ]"
                    ),
                    styles["Checklist"],
                )
            )
            block.append(
                Paragraph(
                    _esc(
                        f"Code: [ ________ ]  (suggestion: {suggested})   "
                        "Decision: [ KEEP / REMOVE ]"
                    ),
                    styles["Checklist"],
                )
            )
            block.append(Spacer(1, 8))
            story.append(KeepTogether(block))

        story.append(PageBreak())

    doc.build(story)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args(argv)

    cfg = load_stage11_config(args.config)
    master = nh.load_master(cfg)
    meanings = load_cell_meanings(cfg)
    books = load_books_index(cfg)
    rep_docs_by_topic = load_representative_docs(cfg)
    out_dir = Path(args.out_dir) if args.out_dir else cfg.output_path("human_review_dir", create=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = collect_freeze_rows(cfg, master)
    if df.empty:
        print("ERROR: no H3 freeze topics found in master", file=sys.stderr)
        return 1
    print(f"Freeze pack: {len(df)} topics")
    print(df.groupby("code_norm").size().to_string())
    print(f"BERTopic representative_docs loaded for {len(rep_docs_by_topic)} topics")

    print("Preloading ±1 sentence context (one corpus scan)…")
    topic_maps = {
        int(tid): load_book_map(cfg, int(tid)) for tid in df["topic_id"].tolist()
    }
    neighbor_cache = preload_freeze_neighbor_cache(cfg, topic_maps)
    print(f"  neighbor anchors cached: {len(neighbor_cache)}")

    md_path = out_dir / "stage11_h3_manual_freeze.md"
    pdf_path = out_dir / "stage11_h3_manual_freeze.pdf"
    decisions_path = out_dir / "h3_manual_freeze_decisions.json"

    print(f"Building markdown → {md_path}")
    md = build_markdown(
        cfg,
        df,
        meanings=meanings,
        books=books,
        neighbor_cache=neighbor_cache,
        rep_docs_by_topic=rep_docs_by_topic,
    )
    md_path.write_text(md, encoding="utf-8")
    print(f"  {md_path.stat().st_size / 1e3:.1f} KB")

    print(f"Building PDF → {pdf_path}")
    build_pdf(
        cfg,
        df,
        pdf_path,
        meanings=meanings,
        books=books,
        neighbor_cache=neighbor_cache,
        rep_docs_by_topic=rep_docs_by_topic,
    )
    print(f"  {pdf_path.stat().st_size / 1e3:.1f} KB")

    worksheet = seed_decisions_worksheet(df)
    decisions_path.write_text(json.dumps(worksheet, indent=2), encoding="utf-8")
    print(f"Blank worksheet → {decisions_path}")

    freeze_path = default_freeze_path(cfg)
    print(
        f"After review: fill decisions, set frozen=true, save as {freeze_path.name} "
        f"(or copy from {decisions_path.name})."
    )
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
