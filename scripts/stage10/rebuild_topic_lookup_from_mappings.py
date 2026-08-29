#!/usr/bin/env python3
"""Rebuild topic_lookup.parquet from a Stage09 taxonomy(+Radway) JSON.

Preserves Stage08 label fields already present in the lookup (scene summary,
sexual-precision tags, keywords) and overwrites only the taxonomy_* and
radway_* columns from the mapping file. Backs up the previous parquet first.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import pandas as pd

TAXONOMY_FIELDS = {
    "main_category_id": "taxonomy_main_id",
    "main_category_name": "taxonomy_main_name",
    "main_category_group": "taxonomy_main_group",
    "secondary_category_id": "taxonomy_secondary_id",
    "secondary_category_name": "taxonomy_secondary_name",
    "secondary_category_group": "taxonomy_secondary_group",
    "confidence": "taxonomy_confidence",
    "confidence_band": "taxonomy_confidence_band",
    "is_noise": "taxonomy_is_noise",
    "exclude_from_axes": "taxonomy_exclude_from_axes",
    "content_type": "taxonomy_content_type",
    "use_in_macro_axes": "taxonomy_use_in_macro_axes",
    "use_in_theory_watchlist": "taxonomy_use_in_theory_watchlist",
    "noise_reason": "taxonomy_noise_reason",
    "evidence_quality": "taxonomy_evidence_quality",
}

RADWAY_FIELDS = {
    "radway_main_id": "radway_main_id",
    "radway_main_name": "radway_main_name",
    "radway_secondary_id": "radway_secondary_id",
    "radway_phase": "radway_phase",
    "radway_phase_name": "radway_phase_name",
    "radway_is_none": "radway_is_none",
    "radway_confidence": "radway_confidence",
    "radway_rationale": "radway_rationale",
}


def _mechanic_tags(entry: Dict[str, Any]) -> str | None:
    tags = entry.get("mechanic_tags") or []
    if isinstance(tags, str):
        return tags or None
    return ", ".join(tags) if tags else None


def rows_from_mappings(mappings: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for tid, entry in mappings.items():
        row: Dict[str, Any] = {"topic_id": int(tid)}
        for src, dst in TAXONOMY_FIELDS.items():
            row[dst] = entry.get(src)
        row["taxonomy_mechanic_tags"] = _mechanic_tags(entry)
        # Prefer nested radway_functions block; fall back to top-level keys.
        rad = entry.get("radway_functions") if isinstance(entry.get("radway_functions"), dict) else entry
        for src, dst in RADWAY_FIELDS.items():
            row[dst] = rad.get(src)
        if row.get("radway_phase") is None and row.get("radway_main_id") is not None:
            row["radway_phase"] = "NA"
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--lookup",
        type=Path,
        default=Path(
            "results/stage10_correlation_analysis/v4_l12_granular_final_call49/"
            "taxonomy_radway_eda/topic_lookup.parquet"
        ),
    )
    ap.add_argument(
        "--mappings",
        type=Path,
        default=Path(
            "results/stage09_category_mapping/stage2_radway_functions/"
            "placeholder_v4_call49_rerun2/taxonomy_with_radway.json"
        ),
        help="taxonomy_with_radway.json preferred; taxonomy_mappings.json also works",
    )
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()

    lookup = pd.read_parquet(args.lookup)
    mappings = json.loads(args.mappings.read_text(encoding="utf-8"))
    new = rows_from_mappings(mappings)

    missing = sorted(set(lookup["topic_id"]) - set(new["topic_id"]))
    extra = sorted(set(new["topic_id"]) - set(lookup["topic_id"]))
    if missing:
        raise SystemExit(f"Mappings missing {len(missing)} lookup topics, e.g. {missing[:10]}")
    if extra:
        print(f"Note: {len(extra)} mapping topic(s) not in lookup (ignored): {extra[:10]}")

    old_main = lookup.set_index("topic_id")["taxonomy_main_id"]
    old_rad = lookup.set_index("topic_id")["radway_main_id"] if "radway_main_id" in lookup else None

    keep = [c for c in lookup.columns if not c.startswith("taxonomy_") and not c.startswith("radway_")]
    # topic_id is in keep; merge new taxonomy/radway onto it
    updated = lookup[keep].merge(new, on="topic_id", how="left", validate="one_to_one")

    # Preserve column order: original non-mapping cols, then taxonomy, then radway
    tax_cols = [c for c in updated.columns if c.startswith("taxonomy_")]
    rad_cols = [c for c in updated.columns if c.startswith("radway_")]
    updated = updated[keep + tax_cols + rad_cols]

    new_main = updated.set_index("topic_id")["taxonomy_main_id"]
    changed = int((old_main.reindex(new_main.index).astype(str) != new_main.astype(str)).sum())
    rad_filled = int(updated["radway_main_id"].notna().sum())
    rad_none = int(updated["radway_is_none"].fillna(False).sum())

    if not args.no_backup:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = args.lookup.with_name(f"topic_lookup_pre_rerun2_{stamp}.parquet")
        shutil.copy2(args.lookup, backup)
        print(f"Backup -> {backup}")

    args.lookup.parent.mkdir(parents=True, exist_ok=True)
    updated.to_parquet(args.lookup, index=False)

    print(f"Wrote {len(updated)} topics -> {args.lookup}")
    print(f"  taxonomy main changed : {changed} / {len(updated)}")
    print(f"  radway filled         : {rad_filled} (none={rad_none}, functions={rad_filled - rad_none})")
    print(f"  3.1 topics            : {int((updated['taxonomy_main_id'] == '3.1').sum())}")
    print(f"  uncertain_interpretable: {int((updated['taxonomy_main_id'] == 'uncertain_interpretable').sum())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
