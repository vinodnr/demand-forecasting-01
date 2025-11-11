#!/usr/bin/env bash
# Add a crontab entry to run billing_worker.generate_monthly_invoices at 01:05 UTC on the 1st of every month
CRON_EXPR="5 1 1 * *"
CMD="cd $(pwd) && /usr/bin/env python3 backend/app/workers/billing_worker.py"
# write a cron job for current user (preview)
( crontab -l 2>/dev/null; echo "$CRON_EXPR $CMD >> /var/log/billing_worker.log 2>&1" ) | crontab -
echo "Cron job installed: $CRON_EXPR $CMD"
