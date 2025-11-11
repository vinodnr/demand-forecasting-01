#!/usr/bin/env bash
# Build and start the monitoring + backend stack (docker-compose).
# Ensure required env vars are exported first:
#   DATABASE_URL, OPENAI_API_KEY, SLACK_WEBHOOK_URL, PAGERDUTY_ROUTING_KEY (optional)
set -euo pipefail
cd "$(dirname "$0")"
echo "Building and starting compose stack..."
docker-compose up -d --build
echo "Stack started. Give containers a few seconds to become healthy."
echo "Check containers with: docker ps"
