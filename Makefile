.PHONY: help install test test-cov lint type-check format demo clean all

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install development dependencies
	pip install pytest pytest-cov mypy ruff

test:  ## Run tests without coverage
	PYTHONPATH=src pytest tests/ -v

test-cov:  ## Run tests with coverage report
	PYTHONPATH=src pytest tests/ -v --cov=ride_discount --cov-report=term-missing --cov-report=html

lint:  ## Run ruff linter
	ruff check src/ tests/

format:  ## Auto-fix linting issues
	ruff check --fix src/ tests/

type-check:  ## Run mypy type checker
	mypy --explicit-package-bases src/ride_discount

demo:  ## Run demo script
	python3 demo.py

clean:  ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete

all: clean lint type-check test-cov demo  ## Run all checks and demo
	@echo "✅ All checks passed!"
