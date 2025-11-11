# Admin UI Quickstart

This document describes how to access and use the Admin UI for the Demand Forecasting SaaS dev environment.

## 1. Start the dev stack
From the repo root run:
```bash
make up
```
(Equivalent to `docker compose -f backend/monitoring/docker-compose.dev.yml up -d --build`)

## 2. Seed dev data (users + orgs)
Run the Make target which executes the seed scripts inside the backend container:
```bash
make seed-dev
```
This runs:
- `backend/scripts/seed_test_users.py` — creates super-admin and sample clients
- `backend/scripts/seed_orgs_and_users.py` — creates orgs and links users to orgs

Default seeded accounts (dev only):
- Super-admin: `vinsbox@gmail.com` / `Myvin1234$`
- Sample client (free): `free1@example.com` / `Cadmin!23$`
(See Sprint-13/SEED_USERS_MANIFEST.json for full list.)

## 3. Login as Super Admin
Use the API login endpoint to get a JWT (example):
```bash
curl -s -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"vinsbox@gmail.com","password":"Myvin1234$"}' | jq
```
Copy the returned `access_token` and use it in the browser dev tools or API clients as:
```
Authorization: Bearer <access_token>
```

If your frontend has an Admin UI, open it (default path suggestions):
- Admin Dashboard: `http://localhost:3000/app/admin` or `http://localhost:3000/admin`
- Trust & Transparency: `http://localhost:3000/trust` (public) and `http://localhost:3000/app/trust` (authenticated)

## 4. Promote a user to Admin (if needed)
If you need to promote another seeded user to admin, do it via SQL or the seed script update. Example SQL using psql in the postgres container:
```bash
docker compose -f backend/monitoring/docker-compose.dev.yml exec postgres psql -U postgres -d demand_forecast -c "  UPDATE users SET role='admin' WHERE email='pro1@example.com';"
```

## 5. Common admin tasks
- Create / manage orgs: use the Admin UI or call backend admin endpoints (check `backend/src/api/admin` routes).
- View audit logs: `/app/trust/audit-logs` (requires admin)
- Trigger delete-org workflow: Admin UI provides a button or call `POST /v1/org/request-delete`

## 6. Troubleshooting
- If login fails, tail backend logs:
```bash
make logs
```
- If backend service name is not `backend`, edit the `Makefile` and set `BACKEND_SERVICE` appropriately.
- If database name differs, set `DATABASE_URL` env when running seed scripts:
```bash
docker compose -f backend/monitoring/docker-compose.dev.yml exec -T backend env DATABASE_URL=postgresql://postgres:postgres@postgres:5432/demand_forecast python backend/scripts/seed_test_users.py
```

## 7. Security notice
These seeds and credentials are for **development only**. Rotate or remove them before sharing or promoting to staging/production.
