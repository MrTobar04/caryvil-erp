# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPurchaseInventoryFlow(TransactionCase):

    def setUp(self):
        super().setUp()

        # Proveedor / Laboratorio de prueba
        self.laboratorio = self.env["res.partner"].create(
            {
                "name": "Laboratorios Vijosa Test",
                "is_company": True,
                "is_pharmacy_vendor": True,
                "vendor_type": "laboratorio",
                "nit": "0614-123456-001-2",
                "nrc": "12345-6",
            }
        )

        self.vendedor = self.env["res.partner"].create(
            {
                "name": "Carlos Méndez Test",
                "is_pharmacy_vendor": True,
                "parent_id": self.laboratorio.id,
            }
        )

        # Medicamento de prueba base
        self.medicine = self.env["product.product"].create(
            {
                "name": "Amoxicilina Test 500mg",
                "detailed_type": "product",
                "tracking": "lot",
                "standard_price": 4.00,
                "list_price": 6.00,
            }
        )

        # Unidades de medida para prueba de conversión (Caja x 100 -> Pastilla)
        self.unit = self.env.ref("caryvil_erp.uom_unit_pill")
        self.box100 = self.env.ref("caryvil_erp.uom_box_100")

    def test_full_purchase_to_stock_flow(self):
        """Test 1: PO creation -> Confirmation -> Reception picking with Lot & Expiration Date -> Stock increase."""
        # 1. Crear Orden de Compra por 10 unidades
        po = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.medicine.id,
                            "name": self.medicine.name,
                            "product_qty": 10.0,
                            "price_unit": 4.00,
                            "date_planned": fields.Datetime.now(),
                        },
                    )
                ],
            }
        )
        po.button_confirm()
        self.assertEqual(po.state, "purchase", "La Orden de Compra debe cambiar a estado 'purchase'.")

        # 2. Procesar Albarán de Recepción
        self.assertTrue(po.picking_ids, "La confirmación de la PO debe haber generado un albarán de recepción.")
        picking = po.picking_ids[0]
        self.assertEqual(picking.state, "assigned", "El albarán debe estar en estado 'assigned'.")

        exp_date = fields.Datetime.now() + timedelta(days=365)
        for move in picking.move_ids:
            for move_line in move.move_line_ids:
                move_line.write(
                    {
                        "quantity": 10.0,
                        "lot_name": "LOT-TEST-2027",
                        "expiration_date": exp_date,
                    }
                )

        picking.button_validate()
        self.assertEqual(picking.state, "done", "El albarán debe pasar a estado 'done'.")

        # 3. Validar Incremento de Existencias
        self.medicine.invalidate_recordset()
        self.assertEqual(
            self.medicine.qty_available,
            10.0,
            "El inventario del medicamento debe registrar exactamente 10 unidades.",
        )

        # 4. Validar Registro de Lote
        lot = self.env["stock.lot"].search(
            [("name", "=", "LOT-TEST-2027"), ("product_id", "=", self.medicine.id)],
            limit=1,
        )
        self.assertTrue(lot.exists(), "El lote 'LOT-TEST-2027' debe existir en el sistema.")
        self.assertFalse(lot.is_expired, "El lote con fecha futura no debe marcarse como vencido.")

        # Verificar balance en stock.quant para este lote
        stock_location = picking.location_dest_id
        quant = self.env["stock.quant"].search(
            [
                ("lot_id", "=", lot.id),
                ("location_id", "=", stock_location.id),
            ],
            limit=1,
        )
        self.assertTrue(quant, "Debe existir un registro de quant para el lote en la ubicación de destino.")
        self.assertEqual(quant.quantity, 10.0, "La cantidad del lote en el quant debe ser 10.0.")

    def test_lot_expiration_capture_required(self):
        """Test 2: Validation attempt without lot or with expired date raises ValidationError."""
        # Escenario A: Bloqueo por falta de lote
        po_no_lot = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.medicine.id,
                            "name": self.medicine.name,
                            "product_qty": 5.0,
                            "price_unit": 4.00,
                        },
                    )
                ],
            }
        )
        po_no_lot.button_confirm()
        picking_no_lot = po_no_lot.picking_ids[0]
        picking_no_lot.move_line_ids.write({"quantity": 5.0})  # Sin asignar lot_name

        with self.assertRaises(
            ValidationError,
            msg="Validar una recepción de medicamento sin lote debe lanzar ValidationError.",
        ):
            picking_no_lot.button_validate()

        # Escenario B: Bloqueo por lote vencido
        po_expired = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.medicine.id,
                            "name": self.medicine.name,
                            "product_qty": 5.0,
                            "price_unit": 4.00,
                        },
                    )
                ],
            }
        )
        po_expired.button_confirm()
        picking_expired = po_expired.picking_ids[0]
        past_date = fields.Datetime.now() - timedelta(days=10)
        picking_expired.move_line_ids.write(
            {
                "quantity": 5.0,
                "lot_name": "LOT-EXPIRED-TEST",
                "expiration_date": past_date,
            }
        )

        with self.assertRaises(
            ValidationError,
            msg="Validar una recepción con fecha de vencimiento caducada debe lanzar ValidationError.",
        ):
            picking_expired.button_validate()

    def test_partial_delivery_backorder_creation(self):
        """Test 3: Partial delivery reception -> Backorder creation -> Remaining state verification."""
        po = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.medicine.id,
                            "name": self.medicine.name,
                            "product_qty": 20.0,
                            "price_unit": 4.00,
                        },
                    )
                ],
            }
        )
        po.button_confirm()
        picking_initial = po.picking_ids[0]

        # Recibir solo 12 de las 20 unidades
        exp_date = fields.Datetime.now() + timedelta(days=365)
        for move_line in picking_initial.move_line_ids:
            move_line.write(
                {
                    "quantity": 12.0,
                    "lot_name": "LOT-PARTIAL-2027",
                    "expiration_date": exp_date,
                }
            )

        res = picking_initial.button_validate()

        # Si el flujo de Odoo abre el wizard de backorder, procesarlo
        if isinstance(res, dict) and res.get("res_model") == "stock.backorder.confirmation":
            backorder_wizard = (
                self.env["stock.backorder.confirmation"]
                .with_context(res.get("context", {}))
                .create({"pick_ids": [(4, picking_initial.id)]})
            )
            backorder_wizard.process()

        self.assertEqual(
            picking_initial.state,
            "done",
            "El albarán de entrega parcial debe pasar a estado 'done'.",
        )
        self.assertEqual(
            po.order_line[0].qty_received,
            12.0,
            "La cantidad recibida en la línea de PO debe ser 12.0.",
        )
        self.assertEqual(
            po.state,
            "purchase",
            "La Orden de Compra debe permanecer en estado 'purchase' al haber entregas pendientes.",
        )

        # Verificar creación y estado del backorder
        backorders = po.picking_ids.filtered(lambda p: p.id != picking_initial.id)
        self.assertTrue(backorders, "Debe haberse creado un albarán de backorder para las unidades pendientes.")
        backorder = backorders[0]
        self.assertIn(
            backorder.state,
            ["assigned", "confirmed", "waiting"],
            "El backorder debe estar pendiente de procesamiento.",
        )
        self.assertEqual(
            backorder.move_ids[0].product_uom_qty,
            8.0,
            "El remanente en el backorder debe ser 8.0 unidades.",
        )

    def test_uom_box_to_unit_conversion(self):
        """Test 4: Purchase in Box x 100 presentation -> Stock increases by 100 base units."""
        dual_uom_medicine = self.env["product.product"].create(
            {
                "name": "Paracetamol Test 500mg Dual UoM",
                "detailed_type": "product",
                "tracking": "lot",
                "uom_id": self.unit.id,
                "uom_po_id": self.box100.id,
                "standard_price": 40.00,
                "list_price": 0.50,
            }
        )

        po = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": dual_uom_medicine.id,
                            "name": dual_uom_medicine.name,
                            "product_qty": 1.0,  # 1 Caja x 100
                            "product_uom": self.box100.id,
                            "price_unit": 40.00,
                        },
                    )
                ],
            }
        )
        po.button_confirm()
        picking = po.picking_ids[0]

        # Verificar conversión en el movimiento de stock (1 Caja x 100 -> 100 Unidades base)
        stock_move = picking.move_ids[0]
        self.assertEqual(
            stock_move.product_uom,
            self.unit,
            "El movimiento de stock debe convertirse a la unidad base de inventario (pastilla).",
        )
        self.assertEqual(
            stock_move.product_uom_qty,
            100.0,
            "La cantidad en el movimiento de stock debe ser 100 unidades base.",
        )

        exp_date = fields.Datetime.now() + timedelta(days=730)
        for move_line in picking.move_line_ids:
            move_line.write(
                {
                    "quantity": 100.0,
                    "lot_name": "LOT-BOX100-2028",
                    "expiration_date": exp_date,
                }
            )

        picking.button_validate()
        self.assertEqual(picking.state, "done")

        # Verificar que el inventario se haya incrementado en 100 unidades base
        dual_uom_medicine.invalidate_recordset()
        self.assertEqual(
            dual_uom_medicine.qty_available,
            100.0,
            "El stock disponible del medicamento debe ser exactamente 100 unidades base.",
        )
