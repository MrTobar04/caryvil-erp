# -*- coding: utf-8 -*-

from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestStockReorderingRules(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.secondary_location = cls.env["stock.location"].create(
            {
                "name": "Bodega Secundaria Test SPEC-7.2.2",
                "usage": "internal",
                "location_id": cls.env.ref("stock.stock_location_locations").id,
            }
        )

        # Proveedor farmacéutico Vijosa
        cls.vendor_vijosa = cls.env["res.partner"].create(
            {
                "name": "Laboratorios Vijosa S.A. de C.V. Test",
                "is_company": True,
                "is_pharmacy_vendor": True,
                "vendor_type": "laboratorio",
                "nit": "0614-123456-001-2",
                "nrc": "12345-6",
                "supplier_rank": 1,
            }
        )

        # Usuarios de prueba con diferentes roles
        cls.user_inventory = cls.env["res.users"].create(
            {
                "name": "Encargado Inventario Test SPEC-7.2.2",
                "login": "inv_test_spec722@caryvil.com",
                "email": "inv_test_spec722@caryvil.com",
                "groups_id": [
                    (4, cls.env.ref("caryvil_erp.group_caryvil_inventory_purchases").id)
                ],
            }
        )

        cls.user_cashier = cls.env["res.users"].create(
            {
                "name": "Cajero Test SPEC-7.2.2",
                "login": "cajero_test_spec722@caryvil.com",
                "email": "cajero_test_spec722@caryvil.com",
                "groups_id": [
                    (4, cls.env.ref("caryvil_erp.group_caryvil_cashier").id)
                ],
            }
        )

        # Medicamento Loratadina 10mg (Escenario 1)
        cls.product_loratadina = cls.env["product.product"].create(
            {
                "name": "Loratadina 10mg Test",
                "type": "product",
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": cls.vendor_vijosa.id,
                            "price": 2.50,
                        },
                    )
                ],
            }
        )

    def _set_stock(self, product, location, quantity):
        self.env["stock.quant"]._update_available_quantity(
            product,
            location,
            quantity,
        )
        product.invalidate_recordset(["qty_available", "virtual_available"])

    def _create_orderpoint(
        self,
        product,
        min_qty=10.0,
        max_qty=30.0,
        qty_multiple=1.0,
        location=None,
    ):
        loc = location or self.stock_location
        return (
            self.env["stock.warehouse.orderpoint"]
            .with_user(self.user_inventory)
            .create(
                {
                    "name": f"Regla {product.name}",
                    "product_id": product.id,
                    "location_id": loc.id,
                    "product_min_qty": min_qty,
                    "product_max_qty": max_qty,
                    "qty_multiple": qty_multiple,
                }
            )
        )

    def test_suggested_quantity_without_multiple(self):
        """Escenario 1 base: Min=10, Max=30, Múltiplo=1, Stock=6 -> Sugerido=24."""
        self._set_stock(self.product_loratadina, self.stock_location, 6.0)

        orderpoint = self._create_orderpoint(
            self.product_loratadina,
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
        """Escenario 1 Criterios de Aceptación: Loratadina 10mg, Min=10, Max=30, Mult=5, Stock=6 -> Sugerido=25."""
        self._set_stock(self.product_loratadina, self.stock_location, 6.0)

        orderpoint = self._create_orderpoint(
            self.product_loratadina,
            min_qty=10.0,
            max_qty=30.0,
            qty_multiple=5.0,
        )

        self.assertEqual(
            orderpoint.suggested_replenishment_qty,
            25.0,
            "Déficit 24 debe redondearse al siguiente múltiplo de 5 (25 cajas).",
        )

    def test_no_replenishment_when_stock_above_minimum(self):
        """Escenario 3 Criterios de Aceptación: Stock=22, Mínimo=15 -> Sugerido=0."""
        self._set_stock(self.product_loratadina, self.stock_location, 22.0)

        orderpoint = self._create_orderpoint(
            self.product_loratadina,
            min_qty=15.0,
            max_qty=30.0,
            qty_multiple=5.0,
        )

        self.assertEqual(
            orderpoint.suggested_replenishment_qty,
            0.0,
            "Si el stock actual está por encima del mínimo, no debe sugerir reabastecimiento.",
        )

    def test_calculate_reorder_grouped_by_vendor(self):
        """Escenario 2 Criterios de Aceptación: 3 medicamentos de Vijosa bajo el mínimo generan un único RFQ agrupado."""
        med1 = self.product_loratadina
        med2 = self.env["product.product"].create(
            {
                "name": "Amoxicilina 500mg Test Vijosa",
                "type": "product",
                "seller_ids": [(0, 0, {"partner_id": self.vendor_vijosa.id, "price": 4.00})],
            }
        )
        med3 = self.env["product.product"].create(
            {
                "name": "Ibuprofeno 400mg Test Vijosa",
                "type": "product",
                "seller_ids": [(0, 0, {"partner_id": self.vendor_vijosa.id, "price": 3.00})],
            }
        )

        self._set_stock(med1, self.stock_location, 6.0)  # Min 10, Max 30, Mult 5 -> Sug 25
        self._set_stock(med2, self.stock_location, 2.0)  # Min 10, Max 20, Mult 1 -> Sug 18
        self._set_stock(med3, self.stock_location, 4.0)  # Min 15, Max 30, Mult 5 -> Sug 30 (30-4=26 -> 30)

        op1 = self._create_orderpoint(med1, min_qty=10.0, max_qty=30.0, qty_multiple=5.0)
        op2 = self._create_orderpoint(med2, min_qty=10.0, max_qty=20.0, qty_multiple=1.0)
        op3 = self._create_orderpoint(med3, min_qty=15.0, max_qty=30.0, qty_multiple=5.0)

        orderpoints = op1 | op2 | op3

        # Ejecutar acción de cálculo con usuario de compras
        action = orderpoints.with_user(self.user_inventory).action_calculate_replenishment_caryvil()
        self.assertIsNotNone(action)

        # Buscar la Solicitud de Presupuesto generada
        po = self.env["purchase.order"].search(
            [
                ("partner_id", "=", self.vendor_vijosa.id),
                ("origin", "=", "Reabastecimiento Caryvil"),
                ("state", "=", "draft"),
            ]
        )

        self.assertEqual(len(po), 1, "Debe generarse una única Solicitud de Presupuesto agrupada para Vijosa.")
        self.assertEqual(len(po.order_line), 3, "El RFQ debe contener exactamente 3 líneas de medicamentos.")

        line_med1 = po.order_line.filtered(lambda l: l.product_id == med1)
        line_med2 = po.order_line.filtered(lambda l: l.product_id == med2)
        line_med3 = po.order_line.filtered(lambda l: l.product_id == med3)

        self.assertEqual(line_med1.product_qty, 25.0, "MED1 debe tener cantidad sugerida de 25 cajas.")
        self.assertEqual(line_med2.product_qty, 18.0, "MED2 debe tener cantidad sugerida de 18 cajas.")
        self.assertEqual(line_med3.product_qty, 30.0, "MED3 debe tener cantidad sugerida de 30 cajas.")

    def test_uom_purchase_conversion(self):
        """Verificar respeto de la Unidad de Medida de Compra (uom_po_id)."""
        uom_unit = self.env.ref("uom.product_uom_unit")
        # Crear o buscar unidad de medida bulto / caja de 10 unidades
        uom_category = uom_unit.category_id
        uom_box_10 = self.env["uom.uom"].create(
            {
                "name": "Caja x 10 Test",
                "category_id": uom_category.id,
                "uom_type": "bigger",
                "factor_inv": 10.0,
                "rounding": 1.0,
            }
        )

        product_with_po_uom = self.env["product.product"].create(
            {
                "name": "Fármaco con UoM Compra Distinta",
                "type": "product",
                "uom_id": uom_unit.id,
                "uom_po_id": uom_box_10.id,
                "seller_ids": [(0, 0, {"partner_id": self.vendor_vijosa.id, "price": 20.00})],
            }
        )

        self._set_stock(product_with_po_uom, self.stock_location, 10.0)
        # Min = 20 Unidades, Max = 50 Unidades, Múltiplo = 10 -> Déficit = 40 unidades
        op = self._create_orderpoint(
            product_with_po_uom,
            min_qty=20.0,
            max_qty=50.0,
            qty_multiple=10.0,
        )

        self.assertEqual(op.suggested_replenishment_qty, 40.0)

        # Al calcular el reorden de compra, 40 unidades deben convertirse a 4 Cajas x 10
        op.with_user(self.user_inventory).action_calculate_replenishment_caryvil()

        po = self.env["purchase.order"].search(
            [
                ("partner_id", "=", self.vendor_vijosa.id),
                ("origin", "=", "Reabastecimiento Caryvil"),
            ],
            order="id desc",
            limit=1,
        )
        line = po.order_line.filtered(lambda l: l.product_id == product_with_po_uom)
        self.assertEqual(line.product_qty, 4.0, "40 unidades de stock deben convertirse a 4 cajas de compra.")
        self.assertEqual(line.product_uom, uom_box_10, "La UoM de la línea debe ser la de compra (uom_po_id).")

    def test_validation_constraints(self):
        """Prueba de restricciones de negocio: min <= max, min >= 0, mult > 0."""
        # Máximo menor a mínimo
        with self.assertRaises(ValidationError):
            self._create_orderpoint(
                self.product_loratadina,
                min_qty=50.0,
                max_qty=20.0,
                qty_multiple=5.0,
            )

        # Mínimo negativo
        with self.assertRaises(ValidationError):
            self._create_orderpoint(
                self.product_loratadina,
                min_qty=-5.0,
                max_qty=20.0,
                qty_multiple=5.0,
            )

        # Múltiplo cero o negativo
        with self.assertRaises(ValidationError):
            self._create_orderpoint(
                self.product_loratadina,
                min_qty=10.0,
                max_qty=20.0,
                qty_multiple=0.0,
            )

    def test_security_cashier_cannot_manage_rules(self):
        """Verificar que un usuario Cajero no puede crear ni modificar reglas de reorden."""
        with self.assertRaises(AccessError):
            self.env["stock.warehouse.orderpoint"].with_user(self.user_cashier).create(
                {
                    "name": "Regla No Autorizada Cajero",
                    "product_id": self.product_loratadina.id,
                    "location_id": self.stock_location.id,
                    "product_min_qty": 5.0,
                    "product_max_qty": 15.0,
                }
            )

    def test_location_context_isolation(self):
        """Verificar que el stock en ubicaciones secundarias (merma/dañados) no afecte el reorden de mostrador."""
        # 10 unidades en ubicación secundaria (bodega secundaria), 0 unidades en Mostrador (WH/Stock)
        self._set_stock(self.product_loratadina, self.secondary_location, 10.0)

        op_stock = self._create_orderpoint(
            self.product_loratadina,
            min_qty=10.0,
            max_qty=30.0,
            qty_multiple=1.0,
            location=self.stock_location,
        )

        # El stock en WH/Stock es 0 -> debe sugerir 30, no verse reducido por las 10 unidades de merma
        self.assertEqual(
            op_stock.suggested_replenishment_qty,
            30.0,
            "El cálculo debe evaluar únicamente el stock de la ubicación especificada en la regla.",
        )

    def test_product_template_orderpoint_sync(self):
        """Verificar que la pestaña de reglas en la plantilla del producto refleja los orderpoints."""
        op = self._create_orderpoint(
            self.product_loratadina,
            min_qty=12.0,
            max_qty=40.0,
            qty_multiple=2.0,
        )

        template = self.product_loratadina.product_tmpl_id
        self.assertIn(op, template.orderpoint_ids, "La regla de reorden debe sincronizarse en la plantilla del medicamento.")
