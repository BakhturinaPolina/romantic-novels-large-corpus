#!/usr/bin/env python3
"""Compare v3 sexual-subset labels across OpenRouter models vs gold YAML."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.stage08_llm_labeling.openrouter_experiments.tools.validate_label_quality import (
    compare_against_gold_yaml,
)

OUT_DIR = ROOT / "results/stage08_llm_labeling/placeholder_v4_call73"
GOLD = ROOT / "configs/stage08_v3_sexual_subset_gold.yaml"
REPORT = ROOT / "results/reports/stage08_v3_sexual_model_comparison.md"

MODEL_GLOBS = [
    ("claude-sonnet-4.6", "anthropic_claude-sonnet-4.6*v3_sexual_subset_topics.json"),
    ("lumimaid-70b", "*lumimaid70b*topics.json"),
    ("grok-4.20", "*grok420*topics.json"),
    ("dolphin-24b-venice-free", "*dolphin24b*topics.json"),
]


def find_labels(pattern: str) -> Path | None:
    matches = sorted(OUT_DIR.glob(f"labels_pos_openrouter_{pattern}"))
    return matches[-1] if matches else None


def main() -> None:
    rows = []
    detail_frames = []

    for short_name, pattern in MODEL_GLOBS:
        path = find_labels(pattern)
        if path is None:
            rows.append({
                "model": short_name,
                "status": "missing",
                "topics": 0,
                "fn_agreement": None,
                "axis_agreement": None,
                "cliches": None,
                "overall_pass": None,
                "path": "",
            })
            continue
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        df, summary = compare_against_gold_yaml(data, GOLD)
        df["model"] = short_name
        detail_frames.append(df)
        rows.append({
            "model": short_name,
            "status": "ok",
            "topics": summary["topics_compared"],
            "fn_agreement": f"{summary['sexual_function_agreement']:.1%}",
            "axis_agreement": f"{summary['axis_hint_agreement']:.1%}",
            "cliches": summary["genre_cliche_count"],
            "overall_pass": summary["overall_pass"],
            "path": str(path.relative_to(ROOT)),
        })

    summary_df = pd.DataFrame(rows)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Stage08 v3 sexual-topic model comparison",
        "",
        "Gold reference: `configs/stage08_v3_sexual_subset_gold.yaml` (28 topics).",
        "Prompt: `v3_sexual_precision` | temp 0.0 | max_tokens 256",
        "",
        "## Summary",
        "",
    ]
    lines.append("| model | status | topics | fn_agreement | axis_agreement | cliches | overall_pass |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for _, r in summary_df.iterrows():
        lines.append(
            f"| {r['model']} | {r['status']} | {r['topics']} | {r['fn_agreement']} | "
            f"{r['axis_agreement']} | {r['cliches']} | {r['overall_pass']} |"
        )
    lines.append("")

    if detail_frames:
        issues = pd.concat(detail_frames, ignore_index=True)
        issues = issues[issues["has_issues"] == True][  # noqa: E712
            ["model", "topic_id", "label", "sexual_function", "axis_hint", "issues"]
        ]
        if not issues.empty:
            lines += ["## Issues by model", ""]
            for _, r in issues.iterrows():
                lines.append(
                    f"- **{r['model']}** topic {r['topic_id']}: `{r['label']}` — {r['issues']}"
                )
            lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(summary_df.to_string(index=False))
    print(f"\nWrote {REPORT}")


if __name__ == "__main__":
    main()
