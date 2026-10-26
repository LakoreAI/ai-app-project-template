# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# dependencies only: this layer is rebuilt just when pyproject.toml / uv.lock change
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --extra datasources --no-install-project

FROM python:3.12-slim
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1

COPY --from=builder /app/.venv /app/.venv
# code last: editing src/ does not invalidate the dependency layers
COPY src ./src
COPY scripts/entrypoints.sh ./scripts/entrypoints.sh

EXPOSE 8000
CMD ["./scripts/entrypoints.sh"]
