# RELEASE NOTES — Demand Forecasting SaaS
Sprint bundle: Sprints 0 → 13 (including Sprint-12A Trust & Transparency)
Date: 2025-11-10

## High-level summary
This release contains the full Demand Forecasting SaaS MVP including:
- Multi-tenant data ingestion (presign + storage drivers: local, MinIO/R2)
- Upload conversion worker (Excel → CSV) with tier-aware retention
- Authentication middleware (JWT/JWKS scaffolding) and DB session-local wiring for RLS
- Quotas, rate-limiter scaffolds, and admin audit logging
- Delete-user and Delete-org workflows (UI + backend + worker scaffolds)
- LLM provider management skeleton, prompt sanitizer, and per-org LLM caching
- Trust & Transparency UI (public Trust Center, Transparency dashboard, Audit Logs, Data Residency, Retention UI)
- Dev tooling: docker-compose.dev, Redis, MinIO, PostgreSQL, worker orchestration, and CI scaffolds (Jest + Playwright + axe-playwright)

## Notable files & entry points
- Backend entry: backend/app/main.py (include routers and middleware)
- JWT middleware: backend/src/auth/jwt_middleware.py
- Storage drivers: backend/src/storage/driver.py, backend/src/storage/minio_driver.py, backend/src/storage/local_driver.py
- Presign API: backend/src/api/presign.py
- Convert worker & jobs: backend/workers/convert_worker.py, backend/workers/jobs.py
- Delete-org: backend/src/api/org_delete.py, backend/workers/delete_org_worker.py
- Privacy endpoints: backend/app/routers/privacy.py
- Quotas: backend/src/middleware/quotas.py and migration backend/migrations/versions/*_quotas_tables.sql
- Frontend trust UI: frontend/src/pages/trust/*, frontend/src/components/trust/*
- Dev compose: backend/monitoring/docker-compose.dev.yml
- Master ZIP: /mnt/data/demand_forecasting_master_sprints_0_13.zip

## Known caveats & TODOs (important)
- JWT/JWKS verification is scaffolded; verify with your identity provider JWKS and tune `verify_jwt` accordingly.
- Production hardening needed for security-definer functions, secret management, and background job reliability.
- DPA and Privacy policy pages use placeholder legal text; have legal review / replace with final legal documents before go-live.
- The CI accessibility axe step is configured as non-blocking by default; consider making it blocking after remediation is complete.
- Extensive testing (integration & E2E) is required in a dev environment before production deployment. You said you will run tests post-deploy to dev.

## Changelog by sprint (short)
- Sprint 0–4: Project scaffolding, DB schema, initial APIs, storage abstraction
- Sprint 5–8: LLM mapping design, admin UI pieces, quotas design, worker designs
- Sprint 9–11: Admin UI polish, roles & permission editor, email invites
- Sprint 12: Privacy endpoints, GDPR deletion requests, retention migration + privacy UI
- Sprint 12-A: Trust & Transparency frontend (public pages + app pages)
- Sprint 13 (this): Packaging, deployment docs, QA checklist, compliance appendix

