# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError
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

        cls.manager_user = cls.env.user
        cls.manager_group = cls.env.ref("caryvil_erp.group_caryvil_manager")
        if cls.manager_group not in cls.manager_user.groups_id:
            cls.manager_user.write({"groups_id": [(4, cls.manager_group.id)]})

        cls.inventory_group = cls.env.ref("caryvil_erp.group_caryvil_inventory_purchases")
        cls.operator_user = cls.env["res.users"].create(
            {
                "name": "Operador Inventario Test",
                "login": "operador_test_731@caryvil.com",
                "email": "operador_test_731@caryvil.com",
                "groups_id": [(6, 0, [cls.env.ref("base.group_user").id, cls.inventory_group.id])],
            }
        )

    def _set_stock(self, quantity):
        self.env["stock.quant"]._update_available_quantity(
            self.product,
            self.stock_location,
            quantity,
        )

        self.product.invalidate_recordset(["qty_available", "virtual_available"])

    def _create_adjustment(self, counted_quantity, reason=None, notes=None):
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
        quant.adjustment_notes = notes

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
            "Ajuste por conteo mensual",
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

    def test_adjustment_shortage_updates_stock(self):
        self._set_stock(10.0)

        quant = self._create_adjustment(
            7.0,
            "error_conteo_previo",
            "Faltante detectado en revisión física",
        )

        quant.action_apply_inventory()

        self.assertEqual(
            quant.quantity,
            7.0,
            "El stock debe quedar en 7 unidades tras conciliar faltante.",
        )

        self.assertEqual(
            quant.validated_by_user_id,
            self.env.user,
            "Debe registrarse el usuario administrador que valida la merma/faltante.",
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

    def test_adjustment_tracked_product_with_lot_success(self):
        product = self.env["product.product"].create(
            {
                "name": "Medicamento Con Lote Válido SPEC-7.3.1",
                "type": "product",
                "tracking": "lot",
            }
        )

        lot = self.env["stock.lot"].create(
            {
                "name": "LOT-731-VALID-01",
                "product_id": product.id,
                "company_id": self.env.company.id,
            }
        )

        stock_location = self.env.ref("stock.stock_location_stock")

        self.env["stock.quant"]._update_available_quantity(
            product,
            stock_location,
            5.0,
            lot_id=lot,
        )

        quant = self.env["stock.quant"].search(
            [
                ("product_id", "=", product.id),
                ("location_id", "=", stock_location.id),
                ("lot_id", "=", lot.id),
            ],
            limit=1,
        )

        quant.inventory_quantity = 8.0
        quant.inventory_quantity_set = True
        quant.adjustment_reason = "conteo_ciclico_periodico"

        quant.action_apply_inventory()

        self.assertEqual(
            quant.quantity,
            8.0,
            "El stock del lote debe incrementarse a 8 unidades.",
        )
        self.assertEqual(
            quant.lot_id,
            lot,
            "El lote debe mantenerse asignado en el quant ajustado.",
        )

    def test_adjustment_negative_quantity_blocked(self):
        self._set_stock(10.0)

        quant = self.env["stock.quant"].search(
            [
                ("product_id", "=", self.product.id),
                ("location_id", "=", self.stock_location.id),
            ],
            limit=1,
        )

        with self.assertRaises(ValidationError):
            quant.write({"inventory_quantity": -5.0})

    def test_adjustment_records_operator_counted_by(self):
        self._set_stock(10.0)

        quant = self.env["stock.quant"].search(
            [
                ("product_id", "=", self.product.id),
                ("location_id", "=", self.stock_location.id),
            ],
            limit=1,
        )

        quant.with_user(self.operator_user).write({"inventory_quantity": 14.0})

        self.assertEqual(
            quant.counted_by_user_id,
            self.operator_user,
            "Debe capturarse automáticamente el usuario operador que ingresó el conteo.",
        )

    def test_adjustment_non_manager_blocked_from_applying(self):
        self._set_stock(10.0)

        quant = self._create_adjustment(13.0, reason="conteo_ciclico_periodico")

        with self.assertRaisesRegex(
            UserError,
            "Solo el Administrador / Propietario puede aplicar ajustes de inventario",
        ):
            quant.with_user(self.operator_user).action_apply_inventory()

    def test_adjustment_propagates_reason_to_stock_move(self):
        self._set_stock(10.0)

        quant = self._create_adjustment(
            15.0,
            reason="conteo_ciclico_periodico",
            notes="Auditoría de pasillo farmacéutico",
        )

        quant.action_apply_inventory()

        move = self.env["stock.move"].search(
            [("product_id", "=", self.product.id)],
            order="id desc",
            limit=1,
        )

        self.assertTrue(move, "Debe existir un movimiento de stock generado por el ajuste.")
        self.assertIn(
            "Conteo Cíclico Periódico",
            move.origin or "",
            "El origen del movimiento de stock debe incluir el motivo del ajuste.",
        )
        self.assertIn(
            "Auditoría de pasillo farmacéutico",
            move.description_picking or "",
            "La descripción del movimiento debe preservar las notas de justificación.",
        )
