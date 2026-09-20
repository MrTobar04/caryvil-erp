# Guía Técnica: Gestión de Variables de Entorno y Secretos

**Proyecto:** Farmacia Caryvil ERP  
**Especificación:** [SPEC-1.2.2](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/specs/spec-1.2.2-gestion-variables-entorno-secretos.md)  
**Entornos:** Local (Docker Compose), CI/CD (GitHub Actions), Producción/Staging (Render Cloud)  

---

## 1. Propósito y Principios de Seguridad

El objetivo de esta guía es estandarizar la configuración del sistema mediante variables de entorno desacopladas del código fuente, garantizando el cumplimiento estricto de las directivas de seguridad informática:

1. **Cero Secretos en Git:** Prohibición absoluta de versionar credenciales reales, tokens de API o contraseñas maestras en el repositorio.
2. **Uso Exclusivo de Plantillas:** Los desarrolladores deben utilizar `.env.example` y `terraform.tfvars.example` como referencia estructural.
3. **Principio de Mínimo Privilegio:** Cada entorno únicamente recibe las variables indispensables para su operación.
4. **Enmascaramiento en CI/CD:** Todos los secretos inyectados en GitHub Actions deben registrarse en *Repository Secrets* para que sean enmascarados en los logs de ejecución.
5. **Complejidad de Contraseñas:** En entornos de staging y producción, toda contraseña generada debe contar con un mínimo de **16 caracteres alfanuméricos y símbolos especiales**.

---

## 2. Catálogo Estandarizado de Variables de Entorno

A continuación se detalla el diccionario maestro de variables utilizadas en los distintos componentes de la arquitectura:

### 2.1. Base de Datos PostgreSQL

| Variable | Entornos | Sensibilidad | Tipo | Valor Ejemplo / Default | Descripción y Propósito |
|---|---|---|---|---|---|
| `POSTGRES_DB` | Local, CI/CD, Render | Público | String | `caryvil_dev` / `caryvil_erp_db` | Nombre de la base de datos PostgreSQL creada al inicializar la instancia. |
| `POSTGRES_USER` | Local, CI/CD, Render | Público | String | `odoo` / `caryvil_admin` | Nombre del usuario administrador de PostgreSQL. |
| `POSTGRES_PASSWORD` | Local, CI/CD, Render | **Secreto** | String | `generate_secure_password_16_chars` | Contraseña para autenticar contra la base de datos PostgreSQL. |
| `POSTGRES_HOST` / `HOST` | Local, CI/CD, Render | Público | String | `db` (local) / `dpg-xxx` (Render) | Hostname de red para resolver el servicio de base de datos. En Render se inyecta como `HOST`. |
| `POSTGRES_PORT` / `DB_PORT` | Local, CI/CD, Render | Público | Entero | `5432` | Puerto TCP de PostgreSQL. En Render se inyecta como `DB_PORT` para no colisionar con la variable reservada `PORT`. |

### 2.2. Servidor de Aplicaciones Odoo 17

| Variable | Entornos | Sensibilidad | Tipo | Valor Ejemplo / Default | Descripción y Propósito |
|---|---|---|---|---|---|
| `ADMIN_PASSWORD` | Local, Render | **Secreto** | String | `admin_caryvil_secret_2026` | Contraseña maestra (*Master Password*) de Odoo para crear, respaldar y restaurar bases de datos. |
| `DB_NAME` / `ODOO_DB_NAME` | Local, Render | Público | String | `caryvil_dev` | Nombre de la base de datos activa a la que Odoo se conecta automáticamente al iniciar. |
| `ODOO_STAGE` | Local, Render | Público | Enum | `dev` / `staging` / `prod` | Identificador de la etapa de despliegue para auditoría y telemetría. |
| `PROXY_MODE` | Local, Render | Público | Booleano | `True` | Habilita el manejo correcto de cabeceras HTTP (`X-Forwarded-For`, `X-Forwarded-Proto`) detrás de proxies inversos. |
| `PORT` | Local, Render | Público | Entero | `8069` (local) / Dinámico (Render) | Puerto HTTP del servidor web Odoo. En Render es inyectado por la plataforma; en local por defecto es 8069. |
| `ODOO_HTTP_PORT` | Local | Público | Entero | `8069` | Puerto expuesto en el host para la interfaz web principal de Odoo. |
| `ODOO_CHAT_PORT` | Local | Público | Entero | `8072` | Puerto expuesto en el host para el servidor de Longpolling (chat en tiempo real y mensajería). |

### 2.3. Infraestructura y Despliegue en la Nube (Terraform & Render)

| Variable | Entornos | Sensibilidad | Tipo | Valor Ejemplo / Default | Descripción y Propósito |
|---|---|---|---|---|---|
| `RENDER_API_KEY` | CI/CD, Local TF | **Secreto** | String | `rnd_sample_api_token_xxxx` | Token de autenticación de Render API generado desde Account Settings -> API Keys. |
| `RENDER_OWNER_ID` | CI/CD, Local TF | **Secreto** | String | `usr-sample...` o `tea-sample...` | Identificador único del usuario o equipo propietario del espacio de trabajo en Render. |
| `RENDER_REGION` | CI/CD, Local TF | Público | Enum | `oregon` | Región geográfica donde se aprovisionan los recursos de cómputo y almacenamiento. |
| `RENDER_SERVICE_NAME` | CI/CD, Local TF | Público | String | `caryvil-erp` | Prefijo o nombre base del servicio web aprovisionado. |
| `RENDER_DEPLOY_HOOK_URL`| CI/CD | **Secreto** | URL | `https://api.render.com/deploy/srv-xxx?key=yyy` | Webhook HTTP POST para disparar el re-despliegue automático tras publicar la imagen en GHCR. |

---

## 3. Puesta en Marcha en Entorno Local (Paso a Paso)

Para inicializar el entorno de desarrollo local por primera vez:

1. **Crear archivo `.env` a partir de la plantilla:**
   ```bash
   cp .env.example .env
   ```
2. **Ajustar credenciales locales en `.env` (si es necesario):**
   Asegúrate de que las contraseñas cumplan con un formato seguro. Para desarrollo local se proporcionan valores funcionales por defecto.
3. **Levantar los servicios con Docker Compose:**
   ```bash
   docker compose -f infra/compose/docker-compose.yml up -d
   ```
4. **Verificar la lectura de variables:**
   ```bash
   docker compose -f infra/compose/docker-compose.yml config
   ```
   El comando mostrará la configuración completamente interpolada sin advertencias de variables indefinidas.

---

## 4. Configuración en GitHub Actions (CI/CD)

En el repositorio de GitHub (Settings -> Secrets and variables -> Actions), deben configurarse los siguientes secretos:

* `RENDER_API_KEY`: Clave API para aprovisionamiento de infraestructura mediante Terraform.
* `RENDER_OWNER_ID`: ID del propietario/equipo de la cuenta de Render.
* `RENDER_DEPLOY_HOOK_URL`: URL del webhook para notificar a Render de nuevas imágenes en GHCR.
* `CR_PAT` o `GITHUB_TOKEN`: Token para autenticar en GitHub Container Registry (`ghcr.io`).

---

## 5. Auditoría de Seguridad y Prevención de Fugas

* **Reglas de Gitignore:** El archivo [`.gitignore`](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/.gitignore) bloquea activamente:
  * `.env`, `.env.local`, `.env.*.local`, `.env.*` (excepto `.env.example`).
  * `*.tfvars`, `*.tfvars.json` (excepto `terraform.tfvars.example`).
  * `*.tfstate`, `*.tfstate.*`, `.terraform/`.
* **Verificación de Bloqueo:**
  ```bash
  git check-ignore -v .env .env.local infra/terraform/terraform.tfvars
  ```
* **Suite de Pruebas Automatizadas:**
  La suite [`tests/test_spec_1_2_2_env_secrets.py`](file:///d:/UDB/CICLO-10-2026/DES/PROYECTO/caryvil-erp/tests/test_spec_1_2_2_env_secrets.py) verifica programáticamente que ningún archivo rastreado en Git contenga credenciales reales y que los archivos sensibles se mantengan excluidos.
