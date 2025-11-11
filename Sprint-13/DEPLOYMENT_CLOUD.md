# Deployment Guide — Cloud (AWS EC2 + Cloudflare R2 + Neon Postgres)
This guide provides a high-level deployment plan for production using AWS EC2 for app hosts,
Cloudflare R2 for object storage, and Neon Postgres (serverless) for the DB.

Architecture overview:
- App servers: one or more EC2 instances behind an autoscaling group and ALB (or containerized on ECS/Fargate)
- DB: Neon Postgres (managed); ensure RLS, extensions, and roles are provisioned
- Object storage: Cloudflare R2 buckets per region (US/EU)
- Cache/Queue: Redis (managed, e.g., Elasticache or Upstash) for job queue and rate-limiting
- Background workers: run as separate ECS tasks or systemd services on EC2 (process jobs and run purge cron)
- Secrets: stored in AWS Secrets Manager or HashiCorp Vault; rotate keys and use environment variable injection at deploy time
- Monitoring: Prometheus + Grafana, Sentry, and alerting rules for job failures and quota spikes

High-level steps
1. Infrastructure (IaC recommended: Terraform)
   - Provision Neon Postgres DB and create roles, networks (VPC peering if needed).
   - Provision Cloudflare R2 buckets (one per region) and set lifecycle rules/retention tags.
   - Provision Redis (managed) and any other managed services (Sentry/Prometheus endpoints).
   - Create DNS records and TLS certificates (Let's Encrypt via ACM or Cloudflare-managed certs).

2. CI/CD pipeline
   - Build Docker images for backend and frontend in CI (GitHub Actions) and push to ECR/Container Registry.
   - Use a blue/green or rolling deployment strategy to update services without downtime.
   - Inject secrets at deploy time (do not store sensitive values in the repo). Use ECS task definitions or systemd env files referencing Secrets Manager.

3. Environment & configuration
   - Required environment variables (example):
     - DATABASE_URL (Neon connection string)
     - REDIS_URL
     - STORAGE_MODE=r2 (or 's3' compatible)
     - R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET_{US,EU}, R2_ENDPOINT
     - JWKS_URL_{US,EU}
     - NEXT_PUBLIC_COMPANY_NAME, NEXT_PUBLIC_BASE_URL
   - Use config templates and encrypted secrets in CI.

4. Object deletion & retention
   - Use lifecycle rules to keep objects per retention policy (however, lifecycles are eventually consistent; the app should also scrub objects explicitly when permanent delete is required).
   - For Delete-Org workflows, run the worker to remove DB rows, revoke tokens, rotate secrets, and remove R2 prefixes.

5. Security hardening
   - Ensure TLS everywhere (ALB/Cloudflare in front of app servers).
   - Enable RLS and session-local variables as implemented (SET LOCAL app.org_id/app.user_id).
   - Use a bastion host or Systems Manager for access to EC2 instances (avoid SSH with public keys if possible).

6. Observability & alerts
   - Provision Sentry and initialize DSN in backend config.
   - Provision Prometheus + Grafana; import dashboards from infra/monitoring if present.
   - Create alert rules: job failure rate > 5%, storage usage > 80% of quota, rate-limit spikes.

Operational notes
- Secrets rotation: rotate R2 keys and database credentials periodically and update running workers without downtime (use rolling restarts).
- Backups: configure Neon backups & retention policy and ensure deletion job is aware of retained backups vs GDPR deletion window.

