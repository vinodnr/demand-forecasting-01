#!/usr/bin/env bash
set -euo pipefail
echo "Sprint-8 Rollout Helper"
echo "This script will run migrations, apply RLS policies, and start backend in soft-mode."
read -p "Have you set DATABASE_URL env var? (y/N) " yn
if [[ "$yn" != "y" ]]; then
  echo "Set DATABASE_URL and re-run. Example:"
  echo "  export DATABASE_URL='postgres://USER:PASSWORD@HOST:PORT/driver-manager'"
  exit 1
fi
echo "Running migrations..."
bash backend/scripts/run_migrations.sh
echo "Applying RLS policies..."
psql "$DATABASE_URL" -f backend/migrations/rls_policies/rls_datasets.sql
psql "$DATABASE_URL" -f backend/migrations/rls_policies/rls_projects.sql
echo "Starting backend in soft-mode (PERMISSIONS_SOFT_MODE=1)..."
export PERMISSIONS_SOFT_MODE=1
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &
echo "Backend started (soft-mode). Tail logs to observe warnings."
