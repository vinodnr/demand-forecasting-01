from fastapi import APIRouter, Body, Depends, HTTPException
from ..deps.permissions import require_permission
from ..services.email_service import send_email
import secrets, json, os
router = APIRouter(prefix='/v1/admin/invites', tags=['admin_invites'])

@router.post('', dependencies=[Depends(require_permission('users.invite','create'))])
def create_invite(body: dict = Body(...)):
    email = body.get('email')
    role = body.get('role')
    if not email or not role:
        raise HTTPException(status_code=400, detail='email and role required')
    token = secrets.token_urlsafe(32)
    # store invite token in a simple invites table (create if not exists)
    try:
        conn = None
        from ..services.llm_manager import _get_conn as _getconn
        conn = _getconn()
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS public.user_invites (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), email text, role text, token text, used boolean DEFAULT false, created_at timestamptz DEFAULT now())')
            cur.execute('INSERT INTO public.user_invites (email, role, token) VALUES (%s,%s,%s) RETURNING id', (email, role, token))
            invite_id = cur.fetchone()[0]
            conn.commit()
    finally:
        try: conn.close()
        except: pass
    # send email with invite link (expect FRONTEND_URL env)
    frontend = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    link = f"{frontend}/signup?invite={token}"
    subject = 'You are invited to join the platform'
    html = f"<p>You were invited to join. Click <a href='{link}'>here</a> to accept the invite.</p>"
    sent = send_email(email, subject, html_body=html, text_body=f'Open {link} to accept invite.')
    # audit
    try:
        conn = _getconn()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO public.admin_audit (actor_id, action, target_type, target_id, details) VALUES (%s,%s,%s,%s,%s)", (None, 'create_invite', 'invite', invite_id, json_build_object('email', email, 'role', role)))
            conn.commit()
    finally:
        try: conn.close()
        except: pass
    return {'status':'sent' if sent else 'stored', 'invite_id': str(invite_id)}

@router.post('/accept')
def accept_invite(body: dict = Body(...)):
    token = body.get('token')
    password = body.get('password')
    name = body.get('name')
    if not token or not password:
        raise HTTPException(status_code=400, detail='token and password required')
    try:
        conn = None
        from ..services.llm_manager import _get_conn as _getconn
        conn = _getconn()
        with conn.cursor() as cur:
            cur.execute('SELECT email, role, used FROM public.user_invites WHERE token=%s LIMIT 1', (token,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=400, detail='invalid token')
            if row[2]:
                raise HTTPException(status_code=400, detail='token already used')
            email = row[0]; role = row[1]
            # create user in public.users table (assumes such table exists and has minimal schema)
            cur.execute('INSERT INTO public.users (email, password_hash, name) VALUES (%s,%s,%s) RETURNING id', (email, password, name))
            user_id = cur.fetchone()[0]
            # assign role
            cur.execute('SELECT id FROM public.roles WHERE name=%s LIMIT 1', (role,))
            r = cur.fetchone()
            if r and r[0]:
                cur.execute('INSERT INTO public.user_roles (user_id, role_id) VALUES (%s,%s)', (user_id, r[0]))
            # mark invite used
            cur.execute('UPDATE public.user_invites SET used=true WHERE token=%s', (token,))
            # audit
            cur.execute("INSERT INTO public.admin_audit (actor_id, action, target_type, target_id, details) VALUES (%s,%s,%s,%s,%s)", (user_id, 'accept_invite', 'user', user_id, json_build_object('email', email)))
            conn.commit()
            return {'status':'ok', 'user_id': str(user_id)}
    finally:
        try: conn.close()
        except: pass
