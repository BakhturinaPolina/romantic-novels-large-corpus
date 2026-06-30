"""Stage 08A: run LLM quality adjudication on Stage07 soft-review topics."""

from __future__ import annotations

import argparse
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

from src.common.config import load_config, resolve_path
from src.stage08_llm_labeling.openrouter_experiments.core.generate_labels_openrouter import (
    DEFAULT_OPENROUTER_API_KEY,
    DEFAULT_RATE_LIMIT_DELAY_S,
    load_openrouter_client,
)
from src.stage08_llm_labeling.openrouter_experiments.core.structured_json_call import (
    chat_completions_json_schema,
)
from src.stage08_llm_labeling.prompts.adjudication.stage08a_quality_adjudication import (
    QUALITY_ADJUDICATION_SCHEMA,
    SYSTEM_PROMPT,
    format_user_prompt,
)

LOGGER = logging.getLogger("stage08a.quality_adjudication")
DEFAULT_CONFIG = Path("configs/stage08a_quality_adjudication.yaml")


def load_review_packets(path: Path) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            packets.append(json.loads(line))
    return packets


def load_existing_results(path: Path) -> dict[int, dict[str, Any]]:
    if not path.is_file():
        return {}
    done: dict[int, dict[str, Any]] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            done[int(row["topic_id"])] = row
    return done


def append_result(path: Path, row: dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_adjudication(
    *,
    config_path: Path | None = None,
    api_key: str | None = None,
    limit: int | None = None,
) -> Path:
    cfg = load_config(resolve_path(config_path or DEFAULT_CONFIG))
    paths = cfg.get("paths", {})
    openrouter_cfg = cfg.get("openrouter", {})
    adjudication_cfg = cfg.get("adjudication", {})

    packet_path = resolve_path(Path(paths["manual_review_packet"]))
    out_dir = resolve_path(Path(paths["output_dir"]))
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "adjudication_results.jsonl"

    packets = load_review_packets(packet_path)
    if adjudication_cfg.get("only_soft_review", True):
        packets = [
            p
            for p in packets
            if p.get("soft_review_candidate")
            and not p.get("hard_exclude_candidate")
        ]
    if limit is not None:
        packets = packets[:limit]

    existing = load_existing_results(output_path) if adjudication_cfg.get("resume", True) else {}
    pending = [p for p in packets if int(p["topic_id"]) not in existing]
    prompt_version = adjudication_cfg.get("prompt_version", "v1")
    LOGGER.info(
        "Adjudication: %d packets, %d pending, %d already done (prompt=%s)",
        len(packets),
        len(pending),
        len(existing),
        prompt_version,
    )

    key = api_key or os.environ.get("OPENROUTER_API_KEY") or DEFAULT_OPENROUTER_API_KEY
    client, model_name = load_openrouter_client(
        api_key=key,
        model_name=str(openrouter_cfg.get("model", "anthropic/claude-sonnet-4.6")),
    )
    delay = float(openrouter_cfg.get("rate_limit_delay_s", DEFAULT_RATE_LIMIT_DELAY_S))
    max_tokens = int(openrouter_cfg.get("max_tokens", 400))
    temperature = float(openrouter_cfg.get("temperature", 0.0))

    for i, packet in enumerate(pending, 1):
        topic_id = int(packet["topic_id"])
        user_prompt = format_user_prompt(packet)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        result = chat_completions_json_schema(
            client,
            model=model_name,
            messages=messages,
            schema=QUALITY_ADJUDICATION_SCHEMA,
            schema_name="stage08a_quality_adjudication",
            max_tokens=max_tokens,
            temperature=temperature,
        )
        result["topic_id"] = topic_id
        result["prompt_version"] = prompt_version
        append_result(output_path, result)
        LOGGER.info(
            "[%d/%d] topic %d -> %s (%s)",
            i,
            len(pending),
            topic_id,
            result.get("llm_quality_decision"),
            result.get("content_status"),
        )
        if i < len(pending):
            time.sleep(delay)

    return output_path


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(description="Stage 08A quality adjudication")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--api-key", type=str, default=None)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    out = run_adjudication(
        config_path=args.config,
        api_key=args.api_key,
        limit=args.limit,
    )
    print(f"Wrote adjudication results to {out}")


if __name__ == "__main__":
    main()
