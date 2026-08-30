"""Shared OpenRouter client + JSON helpers for Stage 11 audits."""

from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Any, Dict, Mapping, Optional, Sequence

LOGGER = logging.getLogger("stage11.llm")

CODE_RE = re.compile(r"\b(I\d+|H2_\d+|S\d+|H4_\d+|D\d+|ARC_\d+|MIXED)\b")


def extract_json(text: str) -> Dict[str, Any]:
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return {"raw": text, "parse_error": True}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"raw": text, "parse_error": True}


def consensus_code(payload: Mapping[str, Any], valid_codes: Sequence[str]) -> str:
    for key in (
        "consensus_code",
        "dominant_code",
        "intimacy_code",
        "hea_code",
        "security_code",
        "care_protection_code",
        "darkness_code",
        "arc_role",
        "include",
        "promoted_code",
    ):
        val = payload.get(key)
        if isinstance(val, str) and val:
            if key == "include":
                continue
            return val
    blob = json.dumps(payload)
    valid = set(valid_codes) | {"MIXED"}
    hits = [m for m in CODE_RE.findall(blob) if m in valid]
    return hits[0] if hits else "UNKNOWN"


def call_openrouter(
    *,
    model: str,
    system: str,
    user: str,
    temperature: float,
    max_tokens: int,
    api_key: str,
    base_url: str = "https://openrouter.ai/api/v1",
    max_retries: int = 10,
    retry_backoff_s: float = 5.0,
    request_timeout_s: float = 180.0,
) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=float(request_timeout_s))
    last_err: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            if not resp.choices:
                # OpenRouter occasionally returns 200 with empty choices under load/moderation.
                detail = ""
                if hasattr(resp, "model_dump"):
                    detail = str(resp.model_dump())[:500]
                raise RuntimeError(f"OpenRouter empty choices (attempt {attempt}): {detail}")
            content = resp.choices[0].message.content
            if content is None:
                raise RuntimeError(f"OpenRouter null message content (attempt {attempt})")
            return content
        except Exception as exc:
            last_err = exc
            # Cap backoff; provider 504s often clear after a longer pause.
            wait = min(120.0, float(retry_backoff_s) * (2 ** (attempt - 1)))
            LOGGER.warning(
                "OpenRouter call failed attempt %d/%d: %s; sleeping %.1fs",
                attempt,
                max_retries,
                exc,
                wait,
            )
            time.sleep(wait)
    raise RuntimeError(f"OpenRouter failed after {max_retries} attempts: {last_err}")


def resolve_api_key(explicit: Optional[str] = None) -> str:
    return (explicit or os.environ.get("OPENROUTER_API_KEY", "") or "").strip()


def load_dotenv_key(env_path: Optional[str] = None) -> str:
    """Load OPENROUTER_API_KEY from a .env file if not already in the environment."""
    existing = resolve_api_key()
    if existing:
        return existing
    candidates = []
    if env_path:
        candidates.append(env_path)
    candidates.append(os.path.join(os.getcwd(), ".env"))
    # Walk up a few levels for pipeline scripts started from repo root or elsewhere.
    here = os.path.abspath(os.getcwd())
    for _ in range(4):
        candidates.append(os.path.join(here, ".env"))
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    for path in candidates:
        if not os.path.isfile(path):
            continue
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            if key.strip() == "OPENROUTER_API_KEY":
                val = val.strip().strip("'").strip('"')
                if val:
                    os.environ["OPENROUTER_API_KEY"] = val
                    return val
    return ""


def chat_json(
    *,
    model: str,
    system: str,
    user: str,
    temperature: float,
    max_tokens: int,
    api_key: str,
    rate_limit_delay_s: float = 0.0,
    max_retries: int = 10,
    retry_backoff_s: float = 5.0,
    request_timeout_s: float = 180.0,
    dry_run_payload: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Call Nemo (or dry-run) and return parsed JSON plus metadata."""
    if dry_run_payload is not None or not api_key:
        parsed = dict(dry_run_payload or {"dry_run": True, "parse_error": False})
        parsed.setdefault("dry_run", True)
        return {
            "parsed": parsed,
            "raw": json.dumps(parsed),
            "dry_run": True,
            "model": model,
        }

    raw = call_openrouter(
        model=model,
        system=system,
        user=user,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        max_retries=int(max_retries),
        retry_backoff_s=float(retry_backoff_s),
        request_timeout_s=float(request_timeout_s),
    )
    if rate_limit_delay_s > 0:
        time.sleep(float(rate_limit_delay_s))
    return {
        "parsed": extract_json(raw),
        "raw": raw,
        "dry_run": False,
        "model": model,
    }
