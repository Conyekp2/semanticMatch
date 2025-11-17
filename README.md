<p align="center">
  <img src="https://raw.githubusercontent.com/Conyekp2/semanticMatch/main/logo.png" width="140" alt="SemanticMatch Logo"/>
</p>

<h1 align="center">SemanticMatch</h1>

<p align="center">
  <strong>AI-Powered Semantic FAQ Engine</strong><br>
  <span>Top-K retrieval • FastAPI • SentenceTransformers • Business-ready NLP</span>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Ready-brightgreen" />
  <img src="https://img.shields.io/badge/Embeddings-MiniLM-orange" />
  <img src="https://img.shields.io/badge/Status-Active-blueviolet" />
</p>

---
# SemanticMatch

SemanticMatch is a lightweight semantic matching engine for business FAQs, built with **Python**, **SentenceTransformers** and **FastAPI**.

It is designed to power:
- customer support assistants (FAQ, helpdesk),
- HR self-service portals,
- education / course support (student FAQs).

The engine takes a user question in natural language and returns the **closest matching FAQ question and answer**, using sentence embeddings and cosine similarity.

---

## ✨ Features

- 🔍 **Semantic matching**, not just keyword search  
- 📚 **Multi-domain support**: `support`, `hr`, `education`, or all combined  
- 📁 **JSON-based dataset** (`data/samples/faq.json`) for easy editing and extension  
- ⚙️ **Configurable** similarity threshold and embedding model  
- 🌐 **FastAPI endpoint** (`POST /match`) with interactive docs at `/docs`  
- 🧱 Clean, modular code structure (`src/embeddings.py`, `src/matcher.py`, `src/data_loader.py`, etc.)

---

## 🧠 How it works

1. FAQ data is stored in `data/samples/faq.json`, organized by domain:
   - `support` (orders, payments, shipping, etc.)
   - `hr` (leave, payslips, remote work, onboarding)
   - `education` (courses, grades, certificates, quizzes)

2. `src/data_loader.py` loads questions and answers from the JSON file and applies basic preprocessing.

3. `src/embeddings.py` uses a SentenceTransformers model (`all-MiniLM-L6-v2`) to convert questions into dense vector embeddings.

4. `src/matcher.py`:
   - stores embeddings for all known questions,
   - encodes the user query,
   - computes cosine similarity,
   - picks the best match and checks it against a configurable threshold.

5. `src/api.py` exposes a `POST /match` endpoint that:
   - accepts `query` and `domain`,
   - runs the matcher,
   - returns the best question, answer, similarity score and a `meets_threshold` flag.

---

## 🧰 Tech stack

- Python 3.10
- [sentence-transformers](https://www.sbert.net/)
- [NumPy](https://numpy.org/)
- [scikit-learn](https://scikit-learn.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- Pydantic

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/semanticMatch.git
cd semanticMatch
```
### 2. pip install -r requirements.txt
```bash
pip install -r requirements.txt
```
### 3. Run the CLI demo
```bash
python3 demo_basic.py
```
### 4. Run the API
```bash
uvicorn src.api:app --reload --port 8000
```
#### Open interactive docs:
```bash
http://127.0.0.1:8000/docs 
```
# Project structure
```bash
semanticMatch/
│
├── src/
│   ├── __init__.py
│   ├── api.py            # FastAPI app exposing /match
│   ├── config.py         # Model + matching configuration
│   ├── embeddings.py     # Embedding engine (SentenceTransformers)
│   ├── matcher.py        # Semantic matching logic (cosine similarity)
│   ├── preprocess.py     # Basic text normalization
│   └── data_loader.py    # Load FAQ data from JSON
│
├── data/
│   └── samples/
│       └── faq.json      # Multi-domain business FAQ dataset
│
├── demo_basic.py         # CLI demo for quick testing
├── requirements.txt
└── README.md



