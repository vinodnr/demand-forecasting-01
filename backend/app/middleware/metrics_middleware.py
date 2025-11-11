import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from ..services import metrics as metrics_svc

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed = time.time() - start
        path = request.url.path
        method = request.method
        status = response.status_code
        # label endpoints by first two path segments to reduce label cardinality if needed
        metrics_svc.record_request(method, path, status, elapsed, service='backend')
        return response
