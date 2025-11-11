Stripe integration setup
1. Set environment variables in your environment or secrets manager:
   - STRIPE_API_KEY - your Stripe secret key
   - STRIPE_WEBHOOK_SECRET - webhook signing secret for your endpoint

2. Expose webhook endpoint to Stripe (e.g., https://yourdomain.com/v1/stripe/webhook).
3. For local testing you can use stripe CLI: `stripe listen --forward-to localhost:8000/v1/stripe/webhook`

4. Ensure that `external_invoice_id` in `public.invoices` is set to Stripe invoice.id when creating invoices from Stripe events.
