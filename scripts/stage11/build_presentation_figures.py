#!/usr/bin/env python3
"""Build Stage 11 presentation figures from saved notebook analysis tables.

Usage:
  .venv/bin/python scripts/stage11/build_presentation_figures.py
  .venv/bin/python scripts/stage11/build_presentation_figures.py --run-id v4_l12_granular_final_call49
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stage11_refined_construct_analysis.analysis.presentation_suite.build import main

if __name__ == "__main__":
    main()
