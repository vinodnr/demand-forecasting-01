#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Deploying Demand Forecasting (dev) from $ROOT_DIR"

# 1) Start dev compose
echo "Starting docker-compose.dev..."
cd "$ROOT_DIR/backend/monitoring"
docker compose -f docker-compose.dev.yml up -d --build

# 2) Wait for Postgres
echo "Waiting for Postgres to accept connections..."
until docker exec $(docker ps --filter "ancestor=postgres:15" -q | head -n1) pg_isready -U postgres > /dev/null 2>&1; do
  sleep 2
done

# 3) Run migrations (adjust path if you use Alembic or custom runner)
echo "Applying migrations..."
docker exec -it $(docker ps --filter "name=backend" -q | head -n1) bash -lc "python backend/migrations/run_migrations.py" || echo "Migration step might need manual invocation."

# 4) Start worker (if not run in compose)
echo "Starting worker (if not running in compose)..."
# docker exec -it <backend_container> bash -lc "python backend/workers/jobs.py &"

echo "Deployment steps completed. Visit http://localhost:3000/trust to verify Trust Center."
