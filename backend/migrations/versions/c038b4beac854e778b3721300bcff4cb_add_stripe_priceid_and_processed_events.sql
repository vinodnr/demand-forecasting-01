-- Migration: add stripe_price_id to plans and processed_events (webhook idempotency)
BEGIN;
ALTER TABLE public.plans ADD COLUMN IF NOT EXISTS stripe_price_id text;
CREATE TABLE IF NOT EXISTS public.processed_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id text UNIQUE NOT NULL,
  event_type text,
  payload jsonb,
  processed_at timestamptz DEFAULT now()
);
COMMIT;
