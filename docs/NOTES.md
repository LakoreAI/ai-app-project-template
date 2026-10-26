# Decisions log

Newest at the top. Record *why*, not just *what*.

## 2026-10-26 - Layered backend, settings, tests
- Services call shared modules in `src/modules/` (LLM, agents, health); they do not own a `modules/` folder.
- `src/` layers: `routes/` -> `services/<name>/` -> `modules/` + `data/` + `utils/`;
  request/response schemas in `models/`. Why: routes stay thin; services compose reusable parts.
- Health is a `HealthModule` (registry of probes) so any source can be added later.
- Datasources (`data/`) are built from env at startup (lifespan); a failed connect is logged and shows
  as `degraded` in `/health` instead of stopping the API. Why: the API should stay inspectable.
- Settings via `pydantic-settings` (reads `.env`). Why: typed config, no manual `export`.
- OpenAI client is created lazily and `/chat` maps provider errors to 502. Why: the app can start
  without a key and clients get a clear error.
- Each agent's prompt is `src/assets/prompt_templates/<agent>.md` (loaded by `BaseAgent`, no prompts in code).
- Skills live in `src/assets/skills/<name>/SKILL.md` and are part of agents: `BaseAgent` loads the skills
  it is given and builds its `system_prompt`. There is no standalone skill module; the chat service
  uses a `ChatAgent`, so `/chat` no longer takes a `skill` field.
- Milvus runs as standalone in Docker (pymilvus 3 rejects a local `.db` file URI); it is behind a
  compose profile because it is heavy.
- Verified against real Postgres 17 and Milvus 2.5.4 containers (`/health` ok). `Dockerfile` and the
  compose `app` service are drafts and have not been built.
