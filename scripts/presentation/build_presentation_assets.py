#!/usr/bin/env python3
"""Build v2 presentation deck (slide-aligned figures + catalogs).

Usage:
  .venv/bin/python scripts/presentation/build_presentation_assets.py
  .venv/bin/python scripts/presentation/build_presentation_assets.py --deck v2
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
