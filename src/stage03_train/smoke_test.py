"""Small Stage03 smoke test on train/eval loaders and OCTIS writer."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.common.config import load_config, resolve_path
from src.stage03_train.data_io import load_train_eval
from src.stage03_train.octis_corpus import write_octis_corpus


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/train.yaml")
    parser.add_argument("--max-docs", type=int, default=10000)
    parser.add_argument("--run-id", default="smoke_test")
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    paths_cfg = load_config(Path("configs/paths.yaml"))
    inputs = paths_cfg["inputs"]
    train_csv = resolve_path(Path(inputs["sentences_train_csv"]))
    eval_csv = resolve_path(Path(inputs["sentences_val_csv"]))

    payload = load_train_eval(train_csv, eval_csv, sentence_column=cfg["text"]["sentence_column"])
    docs_train = payload["docs_train"][: args.max_docs]
    labels_train = payload["labels_train"][: args.max_docs]
    docs_eval = payload["docs_eval"][: args.max_docs]
    labels_eval = payload["labels_eval"][: args.max_docs]

    octis_dir = resolve_path(Path(inputs.get("octis_dataset", "data/interim/octis"))) / args.run_id
    corpus_path = write_octis_corpus(docs_train, labels_train, docs_eval, labels_eval, octis_dir)
    print(f"Smoke test ok. corpus.tsv: {corpus_path}")
    print(f"train_docs={len(docs_train)} eval_docs={len(docs_eval)}")


if __name__ == "__main__":
    main()

