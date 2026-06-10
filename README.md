# Real-Time NLP Intelligence Platform

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production_API-009688)](#)
[![Docker](https://img.shields.io/badge/Docker-Compose_Ready-2496ED)](#)
[![CI](https://img.shields.io/badge/CI-Pytest-green)](#)
[![License](https://img.shields.io/badge/License-MIT-black)](#)

Production-style AI analytics platform for streaming text intelligence. The system ingests news or custom text, extracts sentiment, emotion, entities, topics, graph relationships, and realtime metrics, then exposes a grounded RAG analytics assistant through FastAPI and Streamlit.

## Live Demo

- API docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:8501`
- One-command stack: `docker compose up --build`

Screenshot placeholders:

| Dashboard | RAG Assistant | Metrics |
|---|---|---|
| `docs/screenshots/dashboard.png` | `docs/screenshots/rag_chat.png` | `docs/screenshots/metrics.png` |

## Why This Project Stands Out

- Real-time NLP pipeline with sentiment, emotion, entity extraction, topic modeling, knowledge graph analytics, and RSS ingestion.
- LLM-powered RAG assistant over processed analytics data, retrieved context, entities, topics, and recent news.
- Production engineering: FastAPI, Pydantic schemas, Docker Compose, PostgreSQL support, Redis-ready cache, Alembic migrations, structured request logging, health checks, and metrics endpoints.
- Recruiter-friendly dashboard with chat, live metrics cards, trend charts, entity ranking, and prediction explainability.
- Verified locally with a 62-test pytest suite.

## Architecture

![Architecture](docs/architecture.png)

Source diagram: [docs/architecture.mmd](docs/architecture.mmd)

```text
User Question
  -> FAISS Retriever
  -> Analytics Context Builder
  -> Groq/OpenAI/Ollama/Fallback LLM Provider
  -> Grounded Answer + Sources + Confidence
```

## Core Capabilities

- Sentiment analysis: TF-IDF + Logistic Regression / Multinomial Naive Bayes with model versioning.
- Emotion detection: transformer-ready pipeline with lexical fallback for reliable local demos.
- Context-aware recommendation engine: recommendations based on sentiment and emotion context.
- Information extraction: hybrid spaCy-compatible NER, regex rules, dictionary validation, and confidence scores.
- Knowledge graph: NetworkX entity relationships, centrality, path search, JSON/HTML export.
- Topic modeling: coherence-optimized LDA with versioned topic artifacts.
- Realtime ingestion: RSS/sample stream processing into SQLite or PostgreSQL.
- RAG assistant: FAISS retrieval, persisted vector store, explainable answers, provider fallback.
- Observability: model, API, RAG, cache, DB, CPU, RAM, uptime, and request latency metrics.

## Tech Stack

Python 3.11, FastAPI, Pydantic, scikit-learn, pandas, NumPy, NLTK, spaCy-compatible fallback, gensim, NetworkX, FAISS, sentence-transformers, Streamlit, SQLite, PostgreSQL, SQLAlchemy, Alembic, Redis, Docker, GitHub Actions.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/train.py
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

In another terminal:

```bash
python -m streamlit run dashboard/streamlit_app.py
```

Run ingestion:

```bash
python scripts/realtime_ingest.py --cycles 1
```

Run tests:

```bash
python -m pytest -q
```

## Docker Compose

```bash
docker compose up --build
```

Starts:

- FastAPI backend on `8000`
- Streamlit dashboard on `8501`
- PostgreSQL on `5432`
- Redis on `6379`

## RAG Analytics Assistant

Endpoint:

```http
POST /api/chat
Content-Type: application/json

{
  "query": "Why is tech sentiment negative today?",
  "k": 5
}
```

Response:

```json
{
  "answer": "Tech sentiment declined because retrieved records mention layoffs, regulation, and earnings pressure...",
  "sources_used": [
    {"id": 12, "source": "realtime_events", "score": 0.82}
  ],
  "confidence": 0.89,
  "retrieved_chunks": [],
  "provider": "groq",
  "latency_ms": 842.4
}
```

Provider order is configured with:

```bash
LLM_PROVIDER_ORDER=groq,openai,ollama,fallback
```

The platform runs without API keys by using the local extractive fallback.

## Metrics

| Endpoint | Purpose |
|---|---|
| `GET /api/metrics/models` | Accuracy, precision, recall, F1, model metadata |
| `GET /api/metrics/api` | Request counts, latency, throughput, error rate |
| `GET /api/metrics/rag` | Retrieval latency, LLM latency, confidence, top-k |
| `GET /api/system/status` | CPU, RAM, uptime, cache hit rate, DB health, component status |

See [BENCHMARKS.md](BENCHMARKS.md) for the benchmark report.

## API Examples

```bash
curl -X POST http://localhost:8000/api/sentiment ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Google cloud growth looks strong, but regulation risk is rising.\"}"
```

```bash
curl http://localhost:8000/api/realtime/metrics
curl http://localhost:8000/api/realtime/top-entities?limit=10
curl http://localhost:8000/api/graph/top
curl http://localhost:8000/api/system/status
```

## Project Structure

```text
app/
  main.py                  FastAPI app, CORS, middleware, health
  routes/                  API routes for NLP, RAG, realtime, metrics
  services/                ML, RAG, cache, LLM, graph, realtime services
  schemas/                 Pydantic request/response contracts
  utils/                   Config, logging, NLP fallback helpers
dashboard/                 Streamlit analytics dashboard
scripts/                   Training and realtime ingestion
tests/                     API and service tests
data/vector_store/         Persisted RAG documents and FAISS index
alembic/                   Database migrations
docs/                      Architecture diagrams and screenshots
```

## Deployment

Free deployment targets:

- Backend: Render or Railway
- Dashboard: Streamlit Cloud
- Database: Render/Railway PostgreSQL
- Cache: Redis add-on

Files included:

- `Dockerfile`
- `docker-compose.yml`
- `Procfile`
- `render.yaml`
- `.env.example`
- `deployment.md`
- `alembic/`

## Resume Bullets

- Built a production-style Real-Time NLP Intelligence Platform with FastAPI, Streamlit, scikit-learn, FAISS, SQLAlchemy, Redis-ready caching, and Docker Compose.
- Implemented an LLM-powered RAG analytics assistant that retrieves processed news, sentiment, entities, topics, and graph context to produce grounded answers with confidence and sources.
- Added observability with API latency, throughput, error rate, model metrics, RAG latency, cache hit rate, DB health, CPU/RAM usage, and uptime endpoints.
- Designed deployment-ready architecture with PostgreSQL compatibility, Alembic migrations, structured logging, health checks, and provider fallback across Groq, OpenAI, Ollama, and local extractive generation.

## Documentation

- [deployment.md](deployment.md)
- [MIGRATION_NOTES.md](MIGRATION_NOTES.md)
- [BENCHMARKS.md](BENCHMARKS.md)
- [CHANGELOG.md](CHANGELOG.md)

## License

MIT License.
