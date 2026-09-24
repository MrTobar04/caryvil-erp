# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestStockInventoryAdjustment(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env["product.product"].create(
            {
                "name": "Medicamento Test SPEC-7.3.1",
                "type": "product",
                "tracking": "none",
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

    def _create_adjustment(self, counted_quantity, reason=None):
        quant = self.env["stock.quant"].search(
            [
                ("product_id", "=", self.product.id),
                ("location_id", "=", self.stock_location.id),
            ],
            limit=1,
        )

        quant.inventory_quantity = counted_quantity
        quant.inventory_quantity_set = True
        quant.adjustment_reason = reason

        return quant

    def test_adjustment_requires_reason(self):
        self._set_stock(10.0)

        quant = self._create_adjustment(12.0)

        with self.assertRaises(ValidationError):
            quant.action_apply_inventory()

    def test_adjustment_updates_stock_with_reason(self):
        self._set_stock(10.0)

        quant = self._create_adjustment(
            12.0,
            "conteo_ciclico_periodico",
        )

        quant.action_apply_inventory()

        self.assertEqual(
            quant.quantity,
            12.0,
            "El stock debe quedar en 12 unidades después del ajuste.",
        )

        self.assertEqual(
            quant.validated_by_user_id,
            self.env.user,
            "Debe registrarse el usuario que valida el ajuste.",
        )

    def test_adjustment_without_difference_does_not_require_reason(self):
        self._set_stock(10.0)

        quant = self._create_adjustment(10.0)

        quant.action_apply_inventory()

        self.assertEqual(
            quant.quantity,
            10.0,
            "Si no existe diferencia, el stock debe permanecer en 10 unidades.",
        )

    def test_adjustment_requires_lot_for_tracked_product(self):
        product = self.env["product.product"].create(
            {
                "name": "Medicamento Test Lote SPEC-7.3.1",
                "type": "product",
                "tracking": "lot",
            }
        )

        stock_location = self.env.ref("stock.stock_location_stock")

        self.env["stock.quant"]._update_available_quantity(
            product,
            stock_location,
            10.0,
        )

        quant = self.env["stock.quant"].search(
            [
                ("product_id", "=", product.id),
                ("location_id", "=", stock_location.id),
            ],
            limit=1,
        )

        quant.inventory_quantity = 12.0
        quant.inventory_quantity_set = True
        quant.adjustment_reason = "conteo_ciclico_periodico"

        with self.assertRaisesRegex(
            ValidationError,
            "Debe especificar el lote para el producto",
        ):
            quant.action_apply_inventory()
