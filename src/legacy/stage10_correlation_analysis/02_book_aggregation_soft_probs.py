#!/usr/bin/env python3
"""Book-level aggregation and derived indices.

This script takes the topic-level lookup table produced in script 01 and joins it to
book topic mixture data to produce:
- book-level taxonomy proportions (long + wide)
- optional segment-level taxonomy proportions (if chapter/segment topic probs are available)
- derived taxonomy-proxy indices aligned to hypotheses
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import shared utilities
from utils import (
    assert_overlap,
    first_existing,
    glob_first,
    load_table,
    normalize_id,
    safe_project_root,
)

# Try to import project defaults
try:
    from src.stage06_topic_exploration.explore_retrained_model import (
        DEFAULT_BASE_DIR,
        DEFAULT_EMBEDDING_MODEL,
    )
except ImportError:
    DEFAULT_BASE_DIR = None
    DEFAULT_EMBEDDING_MODEL = None

try:
    from src.stage09_category_mapping.stage1_theory_driven_categories.taxonomy_v2 import (
        build_composite_series,
        composite_index_spec,
    )
except ImportError:
    build_composite_series = None
    composite_index_spec = None


# Leaf taxonomy IDs for book-level component sums (stable across taxonomy renames).
COMPONENT_TAXONOMY_IDS: Dict[str, List[str]] = {
    "commitment_hea": ["4.5"],
    "bonding_growth": ["4.2"],
    "positive_emotions": ["3.1"],
    "nonexplicit_affection": ["2.2"],
    "explicit": ["2.3"],
    "miscommunication": ["4.3"],
    "neg_affect": ["3.2"],
    "breakup_conflict": ["4.4"],
    "protective_care": ["4.6"],
    "possessiveness": ["4.7"],
    "violence_threat": ["7.2"],
    "external_crisis": ["7.3"],
    "elite_work": ["6.1a"],
    "generic_business": ["6.1b"],
    "internal_ambivalence": ["3.3"],
    "material_glamour": ["6.6"],
    "aristocracy_status": ["6.7"],
    "community_ritual": ["5.3a"],
    "community_social": ["5.3b"],
    "economic_precarity": ["6.4"],
    "public_leisure": ["8.2"],
    "commitment_symbols": ["8.3a"],
    "everyday_props": ["8.3b"],
    "appearance_presentation": ["1.6", "1.7"],
    "domestic": ["8.1"],
}


def sum_taxonomy_id_columns(
    wide_id: pd.DataFrame,
    ids: List[str],
    weights: Optional[Dict[str, float]] = None,
) -> pd.Series:
    """Sum weighted taxonomy-id columns from a book-level wide table."""
    if wide_id.empty:
        return pd.Series(dtype=float)
    default_w = (weights or {}).get("default", 1.0)
    total = pd.Series(0.0, index=wide_id.index)
    for cid in ids:
        if cid not in wide_id.columns:
            continue
        w = (weights or {}).get(cid, default_w)
        total = total + wide_id[cid] * w
    return total


def setup_logging(output_dir: Path, log_file: str = "02_book_aggregation.log") -> logging.Logger:
    """Set up logging to both file and console."""
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("book_aggregation")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    fh = logging.FileHandler(output_dir / log_file, mode="w", encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def find_inputs(project_root: Path) -> Dict[str, Optional[Path]]:
    """Best-effort discovery of required inputs.
    
    We prefer pipeline outputs if they exist; otherwise fall back to raw contracts.
    """
    candidates = {}

    # 1) Book topic mixtures (check organized structure first)
    candidates['book_topic_probs'] = first_existing([
        project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "topic_probabilities" / "book_topic_probs.parquet",
        project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "topic_probabilities" / "book_topic_probs.csv",
        project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "book_topic_probs.parquet",
        project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "book_topic_probs.csv",
        project_root / "results" / "stage10_correlation_analysis" / "book_topic_probs.parquet",
        project_root / "results" / "stage10_correlation_analysis" / "book_topic_probs.csv",
        project_root / "book_topic_probs.csv",
        project_root / "data" / "book_topic_probs.csv",
        project_root / "results" / "book_topic_probs.csv",
    ]) or glob_first(project_root / "results", [
        "**/book_topic_probs.csv",
        "**/book_topic_probs.parquet",
        "**/book_topic_proportions*.parquet",
        "**/book_topic_proportions*.csv",
    ])

    # 2) Book metadata
    candidates['books_meta'] = first_existing([
        project_root / "books_meta.csv",
        project_root / "data" / "books_meta.csv",
        project_root / "results" / "books_meta.csv",
        project_root / "data" / "processed" / "goodreads.csv",
    ]) or glob_first(project_root / "results", [
        "**/books_meta.csv",
        "**/books_meta.parquet",
        "**/books_metadata*.csv",
        "**/books_metadata*.parquet",
    ])

    # 3) Optional: chapter/segment topic probs (check organized structure first)
    candidates['chapter_topic_probs'] = first_existing([
        project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "topic_probabilities" / "chapter_topic_probs.parquet",
        project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "topic_probabilities" / "chapter_topic_probs.csv",
        project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "chapter_topic_probs.parquet",
        project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "chapter_topic_probs.csv",
        project_root / "results" / "stage10_correlation_analysis" / "chapter_topic_probs.parquet",
        project_root / "results" / "stage10_correlation_analysis" / "chapter_topic_probs.csv",
        project_root / "chapter_topic_probs.csv",
        project_root / "data" / "chapter_topic_probs.csv",
        project_root / "results" / "chapter_topic_probs.csv",
    ]) or glob_first(project_root / "results", [
        "**/chapter_topic_probs.csv",
        "**/chapter_topic_probs.parquet",
        "**/segment_topic_probs*.csv",
        "**/segment_topic_probs*.parquet",
    ])

    # 4) If Stage09 already computed category proportions, use those directly
    candidates['stage09_book_category_props'] = first_existing([
        project_root / "results" / "stage09_category_mapping" / "stage1_theory_driven_categories" / "book_category_proportions.parquet",
        project_root / "results" / "stage09_category_mapping" / "stage1_theory_driven_categories" / "book_category_proportions.csv",
    ])

    # 5) Sentence dataframe with topics
    candidates['sentence_df_with_topics'] = first_existing([
        project_root / "data" / "processed" / "sentence_df_with_topics.parquet",
        project_root / "data" / "processed" / "sentence_df_with_topics.csv",
        project_root / "data" / "sentence_df_with_topics.parquet",
    ]) or glob_first(project_root / "data", [
        "**/sentence_df_with_topics.parquet",
        "**/sentence_df_with_topics.csv",
    ])

    # 6) Goodreads metadata
    candidates['goodreads_csv'] = first_existing([
        project_root / "data" / "processed" / "goodreads.csv",
        project_root / "data" / "goodreads.csv",
    ])

    return candidates


def aggregate_to_book_level(
    book_topic: pd.DataFrame,
    topic_lookup: pd.DataFrame,
    logger: logging.Logger,
) -> pd.DataFrame:
    """Aggregate topic probabilities to book-level taxonomy proportions.
    
    Args:
        book_topic: DataFrame with columns book_id, topic_id, prob
        topic_lookup: Topic lookup table with taxonomy mappings
        logger: Logger instance
        
    Returns:
        DataFrame with book-level category proportions (long format)
    """
    # Join to taxonomy main categories (+ axis exclusion flags)
    lookup_cols = [
        'topic_id', 'taxonomy_main_id', 'taxonomy_main_name', 'taxonomy_main_group',
        'taxonomy_exclude_from_axes', 'taxonomy_use_in_macro_axes', 'label_exclude_from_axes',
    ]
    present_cols = [c for c in lookup_cols if c in topic_lookup.columns]
    book_topic = book_topic.merge(
        topic_lookup[present_cols],
        on='topic_id', how='left'
    )

    # Honor respect_exclude_from_axes: drop topics flagged for axis exclusion or noise
    exclude_mask = pd.Series(False, index=book_topic.index)
    if 'taxonomy_use_in_macro_axes' in book_topic.columns:
        exclude_mask = exclude_mask | (~book_topic['taxonomy_use_in_macro_axes'].fillna(True))
    elif 'taxonomy_exclude_from_axes' in book_topic.columns:
        exclude_mask = exclude_mask | book_topic['taxonomy_exclude_from_axes'].fillna(False)
    if 'label_exclude_from_axes' in book_topic.columns:
        exclude_mask = exclude_mask | book_topic['label_exclude_from_axes'].fillna(False)
    if 'taxonomy_main_id' in book_topic.columns:
        exclude_mask = exclude_mask | (book_topic['taxonomy_main_id'] == 'noise')
    book_topic = book_topic.loc[~exclude_mask].copy()

    # Track unmapped probability mass per book
    book_topic['is_mapped'] = book_topic['taxonomy_main_id'].notna()
    unmapped_mass = (book_topic
                     .assign(unmapped_prob=lambda d: np.where(d['is_mapped'], 0.0, d['prob']))
                     .groupby('book_id', as_index=False)['unmapped_prob'].sum()
                     .rename(columns={'unmapped_prob': 'unmapped_topic_mass'}))

    # Aggregate to book x taxonomy_main_id (long format)
    book_cat_long = (book_topic[book_topic['is_mapped']]
        .groupby(['book_id', 'taxonomy_main_id', 'taxonomy_main_name', 'taxonomy_main_group'], as_index=False)['prob']
        .sum()
        .rename(columns={'prob': 'category_prop_raw'})
    )

    # Normalize within book across mapped categories
    totals = book_cat_long.groupby('book_id', as_index=False)['category_prop_raw'].sum().rename(columns={'category_prop_raw': 'mapped_mass'})
    book_cat_long = book_cat_long.merge(totals, on='book_id', how='left')
    book_cat_long['category_prop'] = book_cat_long['category_prop_raw'] / book_cat_long['mapped_mass']

    # Attach unmapped mass
    book_cat_long = book_cat_long.merge(unmapped_mass, on='book_id', how='left')
    
    return book_cat_long


def compute_indices(
    book_cat_long: pd.DataFrame,
    books_meta: Optional[pd.DataFrame],
    logger: logging.Logger,
) -> pd.DataFrame:
    """Compute taxonomy-proxy indices aligned to hypotheses.
    
    Args:
        book_cat_long: Long format category proportions
        books_meta: Optional book metadata
        logger: Logger instance
        
    Returns:
        DataFrame with computed indices
    """
    # Build per-book wide table keyed by taxonomy leaf id
    wide_id = (book_cat_long
        .dropna(subset=['taxonomy_main_id'])
        .groupby(['book_id', 'taxonomy_main_id'], as_index=False)['category_prop']
        .sum()
        .pivot_table(
            index='book_id',
            columns='taxonomy_main_id',
            values='category_prop',
            aggfunc='sum',
            fill_value=0.0,
        ))

    # Build component columns from stable taxonomy IDs
    components_df = pd.DataFrame(index=wide_id.index)
    for comp, ids in COMPONENT_TAXONOMY_IDS.items():
        components_df[comp] = sum_taxonomy_id_columns(wide_id, ids)

    # Indices aligned to configs/stage09/theory_aligned_index_schema.yaml (v2.3)
    indices = pd.DataFrame(index=wide_id.index)

    indices['payoff_safety'] = (
        components_df['commitment_hea'] + components_df['positive_emotions']
    )

    # H1: AX_love_over_sex — payoff minus explicit (difference, not log-ratio)
    indices['love_over_sex'] = indices['payoff_safety'] - components_df['explicit']

    # H2: AX_hea_index — commitment + rituals + symbolic objects (weighted)
    if composite_index_spec is not None:
        indices['hea_index'] = sum_taxonomy_id_columns(
            wide_id, ["4.5", "5.3a", "8.3a"], {"default": 1.0, "5.3a": 0.8, "8.3a": 0.5}
        )
    else:
        indices['hea_index'] = (
            components_df['commitment_hea']
            + 0.8 * components_df['community_ritual']
            + 0.5 * components_df['commitment_symbols']
        )

    indices['explicitness'] = components_df['explicit']
    indices['explicitness_ratio'] = (
        components_df['explicit']
        / (indices['payoff_safety'] + components_df['explicit'] + components_df['nonexplicit_affection'] + 1e-9)
    )

    # H5: AX_dark_vs_tender
    indices['dark_vs_tender'] = (
        (
            components_df['neg_affect']
            + components_df['breakup_conflict']
            + components_df['violence_threat']
            + components_df['external_crisis']
        )
        - (components_df['positive_emotions'] + components_df['nonexplicit_affection'] + components_df['protective_care'])
    )

    indices['miscommunication'] = components_df['miscommunication']
    indices['miscommunication_balance'] = indices['payoff_safety'] - components_df['miscommunication']

    # H4: protective vs possessive
    indices['protective_care'] = components_df['protective_care']
    indices['possessiveness'] = components_df['possessiveness']
    indices['protective_vs_possessive'] = (
        components_df['protective_care'] - components_df['possessiveness']
    )

    indices['violence_coercion'] = components_df['violence_threat']
    indices['external_crisis'] = components_df['external_crisis']

    # Legacy proxy (6.1 + 8.2) — kept for backward compatibility
    indices['luxury_saturation_proxy'] = (
        components_df['elite_work'] + components_df['public_leisure']
    )

    if composite_index_spec is not None and build_composite_series is not None:
        lux_spec = composite_index_spec("luxury_composite")
        indices['luxury_composite'] = build_composite_series(wide_id, lux_spec)
    else:
        indices['luxury_composite'] = (
            components_df['material_glamour']
            + components_df['aristocracy_status']
            + components_df['community_ritual']
            + components_df['public_leisure']
            + components_df['commitment_symbols']
            + 0.5 * components_df['elite_work']
        )

    if composite_index_spec is not None and build_composite_series is not None:
        sp_spec = composite_index_spec("status_power")
        indices['status_power'] = build_composite_series(wide_id, sp_spec)
    else:
        indices['status_power'] = (
            components_df['elite_work']
            + components_df['material_glamour']
            + components_df['aristocracy_status']
        )

    if composite_index_spec is not None and build_composite_series is not None:
        ap_spec = composite_index_spec("appearance_presentation")
        indices['appearance_presentation'] = build_composite_series(wide_id, ap_spec)
    else:
        indices['appearance_presentation'] = components_df['appearance_presentation']

    indices['luxury_x_love'] = indices['luxury_composite'] * indices['payoff_safety']

    if composite_index_spec is not None and build_composite_series is not None:
        ei_spec = composite_index_spec("everyday_intimacy_emotional_safety")
        indices['everyday_intimacy_emotional_safety'] = build_composite_series(wide_id, ei_spec)
        sti_spec = composite_index_spec("sexual_tension_explicit_intimacy")
        indices['sexual_tension_explicit_intimacy'] = build_composite_series(wide_id, sti_spec)
        ccr_spec = composite_index_spec("coercion_risk_watchlist")
        indices['coercion_risk_watchlist'] = build_composite_series(wide_id, ccr_spec)
        try:
            eco_spec = composite_index_spec("economic_precarity_dependency")
            indices['economic_precarity_dependency'] = build_composite_series(wide_id, eco_spec)
        except Exception:
            indices['economic_precarity_dependency'] = sum_taxonomy_id_columns(wide_id, ["6.4"])
    else:
        indices['everyday_intimacy_emotional_safety'] = sum_taxonomy_id_columns(
            wide_id,
            ["4.2", "4.6", "2.2", "4.1", "8.1", "8.2"],
            {"4.2": 1.0, "4.6": 1.0, "2.2": 1.0, "4.1": 0.5, "8.1": 0.3, "8.2": 0.3, "default": 1.0},
        )
        indices['sexual_tension_explicit_intimacy'] = sum_taxonomy_id_columns(
            wide_id, ["2.1", "2.3", "2.4", "2.5"]
        )
        indices['coercion_risk_watchlist'] = sum_taxonomy_id_columns(
            wide_id, ["7.4", "7.2"], {"7.4": 1.0, "7.2": 0.8, "default": 1.0}
        )
        indices['economic_precarity_dependency'] = sum_taxonomy_id_columns(wide_id, ["6.4"])

    indices['attraction'] = sum_taxonomy_id_columns(wide_id, ["2.1"])

    indices['internal_ambivalence'] = components_df['internal_ambivalence']

    # Attach unmapped mass
    unmapped = (book_cat_long[['book_id', 'unmapped_topic_mass']].drop_duplicates('book_id')
                .set_index('book_id'))
    indices = indices.join(unmapped, how='left')

    # Join metadata fields if available
    if books_meta is not None:
        meta_cols = [c for c in ['rating_class', 'avg_rating', 'n_ratings', 'author_id', 'length_tokens', 'length_words', 'year'] if c in books_meta.columns]
        meta = books_meta[['book_id'] + meta_cols].drop_duplicates('book_id').set_index('book_id')
        indices = indices.join(meta, how='left')

    indices = indices.reset_index()
    return indices


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Book-level aggregation and derived indices"
    )
    
    parser.add_argument(
        "--topic-lookup",
        type=Path,
        help="Path to topic_lookup.parquet from script 01 (auto-detected if not provided)",
    )
    
    parser.add_argument(
        "--book-topic-probs",
        type=Path,
        help="Path to book_topic_probs.parquet (auto-discovered if not provided)",
    )
    
    parser.add_argument(
        "--chapter-topic-probs",
        type=Path,
        help="Path to chapter_topic_probs.parquet (optional)",
    )
    
    parser.add_argument(
        "--goodreads-path",
        type=Path,
        help="Path to goodreads.csv (auto-detected if not provided)",
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for book features (default: results/stage10_correlation_analysis/data_preparation/book_features)",
    )
    
    parser.add_argument(
        "--excluded-book-ids",
        type=Path,
        help="CSV file with excluded book IDs (default: excluded_book_ids.csv in script directory)",
    )
    
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Project root path (auto-detected if not provided)",
    )
    
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()
    
    # Determine project root
    project_root = args.project_root or safe_project_root()
    
    # Set up output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        # Use organized structure: data_preparation/book_features/
        base_dir = project_root / "results" / "stage10_correlation_analysis" / "data_preparation"
        output_dir = base_dir / "book_features"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set up logging
    logger = setup_logging(output_dir)
    logger.info("="*80)
    logger.info("Book-level Aggregation and Derived Indices")
    logger.info("="*80)
    logger.info(f"Project root: {project_root}")
    logger.info(f"Output directory: {output_dir}")
    
    # Load excluded book IDs
    if args.excluded_book_ids:
        excluded_df = pd.read_csv(args.excluded_book_ids)
        excluded_book_ids = excluded_df["book_id"].astype(str).tolist()
    else:
        # Try default location
        default_excluded = SCRIPT_DIR.parent / "excluded_book_ids.csv"
        if default_excluded.exists():
            excluded_df = pd.read_csv(default_excluded)
            excluded_book_ids = excluded_df["book_id"].astype(str).tolist()
        else:
            excluded_book_ids = ['19561986', '19619918', '25781538', '52061964', '53491034']
    logger.info(f"Excluded book IDs: {excluded_book_ids}")
    
    # Load topic lookup
    logger.info("\n" + "="*80)
    logger.info("Loading topic lookup")
    logger.info("="*80)
    
    if args.topic_lookup:
        topic_lookup_path = Path(args.topic_lookup)
    else:
        # Look in organized structure first, then fallback to old location
        eda_dir = project_root / "results" / "stage10_correlation_analysis" / "data_preparation" / "taxonomy_radway_eda"
        topic_lookup_path = eda_dir / "topic_lookup.parquet"
        if not topic_lookup_path.exists():
            # Fallback to old location (for backward compatibility)
            old_eda_dir = project_root / "results" / "stage10_correlation_analysis" / "taxonomy_radway_eda"
            if old_eda_dir.exists():
                topic_lookup_path = old_eda_dir / "topic_lookup.parquet"
    
    if not topic_lookup_path.exists():
        raise FileNotFoundError(
            f"topic_lookup.parquet not found. Run script 01 first.\n"
            f"Expected: {topic_lookup_path}"
        )
    
    topic_lookup = pd.read_parquet(topic_lookup_path)
    logger.info(f"✓ Loaded topic lookup: {topic_lookup_path} (shape: {topic_lookup.shape})")
    
    # Basic QA: required columns
    required_cols = {'topic_id', 'taxonomy_main_id', 'taxonomy_main_name', 'taxonomy_main_group'}
    missing = required_cols - set(topic_lookup.columns)
    if missing:
        raise ValueError(f"topic_lookup missing required columns: {missing}")
    
    # Discover inputs
    logger.info("\n" + "="*80)
    logger.info("Discovering input files")
    logger.info("="*80)
    inputs = find_inputs(project_root)
    
    for k, v in inputs.items():
        if v:
            logger.info(f"  {k}: {v}")
    
    # Load Goodreads metadata and apply cohort exclusion
    logger.info("\n" + "="*80)
    logger.info("Loading Goodreads metadata")
    logger.info("="*80)
    
    if args.goodreads_path:
        goodreads_path = Path(args.goodreads_path)
    else:
        data_dir = project_root / "data" / "processed"
        results_dir = project_root / "results"
        goodreads_path = first_existing([
            data_dir / "goodreads.csv",
            data_dir / "books_meta.csv",
            results_dir / "books_meta.csv",
        ])
    
    if goodreads_path is None or not goodreads_path.exists():
        raise FileNotFoundError("Could not find goodreads.csv / books_meta.csv")
    
    meta = pd.read_csv(goodreads_path)
    
    # Choose id column
    id_col = None
    for c in ["goodreads_book_id", "ID", "book_id", "goodreads_id", "work_id", "id"]:
        if c in meta.columns:
            id_col = c
            break
    if id_col is None:
        raise ValueError(f"No suitable Goodreads id column found. Columns: {meta.columns.tolist()}")
    
    meta["book_id"] = normalize_id(meta[id_col])
    
    # Apply cohort exclusion
    before = meta["book_id"].nunique()
    meta = meta[~meta["book_id"].isin(excluded_book_ids)].copy()
    after = meta["book_id"].nunique()
    logger.info(f"✓ Cohort meta unique book_id: {before} → {after} (excluded {before-after})")
    
    # Load book category proportions
    logger.info("\n" + "="*80)
    logger.info("Loading book category proportions")
    logger.info("="*80)
    
    book_cat_long = None
    source_used = None
    
    if inputs.get('stage09_book_category_props') is not None:
        p = inputs['stage09_book_category_props']
        book_cat_long = load_table(p)
        source_used = f"stage09_book_category_props: {p}"
        logger.info(f"✓ Using Stage09 book category proportions: {p}")
        
        # Normalize column names
        if 'prop' in book_cat_long.columns:
            book_cat_long = book_cat_long.rename(columns={'prop': 'category_prop'})
        if 'main_category_id' in book_cat_long.columns:
            book_cat_long = book_cat_long.rename(columns={'main_category_id': 'taxonomy_main_id'})
        
        # Join with topic_lookup to get taxonomy_main_name and taxonomy_main_group if missing
        if 'taxonomy_main_name' not in book_cat_long.columns or 'taxonomy_main_group' not in book_cat_long.columns:
            book_cat_long = book_cat_long.merge(
                topic_lookup[['taxonomy_main_id', 'taxonomy_main_name', 'taxonomy_main_group']].drop_duplicates(),
                on='taxonomy_main_id',
                how='left'
            )
        
        # Add unmapped_topic_mass column if missing
        if 'unmapped_topic_mass' not in book_cat_long.columns:
            book_cat_long['unmapped_topic_mass'] = 0.0
    else:
        # Use book_topic_probs and aggregate
        p = args.book_topic_probs or inputs.get('book_topic_probs')
        if p is None or not Path(p).exists():
            raise FileNotFoundError(
                "Could not find book_topic_probs.csv/parquet.\n"
                "Looked under project_root and results/**.\n"
                "If your file name differs, edit the discovery patterns in find_inputs()."
            )
        
        book_topic = load_table(Path(p))
        source_used = f"book_topic_probs: {p}"
        logger.info(f"✓ Using book topic probs: {p}")
        
        # Normalize column names
        col_map = {c.lower(): c for c in book_topic.columns}
        
        def pick(name_options):
            for opt in name_options:
                if opt in col_map:
                    return col_map[opt]
            return None
        
        c_book = pick(['book_id', 'book', 'bookid'])
        c_topic = pick(['topic_id', 'topic', 'topicid'])
        c_prob = pick(['prob', 'probability', 'topic_prob', 'weight'])
        
        if not (c_book and c_topic and c_prob):
            raise ValueError(
                f"book_topic_probs columns not recognized. Found: {list(book_topic.columns)}\n"
                "Need columns like: book_id, topic_id, prob"
            )
        
        book_topic = book_topic.rename(columns={c_book: 'book_id', c_topic: 'topic_id', c_prob: 'prob'})
        book_topic['topic_id'] = book_topic['topic_id'].astype(int, errors='ignore')
        book_topic['prob'] = pd.to_numeric(book_topic['prob'], errors='coerce')
        
        # Aggregate to book level
        book_cat_long = aggregate_to_book_level(book_topic, topic_lookup, logger)
    
    logger.info(f"Source used: {source_used}")
    logger.info(f"book_cat_long shape: {book_cat_long.shape}")
    
    # Normalize + filter to cohort
    logger.info("\n" + "="*80)
    logger.info("Applying cohort filter")
    logger.info("="*80)
    
    if "goodreads_book_id" in book_cat_long.columns:
        book_cat_long["book_id"] = normalize_id(book_cat_long["goodreads_book_id"])
    elif "book_id" in book_cat_long.columns:
        book_cat_long["book_id"] = normalize_id(book_cat_long["book_id"])
    else:
        raise ValueError(f"book_cat_long has no book_id column. Columns: {book_cat_long.columns.tolist()}")
    
    # Restrict to cohort
    book_cat_long = book_cat_long[book_cat_long["book_id"].isin(set(meta["book_id"]))].copy()
    
    # Overlap check
    assert_overlap(book_cat_long["book_id"], meta["book_id"], "book_cat_long(cohort)", "meta(cohort)", logger=logger)
    logger.info(f"✓ book_cat_long rows after cohort filter: {len(book_cat_long)}")
    
    # Load and merge books_meta
    logger.info("\n" + "="*80)
    logger.info("Loading books metadata")
    logger.info("="*80)
    
    books_meta = None
    if inputs.get('books_meta') is not None:
        meta_path = Path(inputs['books_meta'])
        books_meta = load_table(meta_path)
        logger.info(f"✓ Loaded books_meta: {meta_path}  shape={books_meta.shape}")
        
        # Standardize common columns
        if 'rating_class' not in books_meta.columns and 'group' in books_meta.columns:
            books_meta = books_meta.rename(columns={'group': 'rating_class'})
        
        # author_id normalization
        if 'author_id' not in books_meta.columns:
            for alt in ['author', 'authorid', 'author_id']:
                if alt in books_meta.columns:
                    books_meta = books_meta.rename(columns={alt: 'author_id'})
                    break
        
        # book_id normalization
        if 'book_id' not in books_meta.columns:
            for alt in ['ID', 'id', 'book_id', 'bookid']:
                if alt in books_meta.columns:
                    books_meta = books_meta.rename(columns={alt: 'book_id'})
                    break
        
        # Ensure book_id types match
        if 'book_id' in books_meta.columns:
            books_meta['book_id'] = pd.to_numeric(books_meta['book_id'], errors='coerce')
        
        if 'book_id' in book_cat_long.columns:
            book_cat_long['book_id'] = pd.to_numeric(book_cat_long['book_id'], errors='coerce')
        
        # Merge
        book_cat_long = book_cat_long.merge(
            books_meta,
            on='book_id', how='left', suffixes=('', '_meta')
        )
        
        if 'rating_class' in book_cat_long.columns:
            logger.info("rating_class distribution:")
            logger.info(book_cat_long['rating_class'].value_counts(dropna=False).head(10).to_string())
    else:
        logger.warning("⚠ No books_meta found. book_cat_long will not include rating_class/controls unless already present.")
    
    # Save long and wide formats
    logger.info("\n" + "="*80)
    logger.info("Saving book category proportions")
    logger.info("="*80)
    
    book_cat_long_out = output_dir / "book_taxonomy_main_props_long.parquet"
    book_cat_long.to_parquet(book_cat_long_out, index=False)
    logger.info(f"✓ Saved: {book_cat_long_out}")
    
    # Wide format
    book_cat_wide = (book_cat_long
                     .pivot_table(
                         index='book_id',
                         columns='taxonomy_main_id',
                         values='category_prop',
                         aggfunc='sum',
                         fill_value=0.0
                     )
                     .reset_index())
    book_cat_wide_out = output_dir / "book_taxonomy_main_props_wide.parquet"
    book_cat_wide.to_parquet(book_cat_wide_out, index=False)
    logger.info(f"✓ Saved: {book_cat_wide_out}")
    
    # Compute indices
    logger.info("\n" + "="*80)
    logger.info("Computing derived indices")
    logger.info("="*80)
    
    indices = compute_indices(book_cat_long, books_meta, logger)
    
    indices_out = output_dir / "indices_book_taxonomy_proxy.parquet"
    indices.to_parquet(indices_out, index=False)
    logger.info(f"✓ Saved indices: {indices_out}")
    
    # Optional segment-level processing
    if args.chapter_topic_probs or inputs.get('chapter_topic_probs'):
        logger.info("\n" + "="*80)
        logger.info("Processing chapter/segment topic probabilities")
        logger.info("="*80)
        
        seg_path = args.chapter_topic_probs or inputs.get('chapter_topic_probs')
        if seg_path:
            seg = load_table(Path(seg_path))
            logger.info(f"✓ Loaded segment/chapter topic probs: {seg_path}  shape={seg.shape}")
            
            # Normalize columns
            col_map = {c.lower(): c for c in seg.columns}
            
            def pick(name_options):
                for opt in name_options:
                    if opt in col_map:
                        return col_map[opt]
                return None
            
            c_book = pick(['book_id', 'book', 'bookid'])
            c_topic = pick(['topic_id', 'topic', 'topicid'])
            c_prob = pick(['prob', 'probability', 'topic_prob', 'weight'])
            c_seg = pick(['segment', 'tert', 'tertile', 'chapter_segment', 'part', 'section'])
            
            if c_seg is None:
                logger.info("⚠ No explicit segment column found (begin/middle/end). Segment analysis deferred to Notebook 6.")
            else:
                seg = seg.rename(columns={c_book: 'book_id', c_topic: 'topic_id', c_prob: 'prob', c_seg: 'segment'})
                seg['prob'] = pd.to_numeric(seg['prob'], errors='coerce')
                
                seg = seg.merge(
                    topic_lookup[['topic_id', 'taxonomy_main_id', 'taxonomy_main_name', 'taxonomy_main_group']],
                    on='topic_id', how='left'
                )
                seg['is_mapped'] = seg['taxonomy_main_id'].notna()
                
                seg_cat_long = (seg[seg['is_mapped']]
                    .groupby(['book_id', 'segment', 'taxonomy_main_id', 'taxonomy_main_name', 'taxonomy_main_group'], as_index=False)['prob']
                    .sum()
                    .rename(columns={'prob': 'category_prop_raw'})
                )
                totals = seg_cat_long.groupby(['book_id', 'segment'], as_index=False)['category_prop_raw'].sum().rename(columns={'category_prop_raw': 'mapped_mass'})
                seg_cat_long = seg_cat_long.merge(totals, on=['book_id', 'segment'], how='left')
                seg_cat_long['category_prop'] = seg_cat_long['category_prop_raw'] / seg_cat_long['mapped_mass']
                
                seg_out = output_dir / "segment_taxonomy_main_props_long.parquet"
                seg_cat_long.to_parquet(seg_out, index=False)
                logger.info(f"✓ Saved segment taxonomy proportions: {seg_out}")
    
    logger.info("\n" + "="*80)
    logger.info("✓ Book aggregation complete!")
    logger.info("="*80)


if __name__ == "__main__":
    main()

