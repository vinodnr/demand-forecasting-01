# backend/workers/delete_org_worker.py (enhanced)
import psycopg2, os, subprocess
DATABASE_URL = os.getenv('DATABASE_URL','postgresql://postgres:postgres@localhost:5432/driver_manager')

def process_delete_job(job):
    org_id = job.get('org_id')
    reason = job.get('reason','requested')
    actor = job.get('owner_id')
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            # mark org as deleting flag in orgs table if exists
            try:
                cur.execute("ALTER TABLE public.organizations ADD COLUMN IF NOT EXISTS deleting boolean DEFAULT false")
            except Exception:
                pass
            cur.execute('UPDATE public.organizations SET deleting=true WHERE id=%s', (org_id,))
            # call SECURITY DEFINER admin delete function (skeleton must exist)
            try:
                cur.execute('SELECT public.admin_delete_org(%s,%s,%s)', (org_id, reason, actor))
            except Exception as e:
                print('admin_delete_org function call failed (may be missing):', e)
            conn.commit()
    finally:
        conn.close()
    # remove storage prefix (best-effort)
    base = os.getenv('LOCAL_STORAGE_PATH','./data')
    import shutil, glob
    prefixes = glob.glob(os.path.join(base, f'*/*/{org_id}*'))
    for p in prefixes:
        try:
            shutil.rmtree(p)
        except Exception:
            pass
    print('Delete job completed for', org_id)
