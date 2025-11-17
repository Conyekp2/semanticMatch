<p align="center">
  <img src="https://raw.githubusercontent.com/Conyekp2/semanticMatch/main/logo.png" width="140" alt="SemanticMatch Logo"/>
</p>

<h1 align="center">SemanticMatch</h1>

<p align="center">
  <strong>AI-Powered Semantic FAQ Engine</strong><br>
  <span>Top-K retrieval • FastAPI • SentenceTransformers • Streamlit Web UI</span>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Ready-brightgreen" />
  <img src="https://img.shields.io/badge/Embeddings-MiniLM-orange" />
  <img src="https://img.shields.io/badge/Status-Active-blueviolet" />
</p>

---
SemanticMatch is a lightweight **semantic search engine** for business FAQs.  
It uses **SentenceTransformers embeddings**, **cosine similarity**, and a **FastAPI backend** to return the **Top-K closest FAQ questions and answers**.

It supports multiple use cases:

- **Customer support** (orders, payments, shipping)  
- **HR helpdesk** (leave, payslips, remote work)  
- **Education / EdTech** (courses, certificates, instructors)

A clean **Streamlit Web UI** is included for interactive testing.

---

# Features

- **Semantic matching**, not keyword search  
- **Top-K retrieval** with scores and confidence check  
- Multi-domain dataset (`support`, `hr`, `education`, `all`)  
- Configurable similarity threshold  
- Cached matchers per domain (fast repeated queries)  
- **FastAPI endpoint** with `/docs`  
- **Web UI** built in Streamlit  
- CLI demo for quick local testing  
- Clean production-style project structure

---

# How It Works

1. Questions + answers are stored in `data/samples/faq.json`.
2. `data_loader.py` loads the FAQ for the chosen domain.
3. `embeddings.py` computes dense vector embeddings with `SentenceTransformers`.
4. `matcher.py` computes **cosine similarity** and returns the Top-K results.
5. `api.py` exposes a `/match` API endpoint.
6. `ui/app.py` provides a Streamlit user interface.

---

# Architecture Diagram

```mermaid
flowchart TD
    A[User Question] --> B[Domain Selection]
    B --> C[Cached SemanticMatcher]
    C --> D[Embedding Engine | SentenceTransformers]
    D --> E[Cosine Similarity Ranking]
    E --> F[Top-K Matches | Confidence Score]
    F --> G[API or UI Response]
```
### Tech Stack
```bash
Python 3.10
SentenceTransformers (MiniLM)
NumPy
scikit-learn (cosine similarity)
FastAPI
Pydantic
Streamlit
Uvicorn
```
### Installation
```
git clone https://github.com/Conyekp2/semanticMatch.git
cd semanticMatch
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### CLI Demo (Top-K Search)
```
python3 demo_basic.py
You can:
  - choose a domain: support, hr, education, all
  - ask questions in natural language
  - get the Top-3 closest FAQ entries
```
### API Usage (FastAPI)
```
uvicorn src.api:app --reload --port 8000
Docs:
👉 http://127.0.0.1:8000/docs

Health check:
👉 http://127.0.0.1:8000/health
```
### Web UI Demo (Streamlit)
SemanticMatch includes a clean web interface for interactive testing.
#### Run the UI
```
streamlit run ui/app.py
👉 http://localhost:8501
```
#### UI Features
```
Select domain
Choose Top-K
Adjust similarity threshold
Real-time matching
Score visualization with progress bars
```
### Project Structure
```bash
semanticMatch/
│
├── src/
│   ├── api.py            # FastAPI app (/match, /health)
│   ├── config.py         # Model + matcher configuration
│   ├── embeddings.py     # Embedding engine (SentenceTransformers)
│   ├── matcher.py        # Cosine similarity + Top-K logic
│   ├── preprocess.py     # Basic text normalization
│   └── data_loader.py    # Load FAQ data from JSON
│
├── data/
│   └── samples/
│       └── faq.json      # Business multi-domain FAQ dataset
│
├── ui/
│   └── app.py            # Streamlit user interface
│
├── demo_basic.py         # CLI demo
├── requirements.txt
└── README.md
```
### About This Project
SemanticMatch was developed as an applied NLP project combining:
  - semantic search
  - transformer embeddings
  - API design
  - UX for knowledge retrieval
  - HR/Support/EdTech use cases

It is designed to demonstrate practical, production-ready NLP engineering.

⭐ If you find this project interesting, feel free to star the repo!