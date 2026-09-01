#!/usr/bin/env python3
"""Generate A/B/C plot variants for presentation visual QA."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stage11_refined_construct_analysis.analysis.presentation_suite.plot_variants import generate_all_variants


def main() -> None:
    df = generate_all_variants()
    print(f"Generated {len(df)} variant records → variants/visual_qa.csv")


if __name__ == "__main__":
    main()
