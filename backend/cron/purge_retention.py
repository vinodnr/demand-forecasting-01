# backend/cron/purge_retention.py
import os, time, psycopg2, datetime
DATABASE_URL = os.getenv('DATABASE_URL')
RETENTION_DAYS_FREE = int(os.getenv('RETENTION_DAYS_FREE', '30'))
RETENTION_DAYS_PAID = int(os.getenv('RETENTION_DAYS_PAID','365'))

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def purge():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Example: datasets table with created_at and deleted_at
            # Soft-delete old rows for free plans based on plan mapping
            cur.execute("""UPDATE public.datasets d SET deleted_at = now()
                           FROM public.org_subscriptions s
                           WHERE d.org_id = s.org_id
                             AND s.tier = 'free'
                             AND d.created_at < now() - interval '%s days'
                             AND d.deleted_at IS NULL""" % (RETENTION_DAYS_FREE))
            conn.commit()
            # Permanent delete of rows older than retention + grace period (optional)
            # Implement object deletes via storage drivers (not shown here)
    finally:
        conn.close()

if __name__ == '__main__':
    purge()
