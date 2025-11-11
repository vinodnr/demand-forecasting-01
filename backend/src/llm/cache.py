# backend/src/llm/cache.py
import os, json, time
try:
    import redis
    _r = redis.from_url(os.getenv('REDIS_URL','redis://localhost:6379/0'))
except Exception:
    _r = None
TTL = int(os.getenv('LLM_CACHE_TTL', '300'))

def cache_key(org_id, prompt_hash):
    return f'llm:cache:{org_id}:{prompt_hash}'

def get(org_id, key):
    if _r:
        v = _r.get(key)
        return json.loads(v) if v else None
    return None

def set(org_id, key, value):
    if _r:
        _r.setex(key, TTL, json.dumps(value))
