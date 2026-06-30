"""Shared OpenRouter chat completion helper with JSON-schema structured output."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

LOGGER = logging.getLogger(__name__)


def parse_json_object_content(content: str) -> dict[str, Any]:
    """Extract a JSON object from model text (handles optional fences)."""
    text = (content or "").strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    if not text.startswith("{"):
        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last > first:
            text = text[first : last + 1]
    return json.loads(text)


def chat_completions_json_schema(
    client: Any,
    *,
    model: str,
    messages: list[dict[str, str]],
    schema: dict[str, Any],
    schema_name: str = "structured_output",
    max_tokens: int = 700,
    temperature: float = 0.0,
    validate_fn: Any | None = None,
) -> dict[str, Any]:
    """
    Call OpenRouter/OpenAI chat completions with strict JSON schema when supported.

    Falls back to json_object mode and optional validate_fn retry.
    """
    strict_kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": True,
                "schema": schema,
            },
        },
    }

    def _call(kwargs: dict[str, Any]) -> str:
        response = client.chat.completions.create(**kwargs)
        if not response.choices:
            raise ValueError("Empty API response")
        return response.choices[0].message.content.strip()

    content: str | None = None
    try:
        content = _call(strict_kwargs)
    except Exception as exc:
        err = str(exc).lower()
        if "response_format" in err or "json_schema" in err or "structured" in err:
            LOGGER.debug("Strict json_schema unsupported, falling back to json_object: %s", exc)
            loose = dict(strict_kwargs)
            loose.pop("response_format", None)
            loose["response_format"] = {"type": "json_object"}
            try:
                content = _call(loose)
            except Exception:
                loose.pop("response_format", None)
                content = _call(loose)
        else:
            raise

    assert content is not None
    parsed = parse_json_object_content(content)

    if validate_fn is not None:
        errors = validate_fn(parsed)
        if errors:
            LOGGER.warning("JSON schema validation failed, retrying once: %s", errors[0][:120])
            retry_kwargs = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.0,
                "response_format": {"type": "json_object"},
            }
            content = _call(retry_kwargs)
            parsed = parse_json_object_content(content)
            errors = validate_fn(parsed)
            if errors:
                raise ValueError(f"JSON schema validation failed after retry: {errors[0]}")

    return parsed
