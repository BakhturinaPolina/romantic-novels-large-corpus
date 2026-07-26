"""Hugging Face Hub upload/download for Stage03 embedding caches."""

from __future__ import annotations

import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any

from src.stage03_train.embeddings import safe_embedding_name


def load_project_dotenv(project_root: Path | None = None) -> None:
    """Load .env into os.environ without overwriting existing variables."""
    root = project_root or Path.cwd()
    env_path = root / ".env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_hf_token() -> str | None:
    """Return Hub token from environment (after optional .env load)."""
    return os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")


def hub_relpath(run_id: str, cache_filename: str) -> str:
    return f"{run_id}/{cache_filename}"


def manifest_relpath(run_id: str, cache_filename: str) -> str:
    return f"{run_id}/{cache_filename}.manifest.json"


def build_manifest(
    *,
    run_id: str,
    embedding_model: str,
    cache_file: Path,
    n_docs: int | None = None,
    dim: int | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "run_id": run_id,
        "embedding_model": embedding_model,
        "cache_filename": cache_file.name,
        "dtype": "float32",
    }
    if n_docs is not None:
        payload["n_docs"] = int(n_docs)
    if dim is not None:
        payload["dim"] = int(dim)
    if cache_file.exists():
        payload["size_bytes"] = cache_file.stat().st_size
    return payload


def try_download_from_hub(
    repo_id: str,
    hub_path: str,
    local_file: Path,
    *,
    logger: logging.Logger | None = None,
) -> bool:
    """Download a single embedding file from a private Hub dataset repo."""
    token = get_hf_token()
    if not token:
        if logger:
            logger.warning("HF_TOKEN not set; cannot download %s from Hub.", hub_path)
        return False

    try:
        from huggingface_hub import hf_hub_download
    except ImportError as ex:
        raise ImportError("huggingface_hub is required for embeddings_hub") from ex

    local_file.parent.mkdir(parents=True, exist_ok=True)
    if logger:
        logger.info("Downloading Hub artifact %s:%s -> %s", repo_id, hub_path, local_file)

    try:
        cached = Path(
            hf_hub_download(
                repo_id=repo_id,
                filename=hub_path,
                repo_type="dataset",
                token=token,
            )
        )
    except Exception as ex:
        # Brand-new run_ids may not have an artifact yet. Treat missing files/repos as cache
        # miss and allow the pipeline to continue with local embedding computation.
        ex_name = ex.__class__.__name__
        ex_text = str(ex)
        if ex_name in {
            "EntryNotFoundError",
            "LocalEntryNotFoundError",
            "RemoteEntryNotFoundError",
            "RepositoryNotFoundError",
        } or (ex_name == "HfHubHTTPError" and "Entry Not Found" in ex_text):
            if logger:
                logger.warning(
                    "Hub artifact not found (%s:%s). Proceeding with local compute.",
                    repo_id,
                    hub_path,
                )
            return False
        raise
    if cached.resolve() != local_file.resolve():
        shutil.copy2(cached, local_file)

    if logger:
        logger.info("Hub download complete: %s (%d bytes)", local_file, local_file.stat().st_size)
    return True


def upload_to_hub(
    repo_id: str,
    local_file: Path,
    hub_path: str,
    manifest: dict[str, Any],
    *,
    logger: logging.Logger | None = None,
) -> None:
    """Upload embedding .npy and sidecar manifest to a Hub dataset repo."""
    token = get_hf_token()
    if not token:
        raise RuntimeError("HF_TOKEN not set; cannot upload embeddings to Hub.")

    if not local_file.is_file():
        raise FileNotFoundError(f"Cannot upload missing embeddings file: {local_file}")

    try:
        from huggingface_hub import HfApi
    except ImportError as ex:
        raise ImportError("huggingface_hub is required for embeddings_hub") from ex

    api = HfApi(token=token)
    if logger:
        logger.info(
            "Uploading embeddings to Hub %s:%s (%d bytes)",
            repo_id,
            hub_path,
            local_file.stat().st_size,
        )

    api.upload_file(
        path_or_fileobj=str(local_file),
        path_in_repo=hub_path,
        repo_id=repo_id,
        repo_type="dataset",
        commit_message=f"Stage03 embeddings {manifest.get('run_id', '')} {local_file.name}",
    )

    manifest_path = manifest_relpath(
        str(manifest.get("run_id", "run")),
        local_file.name,
    )
    api.upload_file(
        path_or_fileobj=json.dumps(manifest, indent=2).encode("utf-8"),
        path_in_repo=manifest_path,
        repo_id=repo_id,
        repo_type="dataset",
        commit_message=f"Manifest for {local_file.name}",
    )
    if logger:
        logger.info("Hub upload complete: https://huggingface.co/datasets/%s/tree/main/%s", repo_id, hub_path)


def hub_config_enabled(hub_cfg: dict[str, Any] | None) -> bool:
    return bool(hub_cfg and hub_cfg.get("enabled"))


def sync_embeddings_with_hub(
    *,
    hub_cfg: dict[str, Any],
    run_id: str,
    model_name: str,
    cache_file: Path,
    computed: bool,
    n_docs: int | None = None,
    dim: int | None = None,
    logger: logging.Logger | None = None,
) -> None:
    """Download before compute or upload after compute, per config."""
    if not hub_config_enabled(hub_cfg):
        return

    load_project_dotenv()
    repo_id = str(hub_cfg["repo_id"])
    hub_run_id = str(hub_cfg.get("hub_run_id") or run_id)
    hub_path = hub_relpath(hub_run_id, cache_file.name)

    if hub_cfg.get("download_if_missing", True) and not cache_file.exists():
        try_download_from_hub(repo_id, hub_path, cache_file, logger=logger)

    if computed and hub_cfg.get("upload_after_compute", False) and cache_file.is_file():
        manifest = build_manifest(
            run_id=run_id,
            embedding_model=model_name,
            cache_file=cache_file,
            n_docs=n_docs,
            dim=dim,
        )
        try:
            upload_to_hub(repo_id, cache_file, hub_path, manifest, logger=logger)
        except Exception as ex:
            if logger:
                logger.warning(
                    "Hub upload failed (%s). Local embeddings are saved; continuing pipeline.",
                    ex,
                )
