# -*- coding: utf-8 -*-
{
    'name': 'Farmacia Caryvil ERP',
    'version': '17.0.1.0.0',
    'category': 'Pharmacy/ERP',
    'summary': 'Sistema integral de gestión farmacéutica: Inventario, Ventas, Compras y Clientes',
    'description': """
        Personalización y extensión de Odoo ERP para Farmacia Caryvil.
        Características:
        - Control estricto de lotes y fechas de vencimiento con estrategia FEFO.
        - Gestión de unidades de medida farmacéuticas (Cajas, Blísteres, Unidades).
        - Venta ágil de mostrador con emisión de ticket térmico de 80mm.
        - Registro de clientes con validación sintáctica de DUI/NIT salvadoreño.
        - Gestión de compras y abastecimiento con actualización automática de stock.
        - Dashboard ejecutivo de KPIs y monitoreo de stock crítico.
    """,
    'author': 'Equipo de Desarrollo Caryvil - UDB',
    'website': 'https://github.com/MelissaFloresA/Odoo_ERP_Farmacia',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
        'stock',
        'purchase',
        'sale_management',
        'account',
        'uom',
    ],
    'data': [
        'security/caryvil_security.xml',
        'security/ir.model.access.csv',
        'views/caryvil_menus.xml',
        'views/res_partner_customer_views.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'caryvil_erp/static/src/scss/custom_theme.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
