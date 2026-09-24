#!/bin/bash
set -e

# Configuración por defecto de variables de entorno (soporta DB_HOST, POSTGRES_HOST y HOST)
: ${HOST:="${DB_HOST:-${POSTGRES_HOST:-db}}"}
# DB_PORT: puerto de PostgreSQL (5432). Se usa DB_PORT para no colisionar con la
# variable reservada PORT de Render, que indica el puerto HTTP del servicio web.
: ${DB_PORT:="${POSTGRES_PORT:-5432}"}
: ${USER:="${DB_USER:-${POSTGRES_USER:-odoo}}"}
: ${PASSWORD:="${DB_PASSWORD:-${POSTGRES_PASSWORD:-odoo_dev_password_2026}}"}
: ${DB_NAME:="${POSTGRES_DB:-caryvil_dev}"}
: ${ADMIN_PASSWORD:="admin_caryvil_secret_2026"}
# PORT: puerto HTTP en el que Odoo debe escuchar. Render lo inyecta automáticamente.
# Por defecto 8069 para desarrollo local con docker-compose.
: ${PORT:="${ODOO_HTTP_PORT:-8069}"}

# Sanitizar HOST en caso de recibir una cadena de conexión tipo URI (postgresql://user:pass@host/db)
if echo "$HOST" | grep -q "@"; then
    HOST=$(echo "$HOST" | sed -e 's|^.*@||' -e 's|/.*$||' -e 's|:.*$||')
fi

echo "=== [Caryvil ERP] Verificando disponibilidad de PostgreSQL en ${HOST}:${DB_PORT} ==="
while ! nc -z ${HOST} ${DB_PORT} 2>/dev/null && ! pg_isready -h ${HOST} -p ${DB_PORT} -U ${USER} 2>/dev/null; do
  sleep 1
done
echo "=== [Caryvil ERP] Base de datos PostgreSQL disponible ==="

# Sustitución de variables de entorno en odoo.conf si existen marcadores o valores previos
if [ -f /etc/odoo/odoo.conf ]; then
    sed -i "s|^db_host = .*|db_host = ${HOST}|g; s|\$DB_HOST|${HOST}|g; s|\$HOST|${HOST}|g" /etc/odoo/odoo.conf
    sed -i "s|^db_port = .*|db_port = ${DB_PORT}|g; s|\$DB_PORT|${DB_PORT}|g" /etc/odoo/odoo.conf
    sed -i "s|^http_port = .*|http_port = ${PORT}|g" /etc/odoo/odoo.conf
    sed -i "s|^db_user = .*|db_user = ${USER}|g; s|\$DB_USER|${USER}|g; s|\$USER|${USER}|g" /etc/odoo/odoo.conf
    sed -i "s|^db_password = .*|db_password = ${PASSWORD}|g; s|\$DB_PASSWORD|${PASSWORD}|g; s|\$PASSWORD|${PASSWORD}|g" /etc/odoo/odoo.conf
    sed -i "s|^db_name = .*|db_name = ${DB_NAME}|g; s|\$DB_NAME|${DB_NAME}|g" /etc/odoo/odoo.conf
    sed -i "s|^admin_passwd = .*|admin_passwd = ${ADMIN_PASSWORD}|g; s|\$ADMIN_PASSWORD|${ADMIN_PASSWORD}|g" /etc/odoo/odoo.conf
    if grep -q "^dbfilter" /etc/odoo/odoo.conf; then
        sed -i "s|^dbfilter = .*|dbfilter = ^${DB_NAME}\$|g" /etc/odoo/odoo.conf
    else
        echo "dbfilter = ^${DB_NAME}\$" >> /etc/odoo/odoo.conf
    fi
fi

# Verificar si la base de datos ya está inicializada con las tablas del sistema Odoo
INIT_FLAGS=()
if [[ "$*" != *"-i"* && "$*" != *"--init"* ]]; then
    TABLE_CHECK=$(PGPASSWORD="${PASSWORD}" psql -h "${HOST}" -p "${DB_PORT}" -U "${USER}" -d "${DB_NAME}" -tAc "SELECT 1 FROM information_schema.tables WHERE table_name = 'ir_module_module';" 2>/dev/null || true)
    if [ "$TABLE_CHECK" != "1" ]; then
        echo "=== [Caryvil ERP] Base de datos '${DB_NAME}' no inicializada. Ejecutando inicialización automática (-i base,caryvil_erp) ==="
        INIT_FLAGS=(-i "base,caryvil_erp")
    else
        echo "=== [Caryvil ERP] Base de datos '${DB_NAME}' ya inicializada. Sincronizando configuracion y assets... ==="
        # -----------------------------------------------------------------------
        # ALMACENAMIENTO DE ASSETS EN BASE DE DATOS (RENDER EPHEMERAL FIX)
        # En entornos efímeros (como Render Free), el filestore en disco se destruye al reiniciar.
        # Guardar adjuntos y assets compilados en BD (ir_attachment.location='db') evita
        # el error 500 (FileNotFoundError) en web.assets_frontend.min.css y JS bundles.
        # Además se eliminan registros viejos de assets para forzar regeneración limpia en BD.
        # -----------------------------------------------------------------------
        PGPASSWORD="${PASSWORD}" psql -h "${HOST}" -p "${DB_PORT}" -U "${USER}" -d "${DB_NAME}" -q -c "
            INSERT INTO ir_config_parameter (key, value)
            VALUES ('ir_attachment.location', 'db')
            ON CONFLICT (key) DO UPDATE SET value = 'db';
            DELETE FROM ir_attachment WHERE url LIKE '/web/assets/%';
        " 2>/dev/null || true

        echo "=== [Caryvil ERP] Ejecutando actualizacion de esquema (-u caryvil_erp)... ==="
        # -----------------------------------------------------------------------
        # FASE DE ACTUALIZACIÓN DE MÓDULOS — siempre se ejecuta en redespliegues.
        # Odoo -u es idempotente: si no hay columnas/vistas nuevas, termina sin cambios.
        # Esto garantiza que cualquier ALTER TABLE (nuevos campos en res.company,
        # res.partner, etc.) se aplique ANTES de que el servidor HTTP arranque,
        # evitando el crash "UndefinedColumn" en el primer request post-despliegue.
        #
        # Se usa ODOO_UPDATE_MODULES si está definida (permite ampliar la lista de
        # módulos a actualizar desde IaC/Render), o bien "caryvil_erp" por defecto.
        # -----------------------------------------------------------------------
        MODULES_TO_UPDATE="${ODOO_UPDATE_MODULES:-caryvil_erp}"
        odoo -c /etc/odoo/odoo.conf \
            --db_host="${HOST}" \
            --db_port="${DB_PORT}" \
            --db_user="${USER}" \
            --db_password="${PASSWORD}" \
            -d "${DB_NAME}" \
            -u "${MODULES_TO_UPDATE}" \
            --stop-after-init \
            --no-http
        echo "=== [Caryvil ERP] Actualizacion de esquema completada (modulos: ${MODULES_TO_UPDATE}). Iniciando servidor... ==="
    fi
fi

case "$1" in
    -- | odoo)
        shift
        if [[ "$1" == "scaffold" ]] ; then
            exec odoo "$@"
        else
            exec odoo -c /etc/odoo/odoo.conf --db_host="${HOST}" --db_port="${DB_PORT}" --db_user="${USER}" --db_password="${PASSWORD}" -d "${DB_NAME}" --http-port="${PORT}" "${INIT_FLAGS[@]}" "$@"
        fi
        ;;
    -*)
        exec odoo -c /etc/odoo/odoo.conf --db_host="${HOST}" --db_port="${DB_PORT}" --db_user="${USER}" --db_password="${PASSWORD}" -d "${DB_NAME}" --http-port="${PORT}" "${INIT_FLAGS[@]}" "$@"
        ;;
    *)
        exec "$@"
esac

exit 1
