# SPEC-1.1.1: Configuración del Entorno Docker

## 1. Objective
Definir y proveer la infraestructura de contenedorización local y de producción para Farmacia Caryvil mediante Docker y Docker Compose. Esta especificación garantiza un entorno estandarizado, reproducible y aislado que ejecuta Odoo 16/17 Community Edition y PostgreSQL 15+, configurando persistencia de datos mediante volúmenes, mapeo de puertos y conectividad de red interna.

## 2. Scope
### 2.1. Included
* Creación de `docker-compose.yml` para orquestar los servicios `web` (Odoo) y `db` (PostgreSQL).
* Creación de `Dockerfile` personalizado para la construcción de la imagen de Odoo con sus utilidades de sistema (`wkhtmltopdf`, librerías C para Python, soporte de localización en español).
* Configuración de volúmenes persistentes para `odoo-web-data` (filestore y sesiones) y `odoo-db-data` (datos de PostgreSQL).
* Configuración de la red interna Docker tipo bridge (`caryvil-net`) para comunicación segura e intercomunicación entre contenedor de base de datos y servidor de aplicaciones.
* Definición del mecanismo de montaje de la carpeta local de módulos personalizados (`./addons` o `./custom_addons`) hacia `/mnt/extra-addons` en el contenedor.

### 2.2. Not Included (Out of Scope)
* Configuración detallada de directivas internas del archivo `odoo.conf` (cubierto en `SPEC-1.1.2`).
* Aprovisionamiento de infraestructura en Render mediante IaC (cubierto en `SPEC-1.2.1`).
* Pipeline de construcción automática de imágenes en GitHub Actions (cubierto en `SPEC-1.3.1`).

## 3. Context and Restrictions
* **Context:** Constituye la base técnica de ejecución para todo el equipo de desarrollo y el entorno de pruebas local, asegurando que todos los desarrolladores trabajen exactamente bajo las mismas versiones de Python, PostgreSQL y dependencias del sistema operativo.
* **Restrictions:**
  * Uso de licencias libres (Odoo Community Edition y PostgreSQL Open Source).
  * Consumo de memoria restringido para compatibilidad con máquinas de desarrollo (mínimo 8 GB RAM) y contenedores livianos.
  * Compatibilidad del contenedor tanto en entornos Windows (WSL2/Docker Desktop) como en Linux.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:** Ninguna (Es la especificación raíz de infraestructura).
* **Definition of Ready (DoR):**
  * [x] Versión de Odoo definida (Community Edition 16.0 o 17.0).
  * [x] Versión de PostgreSQL definida (15-alpine o 16-alpine).
  * [x] Requerimientos de hardware de desarrollo acordados (8 GB RAM mínimo, 20 GB disco).

## 5. Design (Implementation Details)
* **Architecture:**
  * Servicio `db`: Imagen `postgres:15-alpine`, exponiendo puerto interno `5432`, volumen `odoo-db-data:/var/lib/postgresql/data`.
  * Servicio `web`: Construido desde `./Dockerfile`, exponiendo puerto `8069` (HTTP) y `8072` (Longpolling / Chat), dependiente del servicio `db` mediante `depends_on` con condición `service_healthy`.
* **Data Model:** No aplica a nivel de base de datos relacional; modelado de volúmenes en Docker:
  * `odoo-db-data`: Almacenamiento persistente del cluster PostgreSQL.
  * `odoo-web-data`: Almacenamiento del filestore de Odoo (adjuntos, imágenes de medicamentos, firmas).
* **API / Service Contracts:**
  * Puerto Web Odoo: `http://localhost:8069`
  * Puerto Livechat / Longpolling: `http://localhost:8072`
  * Host DB interno: `db:5432`
* **Healthcheck:**
  * `db`: Comando `pg_isready -U odoo -d postgres` cada 5s, timeout 5s, 5 reintentos.
  * `web`: Petición HTTP a `http://localhost:8069/web/health` o socket check.

## 6. Acceptance Criteria
* **Scenario 1: Despliegue exitoso del entorno local**
  * **Given** Docker y Docker Compose instalados en el equipo de desarrollo.
  * **When** El desarrollador ejecuta el comando `docker compose up -d`.
  * **Then** Ambos contenedores (`caryvil-web` y `caryvil-db`) deben iniciar en estado `healthy`, y la interfaz de Odoo debe responder en `http://localhost:8069` mostrando el asistente de creación de base de datos o pantalla de inicio.
* **Scenario 2: Persistencia de datos tras reinicio de contenedores**
  * **Given** Un contenedor Odoo con una base de datos creada y productos cargados.
  * **When** Se ejecuta `docker compose down` seguido de `docker compose up -d`.
  * **Then** La base de datos y los módulos instalados deben permanecer intactos sin pérdida de información.
* **Scenario 3: Montaje en caliente de módulos personalizados**
  * **Given** Un módulo Odoo creado en el directorio local `./custom_addons/caryvil_erp`.
  * **When** Se inicia el contenedor `web`.
  * **Then** El directorio `/mnt/extra-addons` dentro del contenedor debe reflejar los archivos del módulo local de forma sincronizada.

## 7. Verification Plan
* **Automated Tests:** Script de comprobación `docker compose config` para validar sintaxis de compose.
* **Manual Verification:**
  1. Ejecución de `docker compose up -d --build`.
  2. Verificación de logs limpios mediante `docker compose logs -f web`.
  3. Acceso vía navegador a `http://localhost:8069`.
  4. Prueba de parada y arranque para verificar persistencia en volúmenes.

## 8. Security and Privacy
* Aislamiento de PostgreSQL: El puerto 5432 no debe exponerse a la red pública en producción, únicamente en la red interna `caryvil-net`.
* Credenciales parametrizadas mediante variables de entorno, evitando contraseñas quemadas en el repositorio.
* Ejecución del proceso de Odoo dentro del contenedor bajo el usuario sin privilegios `odoo` (UID 101).

## 9. Risks and Mitigation
* **Risk:** Incompatibilidad de paquetes binarios como `wkhtmltopdf` en arquitecturas ARM/x86.
  * **Mitigation:** Utilizar imágenes base oficiales Debian-based con instalación explícita de `wkhtmltopdf 0.12.6` parcheado para Odoo.
* **Risk:** Bloqueo de inicio de Odoo por no disponibilidad inmediata de PostgreSQL.
  * **Mitigation:** Configurar directiva `depends_on` con `condition: service_healthy` en `docker-compose.yml`.

## 10. Deliverables & Config as Code
* Archivo `docker-compose.yml` raíz.
* Archivo `docker-compose.override.yml.example` para desarrolladores locales.
* Archivo `Dockerfile` para la imagen personalizada de Odoo.
* Archivo `.dockerignore` excluyendo `.git`, `.venv`, `.vscode` y temporales.

## 11. Definition of Done (DoD)
* [ ] Archivos `Dockerfile`, `docker-compose.yml` y `.dockerignore` creados y probados.
* [ ] Contenedores inician limpiamente en menos de 30 segundos sin errores en consola.
* [ ] Persistencia de datos verificada con reinicio forzado del daemon Docker.
* [ ] Documentación de ejecución local (`README.md`) redactada con comandos paso a paso.
* [ ] Revisión de código aprobada e integrada a la rama principal.
