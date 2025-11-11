#!/usr/bin/env python3
"""backend/scripts/seed_orgs_and_users.py

Idempotent script to create organization rows for each plan/tier and link sample users to them.
Run inside the backend container where DATABASE_URL is set, for example:
  docker compose -f backend/monitoring/docker-compose.dev.yml exec backend     python backend/scripts/seed_orgs_and_users.py

It expects users to already exist (created by seed_test_users.py). It will:
 - create organizations table (if missing)
 - create one or two orgs per tier (free, pro, business, enterprise)
 - link sample users (by email) to orgs by updating users.org_id
 - create org_quotas row (basic) if table exists

Adjust table/column names if your schema differs.
"""
import os
import uuid
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://postgres:postgres@postgres:5432/demand_forecast")

# mapping: plan -> list of sample user emails to attach
PLAN_ORG_MAP = {
    'free': ['free1@example.com', 'free2@example.com'],
    'pro': ['pro1@example.com', 'pro2@example.com'],
    'business': ['business1@example.com', 'business2@example.com'],
    'enterprise': ['enterprise1@example.com', 'enterprise2@example.com'],
}

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def ensure_orgs_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            plan TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """)
        conn.commit()

def ensure_org_quotas_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS org_quotas (
            org_id TEXT PRIMARY KEY,
            storage_limit_bytes BIGINT DEFAULT 0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """)
        conn.commit()

def create_org(conn, name, plan):
    org_id = f"org-{uuid.uuid4().hex[:8]}"
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO organizations (id, name, plan, created_at)
        VALUES (%s, %s, %s, now())
        ON CONFLICT (id) DO NOTHING;
        """, (org_id, name, plan))
        conn.commit()
    return org_id

def org_exists(conn, name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM organizations WHERE name = %s LIMIT 1", (name,))
        r = cur.fetchone()
        return r[0] if r else None

def seed_orgs_and_link_users():
    conn = get_conn()
    try:
        ensure_orgs_table(conn)
        ensure_org_quotas_table(conn)
        created = []
        for plan, emails in PLAN_ORG_MAP.items():
            # create 1 org for the plan if not exists
            default_org_name = f"{plan.title()} Org 1"
            existing = org_exists(conn, default_org_name)
            if existing:
                org_id = existing
            else:
                org_id = create_org(conn, default_org_name, plan)
            created.append({'plan': plan, 'org_id': org_id, 'name': default_org_name})
            # link users by email to org_id
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE users SET org_id = %s WHERE email = ANY(%s)
                """, (org_id, emails))
                conn.commit()
            # create an org_quotas row if not exists (example limits)
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO org_quotas (org_id, storage_limit_bytes, created_at)
                VALUES (%s, %s, now())
                ON CONFLICT (org_id) DO NOTHING;
                """, (org_id, 10 * 1024 * 1024 * 1024))  # 10 GB default
                conn.commit()
        print('Seeded orgs and linked users:', created)
    finally:
        conn.close()

if __name__ == '__main__':
    seed_orgs_and_link_users()
