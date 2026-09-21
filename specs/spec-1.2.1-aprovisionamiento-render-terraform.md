# SPEC-1.2.1: Aprovisionamiento en Render con Terraform

> **Status:** `Implemented` — 2026-09-20

## 1. Objective
Automatizar la definición, aprovisionamiento y ciclo de vida de la infraestructura cloud en la plataforma Render mediante Terraform (Infraestructura como Código - IaC). Esta especificación permite desplegar de forma desatendida y reproducible el Web Service para el ERP Odoo de Farmacia Caryvil, el servicio de base de datos PostgreSQL gestionado, la parametrización de variables de entorno y el enlace de red entre ambos componentes.

## 2. Scope
### 2.1. Included
* Creación de los módulos y manifiestos de Terraform en el directorio `terraform/`.
* Configuración del proveedor de Terraform para Render (`render-oss/render` o proveedor REST compatible).
* Definición del recurso `render_postgres` para la base de datos PostgreSQL en el plan Free/Starter con versionamiento 15/16.
* Definición del recurso `render_web_service` para la aplicación Odoo, configurado como Docker runtime con asignación de variables de entorno seguras.
* Parametrización de variables de entrada (`variables.tf`): región (`oregon`), plan de servicio, nombre del proyecto, tags y credenciales.
* Definición de salidas de infraestructura (`outputs.tf`): URL pública del ERP, nombre de host interno de la base de datos y estado de los servicios.

### 2.2. Not Included (Out of Scope)
* Configuración de los workflows de ejecución CI/CD en GitHub Actions (cubierto en `SPEC-1.3.1`).
* Resguardo y cifrado de los valores secretos específicos de las credenciales (cubierto en `SPEC-1.2.2`).

## 3. Context and Restrictions
* **Context:** Permite al equipo de ingeniería provisionar o destruir entornos completos de pruebas o producción en Render de forma determinística, eliminando la configuración manual mediante la consola web de Render.
* **Restrictions:**
  * Debe operar bajo el plan gratuito de Render (Free Tier), contemplando la suspensión automática por inactividad tras 15 minutos en el Web Service y la cuota de conexión de PostgreSQL.
  * El estado de Terraform (`terraform.tfstate`) debe protegerse y excluirse del control de versiones público (`.gitignore`).
  * Requiere un API Token de Render válido con permisos de creación de recursos.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-1.1.1` (Configuración del Entorno Docker).
  * `SPEC-1.1.2` (Configuración del Servidor Odoo).
* **Definition of Ready (DoR):**
  * [x] Cuenta de Render creada y API Key generada.
  * [x] Versión de Terraform definida (v1.5.0 o superior).
  * [x] Repositorio de código fuente vinculado a Render o imagen Docker publicada en registro (GitHub Container Registry / Docker Hub).

## 5. Design (Implementation Details)
* **Architecture:**
  * Estructura de archivos en `terraform/`:
    ```
    terraform/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── terraform.tfvars.example
    └── providers.tf
    ```
  * Configuración de proveedor (`providers.tf`):
    ```hcl
    terraform {
      required_version = ">= 1.5.0"
      required_providers {
        render = {
          source  = "render-oss/render"
          version = "~> 1.3.0"
        }
      }
    }
    provider "render" {
      api_key  = var.render_api_key
      owner_id = var.render_owner_id
    }
    ```
  * Recursos principales (`main.tf`):
    * `resource "render_postgres" "caryvil_db"`: PostgreSQL gestionado, plan `free`, versión `15`, base de datos `caryvil_erp_db`, usuario `caryvil_admin`.
    * `resource "render_web_service" "caryvil_odoo"`: Web Service, runtime `image` o `docker`, auto_deploy `true`, plan `free`, variables de entorno vinculadas (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `ADMIN_PASSWORD`).
* **Outputs (`outputs.tf`):**
  * `service_url`: URL HTTPS asignada por Render (`https://caryvil-erp.onrender.com`).
  * `db_internal_host`: Host de conexión interna para el servicio web.

## 6. Acceptance Criteria
* **Scenario 1: Validación y plan de infraestructura exitoso**
  * **Given** Terraform configurado con un API Token de Render válido y `terraform.tfvars` completado.
  * **When** El ingeniero ejecuta `terraform plan`.
  * **Then** Terraform debe generar un plan limpio mostrando la adición de 2 recursos (`render_postgres` y `render_web_service`) sin errores de sintaxis.
* **Scenario 2: Aprovisionamiento y despliegue en la nube**
  * **Given** Un plan de Terraform aprobado.
  * **When** Se ejecuta `terraform apply -auto-approve`.
  * **Then** Render debe instanciar la base de datos PostgreSQL y el Web Service de Odoo, devolviendo una URL pública accesible vía HTTPS en menos de 10 minutos.
* **Scenario 3: Destrucción limpia de recursos temporales**
  * **Given** Un entorno de prueba provisionado con Terraform en Render.
  * **When** Se ejecuta `terraform destroy -auto-approve`.
  * **Then** Todos los recursos asociados en Render deben ser eliminados sin dejar costos residuales ni instancias huérfanas.

## 7. Verification Plan
* **Automated Tests:**
  * `terraform fmt -check` para verificar formato de código HCL.
  * `terraform validate` para verificar la coherencia de tipos y bloques de recursos.
* **Manual Verification:**
  * Acceso al dashboard de Render para comprobar que los servicios creados coincidan exactamente con la configuración de Terraform.
  * Envío de una petición HTTP GET a la URL generada (`outputs.service_url`) esperando código de respuesta HTTP `200` o `303`.

## 8. Security and Privacy
* El token `render_api_key` y las contraseñas de base de datos deben pasarse mediante variables de entorno `TF_VAR_render_api_key` o archivo `terraform.tfvars` ignorado en git.
* La base de datos PostgreSQL debe configurarse con acceso restringido a la red interna de Render siempre que sea posible.

## 9. Risks and Mitigation
* **Risk:** Suspensión del Web Service gratuito en Render tras 15 minutos sin tráfico entrante (*cold start* con delay de 30-50 segundos).
  * **Mitigation:** Documentar el comportamiento de arranque en frío en los supuestos técnicos e implementar endpoints de healthcheck ligeros.
* **Risk:** Límite de cuota de conexiones simultáneas en PostgreSQL gratuito.
  * **Mitigation:** Configurar Odoo con `workers = 0` y `db_maxconn = 10` para no agotar el pool de conexiones de la base de datos.

## 10. Deliverables & Config as Code
* Código fuente HCL completo en `terraform/` (`main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`).
* Plantilla de variables `terraform/terraform.tfvars.example`.
* Reglas en `.gitignore` para bloquear `*.tfstate`, `*.tfstate.backup`, `.terraform/` y `*.tfvars`.

## 11. Definition of Done (DoD)
* [x] Manifiestos de Terraform formateados y validados (`terraform validate`).
* [x] Despliegue de prueba exitoso realizado en Render mediante `terraform apply`.
* [x] URL pública accesible y conectada a la base de datos PostgreSQL.
* [x] Archivos de estado excluidos del repositorio Git.
* [ ] Pull Request revisado y aprobado por el equipo de arquitectura.
