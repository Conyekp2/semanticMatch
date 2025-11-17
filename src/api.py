"""
FastAPI application for SemanticMatch.

Provides HTTP endpoints to:
- check API status (/ and /health)
- send a user query to /match with a chosen domain
- receive the top-K semantic FAQ matches with scores and confidence
"""

from functools import lru_cache
from typing import List, Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .data_loader import load_faq_json
from .matcher import SemanticMatcher


app = FastAPI(
    title="SemanticMatch API",
    description="A semantic FAQ matching engine for business support, HR, and education.",
    version="0.2.0",
)


VALID_DOMAINS = {"support", "hr", "education", "all"}


def normalize_domain(domain: Optional[str]) -> str:
    """
    Normalize and validate the domain.
    Falls back to 'all' if an unknown value is provided.
    """
    if domain is None:
        return "all"
    d = domain.strip().lower()
    if d in VALID_DOMAINS:
        return d
    return "all"


# --- Basic utility endpoints ---


@app.get("/", include_in_schema=False)
def root():
    """
    Simple welcome endpoint so that GET / does not return 404.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "SemanticMatch API is running.",
            "docs_url": "/docs",
            "endpoints": ["/match", "/health"],
        },
    )


@app.get("/health", include_in_schema=False)
def health():
    """
    Health-check endpoint typically used in production.
    """
    return {"status": "ok"}


# --- Request / response models for /match ---


class MatchRequest(BaseModel):
    query: str
    domain: Optional[str] = "all"  # support | hr | education | all
    top_k: Optional[int] = 3       # number of matches to return


class MatchItem(BaseModel):
    question: str
    answer: str
    score: float


class MatchResponse(BaseModel):
    domain: str
    best_score: float
    meets_threshold: bool
    matches: List[MatchItem]


# --- Cached matchers per domain ---


@lru_cache(maxsize=None)
def get_matcher(domain: str) -> SemanticMatcher:
    """
    Build and cache a SemanticMatcher for a given domain.

    This avoids reloading the JSON and recomputing embeddings
    on every /match request.
    """
    questions, answers = load_faq_json("data/samples/faq.json", domain=domain)
    return SemanticMatcher(questions, metadata=answers)


# --- Main matching endpoint ---


@app.post("/match", response_model=MatchResponse)
def match_faq(request: MatchRequest):
    """
    Match a user query against the FAQ dataset for a given domain.
    Returns the top-K matches.
    """
    domain = normalize_domain(request.domain)
    top_k = request.top_k or 3
    if top_k < 1:
        top_k = 1

    matcher = get_matcher(domain)
    result = matcher.match(request.query, top_k=top_k)

    items: List[MatchItem] = [
        MatchItem(
            question=m["question"],
            answer=m["metadata"],
            score=m["score"],
        )
        for m in result["matches"]
    ]

    return MatchResponse(
        domain=domain,
        best_score=result["best_score"],
        meets_threshold=result["meets_threshold"],
        matches=items,
    )