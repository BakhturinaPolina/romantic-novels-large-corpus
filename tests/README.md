# Tests

Pytest/unittest modules grouped by pipeline stage. Shared CSV fixtures live under [`fixtures/`](fixtures/).

## Layout

| Folder | Coverage |
|--------|----------|
| [`stage03/`](stage03/) | BO resume, search space, embeddings cache, smoke e2e |
| [`stage04/`](stage04/) | Pareto selection wiring |
| [`stage05/`](stage05/) | Compare-fit stability, full-corpus infer, test holdout |
| [`stage06/`](stage06/) | Character-name cleaning (+ call73 integration) |
| [`stage07/`](stage07/) | Representation stats, posthoc rules, Stage07 integration |
| [`stage08/`](stage08/) | Quality adjudication (08a) |
| [`stage09/`](stage09/) | Taxonomy v2 schema + intimacy axes |
| [`legacy/`](legacy/) | Superseded tests (legacy stage04 trials profile, old posthoc) |

## Run

```bash
# Full suite (fast unit tests; skips opt-in GPU/smoke cases)
.venv/bin/python -m pytest tests/ -q

# Stage03 resume guards
.venv/bin/python -m pytest tests/stage03/test_stage03_embeddings_resume.py tests/stage03/test_stage03_bo_resume.py -v

# Opt-in Stage03 smoke e2e (GPU / heavy deps)
STAGE03_SMOKE=1 .venv/bin/python -m pytest tests/stage03/test_stage03_smoke_e2e.py -v -s

# Posthoc rules
.venv/bin/python -m pytest tests/stage07/test_topic_posthoc_rules.py -v
```

Fixtures for smoke configs: `tests/fixtures/stage03_smoke/` (referenced by `configs/stage03/paths_smoke.yaml`).
