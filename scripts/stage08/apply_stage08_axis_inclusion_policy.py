#!/usr/bin/env python3
"""Apply Stage09 axis-inclusion policy to Stage08 labels (call 73, v2_c8).

Policy (2026-06-27):
- Discourse topics stay in analysis: exclude_from_axes=false.
- Scene topics flagged tiny_topic only are included (less conservative Stage09 pool).
- is_noise / publisher_boilerplate / character-name artifacts remain excluded.
- Spot-check overrides for character_name false positives and large discourse topics.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_LABELS = (
    ROOT
    / "results/stage08_llm_labeling/placeholder_v4_call73/legacy_v2"
    / "labels_pos_openrouter_anthropic_claude-sonnet-4.6_romance_aware_paraphrase-MiniLM-L6-v2_v2_c8_character_names.json"
)

# Manual review overrides (character_name false positives + relabeled beats).
TOPIC_OVERRIDES: dict[int, dict] = {
    57: {
        "label": "Dream and Nightmare Imagery",
        "content_type": "scene",
        "exclude_from_axes": False,
        "is_noise": False,
        "primary_categories": ["romance_core", "relationship_conflict"],
        "secondary_categories": ["activity:reflection"],
        "scene_summary": (
            "A character voices or experiences dreams, nightmares, or long-held wishes "
            "that surface in intimate or tense conversation."
        ),
        "rationale": (
            "BERTopic Main centers on dream/dreams/nightmare vocabulary; snippets show "
            "characters sharing dream imagery or nightmares, not a name artifact. "
            "Included on Stage09 axes as an emotional disclosure scene."
        ),
    },
    79: {
        "label": "Insults and Name-Calling in Conflict",
        "content_type": "scene",
        "exclude_from_axes": False,
        "is_noise": False,
        "primary_categories": ["relationship_conflict", "romance_core"],
        "secondary_categories": ["activity:argument"],
        "scene_summary": (
            "Characters trade insults or call each other foolish during a heated "
            "relationship argument."
        ),
        "rationale": (
            "Main keywords are insult lexicon (stupid, fool, asshole). Snippets are "
            "argument beats, not a name cluster. Stage07 character_name flag overridden."
        ),
    },
    95: {
        "label": "Remembering and Forgetting Past Acts",
        "content_type": "scene",
        "exclude_from_axes": False,
        "is_noise": False,
        "primary_categories": ["relationship_conflict", "romance_core"],
        "secondary_categories": ["activity:argument"],
        "scene_summary": (
            "A character invokes what the other has done or failed to do in the past, "
            "pressing memory, gratitude, or blame."
        ),
        "rationale": (
            "Main cluster is remember/forget/forgotten; snippets are relational memory "
            "speech acts with emotional stakes, not a name artifact."
        ),
    },
    111: {
        "label": "Control and Strength Negotiation",
        "content_type": "scene",
        "exclude_from_axes": False,
        "is_noise": False,
        "primary_categories": ["relationship_conflict"],
        "secondary_categories": ["relationship:long_term"],
        "scene_summary": (
            "One character urges another to stay strong, yield control, or manage "
            "their composure during a tense relationship exchange."
        ),
        "rationale": (
            "Main cluster is control/strength/strong; snippets show power-and-control "
            "negotiation in couples talk, not a name artifact."
        ),
    },
}


def _posthoc_reason(entry: dict) -> str:
    return str(entry.get("stage07_posthoc_reason") or "")


def apply_policy(entry: dict) -> dict:
    out = copy.deepcopy(entry)
    reason = _posthoc_reason(out)
    content_type = out.get("content_type", "")
    label = str(out.get("label", ""))

    if "publisher_boilerplate" in reason:
        out["exclude_from_axes"] = True
        out["is_noise"] = True
        return out

    if label == "Character Name Artifact" or (
        content_type == "noise" and out.get("is_noise")
    ):
        out["exclude_from_axes"] = True
        out["is_noise"] = True
        return out

    # Discourse and scene beats stay in analysis even when LLM marked is_noise for tiny/weak topics.
    if content_type == "discourse":
        out["is_noise"] = False
        out["exclude_from_axes"] = False
        return out

    if content_type == "scene":
        out["is_noise"] = False
        out["exclude_from_axes"] = False
        return out

    if out.get("is_noise") or content_type == "noise":
        out["exclude_from_axes"] = True
        return out

    # subgenre_marker, procedural_transition, paratext, etc.
    if content_type in {"paratext"}:
        out["exclude_from_axes"] = True
    else:
        out.setdefault("exclude_from_axes", False)

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply Stage09 axis-inclusion policy to labels JSON")
    parser.add_argument("--input", type=Path, default=DEFAULT_LABELS)
    parser.add_argument("--output", type=Path, default=None, help="Default: overwrite --input")
    args = parser.parse_args()

    labels: dict = json.loads(args.input.read_text(encoding="utf-8"))
    stats = {
        "discourse_included": 0,
        "tiny_scene_included": 0,
        "overrides": 0,
        "still_excluded": 0,
        "included_total": 0,
    }

    for tid_str, entry in labels.items():
        tid = int(tid_str)
        before_ex = entry.get("exclude_from_axes")

        if tid in TOPIC_OVERRIDES:
            entry.update(copy.deepcopy(TOPIC_OVERRIDES[tid]))
            stats["overrides"] += 1

        entry = apply_policy(entry)
        labels[tid_str] = entry

        after_ex = entry.get("exclude_from_axes")
        if before_ex and not after_ex:
            if entry.get("content_type") == "discourse":
                stats["discourse_included"] += 1
            elif "tiny_topic" in _posthoc_reason(entry):
                stats["tiny_scene_included"] += 1

        if after_ex:
            stats["still_excluded"] += 1
        else:
            stats["included_total"] += 1

    out_path = args.output or args.input
    out_path.write_text(json.dumps(labels, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {out_path} ({len(labels)} topics)")
    print(f"  Included for Stage09 axes: {stats['included_total']}")
    print(f"  Still excluded: {stats['still_excluded']}")
    print(f"  Discourse flipped to include: {stats['discourse_included']}")
    print(f"  Tiny scene flipped to include: {stats['tiny_scene_included']}")
    print(f"  Manual overrides applied: {stats['overrides']}")


if __name__ == "__main__":
    main()
