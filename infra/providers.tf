terraform {
  required_version = ">= 1.4.0"
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = ">= 1.35.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = ">= 3.0.0"
    }
  }
}

provider "hcloud" {
  token = var.hetzner_token
}

provider "cloudflare" {
  api_token  = var.cloudflare_api_token
  account_id = var.cloudflare_account_id
}
