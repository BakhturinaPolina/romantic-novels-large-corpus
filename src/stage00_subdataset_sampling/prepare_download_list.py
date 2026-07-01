#!/usr/bin/env python3
"""
prepare_download_list.py

Compare new subsampling results with existing datasets and prepare a download list.

This script:
1. Loads new subsampling splits (train/val/test from results/subsampling/)
2. Loads existing datasets (romance_subdataset_6000.csv, romance_subdataset_next_1000.csv)
3. Loads canonicalized dataset to get MD5 hashes for new subsampling results
4. Checks which books are already downloaded (from existing datasets + download directory)
5. Creates a CSV with books that still need downloading
6. Optionally triggers download using download_parallel_direct.py

Usage:
    python prepare_download_list.py --download-dir ../downloads
    python prepare_download_list.py --download-dir ../downloads --start-download
"""

import argparse
import os
import sys
import pandas as pd
import re
import time
from pathlib import Path
from typing import Set, Dict, List
from difflib import SequenceMatcher

# Add search directory to path for import
sys.path.insert(0, str(Path(__file__).parent.parent / "search"))
from download_parallel_direct import build_downloaded_md5_cache, is_already_downloaded

# Project paths
_THIS_DIR = Path(__file__).parent
# This file is at: src/stage00_subdataset_sampling/prepare_download_list.py
# Project root is 2 levels up
_PROJECT_ROOT = _THIS_DIR.parent.parent

# Default paths
DEFAULT_SUBSAMPLING_DIR = _PROJECT_ROOT / "results" / "subsampling"
DEFAULT_DATA_DIR = _PROJECT_ROOT / "data" / "processed"
DEFAULT_DATA_ROOT = _PROJECT_ROOT / "data"
DEFAULT_DOWNLOAD_DIR = _PROJECT_ROOT / "downloads"
DEFAULT_CANONICALIZED = DEFAULT_DATA_DIR / "romance_books_main_final_canonicalized.csv"

# Existing datasets
EXISTING_6000 = DEFAULT_DATA_DIR / "romance_subdataset_6000.csv"
EXISTING_1000 = DEFAULT_DATA_DIR / "romance_subdataset_next_1000.csv"
# Main dataset with MD5s (if exists)
MAIN_WITH_MD5 = DEFAULT_DATA_ROOT / "romance_books_with_md5.csv"
# MD5 search results (books that were searched)
MD5_SEARCH_RESULTS = DEFAULT_DATA_DIR / "books_needing_md5_search.csv"


def load_subsampling_splits(subsampling_dir: Path) -> pd.DataFrame:
    """
    Load all subsampling splits (train/val/test) and combine into one dataframe.
    
    Returns:
        Combined dataframe with all books from subsampling splits
    """
    print(f"  Scanning {subsampling_dir} for subsampling split files...")
    splits = []
    split_names = ['train', 'val', 'test', 'full']
    
    for split_name in split_names:
        # Try to find files like romance_subdataset_20000_train.csv
        pattern = f"romance_subdataset_*_{split_name}.csv"
        files = list(subsampling_dir.glob(pattern))
        
        if files:
            # Use the most recent one if multiple exist
            file_path = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
            print(f"    ✓ Found {split_name}: {file_path.name} ({file_path.stat().st_size / 1024 / 1024:.1f} MB)")
            start_time = time.time()
            df = pd.read_csv(file_path)
            load_time = time.time() - start_time
            print(f"      Loaded {len(df)} rows in {load_time:.2f}s")
            df['split_source'] = split_name
            splits.append(df)
        else:
            print(f"    ✗ No {split_name} split found")
    
    if not splits:
        raise FileNotFoundError(f"No subsampling split files found in {subsampling_dir}")
    
    # Combine all splits
    print(f"  Combining {len(splits)} splits...")
    combined = pd.concat(splits, ignore_index=True)
    print(f"    Combined total: {len(combined)} books")
    
    # Remove duplicates by work_id if present
    if 'work_id' in combined.columns:
        before = len(combined)
        combined = combined.drop_duplicates(subset=['work_id'], keep='first')
        if len(combined) < before:
            print(f"    Removed {before - len(combined)} duplicate work_ids")
    
    print(f"  ✓ Total unique books from subsampling: {len(combined)}")
    return combined


def load_existing_datasets() -> pd.DataFrame:
    """
    Load existing datasets (6000 and 1000) that have MD5 and downloaded status.
    These datasets have been tagged by tag_downloaded_books.py and match_existing_downloads.py.
    
    Returns:
        Combined dataframe with existing datasets (primary source for MD5s and download status)
    """
    existing_dfs = []
    
    for path, name in [(EXISTING_6000, "6000"), (EXISTING_1000, "1000")]:
        if path.exists():
            print(f"  Loading existing dataset {name}: {path.name}")
            df = pd.read_csv(path)
            df['existing_dataset'] = name
            
            # Verify it has the expected columns
            has_md5 = 'md5' in df.columns
            has_downloaded = 'downloaded' in df.columns
            print(f"    - Has MD5 column: {has_md5}")
            print(f"    - Has downloaded column: {has_downloaded}")
            if has_md5:
                valid_md5 = (df['md5'].notna()) & (df['md5'] != '') & (df['md5'].astype(str).str.len() == 32)
                print(f"    - Valid MD5s: {valid_md5.sum()} / {len(df)}")
            if has_downloaded:
                downloaded_count = ((df['downloaded'] == True) | (df['downloaded'] == 'True') | 
                                  (df['downloaded'].astype(str).str.lower() == 'true')).sum()
                print(f"    - Marked as downloaded: {downloaded_count} / {len(df)}")
            
            existing_dfs.append(df)
        else:
            print(f"  Warning: {path.name} not found, skipping")
    
    if not existing_dfs:
        print("  No existing datasets found")
        return pd.DataFrame()
    
    combined = pd.concat(existing_dfs, ignore_index=True)
    
    # Remove duplicates by work_id if present (keep first occurrence)
    if 'work_id' in combined.columns:
        before = len(combined)
        combined = combined.drop_duplicates(subset=['work_id'], keep='first')
        if len(combined) < before:
            print(f"    - Removed {before - len(combined)} duplicate work_ids")
    
    print(f"  Total unique books from existing datasets: {len(combined)}")
    return combined


def normalize_title(title: str) -> str:
    """Normalize title for comparison."""
    if not title:
        return ""
    # Convert to lowercase
    title = title.lower()
    # Remove punctuation
    title = re.sub(r'[^\w\s]', '', title)
    # Remove extra whitespace
    title = re.sub(r'\s+', '', title)
    return title[:50]  # First 50 chars


def extract_title_from_filename(filename: str) -> str:
    """Extract potential title from filename."""
    stem = Path(filename).stem
    # Remove common patterns
    # Remove work_id patterns like _12345678
    stem = re.sub(r'_\d{6,}$', '', stem)
    # Remove series numbers like "01 - " or "# 08"
    stem = re.sub(r'^\d+\s*[-_]?\s*', '', stem)
    stem = re.sub(r'#\s*\d+', '', stem)
    # Remove author patterns in parentheses
    stem = re.sub(r'\([^)]+\)', '', stem)
    # Remove brackets
    stem = re.sub(r'\[[^\]]+\]', '', stem)
    # Remove epub/pdf mentions
    stem = re.sub(r'\(epub\)|\(pdf\)', '', stem, flags=re.IGNORECASE)
    # Remove "retail" mentions
    stem = re.sub(r'\bretail\b', '', stem, flags=re.IGNORECASE)
    # Remove author name patterns (Last, First or First Last at end)
    stem = re.sub(r'\s*[-_]\s*[A-Z][a-z]+\s+[A-Z][a-z]+\s*$', '', stem)
    stem = re.sub(r'\s*[-_]\s*[A-Z][a-z]+,\s*[A-Z][a-z\.]+\s*$', '', stem)
    
    return stem.strip()


def extract_work_id_from_filename(filename: str) -> str:
    """Extract work_id from filename patterns like 'Title_12345678.epub'."""
    stem = Path(filename).stem
    # Look for _NNNNNNNN pattern at end (7-9 digits)
    match = re.search(r'_(\d{7,9})$', stem)
    if match:
        return match.group(1)
    # Also check for patterns like book_id in middle
    match = re.search(r'_(\d{7,9})_', stem)
    if match:
        return match.group(1)
    return ""


def similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity between two strings."""
    if not s1 or not s2:
        return 0.0
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()


def match_by_metadata(
    df: pd.DataFrame,
    download_dir: Path,
    format: str = 'epub',
    title_threshold: float = 0.7
) -> int:
    """
    Match downloaded files to books by title/author/work_id when MD5s don't match.
    
    Args:
        df: Dataframe with books to check
        download_dir: Directory with downloaded files
        format: File format (default: 'epub')
        title_threshold: Minimum title similarity score (default: 0.7)
    
    Returns:
        Number of additional books matched
    """
    matched_count = 0
    
    # Get all downloaded files
    patterns = [f'*.{format}', f'*.{format.upper()}']
    downloaded_files = []
    for pattern in patterns:
        downloaded_files.extend(download_dir.glob(pattern))
    
    # Skip MD5-named files (already handled by MD5 matching)
    downloaded_files = [
        f for f in downloaded_files
        if not (len(f.stem) == 32 and all(c in '0123456789abcdef' for c in f.stem.lower()))
    ]
    
    if not downloaded_files:
        return 0
    
    print(f"  Matching {len(downloaded_files)} title-named files by metadata...")
    
    # Build lookup structures from dataframe
    print(f"    Building lookup structures from {len(df)} books...")
    start_time = time.time()
    workid_to_book = {}
    title_to_books = {}
    already_downloaded_count = 0
    books_with_workid = 0
    books_with_title = 0
    
    for idx, row in df.iterrows():
        if df.loc[idx, 'already_downloaded']:
            already_downloaded_count += 1
            continue  # Skip already matched books
        
        work_id = str(row.get('work_id', '')).strip() if pd.notna(row.get('work_id')) else ''
        title = str(row.get('title', '')).strip() if pd.notna(row.get('title')) else ''
        author = str(row.get('author_name', '')).strip() if pd.notna(row.get('author_name')) else ''
        
        if work_id:
            workid_to_book[work_id] = {'idx': idx, 'title': title, 'author': author}
            books_with_workid += 1
        
        if title:
            norm_title = normalize_title(title)
            if norm_title:
                if norm_title not in title_to_books:
                    title_to_books[norm_title] = []
                title_to_books[norm_title].append({'idx': idx, 'title': title, 'author': author, 'work_id': work_id})
                books_with_title += 1
    
    build_time = time.time() - start_time
    print(f"      Built in {build_time:.2f}s:")
    print(f"        - {already_downloaded_count} books already marked as downloaded (skipped)")
    print(f"        - {books_with_workid} books with work_id for matching")
    print(f"        - {books_with_title} books with titles for matching")
    print(f"        - {len(title_to_books)} unique normalized titles")
    
    # Match files
    print(f"    Processing {len(downloaded_files)} files...")
    start_time = time.time()
    workid_matches = 0
    title_matches = 0
    
    for i, filepath in enumerate(downloaded_files, 1):
        if i % 10 == 0 or i == len(downloaded_files):
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            print(f"      [{i}/{len(downloaded_files)}] Processed {i} files ({rate:.1f} files/s), matched {matched_count} books (work_id: {workid_matches}, title: {title_matches})...", end='\r')
        filename = filepath.name
        stem = filepath.stem
        
        # Try work_id match first (most reliable)
        extracted_workid = extract_work_id_from_filename(filename)
        if extracted_workid and extracted_workid in workid_to_book:
            book_info = workid_to_book[extracted_workid]
            if not df.loc[book_info['idx'], 'already_downloaded']:
                df.loc[book_info['idx'], 'already_downloaded'] = True
                matched_count += 1
                workid_matches += 1
            continue
        
        # Try title match
        extracted_title = extract_title_from_filename(filename)
        norm_extracted = normalize_title(extracted_title)
        
        if norm_extracted:
            best_match = None
            best_combined_score = 0.0
            
            # Try to extract author from filename first (if available)
            file_author = None
            author_patterns = [
                r'[-_]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\.epub$',
                r'\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'[-_]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\(',  # Author in parentheses
            ]
            for pattern in author_patterns:
                match = re.search(pattern, filename, re.IGNORECASE)
                if match:
                    file_author = match.group(1).lower()
                    break
            
            # Check against all normalized titles
            for norm_title, books in title_to_books.items():
                title_score = similarity_score(norm_extracted, norm_title)
                if title_score >= title_threshold:  # Only consider if title similarity meets threshold
                    # Check each book with this title
                    for book in books:
                        if df.loc[book['idx'], 'already_downloaded']:
                            continue  # Skip already matched
                        
                        # Calculate author score
                        author_score = 1.0  # Default: no author info, assume match
                        if file_author and book['author']:
                            author_score = similarity_score(file_author, book['author'].lower())
                        elif file_author or book['author']:
                            # One has author, other doesn't - penalize slightly
                            author_score = 0.8
                        
                        # Combined score (title + author)
                        combined_score = title_score * 0.7 + author_score * 0.3
                        if combined_score > best_combined_score:
                            best_combined_score = combined_score
                            best_match = book
            
            # Only match if combined score is good enough
            if best_match and best_combined_score >= (title_threshold * 0.7) and not df.loc[best_match['idx'], 'already_downloaded']:
                df.loc[best_match['idx'], 'already_downloaded'] = True
                matched_count += 1
                title_matches += 1
    
    elapsed = time.time() - start_time
    print()  # New line after progress updates
    print(f"    ✓ Completed in {elapsed:.2f}s:")
    print(f"      - {workid_matches} matches by work_id")
    print(f"      - {title_matches} matches by title/author")
    print(f"      - Total: {matched_count} additional books matched")
    return matched_count


def get_md5_from_canonicalized(subsampling_df: pd.DataFrame, canonicalized_path: Path) -> pd.DataFrame:
    """
    Match subsampling books with canonicalized dataset to get MD5 hashes.
    
    Args:
        subsampling_df: Dataframe from subsampling splits
        canonicalized_path: Path to canonicalized dataset
    
    Returns:
        Dataframe with MD5 hashes added
    """
    if not canonicalized_path.exists():
        print(f"  Warning: Canonicalized dataset not found at {canonicalized_path}")
        print("  Will try to get MD5s from existing datasets instead")
        return subsampling_df
    
    print(f"  Loading canonicalized dataset: {canonicalized_path.name}")
    canonicalized = pd.read_csv(canonicalized_path)
    
    # Check if canonicalized has MD5 column
    if 'md5' not in canonicalized.columns:
        print("  Warning: Canonicalized dataset doesn't have 'md5' column")
        return subsampling_df
    
    # Merge on work_id to get MD5
    if 'work_id' in subsampling_df.columns and 'work_id' in canonicalized.columns:
        # Convert work_id to same type for merging
        subsampling_df['work_id'] = subsampling_df['work_id'].astype(str)
        canonicalized['work_id'] = canonicalized['work_id'].astype(str)
        
        # Merge to get MD5
        merged = subsampling_df.merge(
            canonicalized[['work_id', 'md5']],
            on='work_id',
            how='left',
            suffixes=('', '_canonicalized')
        )
        
        # Use canonicalized MD5 if we don't already have one
        if 'md5' in subsampling_df.columns:
            merged['md5'] = merged['md5'].fillna(merged.get('md5_canonicalized', ''))
        else:
            merged['md5'] = merged.get('md5_canonicalized', '')
        
        # Drop temporary column if it exists
        if 'md5_canonicalized' in merged.columns:
            merged = merged.drop(columns=['md5_canonicalized'])
        
        matched = merged['md5'].notna() & (merged['md5'] != '')
        print(f"  Matched MD5 for {matched.sum()} / {len(merged)} books from canonicalized dataset")
        
        return merged
    
    print("  Warning: Cannot match on work_id (column missing)")
    return subsampling_df


def get_md5_from_existing(subsampling_df: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get MD5 hashes from existing datasets by matching work_id.
    Prioritizes non-empty MD5 values.
    
    Args:
        subsampling_df: Dataframe from subsampling splits
        existing_df: Dataframe from existing datasets
    
    Returns:
        Dataframe with MD5 hashes added/updated
    """
    if existing_df.empty or 'md5' not in existing_df.columns:
        return subsampling_df
    
    if 'work_id' not in subsampling_df.columns or 'work_id' not in existing_df.columns:
        return subsampling_df
    
    # Convert work_id to same type
    subsampling_df['work_id'] = subsampling_df['work_id'].astype(str)
    existing_df['work_id'] = existing_df['work_id'].astype(str)
    
    # Filter to only valid MD5s (32 hex chars)
    existing_df_valid = existing_df[
        existing_df['md5'].notna() &
        (existing_df['md5'] != '') &
        (existing_df['md5'].astype(str).str.len() == 32)
    ]
    
    # Create lookup dictionary (work_id -> md5)
    # If multiple MD5s for same work_id, take the first non-empty one
    print(f"    Creating lookup from {len(existing_df_valid)} valid MD5s...")
    existing_md5 = existing_df_valid.groupby('work_id')['md5'].first().to_dict()
    print(f"    Found {len(existing_md5)} unique work_ids with MD5s")
    
    # Fill in MD5s from existing datasets
    if 'md5' not in subsampling_df.columns:
        subsampling_df['md5'] = ''
    
    # Count current MD5s
    current_md5_count = (subsampling_df['md5'].notna() & (subsampling_df['md5'] != '') & 
                        (subsampling_df['md5'].astype(str).str.len() == 32)).sum()
    
    # Update MD5s where we have them from existing datasets
    # Only update if current MD5 is empty/invalid
    mask = subsampling_df['work_id'].isin(existing_md5.keys())
    updated_count = 0
    for idx in subsampling_df[mask].index:
        current_md5 = str(subsampling_df.loc[idx, 'md5']).strip() if pd.notna(subsampling_df.loc[idx, 'md5']) else ''
        work_id = str(subsampling_df.loc[idx, 'work_id'])
        if work_id in existing_md5 and (not current_md5 or len(current_md5) != 32):
            subsampling_df.loc[idx, 'md5'] = existing_md5[work_id]
            updated_count += 1
    
    matched = (subsampling_df['md5'].notna()) & (subsampling_df['md5'] != '') & (subsampling_df['md5'].astype(str).str.len() == 32)
    new_md5_count = matched.sum() - current_md5_count
    print(f"    Updated {updated_count} MD5s, now {matched.sum()} / {len(subsampling_df)} books have MD5s (+{new_md5_count})")
    
    return subsampling_df


def check_downloaded_status(
    df: pd.DataFrame,
    existing_df: pd.DataFrame,
    download_dir: Path,
    format: str = 'epub'
) -> pd.DataFrame:
    """
    Check which books are already downloaded.
    
    Checks:
    1. 'downloaded' column in existing datasets (by work_id)
    2. MD5 matches in existing datasets (if book has MD5 and it's in existing dataset with downloaded=True)
    3. MD5 cache from download directory
    
    Args:
        df: Dataframe with books to check
        existing_df: Dataframe from existing datasets (may have 'downloaded' column)
        download_dir: Directory where downloads are stored
        format: File format (default: 'epub')
    
    Returns:
        Dataframe with 'already_downloaded' column added
    """
    df = df.copy()
    df['already_downloaded'] = False
    
    # Build MD5 cache from download directory (reset cache to ensure fresh scan)
    print(f"\nBuilding MD5 cache from download directory: {download_dir}")
    print(f"  Resetting cache and scanning files...")
    # Reset the global cache to force a fresh scan
    import download_parallel_direct
    download_parallel_direct._downloaded_md5_cache = None
    start_time = time.time()
    downloaded_md5s = build_downloaded_md5_cache(download_dir, verbose=True)
    cache_time = time.time() - start_time
    print(f"  ✓ Found {len(downloaded_md5s)} unique MD5s in {cache_time:.2f}s")
    
    downloaded_count_1 = 0
    downloaded_count_2 = 0
    downloaded_count_3 = 0
    
    # Check 1: From existing datasets' 'downloaded' column (by work_id)
    if not existing_df.empty and 'downloaded' in existing_df.columns:
        if 'work_id' in df.columns and 'work_id' in existing_df.columns:
            # Convert to string for matching
            df['work_id'] = df['work_id'].astype(str)
            existing_df['work_id'] = existing_df['work_id'].astype(str)
            
            # Find books marked as downloaded in existing datasets
            existing_downloaded = existing_df[
                (existing_df['downloaded'] == True) | 
                (existing_df['downloaded'] == 'True') |
                (existing_df['downloaded'].astype(str).str.lower() == 'true')
            ]
            downloaded_work_ids = set(existing_downloaded['work_id'].astype(str))
            
            mask = df['work_id'].isin(downloaded_work_ids)
            df.loc[mask, 'already_downloaded'] = True
            downloaded_count_1 = mask.sum()
            print(f"  Marked {downloaded_count_1} books as downloaded from existing datasets (by work_id)")
    
    # Check 2: From existing datasets' MD5 matches (if book has MD5 and it exists in downloaded books)
    if not existing_df.empty and 'md5' in existing_df.columns and 'md5' in df.columns:
        # Get all MD5s from existing datasets that are marked as downloaded
        if 'downloaded' in existing_df.columns:
            existing_downloaded_md5s = set(
                existing_df[
                    ((existing_df['downloaded'] == True) | 
                     (existing_df['downloaded'] == 'True') |
                     (existing_df['downloaded'].astype(str).str.lower() == 'true')) &
                    existing_df['md5'].notna() &
                    (existing_df['md5'] != '') &
                    (existing_df['md5'].astype(str).str.len() == 32)
                ]['md5'].astype(str).str.lower()
            )
        else:
            # If no downloaded column, use all MD5s from existing dataset
            existing_downloaded_md5s = set(
                existing_df[
                    existing_df['md5'].notna() &
                    (existing_df['md5'] != '') &
                    (existing_df['md5'].astype(str).str.len() == 32)
                ]['md5'].astype(str).str.lower()
            )
        
        # Match by MD5
        if 'md5' in df.columns:
            mask = df['md5'].notna() & (df['md5'] != '') & (~df['already_downloaded'])
            for idx in df[mask].index:
                md5 = str(df.loc[idx, 'md5']).strip().lower()
                if md5 and len(md5) == 32 and md5 in existing_downloaded_md5s:
                    df.loc[idx, 'already_downloaded'] = True
                    downloaded_count_2 += 1
        
        if downloaded_count_2 > 0:
            print(f"  Marked {downloaded_count_2} additional books as downloaded (by MD5 match in existing datasets)")
    
    # Check 3: From download directory MD5 cache (check ALL books with MD5s, not just those not already marked)
    if 'md5' in df.columns:
        # Check all books with valid MD5s, regardless of whether they're already marked
        # This ensures we catch all matches from the downloads folder
        mask = df['md5'].notna() & (df['md5'] != '') & (df['md5'].astype(str).str.len() == 32)
        books_with_md5 = mask.sum()
        print(f"  Checking {books_with_md5} books with MD5s against {len(downloaded_md5s)} downloaded MD5s...")
        start_time = time.time()
        checked = 0
        
        for idx in df[mask].index:
            checked += 1
            if checked % 1000 == 0:
                elapsed = time.time() - start_time
                rate = checked / elapsed if elapsed > 0 else 0
                print(f"    Checked {checked}/{books_with_md5} books ({rate:.0f} books/s)...", end='\r')
            
            md5 = str(df.loc[idx, 'md5']).strip().lower()
            if md5 and len(md5) == 32:
                if md5 in downloaded_md5s:
                    if not df.loc[idx, 'already_downloaded']:
                        downloaded_count_3 += 1
                    df.loc[idx, 'already_downloaded'] = True
        
        elapsed = time.time() - start_time
        print()  # New line after progress
        if downloaded_count_3 > 0:
            print(f"  ✓ Marked {downloaded_count_3} additional books as downloaded from download directory MD5 cache (in {elapsed:.2f}s)")
        else:
            print(f"  ⚠ Warning: No matches found between dataset MD5s and downloaded MD5s (checked in {elapsed:.2f}s)")
            print(f"    This may indicate that MD5s in the dataset don't match the MD5s of downloaded files")
    
    # Check 4: Match by title/author/work_id from filenames (fallback when MD5s don't match)
    print(f"\n  [Check 4] Matching by metadata (title/author/work_id)...")
    downloaded_count_4 = match_by_metadata(df, download_dir, format=format, title_threshold=0.7)
    if downloaded_count_4 > 0:
        print(f"  ✓ Marked {downloaded_count_4} additional books as downloaded (by title/author/work_id from filenames)")
    else:
        print(f"  No additional matches found by metadata")
    
    # Summary of download sources
    print(f"\n  Download status breakdown:")
    print(f"    - From existing datasets (work_id): {downloaded_count_1}")
    print(f"    - From existing datasets (MD5 match): {downloaded_count_2}")
    print(f"    - From download directory (MD5 cache): {downloaded_count_3}")
    print(f"    - From download directory (metadata match): {downloaded_count_4}")
    
    total_downloaded = df['already_downloaded'].sum()
    print(f"\n  Total already downloaded: {total_downloaded} / {len(df)}")
    print(f"  Need to download: {len(df) - total_downloaded}")
    
    return df


def create_download_list(
    df: pd.DataFrame,
    output_path: Path,
    require_md5: bool = True
) -> pd.DataFrame:
    """
    Create a CSV file with books that need downloading.
    
    Args:
        df: Dataframe with 'already_downloaded' column
        output_path: Path to save the download list CSV
        require_md5: If True, only include books with MD5 hashes
    
    Returns:
        Dataframe with books that need downloading
    """
    # Filter to books that need downloading
    to_download = df[~df['already_downloaded']].copy()
    
    # Filter to books with MD5 if required
    if require_md5:
        to_download = to_download[
            to_download['md5'].notna() & 
            (to_download['md5'] != '') &
            (to_download['md5'].str.len() == 32)
        ]
    
    # Select columns needed for download script
    # download_parallel_direct.py expects: md5, title (and optionally other columns)
    columns_to_keep = ['md5', 'title']
    optional_columns = ['work_id', 'author_name', 'author_id', 'publication_year']
    
    for col in optional_columns:
        if col in to_download.columns:
            columns_to_keep.append(col)
    
    # Keep only available columns
    columns_to_keep = [c for c in columns_to_keep if c in to_download.columns]
    to_download = to_download[columns_to_keep]
    
    # Save to CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    to_download.to_csv(output_path, index=False)
    
    print(f"\n✅ Created download list: {output_path}")
    print(f"   {len(to_download)} books ready for download")
    
    if require_md5 and len(df[~df['already_downloaded']]) > len(to_download):
        missing_md5 = len(df[~df['already_downloaded']]) - len(to_download)
        print(f"   ⚠️  {missing_md5} books excluded (no MD5 hash)")
    
    return to_download


def main():
    parser = argparse.ArgumentParser(
        description="Compare subsampling results with existing datasets and prepare download list"
    )
    parser.add_argument(
        '--subsampling-dir',
        type=str,
        default=str(DEFAULT_SUBSAMPLING_DIR),
        help=f"Directory with subsampling splits (default: {DEFAULT_SUBSAMPLING_DIR})"
    )
    parser.add_argument(
        '--canonicalized',
        type=str,
        default=str(DEFAULT_CANONICALIZED),
        help=f"Path to canonicalized dataset (default: {DEFAULT_CANONICALIZED})"
    )
    parser.add_argument(
        '--download-dir',
        type=str,
        default=str(DEFAULT_DOWNLOAD_DIR),
        help=f"Download directory (default: {DEFAULT_DOWNLOAD_DIR})"
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help="Output CSV path for download list (default: data/processed/books_to_download.csv)"
    )
    parser.add_argument(
        '--format',
        type=str,
        default='epub',
        help="File format (default: epub)"
    )
    parser.add_argument(
        '--no-require-md5',
        action='store_true',
        help="Include books without MD5 hashes in download list (not recommended)"
    )
    parser.add_argument(
        '--start-download',
        action='store_true',
        help="Start downloading after creating the list"
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Convert paths
    subsampling_dir = Path(args.subsampling_dir)
    canonicalized_path = Path(args.canonicalized)
    download_dir = Path(args.download_dir)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = DEFAULT_DATA_DIR / "books_to_download.csv"
    
    print("=" * 70)
    print("Prepare Download List from Subsampling Results")
    print("=" * 70)
    print(f"Subsampling dir:  {subsampling_dir}")
    print(f"Canonicalized:    {canonicalized_path}")
    print(f"Download dir:     {download_dir}")
    print(f"Output:           {output_path}")
    print("-" * 70)
    
    script_start_time = time.time()
    
    # Step 1: Load subsampling splits
    print("\n" + "="*70)
    print("[1] Loading subsampling splits...")
    print("="*70)
    step_start = time.time()
    subsampling_df = load_subsampling_splits(subsampling_dir)
    print(f"  Step completed in {time.time() - step_start:.2f}s\n")
    
    # Step 2: Load existing datasets
    print("="*70)
    print("[2] Loading existing datasets...")
    print("="*70)
    step_start = time.time()
    existing_df = load_existing_datasets()
    print(f"  Step completed in {time.time() - step_start:.2f}s\n")
    
    # Step 3: Get MD5 hashes
    print("="*70)
    print("[3] Getting MD5 hashes...")
    print("="*70)
    step_start = time.time()
    
    # First priority: MD5 search results (most recent, most complete)
    if MD5_SEARCH_RESULTS.exists():
        print(f"  Checking MD5 search results: {MD5_SEARCH_RESULTS.name}")
        md5_search_df = pd.read_csv(MD5_SEARCH_RESULTS)
        if 'md5' in md5_search_df.columns:
            subsampling_df = get_md5_from_existing(subsampling_df, md5_search_df)
    
    # Second: Main dataset with MD5s (if exists)
    if MAIN_WITH_MD5.exists():
        print(f"  Checking main dataset with MD5s: {MAIN_WITH_MD5.name}")
        main_md5_df = pd.read_csv(MAIN_WITH_MD5)
        if 'md5' in main_md5_df.columns:
            subsampling_df = get_md5_from_existing(subsampling_df, main_md5_df)
    
    # Third: Existing datasets (6000, 1000)
    if not existing_df.empty:
        subsampling_df = get_md5_from_existing(subsampling_df, existing_df)
    
    # Finally: Canonicalized dataset (unlikely to have MD5s but check anyway)
    subsampling_df = get_md5_from_canonicalized(subsampling_df, canonicalized_path)
    print(f"  Step completed in {time.time() - step_start:.2f}s")
    
    # Count MD5s after merging
    if 'md5' in subsampling_df.columns:
        valid_md5 = (subsampling_df['md5'].notna() & (subsampling_df['md5'] != '') & 
                    (subsampling_df['md5'].astype(str).str.len() == 32)).sum()
        print(f"  Total books with valid MD5s: {valid_md5} / {len(subsampling_df)} ({valid_md5/len(subsampling_df)*100:.1f}%)\n")
    
    # Step 4: Check downloaded status
    print("="*70)
    print("[4] Checking downloaded status...")
    print("="*70)
    step_start = time.time()
    subsampling_df = check_downloaded_status(
        subsampling_df,
        existing_df,
        download_dir,
        format=args.format
    )
    print(f"  Step completed in {time.time() - step_start:.2f}s\n")
    
    # Step 5: Create download list
    print("="*70)
    print("[5] Creating download list...")
    print("="*70)
    step_start = time.time()
    download_list = create_download_list(
        subsampling_df,
        output_path,
        require_md5=not args.no_require_md5
    )
    print(f"  Step completed in {time.time() - step_start:.2f}s\n")
    
    # Summary
    total_time = time.time() - script_start_time
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total books in subsampling:     {len(subsampling_df):,}")
    print(f"Already downloaded:             {subsampling_df['already_downloaded'].sum():,}")
    print(f"Need to download:               {len(download_list):,}")
    if 'md5' in subsampling_df.columns:
        missing_md5 = len(subsampling_df[~subsampling_df['already_downloaded']]) - len(download_list)
        if missing_md5 > 0:
            print(f"Missing MD5s (excluded):        {missing_md5:,}")
    print(f"Download list saved to:         {output_path}")
    print(f"Total script execution time:    {total_time:.2f}s ({total_time/60:.1f} minutes)")
    print("=" * 70)
    
    # Step 6: Optionally start download
    if args.start_download:
        print("\n[6] Starting download...")
        download_script = _PROJECT_ROOT / "search" / "download_parallel_direct.py"
        
        if not download_script.exists():
            print(f"  Error: Download script not found at {download_script}")
            return 1
        
        import subprocess
        cmd = [
            sys.executable,
            str(download_script),
            "--input", str(output_path),
            "--download-dir", str(download_dir),
            "--format", args.format,
            "--single-mode",  # Recommended to avoid rate limits
            "--verbose"
        ]
        
        print(f"  Running: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        return result.returncode
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
