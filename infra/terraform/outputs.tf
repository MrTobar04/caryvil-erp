output "odoo_service_url" {
  description = "URL pública HTTPS del servicio Web de Odoo en Render"
  value       = render_web_service.caryvil_odoo.url
}

output "postgres_internal_host" {
  description = "Cadena de conexión interna de PostgreSQL para la red privada de Render"
  value       = render_postgres.caryvil_db.connection_info.internal_connection_string
  sensitive   = true
}

output "postgres_external_host" {
  description = "Cadena de conexión externa de PostgreSQL (usar solo para acceso administrativo manual)"
  value       = render_postgres.caryvil_db.connection_info.external_connection_string
  sensitive   = true
}
