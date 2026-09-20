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
  - [Flujo 6.1: Directorio y Gestión de Proveedores Farmacéuticos (SPEC-6.1.1)](#flujo-61-directorio-y-gestión-de-proveedores-farmacéuticos-spec-611)

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

#### Matriz de Usuarios y Roles de Prueba:

| Rol de Usuario | Login / Correo | Contraseña | Alcance Operativo |
|---|---|---|---|
| **Administrador General** | `admin` | `admin` | Control total, instalación de addons y ajustes globales |
| **Cajero / Mostrador** | `cajero@caryvil.com` | `cajero123` | Búsqueda rápida de clientes, venta en mostrador y facturación |
| **Farmacéutico / Dispensador** | `farmaceutico@caryvil.com` | `farma123` | Consulta de existencias, dispensación FEFO y mermas |
| **Encargado de Compras/Bodega** | `compras@caryvil.com` | `compras123` | Solicitudes de cotización, órdenes de compra y recepción de lotes |

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

### Flujo 6.1: Directorio y Gestión de Proveedores Farmacéuticos (SPEC-6.1.1)

1. **Acceso al Catálogo de Proveedores:** Iniciar sesión con la cuenta de Encargado de Compras e Inventario (`compras@caryvil.com` / `compras123`) o Administrador General (`admin` / `admin`), acceder al menú principal **Farmacia Caryvil**, hacer clic en el submenú **Compras y Proveedores** y seleccionar **Proveedores y Laboratorios**, debes ver la vista de lista con las columnas *Código*, *Nombre*, *Proveedor* y *Teléfono*, junto con el botón **Nuevo** en la barra superior.
2. **Creación de Vendedor y Alta Rápida de Empresa Proveedora:** Hacer clic en el botón **Nuevo**, debes observar el formulario del Vendedor con el campo *Código* en modo solo lectura. En el campo *Nombre*, ingresar `Carlos Méndez`, en el campo *Proveedor*, desplegar la lista y hacer clic en la opción **Crear y editar...**, debes ver abrirse una ventana emergente modal con el formulario simplificado *Proveedor / Empresa* que contiene exclusivamente los campos *Nombre del Proveedor*, *Tipo de Proveedor*, *NIT* y *NRC*.
3. **Ingreso de Datos Fiscales con Máscaras en Tiempo Real:** En la ventana emergente de la Empresa, escribir en *Nombre del Proveedor* `Laboratorios Vijosa S.A. de C.V.`, seleccionar en *Tipo de Proveedor* la opción `Laboratorio`, en el campo *NIT* tipear los números `06141234560012` y comprobar que la máscara de entrada formatea automáticamente el texto en vivo como `0614-123456-001-2`, en el campo *NRC* ingresar `12345-6`, y presionar el botón **Guardar y cerrar**, debes ver que el modal se cierra y el campo *Proveedor* del formulario principal se completa con `Laboratorios Vijosa S.A. de C.V.`.
4. **Completar Datos del Vendedor y Guardar:** En el formulario principal del Vendedor, tipear en el campo *Teléfono* los dígitos `77889900` y verificar que la máscara formatea dinámicamente el valor a `7788-9900`, ingresar en *Email* `carlos.mendez@vijosa.com` y hacer clic en el botón **Guardar** (o icono de nube), debes observar que el registro se almacena exitosamente y el campo *Código* muestra un código correlativo autogenerado con formato `P0001` (o correlativo siguiente).
5. **Asociación de Múltiples Vendedores a una Misma Empresa:** Regresar a la lista de **Proveedores y Laboratorios** mediante las migas de pan y presionar **Nuevo**. Escribir en *Nombre* `Ana López`, en el desplegable *Proveedor* seleccionar la empresa previamente creada `Laboratorios Vijosa S.A. de C.V.`, en *Teléfono* tipear `71234567` (se formatea como `7123-4567`), ingresar en *Email* `ana.lopez@vijosa.com` y hacer clic en **Guardar**, debes comprobar que Ana López recibe su propio código correlativo único (ej. `P0002`) y queda vinculada al mismo laboratorio.
6. **Verificación de Lista Unificada y Filtros por Tipo de Proveedor:** Regresar a la vista de lista de **Proveedores y Laboratorios**, debes ver a ambos vendedores (`Carlos Méndez` y `Ana López`) listados en registros independientes con sus respectivos códigos y teléfonos, compartiendo `Laboratorios Vijosa S.A. de C.V.` en la columna *Proveedor*. En la barra de búsqueda superior, hacer clic en el filtro rápido **Laboratorios**, debes comprobar que la lista mantiene a los vendedores cuyo proveedor es de tipo Laboratorio y oculta aquellos clasificados como Distribuidora o Droguería.
7. **Edición Modal de Laboratorio desde la Ficha del Vendedor:** En la lista de vendedores, hacer clic sobre `Carlos Méndez` para abrir su formulario y presionar el botón de enlace interno (ícono `->` / botón abrir registro) junto al campo *Proveedor*, debes ver que la Empresa se abre en una ventana modal emergente utilizando el formulario simplificado (`view_res_partner_laboratorio_quick_form`) sin recargar la pantalla completa ni mostrar campos genéricos de contactos de Odoo. Realizar una modificación menor (ej. cambiar nombre a `Laboratorios Vijosa S.A.`) y hacer clic en **Guardar**, debes comprobar que el cambio se sincroniza inmediatamente en la ficha del vendedor.

#### Casos Límite / Rutas de Excepción:
1. **Rechazo por Omisión de NRC Obligatorio en Empresa:** Presionar **Nuevo** para registrar un nuevo contacto, en *Proveedor* seleccionar **Crear y editar...**, ingresar en *Nombre del Proveedor* `Distribuidora Sin NRC`, seleccionar tipo `Distribuidora`, dejar el campo *NRC* en blanco y presionar **Guardar y cerrar**, debes ver una notificación modal de error de validación bloqueante con el mensaje `El NRC de "Distribuidora Sin NRC" es obligatorio.` impidiendo el guardado hasta ingresar el valor.
2. **Rechazo por Formato Inválido de NIT:** En la ventana emergente de la Empresa, escribir en el campo *NIT* un valor incompleto como `0614-123` y hacer clic en **Guardar y cerrar**, debes ver la notificación de validación `El NIT de "Distribuidora Sin NRC" debe tener el formato 0000-000000-000-0.` bloqueando el registro.
3. **Rechazo por Formato Inválido de Teléfono en Vendedor:** En el formulario del Vendedor, ingresar en el campo *Teléfono* una secuencia no conforme con el formato salvadoreño (ej. `12345`) y presionar **Guardar**, debes observar la alerta de validación `El teléfono de "..." debe tener el formato 0000-0000.` impidiendo el guardado.
4. **Independencia de Validaciones frente a Clientes y Contactos Generales:** Iniciar sesión con el usuario de Cajero (`cajero@caryvil.com`), navegar a **Farmacia Caryvil** -> **Clientes**, hacer clic en **Nuevo** y crear un cliente con un teléfono de formato libre (ej. número telefónico fijo o internacional), debes verificar que el cliente se almacena normalmente sin verse afectado por las restricciones estrictas de proveedores farmacéuticos.


