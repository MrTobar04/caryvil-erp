# -*- coding: utf-8 -*-
"""Pruebas unitarias de andamiaje y verificación del módulo caryvil_erp."""

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install", "caryvil", "scaffolding")
class TestCaryvilScaffolding(TransactionCase):
    """Verifica que el módulo caryvil_erp y sus menús estén correctamente instalados y registrados."""

    def test_module_installed(self):
        """Valida que el módulo caryvil_erp esté instalado en el registro de ir.module.module."""
        module = self.env["ir.module.module"].search([("name", "=", "caryvil_erp")], limit=1)
        if module:
            self.assertEqual(module.state, "installed")

    def test_root_menu_exists(self):
        """Valida que el menú raíz de Farmacia Caryvil exista en la base de datos."""
        menu = self.env.ref("caryvil_erp.menu_caryvil_root", raise_if_not_found=False)
        self.assertIsNotNone(menu, "El menú raíz menu_caryvil_root no fue encontrado")
        self.assertEqual(menu.name, "Farmacia Caryvil")

    def test_first_level_menus_exist(self):
        """Valida que los submenús de nivel superior estén creados y vinculados al menú raíz."""
        submenus = [
            "caryvil_erp.menu_caryvil_dashboard",
            "caryvil_erp.menu_caryvil_ventas",
            "caryvil_erp.menu_caryvil_inventario",
            "caryvil_erp.menu_caryvil_compras",
            "caryvil_erp.menu_caryvil_clientes",
            "caryvil_erp.menu_caryvil_configuracion",
        ]
        root_menu = self.env.ref("caryvil_erp.menu_caryvil_root", raise_if_not_found=False)
        for xml_id in submenus:
            menu = self.env.ref(xml_id, raise_if_not_found=False)
            self.assertIsNotNone(menu, f"El submenú {xml_id} no fue encontrado")
            if root_menu:
                self.assertEqual(menu.parent_id, root_menu)
