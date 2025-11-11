# backend/src/middleware/quotas.py
from fastapi import Request, HTTPException, Depends
import psycopg2, os
DATABASE_URL = os.getenv('DATABASE_URL','postgresql://postgres:postgres@localhost:5432/driver_manager')

def check_storage_quota(org_id: str, incoming_size: int):
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT storage_bytes, storage_limit FROM public.org_quotas WHERE org_id=%s LIMIT 1', (org_id,))
            row = cur.fetchone()
            if not row:
                return True
            used, limit = row
            if limit is not None and (used + incoming_size) > limit:
                raise HTTPException(status_code=403, detail='Storage quota exceeded')
            # otherwise allow and update usage optimistically (may race; better to use DB transaction+lock)
            cur.execute('UPDATE public.org_quotas SET storage_bytes = storage_bytes + %s, updated_at = now() WHERE org_id=%s', (incoming_size, org_id))
            conn.commit()
            return True
    finally:
        conn.close()

async def storage_quota_dependency(request: Request):
    # expects header x-org-id and body contains size (for presign we pass size param)
    org_id = request.headers.get('x-org-id')
    if not org_id:
        raise HTTPException(status_code=400, detail='org-id header required for quota check')
    body = await request.json()
    size = int(body.get('size',0))
    return check_storage_quota(org_id, size)
