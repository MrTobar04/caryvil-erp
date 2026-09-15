terraform {
  required_version = ">= 1.5.0"

  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.2.0"
    }
  }
}

provider "render" {
  api_key = var.render_api_key
}
