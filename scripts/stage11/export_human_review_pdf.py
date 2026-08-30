#!/usr/bin/env python3
"""Build a detailed Stage 11 human-review PDF (and markdown twin) for all audited topics.

Covers H1–H6: topic id + label, old taxonomy leaf, new construct code, keywords,
representative novel sentences, and Pass A/B/C model rationales.

Usage:
  .venv/bin/python scripts/stage11/export_human_review_pdf.py
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

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
MAX_SENTENCES = 12
MIN_CHARS = 40


def _esc(text: Any) -> str:
    s = "" if text is None else str(text)
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _wrap_plain(text: str, width: int = 96) -> str:
    parts = []
    for para in str(text).splitlines() or [""]:
        para = " ".join(para.split())
        if not para:
            parts.append("")
            continue
        parts.extend(textwrap.wrap(para, width=width) or [para])
    return "\n".join(parts)


def collect_hypothesis_topics(
    cfg,
    master,
    hyp: str,
) -> Tuple[Any, Dict[int, Dict], Dict[int, Dict], Dict[int, Dict]]:
    code_col = CODE_FIELD[hyp]
    df = master[master[code_col].notna()].copy()
    df["code_norm"] = df[code_col].map(normalize_code)
    lex = nh.load_audit_jsonl(cfg, hyp, "A")
    ctxu = nh.load_audit_jsonl(cfg, hyp, "B")
    adj = nh.load_audit_jsonl(cfg, hyp, "C")
    return df, rd.audit_index(lex), rd.audit_index(ctxu), rd.audit_index(adj)


def topic_markdown_block(
    cfg,
    row,
    *,
    hyp: str,
    code_col: str,
    lex_idx,
    ctx_idx,
    adj_idx,
) -> str:
    tid = int(row["topic_id"])
    audit = rd.audit_rows_for_topic(lex_idx, ctx_idx, adj_idx, tid, hyp=hyp)
    review = rd.load_topic_review(cfg, tid)
    sents = rd._filter_sentences(
        review.get("representative_sentences") or [],
        min_chars=MIN_CHARS,
        max_n=MAX_SENTENCES,
    )
    lines = [
        f"### Topic {rd.fmt_topic(tid, row.get('current_topic_label'))}",
        "",
        f"- **Old taxonomy:** {rd.fmt_leaf(row.get('current_taxonomy_id'), row.get('current_taxonomy_name'))}",
        f"- **New code:** `{row.get(code_col)}` (norm: `{row.get('code_norm')}`)",
        f"- **Mixed:** {bool(row.get('mixed_topic'))}",
    ]
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
    lines.append("**Novel sentences**")
    lines.append("")
    if not sents:
        lines.append("_No representative sentences in packet._")
        lines.append("")
    for s in sents:
        meta = []
        if s.get("book_id_anon"):
            meta.append(str(s["book_id_anon"]))
        elif s.get("sid"):
            sid = str(s["sid"])
            meta.append(sid.rsplit("_", 1)[0] if "_" in sid else sid)
        if s.get("cell"):
            meta.append(str(s["cell"]))
        if s.get("tertile"):
            meta.append(f"tertile={s['tertile']}")
        if s.get("max_topic_prob") is not None:
            try:
                meta.append(f"p={float(s['max_topic_prob']):.2f}")
            except (TypeError, ValueError):
                pass
        prefix = f"*({' · '.join(meta)})* " if meta else ""
        lines.append(f"> {prefix}{' '.join(str(s.get('sentence') or '').split())}")
        lines.append("")
    lines.append("**Model reasonings (new taxonomy audits)**")
    lines.append("")
    for label, ck, rk in (
        ("Pass A — lexical", "code_a", "rationale_a"),
        ("Pass B — contextual", "code_b", "rationale_b"),
        ("Pass C — adjudication", "code_c", "rationale_c"),
    ):
        lines.append(f"- **{label}:** `{audit.get(ck)}`")
        rat = audit.get(rk) or ""
        if rat:
            lines.append(f"  - {rat}")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_markdown(cfg, master) -> str:
    parts = [
        "# Stage 11 — Human review pack (refined construct audits)",
        "",
        "All topics audited under hypotheses **H1–H6**, with old taxonomy leaf, "
        "**new** construct codes, representative novel sentences from evidence packets, "
        "and Pass A/B/C model rationales. Rating cells remain blinded (`CELL_*`). "
        "Book identifiers are anonymised (`BOOK_###`).",
        "",
        f"Run: `{cfg.run_id}`",
        "",
    ]
    toc = ["## Contents", ""]
    bodies: List[str] = []
    for hyp in HYPOTHESES:
        df, lex_idx, ctx_idx, adj_idx = collect_hypothesis_topics(cfg, master, hyp)
        code_col = CODE_FIELD[hyp]
        toc.append(f"- [{HYP_TITLES[hyp]}](#{hyp.lower()}) — **{len(df)}** topics")
        bodies.append(f"## {HYP_TITLES[hyp]} {{#{hyp.lower()}}}")
        bodies.append("")
        bodies.append(
            f"Topics with a non-null `{code_col}` in the master annotation table: "
            f"**{len(df)}**."
        )
        bodies.append("")
        if df.empty:
            bodies.append("_No topics._")
            bodies.append("")
            continue
        overview = rd.annotation_overview(df, code_col)
        bodies.append("| Topic | Taxonomy | Code | Norm | Mixed |")
        bodies.append("| --- | --- | --- | --- | --- |")
        for _, r in overview.iterrows():
            bodies.append(
                f"| {r['topic']} | {r['taxonomy']} | `{r['code']}` | "
                f"`{r['code_norm']}` | {r['mixed']} |"
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
                )
            )
    parts.extend(toc)
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
            spaceBefore=16,
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
    return styles


def build_pdf(cfg, master, out_path: Path) -> None:
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
                "All topics audited under H1–H6 with old taxonomy leaf, new construct "
                "codes, representative novel sentences, and Pass A/B/C model rationales. "
                f"Run: {cfg.run_id}. Rating cells blinded (CELL_*)."
            ),
            styles["BodyCustom"],
        )
    )
    story.append(Spacer(1, 6))

    for hyp in HYPOTHESES:
        df, lex_idx, ctx_idx, adj_idx = collect_hypothesis_topics(cfg, master, hyp)
        code_col = CODE_FIELD[hyp]
        story.append(Paragraph(_esc(HYP_TITLES[hyp]), styles["H1Custom"]))
        story.append(
            Paragraph(
                _esc(f"{len(df)} topics with non-null {code_col}."),
                styles["Meta"],
            )
        )
        if df.empty:
            continue
        for _, row in df.sort_values(["current_taxonomy_id", "topic_id"]).iterrows():
            tid = int(row["topic_id"])
            audit = rd.audit_rows_for_topic(lex_idx, ctx_idx, adj_idx, tid, hyp=hyp)
            review = rd.load_topic_review(cfg, tid)
            sents = rd._filter_sentences(
                review.get("representative_sentences") or [],
                min_chars=MIN_CHARS,
                max_n=MAX_SENTENCES,
            )
            story.append(
                Paragraph(
                    _esc(f"Topic {rd.fmt_topic(tid, row.get('current_topic_label'))}"),
                    styles["H2Custom"],
                )
            )
            story.append(
                Paragraph(
                    _esc(
                        f"Old taxonomy: {rd.fmt_leaf(row.get('current_taxonomy_id'), row.get('current_taxonomy_name'))}"
                    ),
                    styles["Meta"],
                )
            )
            story.append(
                Paragraph(
                    _esc(
                        f"New code: {row.get(code_col)}  (norm: {row.get('code_norm')})  |  "
                        f"mixed={bool(row.get('mixed_topic'))}"
                        + (
                            f"  |  main_couple_prob={row.get('main_couple_prob')}"
                            if hyp == "H6"
                            else ""
                        )
                    ),
                    styles["Meta"],
                )
            )
            main = list((review.get("keywords") or {}).get("Main") or [])[:10]
            if main:
                story.append(
                    Paragraph(_esc("Keywords: " + ", ".join(str(x) for x in main)), styles["Meta"])
                )
            for sn in list(review.get("stage08_snippets") or [])[:3]:
                story.append(
                    Paragraph(_esc("« " + " ".join(str(sn).split()) + " »"), styles["Quote"])
                )
            if sents:
                story.append(Paragraph("<b>Novel sentences</b>", styles["Meta"]))
                for s in sents:
                    meta = []
                    if s.get("book_id_anon"):
                        meta.append(str(s["book_id_anon"]))
                    elif s.get("sid"):
                        sid = str(s["sid"])
                        meta.append(sid.rsplit("_", 1)[0] if "_" in sid else sid)
                    if s.get("cell"):
                        meta.append(str(s["cell"]))
                    if s.get("tertile"):
                        meta.append(f"tertile={s['tertile']}")
                    head = f"[{' · '.join(meta)}] " if meta else ""
                    story.append(
                        Paragraph(
                            _esc(head + " ".join(str(s.get("sentence") or "").split())),
                            styles["Quote"],
                        )
                    )
            else:
                story.append(Paragraph(_esc("(no sentences in packet)"), styles["Meta"]))

            story.append(Paragraph("<b>Model reasonings</b>", styles["Meta"]))
            for label, ck, rk in (
                ("A lexical", "code_a", "rationale_a"),
                ("B contextual", "code_b", "rationale_b"),
                ("C adjudicate", "code_c", "rationale_c"),
            ):
                code = audit.get(ck)
                rat = audit.get(rk) or ""
                action = f" action={audit.get('action')}" if label.startswith("C") and audit.get("action") else ""
                story.append(
                    Paragraph(_esc(f"{label}: {code}{action}"), styles["BodyCustom"])
                )
                if rat:
                    story.append(
                        Preformatted(_wrap_plain(rat, width=100), styles["CodeBlock"])
                    )
        story.append(PageBreak())

    doc.build(story)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Defaults to results/.../human_review/",
    )
    args = parser.parse_args(argv)

    cfg = load_stage11_config(args.config)
    master = nh.load_master(cfg)
    out_dir = Path(args.out_dir) if args.out_dir else cfg.output_path("human_review_dir", create=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    md_path = out_dir / "stage11_human_review_all_topics.md"
    pdf_path = out_dir / "stage11_human_review_all_topics.pdf"

    print(f"Building markdown → {md_path}")
    md = build_markdown(cfg, master)
    md_path.write_text(md, encoding="utf-8")
    print(f"  {md_path.stat().st_size / 1e6:.2f} MB, {md.count(chr(10)):,} lines")

    print(f"Building PDF → {pdf_path}")
    build_pdf(cfg, master, pdf_path)
    print(f"  {pdf_path.stat().st_size / 1e6:.2f} MB")

    # Per-hypothesis markdown slices (easier to open on GitHub)
    for hyp in HYPOTHESES:
        df, lex_idx, ctx_idx, adj_idx = collect_hypothesis_topics(cfg, master, hyp)
        code_col = CODE_FIELD[hyp]
        chunk = [
            f"# {HYP_TITLES[hyp]}",
            "",
            f"Run: `{cfg.run_id}` — {len(df)} topics.",
            "",
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
                )
            )
        p = out_dir / f"stage11_human_review_{hyp.lower()}.md"
        p.write_text("\n".join(chunk), encoding="utf-8")
        print(f"  wrote {p.name} ({p.stat().st_size / 1e3:.0f} KB)")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
