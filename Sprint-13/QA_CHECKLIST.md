# QA CHECKLIST — Sprint 13 (post-deploy to dev environment)
Run these checks after deploying to the dev environment.

## Environment & basic health
- [ ] Backend starts and listens on configured port (default 8000)
- [ ] Frontend (Next.js) runs and serves public pages on port 3000
- [ ] Postgres reachable and migrations applied (no missing tables)
- [ ] Redis reachable and worker can connect

## Functional flows
- [ ] Sign up / login flow works (GET /v1/auth/me returns 200 for test user)
- [ ] Upload presign flow: POST /v1/storage/presign returns presign info
- [ ] Upload → conversion: Worker picks up job and produces .clean.csv file
- [ ] Free-tier retention: original file is removed after conversion
- [ ] Business-tier retention: original file is retained after conversion
- [ ] Delete user: POST /v1/privacy/delete-request creates deletion request and DB record
- [ ] Delete org: POST /v1/org/request-delete enqueues job and worker completes work
- [ ] Audit logs: /v1/logs returns tenant-scoped audit entries

## Security & compliance checks
- [ ] JWT middleware validates tokens and rejects bad signatures (401)
- [ ] DB session local vars are set for transactions (app.org_id, app.user_id)
- [ ] RLS policies enforced (attempt cross-org access should fail)
- [ ] Access control for admin endpoints enforced
- [ ] Privacy pages accessible and DPA document downloadable
- [ ] Data deletion flow audits and logs events

## Observability & alerts
- [ ] Prometheus metrics exposed and scraping target configured
- [ ] Sentry receives an example error (test)
- [ ] Alert rules are present in Grafana/Prometheus provisioning (job failure, storage)

## Performance & scale smoke tests
- [ ] Simulate 100 concurrent presign requests and ensure rate-limiter behaves
- [ ] Worker processes jobs with acceptable latencies (baseline benchmark)
- [ ] Storage usage metrics increase and quotas updated

## Final checks
- [ ] Generate release artifact and checksum (the HANDOVER_PACKAGE contains SHA256)
- [ ] Confirm legal DPA has been uploaded / replaced with final copy
- [ ] Schedule a walkthrough / handover meeting with stakeholders

