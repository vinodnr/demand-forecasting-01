import os, logging, json
import stripe
from ..services import llm_manager
logger = logging.getLogger('stripe_service')
stripe.api_key = os.getenv('STRIPE_API_KEY')

def create_checkout_session(org_id: str, plan_price_id: str, success_url: str, cancel_url: str):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': plan_price_id, 'quantity': 1}],
        mode='subscription',
        metadata={'org_id': org_id},
        success_url=success_url,
        cancel_url=cancel_url
    )
    return session

def _mark_event_processed(event_id: str, event_type: str, payload: dict):
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO public.processed_events (event_id, event_type, payload) VALUES (%s, %s, %s::jsonb) ON CONFLICT (event_id) DO NOTHING", (event_id, event_type, json.dumps(payload)))
            conn.commit()
        conn.close()
    except Exception as e:
        logger.exception('Failed to mark event processed: %s', e)

def _event_already_processed(event_id: str):
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM public.processed_events WHERE event_id = %s", (event_id,))
            row = cur.fetchone()
        conn.close()
        return bool(row)
    except Exception as e:
        logger.exception('Failed to check processed event: %s', e)
        return False

def _set_subscription_status_by_external(subscription_id: str, status: str, stripe_payload: dict=None):
    """Update org_subscriptions by matching external subscription id or metadata.customer/org mapping."""
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            # Try to find subscription by matching external id on invoices or subscriptions table if present
            cur.execute("SELECT id FROM public.org_subscriptions WHERE id = %s", (subscription_id,))
            row = cur.fetchone()
            if row:
                cur.execute("UPDATE public.org_subscriptions SET status=%s WHERE id=%s", (status, subscription_id))
            else:
                # Try to match by metadata.org_id in stripe payload
                org_id = None
                if stripe_payload:
                    org_id = stripe_payload.get('metadata', {}).get('org_id') or stripe_payload.get('customer') or None
                if org_id:
                    cur.execute("UPDATE public.org_subscriptions SET status=%s WHERE org_id=%s", (status, org_id))
            conn.commit()
        conn.close()
    except Exception as e:
        logger.exception('Failed to update subscription status: %s', e)

def handle_webhook(payload: bytes, sig_header: str, webhook_secret: str):
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception as e:
        logger.exception('Stripe webhook signature verification failed: %s', e)
        raise

    event_id = event['id']
    event_type = event['type']
    data = event['data']['object']

    # Idempotency: skip if processed
    if _event_already_processed(event_id):
        logger.info('Stripe event %s already processed; skipping', event_id)
        return event

    # Process events of interest
    try:
        if event_type in ('invoice.payment_succeeded', 'invoice.finalized', 'invoice.paid'):
            external_id = data.get('id')
            try:
                conn = llm_manager._get_conn()
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM public.invoices WHERE external_invoice_id = %s", (external_id,))
                    row = cur.fetchone()
                    if row:
                        cur.execute("UPDATE public.invoices SET status='paid' WHERE external_invoice_id = %s", (external_id,))
                    else:
                        org_id = data.get('metadata', {}).get('org_id') or None
                        amount = int(data.get('amount_due') or data.get('total') or 0)
                        cur.execute("INSERT INTO public.invoices (id, org_id, amount_cents, currency, period_start, period_end, status, external_invoice_id, created_at) VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, 'paid', %s, now()) RETURNING id", (org_id, amount, data.get('currency') or 'usd', None, None, external_id))
                    conn.commit()
            except Exception as e:
                logger.exception('Failed to reconcile/create invoice: %s', e)
            finally:
                try: conn.close()
                except: pass

        elif event_type in ('invoice.payment_failed', 'payment_intent.payment_failed'):
            external_id = data.get('id')
            try:
                conn = llm_manager._get_conn()
                with conn.cursor() as cur:
                    cur.execute("UPDATE public.invoices SET status='failed' WHERE external_invoice_id = %s", (external_id,))
                    conn.commit()
            except Exception as e:
                logger.exception('Failed to mark invoice failed: %s', e)
            finally:
                try: conn.close()
                except: pass

        elif event_type in ('customer.subscription.updated', 'customer.subscription.created'):
            # Update our subscription status based on Stripe subscription status
            sub_id = data.get('id')
            stripe_status = data.get('status')  # e.g., 'active', 'past_due', 'canceled'
            org_id = data.get('metadata', {}).get('org_id') or data.get('customer') or None
            # Map Stripe subscription status to our org_subscriptions.status
            mapped = 'active' if stripe_status in ('active','trialing') else ('past_due' if stripe_status=='past_due' else 'canceled' if stripe_status in ('canceled','unpaid') else stripe_status)
            _set_subscription_status_by_external(sub_id, mapped, data)

        elif event_type == 'customer.subscription.deleted':
            sub_id = data.get('id')
            _set_subscription_status_by_external(sub_id, 'canceled', data)

        # mark processed (idempotency store)
        _mark_event_processed(event_id, event_type, event)
    except Exception as e:
        logger.exception('Error handling stripe event %s: %s', event_id, e)
        raise

    return event
