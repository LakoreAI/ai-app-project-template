#!/usr/bin/env bash
# Build the image. Env: IMAGE (ai-app-project-template), TAG (latest).
# Uses BuildKit, so dependency layers and the uv cache are reused between builds.
set -euo pipefail
cd "$(dirname "$0")/.."

IMAGE="${IMAGE:-ai-app-project-template}"
TAG="${TAG:-latest}"

DOCKER_BUILDKIT=1 docker build -t "${IMAGE}:${TAG}" "$@" .
echo "built ${IMAGE}:${TAG}"
