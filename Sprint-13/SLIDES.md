# Slide 1 — Overview
**Demand Forecasting SaaS — Release (Sprints 0 → 13)**

- Multi-tenant forecasting platform: data upload → convert → forecast → insights
- Key features: secure uploads, tiered retention, LLM-driven insights, Trust UI (Transparency + DPA)
- Target audience: SMBs and enterprises needing demand forecasts

# Slide 2 — Architecture
**Architecture diagram** (visual suggested)

- Browser → Next.js frontend
- Backend API (FastAPI) on Hetzner servers (Docker)
- Neon Postgres (tenant data + RLS)
- Cloudflare R2 (object storage per region)
- Redis queue (jobs + rate limits)
- Background workers (conversion, delete, insights)

# Slide 3 — Security & Compliance
- GDPR support: Delete-user / Delete-org workflows, data residency view, DPA downloads
- SOC2-aligned controls: audit logs, role-based access scaffolds, TLS everywhere
- LLM privacy: prompt sanitizer + per-org metadata caching (no PII stored in prompts)

# Slide 4 — Deployment & Ops
- Dev: docker-compose.dev (Postgres, MinIO, Redis, worker)
- Prod: Hetzner servers + Cloudflare R2 + Neon Postgres (IaC skeleton prepared)
- CI: Jest unit tests, Playwright E2E, axe accessibility scans
- Monitoring: Prometheus + Grafana + Sentry (alerts for job failures & quota spikes)

# Slide 5 — Next steps & risks
**Next steps:**
- Deploy to dev and run full QA checklist (post-deploy tests)
- Harden JWT/JWKS production verification and secret rotation
- Decide Redis managed vs self-hosted and finalize Terraform
- Legal review of DPA & privacy pages

**Risks / Mitigations:**
- Operational overhead for self-hosted Redis — mitigate with managed service or Hetzner managed DB
- Data deletion/backups interplay — add retention policy doc & test deletion end-to-end
