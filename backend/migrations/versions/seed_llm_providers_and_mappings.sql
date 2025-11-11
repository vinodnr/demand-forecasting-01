-- Seed llm_providers and default plan_llm_map mappings
INSERT INTO public.llm_providers (provider_key, display_name, config)
VALUES ('openai', 'OpenAI', jsonb_build_object('default_model','gpt-4o-mini', 'notes','OpenAI provider')) ON CONFLICT (provider_key) DO NOTHING;

INSERT INTO public.llm_providers (provider_key, display_name, config)
VALUES ('gemini', 'Gemini', jsonb_build_object('default_model','gemini-pro', 'notes','Gemini provider')) ON CONFLICT (provider_key) DO NOTHING;

INSERT INTO public.llm_providers (provider_key, display_name, config)
VALUES ('grok', 'Grok (xAI)', jsonb_build_object('default_model','grok-1', 'notes','Grok provider - check availability')) ON CONFLICT (provider_key) DO NOTHING;

-- Default mapping: free->gemini, pro->gemini, business->openai, enterprise->openai
-- This assumes public.plans has rows with tier values; adjust plan_id lookup as needed.
INSERT INTO public.plan_llm_map (plan_id, provider_key)
SELECT p.id, CASE p.tier WHEN 'free' THEN 'gemini' WHEN 'pro' THEN 'gemini' WHEN 'business' THEN 'openai' WHEN 'enterprise' THEN 'openai' END
FROM public.plans p
WHERE p.tier IN ('free','pro','business','enterprise')
ON CONFLICT DO NOTHING;
