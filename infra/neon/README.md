# Neon Postgres provisioning notes

Neon is often provisioned via the Neon console. At minimum:
1. Create project & branch DB in Neon console.
2. Create a DB user for the app with least privilege.
3. Copy DATABASE_URL into your secret store (e.g., Hetzner Vault or other secret manager).
4. Ensure network allowlist includes your Hetzner app IP(s) if you restrict by IP.
