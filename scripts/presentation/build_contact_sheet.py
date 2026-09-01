#!/usr/bin/env python3
"""Build contact sheet PNGs for presentation visual review."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw, ImageFont

from src.stage11_refined_construct_analysis.analysis.presentation_suite.paths import default_paths

MAIN_GRID = [
    ["slide04_pareto_selection", "slide06_context_measurement", "slide07_primary_verdict_preview"],
    ["slide08_component_effects", "slide09_attention_shift", "slide10_quality_reach_dumbbell"],
    ["slide11_richness_preview", "slide12_ees_integrated", None],
]

CELL_W, CELL_H = 640, 360
PADDING = 16
LABEL_H = 28


def _load_png(base: Path, stem: str | None) -> Image.Image | None:
    if not stem:
        return None
    for sub in ("figures", "review/figures"):
        p = base / sub / f"{stem}.png"
        if p.exists():
            return Image.open(p).convert("RGB")
    p = base / "figures" / f"{stem}.png"
    if p.exists():
        return Image.open(p).convert("RGB")
    return None


def _fit_cell(img: Image.Image) -> Image.Image:
    img.thumbnail((CELL_W - 2 * PADDING, CELL_H - LABEL_H - 2 * PADDING), Image.Resampling.LANCZOS)
    cell = Image.new("RGB", (CELL_W, CELL_H), "white")
    x = (CELL_W - img.width) // 2
    y = LABEL_H + (CELL_H - LABEL_H - img.height) // 2
    cell.paste(img, (x, y))
    return cell


def build_contact_sheet(
    paths=None,
    *,
    out_name: str = "contact_sheet_main.png",
    figure_stems: list[list[str | None]] | None = None,
) -> Path:
    paths = paths or default_paths()
    base = paths.deck_root
    grid = figure_stems or MAIN_GRID
    ncols = max(len(row) for row in grid)
    nrows = len(grid)
    sheet_w = ncols * CELL_W
    sheet_h = nrows * CELL_H
    sheet = Image.new("RGB", (sheet_w, sheet_h), "#f0f0f0")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()

    for ri, row in enumerate(grid):
        for ci, stem in enumerate(row):
            x0, y0 = ci * CELL_W, ri * CELL_H
            label = stem or ""
            draw.rectangle([x0, y0, x0 + CELL_W, y0 + CELL_H], outline="#cccccc", fill="white")
            draw.text((x0 + PADDING, y0 + 6), label, fill="#333333", font=font)
            img = _load_png(base, stem)
            if img:
                cell = _fit_cell(img)
                sheet.paste(cell, (x0, y0))

    out_dir = paths.deck_review
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / out_name
    sheet.save(out_path)
    return out_path


def build_variant_contact_sheets(paths=None) -> list[Path]:
    paths = paths or default_paths()
    vdir = paths.deck_root / "variants"
    if not vdir.exists():
        return []
    outputs: list[Path] = []
    for slide in ("S04", "S06", "S08", "S09", "S10", "S12"):
        pngs = sorted(vdir.glob(f"{slide}_*.png"))
        if not pngs:
            continue
        n = len(pngs)
        ncols = min(3, n)
        nrows = (n + ncols - 1) // ncols
        sheet_w = ncols * CELL_W
        sheet_h = nrows * CELL_H
        sheet = Image.new("RGB", (sheet_w, sheet_h), "#f0f0f0")
        draw = ImageDraw.Draw(sheet)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        except OSError:
            font = ImageFont.load_default()
        for i, p in enumerate(pngs):
            ri, ci = divmod(i, ncols)
            x0, y0 = ci * CELL_W, ri * CELL_H
            draw.rectangle([x0, y0, x0 + CELL_W, y0 + CELL_H], outline="#cccccc", fill="white")
            draw.text((x0 + PADDING, y0 + 6), p.stem, fill="#333333", font=font)
            img = Image.open(p).convert("RGB")
            cell = _fit_cell(img)
            sheet.paste(cell, (x0, y0))
        out_path = vdir / f"{slide}_contact_sheet.png"
        sheet.save(out_path)
        outputs.append(out_path)
    return outputs


def main() -> None:
    p = build_contact_sheet()
    print(f"Wrote {p}")
    for vp in build_variant_contact_sheets():
        print(f"Wrote {vp}")


if __name__ == "__main__":
    main()
