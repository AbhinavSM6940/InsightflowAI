# Metrics Benchmark Report

Baseline measured locally with `python -m pytest -q` on the existing test corpus.

## Test Health

- Test suite: 62 passing tests
- Coverage target: 80%+
- Areas covered: API contracts, services, sentiment edge cases, extraction, realtime analytics, graph traversal, RAG retrieval

## Runtime Metrics Exposed

- Model metrics: `GET /api/metrics/models`
- API latency and error rate: `GET /api/metrics/api`
- RAG retrieval and generation latency: `GET /api/metrics/rag`
- System diagnostics: `GET /api/system/status`

## Expected Local Performance

- Sentiment inference: tens of milliseconds for short text
- Retrieval: sub-100ms with local FAISS/hash fallback on small corpora
- RAG answer generation: provider dependent; local fallback is sub-second
- Dashboard refresh: 5-second polling interval

