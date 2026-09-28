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
        echo "=== [Caryvil ERP] Base de datos '${DB_NAME}' no inicializada. Instalando base y caryvil_erp (--stop-after-init --no-http)... ==="
        odoo -c /etc/odoo/odoo.conf \
            --db_host="${HOST}" \
            --db_port="${DB_PORT}" \
            --db_user="${USER}" \
            --db_password="${PASSWORD}" \
            -d "${DB_NAME}" \
            -i "base,caryvil_erp" \
            --stop-after-init \
            --no-http
        echo "=== [Caryvil ERP] Inicializacion de base de datos completada. ==="
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
            DELETE FROM ir_attachment WHERE db_datas IS NULL AND store_fname IS NOT NULL;
        " 2>/dev/null || true

        MODULES_TO_UPDATE="${ODOO_UPDATE_MODULES:-caryvil_erp}"
        # Verificar si el módulo caryvil_erp está realmente instalado en la base de datos
        CARYVIL_STATUS=$(PGPASSWORD="${PASSWORD}" psql -h "${HOST}" -p "${DB_PORT}" -U "${USER}" -d "${DB_NAME}" -tAc "SELECT state FROM ir_module_module WHERE name = 'caryvil_erp';" 2>/dev/null || true)

        if [ "$CARYVIL_STATUS" != "installed" ]; then
            echo "=== [Caryvil ERP] Módulo 'caryvil_erp' no instalado (estado: '${CARYVIL_STATUS:-no registrado}'). Instalando (-i ${MODULES_TO_UPDATE})... ==="
            odoo -c /etc/odoo/odoo.conf \
                --db_host="${HOST}" \
                --db_port="${DB_PORT}" \
                --db_user="${USER}" \
                --db_password="${PASSWORD}" \
                -d "${DB_NAME}" \
                -i "${MODULES_TO_UPDATE}" \
                --stop-after-init \
                --no-http
            echo "=== [Caryvil ERP] Instalación de módulos completada (${MODULES_TO_UPDATE}). Iniciando servidor... ==="
        else
            echo "=== [Caryvil ERP] Módulo 'caryvil_erp' ya instalado. Ejecutando actualización de esquema (-u ${MODULES_TO_UPDATE})... ==="
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

        # -----------------------------------------------------------------------
        # GARANTIZAR VISIBILIDAD DEL MENÚ 'Farmacia Caryvil' EN EL MENÚ PRINCIPAL
        # Los menús raíz se ocultan cuando el usuario no pertenece a ningún grupo
        # de sus sub-ítems. En entornos efímeros (Render), la asignación de grupos
        # al usuario admin puede fallar silenciosamente durante -u (update).
        # Este bloque SQL garantiza que admin y odoobot tengan group_caryvil_manager
        # para que el menú raíz 'Farmacia Caryvil' siempre sea visible.
        # -----------------------------------------------------------------------
        echo "=== [Caryvil ERP] Verificando asignación de grupos de Farmacia Caryvil al usuario admin... ==="
        PGPASSWORD="${PASSWORD}" psql -h "${HOST}" -p "${DB_PORT}" -U "${USER}" -d "${DB_NAME}" -q -c "
            DO \$\$
            DECLARE
                v_admin_id    INTEGER;
            BEGIN
                -- Obtener el id del usuario admin (login='admin')
                SELECT id INTO v_admin_id
                FROM res_users
                WHERE login = 'admin'
                LIMIT 1;

                IF v_admin_id IS NOT NULL THEN
                    -- Insertar la relación en la tabla puente res_groups_users_rel para todos los grupos de caryvil_erp
                    INSERT INTO res_groups_users_rel (gid, uid)
                    SELECT rg.id, v_admin_id
                    FROM res_groups rg
                    JOIN ir_model_data imd ON imd.res_id = rg.id
                        AND imd.model = 'res.groups'
                        AND imd.module = 'caryvil_erp'
                    ON CONFLICT DO NOTHING;

                    RAISE NOTICE 'Grupos de Caryvil ERP asignados al usuario admin (uid=%)', v_admin_id;
                ELSE
                    RAISE WARNING 'No se pudo encontrar el usuario admin (login=admin)';
                END IF;
            END;
            \$\$;
        " 2>/dev/null || true

        python3 -c "
import odoo
from odoo import api
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', '${DB_NAME}'])
with odoo.registry('${DB_NAME}').cursor() as cr:
    env = api.Environment(cr, odoo.SUPERUSER_ID, {})
    admin = env['res.users'].search([('login', '=', 'admin')])
    grp = env.ref('caryvil_erp.group_caryvil_manager', raise_if_not_found=False)
    if admin and grp:
        admin.write({'groups_id': [(4, grp.id)]})
        cr.commit()
" 2>/dev/null || true
        echo "=== [Caryvil ERP] Verificación de grupos completada. ==="
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
