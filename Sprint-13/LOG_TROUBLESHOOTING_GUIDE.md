Log Troubleshooting Guide — what to paste when asking for help

If you run into problems while running the seed scripts or starting the stack, please paste the output of these commands
(you can redact secrets and tokens, but keep error messages intact).

1) Tail backend logs (shows runtime errors):
   make logs
   OR
   docker compose -f backend/monitoring/docker-compose.dev.yml logs -f backend

2) Seed script output (capture stderr/stdout of the seed run):
   docker compose -f backend/monitoring/docker-compose.dev.yml exec -T backend python backend/scripts/seed_test_users.py 2>&1 | sed -n '1,200p'

3) Postgres connectivity check (inside the backend container):
   docker compose -f backend/monitoring/docker-compose.dev.yml exec -T backend bash -lc "python -c 'import os, psycopg2;print(os.getenv("DATABASE_URL"));conn=psycopg2.connect(os.getenv("DATABASE_URL"));print("OK")' "

4) If seed fails due to missing Python deps, paste the output of:
   docker compose -f backend/monitoring/docker-compose.dev.yml exec -T backend pip freeze

Helpful things to include when you paste logs here:
- Full error stacktrace (exception type + message)
- The command you ran and the exact compose service names
- The first 100 lines of the backend logs and any recent seed script output
