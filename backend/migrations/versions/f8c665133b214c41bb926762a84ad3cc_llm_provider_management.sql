-- Migration: LLM provider management tables
BEGIN;

CREATE TABLE IF NOT EXISTS public.llm_providers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  provider_key text UNIQUE NOT NULL, -- e.g., 'openai', 'gemini', 'grok'
  display_name text NOT NULL,
  config jsonb DEFAULT '{}'::jsonb, -- provider-specific metadata like default_model, api_host, price_per_token_cents
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.plan_llm_map (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  plan_id uuid REFERENCES public.plans(id) ON DELETE CASCADE,
  provider_key text NOT NULL, -- must match llm_providers.provider_key
  created_at timestamptz DEFAULT now(),
  UNIQUE(plan_id, provider_key)
);

CREATE TABLE IF NOT EXISTS public.org_llm_override (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id uuid REFERENCES public.organizations(id),
  provider_key text NOT NULL,
  reason text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.llm_changes_audit (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id uuid NULL,
  plan_id uuid NULL,
  old_provider text NULL,
  new_provider text NULL,
  changed_by uuid NULL, -- admin user id
  reason text NULL,
  created_at timestamptz DEFAULT now()
);

COMMIT;
