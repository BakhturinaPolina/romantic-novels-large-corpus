"""Statistics and plumbing for the Stage10 final analysis.

The notebooks in `notebooks/07_analysis/` import from here so that the analytical choices —
which effect size, which multiplicity correction, which clustering level — are written down
once and reviewed once, rather than retyped in nine notebooks.

Modules, in the order a reader would meet them:

  config            load `configs/stage10/final_analysis.yaml`, resolve paths
  compositional     CLR and log-ratio transforms; topic shares are a composition
  axes              build the theory axes from the frozen YAML schema, and audit coverage
  effects           Cliff's delta and friends, with bootstrap confidence intervals
  tests             Kruskal-Wallis, Mann-Whitney, Holm within family, BH across family
  models            OLS/WLS/logistic with author-cluster-robust SEs; predictive check
  reliability       does a composite hold together? alpha, omega, PCA, split-half
  bootstrap         cluster bootstrap and leave-one-cluster-out by author or series
  arc               within-book tertile deltas for the narrative-arc hypothesis
  qual              targeted close-reading samples pulled from the sentence parquets
  notebook_helpers  notebook setup, output paths, table and figure saving
"""

from src.stage10_correlation_analysis.analysis.config import (
    AnalysisConfig,
    DEFAULT_CONFIG_PATH,
    find_project_root,
    load_analysis_config,
)

__all__ = [
    "AnalysisConfig",
    "DEFAULT_CONFIG_PATH",
    "find_project_root",
    "load_analysis_config",
]
