-- Migration: billing, plans, subscriptions, usage_records, invoices, plan_limits
BEGIN;

CREATE TABLE IF NOT EXISTS public.plans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  tier text NOT NULL,
  price_monthly_cents bigint NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.plan_limits (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  plan_id uuid REFERENCES public.plans(id) ON DELETE CASCADE,
  metric text NOT NULL, -- e.g., 'llm_tokens', 'datasets', 'monthly_forecasts'
  limit_value bigint NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.org_subscriptions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id uuid REFERENCES public.organizations(id),
  plan_id uuid REFERENCES public.plans(id),
  status text NOT NULL DEFAULT 'active', -- active, canceled, past_due
  started_at timestamptz DEFAULT now(),
  billing_cycle_anchor timestamptz DEFAULT now(),
  next_billing_at timestamptz NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.usage_records (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id uuid REFERENCES public.organizations(id),
  metric text NOT NULL,
  value numeric NOT NULL,
  metadata jsonb DEFAULT '{}'::jsonb,
  recorded_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.invoices (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id uuid REFERENCES public.organizations(id),
  amount_cents bigint NOT NULL,
  currency text NOT NULL DEFAULT 'usd',
  period_start timestamptz,
  period_end timestamptz,
  status text NOT NULL DEFAULT 'open', -- open, paid, failed
  external_invoice_id text NULL,
  created_at timestamptz DEFAULT now()
);

COMMIT;
