PYTHON=python
VENV=.venv

.PHONY: help install venv train api dashboard realtime test test-unit test-integration test-qa clean logs docs

help:
	@echo "🧠 NLP Intelligence Platform - Make Targets"
	@echo ""
	@echo "Setup:"
	@echo "  make venv          Create virtual environment"
	@echo "  make install       Install dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make train         Train all models (sentiment, topics, extraction, KG)"
	@echo "  make api           Start FastAPI server (http://localhost:8000)"
	@echo "  make dashboard     Start Streamlit dashboard (http://localhost:8501)"
	@echo "  make realtime      Start real-time ingestion (continuous)"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all tests (pytest)"
	@echo "  make test-unit     Run unit tests only"
	@echo "  make test-integration Run integration tests (requires API running)"
	@echo "  make test-qa       Run QA test suite (requires API running)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         Clean up generated files and cache"
	@echo "  make logs          Tail application logs"
	@echo "  make docs          Open documentation"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-run    Run Docker container"
	@echo ""
	@echo "Full Workflow:"
	@echo "  make all           train + test (complete CI/CD)"
	@echo ""

venv:
	@echo "📦 Creating virtual environment..."
	python -m venv $(VENV)
	@echo "✓ Virtual environment created at $(VENV)"
	@echo "Activate with: source $(VENV)/bin/activate (Linux/Mac) or $(VENV)\\Scripts\\activate (Windows)"

install:
	@echo "📥 Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m spacy download en_core_web_sm
	@echo "✓ Dependencies installed"

train:
	@echo "🎓 Training models..."
	$(PYTHON) scripts/train.py
	@echo "✓ Model training complete"

api:
	@echo "🚀 Starting FastAPI server..."
	@echo "📡 Swagger docs: http://localhost:8000/docs"
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dashboard:
	@echo "📊 Starting Streamlit dashboard..."
	@echo "🌐 Dashboard: http://localhost:8501"
	$(PYTHON) -m streamlit run dashboard/streamlit_app.py

realtime:
	@echo "📡 Starting real-time ingestion (continuous)..."
	$(PYTHON) scripts/realtime_ingest.py --cycles 0 --interval_sec 120

test:
	@echo "🧪 Running all tests..."
	$(PYTHON) -m pytest tests/ -v --tb=short
	@echo "✓ Tests complete"

test-unit:
	@echo "🧪 Running unit tests..."
	$(PYTHON) -m pytest tests/test_*.py -v --tb=short -k "not integration"
	@echo "✓ Unit tests complete"

test-integration:
	@echo "⚙️ Running integration tests..."
	@echo "Note: Requires FastAPI running on http://localhost:8000"
	$(PYTHON) -m pytest tests/integration_test_suite.py -v --tb=short

test-qa:
	@echo "✅ Running QA test suite..."
	@echo "Note: Requires FastAPI running on http://localhost:8000"
	$(PYTHON) tests/qa_test_suite.py

all: train test
	@echo ""
	@echo "✅ Full workflow complete!"
	@echo "Next steps:"
	@echo "  1. Run API:       make api"
	@echo "  2. Run Dashboard: make dashboard"
	@echo "  3. Run Realtime:  make realtime"

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -r {} + 2>/dev/null || true
	find . -type d -name .streamlit -exec rm -r {} + 2>/dev/null || true
	find . -type f -name *.pyc -delete
	find . -type f -name .DS_Store -delete
	@echo "✓ Cleanup complete"

logs:
	@echo "📋 Tailing application logs..."
	@echo "(Press Ctrl+C to stop)"
	tail -f logs/app.log

docs:
	@echo "📖 Opening README..."
	@command -v open >/dev/null 2>&1 && open README.md || \
	@command -v xdg-open >/dev/null 2>&1 && xdg-open README.md || \
	@command -v start >/dev/null 2>&1 && start README.md || \
	echo "Please open README.md in your browser"

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t nlp-intelligence:latest .
	@echo "✓ Image built: nlp-intelligence:latest"

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8000:8000 \
	  -v $$(pwd)/models:/app/models \
	  -v $$(pwd)/logs:/app/logs \
	  -v $$(pwd)/data:/app/data \
	  nlp-intelligence:latest
	@echo "✓ Container running at http://localhost:8000"

.PHONY: help install venv train api dashboard realtime test test-unit test-integration test-qa clean logs docs docker-build docker-run all
