# backend/tests/test_admin_functions.py
import os, psycopg2, pytest
DATABASE_URL = os.getenv('DATABASE_URL','postgresql://postgres:postgres@localhost:5432/driver_manager')

def test_admin_delete_org_function():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            # This test assumes the SECURITY DEFINER function admin_delete_org exists
            cur.execute("SELECT exists(SELECT 1 FROM pg_proc WHERE proname='admin_delete_org')")
            r = cur.fetchone()[0]
            assert r, 'admin_delete_org function missing'
    finally:
        conn.close()
