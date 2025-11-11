-- backend/migrations/versions/aa9fb213a2504bf7923153aa8059a0bc_add_deleted_at.sql
BEGIN;
ALTER TABLE IF EXISTS public.datasets ADD COLUMN IF NOT EXISTS deleted_at timestamptz NULL;
ALTER TABLE IF EXISTS public.forecasts ADD COLUMN IF NOT EXISTS deleted_at timestamptz NULL;
COMMIT;
