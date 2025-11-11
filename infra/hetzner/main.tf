resource "hcloud_server" "app" {
  name        = "${var.project_name}-app-1"
  image       = "ubuntu-24.04"
  server_type = "cx31"
  location    = var.region
  ssh_keys    = length(var.ssh_key_fingerprint) > 0 ? [var.ssh_key_fingerprint] : []
  user_data   = templatefile("${path.module}/cloud-init.tpl", {
    project_name = var.project_name
  })
  labels = {
    project = var.project_name
    role    = "app"
  }
}

resource "hcloud_floating_ip" "app_ip" {
  type          = "ipv4"
  home_location = var.region
  server_id     = hcloud_server.app.id
}
