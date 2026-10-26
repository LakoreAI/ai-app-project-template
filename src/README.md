# src/

The backend. `src/__init__.py` builds the FastAPI app (`create_app()`, exposed as `app`), mounts
`routes.api_router`, and in its lifespan creates and connects the datasources, registers their health
probes, and builds the chat service.

```
src/
├── __init__.py      app factory + lifespan
├── config.py        Settings (pydantic-settings, reads .env)
├── routes/          API routers; each route calls a service
├── services/        one folder per service: service.py + modules/ + utils/
├── models/          request/response schemas (pydantic)
├── modules/         shared building blocks (BaseModules, BaseAgent, HealthModule, SkillModule)
├── data/            datasources (DataSource, PostgresSource, MilvusSource, registry)
├── utils/           shared helpers (colored logger)
└── assets/          static files, e.g. prompt skills
```

## Flow

`routes/*` -> `services/<name>/service.py` -> `modules/` (shared) + `services/<name>/modules/` (local)
+ `data/` datasources + `utils/`.

## Adding a feature

1. Schemas in `models/<name>.py` (export them in `models/__init__.py`).
2. `services/<name>/service.py` with a service class; local modules and utils beside it.
3. `routes/<name>.py` with an `APIRouter` that calls the service; include it in `routes/__init__.py`.
4. If the service needs a datasource, pass it in from `src/__init__.py`; to monitor a new source, register a
   probe: `health.register("name", probe)`, where a probe raises when unhealthy.
5. Add a test under `tests/`.

## Datasources

`DataSource` has `connect()`, `ping()` and `close()`. `data/registry.py` builds the ones configured in
the environment (none, one or both). A failed connection is logged and shows up as `degraded` in
`/health`. The drivers are optional: `uv sync --extra datasources`.

## Logging

```python
from src.utils import get_logger

logger = get_logger(__name__)
```
