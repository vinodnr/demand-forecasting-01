# Security & Compliance Appendix — Sprint 13 summary

## GDPR & Data Protection
- Data deletion endpoints implemented (frontend + backend): `/v1/privacy/delete-request`, `/v1/privacy/delete-now/{user_id}`
- Delete-org workflow enqueued via `/v1/org/request-delete` and processed by delete_org_worker
- Audit logs table captures admin actions; Audit UI ensures tenant-scoped viewing (RLS required)

## SOC2 alignment (controls mapped)
- Access control: Role-based access scaffolds and admin UI for roles/permissions (Sprint-11)
- Logging & monitoring: Sentry init scaffold, Prometheus/Grafana provisioning notes (monitoring folder)
- Change management: Release notes and handover package (this Sprint-13) as operational artifact
- Data encryption: TLS recommended everywhere; rely on cloud provider-managed encryption for storage & DB
- Subprocessors: Subprocessor list placeholder in Privacy page; maintain updated list as part of DPA

## Operational controls
- Secrets: Use Secrets Manager or Vault in cloud; local dev uses env vars and docker-compose (not for production)
- Backups: Neon Postgres backups recommended; ensure backup retention policy does not conflict with GDPR deletion requests
- Key rotation: provide a rotation runbook (docs/ops/secret_rotation.md) — recommended next step

## Evidence & artifacts (where to find)
- Audit logs: backend/app/sql or `public.admin_audit` table and UI at `/app/trust/audit-logs`
- DPA & privacy: frontend/src/pages/legal/dpa.tsx and frontend/src/pages/legal/privacy.tsx (placeholders)
- Migrations: backend/migrations/versions/

