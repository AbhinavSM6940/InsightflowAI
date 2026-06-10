# Resume Notes

## Project Title

AI Text Intelligence & Emotional Insight Platform

## One-Line Description

Built a production-style NLP analytics platform that exposes sentiment, emotion, entity extraction, topic modeling, knowledge graph, realtime stream analytics, and wellness recommendations through FastAPI and Streamlit.

## Resume Bullets

- Developed a modular NLP platform with FastAPI, Pydantic, scikit-learn, NetworkX, gensim, FAISS, SQLite, and Streamlit to analyze text across sentiment, emotion, entities, topics, graphs, and realtime metrics.
- Implemented model training/versioning, coherence-optimized topic modeling, hybrid entity extraction, RAG-style document retrieval, and TTL-cached realtime analytics over live RSS/sample streams.
- Added production-readiness features including Docker packaging, GitHub Actions CI, health/system diagnostics, structured YAML configuration, test coverage, and deployment documentation.
- Improved model reliability with lexical confidence calibration for low-data sentiment inference and verified behavior with a 62-test pytest suite.

## Interview Talking Points

- Why the service layer is separated from routes, and how that keeps API contracts independent from model implementation.
- How fallback NLP components keep the app runnable when heavyweight local models are unavailable.
- How the realtime pipeline stores processed records in SQLite, then serves cached aggregate metrics to reduce repeated query work.
- How generated models, logs, local DBs, and caches are excluded from source control for a cleaner production repository.

