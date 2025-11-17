"""
Embedding module for SemanticMatch.

This module loads a SentenceTransformer model and provides
a simple function to encode text into embeddings.
"""

from sentence_transformers import SentenceTransformer
import numpy as np

from .config import EMBEDDING_CONFIG


class EmbeddingEngine:
    def __init__(self, model_name: str = None):
        """
        Load the embedding model.
        """
        model_name = model_name or EMBEDDING_CONFIG.model_name
        self.model = SentenceTransformer(model_name)
        self.normalize = EMBEDDING_CONFIG.normalize_embeddings

    def encode(self, texts):
        """
        Encode a single string or list of strings into embeddings.
        Returns numpy arrays.
        """
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(texts)

        if self.normalize:
            embeddings = self._normalize(embeddings)

        return np.array(embeddings)

    def _normalize(self, vectors):
        """
        Normalize vectors to unit length for stable cosine similarity.
        """
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms