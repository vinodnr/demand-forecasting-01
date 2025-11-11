from fastapi import APIRouter, Request, Header, HTTPException, Body, Depends
import os, logging
from ..services.stripe_service import handle_webhook, create_checkout_session
from ..deps.permissions import require_permission

logger = logging.getLogger('stripe_webhook')
router = APIRouter(prefix='/v1/stripe', tags=['stripe'])

@router.post('/webhook')
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    if not webhook_secret:
        raise HTTPException(status_code=500, detail='webhook secret not configured')
    try:
        event = handle_webhook(payload, stripe_signature, webhook_secret)
        return {'status':'ok', 'type': event['type']}
    except Exception as e:
        logger.exception('stripe webhook handling failed: %s', e)
        raise HTTPException(status_code=400, detail='invalid webhook')

@router.post('/create-checkout-session', dependencies=[Depends(require_permission('billing','create'))])
async def create_checkout(body: dict = Body(...)):
    org_id = body.get('org_id')
    price_id = body.get('price_id')
    success = body.get('success_url')
    cancel = body.get('cancel_url')
    if not org_id or not price_id:
        raise HTTPException(status_code=400, detail='org_id and price_id required')
    session = create_checkout_session(org_id, price_id, success, cancel)
    return {'id': session.id, 'url': session.url}
