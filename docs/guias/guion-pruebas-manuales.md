# Guión de Pruebas Manuales - Farmacia Caryvil ERP

Guía operativa para la ejecución, validación y verificación funcional manual del sistema **Farmacia Caryvil ERP**, desarrollado sobre **Odoo 17.0 Community Edition** y **PostgreSQL 16**.

---

### Índice
- [1. Propósito](#1-propósito)
- [2. Configuración Inicial](#2-configuración-inicial)
- [3. Problemas Comunes](#3-problemas-comunes)
- [4. Flujos de Verificación](#4-flujos-de-verificación)
  - [Flujo 1.1: Despliegue, Persistencia y Montaje en Contenedores Docker (SPEC-1.1.1)](#flujo-11-despliegue-persistencia-y-montaje-en-contenedores-docker-spec-111)
  - [Flujo 1.2: Parámetros del Servidor Odoo, Proxy Inverso y Gestión de Base de Datos (SPEC-1.1.2)](#flujo-12-parámetros-del-servidor-odoo-proxy-inverso-y-gestión-de-base-de-datos-spec-112)
  - [Flujo 1.3: Aprovisionamiento de Infraestructura en Render con Terraform (SPEC-1.2.1)](#flujo-13-aprovisionamiento-de-infraestructura-en-render-con-terraform-spec-121)
  - [Flujo 1.4: Verificación de Variables de Entorno y Bloqueo de Secretos (SPEC-1.2.2)](#flujo-14-verificación-de-variables-de-entorno-y-bloqueo-de-secretos-spec-122)
  - [Flujo 1.5: Pipeline CI/CD con GitHub Actions y Despliegue Automático (SPEC-1.3.1)](#flujo-15-pipeline-cicd-con-github-actions-y-despliegue-automático-spec-131)
  - [Flujo 2.1: Definición de Roles, Grupos de Seguridad y Herencia de Privilegios (SPEC-2.2.1)](#flujo-21-definición-de-roles-grupos-de-seguridad-y-herencia-de-privilegios-spec-221)
  - [Flujo 6.1: Directorio y Gestión de Proveedores Farmacéuticos (SPEC-6.1.1)](#flujo-61-directorio-y-gestión-de-proveedores-farmacéuticos-spec-611)
  - [Flujo 6.2: Catálogo de Precios y Condiciones de Proveedores (SPEC-6.2.1)](#flujo-62-catálogo-de-precios-y-condiciones-de-proveedores-spec-621)
  - [Flujo 8.1: Visibilidad de Abonos y Estado de Pago a Proveedores (SPEC-8.1.2)](#flujo-81-visibilidad-de-abonos-y-estado-de-pago-a-proveedores-spec-812)
  - [Flujo 8.2: Recepción de Mercadería y Captura Obligatoria de Lotes (SPEC-8.2.1)](#flujo-82-recepción-de-mercadería-y-captura-obligatoria-de-lotes-spec-821)
  - [Flujo 8.3: Actualización Automática de Stock y Cierre de Compras (SPEC-8.2.2)](#flujo-83-actualización-automática-de-stock-y-cierre-de-compras-spec-822)
  - [Flujo 8.4: Control de Discrepancias, Daños y Backorders en Recepción (SPEC-8.2.3)](#flujo-84-control-de-discrepancias-daños-y-backorders-en-recepción-spec-823)

---

## 1. Propósito

Establecer una metodología estructurada paso a paso para la verificación manual y validación funcional del sistema **Farmacia Caryvil ERP**. Este documento permite a desarrolladores, evaluadores de calidad (QA) y usuarios clave (*stakeholders*) validar de forma exhaustiva los flujos críticos de negocio:

- **Compras y Abastecimiento:** Emisión de órdenes de compra a laboratorios y recepción física con registro obligatorio de número de lote y fecha de caducidad.
- **Gestión Farmacéutica e Inventario:** Fraccionamiento de unidades (cajas, blísteres, unidades) y control de trazabilidad de lotes.
- **Venta y Despacho FEFO:** Salida prioritaria de medicamentos por fecha de vencimiento más próxima (*First Expired, First Out*).
- **Facturación y Cumplimiento Tributario:** Emisión de tickets térmicos de 80mm con validación de identificadores salvadoreños (DUI/NIT) y cálculo exacto de IVA (13%).
- **Tablero de Control:** Visualización de KPIs de venta, alertas de stock mínimo y monitor preventivo de caducidades (30, 60 y 90 días).

Este guión complementa la suite de pruebas unitarias automatizadas (`specs/spec-11.1.*`) asegurando que la experiencia de usuario y la integridad operativa se ajusten a las especificaciones formales (SDD).

---

## 2. Configuración Inicial

### 2.1. Prerrequisitos del Sistema
Para ejecutar las pruebas manuales localmente, asegúrate de contar con:
- **Docker Engine** v24.0+ y **Docker Compose** v2.20+
- **Git** v2.30+
- **Terraform CLI** v1.5.0+ instalado y disponible en el `PATH` del sistema.
- **Navegador Web Moderno** (Google Chrome, Mozilla Firefox, Microsoft Edge o Safari)
- **Herramienta de terminal / Shell** (Bash, Zsh o PowerShell)

### 2.2. Puesta en Marcha del Entorno
1. **Navegar a la raíz del repositorio:**
   ```bash
   cd caryvil-erp
   ```

2. **Compilar y levantar los contenedores en segundo plano:**
   ```bash
   docker compose -f infra/compose/docker-compose.yml up -d --build
   ```

3. **Verificar el estado de los servicios:**
   ```bash
   docker compose -f infra/compose/docker-compose.yml ps
   ```
   *Ambos contenedores (`caryvil-web` y `caryvil-db`) deben encontrarse en estado `Up` / `healthy`.*

4. **Inspeccionar logs de inicialización (opcional):**
   ```bash
   docker compose -f infra/compose/docker-compose.yml logs -f web
   ```

### 2.3. Parámetros de Acceso y Credenciales

| Parámetro | Valor por Defecto |
|---|---|
| **URL del Servicio Web** | [http://localhost:8069](http://localhost:8069) |
| **Base de Datos** | `caryvil_dev` |
| **Puerto PostgreSQL** | `5432` |
| **Contraseña Maestra de Odoo** | `admin_caryvil_secret_2026` |

#### Matriz de Usuarios y Roles de Prueba (SPEC-2.2.1):

| Rol de Usuario | Grupo Técnico | Login / Correo | Contraseña | Alcance Operativo |
|---|---|---|---|---|
| **Administrador General / Propietaria** | `group_caryvil_manager` | `admin` o `admin_caryvil@caryvil.com` | `admin` o `admin123` | Control total, dashboard gerencial, anulación de transacciones y configuración |
| **Encargado de Compras e Inventario** | `group_caryvil_inventory_purchases` | `compras@caryvil.com` | `compras123` | Órdenes de compra a laboratorios, recepción con lotes/vencimiento, catálogo y ajustes de existencias |
| **Cajero / Dependiente de Mostrador** | `group_caryvil_cashier` | `cajero@caryvil.com` | `cajero123` | Punto de venta en mostrador, consulta de existencias/precios, registro de clientes y factura simple |

### 2.4. Instalación y Verificación del Módulo `caryvil_erp`
1. Ingresar a [http://localhost:8069](http://localhost:8069) con el usuario `admin`.
2. Activar el **Modo Desarrollador** navegando a **Ajustes** -> **Activar modo de desarrollador** (o agregando `?debug=1` en la URL del navegador).
3. Acceder al menú **Aplicaciones**.
4. Hacer clic en el botón **Actualizar lista de aplicaciones** en la barra superior.
5. En la barra de búsqueda, escribir `Farmacia Caryvil ERP` (módulo técnico: `caryvil_erp`).
6. Hacer clic en **Instalar** (o **Actualizar** si ya está presente).
7. Verificar que el menú principal **Farmacia Caryvil** aparezca disponible en la barra de navegación superior.

---

## 3. Problemas Comunes

| Incidente / Síntoma | Causa Probable | Solución Paso a Paso |
|---|---|---|
| **Error `Bind for 0.0.0.0:8069 failed: port is already allocated`** | Existe otra instancia de Odoo o un proceso local ocupando el puerto `8069`. | 1. Detener el proceso en conflicto o cambiar el puerto mapeado en `infra/compose/docker-compose.override.yml`.<br>2. En Windows: `Get-Process -Id (Get-NetTCPConnection -LocalPort 8069).OwningProcess \| Stop-Process -Force`. |
| **Error `Bind for 0.0.0.0:5432 failed: port is already allocated`** | Servicio local de PostgreSQL nativo ejecutándose en la máquina host. | 1. Detener temporalmente el servicio local de PostgreSQL (`Stop-Service postgresql*` en PowerShell).<br>2. O eliminar el mapeo del puerto externo `5432` en el compose para aislar la base de datos a la red interna. |
| **Odoo reinicia constantemente con error `Connection to PostgreSQL failed`** | El contenedor de base de datos aún no completa su inicialización interna de cluster. | El archivo `entrypoint.sh` y el `depends_on` con `condition: service_healthy` gestionan la espera automáticamente. Esperar 15-20 segundos y revisar con `docker compose -f infra/compose/docker-compose.yml logs -f web`. |
| **Los cambios en archivos de `./custom_addons` no se reflejan** | El modo desarrollador no está activo o se requiere recarga de assets en caliente. | 1. Iniciar los contenedores con la configuración `docker-compose.override.yml` (`--dev=all`).<br>2. En el navegador, forzar recarga dura con `Ctrl + F5` o actualizar el módulo desde **Aplicaciones** -> **Actualizar**. |
| **Permisos denegados en `/var/lib/odoo` o `/mnt/extra-addons`** | Permisos del host incompatibles con el usuario `odoo` (UID 101). | Ejecutar en el host o contenedor: `docker compose -f infra/compose/docker-compose.yml exec -u 0 web chown -R odoo:odoo /var/lib/odoo /mnt/extra-addons`. |

---

## 4. Flujos de Verificación

### Flujo 1.1: Despliegue, Persistencia y Montaje en Contenedores Docker (SPEC-1.1.1)

1. **Validación de sintaxis de orquestación:** En la terminal del host, ejecutar `docker compose -f infra/compose/docker-compose.yml config`, debes observar la definición completa del esquema YAML resuelta sin errores de sintaxis y con los servicios `db` y `web` vinculados a la red `caryvil-net`.
2. **Construcción y arranque de servicios:** Ejecutar `docker compose -f infra/compose/docker-compose.yml up -d --build`, debes ver cómo Docker descarga/compila las imágenes y levanta los contenedores `caryvil-db` y `caryvil-web` en segundo plano en menos de 30 segundos.
3. **Comprobación de estado de salud (Healthcheck):** Ejecutar `docker compose -f infra/compose/docker-compose.yml ps`, debes observar ambos contenedores en estado `Up (healthy)` con los puertos `5432->5432/tcp` en `db` y `8069->8069/tcp`, `8072->8072/tcp` en `web`.
4. **Verificación de logs de conectividad:** Ejecutar `docker compose -f infra/compose/docker-compose.yml logs web`, debes observar en consola el mensaje `=== [Caryvil ERP] Base de datos PostgreSQL disponible ===` seguido del inicio del servidor HTTP de Odoo listo para recibir peticiones en el puerto `8069`.
5. **Acceso web inicial al ERP:** Abrir el navegador web y navegar a [http://localhost:8069](http://localhost:8069), debes ver la pantalla de inicio de sesión de Odoo o el asistente del gestor de base de datos cargando limpiamente y sin errores de hoja de estilos ni librerías faltantes.
6. **Verificación del montaje en caliente de addons:** En el host, crear un archivo de prueba en `custom_addons/caryvil_erp/test_sync.txt` con el contenido `sincronizacion_activa` y ejecutar en terminal `docker compose -f infra/compose/docker-compose.yml exec web cat /mnt/extra-addons/caryvil_erp/test_sync.txt`, debes ver en la salida del contenedor el texto `sincronizacion_activa`, confirmando la sincronización bidireccional inmediata (luego eliminar el archivo temporal `custom_addons/caryvil_erp/test_sync.txt`).
7. **Verificación de usuario no privilegiado en runtime:** Ejecutar `docker compose -f infra/compose/docker-compose.yml exec web whoami`, debes observar la respuesta `odoo` (UID 101), garantizando que el proceso no corre como `root`.
8. **Prueba de persistencia tras reinicio:** Con el sistema iniciado, detener los contenedores mediante `docker compose -f infra/compose/docker-compose.yml down` y volver a levantarlos con `docker compose -f infra/compose/docker-compose.yml up -d`, navegar nuevamente a [http://localhost:8069](http://localhost:8069) y debes comprobar que el estado de la base de datos `caryvil_dev` y las sesiones persisten intactas en los volúmenes `caryvil_odoo_db_data` y `caryvil_odoo_web_data`.

#### Casos Límite / Rutas de Excepción:
1. **Recuperación ante caída o demora de PostgreSQL:** Detener el contenedor de base de datos con `docker compose -f infra/compose/docker-compose.yml stop db` y reiniciar el contenedor web con `docker compose -f infra/compose/docker-compose.yml restart web`, al inspeccionar `docker compose -f infra/compose/docker-compose.yml logs -f web` debes ver que el script `entrypoint.sh` entra en bucle de espera sin abortar el contenedor (`Verificando disponibilidad de PostgreSQL...`), y al reiniciar la base de datos con `docker compose -f infra/compose/docker-compose.yml start db`, el servicio web debe detectar la conexión y arrancar automáticamente.

---

### Flujo 1.2: Parámetros del Servidor Odoo, Proxy Inverso y Gestión de Base de Datos (SPEC-1.1.2)

1. **Detección e indexación del módulo en Addons Path (UI):** Ingresar al navegador web en [http://localhost:8069](http://localhost:8069), iniciar sesión como administrador (`admin` / `admin`), activar el modo desarrollador (`?debug=1`), navegar a **Aplicaciones**, presionar el botón **Actualizar lista de aplicaciones**, remover cualquier filtro predeterminado en la barra de búsqueda y escribir `caryvil_erp`, debes ver la tarjeta del módulo **Farmacia Caryvil ERP** (versión `17.0.1.0.0`, autor *Farmacia Caryvil*) listada en estado *"No instalado"* y lista para su despliegue.
2. **Disponibilidad del gestor gráfico de bases de datos (`list_db = True`):** En la barra superior, hacer clic en el avatar de usuario y seleccionar **Cerrar sesión**, en la pantalla de bienvenida hacer clic en el enlace inferior **Gestionar bases de datos** (o acceder directamente a [http://localhost:8069/web/database/manager](http://localhost:8069/web/database/manager)), debes ver el panel administrativo visual con la base de datos `caryvil_dev` y las opciones de **Crear**, **Respaldar (Backup)**, **Duplicar** y **Eliminar**.
3. **Verificación visual de renderizado de assets y modo proxy (Navegador):** En la interfaz web de Odoo, presionar `F12` para abrir las herramientas de desarrollador y seleccionar la pestaña **Consola**, debes observar que la pantalla carga sin advertencias de contenido mixto (*Mixed Content*) ni bloqueos de scripts; en la pestaña **Red (Network)**, forzar una recarga limpia (`Ctrl + F5`) y verificar que todas las hojas de estilo y scripts de Odoo (`web.assets_backend`) respondan con código `200 OK` o `304 Not Modified`.
4. **Inspección del entorno y versión del servidor (UI):** Con el modo desarrollador activo, hacer clic en el avatar del usuario administrador en la esquina superior derecha y seleccionar **Acerca de**, debes ver el cuadro de diálogo modal confirmando la versión **Odoo 17.0 (Community Edition)** y el entorno operativo sobre la base de datos `caryvil_dev`.

#### Casos Límite / Rutas de Excepción:
1. **Persistencia de sesión en navegación protegida:** Navegar entre diferentes aplicaciones y menús del sistema recargando la página con `F5`, debes comprobar que la sesión de usuario y la apariencia gráfica se mantienen estables sin desconexiones inesperadas ni pérdida de estilos por reescritura de cabeceras.

---

### Flujo 1.3: Aprovisionamiento de Infraestructura en Render con Terraform (SPEC-1.2.1)

> **Prerrequisito:** Tener `terraform.tfvars` completado con `render_api_key` y `render_owner_id` válidos.

#### Fase A: Validación local del plan de infraestructura (Escenario 1 del spec)

1. **Inicialización del provider:** En la terminal, navegar a `infra/terraform/` y ejecutar `terraform init`. Debes observar que Terraform descarga el provider `render-oss/render v1.3.x` sin errores, y que se crea el directorio `.terraform/` con los binarios del provider.
2. **Verificación de formato HCL:** Ejecutar `terraform fmt -check`. El comando debe retornar código de salida `0` sin imprimir ningún nombre de archivo (indica que todos los archivos ya están correctamente formateados). Si retorna código `1` con nombres de archivo, ejecutar `terraform fmt` para auto-corregir y repetir la verificación.
3. **Validación de sintaxis y tipos:** Ejecutar `terraform validate`. Debes obtener la respuesta `Success! The configuration is valid.` sin errores de sintaxis, tipos o referencias inexistentes.
4. **Generación del plan de ejecución:** Ejecutar `terraform plan`. Terraform debe mostrar el plan con exactamente **2 recursos a crear** (`render_postgres.caryvil_db` y `render_web_service.caryvil_odoo`) y **0 a modificar** o **destruir**. Verificar que en el plan no aparezca ningún valor sensible expuesto en texto plano en los campos `render_api_key`, `PASSWORD` o `ADMIN_PASSWORD` (deben mostrarse como `(sensitive value)`).

#### Fase B: Aprovisionamiento real en Render (Escenario 2 del spec)

5. **Aplicar el plan:** Ejecutar `terraform apply -auto-approve`. Terraform debe completar el aprovisionamiento en menos de 10 minutos mostrando `Apply complete! Resources: 2 added, 0 changed, 0 destroyed.` al finalizar.
6. **Verificar outputs de infraestructura:** Ejecutar `terraform output odoo_service_url`. Debes obtener una URL HTTPS con el formato `https://caryvil-erp-dev.onrender.com` (o similar). Acceder a esa URL en el navegador; puede tomar entre 30-120 segundos en el primer acceso (*cold start*) y debes llegar a la pantalla de login de Odoo o al gestor de bases de datos.
7. **Comprobación en el Dashboard de Render:** Iniciar sesión en [dashboard.render.com](https://dashboard.render.com) y verificar que aparecen los servicios creados:
   - Base de datos PostgreSQL nombrada `caryvil-postgres-dev` en estado `Available`.
   - Web Service nombrado `caryvil-erp-dev` en estado `Live` con la imagen `ghcr.io/melissafloresa/odoo_erp_farmacia:latest`.
   - Las variables de entorno `HOST`, `PORT`, `USER`, `PASSWORD`, `DB_NAME`, `ADMIN_PASSWORD` y `PROXY_MODE` visibles en la pestaña *Environment* del Web Service (sin exponer los valores, usando *Reveal*).  
8. **Verificación de conectividad HTTP:** Desde la terminal del host, ejecutar `curl -sI <URL_DEL_SERVICIO>` y verificar que el encabezado de respuesta retorna código `200 OK` o `303 See Other`.

#### Fase C: Destrucción limpia de recursos de prueba (Escenario 3 del spec)

9. **Destruir la infraestructura:** Ejecutar `terraform destroy -auto-approve`. Terraform debe mostrar `Destroy complete! Resources: 2 destroyed.` al finalizar.
10. **Confirmar eliminación en Render Dashboard:** Ingresar al Dashboard de Render y verificar que los servicios `caryvil-postgres-dev` y `caryvil-erp-dev` ya no aparecen en la lista de servicios activos, confirmando que no quedaron instancias huérfanas.

#### Casos Límite / Rutas de Excepción:
1. **Cold start del Web Service gratuito:** El Web Service en el plan *Free* de Render se suspende tras 15 minutos de inactividad. Al acceder por primera vez o después de un período de inactividad, el navegador puede demorar 30-50 segundos en recibir la primera respuesta. Este comportamiento es esperado y está documentado en el SPEC-1.2.1 §9 (Risk 1). Esperar la carga completa antes de reportar un error.
2. **Error `No valid credential sources found` en `terraform init`:** Indica que `render_api_key` no está configurada. Verificar que `terraform.tfvars` existe en `infra/terraform/` con el valor correcto de `render_api_key`, o que la variable de entorno `TF_VAR_render_api_key` está configurada en la sesión actual.

---

### Flujo 1.4: Verificación de Variables de Entorno y Bloqueo de Secretos (SPEC-1.2.2)

> **Prerrequisito:** Disponer de una terminal Git y Docker Compose en la raíz del repositorio.

#### Fase A: Inicialización a partir de la plantilla segura (Escenario 1 del spec)

1. **Crear archivo local desde plantilla:**
   ```bash
   cp .env.example .env
   ```
2. **Validar lectura de variables con Docker Compose:**
   ```bash
   docker compose -f infra/compose/docker-compose.yml config
   ```
   *Comprobar que la salida no arroje variables no sustituidas (vacías) y que los puertos expuestos sean 8069 y 8072.*
3. **Comprobar valores de marcadores (*placeholders*):**
   Abrir `.env.example` y verificar visualmente que no figure ninguna contraseña real de producción ni tokens que inicien con `rnd_` real.

#### Fase B: Detección y bloqueo de archivos sensibles en Git (Escenario 2 del spec)

4. **Verificación de bloqueo estricto con `git check-ignore`:**
   Ejecutar en la raíz del repositorio:
   ```bash
   git check-ignore -v .env .env.local .env.prod infra/terraform/terraform.tfvars
   ```
   *El comando debe mostrar que cada archivo coincide con una regla activa de `.gitignore` (ej. `.env`, `.env.*`, `*.tfvars`).*
5. **Intento de seguimiento con `git status`:**
   Crear un archivo temporal de prueba `test.tfvars` y ejecutar `git status`.
   *Verificar que `test.tfvars` NO aparezca bajo "Untracked files". Luego eliminar el archivo de prueba.*
6. **Permitir plantillas públicas:**
   Ejecutar:
   ```bash
   git check-ignore -v .env.example infra/terraform/terraform.tfvars.example
   ```
   *No debe haber salida (código de salida 1), confirmando que las plantillas `.example` son rastreables y forman parte del repositorio.*

#### Fase C: Verificación de variables sensibles en Terraform (Escenario 3 del spec)

7. **Inspección de flags sensibles en Terraform:**
   Revisar `infra/terraform/variables.tf` y verificar que las siguientes variables incluyan `sensitive = true`:
   - `render_api_key`
   - `render_owner_id`
   - `odoo_admin_password`
8. **Validación de logs limpios en Terraform Plan:**
   Ejecutar `terraform plan` en `infra/terraform/` y verificar que las credenciales no se impriman en texto plano en la terminal.

---

### Flujo 1.5: Pipeline CI/CD con GitHub Actions y Despliegue Automático (SPEC-1.3.1)

> **Prerrequisito:** Disponer de acceso al repositorio en GitHub con permisos de visualización de Actions y Pull Requests, así como acceso al dashboard de Render.

#### Fase A: Rechazo de Pull Request con errores de sintaxis (Escenario 1 del spec)

1. **Crear rama temporal con error intencional de sintaxis o formato:**
   ```bash
   git checkout -b test/ci-syntax-error
   ```
2. **Introducir error en un archivo Python o XML de Odoo:**
   - Ejemplo: agregar una línea con error de indentación PEP8 o sintaxis inválida en un archivo de prueba.
3. **Enviar commit y abrir Pull Request hacia `develop` o `main`:**
   ```bash
   git add .
   git commit -m "test: validar bloqueo de CI ante errores de sintaxis"
   git push origin test/ci-syntax-error
   ```
4. **Comprobar fallo en GitHub Actions:**
   - Navegar a la pestaña **Actions** o en la vista del Pull Request en GitHub.
   - Verificar que el workflow `CI Quality & Static Validation Pipeline` se active automáticamente.
   - Comprobar que el job `Lint & Static Code Analysis` finalice en estado **Fallido (rojo)** indicando en los logs el archivo y la línea exacta del error (Flake8, Black, Yamllint o XML).
   - Verificar que el merge del Pull Request quede bloqueado por el fallo del check.
5. **Limpieza:** Cerrar el Pull Request de prueba y eliminar la rama temporal.

#### Fase B: Validación exitosa de Pull Request conforme (Escenario 2 del spec)

6. **Crear rama de funcionalidad con código conforme:**
   ```bash
   git checkout -b test/ci-success-validation
   ```
7. **Verificar calidad localmente antes del push:**
   ```bash
   flake8 --config=.flake8 tests/
   pytest tests/test_spec_1_3_1_ci_cd.py -v
   ```
8. **Enviar Pull Request hacia `develop` o `main`:**
   ```bash
   git push origin test/ci-success-validation
   ```
9. **Confirmar ejecución exitosa en GitHub Actions:**
   - Observar en GitHub Actions que se ejecutan secuencialmente los jobs:
     1. `Lint & Static Code Analysis` (Flake8, Black, Yamllint, Terraform, XML).
     2. `Docker Build & Dependency Verification` (compilación con caché `type=gha`).
   - Verificar que todos los checks finalicen en estado **Aprobado (verde)** en un tiempo total inferior a 5 minutos.
10. **Limpieza:** Eliminar la rama de prueba o proceder con el merge.

#### Fase C: Despliegue automático a Render y Health Check tras merge en main (Escenario 3 del spec)

11. **Integrar cambios a la rama principal (`main`):**
    - Realizar merge del Pull Request aprobado hacia `main` (o ejecutar `workflow_dispatch` manual en Actions).
12. **Monitorear el workflow `CD Deployment Pipeline - Render`:**
    - Verificar que el job `Build & Publish Docker Image (GHCR)` construya y publique la imagen en `ghcr.io` con tags `:latest` y `:<commit_sha>`.
    - Verificar que el job `Trigger Render Deployment Webhook` invoque el `RENDER_DEPLOY_HOOK_URL` retornando código `HTTP 200` o `201`.
    - Verificar que el job `Verify Public Endpoint Health Check` realice el sondeo de disponibilidad y confirme que el servicio responda con `HTTP 200` o `303`.
13. **Comprobar despliegue en Render Dashboard:**
    - Iniciar sesión en [dashboard.render.com](https://dashboard.render.com).
    - Verificar en la pestaña *Events* y *Logs* del Web Service que se haya iniciado y completado un nuevo despliegue con la última imagen generada.

---

### Flujo 2.1: Definición de Roles, Grupos de Seguridad y Herencia de Privilegios (SPEC-2.2.1)

1. **Inspección de la Categoría y Grupos en el Gestor de Usuarios (UI):** Iniciar sesión con la cuenta de Administrador General (`admin` / `admin` o `admin_caryvil@caryvil.com` / `admin123`), activar el modo desarrollador (`?debug=1`), navegar a **Ajustes** -> **Usuarios y Compañías** -> **Grupos** (o filtrar por aplicación), buscar `Farmacia Caryvil`, debes ver la categoría de módulo `Farmacia Caryvil` (secuencia 10) conteniendo exactamente los tres roles definidos:
   - `Cajero / Dependiente de Mostrador` (`group_caryvil_cashier`)
   - `Encargado de Compras e Inventario` (`group_caryvil_inventory_purchases`)
   - `Administrador / Propietario` (`group_caryvil_manager`)
2. **Verificación del Rol Cajero / Dependiente de Mostrador (Escenario 1):** Cerrar sesión e ingresar con las credenciales del cajero (`cajero@caryvil.com` / `cajero123`):
   - Acceder al menú principal **Farmacia Caryvil**: verificar que los menús disponibles son **Ventas y Caja**, **Medicamentos e Inventario** (solo consulta y venta) y **Clientes**.
   - Comprobar que los menús **Compras y Proveedores**, **Configuración** y el **Dashboard** gerencial se encuentran totalmente ocultos e inaccesibles.
   - Navegar a **Farmacia Caryvil** -> **Clientes**, presionar **Nuevo**, registrar un cliente de prueba con DUI y teléfono, debes comprobar que el guardado es exitoso (`perm_create = 1`, `perm_write = 1`), pero no se dispone de permisos para eliminar registros históricos de clientes.
3. **Protección de Confidencialidad de Costos ante el Rol Cajero:** Con la sesión de cajero activa, abrir el catálogo de medicamentos y acceder a la ficha técnica de cualquier producto:
   - Verificar que no se visualizan los costos de compra a laboratorios, precios de adquisición de proveedores ni los márgenes de ganancia.
4. **Verificación del Rol Encargado de Compras e Inventario (Escenario 2):** Cerrar sesión e ingresar con las credenciales de compras e inventario (`compras@caryvil.com` / `compras123`):
   - Acceder a **Farmacia Caryvil**: debes observar habilitados los menús **Compras y Proveedores**, **Medicamentos e Inventario** y **Clientes**, así como la herencia operativa del rol de mostrador/cajero.
   - Navegar a **Compras y Proveedores** -> **Órdenes de Compra**, hacer clic en **Nuevo** y verificar la visibilidad de los campos de costos, descuentos comerciales y precios de proveedor.
   - Acceder al albarán de recepción de mercadería y validar la captura de lotes y fechas de vencimiento.
   - Verificar que no se tiene acceso al menú **Configuración** de la empresa ni a la eliminación o administración de cuentas de usuario en el ERP.
5. **Verificación de Control Total del Rol Administrador / Propietaria (Escenario 3):** Cerrar sesión e iniciar sesión como Administrador General / Propietaria (`admin` / `admin` o `admin_caryvil@caryvil.com` / `admin123`):
   - Verificar acceso integral irrestricto a todos los módulos: **Dashboard**, **Ventas y Caja**, **Medicamentos e Inventario**, **Compras y Proveedores**, **Clientes** y **Configuración**.
   - Acceder a **Ajustes** -> **Usuarios y Compañías** -> **Usuarios**, abrir cualquier usuario y comprobar que la sección de permisos muestra el campo desplegable/selección para la categoría *Farmacia Caryvil* permitiendo promover o reasignar cualquiera de los 3 niveles funcionales.

#### Casos Límite / Rutas de Excepción:
1. **Comprobación de Herencia Transitiva en Cascada (*Implied Groups*):** En el formulario de edición de usuarios de Odoo (**Ajustes** -> **Usuarios y Compañías** -> **Usuarios**), crear un usuario temporal y asignarle el rol `Administrador / Propietario`. Al inspeccionar los grupos técnicos asignados, verificar que el usuario hereda automáticamente los grupos `group_caryvil_inventory_purchases`, `group_caryvil_cashier`, `stock.group_stock_manager`, `purchase.group_purchase_manager` y `sales_team.group_sale_manager` sin requerir marcación manual individual.
2. **Bloqueo de Acceso Directo por URL a Vistas Restringidas:** Con la sesión iniciada como `cajero@caryvil.com`, intentar ingresar manualmente por URL a una acción de compras o configuración (ej. `http://localhost:8069/web#action=purchase.purchase_rfq`), debes ver que Odoo bloquea la carga de la vista y muestra una advertencia de permisos denegados (*AccessError*).

---

### Flujo 6.1: Directorio y Gestión de Proveedores Farmacéuticos (SPEC-6.1.1)

1. **Acceso al Catálogo de Proveedores:** Iniciar sesión con la cuenta de Encargado de Compras e Inventario (`compras@caryvil.com` / `compras123`) o Administrador General (`admin` / `admin`), acceder al menú principal **Farmacia Caryvil**, hacer clic en el submenú **Compras y Proveedores** y seleccionar **Proveedores y Laboratorios**, debes ver la vista de lista con las columnas *Código*, *Nombre*, *Proveedor* y *Teléfono*, junto con el botón **Nuevo** en la barra superior.
2. **Creación de Vendedor y Alta Rápida de Empresa Proveedora:** Hacer clic en el botón **Nuevo**, debes observar el formulario del Vendedor con el campo *Código* en modo solo lectura. En el campo *Nombre*, ingresar `Carlos Méndez`, en el campo *Proveedor*, desplegar la lista y hacer clic en la opción **Crear y editar...**, debes ver abrirse una ventana emergente modal con el formulario simplificado *Proveedor / Empresa* que contiene exclusivamente los campos *Nombre del Proveedor*, *Tipo de Proveedor*, *NIT* y *NRC*.
3. **Ingreso de Datos Fiscales con Máscaras en Tiempo Real:** En la ventana emergente de la Empresa, escribir en *Nombre del Proveedor* `Laboratorios Vijosa S.A. de C.V.`, seleccionar en *Tipo de Proveedor* la opción `Laboratorio`, en el campo *NIT* tipear los números `06141234560012` y comprobar que la máscara de entrada formatea automáticamente el texto en vivo como `0614-123456-001-2`, en el campo *NRC* ingresar `12345-6`, y presionar el botón **Guardar y cerrar**, debes ver que el modal se cierra y el campo *Proveedor* del formulario principal se completa con `Laboratorios Vijosa S.A. de C.V.`.
4. **Completar Datos del Vendedor y Guardar:** En el formulario principal del Vendedor, tipear en el campo *Teléfono* los dígitos `77889900` y verificar que la máscara formatea dinámicamente el valor a `7788-9900`, ingresar en *Email* `carlos.mendez@vijosa.com` y hacer clic en el botón **Guardar** (o icono de nube), debes observar que el registro se almacena exitosamente y el campo *Código* muestra un código correlativo autogenerado con formato `P0001` (o correlativo siguiente).
5. **Asociación de Múltiples Vendedores a una Misma Empresa:** Regresar a la lista de **Proveedores y Laboratorios** mediante las migas de pan y presionar **Nuevo**. Escribir en *Nombre* `Ana López`, en el desplegable *Proveedor* seleccionar la empresa previamente creada `Laboratorios Vijosa S.A. de C.V.`, en *Teléfono* tipear `71234567` (se formatea como `7123-4567`), ingresar en *Email* `ana.lopez@vijosa.com` y hacer clic en **Guardar**, debes comprobar que Ana López recibe su propio código correlativo único (ej. `P0002`) y queda vinculada al mismo laboratorio.
6. **Verificación de Lista Unificada y Filtros por Tipo de Proveedor:** Regresar a la vista de lista de **Proveedores y Laboratorios**, debes ver a ambos vendedores (`Carlos Méndez` y `Ana López`) listados en registros independientes con sus respectivos códigos y teléfonos, compartiendo `Laboratorios Vijosa S.A. de C.V.` en la columna *Proveedor*. En la barra de búsqueda superior, hacer clic en el filtro rápido **Laboratorios**, debes comprobar que la lista mantiene a los vendedores cuyo proveedor es de tipo Laboratorio y oculta aquellos clasificados como Distribuidora o Droguería.
7. **Edición Modal de Laboratorio desde la Ficha del Vendedor:** En la lista de vendedores, hacer clic sobre `Carlos Méndez` para abrir su formulario y presionar el botón de enlace interno (ícono `->` / botón abrir registro) junto al campo *Proveedor*, debes ver que la Empresa se abre en una ventana modal emergente utilizando el formulario simplificado (`view_res_partner_laboratorio_quick_form`) sin recargar la pantalla completa ni mostrar campos genéricos de contactos de Odoo. Realizar una modificación menor (ej. cambiar nombre a `Laboratorios Vijosa S.A.`) y hacer clic en **Guardar**, debes comprobar que el cambio se sincroniza inmediatamente en la ficha del vendedor.
8. **Trazabilidad de Historial de Compras en la Ficha del Vendedor:** En la ficha del vendedor `Carlos Méndez`, desplazarse hasta la pestaña inferior **Historial de Compras**, debes observar la tabla con las órdenes de compra asociadas directamente a este vendedor mostrando las columnas *Código*, *Fecha*, *Monto Total* y *Estado*, permitiendo consultar el historial comercial directo sin cambiar de menú.

#### Casos Límite / Rutas de Excepción:
1. **Rechazo por Omisión de NRC Obligatorio en Empresa:** Presionar **Nuevo** para registrar un nuevo contacto, en *Proveedor* seleccionar **Crear y editar...**, ingresar en *Nombre del Proveedor* `Distribuidora Sin NRC`, seleccionar tipo `Distribuidora`, dejar el campo *NRC* en blanco y presionar **Guardar y cerrar**, debes ver una notificación modal de error de validación bloqueante con el mensaje `El NRC de "Distribuidora Sin NRC" es obligatorio.` impidiendo el guardado hasta ingresar el valor.
2. **Rechazo por Formato Inválido de NIT:** En la ventana emergente de la Empresa, escribir en el campo *NIT* un valor incompleto como `0614-123` y hacer clic en **Guardar y cerrar**, debes ver la notificación de validación `El NIT de "Distribuidora Sin NRC" debe tener el formato 0000-000000-000-0.` bloqueando el registro.
3. **Rechazo por Formato Inválido de Teléfono en Vendedor:** En el formulario del Vendedor, ingresar en el campo *Teléfono* una secuencia no conforme con el formato salvadoreño (ej. `12345`) y presionar **Guardar**, debes observar la alerta de validación `El teléfono de "..." debe tener el formato 0000-0000.` impidiendo el guardado.
4. **Independencia de Validaciones frente a Clientes y Contactos Generales:** Iniciar sesión con el usuario de Cajero (`cajero@caryvil.com`), navegar a **Farmacia Caryvil** -> **Clientes**, hacer clic en **Nuevo** y crear un cliente con un teléfono de formato libre (ej. número telefónico fijo o internacional), debes verificar que el cliente se almacena normalmente sin verse afectado por las restricciones estrictas de proveedores farmacéuticos.
5. **Bloqueo de Proveedor no Farmacéutico en Órdenes de Compra:** Iniciar sesión como Encargado de Compras (`compras@caryvil.com`), navegar a **Farmacia Caryvil** -> **Compras y Proveedores** -> **Órdenes de Compra**, hacer clic en **Nuevo**, en el campo *Nombre Vendedor* seleccionar un contacto que no esté catalogado como proveedor farmacéutico ni dependiente de una empresa farmacéutica (ej. un contacto genérico de oficina) e intentar guardar o confirmar la orden, debes observar la alerta modal de validación bloqueante `El proveedor "..." no está catalogado como proveedor farmacéutico.` impidiendo emitir órdenes de compra a terceros no autorizados.

---

### Flujo 6.2: Catálogo de Precios y Condiciones de Proveedores (SPEC-6.2.1)

1. **Acceso a la Ficha del Medicamento desde Compras:** Iniciar sesión con el usuario de Encargado de Compras e Inventario (`compras@caryvil.com` / `compras123`), acceder al menú principal **Farmacia Caryvil** -> **Inventario y Medicamentos** -> **Medicamentos** (o catálogo de productos) y seleccionar un producto de prueba (ej. `Amoxicilina 500mg (Caja x 50)`), debes observar el formulario del medicamento con la pestaña **Compras** visible.
2. **Registro de Laboratorio con Precio Bruto y Descuento (CA-1):** En la pestaña **Compras**, hacer clic en **Agregar una línea** dentro de la tabla de proveedores:
   - Seleccionar en *Proveedor* a `Laboratorios Vijosa S.A. de C.V.`.
   - Ingresar en *Código Proveedor* `VIJ-AMX-500`.
   - En *Presentación Proveedor*, escribir `Caja con 50 tabletas`.
   - En *Cantidad Mínima*, dejar `1.0`.
   - En *Plazo de entrega*, ingresar `2` días.
   - En *Precio Bruto*, ingresar `5.00`.
   - En *% Desc.*, ingresar `10.0`.
   - Debes comprobar que el campo **Precio Neto** se recalcula automáticamente a `$4.50`. Presionar **Guardar**.
3. **Registro de Segundo Proveedor para Comparativa de Costos (CA-1):** En la misma tabla, agregar una segunda línea con *Proveedor* `Droguería Santa Lucía`, *Presentación Proveedor* `Caja x 50 cápsulas`, *Plazo de entrega* `1` día, *Precio Bruto* `4.80` y *% Desc.* `0.0` (Precio Neto `$4.80`). Guardar el producto, debes ver ambas opciones registradas permitiendo al comprador comparar costos y tiempos de entrega.
4. **Configuración de Escala por Volumen (CA-3):** Agregar una tercera línea seleccionando a `Laboratorios Vijosa S.A. de C.V.` con *Cantidad Mínima* `10.0`, *Precio Bruto* `5.00` y *% Desc.* `16.0` (Precio Neto `$4.20`). Guardar.
5. **Autocompletado de Precios y Escalas en Orden de Compra (CA-2 y CA-3):** Navegar a **Farmacia Caryvil** -> **Compras y Proveedores** -> **Órdenes de Compra**, presionar **Nuevo**, seleccionar como proveedor un contacto asociado a `Laboratorios Vijosa S.A. de C.V.` y en la tabla de productos agregar `Amoxicilina 500mg`:
   - Con cantidad `5`, verificar que el precio unitario se autocompleta en `$4.50`.
   - Cambiar la cantidad a `12`, verificar que el precio unitario se actualiza automáticamente a `$4.20` por la escala de volumen.
6. **Protección de Confidencialidad de Precios ante Rol Cajero:** Cerrar sesión e ingresar como `cajero@caryvil.com` / `cajero123`. Abrir el catálogo de medicamentos y revisar la pestaña de compras, debes verificar que las columnas `Precio Bruto`, `% Desc.`, `Presentación Proveedor` y `Precio Neto` se encuentran totalmente ocultas.

#### Casos Límite / Rutas de Excepción:
1. **Modificación Sucesiva de Descuentos (No Acumulativo):** Con el usuario de compras, en una línea con Precio Bruto `$10.00`, ingresar `% Desc.` `10.0` (calcula `$9.00`). Luego cambiar a `20.0` (debe calcular `$8.00`, no `$7.20`) y finalmente a `0.0` (debe retornar a `$10.00`).
2. **Validación de Rango de Descuento Comercial:** Ingresar valores como `150.0` o `-10.0`, el sistema acota el descuento entre `0.0` y `100.0%` sin generar precios negativos.

---

### Flujo 8.1: Visibilidad de Abonos y Estado de Pago a Proveedores (SPEC-8.1.2)

1. **Consulta de Estado Inicial en Orden de Compra Confirmada:** Iniciar sesión con la cuenta de Encargado de Compras e Inventario (`compras@caryvil.com` / `compras123`), acceder a **Farmacia Caryvil** -> **Compras y Proveedores** -> **Órdenes de Compra**, hacer clic en **Nuevo**, seleccionar en *Nombre Vendedor* a `Carlos Méndez` (se autocompleta el campo *Proveedor* con `Laboratorios Vijosa`), en la tabla de productos agregar una línea con `Amoxicilina 500mg`, *Cantidad* `10` y *Precio Unitario* `50.00`. Verificar que el resumen en vivo calcula *Subtotal* `$500.00`, *IVA (13%)* `$65.00` y *Total* `$565.00`. Hacer clic en **Confirmar Pedido**, debes observar que la orden adopta un código correlativo (ej. `PE0001`), el campo *Estado de Factura* muestra la insignia gris `Sin Facturar` y en la pestaña **Abonos** se visualiza *Total Abonado: $0.00*, *Saldo Pendiente: $565.00* y *Estado de Abonos: Pendiente* con insignia roja.
2. **Recepción Física de Mercadería (Prerrequisito de Control de Facturación):** En el flujo operativo a crédito de Farmacia Caryvil, el laboratorio entrega primero el pedido y se registra su ingreso en bodega: en el encabezado de la orden de compra confirmada, hacer clic en el botón inteligente **Recepción** (ícono de camión con contador `1`), en el albarán de entrada (`WH/IN/...`) ingresar la cantidad recibida (y lote si aplica) y hacer clic en **Validar**, debes comprobar que el albarán pasa a estado verde **Hecho** (`done`). Regresar a la orden de compra mediante las migas de pan **PE0001**.
3. **Registro de Primer Abono Parcial en Compras:** En el formulario de la orden, acceder a la pestaña **Abonos**, hacer clic en **Agregar una línea** dentro de la tabla de abonos, seleccionar la fecha de hoy, en el campo *Monto Abonado* ingresar `200.00`, en *Nota* escribir `Primer abono - transferencia bancaria lote 1` y hacer clic fuera de la fila o en el icono de guardar, debes ver que inmediatamente *Total Abonado* se actualiza a `$200.00`, *Saldo Pendiente* se reduce a `$365.00` y la insignia de *Estado de Abonos* cambia a color amarillo con la etiqueta `Abono Parcial`.
4. **Comprobación de Visibilidad en Vista de Lista:** Regresar a la lista de órdenes mediante las migas de pan **Órdenes de Compra**, debes observar en la fila de la orden `PE0001` que la columna *Saldo Pendiente* refleja `$365.00` y la columna *Estado de Pago* muestra la insignia amarilla `Abono Parcial`, permitiendo monitorear la deuda activa sin ingresar al módulo contable.
5. **Registro de Segundo Abono y Liquidación del Saldo:** Hacer clic sobre la orden `PE0001`, ingresar a la pestaña **Abonos**, presionar **Agregar una línea**, ingresar la fecha de hoy, en *Monto Abonado* digitar `365.00` y en *Nota* escribir `Segundo abono - liquidación final`. Al guardar la línea, debes comprobar que *Total Abonado* alcanza `$565.00`, *Saldo Pendiente* pasa a `$0.00`, el badge *Estado de Abonos* cambia a verde con la leyenda `Completo`, y en la barra superior de acciones aparece habilitado y destacado el botón morado **Generar Factura Final** (mientras que el botón estándar "Crear Factura" se mantiene oculto para evitar desvíos contables).
6. **Generación Automatizada de Factura Final y Reconciliación en un Clic:** Hacer clic en el botón **Generar Factura Final**, dado que la mercadería ya fue recibida y la deuda está saldada al 100%, Odoo procesa la factura de proveedor (`account.move`) y su pago de forma atómica (si requiere fecha de emisión del proveedor, se abre el formulario para digitarla y confirmar). Debes observar que en el encabezado de la orden de compra aparece el botón estadístico **Pagos** mostrando el contador `1`, el campo *Estado de Factura* cambia a la insignia verde `Pagado` y el saldo residual en factura marca `$0.00`.
7. **Inspección del Historial de Pagos Reconciliados:** Hacer clic en el botón estadístico **Pagos** en el encabezado de la orden, debes ver abrirse la vista con el registro formal de pago (`account.payment`) por `$565.00` debidamente cruzado con la factura de proveedor, garantizando la trazabilidad contable sin haber requerido registrar facturas parciales intermedias.

#### Casos Límite / Rutas de Excepción:
1. **Bloqueo Preventivo por Mercadería No Recibida:** En una orden de compra confirmada donde se hayan completado los abonos al 100% pero no se haya validado el albarán de recepción en bodega (cantidad recibida en 0), hacer clic en **Generar Factura Final**, debes observar la notificación de validación bloqueante `No se puede generar la Factura Final porque la mercadería aún no ha sido recibida en inventario. Valide primero el albarán de entrada mediante el botón inteligente 'Recepción' antes de facturar.` impidiendo pagar o facturar por productos no recibidos.
2. **Bloqueo de Generación de Factura Final con Saldo Pendiente:** En una orden de compra con saldo remanente (ej. donde solo se han abonado `$200.00` de `$565.00`), intentar forzar la acción de facturación final: el sistema arroja la alerta bloqueante de validación `Aún falta abonar $365.00 para poder generar la factura final.` impidiendo el cierre fiscal hasta que la deuda esté 100% saldada en compras.
3. **Reconocimiento Dinámico de Pagos Parciales en Contabilidad Nativa:** En una orden donde el contador decida registrar pagos parciales directamente sobre la factura de proveedor nativa (`account.move`), comprobar que el campo computado `amount_residual_total` y la insignia `payment_status_label` de la orden de compra reflejan exactamente el mismo saldo pendiente de la factura contable en tiempo real.

---

### Flujo 8.2: Recepción de Mercadería y Captura Obligatoria de Lotes (SPEC-8.2.1)

1. **Acceso al Albarán de Recepción de Mercadería:** Iniciar sesión con el usuario de Encargado de Compras e Inventario (`compras@caryvil.com` / `compras123`), navegar a **Farmacia Caryvil** -> **Compras y Proveedores** -> **Órdenes de Compra**, hacer clic en **Nuevo**, seleccionar proveedor `Carlos Méndez`, agregar una línea con el medicamento `Ibuprofeno 400mg` con *Cantidad* `15.00` y hacer clic en **Confirmar Pedido**. En la esquina superior derecha del formulario de la orden, hacer clic en el botón inteligente **Recepción** (ícono de camión con contador `1`), debes ver abrirse el albarán de entrada entrante (`WH/IN/...`) en estado `Listo`.
2. **Apertura de Operaciones Detalladas para Captura de Lote y Vencimiento:** En el albarán de entrada, ubicarse en la pestaña **Operaciones** y presionar el botón de **Operaciones Detalladas** (icono de lista con viñetas situado en el extremo derecho de la línea del producto), debes ver desplegarse la tabla emergente con las columnas en español: *Código de Lote*, *Fecha de Vencimiento* y *Stock Ingresado*.
3. **Captura Exitosa de Lote y Fecha de Vencimiento Válida (CA-1):** En la columna *Código de Lote*, escribir `LOT-IBU-2027-01`, en la columna *Fecha de Vencimiento* ingresar una fecha futura válida (ej. `31/12/2027 00:00:00`), y en *Stock Ingresado* digitar `15.00`. Cerrar el panel o hacer clic en **Guardar**, y en la barra superior del albarán presionar el botón **Validar**, debes comprobar que el albarán de recepción transiciona exitosamente al estado verde **Hecho** (`done`) y genera el registro formal del lote en el inventario con su respectiva caducidad.
4. **Recepción Desglosada en Múltiples Lotes Distintos (CA-3):** Crear y confirmar una orden de compra por `20.00` unidades de `Ibuprofeno 400mg`, acceder a su albarán de recepción y abrir la tabla de **Operaciones Detalladas**:
   - En la primera fila, ingresar en *Código de Lote* `LOT-A-2026`, en *Fecha de Vencimiento* `31/10/2026 00:00:00` y en *Stock Ingresado* `10.00`.
   - Hacer clic en **Agregar una línea**, en *Código de Lote* escribir `LOT-B-2027`, en *Fecha de Vencimiento* `31/05/2027 00:00:00` y en *Stock Ingresado* `10.00`.
   - Cerrar el panel y presionar **Validar**, debes verificar que el albarán concluye en estado **Hecho**, creando ambos lotes en el inventario farmacéutico de forma totalmente independiente con sus respectivas existencias y fechas.

#### Casos Límite / Rutas de Excepción:
1. **Bloqueo Estricto por Omisión de Lote (CA-2):** En una recepción entrante de medicamento con seguimiento activo, ingresar en la línea de operaciones la cantidad física recibida (`15.00`) pero dejar el campo *Código de Lote* vacío, y presionar **Validar**, debes ver una notificación modal de error de validación bloqueante con el mensaje `Debe asignar el Número de Lote para el medicamento Ibuprofeno 400mg en la recepción.` impidiendo el ingreso físico sin trazabilidad.
2. **Bloqueo Estricto por Omisión de Fecha de Vencimiento:** En la tabla de operaciones detalladas, escribir un código de lote válido (ej. `LOT-TEMP-01`) pero dejar el campo *Fecha de Vencimiento* en blanco, y hacer clic en **Validar**, debes observar la alerta de validación bloqueante `Debe especificar la Fecha de Vencimiento para el lote LOT-TEMP-01 del producto Ibuprofeno 400mg.` deteniendo el albarán.
3. **Bloqueo de Mercadería Vencida (Fecha Anterior a Hoy):** En el campo *Fecha de Vencimiento*, seleccionar deliberadamente una fecha pasada (ej. `01/01/2020`), y hacer clic en **Validar**, debes comprobar que el sistema rechaza rotundamente la recepción mediante la advertencia `La fecha de vencimiento (...) del lote LOT-... ya está caducada. No se puede recibir mercadería vencida.` evitando el ingreso de producto deteriorado a la farmacia.

---

### Flujo 8.3: Actualización Automática de Stock y Cierre de Compras (SPEC-8.2.2)

1. **Inspección Previa de Saldo de Inventario en Bodega:** Iniciar sesión con la cuenta de Encargado de Compras e Inventario (`compras@caryvil.com` / `compras123`), acceder al menú principal **Farmacia Caryvil** -> **Inventario y Medicamentos** -> **Medicamentos**, buscar en el catálogo `Loratadina 10mg` y abrir su ficha técnica, debes verificar y anotar el valor inicial mostrado en el campo *A mano* (ej. `5.00 Unidades`).
2. **Emisión de Orden de Compra y Recepción Total:** Navegar a **Compras y Proveedores** -> **Órdenes de Compra**, hacer clic en **Nuevo**, seleccionar proveedor `Carlos Méndez`, agregar una línea con `Loratadina 10mg` con *Cantidad* `20.00` y hacer clic en **Confirmar Pedido**. Acceder al albarán mediante el botón inteligente **Recepción**, en operaciones detalladas capturar el lote `LOT-LOR-2027` con vencimiento `31/08/2027`, cantidad `20.00` y presionar el botón **Validar**, debes observar que el albarán se cierra en estado **Hecho**.
3. **Verificación de Incremento Inmediato de Existencias (CA-1):** Regresar de inmediato a **Inventario y Medicamentos** -> **Medicamentos** y abrir `Loratadina 10mg`, debes comprobar que el campo *A mano* refleja exactamente `25.00 Unidades` (incremento instantáneo de 20 unidades). En la parte superior de la ficha, hacer clic en el botón inteligente **Lotes / Nros de serie**, debes ver el registro del lote `LOT-LOR-2027` con un saldo a mano de exactamente `20.00 Unidades`.
4. **Comprobación de Disponibilidad Inmediata para Venta en Mostrador (CA-2):** Cerrar sesión e ingresar con la cuenta de Cajero (`cajero@caryvil.com` / `cajero123`). Acceder al catálogo o terminal de mostrador y buscar `Loratadina 10mg`, debes verificar que el medicamento y su nuevo lote `LOT-LOR-2027` aparecen inmediatamente disponibles para despacho y venta al público sin demoras de sincronización.
5. **Cierre y Bloqueo Automático de la Orden de Compra (CA-3):** Iniciar sesión nuevamente como Encargado de Compras (`compras@caryvil.com`), acceder a **Compras y Proveedores** -> **Órdenes de Compra** y abrir la orden recién procesada, debes observar en la tabla de productos que la columna *Cantidad Recibida* (`qty_received`) se actualizó automáticamente a `20.00`, y en la barra superior el estado de la orden pasó de forma automática a **Bloqueada** (`done`) mostrando en la vista de lista la insignia verde `Recibido`.

#### Casos Límite / Rutas de Excepción:
1. **Permanencia en Estado Pendiente ante Recepción Parcial:** En una orden de compra por `50.00` unidades donde el albarán de entrega solo recibe físicamente `20.00` unidades, verificar que en la orden de compra la columna *Cantidad Recibida* marca `20.00`, pero el estado de la orden permanece en **Pedido de Compra** (`purchase`) con la insignia amarilla `Pendiente`, evitando el bloqueo prematuro hasta que se reciba el 100% de la mercadería.

---

### Flujo 8.4: Control de Discrepancias, Daños y Backorders en Recepción (SPEC-8.2.3)

1. **Recepción con Entrega Parcial y Generación de Backorder (CA-1):** Iniciar sesión con la cuenta de Encargado de Compras e Inventario (`compras@caryvil.com` / `compras123`), navegar a **Farmacia Caryvil** -> **Compras y Proveedores** -> **Órdenes de Compra**, hacer clic en **Nuevo**, seleccionar proveedor `Carlos Méndez`, añadir `Amoxicilina 500mg` con *Cantidad* `30.00` y hacer clic en **Confirmar Pedido**. Abrir el albarán de entrada mediante el botón inteligente **Recepción**, en operaciones detalladas ingresar lote `LOT-AMX-PARC`, fecha futura y en *Stock Ingresado* digitar únicamente `20.00` (el proveedor entregó 20 de las 30 cajas solicitadas). Presionar el botón **Validar**, debes ver emerger la ventana modal interactiva **¿Crear Entrega Parcial?** (`stock.backorder.confirmation`).
2. **Confirmación del Albarán Pendiente (Backorder):** En la ventana emergente, hacer clic en el botón **Crear entrega parcial**, debes verificar que el albarán actual se valida en estado **Hecho** por las 20 unidades ingresadas, y al regresar a la orden de compra mediante las migas de pan, el botón inteligente **Recepción** muestra el número `2`. Hacer clic en el botón inteligente, debes ver dos albaranes listados: el primero en estado `Hecho` (20 unidades) y un segundo albarán pendiente en estado `Listo` (*assigned*) por las `10.00` unidades restantes a la espera de la segunda entrega del laboratorio.
3. **Recepción con Cancelación de Remanente por Producto Agotado (CA-2):** Crear y confirmar una orden de compra por `15.00` unidades de `Ibuprofeno 400mg` donde el distribuidor entrega 10 cajas y notifica que las 5 restantes están descontinuadas. Abrir el albarán, ingresar lote para `10.00` unidades y presionar **Validar**. En el modal emergente, hacer clic en **No crear entrega parcial**, debes observar que el albarán se valida en estado **Hecho**, no se genera ningún albarán secundario en espera, la orden de compra actualiza su cantidad recibida a 10 unidades, y en el albarán se activa la pestaña **Discrepancias** mostrando la alerta amarilla `Esta recepción presenta discrepancia: la cantidad recibida es menor a la cantidad ordenada.`
4. **Registro de Incidencias por Producto Dañado y Notificación en Chatter (CA-3):** En una recepción entrante de 20 frascos donde 5 frascos llegaron quebrados en la caja de transporte:
   - En operaciones detalladas ingresar lote y digitar únicamente `15.00` en *Stock Ingresado* (rechazando los 5 frascos rotos al repartidor).
   - En el formulario del albarán, hacer clic en la pestaña **Discrepancias** y en el campo de texto *Detalle de Discrepancia / Daños* escribir: `5 frascos rotos por estiba inadecuada en transporte rechazados formalmente al repartidor de la droguería.`
   - Presionar **Validar** y seleccionar **No crear entrega parcial**.
   - Debes comprobar que el inventario solo recibe las 15 unidades aptas (los 5 frascos rotos nunca ingresan a stock vendible), y en el panel lateral del **Chatter** se publica automáticamente una nota de auditoría del sistema alertando: `Discrepancia detectada en la recepción WH/IN/...: la cantidad recibida es menor a la ordenada. 5 frascos rotos por estiba inadecuada...` quedando registrado para el ajuste de la factura con el proveedor.

#### Casos Límite / Rutas de Excepción:
1. **Ausencia de Falsos Positivos en Recepción Conforme:** En una recepción donde se recibe físicamente la totalidad de las unidades solicitadas (ej. demanda 15 = recibido 15), verificar que el campo `has_discrepancy` permanece en falso, el banner amarillo de advertencia en la pestaña *Discrepancias* se mantiene oculto y no se emite ninguna notificación en el chatter.
2. **Trazabilidad y Filtro de Entregas Pendientes:** Navegar a **Inventario** -> **Operaciones** -> **Albaranes**, hacer clic en la barra de búsqueda y seleccionar el filtro predeterminado **Entregas Pendientes / Retrasadas**, debes verificar que todos los backorders generados aparecen agrupados y visibles para el seguimiento periódico con los laboratorios.


