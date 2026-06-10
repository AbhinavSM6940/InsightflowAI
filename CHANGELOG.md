# Changelog

## Added

- LLM-powered RAG Analytics Assistant with `POST /api/chat`.
- Pluggable LLM providers for Groq, OpenAI, Ollama, and local fallback generation.
- Persistent FAISS vector store under `data/vector_store/`.
- API, model, RAG, and system metrics endpoints.
- PostgreSQL and Redis deployment support with Docker Compose.
- Alembic migration scaffold for realtime analytics storage.
- Streamlit RAG chat interface, live metrics cards, and explainability panel.
- Deployment files for Render/Railway-style hosting.

## Improved

- Renamed product positioning to Real-Time NLP Intelligence Platform.
- Upgraded system status with CPU, RAM, uptime, cache, DB, API, and RAG metrics.
- Added structured request logging with endpoint, latency, status code, and timestamp.
- Made dashboard API handling match actual backend response contracts.

## Refactored

- Added service registry for shared RAG and realtime query services.
- Added SQLAlchemy ORM model for realtime events while preserving SQLite compatibility.
- Introduced LLM provider abstraction to avoid vendor lock-in.

## Performance Gains

- Added persisted vector index to avoid rebuilding retrieval state every run.
- Added Redis-ready cache abstraction with in-memory fallback.
- Exposed latency metrics to measure API and RAG bottlenecks.

