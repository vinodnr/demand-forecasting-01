# SECRET ROTATION RUNBOOK (summary)

## Objective
Rotate Neon DB credentials and Cloudflare R2 keys with zero-downtime rolling updates.

## Preconditions
- Access to secret store (Vault/Hetzner secrets manager) and CI/CD pipeline
- Ability to perform rolling restarts of app nodes (systemd/docker compose or orchestrator)

## Steps (DB)
1. Create new DB user/credentials in Neon or rotate password for existing user.
2. Add new `DATABASE_URL` under a new secret path (e.g., secrets/db/driver_manager_v2).
3. Deploy one app instance with new secret reference and run health checks.
4. If healthy, roll the change across nodes; monitor errors and logs.
5. After 24h with no failures, revoke old credentials.

## Steps (R2 keys)
1. Create new R2 access key pair in Cloudflare console.
2. Add them to secret store with path `r2/keys_v2`.
3. Update one worker/backend process to use new keys; test presign & download.
4. Roll update across instances and verify behavior.
5. Revoke old keys once stable.

## JWT / JWKS rotation
- Add new key entry to your JWKS endpoint, but keep old key present during token grace period (token TTL).
- Orchestrate rotation by updating identity provider and app JWKS cache TTL to a small value during rotation.
