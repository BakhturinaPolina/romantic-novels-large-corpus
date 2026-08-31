"""Notebook helpers for Stage 11 (mirrors Stage 10 setup pattern)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from src.stage11_refined_construct_analysis.config import (
    DEFAULT_CONFIG_PATH,
    Stage11Config,
    find_project_root,
    load_stage11_config,
)


@dataclass
class NotebookContext:
    cfg: Stage11Config
    notebook: str
    root: Path
    figures_dir: Path
    tables_dir: Path

    def save_table(self, frame: pd.DataFrame, name: str, *, index: bool = False) -> None:
        csv_path = self.tables_dir / f"{name}.csv"
        frame.to_csv(csv_path, index=index)
        try:
            frame.to_parquet(self.tables_dir / f"{name}.parquet", index=index)
        except Exception:
            pass
        print(f"  saved table: {csv_path.relative_to(self.root)}  ({len(frame):,} rows)")

    def save_figure(self, fig, name: str, *, dpi: int = 120) -> None:
        path = self.figures_dir / f"{name}.png"
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        print(f"  saved figure: {path.relative_to(self.root)}")

    def save_markdown(self, text: str, name: str) -> None:
        path = self.tables_dir / f"{name}.md"
        path.write_text(text, encoding="utf-8")
        print(f"  saved markdown: {path.relative_to(self.root)}")


def setup(
    notebook: str,
    *,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    quiet: bool = False,
) -> NotebookContext:
    root = find_project_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    cfg = load_stage11_config(config_path, root=root)
    base = cfg.output_path("notebook_dir", create=True) / notebook
    figures = base / "figures"
    tables = base / "tables"
    figures.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)

    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["figure.dpi"] = 120
    pd.set_option("display.max_columns", 80)
    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda v: f"{v:,.4f}")

    if not quiet:
        print(f"Project root : {root}")
        print(f"Config       : {cfg.config_path.relative_to(root)}")
        print(f"Run          : {cfg.run_id}")
        print(f"Outputs      : {base.relative_to(root)}")

    return NotebookContext(
        cfg=cfg,
        notebook=notebook,
        root=root,
        figures_dir=figures,
        tables_dir=tables,
    )


def load_master(cfg: Stage11Config) -> pd.DataFrame:
    path = cfg.output_path("constructs_dir") / "master_annotations.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Master annotations missing: {path}")
    return pd.read_parquet(path)


def load_weights(cfg: Stage11Config, mode: str = "strict") -> pd.DataFrame:
    path = cfg.output_path("constructs_dir") / f"W_tk_{mode}.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def load_w_tkr(cfg: Stage11Config) -> pd.DataFrame:
    path = cfg.output_path("constructs_dir") / "W_tkr.parquet"
    return pd.read_parquet(path) if path.exists() else pd.DataFrame()


def load_refined_frame(cfg: Stage11Config, mode: str = "strict") -> pd.DataFrame:
    out = cfg.output_path("book_features_dir")
    path = out / (
        "book_refined_analysis_frame.parquet"
        if mode == "strict"
        else f"book_refined_analysis_frame_{mode}.parquet"
    )
    if not path.exists():
        raise FileNotFoundError(
            f"Refined frame missing at {path}. Run "
            "pipeline/08_build_refined_analysis_frame.py first."
        )
    frame = pd.read_parquet(path)
    return frame


def load_freeze(cfg: Stage11Config) -> Dict[str, Any]:
    path = cfg.output_path("constructs_dir") / "dictionary_freeze.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_construct_coverage(cfg: Stage11Config) -> Dict[str, Any]:
    """Measurement gates written by pipeline 07 (`construct_coverage.json`)."""
    path = cfg.output_path("constructs_dir") / "construct_coverage.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    freeze = load_freeze(cfg)
    return freeze.get("construct_coverage") or {}


def gate_for_feature(coverage: Dict[str, Any], feature: str) -> str:
    """Return unmeasurable | thin | viable | unknown for a RAX/RLR/composite name."""
    if not coverage:
        return "unknown"
    ratios = coverage.get("ratios") or {}
    if feature in ratios:
        return str(ratios[feature].get("gate") or "unknown")
    composites = coverage.get("composites") or {}
    if feature in composites:
        return str(composites[feature].get("gate") or "unknown")
    atoms = coverage.get("atoms") or {}
    if feature in atoms:
        return str(atoms[feature].get("gate") or "unknown")
    # H6 deltas / RARC: use rising+falling composite atoms if present
    if feature in ("RARC", "DELTA_rising", "DELTA_falling"):
        rising = (atoms.get("RAX_arc_rising") or {}).get("n_topics", 0)
        falling = (atoms.get("RAX_arc_falling") or {}).get("n_topics", 0)
        if rising <= 0 or falling <= 0:
            return "unmeasurable"
        if rising <= 2 or falling <= 2:
            return "thin"
        return "viable"
    # Known RAX_* with no coverage entry ⇒ no mapped topics
    if feature.startswith("RAX_") or feature.startswith("RLR_"):
        return "unmeasurable"
    return "unknown"


def load_frozen_inputs(cfg: Stage11Config) -> Dict[str, Any]:
    path = cfg.output_path("frozen_inputs")
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_candidates(cfg: Stage11Config, hyp: str) -> Dict[str, Any]:
    path = cfg.output_path("candidates_dir") / f"{hyp.lower()}_candidates.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_audit_jsonl(cfg: Stage11Config, hyp: str, pass_name: str) -> pd.DataFrame:
    from src.stage11_refined_construct_analysis.audits.runner import PASS_FILES, audit_dir

    path = audit_dir(cfg, hyp) / PASS_FILES[pass_name]
    if not path.exists():
        return pd.DataFrame()
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return pd.DataFrame(rows)


def load_cell_key(cfg: Stage11Config) -> Dict[str, Any]:
    path = cfg.output_path("cell_key")
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def effect_gate(cfg: Stage11Config) -> float:
    # Prefer Stage 10 gate if available via inputs; else 0.11
    return 0.11


def cliffs_delta_table(
    frame: pd.DataFrame,
    columns: Sequence[str],
    *,
    tier_col: str = "rating_class",
    high: str = "high_rate",
    low: str = "low_rate",
    n_boot: int = 500,
    seed: int = 42,
) -> pd.DataFrame:
    """Cliff's δ high vs low for each column, with bootstrap CI (reuse Stage 10 effects)."""
    from src.stage10_correlation_analysis.analysis import effects as eff

    rows = []
    rng = np.random.default_rng(seed)
    usable = frame
    if "analysable" in frame.columns:
        usable = frame[frame["analysable"].fillna(True)]
    for col in columns:
        if col not in usable.columns:
            continue
        a = usable.loc[usable[tier_col] == high, col].dropna().to_numpy(dtype=float)
        b = usable.loc[usable[tier_col] == low, col].dropna().to_numpy(dtype=float)
        if a.size < 10 or b.size < 10:
            continue
        delta = eff.cliffs_delta(a, b)
        # percentile bootstrap
        boots = []
        for _ in range(n_boot):
            aa = rng.choice(a, size=a.size, replace=True)
            bb = rng.choice(b, size=b.size, replace=True)
            try:
                boots.append(eff.cliffs_delta(aa, bb))
            except ValueError:
                continue
        if boots:
            lo, hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
        else:
            lo = hi = float("nan")
        rows.append(
            {
                "feature": col,
                "cliffs_delta": float(delta),
                "ci_low": lo,
                "ci_high": hi,
                "magnitude": eff.magnitude(delta),
                "n_high": int(a.size),
                "n_low": int(b.size),
                "mean_high": float(np.mean(a)),
                "mean_low": float(np.mean(b)),
            }
        )
    return pd.DataFrame(rows)


def verdict(
    delta: float,
    lo: float,
    hi: float,
    expected_sign: Optional[int] = None,
    *,
    gate: float = 0.11,
) -> str:
    """Stage 10-style directional verdict; unsigned labels if expected_sign is None."""
    import math

    if not math.isfinite(delta):
        return "no reliable effect"
    reliable = not (lo <= 0 <= hi)
    material = abs(delta) >= gate
    if expected_sign is None:
        if reliable and material:
            return "clears_gate"
        if reliable:
            return "directional_only"
        # Avoid the literal "null" (pandas read_csv treats it as NaN).
        return "no reliable effect"
    directional = int(np.sign(delta)) == int(np.sign(expected_sign))
    if directional and reliable and material:
        return "supported"
    if directional and reliable:
        return "directionally consistent, effect below threshold"
    if reliable:
        return "contradicted"
    return "no reliable effect"


def gated_verdict(
    delta: float,
    lo: float,
    hi: float,
    *,
    measurement_gate: str = "viable",
    effect_gate: float = 0.11,
    expected_sign: Optional[int] = None,
) -> str:
    """Respect measurement gates before ordinary effect verdicts."""
    if measurement_gate == "unmeasurable":
        return "unmeasurable"
    base = verdict(delta, lo, hi, expected_sign, gate=effect_gate)
    if measurement_gate == "thin":
        return f"thin:{base}"
    return base


def test_axis(
    frame: pd.DataFrame,
    axis_name: str,
    hypothesis: str,
    *,
    label: str = "",
    tier_col: str = "rating_class",
    tiers: Sequence[str] = ("low_rate", "mid_rate", "high_rate"),
    high: str = "high_rate",
    low: str = "low_rate",
    quality: str = "rating_shrunk",
    reach: str = "log_n_ratings",
    controls: Optional[Sequence[str]] = None,
    categorical: Optional[Sequence[str]] = None,
    cluster: str = "author_id",
    weight: Optional[str] = "reliability",
    n_replicates: int = 400,
    seed: int = 42,
    measurement_gate: str = "viable",
    effect_gate: float = 0.11,
    expected_sign: Optional[int] = None,
) -> Dict[str, Any]:
    """Stage 10-style test_axis for refined constructs (no CLR required)."""
    from src.stage10_correlation_analysis.analysis import effects as eff
    from src.stage10_correlation_analysis.analysis import models as mdl
    from src.stage10_correlation_analysis.analysis import tests as tst

    controls = list(controls or ["log_pages", "n_sentences", "publication_year"])
    categorical = list(categorical or ["genre_group"])
    controls = [c for c in controls if c in frame.columns]
    categorical = [c for c in categorical if c in frame.columns]

    if axis_name not in frame.columns:
        return {
            "hypothesis": hypothesis,
            "feature": axis_name,
            "label": label or axis_name,
            "status": "absent",
            "measurement_gate": measurement_gate,
            "verdict": "unmeasurable" if measurement_gate == "unmeasurable" else "absent",
            "note": "column not present",
        }

    if measurement_gate == "unmeasurable":
        return {
            "hypothesis": hypothesis,
            "feature": axis_name,
            "label": label or axis_name,
            "status": "unmeasurable",
            "measurement_gate": measurement_gate,
            "verdict": "unmeasurable",
            "cliffs_delta": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "note": "zero or missing mapped topics",
        }

    tier_effect = eff.two_group_effects(
        frame,
        [axis_name],
        tier_col,
        high,
        low,
        n_replicates=n_replicates,
        seed=seed,
    )
    trend = tst.compare_tier_trend(frame, [axis_name], tier_col, list(tiers))
    omnibus = tst.kruskal_wallis(frame, [axis_name], tier_col, list(tiers))

    predictor = axis_name
    wcol = weight if weight and weight in frame.columns else None
    quality_fit = mdl.fit_ols(
        frame,
        quality,
        [predictor, *controls],
        categorical=categorical,
        cluster=cluster if cluster in frame.columns else None,
        weights=wcol,
        name=f"{axis_name}->quality",
    )
    reach_fit = mdl.fit_ols(
        frame,
        reach,
        [predictor, *controls],
        categorical=categorical,
        cluster=cluster if cluster in frame.columns else None,
        name=f"{axis_name}->reach",
    )

    def coefficient(fit):
        row = fit.coefficients[fit.coefficients["term"] == predictor]
        if row.empty:
            return {}
        row = row.iloc[0]
        return {
            "beta": float(row["coefficient"]),
            "se": float(row["std_error"]),
            "p": float(row["p_value"]),
            "lo": float(row["ci_low"]),
            "hi": float(row["ci_high"]),
        }

    q = coefficient(quality_fit)
    r = coefficient(reach_fit)
    te = tier_effect.iloc[0]
    delta = float(te["cliffs_delta"])
    lo = float(te["ci_low"])
    hi = float(te["ci_high"])
    return {
        "hypothesis": hypothesis,
        "feature": axis_name,
        "label": label or axis_name,
        "status": "tested",
        "measurement_gate": measurement_gate,
        "verdict": gated_verdict(
            delta,
            lo,
            hi,
            measurement_gate=measurement_gate,
            effect_gate=effect_gate,
            expected_sign=expected_sign,
        ),
        "expected_sign": expected_sign,
        "cliffs_delta": delta,
        "ci_low": lo,
        "ci_high": hi,
        "magnitude": te.get("magnitude"),
        "epsilon_squared": float(omnibus.iloc[0]["epsilon_squared"]) if len(omnibus) else float("nan"),
        "kw_p_value": float(omnibus.iloc[0]["p_value"]) if len(omnibus) else float("nan"),
        "spearman_rho": float(trend.iloc[0]["spearman_rho"]) if len(trend) else float("nan"),
        "quality_beta": q.get("beta", float("nan")),
        "quality_se": q.get("se", float("nan")),
        "quality_p": q.get("p", float("nan")),
        "quality_ci_low": q.get("lo", float("nan")),
        "quality_ci_high": q.get("hi", float("nan")),
        "reach_beta": r.get("beta", float("nan")),
        "reach_p": r.get("p", float("nan")),
        "n_clusters": getattr(quality_fit, "n_clusters", float("nan")),
        "note": "",
    }


def cliffs_delta_author_cluster_ci(
    frame: pd.DataFrame,
    feature: str,
    *,
    tier_col: str = "rating_class",
    high: str = "high_rate",
    low: str = "low_rate",
    cluster: str = "author_id",
    n_replicates: int = 400,
    seed: int = 42,
    ci_level: float = 0.95,
) -> Dict[str, Any]:
    """Cliff's δ with author-cluster bootstrap CI (final uncertainty for NB13)."""
    from src.stage10_correlation_analysis.analysis import effects as eff
    from src.stage10_correlation_analysis.analysis.bootstrap import (
        cluster_bootstrap,
        make_delta_statistic,
    )

    if feature not in frame.columns or cluster not in frame.columns:
        return {
            "feature": feature,
            "cliffs_delta": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "status": "absent",
        }
    a = frame.loc[frame[tier_col] == high, feature].dropna().to_numpy(dtype=float)
    b = frame.loc[frame[tier_col] == low, feature].dropna().to_numpy(dtype=float)
    if a.size < 10 or b.size < 10:
        return {
            "feature": feature,
            "cliffs_delta": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "status": "too_few",
        }
    delta = float(eff.cliffs_delta(a, b))
    stat = make_delta_statistic(feature, tier_col, high, low)
    try:
        boot = cluster_bootstrap(
            frame.dropna(subset=[feature, tier_col, cluster]),
            stat,
            cluster,
            n_replicates=n_replicates,
            ci_level=ci_level,
            seed=seed,
        )
        return {
            "feature": feature,
            "cliffs_delta": delta,
            "ci_low": float(boot["ci_low"]),
            "ci_high": float(boot["ci_high"]),
            "ci_excludes_zero": bool(boot["ci_excludes_zero"]),
            "n_replicates_used": int(boot["n_replicates_used"]),
            "n_clusters": int(boot["n_clusters"]),
            "status": "ok",
        }
    except Exception as exc:
        return {
            "feature": feature,
            "cliffs_delta": delta,
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "status": f"bootstrap_failed:{exc}",
        }


def cliffs_delta_author_cluster_ci_many(
    frame: pd.DataFrame,
    features: Sequence[str],
    *,
    tier_col: str = "rating_class",
    high: str = "high_rate",
    low: str = "low_rate",
    cluster: str = "author_id",
    n_replicates: int = 400,
    seed: int = 42,
    ci_level: float = 0.95,
) -> pd.DataFrame:
    """Batch author-cluster CIs for Cliff's δ (shared resamples)."""
    from src.stage10_correlation_analysis.analysis import effects as eff
    from src.stage10_correlation_analysis.analysis.bootstrap import (
        cluster_bootstrap_many,
        make_delta_statistic,
    )

    present = [f for f in features if f in frame.columns]
    if not present or cluster not in frame.columns:
        return pd.DataFrame()
    stats = {
        f: make_delta_statistic(f, tier_col, high, low) for f in present
    }
    work = frame.dropna(subset=[tier_col, cluster]).copy()
    boot = cluster_bootstrap_many(
        work,
        stats,
        cluster,
        n_replicates=n_replicates,
        ci_level=ci_level,
        seed=seed,
    )
    rows = []
    for f in present:
        a = work.loc[work[tier_col] == high, f].dropna().to_numpy(dtype=float)
        b = work.loc[work[tier_col] == low, f].dropna().to_numpy(dtype=float)
        if a.size < 10 or b.size < 10:
            rows.append(
                {
                    "feature": f,
                    "cliffs_delta": float("nan"),
                    "ci_low": float("nan"),
                    "ci_high": float("nan"),
                    "status": "too_few",
                }
            )
            continue
        delta = float(eff.cliffs_delta(a, b))
        br = boot[boot["statistic"] == f]
        if br.empty:
            rows.append(
                {
                    "feature": f,
                    "cliffs_delta": delta,
                    "ci_low": float("nan"),
                    "ci_high": float("nan"),
                    "status": "missing_boot",
                }
            )
            continue
        r0 = br.iloc[0]
        rows.append(
            {
                "feature": f,
                "cliffs_delta": delta,
                "ci_low": float(r0["ci_low"]) if pd.notna(r0["ci_low"]) else float("nan"),
                "ci_high": float(r0["ci_high"]) if pd.notna(r0["ci_high"]) else float("nan"),
                "ci_excludes_zero": bool(r0.get("ci_excludes_zero")),
                "n_replicates_used": int(r0.get("n_replicates_used") or 0),
                "n_clusters": int(r0.get("n_clusters") or 0),
                "status": "ok",
            }
        )
    return pd.DataFrame(rows)


def cell_code_stability(
    cfg: Stage11Config,
    *,
    hypotheses: Sequence[str] = ("H1", "H2", "H3", "H4", "H5", "H6"),
) -> pd.DataFrame:
    """Per-topic cell code proportions from Pass B sentence_codes × packet cells."""
    from collections import Counter

    from src.stage11_refined_construct_analysis.audits.runner import load_evidence_packet
    from src.stage11_refined_construct_analysis.evidence.blinding import unblind_cell

    cell_key = load_cell_key(cfg)
    meanings = (cell_key.get("meanings") if isinstance(cell_key, dict) else None) or {}
    # Also accept flat {CELL_A: meaning} shape
    if meanings and isinstance(next(iter(meanings.values()), None), dict):
        meanings = cell_key.get("meanings") or {}
    if not meanings:
        meanings = cfg.section("evidence", "cell_meanings") or {}

    rows: List[Dict[str, Any]] = []
    for hyp in hypotheses:
        b = load_audit_jsonl(cfg, hyp, "B")
        if b.empty:
            continue
        for _, r in b.iterrows():
            tid = int(r["topic_id"])
            resp = r.get("response") or {}
            if not isinstance(resp, dict):
                resp = {}
            sc = resp.get("sentence_codes") or []
            if not isinstance(sc, list) or not sc:
                continue
            packet = load_evidence_packet(cfg, tid) or {}
            sid_to_cell = {
                str(s.get("sid")): str(s.get("cell"))
                for s in (packet.get("contextual") or {}).get("sentences") or []
                if s.get("sid") and s.get("cell")
            }
            by_cell: Dict[str, Counter] = {}
            for item in sc:
                if not isinstance(item, dict):
                    continue
                sid = str(item.get("sid") or "")
                code = str(item.get("code") or "")
                cell = sid_to_cell.get(sid)
                if not cell or not code:
                    continue
                by_cell.setdefault(cell, Counter())[code] += 1

            # Dominant per cell + high-prev high vs low comparison
            cell_dom: Dict[str, str] = {}
            cell_props: Dict[str, Dict[str, float]] = {}
            for cell, ctr in by_cell.items():
                total = sum(ctr.values()) or 1
                props = {k: v / total for k, v in ctr.items()}
                cell_props[cell] = props
                cell_dom[cell] = max(props, key=props.get)

            # Map CELL_* → meaning
            meaning_dom: Dict[str, str] = {}
            for cell, dom in cell_dom.items():
                try:
                    meaning = unblind_cell(cell, meanings)
                except Exception:
                    meaning = meanings.get(cell, cell)
                meaning_dom[str(meaning)] = dom

            hi_hi = meaning_dom.get("high_prevalence_high_tier")
            hi_lo = meaning_dom.get("high_prevalence_low_tier")
            differs = (
                bool(hi_hi and hi_lo and hi_hi != hi_lo)
                if (hi_hi and hi_lo)
                else None
            )
            rows.append(
                {
                    "hypothesis": hyp,
                    "topic_id": tid,
                    "n_coded_sentences": sum(sum(c.values()) for c in by_cell.values()),
                    "n_cells_with_codes": len(by_cell),
                    "dominant_by_cell": json.dumps(cell_dom),
                    "dominant_by_meaning": json.dumps(meaning_dom),
                    "high_prev_high_tier_code": hi_hi,
                    "high_prev_low_tier_code": hi_lo,
                    "meaning_differs_high_prevalence": differs,
                    "pass_b_dominant": resp.get("dominant_code") or r.get("code"),
                }
            )
    return pd.DataFrame(rows)
