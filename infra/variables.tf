variable "hetzner_token" {
  type = string
  description = "Hetzner API token (set via environment or vars file)"
}

variable "cloudflare_api_token" {
  type = string
  description = "Cloudflare API token with R2 permissions"
}

variable "cloudflare_account_id" {
  type = string
  description = "Cloudflare account id for R2"
}

variable "project_name" {
  type    = string
  default = "driver-forecast"
}

variable "region" {
  type    = string
  default = "nbg1"
}

variable "ssh_key_fingerprint" {
  type = string
  description = "Hetzner SSH key fingerprint to inject"
  default = ""
}
