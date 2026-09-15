FROM odoo:17.0

USER root

# Instalar dependencias Python adicionales sin romper paquetes del sistema base
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Crear directorios para addons y configuración con permisos para usuario odoo
RUN mkdir -p /mnt/extra-addons /etc/odoo /var/lib/odoo \
    && chown -R odoo:odoo /mnt/extra-addons /etc/odoo /var/lib/odoo

# Copiar addons personalizados, configuración y script de arranque
COPY ./custom_addons /mnt/extra-addons
COPY ./infra/config/odoo.conf /etc/odoo/odoo.conf
COPY ./infra/docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && chown -R odoo:odoo /mnt/extra-addons /etc/odoo/odoo.conf /entrypoint.sh

USER odoo

VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

EXPOSE 8069 8072

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
