# Deployment Guide — Local Docker Compose (recommended for dev & staging)
This guide explains how to run the full stack locally using docker-compose for integration testing.

Requirements:
- Docker & Docker Compose v2+ installed
- Make or bash shell
- Ports: 8000 (backend), 3000 (frontend dev), 5432 (postgres), 9000 (minio), 6379 (redis)

Steps:
1. Build images (from repo root)
   - Ensure backend/Dockerfile.dev exists. If not, create a simple one that installs backend requirements and uses uvicorn to run app.
   - Example build (optional): `docker build -f backend/Dockerfile.dev -t df-backend:dev .`

2. Start services (from backend/monitoring)
   ```bash
   cd backend/monitoring
   docker-compose -f docker-compose.dev.yml up -d --build
   ```

3. Apply DB migrations
   - Ensure DATABASE_URL env var points to postgres container `postgresql://postgres:postgres@postgres:5432/driver_manager`
   - Run your migration runner, e.g. Alembic or custom scripts:
     ```bash
     docker exec -it <backend_container> bash -c "python backend/migrations/run_migrations.py"
     ```
   - Alternatively, use `psql` from host to apply SQL files in backend/migrations/versions/

4. Seed basic data (optional)
   - Create a test org, test user, and org_quotas row for dev testing.

5. Start frontend (if using Next.js dev)
   - From repo root: `cd frontend && npm ci && npm run dev` (runs on port 3000 by default)

6. Run worker(s)
   - Start conversion worker to listen to Redis queue:
     ```bash
     docker exec -it <backend_container> bash -lc "python backend/workers/jobs.py"
     ```
   - Or run the worker service provided in docker-compose.dev.yml

7. Validate flows
   - Visit `http://localhost:3000/trust` (public Trust Center)
   - Authenticated flows require creating a test user and logging in; use `/v1/auth/me` behavior expected by ProtectedRoute

Notes & troubleshooting
- MinIO console available at http://localhost:9000 (default credentials minioadmin:minioadmin)
- If ports conflict, update compose ports mapping
- For faster edit-apply cycles, mount source directories into containers using volumes in compose

