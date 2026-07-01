#!/usr/bin/env python3
"""Merge C8 sweep labels into full production labels JSON (no API rerun)."""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAME_ARTIFACT_LABEL = re.compile(
    r"\b("
    r"Scattered.*Name|Name Cluster|Name References|Name-Clustered|Character References"
    r")\b",
    re.IGNORECASE,
)
PROPER_IN_LABEL = re.compile(
    r"\b(Cole|Ryan|Jared|Shane|Aiden|Caleb|Noah|Rose|Josh|Travis|Callie|Miles|Dylan|Marcus|Luke|Babsie)\b",
    re.IGNORECASE,
)

# stage07 false positives — keep scene/discourse labels (validated in C8 panel)
KEEP_OVERRIDE_IDS = {
    28, 29, 52, 57, 63, 78, 79, 93, 95, 98, 105, 111, 146, 156, 163, 168,
    171, 177, 184, 200, 208, 227, 253, 271, 272, 277, 297, 314, 324, 326,
}


def _artifact_patch(entry: dict) -> dict:
    out = copy.deepcopy(entry)
    out["label"] = "Character Name Artifact"
    out["content_type"] = "noise"
    out["register"] = "neutral"
    out["exclude_from_axes"] = True
    out["is_noise"] = True
    out["merge_group_hint"] = None
    out["subgenre_hints"] = []
    out["primary_categories"] = ["narrative_style"]
    out["secondary_categories"] = []
    out["scene_summary"] = (
        "Snippets share only a character name across unrelated situations "
        "without a common scene anchor."
    )
    out["rationale"] = (
        "Topic is a character-name cluster: snippets co-occur on a proper name "
        "but lack a shared setting or action. Routed as noise per v2_c8_character_names."
    )
    return out


def _needs_artifact_patch(tid: int, entry: dict) -> bool:
    if tid in KEEP_OVERRIDE_IDS:
        return False
    reason = str(entry.get("stage07_posthoc_reason") or "")
    if "publisher_boilerplate" in reason:
        return False
    lab = str(entry.get("label", ""))
    if entry.get("content_type") == "character_name":
        return True
    if NAME_ARTIFACT_LABEL.search(lab):
        return True
    if PROPER_IN_LABEL.search(lab):
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch production labels with C8 sweep output")
    parser.add_argument(
        "--production",
        type=Path,
        default=ROOT
        / "results/stage08_llm_labeling/placeholder_v4_call73/legacy_v2"
        / "labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v2_s1_snippets_first.json",
    )
    parser.add_argument(
        "--c8-sweep",
        type=Path,
        default=ROOT
        / "results/stage08_llm_labeling/prompt_sweeps/call73/character_names"
        / "labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v2_c8_character_names_sweep_c8_topics.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT
        / "results/stage08_llm_labeling/placeholder_v4_call73/legacy_v2"
        / "labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v2_c8_character_names.json",
    )
    parser.add_argument(
        "--patch-remaining-artifacts",
        action="store_true",
        help="Apply C8-style artifact template to other obvious name-cluster labels",
    )
    args = parser.parse_args()

    prod: dict = json.loads(args.production.read_text(encoding="utf-8"))
    c8: dict = json.loads(args.c8_sweep.read_text(encoding="utf-8"))

    merged = copy.deepcopy(prod)
    merged_from_c8 = []
    for tid, entry in c8.items():
        merged[tid] = entry
        merged_from_c8.append(int(tid))

    patched = []
    if args.patch_remaining_artifacts:
        for tid, entry in merged.items():
            i = int(tid)
            if i in merged_from_c8:
                continue
            if _needs_artifact_patch(i, entry):
                merged[tid] = _artifact_patch(entry)
                patched.append(i)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {args.output} ({len(merged)} topics)")
    print(f"  Merged from C8 sweep: {len(merged_from_c8)} topics {sorted(merged_from_c8)}")
    if args.patch_remaining_artifacts:
        print(f"  Rule-patched artifacts: {len(patched)} topics {sorted(patched)}")


if __name__ == "__main__":
    main()
