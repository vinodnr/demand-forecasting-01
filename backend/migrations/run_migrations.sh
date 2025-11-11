#!/usr/bin/env bash
set -euo pipefail

if [ -z "${DATABASE_URL-}" ]; then
  echo "Error: DATABASE_URL must be set"
  exit 2
fi

PSQL="psql $DATABASE_URL -v ON_ERROR_STOP=1"

echo "Found migrations:"
echo "  - backend/migrations/versions/95ca046c300643febb4666ba82786140_add_billing_usage_tables.sql"
echo "  - backend/migrations/versions/c038b4beac854e778b3721300bcff4cb_add_stripe_priceid_and_processed_events.sql"
echo "  - backend/migrations/versions/f8c665133b214c41bb926762a84ad3cc_llm_provider_management.sql"
echo "  - backend/migrations/versions/seed_basic_plans.sql"
echo "  - backend/migrations/versions/seed_llm_providers_and_mappings.sql"

# Run migrations in lexical order
echo "Applying backend/migrations/versions/95ca046c300643febb4666ba82786140_add_billing_usage_tables.sql..."
$PSQL -f "backend/migrations/versions/95ca046c300643febb4666ba82786140_add_billing_usage_tables.sql"
echo "Applying backend/migrations/versions/c038b4beac854e778b3721300bcff4cb_add_stripe_priceid_and_processed_events.sql..."
$PSQL -f "backend/migrations/versions/c038b4beac854e778b3721300bcff4cb_add_stripe_priceid_and_processed_events.sql"
echo "Applying backend/migrations/versions/f8c665133b214c41bb926762a84ad3cc_llm_provider_management.sql..."
$PSQL -f "backend/migrations/versions/f8c665133b214c41bb926762a84ad3cc_llm_provider_management.sql"
echo "Applying backend/migrations/versions/seed_basic_plans.sql..."
$PSQL -f "backend/migrations/versions/seed_basic_plans.sql"
echo "Applying backend/migrations/versions/seed_llm_providers_and_mappings.sql..."
$PSQL -f "backend/migrations/versions/seed_llm_providers_and_mappings.sql"
echo "Migrations applied."
