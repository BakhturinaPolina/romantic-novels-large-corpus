"""Config loading for Stage 11 refined construct analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml

DEFAULT_CONFIG_PATH = "configs/stage11/refined_constructs.yaml"
_ROOT_MARKERS = ("src", "configs", "results")


def find_project_root(start: Optional[Path] = None) -> Path:
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / marker).is_dir() for marker in _ROOT_MARKERS):
            return candidate
    raise RuntimeError(
        f"Could not locate the project root above {here}. "
        f"Expected a directory containing {', '.join(_ROOT_MARKERS)}."
    )


class Stage11Config:
    """Thin wrapper over refined_constructs.yaml with path resolution."""

    def __init__(self, data: Dict[str, Any], root: Path, config_path: Path):
        self.data = data
        self.root = root
        self.config_path = config_path

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    _MISSING = object()

    def section(self, *keys: str, default: Any = _MISSING) -> Any:
        node: Any = self.data
        for key in keys:
            if not isinstance(node, dict) or key not in node:
                if default is not Stage11Config._MISSING:
                    return default
                raise KeyError(f"Missing config key: {' -> '.join(keys)}")
            node = node[key]
        return node

    def path(self, *keys: str, required: bool = False) -> Optional[Path]:
        value = self.section(*keys)
        if value is None:
            if required:
                raise FileNotFoundError(f"Config path {' -> '.join(keys)} is null but required")
            return None
        resolved = Path(value)
        if not resolved.is_absolute():
            resolved = self.root / resolved
        if required and not resolved.exists():
            raise FileNotFoundError(f"{' -> '.join(keys)} does not exist: {resolved}")
        return resolved

    def input_path(self, name: str, *, required: bool = False) -> Optional[Path]:
        return self.path("inputs", name, required=required)

    def output_path(self, name: str, *, create: bool = False) -> Path:
        resolved = self.path("outputs", name)
        assert resolved is not None
        if create:
            target = resolved if resolved.suffix == "" else resolved.parent
            target.mkdir(parents=True, exist_ok=True)
        return resolved

    def sentence_topic_files(self) -> List[Path]:
        pattern = self.section("inputs", "sentence_topics_glob")
        files = sorted(self.root.glob(pattern))
        if not files:
            raise FileNotFoundError(f"No sentence topic parquet files matched {pattern}")
        return files

    @property
    def run_id(self) -> str:
        return str(self.data["run_id"])

    def ensure_output_tree(self) -> Dict[str, Path]:
        """Create the Stage 11 results layout under outputs.base_dir."""
        base = self.output_path("base_dir", create=True)
        dirs = {
            "base": base,
            "candidates": self.output_path("candidates_dir", create=True),
            "evidence_packets": self.output_path("evidence_packets_dir", create=True),
            "stability_pilot": self.output_path("stability_pilot_dir", create=True),
            "audits": self.output_path("audits_dir", create=True),
            "human_review": self.output_path("human_review_dir", create=True),
            "constructs": self.output_path("constructs_dir", create=True),
            "book_features": self.output_path("book_features_dir", create=True),
            "notebook_analysis": self.output_path("notebook_dir", create=True),
        }
        for hyp in ("h1", "h2", "h3", "h4", "h5", "h6"):
            (dirs["audits"] / hyp).mkdir(parents=True, exist_ok=True)
        return dirs


def load_stage11_config(
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    *,
    root: Optional[Path] = None,
) -> Stage11Config:
    project_root = root or find_project_root()
    path = Path(config_path)
    if not path.is_absolute():
        path = project_root / path
    if not path.exists():
        raise FileNotFoundError(f"Stage 11 config not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Stage11Config(data, project_root, path)


def load_prompt_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Prompt YAML not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Prompt YAML must be a mapping: {path}")
    return data
