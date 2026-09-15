resource "render_postgres" "caryvil_db" {
  name        = "caryvil-postgres-${var.environment}"
  owner_id    = var.owner_id
  plan        = "free"
  region      = var.region
  version     = "16"
  database_name = var.db_name
  database_user = var.db_user
}

resource "render_web_service" "caryvil_odoo" {
  name     = "caryvil-odoo-${var.environment}"
  owner_id = var.owner_id
  plan     = "free"
  region   = var.region

  runtime_source = {
    image = {
      image_url = "ghcr.io/melissafloresa/odoo_erp_farmacia:latest"
    }
  }

  env_vars = {
    HOST = {
      value = render_postgres.caryvil_db.internal_connection_string
    }
    DB_NAME = {
      value = var.db_name
    }
    USER = {
      value = var.db_user
    }
    PASSWORD = {
      value = render_postgres.caryvil_db.password
    }
    ADMIN_PASSWORD = {
      value = var.odoo_admin_password
    }
  }
}
