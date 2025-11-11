from fastapi import APIRouter, Depends
from ..deps.permissions import require_permission
router = APIRouter(prefix='/v1/admin/audit', tags=['admin_audit'])

@router.get('', dependencies=[Depends(require_permission('admin.view','view'))])
def get_audit(limit: int = 100):
    try:
        from ..services.llm_manager import _get_conn
        conn = _get_conn()
        with conn.cursor() as cur:
            cur.execute('SELECT id, actor_id, action, target_type, target_id, details, created_at FROM public.admin_audit ORDER BY created_at DESC LIMIT %s', (limit,))
            rows = cur.fetchall()
            return [dict(r) for r in rows]
    finally:
        try: conn.close()
        except: pass
