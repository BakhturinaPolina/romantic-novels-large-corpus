#!/usr/bin/env python3
"""Convert percent-format `_src/*.py` into notebooks under `notebooks/08_refined_construct_analysis/`.

Same converter as Stage 10; notebooks never call the OpenRouter API.

Usage:
  .venv/bin/python scripts/stage11/percent_to_notebook.py notebooks/08_refined_construct_analysis/_src/*.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Reuse the Stage 10 converter implementation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "stage10"))
from percent_to_notebook import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
