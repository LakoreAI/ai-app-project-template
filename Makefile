.PHONY: install run test lint fmt up down docker-build docker-push

install:
	uv sync --extra datasources

run:
	RELOAD=1 ./scripts/entrypoints.sh

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

docker-build:
	./scripts/docker-build.sh

docker-push:
	./scripts/docker-push.sh
