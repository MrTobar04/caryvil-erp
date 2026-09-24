# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestStockReorderingRules(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env["product.product"].create(
            {
                "name": "Medicamento Test SPEC-7.2.2",
                "type": "product",
            }
        )

        cls.stock_location = cls.env.ref("stock.stock_location_stock")

    def _set_stock(self, quantity):
        self.env["stock.quant"]._update_available_quantity(
            self.product,
            self.stock_location,
            quantity,
        )

        self.product.invalidate_recordset(["qty_available", "virtual_available"])

    def _create_orderpoint(
        self,
        min_qty=10.0,
        max_qty=30.0,
        qty_multiple=1.0,
    ):
        return self.env["stock.warehouse.orderpoint"].create(
            {
                "name": "Regla Test SPEC-7.2.2",
                "product_id": self.product.id,
                "location_id": self.stock_location.id,
                "product_min_qty": min_qty,
                "product_max_qty": max_qty,
                "qty_multiple": qty_multiple,
            }
        )

    def test_suggested_quantity_without_multiple(self):
        self._set_stock(6.0)

        orderpoint = self._create_orderpoint(
            min_qty=10.0,
            max_qty=30.0,
            qty_multiple=1.0,
        )

        self.assertEqual(
            orderpoint.suggested_replenishment_qty,
            24.0,
            "Con stock 6, mínimo 10 y máximo 30, debe sugerir 24 unidades.",
        )

    def test_suggested_quantity_with_multiple(self):
        self._set_stock(6.0)

        orderpoint = self._create_orderpoint(
            min_qty=10.0,
            max_qty=30.0,
            qty_multiple=5.0,
        )

        self.assertEqual(
            orderpoint.suggested_replenishment_qty,
            25.0,
            "La cantidad 24 debe redondearse al siguiente múltiplo de 5.",
        )

    def test_no_replenishment_when_stock_above_minimum(self):
        self._set_stock(22.0)

        orderpoint = self._create_orderpoint(
            min_qty=15.0,
            max_qty=30.0,
            qty_multiple=5.0,
        )

        self.assertEqual(
            orderpoint.suggested_replenishment_qty,
            0.0,
            "Si el stock está por encima del mínimo, no debe sugerir compra.",
        )
