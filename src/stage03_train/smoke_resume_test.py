"""
Opt-in Stage03 smoke + resume harness.

Run:
  STAGE03_SMOKE=1 python -m pytest tests/test_stage03_smoke_e2e.py -v -s
  python -m src.stage03_train.smoke_resume_test
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import unittest
from pathlib import Path

import pandas as pd

from src.common.config import load_config, resolve_path
from src.stage03_train.bo_resume import bo_calls_done, load_bo_checkpoint


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SMOKE_CONFIG = PROJECT_ROOT / "configs" / "train_smoke.yaml"
DEFAULT_RUN_ID = "stage03_smoke_resume"
CHECKPOINT_POLL_S = 2.0
CHECKPOINT_TIMEOUT_S = 3600.0


def _experiments_dir(run_id: str) -> Path:
    cfg = load_config(SMOKE_CONFIG)
    paths_cfg = load_config(Path(cfg.get("paths_config", "configs/paths.yaml")))
    base = resolve_path(Path(paths_cfg["outputs"]["experiments"]))
    return base / run_id


def _wait_for_opt_dir(run_id: str, timeout_s: float = CHECKPOINT_TIMEOUT_S) -> Path:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        exp = _experiments_dir(run_id)
        matches = list(exp.glob("opt_1_*"))
        if matches:
            return matches[0]
        time.sleep(CHECKPOINT_POLL_S)
    raise TimeoutError(f"Timed out waiting for optimization dir under {_experiments_dir(run_id)}")


def _opt_dir(run_id: str) -> Path:
    exp = _experiments_dir(run_id)
    matches = list(exp.glob("opt_1_*"))
    if not matches:
        raise FileNotFoundError(f"No optimization dir under {exp}")
    return matches[0]


def _clean_run(run_id: str) -> None:
    exp = _experiments_dir(run_id)
    cfg = load_config(SMOKE_CONFIG)
    paths_cfg = load_config(Path(cfg.get("paths_config", "configs/paths.yaml")))
    octis = resolve_path(Path(paths_cfg["inputs"]["octis_dataset"])) / run_id
    for path in (exp, octis):
        if path.exists():
            shutil.rmtree(path)


def _run_tune(run_id: str, *, timeout: float | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        "-m",
        "src.stage03_train.cli",
        "tune",
        "--config",
        str(SMOKE_CONFIG),
        "--run-id",
        run_id,
    ]
    return subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _wait_for_bo_checkpoint(result_json: Path, min_calls: int = 1) -> None:
    deadline = time.time() + CHECKPOINT_TIMEOUT_S
    while time.time() < deadline:
        payload = load_bo_checkpoint(result_json)
        if payload is not None and bo_calls_done(payload) >= min_calls:
            return
        time.sleep(CHECKPOINT_POLL_S)
    raise TimeoutError(f"Timed out waiting for BO checkpoint at {result_json}")


def run_smoke_resume_test(run_id: str = DEFAULT_RUN_ID) -> None:
    """Interrupt after first BO call, then resume and verify artifacts."""
    _clean_run(run_id)

    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "src.stage03_train.cli",
            "tune",
            "--config",
            str(SMOKE_CONFIG),
            "--run-id",
            run_id,
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        opt_dir = _wait_for_opt_dir(run_id)
        result_json = opt_dir / "result.json"
        deadline = time.time() + CHECKPOINT_TIMEOUT_S
        interrupted = False
        while time.time() < deadline and proc.poll() is None:
            payload = load_bo_checkpoint(result_json)
            if payload is not None and bo_calls_done(payload) >= 1:
                proc.terminate()
                proc.communicate(timeout=30)
                interrupted = True
                break
            time.sleep(CHECKPOINT_POLL_S)
        if not interrupted:
            if proc.poll() is None:
                proc.kill()
                proc.communicate(timeout=30)
            raise TimeoutError(f"Timed out waiting for first BO checkpoint at {result_json}")
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.communicate(timeout=30)

    opt_dir = _wait_for_opt_dir(run_id)
    result_json = opt_dir / "result.json"
    payload = load_bo_checkpoint(result_json)
    assert payload is not None, f"Expected BO checkpoint at {result_json}"
    calls_before = bo_calls_done(payload)
    assert calls_before >= 1, f"Expected >=1 completed BO call, got {calls_before}"

    partial_csv = opt_dir / "trials_partial.csv"
    partial_before = len(pd.read_csv(partial_csv)) if partial_csv.exists() else 0

    resume = _run_tune(run_id, timeout=CHECKPOINT_TIMEOUT_S)
    combined = (resume.stdout or "") + (resume.stderr or "")
    assert resume.returncode == 0, combined
    assert "Resuming BO from checkpoint" in combined or "BO checkpoint complete" in combined

    exp = _experiments_dir(run_id)
    trials_csv = exp / "trials.csv"
    run_state = exp / "run_state.json"
    assert trials_csv.exists()
    assert run_state.exists()
    with open(run_state, encoding="utf-8") as f:
        state = json.load(f)
    assert state.get("completed") is True

    partial_after = len(pd.read_csv(partial_csv))
    assert partial_csv.exists()
    assert partial_after >= calls_before
    if partial_before > 0:
        assert partial_after >= partial_before
    print(f"Smoke resume ok: partial_trials={partial_after}, aggregate_trials={len(pd.read_csv(trials_csv))}")


def run_smoke_full_test(run_id: str = "stage03_smoke_full") -> None:
    """Run smoke tuning to completion on tiny fixtures."""
    _clean_run(run_id)
    result = _run_tune(run_id, timeout=CHECKPOINT_TIMEOUT_S)
    combined = (result.stdout or "") + (result.stderr or "")
    assert result.returncode == 0, combined
    exp = _experiments_dir(run_id)
    assert (exp / "trials.csv").exists()
    with open(exp / "run_state.json", encoding="utf-8") as f:
        assert json.load(f).get("completed") is True
    print(f"Smoke full run ok: {exp / 'trials.csv'}")


class Stage03SmokeE2ETests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("STAGE03_SMOKE") == "1", "set STAGE03_SMOKE=1 to run")
    def test_smoke_full_run(self) -> None:
        run_smoke_full_test()

    @unittest.skipUnless(os.environ.get("STAGE03_SMOKE") == "1", "set STAGE03_SMOKE=1 to run")
    def test_smoke_interrupt_and_resume(self) -> None:
        run_smoke_resume_test()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Stage03 smoke/resume harness")
    parser.add_argument(
        "--mode",
        choices=("full", "resume"),
        default="resume",
        help="full=complete smoke run; resume=interrupt after 1 BO call then resume",
    )
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    if args.mode == "full":
        run_smoke_full_test(args.run_id or "stage03_smoke_full")
    else:
        run_smoke_resume_test(args.run_id or DEFAULT_RUN_ID)
