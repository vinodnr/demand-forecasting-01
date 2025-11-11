# Alert Playbook (Runbook) — Demand Forecasting

This playbook lists common alerts, immediate triage steps, escalation, and post-mortem actions.

## On-call contacts
- Primary on-call: ops@example.com (Slack: @ops_lead)
- Secondary on-call: eng@example.com (Slack: @eng_oncall)
- Pager duty / escalation: PagerDuty service (configured separately)

## Alert: HighErrorRate (5xx)
**Severity:** critical
**What it means:** Increasing number of 5xx responses, users may be unable to use forecast endpoints.
**Immediate steps:**
1. Open Grafana dashboard -> Error Rate panel. Identify recent spike time and affected endpoints.
2. Check backend logs (filter by timestamp) for stack traces and common request paths.
3. If database errors: check Postgres health, slow queries, connection pool exhaustion.
4. If external service errors (e.g., LLM provider): check upstream provider status page and failures in worker logs.
5. If fix requires restart, perform rolling restart of backend pods/containers. Monitor error rate for improvement.
**Escalation:** If not resolved in 15 minutes, paging to secondary on-call and open incident in PagerDuty.  
**Post-incident:** Create an incident ticket with root cause, timeline, and remediation.

## Alert: HighLLMUsage
**Severity:** warning -> can become critical if sustained
**What it means:** LLM token consumption is high and may cause cost overages.
**Immediate steps:**
1. Identify org(s) with highest token usage on the dashboard (use 'Org' variable).
2. Check recent changes: new batch jobs, heavy insight runs, or scheduled forecasts.
3. If a runaway job, suspend the worker/process or revoke API keys temporarily.
4. Consider throttling LLM calls or switching provider if available.
**Escalation:** If cost is expected to exceed monthly budget, notify finance and consider temporary limits for offending orgs.
**Post-incident:** Add quota protections and alerts for sudden spikes.

## Alert: High P95 Latency
**Severity:** critical
**What it means:** 95th percentile latency exceeds target (~500ms).
**Immediate steps:**
1. Check Grafana p95 panel and traces (if available) to find slow endpoints.
2. Inspect database slow queries; run EXPLAIN ANALYZE on suspect queries.
3. Check CPU/memory on backend hosts and worker queues for backlog.
4. If due to LLM calls, investigate provider latency and timeouts; consider fallback provider.

## Alert routing & runbook hygiene
- Always annotate the alert with suspected root cause before paging.
- Triage owner should update the incident ticket with timeline and actions taken.
- After resolution, schedule a post-mortem with stakeholders if severity was critical.

## How to silence alerts for maintenance
- Use Alertmanager silence UI (http://<alertmanager-host>:9093) to create temporary silences for planned maintenance windows.
- Record maintenance windows in team calendar and coordinate with stakeholders.

