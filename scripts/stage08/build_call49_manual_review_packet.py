#!/usr/bin/env python3
"""Build a printable manual-review packet for call-49 Stage08 labels.

Produces:
  1) enriched JSON twin of the labels file (representations + snippets + Stage07 flags)
  2) print-ready HTML (one topic per page, A4/Letter CSS)

Usage:
  .venv/bin/python scripts/stage08/build_call49_manual_review_packet.py
"""

from __future__ import annotations

import argparse
import html
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


DEFAULT_LABELS = Path(
    "results/stage08_llm_labeling/placeholder_v4_call49/production/"
    "labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_"
    "paraphrase-MiniLM-L6-v2_v3_topic_labeling.json"
)
DEFAULT_REPS = Path(
    "results/stage06_name_cleaning/placeholder_v4_call49/"
    "cleaned_topics_all_representations.json"
)
DEFAULT_DOCS = Path(
    "results/stage06_name_cleaning/placeholder_v4_call49/"
    "cleaned_representative_docs.csv"
)
DEFAULT_AUDIT = Path(
    "results/stage07_topic_quality/placeholder_v4_call49/"
    "stage07_topic_quality_audit.csv"
)
DEFAULT_COUNTS = Path(
    "results/experiments/placeholder_v4_models/final_compare/call_49/topic_info.csv"
)
DEFAULT_TAXONOMY = Path(
    "results/stage09_category_mapping/stage1_theory_driven_categories/"
    "placeholder_v4_call49/taxonomy_mappings.json"
)


def _words_from_rep_entries(entries) -> list[str]:
    out = []
    for e in entries or []:
        if isinstance(e, dict):
            w = e.get("word")
        elif isinstance(e, (list, tuple)) and e:
            w = e[0]
        else:
            w = e
        if w is None:
            continue
        s = str(w).strip()
        if s:
            out.append(s)
    return out


def load_representations(path: Path) -> dict[int, dict[str, list[str]]]:
    raw = json.loads(path.read_text())
    out: dict[int, dict[str, list[str]]] = defaultdict(dict)
    for rep_name, per_topic in raw.items():
        for tid, entries in per_topic.items():
            if str(tid) == "-1":
                continue
            out[int(tid)][rep_name] = _words_from_rep_entries(entries)
    return out


def load_snippets(path: Path) -> dict[int, list[str]]:
    df = pd.read_csv(path)
    out: dict[int, list[str]] = defaultdict(list)
    for _, row in df.sort_values(["topic", "doc_rank"]).iterrows():
        tid = int(row["topic"])
        if tid < 0:
            continue
        sent = str(row["sentence"]).strip()
        if sent and sent.lower() != "nan":
            out[tid].append(sent)
    return out


def load_counts(path: Path) -> dict[int, int]:
    if not path.exists():
        return {}
    df = pd.read_csv(path)
    # topic_info usually has Topic + Count
    tcol = "Topic" if "Topic" in df.columns else "topic"
    ccol = "Count" if "Count" in df.columns else "count"
    return {int(r[tcol]): int(r[ccol]) for _, r in df.iterrows() if int(r[tcol]) >= 0}


def load_stage07(path: Path) -> dict[int, dict]:
    if not path.exists():
        return {}
    df = pd.read_csv(path)
    keep = [
        c
        for c in (
            "Topic",
            "Count",
            "exclude_from_axes",
            "hard_exclude_candidate",
            "soft_review_candidate",
            "noise_candidate",
            "noise_reason",
            "recommended_next_step",
            "posthoc_reason",
            "stage07_reason",
            "inspection_label",
        )
        if c in df.columns
    ]
    out = {}
    for _, row in df.iterrows():
        tid = int(row["Topic"])
        out[tid] = {k: (None if pd.isna(row[k]) else row[k]) for k in keep if k != "Topic"}
    return out


def load_taxonomy(path: Path) -> dict[int, dict]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text())
    out: dict[int, dict] = {}
    for k, v in raw.items():
        try:
            tid = int(k)
        except (TypeError, ValueError):
            continue
        out[tid] = v
    return out


def build_packet(
    labels: dict,
    reps: dict[int, dict[str, list[str]]],
    snippets: dict[int, list[str]],
    counts: dict[int, int],
    stage07: dict[int, dict],
    taxonomy: dict[int, dict] | None = None,
) -> dict:
    labeled_ids = sorted(int(k) for k in labels)
    all_ids = sorted(set(reps) | set(labeled_ids))
    taxonomy = taxonomy or {}

    topics = []
    for tid in all_ids:
        lab = labels.get(str(tid)) or labels.get(tid)
        tax = taxonomy.get(tid)
        entry = {
            "topic_id": tid,
            "has_stage08_label": lab is not None,
            "n_docs": counts.get(tid, stage07.get(tid, {}).get("Count")),
            "representations": reps.get(tid, {}),
            "representative_snippets": snippets.get(tid, []),
            "stage07": stage07.get(tid, {}),
            "stage08": lab,
            "stage09": tax,
            "review": {
                "decision": None,  # keep / revise_label / exclude / unsure
                "notes": "",
                "revised_label": "",
            },
        }
        topics.append(entry)

    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_labels": str(DEFAULT_LABELS),
            "source_taxonomy": str(DEFAULT_TAXONOMY) if taxonomy else None,
            "n_topics_total": len(topics),
            "n_with_stage08_label": sum(1 for t in topics if t["has_stage08_label"]),
            "n_without_stage08_label": sum(1 for t in topics if not t["has_stage08_label"]),
            "n_with_stage09_taxonomy": sum(1 for t in topics if t.get("stage09")),
            "representation_names": sorted({r for t in topics for r in t["representations"]}),
            "purpose": (
                "Printable / editable twin of Stage08 labels for full manual review. "
                "Includes all representation keywords, representative snippets, "
                "and Stage09 taxonomy mappings when available."
            ),
        },
        "topics": topics,
    }


CSS = """
@page { size: Letter; margin: 0.5in; }
* { box-sizing: border-box; }
body {
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: 8.5pt;
  line-height: 1.25;
  color: #111;
  margin: 0;
  background: #fff;
}
h1 { font-size: 16pt; margin: 0 0 0.25em; }
h2 {
  font-size: 10pt;
  margin: 0 0 0.15em;
  page-break-after: avoid;
  break-after: avoid;
}
h3 { font-size: 8.5pt; margin: 0.35em 0 0.1em; page-break-after: avoid; }
.cover { page-break-after: always; padding-bottom: 0.3in; }
.cover p { max-width: 46em; }
.topic {
  border-top: 1px solid #222;
  padding: 0.35em 0 0.45em;
  margin: 0;
  break-inside: avoid;
  page-break-inside: avoid;
}
.meta { color: #444; font-size: 8pt; }
.badge {
  display: inline-block;
  border: 1px solid #555;
  padding: 0 0.3em;
  margin-right: 0.25em;
  font-size: 7.5pt;
  line-height: 1.3;
}
.badge.warn { border-color: #a40; color: #a40; }
.badge.muted { color: #666; border-color: #999; }
.badge.tax { border-color: #246; color: #246; }
.badge.macro { border-color: #063; color: #063; font-weight: 700; }
.tax-line { font-size: 8pt; margin: 0.1em 0 0.2em; color: #123; }
.headline-meta { color: #333; font-size: 8pt; margin: 0.1em 0 0.25em; }
.kw-block { margin: 0.05em 0; }
.kw-name {
  font-size: 7.5pt; font-weight: 700; color: #333;
  display: inline-block; min-width: 3.8em;
}
.kw-words { font-size: 7.5pt; }
.snippets {
  margin: 0.15em 0 0.1em 1.1em;
  padding: 0;
  font-size: 8pt;
}
.snippets li { margin: 0.08em 0; }
.rationale { font-size: 8pt; margin: 0.15em 0; color: #222; }
.review-inline {
  margin-top: 0.2em;
  font-size: 8pt;
  color: #222;
}
.check { margin-right: 0.7em; white-space: nowrap; }
.notes-line {
  display: inline-block;
  border-bottom: 1px dotted #888;
  min-width: 55%;
  height: 0.95em;
  vertical-align: bottom;
  margin-left: 0.25em;
}
.toc { columns: 3; column-gap: 1em; font-size: 8pt; }
.toc div { break-inside: avoid; margin: 0.05em 0; }
@media print {
  a { color: inherit; text-decoration: none; }
  .no-print { display: none; }
}
"""


def _esc(x) -> str:
    if x is None:
        return ""
    return html.escape(str(x))


def render_html(packet: dict) -> str:
    meta = packet["meta"]
    topics = packet["topics"]
    labeled = [t for t in topics if t["has_stage08_label"]]
    unlabeled = [t for t in topics if not t["has_stage08_label"]]

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8">',
        "<title>Call 49 Stage08 Manual Review Packet</title>",
        f"<style>{CSS}</style></head><body>",
        '<section class="cover">',
        "<h1>Call 49 — Stage08 Manual Review</h1>",
        f'<p class="meta">Generated { _esc(meta["generated_at"]) }</p>',
        "<p>Compact printable review packet for the Sonnet Stage08 labels. Topics are packed "
        "several per page: label + key flags, <strong>Stage09 taxonomy</strong>, "
        "<strong>all representation keywords</strong> "
        "(Main / KeyBERT / POS / MMR), representative snippets, and a one-line review row.</p>",
        "<p class=\"meta\">"
        f"Topics with Stage08 label: {meta['n_with_stage08_label']} · "
        f"With Stage09 taxonomy: {meta.get('n_with_stage09_taxonomy', 0)} · "
        f"Unlabeled (appendix): {meta['n_without_stage08_label']} · "
        f"Total: {meta['n_topics_total']}"
        "</p>",
        '<p class="no-print"><em>Tip: File → Print → Save as PDF. Use Letter/A4, margins ≥0.5″.</em></p>',
        "<h3>Contents (labeled)</h3>",
        '<div class="toc">',
    ]
    for t in labeled:
        lab = (t.get("stage08") or {}).get("label") or "(no label)"
        parts.append(
            f'<div><a href="#t{t["topic_id"]}">t{t["topic_id"]}</a> — {_esc(lab)}</div>'
        )
    parts.append("</div>")
    if unlabeled:
        parts.append("<h3>Appendix — unlabeled / pre-excluded</h3><div class='toc'>")
        for t in unlabeled:
            parts.append(
                f'<div><a href="#t{t["topic_id"]}">t{t["topic_id"]}</a> — (no Stage08 label)</div>'
            )
        parts.append("</div>")
    parts.append("</section>")

    for t in labeled + unlabeled:
        parts.append(render_topic_html(t))

    parts.append("</body></html>")
    return "\n".join(parts)


def render_topic_html(t: dict) -> str:
    tid = t["topic_id"]
    s08 = t.get("stage08") or {}
    s07 = t.get("stage07") or {}
    s09 = t.get("stage09") or {}
    label = s08.get("label") or "(no Stage08 label)"
    badges = []
    if not t["has_stage08_label"]:
        badges.append('<span class="badge warn">unlabeled</span>')
    if s08.get("is_noise") or s07.get("noise_candidate") or s09.get("is_noise"):
        badges.append('<span class="badge warn">noise?</span>')
    if s08.get("exclude_from_axes") or s07.get("exclude_from_axes") or s09.get("exclude_from_axes"):
        badges.append('<span class="badge warn">exclude_axes</span>')
    if s08.get("sexual_explicitness") and s08.get("sexual_explicitness") != "none":
        badges.append(
            f'<span class="badge">{_esc(s08.get("sexual_explicitness"))}</span>'
        )
    if s08.get("content_type"):
        badges.append(f'<span class="badge muted">{_esc(s08.get("content_type"))}</span>')
    if s09.get("main_category_id"):
        badges.append(
            f'<span class="badge tax">{_esc(s09.get("main_category_id"))}</span>'
        )
    if s09.get("use_in_macro_axes"):
        badges.append('<span class="badge macro">macro</span>')

    n_docs = t.get("n_docs")
    n_docs_s = str(n_docs) if n_docs is not None else "—"
    summary = s08.get("scene_summary") or ""
    sex_fn = s08.get("sexual_function") or "—"
    consent = s08.get("consent_status") or "—"
    s07_next = s07.get("recommended_next_step") or ""
    meta_bits = [
        f"docs={_esc(n_docs_s)}",
        f"sex_fn={_esc(sex_fn)}",
        f"consent={_esc(consent)}",
    ]
    if s07_next:
        meta_bits.append(f"s07={_esc(s07_next)}")
    if summary:
        meta_bits.append(_esc(summary))

    tax_html = ""
    if s09.get("main_category_id"):
        main_name = s09.get("main_category_name") or ""
        sec_id = s09.get("secondary_category_id")
        sec_name = s09.get("secondary_category_name") or ""
        conf = s09.get("confidence")
        evid = s09.get("evidence_quality") or ""
        macro = "yes" if s09.get("use_in_macro_axes") else "no"
        sec_bit = (
            f" · sec {_esc(sec_id)}"
            + (f" ({_esc(sec_name)})" if sec_name else "")
            if sec_id
            else ""
        )
        tax_html = (
            f'<div class="tax-line"><strong>Taxonomy:</strong> '
            f'{_esc(s09.get("main_category_id"))}'
            + (f" — {_esc(main_name)}" if main_name else "")
            + sec_bit
            + f" · macro={macro}"
            + (f" · conf={_esc(conf)}" if conf is not None else "")
            + (f" · evid={_esc(evid)}" if evid else "")
            + "</div>"
        )

    kw_html = []
    for rep in ("Main", "KeyBERT", "POS", "MMR"):
        words = (t.get("representations") or {}).get(rep) or []
        kw_html.append(
            f'<div class="kw-block"><span class="kw-name">{rep}</span> '
            f'<span class="kw-words">{_esc(", ".join(words) if words else "—")}</span></div>'
        )
    if s08.get("keywords"):
        kw_html.append(
            '<div class="kw-block"><span class="kw-name">Stage08</span> '
            f'<span class="kw-words">{_esc(", ".join(s08["keywords"]))}</span></div>'
        )

    snips = t.get("representative_snippets") or []
    snip_html = (
        "<ol class='snippets'>"
        + "".join(f"<li>{_esc(s)}</li>" for s in snips)
        + "</ol>"
        if snips
        else '<p class="meta">(no snippets)</p>'
    )

    rationale = s08.get("rationale") or ""
    rationale_html = (
        f"<p class='rationale'><strong>Why:</strong> {_esc(rationale)}</p>"
        if rationale
        else ""
    )
    tax_rat = s09.get("rationale") or ""
    tax_rat_html = (
        f"<p class='rationale'><strong>Tax why:</strong> {_esc(tax_rat)}</p>"
        if tax_rat
        else ""
    )

    return f"""
<section class="topic" id="t{tid}">
  <h2>t{tid}: {_esc(label)} {" ".join(badges)}</h2>
  <div class="headline-meta">{" · ".join(meta_bits)}</div>
  {tax_html}
  {"".join(kw_html)}
  {snip_html}
  {rationale_html}
  {tax_rat_html}
  <div class="review-inline">
    <span class="check">☐ keep</span>
    <span class="check">☐ revise</span>
    <span class="check">☐ exclude</span>
    <span class="check">☐ unsure</span>
    Notes:<span class="notes-line"></span>
  </div>
</section>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", type=Path, default=DEFAULT_LABELS)
    ap.add_argument("--representations", type=Path, default=DEFAULT_REPS)
    ap.add_argument("--docs", type=Path, default=DEFAULT_DOCS)
    ap.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    ap.add_argument("--topic-info", type=Path, default=DEFAULT_COUNTS)
    ap.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=Path(
            "results/stage08_llm_labeling/placeholder_v4_call49/production/manual_review"
        ),
    )
    args = ap.parse_args()

    labels = json.loads(args.labels.read_text())
    reps = load_representations(args.representations)
    snippets = load_snippets(args.docs)
    counts = load_counts(args.topic_info)
    stage07 = load_stage07(args.audit)
    taxonomy = load_taxonomy(args.taxonomy)

    packet = build_packet(labels, reps, snippets, counts, stage07, taxonomy=taxonomy)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    json_out = args.out_dir / "call49_stage08_manual_review_enriched.json"
    html_out = args.out_dir / "call49_stage08_manual_review.html"

    json_out.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
    html_out.write_text(render_html(packet))

    print(f"wrote {json_out} ({json_out.stat().st_size / 1e6:.2f} MB)")
    print(f"wrote {html_out} ({html_out.stat().st_size / 1e6:.2f} MB)")
    print(
        f"topics: {packet['meta']['n_topics_total']} "
        f"(labeled {packet['meta']['n_with_stage08_label']}, "
        f"taxonomy {packet['meta'].get('n_with_stage09_taxonomy', 0)}, "
        f"appendix {packet['meta']['n_without_stage08_label']})"
    )


if __name__ == "__main__":
    main()
