#!/usr/bin/env python3
"""Export a lean H4 manual-freeze checklist PDF for the 26 atom-relevant topics.

No Pass A/B/C rationales. Human fills: external threat, main romantic target,
final code, KEEP/REMOVE.

Usage:
  .venv/bin/python scripts/stage11/export_h4_manual_freeze_pdf.py
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
from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
    BUCKET_ORDER,
    EXPECTED_TOPIC_IDS,
    FREEZE_CELLS,
    H4_MANUAL_FREEZE_CODES,
    bucket_for_code,
    default_freeze_path,
    load_construct_coverage_ids,
    load_freeze_review_sentences,
    preload_freeze_neighbor_cache,
    seed_decisions_worksheet,
)
from src.stage11_refined_construct_analysis.config import DEFAULT_CONFIG_PATH, load_stage11_config


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
    "external_protection": "1. External protection (H4_5 / H4_6)",
    "protective_commitment": "2. Protective commitment (H4_5a)",
    "possession_control": "3. Possession / control (H4_7–H4_11)",
}

DECISION_RULES = """\
Decision rules (manual freeze — no LLM)

1. H4_5 / H4_6 (external protection) REQUIRE a concrete EXTERNAL threat
   (attacker, danger, legal/social adversary). No external threat → not H4_5/H4_6.
2. H4_5a (protective commitment) = explicit safety/welfare responsibility pledge
   WITHOUT a concrete external threat strong enough for H4_5/H4_6.
   Do not code H4_5a from generic promise vocabulary alone ("I'll help", "I promise").
3. Partner-as-danger or "for their own good" restriction → H4_10 / H4_11, not protection.
4. Claiming / jealousy without coercion → H4_7 / H4_8; coercion → H4_9–H4_11.
5. Contradiction trap: if evidence shows no external threat, do NOT keep H4_5/H4_6.
6. KEEP = retain in construct atoms under final_code.
   REMOVE = drop from atoms (applied as H4_0).
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
    """Prefer review/evidence representations; fall back to master columns."""
    reps = review.get("representations") or review.get("keywords") or {}
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


def resolve_topic_ids(cfg) -> List[int]:
    """Union of coverage atom IDs for the three H4 buckets (stable sort by bucket)."""
    by_bucket = load_construct_coverage_ids(cfg)
    seen: set[int] = set()
    ordered: List[int] = []
    for bucket in BUCKET_ORDER:
        for tid in by_bucket.get(bucket) or []:
            if tid not in seen:
                seen.add(tid)
                ordered.append(tid)
    # Fallback to plan defaults if coverage missing keys
    if not ordered:
        ordered = list(EXPECTED_TOPIC_IDS)
    return ordered


def collect_freeze_rows(cfg, master: pd.DataFrame) -> pd.DataFrame:
    ids = resolve_topic_ids(cfg)
    sub = master[master["topic_id"].isin(ids)].copy()
    sub["code_norm"] = sub["care_protection_code"].map(normalize_code)
    # Preserve bucket order
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
) -> str:
    tid = int(row["topic_id"])
    review = rd.load_topic_review(cfg, tid)
    book_map = load_book_map(cfg, tid)
    sents, meta = load_freeze_review_sentences(
        cfg, tid, book_map, neighbor_cache=neighbor_cache
    )
    code = fmt_code(row.get("care_protection_code"), lookup)
    kws = four_keyword_reps(row, review)
    cov = _coverage_note(meta)
    lines = [
        f"### Topic {rd.fmt_topic(tid, row.get('current_topic_label'))}",
        "",
        f"- **Taxonomy:** {rd.fmt_leaf(row.get('current_taxonomy_id'), row.get('current_taxonomy_name'))}",
        f"- **Current code (LLM):** **{code}**",
        "",
        "**Four keyword representations**",
        "",
        f"- **Main:** {', '.join(kws['Main']) or '—'}",
        f"- **KeyBERT:** {', '.join(kws['KeyBERT']) or '—'}",
        f"- **POS:** {', '.join(kws['POS']) or '—'}",
        f"- **MMR:** {', '.join(kws['MMR']) or '—'}",
        "",
        "**Sampled sentences** (stratified CELL_A–D, different books, longer text / ±1 context)",
        "",
    ]
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
    lines.extend(
        [
            "**Manual checklist** (fill in)",
            "",
            "- External threat: yes / no",
            "- Main romantic target: yes / no",
            f"- Protection / commitment / control code: ________ "
            f"(suggestion: `{normalize_code(row.get('care_protection_code')) or row.get('care_protection_code')}`)",
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
) -> str:
    codes = load_codebook(cfg, "H4")
    lookup = codebook_lookup(codes)
    focus = [c for c in codes if c["id"] in H4_MANUAL_FREEZE_CODES or c["id"] in ("H4_0", "H4_6", "H4_10", "H4_11")]
    lines = [
        "# H4 manual freeze — 26 atom-relevant topics",
        "",
        f"Run: `{cfg.run_id}` — {len(df)} topics.",
        "",
        "No LLM adjudication on this pack. Fill KEEP/REMOVE after reading evidence.",
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
                )
            )
    return "\n".join(lines)


def _styles():
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle(
            "H4FreezeTitle",
            parent=base["Title"],
            fontSize=16,
            leading=20,
            spaceAfter=8,
        ),
        "H1": ParagraphStyle(
            "H4FreezeH1",
            parent=base["Heading1"],
            fontSize=13,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "H2": ParagraphStyle(
            "H4FreezeH2",
            parent=base["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "Body": ParagraphStyle(
            "H4FreezeBody",
            parent=base["BodyText"],
            fontSize=9,
            leading=12,
            spaceAfter=3,
        ),
        "Meta": ParagraphStyle(
            "H4FreezeMeta",
            parent=base["BodyText"],
            fontSize=9,
            leading=11,
            spaceAfter=2,
        ),
        "Quote": ParagraphStyle(
            "H4FreezeQuote",
            parent=base["BodyText"],
            fontSize=8.5,
            leading=11,
            leftIndent=8,
            spaceAfter=2,
        ),
        "CodeBlock": ParagraphStyle(
            "H4FreezeCode",
            parent=base["Code"],
            fontSize=7.5,
            leading=9.5,
            spaceAfter=6,
        ),
        "Checklist": ParagraphStyle(
            "H4FreezeCheck",
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
) -> None:
    codes = load_codebook(cfg, "H4")
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
    story.append(Paragraph(_esc("H4 manual freeze — 26 atom-relevant topics"), styles["Title"]))
    story.append(
        Paragraph(
            _esc(f"Run: {cfg.run_id} — {len(df)} topics. No LLM adjudication."),
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
            code = fmt_code(row.get("care_protection_code"), lookup)
            suggested = normalize_code(row.get("care_protection_code")) or str(
                row.get("care_protection_code") or ""
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
            block.append(Paragraph("<b>Four keyword representations</b>", styles["Meta"]))
            for name in ("Main", "KeyBERT", "POS", "MMR"):
                block.append(
                    Paragraph(
                        _esc(f"{name}: {', '.join(kws[name]) or '—'}"),
                        styles["Body"],
                    )
                )
            block.append(
                Paragraph(
                    "<b>Sampled sentences</b> (CELL_A–D · different books · ±1 context)",
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
            block.append(Spacer(1, 4))
            block.append(
                Paragraph(
                    _esc(
                        "CHECKLIST — External threat: [ yes / no ]   "
                        "Main romantic target: [ yes / no ]"
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
    out_dir = Path(args.out_dir) if args.out_dir else cfg.output_path("human_review_dir", create=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = collect_freeze_rows(cfg, master)
    if df.empty:
        print("ERROR: no H4 freeze topics found in master", file=sys.stderr)
        return 1
    print(f"Freeze pack: {len(df)} topics")
    print(df.groupby("code_norm").size().to_string())

    print("Preloading ±1 sentence context (one corpus scan)…")
    topic_maps = {
        int(tid): load_book_map(cfg, int(tid)) for tid in df["topic_id"].tolist()
    }
    neighbor_cache = preload_freeze_neighbor_cache(cfg, topic_maps)
    print(f"  neighbor anchors cached: {len(neighbor_cache)}")

    md_path = out_dir / "stage11_h4_manual_freeze.md"
    pdf_path = out_dir / "stage11_h4_manual_freeze.pdf"
    decisions_path = out_dir / "h4_manual_freeze_decisions.json"

    print(f"Building markdown → {md_path}")
    md = build_markdown(
        cfg, df, meanings=meanings, books=books, neighbor_cache=neighbor_cache
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
