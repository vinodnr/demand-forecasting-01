#!/usr/bin/env bash
# Sprint-8 rollout commands (copy, replace placeholders, then run on staging machine)
# Replace placeholders: USER, PASSWORD, HOST, PORT, ADMIN_TOKEN, ROLE_UUID, ORG_ID, DATASET_ID

export DATABASE_URL="postgres://USER:PASSWORD@HOST:PORT/driver-manager"
echo "Using DATABASE_URL=$DATABASE_URL"

echo "==> Step 1: Run migrations & seeds"
bash backend/scripts/run_migrations.sh

echo "==> Verify tables and seeded roles"
psql "$DATABASE_URL" -c "\dt public.roles public.user_roles public.permission_templates public.role_audit public.service_accounts"
psql "$DATABASE_URL" -c "SELECT name FROM public.roles ORDER BY name;"

echo "==> Step 2: Apply RLS policies (review files before running)"
psql "$DATABASE_URL" -f backend/migrations/rls_policies/rls_datasets.sql
psql "$DATABASE_URL" -f backend/migrations/rls_policies/rls_projects.sql

echo "==> Step 3: Start backend in soft-mode (PERMISSIONS_SOFT_MODE=1)"
export PERMISSIONS_SOFT_MODE=1
# start backend (adjust to your deployment)
# uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &
echo "Started backend in soft-mode; tail logs to observe 'Soft-mode' warnings."

echo "==> Example admin API calls (replace ADMIN_TOKEN and ROLE_UUID)"
curl -s -H "X-Admin-Token: $ADMIN_TOKEN" http://localhost:8000/v1/admin/roles | jq .
curl -s -X POST -H "Content-Type: application/json" -H "X-Admin-Token: $ADMIN_TOKEN" \
  -d '{"role_id":"<ROLE_UUID>","resource":"projects","can_create":true,"can_read":true,"can_update":true,"can_delete":false}' \
  http://localhost:8000/v1/admin/permission_templates | jq .

echo "==> TIP: After tuning, flip enforcement:"
echo "export PERMISSIONS_SOFT_MODE=0 && systemctl restart your-backend.service"
