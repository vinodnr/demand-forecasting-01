from fastapi import APIRouter, Depends, HTTPException
from ..services import llm_manager, usage_meter
from ..schemas import admin_schemas
from ..deps.permissions import require_permission
import json

router = APIRouter(prefix='/v1/billing', tags=['billing'])

@router.get('/plans')
def list_plans():
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, tier, price_monthly_cents FROM public.plans ORDER BY price_monthly_cents')
            rows = cur.fetchall()
            return [dict(r) for r in rows]
    finally:
        try: conn.close()
        except: pass

@router.post('/subscribe', dependencies=[Depends(require_permission('billing','create'))])
def subscribe(org_id: str, plan_id: str):
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute('INSERT INTO public.org_subscriptions (id, org_id, plan_id, status, started_at, billing_cycle_anchor, created_at) VALUES (gen_random_uuid(), %s, %s, %s, now(), now(), now()) RETURNING id', (org_id, plan_id, 'active'))
            row = cur.fetchone()
            conn.commit()
            return {'status':'ok', 'subscription_id': row[0] if row else None}
    finally:
        try: conn.close()
        except: pass

@router.post('/usage')
def report_usage(org_id: str, metric: str, value: float, metadata: dict = None):
    ok = usage_meter.record_usage(org_id, metric, value, metadata or {})
    if not ok:
        raise HTTPException(status_code=500, detail='failed to record usage')
    return {'status':'ok'}

@router.get('/invoices/{org_id}')
def list_invoices(org_id: str):
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute('SELECT id, amount_cents, currency, period_start, period_end, status, created_at FROM public.invoices WHERE org_id=%s ORDER BY created_at DESC', (org_id,))
            rows = cur.fetchall()
            return [dict(r) for r in rows]
    finally:
        try: conn.close()
        except: pass
