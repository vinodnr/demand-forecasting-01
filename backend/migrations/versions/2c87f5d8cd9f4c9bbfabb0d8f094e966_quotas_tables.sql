-- backend/migrations/versions/bddec5f778a343a3975355b4f283e2d7_quotas_tables.sql
BEGIN;
CREATE TABLE IF NOT EXISTS public.org_quotas (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id uuid NOT NULL UNIQUE,
  storage_bytes bigint DEFAULT 0,
  storage_limit bigint DEFAULT 0,
  api_calls bigint DEFAULT 0,
  api_limit bigint DEFAULT 0,
  updated_at timestamptz DEFAULT now()
);
-- seed example for a free org (adjust org_id)
-- INSERT INTO public.org_quotas (org_id, storage_limit, api_limit) VALUES ('00000000-0000-0000-0000-000000000000', 1073741824, 10000);
COMMIT;
