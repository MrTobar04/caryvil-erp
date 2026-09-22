# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestCaryvilSecurity(TransactionCase):
    """Suite de pruebas unitarias para SPEC-2.2.1: Definición de Roles y Grupos de Usuarios.

    Valida:
    1. Existencia y parametrización de la categoría de módulo 'Farmacia Caryvil'.
    2. Creación y asignación de los 3 grupos de seguridad jerárquicos.
    3. Herencia de privilegios e implied_ids según el diseño RBAC.
    4. Comportamiento de `has_group` en usuarios asignados a cada nivel funcional.
    """

    def setUp(self):
        super(TestCaryvilSecurity, self).setUp()
        self.category = self.env.ref("caryvil_erp.module_category_caryvil_erp")
        self.group_cashier = self.env.ref("caryvil_erp.group_caryvil_cashier")
        self.group_inventory = self.env.ref("caryvil_erp.group_caryvil_inventory_purchases")
        self.group_manager = self.env.ref("caryvil_erp.group_caryvil_manager")

        # Usuarios de prueba para cada rol
        self.user_cashier = self.env["res.users"].create({
            "name": "Test Cajero Dependiente",
            "login": "test_cashier_user",
            "email": "test_cashier@caryvil.test",
            "groups_id": [(6, 0, [self.group_cashier.id])],
        })

        self.user_inventory = self.env["res.users"].create({
            "name": "Test Encargado Compras e Inventario",
            "login": "test_inventory_user",
            "email": "test_inventory@caryvil.test",
            "groups_id": [(6, 0, [self.group_inventory.id])],
        })

        self.user_manager = self.env["res.users"].create({
            "name": "Test Administrador General",
            "login": "test_manager_user",
            "email": "test_manager@caryvil.test",
            "groups_id": [(6, 0, [self.group_manager.id])],
        })

    def test_01_security_category_definition(self):
        """Valida que la categoría de módulo exista con el nombre y secuencia configurados."""
        self.assertTrue(self.category, "La categoría module_category_caryvil_erp debe existir")
        self.assertEqual(self.category.name, "Farmacia Caryvil")
        self.assertEqual(self.category.sequence, 10)

    def test_02_groups_belong_to_caryvil_category(self):
        """Valida que los 3 grupos pertenezcan a la categoría de Farmacia Caryvil."""
        self.assertEqual(self.group_cashier.category_id.id, self.category.id)
        self.assertEqual(self.group_inventory.category_id.id, self.category.id)
        self.assertEqual(self.group_manager.category_id.id, self.category.id)

    def test_03_cashier_role_permissions(self):
        """Valida que el rol Cajero herede base.group_user pero no compras ni administración."""
        self.assertTrue(self.user_cashier.has_group("caryvil_erp.group_caryvil_cashier"))
        self.assertTrue(self.user_cashier.has_group("base.group_user"))
        self.assertFalse(self.user_cashier.has_group("caryvil_erp.group_caryvil_inventory_purchases"))
        self.assertFalse(self.user_cashier.has_group("caryvil_erp.group_caryvil_manager"))
        self.assertFalse(self.user_cashier.has_group("purchase.group_purchase_user"))
        self.assertFalse(self.user_cashier.has_group("stock.group_stock_user"))

    def test_04_inventory_purchases_role_inheritance(self):
        """Valida que el rol Encargado herede permisos de cajero, stock user y purchase user."""
        self.assertTrue(self.user_inventory.has_group("caryvil_erp.group_caryvil_inventory_purchases"))
        self.assertTrue(self.user_inventory.has_group("caryvil_erp.group_caryvil_cashier"))
        self.assertTrue(self.user_inventory.has_group("base.group_user"))
        self.assertTrue(self.user_inventory.has_group("stock.group_stock_user"))
        self.assertTrue(self.user_inventory.has_group("purchase.group_purchase_user"))
        self.assertFalse(self.user_inventory.has_group("caryvil_erp.group_caryvil_manager"))
        self.assertFalse(self.user_inventory.has_group("stock.group_stock_manager"))
        self.assertFalse(self.user_inventory.has_group("purchase.group_purchase_manager"))

    def test_05_manager_role_full_inheritance(self):
        """Valida que el rol Administrador herede los permisos operativos y de gestión."""
        self.assertTrue(self.user_manager.has_group("caryvil_erp.group_caryvil_manager"))
        self.assertTrue(self.user_manager.has_group("caryvil_erp.group_caryvil_inventory_purchases"))
        self.assertTrue(self.user_manager.has_group("caryvil_erp.group_caryvil_cashier"))
        self.assertTrue(self.user_manager.has_group("base.group_user"))
        self.assertTrue(self.user_manager.has_group("stock.group_stock_manager"))
        self.assertTrue(self.user_manager.has_group("stock.group_stock_user"))
        self.assertTrue(self.user_manager.has_group("purchase.group_purchase_manager"))
        self.assertTrue(self.user_manager.has_group("purchase.group_purchase_user"))
        self.assertTrue(self.user_manager.has_group("sales_team.group_sale_manager"))
