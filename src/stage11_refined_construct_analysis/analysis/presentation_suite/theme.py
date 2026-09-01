"""Shared matplotlib theme for presentation figures."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Literal, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

PresentationMode = Literal["chart_only", "review"]

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
C_SELECTED = "#0072B2"
C_BG = "white"

EFFECT_GATE = 0.11

# Presentation typography (projection-readable)
PLOT_TEXT = 14
TICK_TEXT = 13
AXIS_LABEL = 14
VALUE_LABEL = 13
PANEL_TITLE = 15

HYPOTHESIS_ORDER: Sequence[str] = ("H1", "H2", "H3", "H4", "H5", "H6")


def scientific_plot_style() -> None:
    """Font sizes, axes, ticks — presentation-readable defaults."""
    mpl.rcParams.update(
        {
            "figure.facecolor": C_BG,
            "axes.facecolor": C_BG,
            "axes.edgecolor": "#444444",
            "axes.labelcolor": C_NEUTRAL,
            "axes.titlesize": PANEL_TITLE,
            "axes.labelsize": AXIS_LABEL,
            "xtick.labelsize": TICK_TEXT,
            "ytick.labelsize": TICK_TEXT,
            "font.size": PLOT_TEXT,
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


def apply_theme() -> None:
    """Apply presentation scientific plot style (backward-compatible alias)."""
    scientific_plot_style()


def resolve_output_dir(paths, mode: PresentationMode) -> Path:
    """chart_only → deck figures; review → review/figures."""
    if mode == "review":
        out = paths.deck_review / "figures"
        out.mkdir(parents=True, exist_ok=True)
        return out
    paths.deck_figures.mkdir(parents=True, exist_ok=True)
    return paths.deck_figures


def set_title_with_subtitle(
    ax,
    title: str,
    subtitle: str | None = None,
    *,
    title_size: float = PANEL_TITLE,
    subtitle_size: float = VALUE_LABEL,
    subtitle_color: str = "#555555",
    subtitle_weight: str = "normal",
    loc: str = "left",
) -> None:
    """Place title and optional subtitle without colliding."""
    ha = {"left": "left", "center": "center", "right": "right"}.get(loc, "left")
    x = {"left": 0.0, "center": 0.5, "right": 1.0}.get(loc, 0.0)
    if subtitle:
        ax.set_title("")
        ax.text(
            x,
            1.16,
            title,
            transform=ax.transAxes,
            ha=ha,
            va="bottom",
            fontsize=title_size,
            fontweight="bold",
            color=C_NEUTRAL,
            clip_on=False,
        )
        ax.text(
            x,
            1.06,
            subtitle,
            transform=ax.transAxes,
            ha=ha,
            va="bottom",
            fontsize=subtitle_size,
            color=subtitle_color,
            fontweight=subtitle_weight,
            clip_on=False,
        )
    else:
        ax.set_title(title, fontsize=title_size, loc=loc if loc in ("left", "center", "right") else "center")


def apply_presentation_context(
    ax,
    *,
    mode: PresentationMode,
    title: str | None = None,
    subtitle: str | None = None,
    exploratory: bool = False,
) -> None:
    """Add review-only decorators (title, subtitle, exploratory badge)."""
    if mode == "chart_only":
        return
    if title:
        set_title_with_subtitle(ax, title, subtitle)
    if exploratory:
        exploratory_tag(ax)


def format_delta(value: float | None, *, decimals: int = 2) -> str:
    """Two-decimal presentation label for Cliff's δ."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "—"
    sign = "+" if value > 0 else "−" if value < 0 else ""
    return f"{sign}{abs(value):.{decimals}f}"


def format_pp(value: float, *, decimals: int = 2) -> str:
    """Signed percentage-point label for compositional shifts."""
    sign = "+" if value > 0 else "−" if value < 0 else ""
    return f"{sign}{abs(value):.{decimals}f} pp"


def gate_band(ax, *, orientation: str = "vertical", alpha: float = 0.12) -> None:
    """Shaded region for prespecified effect-size gate (below |δ| = 0.11)."""
    lo, hi = -EFFECT_GATE, EFFECT_GATE
    if orientation == "vertical":
        ax.axvspan(lo, hi, color="#cccccc", alpha=alpha, zorder=0)
    else:
        ax.axhspan(lo, hi, color="#cccccc", alpha=alpha, zorder=0)


def exploratory_tag(ax, text: str = "EXPLORATORY", *, x: float = 0.99, y: float = 0.98) -> None:
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        color=C_EXPL,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=C_EXPL, linewidth=0.8),
        clip_on=False,
    )


def verdict_card_style(status: str) -> dict:
    """Return facecolor, edgecolor, text_color for verdict cards."""
    s = (status or "").lower()
    if s == "unmeasurable":
        return {"facecolor": "#eeeeee", "edgecolor": C_UNMEAS, "color": C_UNMEAS}
    if s == "thin":
        return {"facecolor": "#f5f5f5", "edgecolor": C_NEUTRAL, "color": C_NEUTRAL}
    if s in ("contradicted", "not_supported"):
        return {"facecolor": "#fde8e0", "edgecolor": C_NEG, "color": C_NEUTRAL}
    return {"facecolor": "#f5f5f5", "edgecolor": C_NEUTRAL, "color": C_NEUTRAL}


def save_figure(
    fig: plt.Figure,
    out_dir: Path,
    stem: str,
    *,
    close: bool = True,
    fixed_canvas: bool = False,
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    bbox = None if fixed_canvas else "tight"
    pad = 0.0 if fixed_canvas else 0.35
    for ext in ("png", "svg", "pdf"):
        p = out_dir / f"{stem}.{ext}"
        fig.savefig(p, bbox_inches=bbox, pad_inches=pad)
        paths.append(p)
    if close:
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
