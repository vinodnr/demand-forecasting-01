# Monitoring Stack Detailed Guide

This guide explains how to run the local monitoring stack, configure your backend, and import Grafana dashboards.

## Start the monitoring stack (docker-compose)
1. From repository root:
```bash
cd backend/monitoring
docker-compose up -d
```

2. Verify services:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default admin/admin)

## Environment variables & backend configuration
- Ensure backend exposes metrics at `/metrics` (the app wires this endpoint in `backend/app/main.py`).
- If running backend on host, adjust `backend/monitoring/prometheus.yml` scrape target to `host.docker.internal:8000` (or the reachable host).
- For OpenTelemetry export to collector, set `OTEL_EXPORTER_OTLP_ENDPOINT` to `http://<collector_host>:4318` (collector in docker-compose exposes 4318).

## Import Grafana dashboard
1. Open Grafana UI -> Dashboards -> Manage -> Import.
2. Upload `backend/monitoring/grafana/demand_forecasting_full_dashboard.json` or use the provisioning configured in docker-compose (provisioning may auto-load).

## Verify metrics & SLOs
- In Prometheus, run queries:
  - `job:http_requests:rate1m`
  - `job:request_latency_p95:histogram`
  - `job:llm_tokens_rate:1h`
  - `slo:availability_30d`
- Check alert rules in Prometheus UI -> Alerts.

## Notes on worker labels
- Worker labels are generated using `backend/app/services/worker_label_map.get_worker_label(filename)` to create readable labels like "Insights" or "Billing".
- If you prefer different labels, edit `backend/app/services/worker_label_map.py`.

## Running locally with backend
1. Start backend (ensure monitoring requirements are installed):
```bash
pip install -r backend/requirements-monitoring.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
2. The `/metrics` endpoint should now be scrapeable by Prometheus.

## Troubleshooting
- If no metrics appear, check backend logs for import errors or missing packages.
- Ensure firewall/ports allow Prometheus to reach the backend.



## Custom Grafana Dashboard
Import the file `grafana/demand_forecasting_custom_dashboard.json` into Grafana (Dashboards → Import) or use provisioning to load it.


## Grafana provisioning & Alerting

Grafana dashboards and datasource are provisioned from `backend/monitoring/grafana/provisioning` directory. To enable Slack alerts, update `notification_channels/notification_channels.yml` with your Slack webhook URL or configure via Grafana UI.

After editing provisioning files restart the grafana container: `docker-compose restart grafana`.


## Sending a test alert to Alertmanager (verify notifications)
You can send a test alert to Alertmanager to verify end-to-end delivery to Slack and PagerDuty.

1. Ensure Alertmanager is running (default: http://localhost:9093).
2. Set your Slack webhook and PagerDuty routing key as environment variables when running docker-compose:
   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/AAA/BBB/CCC"
   export PAGERDUTY_ROUTING_KEY="your_pagerduty_integration_key"
   cd backend/monitoring
   docker-compose up -d
   ```
3. Run the test alert script:
   ```bash
   python backend/monitoring/send_test_alert.py --org org_demo --severity critical --summary "Test alert" --instance local-test
   ```
4. Check Alertmanager UI (http://localhost:9093) -> Alerts and Grafana/Slack/PagerDuty for notifications.

## PagerDuty integration notes
- The `pagerduty_configs` in `alertmanager.yml` uses `${PAGERDUTY_ROUTING_KEY}` so you should supply this as an environment variable (or via your orchestration secrets).
- Create a PagerDuty "Events API v2" service or integration and copy the Integration Key into `PAGERDUTY_ROUTING_KEY`.
- PagerDuty events will be created for alerts matching `severity=critical` per the routing rules above.


## Running the full monitoring stack including the backend
You can run the entire monitoring stack including the backend service in one docker-compose invocation. This is useful for local dev where you want the backend container to run together with Prometheus, Grafana, Alertmanager, OTEL collector and Redis.

Start the stack:
```bash
cd backend/monitoring
docker-compose up -d
```
This will build the backend image from the `backend/` directory (Dockerfile expected at `backend/Dockerfile`) and start the service. The backend will be reachable at `http://localhost:8000` and exposes `/metrics` for Prometheus scraping.

If you prefer to keep the backend running on your host (not in the compose), set `REDIS_URL` in your host environment and start the compose as usual; the backend container is optional.


## Dockerfile selection & healthcheck behavior
- The compose file supports selecting the Dockerfile via environment variable `BACKEND_DOCKERFILE`. By default it uses `Dockerfile` in the backend/ directory. To use a production Dockerfile (e.g. `Dockerfile.prod`), export:

```bash
export BACKEND_DOCKERFILE=Dockerfile.prod
```

- A build arg `BACKEND_ENV` is provided to pass environment context into your Dockerfile (`development`, `staging`, `production`, etc.).

- Healthcheck: the backend service healthcheck now attempts `/metrics` first and falls back to `/health`. If neither responds with HTTP 200, the container is marked unhealthy. You can customize this by adding a `/health` endpoint that returns 200 when ready.

## Dev workflow (live code mounting)
- Use the dev override compose to mount your backend source into the container and enable auto-reload. Example:

```bash
cd backend/monitoring
# Builds with Dockerfile.dev and mounts source so code changes are reflected without rebuild
docker-compose -f docker-compose.yml -f docker-compose.backend.dev.yml up --build
```

Make sure you have a `Dockerfile.dev` in the `backend/` directory that installs dev deps and sets the working directory appropriately. A minimal Dockerfile.dev example:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```


Admin UI pages added: /admin/AdminRoles, /admin/AdminInvites, /admin/AdminAudit


Privacy & GDPR: added frontend pages under /privacy and backend endpoints /v1/privacy/* for deletion requests. Ensure auth is wired in production.


Sprint 12-A: Added Trust & Transparency frontend pages under /trust and /app/trust/*; ensure public routes are served from app/(public) if using Next.js app router.
