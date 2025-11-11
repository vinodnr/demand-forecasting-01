#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
echo "Starting full dev setup from $ROOT"
docker compose -f backend/monitoring/docker-compose.dev.yml up -d --build
