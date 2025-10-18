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
variable "hostname" {
  type    = string
  default = "test"
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
  CLOUDINIT
}
