# backend/src/middleware/rate_limit.py
import time, os
from fastapi import Request, HTTPException
try:
    import redis
    _r = redis.from_url(os.getenv('REDIS_URL','redis://localhost:6379/0'))
except Exception:
    _r = None

DEFAULT_RATE = int(os.getenv('RATE_DEFAULT_PER_MIN', '60'))

async def rate_limit_dependency(request: Request):
    # key by org or api key
    org = request.headers.get('x-org') or 'anon'
    window = 60
    limit = DEFAULT_RATE
    key = f'rl:{org}:{int(time.time()/window)}'
    if not _r:
        return True
    count = _r.incr(key)
    if count == 1:
        _r.expire(key, window+2)
    if count > limit:
        raise HTTPException(status_code=429, detail='Rate limit exceeded')
    return True
