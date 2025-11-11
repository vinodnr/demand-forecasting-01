output "app_server_ipv4" {
  description = "Public IPv4 of the app server"
  value       = hcloud_server.app.ipv4_address
  depends_on  = [hcloud_server.app]
  condition   = length([for s in [hcloud_server.app] : s]) > 0
}
