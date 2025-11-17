"""
Matching engine for SemanticMatch.

This module:
- stores known questions and their embeddings
- computes similarity with new queries
- returns the top-K best matches with scores
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .embeddings import EmbeddingEngine
from .config import MATCHING_CONFIG


class SemanticMatcher:
    def __init__(self, questions, metadata=None):
        """
        Initialize the matcher with a list of known questions.

        :param questions: list of strings (known questions / FAQ entries)
        :param metadata: optional list of metadata objects aligned with questions
                         (e.g., answers, IDs, tags)
        """
        if not questions:
            raise ValueError("You must provide at least one question to initialize SemanticMatcher.")

        self.questions = questions
        self.metadata = metadata or [None] * len(questions)

        if len(self.metadata) != len(self.questions):
            raise ValueError("metadata must have the same length as questions.")

        self.embedding_engine = EmbeddingEngine()
        self.question_embeddings = self.embedding_engine.encode(self.questions)

    def match(self, query: str, top_k: int = 3):
        """
        Find the top-K matching questions for the given query.

        Returns a dict with:
        - matches: list of {question, metadata, score}
        - best_score: float
        - meets_threshold: bool (based on best_score)
        """
        if top_k <= 0:
            raise ValueError("top_k must be >= 1")

        query_embedding = self.embedding_engine.encode(query)
        # cosine_similarity expects 2D arrays
        sims = cosine_similarity(query_embedding, self.question_embeddings)[0]

        # Get indices of top-K scores (sorted desc)
        top_k = min(top_k, len(self.questions))
        top_indices = np.argsort(sims)[-top_k:][::-1]

        matches = []
        for idx in top_indices:
            score = float(sims[idx])
            matches.append(
                {
                    "question": self.questions[int(idx)],
                    "metadata": self.metadata[int(idx)],
                    "score": score,
                }
            )

        best_score = matches[0]["score"] if matches else 0.0
        meets_threshold = best_score >= MATCHING_CONFIG.similarity_threshold

        return {
            "matches": matches,
            "best_score": best_score,
            "meets_threshold": meets_threshold,
        }