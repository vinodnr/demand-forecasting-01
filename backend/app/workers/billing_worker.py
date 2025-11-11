import logging, time, json, os, datetime
from ..services import llm_manager, usage_meter
from backend.app.services.llm_integration import get_llm_client
from backend.app.services.metrics import ACTIVE_WORKERS, record_llm_usage
import atexit
from backend.app.services.worker_label_map import get_worker_label
try:
    ACTIVE_WORKERS.labels(worker_name=get_worker_label('billing_worker')).inc()
except Exception:
    pass

def _decr_worker():
    try:
        ACTIVE_WORKERS.labels(worker_name=get_worker_label('billing_worker')).dec()
    except Exception:
        pass
atexit.register(_decr_worker)


logger = logging.getLogger('billing_worker')

def generate_monthly_invoices(process_date=None):
    """Generate invoices for all active subscriptions for the previous billing period."""
    process_date = process_date or datetime.datetime.utcnow()
    period_end = process_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    period_start = (period_end - datetime.timedelta(days=1)).replace(day=1)
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT id, org_id, plan_id, started_at FROM public.org_subscriptions WHERE status='active'")
            subs = cur.fetchall()
            for s in subs:
                sub_id, org_id, plan_id, started = s[0], s[1], s[2], s[3]
                # compute base price
                cur.execute("SELECT price_monthly_cents FROM public.plans WHERE id = %s", (plan_id,))
                p = cur.fetchone()
                price_cents = int(p[0]) if p and p[0] is not None else 0
                # compute overage for llm_tokens (example metric)
                token_usage = usage_meter.get_usage_sum(org_id, 'llm_tokens', period_start.isoformat(), period_end.isoformat())
                # get plan limit
                cur.execute("SELECT limit_value FROM public.plan_limits WHERE plan_id=%s AND metric='llm_tokens'", (plan_id,))
                row = cur.fetchone()
                limit = int(row[0]) if row and row[0] is not None else 0
                overage_cents = 0
                if limit and token_usage > limit:
                    # simple overage pricing: $0.0001 per token -> cents = tokens * 0.0001 * 100 = tokens * 0.01
                    overage_cents = int((token_usage - limit) * 0.01)
                total_cents = price_cents + overage_cents
                # create invoice row
                cur.execute("INSERT INTO public.invoices (id, org_id, amount_cents, currency, period_start, period_end, status, created_at) VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, 'open', now()) RETURNING id", (org_id, total_cents, 'usd', period_start, period_end))
                inv_id = cur.fetchone()[0]
                conn.commit()
                logger.info('Created invoice %s for org %s total_cents=%s', inv_id, org_id, total_cents)
        conn.close()
        return True
    except Exception as e:
        logger.exception('Monthly invoice generation failed: %s', e)
        return False

def _llm_call_and_metric(org_id, messages=None, prompt=None, model='gpt-4o-mini', max_tokens=512, **kwargs):
    from backend.app.services.llm_integration import get_llm_client
    client = get_llm_client()
    resp = client.chat_completion(org_id=org_id, messages=messages, model=model, max_tokens=max_tokens, **kwargs)
    # record tokens if available
    try:
        usage = None
        if isinstance(resp, dict):
            usage = resp.get('usage')
        elif hasattr(resp, 'usage'):
            usage = getattr(resp, 'usage')
        total = 0
        if usage and isinstance(usage, dict):
            total = int(usage.get('total_tokens', 0) or 0)
        if total>0:
            try:
                record_llm_usage(org_id, getattr(resp, 'provider', 'openai'), model, total)
            except Exception:
                pass
    except Exception:
        pass
    return resp
