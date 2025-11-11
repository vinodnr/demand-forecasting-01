# backend/src/auth/jwt_middleware.py
from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
import time, requests, threading, os
from typing import Dict, Any, Optional
from functools import lru_cache

# Simple in-memory JWKS cache per-region with TTL
_JWKS_CACHE = {}
_JWKS_LOCK = threading.Lock()
_JWKS_TTL = int(os.getenv('JWKS_CACHE_TTL', '300'))

def fetch_jwks(jwks_url: str) -> Dict[str, Any]:
    now = int(time.time())
    with _JWKS_LOCK:
        entry = _JWKS_CACHE.get(jwks_url)
        if entry and now - entry['ts'] < _JWKS_TTL:
            return entry['jwks']
    r = requests.get(jwks_url, timeout=5)
    r.raise_for_status()
    jwks = r.json()
    with _JWKS_LOCK:
        _JWKS_CACHE[jwks_url] = {'jwks': jwks, 'ts': now}
    return jwks

def verify_jwt(token: str, jwks_url: str, audience: Optional[str]=None):
    jwks = fetch_jwks(jwks_url)
    # Use jose to verify signature; find key by kid
    unverified = jwt.get_unverified_header(token)
    kid = unverified.get('kid')
    # find key
    key = None
    for k in jwks.get('keys', []):
        if k.get('kid') == kid:
            key = k
            break
    if not key:
        raise HTTPException(status_code=401, detail='Invalid token (kid)')
    try:
        public_key = jwt.construct_rsa_public_key(key)
    except Exception:
        public_key = None
    # Let jose decode with jwk directly
    try:
        claims = jwt.decode(token, key, audience=audience, options={'verify_exp': True})
    except JWTError as e:
        raise HTTPException(status_code=401, detail='Token verification failed: ' + str(e))
    return claims

async def jwt_dependency(request: Request):
    # Expect Authorization: Bearer <token> and header X-Region (optional)
    auth = request.headers.get('authorization') or ''
    if not auth.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Missing bearer token')
    token = auth.split(' ',1)[1].strip()
    region = request.headers.get('x-region') or os.getenv('DEFAULT_REGION') or 'us'
    # map region to jwks url via env var like JWKS_URL_US, JWKS_URL_EU
    jwks_env = f'JWKS_URL_{region.upper()}'
    jwks_url = os.getenv(jwks_env)
    if not jwks_url:
        raise HTTPException(status_code=500, detail='JWKS URL not configured for region')
    claims = verify_jwt(token, jwks_url, audience=None)
    # populate request.state
    request.state.user = {
        'sub': claims.get('sub'),
        'email': claims.get('email'),
        'role': claims.get('role'),
        'org_id': claims.get('org_id')
    }
    # If org_id missing, attempt DB lookup by sub/email (consumer must wire db conn setter)
    if not request.state.user.get('org_id'):
        # try to import a lookup helper if available
        try:
            from ..services.identity import resolve_org_for_subject
            org_id = resolve_org_for_subject(claims)
            request.state.user['org_id'] = org_id
        except Exception:
            pass
    return request.state.user

# Helper to set DB session-local vars once you have a DB connection for the transaction
def set_db_session_vars(conn, org_id=None, user_id=None):
    try:
        with conn.cursor() as cur:
            if org_id is not None:
                cur.execute('SET LOCAL app.org_id = %s', (org_id,))
            if user_id is not None:
                cur.execute('SET LOCAL app.user_id = %s', (user_id,))
    except Exception as e:
        # don't raise; it's non-fatal but recommended
        print('set_db_session_vars failed:', e)
