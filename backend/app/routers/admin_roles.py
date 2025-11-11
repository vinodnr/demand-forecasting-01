from fastapi import APIRouter, Body, Depends, HTTPException
from ..deps.permissions import require_permission
router = APIRouter(prefix='/v1/admin/roles', tags=['admin_roles'])

@router.get('', dependencies=[Depends(require_permission('roles.manage','view'))])
def list_roles():
    try:
        from ..services.llm_manager import _get_conn
        conn = _get_conn()
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, description, created_at FROM public.roles ORDER BY name')
            rows = cur.fetchall()
            return [dict(r) for r in rows]
    finally:
        try: conn.close()
        except: pass

@router.post('', dependencies=[Depends(require_permission('roles.manage','create'))])
def create_role(body: dict = Body(...)):
    name = body.get('name')
    desc = body.get('description')
    if not name:
        raise HTTPException(status_code=400, detail='name required')
    try:
        conn = _get_conn()
        with conn.cursor() as cur:
            cur.execute('INSERT INTO public.roles (name, description) VALUES (%s,%s) RETURNING id, name, description', (name, desc))
            row = cur.fetchone()
            # audit
            cur.execute("INSERT INTO public.admin_audit (actor_id, action, target_type, target_id, details) VALUES (%s,%s,%s,%s,%s)", (None, 'create_role', 'role', row[0], json_build_object('name', name)))
            conn.commit()
            return dict(row)
    finally:
        try: conn.close()
        except: pass

@router.put('/{role_id}', dependencies=[Depends(require_permission('roles.manage','update'))])
def update_role(role_id: str, body: dict = Body(...)):
    name = body.get('name')
    desc = body.get('description')
    try:
        conn = _get_conn()
        with conn.cursor() as cur:
            cur.execute('UPDATE public.roles SET name=%s, description=%s WHERE id=%s RETURNING id, name, description', (name, desc, role_id))
            row = cur.fetchone()
            cur.execute("INSERT INTO public.admin_audit (actor_id, action, target_type, target_id, details) VALUES (%s,%s,%s,%s,%s)", (None, 'update_role', 'role', role_id, json_build_object('name', name)))
            conn.commit()
            return dict(row)
    finally:
        try: conn.close()
        except: pass
