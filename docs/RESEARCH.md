# Research

## Question
Which structure lets an AI app grow (new services, datasources, agents) without rewriting the
API layer?

## Scope
- In scope: backend template (FastAPI + OpenAI), datasource abstraction, health checks, prompt skills.
- Out of scope: front-end (`app/`), agents (only `BaseAgent` exists), deployment.

## Method
Layered design (see `NOTES.md`), checked by tests in `tests/` and a manual run against Postgres and
Milvus in Docker.
