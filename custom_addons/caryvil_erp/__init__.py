# -*- coding: utf-8 -*-
from odoo.fields import Command
from . import models  # noqa: F401
from . import controllers  # noqa: F401
from . import wizards  # noqa: F401


def _setup_company_and_users(env):
    """Configura la compañía principal (Farmacia Caryvil) e impuestos."""
    env["ir.config_parameter"].sudo().set_param("ir_attachment.location", "db")

    company = env.ref("base.main_company", raise_if_not_found=False)
    tax_13 = env.ref("caryvil_erp.tax_caryvil_iva_ventas_13", raise_if_not_found=False)
    account_recv = env.ref("caryvil_erp.account_caryvil_receivable", raise_if_not_found=False)

    if not company:
        return

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

    if account_recv:
        env["ir.property"].sudo()._set_default(
            "property_account_receivable_id",
            "res.partner",
            account_recv,
            company,
        )

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
        user.write({"company_ids": [Command.link(company.id)]})
        user.write({"company_id": company.id})


def _purge_generic_demo_data(env):
    """Elimina registros demo nativos de Odoo incompatibles con el catálogo farmacéutico."""
    company = env.ref("base.main_company", raise_if_not_found=False)
    try:
        # 0. Eliminar reglas de reabastecimiento (orderpoints) genéricas
        # de Odoo demo (ej. Office Lamp FURN_8888, Desk Pad, etc.)
        env["stock.warehouse.orderpoint"].sudo().search(
            [("product_id.active_ingredient_id", "=", False)]
        ).unlink()

        # 1. Eliminar órdenes de venta y compra genéricas nativas de Odoo demo
        env["sale.order"].sudo().search([("partner_id.is_pharmacy_customer", "=", False)]).unlink()
        env["purchase.order"].sudo().search(
            [
                ("partner_id.is_pharmacy_vendor", "=", False),
                ("laboratory_id.is_pharmacy_vendor", "=", False),
            ]
        ).unlink()

        # 2. Eliminar plantillas de producto genéricas que no son medicamentos de Caryvil
        generic_tmpls = env["product.template"].sudo().search(
            [
                ("active_ingredient_id", "=", False),
                ("therapeutic_category_id", "=", False),
            ]
        )
        if generic_tmpls:
            generic_prods = generic_tmpls.product_variant_ids
            env["stock.quant"].sudo().search([("product_id", "in", generic_prods.ids)]).unlink()
            env["stock.move.line"].sudo().search([("product_id", "in", generic_prods.ids)]).unlink()
            env["stock.move"].sudo().search([("product_id", "in", generic_prods.ids)]).unlink()
            env["stock.valuation.layer"].sudo().search([("product_id", "in", generic_prods.ids)]).unlink()
            generic_tmpls.unlink()

        # 3. Eliminar partners demo genéricos nativos de Odoo
        protected_partner_ids = [company.id] if company else []
        admin_user = env.ref("base.user_admin", raise_if_not_found=False)
        root_partner = env.ref("base.partner_root", raise_if_not_found=False)
        if admin_user and admin_user.partner_id:
            protected_partner_ids.append(admin_user.partner_id.id)
        if root_partner:
            protected_partner_ids.append(root_partner.id)

        generic_partners = env["res.partner"].sudo().search(
            [
                ("is_pharmacy_customer", "=", False),
                ("is_pharmacy_vendor", "=", False),
                ("id", "not in", protected_partner_ids),
                ("is_company", "=", True),
            ]
        )
        if generic_partners:
            generic_partners.unlink()
    except Exception:
        pass


def post_init_hook(env):
    """Configura el almacenamiento de adjuntos, compañía e IVA, y limpia datos demo."""
    _setup_company_and_users(env)
    _purge_generic_demo_data(env)
