# -*- coding: utf-8 -*-
{
    "name": "Farmacia Caryvil ERP",
    "version": "17.0.1.0.1",
    "category": "Pharmacy/ERP",
    "summary": "Sistema integral de gestión farmacéutica: Inventario, Ventas, Compras y Clientes",
    "description": """
        Personalización y extensión de Odoo ERP para Farmacia Caryvil.
        Características:
        - Control estricto de lotes y fechas de vencimiento con estrategia FEFO.
        - Gestión de unidades de medida farmacéuticas (Cajas, Blísteres, Unidades).
        - Venta ágil de mostrador con emisión de ticket térmico de 80mm.
        - Registro de clientes con validación sintáctica de DUI/NIT salvadoreño.
        - Gestión de compras y abastecimiento con actualización automática de stock.
        - Dashboard ejecutivo de KPIs y monitoreo de stock crítico.
    """,
    "author": "Equipo de Desarrollo Caryvil - UDB",
    "website": "https://github.com/MelissaFloresA/Odoo_ERP_Farmacia",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
        "stock",
        "product_expiry",
        "purchase",
        "purchase_stock",
        "sale_management",
        "account",
        "uom",
    ],
    "data": [
        "security/caryvil_security.xml",
        "security/ir.model.access.csv",
        "security/caryvil_security_rules.xml",
        "data/company_data.xml",
        "data/tax_data.xml",
        "data/pharmacy_categories_data.xml",
        "data/active_ingredients_data.xml",
        "data/pharmacy_uom_data.xml",
        "data/users_roles_data.xml",
        "data/res_partner_vendor_sequence.xml",
        "data/purchase_order_sequence.xml",
        "data/iva_purchase_tax.xml",
        "data/stock_lot_cron.xml",
        "views/caryvil_medicine_views.xml",
        "views/caryvil_dashboard_views.xml",
        "views/caryvil_menus.xml",
        "views/res_partner_customer_views.xml",
        "views/res_partner_vendor_views.xml",
        "views/product_supplierinfo_views.xml",
        "views/purchase_order_views.xml",
        "views/stock_picking_views.xml",
        "views/product_medicine_views.xml",
        "views/product_template_views.xml",
        "views/web_login_templates.xml",
        "reports/report_purchase_order.xml",
        "reports/purchase_order_report_action.xml",
        "views/stock_lot_medicine_views.xml",
        "views/stock_reordering_rules_views.xml",
        "views/stock_quant_views.xml",
    ],
    "demo": [
        "demo/demo_vendors_data.xml",
        "demo/demo_customers_data.xml",
        "demo/demo_medicines_data.xml",
        "demo/demo_inventory_stock_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "caryvil_erp/static/src/scss/custom_theme.scss",
            "caryvil_erp/static/src/scss/caryvil_sales_dashboard.scss",
            "caryvil_erp/static/src/js/masked_char_field.js",
            "caryvil_erp/static/src/js/purchase_live_totals.js",
            "caryvil_erp/static/src/js/caryvil_sales_dashboard.js",
            "caryvil_erp/static/src/xml/purchase_live_totals.xml",
            "caryvil_erp/static/src/xml/caryvil_sales_dashboard.xml",
        ],
        "web.assets_frontend": [
            "caryvil_erp/static/src/scss/custom_login.scss",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
}
