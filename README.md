# AI App Project Template: FastAPI + OpenAI + Postgres + Milvus (RAG-ready)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/LakoreAI/ai-app-project-template)](https://github.com/LakoreAI/ai-app-project-template/releases)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.162-009688.svg)

**ai-app-project-template** is an open-source, MIT-licensed Python starter for building AI applications
and LLM backends. It gives you a layered **FastAPI** service that calls the **OpenAI API**, optional
**PostgreSQL** and **Milvus** (vector database) datasources for RAG-style apps, agents with reusable prompt skills,
health checks, tests, and a fast-building **Docker** image, so you can start from a working structure
instead of an empty folder.

Current version: **v0.1.0** (first release). Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

## Features

- **Layered architecture**: `routes -> services -> modules / data / utils`, with request/response schemas in `models/`
- **LLM chat endpoint**: `POST /chat` calls OpenAI (default `gpt-4o-mini`) through a chat agent
- **Agents with prompts and skills**: each agent's prompt is a file in `src/assets/prompt_templates/`, and its skills are `SKILL.md` files in `src/assets/skills/`
- **Pluggable datasources**: Postgres and Milvus, enabled by environment variables (none, one or both)
- **Health checks**: `GET /health` runs a registry of probes; any datasource or provider can be added
- **Typed settings**: `pydantic-settings`, read from the environment or `.env`
- **Quality tooling**: pytest suite that needs no network or database, ruff lint and format, Makefile
- **Docker ready**: multi-stage Dockerfile with layer caching and a uv cache mount, plus docker-compose
- **fastapi-cli entrypoint**: the API runs with `fastapi run`, in the container and locally

## Tech stack

| Area | Choice |
|---|---|
| Web framework | FastAPI (run with fastapi-cli) |
| LLM provider | OpenAI Python SDK |
| Relational database | PostgreSQL (psycopg 3), optional |
| Vector database | Milvus (pymilvus), optional |
| Config and validation | pydantic, pydantic-settings |
| Packaging | uv, Python 3.12+ |
| Testing and linting | pytest, ruff |
| Containers | Docker (multi-stage, BuildKit), docker-compose |

## Quick start

```bash
git clone https://github.com/LakoreAI/ai-app-project-template.git
cd ai-app-project-template
cp .env.example .env      # set OPENAI_API_KEY
make install              # uv sync --extra datasources
make run                  # http://127.0.0.1:8000/docs
```

Try it:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is FastAPI?"}'
```

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | `{"status": "ok" or "degraded", "checks": {name: {ok, detail}}}` |
| `POST` | `/chat` | body `{"prompt": str}`, returns `{"answer": str}` |

`/chat` returns `502` when the LLM provider fails. Interactive docs are at `/docs`.

## Project structure

```
.
├── src/                 backend (see src/README.md)
│   ├── routes/          API routers; each route calls a service
│   ├── services/        one folder per service (service.py + utils/); it calls shared src/modules
│   ├── models/          request/response schemas
│   ├── modules/         shared building blocks (LLM, agents and their skills, health, base classes)
│   ├── data/            datasources (Postgres, Milvus)
│   ├── utils/           shared helpers (colored logger)
│   └── assets/          agent prompt templates and skills
├── app/                 front-end, or code that calls src/
├── data/                local datasets
├── docs/                research docs, notes, analysis, reports
├── notebooks/           exploration notebooks
├── tests/               pytest suite
├── scripts/             entrypoints.sh, docker-build.sh, docker-push.sh
├── Dockerfile           multi-stage image for the API
├── docker-compose.yml   Postgres, Milvus (profile), app (profile, draft)
└── Makefile             common commands
```

## Configuration

Settings are read from the environment or `.env` (`src/config.py`):

| Variable | Default | Meaning |
|---|---|---|
| `OPENAI_API_KEY` | empty | OpenAI key (needed for `/chat`) |
| `OPENAI_MODEL` | `gpt-4o-mini` | model name |
| `POSTGRES_DSN` | empty | enables the Postgres datasource |
| `MILVUS_URI` | empty | enables the Milvus datasource |

## Run with Docker

```bash
make up                                        # Postgres on localhost:5433
docker compose --profile milvus up -d milvus   # Milvus on localhost:19530 (heavy)
docker compose --profile app up --build        # API in a container (draft)
```

Then set `POSTGRES_DSN=postgresql://app:app@localhost:5433/app` and
`MILVUS_URI=http://localhost:19530` in `.env`. `make down` stops everything.

The `Dockerfile` is multi-stage and ordered for layer caching, with a BuildKit cache mount for uv:
dependencies are installed before the code is copied, so editing `src/` rebuilds in about a second.

| Script | Purpose |
|---|---|
| `scripts/entrypoints.sh` | run the API with fastapi-cli (`HOST`, `PORT`, `RELOAD=1`); also the container's CMD |
| `scripts/docker-build.sh` | build the image (`IMAGE`, `TAG`) |
| `scripts/docker-push.sh` | tag and push to `IMAGE_REPO` (required, e.g. `ghcr.io/<org>/<image>`) |

## Development

```bash
make test    # pytest
make lint    # ruff check
make fmt     # ruff format + fix
```

To add a feature, create `models/<name>.py`, `services/<name>/service.py` and `routes/<name>.py`, then
include the router in `src/routes/__init__.py`. Details are in [src/README.md](src/README.md).

## FAQ

### What is this template for?
Starting an LLM-powered backend with a clean structure: an API layer, services, datasources, prompt
skills, health checks, tests and Docker already wired together.

### Does it support RAG (retrieval-augmented generation)?
It provides the building blocks: a Milvus vector datasource, a Postgres datasource, an
`answer-with-sources` skill for agents and a service layer to compose them. A retrieval pipeline is not included yet.

### Can I use a different LLM provider?
The OpenAI call is isolated in `src/modules/llm.py`, so you can replace that module with
another provider's client.

### Do I need Postgres or Milvus to run it?
No. Both are optional; with neither configured, the API starts and `/health` reports `ok` with no checks.

### How do I add a skill to an agent?
Create `src/assets/skills/<name>/SKILL.md` (YAML frontmatter with `name` and `description`, then the
instructions) and list its name in the agent's `skills`, e.g. `ChatAgent(skills=["summarize"])`.

### Is it production ready?
It is a first release (v0.1.0) meant as a starting point. The Docker `app` service and the image push
destination are drafts, and there is no authentication, rate limiting or retrieval pipeline yet.

## License

MIT. See [LICENSE](LICENSE).
