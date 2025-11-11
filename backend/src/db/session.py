# backend/src/db/session.py
import psycopg2, os, contextlib
from contextlib import contextmanager
from typing import Generator
from ..auth.jwt_middleware import set_db_session_vars

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/driver_manager')

@contextmanager
def db_session(user=None, org_id=None):
    conn = psycopg2.connect(DATABASE_URL)
    try:
        # begin transaction
        conn.autocommit = False
        # set local vars for RLS within this transaction
        if org_id or user:
            set_db_session_vars(conn, org_id=org_id, user_id=user)
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()
