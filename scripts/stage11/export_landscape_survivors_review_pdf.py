#!/usr/bin/env python3
"""Export a human-review PDF for Stage10 topic-landscape survivors (38 topics).

Topics that pass |Cliff's delta| >= 0.11 and bootstrap CI excludes zero in
``01_topic_landscape``. Same evidence layout as the H3 manual-freeze pack
(keywords, BERTopic docs, Stage08 snippets, CELL samples when packets exist).

Usage:
  .venv/bin/python scripts/stage11/export_landscape_survivors_review_pdf.py
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stage11_refined_construct_analysis.analysis import notebook_helpers as nh
from src.stage11_refined_construct_analysis.analysis import review_display as rd
from src.stage11_refined_construct_analysis.analysis.h4_manual_freeze import (
    FREEZE_CELLS,
    load_freeze_review_sentences,
    preload_freeze_neighbor_cache,
)
from src.stage11_refined_construct_analysis.config import DEFAULT_CONFIG_PATH, load_stage11_config
from src.stage11_refined_construct_analysis.evidence.packets import load_representative_docs

SURVIVORS_CSV = (
    ROOT
    / "results/stage10_correlation_analysis/v4_l12_granular_final_call49"
    / "notebook_analysis/01_topic_landscape/tables/topic_tier_effects_full.csv"
)
TOPIC_INFO_CSV = (
    ROOT
    / "results/experiments/v4_l12_granular_final_call49/final_compare/call_49/topic_info.csv"
)
STAGE08_LABELS_JSON = (
    ROOT
    / "results/stage08_llm_labeling/placeholder_v4_call49/production"
    / "labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v3_topic_labeling.json"
)
STAGE07_QUALITY_CSV = (
    ROOT
    / "results/stage07_topic_quality/placeholder_v4_call49/topic_quality_placeholder_v4_call49.csv"
)

DELTA_GATE = 0.11

REVIEW_NOTES = """\
Review notes (landscape survivors — effect-size gate)

1. These 38 topics are the only ones with |Cliff's delta| >= 0.11 and a
   bootstrap CI that excludes zero (high vs low rating tier).
2. Read keywords + sentences before trusting the Stage08 label. Three topics
   were never labeled (absent from topic_lookup / Stage08 JSON).
3. Unlabeled survivors (topic 8, 309, 310) were excluded upstream:
   - 8: Stage07 HARD_EXCLUDE publisher_boilerplate
   - 309 / 310: Stage07 soft_review tiny_topic; never routed to Stage08 label
4. Checklist: is the topic interpretable romance content, residual
   discourse/boilerplate, or mixed? Suggest a label if unlabeled.
"""


def _load_human_review_export():
    path = Path(__file__).resolve().parent / "export_human_review_pdf.py"
    spec = importlib.util.spec_from_file_location("stage11_export_human_review_pdf", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_h3_export():
    path = Path(__file__).resolve().parent / "export_h3_manual_freeze_pdf.py"
    spec = importlib.util.spec_from_file_location("stage11_export_h3_manual_freeze_pdf", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_hr = _load_human_review_export()
_h3 = _load_h3_export()
_esc = _hr._esc
load_book_map = _hr.load_book_map
load_books_index = _hr.load_books_index
load_cell_meanings = _hr.load_cell_meanings
sentence_source_line = _hr.sentence_source_line
four_keyword_reps = _h3.four_keyword_reps
bertopic_sentences = _h3.bertopic_sentences


def _parse_listish(val: Any) -> List[str]:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    s = str(val).strip()
    if not s:
        return []
    try:
        parsed = ast.literal_eval(s)
        if isinstance(parsed, (list, tuple)):
            return [str(x).strip() for x in parsed if str(x).strip()]
    except (SyntaxError, ValueError):
        pass
    return [p.strip() for p in s.split(",") if p.strip()]


def load_survivors(path: Path = SURVIVORS_CSV) -> pd.DataFrame:
    df = pd.read_csv(path)
    mask = (df["cliffs_delta"].abs() >= DELTA_GATE) & (df["ci_excludes_zero"].astype(bool))
    out = df.loc[mask].copy()
    out["topic_id"] = out["topic_id"].astype(int)
    out = out.sort_values("cliffs_delta", key=lambda s: s.abs(), ascending=False)
    return out.reset_index(drop=True)


def load_topic_info_index(path: Path = TOPIC_INFO_CSV) -> Dict[int, Dict[str, Any]]:
    df = pd.read_csv(path)
    out: Dict[int, Dict[str, Any]] = {}
    for _, row in df.iterrows():
        tid = int(row["Topic"])
        if tid < 0:
            continue
        out[tid] = {
            "name": row.get("Name"),
            "count": int(row["Count"]) if pd.notna(row.get("Count")) else None,
            "representations": {
                "Main": _parse_listish(row.get("Representation")),
                "KeyBERT": _parse_listish(row.get("KeyBERT")),
                "POS": _parse_listish(row.get("POS")),
                "MMR": _parse_listish(row.get("MMR")),
            },
            "representative_docs": _parse_listish(row.get("Representative_Docs")),
        }
    return out


def load_stage08_labels(path: Path = STAGE08_LABELS_JSON) -> Dict[int, Dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: Dict[int, Dict[str, Any]] = {}
    for key, value in raw.items():
        try:
            tid = int(key)
        except (TypeError, ValueError):
            continue
        if isinstance(value, dict):
            out[tid] = value
    return out


def load_stage07_notes(path: Path = STAGE07_QUALITY_CSV) -> Dict[int, Dict[str, Any]]:
    if not path.exists():
        return {}
    df = pd.read_csv(path)
    tid_col = "Topic" if "Topic" in df.columns else "topic_id"
    out: Dict[int, Dict[str, Any]] = {}
    for _, row in df.iterrows():
        tid = int(row[tid_col])
        out[tid] = {
            "stage07_reason": row.get("stage07_reason"),
            "noise_reason": row.get("noise_reason"),
            "recommended_next_step": row.get("recommended_next_step"),
            "hard_exclude_candidate": bool(row.get("hard_exclude_candidate")),
            "soft_review_candidate": bool(row.get("soft_review_candidate")),
            "inspection_label": row.get("inspection_label"),
            "snippets": [
                str(row.get(f"snippet_{i}")).strip()
                for i in range(1, 7)
                if pd.notna(row.get(f"snippet_{i}")) and str(row.get(f"snippet_{i}")).strip()
            ],
        }
    return out


def enrich_row(
    row: Mapping[str, Any],
    *,
    stage08: Mapping[int, Mapping[str, Any]],
    topic_info: Mapping[int, Mapping[str, Any]],
    stage07: Mapping[int, Mapping[str, Any]],
) -> Dict[str, Any]:
    tid = int(row["topic_id"])
    s08 = dict(stage08.get(tid) or {})
    info = dict(topic_info.get(tid) or {})
    s07 = dict(stage07.get(tid) or {})
    label = row.get("label")
    if label is None or (isinstance(label, float) and pd.isna(label)) or not str(label).strip():
        label = s08.get("label")
    unlabeled = label is None or (isinstance(label, float) and pd.isna(label)) or not str(label).strip()
    return {
        **dict(row),
        "topic_id": tid,
        "current_topic_label": None if unlabeled else str(label),
        "unlabeled": bool(unlabeled),
        "current_taxonomy_id": row.get("taxonomy_main_id"),
        "current_taxonomy_name": row.get("taxonomy_main_name"),
        "main_keywords": (info.get("reps") or {}).get("Main") or s08.get("keywords"),
        "keybert_keywords": (info.get("reps") or {}).get("KeyBERT"),
        "pos_keywords": (info.get("reps") or {}).get("POS"),
        "mmr_keywords": (info.get("reps") or {}).get("MMR"),
        "topic_info_reps": info.get("reps") or {},
        "topic_info_docs": info.get("representative_docs") or [],
        "stage08": s08,
        "stage07": s07,
        "doc_count": info.get("count"),
    }



def _render_sentence_fallback_md(
    sents: Sequence[Mapping[str, Any]],
    bt: Mapping[str, Sequence[str]],
    *,
    cell_hit_count: int,
) -> List[str]:
    """When CELL buckets are empty, still show packet / representative sentences."""
    lines: List[str] = []
    if cell_hit_count > 0:
        return lines
    if sents:
        lines.append("**Other packet sentences** (not tagged CELL_A–D)")
        lines.append("")
        for i, s in enumerate(sents[:12], start=1):
            text = " ".join(str(s.get("display_sentence") or s.get("sentence") or "").split())
            cell = str(s.get("cell") or "—")
            lines.append(f"> {i}. [{cell}] {text}")
            lines.append("")
        return lines
    if bt.get("packet_representatives"):
        lines.append("**Packet representative sentences** (fallback when CELL sample empty)")
        lines.append("")
        for i, text in enumerate(bt["packet_representatives"], start=1):
            lines.append(f"> {i}. {text}")
            lines.append("")
    return lines

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


def _kw_from_enriched(enriched: Mapping[str, Any], review: Mapping[str, Any]) -> Dict[str, List[str]]:
    # Prefer review packet reps; else Stage08/topic_info via a fake row for four_keyword_reps.
    fake = {
        "main_keywords": enriched.get("main_keywords"),
        "keybert_keywords": enriched.get("keybert_keywords"),
        "pos_keywords": enriched.get("pos_keywords"),
        "mmr_keywords": enriched.get("mmr_keywords"),
    }
    review2 = dict(review)
    if not review2.get("representations") and enriched.get("topic_info_reps"):
        review2["representations"] = enriched["topic_info_reps"]
    return four_keyword_reps(fake, review2)


def topic_markdown_block(
    cfg,
    enriched: Mapping[str, Any],
    *,
    meanings: Mapping[str, str],
    books: pd.DataFrame,
    neighbor_cache=None,
    rep_docs_by_topic: Optional[Mapping[int, Sequence[str]]] = None,
) -> str:
    tid = int(enriched["topic_id"])
    review = rd.load_topic_review(cfg, tid)
    book_map = load_book_map(cfg, tid)
    sents, meta = load_freeze_review_sentences(
        cfg, tid, book_map, neighbor_cache=neighbor_cache
    )
    kws = _kw_from_enriched(enriched, review)
    bt = bertopic_sentences(
        review, rep_docs_by_topic=rep_docs_by_topic or {}, topic_id=tid
    )
    # Fall back to topic_info Representative_Docs when CSV/packet empty
    if not bt["bertopic_representative_docs"] and enriched.get("topic_info_docs"):
        bt["bertopic_representative_docs"] = list(enriched["topic_info_docs"])[:8]
    if not bt["stage08_snippets"]:
        s07_snips = (enriched.get("stage07") or {}).get("snippets") or []
        s08_snips = (enriched.get("stage08") or {}).get("snippets") or []
        bt["stage08_snippets"] = [str(x) for x in (s08_snips or s07_snips)][:8]

    label = enriched.get("current_topic_label") or "UNLABELED"
    tax = rd.fmt_leaf(enriched.get("current_taxonomy_id"), enriched.get("current_taxonomy_name"))
    delta = float(enriched["cliffs_delta"])
    direction = "more in HIGH-rated" if delta > 0 else "more in LOW-rated"
    cov = _coverage_note(meta)
    s07 = enriched.get("stage07") or {}

    lines = [
        f"### Topic {rd.fmt_topic(tid, None if enriched.get('unlabeled') else label)}",
        "",
        f"- **Label:** {'**UNLABELED** (absent from Stage08 / topic_lookup)' if enriched.get('unlabeled') else label}",
        f"- **Taxonomy:** {tax}",
        f"- **Cliff's delta:** {delta:+.4f} [{float(enriched['ci_low']):+.4f}, {float(enriched['ci_high']):+.4f}] "
        f"— {enriched.get('magnitude')} — {direction}",
        f"- **Mean share:** high {float(enriched.get('mean_a', float('nan')))*100:.3f}% vs "
        f"low {float(enriched.get('mean_b', float('nan')))*100:.3f}% "
        f"(n_high={int(enriched.get('n_a', 0))}, n_low={int(enriched.get('n_b', 0))})",
    ]
    if enriched.get("doc_count") is not None:
        lines.append(f"- **BERTopic cluster size:** {enriched['doc_count']} docs")
    if enriched.get("unlabeled") and s07:
        lines.append(
            f"- **Stage07 exclusion:** {s07.get('inspection_label') or s07.get('stage07_reason') or '—'} "
            f"(next={s07.get('recommended_next_step') or '—'})"
        )
    lines.extend(
        [
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
    )
    if bt["bertopic_representative_docs"]:
        for i, text in enumerate(bt["bertopic_representative_docs"], start=1):
            lines.append(f"> {i}. {text}")
            lines.append("")
    else:
        lines.append("_No BERTopic representative_docs for this topic._")
        lines.append("")

    lines.append("**Stage-08 / Stage-07 snippets**")
    lines.append("")
    if bt["stage08_snippets"]:
        for i, text in enumerate(bt["stage08_snippets"], start=1):
            lines.append(f"> {i}. {text}")
            lines.append("")
    else:
        lines.append("_No snippets._")
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

    cell_hits = sum(len(by_cell[c]) for c in FREEZE_CELLS)
    lines.extend(_render_sentence_fallback_md(sents, bt, cell_hit_count=cell_hits))

    lines.extend(
        [
            "**Manual checklist** (fill in)",
            "",
            "- Interpretable romance content: yes / no / mixed",
            "- Noise / boilerplate / discourse residue: yes / no",
            "- Suggested label (if unlabeled or wrong): ________",
            "- Keep in landscape narrative: KEEP / DROP / FLAG",
            "- Notes: ________",
            "",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def build_markdown(
    cfg,
    rows: Sequence[Mapping[str, Any]],
    *,
    meanings: Mapping[str, str],
    books: pd.DataFrame,
    neighbor_cache=None,
    rep_docs_by_topic: Optional[Mapping[int, Sequence[str]]] = None,
) -> str:
    n_unlab = sum(1 for r in rows if r.get("unlabeled"))
    more_high = [r for r in rows if float(r["cliffs_delta"]) > 0]
    more_low = [r for r in rows if float(r["cliffs_delta"]) < 0]
    lines = [
        f"# Landscape survivors review — |δ| ≥ 0.11 + CI excludes 0 ({len(rows)} topics)",
        "",
        f"Run: `{cfg.run_id}` — {len(rows)} topics "
        f"({len(more_high)} more in high-rated, {len(more_low)} more in low-rated; "
        f"{n_unlab} unlabeled).",
        "",
        "No LLM adjudication. Read evidence, then fill KEEP/DROP/FLAG.",
        "",
        "```",
        REVIEW_NOTES.strip(),
        "```",
        "",
        "## Unlabeled survivors (why blank in the notebook)",
        "",
        "| Topic | Stage07 | Why no Stage08 label |",
        "| --- | --- | --- |",
        "| 8 | HARD_EXCLUDE `publisher_boilerplate` | Excluded before LLM labeling (EPUB copyright / buy-links) |",
        "| 309 | soft_review `tiny_topic` | Soft-excluded; degenerate “she shook her head” cluster |",
        "| 310 | soft_review `tiny_topic` | Soft-excluded; thin “hold / holding” cluster never labeled |",
        "",
        "These three are among 25 topics absent from `topic_lookup.parquet` "
        "(348 labeled of 374 BERTopic topics), so `LABELS.get(...)` is NaN in "
        "`01_topic_landscape`.",
        "",
    ]

    lines.append(f"## More in high-rated books ({len(more_high)})")
    lines.append("")
    for enriched in more_high:
        lines.append(
            topic_markdown_block(
                cfg,
                enriched,
                meanings=meanings,
                books=books,
                neighbor_cache=neighbor_cache,
                rep_docs_by_topic=rep_docs_by_topic,
            )
        )

    lines.append(f"## More in low-rated books ({len(more_low)})")
    lines.append("")
    for enriched in more_low:
        lines.append(
            topic_markdown_block(
                cfg,
                enriched,
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
            "LandSurvTitle", parent=base["Title"], fontSize=16, leading=20, spaceAfter=8
        ),
        "H1": ParagraphStyle(
            "LandSurvH1", parent=base["Heading1"], fontSize=13, leading=16, spaceBefore=10, spaceAfter=6
        ),
        "H2": ParagraphStyle(
            "LandSurvH2", parent=base["Heading2"], fontSize=11, leading=14, spaceBefore=8, spaceAfter=4
        ),
        "Body": ParagraphStyle(
            "LandSurvBody", parent=base["BodyText"], fontSize=9, leading=12, spaceAfter=3
        ),
        "Meta": ParagraphStyle(
            "LandSurvMeta", parent=base["BodyText"], fontSize=9, leading=11, spaceAfter=2
        ),
        "Quote": ParagraphStyle(
            "LandSurvQuote",
            parent=base["BodyText"],
            fontSize=8.5,
            leading=11,
            leftIndent=8,
            spaceAfter=2,
        ),
        "CodeBlock": ParagraphStyle(
            "LandSurvCode", parent=base["Code"], fontSize=7.5, leading=9.5, spaceAfter=6
        ),
        "Checklist": ParagraphStyle(
            "LandSurvCheck",
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
    rows: Sequence[Mapping[str, Any]],
    pdf_path: Path,
    *,
    meanings: Mapping[str, str],
    books: pd.DataFrame,
    neighbor_cache=None,
    rep_docs_by_topic: Optional[Mapping[int, Sequence[str]]] = None,
) -> None:
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
    n_unlab = sum(1 for r in rows if r.get("unlabeled"))
    story.append(
        Paragraph(
            _esc(f"Landscape survivors review — |δ| ≥ 0.11 ({len(rows)} topics)"),
            styles["Title"],
        )
    )
    story.append(
        Paragraph(
            _esc(
                f"Run: {cfg.run_id} — {len(rows)} topics, {n_unlab} unlabeled. "
                "Fill KEEP/DROP/FLAG after reading evidence."
            ),
            styles["Meta"],
        )
    )
    story.append(Preformatted(REVIEW_NOTES.strip(), styles["CodeBlock"]))
    story.append(PageBreak())

    sections = [
        ("More in high-rated books", [r for r in rows if float(r["cliffs_delta"]) > 0]),
        ("More in low-rated books", [r for r in rows if float(r["cliffs_delta"]) < 0]),
    ]
    for title, section_rows in sections:
        if not section_rows:
            continue
        story.append(Paragraph(_esc(title), styles["H1"]))
        story.append(Paragraph(_esc(f"{len(section_rows)} topics"), styles["Meta"]))
        for enriched in section_rows:
            tid = int(enriched["topic_id"])
            review = rd.load_topic_review(cfg, tid)
            book_map = load_book_map(cfg, tid)
            sents, meta = load_freeze_review_sentences(
                cfg, tid, book_map, neighbor_cache=neighbor_cache
            )
            kws = _kw_from_enriched(enriched, review)
            bt = bertopic_sentences(
                review, rep_docs_by_topic=rep_docs_by_topic or {}, topic_id=tid
            )
            if not bt["bertopic_representative_docs"] and enriched.get("topic_info_docs"):
                bt["bertopic_representative_docs"] = list(enriched["topic_info_docs"])[:8]
            if not bt["stage08_snippets"]:
                s07_snips = (enriched.get("stage07") or {}).get("snippets") or []
                s08_snips = (enriched.get("stage08") or {}).get("snippets") or []
                bt["stage08_snippets"] = [str(x) for x in (s08_snips or s07_snips)][:8]
            cov = _coverage_note(meta)
            label = enriched.get("current_topic_label") or "UNLABELED"
            delta = float(enriched["cliffs_delta"])
            direction = "more in HIGH-rated" if delta > 0 else "more in LOW-rated"
            s07 = enriched.get("stage07") or {}

            block: List[Any] = []
            block.append(
                Paragraph(
                    _esc(
                        f"Topic {tid} — {label}"
                        + (" [UNLABELED]" if enriched.get("unlabeled") else "")
                    ),
                    styles["H2"],
                )
            )
            block.append(
                Paragraph(
                    _esc(
                        f"Taxonomy: {rd.fmt_leaf(enriched.get('current_taxonomy_id'), enriched.get('current_taxonomy_name'))}"
                    ),
                    styles["Meta"],
                )
            )
            block.append(
                Paragraph(
                    _esc(
                        f"Cliff's δ = {delta:+.4f} "
                        f"[{float(enriched['ci_low']):+.4f}, {float(enriched['ci_high']):+.4f}] "
                        f"({enriched.get('magnitude')}; {direction})"
                    ),
                    styles["Meta"],
                )
            )
            if enriched.get("unlabeled") and s07:
                block.append(
                    Paragraph(
                        _esc(
                            f"Stage07: {s07.get('inspection_label') or s07.get('stage07_reason')}"
                        ),
                        styles["Meta"],
                    )
                )
            block.append(
                Paragraph("<b>Four keyword representations</b> (BERTopic / labeling)", styles["Meta"])
            )
            for name in ("Main", "KeyBERT", "POS", "MMR"):
                block.append(
                    Paragraph(_esc(f"{name}: {', '.join(kws[name]) or '—'}"), styles["Body"])
                )
            block.append(Paragraph("<b>BERTopic representative docs</b>", styles["Meta"]))
            if bt["bertopic_representative_docs"]:
                for i, text in enumerate(bt["bertopic_representative_docs"], start=1):
                    block.append(Paragraph(_esc(f"{i}. {text}"), styles["Quote"]))
            else:
                block.append(
                    Paragraph(_esc("No BERTopic representative_docs."), styles["Meta"])
                )
            block.append(Paragraph("<b>Stage-08 / Stage-07 snippets</b>", styles["Meta"]))
            if bt["stage08_snippets"]:
                for i, text in enumerate(bt["stage08_snippets"], start=1):
                    block.append(Paragraph(_esc(f"{i}. {text}"), styles["Quote"]))
            else:
                block.append(Paragraph(_esc("No snippets."), styles["Meta"]))
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
            for cell in FREEZE_CELLS:
                meaning = meanings.get(cell, "")
                header = f"{cell}" + (f" ({meaning})" if meaning else "")
                cell_sents = by_cell.get(cell) or []
                if not cell_sents:
                    block.append(
                        Paragraph(_esc(f"{header}: no usable sentences in packet"), styles["Meta"])
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
            cell_hits = sum(len(by_cell[c]) for c in FREEZE_CELLS)
            if cell_hits == 0 and sents:
                block.append(
                    Paragraph(
                        "<b>Other packet sentences</b> (not tagged CELL_A–D)",
                        styles["Meta"],
                    )
                )
                for i, s in enumerate(sents[:12], start=1):
                    cell = str(s.get("cell") or "—")
                    block.append(
                        Paragraph(
                            _esc(
                                f"{i}. [{cell}] "
                                + " ".join(
                                    str(
                                        s.get("display_sentence") or s.get("sentence") or ""
                                    ).split()
                                )
                            ),
                            styles["Quote"],
                        )
                    )
            elif cell_hits == 0 and bt["packet_representatives"]:
                block.append(
                    Paragraph("<b>Packet representative sentences</b> (fallback)", styles["Meta"])
                )
                for i, text in enumerate(bt["packet_representatives"], start=1):
                    block.append(Paragraph(_esc(f"{i}. {text}"), styles["Quote"]))
            block.append(Spacer(1, 4))
            block.append(
                Paragraph(
                    _esc(
                        "CHECKLIST — Interpretable: [ yes / no / mixed ]   "
                        "Noise/boilerplate: [ yes / no ]"
                    ),
                    styles["Checklist"],
                )
            )
            block.append(
                Paragraph(
                    _esc(
                        "Suggested label: [ ________ ]   "
                        "Decision: [ KEEP / DROP / FLAG ]"
                    ),
                    styles["Checklist"],
                )
            )
            block.append(Spacer(1, 8))
            story.append(KeepTogether(block))
        story.append(PageBreak())

    doc.build(story)


def seed_decisions_worksheet(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    decisions = []
    for r in rows:
        decisions.append(
            {
                "topic_id": int(r["topic_id"]),
                "label": r.get("current_topic_label"),
                "unlabeled": bool(r.get("unlabeled")),
                "cliffs_delta": float(r["cliffs_delta"]),
                "taxonomy_main_id": None
                if pd.isna(r.get("current_taxonomy_id"))
                else str(r.get("current_taxonomy_id")),
                "interpretable": "",
                "is_noise": "",
                "suggested_label": "",
                "decision": "",
                "notes": "",
            }
        )
    return {
        "frozen": False,
        "description": "Landscape survivors (|δ|>=0.11, CI excludes 0) human review worksheet",
        "n_topics": len(decisions),
        "decisions": decisions,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--survivors-csv", default=str(SURVIVORS_CSV))
    args = parser.parse_args(argv)

    cfg = load_stage11_config(args.config)
    meanings = load_cell_meanings(cfg)
    books = load_books_index(cfg)
    rep_docs_by_topic = load_representative_docs(cfg)
    out_dir = Path(args.out_dir) if args.out_dir else cfg.output_path("human_review_dir", create=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    survivors = load_survivors(Path(args.survivors_csv))
    stage08 = load_stage08_labels()
    topic_info = load_topic_info_index()
    stage07 = load_stage07_notes()
    rows = [
        enrich_row(row, stage08=stage08, topic_info=topic_info, stage07=stage07)
        for _, row in survivors.iterrows()
    ]
    print(f"Landscape survivors: {len(rows)} topics")
    print(f"  unlabeled: {[r['topic_id'] for r in rows if r.get('unlabeled')]}")
    print(f"BERTopic representative_docs loaded for {len(rep_docs_by_topic)} topics")

    print("Preloading ±1 sentence context (one corpus scan)…")
    topic_maps = {int(r["topic_id"]): load_book_map(cfg, int(r["topic_id"])) for r in rows}
    neighbor_cache = preload_freeze_neighbor_cache(cfg, topic_maps)
    print(f"  neighbor anchors cached: {len(neighbor_cache)}")

    md_path = out_dir / "stage10_landscape_survivors_review.md"
    pdf_path = out_dir / "stage10_landscape_survivors_review.pdf"
    decisions_path = out_dir / "landscape_survivors_decisions.json"

    print(f"Building markdown → {md_path}")
    md = build_markdown(
        cfg,
        rows,
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
        rows,
        pdf_path,
        meanings=meanings,
        books=books,
        neighbor_cache=neighbor_cache,
        rep_docs_by_topic=rep_docs_by_topic,
    )
    print(f"  {pdf_path.stat().st_size / 1e3:.1f} KB")

    worksheet = seed_decisions_worksheet(rows)
    decisions_path.write_text(json.dumps(worksheet, indent=2), encoding="utf-8")
    print(f"Blank worksheet → {decisions_path}")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
