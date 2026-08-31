"""Shared matplotlib theme for presentation figures."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt

# Colorblind-safe (Tol-inspired) categorical palette
C_POS = "#0072B2"
C_NEG = "#D55E00"
C_NEUTRAL = "#333333"
C_GATE = "#666666"
C_THIN = "#E69F00"
C_UNMEAS = "#999999"
C_FILL_VIABLE = "#0072B2"
C_OPEN_EDGE = "#0072B2"
C_EXPL = "#009E73"
C_BG = "white"

EFFECT_GATE = 0.11

HYPOTHESIS_ORDER: Sequence[str] = ("H1", "H2", "H3", "H4", "H5", "H6")


def apply_theme() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": C_BG,
            "axes.facecolor": C_BG,
            "axes.edgecolor": "#444444",
            "axes.labelcolor": C_NEUTRAL,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "font.size": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "savefig.facecolor": C_BG,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save_figure(fig: plt.Figure, out_dir: Path, stem: str) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for ext in ("png", "pdf"):
        p = out_dir / f"{stem}.{ext}"
        fig.savefig(p, bbox_inches="tight", pad_inches=0.25)
        paths.append(p)
    plt.close(fig)
    return paths


def gate_lines(ax, *, orientation: str = "vertical") -> None:
    for g in (-EFFECT_GATE, EFFECT_GATE):
        if orientation == "vertical":
            ax.axvline(g, color=C_GATE, ls="--", lw=1.0, zorder=0)
        else:
            ax.axhline(g, color=C_GATE, ls="--", lw=1.0, zorder=0)
    if orientation == "vertical":
        ax.axvline(0, color="#888888", lw=0.8, zorder=0)
    else:
        ax.axhline(0, color="#888888", lw=0.8, zorder=0)


def marker_for_gate(gate: str) -> dict:
    g = (gate or "").lower()
    if g == "thin":
        return {"marker": "o", "facecolors": "none", "edgecolors": C_OPEN_EDGE, "linewidths": 1.8, "s": 90}
    if g == "unmeasurable":
        return {"marker": "x", "color": C_UNMEAS, "s": 80}
    return {"marker": "o", "facecolors": C_FILL_VIABLE, "edgecolors": C_FILL_VIABLE, "s": 90}


def status_symbol(status: str) -> str:
    s = (status or "").lower()
    if s == "viable":
        return "●"
    if s == "thin":
        return "○"
    if s == "unmeasurable":
        return "—"
    return "?"
