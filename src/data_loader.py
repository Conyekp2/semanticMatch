"""
Data loading utilities for SemanticMatch.

This module loads FAQ-style data from JSON files.
"""

import json
from pathlib import Path
from typing import List, Tuple, Optional

from .preprocess import basic_clean


def load_faq_json(
    path: str = "data/samples/faq.json",
    domain: Optional[str] = None
) -> Tuple[List[str], List[str]]:
    """
    Load FAQ questions and answers from a JSON file.

    :param path: path to the JSON file
    :param domain: if provided, one of 'support', 'hr', 'education' or 'all'.
                   If None, all domains are loaded.
    :return: (questions, answers) lists aligned by index
    """
    json_path = Path(path)
    if not json_path.exists():
        raise FileNotFoundError(f"FAQ JSON file not found at: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions: List[str] = []
    answers: List[str] = []

    # Helper to add items from a single domain
    def add_domain_items(domain_key: str):
        entries = data.get(domain_key, [])
        for item in entries:
            q = basic_clean(item["question"])
            a = item["answer"]
            questions.append(q)
            answers.append(a)

    if domain is None or domain == "all":
        # Load all domains
        for key in data.keys():
            add_domain_items(key)
    else:
        if domain not in data:
            raise ValueError(f"Unknown domain '{domain}'. Expected one of: {list(data.keys())} or 'all'.")
        add_domain_items(domain)

    if not questions:
        raise ValueError("No questions were loaded from the FAQ JSON.")

    return questions, answers