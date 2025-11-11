#!/usr/bin/env bash
# Basic admin API checks. Assumes backend reachable at localhost:8000 and no auth for admin endpoints in local dev.
set -euo pipefail
BASE=${BASE_URL:-http://localhost:8000}

echo "GET providers:"
curl -sS ${BASE}/v1/admin/llm/providers | jq || true
echo -e "\nGET plan mappings:"
curl -sS ${BASE}/v1/admin/llm/plan-mapping | jq || true
echo -e "\nGET audit (limit 10):"
curl -sS ${BASE}/v1/admin/llm/plan-mapping-audit?limit=10 | jq || true
