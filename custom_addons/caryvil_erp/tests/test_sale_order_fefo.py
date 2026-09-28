# -*- coding: utf-8 -*-

from odoo import Command, fields
from odoo.tests.common import TransactionCase


class TestSaleOrderFEFO(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env.ref("base.main_company")

        cls.tax = cls.env.ref("caryvil_erp.tax_caryvil_iva_ventas_13")

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Cliente FEFO Test",
                "customer_rank": 1,
                "is_pharmacy_customer": True,
            }
        )

        cls.ingredient = cls.env["caryvil.active.ingredient"].create(
            {
                "name": "Principio Activo FEFO Test",
            }
        )

        cls.category = cls.env.ref("caryvil_erp.cat_analgesicos")

        cls.fefo = cls.env.ref("product_expiry.removal_fefo")

        cls.product = cls.env["product.product"].create(
            {
                "name": "Medicamento FEFO Test",
                "detailed_type": "product",
                "sale_ok": True,
                "list_price": 10.00,
                "tracking": "lot",
                "categ_id": cls.category.id,
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

    def _create_lot(self, name, expiration_date):
        return self.env["stock.lot"].create(
            {
                "name": name,
                "product_id": self.product.id,
                "company_id": self.company.id,
                "expiration_date": expiration_date,
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

    def _get_done_lot_quantities(self, order):
        quantities = {}

        move_lines = order.picking_ids.mapped("move_line_ids").filtered(
            lambda line: (line.state == "done" and line.product_id == self.product and line.lot_id)
        )

        for move_line in move_lines:
            quantities[move_line.lot_id.name] = quantities.get(move_line.lot_id.name, 0.0) + move_line.quantity

        return quantities

    def test_01_fefo_uses_earliest_expiring_lot(self):
        """
        SPEC-9.3.2:
        Debe seleccionarse automáticamente el lote vigente con fecha de vencimiento más próxima.
        """

        self.assertEqual(
            self.category.removal_strategy_id,
            self.fefo,
        )

        lot_a = self._create_lot(
            "LOT-FEFO-A",
            fields.Datetime.add(
                fields.Datetime.now(),
                days=35,
            ),
        )

        lot_b = self._create_lot(
            "LOT-FEFO-B",
            fields.Datetime.add(
                fields.Datetime.now(),
                days=200,
            ),
        )

        self._add_stock(lot_a, 10.0)
        self._add_stock(lot_b, 15.0)

        order = self._create_order(4.0)
        order.action_confirm_and_invoice()

        quantities = self._get_done_lot_quantities(order)

        self.assertEqual(
            quantities,
            {
                lot_a.name: 4.0,
            },
        )

    def test_02_fefo_splits_between_lots(self):
        """
        SPEC-9.3.2:
        Si el lote más próximo a vencer no tiene suficiente stock, la cantidad restante debe tomarse del siguiente lote.
        """

        lot_a = self._create_lot(
            "LOT-FEFO-SPLIT-A",
            fields.Datetime.add(
                fields.Datetime.now(),
                days=35,
            ),
        )

        lot_b = self._create_lot(
            "LOT-FEFO-SPLIT-B",
            fields.Datetime.add(
                fields.Datetime.now(),
                days=200,
            ),
        )

        self._add_stock(lot_a, 3.0)
        self._add_stock(lot_b, 15.0)

        order = self._create_order(5.0)
        order.action_confirm_and_invoice()

        quantities = self._get_done_lot_quantities(order)

        self.assertEqual(
            quantities,
            {
                lot_a.name: 3.0,
                lot_b.name: 2.0,
            },
        )

    def test_03_fefo_ignores_expired_lot(self):
        """
        SPEC-9.3.2:
        Un lote vencido debe ser excluido completamente aunque tenga existencias físicas disponibles.
        """

        expired_lot = self._create_lot(
            "LOT-FEFO-EXPIRED",
            fields.Datetime.subtract(
                fields.Datetime.now(),
                days=5,
            ),
        )

        valid_lot = self._create_lot(
            "LOT-FEFO-VALID",
            fields.Datetime.add(
                fields.Datetime.now(),
                days=365,
            ),
        )

        self._add_stock(expired_lot, 10.0)
        self._add_stock(valid_lot, 10.0)

        order = self._create_order(2.0)
        order.action_confirm_and_invoice()

        quantities = self._get_done_lot_quantities(order)

        self.assertEqual(
            quantities,
            {
                valid_lot.name: 2.0,
            },
        )

        self.assertNotIn(
            expired_lot.name,
            quantities,
        )
