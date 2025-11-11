resource "hcloud_firewall" "app_fw" {
  name = "${var.project_name}-fw"
  rules = [
    {
      direction = "in"
      protocol  = "tcp"
      port      = "22"
      source_ips = ["0.0.0.0/0", "::/0"]
    },
    {
      direction = "in"
      protocol  = "tcp"
      port      = "80"
      source_ips = ["0.0.0.0/0", "::/0"]
    },
    {
      direction = "in"
      protocol  = "tcp"
      port      = "443"
      source_ips = ["0.0.0.0/0", "::/0"]
    },
    {
      direction = "in"
      protocol  = "tcp"
      port      = "8000"
      source_ips = ["0.0.0.0/0", "::/0"]
    }
  ]
}

resource "hcloud_firewall_attachment" "attach_app" {
  firewall_id = hcloud_firewall.app_fw.id
  server_id   = hcloud_server.app.id
}
