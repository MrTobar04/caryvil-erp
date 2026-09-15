output "odoo_service_url" {
  description = "URL pública del servicio Web de Odoo en Render"
  value       = render_web_service.caryvil_odoo.url
}

output "postgres_host" {
  description = "Host interno de la base de datos PostgreSQL"
  value       = render_postgres.caryvil_db.host
  sensitive   = true
}
