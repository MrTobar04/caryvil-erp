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


