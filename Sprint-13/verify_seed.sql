-- verify_seed.sql
-- Run this inside your Postgres container or psql connected to your dev DB (demand_forecast)
-- This will show the seeded users and their org associations.
SELECT id, email, role, org_id, plan, is_active, created_at FROM users ORDER BY email;
SELECT id, name, plan, created_at FROM organizations ORDER BY plan;
SELECT org_id, storage_limit_bytes, created_at FROM org_quotas ORDER BY org_id;
