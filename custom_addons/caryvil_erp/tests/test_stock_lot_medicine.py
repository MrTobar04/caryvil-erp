# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields


class TestStockLotMedicine(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env["product.product"].create({
            "name": "Medicamento Test SPEC-7.2.1",
            "type": "product",
            "tracking": "lot",
        })

        cls.customer = cls.env["res.partner"].create({
            "name": "Cliente Test SPEC-7.2.1",
        })

        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")

    def _create_lot(self, expiration_date):
        return self.env["stock.lot"].create({
            "name": "LOT-TEST-%s" % expiration_date,
            "product_id": self.product.id,
            "company_id": self.env.company.id,
            "expiration_date": expiration_date,
        })

    def _add_stock(self, lot, quantity=10):
        self.env["stock.quant"]._update_available_quantity(
            self.product,
            self.stock_location,
            quantity,
            lot_id=lot,
        )

    def _create_delivery(self, lot, quantity=1):
        picking_type = self.env["stock.picking.type"].search([
            ("code", "=", "outgoing"),
            ("warehouse_id.company_id", "=", self.env.company.id),
        ], limit=1)

        picking = self.env["stock.picking"].create({
            "picking_type_id": picking_type.id,
            "location_id": self.stock_location.id,
            "location_dest_id": self.customer_location.id,
            "partner_id": self.customer.id,
        })

        move = self.env["stock.move"].create({
            "name": self.product.name,
            "product_id": self.product.id,
            "product_uom_qty": quantity,
            "product_uom": self.product.uom_id.id,
            "picking_id": picking.id,
            "location_id": self.stock_location.id,
            "location_dest_id": self.customer_location.id,
        })

        picking.action_confirm()
        picking.action_assign()

        move_line = picking.move_line_ids.filtered(
            lambda line: line.product_id == self.product
        )[:1]

        move_line.quantity = quantity
        move_line.lot_id = lot

        return picking

    def test_expired_lot_is_marked_as_expired(self):
        lot = self._create_lot(
            fields.Datetime.subtract(
                fields.Datetime.now(),
                days=1,
            )
        )

        self.assertTrue(
            lot.is_expired,
            "Un lote con fecha de vencimiento pasada debe marcarse como vencido.",
        )

    def test_expired_lot_cannot_be_dispensed(self):
        lot = self._create_lot(
            fields.Datetime.subtract(
                fields.Datetime.now(),
                days=1,
            )
        )

        self._add_stock(lot)

        picking = self._create_delivery(lot)

        with self.assertRaisesRegex(
            ValidationError,
            "No es posible dispensar el lote .* porque se encuentra vencido.",
        ):
            picking.button_validate()

    def test_valid_lot_can_be_dispensed(self):
        lot = self._create_lot(
            fields.Datetime.add(
                fields.Datetime.now(),
                days=30,
            )
        )

        self._add_stock(lot)

        picking = self._create_delivery(lot)

        picking.button_validate()

        self.assertEqual(
            picking.state,
            "done",
            "Un lote vigente debe poder dispensarse correctamente.",
        )