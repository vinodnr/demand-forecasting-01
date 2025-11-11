#!/usr/bin/env python3
"""backend/scripts/seed_test_users.py

Idempotent script to create a superadmin and example clients for each tier.
Run inside the backend container where DATABASE_URL is set, for example:
  docker compose -f backend/monitoring/docker-compose.dev.yml exec backend     python backend/scripts/seed_test_users.py

Defaults (can be overridden with env vars):
  SUPER_EMAIL, SUPER_PW, SUPER_ID
  TIER_PASSWORD (applies to all sample clients)
  DATABASE_URL (must be set; default fallback is postgres on localhost)

This script uses bcrypt for password hashing.
"""
import os
import uuid
import bcrypt
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://postgres:postgres@postgres:5432/demand_forecast")

SUPER_EMAIL = os.getenv('SUPER_EMAIL', 'vinsbox@gmail.com')
SUPER_PW = os.getenv('SUPER_PW', 'Myvin1234$')
SUPER_ID = os.getenv('SUPER_ID', 'super-admin-1')
SUPER_ROLE = os.getenv('SUPER_ROLE', 'superadmin')

TIER_PASSWORD = os.getenv('TIER_PASSWORD', 'Cadmin!23$')

# example clients per tier (email localpart -> tier)
SAMPLE_CLIENTS = [
    ('free1@example.com', 'free'),
    ('free2@example.com', 'free'),
    ('pro1@example.com', 'pro'),
    ('pro2@example.com', 'pro'),
    ('business1@example.com', 'business'),
    ('business2@example.com', 'business'),
    ('enterprise1@example.com', 'enterprise'),
    ('enterprise2@example.com', 'enterprise'),
]

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def ensure_users_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            role TEXT,
            org_id TEXT,
            plan TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """)
        conn.commit()

def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_superadmin(conn):
    pw_hash = hash_password(SUPER_PW)
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users (id, email, password_hash, role, is_active, created_at)
        VALUES (%s, %s, %s, %s, true, now())
        ON CONFLICT (email) DO UPDATE SET password_hash = EXCLUDED.password_hash, role = EXCLUDED.role, is_active = EXCLUDED.is_active;
        """, (SUPER_ID, SUPER_EMAIL, pw_hash, SUPER_ROLE))
        conn.commit()
    print(f"Seeded superadmin: {SUPER_EMAIL} (id={SUPER_ID})")

def seed_clients(conn):
    rows = []
    for email, plan in SAMPLE_CLIENTS:
        uid = str(uuid.uuid4())
        pw_hash = hash_password(TIER_PASSWORD)
        rows.append((uid, email, pw_hash, 'user', None, plan, True))
    with conn.cursor() as cur:
        execute_values(cur,
            """INSERT INTO users (id, email, password_hash, role, org_id, plan, is_active)
               VALUES %s
               ON CONFLICT (email) DO UPDATE SET password_hash = EXCLUDED.password_hash, plan = EXCLUDED.plan, is_active = EXCLUDED.is_active;
            """, rows)
        conn.commit()
    print(f"Seeded {len(rows)} sample clients with password: '{TIER_PASSWORD}'")

def main():
    print("Connecting to:", DATABASE_URL)
    conn = get_conn()
    try:
        ensure_users_table(conn)
        seed_superadmin(conn)
        seed_clients(conn)
        print("Seeding complete.")
    finally:
        conn.close()

if __name__ == '__main__':
    main()
