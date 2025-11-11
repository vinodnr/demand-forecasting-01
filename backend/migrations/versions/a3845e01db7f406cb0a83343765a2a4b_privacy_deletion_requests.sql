-- Migration: privacy deletion requests table
BEGIN;
CREATE TABLE IF NOT EXISTS public.privacy_deletion_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  reason text,
  status text DEFAULT 'requested',
  requested_at timestamptz DEFAULT now()
);
COMMIT;
