#!/usr/bin/env python3
"""Detect non-English books in the romance corpus and create v3 filtered dataset.

This script:
1. Samples sentences from each book and uses langdetect to identify language
2. Reports statistics on non-English books
3. Creates v3 train/val/test splits excluding non-English books

Usage:
    python scripts/data/detect_non_english_books.py --analyze    # Just report stats
    python scripts/data/detect_non_english_books.py --create-v3  # Create filtered v3 splits
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

# langdetect: pip install langdetect
try:
    from langdetect import detect, detect_langs, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("WARNING: langdetect not installed. Run: pip install langdetect")

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
LOGGER = logging.getLogger(__name__)

# Paths
DATA_RAW = Path("data/raw/romance_subdataset_downloaded_v2_full")
DATA_PROCESSED = Path("data/processed/romance_subdataset_downloaded_v2_sentences")
OUTPUT_DIR = Path("data/raw/romance_subdataset_filtered_v3")


def detect_book_language(
    df_book: pd.DataFrame,
    sentence_col: str = "sentence",
    sample_size: int = 50,
    min_sentence_len: int = 30,
) -> dict[str, Any]:
    """Detect the primary language of a book by sampling sentences.
    
    Returns dict with: primary_lang, confidence, lang_distribution, n_samples
    """
    # Filter to sentences with sufficient length for reliable detection
    valid_sentences = df_book[df_book[sentence_col].str.len() >= min_sentence_len][sentence_col].tolist()
    
    if len(valid_sentences) == 0:
        return {"primary_lang": "unknown", "confidence": 0.0, "lang_distribution": {}, "n_samples": 0}
    
    # Sample sentences (evenly distributed through book)
    n_samples = min(sample_size, len(valid_sentences))
    step = max(1, len(valid_sentences) // n_samples)
    sampled = [valid_sentences[i] for i in range(0, len(valid_sentences), step)][:n_samples]
    
    lang_counts: Counter[str] = Counter()
    for sentence in sampled:
        try:
            lang = detect(sentence)
            lang_counts[lang] += 1
        except LangDetectException:
            lang_counts["unknown"] += 1
    
    total = sum(lang_counts.values())
    if total == 0:
        return {"primary_lang": "unknown", "confidence": 0.0, "lang_distribution": {}, "n_samples": 0}
    
    primary_lang, primary_count = lang_counts.most_common(1)[0]
    confidence = primary_count / total
    
    return {
        "primary_lang": primary_lang,
        "confidence": confidence,
        "lang_distribution": dict(lang_counts),
        "n_samples": total,
    }


def analyze_corpus_languages(
    sentences_csv: Path,
    metadata_csv: Path | None = None,
    sample_per_book: int = 50,
) -> pd.DataFrame:
    """Analyze language distribution across all books in the corpus.
    
    Returns DataFrame with work_id, primary_lang, confidence, lang_distribution, n_sentences.
    """
    import time
    from datetime import datetime, timedelta
    
    def ts() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[{ts()}] Loading sentences from {sentences_csv}...", flush=True)
    df = pd.read_csv(sentences_csv)
    n_books = df["work_id"].nunique()
    print(f"[{ts()}] Loaded {len(df):,} sentences from {n_books:,} books", flush=True)
    
    results = []
    start_time = time.time()
    non_english_found: dict[str, int] = defaultdict(int)
    
    book_groups = list(df.groupby("work_id"))
    total_books = len(book_groups)
    
    print(f"[{ts()}] Starting language detection for {total_books:,} books...", flush=True)
    print(f"[{ts()}] Sampling {sample_per_book} sentences per book", flush=True)
    print("-" * 80, flush=True)
    
    for i, (work_id, group) in enumerate(book_groups):
        lang_info = detect_book_language(group, sample_size=sample_per_book)
        results.append({
            "work_id": work_id,
            "n_sentences": len(group),
            **lang_info,
        })
        
        # Track non-English
        if lang_info["primary_lang"] != "en":
            non_english_found[lang_info["primary_lang"]] += 1
        
        # Progress every 100 books or at milestones
        if (i + 1) % 100 == 0 or (i + 1) == total_books or (i + 1) in [10, 50]:
            elapsed = time.time() - start_time
            books_per_sec = (i + 1) / elapsed if elapsed > 0 else 0
            remaining = total_books - (i + 1)
            eta_sec = remaining / books_per_sec if books_per_sec > 0 else 0
            eta_str = str(timedelta(seconds=int(eta_sec)))
            
            pct = 100 * (i + 1) / total_books
            non_en_count = sum(non_english_found.values())
            non_en_pct = 100 * non_en_count / (i + 1) if (i + 1) > 0 else 0
            
            print(
                f"[{ts()}] Progress: {i+1:,}/{total_books:,} ({pct:.1f}%) | "
                f"Speed: {books_per_sec:.1f} books/s | ETA: {eta_str} | "
                f"Non-English so far: {non_en_count} ({non_en_pct:.1f}%)",
                flush=True
            )
            
            # Show language breakdown every 500 books
            if (i + 1) % 500 == 0 and non_english_found:
                lang_summary = ", ".join(f"{lang}:{cnt}" for lang, cnt in sorted(non_english_found.items(), key=lambda x: -x[1])[:5])
                print(f"[{ts()}]   Top non-English: {lang_summary}", flush=True)
    
    print("-" * 80, flush=True)
    total_elapsed = time.time() - start_time
    print(f"[{ts()}] Completed in {timedelta(seconds=int(total_elapsed))}", flush=True)
    print(f"[{ts()}] Final: {sum(non_english_found.values())} non-English books detected", flush=True)
    
    results_df = pd.DataFrame(results)
    
    # Merge with metadata if available
    if metadata_csv and metadata_csv.exists():
        meta = pd.read_csv(metadata_csv)
        meta_cols = ["work_id", "title", "author_name"]
        if all(c in meta.columns for c in meta_cols):
            results_df = results_df.merge(meta[meta_cols], on="work_id", how="left")
    
    return results_df


def print_language_report(lang_df: pd.DataFrame) -> None:
    """Print summary statistics about language distribution."""
    print("\n" + "=" * 80)
    print("LANGUAGE ANALYSIS REPORT")
    print("=" * 80)
    
    total_books = len(lang_df)
    english_books = lang_df[lang_df["primary_lang"] == "en"]
    non_english = lang_df[lang_df["primary_lang"] != "en"]
    
    print(f"\nTotal books analyzed: {total_books}")
    print(f"English books: {len(english_books)} ({100 * len(english_books) / total_books:.1f}%)")
    print(f"Non-English books: {len(non_english)} ({100 * len(non_english) / total_books:.1f}%)")
    
    # Language breakdown
    print("\n--- Language Distribution ---")
    lang_counts = lang_df["primary_lang"].value_counts()
    for lang, count in lang_counts.items():
        pct = 100 * count / total_books
        total_sents = lang_df[lang_df["primary_lang"] == lang]["n_sentences"].sum()
        print(f"  {lang}: {count} books ({pct:.1f}%), {total_sents:,} sentences")
    
    # Non-English details
    if len(non_english) > 0:
        print("\n--- Non-English Books (sample) ---")
        cols = ["work_id", "title", "author_name", "primary_lang", "confidence", "n_sentences"]
        display_cols = [c for c in cols if c in non_english.columns]
        sample = non_english.head(20)[display_cols]
        for _, row in sample.iterrows():
            title = row.get("title", "N/A")[:50]
            author = row.get("author_name", "N/A")
            print(f"  [{row['primary_lang']}] {row['work_id']}: \"{title}\" by {author} ({row['n_sentences']} sentences, conf={row['confidence']:.2f})")
        
        if len(non_english) > 20:
            print(f"  ... and {len(non_english) - 20} more non-English books")
    
    # Low confidence English books (might be misdetected)
    low_conf_en = english_books[english_books["confidence"] < 0.7]
    if len(low_conf_en) > 0:
        print(f"\n--- Low-Confidence English Books ({len(low_conf_en)} books, conf < 0.7) ---")
        for _, row in low_conf_en.head(10).iterrows():
            dist = row.get("lang_distribution", {})
            print(f"  {row['work_id']}: conf={row['confidence']:.2f}, dist={dist}")


def create_v3_filtered_splits(
    lang_df: pd.DataFrame,
    min_confidence: float = 0.6,
) -> None:
    """Create v3 train/val/test splits excluding non-English books."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Identify books to keep (English with sufficient confidence)
    keep_books = set(
        lang_df[(lang_df["primary_lang"] == "en") & (lang_df["confidence"] >= min_confidence)]["work_id"]
    )
    exclude_books = set(lang_df["work_id"]) - keep_books
    
    LOGGER.info("Keeping %d English books (conf >= %.2f)", len(keep_books), min_confidence)
    LOGGER.info("Excluding %d non-English/low-confidence books", len(exclude_books))
    
    # Process each split
    for split_name in ["train", "val", "test"]:
        input_csv = DATA_PROCESSED / f"sentences_{split_name}.csv"
        if not input_csv.exists():
            LOGGER.warning("Skipping missing file: %s", input_csv)
            continue
        
        LOGGER.info("Processing %s split...", split_name)
        df = pd.read_csv(input_csv)
        n_before = len(df)
        books_before = df["work_id"].nunique()
        
        # Filter to English books only
        df_filtered = df[df["work_id"].isin(keep_books)].reset_index(drop=True)
        n_after = len(df_filtered)
        books_after = df_filtered["work_id"].nunique()
        
        output_csv = OUTPUT_DIR / f"sentences_{split_name}.csv"
        df_filtered.to_csv(output_csv, index=False)
        
        LOGGER.info(
            "  %s: %d → %d sentences (%.1f%% kept), %d → %d books",
            split_name,
            n_before,
            n_after,
            100 * n_after / n_before,
            books_before,
            books_after,
        )
    
    # Copy and filter metadata
    for split_name in ["train", "val", "test", "full"]:
        meta_input = DATA_RAW / "subsampling_metadata" / f"romance_subdataset_downloaded_v2_{split_name}.csv"
        if not meta_input.exists():
            continue
        
        meta_df = pd.read_csv(meta_input)
        meta_filtered = meta_df[meta_df["work_id"].isin(keep_books)].reset_index(drop=True)
        
        meta_output = OUTPUT_DIR / "subsampling_metadata" / f"romance_subdataset_filtered_v3_{split_name}.csv"
        meta_output.parent.mkdir(parents=True, exist_ok=True)
        meta_filtered.to_csv(meta_output, index=False)
        LOGGER.info("  Metadata %s: %d → %d books", split_name, len(meta_df), len(meta_filtered))
    
    # Save exclusion manifest
    exclusion_manifest = {
        "created_at": pd.Timestamp.now().isoformat(),
        "min_confidence": min_confidence,
        "total_books_analyzed": len(lang_df),
        "books_kept": len(keep_books),
        "books_excluded": len(exclude_books),
        "excluded_work_ids": sorted(exclude_books),
        "language_distribution": lang_df["primary_lang"].value_counts().to_dict(),
    }
    manifest_path = OUTPUT_DIR / "v3_filtering_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(exclusion_manifest, f, indent=2)
    LOGGER.info("Saved exclusion manifest: %s", manifest_path)
    
    # Save language analysis results
    lang_df.to_csv(OUTPUT_DIR / "language_analysis.csv", index=False)
    LOGGER.info("Saved language analysis: %s", OUTPUT_DIR / "language_analysis.csv")
    
    print(f"\n✅ Created v3 filtered dataset in {OUTPUT_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Detect non-English books in corpus")
    parser.add_argument("--analyze", action="store_true", help="Just report language statistics")
    parser.add_argument("--create-v3", action="store_true", help="Create v3 filtered splits")
    parser.add_argument("--sample-per-book", type=int, default=50, help="Sentences to sample per book")
    parser.add_argument("--min-confidence", type=float, default=0.6, help="Min confidence to keep English books")
    parser.add_argument("--split", type=str, default="train", help="Split to analyze (train/val/test/all)")
    parser.add_argument("--use-cached", action="store_true", help="Use cached language analysis if available")
    args = parser.parse_args()
    
    if not LANGDETECT_AVAILABLE:
        print("ERROR: langdetect is required. Install with: pip install langdetect")
        return 1
    
    cached_analysis = OUTPUT_DIR / "language_analysis.csv"
    
    if args.use_cached and cached_analysis.exists():
        LOGGER.info("Loading cached language analysis from %s", cached_analysis)
        lang_df = pd.read_csv(cached_analysis)
    else:
        # Determine which splits to analyze
        if args.create_v3 or args.split == "all":
            splits_to_analyze = ["train", "val", "test"]
        else:
            splits_to_analyze = [args.split]
        
        all_results = []
        for split_name in splits_to_analyze:
            sentences_csv = DATA_PROCESSED / f"sentences_{split_name}.csv"
            metadata_csv = DATA_RAW / "subsampling_metadata" / f"romance_subdataset_downloaded_v2_{split_name}.csv"
            
            if not sentences_csv.exists():
                print(f"WARNING: Sentences file not found: {sentences_csv}, skipping")
                continue
            
            print(f"\n{'='*80}")
            print(f"ANALYZING {split_name.upper()} SPLIT")
            print(f"{'='*80}")
            
            split_df = analyze_corpus_languages(
                sentences_csv=sentences_csv,
                metadata_csv=metadata_csv if metadata_csv.exists() else None,
                sample_per_book=args.sample_per_book,
            )
            split_df["split"] = split_name
            all_results.append(split_df)
        
        if not all_results:
            print("ERROR: No splits could be analyzed")
            return 1
        
        lang_df = pd.concat(all_results, ignore_index=True)
        # Remove duplicate work_ids if any (keep first occurrence)
        lang_df = lang_df.drop_duplicates(subset=["work_id"], keep="first")
        print(f"\n{'='*80}")
        print(f"COMBINED ANALYSIS: {len(lang_df)} unique books across {len(splits_to_analyze)} splits")
        print(f"{'='*80}")
    
    if args.analyze or not args.create_v3:
        print_language_report(lang_df)
    
    if args.create_v3:
        create_v3_filtered_splits(lang_df, min_confidence=args.min_confidence)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
