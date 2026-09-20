#!/bin/bash
set -e

# Configuración por defecto de variables de entorno (soporta DB_HOST y HOST)
: ${HOST:="${DB_HOST:-db}"}
# DB_PORT: puerto de PostgreSQL (5432). Se usa DB_PORT para no colisionar con la
# variable reservada PORT de Render, que indica el puerto HTTP del servicio web.
: ${DB_PORT:="5432"}
: ${USER:="${DB_USER:-odoo}"}
: ${PASSWORD:="${DB_PASSWORD:-odoo_dev_password_2026}"}
: ${DB_NAME:="caryvil_dev"}
: ${ADMIN_PASSWORD:="admin_caryvil_secret_2026"}
# PORT: puerto HTTP en el que Odoo debe escuchar. Render lo inyecta automáticamente.
# Por defecto 8069 para desarrollo local con docker-compose.
: ${PORT:="8069"}

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
fi

# Verificar si la base de datos ya está inicializada con las tablas del sistema Odoo
INIT_FLAGS=()
if [[ "$*" != *"-i"* && "$*" != *"--init"* ]]; then
    TABLE_CHECK=$(PGPASSWORD="${PASSWORD}" psql -h "${HOST}" -p "${DB_PORT}" -U "${USER}" -d "${DB_NAME}" -tAc "SELECT 1 FROM information_schema.tables WHERE table_name = 'ir_module_module';" 2>/dev/null || true)
    if [ "$TABLE_CHECK" != "1" ]; then
        echo "=== [Caryvil ERP] Base de datos '${DB_NAME}' no inicializada. Ejecutando inicialización automática (-i base,caryvil_erp) ==="
        INIT_FLAGS=(-i "base,caryvil_erp")
    else
        echo "=== [Caryvil ERP] Base de datos '${DB_NAME}' ya inicializada ==="
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
