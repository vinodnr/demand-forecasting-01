from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
import time, os

# Create a registry so we don't conflict with other process collectors
REGISTRY = CollectorRegistry(auto_describe=True)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method','endpoint','http_status','service'], registry=REGISTRY)
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency seconds', ['method','endpoint','service'], registry=REGISTRY)
LLM_TOKENS_USED = Counter('llm_tokens_used_total', 'Total LLM tokens used', ['org_id','provider','model'], registry=REGISTRY)
ACTIVE_WORKERS = Gauge('active_worker_count', 'Number of active worker processes', ['worker_name'], registry=REGISTRY)
LAST_METRIC_TIME = Gauge('last_metric_timestamp', 'Last time metrics were updated', registry=REGISTRY)

def record_request(method, endpoint, status, elapsed, service='backend'):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=str(status), service=service).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint, service=service).observe(elapsed)
    LAST_METRIC_TIME.set_to_current_time()

def record_llm_usage(org_id, provider, model, tokens):
    try:
        LLM_TOKENS_USED.labels(org_id=org_id, provider=provider, model=model).inc(tokens)
    except Exception:
        # fallback if token not numeric
        pass

def metrics_response():
    # return (content, content_type)
    return generate_latest(REGISTRY), CONTENT_TYPE_LATEST
