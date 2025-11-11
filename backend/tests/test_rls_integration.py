# backend/tests/test_rls_integration.py
import os
import psycopg2
import uuid

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/driver_manager')

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def setup_test_data():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Create organizations and tenant_items if not exist (id textual for tests)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS organizations (id text PRIMARY KEY, name text);
            CREATE TABLE IF NOT EXISTS tenant_items (id text PRIMARY KEY, org_id text REFERENCES organizations(id), name text);
            """)
            cur.execute("INSERT INTO organizations (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING;", ('org-a','Org A'))
            cur.execute("INSERT INTO organizations (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING;", ('org-b','Org B'))
            cur.execute("INSERT INTO tenant_items (id, org_id, name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", ('item-a','org-a','A'))
            cur.execute("INSERT INTO tenant_items (id, org_id, name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", ('item-b','org-b','B'))
            conn.commit()
    finally:
        conn.close()

def test_rls_session_local_enforcement():
    setup_test_data()
    tx = get_conn()
    try:
        tx.autocommit = False
        cur = tx.cursor()
        # set local session var as application would
        cur.execute("SET LOCAL app.org_id = %s", ('org-a',))
        cur.execute("SELECT id, org_id FROM tenant_items;")
        rows = cur.fetchall()
        # Should only see rows for org-a when RLS is enforced
        assert all(r[1] == 'org-a' for r in rows), f"unexpected rows: {rows}"
    finally:
        tx.rollback()
        tx.close()
