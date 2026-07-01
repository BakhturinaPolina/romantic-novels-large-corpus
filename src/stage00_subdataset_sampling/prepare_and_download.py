#!/usr/bin/env python3
"""
prepare_and_download.py

Complete workflow to prepare subdataset CSVs with MD5 hashes and download books.

This script:
1. Merges MD5 hashes from various sources into subdataset CSVs
2. Creates a download list
3. Optionally runs downloads

Usage:
    # Step 1: Prepare download list (merges MD5s, checks what's already downloaded)
    python prepare_and_download.py --prepare-only
    
    # Step 2: Download books (after reviewing the download list)
    python prepare_and_download.py --download-only
    
    # Or do both in one go:
    python prepare_and_download.py --prepare-and-download
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from prepare_download_list import main as prepare_main
from prepare_download_list import DEFAULT_DATA_DIR, DEFAULT_DOWNLOAD_DIR

import subprocess
import os


def run_prepare():
    """Run the prepare_download_list script."""
    print("=" * 70)
    print("STEP 1: Preparing download list")
    print("=" * 70)
    
    # Use default paths
    download_dir = DEFAULT_DOWNLOAD_DIR
    output_path = DEFAULT_DATA_DIR / "books_to_download.csv"
    
    # Build command
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "prepare_download_list.py"),
        "--download-dir", str(download_dir),
        "--output", str(output_path),
        "--format", "epub",
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print(f"\n❌ Error: prepare_download_list.py failed with exit code {result.returncode}")
        return False
    
    print(f"\n✅ Download list prepared: {output_path}")
    return True


def run_download(use_no_quota=True, max_workers=2, delay=2.0, single_mode=False):
    """Run the download script."""
    print("=" * 70)
    print("STEP 2: Downloading books")
    print("=" * 70)
    
    download_dir = DEFAULT_DOWNLOAD_DIR
    input_path = DEFAULT_DATA_DIR / "books_to_download.csv"
    
    if not input_path.exists():
        print(f"❌ Error: Download list not found: {input_path}")
        print("   Run with --prepare-only first")
        return False
    
    # Build command
    download_script = Path(__file__).parent.parent / "search" / "download_parallel_direct.py"
    
    if not download_script.exists():
        print(f"❌ Error: Download script not found: {download_script}")
        return False
    
    cmd = [
        sys.executable,
        str(download_script),
        "--input", str(input_path),
        "--download-dir", str(download_dir),
        "--format", "epub",
        "--max-workers", str(max_workers),
        "--delay", str(delay),
    ]
    
    if use_no_quota:
        cmd.append("--no-quota")
    
    if single_mode:
        cmd.append("--single-mode")
    else:
        cmd.append("--verbose")
    
    print(f"Running: {' '.join(cmd)}")
    print(f"\nNote: IPFS links may return HTML (ad pages) - the script will try to handle this")
    print(f"      If downloads fail, try --single-mode for more reliable downloads\n")
    
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print(f"\n⚠️  Download script exited with code {result.returncode}")
        print("   Some downloads may have failed - check logs above")
        return False
    
    print(f"\n✅ Downloads completed")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Prepare subdataset CSVs with MD5 hashes and download books"
    )
    parser.add_argument(
        '--prepare-only',
        action='store_true',
        help="Only prepare download list (merge MD5s, check downloads)"
    )
    parser.add_argument(
        '--download-only',
        action='store_true',
        help="Only run downloads (assumes download list already exists)"
    )
    parser.add_argument(
        '--prepare-and-download',
        action='store_true',
        help="Do both: prepare list and download"
    )
    parser.add_argument(
        '--max-workers',
        type=int,
        default=2,
        help="Number of parallel download workers (default: 2)"
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=2.0,
        help="Delay between downloads per worker in seconds (default: 2.0)"
    )
    parser.add_argument(
        '--single-mode',
        action='store_true',
        help="Use sequential downloads (slower but more reliable, avoids IPFS HTML issues)"
    )
    parser.add_argument(
        '--use-api',
        action='store_true',
        help="Use fast download API (requires ANNAS_SECRET_KEY, quota limited)"
    )
    
    args = parser.parse_args()
    
    # Determine what to do
    if args.prepare_only:
        success = run_prepare()
        return 0 if success else 1
    elif args.download_only:
        success = run_download(
            use_no_quota=not args.use_api,
            max_workers=args.max_workers,
            delay=args.delay,
            single_mode=args.single_mode
        )
        return 0 if success else 1
    elif args.prepare_and_download:
        if not run_prepare():
            return 1
        print("\n" + "=" * 70)
        print("Review the download list above, then continuing with downloads...")
        print("=" * 70 + "\n")
        success = run_download(
            use_no_quota=not args.use_api,
            max_workers=args.max_workers,
            delay=args.delay,
            single_mode=args.single_mode
        )
        return 0 if success else 1
    else:
        parser.print_help()
        print("\n❌ Error: Must specify one of --prepare-only, --download-only, or --prepare-and-download")
        return 1


if __name__ == "__main__":
    sys.exit(main())
