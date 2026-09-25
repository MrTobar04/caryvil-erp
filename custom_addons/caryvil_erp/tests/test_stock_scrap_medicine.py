# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError
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
        if not cls.warehouse:
            cls.warehouse = cls.env["stock.warehouse"].search([], limit=1)

        cls.stock_location = cls.warehouse.lot_stock_id
        cls.scrap_location = cls.env.ref("caryvil_erp.stock_location_scrap_caryvil")

        cls.manager_user = cls.env.ref("caryvil_erp.user_admin_demo")
        cls.manager_user.write({
            "company_id": cls.company.id,
            "company_ids": [(4, cls.company.id)],
        })
        cls.inventory_user = cls.env.ref("caryvil_erp.user_compras_demo")
        cls.inventory_user.write({
            "company_id": cls.company.id,
            "company_ids": [(4, cls.company.id)],
        })
        cls.cashier_user = cls.env.ref("caryvil_erp.user_cajero_demo")
        cls.cashier_user.write({
            "company_id": cls.company.id,
            "company_ids": [(4, cls.company.id)],
        })

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
            .with_user(self.manager_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 1.0,
                    "location_id": self.stock_location.id,
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
        self.assertEqual(scrap.authorized_by_id, self.manager_user)
        self.assertTrue(scrap.authorization_date)

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
            .with_user(self.manager_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 1.0,
                    "location_id": self.stock_location.id,
                    "scrap_reason": "medicamento_vencido",
                }
            )
        )

        with self.assertRaises(ValidationError):
            scrap.action_validate()

    def test_scrap_quantity_cannot_exceed_physical_stock(self):
        scrap = (
            self.env["stock.scrap"]
            .with_user(self.manager_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 100.0,
                    "location_id": self.stock_location.id,
                    "lot_id": self.lot.id,
                    "scrap_reason": "medicamento_vencido",
                }
            )
        )

        with self.assertRaises(ValidationError):
            scrap.action_validate()

    def test_scrap_quantity_must_be_positive(self):
        scrap = (
            self.env["stock.scrap"]
            .with_user(self.manager_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 0.0,
                    "location_id": self.stock_location.id,
                    "lot_id": self.lot.id,
                    "scrap_reason": "medicamento_vencido",
                }
            )
        )

        with self.assertRaises(ValidationError):
            scrap.action_validate()

    def test_scrap_permission_restricted_to_manager(self):
        scrap = (
            self.env["stock.scrap"]
            .with_user(self.inventory_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 1.0,
                    "location_id": self.stock_location.id,
                    "lot_id": self.lot.id,
                    "scrap_reason": "rotura_frasco_ampolla",
                }
            )
        )

        with self.assertRaises(UserError):
            scrap.with_user(self.inventory_user).action_validate()

    def test_scrap_direct_do_scrap_enforces_security_and_lot(self):
        scrap = (
            self.env["stock.scrap"]
            .with_user(self.inventory_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 1.0,
                    "location_id": self.stock_location.id,
                    "lot_id": self.lot.id,
                    "scrap_reason": "otro",
                }
            )
        )

        with self.assertRaises(UserError):
            scrap.with_user(self.inventory_user).do_scrap()

        scrap_no_lot = (
            self.env["stock.scrap"]
            .with_user(self.manager_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 1.0,
                    "location_id": self.stock_location.id,
                    "scrap_reason": "otro",
                }
            )
        )

        with self.assertRaises(ValidationError):
            scrap_no_lot.with_user(self.manager_user).do_scrap()

    def test_scrap_cost_calculation_with_uom_conversion(self):
        uom_unit = self.env.ref("uom.product_uom_unit")
        uom_dozen = self.env.ref("uom.product_uom_dozen")

        product_dozen = (
            self.env["product.product"]
            .with_company(self.company)
            .create(
                {
                    "name": "Medicamento en Docenas",
                    "detailed_type": "product",
                    "tracking": "none",
                    "standard_price": 120.0,
                    "uom_id": uom_dozen.id,
                    "uom_po_id": uom_dozen.id,
                    "company_id": self.company.id,
                }
            )
        )

        self.env["stock.quant"].with_company(self.company)._update_available_quantity(
            product_dozen,
            self.stock_location,
            10.0,
        )

        scrap = (
            self.env["stock.scrap"]
            .with_user(self.manager_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": product_dozen.id,
                    "product_uom_id": uom_unit.id,
                    "scrap_qty": 2.0,
                    "location_id": self.stock_location.id,
                    "scrap_reason": "empaque_deteriorado_humedad",
                }
            )
        )

        self.assertAlmostEqual(scrap.scrap_unit_cost, 10.0, places=2)
        self.assertAlmostEqual(scrap.scrap_total_loss, 20.0, places=2)

    def test_scrap_post_validation_immutability(self):
        scrap = (
            self.env["stock.scrap"]
            .with_user(self.manager_user)
            .with_company(self.company)
            .create(
                {
                    "product_id": self.product.id,
                    "product_uom_id": self.product.uom_id.id,
                    "scrap_qty": 1.0,
                    "location_id": self.stock_location.id,
                    "lot_id": self.lot.id,
                    "scrap_reason": "medicamento_vencido",
                    "justification_notes": "Texto inicial",
                }
            )
        )
        scrap.action_validate()
        self.assertEqual(scrap.state, "done")

        with self.assertRaises(UserError):
            scrap.write({"scrap_reason": "otro"})

        with self.assertRaises(UserError):
            scrap.write({"justification_notes": "Texto alterado"})

        with self.assertRaises(UserError):
            scrap.unlink()
