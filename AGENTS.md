## Learned User Preferences

- Prefer short, clear run instructions (bash helper scripts over long copy-paste command blocks) for Docker and remote GPU workflows.
- Run Docker without sudo; target machines should have the user in the `docker` group.
- Remote `transfer_bundle` embedding encode should not require `.env`, API keys, or Hugging Face tokens; public sentence-transformer models only.
- When assembling transfer bundles, explicitly list files too large to include that must be copied manually.
- Remove superseded v2 dataset references and already-completed model docs from active READMEs when updating.
- Pattern new BO selection analysis notebooks after `notebooks/04_selection/`, driven by YAML configs such as `configs/stage04/selection_notebooks.yaml`.
- Prefer simpler, shorter README text following GitHub best practices.
- Move deprecated code under `src/legacy/` and gitignore rather than deleting outright.
- Wants detailed terminal progress during long Stage03 runs (progress bars, timing, ETA helpers).
- Only create git commits when explicitly asked.
- Use stratified subsampling for BERTopic fit, not random subsampling.

## Learned Workspace Facts

- Neural topic modeling pipeline (BERTopic + OCTIS BO) on romance novels; active modules are `stage03_train`, `stage04_eval_select`, `stage05_final_fit`, and `stage05b_test_holdout`.
- Current corpus is v3 English-only at `data/raw/romance_subdataset_filtered_v3/` (~97M sentences: train 80.2M, val 17.2M, test 17.5M); 460 non-English books removed (~2.7% of sentences).
- v2 paths (`romance_subdataset_downloaded_v2_*`) are legacy; v3 is the active dataset for new work.
- Stage03 v3 uses stratified 500k train / 100k val fit indices in `data/stage03_samples_v3/` (seed 42) and OCTIS corpus in `data/interim/octis/v3_english_only/`.
- Three v3 embedding models: MiniLM-L12 (`v3_minilm12v2_first`, completed on primary laptop), MPNet (`v3_mpnet`), MiniLM-L6 (`v3_minilm6_first`).
- BO config: 130 calls, 3 `model_runs` per call, topic-count-penalized coherence objective, topic stability enabled (`configs/stage03/train_v3*.yaml`).
- `transfer_bundle/` is built via `scripts/bundle/make_transfer_bundle.sh`; remote runs use `scripts/stage03/run_v3_remote_model.sh`; CPU encode on remote, GPU required for cuML BO tuning.
- Three sentence CSVs (~9 GB total) must be copied manually to `data/raw/romance_subdataset_filtered_v3/` on target machines.
- Optional HF embeddings mirror: `RuthonField/romance-v2-train-eval-embeddings` for `.npy` cache download/upload on the primary machine.
- Experiment outputs live under `results/experiments/{run_id}/`; selection notebook outputs under `results/selection/{run_id}/notebook_analysis/`.
- Python 3.12+, CUDA 12.x, RAPIDS cuML for GPU UMAP/HDBSCAN; ~6 GB VRAM minimum.
- Source corpus: 17,514 romance EPUBs (2000–2017), 8,828 authors; book-level train/val/test splits preserved in subsampling metadata.
