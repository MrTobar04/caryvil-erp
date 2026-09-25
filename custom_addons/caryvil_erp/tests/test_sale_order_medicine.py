# -*- coding: utf-8 -*-

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestSaleOrderMedicine(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ingredient = cls.env["caryvil.active.ingredient"].create(
            {
                "name": "Amoxicilina Test",
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Amoxicilina Test 500mg",
                "detailed_type": "product",
                "sale_ok": True,
                "list_price": 4.50,
                "barcode": "7412345678901",
                "active_ingredient_id": cls.ingredient.id,
                "taxes_id": [Command.clear()],
            }
        )

        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Cliente Venta Test",
                "customer_rank": 1,
                "is_pharmacy_customer": True,
            }
        )

    def _new_order(self):
        return self.env["sale.order"].new(
            {
                "partner_id": self.customer.id,
                "payment_method": "efectivo",
            }
        )

    def _add_test_line(self, order, quantity=1.0, price=4.50):
        order.order_line = [
            Command.create(
                {
                    "product_id": self.product.id,
                    "product_uom": self.product.uom_id.id,
                    "product_uom_qty": quantity,
                    "price_unit": price,
                }
            )
        ]

    def test_01_default_payment_method(self):
        """
        SPEC-9.1.1:
        La forma de pago por defecto debe ser efectivo.
        """
        order = self._new_order()

        self.assertEqual(
            order.payment_method,
            "efectivo",
        )

    def test_02_amount_change_cash(self):
        """
        SPEC-9.1.1:
        El cambio debe ser monto recibido - total.
        """
        order = self._new_order()

        self._add_test_line(
            order,
            quantity=1.0,
            price=4.50,
        )

        order.amount_tendered = 10.00

        order._compute_amount_change()

        self.assertAlmostEqual(
            order.amount_change,
            4.91,
            places=2,
        )

    def test_03_amount_change_zero_for_non_cash(self):
        """
        SPEC-9.1.1:
        Tarjeta y transferencia no generan cambio.
        """
        order = self._new_order()

        self._add_test_line(
            order,
            quantity=1.0,
            price=4.50,
        )

        order.payment_method = "tarjeta_debito_credito"
        order.amount_tendered = 10.00

        order._compute_amount_change()

        self.assertEqual(
            order.amount_change,
            0.0,
        )

    def test_04_reject_insufficient_cash(self):
        """
        SPEC-9.1.1:
        Debe bloquearse el cobro cuando el efectivo recibido es menor que el total.
        """
        order = self._new_order()

        self._add_test_line(
            order,
            quantity=1.0,
            price=4.50,
        )

        order.amount_tendered = 2.00

        with self.assertRaises(UserError):
            order._check_caryvil_payment()

    def test_05_barcode_scan_adds_product(self):
        """
        SPEC-9.1.1:
        Un EAN-13 válido debe agregar automáticamente el producto.
        """
        order = self._new_order()

        order.caryvil_barcode_input = "7412345678901"
        order._onchange_caryvil_barcode_input()

        self.assertFalse(
            order.caryvil_barcode_input
        )

        self.assertEqual(
            len(order.order_line),
            1,
        )

        self.assertEqual(
            order.order_line.product_id,
            self.product,
        )

        self.assertEqual(
            order.order_line.product_uom_qty,
            1.0,
        )

    def test_06_barcode_scan_increments_existing_line(self):
        """
        SPEC-9.1.1:
        Escanear dos veces el mismo producto incrementa la cantidad.
        """
        order = self._new_order()

        order.caryvil_barcode_input = "7412345678901"
        order._onchange_caryvil_barcode_input()

        order.caryvil_barcode_input = "7412345678901"
        order._onchange_caryvil_barcode_input()

        self.assertEqual(
            len(order.order_line),
            1,
        )

        self.assertEqual(
            order.order_line.product_uom_qty,
            2.0,
        )

    def test_07_search_by_active_ingredient(self):
        """
        SPEC-9.1.1:
        El selector de productos debe localizar un medicamento mediante el principio activo.
        """
        results = self.env[
            "product.product"
        ].name_search(
            "Amoxicilina Test",
            operator="ilike",
            limit=10,
        )

        result_ids = [record_id for record_id, _name in results]

        self.assertIn(
            self.product.id,
            result_ids,
        )

    def test_08_stock_validation(self):
        """
        SPEC-9.1.1:
        Una venta que supera el stock disponible debe bloquearse.
        """
        order = self._new_order()

        self._add_test_line(
            order,
            quantity=999.0,
            price=4.50,
        )

        with self.assertRaises(UserError):
            order._check_caryvil_stock_availability()

    def test_09_sale_line_uses_caryvil_iva_13(self):
        """
        SPEC-9.1.1:
        Las ventas de medicamentos deben utilizar únicamente el IVA 13% de Caryvil.
        """
        order = self._new_order()

        order._add_caryvil_scanned_product(self.product)

        tax = self.env.ref(
            "caryvil_erp.tax_caryvil_iva_ventas_13"
        )

        line = order.order_line

        self.assertEqual(
            len(line.tax_id),
            1,
        )

        self.assertEqual(
            line.tax_id.amount,
            13.0,
        )

        self.assertEqual(
            line.tax_id._origin.ids,
            tax.ids,
        )