"""Parse v2 romance EPUB corpus into train/val/test sentence CSVs.

Reads subsampling split CSVs (work_id, md5, split_v2, ...), resolves EPUB paths under
``{corpus_root}/{split_v2}/{md5}.epub``, walks each book's spine in order, extracts
plain text per XHTML chapter, splits sentences with spaCy, and writes one CSV per split.

Join sentence rows to full metadata via ``work_id`` on the mirrored subsampling tables.

Resume: without ``--overwrite``, each split uses ``sentences_<split>.ckpt`` (one ``work_id``
per line, fsynced after each fully written work). Interrupted runs drop any trailing
partial work (rows for ``work_id`` not yet listed in the checkpoint) and continue.
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Iterator, List, Optional, Set, TextIO, Tuple

from bs4 import BeautifulSoup
from ebooklib import epub, ITEM_DOCUMENT
import pandas as pd
import spacy
from tqdm import tqdm

from .epub_zip_fallback import iter_spine_html_raw

LOG = logging.getLogger(__name__)

SPLIT_NAMES = ("train", "val", "test")
METADATA_GLOB = "romance_subdataset_downloaded_v2_{split}.csv"
OUTPUT_SENTENCES = "sentences_{split}.csv"
OUTPUT_CHECKPOINT = "sentences_{split}.ckpt"
OUTPUT_ERRORS = "parse_errors.csv"

SENTENCE_FIELDNAMES = ["work_id", "chapter_index", "chapter_title", "sentence_index", "sentence"]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _spine_idref(entry: Any) -> str:
    if isinstance(entry, (list, tuple)):
        return str(entry[0])
    return str(entry)


def _chapter_title_from_soup(soup: BeautifulSoup) -> str:
    for tag in ("h1", "h2", "h3"):
        el = soup.find(tag)
        if el is not None:
            t = el.get_text(strip=True)
            if t:
                return t
    return ""


def _html_body_to_plain(html_bytes: bytes) -> Tuple[str, str]:
    soup = BeautifulSoup(html_bytes, "html.parser")
    title = _chapter_title_from_soup(soup)
    for bad in soup(["script", "style", "noscript"]):
        bad.decompose()
    body = soup.find("body")
    root = body if body is not None else soup
    text = root.get_text(separator=" ", strip=True)
    text = " ".join(text.split())
    return text, title


def load_nlp(model_name: str):
    """Load spaCy for sentence boundaries only (heavy components disabled for speed)."""
    try:
        nlp = spacy.load(
            model_name,
            disable=["tok2vec", "tagger", "parser", "ner", "lemmatizer", "attribute_ruler"],
        )
    except OSError:
        LOG.error("spaCy model %r not found. Install with: python -m spacy download %s", model_name, model_name)
        raise
    if "sentencizer" not in nlp.pipe_names:
        # ``tokenizer`` is not a registered pipe name in spaCy 3.x; ``first=True`` runs after tokenization.
        nlp.add_pipe("sentencizer", first=True)
    # Default cap is 1_000_000 chars; long spine XHTML can exceed that. Parser/NER are disabled above.
    nlp.max_length = 10_000_000
    return nlp


def _resolve_spine_item(book: epub.EpubBook, idref: str) -> Optional[epub.EpubItem]:
    item = book.get_item_with_id(idref)
    if item is not None:
        return item
    return book.get_item_with_href(idref)


def iter_spine_chapters(book: epub.EpubBook) -> Iterator[Tuple[epub.EpubItem, int]]:
    """Yield (item, spine_position) for spine entries that resolve to ITEM_DOCUMENT."""
    for spine_pos, spine_entry in enumerate(book.spine):
        idref = _spine_idref(spine_entry)
        item = _resolve_spine_item(book, idref)
        if item is None:
            continue
        if item.get_type() != ITEM_DOCUMENT:
            continue
        yield item, spine_pos


def _extract_sentences_zip_fallback(
    epub_path: Path,
    nlp: spacy.Language,
) -> Tuple[List[dict], Optional[str]]:
    """Spine-ordered HTML via ZIP/OPF (case-insensitive member names)."""
    chapters, zerr = iter_spine_html_raw(epub_path)
    if zerr:
        return [], f"zip_fallback_failed: {zerr}"

    rows: List[dict] = []
    chapter_index = 0
    for _logical, raw in chapters:
        plain, title = _html_body_to_plain(raw)
        if not plain.strip():
            continue
        doc = nlp(plain)
        sent_list = [s.text.strip() for s in doc.sents if s.text.strip()]
        if not sent_list:
            chapter_index += 1
            continue
        for sentence_index, sentence in enumerate(sent_list):
            rows.append(
                {
                    "chapter_index": chapter_index,
                    "chapter_title": title,
                    "sentence_index": sentence_index,
                    "sentence": sentence,
                }
            )
        chapter_index += 1

    if not rows:
        return [], "zip_fallback_no_sentences"
    return rows, None


def extract_sentences_for_epub(
    epub_path: Path,
    nlp: spacy.Language,
    use_zip_fallback: bool = False,
) -> Tuple[List[dict], Optional[str]]:
    """
    Returns (rows, error_message).
    Each row: chapter_index, chapter_title, sentence_index, sentence (no work_id).
    chapter_index is contiguous among spine XHTML documents that produced non-empty text.
    """
    try:
        book = epub.read_epub(str(epub_path))
    except Exception as e:
        if use_zip_fallback:
            return _extract_sentences_zip_fallback(epub_path, nlp)
        return [], f"read_epub_failed: {e}"

    rows: List[dict] = []
    chapter_index = 0

    for item, _spine_pos in iter_spine_chapters(book):
        try:
            raw = item.get_body_content()
        except Exception as e:
            return rows, f"get_body_content_failed: {e}"
        if not raw:
            continue
        plain, title = _html_body_to_plain(raw if isinstance(raw, bytes) else bytes(raw, "utf-8", errors="replace"))
        if not plain.strip():
            continue

        doc = nlp(plain)
        sent_list = [s.text.strip() for s in doc.sents if s.text.strip()]
        if not sent_list:
            chapter_index += 1
            continue

        for sentence_index, sentence in enumerate(sent_list):
            rows.append(
                {
                    "chapter_index": chapter_index,
                    "chapter_title": title,
                    "sentence_index": sentence_index,
                    "sentence": sentence,
                }
            )
        chapter_index += 1

    if not rows:
        if use_zip_fallback:
            return _extract_sentences_zip_fallback(epub_path, nlp)
        return [], "no_sentences_extracted"
    return rows, None


def default_paths(project_root: Path) -> Tuple[Path, Path, Path]:
    corpus = project_root / "data/raw/romance_subdataset_downloaded_v2_full"
    meta = corpus / "subsampling_metadata"
    out = project_root / "data/processed/romance_subdataset_downloaded_v2_sentences"
    return corpus, meta, out


def _load_checkpoint_ids(ckpt_path: Path) -> Set[int]:
    if not ckpt_path.is_file():
        return set()
    out: Set[int] = set()
    with open(ckpt_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.add(int(line))
            except ValueError:
                LOG.warning("Skipping bad checkpoint line in %s: %r", ckpt_path, line[:80])
    return out


def _append_checkpoint(ckpt_path: Path, work_id: int) -> None:
    with open(ckpt_path, "a", encoding="utf-8") as ckf:
        ckf.write(f"{work_id}\n")
        ckf.flush()
        os.fsync(ckf.fileno())


def _write_checkpoint_ids(ckpt_path: Path, work_ids: Set[int]) -> None:
    ckpt_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ckpt_path, "w", encoding="utf-8") as ckf:
        for wid in sorted(work_ids):
            ckf.write(f"{wid}\n")
        ckf.flush()
        os.fsync(ckf.fileno())


def _infer_completed_from_csv(sentences_out: Path) -> Set[int]:
    """Unique work_id values in an existing sentence CSV (migration / legacy runs)."""
    found: Set[int] = set()
    with open(sentences_out, newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            try:
                found.add(int(row["work_id"]))
            except (KeyError, ValueError):
                continue
    return found


def _last_work_id_in_csv(sentences_out: Path) -> Optional[int]:
    """work_id on the last data row (append order), or None if empty."""
    last: Optional[int] = None
    with open(sentences_out, newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            try:
                last = int(row["work_id"])
            except (KeyError, ValueError):
                continue
    return last


def _filter_sentences_csv(sentences_out: Path, keep_work_ids: Set[int]) -> int:
    """Rewrite CSV keeping only rows whose work_id is in keep_work_ids. Returns rows kept."""
    if not sentences_out.is_file():
        return 0
    kept = 0
    fd, tmp = tempfile.mkstemp(prefix=".sentences_", suffix=".csv.tmp", dir=str(sentences_out.parent))
    os.close(fd)
    tmp_path = Path(tmp)
    try:
        with open(sentences_out, newline="", encoding="utf-8") as inp, open(
            tmp_path, "w", newline="", encoding="utf-8"
        ) as outp:
            reader = csv.DictReader(inp)
            writer = csv.DictWriter(outp, fieldnames=SENTENCE_FIELDNAMES, extrasaction="ignore")
            writer.writeheader()
            for row in reader:
                try:
                    wid = int(row["work_id"])
                except (KeyError, ValueError):
                    continue
                if wid not in keep_work_ids:
                    continue
                writer.writerow({k: row.get(k, "") for k in SENTENCE_FIELDNAMES})
                kept += 1
        os.replace(tmp_path, sentences_out)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise
    return kept


def reconcile_resume_state(sentences_out: Path, ckpt_path: Path) -> Set[int]:
    """
    Prepare sentence CSV + checkpoint for a resumed run.

    - If sentence CSV is missing, drop any orphan checkpoint.
    - If a non-empty checkpoint exists: drop sentence rows whose ``work_id`` is not
      listed in the checkpoint (removes the last interrupted, partially written book).
    - If the checkpoint is missing or empty but the CSV exists: infer completed
      ``work_id`` values from the CSV and write a new checkpoint (migration from older
      runs without ``.ckpt``). This assumes each ``work_id`` in the file was finished;
      if that is not true, use ``--overwrite``.
    """
    if not sentences_out.is_file():
        if ckpt_path.exists():
            ckpt_path.unlink()
            LOG.info("Removed orphan checkpoint (no sentence CSV): %s", ckpt_path)
        return set()

    ck_nonempty = ckpt_path.is_file() and ckpt_path.stat().st_size > 0
    if not ck_nonempty:
        if ckpt_path.exists():
            ckpt_path.unlink()
        completed = _infer_completed_from_csv(sentences_out)
        last_w = _last_work_id_in_csv(sentences_out)
        if last_w is not None and len(completed) > 1 and last_w in completed:
            completed.discard(last_w)
            LOG.info(
                "No .ckpt yet: assuming trailing work_id %s was incomplete; "
                "it will be re-parsed (legacy CSV migration).",
                last_w,
            )
        _write_checkpoint_ids(ckpt_path, completed)
        kept = _filter_sentences_csv(sentences_out, completed)
        LOG.info(
            "Initialized checkpoint from %s (%s completed work_ids, %s sentence rows kept).",
            sentences_out.name,
            len(completed),
            kept,
        )
        return completed

    completed = _load_checkpoint_ids(ckpt_path)
    kept = _filter_sentences_csv(sentences_out, completed)
    LOG.info(
        "Resume %s: %s completed work_ids, %s sentence rows retained after repair",
        sentences_out.name,
        len(completed),
        kept,
    )
    return completed


def process_split(
    split: str,
    metadata_dir: Path,
    corpus_root: Path,
    sentences_out: Path,
    ckpt_path: Path,
    errors_writer: csv.DictWriter,
    errors_fp: TextIO,
    nlp: spacy.Language,
    limit: Optional[int] = None,
    use_zip_fallback: bool = False,
) -> int:
    meta_path = metadata_dir / METADATA_GLOB.format(split=split)
    if not meta_path.exists():
        LOG.warning("Missing metadata file: %s", meta_path)
        return 0

    LOG.info("Reading metadata: %s", meta_path)
    df = pd.read_csv(meta_path)
    if "split_v2" in df.columns:
        df = df[df["split_v2"].astype(str) == split]
    if limit is not None:
        df = df.head(limit)
    LOG.info("Metadata rows for split=%s: %s", split, len(df))

    LOG.info("Reconciling resume state (may read large CSV): %s", sentences_out.name)
    completed = reconcile_resume_state(sentences_out, ckpt_path)
    LOG.info("Split=%s: %s works already complete, %s remaining", split, len(completed), len(df) - len(completed))

    work_ids_series = df["work_id"].astype(int)
    pending = df[~work_ids_series.isin(completed)]
    if pending.empty:
        LOG.info("Split=%s: nothing to do (all works in checkpoint).", split)
        return 0

    n_written = 0
    file_exists = sentences_out.exists() and sentences_out.stat().st_size > 0
    with open(sentences_out, "a", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=SENTENCE_FIELDNAMES)
        if not file_exists:
            writer.writeheader()

        bar = tqdm(
            pending.iterrows(),
            total=len(pending),
            desc=f"split={split}",
            unit="work",
            file=sys.stdout,
            dynamic_ncols=True,
        )
        for _, row in bar:
            work_id = int(row["work_id"])

            md5 = str(row["md5"]).strip().lower()
            split_v2 = str(row.get("split_v2", split)).strip().lower()
            epub_path = corpus_root / split_v2 / f"{md5}.epub"

            if not epub_path.is_file():
                errors_writer.writerow(
                    {
                        "work_id": work_id,
                        "md5": md5,
                        "epub_path": str(epub_path),
                        "error": "epub_missing_on_disk",
                    }
                )
                errors_fp.flush()
                continue

            chapter_rows, err = extract_sentences_for_epub(epub_path, nlp, use_zip_fallback=use_zip_fallback)
            if err:
                errors_writer.writerow(
                    {
                        "work_id": work_id,
                        "md5": md5,
                        "epub_path": str(epub_path),
                        "error": err,
                    }
                )
                errors_fp.flush()
                continue

            for cr in chapter_rows:
                writer.writerow(
                    {
                        "work_id": work_id,
                        "chapter_index": cr["chapter_index"],
                        "chapter_title": cr["chapter_title"],
                        "sentence_index": cr["sentence_index"],
                        "sentence": cr["sentence"],
                    }
                )
                n_written += 1

            fp.flush()
            os.fsync(fp.fileno())
            _append_checkpoint(ckpt_path, work_id)
            completed.add(work_id)
            bar.set_postfix_str(f"work_id={work_id}", refresh=False)

    return n_written


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    root = _project_root()
    corpus_def, meta_def, out_def = default_paths(root)
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus-root", type=Path, default=corpus_def, help="v2 folder with train/val/test subdirs")
    p.add_argument("--metadata-dir", type=Path, default=meta_def, help="subsampling_metadata directory")
    p.add_argument("--output-dir", type=Path, default=out_def, help="output directory for CSVs")
    p.add_argument("--spacy-model", type=str, default="en_core_web_sm", help="spaCy model name")
    p.add_argument("--workers", type=int, default=1, help="reserved for future parallel runs (only 1 supported)")
    p.add_argument("--limit", type=int, default=None, help="max works per split (debug)")
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="delete existing sentence CSVs, per-split .ckpt checkpoints, and parse_errors.csv before running",
    )
    p.add_argument(
        "--use-zip-fallback",
        action="store_true",
        help="if ebooklib fails or yields no sentences, retry via ZIP+OPF spine HTML (case-insensitive paths)",
    )
    return p.parse_args(list(argv) if argv is not None else None)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if args.workers != 1:
        LOG.warning("--workers=%s ignored; only single-process mode is implemented.", args.workers)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.overwrite:
        for split in SPLIT_NAMES:
            p = args.output_dir / OUTPUT_SENTENCES.format(split=split)
            if p.exists():
                p.unlink()
            ck = args.output_dir / OUTPUT_CHECKPOINT.format(split=split)
            if ck.exists():
                ck.unlink()
        err_path = args.output_dir / OUTPUT_ERRORS
        if err_path.exists():
            err_path.unlink()

    LOG.info("Loading spaCy model %r (can take a while on first run)...", args.spacy_model)
    nlp = load_nlp(args.spacy_model)
    LOG.info("spaCy model ready.")

    err_path = args.output_dir / OUTPUT_ERRORS
    err_new = not err_path.exists()
    total_rows = 0
    with open(err_path, "a", newline="", encoding="utf-8") as efp:
        err_fields = ["work_id", "md5", "epub_path", "error"]
        err_writer = csv.DictWriter(efp, fieldnames=err_fields)
        if err_new:
            err_writer.writeheader()

        for split in SPLIT_NAMES:
            out_csv = args.output_dir / OUTPUT_SENTENCES.format(split=split)
            ckpt = args.output_dir / OUTPUT_CHECKPOINT.format(split=split)
            n = process_split(
                split=split,
                metadata_dir=args.metadata_dir,
                corpus_root=args.corpus_root,
                sentences_out=out_csv,
                ckpt_path=ckpt,
                errors_writer=err_writer,
                errors_fp=efp,
                nlp=nlp,
                limit=args.limit,
                use_zip_fallback=args.use_zip_fallback,
            )
            total_rows += n
            LOG.info("Wrote %s sentence rows -> %s", n, out_csv)
            efp.flush()

    LOG.info("Done. Total sentence rows: %s", total_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
