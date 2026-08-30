#!/usr/bin/env python3
"""Build a detailed Stage 11 human-review PDF (and markdown twin) for all audited topics.

Covers H1–H6: readable new category legends, topic id + label, old taxonomy leaf,
new construct code with human label, novel sentences tagged HIGH-/LOW-rated (with
book title when sealed maps exist), and Pass A/B/C model rationales.

Usage:
  .venv/bin/python scripts/stage11/export_human_review_pdf.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import pandas as pd
import yaml
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
from src.stage11_refined_construct_analysis.audits.runner import CODE_FIELD
from src.stage11_refined_construct_analysis.config import DEFAULT_CONFIG_PATH, load_stage11_config

HYPOTHESES: Tuple[str, ...] = ("H1", "H2", "H3", "H4", "H5", "H6")
HYP_TITLES = {
    "H1": "H1 — Intimacy (functional re-coding)",
    "H2": "H2 — HEA / final relational payoff",
    "H3": "H3 — Security / material vs display",
    "H4": "H4 — Protection vs possession",
    "H5": "H5 — Darkness vs tenderness boundaries",
    "H6": "H6 — Arc semantics (main-couple / position)",
}
PROMPT_FILES = {
    "H1": "h1_intimacy.yaml",
    "H2": "h2_hea.yaml",
    "H3": "h3_security.yaml",
    "H4": "h4_protection.yaml",
    "H5": "h5_darkness.yaml",
    "H6": "h6_arc.yaml",
}
MAX_SENTENCES = 12
MIN_CHARS = 40


def _esc(text: Any) -> str:
    s = "" if text is None else str(text)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _wrap_plain(text: str, width: int = 96) -> str:
    parts = []
    for para in str(text).splitlines() or [""]:
        para = " ".join(para.split())
        if not para:
            parts.append("")
            continue
        parts.extend(textwrap.wrap(para, width=width) or [para])
    return "\n".join(parts)


def _humanize_label(label: Any) -> str:
    s = str(label or "").strip()
    if not s:
        return ""
    return s.replace("_", " ")


def load_codebook(cfg, hyp: str) -> List[Dict[str, str]]:
    """Readable new categories from frozen prompt YAML."""
    path = cfg.root / "configs" / "stage11" / "prompts" / PROMPT_FILES[hyp]
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    out = []
    for item in data.get("codes") or []:
        cid = str(item.get("id") or "").strip()
        if not cid:
            continue
        out.append(
            {
                "id": cid,
                "label": _humanize_label(item.get("label") or cid),
                "definition": " ".join(str(item.get("definition") or "").split()),
            }
        )
    return out


def codebook_lookup(codes: Sequence[Mapping[str, str]]) -> Dict[str, Mapping[str, str]]:
    return {c["id"]: c for c in codes}


def fmt_code(raw: Any, lookup: Mapping[str, Mapping[str, str]]) -> str:
    """Format ``I3 — nonexplicit affection`` (never bare I3 alone when known)."""
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return "—"
    s = str(raw).strip()
    if not s:
        return "—"
    if s.upper() in ("MIXED", "NULL", "NONE", "UNKNOWN"):
        return s
    norm = normalize_code(s) or s
    meta = lookup.get(norm) or lookup.get(s)
    if meta:
        return f"{norm} — {meta['label']}"
    # Alias phrases already human
    if re.search(r"[a-zA-Z]{3,}", s) and "_" in s:
        return f"{s} — {_humanize_label(s)}"
    return s


def load_cell_meanings(cfg) -> Dict[str, str]:
    key = nh.load_cell_key(cfg)
    return dict(key.get("meanings") or {})


def cell_rating_label(cell: Any, meanings: Mapping[str, str]) -> str:
    """Map CELL_* → clear HIGH-rated / LOW-rated label for human review."""
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        return "rating unknown"
    c = str(cell).strip()
    meaning = meanings.get(c, "")
    # meanings like high_prevalence_high_tier
    rating = "rating unknown"
    prevalence = ""
    if "high_tier" in meaning:
        rating = "HIGH-rated"
    elif "low_tier" in meaning:
        rating = "LOW-rated"
    if "high_prevalence" in meaning:
        prevalence = "high topic share in this book"
    elif "low_prevalence" in meaning:
        prevalence = "low topic share in this book"
    if rating == "rating unknown" and not meaning:
        return c
    if prevalence:
        return f"{rating} ({prevalence}; was {c})"
    return f"{rating} (was {c})"


@lru_cache(maxsize=1)
def load_books_index(cfg) -> pd.DataFrame:
    path = cfg.input_path("analysis_frame")
    df = pd.read_parquet(path, columns=["book_id", "title", "author_name", "rating_class", "avg_rating"])
    return df.drop_duplicates("book_id").set_index("book_id")


def load_book_map(cfg, topic_id: int) -> Dict[str, int]:
    path = cfg.output_path("evidence_packets_dir") / "sealed" / f"topic_{int(topic_id):04d}_book_map.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): int(v) for k, v in raw.items()}


def sentence_source_line(
    s: Mapping[str, Any],
    *,
    topic_id: int,
    cfg,
    meanings: Mapping[str, str],
    books: pd.DataFrame,
    book_map: Mapping[str, int],
) -> str:
    anon = s.get("book_id_anon")
    if not anon and s.get("sid"):
        sid = str(s["sid"])
        anon = sid.rsplit("_", 1)[0] if "_" in sid else sid
    anon = str(anon or "BOOK_?")
    rating = cell_rating_label(s.get("cell"), meanings)

    book_bits = [anon]
    real_id = book_map.get(anon)
    if real_id is not None and real_id in books.index:
        meta = books.loc[real_id]
        title = str(meta.get("title") or "?").strip()
        author = str(meta.get("author_name") or "?").strip()
        book_bits.append(f"{title} — {author}")
        # Cross-check rating_class if present
        rc = str(meta.get("rating_class") or "")
        if "high" in rc and "HIGH" not in rating:
            rating = f"{rating} [frame={rc}]"
        elif "low" in rc and "LOW" not in rating:
            rating = f"{rating} [frame={rc}]"

    extras = []
    if s.get("tertile"):
        extras.append(f"tertile={s['tertile']}")
    if s.get("max_topic_prob") is not None:
        try:
            extras.append(f"p={float(s['max_topic_prob']):.2f}")
        except (TypeError, ValueError):
            pass
    tail = f"; {'; '.join(extras)}" if extras else ""
    return f"{rating} · {' · '.join(book_bits)}{tail}"


def collect_hypothesis_topics(cfg, master, hyp: str):
    code_col = CODE_FIELD[hyp]
    df = master[master[code_col].notna()].copy()
    df["code_norm"] = df[code_col].map(normalize_code)
    lex = nh.load_audit_jsonl(cfg, hyp, "A")
    ctxu = nh.load_audit_jsonl(cfg, hyp, "B")
    adj = nh.load_audit_jsonl(cfg, hyp, "C")
    return df, rd.audit_index(lex), rd.audit_index(ctxu), rd.audit_index(adj)


def codebook_markdown(codes: Sequence[Mapping[str, str]]) -> List[str]:
    lines = [
        "### New categories (read these before the topics)",
        "",
        "| Code | Category | Definition |",
        "| --- | --- | --- |",
    ]
    for c in codes:
        defn = c["definition"] or "—"
        lines.append(f"| `{c['id']}` | **{c['label']}** | {defn} |")
    lines.append("")
    return lines


def topic_markdown_block(
    cfg,
    row,
    *,
    hyp: str,
    code_col: str,
    lex_idx,
    ctx_idx,
    adj_idx,
    lookup: Mapping[str, Mapping[str, str]],
    meanings: Mapping[str, str],
    books: pd.DataFrame,
) -> str:
    tid = int(row["topic_id"])
    audit = rd.audit_rows_for_topic(lex_idx, ctx_idx, adj_idx, tid, hyp=hyp)
    review = rd.load_topic_review(cfg, tid)
    book_map = load_book_map(cfg, tid)
    sents = rd._filter_sentences(
        review.get("representative_sentences") or [],
        min_chars=MIN_CHARS,
        max_n=MAX_SENTENCES,
    )
    new_code = fmt_code(row.get(code_col), lookup)
    norm_code = fmt_code(row.get("code_norm"), lookup)
    anchor = f"topic-{hyp.lower()}-{tid}"
    lines = [
        f"### Topic {rd.fmt_topic(tid, row.get('current_topic_label'))} {{#{anchor}}}",
        "",
        f"- **Old taxonomy:** {rd.fmt_leaf(row.get('current_taxonomy_id'), row.get('current_taxonomy_name'))}",
        f"- **New category:** **{new_code}**",
    ]
    if str(row.get("code_norm")) != str(row.get(code_col)):
        lines.append(f"- **Normalised category:** {norm_code}")
    lines.append(f"- **Mixed:** {bool(row.get('mixed_topic'))}")
    if hyp == "H6":
        lines.append(
            f"- **Main-couple prob:** {row.get('main_couple_prob')} | "
            f"non-couple: {row.get('non_couple_prob')}"
        )
    if audit.get("action"):
        lines.append(f"- **Adjudication action:** `{audit.get('action')}`")
    kw = review.get("keywords") or {}
    main = list(kw.get("Main") or [])[:10]
    if main:
        lines.append(f"- **Keywords:** {', '.join(str(x) for x in main)}")
    snippets = list(review.get("stage08_snippets") or [])[:4]
    if snippets:
        lines.append("")
        lines.append("**Stage-08 snippets**")
        lines.append("")
        for sn in snippets:
            lines.append(f"> {' '.join(str(sn).split())}")
            lines.append("")
    lines.append("**Novel sentences** (HIGH-rated / LOW-rated from unblinded sampling cells)")
    lines.append("")
    if not sents:
        lines.append("_No representative sentences in packet._")
        lines.append("")
    for s in sents:
        src = sentence_source_line(
            s, topic_id=tid, cfg=cfg, meanings=meanings, books=books, book_map=book_map
        )
        lines.append(f"> **{src}**")
        lines.append(f">")
        lines.append(f"> {' '.join(str(s.get('sentence') or '').split())}")
        lines.append("")
    lines.append("**Model reasonings (new taxonomy audits)**")
    lines.append("")
    for label, ck, rk in (
        ("Pass A — lexical", "code_a", "rationale_a"),
        ("Pass B — contextual", "code_b", "rationale_b"),
        ("Pass C — adjudication", "code_c", "rationale_c"),
    ):
        lines.append(f"- **{label}:** **{fmt_code(audit.get(ck), lookup)}**")
        rat = audit.get(rk) or ""
        if rat:
            lines.append(f"  - {rat}")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_markdown(cfg, master, meanings, books) -> str:
    parts = [
        "# Stage 11 — Human review pack (refined construct audits)",
        "",
        "All topics audited under hypotheses **H1–H6**. Each hypothesis starts with a "
        "**readable new-category legend**, then every topic with old taxonomy leaf, "
        "new category name (not bare codes), novel sentences tagged **HIGH-rated** / "
        "**LOW-rated**, book title when available, and Pass A/B/C model reasonings.",
        "",
        f"Run: `{cfg.run_id}`",
        "",
        "## Table of contents",
        "",
    ]
    bodies: List[str] = []
    for hyp in HYPOTHESES:
        df, lex_idx, ctx_idx, adj_idx = collect_hypothesis_topics(cfg, master, hyp)
        code_col = CODE_FIELD[hyp]
        codes = load_codebook(cfg, hyp)
        lookup = codebook_lookup(codes)
        hyp_anchor = hyp.lower()
        parts.append(f"### [{HYP_TITLES[hyp]}](#{hyp_anchor}) — {len(df)} topics")
        parts.append("")
        if not df.empty:
            for _, row in df.sort_values(["current_taxonomy_id", "topic_id"]).iterrows():
                tid = int(row["topic_id"])
                cat = fmt_code(row.get(code_col), lookup)
                parts.append(
                    f"- [{rd.fmt_topic(tid, row.get('current_topic_label'))}]"
                    f"(#topic-{hyp_anchor}-{tid}) — {cat}"
                )
            parts.append("")

        bodies.append(f"## {HYP_TITLES[hyp]} {{#{hyp_anchor}}}")
        bodies.append("")
        bodies.extend(codebook_markdown(codes))
        bodies.append(
            f"Topics with a non-null `{code_col}`: **{len(df)}**. "
            "Sentence tags use the unblinded cell key "
            "(`high_tier` → HIGH-rated, `low_tier` → LOW-rated)."
        )
        bodies.append("")
        if df.empty:
            bodies.append("_No topics._")
            bodies.append("")
            continue
        overview = rd.annotation_overview(df, code_col)
        bodies.append("| Topic | Old taxonomy | New category | Mixed |")
        bodies.append("| --- | --- | --- | --- |")
        for _, r in overview.iterrows():
            bodies.append(
                f"| {r['topic']} | {r['taxonomy']} | {fmt_code(r['code'], lookup)} | {r['mixed']} |"
            )
        bodies.append("")
        for _, row in df.sort_values(["current_taxonomy_id", "topic_id"]).iterrows():
            bodies.append(
                topic_markdown_block(
                    cfg,
                    row,
                    hyp=hyp,
                    code_col=code_col,
                    lex_idx=lex_idx,
                    ctx_idx=ctx_idx,
                    adj_idx=adj_idx,
                    lookup=lookup,
                    meanings=meanings,
                    books=books,
                )
            )
    parts.append("")
    parts.extend(bodies)
    return "\n".join(parts)


def _pdf_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontSize=18,
            leading=22,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1Custom",
            parent=styles["Heading1"],
            fontSize=14,
            leading=18,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2Custom",
            parent=styles["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=10,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H3Custom",
            parent=styles["Heading3"],
            fontSize=9.5,
            leading=12,
            spaceBefore=6,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
            textColor="#333333",
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Quote",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
            leftIndent=10,
            textColor="#222222",
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=styles["Code"],
            fontSize=7.5,
            leading=9.5,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TocHyp",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=12,
            spaceBefore=6,
            spaceAfter=2,
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            name="TocTopic",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
            leftIndent=12,
            spaceAfter=1,
        )
    )
    return styles


def build_pdf(cfg, master, out_path: Path, meanings, books) -> None:
    styles = _pdf_styles()
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="Stage 11 human review pack",
        author="Stage 11 refined construct analysis",
    )
    story: List[Any] = []
    story.append(Paragraph("Stage 11 — Human review pack", styles["CoverTitle"]))
    story.append(
        Paragraph(
            _esc(
                "Readable new categories before each hypothesis; every topic shows "
                "category names (not bare codes); novel sentences are tagged HIGH-rated "
                f"or LOW-rated with book title when available. Run: {cfg.run_id}."
            ),
            styles["BodyCustom"],
        )
    )
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table of contents (by hypothesis)", styles["H2Custom"]))

    # Preload per-hyp frames for TOC + body
    packed = {}
    for hyp in HYPOTHESES:
        df, lex_idx, ctx_idx, adj_idx = collect_hypothesis_topics(cfg, master, hyp)
        codes = load_codebook(cfg, hyp)
        packed[hyp] = {
            "df": df,
            "lex_idx": lex_idx,
            "ctx_idx": ctx_idx,
            "adj_idx": adj_idx,
            "codes": codes,
            "lookup": codebook_lookup(codes),
            "code_col": CODE_FIELD[hyp],
        }

    for hyp in HYPOTHESES:
        info = packed[hyp]
        df = info["df"]
        lookup = info["lookup"]
        story.append(
            Paragraph(
                _esc(f"{HYP_TITLES[hyp]}  ({len(df)} topics)"),
                styles["TocHyp"],
            )
        )
        for _, row in df.sort_values(["current_taxonomy_id", "topic_id"]).iterrows():
            tid = int(row["topic_id"])
            story.append(
                Paragraph(
                    _esc(
                        f"· {rd.fmt_topic(tid, row.get('current_topic_label'))} — "
                        f"{fmt_code(row.get(info['code_col']), lookup)}"
                    ),
                    styles["TocTopic"],
                )
            )

    story.append(PageBreak())

    for hyp in HYPOTHESES:
        info = packed[hyp]
        df = info["df"]
        lookup = info["lookup"]
        code_col = info["code_col"]
        story.append(Paragraph(_esc(HYP_TITLES[hyp]), styles["H1Custom"]))
        story.append(Paragraph("New categories for this hypothesis", styles["H2Custom"]))
        story.append(
            Paragraph(
                _esc(
                    "Read these names before reviewing topics. Codes alone (I3, S12, …) "
                    "are not enough — use the category label."
                ),
                styles["Meta"],
            )
        )
        for c in info["codes"]:
            defn = c["definition"]
            line = f"<b>{_esc(c['id'])} — {_esc(c['label'])}</b>"
            if defn:
                line += f": {_esc(defn)}"
            story.append(Paragraph(line, styles["BodyCustom"]))
        story.append(Spacer(1, 4))
        story.append(
            Paragraph(
                _esc(
                    f"{len(df)} topics. Sentence tags: HIGH-rated / LOW-rated from "
                    "unblinded CELL_* key (high_tier / low_tier)."
                ),
                styles["Meta"],
            )
        )
        if df.empty:
            story.append(PageBreak())
            continue

        for _, row in df.sort_values(["current_taxonomy_id", "topic_id"]).iterrows():
            tid = int(row["topic_id"])
            audit = rd.audit_rows_for_topic(
                info["lex_idx"], info["ctx_idx"], info["adj_idx"], tid, hyp=hyp
            )
            review = rd.load_topic_review(cfg, tid)
            book_map = load_book_map(cfg, tid)
            sents = rd._filter_sentences(
                review.get("representative_sentences") or [],
                min_chars=MIN_CHARS,
                max_n=MAX_SENTENCES,
            )
            block: List[Any] = [
                Paragraph(
                    _esc(f"Topic {rd.fmt_topic(tid, row.get('current_topic_label'))}"),
                    styles["H2Custom"],
                ),
                Paragraph(
                    _esc(
                        "Old taxonomy: "
                        + rd.fmt_leaf(
                            row.get("current_taxonomy_id"),
                            row.get("current_taxonomy_name"),
                        )
                    ),
                    styles["Meta"],
                ),
                Paragraph(
                    _esc(f"New category: {fmt_code(row.get(code_col), lookup)}"),
                    styles["Meta"],
                ),
            ]
            if hyp == "H6":
                block.append(
                    Paragraph(
                        _esc(
                            f"main_couple_prob={row.get('main_couple_prob')} | "
                            f"non_couple={row.get('non_couple_prob')}"
                        ),
                        styles["Meta"],
                    )
                )
            main = list((review.get("keywords") or {}).get("Main") or [])[:10]
            if main:
                block.append(
                    Paragraph(
                        _esc("Keywords: " + ", ".join(str(x) for x in main)),
                        styles["Meta"],
                    )
                )
            for sn in list(review.get("stage08_snippets") or [])[:3]:
                block.append(
                    Paragraph(
                        _esc("« " + " ".join(str(sn).split()) + " »"),
                        styles["Quote"],
                    )
                )
            block.append(
                Paragraph(
                    "<b>Novel sentences</b> (HIGH-rated / LOW-rated)",
                    styles["Meta"],
                )
            )
            if sents:
                for s in sents:
                    src = sentence_source_line(
                        s,
                        topic_id=tid,
                        cfg=cfg,
                        meanings=meanings,
                        books=books,
                        book_map=book_map,
                    )
                    block.append(Paragraph(_esc(src), styles["Meta"]))
                    block.append(
                        Paragraph(
                            _esc(" ".join(str(s.get("sentence") or "").split())),
                            styles["Quote"],
                        )
                    )
            else:
                block.append(Paragraph(_esc("(no sentences in packet)"), styles["Meta"]))

            block.append(Paragraph("<b>Model reasonings</b>", styles["Meta"]))
            for label, ck, rk in (
                ("A lexical", "code_a", "rationale_a"),
                ("B contextual", "code_b", "rationale_b"),
                ("C adjudicate", "code_c", "rationale_c"),
            ):
                code = fmt_code(audit.get(ck), lookup)
                action = (
                    f" action={audit.get('action')}"
                    if label.startswith("C") and audit.get("action")
                    else ""
                )
                block.append(
                    Paragraph(_esc(f"{label}: {code}{action}"), styles["BodyCustom"])
                )
                rat = audit.get(rk) or ""
                if rat:
                    block.append(
                        Preformatted(_wrap_plain(rat, width=100), styles["CodeBlock"])
                    )
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

    md_path = out_dir / "stage11_human_review_all_topics.md"
    pdf_path = out_dir / "stage11_human_review_all_topics.pdf"

    print(f"Building markdown → {md_path}")
    md = build_markdown(cfg, master, meanings, books)
    md_path.write_text(md, encoding="utf-8")
    print(f"  {md_path.stat().st_size / 1e6:.2f} MB, {md.count(chr(10)):,} lines")

    print(f"Building PDF → {pdf_path}")
    build_pdf(cfg, master, pdf_path, meanings, books)
    print(f"  {pdf_path.stat().st_size / 1e6:.2f} MB")

    for hyp in HYPOTHESES:
        df, lex_idx, ctx_idx, adj_idx = collect_hypothesis_topics(cfg, master, hyp)
        codes = load_codebook(cfg, hyp)
        lookup = codebook_lookup(codes)
        code_col = CODE_FIELD[hyp]
        chunk = [
            f"# {HYP_TITLES[hyp]}",
            "",
            f"Run: `{cfg.run_id}` — {len(df)} topics.",
            "",
            *codebook_markdown(codes),
        ]
        for _, row in df.sort_values(["current_taxonomy_id", "topic_id"]).iterrows():
            chunk.append(
                topic_markdown_block(
                    cfg,
                    row,
                    hyp=hyp,
                    code_col=code_col,
                    lex_idx=lex_idx,
                    ctx_idx=ctx_idx,
                    adj_idx=adj_idx,
                    lookup=lookup,
                    meanings=meanings,
                    books=books,
                )
            )
        p = out_dir / f"stage11_human_review_{hyp.lower()}.md"
        p.write_text("\n".join(chunk), encoding="utf-8")
        print(f"  wrote {p.name} ({p.stat().st_size / 1e3:.0f} KB)")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
