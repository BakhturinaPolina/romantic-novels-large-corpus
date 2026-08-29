"""Build theory axes from the frozen YAML schema, and audit what they actually rest on.

The previous aggregation script carried its own Python dict of taxonomy IDs, which drifted
from `configs/stage09/theory_aligned_index_schema.yaml` and silently produced four axes that
were exactly 0.0 for all 16,000 books. This module reads the schema instead, so the axis
definitions have one home, and refuses to emit an axis whose components have no topics.

Two things make the audit as important as the construction:

- An axis is only as strong as the leaves under it. `AX_hea_index` weights three leaves, but
  `5.3a` and `8.3a` each hold exactly one topic, so the axis is really `4.5` with decoration.
  `axis_coverage` states that in a table rather than leaving it for a reader to discover.
- Absence is a finding here. `6.1a`, `6.6`, `6.7` are empty because this corpus has no luxury
  vocabulary, which is substantive information about multi-genre popular romance, not a bug
  to paper over.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np
import pandas as pd
import yaml

LOGGER = logging.getLogger("stage10.axes")

# Axes the schema itself marks as not book-level, or as deprecated aliases.
SEGMENT_LEVEL_METHODS = {"tertile_delta"}


class AxisConstructionError(RuntimeError):
    """Raised when an axis cannot be built from the topics that exist."""


@dataclass
class ComponentCoverage:
    axis: str
    leaf_id: str
    role: str            # minuend | subtrahend | anchor | composite | factor
    weight: float
    n_topics: int
    total_mass: float
    verdict: str         # viable | weak | empty

    def as_row(self) -> Dict[str, object]:
        return {
            "axis": self.axis, "leaf_id": self.leaf_id, "role": self.role,
            "weight": self.weight, "n_topics": self.n_topics,
            "total_mass": self.total_mass, "verdict": self.verdict,
        }


@dataclass
class AxisSpec:
    """A resolved, buildable axis: leaves with signed weights, plus provenance."""
    name: str
    method: str
    hypothesis: List[str]
    hypothesis_role: str
    axis_type: str
    description: str
    leaf_weights: Dict[str, float] = field(default_factory=dict)   # signed
    product_factors: List[str] = field(default_factory=list)
    ratio_numerator: Optional[str] = None
    ratio_denominators: List[str] = field(default_factory=list)
    coverage: List[ComponentCoverage] = field(default_factory=list)

    @property
    def verdict(self) -> str:
        """An axis is as weak as its weakest signed leg."""
        if not self.coverage:
            return "derived"
        verdicts = {c.verdict for c in self.coverage}
        if verdicts == {"empty"}:
            return "empty"
        if "empty" in verdicts or "weak" in verdicts:
            return "weak"
        return "viable"


# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------

def load_axis_schema(path: str | Path) -> Dict[str, dict]:
    with open(path, "r", encoding="utf-8") as fh:
        schema = yaml.safe_load(fh)
    return schema


def load_composites(taxonomy_path: str | Path) -> Dict[str, dict]:
    with open(taxonomy_path, "r", encoding="utf-8") as fh:
        taxonomy = yaml.safe_load(fh)
    return taxonomy.get("composite_indices", {})


def taxonomy_id_sets(taxonomy_path: str | Path) -> Dict[str, Set[str]]:
    with open(taxonomy_path, "r", encoding="utf-8") as fh:
        taxonomy = yaml.safe_load(fh)
    return {
        "axis_bearing": set(taxonomy.get("axis_bearing_ids", [])),
        "excluded": set(taxonomy.get("exclude_from_axes_ids", [])),
        "exploratory_only": set(taxonomy.get("exploratory_only_ids", [])),
        "secondary_context": set(taxonomy.get("secondary_context_ids", [])),
    }


def _composite_leaf_weights(composite: dict) -> Dict[str, float]:
    """Composite blocks use several key spellings; normalise them to leaf -> weight."""
    ids: List[str] = []
    for key in ("taxonomy_ids", "core_taxonomy_ids"):
        ids += [str(i) for i in composite.get(key, []) or []]
    ids += [str(i) for i in composite.get("optional_low_weight_context", []) or []]

    weights = composite.get("weights", {}) or {}
    default = float(weights.get("default", 1.0))
    return {leaf: float(weights.get(leaf, default)) for leaf in dict.fromkeys(ids)}


def _anchor_leaf_weights(block: dict) -> Dict[str, float]:
    """Leaves and weights for a `weighted_sum` axis.

    The frozen schema lists leaves under `anchors.taxonomy` and weights separately. The
    additional axes declared in the Stage10 config (the H3 reframe) carry their leaves in the
    weights map alone, so both spellings are accepted.
    """
    anchors = [str(a) for a in ((block.get("anchors") or {}).get("taxonomy", []) or [])]
    weights = block.get("construction", {}).get("weights", "equal")

    if weights == "equal" or not isinstance(weights, dict):
        return {a: 1.0 for a in anchors}

    default = float(weights.get("default", 1.0))
    if not anchors:
        anchors = [k for k in weights if k != "default"]
    return {a: float(weights.get(a, default)) for a in anchors}


def _side_leaf_weights(
    side: dict,
    resolved: Dict[str, AxisSpec],
    axis_name: str,
) -> Dict[str, float]:
    """A difference side is either an explicit leaf list or a reference to another axis."""
    if "taxonomy" in side:
        return {str(leaf): 1.0 for leaf in side["taxonomy"]}
    if "ref" in side:
        ref = side["ref"]
        if ref not in resolved:
            raise AxisConstructionError(
                f"{axis_name} references {ref}, which is not defined earlier in the schema"
            )
        return dict(resolved[ref].leaf_weights)
    raise AxisConstructionError(f"{axis_name}: difference side has neither 'taxonomy' nor 'ref'")


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------

def resolve_axes(
    schema: Dict[str, dict],
    composites: Dict[str, dict],
    *,
    additional: Optional[Dict[str, dict]] = None,
    skip: Sequence[str] = (),
) -> Dict[str, AxisSpec]:
    """Turn the schema into signed leaf weights per axis, resolving refs in order.

    Difference axes become a single signed weight vector (`AX_love_over_sex` is payoff leaves
    at +1 and `2.3` at -1) so that one dot product builds the axis and one table explains it.
    Products and ratios stay symbolic because they need the other axes computed first.
    """
    blocks = dict(schema)
    for key in ("global", *skip):
        blocks.pop(key, None)
    if additional:
        blocks.update(additional)

    resolved: Dict[str, AxisSpec] = {}
    deferred: List[Tuple[str, dict]] = []

    for name, block in blocks.items():
        if not isinstance(block, dict) or not name.startswith("AX_"):
            continue
        if block.get("deprecated"):
            LOGGER.info("Skipping %s (deprecated alias of %s)", name, block.get("alias_of"))
            continue

        construction = block.get("construction", {}) or {}
        method = construction.get("method", "weighted_sum")

        if method in SEGMENT_LEVEL_METHODS or (block.get("usage", {}) or {}).get("book_level") is False:
            LOGGER.info("Skipping %s at book level (%s is segment-level; see arc.py)", name, method)
            continue

        spec = AxisSpec(
            name=name,
            method=method,
            hypothesis=[str(h) for h in (block.get("hypothesis") or [])],
            hypothesis_role=str(block.get("hypothesis_role", "exploratory")),
            axis_type=str(block.get("type", "evaluative")),
            description=" ".join(str(block.get("description", "")).split()),
        )

        if method == "weighted_sum":
            spec.leaf_weights = _anchor_leaf_weights(block)
        elif method == "weighted_sum_from_composite":
            ref = block.get("composite_ref")
            if ref not in composites:
                raise AxisConstructionError(f"{name}: composite_ref {ref!r} not in taxonomy config")
            spec.leaf_weights = _composite_leaf_weights(composites[ref])
        elif method == "difference":
            try:
                plus = _side_leaf_weights(construction["minuend"], resolved, name)
                minus = _side_leaf_weights(construction["subtrahend"], resolved, name)
            except AxisConstructionError:
                deferred.append((name, block))
                continue
            signed = dict(plus)
            for leaf, w in minus.items():
                signed[leaf] = signed.get(leaf, 0.0) - w
            spec.leaf_weights = signed
        elif method == "product":
            spec.product_factors = [str(f) for f in construction.get("factors", [])]
        elif method == "ratio":
            spec.ratio_numerator = construction.get("numerator_ref")
            spec.ratio_denominators = [str(r) for r in construction.get("denominator_refs", [])]
        else:
            raise AxisConstructionError(f"{name}: unknown construction method {method!r}")

        resolved[name] = spec

    # Second pass for difference axes whose reference appeared later in the file.
    for name, block in deferred:
        construction = block["construction"]
        plus = _side_leaf_weights(construction["minuend"], resolved, name)
        minus = _side_leaf_weights(construction["subtrahend"], resolved, name)
        signed = dict(plus)
        for leaf, w in minus.items():
            signed[leaf] = signed.get(leaf, 0.0) - w
        resolved[name] = AxisSpec(
            name=name,
            method="difference",
            hypothesis=[str(h) for h in (block.get("hypothesis") or [])],
            hypothesis_role=str(block.get("hypothesis_role", "exploratory")),
            axis_type=str(block.get("type", "evaluative")),
            description=" ".join(str(block.get("description", "")).split()),
            leaf_weights=signed,
        )

    # `derived:` blocks (currently only explicitness_ratio) hang off a parent axis.
    for name, block in blocks.items():
        if not isinstance(block, dict):
            continue
        for derived_name, derived in (block.get("derived") or {}).items():
            axis_name = f"AX_{derived_name}" if not derived_name.startswith("AX_") else derived_name
            resolved[axis_name] = AxisSpec(
                name=axis_name,
                method=str(derived.get("method", "ratio")),
                hypothesis=[str(h) for h in (block.get("hypothesis") or [])],
                hypothesis_role="exploratory",
                axis_type=str(block.get("type", "evaluative")),
                description=f"Derived from {name}: {derived.get('method')}",
                ratio_numerator=derived.get("numerator_ref"),
                ratio_denominators=[str(r) for r in derived.get("denominator_refs", [])],
            )

    LOGGER.info("Resolved %d book-level axes from the schema", len(resolved))
    return resolved


# ---------------------------------------------------------------------------
# Coverage audit
# ---------------------------------------------------------------------------

def audit_coverage(
    specs: Dict[str, AxisSpec],
    leaf_topic_counts: Dict[str, int],
    leaf_mass: Dict[str, float],
    *,
    viable_min_topics: int = 3,
    weak_min_topics: int = 1,
) -> pd.DataFrame:
    """Per axis component: how many topics and how much corpus mass it actually has."""
    rows: List[Dict[str, object]] = []
    for spec in specs.values():
        if spec.product_factors:
            for factor in spec.product_factors:
                rows.append(ComponentCoverage(
                    axis=spec.name, leaf_id=factor, role="factor", weight=1.0,
                    n_topics=-1, total_mass=float("nan"), verdict="derived",
                ).as_row())
            continue
        if spec.ratio_numerator:
            for ref in [spec.ratio_numerator, *spec.ratio_denominators]:
                rows.append(ComponentCoverage(
                    axis=spec.name, leaf_id=ref, role="ratio_ref", weight=1.0,
                    n_topics=-1, total_mass=float("nan"), verdict="derived",
                ).as_row())
            continue

        for leaf, weight in sorted(spec.leaf_weights.items()):
            n = int(leaf_topic_counts.get(leaf, 0))
            mass = float(leaf_mass.get(leaf, 0.0))
            if n >= viable_min_topics:
                verdict = "viable"
            elif n >= weak_min_topics:
                verdict = "weak"
            else:
                verdict = "empty"
            cov = ComponentCoverage(
                axis=spec.name, leaf_id=leaf,
                role="minuend" if weight > 0 else "subtrahend",
                weight=float(weight), n_topics=n, total_mass=mass, verdict=verdict,
            )
            spec.coverage.append(cov)
            rows.append(cov.as_row())

    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame

    axis_verdict = {name: spec.verdict for name, spec in specs.items()}
    frame["axis_verdict"] = frame["axis"].map(axis_verdict)
    frame["hypothesis"] = frame["axis"].map(
        {n: ",".join(s.hypothesis) or "-" for n, s in specs.items()}
    )
    frame["hypothesis_role"] = frame["axis"].map({n: s.hypothesis_role for n, s in specs.items()})
    return frame.sort_values(["axis", "role", "leaf_id"]).reset_index(drop=True)


def summarise_coverage(coverage: pd.DataFrame) -> pd.DataFrame:
    """One row per axis: how many legs are viable, weak, or missing entirely."""
    real = coverage[coverage["verdict"] != "derived"]
    if real.empty:
        return pd.DataFrame()
    grouped = real.groupby("axis").agg(
        hypothesis=("hypothesis", "first"),
        hypothesis_role=("hypothesis_role", "first"),
        axis_verdict=("axis_verdict", "first"),
        n_components=("leaf_id", "size"),
        n_viable=("verdict", lambda s: int((s == "viable").sum())),
        n_weak=("verdict", lambda s: int((s == "weak").sum())),
        n_empty=("verdict", lambda s: int((s == "empty").sum())),
        total_topics=("n_topics", "sum"),
        total_mass=("total_mass", "sum"),
    ).reset_index()
    grouped["empty_leaves"] = grouped["axis"].map(
        real[real["verdict"] == "empty"].groupby("axis")["leaf_id"].apply(", ".join)
    ).fillna("")
    return grouped.sort_values(["hypothesis_role", "axis_verdict", "axis"]).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def build_axis_values(
    leaf_shares: pd.DataFrame,
    specs: Dict[str, AxisSpec],
    *,
    fail_on_empty_component: bool = True,
    allow_empty_axes: Sequence[str] = (),
    epsilon: float = 1e-6,
) -> pd.DataFrame:
    """Compute every axis for every book from a wide leaf-share frame.

    Refusing to emit an all-zero axis is the point of `fail_on_empty_component`. The previous
    run shipped `status_power`, `appearance_presentation`, `external_crisis` and
    `internal_ambivalence` as constant zero columns, which look like real variables in a
    regression table and quietly contribute nothing.
    """
    values: Dict[str, pd.Series] = {}
    skipped: Dict[str, str] = {}
    index = leaf_shares.index

    def leaf_series(leaf: str) -> Optional[pd.Series]:
        col = f"leaf_{leaf}"
        return leaf_shares[col] if col in leaf_shares.columns else None

    # Pass 1: everything expressible as a signed sum of leaves.
    for name, spec in specs.items():
        if spec.product_factors or spec.ratio_numerator:
            continue

        present = {leaf: w for leaf, w in spec.leaf_weights.items() if leaf_series(leaf) is not None}
        missing = sorted(set(spec.leaf_weights) - set(present))

        if not present:
            reason = f"no topics for any component ({', '.join(sorted(spec.leaf_weights)) or 'none'})"
            if fail_on_empty_component and name not in allow_empty_axes:
                raise AxisConstructionError(
                    f"{name} has no measurable component: {reason}. "
                    "Either add it to robustness.allow_empty_axes in the config, or drop the axis, "
                    "but do not emit a column of zeros."
                )
            skipped[name] = reason
            LOGGER.warning("SKIP %s — %s", name, reason)
            continue

        if missing:
            LOGGER.warning(
                "%s built from %d of %d components; missing %s",
                name, len(present), len(spec.leaf_weights), ", ".join(missing),
            )

        total = pd.Series(0.0, index=index)
        for leaf, weight in present.items():
            total = total + weight * leaf_series(leaf).astype(float)
        values[name] = total

    # Pass 2: products and ratios over the axes just built.
    for name, spec in specs.items():
        if spec.product_factors:
            factors = [values[f] for f in spec.product_factors if f in values]
            if len(factors) != len(spec.product_factors):
                absent = [f for f in spec.product_factors if f not in values]
                skipped[name] = f"factor(s) unavailable: {', '.join(absent)}"
                LOGGER.warning("SKIP %s — %s", name, skipped[name])
                continue
            # Centre before multiplying so the product is an interaction, not a proxy for
            # whichever factor has the larger scale.
            product = pd.Series(1.0, index=index)
            for f in factors:
                product = product * (f - f.mean())
            values[name] = product
        elif spec.ratio_numerator:
            num = values.get(spec.ratio_numerator)
            dens = [values.get(d) for d in spec.ratio_denominators]
            if num is None or any(d is None for d in dens):
                skipped[name] = "numerator or denominator axis unavailable"
                LOGGER.warning("SKIP %s — %s", name, skipped[name])
                continue
            denom = pd.Series(0.0, index=index)
            for d in dens:
                denom = denom + d
            values[name] = num / (denom.abs() + epsilon)

    frame = pd.DataFrame(values, index=index)
    frame.attrs["skipped_axes"] = skipped
    LOGGER.info("Built %d axes; skipped %d", frame.shape[1], len(skipped))

    constant = [c for c in frame.columns if frame[c].std(ddof=0) < 1e-12]
    if constant:
        raise AxisConstructionError(
            f"These axes came out constant across all books: {constant}. "
            "That is the failure mode this check exists to catch."
        )
    return frame


def leaf_weight_table(specs: Dict[str, AxisSpec]) -> pd.DataFrame:
    """The full axis definition as a table, so the notebook can print what it is testing."""
    rows = []
    for name, spec in specs.items():
        if spec.product_factors:
            rows.append({"axis": name, "method": spec.method,
                         "definition": " x ".join(spec.product_factors),
                         "hypothesis": ",".join(spec.hypothesis) or "-",
                         "role": spec.hypothesis_role})
        elif spec.ratio_numerator:
            rows.append({"axis": name, "method": spec.method,
                         "definition": f"{spec.ratio_numerator} / ({' + '.join(spec.ratio_denominators)})",
                         "hypothesis": ",".join(spec.hypothesis) or "-",
                         "role": spec.hypothesis_role})
        else:
            parts = [
                f"{'+' if w > 0 else '-'}{abs(w):g}*{leaf}"
                for leaf, w in sorted(spec.leaf_weights.items(), key=lambda kv: -kv[1])
            ]
            rows.append({"axis": name, "method": spec.method, "definition": " ".join(parts),
                         "hypothesis": ",".join(spec.hypothesis) or "-",
                         "role": spec.hypothesis_role})
    return pd.DataFrame(rows).sort_values(["role", "axis"]).reset_index(drop=True)
