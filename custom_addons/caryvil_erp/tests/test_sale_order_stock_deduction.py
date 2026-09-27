# -*- coding: utf-8 -*-

from odoo import Command, fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestSaleOrderStockDeduction(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env.ref("caryvil_erp.company_farmacia_caryvil")

        cls.tax = cls.env.ref("caryvil_erp.tax_caryvil_iva_ventas_13")

        cls.sales_account = cls.env.ref("caryvil_erp.account_caryvil_ventas_medicamentos")

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Cliente Stock Test",
                "customer_rank": 1,
                "is_pharmacy_customer": True,
            }
        )

        cls.ingredient = cls.env["caryvil.active.ingredient"].create(
            {
                "name": "Principio Activo Stock Test",
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Medicamento Stock Test",
                "detailed_type": "product",
                "sale_ok": True,
                "list_price": 10.00,
                "tracking": "lot",
                "active_ingredient_id": cls.ingredient.id,
                "taxes_id": [
                    Command.set([cls.tax.id]),
                ],
            }
        )

        cls.warehouse = cls.env["stock.warehouse"].search(
            [
                (
                    "company_id",
                    "=",
                    cls.company.id,
                )
            ],
            limit=1,
        )

        if not cls.warehouse:
            raise AssertionError("La compañía Caryvil debe tener un almacén configurado.")

        cls.stock_location = cls.warehouse.lot_stock_id
        cls.customer_location = cls.env.ref("stock.stock_location_customers")

    def _create_lot(self, name):
        return self.env["stock.lot"].create(
            {
                "name": name,
                "product_id": self.product.id,
                "company_id": self.company.id,
                "expiration_date": fields.Datetime.add(
                    fields.Datetime.now(),
                    days=90,
                ),
            }
        )

    def _add_stock(self, lot, quantity):
        self.env["stock.quant"]._update_available_quantity(
            self.product,
            self.stock_location,
            quantity,
            lot_id=lot,
        )

    def _create_order(self, quantity):
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom": self.product.uom_id.id,
                            "product_uom_qty": quantity,
                            "price_unit": 10.00,
                        }
                    ),
                ],
                "payment_method": "efectivo",
                "amount_tendered": 1000.00,
            }
        )

    def _get_available_stock(self):
        return self.env["stock.quant"]._get_available_quantity(
            self.product,
            self.stock_location,
            strict=False,
        )

    def _get_lot_quantity(self, lot):
        quant = self.env["stock.quant"].search(
            [
                ("product_id", "=", self.product.id),
                ("location_id", "=", self.stock_location.id),
                ("lot_id", "=", lot.id),
            ],
            limit=1,
        )

        return quant.quantity if quant else 0.0

    def test_01_sale_deducts_stock(self):
        """
        SPEC-9.3.1:
        Una venta completada debe descontar inmediatamente las unidades físicas del inventario.
        """

        lot = self._create_lot("LOT-STOCK-10")
        self._add_stock(lot, 10.0)

        self.assertAlmostEqual(
            self._get_available_stock(),
            10.0,
            places=2,
        )

        order = self._create_order(4.0)

        action = order.action_confirm_and_invoice()

        self.assertEqual(
            order.state,
            "sale",
        )

        self.assertAlmostEqual(
            self._get_available_stock(),
            6.0,
            places=2,
        )

        invoice = self.env["account.move"].search(
            [
                (
                    "invoice_origin",
                    "=",
                    order.name,
                ),
            ],
            order="id desc",
            limit=1,
        )

        self.assertTrue(
            invoice,
            "La venta debe generar una factura.",
        )

        self.assertEqual(
            invoice.state,
            "posted",
        )

        self.assertTrue(
            action,
            "El flujo debe devolver una acción para la factura/ticket.",
        )

    def test_02_insufficient_stock_rolls_back(self):
        """
        SPEC-9.3.1:
        No debe permitirse una venta que genere saldo negativo y el stock existente debe permanecer intacto.
        """

        lot = self._create_lot("LOT-STOCK-3")
        self._add_stock(lot, 3.0)

        order = self._create_order(4.0)

        with self.assertRaises(UserError):
            order.action_confirm_and_invoice()

        self.assertEqual(
            order.state,
            "draft",
        )

        self.assertAlmostEqual(
            self._get_available_stock(),
            3.0,
            places=2,
        )

        invoice = self.env["account.move"].search(
            [
                (
                    "invoice_origin",
                    "=",
                    order.name,
                ),
            ],
            limit=1,
        )

        self.assertFalse(
            invoice,
            "La venta rechazada no debe generar una factura.",
        )

    def test_03_sale_deducts_stock_from_lot(self):
        """
        SPEC-9.3.1:
        El balance del lote efectivamente dispensado debe disminuir en la misma cantidad despachada.
        """

        lot = self._create_lot("LOT-STOCK-50")
        self._add_stock(lot, 50.0)

        order = self._create_order(10.0)

        order.action_confirm_and_invoice()

        self.assertAlmostEqual(
            self._get_lot_quantity(lot),
            40.0,
            places=2,
        )
