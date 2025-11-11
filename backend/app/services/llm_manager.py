import os, time, json, logging
from functools import lru_cache
logger = logging.getLogger('llm_manager')

# Redis-backed caching: if REDIS_URL provided and 'redis' package installed we'll use it.
_REDIS_URL = os.getenv('REDIS_URL', None)
_CACHE_TTL = int(os.getenv('LLM_MANAGER_CACHE_TTL_SECONDS', '30'))
_redis_client = None
_try_redis = False
try:
    if _REDIS_URL:
        import redis as _redis_lib
        _redis_client = _redis_lib.from_url(_REDIS_URL, decode_responses=True)
        _try_redis = True
except Exception as e:
    logger.info('Redis not available or not configured for llm_manager cache: %s', e)
    _redis_client = None
    _try_redis = False

# In-memory fallback cache
_memory_cache = {}

def _now():
    return int(time.time())

def _cache_set(key, value, ttl=_CACHE_TTL):
    if _try_redis and _redis_client:
        try:
            _redis_client.setex(key, ttl, json.dumps({'value': value, 'ts': _now()}))
            return
        except Exception as e:
            logger.exception('Redis set failed, falling back to memory: %s', e)
    # fallback
    _memory_cache[key] = {'value': value, 'ts': _now()}

def _cache_get(key):
    if _try_redis and _redis_client:
        try:
            raw = _redis_client.get(key)
            if raw:
                obj = json.loads(raw)
                # check TTL roughly via timestamp
                return obj.get('value')
            return None
        except Exception as e:
            logger.exception('Redis get failed, falling back to memory: %s', e)
    ent = _memory_cache.get(key)
    if not ent:
        return None
    if _now() - ent['ts'] > _CACHE_TTL:
        try:
            del _memory_cache[key]
        except Exception:
            pass
        return None
    return ent.get('value')

# DB helper injector: default attempts to auto-detect common helpers, but allow override.
_db_get_conn = None

def register_db_get_conn(fn):
    global _db_get_conn
    _db_get_conn = fn

def _get_conn():
    if _db_get_conn is not None:
        return _db_get_conn()
    # auto-detect common helpers
    candidates = [
        'backend.app.services.db',
        'backend.app.services.postgres',
        'backend.app.db',
        'backend.app.services.db_manager',
        'backend.app.services.llm_db',
        'backend.app.services.db_client',
    ]
    for mod_path in candidates:
        try:
            mod = __import__(mod_path, fromlist=['get_conn'])
            if hasattr(mod, 'get_conn'):
                return getattr(mod, 'get_conn')()
            if hasattr(mod, 'get_connection'):
                return getattr(mod, 'get_connection')()
        except Exception:
            continue
    # last resort: look for a module named 'db' at package root
    try:
        import backend.app as apppkg
        if hasattr(apppkg, 'get_conn'):
            return getattr(apppkg, 'get_conn')()
    except Exception:
        pass
    raise RuntimeError('Database connection helper not found. Please call register_db_get_conn(get_conn_fn) at app startup to wire your DB helper.')

def get_provider_for_org(org_id=None, plan_id=None):
    """Resolve provider_key for an org, with precedence:
      1) org_llm_override
      2) plan_llm_map (using plan_id or org's subscription plan)
      3) default provider from llm_providers table (first row) - fallback
    Returns provider_key string (e.g., 'openai', 'gemini') or None
    """
    cache_key = f'prov:{org_id}:{plan_id}'
    cached = _cache_get(cache_key)
    if cached:
        return cached

    # 1) check override
    conn = None
    try:
        conn = _get_conn()
        with conn.cursor() as cur:
            if org_id:
                cur.execute('SELECT provider_key FROM public.org_llm_override WHERE org_id=%s ORDER BY created_at DESC LIMIT 1', (org_id,))
                r = cur.fetchone()
                if r and r[0]:
                    _cache_set(cache_key, r[0])
                    return r[0]
            # 2) If plan_id provided, check mapping directly
            if plan_id:
                cur.execute('SELECT provider_key FROM public.plan_llm_map WHERE plan_id=%s LIMIT 1', (plan_id,))
                r = cur.fetchone()
                if r and r[0]:
                    _cache_set(cache_key, r[0])
                    return r[0]
            # 2b) If no plan_id, try to lookup org subscription's plan_id
            if org_id:
                cur.execute('SELECT plan_id FROM public.org_subscriptions WHERE org_id=%s AND status=%s ORDER BY started_at DESC LIMIT 1', (org_id, 'active'))
                r = cur.fetchone()
                if r and r[0]:
                    plan_id_found = r[0]
                    cur.execute('SELECT provider_key FROM public.plan_llm_map WHERE plan_id=%s LIMIT 1', (plan_id_found,))
                    r2 = cur.fetchone()
                    if r2 and r2[0]:
                        _cache_set(cache_key, r2[0])
                        return r2[0]
            # 3) fallback to first provider in llm_providers
            cur.execute('SELECT provider_key FROM public.llm_providers ORDER BY created_at LIMIT 1')
            r = cur.fetchone()
            if r and r[0]:
                _cache_set(cache_key, r[0])
                return r[0]
    except Exception as e:
        logger.exception('Error resolving provider for org %s: %s', org_id, e)
    finally:
        try:
            if conn: conn.close()
        except Exception:
            pass
    return None

def set_org_override(org_id, provider_key, changed_by=None, reason=None):
    conn = None
    try:
        conn = _get_conn()
        with conn.cursor() as cur:
            # find current provider for audit
            cur.execute('SELECT provider_key FROM public.org_llm_override WHERE org_id=%s ORDER BY created_at DESC LIMIT 1', (org_id,))
            old = cur.fetchone()
            old_provider = old[0] if old else None
            cur.execute('INSERT INTO public.org_llm_override (org_id, provider_key, reason) VALUES (%s,%s,%s) RETURNING id', (org_id, provider_key, reason))
            oid = cur.fetchone()[0]
            # audit
            cur.execute('INSERT INTO public.llm_changes_audit (org_id, old_provider, new_provider, changed_by, reason) VALUES (%s,%s,%s,%s,%s)', (org_id, old_provider, provider_key, changed_by, reason))
            conn.commit()
            # update cache
            _cache_set(f'prov:{org_id}:', provider_key)
            return oid
    finally:
        try:
            if conn: conn.close()
        except Exception:
            pass
