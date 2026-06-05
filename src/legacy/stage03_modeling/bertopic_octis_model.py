"""
BERTopic OCTIS Model Wrapper with Embeddings Support.

This module provides BERTopicOctisModelWithEmbeddings, a wrapper class that integrates
BERTopic with the OCTIS framework for hyperparameter optimization.

The class ensures embedding models are downloaded and cached locally before use.

Location: src/stage03_modeling/bertopic_octis_model.py
Reason: This module is specific to Stage 03 (Modeling) and is not used by other stages.
        It was moved from src/common/ to keep common/ for truly shared utilities.
"""

import os
import json
import traceback
import gc
from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np
import torch
import pprint
import re

# Import memory and thermal monitoring utilities
from src.legacy.stage03_modeling.memory_utils import (
    print_gpu_memory_usage, cleanup_gpu_memory, track_memory_peak,
    log_memory_usage, enforce_memory_limit
)
from src.common.thermal_monitor import ThermalMonitor

import gensim.corpora as corpora
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, PartOfSpeech
from bertopic.vectorizers import ClassTfidfTransformer
from octis.models.model import AbstractModel
from scipy.sparse import csr_matrix, issparse
from src.common.config import load_config, resolve_path

# Import GPU models (RAPIDS required)
try:
    from cuml.cluster import HDBSCAN
    from cuml.manifold import UMAP
    RAPIDS_AVAILABLE = True
except ImportError:
    RAPIDS_AVAILABLE = False
    raise ImportError(
        "RAPIDS (cuML) is required for BERTopicOctisModelWithEmbeddings. "
        "Install with: pip install cuml-cu12 --extra-index-url=https://pypi.nvidia.com"
    )


def get_embedding_model_cache_dir() -> str:
    """
    Get the local cache directory for embedding models.
    
    Models are downloaded and cached here to avoid re-downloading.
    Uses project root/cache/huggingface by default.
    
    Returns:
        Path to cache directory
    """
    cache_dir = os.path.join(os.getcwd(), "cache", "huggingface")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def load_embedding_model(
    model_name: str,
    device: Optional[str] = None,
    cache_folder: Optional[str] = None
) -> SentenceTransformer:
    """
    Load an embedding model, ensuring it's downloaded and cached locally.
    
    This function ensures models are downloaded to local cache before use,
    preventing them from being kept only in memory.
    
    Args:
        model_name: Name of the SentenceTransformer model (e.g., 'all-MiniLM-L12-v2')
        device: Device to load model on ('cuda' or 'cpu'). Auto-detects if None.
        cache_folder: Cache directory. Uses default if None.
        
    Returns:
        Loaded SentenceTransformer model (cached locally)
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    if cache_folder is None:
        cache_folder = get_embedding_model_cache_dir()
    
    # Set environment variables to ensure models are cached locally
    os.environ['TRANSFORMERS_CACHE'] = cache_folder
    os.environ['HF_HOME'] = cache_folder
    
    print(f"📥 Loading embedding model: {model_name}")
    print(f"   Device: {device}")
    print(f"   Cache folder: {cache_folder}")
    print(f"   (Model will be downloaded and cached locally if not already present)")
    
    # SentenceTransformer automatically downloads and caches models locally
    # when cache_folder is specified
    model = SentenceTransformer(model_name, device=device, cache_folder=cache_folder)
    
    print(f"   ✅ Model loaded and cached locally")
    
    return model


def create_representation_models():
    """
    Create representation models for BERTopic.
    
    Returns:
        Dictionary of representation models
    """
    keybert_model = KeyBERTInspired()
    pos_model = PartOfSpeech("en_core_web_sm")
    mmr_model = MaximalMarginalRelevance(diversity=0.3)
    
    return {
        "KeyBERT": keybert_model,
        "MMR": mmr_model,
        "POS": pos_model
    }


def load_custom_stopwords_from_config(verbose: bool = True) -> List[str]:
    """Load custom stopwords from paths.yaml and normalize to token-level entries."""
    token_re = re.compile(r"[A-Za-z][A-Za-z'-]*")
    try:
        paths_cfg = load_config(Path("configs/paths.yaml"))
        raw_path = paths_cfg.get("inputs", {}).get("custom_stoplist")
        if not raw_path:
            if verbose:
                print("[STOPWORDS] No inputs.custom_stoplist in configs/paths.yaml, using English stopwords only")
            return []

        stoplist_path = resolve_path(Path(raw_path))
        if not stoplist_path.exists():
            if verbose:
                print(f"[STOPWORDS] Custom stoplist not found at {stoplist_path}, using English stopwords only")
            return []

        tokens: set[str] = set()
        with open(stoplist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                for m in token_re.finditer(s.lower()):
                    tok = m.group(0).strip("'-")
                    if tok:
                        tokens.add(tok)

        if verbose:
            print(f"[STOPWORDS] Loaded {len(tokens):,} custom stopword token(s) from {stoplist_path}")
        return sorted(tokens)
    except Exception as e:
        if verbose:
            print(f"[STOPWORDS] Failed to load custom stoplist: {e}. Falling back to English-only stopwords.")
        return []


class BERTopicOctisModelWithEmbeddings(AbstractModel):
    """
    BERTopic model wrapper for OCTIS framework with pre-computed embeddings support.
    
    This class integrates BERTopic with OCTIS for hyperparameter optimization.
    It uses RAPIDS (cuML) for GPU-accelerated UMAP and HDBSCAN.
    
    The embedding model is loaded and cached locally before use to ensure
    models are downloaded to disk, not just kept in memory.
    
    Attributes:
        embedding_model: SentenceTransformer model (cached locally)
        embedding_model_name: Name of the embedding model
        embeddings: Pre-computed embeddings array
        dataset_as_list_of_strings: Dataset as list of sentence strings
        dataset_as_list_of_lists: Dataset as list of tokenized sentences
        hyperparameters: Default hyperparameters for BERTopic components
    """
    
    def __init__(
        self,
        embedding_model: SentenceTransformer,
        embedding_model_name: str,
        embeddings: np.ndarray,
        dataset_as_list_of_strings: List[str],
        dataset_as_list_of_lists: Optional[List[List[str]]] = None,
        optimization_results_dir: Optional[str] = None,
        verbose: bool = True,
        calculate_probabilities: bool = False,
        topic_filter_dictionary: Optional[Any] = None
    ):
        """
        Initialize BERTopicOctisModelWithEmbeddings.
        
        Args:
            embedding_model: SentenceTransformer model (should be loaded via load_embedding_model)
            embedding_model_name: Name identifier for the embedding model
            embeddings: Pre-computed embeddings array
            dataset_as_list_of_strings: Dataset as list of sentence strings
            dataset_as_list_of_lists: Dataset as list of tokenized sentences (auto-generated if None)
            optimization_results_dir: Directory for optimization results (optional)
            verbose: Enable verbose logging
            calculate_probabilities: Compute full document-by-topic probability matrices.
                Defaults to False: it is expensive at large document counts and is not
                needed for OCTIS coherence/diversity selection (outlier rate is read from
                hard topic labels). Enable only for a dedicated probability run.
            topic_filter_dictionary: Optional precomputed gensim ``Dictionary`` used to
                filter topic words when building the model output. Pass a dictionary built
                from the *fit* corpus so topics are not dropped because their words are
                absent from the (smaller) eval token set. When None, the filter dictionary
                is rebuilt from ``dataset_as_list_of_lists`` on every call (legacy behavior).
        """
        super().__init__()
        
        self.embedding_model = embedding_model
        self.embedding_model_name = embedding_model_name
        self.embeddings = embeddings
        self.calculate_probabilities = bool(calculate_probabilities)
        self.topic_filter_dictionary = topic_filter_dictionary
        self.dataset_as_list_of_strings = dataset_as_list_of_strings
        
        # Auto-generate tokenized list if not provided (skip for disk-backed doc stores).
        if dataset_as_list_of_lists is None:
            if isinstance(dataset_as_list_of_strings, list):
                self.dataset_as_list_of_lists = [
                    sentence.split() for sentence in dataset_as_list_of_strings
                ]
            else:
                self.dataset_as_list_of_lists = []
        else:
            self.dataset_as_list_of_lists = dataset_as_list_of_lists
        
        self.use_partitions = False
        self.optimization_results_dir = optimization_results_dir
        self.verbose = verbose
        
        # Initialize thermal monitor (optional, can be None)
        self.thermal_monitor = None
        if verbose:
            try:
                self.thermal_monitor = ThermalMonitor(alert_cpu=85.0, alert_gpu=80.0)
            except Exception as e:
                if self.verbose:
                    print(f"[MODEL_INIT] ⚠️ Could not initialize thermal monitor: {e}")
        
        # Default hyperparameters
        self.hyperparameters = {
            'umap': {
                'n_neighbors': 11,
                'n_components': 5,
                'min_dist': 0.05,
                'metric': 'cosine',
                'random_state': 42
            },
            'hdbscan': {
                'min_cluster_size': 150,
                'metric': 'euclidean',
                'cluster_selection_method': 'eom',
                'prediction_data': True,
                'gen_min_span_tree': True,
                'min_samples': 20
            },
            'vectorizer': {
                'stop_words': 'english',
                'min_df': 0.005,
                'ngram_range': (1, 1)
            },
            'tfdf_vectorizer': {
                'reduce_frequent_words': True,
                'bm25_weighting': True
            },
            'bertopic': {
                'language': "english",
                'top_n_words': 30,
                'n_gram_range': (1, 1),
                'min_topic_size': 127,
                'nr_topics': None,
                'low_memory': False,
                'calculate_probabilities': self.calculate_probabilities,
                'verbose': True
            }
        }
        
        if self.verbose:
            print(f"[MODEL_INIT] ✓ BERTopicOctisModelWithEmbeddings initialized")
            print(f"   Model: {embedding_model_name}")
            print(f"   Embeddings shape: {embeddings.shape}")
            print(f"   Dataset size: {len(dataset_as_list_of_strings):,} documents")
    
    def train_model(self, dataset, hyperparameters: Dict[str, Any] = None, top_words: int = 10) -> Dict[str, Any]:
        """
        Train BERTopic model with given hyperparameters.
        
        Args:
            dataset: OCTIS dataset (unused, kept for compatibility)
            hyperparameters: Dictionary of hyperparameters in format 'section__parameter'
            top_words: Number of top words per topic (unused, kept for compatibility)
            
        Returns:
            Dictionary with keys: 'topics', 'topic-word-matrix', 'topic-document-matrix'
        """
        if hyperparameters is None:
            hyperparameters = {}
        
        if self.verbose:
            print(f"[TRAIN] ========== Starting train_model() ==========")
            print(f"[TRAIN] Model: {self.embedding_model_name}")
            print(f"[TRAIN] Hyperparameters provided: {len(hyperparameters)} parameters")
            
            # Check GPU memory before training
            print(f"[TRAIN] Checking GPU memory before training...")
            mem_before = print_gpu_memory_usage("Pre-training Memory", verbose=True)
            
            # Log memory usage to file
            memory_log_file = Path("logs/memory_usage.jsonl")
            memory_log_file.parent.mkdir(parents=True, exist_ok=True)
            log_memory_usage(memory_log_file, f"Pre-training: {self.embedding_model_name}")
            
            # Enforce memory limit before training
            memory_sufficient, _ = enforce_memory_limit(required_gb=1.5, abort_on_insufficient=False)
            if not memory_sufficient:
                print(f"[TRAIN] ⚠️ WARNING: Low memory before training - may fail")
            
            # Check thermal status before training
            if self.thermal_monitor:
                thermal_status = self.thermal_monitor.get_status()
                if thermal_status['alerts']:
                    print(f"[TRAIN] ⚠️ WARNING: High temperatures detected before training:")
                    for alert in thermal_status['alerts']:
                        print(f"   {alert}")
                elif thermal_status['gpu_temp']:
                    print(f"[TRAIN] ✓ GPU temperature: {thermal_status['gpu_temp']:.1f}°C")
                
                # Check for throttling
                if thermal_status.get('throttling'):
                    print(f"[TRAIN] ⚠️ Thermal throttling detected: {thermal_status['throttling'][:80]}")
        
        # Check for existing results (for resume functionality)
        if self.optimization_results_dir:
            file_path = os.path.join(self.optimization_results_dir, self.embedding_model_name, 'result.json')
            if os.path.exists(file_path):
                if self.verbose:
                    print(f"[TRAIN] Found existing result file: {file_path}")
                # Note: Resume logic can be added here if needed
        
        # Set hyperparameters
        self.set_hyperparameters(hyperparameters)
        
        if self.verbose:
            print("[TRAIN] Hyperparameters:")
            pprint.pprint(self.hyperparameters)
        
        # Create representation models
        representation_model = create_representation_models()
        
        # Create GPU models using RAPIDS (required)
        if self.verbose:
            print("[TRAIN] Creating GPU UMAP model (RAPIDS)...")
        umap_model = UMAP(**self.hyperparameters['umap'])
        
        if self.verbose:
            print("[TRAIN] Creating GPU HDBSCAN model (RAPIDS)...")
        hdbscan_model = HDBSCAN(**self.hyperparameters['hdbscan'])
        
        if self.verbose:
            print("[TRAIN] Creating CountVectorizer...")
        vectorizer_params = self.hyperparameters["vectorizer"].copy()
        custom_stopwords = load_custom_stopwords_from_config(verbose=self.verbose)
        base_stop_words = vectorizer_params.get("stop_words", "english")
        if base_stop_words == "english" or base_stop_words is None:
            merged_stop_words = sorted(set(ENGLISH_STOP_WORDS).union(custom_stopwords))
        elif isinstance(base_stop_words, (list, set, tuple)):
            merged_stop_words = sorted(set(base_stop_words).union(custom_stopwords))
        else:
            merged_stop_words = sorted(set(ENGLISH_STOP_WORDS).union(custom_stopwords))
            if self.verbose:
                print(
                    f"[STOPWORDS] Unsupported stop_words={base_stop_words!r}; "
                    "falling back to English + custom stopwords"
                )
        vectorizer_params["stop_words"] = merged_stop_words
        if self.verbose:
            print(f"[TRAIN] CountVectorizer stopwords: {len(merged_stop_words):,} total")
        vectorizer_model = CountVectorizer(**vectorizer_params)
        
        if self.verbose:
            print("[TRAIN] Creating ClassTfidfTransformer...")
        tfdf_model = ClassTfidfTransformer(**self.hyperparameters['tfdf_vectorizer'])
        
        if self.verbose:
            print("[TRAIN] Creating BERTopic model instance...")
        topic_model = BERTopic(
            embedding_model=self.embedding_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            vectorizer_model=vectorizer_model,
            representation_model=representation_model,
            **self.hyperparameters['bertopic']
        )
        
        try:
            if self.verbose:
                print("[TRAIN] Starting fit_transform...")
                print(f"[TRAIN] Input documents: {len(self.dataset_as_list_of_strings):,}")
                print(f"[TRAIN] Embeddings shape: {self.embeddings.shape}")
                print(f"[TRAIN] Embeddings type: {type(self.embeddings)}")
                print("[TRAIN] This may take several minutes...")
            
            # Convert embeddings to numpy array if needed (e.g., if it's a CuPy array)
            # BERTopic requires numpy arrays, not CuPy arrays
            # Note: RAPIDS cuML (UMAP/HDBSCAN) will automatically transfer NumPy arrays to GPU
            # during fit_transform, so clustering operations run on GPU even with NumPy input
            if hasattr(self.embeddings, 'get'):  # CuPy array
                if self.verbose:
                    print("[TRAIN] Converting CuPy array to NumPy array...")
                embeddings_numpy = self.embeddings.get()
            elif not isinstance(self.embeddings, np.ndarray):
                if self.verbose:
                    print(f"[TRAIN] Converting {type(self.embeddings)} to NumPy array...")
                embeddings_numpy = np.asarray(self.embeddings)
            else:
                embeddings_numpy = self.embeddings
            
            # Validate embeddings shape
            if len(embeddings_numpy.shape) != 2:
                raise ValueError(f"Embeddings must be 2D array, got shape: {embeddings_numpy.shape}")
            if embeddings_numpy.shape[0] != len(self.dataset_as_list_of_strings):
                raise ValueError(
                    f"Embeddings first dimension ({embeddings_numpy.shape[0]}) must match "
                    f"number of documents ({len(self.dataset_as_list_of_strings)})"
                )
            
            if self.verbose:
                print(f"[TRAIN] Final embeddings shape: {embeddings_numpy.shape}, dtype: {embeddings_numpy.dtype}")
                print("[TRAIN] Note: RAPIDS cuML will automatically use GPU for UMAP and HDBSCAN clustering")
                # Log GPU memory before clustering to confirm GPU usage
                print_gpu_memory_usage("Pre-clustering GPU Memory", verbose=True)
            
            # Track memory peak during training
            # This includes GPU-accelerated UMAP dimensionality reduction and HDBSCAN clustering
            # RAPIDS cuML automatically transfers NumPy arrays to GPU during operations
            with track_memory_peak(f"BERTopic Training: {self.embedding_model_name}"):
                topics, probabilities = topic_model.fit_transform(
                    self.dataset_as_list_of_strings,
                    embeddings=embeddings_numpy
                )
            
            if self.verbose:
                print(f"[TRAIN] ✓ fit_transform completed")
                print(f"[TRAIN] Topics found: {len(set(topics)) - (1 if -1 in topics else 0)}")
                print(f"[TRAIN] Outliers: {sum(1 for t in topics if t == -1)}")
            
            # Enhanced GPU memory cleanup
            if self.verbose:
                print("[TRAIN] Performing GPU memory cleanup...")
            cleanup_result = cleanup_gpu_memory(verbose=self.verbose)
            
            # Log memory usage after training
            memory_log_file = Path("logs/memory_usage.jsonl")
            log_memory_usage(memory_log_file, f"Post-training: {self.embedding_model_name}")
            
            # Check thermal status after training
            if self.verbose and self.thermal_monitor:
                thermal_status = self.thermal_monitor.get_status()
                if thermal_status['alerts']:
                    print(f"[TRAIN] ⚠️ WARNING: High temperatures after training:")
                    for alert in thermal_status['alerts']:
                        print(f"   {alert}")
                elif thermal_status['gpu_temp']:
                    print(f"[TRAIN] ✓ GPU temperature after training: {thermal_status['gpu_temp']:.1f}°C")
                
                # Check for throttling
                if thermal_status.get('throttling'):
                    print(f"[TRAIN] ⚠️ Thermal throttling detected: {thermal_status['throttling'][:80]}")
            
            # Create output dictionary
            output_dict = {}
            output_dict['topics'] = []
            
            # Dictionary used to filter topic words. Prefer a precomputed dictionary
            # (built from the fit corpus) so topics are not dropped when their words
            # are absent from the smaller eval token set. Fall back to rebuilding from
            # the tokenized dataset for backward compatibility.
            dictionary = self.topic_filter_dictionary
            if dictionary is None:
                dictionary = (
                    corpora.Dictionary(self.dataset_as_list_of_lists)
                    if self.dataset_as_list_of_lists
                    else None
                )

            # Extract topic words
            num_topics = len(set(topics)) - (1 if -1 in topics else 0)
            for topic in range(num_topics):
                words = list(zip(*topic_model.get_topic(topic)))[0]
                if dictionary is not None:
                    words = [word for word in words if word in dictionary.token2id]
                words = [word for word in words if word.lower() != "mr"]
                words = [word for word in words if word.lower() != "ms"]
                output_dict['topics'].append(words)
            
            # Filter empty topic lists
            output_dict['topics'] = [words for words in output_dict['topics'] if len(words) > 0]
            
            if len(output_dict['topics']) == 0:
                output_dict['topics'] = None
            
            # Add matrices
            # Extract topic-word matrix (c-TF-IDF matrix)
            # According to BERTopic API: c_tf_idf_ is a csr_matrix (sparse matrix)
            # Reference: https://maartengr.github.io/BERTopic/api/bertopic.html
            topic_word_matrix = None
            
            # Try to access c_tf_idf_ directly (primary method per BERTopic API)
            if hasattr(topic_model, 'c_tf_idf_') and topic_model.c_tf_idf_ is not None:
                c_tf_idf = topic_model.c_tf_idf_
                # Handle sparse matrix (csr_matrix) - convert to dense array
                if issparse(c_tf_idf):
                    topic_word_matrix = c_tf_idf.toarray()
                    if self.verbose:
                        print(f"[TRAIN] Found c-TF-IDF matrix via c_tf_idf_ (sparse, shape: {c_tf_idf.shape})")
                else:
                    topic_word_matrix = np.array(c_tf_idf)
                    if self.verbose:
                        print(f"[TRAIN] Found c-TF-IDF matrix via c_tf_idf_ (dense, shape: {topic_word_matrix.shape})")
            elif hasattr(topic_model, 'ctfidf_model') and topic_model.ctfidf_model is not None:
                # Fallback: Access through ctfidf_model if available
                ctfidf = topic_model.ctfidf_model
                if hasattr(ctfidf, 'c_tf_idf_') and ctfidf.c_tf_idf_ is not None:
                    c_tf_idf = ctfidf.c_tf_idf_
                    if issparse(c_tf_idf):
                        topic_word_matrix = c_tf_idf.toarray()
                    else:
                        topic_word_matrix = np.array(c_tf_idf)
                    if self.verbose:
                        print(f"[TRAIN] Found c-TF-IDF matrix via ctfidf_model.c_tf_idf_")
                elif hasattr(ctfidf, 'matrix_') and ctfidf.matrix_ is not None:
                    matrix = ctfidf.matrix_
                    if issparse(matrix):
                        topic_word_matrix = matrix.toarray()
                    else:
                        topic_word_matrix = np.array(matrix)
                    if self.verbose:
                        print(f"[TRAIN] Found c-TF-IDF matrix via ctfidf_model.matrix_")
            
            # Validate the matrix
            if topic_word_matrix is None:
                if self.verbose:
                    print("[TRAIN] ⚠️ Warning: c-TF-IDF matrix not found")
                    print("[TRAIN] Checking available attributes on topic_model...")
                    # Check if model has been fitted
                    if not hasattr(topic_model, 'c_tf_idf_'):
                        print("[TRAIN] ⚠️ Model may not be fitted yet - c_tf_idf_ attribute missing")
                    else:
                        print(f"[TRAIN] c_tf_idf_ exists but is None or empty")
                    attrs = [attr for attr in dir(topic_model) if not attr.startswith('_') and ('tf' in attr.lower() or 'idf' in attr.lower() or 'matrix' in attr.lower())]
                    if attrs:
                        print(f"[TRAIN] Available relevant attributes: {attrs[:10]}")
                # Create empty matrix as fallback (shape will be ())
                topic_word_matrix = np.array([])
            elif topic_word_matrix.size == 0:
                if self.verbose:
                    print("[TRAIN] ⚠️ Warning: c-TF-IDF matrix is empty (size=0)")
                # Keep the empty matrix
            else:
                if self.verbose:
                    print(f"[TRAIN] ✓ c-TF-IDF matrix extracted successfully, shape: {topic_word_matrix.shape}")
            
            output_dict['topic-word-matrix'] = topic_word_matrix
            # Hard topic assignment per document; -1 marks outliers. Used for the
            # outlier rate so it does not depend on calculate_probabilities.
            output_dict['document-topics'] = np.asarray(topics)
            # Full probability matrix only exists when calculate_probabilities=True;
            # otherwise BERTopic returns None (kept for backward compatibility).
            output_dict['topic-document-matrix'] = (
                np.array(probabilities) if probabilities is not None else None
            )
            
            topics_out = output_dict["topics"]
            output_dict["n_topics"] = len(topics_out) if topics_out else 0

            if self.verbose:
                print(f"[TRAIN] ✓ Output created:")
                n_topics_out = output_dict["n_topics"]
                print(f"   Topics: {n_topics_out}")
                print(f"   Topic-word matrix shape: {output_dict['topic-word-matrix'].shape}")
                print(f"   Topic-document matrix shape: {output_dict['topic-document-matrix'].shape}")
            
            del topic_model
            return output_dict
            
        except Exception as ex:
            if self.verbose:
                print(f"[TRAIN] ❌ Training error: {ex}")
                print(traceback.format_exc())
            return {'topics': None}
    
    def set_hyperparameters(self, hyperparameters: Dict[str, Any]):
        """
        Set hyperparameters from flat dictionary.
        
        Args:
            hyperparameters: Dictionary with keys in format 'section__parameter'
                            (e.g., 'umap__n_neighbors', 'hdbscan__min_cluster_size')
        """
        for key, value in hyperparameters.items():
            if '__' in key:
                section, hyperparameter = key.split('__', 1)
                if section in self.hyperparameters and hyperparameter in self.hyperparameters[section]:
                    self.hyperparameters[section][hyperparameter] = value
                else:
                    if self.verbose:
                        print(f"⚠️  Warning: Parameter '{key}' not recognized.")
            else:
                if self.verbose:
                    print(f"⚠️  Warning: Parameter '{key}' does not match format 'section__hyperparameter'.")

