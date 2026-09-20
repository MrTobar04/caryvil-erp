# ==============================================================================
# FARMACIA CARYVIL ERP — Infraestructura en Render
# SPEC-1.2.1: Aprovisionamiento con Terraform
# ==============================================================================

# ------------------------------------------------------------------------------
# Base de Datos PostgreSQL Gestionada
# Plan: free | Versión: 16 | Región: oregon (US West)
# ------------------------------------------------------------------------------
resource "render_postgres" "caryvil_db" {
  name          = "caryvil-postgres-${var.environment}"
  plan          = "free"
  region        = var.region
  version       = "16"
  database_name = var.db_name
  database_user = var.db_user
}

# ------------------------------------------------------------------------------
# Web Service — Odoo 17 Community (Runtime: Docker Image)
# Imagen publicada en GitHub Container Registry (GHCR)
# Requiere: render_postgres.caryvil_db desplegado y activo
# ------------------------------------------------------------------------------
resource "render_web_service" "caryvil_odoo" {
  name   = "caryvil-erp-${var.environment}"
  plan   = "free"
  region = var.region

  runtime_source = {
    image = {
      image_url = "ghcr.io/mrtobar04/caryvil-erp"
      tag       = "latest"
    }
  }

  # Variables de entorno inyectadas en el contenedor Odoo.
  # - HOST: cadena de conexión interna a la BD en la red privada de Render
  # - PORT: puerto estándar de PostgreSQL
  # - USER: usuario de la BD provisto por Render Postgres
  # - PASSWORD: contraseña de la BD auto-generada por Render Postgres
  # - DB_NAME: nombre de la base de datos de trabajo de Odoo
  # - ADMIN_PASSWORD: contraseña maestra de gestión de Odoo (admin_passwd)
  # - PROXY_MODE: True es obligatorio detrás del reverse-proxy de Render
  env_vars = {
    HOST = {
      value = render_postgres.caryvil_db.connection_info.internal_connection_string
    }
    PORT = {
      value = "5432"
    }
    USER = {
      value = render_postgres.caryvil_db.database_user
    }
    PASSWORD = {
      value = render_postgres.caryvil_db.connection_info.password
    }
    DB_NAME = {
      value = var.db_name
    }
    ADMIN_PASSWORD = {
      value = var.odoo_admin_password
    }
    PROXY_MODE = {
      value = "True"
    }
  }
}
