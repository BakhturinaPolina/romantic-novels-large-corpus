# %% [markdown]
# # Presentation review (v2 deck)
#
# Single control room for the 17–19 minute storyboard deck.
# Regenerate assets: `make presentation`

# %%
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from IPython.display import Image, display

ROOT = Path.cwd()
for p in [ROOT, *ROOT.parents]:
    if (p / "pyproject.toml").exists() or (p / "requirements.txt").exists():
        if (p / "src").is_dir():
            ROOT = p
            break

DECK = ROOT / "results" / "presentation" / "final_v1"
FIG = DECK / "figures"
DATA = DECK / "data"
MANIFEST = DECK / "manifests"
TABLES = DECK / "tables"

RUN_ID = "v4_l12_granular_final_call49"


def _git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def show_slide(slide_id: str, title: str, evidence: str, takeaway: str, figure_stem: str | None = None, data_csv: str | None = None):
    print(f"### {slide_id} — {title}")
    print(f"**Evidence:** {evidence}")
    print(f"**Takeaway:** {takeaway}")
    if figure_stem:
        png = FIG / f"{figure_stem}.png"
        if png.exists():
            display(Image(str(png)))
        else:
            print(f"_Missing figure: {png}_")
    if data_csv:
        p = DATA / data_csv if (DATA / data_csv).exists() else TABLES / data_csv
        if p.exists():
            display(pd.read_csv(p))
        else:
            print(f"_Missing data: {p}_")
    print("**Statistics changed:** NO (presentation layer selects/visualizes upstream tables only)")
    print("---")

# %% [markdown]
# ## Section 0 — Build status

# %%
main_figs = sorted(FIG.glob("slide*.png")) if FIG.exists() else []
manifest_ok = (MANIFEST / "slide_manifest.csv").exists()
print(f"Presentation build: {'PASS' if main_figs and manifest_ok else 'INCOMPLETE'}")
print(f"Figures built: {len(main_figs)}")
print(f"Run ID: {RUN_ID}")
print(f"Git: {_git_hash()}")
print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")

if manifest_ok:
    display(pd.read_csv(MANIFEST / "slide_manifest.csv"))

# %% [markdown]
# ## Section 1 — Main slides

# %%
show_slide(
    "S04", "The final topic model was chosen as a trade-off, not by one metric",
    "METHOD", "Pareto-efficient selection among hundreds of BO trials",
    "slide04_pareto_selection", "slide04_pareto_points.csv",
)
show_slide(
    "S06", "Context changed what the topics actually meant",
    "METHOD", "Agreement 30–55%; H2/H3 unmeasurable after refinement",
    "slide06_context_measurement", "slide06_agreement.csv",
)
show_slide(
    "S07", "None of the six broad hypotheses produced a clean confirmatory win",
    "CONFIRMATORY", "Broad binaries fail prespecified gate",
    "slide07_primary_verdict_cards", "slide07_primary_verdicts.csv",
)
show_slide(
    "S08", "Specific narrative functions reveal clearer differences",
    "CONFIRMATORY (components)", "Reassurance, tenderness, appearance dominate",
    "slide08_component_effects", "slide08_component_effects.csv",
)
show_slide(
    "S09", "Higher-rated romances devote relatively more space to tenderness",
    "EXPLORATORY", "Compositional attention shift",
    "slide09_attention_shift", "slide09_attention_shift.csv",
)
show_slide(
    "S10", "What makes a book widely read is not what makes it highly rated",
    "EXPLORATORY", "Quality and reach separate strongly",
    "slide10_quality_reach_dumbbell", "slide10_quality_reach.csv",
)
show_slide(
    "S11", "Better-rated books are not simply about more things",
    "EXPLORATORY", "Rarefaction removes raw richness; suppression after drivers",
    "slide11_richness_evidence", "slide11_richness_story.csv",
)
show_slide(
    "S12", "The exploratory extension shifts the question from topics to narrative experience",
    "EXPLORATORY (EES)", "Frozen coding; does not change H1–H6",
    "slide12_ees_integrated", "slide12_ees_integrated.csv",
)

# %% [markdown]
# ## Data-only slides (manual PowerPoint layout)

# %%
show_slide("S02", "16,000 novels let us study reader appreciation at scale", "METHOD", "Corpus scale", None, "corpus_stats.csv")
show_slide("S05", "A topic label is not yet a narrative interpretation", "METHOD", "Interpretation ladder", None, "slide05_topic_card.csv")
show_slide("S13", "What do these statistical patterns look like in actual novels?", "EXPLORATORY", "Deterministic passages", None, "slide13_representative_examples.csv")

# %% [markdown]
# ## Part II — Appendix (v1 suite figures)

# %%
V1 = ROOT / "results" / "stage11_refined_construct_analysis" / RUN_ID / "presentation_figures"
appendix_stems = [
    ("A3", "fig03_primary_hypothesis_verdicts", "Full H1–H6 forest"),
    ("A4", "fig04_stage10_stage11_transition", "Stage10→Stage11 transition"),
    ("A5", "fig05b_component_evidence_matrix", "Component evidence matrix"),
    ("A7", "appendix_quality_reach", "Full quality/reach quadrant"),
    ("A8", "appendix_richness", "Full richness diagnostics"),
    ("A9", "appendix_ees_three_panel", "Full EES three-panel"),
]
for aid, stem, desc in appendix_stems:
    png = V1 / f"{stem}.png"
    print(f"### {aid} — {desc}")
    if png.exists():
        display(Image(str(png)))
    else:
        print(f"_Run v1 build for {stem}_")
    print("---")

# %% [markdown]
# ## Manifests & warnings

# %%
if (MANIFEST / "figure_manifest.csv").exists():
    display(pd.read_csv(MANIFEST / "figure_manifest.csv"))
if (DECK / "annotations" / "plot_annotations.csv").exists():
    display(pd.read_csv(DECK / "annotations" / "plot_annotations.csv"))
