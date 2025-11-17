"""
Basic text preprocessing for SemanticMatch.

Here we keep things intentionally simple:
- lowercase
- strip whitespace

You can extend this later with more advanced normalization
(removing punctuation, accents, etc.) depending on your use case.
"""

import re


def basic_clean(text: str) -> str:
    """
    Apply very simple normalization to the input text.
    """
    if not isinstance(text, str):
        raise TypeError("basic_clean expects a string.")

    # Lowercase and strip spaces
    cleaned = text.strip().lower()

    # Optionally: collapse multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned