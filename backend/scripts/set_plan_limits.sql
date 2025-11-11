-- Example inserts to set plan limits for llm_tokens per month
-- Replace PLAN_IDs with actual UUIDs from public.plans table after running seed
INSERT INTO public.plan_limits (id, plan_id, metric, limit_value, created_at)
VALUES (gen_random_uuid(), '<FREE_PLAN_ID>', 'llm_tokens', 100000, now())
ON CONFLICT DO NOTHING;

INSERT INTO public.plan_limits (id, plan_id, metric, limit_value, created_at)
VALUES (gen_random_uuid(), '<PRO_PLAN_ID>', 'llm_tokens', 1000000, now())
ON CONFLICT DO NOTHING;

INSERT INTO public.plan_limits (id, plan_id, metric, limit_value, created_at)
VALUES (gen_random_uuid(), '<BUSINESS_PLAN_ID>', 'llm_tokens', 10000000, now())
ON CONFLICT DO NOTHING;
