# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestStockPickingReception(TransactionCase):

    def setUp(self):
        super().setUp()
        self.laboratorio = self.env["res.partner"].create(
            {
                "name": "Laboratorios Vijosa",
                "is_company": True,
                "is_pharmacy_vendor": True,
                "vendor_type": "laboratorio",
                "nit": "0614-123456-001-2",
                "nrc": "12345-6",
            }
        )
        self.vendedor = self.env["res.partner"].create(
            {
                "name": "Carlos Méndez",
                "is_pharmacy_vendor": True,
                "parent_id": self.laboratorio.id,
            }
        )
        self.producto = self.env["product.product"].create(
            {
                "name": "Ibuprofeno 400mg",
                "purchase_method": "purchase",
                "type": "product",
                "tracking": "lot",
            }
        )

    def _crear_orden_confirmada(self, qty=15, price=1.0):
        orden = self.env["purchase.order"].create(
            {
                "partner_id": self.vendedor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.producto.id,
                            "name": self.producto.name,
                            "product_qty": qty,
                            "price_unit": price,
                        },
                    )
                ],
            }
        )
        orden.button_confirm()
        return orden

    # Escenario 2 (SPEC-8.2.1): bloquea la validación si no se asigna número de lote.
    def test_bloqueo_recepcion_sin_lote(self):
        orden = self._crear_orden_confirmada()
        picking = orden.picking_ids[0]
        picking.move_line_ids.write({"quantity": 15})
        with self.assertRaises(ValidationError):
            picking.button_validate()

    # Escenario 1 (SPEC-8.2.1): recepción exitosa con lote y fecha de vencimiento válida.
    def test_recepcion_exitosa_con_lote_y_vencimiento(self):
        orden = self._crear_orden_confirmada()
        picking = orden.picking_ids[0]
        picking.move_line_ids.write(
            {
                "quantity": 15,
                "lot_name": "LOT-IBU-2027-01",
                "expiration_date": "2027-08-31",
            }
        )
        picking.button_validate()
        self.assertEqual(picking.state, "done")

    # Bloquea si hay lote pero no fecha de vencimiento.
    def test_bloqueo_recepcion_sin_fecha_vencimiento(self):
        orden = self._crear_orden_confirmada()
        picking = orden.picking_ids[0]
        picking.move_line_ids.write(
            {
                "quantity": 15,
                "lot_name": "LOT-IBU-2027-01",
            }
        )
        with self.assertRaises(ValidationError):
            picking.button_validate()

    # Bloquea si la fecha de vencimiento ya está caducada.
    def test_bloqueo_recepcion_lote_caducado(self):
        orden = self._crear_orden_confirmada()
        picking = orden.picking_ids[0]
        picking.move_line_ids.write(
            {
                "quantity": 15,
                "lot_name": "LOT-VIEJO",
                "expiration_date": "2000-01-01",
            }
        )
        with self.assertRaises(ValidationError):
            picking.button_validate()

    # SPEC-8.2.2: al recibir todo lo pedido, la Orden de Compra se bloquea (Lock / estado done).
    def test_recepcion_completa_bloquea_orden_de_compra(self):
        orden = self._crear_orden_confirmada(qty=15)
        picking = orden.picking_ids[0]
        picking.move_line_ids.write(
            {
                "quantity": 15,
                "lot_name": "LOT-IBU-2027-01",
                "expiration_date": "2027-08-31",
            }
        )
        picking.button_validate()
        self.assertEqual(orden.state, "done")
        self.assertEqual(orden.order_line[0].qty_received, 15)

    # SPEC-8.2.3: recepción parcial deja la orden en 'purchase' (no bloqueada) y marca discrepancia.
    def test_recepcion_parcial_marca_discrepancia_y_no_bloquea_orden(self):
        orden = self._crear_orden_confirmada(qty=30)
        picking = orden.picking_ids[0]
        picking.move_line_ids.write(
            {
                "quantity": 20,
                "lot_name": "LOT-PARCIAL",
                "expiration_date": "2027-08-31",
            }
        )
        picking.with_context(skip_backorder=True, picking_ids_not_to_backorder=picking.ids).button_validate()
        self.assertEqual(picking.state, "done")
        self.assertTrue(picking.has_discrepancy)
        self.assertEqual(orden.state, "purchase")
        self.assertEqual(orden.order_line[0].qty_received, 20)
