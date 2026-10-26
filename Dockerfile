# Draft - not built or run yet
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# install dependencies first for better layer caching
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --extra datasources --no-install-project

COPY src ./src

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]
