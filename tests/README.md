# tests/

Run with `make test` (pytest). The suite needs no network or database: the LLM is faked and
`/health` runs with no datasources configured. `conftest.py` provides a `client` fixture.
