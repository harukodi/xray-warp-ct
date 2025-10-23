terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.68.0"
    }
  }
  cloud {
    organization = "xia1997x-org"
    workspaces {
      name = "xray-warp-ct-workspace"
    }
  }
}

variable "do_token" {}
variable "droplet_size" {}
variable "droplet_image" {}
variable "region" {}
variable "domain_name" {
  type      = string
  sensitive = true
  default   = ""
}
variable "cloudflare_token" {
  type      = string
  sensitive = true
  default   = ""
}

provider "digitalocean" {
  token = var.do_token
}

# Create a new Web Droplet in the nyc2 region
resource "digitalocean_droplet" "xray-warp-ct-droplet" {
  name      = "xray-warp-ct-test-droplet"
  image     = var.droplet_image
  region    = var.region
  size      = var.droplet_size
  user_data = <<-CLOUDINIT
    #cloud-config
    packages:
      - git
      - docker.io
      - docker-compose
    runcmd:
      - git clone https://github.com/harukodi/xray-warp-ct.git
      - [ bash, -c, './xray-warp-ct/tests/infrastructure/xray_server_config/setup-xray-server.sh "${DOMAIN_NAME}" "xray-warp-test-path" "eefc8f5f-f2fe-43b5-881c-653994d5a617" "${CLOUDFLARE_TOKEN}"' ]
  CLOUDINIT
}
