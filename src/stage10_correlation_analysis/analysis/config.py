"""Config loading and path resolution for the Stage10 final analysis.

Every script and notebook in the final analysis reads `configs/stage10/final_analysis.yaml`
through here, so run ids and paths are declared in exactly one place.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml

DEFAULT_CONFIG_PATH = "configs/stage10/final_analysis.yaml"
_ROOT_MARKERS = ("src", "configs", "results")


def find_project_root(start: Optional[Path] = None) -> Path:
    """Walk up from `start` until a directory holding src/, configs/ and results/ is found."""
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / marker).is_dir() for marker in _ROOT_MARKERS):
            return candidate
    raise RuntimeError(
        f"Could not locate the project root above {here}. "
        f"Expected a directory containing {', '.join(_ROOT_MARKERS)}."
    )


class AnalysisConfig:
    """Thin wrapper over the YAML config that resolves paths against the project root."""

    def __init__(self, data: Dict[str, Any], root: Path, config_path: Path):
        self.data = data
        self.root = root
        self.config_path = config_path

    # -- dict-like access ---------------------------------------------------
    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    _MISSING = object()

    def section(self, *keys: str, default: Any = _MISSING) -> Any:
        """Fetch a nested section, e.g. `cfg.section("outcomes", "quality", "raw")`."""
        node: Any = self.data
        for key in keys:
            if not isinstance(node, dict) or key not in node:
                if default is not AnalysisConfig._MISSING:
                    return default
                raise KeyError(f"Missing config key: {' -> '.join(keys)}")
            node = node[key]
        return node

    # -- paths --------------------------------------------------------------
    def path(self, *keys: str, required: bool = False) -> Optional[Path]:
        """Resolve a config value that names a path, relative to the project root."""
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

    def first_existing_input(self, names: Iterable[str]) -> Path:
        """Return the first input path that exists — used for the Stage09 re-run fallback."""
        tried: List[Path] = []
        for name in names:
            candidate = self.input_path(name)
            if candidate is None:
                continue
            tried.append(candidate)
            if candidate.exists():
                return candidate
        raise FileNotFoundError(
            "None of these inputs exist:\n  " + "\n  ".join(str(p) for p in tried)
        )

    def sentence_topic_files(self) -> List[Path]:
        pattern = self.section("inputs", "sentence_topics_glob")
        files = sorted(self.root.glob(pattern))
        if not files:
            raise FileNotFoundError(f"No sentence topic parquet files matched {pattern}")
        return files

    def notebook_output_dirs(self, notebook: str) -> Dict[str, Path]:
        """Create and return the figures/tables directories for one notebook."""
        base = self.output_path("notebook_dir") / notebook
        dirs = {"base": base, "figures": base / "figures", "tables": base / "tables"}
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        return dirs

    # -- convenience accessors ---------------------------------------------
    @property
    def run_id(self) -> str:
        return str(self.data["run_id"])

    @property
    def tier_column(self) -> str:
        return str(self.section("tiers", "column"))

    @property
    def tier_order(self) -> List[str]:
        return list(self.section("tiers", "order"))

    @property
    def cluster_column(self) -> str:
        return str(self.section("controls", "cluster"))

    def excluded_book_ids(self) -> List[int]:
        """Book ids to drop, if an exclusion list has been declared. Usually empty."""
        path = self.input_path("excluded_book_ids")
        if path is None or not path.exists():
            return []
        text = path.read_text(encoding="utf-8")
        return [int(line.strip()) for line in text.splitlines() if line.strip().isdigit()]

    def taxonomy_config(self) -> Dict[str, Any]:
        path = self.input_path("taxonomy_config", required=True)
        assert path is not None
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def axis_schema(self) -> Dict[str, Any]:
        path = self.input_path("axis_schema", required=True)
        assert path is not None
        return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_analysis_config(
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    *,
    root: Optional[Path] = None,
) -> AnalysisConfig:
    """Load the Stage10 analysis config, resolving `config_path` against the project root."""
    project_root = root or find_project_root()
    path = Path(config_path)
    if not path.is_absolute():
        path = project_root / path
    if not path.exists():
        raise FileNotFoundError(f"Analysis config not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return AnalysisConfig(data, project_root, path)
