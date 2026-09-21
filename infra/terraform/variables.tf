variable "render_api_key" {
  description = "API Key para autenticación en la plataforma Render"
  type        = string
  sensitive   = true
}

variable "render_owner_id" {
  description = "ID del usuario o equipo propietario en Render (formato usr-... o tea-...)"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Ambiente de despliegue (dev | staging | production)"
  type        = string
  default     = "dev"
}

variable "region" {
  description = "Región geográfica de Render (oregon | frankfurt | ohio | singapore)"
  type        = string
  default     = "oregon"
}

variable "db_name" {
  description = "Nombre de la base de datos PostgreSQL de Odoo"
  type        = string
  default     = "caryvil_erp_db"
}

variable "db_user" {
  description = "Usuario administrador de PostgreSQL"
  type        = string
  default     = "caryvil_admin"
}

variable "odoo_admin_password" {
  description = "Contraseña maestra para la gestión de bases de datos de Odoo (admin_passwd en odoo.conf)"
  type        = string
  sensitive   = true
}
