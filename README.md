# ai-app-project-template

Template for Lakore's AI App Project: a FastAPI backend (`src/`) that calls the OpenAI API,
with optional Postgres and Milvus datasources, prompt skills, and room for a front-end in `app/`.

## Layout

```
.
├── src/             backend (see src/README.md)
├── app/             front-end, or code that calls src/
├── data/            local datasets
├── docs/            research docs, notes, analysis, reports (see docs/README.md)
├── notebooks/       exploration notebooks
├── tests/           pytest suite
├── scripts/         entrypoints.sh, docker-build.sh, docker-push.sh
├── Dockerfile       multi-stage image for the API
├── docker-compose.yml   Postgres, Milvus (profile), app (profile, draft)
└── Makefile         common commands
```

## Quick start

```
cp .env.example .env      # set OPENAI_API_KEY
make install              # uv sync --extra datasources
make run                  # http://127.0.0.1:8000/docs
```

Endpoints: `GET /health`, `POST /chat` (`{"prompt": "...", "skill": "summarize"}`; `skill` is optional).

## Configuration

Settings are read from the environment or `.env` (`src/config.py`):

| Variable | Default | Meaning |
|---|---|---|
| `OPENAI_API_KEY` | empty | OpenAI key (needed for `/chat`) |
| `OPENAI_MODEL` | `gpt-4o-mini` | model name |
| `POSTGRES_DSN` | empty | enables the Postgres datasource |
| `MILVUS_URI` | empty | enables the Milvus datasource |

## Datasources and Docker

```
make up                                        # Postgres on localhost:5433
docker compose --profile milvus up -d milvus   # Milvus on localhost:19530 (heavy)
docker compose --profile app up --build        # API in a container (draft)
```

Then set `POSTGRES_DSN=postgresql://app:app@localhost:5433/app` and
`MILVUS_URI=http://localhost:19530` in `.env`. `make down` stops everything.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/entrypoints.sh` | run `src/` (`HOST`, `PORT`, `RELOAD=1`); also the container's CMD |
| `scripts/docker-build.sh` | build the image (`IMAGE`, `TAG`) |
| `scripts/docker-push.sh` | tag and push to `IMAGE_REPO` (required, e.g. `ghcr.io/<org>/<image>`) |

The `Dockerfile` is multi-stage and ordered for layer caching, with a BuildKit cache mount for uv:
dependencies are installed before the code is copied, so editing `src/` rebuilds in about a second.
The `app` compose service is a draft.

## Development

```
make test    # pytest
make lint    # ruff check
make fmt     # ruff format + fix
```
