import logging, time, json, os
from decimal import Decimal
from . import llm_manager

logger = logging.getLogger('usage_meter')

def record_usage(org_id: str, metric: str, value: float, metadata: dict=None):
    """Insert a usage record for an org."""
    metadata = metadata or {}
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO public.usage_records (org_id, metric, value, metadata, recorded_at) VALUES (%s, %s, %s, %s::jsonb, now())""", (org_id, metric, Decimal(str(value)), json.dumps(metadata)))
            conn.commit()
        conn.close()
        logger.debug('Recorded usage for %s metric=%s value=%s', org_id, metric, value)
        return True
    except Exception as e:
        logger.exception('Failed to record usage: %s', e)
        return False

def get_usage_sum(org_id: str, metric: str, period_start: str, period_end: str):
    """Sum usage for an org & metric within a period (ISO timestamps)."""
    try:
        conn = llm_manager._get_conn()
        with conn.cursor() as cur:
            cur.execute("""SELECT COALESCE(SUM(value),0) FROM public.usage_records WHERE org_id=%s AND metric=%s AND recorded_at >= %s AND recorded_at < %s""", (org_id, metric, period_start, period_end))
            row = cur.fetchone()
            total = float(row[0]) if row and row[0] is not None else 0.0
        conn.close()
        return total
    except Exception as e:
        logger.exception('Failed to query usage sum: %s', e)
        return 0.0
