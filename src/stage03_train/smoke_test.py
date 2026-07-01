"""Small Stage03 smoke test on train/eval loaders and OCTIS writer."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.common.config import load_config, resolve_path
from src.stage03_train.data_io import count_split_rows, load_train_eval_in_memory
from src.stage03_train.octis_corpus import write_octis_corpus, write_octis_corpus_from_csvs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/stage03/train_smoke.yaml")
    parser.add_argument("--max-docs", type=int, default=10000)
    parser.add_argument("--run-id", default="smoke_test")
    parser.add_argument(
        "--chunked",
        action="store_true",
        help="Use streaming CSV corpus writer (same path as full tune).",
    )
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    paths_cfg = load_config(Path("configs/paths.yaml"))
    inputs = paths_cfg["inputs"]
    train_csv = resolve_path(Path(inputs["sentences_train_csv"]))
    eval_csv = resolve_path(Path(inputs["sentences_val_csv"]))
    sentence_column = cfg["text"]["sentence_column"]
    chunk_size = int(cfg["text"].get("csv_chunk_size", 50_000))

    octis_dir = resolve_path(Path(inputs.get("octis_dataset", "data/interim/octis"))) / args.run_id

    if args.chunked:
        n_train = count_split_rows(train_csv, sentence_column=sentence_column)
        n_eval = count_split_rows(eval_csv, sentence_column=sentence_column)
        print(f"Row counts: train={n_train} eval={n_eval}")
        corpus_path, _, w_train, w_val = write_octis_corpus_from_csvs(
            train_csv,
            eval_csv,
            octis_dir,
            sentence_column=sentence_column,
            chunk_size=chunk_size,
        )
        print(f"Chunked smoke test ok. corpus.tsv: {corpus_path}")
        print(f"written train={w_train} val={w_val}")
        return

    payload = load_train_eval_in_memory(
        train_csv, eval_csv, sentence_column=sentence_column
    )
    docs_train = payload["docs_train"][: args.max_docs]
    labels_train = payload["labels_train"][: args.max_docs]
    docs_eval = payload["docs_eval"][: args.max_docs]
    labels_eval = payload["labels_eval"][: args.max_docs]

    corpus_path = write_octis_corpus(docs_train, labels_train, docs_eval, labels_eval, octis_dir)
    print(f"Smoke test ok. corpus.tsv: {corpus_path}")
    print(f"train_docs={len(docs_train)} eval_docs={len(docs_eval)}")


if __name__ == "__main__":
    main()
