# Deployment Guide

## Local Production Stack

```bash
docker compose up --build
```

Tip: the backend container uses `python -m uvicorn` so it behaves the same on local shells, CI, and Docker.

Services:
- FastAPI: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Streamlit: http://localhost:8501
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Environment

Copy `.env.example` and configure provider keys as needed. The RAG assistant checks providers in this order by default:

1. Groq
2. OpenAI
3. Ollama
4. Local extractive fallback

## Database Migrations

SQLite works by default. PostgreSQL is enabled when `DATABASE_URL` points to a Postgres database.

```bash
alembic upgrade head
```

The app also creates the realtime table on startup for ingestion, so migrations are recommended for production but not required for local demos.

## Free Deployment

Backend: Render or Railway using `Procfile` or `render.yaml`.

Dashboard: Streamlit Cloud with:

```bash
streamlit run dashboard/streamlit_app.py
```

Set the dashboard Backend URL to the deployed API URL.

## Health Checks

- `/health` for load balancers
- `/api/system/status` for deep diagnostics
- `/api/metrics/api`, `/api/metrics/models`, `/api/metrics/rag` for monitoring
