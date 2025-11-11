# Monitoring & Observability (Sprint-10)


This directory contains example instrumentation and configs to run monitoring stack for the Demand Forecasting app.


## Components added
- Prometheus metrics via `prometheus_client` (exposes `/metrics` endpoint)
- FastAPI MetricsMiddleware to record request counts & latencies
- OpenTelemetry (OTLP) tracing helper (`backend/app/services/telemetry.py`)
- Structured JSON logging helper (`backend/app/services/logging_config.py`)
- Prometheus config: `backend/monitoring/prometheus.yml`
- Alert rules: `backend/monitoring/alerts.yml`
- Grafana dashboard sample: `backend/monitoring/grafana/demand_forecasting_dashboard.json`

## Quick start (staging)
1. Install monitoring deps: `pip install -r backend/requirements-monitoring.txt`
2. Start Prometheus & Grafana (docker-compose recommended). Use `backend/monitoring/prometheus.yml` as Prometheus config.
3. Ensure your backend is reachable at the address configured in `prometheus.yml` (update target as needed).
4. Start backend. `/metrics` will be available for scraping.
5. Configure Grafana to import the sample dashboard JSON.

## Alerts & SLOs
- Example alerts defined in `backend/monitoring/alerts.yml` include HighErrorRate and HighLLMUsage.
- Define SLOs (example): availability = ratio of successful requests (2xx/total) over 30d; latency p95 < 500ms.

## Notes
- OTLP exporter endpoint can be set via `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable.
- The telemetry setup is best-effort; if the OpenTelemetry packages are not installed, tracing will be disabled gracefully.
