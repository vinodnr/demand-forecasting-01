# Production Hardening Checklist for LLM Provider Management & Monitoring Stack

1. Database & Migrations
   - Run migrations under a controlled release window; backup DB before applying.
   - Use migration tool with transactional migrations (e.g., Alembic) for safety.
   - Ensure roles and least-privilege for migration user; use a special migration role.

2. Secrets & Keys
   - Store secrets (OPENAI_API_KEY, GEMINI_API_KEY, GROK_API_KEY, DATABASE_URL, REDIS_URL) in a secrets manager (HashiVault, AWS Secrets Manager, GCP Secret Manager).
   - Do not commit secrets into repo or compose files. Use environment injection.

3. Redis & Cache
   - Use managed Redis (Cloud provider) or cluster + AUTH and TLS for production.
   - Configure eviction policy, monitor memory usage, and set appropriate TTLs.
   - Consider using a Redis namespace/prefix for metrics vs routing keys.

4. High Availability & Scaling
   - Run backend as multiple replicas behind a load balancer. Use shared Redis for cache coherence.
   - Use managed Postgres or high-availability replica set.
   - Use rate-limiting & quota management to protect LLM usage costs and providers.

5. Observability & Alerts
   - Ensure Prometheus scrapes are secured (mTLS or network ACLs) in production.
   - Configure alert routing to on-call with silences for maintenance windows.
   - Export traces & logs to a managed backend (Tempo, Jaeger, Datadog) and correlate traces with metrics.

6. Security & Governance
   - Enable RLS (Row Level Security) for tenant isolation if multi-tenant data is in same DB.
   - Audit all admin actions: include changed_by from authenticated admin user in `llm_changes_audit`.
   - Harden admin UI with RBAC and 2FA for admin accounts.

7. Provider Integration & Cost Controls
   - Use per-org quotas and rate limits; integrate quota checks in llm_manager or middleware.
   - Track usage per provider and alert on sudden spikes and monthly budget thresholds.
   - Consider dynamic provider switching / throttling under high-cost scenarios.

8. CI/CD & Releases
   - Run migrations as part of a release job with rollback plan.
   - Smoke-test admin APIs and provider resolution after deploy (use health checks and synthetic tests).
   - Tag releases and keep release notes highlighting DB changes.

9. Backup & Recovery
   - Regular DB backups and periodic restore drills.
   - Snapshot Redis where appropriate and set retention windows.

10. Compliance
   - Ensure logs and customer data handling comply with GDPR (data retention policies) and other regional regulations.
   - Maintain a data processing agreement and document provider data flow.

