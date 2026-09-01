#!/usr/bin/env python3
"""Optional color-vision-deficiency check for presentation palette."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stage11_refined_construct_analysis.analysis.presentation_suite.paths import default_paths
from src.stage11_refined_construct_analysis.analysis.presentation_suite.theme import (
    C_NEG,
    C_NEUTRAL,
    C_POS,
    C_SELECTED,
)


def main() -> None:
    paths = default_paths()
    paths.ensure_deck_dirs()
    out = paths.deck_review / "palette_cvd_report.txt"
    lines = ["Presentation palette CVD check", ""]

    palette = {
        "C_POS": C_POS,
        "C_NEG": C_NEG,
        "C_NEUTRAL": C_NEUTRAL,
        "C_SELECTED": C_SELECTED,
    }

    try:
        import colorspacious as cs  # type: ignore

        cvd_spaces = {
            "protanomaly": "Protanomaly",
            "deuteranomaly": "Deuteranomaly",
            "tritanomaly": "Tritanomaly",
        }
        for name, hex_color in palette.items():
            rgb = tuple(int(hex_color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
            for sim_key, sim_space in cvd_spaces.items():
                transformed = cs.cspace_convert(rgb, "sRGB255", sim_space)
                lines.append(f"{name} under {sim_key}: {transformed}")
        lines.append("")
        lines.append("PASS: colorspacious simulation completed (manual review required).")
    except (ImportError, ValueError) as exc:
        lines.append(f"SKIP: colorspacious CVD check unavailable ({exc}).")
        lines.append(f"Palette: {palette}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
