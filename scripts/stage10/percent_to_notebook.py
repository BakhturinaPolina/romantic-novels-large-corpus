#!/usr/bin/env python3
"""Convert a percent-format Python file into a .ipynb with the repo's kernel metadata.

The notebooks in `notebooks/07_analysis/` are authored as percent-format `.py` sources under
`notebooks/07_analysis/_src/`, which are reviewable in a diff, and converted here. Re-running
this after editing a source file regenerates the notebook with cleared outputs.

  # %% [markdown]
  # ## A heading
  # Prose here.

  # %%
  code_here()

Usage:
  .venv/bin/python scripts/stage10/percent_to_notebook.py notebooks/07_analysis/_src/*.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

KERNEL_METADATA: Dict[str, object] = {
    "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.12.3",
    },
}


def split_cells(text: str) -> List[Tuple[str, str]]:
    cells: List[Tuple[str, str]] = []
    kind = "code"
    buffer: List[str] = []

    def flush() -> None:
        body = "\n".join(buffer).strip("\n")
        if body:
            cells.append((kind, body))
        buffer.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# %%"):
            flush()
            kind = "markdown" if "[markdown]" in stripped else "code"
            continue
        if kind == "markdown":
            # Markdown lines are comment-prefixed in percent format.
            buffer.append(line[2:] if line.startswith("# ") else line.lstrip("#"))
        else:
            buffer.append(line)
    flush()
    return cells


def to_notebook(cells: List[Tuple[str, str]]) -> Dict[str, object]:
    out = []
    for position, (kind, body) in enumerate(cells):
        lines = body.split("\n")
        source = [f"{line}\n" for line in lines[:-1]] + [lines[-1]]
        cell: Dict[str, object] = {
            "cell_type": kind,
            "id": f"cell-{position:03d}",
            "metadata": {},
            "source": source,
        }
        if kind == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        out.append(cell)
    return {"cells": out, "metadata": KERNEL_METADATA, "nbformat": 4, "nbformat_minor": 5}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", type=Path)
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="Defaults to the parent of the source file's directory.")
    args = ap.parse_args()

    for source in args.sources:
        text = source.read_text(encoding="utf-8")
        notebook = to_notebook(split_cells(text))
        out_dir = args.out_dir or source.parent.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / f"{source.stem}.ipynb"
        target.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        n_md = sum(1 for c in notebook["cells"] if c["cell_type"] == "markdown")
        print(f"{source.name} -> {target} ({len(notebook['cells'])} cells, {n_md} markdown)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
