"""Quantitative-to-qualitative bridge: targeted close reading.

The problem with reading examples from a 16,000-book corpus is that whatever you read will
confirm whatever you expected. This module removes the choice from the reader: the
quantitative result names the cells (high/low index x high/low tier), a fixed seed names the
books, and the topic model names the sentences. What is left to interpret is genuinely a
sample rather than a selection.

Pulling sentences straight from the 255 GB sentence parquet files via DuckDB means the
close-reading text is the exact text the model scored, not a re-derived approximation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

import numpy as np
import pandas as pd


def sample_extreme_books(
    frame: pd.DataFrame,
    index_column: str,
    tier_column: str,
    *,
    tier_high: str,
    tier_low: str,
    quantiles: Sequence[float] = (0.1, 0.9),
    books_per_cell: int = 5,
    seed: int = 42,
    extra_columns: Sequence[str] = (),
) -> pd.DataFrame:
    """2x2 sampling design: index extreme x rating tier.

    The off-diagonal cells are the interesting ones. A high-index book that is *poorly*
    rated shows what the index measures when it fails, which is far more informative about
    construct validity than another confirming example from the main diagonal.
    """
    valid = frame[[index_column, tier_column, *extra_columns]].dropna(subset=[index_column, tier_column])
    low_cut, high_cut = valid[index_column].quantile(list(quantiles))

    cells = {
        "high_index_high_tier": (valid[index_column] >= high_cut) & (valid[tier_column] == tier_high),
        "high_index_low_tier": (valid[index_column] >= high_cut) & (valid[tier_column] == tier_low),
        "low_index_high_tier": (valid[index_column] <= low_cut) & (valid[tier_column] == tier_high),
        "low_index_low_tier": (valid[index_column] <= low_cut) & (valid[tier_column] == tier_low),
    }

    rng = np.random.default_rng(seed)
    picks: List[pd.DataFrame] = []
    for cell, mask in cells.items():
        candidates = valid.loc[mask]
        if candidates.empty:
            continue
        take = min(books_per_cell, len(candidates))
        chosen = candidates.iloc[rng.choice(len(candidates), take, replace=False)].copy()
        chosen.insert(0, "cell", cell)
        picks.append(chosen)

    if not picks:
        return pd.DataFrame(columns=["cell", "book_id", index_column, tier_column])

    out = pd.concat(picks).reset_index().rename(columns={"index": "book_id"})
    out.attrs["low_cut"] = float(low_cut)
    out.attrs["high_cut"] = float(high_cut)
    return out


def top_loading_topics(
    book_topic_counts: pd.DataFrame,
    book_ids: Iterable[int],
    topic_lookup: pd.DataFrame,
    *,
    top_n: int = 8,
    restrict_to_topics: Optional[Sequence[int]] = None,
) -> pd.DataFrame:
    """The topics that dominate each sampled book, with their labels attached."""
    subset = book_topic_counts[book_topic_counts["book_id"].isin(list(book_ids))].copy()
    if restrict_to_topics is not None:
        subset = subset[subset["topic_id"].isin(list(restrict_to_topics))]

    subset = subset.sort_values(["book_id", "share"], ascending=[True, False])
    subset["rank_in_book"] = subset.groupby("book_id").cumcount() + 1
    subset = subset[subset["rank_in_book"] <= top_n]

    label_cols = [c for c in ["topic_id", "label", "taxonomy_main_id", "taxonomy_main_name"]
                  if c in topic_lookup.columns]
    return subset.merge(topic_lookup[label_cols], on="topic_id", how="left")


def fetch_sentences(
    sentence_files: Sequence[Path],
    book_ids: Sequence[int],
    topic_ids: Optional[Sequence[int]] = None,
    *,
    per_book_topic: int = 5,
    threads: int = 4,
    order_by_confidence: bool = True,
) -> pd.DataFrame:
    """Pull representative sentences for specific books and topics.

    Filtering on `work_id` first lets DuckDB skip almost every parquet row group, so this
    reads a few hundred MB rather than 255 GB. Ordering by `max_topic_prob` returns the
    sentences the model was most confident about, which are the clearest illustrations of
    what a topic actually contains.
    """
    import duckdb

    if not book_ids:
        return pd.DataFrame()

    con = duckdb.connect()
    con.execute(f"pragma threads={threads}")
    files = ", ".join(f"'{f}'" for f in sentence_files)
    book_list = ", ".join(str(int(b)) for b in book_ids)
    topic_filter = (
        f"and topic in ({', '.join(str(int(t)) for t in topic_ids)})" if topic_ids else ""
    )
    order = "max_topic_prob desc" if order_by_confidence else "random()"

    query = f"""
        with hits as (
            select
                work_id as book_id,
                chapter_index,
                sentence_index,
                sentence,
                topic as topic_id,
                max_topic_prob,
                row_number() over (
                    partition by work_id, topic order by {order}
                ) as rank_in_topic
            from read_parquet([{files}])
            where work_id in ({book_list}) {topic_filter}
        )
        select * from hits
        where rank_in_topic <= {int(per_book_topic)}
        order by book_id, topic_id, rank_in_topic
    """
    result = con.execute(query).df()
    con.close()
    return result


def build_close_reading_pack(
    sampled_books: pd.DataFrame,
    top_topics: pd.DataFrame,
    sentences: pd.DataFrame,
    books_meta: pd.DataFrame,
) -> pd.DataFrame:
    """Assemble one readable table: cell, book, topic, label, and the sentences."""
    meta_cols = [c for c in ["book_id", "title", "author_name", "average_rating_weighted_mean",
                             "ratings_count_sum", "genre_group", "publication_year"]
                 if c in books_meta.columns]

    pack = (
        sentences
        .merge(top_topics.drop(columns=["n_sentences"], errors="ignore"),
               on=["book_id", "topic_id"], how="inner")
        .merge(sampled_books[["cell", "book_id"]], on="book_id", how="left")
        .merge(books_meta[meta_cols], on="book_id", how="left")
    )
    ordered = [c for c in [
        "cell", "book_id", "title", "author_name", "average_rating_weighted_mean",
        "ratings_count_sum", "topic_id", "label", "taxonomy_main_id", "taxonomy_main_name",
        "share", "rank_in_book", "rank_in_topic", "max_topic_prob", "sentence",
    ] if c in pack.columns]
    return pack[ordered].sort_values(
        ["cell", "book_id", "rank_in_book", "rank_in_topic"]
    ).reset_index(drop=True)


def render_close_reading_markdown(pack: pd.DataFrame, max_sentences_per_topic: int = 3) -> str:
    """Format a close-reading pack as markdown for the notebook and the write-up."""
    lines: List[str] = []
    for cell, cell_rows in pack.groupby("cell", sort=False):
        lines += [f"## {cell.replace('_', ' ')}", ""]
        for book_id, book_rows in cell_rows.groupby("book_id", sort=False):
            first = book_rows.iloc[0]
            title = first.get("title", "(untitled)")
            author = first.get("author_name", "(unknown)")
            rating = first.get("average_rating_weighted_mean", float("nan"))
            n_ratings = first.get("ratings_count_sum", float("nan"))
            lines.append(
                f"**{title}** — {author} "
                f"(rating {rating:.2f}, {int(n_ratings):,} ratings, book_id {book_id})"
            )
            lines.append("")
            for (topic_id, label), topic_rows in book_rows.groupby(
                ["topic_id", "label"], sort=False
            ):
                share = float(topic_rows["share"].iloc[0])
                lines.append(f"- *Topic {topic_id} — {label}* ({share:.1%} of sentences)")
                for _, row in topic_rows.head(max_sentences_per_topic).iterrows():
                    text = str(row["sentence"]).strip().replace("\n", " ")
                    lines.append(f"    > {text}")
                lines.append("")
        lines.append("")
    return "\n".join(lines)


def contrast_summary(
    sampled_books: pd.DataFrame,
    index_column: str,
) -> pd.DataFrame:
    """Cell means, so the reader knows how the sampled books differ before reading them."""
    return sampled_books.groupby("cell").agg(
        n_books=("book_id", "size"),
        mean_index=(index_column, "mean"),
        min_index=(index_column, "min"),
        max_index=(index_column, "max"),
    ).reset_index()
