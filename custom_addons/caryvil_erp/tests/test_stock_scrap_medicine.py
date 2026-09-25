# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestStockScrapMedicine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env.ref("caryvil_erp.company_farmacia_caryvil")
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)],
            limit=1,
        )
        cls.stock_location = cls.warehouse.lot_stock_id

        cls.scrap_location = cls.env.ref("caryvil_erp.stock_location_scrap_caryvil")

        cls.product = (
            cls.env["product.product"]
            .with_company(cls.company)
            .create(
                {
                    "name": "Medicamento Test Merma",
                    "detailed_type": "product",
                    "tracking": "lot",
                    "standard_price": 3.50,
                    "company_id": cls.company.id,
                }
            )
        )

        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "CARYVIL-TEST-001",
                "product_id": cls.product.id,
                "company_id": cls.company.id,
            }
        )

        cls.env["stock.quant"].with_company(cls.company)._update_available_quantity(
            cls.product,
            cls.stock_location,
            8.0,
            lot_id=cls.lot,
        )

    def test_scrap_medicine_moves_lot_to_caryvil_waste(self):
        scrap = (
            self.env["stock.scrap"]
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 1.0,
                    "location_id": self.stock_location.id,
                    "scrap_location_id": self.scrap_location.id,
                    "lot_id": self.lot.id,
                    "scrap_reason": "medicamento_vencido",
                    "justification_notes": "Prueba automatizada SPEC-7.3.2",
                }
            )
        )

        self.assertEqual(scrap.scrap_unit_cost, 3.50)
        self.assertEqual(scrap.scrap_total_loss, 3.50)
        self.assertEqual(scrap.scrap_location_id, self.scrap_location)

        scrap.action_validate()

        self.assertEqual(scrap.state, "done")
        self.assertEqual(scrap.authorized_by_id, self.env.user)

        available_qty = (
            self.env["stock.quant"]
            .with_company(self.company)
            ._get_available_quantity(
                self.product,
                self.stock_location,
                lot_id=self.lot,
                strict=True,
            )
        )

        self.assertEqual(available_qty, 7.0)

        move = self.env["stock.move"].search(
            [("scrap_id", "=", scrap.id)],
            limit=1,
        )

        self.assertTrue(move)
        self.assertEqual(move.location_id, self.stock_location)
        self.assertEqual(move.location_dest_id, self.scrap_location)
        self.assertEqual(move.state, "done")

    def test_tracked_medicine_requires_lot(self):
        scrap = (
            self.env["stock.scrap"]
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 1.0,
                    "location_id": self.stock_location.id,
                    "scrap_location_id": self.scrap_location.id,
                    "scrap_reason": "medicamento_vencido",
                }
            )
        )

        with self.assertRaises(ValidationError):
            scrap.action_validate()
