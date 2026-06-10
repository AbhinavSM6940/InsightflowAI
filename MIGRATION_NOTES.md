# Migration Notes

## SQLite to PostgreSQL

The platform remains SQLite-compatible by default. To use PostgreSQL:

1. Set `DATABASE_URL=postgresql+psycopg2://user:password@host:5432/db`.
2. Run `alembic upgrade head`.
3. Start the API and realtime ingestion normally.

The realtime query service and ingestion pipeline use SQLAlchemy when `DATABASE_URL` points to PostgreSQL. If the variable is absent or starts with `sqlite`, the existing SQLite path is preserved.

## RAG Vector Store

RAG artifacts are persisted in:

```text
data/vector_store/
```

Delete this folder to force a full rebuild from realtime records.

