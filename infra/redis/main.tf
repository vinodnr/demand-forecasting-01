# Redis module placeholder.
# Option A: Use Upstash (managed serverless Redis) and set REDIS_URL in secrets.
# Option B: Provision a Hetzner server and install Redis (requires manual HA/backup setup).

# Example (Hetzner VM) - NOT production HA:
resource "hcloud_server" "redis" {
  name        = "${var.project_name}-redis-1"
  image       = "ubuntu-24.04"
  server_type = "cx21"
  location    = var.region
  ssh_keys    = length(var.ssh_key_fingerprint) > 0 ? [var.ssh_key_fingerprint] : []
  user_data   = file("${path.module}/redis-cloud-init.tpl")
  labels = {
    project = var.project_name
    role    = "redis"
  }
}
