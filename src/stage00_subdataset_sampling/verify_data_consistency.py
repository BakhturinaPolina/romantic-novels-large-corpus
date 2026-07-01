#!/usr/bin/env python3
"""
verify_data_consistency.py

Verify that books and titles are consistent across all datasets:
- Subsampling results (results/subsampling/)
- romance_books_main_final.csv
- romance_books_main_final_canonicalized.csv
- romance_subdataset_6000.csv
- romance_subdataset_next_1000.csv

Checks:
1. Same work_ids appear with same titles
2. Normalization consistency
3. Missing books in any dataset
"""

import pandas as pd
from pathlib import Path
import sys

# Project paths
_THIS_DIR = Path(__file__).parent
# This file is at: src/stage00_subdataset_sampling/verify_data_consistency.py
# Project root is 2 levels up
_PROJECT_ROOT = _THIS_DIR.parent.parent

# File paths
SUBSAMPLING_DIR = _PROJECT_ROOT / "results" / "subsampling"
DATA_DIR = _PROJECT_ROOT / "data" / "processed"

FILES = {
    'subsampling_full': SUBSAMPLING_DIR / "romance_subdataset_20000_full.csv",
    'main_final': DATA_DIR / "romance_books_main_final.csv",
    'main_canonicalized': DATA_DIR / "romance_books_main_final_canonicalized.csv",
    'subset_6000': DATA_DIR / "romance_subdataset_6000.csv",
    'subset_1000': DATA_DIR / "romance_subdataset_next_1000.csv",
}


def load_dataset(name: str, path: Path, usecols=None) -> pd.DataFrame:
    """Load a dataset and return it with a source column."""
    if not path.exists():
        print(f"  ⚠️  {name}: File not found at {path}")
        return pd.DataFrame()
    
    try:
        # For large files, only load required columns
        if usecols:
            df = pd.read_csv(path, usecols=usecols)
        else:
            df = pd.read_csv(path)
        
        df['_source'] = name
        print(f"  ✓ {name}: {len(df):,} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        print(f"  ✗ {name}: Error loading - {e}")
        return pd.DataFrame()


def normalize_title(title):
    """Normalize title for comparison."""
    if pd.isna(title):
        return ""
    title = str(title).strip()
    # Remove extra whitespace
    title = " ".join(title.split())
    return title


def check_consistency():
    """Check consistency across all datasets."""
    print("=" * 80)
    print("DATA CONSISTENCY CHECK")
    print("=" * 80)
    
    # Load all datasets (only work_id and title columns for large files)
    print("\n[1] Loading datasets...")
    datasets = {}
    for name, path in FILES.items():
        # For large main_final file, only load work_id and title
        usecols = None
        if name == 'main_final':
            usecols = ['work_id', 'title']
        elif name in ['main_canonicalized', 'subsampling_full']:
            usecols = ['work_id', 'title']
        
        df = load_dataset(name, path, usecols=usecols)
        if not df.empty:
            datasets[name] = df
    
    if not datasets:
        print("\n❌ No datasets loaded!")
        return
    
    # Check required columns
    print("\n[2] Checking required columns...")
    required_cols = ['work_id', 'title']
    for name, df in datasets.items():
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"  ✗ {name}: Missing columns {missing}")
        else:
            print(f"  ✓ {name}: Has required columns")
    
    # Create unified comparison (more efficient approach)
    print("\n[3] Creating unified comparison...")
    
    # Build lookup dictionaries for each dataset
    lookups = {}
    for name, df in datasets.items():
        if 'work_id' in df.columns and 'title' in df.columns:
            # Create lookup: work_id -> normalized_title
            lookup = {}
            for _, row in df.iterrows():
                work_id = str(row['work_id'])
                title = normalize_title(row['title'])
                lookup[work_id] = title
            lookups[name] = lookup
            print(f"  {name}: {len(lookup):,} books indexed")
    
    # Get all unique work_ids from subsampling (primary reference)
    if 'subsampling_full' in datasets:
        all_work_ids = set(datasets['subsampling_full']['work_id'].astype(str))
        print(f"  Using subsampling_full as reference: {len(all_work_ids):,} work_ids")
    else:
        # Fallback: union of all datasets
        all_work_ids = set()
        for df in datasets.values():
            if 'work_id' in df.columns:
                all_work_ids.update(df['work_id'].astype(str))
        print(f"  Total unique work_ids: {len(all_work_ids):,}")
    
    # Build comparison dataframe (only for subsampling work_ids)
    print("  Building comparison table...")
    comparison = []
    for work_id in sorted(all_work_ids):
        row = {'work_id': work_id}
        
        for name in datasets.keys():
            if name in lookups:
                if work_id in lookups[name]:
                    row[f'{name}_title'] = lookups[name][work_id]
                    row[f'{name}_present'] = True
                else:
                    row[f'{name}_title'] = None
                    row[f'{name}_present'] = False
            else:
                row[f'{name}_title'] = None
                row[f'{name}_present'] = False
        
        comparison.append(row)
    
    comp_df = pd.DataFrame(comparison)
    print(f"  Comparison table created: {len(comp_df):,} rows")
    
    # Check for title mismatches
    print("\n[4] Checking title consistency...")
    
    # Get datasets that have title columns
    title_cols = [c for c in comp_df.columns if c.endswith('_title')]
    
    mismatches = []
    for idx, row in comp_df.iterrows():
        work_id = row['work_id']
        titles = {}
        
        for col in title_cols:
            name = col.replace('_title', '')
            if row[f'{name}_present']:
                title = row[col]
                if title and pd.notna(title):
                    titles[name] = title
        
        if len(titles) > 1:
            # Check if all titles are the same
            unique_titles = set(titles.values())
            if len(unique_titles) > 1:
                mismatches.append({
                    'work_id': work_id,
                    'titles': titles
                })
    
    if mismatches:
        print(f"  ✗ Found {len(mismatches)} work_ids with title mismatches:")
        for i, mm in enumerate(mismatches[:10], 1):
            print(f"\n    {i}. work_id: {mm['work_id']}")
            for name, title in mm['titles'].items():
                print(f"       {name}: {title[:60]}")
        if len(mismatches) > 10:
            print(f"\n    ... and {len(mismatches) - 10} more")
    else:
        print(f"  ✓ All titles are consistent across datasets")
    
    # Check presence in each dataset
    print("\n[5] Checking book presence across datasets...")
    
    presence_summary = {}
    for name in datasets.keys():
        present_col = f'{name}_present'
        if present_col in comp_df.columns:
            count = comp_df[present_col].sum()
            presence_summary[name] = count
            print(f"  {name}: {count:,} books")
    
    # Check overlaps
    print("\n[6] Checking overlaps...")
    
    # Subsampling vs main datasets
    if 'subsampling_full' in datasets and 'main_final' in datasets:
        subsampling_ids = set(datasets['subsampling_full']['work_id'].astype(str))
        main_ids = set(datasets['main_final']['work_id'].astype(str))
        
        in_both = subsampling_ids & main_ids
        only_subsampling = subsampling_ids - main_ids
        only_main = main_ids - subsampling_ids
        
        print(f"\n  Subsampling vs Main Final:")
        print(f"    In both: {len(in_both):,}")
        print(f"    Only in subsampling: {len(only_subsampling):,}")
        print(f"    Only in main: {len(only_main):,}")
        
        if only_subsampling:
            print(f"\n    ⚠️  Sample work_ids only in subsampling:")
            for wid in list(only_subsampling)[:5]:
                print(f"      {wid}")
        
        if only_main:
            print(f"\n    ⚠️  Sample work_ids only in main:")
            for wid in list(only_main)[:5]:
                print(f"      {wid}")
    
    # Subsampling vs canonicalized
    if 'subsampling_full' in datasets and 'main_canonicalized' in datasets:
        subsampling_ids = set(datasets['subsampling_full']['work_id'].astype(str))
        canon_ids = set(datasets['main_canonicalized']['work_id'].astype(str))
        
        in_both = subsampling_ids & canon_ids
        only_subsampling = subsampling_ids - canon_ids
        only_canon = canon_ids - subsampling_ids
        
        print(f"\n  Subsampling vs Canonicalized:")
        print(f"    In both: {len(in_both):,}")
        print(f"    Only in subsampling: {len(only_subsampling):,}")
        print(f"    Only in canonicalized: {len(only_canon):,}")
    
    # Check subsets
    if 'subset_6000' in datasets and 'subset_1000' in datasets:
        subset_6000_ids = set(datasets['subset_6000']['work_id'].astype(str))
        subset_1000_ids = set(datasets['subset_1000']['work_id'].astype(str))
        
        overlap = subset_6000_ids & subset_1000_ids
        if overlap:
            print(f"\n  ⚠️  Overlap between subset_6000 and subset_1000: {len(overlap)} books")
            print(f"      Sample overlapping work_ids: {list(overlap)[:5]}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if mismatches:
        print(f"❌ Found {len(mismatches)} title inconsistencies")
        print("   Review the mismatches above")
    else:
        print("✓ All titles are consistent")
    
    # Check if subsampling books are all in main datasets
    if 'subsampling_full' in datasets:
        subsampling_ids = set(datasets['subsampling_full']['work_id'].astype(str))
        
        if 'main_final' in datasets:
            main_ids = set(datasets['main_final']['work_id'].astype(str))
            missing_in_main = subsampling_ids - main_ids
            if missing_in_main:
                print(f"\n⚠️  {len(missing_in_main)} books in subsampling are NOT in main_final")
            else:
                print(f"\n✓ All subsampling books are in main_final")
        
        if 'main_canonicalized' in datasets:
            canon_ids = set(datasets['main_canonicalized']['work_id'].astype(str))
            missing_in_canon = subsampling_ids - canon_ids
            if missing_in_canon:
                print(f"⚠️  {len(missing_in_canon)} books in subsampling are NOT in canonicalized")
            else:
                print(f"✓ All subsampling books are in canonicalized")
    
    print("=" * 80)
    
    return comp_df, mismatches


def main():
    comp_df, mismatches = check_consistency()
    
    # Save comparison if requested
    if len(sys.argv) > 1 and sys.argv[1] == '--save':
        output_path = DATA_DIR / "data_consistency_check.csv"
        comp_df.to_csv(output_path, index=False)
        print(f"\n💾 Saved comparison to: {output_path}")
    
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
