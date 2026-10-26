.PHONY: install run test lint fmt up down

install:
	uv sync --extra datasources

run:
	uv run uvicorn src:app --reload

test:
	uv run pytest

lint:
	uv run ruff check .

fmt:
	uv run ruff format . && uv run ruff check --fix .

up:
	docker compose up -d postgres

down:
	docker compose --profile milvus --profile app down
