#!/usr/bin/env python3
"""
create_subdataset_flexible.py

Flexible sub-dataset sampler + splitter for the Goodreads Romance project.

WHY THIS EXISTS
---------------
You have a full canonicalized romance corpus (~52k books) and want to:
1) Keep a smaller working corpus (<= 20k) for the big project.
2) Avoid selection bias from always choosing the most-engaged books.
3) Still keep enough review text for BERTopic (topic modeling).
4) Create train/val/test splits with a TIME-BASED holdout
   (harder but stronger generalization: learn on earlier years, test on later years).

DESIGN OVERVIEW
---------------
A) Sampling (build a "full subset" of size total_n):
   - We stratify by:
       year_bin × genre_group × engagement_tier × rating_tier
   - Then we sample within each stratum using one of three modes:
       1) inference: random within each cell (less engagement bias)
       2) topic:     top-engagement within each cell (text-rich)
       3) hybrid:    mix inference + topic inside each cell (recommended)
          e.g., 70% random + 30% top-engagement

B) Splitting (train/val/test):
   - Simple fraction-based TIME split:
       sort by publication_year (unknown years placed first),
       then take the earliest books as train, middle as val, latest as test.

OUTPUTS
-------
Results are saved to: <project_root>/results/subsampling/
- romance_subdataset_<N>_full.csv
- romance_subdataset_<N>_train.csv
- romance_subdataset_<N>_val.csv
- romance_subdataset_<N>_test.csv

EXAMPLE COMMAND (your planned setup)
------------------------------------
python create_subdataset_flexible.py \
  --input "/.../romance_books_main_final_canonicalized.csv" \
  --outdir "/.../results/subsampling" \
  --total_n 20000 \
  --mode hybrid \
  --inference_share 0.7 \
  --split_strategy time \
  --train_frac 0.70 \
  --val_frac 0.15 \
  --year_bin_years 5 \
  --seed 42

NOTES / EXPECTATIONS ABOUT INPUT CSV
------------------------------------
The script will work best if your CSV has these columns (some are optional):
- work_id (preferred unique book identifier)
- publication_year
- genres_str
- ratings_count_sum (engagement proxy)
- text_reviews_count_sum (optional engagement proxy)
- average_rating_weighted_mean (rating/quality proxy)
- author_id (optional, used only if you choose author split)

If a column is missing, the script degrades gracefully (uses 'unknown' strata labels).
"""

import argparse
import os
import numpy as np
import pandas as pd


# Default random seed for reproducible sampling
RANDOM_SEED_DEFAULT = 42

# Compute project root relative to this file's location
# This file is at: src/stage00_subdataset_sampling/create_subdataset_flexible.py
# Project root is 2 levels up
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(os.path.dirname(_THIS_DIR))

# Default output directory: <project_root>/results/subsampling/
DEFAULT_OUTDIR = os.path.join(_PROJECT_ROOT, "results", "subsampling")


# -----------------------------
#  Helper: genre grouping
# -----------------------------
def _genre_group(genres_str: str) -> str:
    """
    Map raw genre strings into a small set of canonical genre groups.

    This is intentionally coarse. You can expand/modify rules later.
    """
    s = str(genres_str).lower()
    if 'paranormal' in s:
        return 'paranormal'
    if 'historical romance' in s:
        return 'historical'
    if 'fantasy' in s:
        return 'fantasy'
    if 'mystery' in s:
        return 'mystery'
    if 'young adult' in s:
        return 'young_adult'
    return 'other'


# -----------------------------
#  Helper: year binning
# -----------------------------
def _make_year_bins(year_series: pd.Series, bin_years: int = 5) -> pd.Series:
    """
    Convert publication_year into fixed-width bins like:
      2000-2004, 2005-2009, 2010-2014, ...

    Missing/unparseable years -> 'unknown'.

    Why bins:
      - Stratification by raw year creates too many tiny cells.
      - Bins preserve time structure without exploding strata.
    """
    y = pd.to_numeric(year_series, errors='coerce')

    if y.notna().sum() == 0:
        return pd.Series(['unknown'] * len(year_series), index=year_series.index)

    y_min = int(np.nanmin(y))
    y_max = int(np.nanmax(y))

    # Align bins to multiples of bin_years (e.g., 2000, 2005, 2010, ...)
    start = (y_min // bin_years) * bin_years
    end = ((y_max // bin_years) + 1) * bin_years

    bins = list(range(start, end + 1, bin_years))
    labels = [f"{b}-{b + bin_years - 1}" for b in bins[:-1]]

    out = pd.cut(y, bins=bins, labels=labels, include_lowest=True)
    return out.astype(str).fillna('unknown')


# -----------------------------
#  Helper: safe qcut
# -----------------------------
def _qcut_safe(x: pd.Series, q: int, labels):
    """
    Quantile-binning with safety:
      - If too few non-NaN values, return 'unknown'
      - If qcut fails due to many ties, return 'unknown'

    Used for:
      engagement_tier (ratings_count_sum quantiles)
      rating_tier (average_rating_weighted_mean quantiles)
    """
    x2 = pd.to_numeric(x, errors='coerce')
    if x2.notna().sum() < q:
        return pd.Series(['unknown'] * len(x), index=x.index)

    try:
        return pd.qcut(x2, q=q, labels=labels, duplicates='drop').astype(str)
    except Exception:
        return pd.Series(['unknown'] * len(x), index=x.index)


# -----------------------------
#  Helper: compute quotas per cell
# -----------------------------
def _quota_table(df: pd.DataFrame, strata_cols, target_n: int, min_per_cell: int = 1) -> pd.DataFrame:
    """
    Compute per-cell sampling quotas proportional to cell sizes.

    - target_n: total desired sample size
    - min_per_cell: ensure at least 1 book from each cell that exists

    Then we do a rounding fix to hit exactly target_n.
    """
    base = df.groupby(strata_cols).size().rename('n').reset_index()
    base['prop'] = base['n'] / base['n'].sum()

    # Floor allocation and then enforce minimums
    base['quota'] = np.floor(base['prop'] * target_n).astype(int)
    base.loc[(base['n'] > 0) & (base['quota'] < min_per_cell), 'quota'] = min_per_cell

    # Fix rounding so sum(quota) == target_n
    diff = int(target_n - base['quota'].sum())

    if diff > 0:
        # Add 1 to the largest-proportion cells
        bump_idx = base.sort_values('prop', ascending=False).index[:diff]
        base.loc[bump_idx, 'quota'] += 1
    elif diff < 0:
        # Remove 1 from smallest-proportion cells (but keep min_per_cell)
        candidates = base[base['quota'] > min_per_cell].sort_values('prop')
        drop_idx = candidates.index[:(-diff)]
        base.loc[drop_idx, 'quota'] -= 1

    return base


# -----------------------------
#  Helper: sample from a single cell
# -----------------------------
def _sample_cell(df_cell: pd.DataFrame, n: int, mode: str, rng: np.random.Generator) -> pd.DataFrame:
    """
    Sample n rows from df_cell using one of two behaviors:
      - mode="topic": prefer high engagement (top-of-cell) -> text-rich
      - mode="inference": random within cell -> less selection bias

    For "topic", we sort by a few engagement-like columns if present.
    """
    if n <= 0 or df_cell.empty:
        return df_cell.iloc[0:0]

    if mode == "topic":
        sort_cols = [c for c in ['ratings_count_sum', 'text_reviews_count_sum', 'author_ratings_count']
                     if c in df_cell.columns]
        if sort_cols:
            inner = df_cell.sort_values(by=sort_cols, ascending=[False] * len(sort_cols))
        else:
            inner = df_cell
        return inner.head(n)

    # inference mode: random sample in the cell
    return df_cell.sample(
        n=min(n, len(df_cell)),
        random_state=int(rng.integers(0, 2**31 - 1))
    )


# -----------------------------
#  Main: create the subset + splits
# -----------------------------
def create_subdataset_flexible(
    input_csv_path: str,
    total_n: int = 20000,
    outdir: str = None,
    mode: str = "hybrid",          # inference | topic | hybrid
    inference_share: float = 0.7,  # only used for hybrid
    min_text_reviews: int = 0,     # optional threshold to ensure enough text
    year_bin_years: int = 5,
    seed: int = RANDOM_SEED_DEFAULT,
    split_strategy: str = "time",  # random | author | time
    train_frac: float = 0.70,
    val_frac: float = 0.15
):
    """
    Build a subset of size total_n and create train/val/test splits.

    For your request:
      - total_n <= 20000
      - split_strategy="time" (fraction-based time split)

    Returns a dict with output paths and row counts.
    """
    # Use default output directory if not specified
    if outdir is None:
        outdir = DEFAULT_OUTDIR

    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(seed)

    # Load
    meta = pd.read_csv(input_csv_path)

    # Filter: remove comics/graphic (matches your existing sampling intent)
    if 'genres_str' in meta.columns:
        meta = meta[~meta['genres_str'].astype(str).str.contains('comics|graphic', case=False, na=False)].copy()

    # Optional: ensure minimum number of text reviews (improves BERTopic quality)
    if min_text_reviews > 0 and 'text_reviews_count_sum' in meta.columns:
        tr = pd.to_numeric(meta['text_reviews_count_sum'], errors='coerce').fillna(0)
        meta = meta[tr >= min_text_reviews].copy()

    # Add derived stratification columns
    meta['genre_group'] = meta['genres_str'].apply(_genre_group) if 'genres_str' in meta.columns else 'other'

    year_col = 'publication_year' if 'publication_year' in meta.columns else None
    meta['year_bin'] = _make_year_bins(meta[year_col] if year_col else pd.Series([np.nan] * len(meta)),
                                       bin_years=year_bin_years)

    # Engagement tier: use ratings_count_sum quantiles if available
    if 'ratings_count_sum' in meta.columns:
        meta['engagement_tier'] = _qcut_safe(
            meta['ratings_count_sum'],
            q=3,
            labels=['low_eng', 'mid_eng', 'high_eng']
        )
    else:
        meta['engagement_tier'] = 'unknown'

    # Rating tier: use average_rating_weighted_mean quantiles if available
    if 'average_rating_weighted_mean' in meta.columns:
        meta['rating_tier'] = _qcut_safe(
            meta['average_rating_weighted_mean'],
            q=3,
            labels=['low_rate', 'mid_rate', 'high_rate']
        )
    else:
        meta['rating_tier'] = 'unknown'

    # Deduplicate on work_id if present (important to avoid duplicates from preprocessing merges)
    if 'work_id' in meta.columns:
        meta = meta.drop_duplicates(subset=['work_id']).copy()

    # Define strata (this is your "representativeness spine")
    strata = ['year_bin', 'genre_group', 'engagement_tier', 'rating_tier']

    # Allocate quotas
    quotas = _quota_table(meta, strata, target_n=total_n, min_per_cell=1)

    # Sample cell-by-cell
    picked = []
    for _, row in quotas.iterrows():
        mask = np.ones(len(meta), dtype=bool)
        for c in strata:
            mask &= (meta[c].astype(str) == str(row[c]))

        cell = meta.loc[mask]
        n = int(row['quota'])

        if mode == "hybrid":
            # Split the quota into random + top-engagement inside the same cell
            n_inf = int(np.floor(n * inference_share))
            n_top = n - n_inf

            part_inf = _sample_cell(cell, n_inf, mode="inference", rng=rng)
            remaining = cell.loc[~cell.index.isin(part_inf.index)]
            part_top = _sample_cell(remaining, n_top, mode="topic", rng=rng)

            cell_pick = pd.concat([part_inf, part_top], axis=0)
        else:
            cell_pick = _sample_cell(cell, n, mode=mode, rng=rng)

        picked.append(cell_pick)

    sub = pd.concat(picked, axis=0)

    # Ensure uniqueness again
    if 'work_id' in sub.columns:
        sub = sub.drop_duplicates(subset=['work_id'])

    # If we ended up short due to tiny cells, top up randomly from remaining pool
    if len(sub) < total_n:
        remainder = meta.loc[~meta.index.isin(sub.index)]
        need = total_n - len(sub)
        if need > 0 and len(remainder) > 0:
            sub = pd.concat([
                sub,
                remainder.sample(
                    n=min(need, len(remainder)),
                    random_state=int(rng.integers(0, 2**31 - 1))
                )
            ])
            if 'work_id' in sub.columns:
                sub = sub.drop_duplicates(subset=['work_id'])

    # Hard cap to exact N
    sub = sub.head(total_n).copy()

    # Write full subset
    base = f"romance_subdataset_{total_n}"
    full_path = os.path.join(outdir, f"{base}_full.csv")
    sub.to_csv(full_path, index=False)

    # Split into train/val/test
    train_df, val_df, test_df = split_subdataset(
        sub,
        strategy=split_strategy,
        seed=seed,
        train_frac=train_frac,
        val_frac=val_frac
    )

    train_path = os.path.join(outdir, f"{base}_train.csv")
    val_path = os.path.join(outdir, f"{base}_val.csv")
    test_path = os.path.join(outdir, f"{base}_test.csv")

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    return {
        "full": full_path,
        "train": train_path,
        "val": val_path,
        "test": test_path,
        "n_full": len(sub),
        "n_train": len(train_df),
        "n_val": len(val_df),
        "n_test": len(test_df),
    }


# -----------------------------
#  Splitter: fraction-based time split
# -----------------------------
def split_subdataset(
    df: pd.DataFrame,
    strategy: str = "time",
    seed: int = RANDOM_SEED_DEFAULT,
    train_frac: float = 0.70,
    val_frac: float = 0.15
):
    """
    Split a subset into train/val/test.

    For your requested setting:
      strategy="time"

    TIME STRATEGY (fraction-based with within-year shuffle):
      - convert publication_year to numeric (NaN if missing)
      - sort by year ascending
      - unknown years are placed FIRST (na_position="first"), and therefore
        tend to land in train (avoids artificially hard test set with unknowns)
      - shuffle rows *within each year* (reproducibly with seed) to avoid
        within-year ordering artifacts while preserving year order
      - allocate earliest fraction to train, next to val, latest to test

    This creates a "future era" test set in a simple, reproducible way.
    No leakage across time; later years still go to val/test.
    """
    rng = np.random.default_rng(seed)

    test_frac = 1.0 - train_frac - val_frac
    if test_frac <= 0:
        raise ValueError("train_frac + val_frac must be < 1.0")

    df = df.copy()

    if strategy == "time":
        if "publication_year" not in df.columns:
            # fallback: if year missing, do random by work_id
            return split_subdataset(df, strategy="random", seed=seed, train_frac=train_frac, val_frac=val_frac)

        df = df.copy()
        y = pd.to_numeric(df["publication_year"], errors="coerce")
        df["_py"] = y

        # 1) Sort by year (unknown years first so they go to train)
        df_sorted = df.sort_values(by=["_py"], na_position="first")

        # 2) Shuffle *within each year* (including the NaN group), but keep year ordering
        # We do this by grouping on _py and sampling each group with a deterministic seed
        # derived from the global seed (so results are stable/reproducible).
        pieces = []
        for i, (yr, g) in enumerate(df_sorted.groupby("_py", sort=False, dropna=False)):
            # deterministic per-year random_state so shuffle is stable across runs
            rs = seed + i
            pieces.append(g.sample(frac=1.0, random_state=rs))

        df_shuffled = pd.concat(pieces, axis=0)

        # 3) Fraction-based split
        n = len(df_shuffled)
        n_train = int(np.floor(n * train_frac))
        n_val = int(np.floor(n * val_frac))

        train_df = df_shuffled.iloc[:n_train].drop(columns=["_py"])
        val_df = df_shuffled.iloc[n_train:n_train + n_val].drop(columns=["_py"])
        test_df = df_shuffled.iloc[n_train + n_val:].drop(columns=["_py"])

        return train_df, val_df, test_df

    # Other options (kept for completeness)
    if strategy == "random":
        # Prefer splitting by work_id so a work cannot appear in multiple sets
        if "work_id" in df.columns:
            groups = df["work_id"].astype(str).unique().tolist()
            rng.shuffle(groups)

            n = len(groups)
            n_train = int(np.floor(n * train_frac))
            n_val = int(np.floor(n * val_frac))

            train_groups = set(groups[:n_train])
            val_groups = set(groups[n_train:n_train + n_val])
            test_groups = set(groups[n_train + n_val:])

            train_df = df[df["work_id"].astype(str).isin(train_groups)]
            val_df = df[df["work_id"].astype(str).isin(val_groups)]
            test_df = df[df["work_id"].astype(str).isin(test_groups)]
            return train_df, val_df, test_df

        # fallback: row-level shuffle (not ideal)
        df = df.sample(frac=1.0, random_state=seed)
        n = len(df)
        n_train = int(np.floor(n * train_frac))
        n_val = int(np.floor(n * val_frac))
        return df.iloc[:n_train], df.iloc[n_train:n_train + n_val], df.iloc[n_train + n_val:]

    if strategy == "author":
        # Optional: group split by author if you want to prevent author leakage
        author_col = None
        for c in ["author_id", "author_id_median", "author_id_primary", "author"]:
            if c in df.columns:
                author_col = c
                break

        if author_col is None:
            return split_subdataset(df, strategy="random", seed=seed, train_frac=train_frac, val_frac=val_frac)

        groups = df[author_col].astype(str).unique().tolist()
        rng.shuffle(groups)

        n = len(groups)
        n_train = int(np.floor(n * train_frac))
        n_val = int(np.floor(n * val_frac))

        train_groups = set(groups[:n_train])
        val_groups = set(groups[n_train:n_train + n_val])
        test_groups = set(groups[n_train + n_val:])

        train_df = df[df[author_col].astype(str).isin(train_groups)]
        val_df = df[df[author_col].astype(str).isin(val_groups)]
        test_df = df[df[author_col].astype(str).isin(test_groups)]
        return train_df, val_df, test_df

    # Ultimate fallback
    return split_subdataset(df, strategy="random", seed=seed, train_frac=train_frac, val_frac=val_frac)


# -----------------------------
#  CLI
# -----------------------------
def _parse_args():
    ap = argparse.ArgumentParser(
        description="Flexible sub-dataset sampler + splitter for Goodreads Romance project."
    )
    ap.add_argument("--input", required=True, help="Path to romance_books_main_final_canonicalized.csv (or equivalent)")
    ap.add_argument("--outdir", default=None,
                    help=f"Output directory for subset files (default: {DEFAULT_OUTDIR})")
    ap.add_argument("--total_n", type=int, default=20000)
    ap.add_argument("--mode", choices=["inference", "topic", "hybrid"], default="hybrid")
    ap.add_argument("--inference_share", type=float, default=0.7, help="Only used for hybrid mode")
    ap.add_argument("--min_text_reviews", type=int, default=0, help="Optional min text_reviews_count_sum threshold")
    ap.add_argument("--year_bin_years", type=int, default=5)
    ap.add_argument("--seed", type=int, default=RANDOM_SEED_DEFAULT)
    ap.add_argument("--split_strategy", choices=["random", "author", "time"], default="time")
    ap.add_argument("--train_frac", type=float, default=0.70)
    ap.add_argument("--val_frac", type=float, default=0.15)
    return ap.parse_args()


def main():
    args = _parse_args()

    # Use default outdir if not provided
    outdir = args.outdir if args.outdir else DEFAULT_OUTDIR

    print("=" * 70)
    print("Flexible Sub-dataset Sampler + Splitter")
    print("=" * 70)
    print(f"Input CSV:       {args.input}")
    print(f"Output dir:      {outdir}")
    print(f"Total N:         {args.total_n}")
    print(f"Mode:            {args.mode}", end="")
    if args.mode == "hybrid":
        print(f" (inference_share={args.inference_share})")
    else:
        print()
    print(f"Split strategy:  {args.split_strategy}")
    print(f"Train/Val/Test:  {args.train_frac:.0%} / {args.val_frac:.0%} / {1 - args.train_frac - args.val_frac:.0%}")
    print(f"Year bin width:  {args.year_bin_years} years")
    print(f"Random seed:     {args.seed}")
    print("-" * 70)

    res = create_subdataset_flexible(
        input_csv_path=args.input,
        total_n=args.total_n,
        outdir=outdir,
        mode=args.mode,
        inference_share=args.inference_share,
        min_text_reviews=args.min_text_reviews,
        year_bin_years=args.year_bin_years,
        seed=args.seed,
        split_strategy=args.split_strategy,
        train_frac=args.train_frac,
        val_frac=args.val_frac,
    )

    print("\n✅ Done!")
    print("-" * 70)
    print(f"Full subset:  {res['n_full']:,} books → {res['full']}")
    print(f"Train set:    {res['n_train']:,} books → {res['train']}")
    print(f"Val set:      {res['n_val']:,} books → {res['val']}")
    print(f"Test set:     {res['n_test']:,} books → {res['test']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
