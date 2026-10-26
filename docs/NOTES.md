# Decisions log

Newest at the top. Record *why*, not just *what*.

## 2026-10-26 - Layered backend, settings, tests
- `src/` layers: `routes/` -> `services/<name>/` -> `modules/` + `data/` + `utils/`;
  request/response schemas in `models/`. Why: routes stay thin; services compose reusable parts.
- Health is a `HealthModule` (registry of probes) so any source can be added later.
- Datasources (`data/`) are built from env at startup (lifespan); a failed connect is logged and shows
  as `degraded` in `/health` instead of stopping the API. Why: the API should stay inspectable.
- Settings via `pydantic-settings` (reads `.env`). Why: typed config, no manual `export`.
- OpenAI client is created lazily and `/chat` maps provider errors to 502. Why: the app can start
  without a key and clients get a clear error.
- Prompt skills live in `src/assets/skills/<name>/SKILL.md`, loaded by `SkillModule`.
- Milvus runs as standalone in Docker (pymilvus 3 rejects a local `.db` file URI); it is behind a
  compose profile because it is heavy.
- Verified against real Postgres 17 and Milvus 2.5.4 containers (`/health` ok). `Dockerfile` and the
  compose `app` service are drafts and have not been built.
