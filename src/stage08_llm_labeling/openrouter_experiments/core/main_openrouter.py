"""CLI entry point for Stage 08 topic labeling via OpenRouter API."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from bertopic import BERTopic

from src.common.config import load_config, resolve_path
from src.common.logging import setup_logging
from src.stage06_topic_exploration.explore_retrained_model import (
    DEFAULT_BASE_DIR,
    DEFAULT_EMBEDDING_MODEL,
)
from src.stage08_llm_labeling.generate_labels import (
    compare_topics_sources,
    extract_pos_topics,
    extract_pos_topics_from_json,
    integrate_labels_to_bertopic,
    load_all_representations_from_json,
    load_bertopic_model,
)
from src.stage08_llm_labeling.openrouter_experiments.core.labeling_runners import (
    estimate_openrouter_cost,
    get_token_usage,
    reset_token_usage,
)
from src.stage08_llm_labeling.openrouter_experiments.core.generate_labels_openrouter import (
    DEFAULT_OPENROUTER_API_KEY,
    DEFAULT_OPENROUTER_MODEL,
    DEFAULT_RATE_LIMIT_DELAY_S,
    extract_representative_docs_per_topic,
    generate_all_labels,
    generate_labels_streaming,
    load_openrouter_client,
    save_labels_openrouter,
    test_openrouter_authentication,
)
from src.stage08_llm_labeling.prompts.loader import DEFAULT_PROMPT_VERSION
from src.stage08_llm_labeling.topic_quality_hints import (
    filter_topics_dict,
    load_quality_adjudication_results,
    load_topic_quality_hints,
    topic_ids_for_labeling,
)

DEFAULT_OUTPUT_DIR = Path("results/stage08_llm_labeling")
DEFAULT_STAGE08_CONFIG = Path("configs/stage08/stage08_labeling.yaml")
DEFAULT_NUM_KEYWORDS = 15
DEFAULT_MAX_TOKENS = 256
DEFAULT_BATCH_SIZE = 50
DEFAULT_TEMPERATURE = 0.35


class Tee:
    """Write to both file and stdout/stderr with immediate flushing."""
    def __init__(self, file_path: Path, stream):
        # Open file in line-buffered mode for immediate flushing
        self.file = open(file_path, 'w', encoding='utf-8', buffering=1)  # Line buffering
        self.stream = stream
    
    def write(self, data):
        self.file.write(data)
        self.stream.write(data)
        # Force immediate flush for both
        self.file.flush()
        self.stream.flush()
    
    def flush(self):
        self.file.flush()
        self.stream.flush()
    
    def close(self):
        self.flush()
        self.file.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate topic labels from POS representation using OpenRouter API. Supports mistralai/mistral-nemo and google/gemini-2.5-flash (with reasoning).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    parser.add_argument(
        "--embedding-model",
        type=str,
        default=DEFAULT_EMBEDDING_MODEL,
        help="Embedding model name (e.g., 'paraphrase-MiniLM-L6-v2')",
    )
    
    parser.add_argument(
        "--pareto-rank",
        type=int,
        default=1,
        help="Pareto rank of the model to load",
    )
    
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=DEFAULT_BASE_DIR,
        help="Base directory containing retrained models",
    )
    
    parser.add_argument(
        "--use-native",
        action="store_true",
        help="Load native safetensors instead of pickle wrapper",
    )
    
    parser.add_argument(
        "--model-suffix",
        type=str,
        default="_with_noise_labels",
        help="Optional suffix to append to model filename/directory (default: '_with_noise_labels')",
    )
    
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=None,
        help="Path to enriched BERTopic model directory (e.g. call_73/model_compare_enriched)",
    )

    parser.add_argument(
        "--model-stage",
        type=str,
        default=None,
        help="Legacy stage subfolder when loading via --base-dir (ignored if --model-dir set)",
    )

    parser.add_argument(
        "--stage08-config",
        type=Path,
        default=DEFAULT_STAGE08_CONFIG,
        help="Stage08 labeling YAML (call_73 defaults)",
    )

    parser.add_argument(
        "--quality-csv",
        type=Path,
        default=None,
        help="Stage07 quality audit CSV for routing hints",
    )

    parser.add_argument(
        "--quality-adjudication-jsonl",
        type=Path,
        default=None,
        help="Stage08A adjudication results JSONL",
    )

    parser.add_argument(
        "--label-all-topics",
        action="store_true",
        default=False,
        help="Label every topic (ignore Stage07/08A routing filters)",
    )

    parser.add_argument(
        "--skip-hard-exclude",
        action="store_true",
        default=True,
        help="Skip topics with hard_exclude_candidate (default: True)",
    )

    parser.add_argument(
        "--require-08a-pass",
        action="store_true",
        default=True,
        help="Require Stage08A pass_to_labeling for soft-review topics (default: True)",
    )

    parser.add_argument(
        "--representative-docs-csv",
        type=Path,
        default=None,
        help="Fallback representative_docs.csv from compare-fit when model has no rep docs",
    )

    parser.add_argument(
        "--prompt-version",
        type=str,
        default=DEFAULT_PROMPT_VERSION,
        help="Prompt version: v3_topic_labeling (default), v3_rep_first, v1, v2, v2_*",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        default=True,
        help="Resume from partial labels JSON if present (default: True)",
    )

    parser.add_argument(
        "--no-resume",
        action="store_false",
        dest="resume",
        help="Do not resume from existing labels JSON",
    )

    parser.add_argument(
        "--rate-limit-delay",
        type=float,
        default=DEFAULT_RATE_LIMIT_DELAY_S,
        help="Seconds between OpenRouter API calls",
    )
    
    parser.add_argument(
        "--num-keywords",
        type=int,
        default=DEFAULT_NUM_KEYWORDS,
        help=f"Number of top keywords per topic to use for label generation (default: {DEFAULT_NUM_KEYWORDS})",
    )
    
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"Maximum number of tokens to generate per label (default: {DEFAULT_MAX_TOKENS})",
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for labels JSON file",
    )
    
    parser.add_argument(
        "--no-integrate",
        action="store_true",
        help="Skip integrating labels back into BERTopic model (NOT RECOMMENDED - labels should be saved to model)",
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=DEFAULT_OPENROUTER_API_KEY,
        help="OpenRouter API key (default: uses hardcoded key)",
    )
    
    parser.add_argument(
        "--model-name",
        type=str,
        default=DEFAULT_OPENROUTER_MODEL,
        help=(
            "OpenRouter model name. "
            "Default: mistralai/Mistral-Nemo-Instruct-2407 "
            "(set via DEFAULT_OPENROUTER_MODEL in generate_labels_openrouter.py)."
        ),
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Sampling temperature for generation (default: {DEFAULT_TEMPERATURE})",
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Number of topics to process before logging progress",
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/paths.yaml"),
        help="Path to paths configuration file",
    )
    
    parser.add_argument(
        "--topics-json",
        type=Path,
        default=None,
        help="Path to topics JSON file (optional, for comparison/inspection with BERTopic topics)",
    )
    
    parser.add_argument(
        "--limit-topics",
        type=int,
        default=None,
        help="Limit number of topics to process (useful for testing)",
    )

    parser.add_argument(
        "--topic-ids",
        type=str,
        default=None,
        help="Comma-separated topic IDs to label only (e.g. '0,1,12,31'). Ignores stream order.",
    )

    parser.add_argument(
        "--max-snippets",
        type=int,
        default=None,
        help="Max representative snippets per topic (default: from stage08 yaml or 6)",
    )

    parser.add_argument(
        "--output-suffix",
        type=str,
        default=None,
        help="Suffix for labels JSON filename (prompt sweeps), e.g. prompt_sweep_S1",
    )
    
    parser.add_argument(
        "--use-improved-prompts",
        action="store_true",
        default=True,
        help="Use full JSON schema (v2 by default): label, scene_summary, categories, is_noise, rationale",
    )

    parser.add_argument(
        "--label-only",
        action="store_false",
        dest="use_improved_prompts",
        help="Legacy v1-style minimal JSON output",
    )
    
    parser.add_argument(
        "--reasoning-effort",
        type=str,
        choices=["none", "low", "medium", "high"],
        default="none",
        help=(
            "Optional reasoning effort for supported models, passed via "
            "OpenRouter extra_body['reasoning']['effort']. "
            "Use 'none' to disable. Supported by models like google/gemini-2.5-flash."
        ),
    )
    
    return parser.parse_args()


def _apply_stage08_config_defaults(args: argparse.Namespace) -> None:
    """Merge call_73 defaults from configs/stage08/stage08_labeling.yaml when paths unset."""
    if not args.stage08_config or not Path(args.stage08_config).is_file():
        return
    cfg = load_config(Path(args.stage08_config))
    paths = cfg.get("paths", {})
    labeling = cfg.get("labeling", {})
    openrouter = cfg.get("openrouter", {})

    if args.model_dir is None and paths.get("enriched_model"):
        args.model_dir = Path(paths["enriched_model"])
    if args.topics_json is None and paths.get("topics_json"):
        args.topics_json = Path(paths["topics_json"])
    if args.quality_csv is None and paths.get("quality_csv"):
        args.quality_csv = Path(paths["quality_csv"])
    if args.representative_docs_csv is None:
        if paths.get("representative_docs_csv"):
            args.representative_docs_csv = Path(paths["representative_docs_csv"])
        elif paths.get("compare_fit_dir"):
            args.representative_docs_csv = Path(paths["compare_fit_dir"]) / "representative_docs.csv"
    if args.output_dir == DEFAULT_OUTPUT_DIR and paths.get("output_dir"):
        args.output_dir = Path(paths["output_dir"])
    if args.model_name == DEFAULT_OPENROUTER_MODEL and openrouter.get("model"):
        args.model_name = openrouter["model"]
    if args.temperature == DEFAULT_TEMPERATURE and openrouter.get("temperature") is not None:
        args.temperature = float(openrouter["temperature"])
    if args.max_tokens == DEFAULT_MAX_TOKENS and openrouter.get("max_tokens") is not None:
        args.max_tokens = int(openrouter["max_tokens"])
    if args.rate_limit_delay == DEFAULT_RATE_LIMIT_DELAY_S and openrouter.get("rate_limit_delay_s") is not None:
        args.rate_limit_delay = float(openrouter["rate_limit_delay_s"])
    if args.num_keywords == DEFAULT_NUM_KEYWORDS and labeling.get("num_keywords") is not None:
        args.num_keywords = int(labeling["num_keywords"])
    if args.max_snippets is None and labeling.get("max_snippets") is not None:
        args.max_snippets = int(labeling["max_snippets"])
    if args.max_snippets is None:
        args.max_snippets = 6
    if cfg.get("prompt_version") and "--prompt-version" not in sys.argv:
        args.prompt_version = str(cfg["prompt_version"])
    # YAML resume default must not override explicit --no-resume / --resume on CLI.
    if labeling.get("resume") is not None and "--no-resume" not in sys.argv and "--resume" not in sys.argv:
        args.resume = bool(labeling["resume"])
    if "--label-all-topics" not in sys.argv:
        args.label_all_topics = bool(labeling.get("label_all_topics", args.label_all_topics))
    if paths.get("quality_adjudication_jsonl") and args.quality_adjudication_jsonl is None:
        args.quality_adjudication_jsonl = Path(paths["quality_adjudication_jsonl"])
    if "skip_hard_exclude" in labeling and "--skip-hard-exclude" not in sys.argv:
        args.skip_hard_exclude = bool(labeling["skip_hard_exclude"])
    if "require_08a_pass" in labeling and "--require-08a-pass" not in sys.argv:
        args.require_08a_pass = bool(labeling["require_08a_pass"])


def main() -> None:
    """Main entry point for topic labeling with OpenRouter API."""
    args = parse_args()
    _apply_stage08_config_defaults(args)
    
    # Load configuration first to get logs directory
    try:
        paths_cfg = load_config(args.config)
        outputs = paths_cfg.get("outputs", {})
        logs_dir = resolve_path(Path(outputs.get("logs", "logs")))
    except Exception as e:
        # Fallback to default logs directory if config loading fails
        logs_dir = Path("logs")
        print(f"[LABELING_CMD] Warning: Could not load config: {e}")
        print(f"[LABELING_CMD] Using default logs directory: {logs_dir}")
    
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Set up logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"stage08_llm_labeling_{timestamp}.log"
    logger = setup_logging(logs_dir, log_file=log_file)
    logger.info("=" * 80)
    # logger.info("Stage 06: POS Topic Labeling with OpenRouter API (mistralai/mistral-nemo)")
    logger.info("Stage 08: POS Topic Labeling with OpenRouter API")
    logger.info("=" * 80)
    
    # Set up Tee to capture all print output to log file
    log_path = logs_dir / log_file
    stdout_tee = Tee(log_path, sys.stdout)
    stderr_tee = Tee(log_path, sys.stderr)
    
    try:
        # Set unbuffered mode for immediate output
        os.environ['PYTHONUNBUFFERED'] = '1'
        
        # Redirect stdout and stderr to Tee
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = stdout_tee
        sys.stderr = stderr_tee
        
        # Force immediate flush
        sys.stdout.flush()
        sys.stderr.flush()
        
        logger.info(f"[LABELING_CMD] Log file: {log_path}")
        logger.info(f"[LABELING_CMD] ========== Starting labeling command ==========")
        print("[LABELING_CMD] ========== Starting labeling command ==========")
        print("=" * 80)
        # print("Stage 06: POS Topic Labeling with OpenRouter API (mistralai/mistral-nemo)")
        print("Stage 08: POS Topic Labeling with OpenRouter API")
        print("=" * 80)
        print(f"[LABELING_CMD] Arguments:")
        print(f"[LABELING_CMD]   Embedding model: {args.embedding_model}")
        print(f"[LABELING_CMD]   Pareto rank: {args.pareto_rank}")
        print(f"[LABELING_CMD]   Base dir: {args.base_dir}")
        print(f"[LABELING_CMD]   Use native: {args.use_native}")
        print(f"[LABELING_CMD]   Model suffix: {args.model_suffix or '(none)'}")
        print(f"[LABELING_CMD]   Model stage: {args.model_stage or '(none)'}")
        print(f"[LABELING_CMD]   Num keywords: {args.num_keywords}")
        print(f"[LABELING_CMD]   Max tokens: {args.max_tokens}")
        print(f"[LABELING_CMD]   Output dir: {args.output_dir}")
        print(f"[LABELING_CMD]   Model name: {args.model_name}")
        print(f"[LABELING_CMD]   Temperature: {args.temperature}")
        print(f"[LABELING_CMD]   Batch size: {args.batch_size}")
        print(f"[LABELING_CMD]   No integrate: {args.no_integrate}")
        print(f"[LABELING_CMD]   Topics JSON: {args.topics_json} (for inspection/comparison)")
        print(f"[LABELING_CMD]   Limit topics: {args.limit_topics}")
        print(f"[LABELING_CMD]   Use improved prompts: {args.use_improved_prompts}")
        print(f"[LABELING_CMD]   Prompt version: {args.prompt_version}")
        print(f"[LABELING_CMD]   Quality CSV: {args.quality_csv}")
        print(f"[LABELING_CMD]   Representative docs CSV: {args.representative_docs_csv}")
        print(f"[LABELING_CMD]   Model dir: {args.model_dir}")
        print(f"[LABELING_CMD]   Resume: {args.resume}")
        print(f"[LABELING_CMD]   Rate limit delay: {args.rate_limit_delay}s")
        print()

        quality_hints = None
        adjudication_results = None
        if args.quality_csv and Path(args.quality_csv).is_file():
            quality_hints = load_topic_quality_hints(args.quality_csv)
            print(
                f"[LABELING_CMD] Loaded Stage07 hints for {len(quality_hints)} topics"
            )
            sys.stdout.flush()
        if args.quality_adjudication_jsonl and Path(args.quality_adjudication_jsonl).is_file():
            adjudication_results = load_quality_adjudication_results(
                args.quality_adjudication_jsonl
            )
            print(
                f"[LABELING_CMD] Loaded Stage08A adjudication for {len(adjudication_results)} topics"
            )
            sys.stdout.flush()
        print()

        # Step 1: Load BERTopic model
        print("[LABELING_CMD] Step 1: Loading BERTopic model...")
        sys.stdout.flush()
        wrapper = None
        if args.model_dir:
            model_dir = Path(args.model_dir)
            if not model_dir.is_dir():
                raise FileNotFoundError(f"Model directory not found: {model_dir}")
            topic_model = BERTopic.load(str(model_dir))
            print(f"[LABELING_CMD] ✓ Loaded BERTopic model from {model_dir}")
        else:
            wrapper, topic_model = load_bertopic_model(
                base_dir=args.base_dir,
                embedding_model=args.embedding_model,
                pareto_rank=args.pareto_rank,
                use_native=args.use_native,
                model_suffix=args.model_suffix,
                stage_subfolder=args.model_stage,
            )
            print(f"[LABELING_CMD] ✓ Loaded BERTopic model (use_native={args.use_native})")
        sys.stdout.flush()
        print()

        # Step 2: Extract POS topics from BERTopic model (primary source)
        print("[LABELING_CMD] Step 2: Extracting POS representation topics from BERTopic model...")
        sys.stdout.flush()
        try:
            pos_topics_dict = extract_pos_topics(
                topic_model=topic_model,
                top_k=args.num_keywords,
                limit=args.limit_topics,
            )
            limit_msg = f" (limited to {args.limit_topics})" if args.limit_topics else ""
            print(f"[LABELING_CMD] ✓ Extracted {len(pos_topics_dict)} topics from BERTopic model{limit_msg}")
            if quality_hints and not args.label_all_topics:
                before = len(pos_topics_dict)
                pos_topics_dict = filter_topics_dict(
                    pos_topics_dict,
                    quality_hints,
                    adjudication_results,
                    skip_hard_exclude=args.skip_hard_exclude,
                    require_08a_pass=args.require_08a_pass,
                    label_all_topics=False,
                )
                print(
                    f"[LABELING_CMD] Stage07/08A filter: {before} -> {len(pos_topics_dict)} topics for labeling"
                )
            sys.stdout.flush()
        except ValueError as e:
            print(f"[LABELING_CMD] ✗ Error: {e}")
            print("\n[LABELING_CMD] Hint: Run explore_retrained_model.py with --save-topics first")
            print("[LABELING_CMD]       to generate POS representation.")
            sys.stdout.flush()
            logger.error(f"[LABELING_CMD] Failed to extract POS topics: {e}")
            return
        print()
        
        # Step 2b: Optionally load from JSON for comparison/inspection
        json_topics_iter = None
        if args.topics_json:
            topics_json_path = args.topics_json
            if topics_json_path.exists():
                print(f"[LABELING_CMD] Step 2b: Loading topics from JSON for comparison/inspection: {topics_json_path}")
                sys.stdout.flush()
                try:
                    json_topics_iter = extract_pos_topics_from_json(
                        json_path=topics_json_path,
                        top_k=args.num_keywords,
                    )
                    # Convert iterator to dict for comparison
                    json_topics_dict = dict(json_topics_iter)
                    json_topics_iter = iter(json_topics_dict.items())  # Recreate iterator for later use
                    
                    # Compare sources
                    comparison = compare_topics_sources(pos_topics_dict, json_topics_dict)
                    print(f"[LABELING_CMD] Comparison results:")
                    print(f"[LABELING_CMD]   BERTopic topics: {comparison['bertopic_topics_count']}")
                    print(f"[LABELING_CMD]   JSON topics: {comparison['json_topics_count']}")
                    print(f"[LABELING_CMD]   Common topics: {comparison['common_topics']}")
                    print(f"[LABELING_CMD]   Keyword matches: {comparison['keyword_matches']}")
                    print(f"[LABELING_CMD]   Keyword differences: {comparison['keyword_differences']}")
                    if comparison['only_in_bertopic'] > 0:
                        print(f"[LABELING_CMD]   Only in BERTopic: {comparison['only_in_bertopic']}")
                    if comparison['only_in_json'] > 0:
                        print(f"[LABELING_CMD]   Only in JSON: {comparison['only_in_json']}")
                    sys.stdout.flush()
                    logger.info(f"[LABELING_CMD] Topics comparison: {comparison}")
                except Exception as e:
                    print(f"[LABELING_CMD] ✗ Warning: Could not load/compare JSON: {e}")
                    print("[LABELING_CMD] Continuing with BERTopic topics only...")
                    sys.stdout.flush()
                    logger.warning(f"[LABELING_CMD] Failed to load JSON for comparison: {e}")
            else:
                print(f"[LABELING_CMD] Step 2b: JSON file not found: {topics_json_path}")
                print("[LABELING_CMD] Skipping JSON comparison...")
                sys.stdout.flush()
        print()
        
        # Step 3: Initialize OpenRouter API client
        print("[LABELING_CMD] Step 3: Initializing OpenRouter API client...")
        print(f"[LABELING_CMD]   Model: {args.model_name}")
        print(f"[LABELING_CMD]   Base URL: https://openrouter.ai/api/v1")
        # Log API key status (masked for security)
        api_key_display = f"{args.api_key[:10]}...{args.api_key[-4:]}" if len(args.api_key) > 14 else "***"
        print(f"[LABELING_CMD]   API key: {api_key_display} ({'provided' if args.api_key else 'MISSING - using default'})")
        sys.stdout.flush()
        if not args.api_key or args.api_key == "":
            print("[LABELING_CMD] ⚠️  WARNING: No API key provided! Using default from environment or code.")
            print("[LABELING_CMD]   Set OPENROUTER_API_KEY environment variable or use --api-key flag")
            sys.stdout.flush()
        client, model_name = load_openrouter_client(
            api_key=args.api_key,
            model_name=args.model_name,
        )
        print(f"[LABELING_CMD] ✓ Initialized OpenRouter client for {model_name}")
        sys.stdout.flush()
        
        # Test API authentication before proceeding
        print("[LABELING_CMD] Testing API authentication...")
        sys.stdout.flush()
        auth_success = test_openrouter_authentication(client, model_name)
        if not auth_success:
            print("[LABELING_CMD] ✗ Authentication test FAILED")
            print("[LABELING_CMD]   Cannot proceed with label generation")
            print("[LABELING_CMD]   Please fix API key/account issues and try again")
            sys.stdout.flush()
            logger.error("[LABELING_CMD] Authentication test failed - aborting")
            return
        print(f"[LABELING_CMD] ✓ Authentication test passed")
        print(f"[LABELING_CMD]   Ready to generate labels via API")
        sys.stdout.flush()
        print()
        
        # Step 3b: Extract representative documents for snippets
        print("[LABELING_CMD] Step 3b: Extracting representative documents for snippets...")
        sys.stdout.flush()
        max_snippets = args.max_snippets
        topic_to_snippets = extract_representative_docs_per_topic(
            topic_model,
            max_docs_per_topic=max_snippets,
            fallback_csv=args.representative_docs_csv,
        )
        snippets_count = len([tid for tid, docs in topic_to_snippets.items() if docs])
        avg_snippets = sum(len(docs) for docs in topic_to_snippets.values()) / max(snippets_count, 1)
        print(f"[LABELING_CMD] ✓ Extracted representative docs for {snippets_count} topics")
        if snippets_count and args.representative_docs_csv and not getattr(
            topic_model, "representative_docs_", None
        ):
            print(
                f"[LABELING_CMD]   Source: compare-fit CSV fallback ({args.representative_docs_csv})"
            )
        print(f"[LABELING_CMD]   Average snippets per topic: {avg_snippets:.1f}")
        print(f"[LABELING_CMD]   Snippets will be included in prompts for better label precision")
        sys.stdout.flush()
        print()
        
        # Step 4: Generate labels from topics (use streaming if JSON available for memory efficiency)
        # Create model-specific filename with romance-aware suffix, model name, and reasoning effort
        model_name_safe = args.embedding_model.replace("/", "_").replace("\\", "_")
        model_name_file = model_name.replace("/", "_").replace(":", "_")
        reasoning_suffix = f"_reasoning_{args.reasoning_effort}" if args.reasoning_effort != "none" else ""
        limit_suffix = f"_limit{args.limit_topics}" if args.limit_topics else ""
        topic_ids_suffix = ""
        if args.topic_ids:
            topic_ids_suffix = "_topics"
        output_suffix = f"_{args.output_suffix}" if args.output_suffix else ""
        prompt_suffix = ""
        if args.prompt_version and args.prompt_version not in ("v2", "v2_multi_genre"):
            prompt_suffix = f"_{args.prompt_version.replace('/', '_')}"
        labels_filename = (
            f"labels_pos_openrouter_{model_name_file}_romance_aware_{model_name_safe}"
            f"{prompt_suffix}{output_suffix}{topic_ids_suffix}{reasoning_suffix}{limit_suffix}"
        )
        labels_path = args.output_dir / labels_filename

        topic_id_filter: set[int] | None = None
        if args.topic_ids:
            topic_id_filter = {int(x.strip()) for x in args.topic_ids.split(",") if x.strip()}
        if quality_hints and not args.label_all_topics:
            routing_ids = topic_ids_for_labeling(
                quality_hints,
                adjudication_results,
                skip_hard_exclude=args.skip_hard_exclude,
                require_08a_pass=args.require_08a_pass,
                label_all_topics=False,
            )
            topic_id_filter = (
                routing_ids
                if topic_id_filter is None
                else topic_id_filter & routing_ids
            )

        topic_to_representations = None
        if args.topics_json and args.topics_json.exists():
            topic_to_representations = load_all_representations_from_json(
                args.topics_json,
                top_k=args.num_keywords,
            )
            print(
                f"[LABELING_CMD] Loaded all keyword representations for "
                f"{len(topic_to_representations)} topics"
            )
            sys.stdout.flush()

        max_chars_per_snippet = 1200
        if args.stage08_config and Path(args.stage08_config).is_file():
            labeling_cfg = load_config(Path(args.stage08_config)).get("labeling", {})
            if labeling_cfg.get("max_chars_per_snippet") is not None:
                max_chars_per_snippet = int(labeling_cfg["max_chars_per_snippet"])
        # Debug: Log the full filename to verify it's not being truncated
        logger.info(f"[LABELING_CMD] Generated filename: {labels_filename} (length: {len(labels_filename)})")
        logger.info(f"[LABELING_CMD] Full path: {labels_path} (path length: {len(str(labels_path))})")
        
        # Use streaming mode if JSON file is provided (more memory-efficient)
        use_streaming = args.topics_json and args.topics_json.exists()
        reset_token_usage()
        
        if use_streaming:
            print(f"[LABELING_CMD] Step 4: Generating labels using STREAMING mode (memory-efficient, batch_size={args.batch_size})...")
            print("[LABELING_CMD]   Labels will be written incrementally to disk")
            print(f"[LABELING_CMD]   Using topics from JSON: {args.topics_json}")
            print(f"[LABELING_CMD]   Temperature: {args.temperature}")
            print(f"[LABELING_CMD]   Max tokens per label: {args.max_tokens}")
            sys.stdout.flush()
            # Recreate iterator from JSON for streaming
            pos_topics_iter = extract_pos_topics_from_json(
                json_path=args.topics_json,
                top_k=args.num_keywords,
            )
            topic_labels = generate_labels_streaming(
                pos_topics_iter=pos_topics_iter,
                client=client,
                model_name=model_name,
                output_path=labels_path,
                max_new_tokens=args.max_tokens,
                batch_size=args.batch_size,
                temperature=args.temperature,
                limit=args.limit_topics,
                use_improved_prompts=args.use_improved_prompts,
                topic_model=topic_model,
                topic_to_snippets=topic_to_snippets,
                max_snippets=max_snippets,
                max_chars_per_snippet=max_chars_per_snippet,
                reasoning_effort=args.reasoning_effort,
                prompt_version=args.prompt_version,
                quality_hints=quality_hints,
                resume=args.resume,
                rate_limit_delay_s=args.rate_limit_delay,
                topic_id_filter=topic_id_filter,
                topic_to_representations=topic_to_representations,
            )
            json_display_path = str(labels_path.parent) + "/" + labels_path.name + ".json"
            print(f"[LABELING_CMD] ✓ Labels already saved to {json_display_path}")
            sys.stdout.flush()
            print()
        else:
            print(f"[LABELING_CMD] Step 4: Generating labels for all topics (batch_size={args.batch_size})...")
            print(f"[LABELING_CMD]   Total topics to process: {len(pos_topics_dict)}")
            print(f"[LABELING_CMD]   Temperature: {args.temperature}")
            print(f"[LABELING_CMD]   Max tokens per label: {args.max_tokens}")
            print(f"[LABELING_CMD]   Rate limit delay: {args.rate_limit_delay}s between API calls")
            sys.stdout.flush()
            topic_labels = generate_all_labels(
                pos_topics=pos_topics_dict,
                client=client,
                model_name=model_name,
                max_new_tokens=args.max_tokens,
                batch_size=args.batch_size,
                temperature=args.temperature,
                use_improved_prompts=args.use_improved_prompts,
                topic_model=topic_model,
                topic_to_snippets=topic_to_snippets,
                reasoning_effort=args.reasoning_effort,
                prompt_version=args.prompt_version,
                quality_hints=quality_hints,
                rate_limit_delay_s=args.rate_limit_delay,
                topic_to_representations=topic_to_representations,
            )
            sys.stdout.flush()
            print()
            
            # Step 5: Save labels to JSON
            print("[LABELING_CMD] Step 5: Saving labels to JSON...")
            sys.stdout.flush()
            save_labels_openrouter(
                topic_data=topic_labels,
                output_path=labels_path,
            )
            # Use manual string construction to avoid truncation in display
            json_display_path = str(labels_path.parent) + "/" + labels_path.name + ".json"
            print(f"[LABELING_CMD] ✓ Saved labels to {json_display_path}")
            sys.stdout.flush()
            print()
        
        # Step 6: Always integrate labels into BERTopic model (unless --no-integrate is set)
        if not args.no_integrate:
            print("[LABELING_CMD] Step 6: Integrating labels into BERTopic model...")
            sys.stdout.flush()
            try:
                # Extract just the labels for BERTopic integration
                labels_only: dict[int, str] = {
                    topic_id: data["label"] 
                    for topic_id, data in topic_labels.items()
                }
                # Also pass full metadata (includes keywords, categories, etc.)
                integrate_labels_to_bertopic(
                    topic_model=topic_model,
                    topic_labels=labels_only,
                    topic_metadata=topic_labels,  # Full metadata dict
                )
                print("[LABELING_CMD] ✓ Labels integrated into BERTopic model")
                print("[LABELING_CMD]   (Labels will appear in BERTopic visualizations)")
                sys.stdout.flush()
                
                # Save model with LLM labels to stage08 subfolder (both formats)
                print("[LABELING_CMD] Step 7: Saving model with LLM labels to stage08_llm_labeling subfolder...")
                sys.stdout.flush()
                try:
                    import pickle
                    import shutil
                    from src.stage06_topic_exploration.explore_retrained_model import backup_existing_file, stage_timer
                    
                    # Create stage subfolder path
                    stage_subfolder = Path(args.base_dir) / args.embedding_model / "stage08_llm_labeling"
                    stage_subfolder.mkdir(parents=True, exist_ok=True)
                    
                    # Include model name in save path to avoid overwriting different LLM models
                    model_name_safe = model_name.replace("/", "_").replace(":", "_")
                    model_suffix = f"_with_llm_labels_{model_name_safe}"
                    
                    # 1. Save as native BERTopic model (directory format)
                    native_model_dir = stage_subfolder / f"model_{args.pareto_rank}{model_suffix}"
                    if native_model_dir.exists() and native_model_dir.is_dir():
                        shutil.rmtree(native_model_dir)
                    
                    with stage_timer(f"Saving native BERTopic model with LLM labels to {native_model_dir}"):
                        topic_model.save(str(native_model_dir))
                        logger.info("Saved native BERTopic model with LLM labels to %s", native_model_dir)
                    
                    # 2. Save as wrapper pickle (file format) - only if wrapper was loaded
                    if wrapper is not None:
                        wrapper_pickle_path = stage_subfolder / f"model_{args.pareto_rank}{model_suffix}.pkl"
                        backup_existing_file(wrapper_pickle_path)
                        
                        with stage_timer(f"Saving wrapper with LLM labels to {wrapper_pickle_path.name}"):
                            with open(wrapper_pickle_path, "wb") as f:
                                pickle.dump(wrapper, f)
                            logger.info("Saved wrapper with LLM labels to %s", wrapper_pickle_path)
                    else:
                        logger.info("Wrapper not available (loaded native model), skipping wrapper save")
                    
                    print(f"[LABELING_CMD] ✓ Saved model to {stage_subfolder}")
                    sys.stdout.flush()
                except Exception as e:
                    print(f"[LABELING_CMD] ⚠️  Warning: Could not save model: {e}")
                    print("[LABELING_CMD]   Labels are integrated but model was not saved")
                    sys.stdout.flush()
                    logger.warning(f"[LABELING_CMD] Failed to save model: {e}")
            except Exception as e:
                print(f"[LABELING_CMD] ✗ Error: Could not integrate labels: {e}")
                print("[LABELING_CMD]   Labels are saved to JSON file but NOT in model")
                sys.stdout.flush()
                logger.error(f"[LABELING_CMD] Failed to integrate labels: {e}")
                raise  # Re-raise since integration is important
        else:
            print("[LABELING_CMD] Step 6: Skipping BERTopic integration (--no-integrate flag set)")
            print("[LABELING_CMD] ⚠️  WARNING: Labels are NOT saved to model!")
            sys.stdout.flush()
            logger.warning("[LABELING_CMD] Labels not integrated into model (--no-integrate set)")
        print()
        
        # Summary
        print("=" * 80)
        print("[LABELING_CMD] Labeling Summary")
        print("=" * 80)
        # Extract labels count (topic_labels now contains dict with label and keywords)
        topics_count = len(topic_labels)
        print(f"[LABELING_CMD] Topics processed: {topics_count}")
        json_display_path = str(labels_path.parent) + "/" + labels_path.name + ".json"
        print(f"[LABELING_CMD] Labels saved to: {json_display_path}")
        if not args.no_integrate:
            print("[LABELING_CMD] Labels integrated into BERTopic: Yes")
        else:
            print("[LABELING_CMD] Labels integrated into BERTopic: No")
        usage = get_token_usage()
        if usage["requests"]:
            cost_usd = estimate_openrouter_cost(model_name, usage)
            per_topic = cost_usd / max(topics_count, 1)
            print(
                f"[LABELING_CMD] API usage: {usage['prompt_tokens']} prompt + "
                f"{usage['completion_tokens']} completion ({usage['requests']} requests)"
            )
            print(f"[LABELING_CMD] Est. API cost (OpenRouter list price): ${cost_usd:.4f}")
            print(f"[LABELING_CMD] Est. per topic: ${per_topic:.4f}")
            print(f"[LABELING_CMD] Est. full 330-topic run: ${per_topic * 330:.2f}")
        print(f"[LABELING_CMD] Log file: {log_path}")
        print("[LABELING_CMD] ========== labeling command completed ==========")
        sys.stdout.flush()
        logger.info(f"[LABELING_CMD] ========== labeling command completed ==========")
        logger.info(f"[LABELING_CMD] Log file saved to: {log_path}")
    
    finally:
        # Restore original stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        stdout_tee.close()
        stderr_tee.close()


if __name__ == "__main__":
    main()

