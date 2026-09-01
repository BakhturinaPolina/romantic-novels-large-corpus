#!/usr/bin/env python3
"""Execute presentation review notebook and export HTML.

Usage:
  .venv/bin/python scripts/presentation/build_presentation_review.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NB_SRC = ROOT / "notebooks" / "09_presentation" / "_src" / "00_presentation_review.py"
NB_IPYNB = ROOT / "notebooks" / "09_presentation" / "00_presentation_review.ipynb"
OUT_DIR = ROOT / "results" / "presentation" / "final_v1" / "review"
PERCENT_SCRIPT = ROOT / "scripts" / "stage11" / "percent_to_notebook.py"


def main() -> None:
    if PERCENT_SCRIPT.exists():
        subprocess.run(
            [sys.executable, str(PERCENT_SCRIPT), str(NB_SRC)],
            check=True,
            cwd=ROOT,
        )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--execute",
            "--to",
            "html",
            str(NB_IPYNB),
            "--output-dir",
            str(OUT_DIR),
            "--output",
            "presentation_review",
        ],
        check=True,
        cwd=ROOT,
    )
    print(f"Wrote {OUT_DIR / 'presentation_review.html'}")


if __name__ == "__main__":
    main()
