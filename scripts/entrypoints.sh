#!/usr/bin/env bash
# Run the API (src/) with fastapi-cli. Env: HOST (0.0.0.0), PORT (8000), RELOAD (set to 1 for dev reload).
set -euo pipefail
cd "$(dirname "$0")/.."

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

args=(run --entrypoint src:app --host "$HOST" --port "$PORT")
[[ "${RELOAD:-0}" == "1" ]] && args+=(--reload)

# inside the image the venv is already on PATH; locally go through uv
if command -v uv >/dev/null 2>&1 && [[ ! -x /app/.venv/bin/fastapi ]]; then
  exec uv run fastapi "${args[@]}"
fi
exec fastapi "${args[@]}"
