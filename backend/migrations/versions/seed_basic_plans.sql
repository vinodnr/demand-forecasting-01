-- Seed basic plans (free/pro/business/enterprise)
INSERT INTO public.plans (id, name, tier, price_monthly_cents, created_at) VALUES (gen_random_uuid(), 'Free', 'free', 0, now()) ON CONFLICT DO NOTHING;
INSERT INTO public.plans (id, name, tier, price_monthly_cents, created_at) VALUES (gen_random_uuid(), 'Pro', 'pro', 1999, now()) ON CONFLICT DO NOTHING;
INSERT INTO public.plans (id, name, tier, price_monthly_cents, created_at) VALUES (gen_random_uuid(), 'Business', 'business', 4999, now()) ON CONFLICT DO NOTHING;
INSERT INTO public.plans (id, name, tier, price_monthly_cents, created_at) VALUES (gen_random_uuid(), 'Enterprise', 'enterprise', 19999, now()) ON CONFLICT DO NOTHING;
