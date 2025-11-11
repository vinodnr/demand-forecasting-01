#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE=backend/monitoring/docker-compose.dev.yml
POSTGRES_SERVICE=postgres
DB_NAME=${DB_NAME:-demand_forecast}
PSQL_CMD="docker compose -f $COMPOSE_FILE exec -T $POSTGRES_SERVICE psql -U postgres -d $DB_NAME -c"

echo "Listing seeded users:"
eval $PSQL_CMD "\"SELECT id,email,role,org_id,plan,is_active,created_at FROM users ORDER BY email;\""

echo "\nListing organizations:"
eval $PSQL_CMD "\"SELECT id,name,plan,created_at FROM organizations ORDER BY plan;\""

echo "\nListing org quotas:"
eval $PSQL_CMD "\"SELECT org_id,storage_limit_bytes,created_at FROM org_quotas ORDER BY org_id;\""
