# -*- coding: utf-8 -*-
from odoo.fields import Command
from . import models  # noqa: F401
from . import controllers  # noqa: F401
from . import wizards  # noqa: F401


def post_init_hook(env):
    """Configura el almacenamiento de adjuntos, sincronización de compañía e IVA salvadoreño.

    En entornos efímeros (como Render), evita errores 500 garantizando que
    los bundles de assets se persistan en PostgreSQL. Además, sincroniza la
    compañía principal (Farmacia Caryvil) e impuestos por defecto para todos los usuarios.
    """
    env["ir.config_parameter"].sudo().set_param("ir_attachment.location", "db")

    company = env.ref("base.main_company", raise_if_not_found=False)
    tax_13 = env.ref("caryvil_erp.tax_caryvil_iva_ventas_13", raise_if_not_found=False)
    account_recv = env.ref("caryvil_erp.account_caryvil_receivable", raise_if_not_found=False)

    if company:
        company_vals = {
            "name": "Farmacia Caryvil",
            "legal_name": "Farmacia Caryvil S.A. de C.V.",
            "street": "Colonia San Antonio, Calle Principal #12",
            "city": "Soyapango",
            "phone": "2270-1234",
            "email": "contacto@farmaciacaryvil.com",
            "economic_activity": ("Venta al por menor de productos farmacéuticos y medicinales"),
        }
        if tax_13:
            company_vals["account_sale_tax_id"] = tax_13.id
        company.sudo().write(company_vals)

        # Configurar la cuenta por cobrar por defecto para los clientes
        if account_recv:
            env["ir.property"].sudo()._set_default(
                "property_account_receivable_id",
                "res.partner",
                account_recv,
                company,
            )

        # Garantizar que los usuarios clave tengan asignada la compañía principal
        users = (
            env["res.users"]
            .sudo()
            .search(
                [
                    (
                        "login",
                        "in",
                        [
                            "cajero@caryvil.com",
                            "compras@caryvil.com",
                            "admin_caryvil@caryvil.com",
                            "admin",
                        ],
                    )
                ]
            )
        )
        for user in users:
            user.write(
                {
                    "company_ids": [Command.link(company.id)],
                }
            )
            user.write(
                {
                    "company_id": company.id,
                }
            )
