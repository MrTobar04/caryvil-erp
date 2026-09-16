# SPEC-1.1.2: Configuración del Servidor Odoo

## 1. Objective
Definir y parametrizar de manera estandarizada el archivo de configuración del servidor `odoo.conf` y el archivo de dependencias Python `requirements.txt`. Esta configuración optimiza el rendimiento del servidor Odoo para Farmacia Caryvil, habilitando la gestión de rutas de módulos personalizados (`addons_path`), el modo proxy para despliegue detrás de balanceadores en la nube (Render), límites de memoria y tiempo de CPU para evitar sobrecargas en servidores gratuitos, y dependencias para reportes e impresiones.

## 2. Scope
### 2.1. Included
* Creación y parametrización del archivo `infra/config/odoo.conf` base.
* Configuración de la directiva `addons_path` incluyendo los módulos base de Odoo y la ruta `/mnt/extra-addons`.
* Habilitación de `proxy_mode = True` para soportar cabeceras `X-Forwarded-For` y `X-Forwarded-Proto` en Render.
* Ajuste de directivas de límites de recursos: `workers`, `max_cron_threads`, `limit_memory_soft`, `limit_memory_hard`, `limit_time_cpu`, `limit_time_real`.
* Definición de `requirements.txt` con librerías requeridas (e.g., `num2words`, `phonenumbers`, `qrcode`, `psycopg2-binary`).
* Configuración de logging unificado (`logfile`, `log_level = info`, `log_handler = :INFO`).

### 2.2. Not Included (Out of Scope)
* Configuración de variables de entorno específicas y credenciales de producción (cubierto en `SPEC-1.2.2`).
* Creación de modelos de datos o lógica Python del módulo de negocio (cubierto en `SPEC-2.1.1`).

## 3. Context and Restrictions
* **Context:** Proporciona las directivas de comportamiento del motor Odoo en tiempo de ejecución, tanto en entorno local Docker como en el Web Service de Render.
* **Restrictions:**
  * Debe operar de forma óptima dentro de los límites del plan Free de Render (512 MB RAM / 0.1 CPU).
  * El modo de multiprocesamiento (`workers > 0`) o modo mono-proceso (`workers = 0`) debe ser configurable por variable de entorno para entornos restringidos.
  * La contraseña maestra de la base de datos (`admin_passwd`) jamás debe quedar escrita en texto plano en el repositorio.

## 4. Dependencias y Definición de Preparación (DoR)
* **Dependencias Previas:**
  * `SPEC-1.1.1` (Configuración del Entorno Docker).
* **Definition of Ready (DoR):**
  * [x] Arquitectura de carpetas del proyecto definida (`./infra/config`, `./custom_addons`).
  * [x] Versión de Python definida (Python 3.10 o superior).
  * [x] Lista de librerías auxiliares requeridas acordada (cálculo de montos en letras, generación de QR para comprobantes).

## 5. Design (Implementation Details)
* **Architecture:**
  * Archivo `infra/config/odoo.conf`:
    ```ini
    [options]
    addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
    data_dir = /var/lib/odoo
    admin_passwd = $ADMIN_PASSWORD
    db_host = $DB_HOST
    db_port = $DB_PORT
    db_user = $DB_USER
    db_password = $DB_PASSWORD
    db_name = $DB_NAME
    proxy_mode = True
    list_db = True
    workers = 0
    max_cron_threads = 1
    limit_time_cpu = 120
    limit_time_real = 240
    limit_memory_soft = 671088640
    limit_memory_hard = 805306368
    log_level = info
    ```
  * Archivo `requirements.txt`:
    ```text
    num2words>=0.5.12
    phonenumbers>=8.13.0
    qrcode[pil]>=7.4.2
    psycopg2-binary>=2.9.9
    python-dotenv>=1.0.0
    ```
* **Configuration Lifecycle:**
  * El archivo de configuración es montado como volumen en Docker local en `/etc/odoo/odoo.conf` o inyectado mediante comando de arranque `odoo -c /etc/odoo/odoo.conf`.

## 6. Acceptance Criteria
* **Scenario 1: Carga automática de módulos personalizados**
  * **Given** El servidor Odoo arrancando con `odoo.conf` configurado.
  * **When** El administrador actualiza la lista de aplicaciones desde la interfaz web.
  * **Then** Los módulos ubicados en `/mnt/extra-addons/` (como `caryvil_erp`) deben aparecer disponibles para instalación.
* **Scenario 2: Detección correcta de protocolo HTTPS tras proxy inverso**
  * **Given** `proxy_mode = True` configurado en `odoo.conf`.
  * **When** Un cliente accede a Odoo a través de un dominio HTTPS en Render (`https://caryvil-erp.onrender.com`).
  * **Then** Odoo no debe generar redirecciones infinitas ni errores de recursos mixtos (HTTP/HTTPS) en hojas de estilo o scripts.
* **Scenario 3: Instalación de dependencias Python en la imagen**
  * **Given** El archivo `requirements.txt` referenciado en el `Dockerfile`.
  * **When** Se compila la imagen Docker.
  * **Then** Los módulos `num2words` y `qrcode` deben poder ser importados desde el intérprete Python de Odoo sin errores `ModuleNotFoundError`.

## 7. Verification Plan
* **Automated Tests:**
  * Ejecutar `python3 -c "import num2words, qrcode, phonenumbers"` dentro del contenedor para validar dependencias instaladas.
* **Manual Verification:**
  * Verificar en los logs de arranque de Odoo (`docker compose logs web`) que las rutas de `addons_path` incluyan `/mnt/extra-addons`.
  * Validar que la opción de gestionar base de datos responda adecuadamente.

## 8. Security and Privacy
* La directiva `admin_passwd` debe poblarse dinámicamente mediante variables de entorno en el entrypoint o pasarse como argumento CLI.
* Directiva `list_db`: Debe poder desactivarse (`list_db = False`) en producción para impedir que usuarios anónimos listen o gestionen bases de datos.

## 9. Risks and Mitigation
* **Risk:** Límite de memoria superado en Render (*Out of Memory* - OOM Kill) si se activan múltiples `workers`.
  * **Mitigation:** Mantener `workers = 0` en entornos con menos de 1 GB de RAM para que Odoo corra en modo mono-proceso multihilo liviano.

## 10. Deliverables & Config as Code
* Archivo `infra/config/odoo.conf.template` o `infra/config/odoo.conf`.
* Archivo `requirements.txt` con versiones fijadas (*pinned*).
* Script de inicialización / entrypoint `entrypoint.sh` para sustitución de variables en `odoo.conf` si aplica.

## 11. Definition of Done (DoD)
* [x] Archivos `infra/config/odoo.conf` y `requirements.txt` creados en el repositorio.
* [x] Dependencias Python instaladas y verificadas dentro del contenedor.
* [x] Carga exitosa de rutas de addons comprobada en los logs de inicialización.
* [x] `proxy_mode = True` validado sin provocar bucles de redirección.
* [x] Revisión de código completada y aprobada.
