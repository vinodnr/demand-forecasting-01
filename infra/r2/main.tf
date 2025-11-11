resource "cloudflare_r2_bucket" "datasets" {
  account_id = var.cloudflare_account_id
  name       = "${var.project_name}-datasets"
}
