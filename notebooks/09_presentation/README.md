# Presentation review (v2 deck)

Build slide-aligned figures and open the review notebook:

```bash
make presentation
```

Or step by step:

```bash
.venv/bin/python scripts/presentation/build_presentation_assets.py --deck v2
.venv/bin/python scripts/presentation/build_presentation_review.py
```

Outputs:

- Figures: `results/presentation/final_v1/figures/slide*.png|svg|pdf`
- Data: `results/presentation/final_v1/data/`
- Manifests: `results/presentation/final_v1/manifests/`
- Review HTML: `results/presentation/final_v1/review/presentation_review.html`

Legacy v1 figures (`fig01_*`) remain under `results/stage11_refined_construct_analysis/<run_id>/presentation_figures/`.

Edit slide selection without code changes: `results/presentation/final_v1/annotations/slide_feature_selection.csv`
