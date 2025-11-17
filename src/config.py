"""
Project-wide configuration for SemanticMatch.

This file centralizes all important settings so we can
easily switch models or tune thresholds later.
"""

from dataclasses import dataclass


@dataclass
class EmbeddingConfig:
    model_name: str = "all-MiniLM-L6-v2"  # SentenceTransformers model
    normalize_embeddings: bool = True     # keep vectors on unit sphere for cosine similarity


@dataclass
class MatchingConfig:
    similarity_threshold: float = 0.3     # minimum similarity to accept a match (demo-friendly)


# Global config objects
EMBEDDING_CONFIG = EmbeddingConfig()
MATCHING_CONFIG = MatchingConfig()