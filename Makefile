.PHONY: test lint fmt

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run mypy src

fmt:
	uv run ruff format .
