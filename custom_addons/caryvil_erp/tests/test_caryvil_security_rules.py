# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestCaryvilSecurityRules(TransactionCase):
    """Suite de pruebas unitarias para SPEC-2.2.2: Reglas de Acceso y Seguridad de Modelos.

    Valida:
    1. Permisos CRUD a nivel de modelo (ACL ir.model.access.csv) para Cajero, Inventario y Administrador.
    2. Restricción de eliminación en catálogo de productos y clientes para no administradores.
    3. Restricción de modificación de facturas publicadas para el rol Cajero.
    4. Reglas de registro (ir.rule) para órdenes de venta y albaranes validados.
    """

    def setUp(self):
        super(TestCaryvilSecurityRules, self).setUp()
        self.group_cashier = self.env.ref("caryvil_erp.group_caryvil_cashier")
        self.group_inventory = self.env.ref("caryvil_erp.group_caryvil_inventory_purchases")
        self.group_manager = self.env.ref("caryvil_erp.group_caryvil_manager")

        # Usuarios de prueba para cada rol
        self.user_cashier = self.env["res.users"].create({
            "name": "Cajero Seguridad Test",
            "login": "cashier_sec_test",
            "email": "cashier_sec@caryvil.test",
            "groups_id": [(6, 0, [self.group_cashier.id])],
        })

        self.user_inventory = self.env["res.users"].create({
            "name": "Inventario Seguridad Test",
            "login": "inv_sec_test",
            "email": "inv_sec@caryvil.test",
            "groups_id": [(6, 0, [self.group_inventory.id])],
        })

        self.user_manager = self.env["res.users"].create({
            "name": "Manager Seguridad Test",
            "login": "mgr_sec_test",
            "email": "mgr_sec@caryvil.test",
            "groups_id": [(6, 0, [self.group_manager.id])],
        })

        # Datos base de prueba
        self.category = self.env["product.category"].create({
            "name": "Categoría Test Seguridad",
        })

        self.medicine = self.env["product.template"].create({
            "name": "Paracetamol 500mg Test Sec",
            "categ_id": self.category.id,
            "type": "consu",
            "list_price": 1.50,
        })

        self.customer = self.env["res.partner"].create({
            "name": "Cliente Test Seguridad",
            "customer_rank": 1,
            "dui": "01234567-8",
        })

    def test_01_cashier_product_read_only_and_no_unlink(self):
        """Scenario 1: Cajero puede leer catálogo pero no puede crear, modificar ni eliminar productos."""
        # Lectura permitida
        med_cashier = self.medicine.with_user(self.user_cashier)
        self.assertEqual(med_cashier.name, "Paracetamol 500mg Test Sec")

        # Intento de modificación -> AccessError
        with self.assertRaises(AccessError):
            med_cashier.write({"list_price": 2.00})

        # Intento de creación -> AccessError
        with self.assertRaises(AccessError):
            self.env["product.template"].with_user(self.user_cashier).create({
                "name": "Amoxicilina 500mg No Autorizada",
                "categ_id": self.category.id,
            })

        # Intento de eliminación -> AccessError
        with self.assertRaises(AccessError):
            med_cashier.unlink()

    def test_02_cashier_partner_create_edit_allowed_unlink_denied(self):
        """Scenario 2: Cajero puede crear y editar clientes en mostrador, pero no puede eliminarlos."""
        # Creación permitida
        new_partner = self.env["res.partner"].with_user(self.user_cashier).create({
            "name": "Nuevo Paciente Mostrador",
            "dui": "09876543-2",
            "customer_rank": 1,
        })
        self.assertTrue(new_partner.id, "El cajero debe poder registrar nuevos clientes")

        # Modificación permitida
        new_partner.write({"phone": "7000-1122"})
        self.assertEqual(new_partner.phone, "7000-1122")

        # Eliminación denegada por ACL perm_unlink = 0
        with self.assertRaises(AccessError):
            new_partner.unlink()

        # Administrador sí puede eliminar clientes
        partner_mgr = new_partner.with_user(self.user_manager)
        partner_mgr.unlink()

    def test_03_posted_invoice_readonly_for_cashier(self):
        """Scenario 3: Cajero no puede modificar facturas en estado publicado (posted)."""
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            journal = self.env["account.journal"].create({
                "name": "Ventas Test Sec",
                "code": "VTSEC",
                "type": "sale",
            })

        # Crear factura en borrador con usuario administrador
        invoice = self.env["account.move"].create({
            "partner_id": self.customer.id,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "invoice_line_ids": [(0, 0, {
                "name": "Venta Medicamento Test",
                "quantity": 2,
                "price_unit": 3.00,
            })],
        })

        # Cajero puede leer la factura
        inv_cashier = invoice.with_user(self.user_cashier)
        self.assertTrue(inv_cashier.exists())

        # Publicar factura con admin
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

        # Cajero intenta modificar la factura publicada -> AccessError
        with self.assertRaises(AccessError):
            inv_cashier.write({"ref": "Modificación No Autorizada"})

        # Cajero intenta eliminar la factura publicada -> AccessError
        with self.assertRaises(AccessError):
            inv_cashier.unlink()

    def test_04_inventory_product_crud_no_unlink(self):
        """Valida que el rol Inventario puede crear/editar productos pero no eliminarlos."""
        # Creación permitida
        med_inv = self.env["product.template"].with_user(self.user_inventory).create({
            "name": "Ibuprofeno 400mg Inv Test",
            "categ_id": self.category.id,
            "list_price": 0.80,
        })
        self.assertTrue(med_inv.id)

        # Modificación permitida
        med_inv.write({"list_price": 0.90})
        self.assertEqual(med_inv.list_price, 0.90)

        # Eliminación denegada
        with self.assertRaises(AccessError):
            med_inv.unlink()

        # Administrador puede eliminar el producto
        med_mgr = med_inv.with_user(self.user_manager)
        med_mgr.unlink()

    def test_05_sale_order_cashier_visibility_and_unlink_restriction(self):
        """Valida regla de ventas accesibles por cajero y restricción de eliminación en confirmadas."""
        sale_order_other = self.env["sale.order"].create({
            "partner_id": self.customer.id,
            "user_id": self.user_inventory.id,
        })

        sale_order_own = self.env["sale.order"].create({
            "partner_id": self.customer.id,
            "user_id": self.user_cashier.id,
        })

        # Cajero solo puede ver ventas asignadas a él o sin asignar
        visible_sales = self.env["sale.order"].with_user(self.user_cashier).search([])
        self.assertIn(sale_order_own.id, visible_sales.ids)
        self.assertNotIn(sale_order_other.id, visible_sales.ids)

        # Confirmar venta propia
        sale_order_own.action_confirm()
        self.assertEqual(sale_order_own.state, "sale")

        # Cajero intenta eliminar orden confirmada -> AccessError
        with self.assertRaises(AccessError):
            sale_order_own.with_user(self.user_cashier).unlink()
