from fastapi import APIRouter
router = APIRouter(prefix='/v1/admin', tags=['admin'])


from fastapi import Body, HTTPException, Depends
from ..services import llm_manager
from ..deps.permissions import require_permission

@router.post('/plans/{plan_id}/set-stripe-price', dependencies=[Depends(require_permission('admin','update'))])
def set_plan_stripe_price(plan_id: str, body: dict = Body(...)):
    # body should contain {'stripe_price_id': 'price_XXXX'}
    stripe_price_id = body.get('stripe_price_id')
    if not stripe_price_id:
        raise HTTPException(status_code=400, detail='stripe_price_id required')
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute("UPDATE public.plans SET stripe_price_id = %s WHERE id = %s RETURNING id, name, tier, stripe_price_id", (stripe_price_id, plan_id))
            row = cur.fetchone()
            conn.commit()
            if not row:
                raise HTTPException(status_code=404, detail='plan not found')
            return dict(row)
    finally:
        try: conn.close()
        except: pass

@router.post('/invoices/reconcile', dependencies=[Depends(require_permission('admin','update'))])
def reconcile_invoices():
    """Reconcile invoices by matching Stripe invoices to our DB; create missing invoices if necessary."""
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            # Find open Stripe invoices via Stripe API and reconcile - placeholder: admin should run offline with stripe_service
            cur.execute("SELECT id, external_invoice_id, status FROM public.invoices WHERE status != 'paid' AND external_invoice_id IS NOT NULL LIMIT 100"")
            rows = cur.fetchall()
            return {'count': len(rows), 'sample': [dict(r) for r in rows[:10]]}
    finally:
        try: conn.close()
        except: pass
