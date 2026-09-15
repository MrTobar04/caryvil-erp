# SPEC-1.2.2: Gestión de Variables de Entorno y Secretos

## 1. Objective
Definir, documentar y estandarizar el esquema de configuración mediante variables de entorno y gestión segura de secretos para el ERP Farmacia Caryvil en todos sus entornos (desarrollo local, pipeline de CI/CD y despliegue en producción en Render). Esta especificación previene la exposición accidental de credenciales sensibles, centraliza los parámetros de conexión y proporciona plantillas seguras (`.env.example`) para el equipo de desarrollo.

## 2. Scope
### 2.1. Included
* Creación del archivo de plantilla `.env.example` en la raíz del proyecto con documentación de cada parámetro.
* Definición formal del catálogo de variables de entorno para los entornos local, CI/CD y Render Cloud:
  * Parámetros de base de datos: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`.
  * Parámetros de Odoo: `ADMIN_PASSWORD`, `ODOO_DB_NAME`, `ODOO_STAGE` (`dev` / `staging` / `prod`), `PROXY_MODE`.
  * Parámetros de infraestructura Terraform / Render: `RENDER_API_KEY`, `RENDER_OWNER_ID`, `RENDER_SERVICE_NAME`.
* Configuración de reglas en `.gitignore` para bloquear archivos de credenciales (`.env`, `.env.local`, `*.tfvars`).
* Mecanismo de inyección de variables en `docker-compose.yml` y configuración en GitHub Secrets.

### 2.2. Not Included (Out of Scope)
* Creación de los recursos de Terraform (cubierto en `SPEC-1.2.1`).
* Configuración de flujos de GitHub Actions (cubierto en `SPEC-1.3.1`).

## 3. Context and Restrictions
* **Context:** Garantiza que ningún integrante del equipo ni el repositorio público contengan contraseñas o llaves maestras quemadas en el código fuente (*hardcoded*), cumpliendo con los estándares de seguridad de la industria.
* **Restrictions:**
  * Prohibición estricta de subir archivos `.env` reales al repositorio Git.
  * Los secretos deben ser inyectados en tiempo de despliegue en Render y en tiempo de ejecución en GitHub Actions usando Secret Variables.
  * Todas las contraseñas generadas deben tener un mínimo de 16 caracteres alfanuméricos con caracteres especiales.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-1.1.1` (Configuración del Entorno Docker).
  * `SPEC-1.1.2` (Configuración del Servidor Odoo).
* **Definition of Ready (DoR):**
  * [x] Identificación de todos los servicios que requieren autenticación (PostgreSQL, Odoo Master, Render API).
  * [x] Estructura de nombres de variables estandarizada en mayúsculas sostenidas (`SNAKE_CASE`).

## 5. Design (Implementation Details)
* **Variable Catalog (`.env.example`):**
  ```bash
  # ==========================================
  # CONFIGURACIÓN DE BASE DE DATOS POSTGRESQL
  # ==========================================
  POSTGRES_DB=caryvil_erp_db
  POSTGRES_USER=caryvil_admin
  POSTGRES_PASSWORD=generate_secure_password_here_16_chars
  POSTGRES_HOST=db
  POSTGRES_PORT=5432

  # ==========================================
  # CONFIGURACIÓN DEL SERVIDOR ODOO
  # ==========================================
  ADMIN_PASSWORD=generate_super_admin_master_pwd_here
  ODOO_DB_NAME=caryvil_erp_db
  PROXY_MODE=True
  ODOO_STAGE=dev

  # ==========================================
  # APROVISIONAMIENTO TERRAFORM / RENDER
  # ==========================================
  RENDER_API_KEY=rnd_sample_api_token_value
  RENDER_OWNER_ID=usr-sample_owner_id
  RENDER_SERVICE_NAME=caryvil-erp
  ```
* **Environment Mapping:**
  * **Local:** Archivo `.env` leído por `docker-compose.yml`.
  * **CI/CD:** GitHub Repository Secrets (`RENDER_API_KEY`, `RENDER_OWNER_ID`, `PROD_DB_PASSWORD`, `PROD_ADMIN_PASSWORD`).
  * **Producción (Render):** Render Environment Group o Secret Variables inyectadas por Terraform en el `render_web_service`.

## 6. Acceptance Criteria
* **Scenario 1: Inicialización de entorno local a partir de la plantilla**
  * **Given** Un nuevo desarrollador clonando el repositorio caryvil-erp.
  * **When** Copia `.env.example` a `.env` y ejecuta `docker compose up -d`.
  * **Then** Los contenedores deben leer las variables de entorno sin errores y levantar el sistema con las credenciales definidas en su `.env` local.
* **Scenario 2: Detección y bloqueo de archivos sensibles en Git**
  * **Given** Un desarrollador creando un archivo `.env` o `terraform.tfvars` con contraseñas reales.
  * **When** Intenta ejecutar `git add .` o `git status`.
  * **Then** Los archivos con credenciales reales no deben ser rastreados por Git debido a las reglas de `.gitignore`.
* **Scenario 3: Inyección de variables en Render vía Terraform**
  * **Given** Manifiestos de Terraform ejecutándose en CI/CD con secretos inyectados desde GitHub Secrets.
  * **When** El Web Service de Render es aprovisionado.
  * **Then** Las variables de entorno de producción deben estar disponibles para Odoo sin quedar registradas en texto plano en los logs de la consola.

## 7. Verification Plan
* **Automated Tests:**
  * Script de escaneo pre-commit o linter de seguridad (`git-secrets` / `trufflehog`) en el pipeline para verificar que ningún commit contenga tokens o contraseñas expuestas.
* **Manual Verification:**
  * Validar que `.env` figure en el archivo `.gitignore`.
  * Validar que `.env.example` contenga únicamente valores ficticios o de marcador (*placeholders* descriptivos).

## 8. Security and Privacy
* Enmascaramiento (*masking*) de todas las variables secretas en los registros de ejecución de GitHub Actions.
* Principio de mínimo privilegio: La clave de Render API no debe compartirse entre integrantes, sino inyectarse a través de GitHub Secrets del repositorio.

## 9. Risks and Mitigation
* **Risk:** Exposición accidental de contraseñas de producción en commits públicos.
  * **Mitigation:** Configurar reglas de protección de ramas en GitHub que rechacen commits con secretos y verificación estricta en `.gitignore`.

## 10. Deliverables & Config as Code
* Archivo `.env.example` documentado en la raíz del repositorio.
* Actualización de `.gitignore` con exclusiones completas de archivos de entorno y llaves privadas.
* Guía de configuración de variables en el archivo de documentación técnica.

## 11. Definition of Done (DoD)
* [ ] Archivo `.env.example` creado y probado con `docker compose`.
* [ ] `.gitignore` verificado para asegurar el bloqueo de `.env`, `.env.local` y `*.tfvars`.
* [ ] Variables y secretos requeridos documentados con su tipo y propósito.
* [ ] Revisión de seguridad aprobada por el equipo técnico.
