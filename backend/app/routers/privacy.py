from fastapi import APIRouter, Depends, HTTPException, Body
from datetime import datetime
router = APIRouter(prefix='/v1/privacy', tags=['privacy'])

@router.get('/policy')
def get_policy():
    # Return a short machine-readable policy summary (clients can show full pages)
    return {'us_policy_url':'/privacy/gdpr-us', 'eu_policy_url':'/privacy/gdpr-eu', 'data_deletion_supported': True}

@router.post('/delete-request')
def request_data_deletion(body: dict = Body(...)):
    # IMPORTANT: This endpoint expects authenticated user context in production. Here we accept a request and create a deletion request record.
    user_id = body.get('user_id')  # in prod, derive from auth token
    reason = body.get('reason')
    if not user_id:
        raise HTTPException(status_code=400, detail='user_id required (in production derive from authentication)')
    try:
        conn = None
        from ..services.llm_manager import _get_conn
        conn = _get_conn()
        with conn.cursor() as cur:
            # create table if not exists
            cur.execute("""CREATE TABLE IF NOT EXISTS public.privacy_deletion_requests (
                id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id uuid NOT NULL,
                reason text,
                status text DEFAULT 'requested',
                requested_at timestamptz DEFAULT now()
            )""")
            cur.execute('INSERT INTO public.privacy_deletion_requests (user_id, reason) VALUES (%s,%s) RETURNING id, status, requested_at', (user_id, reason))
            row = cur.fetchone()
            conn.commit()
            # In production, enqueue background job to scrub data from all tables and storage, notify customer and admins.
            return {'status':'requested', 'request': {'id': str(row[0]), 'status': row[1], 'requested_at': row[2].isoformat()}}
    finally:
        try:
            if conn: conn.close()
        except:
            pass

@router.delete('/delete-now/{user_id}')
def delete_user_now(user_id: str):
    # Admin-only immediate deletion (dangerous). In production protect with require_permission('admin')
    try:
        conn = None
        from ..services.llm_manager import _get_conn
        conn = _get_conn()
        with conn.cursor() as cur:
            # Soft-delete example: mark users.deleted_at and remove sensitive rows in controlled manner
            try:
                cur.execute('ALTER TABLE public.users ADD COLUMN IF NOT EXISTS deleted_at timestamptz NULL')
            except Exception:
                pass
            cur.execute('UPDATE public.users SET deleted_at = now() WHERE id=%s', (user_id,))
            # Example deletions (customize per your schema)
            # Remove personal rows from user_profiles, sessions, tokens, etc.
            # cur.execute('DELETE FROM public.user_profiles WHERE user_id=%s', (user_id,))
            # cur.execute('DELETE FROM public.user_tokens WHERE user_id=%s', (user_id,))
            cur.execute('INSERT INTO public.admin_audit (actor_id, action, target_type, target_id, details) VALUES (%s,%s,%s,%s,%s)', (None, 'delete_user', 'user', user_id, {'method':'delete_now'}))
            conn.commit()
            return {'status':'deleted', 'user_id': user_id}
    finally:
        try:
            if conn: conn.close()
        except:
            pass
