"""Pure helpers for Stage03 Bayesian-optimization checkpoint/resume."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def load_bo_checkpoint(result_json: Path) -> dict[str, Any] | None:
    """Load OCTIS ``result.json`` if present."""
    if not result_json.exists():
        return None
    with open(result_json, "r", encoding="utf-8") as f:
        return json.load(f)


def bo_calls_done(payload: dict[str, Any]) -> int:
    """Number of completed BO iterations stored in a checkpoint."""
    f_val = payload.get("f_val")
    if isinstance(f_val, list):
        return len(f_val)
    x_iters = payload.get("x_iters") or {}
    if not x_iters:
        return 0
    first = next(iter(x_iters.values()))
    return len(first) if isinstance(first, list) else 0


def bo_calls_total(payload: dict[str, Any]) -> int:
    return int(payload.get("number_of_call", 0))


def is_bo_complete(payload: dict[str, Any], *, number_of_calls: int | None = None) -> bool:
    """Return True when the checkpoint already contains all planned calls."""
    total = number_of_calls if number_of_calls is not None else bo_calls_total(payload)
    return bo_calls_done(payload) >= total > 0


def build_bo_resume_seed(payload: dict[str, Any]) -> tuple[dict[str, list[Any]], list[float], int]:
    """
    Build ``x0``/``y0`` for OCTIS ``optimize(x0=..., y0=...)`` resume.

    OCTIS replays the first ``k`` calls from ``x0``/``y0`` without re-evaluating
    the objective when ``y0`` is non-empty.
    """
    k = bo_calls_done(payload)
    if k == 0:
        return {}, [], 0

    x_iters = payload.get("x_iters") or {}
    f_val = payload.get("f_val") or []
    hyperparams = sorted(x_iters.keys())
    x0 = {name: list(x_iters[name][:k]) for name in hyperparams}
    y0 = [float(f_val[i]) for i in range(k)]
    return x0, y0, k


def best_params_from_bo(payload: dict[str, Any]) -> dict[str, Any]:
    """Pick hyperparameters at the best (max) objective value."""
    f_val = payload.get("f_val") or []
    x_iters = payload.get("x_iters") or {}
    if not f_val or not x_iters:
        return {}
    best_idx = int(np.argmax(f_val))
    return {name: x_iters[name][best_idx] for name in sorted(x_iters.keys())}


def _median_metric(
    dict_model_runs: dict[str, Any],
    metric_key: str,
    iteration: int,
) -> float:
    runs = dict_model_runs.get(metric_key, {}).get(f"iteration_{iteration}", [])
    if not runs:
        return float("nan")
    return float(np.median(runs))


def _runs_metric(
    dict_model_runs: dict[str, Any],
    metric_key: str | None,
    iteration: int,
) -> list[float]:
    if not metric_key:
        return []
    runs = dict_model_runs.get(metric_key, {}).get(f"iteration_{iteration}", [])
    return [float(x) for x in runs]


def _metric_key_by_substring(extra_names: list[str], substring: str) -> str | None:
    """Find an OCTIS extra-metric key whose name contains ``substring``."""
    for name in extra_names:
        if substring in name:
            return name
    return None


def project_result_to_trials(
    payload: dict[str, Any],
    *,
    run_id: str,
    model_idx: int,
    model_name: str,
    train_csv: Path,
    eval_csv: Path,
    test_csv: Path,
    seed: int,
    stability_score: float,
    topic_stability_cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Project OCTIS checkpoint JSON into one row per completed BO call."""
    k = bo_calls_done(payload)
    if k == 0:
        return []

    metric_name = str(payload.get("metric_name", "Coherence"))
    extra_names = list(payload.get("extra_metric_names") or [])
    diversity_key = (
        _metric_key_by_substring(extra_names, "TopicDiversity")
        or (extra_names[0] if extra_names else None)
    )
    n_topics_key = _metric_key_by_substring(extra_names, "TopicCount")
    raw_coh_key = _metric_key_by_substring(extra_names, "RawCoherence")
    extra_column_map = {
        "OutlierRate": "outlier_rate",
        "LargestTopicShare": "largest_topic_share",
        "MedianTopicSize": "median_topic_size",
        "P10TopicSize": "p10_topic_size",
        "P90TopicSize": "p90_topic_size",
        "TinyTopicsLt25": "n_tiny_topics_lt25",
        "TinyTopicsLt50": "n_tiny_topics_lt50",
    }
    extra_keys: dict[str, str | None] = {
        col: _metric_key_by_substring(extra_names, substr)
        for substr, col in extra_column_map.items()
    }
    dict_model_runs = payload.get("dict_model_runs") or {}
    x_iters = payload.get("x_iters") or {}
    ts_cfg = topic_stability_cfg or {}
    max_std = float(ts_cfg.get("max_n_topics_std", 3.0))
    collapse_ratio = float(ts_cfg.get("collapse_ratio", 0.5))

    from src.stage03_train.topic_stability import stability_pass, topic_run_stats

    rows: list[dict[str, Any]] = []
    for i in range(k):
        bo_objective = _median_metric(dict_model_runs, metric_name, i)
        raw_coherence = (
            _median_metric(dict_model_runs, raw_coh_key, i) if raw_coh_key else np.nan
        )
        if raw_coh_key:
            coherence_c_v = raw_coherence
        else:
            coherence_c_v = bo_objective

        row: dict[str, Any] = {
            "run_id": run_id,
            "trial_id": f"{run_id}_{model_idx}_call_{i}",
            "bo_call": i,
            "seed": seed,
            "embedding_model": model_name,
            "coherence_c_v": coherence_c_v,
            "bo_objective": bo_objective if raw_coh_key else np.nan,
            "topic_diversity": (
                _median_metric(dict_model_runs, diversity_key, i) if diversity_key else np.nan
            ),
            "n_topics": (
                _median_metric(dict_model_runs, n_topics_key, i) if n_topics_key else np.nan
            ),
            "stability_score": stability_score,
            "train_csv": str(train_csv),
            "eval_csv": str(eval_csv),
            "test_csv": str(test_csv),
        }
        for col, metric_key in extra_keys.items():
            if metric_key:
                row[col] = _median_metric(dict_model_runs, metric_key, i)
        n_topics_runs = _runs_metric(dict_model_runs, n_topics_key, i)
        if n_topics_runs:
            stats = topic_run_stats(n_topics_runs)
            row["n_topics_min"] = stats["min"]
            row["n_topics_max"] = stats["max"]
            row["n_topics_std"] = stats["std"]
            row["n_topics_runs"] = int(stats["n_runs"])
            row["topic_stability_pass"] = stability_pass(
                n_topics_runs,
                max_std=max_std,
                collapse_ratio=collapse_ratio,
            )
        else:
            row["n_topics_min"] = np.nan
            row["n_topics_max"] = np.nan
            row["n_topics_std"] = np.nan
            row["n_topics_runs"] = 0
            row["topic_stability_pass"] = True
        for name in sorted(x_iters.keys()):
            row[name] = x_iters[name][i]
        rows.append(row)
    return rows


def restore_optimizer_skopt_state(
    optimizer: Any,
    payload: dict[str, Any],
) -> tuple[Any, Any]:
    """
    Replay skopt state from OCTIS ``result.json`` without reloading model/dataset.

    OCTIS ``_restore_parameters`` tries to import the topic model from
    ``octis.models/``, which fails for our custom ``BERTopicOctisModelWithEmbeddings``.
    """
    from pathlib import Path as PathLib

    from octis.optimization.optimizer_tool import choose_optimizer, load_search_space
    from sklearn.gaussian_process.kernels import Matern

    optimizer.search_space = load_search_space(payload["search_space"])
    optimizer.acq_func = payload["acq_func"]
    optimizer.surrogate_model = payload["surrogate_model"]
    optimizer.kernel = eval(payload["kernel"], {"Matern": Matern})
    optimizer.optimization_type = payload["optimization_type"]
    optimizer.model_runs = payload["model_runs"]
    optimizer.save_models = payload["save_models"]
    optimizer.save_step = payload["save_step"]
    optimizer.save_name = payload["save_name"]
    optimizer.save_path = payload["save_path"]
    optimizer.early_stop = payload["early_stop"]
    optimizer.early_step = payload["early_step"]
    optimizer.plot_model = payload["plot_model"]
    optimizer.plot_best_seen = payload["plot_best_seen"]
    optimizer.plot_name = payload["plot_name"]
    optimizer.log_scale_plot = payload["log_scale_plot"]
    optimizer.random_state = payload["random_state"]
    optimizer.dict_model_runs = payload["dict_model_runs"]
    optimizer.number_of_previous_calls = int(payload["current_call"]) + 1
    optimizer.current_call = int(payload["current_call"]) + 1
    optimizer.number_of_call = int(payload["number_of_call"])
    optimizer.x0 = payload.get("x0") or {}
    optimizer.y0 = payload.get("y0") or []
    optimizer.n_random_starts = payload["n_random_starts"]
    optimizer.initial_point_generator = payload["initial_point_generator"]
    optimizer.topk = payload["topk"]
    optimizer.time_eval = payload["time_eval"]
    optimizer.name_optimized_metric = payload["metric_name"]
    optimizer.extra_metric_names = list(payload.get("extra_metric_names") or [])
    optimizer.hyperparameters = list(sorted(optimizer.search_space.keys()))
    optimizer.lenx0 = (
        len(list(optimizer.x0.values())[0]) if optimizer.x0 else 0
    )

    if not str(optimizer.save_path).endswith("/"):
        optimizer.save_path = str(optimizer.save_path) + "/"

    opt = choose_optimizer(optimizer)
    res = None
    x_iters = payload["x_iters"]
    f_val = payload["f_val"]
    for i in range(optimizer.number_of_previous_calls):
        next_x = [x_iters[key][i] for key in optimizer.hyperparameters]
        if optimizer.optimization_type == "Maximize":
            told_f = -float(f_val[i])
        else:
            told_f = float(f_val[i])
        res = opt.tell(next_x, told_f)

    PathLib(optimizer.save_path).mkdir(parents=True, exist_ok=True)
    if optimizer.save_models:
        optimizer.model_path_models = optimizer.save_path + "models/"

    return res, opt


def make_resumable_optimizer_class() -> type:
    """Build an OCTIS ``Optimizer`` subclass that fires a callback after each BO call.

    Imported lazily so that ``bo_resume`` stays import-light for unit tests that
    do not need OCTIS installed.

    The override mirrors ``octis.optimization.optimizer.Optimizer._optimization_loop``
    exactly (same point proposal, ``opt.tell``, timing, save_step, early-stop), and
    only adds a fail-safe ``on_call_complete(current_call, res)`` hook right after the
    per-call ``result.json`` is written.
    """
    import time

    from octis.optimization.optimizer import Optimizer
    from octis.optimization.optimizer_evaluation import OptimizerEvaluation
    from octis.models.model import save_model_output
    from octis.optimization.optimizer_tool import (
        early_condition,
        plot_bayesian_optimization,
        plot_model_runs,
    )

    from src.stage03_train.topic_stability import stability_pass, stability_penalty

    class ResumableOptimizer(Optimizer):
        on_call_complete = None  # type: ignore[assignment]
        topic_stability_enabled = False
        topic_stability_max_std = 3.0
        topic_stability_collapse_ratio = 0.5
        topic_stability_penalty_weight = 0.2
        topic_stability_base_seed = 42

        def _fire_call_complete(self, res: Any) -> None:
            cb = getattr(self, "on_call_complete", None)
            if cb is None:
                return
            try:
                cb(self.current_call, res)
            except Exception:  # pragma: no cover - never let a hook break BO
                pass

        def _topic_count_metric_index(self) -> int | None:
            for j, name in enumerate(self.extra_metric_names):
                if "TopicCount" in name:
                    return j
            return None

        def _objective_function(self, hyperparameter_values: list) -> float:
            params: dict[str, Any] = {}
            for i in range(len(self.hyperparameters)):
                params[self.hyperparameters[i]] = hyperparameter_values[i]

            different_model_runs: list[float] = []
            different_model_runs_extra_metrics = [[] for _ in range(len(self.extra_metrics))]
            topic_count_idx = self._topic_count_metric_index()
            topic_counts_per_run: list[float] = []
            vary_umap_seed = self.topic_stability_enabled and self.model_runs > 1

            for run_i in range(self.model_runs):
                run_params = dict(params)
                if vary_umap_seed:
                    run_params["umap__random_state"] = self.topic_stability_base_seed + run_i

                model_output = self.model.train_model(self.dataset, run_params, self.topk)
                score = self.metric.score(model_output)
                different_model_runs.append(score)

                for j, extra_metric in enumerate(self.extra_metrics):
                    extra_score = extra_metric.score(model_output)
                    different_model_runs_extra_metrics[j].append(extra_score)
                    if topic_count_idx is not None and j == topic_count_idx:
                        topic_counts_per_run.append(float(extra_score))

                if self.topic_stability_enabled:
                    print(
                        f"[STABILITY] call={self.current_call} run={run_i + 1}/{self.model_runs} "
                        f"umap_seed={run_params.get('umap__random_state')} "
                        f"n_topics={topic_counts_per_run[-1] if topic_counts_per_run else 'n/a'} "
                        f"score={score:.4f}"
                    )

                if self.save_models:
                    name = str(self.current_call) + "_" + str(run_i)
                    save_model_path = self.model_path_models + name
                    save_model_output(model_output, save_model_path)

            self.dict_model_runs[self.name_optimized_metric][
                "iteration_" + str(self.current_call)
            ] = different_model_runs

            for j, extra_metric in enumerate(self.extra_metrics):
                self.dict_model_runs[self.extra_metric_names[j]][
                    "iteration_" + str(self.current_call)
                ] = different_model_runs_extra_metrics[j]

            result = float(np.median(different_model_runs))
            if self.topic_stability_enabled and topic_counts_per_run:
                penalized = stability_penalty(
                    result,
                    topic_counts_per_run,
                    max_std=self.topic_stability_max_std,
                    collapse_ratio=self.topic_stability_collapse_ratio,
                    weight=self.topic_stability_penalty_weight,
                )
                passed = stability_pass(
                    topic_counts_per_run,
                    max_std=self.topic_stability_max_std,
                    collapse_ratio=self.topic_stability_collapse_ratio,
                )
                print(
                    f"[STABILITY] call={self.current_call} summary "
                    f"counts={topic_counts_per_run} "
                    f"std={float(np.std(topic_counts_per_run)) if len(topic_counts_per_run) > 1 else 0.0:.2f} "
                    f"pass={passed} penalty={result - penalized:.4f} "
                    f"median_score={result:.4f} final={penalized:.4f}"
                )
                result = penalized

            if self.optimization_type == "Maximize":
                result = -result

            if self.plot_model:
                name_plot = "".join([
                    self.save_path,
                    self.plot_name,
                    "_model_runs_",
                    self.name_optimized_metric,
                ])
                plot_model_runs(
                    self.dict_model_runs[self.name_optimized_metric],
                    self.current_call,
                    name_plot,
                )
                for j in range(len(self.extra_metrics)):
                    name_plot = "".join([
                        self.save_path,
                        self.plot_name,
                        "_model_runs_" + self.extra_metric_names[j],
                    ])
                    plot_model_runs(
                        self.dict_model_runs[self.extra_metric_names[j]],
                        self.current_call,
                        name_plot,
                    )

            return result

        def _optimization_loop(self, opt: Any) -> Any:
            results = None
            for i in range(self.number_of_previous_calls, self.number_of_call):
                print("Current call: ", self.current_call)
                start_time = time.time()

                if i < self.lenx0:
                    next_x = [self.x0[name][i] for name in self.hyperparameters]
                    if len(self.y0) == 0:
                        f_val = self._objective_function(next_x)
                    else:
                        self.dict_model_runs[self.name_optimized_metric][
                            "iteration_" + str(i)
                        ] = self.y0[i]
                        f_val = (
                            -self.y0[i]
                            if (self.optimization_type == "Maximize")
                            else self.y0[i]
                        )
                else:
                    next_x = opt.ask()
                    f_val = self._objective_function(next_x)

                res = opt.tell(next_x, f_val)

                end_time = time.time()
                total_time_function = end_time - start_time
                self.time_eval.append(total_time_function)

                if self.plot_best_seen:
                    plot_bayesian_optimization(
                        res.func_vals,
                        self.save_path + self.plot_name + "_best_seen",
                        self.log_scale_plot,
                        conv_max=self.optimization_type == "Maximize",
                    )

                results = OptimizerEvaluation(self, BO_results=res)

                if i % self.save_step == 0:
                    name_json = self.save_path + self.save_name + ".json"
                    results.save(name_json)

                self._fire_call_complete(res)

                if (
                    i >= len(self.x0)
                    and self.early_stop
                    and early_condition(res.func_vals, self.early_step, self.n_random_starts)
                ):
                    print("Stop because of early stopping condition")
                    break

                self.current_call = self.current_call + 1

            return results

    return ResumableOptimizer


def write_trials_partial_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write per-call partial trials (overwrites file with full projection)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        if path.exists():
            path.unlink()
        return
    pd.DataFrame(rows).to_csv(path, index=False)


def sync_trials_partial_from_checkpoint(
    result_json: Path,
    trials_partial_csv: Path,
    *,
    run_id: str,
    model_idx: int,
    model_name: str,
    train_csv: Path,
    eval_csv: Path,
    test_csv: Path,
    seed: int,
    stability_score: float,
    topic_stability_cfg: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], int, int]:
    """Load checkpoint, project rows, persist ``trials_partial.csv``."""
    payload = load_bo_checkpoint(result_json)
    if payload is None:
        return [], 0, 0
    rows = project_result_to_trials(
        payload,
        run_id=run_id,
        model_idx=model_idx,
        model_name=model_name,
        train_csv=train_csv,
        eval_csv=eval_csv,
        test_csv=test_csv,
        seed=seed,
        stability_score=stability_score,
        topic_stability_cfg=topic_stability_cfg,
    )
    write_trials_partial_csv(trials_partial_csv, rows)
    return rows, bo_calls_done(payload), bo_calls_total(payload)
