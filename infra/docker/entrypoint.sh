#!/bin/bash
set -e

# Configuración por defecto de variables de entorno
: ${HOST:="db"}
: ${PORT:="5432"}
: ${USER:="odoo"}
: ${PASSWORD:="odoo_dev_password_2026"}
: ${DB_NAME:="caryvil_dev"}
: ${ADMIN_PASSWORD:="admin_caryvil_secret_2026"}

echo "=== [Caryvil ERP] Verificando disponibilidad de PostgreSQL en ${HOST}:${PORT} ==="
while ! nc -z ${HOST} ${PORT} 2>/dev/null && ! pg_isready -h ${HOST} -p ${PORT} -U ${USER} 2>/dev/null; do
  sleep 1
done
echo "=== [Caryvil ERP] Base de datos PostgreSQL disponible ==="

# Sustitución de variables de entorno en odoo.conf si existen marcadores
if [ -f /etc/odoo/odoo.conf ]; then
    sed -i "s|\$HOST|${HOST}|g" /etc/odoo/odoo.conf
    sed -i "s|\$PORT|${PORT}|g" /etc/odoo/odoo.conf
    sed -i "s|\$USER|${USER}|g" /etc/odoo/odoo.conf
    sed -i "s|\$PASSWORD|${PASSWORD}|g" /etc/odoo/odoo.conf
    sed -i "s|\$DB_NAME|${DB_NAME}|g" /etc/odoo/odoo.conf
    sed -i "s|\$ADMIN_PASSWORD|${ADMIN_PASSWORD}|g" /etc/odoo/odoo.conf
fi

case "$1" in
    -- | odoo)
        shift
        if [[ "$1" == "scaffold" ]] ; then
            exec odoo "$@"
        else
            exec odoo -c /etc/odoo/odoo.conf "$@"
        fi
        ;;
    -*)
        exec odoo -c /etc/odoo/odoo.conf "$@"
        ;;
    *)
        exec "$@"
esac

exit 1
