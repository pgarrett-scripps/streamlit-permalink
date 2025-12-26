.PHONY: help install install-dev install-docs test test-cov test-parallel lint format type-check clean build publish docs serve-docs pre-commit

# Default target
help:
	@echo "Available targets:"
	@echo "  install          - Install package in editable mode"
	@echo "  install-dev      - Install package with dev dependencies"
	@echo "  install-docs     - Install package with docs dependencies"
	@echo "  test             - Run tests"
	@echo "  test-cov         - Run tests with coverage report"
	@echo "  test-parallel    - Run tests in parallel"
	@echo "  lint             - Run pylint"
	@echo "  format           - Format code with black"
	@echo "  type-check       - Run mypy type checking"
	@echo "  clean            - Clean build artifacts"
	@echo "  build            - Build package distribution"
	@echo "  publish          - Publish package to PyPI"
	@echo "  docs             - Build documentation"
	@echo "  serve-docs       - Serve documentation locally"
	@echo "  pre-commit       - Run pre-commit hooks"

# Installation targets
install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[test]"
	uv pip install black pylint mypy pre-commit

install-docs:
	uv pip install -e ".[docs]"

# Testing targets
test:
	uv run pytest tests

test-cov:
	uv run pytest tests --cov=src/streamlit_permalink --cov-report=html --cov-report=term

test-parallel:
	uv run pytest tests -n auto

# Code quality targets
lint:
	uv run pylint src/streamlit_permalink

format:
	uv run black src tests examples

type-check:
	uv run ty check src/streamlit_permalink

# Clean targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build and publish targets
build: clean
	uv build

publish: build
	uv publish

# Documentation targets
docs:
	cd docs && uv run make html

serve-docs:
	cd docs/build/html && python -m http.server 8000

# Pre-commit targets
pre-commit:
	uv run pre-commit run --all-files
